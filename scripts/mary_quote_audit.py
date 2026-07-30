# -*- coding: utf-8 -*-
"""Audit the pricing documents Fenster ITSELF sent, for arithmetic that is wrong.

Zac, dashmsg-97: "look through old projects for work that we ourselves have
quoted, check they have no mistakes, tell us if they do."

This is deliberately NOT the engine's job. mary_backtest asks "would Mary have
said the same number"; a disagreement there is usually the engine being wrong.
This asks a question with no opinion in it: does the document agree with
ITSELF, and with the supplier quote it was built from? Every finding here is
arithmetic, so a failure is an error in OUR document, not a lab finding - and
errors go to Adam.

Four checks, in order of how sure we can be:

  FOOT_LINE      Total = Unit Rate x Qty, on every priced row.
  FOOT_DOC       TOTAL* = sum of the line totals + installation.
  BUILDUP        Unit Rate = Frames + Glass + Additional + CW, where the
                 document shows those components.
  SUPPLIER       Sum of Frames x Qty = the "Supplier used:" cost in the header.
                 This is the one that catches a discount applied twice, or not
                 at all: a 15% trade discount taken a second time shows up here
                 as the frames total sitting at 0.85 of the stated buy.

Column positions are read off the header row, not hard-coded, because the
documents are template clones of different vintages and the components drift a
column either way.

  python scripts/mary_quote_audit.py            # every sent document
  python scripts/mary_quote_audit.py <file>     # one document
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_calibrate as cal
import mary_pricing as engine
import mary_quote_reader as reader


def is_marked_do_not_send(name):
    """The estimator's own labelling. NOT proof either way - it is a filename
    convention, and the only real proof a quote left the building is the sent
    folder (scripts/quote_send_dates.py). But it is the right first sort: an
    error in a document marked DO NOT SEND is an internal working, and an error
    in one that is not so marked may be sitting with a client."""
    return "do not send" in name.lower()

SIZE_RE = re.compile(r"(\d{3,5})\s*[xX*]\s*(\d{3,5})")

# Money is written to the penny, so a real slip is pounds. Anything under this
# is a rounding artefact of the spreadsheet and not worth Adam's morning.
PENCE = 0.02
# Proportional tolerance for the supplier reconciliation, which legitimately
# carries carriage, small extras and part-quantities.
SUPPLIER_TOL = 0.005

# Labels that appear in the 'Supplier used:' column but are not suppliers: the
# priced-row column headers sit inside the block's six-row window and one of
# them lands in the cell straight after 'Supplier used:'.
_NOT_A_SUPPLIER = ("frames", "glass", "additional", "cw", "cw labour", "cw sqm",
                   "unit rate", "total", "qty", "unit", "description", "size",
                   "product codes")

# A GLASS MERCHANT IN THE BLOCK MEANS THE GLASS COLUMN IS IN THE BUY (31/07).
# The supply build-up of a priced row is frames + glass + additional, and the
# 'Supplier used:' block is a list of who supplied what. Where the list is a
# frame supplier alone, the figure it totals is the Frames column and the check
# reconciles perfectly - 22 documents, median |ratio - 1| of 0.006. Where it
# also names a GLASS merchant, the figure covers Frames AND Glass, and checking
# it against Frames alone manufactures a gap of a quarter of the buy:
#
#     Trafalgar House   TruFrame / Vetroseal / Ikon    0.657 -> 0.919
#     Brandon, COMAR    4Ali / Vetroseal               0.823 -> 0.991
#     Brandon, Elkins   4Ali / Vetroseal               0.823 -> 1.006
#     Brandon, earlier  BSW / Vetroseal                4.094 -> 5.171  (still open)
#
# Median |ratio - 1| over those four: 0.260 against Frames, 0.045 against
# Frames+Glass. And the rule discriminates BOTH ways - on the 22 documents with
# no glass merchant, adding the Glass column would move a median 0.006 out to
# 0.074, so this is not "always use the whole build-up". It is: reconcile
# against the columns the NAMED suppliers actually supply.
#
# A NAMED LIST, NOT A KEYWORD MATCH, and deliberately so. 'glass' and 'glaz'
# appear in Fenster Glazing's own name and in half the client names in this
# archive, so a substring test would put the Glass column into every buy in the
# corpus. Extend this list when a new glass merchant appears in a block; the
# cost of a name missing from it is a false alarm of exactly the kind this
# check already exists to kill.
GLASS_SUPPLIERS = ("vetroseal", "tufwell", "romag", "pilkington", "saint gobain",
                   "saint-gobain", "guardian glass", "cantifix")


def _supplies_glass(names):
    low = [str(n).lower() for n in (names or [])]
    return [n for n in low if any(g in n for g in GLASS_SUPPLIERS)]


def _num(c):
    return float(c) if isinstance(c, (int, float)) and not isinstance(c, bool) else None


def _txt(c):
    return str(c).strip().lower() if isinstance(c, str) else ""


def read_doc(path):
    """Pull the priced rows AND the column map out of a pricing document."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return None
    doc = {"file": os.path.basename(path), "path": path, "rows": [], "installation": None,
           "total": None, "supplier": None, "supplier_cost": None, "cols": {}, "total_row": None,
           "extras": [], "optional_from": None, "_sup_vals": [], "_sup_row": None,
           "_sup_col": 0, "supplier_n": 0, "_sup_done": False, "supplier_names": []}
    try:
        sheets = [w for w in wb.worksheets
                  if w.title.strip().lower().startswith("pricing document")]
        if not sheets:
            return None
        ws = sheets[0]
        cols = {}
        for rn, row in enumerate(ws.iter_rows(values_only=True), 1):
            cells = list(row) + [None] * (20 - len(row))
            texts = [_txt(c) for c in cells]

            # 'Supplier used:' heads a small TABLE, not a single figure - one
            # row per supplier and a total underneath. Gordon Court reads
            # BSW 182,787.76 / Aluminium Fire Systems 18,298.94 / 201,086.70,
            # and its Frames column totals 201,086.70 exactly. Reading only the
            # first row made that perfect reconciliation look 18,298.94 out -
            # the residual was simply the second supplier.
            for i, t in enumerate(texts):
                if t.startswith("supplier used"):
                    doc["_sup_col"] = i
                    doc["_sup_row"] = rn
                    after = [c for c in cells[i + 1:]
                             if c is not None and str(c).strip() not in ("", "None")]
                    if after and isinstance(after[0], str):
                        doc["supplier"] = after[0].strip()
            # THE BLOCK ENDS AT THE PRICED-ROW HEADER, and that is a fact about
            # the template rather than a tolerance (31/07, fourth run). The two
            # softer rules below - stop at the first empty row, and require the
            # row to LOOK like a supplier row - both failed on the earlier
            # Brandon Estate revision, which is where the 4.094 came from. That
            # document NAMES BSW and Vetroseal and never types a cost against
            # either, so the block never hits an empty row; and its first priced
            # row has an EMPTY Additional cell, which is the one thing
            # looks_like() relies on to recognise a priced row. The window then
            # ran six rows past the names into row 9 and took 362,678.40 from
            # column 15 - a spare working cell holding that row's own
            # (frames + glass) x qty, 863.52 x 420 to the penny. GBP 1.12m of
            # reported gap on a GBP 3.17m document, all of it manufactured.
            # The header row carries 'Qty' and 'Unit Rate' and every supplier
            # block in the archive sits above it, so nothing at or below it can
            # be part of the buy. This subsumes the empty-row rule; both are
            # kept, because a block that ends early should still end early.
            if any(t in ("qty", "quantity") for t in texts) \
                    and any(t.replace(" ", "") == "unitrate" for t in texts):
                doc["_sup_done"] = True
            if (doc.get("_sup_row") and not doc.get("_sup_done")
                    and doc["_sup_row"] <= rn <= doc["_sup_row"] + 6):
                i = doc["_sup_col"]
                money = [m for m in (_num(c) for c in cells[i + 1:]) if m and m > 1]
                # AND the row has to LOOK like a supplier row. The stop-at-first-
                # empty-row rule is not enough on its own: Zelltec Crownhill
                # lists three suppliers with NO costs against them, so the block
                # never hits an empty row before the window runs out and the
                # first priced row's Additional cell got read as the buy. Hence
                # ratios of 8.268 and 22.139 on two Zelltec documents.
                # A supplier row carries a NAME in the column straight after
                # 'Supplier used:' (BSW, Aluminium Fire Systems, Teleflex); the
                # block's total row leaves that cell empty and puts the figure
                # further right. A PRICED row has a number there - that is its
                # Additional column - so requiring a name-or-empty excludes it.
                label = cells[i + 1] if len(cells) > i + 1 else None
                # RECORD THE NAME EVEN WHERE IT CARRIES NO FIGURE. A block can
                # name several suppliers and total them ONCE underneath -
                # Trafalgar House is TruFrame / Vetroseal / Ikon and then a
                # single 25,206.56 - and until now those three names were
                # dropped on the floor, because a row with no money and nothing
                # yet collected falls through both branches below. The names are
                # what say WHICH supply columns the figure covers. Column
                # headers sit inside the six-row window and one of them lands in
                # this very cell, so they are excluded by name.
                if isinstance(label, str) and label.strip() \
                        and label.strip().lower() not in _NOT_A_SUPPLIER \
                        and label.strip() not in doc["supplier_names"]:
                    doc["supplier_names"].append(label.strip())
                looks_like = isinstance(label, str) and label.strip() != "" \
                    or label is None or str(label).strip() == ""
                if money and looks_like:
                    doc["_sup_vals"].append(
                        (rn, str(label).strip() if isinstance(label, str) else "", max(money)))
                elif doc["_sup_vals"]:
                    doc["_sup_done"] = True

            # Header rows: Qty / Unit Rate / Total on one, components below.
            for i, t in enumerate(texts):
                if t in ("qty", "quantity"):
                    cols["qty"] = i
                elif t.replace(" ", "") == "unitrate":
                    cols["unit_rate"] = i
                elif t == "total" and "qty" in cols and "unit_rate" in cols \
                        and "line_total" not in cols:
                    cols["line_total"] = i
                elif t == "frames":
                    cols["frames"] = i
                elif t == "glass":
                    cols["glass"] = i
                elif t.startswith("additional"):
                    cols["additional"] = i
                elif t == "cw":
                    cols["cw"] = i
                # CW LABOUR is what tells a GENUINE curtain-walling row from an
                # ordinary window row carrying a CW working figure (31/07).
                # Checked before 'cw' would swallow it - startswith, because the
                # header is written 'CW LABOUR' with a trailing space in places.
                elif t.startswith("cw labour"):
                    cols["cw_labour"] = i
                elif t == "description":
                    cols["desc"] = i

            # Everything below the priced lines and above TOTAL* is an addendum
            # row - INSTALLATION, EXTERNAL MASTIC, TELEFLEX - and every one of
            # them counts. The first run of this audit knew only about
            # INSTALLATION and so reported Crestwood Park 17,779.06 out and
            # Wisley 1,419.00 out; both were the addendum row it had not read,
            # to the penny, and both documents foot perfectly.
            # The OPTIONAL heading is a hard stop. What sits under it - EPDM,
            # sometimes a second mastic - is deliberately EXCLUDED from TOTAL*,
            # so counting it would invent an error rather than find one.
            # startswith, not equality: Brandon Estate heads the block
            # 'OPTIONAL EXTRAS' and all three Brandon documents were reported
            # as failing to foot by exactly their mastic + EDPM as a result.
            if any(t.startswith("optional") for t in texts):
                doc["optional_from"] = rn
                continue
            if any(t.startswith("total") and t != "total" for t in texts) and doc["total"] is None:
                vals = [n for n in (_num(c) for c in cells) if n]
                if vals:
                    doc["total"] = max(vals)
                    doc["total_row"] = rn
                continue
            if "qty" not in cols or "unit_rate" not in cols:
                continue
            qty = _num(cells[cols["qty"]])
            unit_rate = _num(cells[cols["unit_rate"]])

            # An addendum row has NO quantity - it is a lump. Require a real
            # word as its label: the working columns to the right carry column
            # sums and cached '#VALUE!' errors, and both were being read as
            # addenda. SUBTOTAL is excluded because it aggregates rows already
            # counted, so adding it doubles them.
            if qty is None or unit_rate is None:
                label = next((str(c).strip() for c in cells
                              if isinstance(c, str) and str(c).strip()
                              and not SIZE_RE.search(str(c))), "")
                # The money must sit in a MONEY column. ASHE - CDC heads its
                # door block with a row reading 'Doors' and a stray 1 in the
                # Qty column, and reading that as a 1.00 addendum made a
                # document that foots perfectly look 1.00 out - in both copies.
                vals = [n for n in (_num(c) if i >= cols.get("unit_rate", 0) else None
                                    for i, c in enumerate(cells)) if n]
                # Two rules learned the hard way, both from false alarms:
                # do NOT require upper case (Crestwood writes 'TELEFLEX' and
                # Feltham 'Teleflex ' for the same 8,920.00 line), and do NOT
                # require the label to be letters-only - Coventry's addenda are
                # 'Aluminium  Fascias, Canopy' and 'FASCIA/SOFFIT INSTALLATION',
                # and a comma and a slash were enough to hide 39,349.26 of
                # perfectly good money and report the document as not footing.
                # What must be excluded is the cached '#VALUE!' of a broken
                # working column, and SUBTOTAL, which re-counts rows already in.
                letters = sum(c.isalpha() for c in label)
                if (label and vals and doc["rows"] and letters >= 3
                        and not label.startswith("#") and len(label) < 200
                        and "subtotal" not in label.lower()):
                    entry = {"row": rn, "label": label.strip(), "value": max(vals),
                             "optional": doc.get("optional_from") is not None}
                    doc["extras"].append(entry)
                    if label.strip().lower() == "installation" and not entry["optional"]:
                        doc["installation"] = max(vals)
                    continue
                # NOT an addendum and not priced: it is a SECTION HEADING, and it
                # is what makes the supplier check able to say WHERE a gap is.
                # A document is organised in blocks under a heading naming the
                # system - 'SMA Smart Wall Doors', then 'Sheerline Aluminium
                # Windows' - and the 'Supplier used:' table above is one row per
                # supplier. The two line up: Brocks Hill's Sheerline block totals
                # 37,960.33 and its second supplier figure IS 37,960.33.
                d = cols.get("desc")
                head = str(cells[d]).strip() if d is not None and isinstance(cells[d], str) else ""
                if head and not SIZE_RE.search(head) and sum(c.isalpha() for c in head) >= 4 \
                        and not head.lower().startswith(
                            ("client", "project", "site", "date", "description", "product",
                             "total", "installation", "*", "optional")):
                    doc["heading"] = head
                continue

            # A PRICED row is one with a quantity and a rate. It does NOT need a
            # product code: Fortis Vision's 'Sliding door automation' at 4,490
            # carries no code, and dropping it made a document that foots
            # perfectly look 13,181.53 out. Code-less rows are still audited for
            # footing; only BUILDUP, which needs a code to know the adder,
            # skips them.
            code = str(cells[1]).strip().upper() if isinstance(cells[1], str) else ""
            if not code or len(code) > 6 or not code.isalpha() or code not in engine.CODE_VALUE:
                code = ""
            size = next((str(c) for c in cells if isinstance(c, str) and SIZE_RE.search(str(c))), "")
            m = SIZE_RE.search(size)
            area = round(int(m.group(1)) / 1000.0 * int(m.group(2)) / 1000.0, 4) if m else None
            doc["rows"].append({
                "row": rn, "code": code, "heading": doc.get("heading", ""),
                "desc": str(cells[2] or "").strip()[:40],
                "size": size, "area": area, "qty": qty, "unit_rate": unit_rate,
                "line_total": _num(cells[cols["line_total"]]) if "line_total" in cols else None,
                "frames": _num(cells[cols["frames"]]) if "frames" in cols else None,
                "glass": _num(cells[cols["glass"]]) if "glass" in cols else None,
                "additional": _num(cells[cols["additional"]]) if "additional" in cols else None,
                "cw": _num(cells[cols["cw"]]) if "cw" in cols else None,
                "cw_labour": _num(cells[cols["cw_labour"]]) if "cw_labour" in cols else None,
            })
        doc["cols"] = cols
        # Resolve the supplier block: if the last figure equals the sum of the
        # ones above it, that is the block's own total and the rest are its
        # parts. Otherwise take the sum, which is the same answer when there is
        # only one supplier.
        vals = [v for _, _, v in doc["_sup_vals"]]
        labels = [lb for _, lb, _ in doc["_sup_vals"]]
        if vals:
            parts, last = vals[:-1], vals[-1]
            if parts and abs(sum(parts) - last) <= 0.02:
                doc["supplier_cost"] = last
                doc["supplier_n"] = len(parts)
                # Keep the PARTS, not just the total. Not every supplier in the
                # block is a frame supplier - see the SUPPLIER check.
                doc["supplier_parts"] = list(zip(labels[:-1], parts))
            else:
                doc["supplier_cost"] = sum(vals)
                doc["supplier_n"] = len(vals)
                doc["supplier_parts"] = list(zip(labels, vals))
    finally:
        wb.close()
    return doc if doc["rows"] else None


def audit(doc):
    """Return a list of findings. Each one is money, a row, and a reason."""
    out = []

    # 1. Every line must multiply out.
    for r in doc["rows"]:
        if r["line_total"] is None:
            continue
        expect = r["unit_rate"] * r["qty"]
        if abs(expect - r["line_total"]) > max(PENCE, abs(expect) * 1e-6):
            out.append({
                "check": "FOOT_LINE", "row": r["row"], "code": r["code"],
                "money": round(r["line_total"] - expect, 2),
                "detail": "row %d %s %s: %.2f x %g = %.2f, document says %.2f"
                          % (r["row"], r["code"], r["size"], r["unit_rate"], r["qty"],
                             expect, r["line_total"])})

    # 2. The document must foot to its own TOTAL.
    line_sum = sum((r["line_total"] if r["line_total"] is not None
                    else r["unit_rate"] * r["qty"]) for r in doc["rows"])
    counted = [e for e in doc["extras"] if not e["optional"]]
    if doc["total"] is not None:
        expect = line_sum + sum(e["value"] for e in counted)
        gap = doc["total"] - expect
        if abs(gap) > max(PENCE, abs(expect) * 1e-6):
            # A shortfall that is a clean percentage of the sum is a discount
            # taken at the total, not a miscast, and saying "this does not
            # foot" would be wrong. THIS CHECK CURRENTLY FIRES ON NOTHING, and
            # that is the right answer: it was written because Princess
            # Beatrice House appeared to be short by exactly 2.500%, and the
            # truth was that the document has a '2.5% MCD Discount' row saying
            # so in full, which an over-strict label filter had hidden. The
            # lesson is worth more than the check - a gap that lands on a
            # suspiciously round percentage is far more likely to be a row you
            # failed to read than a discount somebody failed to write down.
            # Look for the row before believing the inference.
            pct = -gap / expect * 100.0 if expect else 0.0
            named = next((p for p in (2.5, 3.0, 5.0, 7.5, 10.0, 15.0)
                          if abs(pct - p) < 0.01), None)
            already = [e for e in counted if "discount" in e["label"].lower()]
            if named and not already:
                out.append({
                    "check": "DISCOUNT", "row": doc["total_row"], "code": "",
                    "money": round(gap, 2),
                    "detail": "TOTAL is %.3f%% below the sum of its own parts (%.2f vs %.2f) - "
                              "an unwritten %.1f%% discount, taken once, with no row saying so"
                              % (pct, doc["total"], expect, named)})
            else:
                out.append({
                    "check": "FOOT_DOC", "row": doc["total_row"], "code": "",
                    "money": round(gap, 2),
                    "detail": "lines %.2f + %s = %.2f, TOTAL says %.2f"
                              % (line_sum,
                                 " + ".join("%s %.2f" % (e["label"], e["value"])
                                            for e in counted) or "no addenda",
                                 expect, doc["total"])})

    # 3. The unit rate must equal the components the document itself shows,
    #    PLUS the template's code adder - which is not written in any column, so
    #    a naive components-only check fires on every line in the archive. The
    #    first run of this audit did exactly that: 513 findings, all of them the
    #    adder, none of them errors. What is left after the adder is modelled is
    #    money in the unit rate that the document does not explain.
    #
    #    CW IS NOT IN THE BUILD-UP OF A CODED UNIT LINE. It is a working column.
    #    Including it left 156 of 508 lines with components EXCEEDING their own
    #    unit rate, which the board had set aside as Brandon Estate being "not
    #    per-unit money". It is not a Brandon property. The header reads
    #    Frames | Glass | Additional | CW | CW LABOUR | CW SQM, and on every one
    #    of those 156 lines - all 156, without exception - the CW cell equals
    #    area x GBP 850.00, which is CW_SUPPLY_M2. It is the estimator asking
    #    "what would this opening cost as curtain walling instead", parked in a
    #    spare column. Oldswinford row 9 proves it on its face: Frames 1,003.70
    #    + Additional 210.00 + LAW adder 487.50 = 1,701.20, the unit rate to the
    #    penny, while the CW cell says 2,041.67 and CW SQM says 2.40.
    #    Dropping it takes reconciliation from 352/508 to 495/508.
    #    A GENUINE curtain-walling line is a different row: no product code, a
    #    CW LABOUR figure filled in, and Frames equal to the CW money (CB
    #    Refrigeration CWT-A, 17.69m2, 15,036.50 = 850 x 17.69 with labour
    #    2,653.50 = 150 x 17.69). Those rows have no code, so BUILDUP skips them
    #    anyway - which is why excluding CW here loses no coverage.
    comps = [c for c in ("frames", "glass", "additional") if c in doc["cols"]]
    if comps:
        for r in doc["rows"]:
            parts = [r[c] for c in comps if r[c] is not None]
            if not parts or r["frames"] is None or not r["code"]:
                continue
            #    0.75 FLAT, not engine.adder_factor(). The engine carries 1.25
            #    above 6m2 as an admitted fudge for money it does not model
            #    (30/07). This check asks what the DOCUMENT did, and the
            #    document uses 0.75 in every band - measured over 508 lines.
            #    Feeding an engine fudge into an arithmetic check invents
            #    findings on exactly the largest, dearest lines.
            adder = engine.CODE_VALUE.get(r["code"], 0) * engine.ADDER_FACTOR
            built = sum(parts) + adder
            gap = r["unit_rate"] - built
            if abs(gap) > max(PENCE, abs(r["unit_rate"]) * 1e-6):
                out.append({
                    "check": "BUILDUP", "row": r["row"], "code": r["code"],
                    "money": round(gap, 2),
                    "detail": "row %d %s %s: %s + adder %.2f = %.2f, unit rate says %.2f"
                              % (r["row"], r["code"], r["size"],
                                 " + ".join("%s %.2f" % (c, r[c]) for c in comps
                                            if r[c] is not None),
                                 adder, built, r["unit_rate"])})

    # 4. The frames must reconcile to the supplier quote the document names.
    #
    #    NOT EVERY SUPPLIER IN THE BLOCK IS A FRAME SUPPLIER, and this was the
    #    single biggest source of SUPPLIER noise. Crestwood Park heads its block
    #    BSW 27,329.60 / Teleflex 14,223.25 / total 41,552.85, and its Frames
    #    column totals 27,329.60 - the BSW figure EXACTLY. It was reported as
    #    -14,223.25 out at ratio 0.658, and that gap is the Teleflex line to the
    #    penny. Teleflex is not framing: it is a separate scope item that appears
    #    as an ADDENDUM ROW below the priced lines, which is the same Teleflex
    #    the footing checks already know about. Frames cannot contain it.
    #    So before reporting a gap, try the SUBSETS of the block. If the frames
    #    total matches any subset, the document reconciles and the suppliers left
    #    out are addendum suppliers - report nothing and say which matched.
    #    Only a frames total that matches NO subset is a real question.
    #
    #    AND THE BUY COVERS WHATEVER THE NAMED SUPPLIERS SUPPLY. If a glass
    #    merchant is in the block then Glass is in the figure, so the thing to
    #    reconcile is Frames + Glass. See GLASS_SUPPLIERS above for the evidence
    #    and for why this is a named list rather than a keyword match.
    #
    #    SO THERE ARE NOW TWO READINGS OF THE SAME BLOCK, AND THE CHECK OWES THE
    #    DOCUMENT BOTH. Trying Frames+Glass INSTEAD OF Frames, rather than as
    #    well as, took the finding count UP from 13 to 15: the two big Brandon
    #    revisions reconciled on a SUBSET of their block under Frames alone and
    #    stopped doing so under Frames+Glass. A document is not wrong because
    #    the first reading of its supplier block failed - it is wrong when NO
    #    reading works. Same principle as the subsets above, one level out:
    #    enumerate the readings, report only if every one of them fails, and
    #    quote the one that came closest.
    # A BLOCK THAT NAMES SUPPLIERS AND STATES NO COST IS ITS OWN FINDING, and
    # it is what is left of the Brandon Estate 4.094 once the reader stops
    # inventing a figure for it (31/07, fourth run). The old reader could never
    # report this, because whenever the block was blank it filled the gap from
    # whatever number the window happened to reach. It is NOT an arithmetic
    # error - nothing in the client's document is wrong and it foots - but it is
    # a control gap, and on the largest job in the archive: with no buy recorded
    # there is nothing to check the margin against, and SUPPLIER, SUP_DUP and
    # the whole-unit test are all silently skipped for that document. Reported
    # separately from SUPPLIER for exactly the reason the board keeps insisting
    # on: a missing figure and a wrong figure are different findings.
    if doc["supplier_names"] and not doc["supplier_cost"] \
            and any(r["frames"] is not None for r in doc["rows"]):
        frames_sum = sum(r["frames"] * r["qty"]
                         for r in doc["rows"] if r["frames"] is not None)
        out.append({"check": "SUP_BLANK", "money": frames_sum,
                    "detail": ("the block names %s and states NO cost against any of them, "
                               "so this document records no buy at all - the frames column "
                               "totals %.2f and nothing in the document says what it cost. "
                               "Not an arithmetic error; the margin on it cannot be checked"
                               % (" + ".join(doc["supplier_names"]), frames_sum))})

    if doc["supplier_cost"] and any(r["frames"] is not None for r in doc["rows"]):
        glass_names = _supplies_glass(doc.get("supplier_names"))
        doc["glass_in_buy"] = glass_names
        bases = [("frames", sum(r["frames"] * r["qty"]
                                for r in doc["rows"] if r["frames"] is not None))]
        if glass_names:
            bases.append(("frames+glass",
                          sum((r["frames"] + (r["glass"] or 0.0)) * r["qty"]
                              for r in doc["rows"] if r["frames"] is not None)))
        full = doc["supplier_cost"]
        allparts = doc.get("supplier_parts") or []

        def _reconciles(total):
            """Does this supply total match the block, or any subset of it?"""
            if abs(total - full) <= max(1.0, full * SUPPLIER_TOL):
                return full, None
            best = None
            for mask in range(1, 1 << min(len(allparts), 8)):
                sub = [allparts[b] for b in range(min(len(allparts), 8)) if mask >> b & 1]
                tot = sum(v for _, v in sub)
                if tot and abs(total - tot) <= max(1.0, tot * SUPPLIER_TOL):
                    if best is None or len(sub) > len(best[1]):
                        best = (tot, sub)
            return best if best else (None, None)

        chosen = None
        for label, total in bases:
            cost, sub = _reconciles(total)
            if cost is not None:
                chosen = (label, total, cost, sub, True)
                break
        if chosen is None:
            # Nothing reconciles. Quote the reading that came closest to 1.00,
            # because that is the one a human should argue with.
            label, total = min(bases, key=lambda b: abs(b[1] / full - 1.0) if full else 0)
            chosen = (label, total, full, None, False)
        base_label, frames_sum, doc["supplier_cost"], sub, ok = chosen
        if sub:
            doc["supplier_subset"] = sub
        # _reconciles() has already tried every subset of the block against every
        # reading, so `ok` is the whole answer and there is no second pass here.
        parts = allparts        # the block-localisation below still wants them
        gap = 0.0 if ok else frames_sum - doc["supplier_cost"]
        if abs(gap) > max(1.0, doc["supplier_cost"] * SUPPLIER_TOL):
            ratio = frames_sum / doc["supplier_cost"]
            note = ""
            for label, f in (("a 15% discount taken twice", 0.85),
                             ("a 15% discount not taken", 1.0 / 0.85),
                             ("a 10% discount taken twice", 0.90),
                             ("a 10% discount not taken", 1.0 / 0.90),
                             ("a 5% discount taken twice", 0.95)):
                if abs(ratio - f) < 0.01:
                    note = " - consistent with %s" % label
                    break
            # WHICH BLOCK IS THE GAP IN? A document-level gap says nothing about
            # where to look; a block-level one names the row. The document is
            # organised in blocks under a system heading and the 'Supplier used:'
            # table is one row per supplier, and they line up: Brocks Hill's
            # Sheerline block totals 37,960.33 against a second supplier figure of
            # 37,960.33 EXACTLY, so the whole of its 2,723.49 gap is in the Smart
            # Wall door block. Pair greedily, largest block first, and only report
            # the localisation when the per-block residuals add back to the
            # document gap - otherwise the pairing is a guess and says nothing.
            blocks = {}
            for r in doc["rows"]:
                if r.get("frames") is not None:
                    blocks.setdefault(r.get("heading") or "", []).append(r)
            local = None
            if len(blocks) > 1 and len(parts) > 1:
                free = list(parts)
                pairs = []
                for head, rs in sorted(blocks.items(),
                                       key=lambda kv: -sum(r["frames"] * r["qty"] for r in kv[1])):
                    tot = sum(r["frames"] * r["qty"] for r in rs)
                    best = None
                    for mask in range(1, 1 << min(len(free), 6)):
                        subset = [free[b] for b in range(min(len(free), 6)) if mask >> b & 1]
                        d = abs(tot - sum(v for _, v in subset))
                        if best is None or d < best[0]:
                            best = (d, subset)
                    if best is None:
                        continue
                    for s in best[1]:
                        free.remove(s)
                    pairs.append((head, rs, tot, sum(v for _, v in best[1]), best[1]))
                if pairs and abs(sum(t - s for _, _, t, s, _ in pairs) - gap) <= 0.05:
                    off = [p for p in pairs if abs(p[2] - p[3]) > 0.05]
                    if len(off) == 1 and len(pairs) > 1:
                        local = off[0]
                        note += (" - LOCALISED: %d of %d blocks reconcile to the penny and the "
                                 "whole gap is in '%s' (%s), which prices %.2f against %s %.2f"
                                 % (len(pairs) - 1, len(pairs), local[0][:40],
                                    ", ".join("row %s" % r["row"] for r in local[1][:6]),
                                    local[2], "+".join(lb or "?" for lb, _ in local[4]),
                                    local[3]))

            # IS THE GAP A WHOLE UNIT? This is the test that separates a real
            # catch from a rounding difference, and percentage cannot do it.
            # Grange Hill is a REAL error at ratio 1.018 - seven windows priced
            # where BSW quote eight, GBP 419.32 each - while six other findings
            # sit nearer 1.00 than that and mean nothing. What made Grange Hill
            # real is that its gap is an EXACT MULTIPLE of one line's unit frames
            # cost, which is what a missed or doubled opening looks like. An
            # arithmetic slip, a rounding, or a supplier revision does not land on
            # a multiple of a unit price.
            #
            # THE MATCH HAS TO BE EXACT, to a penny a unit. GBP 1 is far too
            # loose and lets a near-miss in: Princess Beatrice is 668.41 out
            # against a 668.94 unit, which is 53p adrift and therefore NOT a
            # whole unit, but a pound of slack reported it as one. A real missed
            # opening is exact, because it is the same cell multiplied.
            # Only k = 1..4, and never more than the line's own quantity + 1,
            # because "the gap is 19 of these" is a coincidence hunt.
            # Search the LOCALISED block's rows when there is one - the gap
            # cannot be a unit from a block that already reconciles.
            whole = []
            for r in (local[1] if local else doc["rows"]):
                if not r.get("frames"):
                    continue
                unit = r["frames"]
                if unit < 50:
                    continue
                k = round(abs(gap) / unit)
                if 1 <= k <= min(4, r["qty"] + 1) \
                        and abs(abs(gap) - k * unit) <= max(0.02, k * 0.01):
                    whole.append((k, unit, r))
            if whole:
                k, unit, r = min(whole, key=lambda w: w[0])
                note += (" - AND THE GAP IS %d x GBP %.2f EXACTLY, the unit frames cost of row %s "
                         "'%s' (qty %g): %s" % (
                             k, unit, r["row"], (r.get("desc") or "")[:26], r["qty"],
                             "the document prices %g of it where the supplier quotes %g"
                             % (r["qty"], r["qty"] + k) if gap < 0 else
                             "the document prices %g of it where the supplier quotes %g"
                             % (r["qty"], r["qty"] - k)))
            out.append({
                "check": "SUPPLIER", "row": None, "code": "",
                "money": round(gap, 2),
                "whole_unit": bool(whole),
                "detail": "%s total %.2f against %s buy %.2f, ratio %.3f%s"
                          % (base_label, frames_sum,
                             ("the block's %s" % " + ".join(doc["supplier_names"]))
                             if len(doc.get("supplier_names") or []) > 1
                             else "'%s'" % (doc["supplier"] or "?"),
                             doc["supplier_cost"], ratio, note)})
    return out


def cross_document(docs):
    """One check that cannot be done a document at a time: the SAME supplier cost
    figure appearing in two unrelated jobs.

    A pricing document is made by saving the last one under a new name, and the
    'Supplier used:' cell is typed in by hand, so it is the cell most likely to be
    left behind. Across 65 documents there is exactly ONE cross-client duplicate
    and it is real: GBP 31,335.40 sits in ASHE - CDC and in Zelltec's Wisley Golf
    Club, two unrelated jobs, and NEITHER document's Frames column reconciles to
    it - Wisley at ratio 1.538 and ASHE at 0.778, which the board had recorded as
    two separate open questions. They are one cause.

    Same client and same job is NOT a finding: the two Brandon Estate revisions
    share Vetroseal 679,820.32 and 4Ali 3,166,748.58 because they are re-prices of
    one estate off the same supplier quotes, which is exactly right."""
    out = []
    seen = {}
    for d in docs:
        for label, val in (d.get("supplier_parts") or []):
            seen.setdefault(round(val, 2), []).append((d, label))
    for val, rows in sorted(seen.items()):
        jobs = {(r[0].get("client"), r[0].get("job")) for r in rows}
        if len(rows) > 1 and len(jobs) > 1:
            for d, label in rows:
                others = [r[0]["file"] for r in rows if r[0] is not d]
                out.append((d, {
                    "check": "SUP_DUP", "row": None, "code": "", "money": round(val, 2),
                    "detail": "'%s' cost %.2f is the SAME FIGURE TO THE PENNY as in %s, a "
                              "different job - one of them is a cell left behind by a save-as, "
                              "and neither document's frames reconcile to it"
                              % (label or "?", val, "; ".join(o[:52] for o in others))}))
    return out


def collect_docs():
    seen, docs = set(), []
    for q in reader.scan(cal.TENDERS):
        if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
            continue
        d = read_doc(q["path"])
        if not d:
            continue
        sig = repr([[r["code"], r["size"], r["qty"], r["unit_rate"]] for r in d["rows"]])
        if sig in seen:
            continue
        seen.add(sig)
        d["client"], d["job"] = q["client"], q["job"]
        docs.append(d)
    return docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", nargs="?")
    ap.add_argument("--check", help="only this check")
    args = ap.parse_args()

    docs = [d for d in ([read_doc(args.doc)] if args.doc else collect_docs()) if d]
    print("audited %d sent pricing document(s)\n" % len(docs))

    extra = {}
    for d, x in cross_document(docs):
        extra.setdefault(id(d), []).append(x)

    by_check = {}
    total_findings = 0
    for d in sorted(docs, key=lambda x: x["file"]):
        f = audit(d) + extra.get(id(d), [])
        for x in f:
            by_check.setdefault(x["check"], []).append((d["file"], x))
        if args.check:
            f = [x for x in f if x["check"] == args.check]
        if not f:
            continue
        total_findings += len(f)
        print("%s   [%s]" % (d["file"], "internal" if is_marked_do_not_send(d["file"])
                              else "NOT MARKED DO NOT SEND"))
        print("   client %s | %d rows | supplier %s"
              % (d.get("client", "?"), len(d["rows"]), d["supplier"] or "not stated"))
        for x in f:
            print("   [%-9s] %+13s   %s"
                  % (x["check"], "{:,.2f}".format(x["money"]), x["detail"]))
        print()

    print("=" * 78)
    print("%d finding(s) shown across %d document(s)" % (total_findings, len(docs)))
    for c in ("FOOT_LINE", "FOOT_DOC", "DISCOUNT", "BUILDUP", "SUPPLIER", "SUP_DUP",
              "SUP_BLANK"):
        hits = by_check.get(c, [])
        print("  %-10s %3d finding(s) in %2d document(s)"
              % (c, len(hits), len(set(h[0] for h in hits))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
           "_sup_col": 0, "supplier_n": 0, "_sup_done": False}
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
            # Stop the block at the FIRST empty row. Without that it runs on
            # into the priced rows, whose Glass/Additional/CW columns sit in the
            # same place as the supplier figures, and every ratio collapsed to
            # about 0.47 - the supplier total had silently doubled.
            if (doc.get("_sup_row") and not doc.get("_sup_done")
                    and doc["_sup_row"] <= rn <= doc["_sup_row"] + 6):
                i = doc["_sup_col"]
                money = [m for m in (_num(c) for c in cells[i + 1:]) if m and m > 1]
                if money:
                    doc["_sup_vals"].append((rn, max(money)))
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
                "row": rn, "code": code,
                "desc": str(cells[2] or "").strip()[:40],
                "size": size, "area": area, "qty": qty, "unit_rate": unit_rate,
                "line_total": _num(cells[cols["line_total"]]) if "line_total" in cols else None,
                "frames": _num(cells[cols["frames"]]) if "frames" in cols else None,
                "glass": _num(cells[cols["glass"]]) if "glass" in cols else None,
                "additional": _num(cells[cols["additional"]]) if "additional" in cols else None,
                "cw": _num(cells[cols["cw"]]) if "cw" in cols else None,
            })
        doc["cols"] = cols
        # Resolve the supplier block: if the last figure equals the sum of the
        # ones above it, that is the block's own total and the rest are its
        # parts. Otherwise take the sum, which is the same answer when there is
        # only one supplier.
        vals = [v for _, v in doc["_sup_vals"]]
        if vals:
            parts, last = vals[:-1], vals[-1]
            if parts and abs(sum(parts) - last) <= 0.02:
                doc["supplier_cost"] = last
                doc["supplier_n"] = len(parts)
            else:
                doc["supplier_cost"] = sum(vals)
                doc["supplier_n"] = len(vals)
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
    if doc["supplier_cost"] and any(r["frames"] is not None for r in doc["rows"]):
        frames_sum = sum(r["frames"] * r["qty"] for r in doc["rows"] if r["frames"] is not None)
        gap = frames_sum - doc["supplier_cost"]
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
            out.append({
                "check": "SUPPLIER", "row": None, "code": "",
                "money": round(gap, 2),
                "detail": "frames total %.2f against '%s' buy %.2f, ratio %.3f%s"
                          % (frames_sum, doc["supplier"] or "?", doc["supplier_cost"],
                             ratio, note)})
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

    by_check = {}
    total_findings = 0
    for d in sorted(docs, key=lambda x: x["file"]):
        f = audit(d)
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
    for c in ("FOOT_LINE", "FOOT_DOC", "DISCOUNT", "BUILDUP", "SUPPLIER"):
        hits = by_check.get(c, [])
        print("  %-10s %3d finding(s) in %2d document(s)"
              % (c, len(hits), len(set(h[0] for h in hits))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

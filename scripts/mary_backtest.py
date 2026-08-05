# -*- coding: utf-8 -*-
"""Run Mary's engine over quotes Fenster has already sent, and score her.

This is the question that matters: not "is the arithmetic right" but "if Mary
had priced this job, how close would she have been to what we actually
charged?" We have hundreds of sent quotes sitting in the archive with the real
answer in them, so there is no need to wait for new jobs to find out.

Every client quote is a MASTER PRICING DOC clone, which means it is structured:
each row carries the product code, the size, the quantity, and - in the Frames
column - the supply money the estimator actually used. That last column is the
prize. Divided by area it gives the real GBP/m2 Fenster charges, per code, per
supplier, on real won and lost work. It is far better evidence than a median of
supplier quotes, because it is what we actually did.

So this does two jobs:
  1. Scores the engine against reality, job by job and code by code.
  2. Mines empirical rates from those Frames figures, which is what lets the
     engine calibrate itself instead of carrying constants I typed in by hand.

  python scripts/mary_backtest.py --scan          # score every quote on file
  python scripts/mary_backtest.py <file.xlsx>     # one job, line by line
  python scripts/mary_backtest.py --learn         # write empirical rates
"""
import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_pricing as engine
import mary_quote_reader as reader
import mary_calibrate as cal

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNED = os.path.join(REPO, "data", "learned-rates.json")
TENDERS = cal.TENDERS

SIZE_RE = re.compile(r"(\d{3,5})\s*[xX*]\s*(\d{3,5})")
_CW_REF_RE = re.compile(r"^\s*cwt?[\s\-]?[a-z0-9]", re.I)


def parse_doc(path):
    """Pull the priced lines out of a Fenster pricing document."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return None
    doc = {"file": os.path.basename(path), "lines": [], "installation": None, "total": None,
           "supplier": None}
    try:
        sheets = [w for w in wb.worksheets if w.title.strip().lower().startswith("pricing document")]
        if not sheets:
            return None
        ws = sheets[0]
        # Read once into memory: a read-only worksheet cannot be iterated twice,
        # and the client-facing pass below needs the same rows.
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        heading = ""
        for row in rows:
            cells = list(row) + [None] * (14 - len(row))
            texts = [str(c).strip().lower() if isinstance(c, str) else "" for c in cells]
            nums = [c if isinstance(c, (int, float)) else None for c in cells]

            if any(t.startswith("supplier used") for t in texts):
                idx = next(i for i, t in enumerate(texts) if t.startswith("supplier used"))
                after = [c for c in cells[idx + 1:] if isinstance(c, str) and c.strip()]
                if after:
                    doc["supplier"] = after[0].strip()
            if any(t == "installation" for t in texts):
                vals = [n for n in nums if n]
                if vals:
                    doc["installation"] = float(max(vals))
                continue
            if any(t.startswith("total") for t in texts):
                vals = [n for n in nums if n]
                if vals and doc["total"] is None:
                    doc["total"] = float(max(vals))
                continue

            code = str(cells[1]).strip().upper() if isinstance(cells[1], str) else ""

            # THE SECTION HEADING, which is where the product actually is.
            # A pricing document is organised in blocks under a heading that
            # names the system and the product - 'Sheerline Aluminium Casement
            # Windows', 'External Steel Door', 'Liniar uPVC Windows & Doors' -
            # and the product CODE beneath it only says window-or-door and
            # small-medium-large. So the code cannot tell a Strongdoor steel
            # security door from an aluminium one; both are SAD, and the money
            # is 1.7x apart. This is the term the engine has never had.
            # A heading is words in the description column with no unit rate
            # and no size in it. The qty test is deliberately NOT used: two
            # ASHE section headings carry a stray 1 in the Qty column, which
            # has already cost the audit a false alarm twice.
            desc = str(cells[2]).strip() if isinstance(cells[2], str) else ""
            # Tested BEFORE the code check, and it has to be: ASHE's 'Doors'
            # heading carries DAD in the code column and a stray 1 in Qty, so a
            # code-first reader skips it, loses the heading and carries
            # 'Secondary Glazing' down onto seven entrance doors. Neither a code
            # nor a quantity disqualifies a heading. No unit rate and no size in
            # the description does the work.
            if desc and cells[7] is None and not SIZE_RE.search(desc) \
                    and sum(c.isalpha() for c in desc) >= 4 \
                    and not desc.lower().startswith(
                        ("client", "project", "site", "date", "description", "product",
                         "total", "installation", "*", "optional")):
                heading = desc
                continue
            # A GENUINE CURTAIN-WALLING ROW HAS NO PRODUCT CODE AND IS NOT NOISE
            # (31/07, fourth run). Until now every code-less row was dropped
            # here, so the engine did not price curtain walling at all - and it
            # is not a rounding error's worth of the archive: 8 rows across 6
            # documents, GBP 129,657 of sell, and on CB Refrigeration one row is
            # 36% of the document. The engine has HAD a CW convention all along
            # (area x CW_SUPPLY_M2 supply, no code adder, labour in its own
            # column) - nothing could ever reach it.
            # The marker is the CW LABOUR cell at column 13. That is what tells
            # a genuine CW row from an ordinary coded window row carrying a CW
            # working figure, which the board established on 30/07: all 156 of
            # those hold area x GBP 850 in a spare column and it is NOT money in
            # the unit rate. A CW row is the other thing - no code, a CW LABOUR
            # figure, and the unit rate IS the area money.
            cw_labour = cells[13] if len(cells) > 13 and isinstance(cells[13], (int, float)) else None
            is_cw = code not in engine.CODE_VALUE and bool(cw_labour)
            if code not in engine.CODE_VALUE and not is_cw:
                continue
            size = next((str(c) for c in cells if isinstance(c, str) and SIZE_RE.search(str(c))), "")
            m = SIZE_RE.search(size)
            if not m:
                continue
            w, h = int(m.group(1)), int(m.group(2))
            qty = cells[5] if isinstance(cells[5], (int, float)) else 1
            unit_rate = cells[7] if isinstance(cells[7], (int, float)) else None
            frames = cells[9] if isinstance(cells[9], (int, float)) else None
            glass = cells[10] if isinstance(cells[10], (int, float)) else None
            # Column 11. The reader ignored it, which is why the engine had no
            # term for it - see supply_money() below. Verified 30/07: all 29
            # scored documents carry 'Additional' at exactly column 11, and
            # qty/unit rate/frames/glass are all where these fixed indices
            # assume. Some ARCHIVE copies are shifted (Gordon Court's
            # client-facing copy puts Qty at 4 and Unit Rate at 6; Roxbourne
            # puts Frames at 7), but those carry a reference like 'LW_1' in
            # column 1 instead of a product code, so every row is dropped and
            # they never enter the corpus. Column 12 is deliberately NOT read:
            # it is CW, and on a coded unit line that is a working column
            # holding area x GBP 850, not money in the unit rate.
            additional = cells[11] if isinstance(cells[11], (int, float)) else None
            if not unit_rate:
                continue
            doc["lines"].append({
                "code": code, "ref": str(cells[2] or "").strip()[:24],
                # Heading first, then the row's own description. Both carry the
                # product: a block of windows is named in the heading above it,
                # but a one-line document has no heading and puts the product in
                # the row itself - Tenbury Close is a single 'Aluminium
                # horizontal sliding' MAW, Tradeteam Stretton a single 'Tilt &
                # Turn Aluminium' MAW, and each is out by 38-48%.
                "heading": heading,
                "text": ("%s %s" % (heading, desc)).strip().lower(),
                "w": w, "h": h, "qty": float(qty or 1),
                "unit_rate": float(unit_rate),
                "frames": float(frames) if frames else None,
                "glass": float(glass) if glass else None,
                "additional": float(additional) if additional else None,
                "area": round(w / 1000.0 * h / 1000.0, 4),
                "cw": is_cw,
            })
        # THE CLIENT-FACING COPY, which the fixed column indices above cannot
        # read at all. Two thirds of the trustworthy sent quotes are this shape:
        # Description / Size / Qty / Unit Rate / Total, no product code column
        # and no Frames-Glass-Additional breakdown, with the columns wherever
        # that document happened to put them. Every row fell out at the
        # `code not in engine.CODE_VALUE` test, so 49 of 79 quotes never
        # reached the corpus and the engine was being tuned on 30.
        #
        # They cannot contribute a BUY rate - there is no Frames figure to mine
        # - and they do not: supply_money() returns None without one, so learn()
        # and the supplier factors skip these lines untouched. What they can do
        # is SCORE: a real total Fenster sent a client, against what the engine
        # would have said.
        if not doc["lines"]:
            cf = _parse_client_facing(rows)
            if cf:
                doc["lines"] = cf
                doc["client_facing"] = True
    finally:
        wb.close()
    return doc if doc["lines"] else None


def _find_header(rows):
    """Where this document put its columns. A client-facing copy is laid out to
    be read by a customer, not by us, so the positions move between documents
    and only the header row knows them."""
    for cells in rows:
        low = [str(c).strip().lower() if isinstance(c, str) else "" for c in cells]
        if "description" not in low:
            continue
        if not any(x in low for x in ("qty", "quantity")):
            continue
        idx = {}
        for i, t in enumerate(low):
            if t == "description" and "desc" not in idx:
                idx["desc"] = i
            elif t in ("qty", "quantity") and "qty" not in idx:
                idx["qty"] = i
            elif t in ("unit rate", "rate", "unit price") and "rate" not in idx:
                idx["rate"] = i
            elif t == "total" and "total" not in idx:
                idx["total"] = i
            elif t.startswith("size") and "size" not in idx:
                idx["size"] = i
        return idx
    return None


def _client_facing_code(heading, desc, area, width_mm):
    """The product code from the words, because this copy has no code column.

    Returns None for anything the register cannot price by code - curtain
    walling, secondary glazing and steel all take a different path, and
    guessing a code for them would be worse than leaving the line out.

    Window-vs-door has to be decided off the ROW first, not the heading: a
    'Sheerline Aluminium Windows & Doors' or 'uPVC Windows and Doors' heading
    is the template's own product name and contains the substring 'door' on
    every window row underneath it too - measured 05/08, this alone put four
    client-facing documents 60-150% out (Redditch Library, Severn Trent,
    Willseden Junction, Trafalgar House all coded window rows as DAD/SAD).
    Fenster's own ref numbering ('W1', 'D0.01', 'DG-01') is the fallback when
    the row text is silent, and is safer than the heading because it is
    written per item, not per section."""
    hay_head = heading.lower()
    hay_desc = desc.lower()
    if any(k in hay_head or k in hay_desc
           for k in ("curtain wall", "cw0", "secondary glazing", "steel")):
        return None
    upvc = "upvc" in hay_head or "upvc" in hay_desc or " pvc" in hay_desc
    is_window = "window" in hay_desc
    is_door = "door" in hay_desc
    if not is_window and not is_door:
        head_window, head_door = "window" in hay_head, "door" in hay_head
        if head_window and not head_door:
            is_window = True
        elif head_door and not head_window:
            is_door = True
        else:
            m = re.match(r"\s*([A-Za-z]+)", desc)
            prefix = m.group(1).upper() if m else ""
            if prefix.startswith("W"):
                is_window = True
            elif prefix.startswith("D"):
                is_door = True
    if is_door and not is_window:
        double = width_mm >= 1550
        if upvc:
            return "DUPD" if double else "SUPD"
        return "DAD" if double else "SAD"
    if is_window and not is_door:
        if upvc:
            return "LPVC" if area >= 3 else ("MPVC" if area >= 1.5 else "SPVC")
        return "LAW" if area >= 3 else ("MAW" if area >= 1.5 else "SAW")
    # Both or neither - the row said nothing usable and the ref carried no
    # W/D prefix either. Guessing here is exactly the mistake this fixes.
    return None


def _parse_client_facing(rows):
    """Priced lines out of a client-facing pricing document."""
    idx = _find_header(rows)
    if not idx or "desc" not in idx or "qty" not in idx:
        return []
    lines, heading, started = [], "", False
    for cells in rows:
        n = len(cells)

        def get(k):
            i = idx.get(k)
            return cells[i] if i is not None and i < n else None

        desc = get("desc")
        descs = str(desc).strip() if isinstance(desc, str) else ""
        if not descs:
            continue
        if descs.lower() == "description":
            started = True
            continue
        if not started:
            continue
        if descs.lower().startswith(("*", "optional", "total", "installation",
                                     "client", "project", "site", "date")):
            continue
        qty = get("qty")
        size_cell = get("size")
        size_text = str(size_cell) if isinstance(size_cell, (str, int, float)) else ""
        m = SIZE_RE.search(size_text) or SIZE_RE.search(descs)
        if not m:
            # No size and no quantity is a section heading - and the heading is
            # where the product is named, so it has to be carried down.
            if not isinstance(qty, (int, float)) and sum(c.isalpha() for c in descs) >= 4:
                heading = descs
            continue
        if not isinstance(qty, (int, float)) or qty <= 0:
            continue
        w, h = int(m.group(1)), int(m.group(2))
        area = round(w / 1000.0 * h / 1000.0, 4)
        if area <= 0:
            continue
        rate, total = get("rate"), get("total")
        unit_rate = rate if isinstance(rate, (int, float)) and rate else None
        if unit_rate is None and isinstance(total, (int, float)) and total:
            unit_rate = total / qty          # some copies show only the line total
        if not unit_rate:
            continue
        # A ref of 'CWT-A' or 'CW01' is curtain walling priced by area, same as
        # the master format - CB Refrigeration's CWT-A reproduces area x GBP850
        # to the penny (15,036.50 at 17.69 m2). Missing this dropped the row
        # entirely before (_client_facing_code's own 'curtain wall'/'cw0' text
        # filter never matches an abbreviated ref), and worse, a version of this
        # check that only excluded it left a 17.69 m2 unit being coded as an
        # ordinary LAW window - the single biggest line in the document, priced
        # off a bucket that has never seen anything a tenth of that size.
        is_cw = bool(_CW_REF_RE.match(descs)) or "curtain wall" in heading.lower()
        code = "" if is_cw else _client_facing_code(heading, descs, area, w)
        if not is_cw and not code:
            continue
        lines.append({
            "code": code, "ref": descs[:24], "heading": heading,
            "text": ("%s %s" % (heading, descs)).strip().lower(),
            "w": w, "h": h, "qty": float(qty), "unit_rate": float(unit_rate),
            # No breakdown exists in this shape. Left as None on purpose so
            # supply_money() refuses them and no buy rate is ever mined from a
            # sell price.
            "frames": None, "glass": None, "additional": None,
            "area": area, "cw": is_cw,
        })
    return lines


def _learn_code(l):
    """The bucket a line's rate is mined into and looked up from.

    A sliding window prices 3-4x an ordinary casement of the same code and
    band - measured 05/08 on Tenbury Close and Georgie's Rosebank, two
    independent jobs, both consistently GBP1,200-2,800/m2 against a normal
    MAW/SAW/LAW median of GBP300-500/m2 for the same size band. The archive
    does not even code sliding windows consistently - the same 855x1455 unit
    is LAW in Georgie's own master document and something else in its sibling
    copy - so the code itself is not a reliable signal for this product, only
    the word 'sliding' in the description is."""
    if l["code"] not in ("SAD", "DAD", "SUPD", "DUPD") and "slid" in (l.get("text") or ""):
        return "SLIDE"
    return l["code"]


def engine_price(line, supplier=None, system="", learned=None, factors=None):
    """What Mary's engine would have said for this row.

    Prefers a rate learned from what Fenster actually charged for this code and
    size band; falls back to the supplier-quote register when there is not
    enough of it. `learned` can be passed in for holdout testing so the rates
    under test are never the ones mined from the same job, and `factors` the
    same way for the supplier corrections - they have to be re-mined inside the
    fold too, or the supplier effect of the job being scored is in its own
    correction."""
    # CURTAIN WALLING IS PRICED BY AREA, NOT BY CODE, and it takes no learned
    # rate and no code adder - so it is answered before any of the register
    # machinery below and is UNAFFECTED BY THE FOLD. CW_SUPPLY_M2 is a constant
    # calibrated off Greenfields on 22/07, and the reason it is trustworthy here
    # is that it reproduces on rows it was NOT set from: of the 6 independent CW
    # rows in the archive, 5 sit within 3p of area x GBP 850 - St Mary's Type AK
    # 8,655.98, CB Refrigeration CWT-A 15,036.50, St Christopher's EW1 7,811.53
    # and W2 3,898.91, Wisley CW1 19,975.00. The sixth is Georgie's, out by
    # exactly GBP 2,000.02, and its description is 'CW01, D03, CW0...' - a door
    # in with the curtain walling, which is scope and not a rate error.
    if line.get("cw"):
        return {"unit_rate": line["area"] * engine.CW_SUPPLY_M2,
                "supply": line["area"] * engine.CW_SUPPLY_M2,
                "rate_per_m2": engine.CW_SUPPLY_M2}

    key = "%s|%s" % (_learn_code(line), engine.learned_band_of(line["area"]))
    rec = (learned or {}).get(key) if learned is not None else None
    if learned is None:
        r = engine.learned_rate(_learn_code(line), line["area"], supplier, system)
    elif rec and rec.get("n", 0) >= engine.MIN_LEARNED_N:
        fac = []
        if factors:
            key_s = _supplier_key(system or supplier or "")
            f = factors.get(key_s)
            if f and f.get("applied"):
                fac = [{"factor": f["factor"], "why": f.get("why", ""),
                        "source": f.get("source", "")}]
        r = engine.LearnedRate(key, rec, fac)
    else:
        r = None
    if r is not None:
        supply = line["area"] * r.rate
        adder = engine.CODE_VALUE.get(line["code"], 0) * engine.adder_factor(line["area"])
        return {"unit_rate": supply + adder, "supply": supply, "rate_per_m2": r.rate}

    family = "aluminium door, glazed" if line["code"] in ("SAD", "DAD", "SUPD", "DUPD") \
        else "aluminium casement window, glazed"
    try:
        r = engine.find_rate(family, line["area"], None, system or (supplier or ""))
    except Exception:
        return None
    if r is None:
        return None
    supply = line["area"] * r.rate
    adder = engine.CODE_VALUE.get(line["code"], 0) * engine.adder_factor(line["area"])
    return {"unit_rate": supply + adder, "supply": supply, "rate_per_m2": r.rate}


def score_doc(doc, learned=None, factors=None):
    got = missed = 0
    eng_total = 0.0
    human_total = 0.0
    per_line = []
    for l in doc["lines"]:
        e = engine_price(l, doc.get("supplier"), learned=learned, factors=factors)
        if not e:
            missed += 1
            continue
        got += 1
        eng_total += e["unit_rate"] * l["qty"]
        human_total += l["unit_rate"] * l["qty"]
        err = (e["unit_rate"] - l["unit_rate"]) / l["unit_rate"] * 100.0
        per_line.append(dict(l, engine_unit=round(e["unit_rate"], 2),
                             engine_rate_m2=round(e["rate_per_m2"], 2), err_pct=round(err, 1)))
    if not got or not human_total:
        return None
    return {"file": doc["file"], "supplier": doc.get("supplier"),
            "lines_priced": got, "lines_skipped": missed,
            "engine_items": round(eng_total, 2), "human_items": round(human_total, 2),
            "err_pct": round((eng_total - human_total) / human_total * 100.0, 2),
            "per_line": per_line}


def doc_signature(doc):
    """Identify a pricing document by what it PRICES, not by what it is called.

    A job folder routinely holds the same quote several times over - 'X.xlsx',
    'X (1).xlsx', 'X DO NOT SEND.xlsx' - and collect() used to return every one
    of them, so the corpus counted Zelltec Crownhill three times. Filename
    matching is the obvious fix and it is the wrong one: two of the '- Copy'
    files in this archive (Wisley Golf Club, Tradeteam Stretton) are the ONLY
    copy of their job, and dropping them on the name would have lost real
    evidence. Same priced lines and same money is the test."""
    return json.dumps([[l["code"], l["w"], l["h"], l["qty"], l["unit_rate"], l["frames"]]
                       for l in doc["lines"]], sort_keys=True)


def _copy_rank(name):
    """Among identical copies, prefer the plainest filename for the report."""
    n = name.lower()
    return (1 if "do not send" in n else 0,
            1 if "copy" in n else 0,
            1 if re.search(r"\(\d+\)", n) else 0,
            len(n))


def collect(limit=None):
    docs = []
    for q in reader.scan(TENDERS):
        if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
            continue
        d = parse_doc(q["path"])
        if d:
            d["client"], d["job"] = q["client"], q["job"]
            docs.append(d)

    # One job, one vote. Before this, the scan mean was weighted by how many
    # copies of a file happened to sit in a folder. NOTE, measured 30/07: this
    # does NOT move accuracy - three folds put it at 0.01/0.04/0.00 points, with
    # one fold favouring each arm, because a median over 500 lines barely
    # notices 8 of them counted twice over. It is a reporting fix, not a rate
    # fix, and the next person should not expect the error to fall.
    unique, seen = [], {}
    for d in docs:
        sig = doc_signature(d)
        if sig in seen:
            d["duplicate_of"] = seen[sig]["file"]
            if _copy_rank(d["file"]) < _copy_rank(seen[sig]["file"]):
                seen[sig]["file"], d["file"] = d["file"], seen[sig]["file"]
            continue
        seen[sig] = d
        unique.append(d)
        if limit and len(unique) >= limit:
            break
    return unique


def supply_money(l):
    """The WHOLE supply money in a line, not just its Frames cell.

    The document builds a unit rate as
        frames + glass + additional + 0.75 x code_value
    and that reconciles on 495 of 508 priced lines (30/07, once the CW working
    column is excluded). The engine models
        area x learned_rate + adder x code_value
    so if learned_rate is mined from Frames ALONE, then Glass and Additional are
    money the engine has no term for anywhere - 20.4% of supply above 6m2 and
    9.3% at 2-3m2. ADDER_FACTOR_LARGE = 1.25 was a patch over the largest part of
    it, and 30/07 identified it as exactly that: the median GBP 1,000 of extras
    on a large unit charged to a median code value of 2,000.

    Mining the whole build-up instead makes the engine's arithmetic the same
    arithmetic as the document's, and lets the adder go back to a flat 0.75.
    THIS IS NOT the fix rejected on 30/07 - that one added a flat learned extras
    SUM on large units only and scored 14.73. This puts the extras into the
    per-m2 rate itself, per code and per band, so it varies with size and
    product the way the money actually does.

    Measured leave-one-out over all 29 documents, every job scored on rates
    mined from the other 28:
        frames only,       1.25 large   mean abs 14.02%  median 10.05%  bias -4.91%
        whole build-up,    0.75 flat    mean abs 13.24%  median  7.98%  bias -1.66%
    Better on 16 documents, worse on 11, within-10 up from 14 to 16. Three
    positional folds agree but only just (13.88 -> 13.68), which is why this was
    decided on leave-one-out: a 0.20-point win on three folds is the shape of
    result that has already misled this board twice.

    A CURTAIN-WALLING ROW CONTRIBUTES NOTHING HERE and is excluded (31/07). It
    carries no product code, so it would land in a bucket keyed '|band' that no
    lookup can ever reach - harmless in learn(), but learn_supplier_factors()
    reads the same buckets and a bogus one there would move a real supplier's
    correction. And the Frames cell on a CW row is not reliably a buy at all:
    CB Refrigeration's holds 15,036.50, which is the CW NOTIONAL of area x 850
    to the penny, against a BSW quote of 15,994.08 for TWO units. Mining it
    would teach the engine a figure the supplier never charged."""
    if l.get("cw"):
        return None
    if not l.get("frames"):
        return None
    return l["frames"] + (l.get("glass") or 0.0) + (l.get("additional") or 0.0)


def learn(docs):
    """Empirical GBP/m2 from what Fenster actually charged, by code and band.

    Grouped by product code and size band this is a far better rate than a
    median of supplier quotes, because it already contains every judgement the
    estimator applied."""
    buckets = {}
    for d in docs:
        for l in d["lines"]:
            money = supply_money(l)
            if not money or l["area"] <= 0:
                continue
            key = "%s|%s" % (_learn_code(l), engine.learned_band_of(l["area"]))
            buckets.setdefault(key, []).append(money / l["area"])
    out = {}
    for key, vals in sorted(buckets.items()):
        if len(vals) < 3:
            continue
        out[key] = {"median_per_m2": round(statistics.median(vals), 2),
                    "n": len(vals),
                    "low": round(min(vals), 2), "high": round(max(vals), 2)}
    return out


MIN_SUPPLIER_LINES = 8
# A supplier genuinely runs maybe 20% either side of the norm. Outside this the
# likely cause is a mis-parse or a job priced on a different basis, and a
# self-improving system that swallows it teaches itself to underprice. Recorded
# but not applied, so a human can look.
PLAUSIBLE_FACTOR = (0.65, 1.55)


def _supplier_key(name):
    """'Tru Frame' and 'TruFrame' are one supplier - they came out as two, with
    factors of 0.842 and 0.378, which is how you get a self-inflicted 60% error."""
    return re.sub(r"[^a-z0-9]", "", str(name or "").lower())


def learn_supplier_factors(docs, base):
    """How much dearer or cheaper each supplier runs than the overall rate.

    These replace the calibration constants that were previously typed in by
    hand ("Sheerline +10%", "Smart Wall +45%"). Each line is compared against
    the all-supplier median for its own code and size band, so the factor is
    the supplier's effect with size and product already held constant."""
    ratios = {}
    for d in docs:
        supplier = (d.get("supplier") or "").strip()
        if not supplier:
            continue
        for l in d["lines"]:
            # Same money basis as learn(), or the ratio compares a whole
            # build-up against a Frames-only median and every supplier looks
            # cheap by however much Glass and Additional they happen to carry.
            money = supply_money(l)
            if not money or l["area"] <= 0:
                continue
            key = "%s|%s" % (_learn_code(l), engine.learned_band_of(l["area"]))
            b = base.get(key)
            if not b or not b["median_per_m2"]:
                continue
            ratios.setdefault(_supplier_key(supplier), []).append(
                (money / l["area"]) / b["median_per_m2"])
    out = {}
    for supplier, vals in sorted(ratios.items()):
        if len(vals) < MIN_SUPPLIER_LINES:
            continue
        factor = round(statistics.median(vals), 3)
        applied = PLAUSIBLE_FACTOR[0] <= factor <= PLAUSIBLE_FACTOR[1]
        out[supplier] = {
            "factor": factor,
            "applied": applied,
            "n": len(vals),
            "why": "median of %d priced lines against the all-supplier rate for the same code "
                   "and size band" % len(vals),
            "source": "derived from sent pricing documents",
        }
        if not applied:
            out[supplier]["held_back"] = (
                "outside the plausible %.2f-%.2f band - looks like a mis-parse or a job priced on "
                "a different basis, so it is recorded but NOT applied" % PLAUSIBLE_FACTOR)
    return out


def job_key(doc):
    """Which JOB a document belongs to, which is not the same as which document.

    The corpus is 29 documents and 26 jobs. Brandon Estate is in it THREE times -
    Elkins at GBP 7,196,696, a COMAR-priced variant at 6,184,746 and an earlier
    11-line version at 3,998,687 - and Zelltec Crownhill twice. These are
    revisions and re-prices of one estate, not separate evidence, and the 30/07
    content dedup could not see them because their priced lines genuinely differ.

    It matters twice over. Brandon Estate is 93 of the 508 mined lines, so one
    estate sets 18% of the rates. And leaving out one DOCUMENT leaves the other
    two revisions of the same job in the training set, with the same elevations
    at the same unit rates - so the engine is shown the answer and the honest
    number is not honest. Hold out the whole job."""
    return re.sub(r"[^a-z0-9]", "", "%s|%s" % (str(doc.get("client") or "")[:18].lower(),
                                               str(doc.get("job") or "")[:18].lower()))


def leave_one_out(docs):
    """Score every document on rates mined from all the others.

    THIS IS THE NUMBER TO DECIDE ON, and until now it only existed as a
    scratchpad experiment, so two sessions running have had to re-derive it
    before they could judge a change. --holdout --folds splits the corpus by
    POSITION in the scan order, so fold 0 is the odd one out (21.4% where the
    same engine does 9.9% and 10.4%) and adding one document to the archive
    reshuffles all three. Leave-one-out has no such handle: every document is a
    test document, scored on rates it contributed nothing to, and the answer
    cannot depend on where a file sits in a directory listing. The 30/07
    build-up change was worth 0.78 points here and 0.20 on three folds, where it
    won one fold of three - on the folds alone it would have been dropped.

    Quote --folds for continuity with the earlier board entries. Decide here."""
    groups = {}
    for d in docs:
        groups.setdefault(job_key(d), []).append(d)
    rows = []
    for key, group in groups.items():
        train = [d for d in docs if job_key(d) != key]
        rates = learn(train)
        facs = learn_supplier_factors(train, rates)
        for d in group:
            s = score_doc(d, learned=rates, factors=facs)
            if s:
                s["job"] = key
                rows.append(s)
    if not rows:
        print("nothing scored")
        return 1
    absol = [abs(s["err_pct"]) for s in rows]
    signed = [s["err_pct"] for s in rows]
    print("leave-one-JOB-out: %d documents in %d jobs, each scored on rates mined from the\n"
          "other jobs only - a revision of the same estate is not independent evidence\n"
          % (len(rows), len(groups)))
    print("  mean abs %6.2f%%   median abs %6.2f%%   bias %+6.2f%%   within 10%%: %d/%d   "
          "within 25%%: %d/%d"
          % (statistics.fmean(absol), statistics.median(absol), statistics.fmean(signed),
             sum(1 for a in absol if a <= 10), len(absol),
             sum(1 for a in absol if a <= 25), len(absol)))
    print("  lines priced %d   skipped %d"
          % (sum(s["lines_priced"] for s in rows), sum(s["lines_skipped"] for s in rows)))

    # And the same thing weighted by money, which is what "1 to 1" means to Zac -
    # WITH ITS HEALTH WARNING, because it is not a second opinion. Brandon Estate
    # is 89% of the archive's priced money across its three revisions, so a
    # money-weighted archive figure is very nearly a report on one estate. Quote
    # the per-document mean as the headline and this as the exposure.
    H = sum(s["human_items"] for s in rows)
    E = sum(s["engine_items"] for s in rows)
    big = max(groups, key=lambda k: sum(s["human_items"] for s in rows if s["job"] == k))
    bigshare = sum(s["human_items"] for s in rows if s["job"] == big) / H * 100.0
    print("  money-weighted abs %5.2f%%   whole archive human %s v mary %s -> %+.2f%%"
          % (sum(abs(s["engine_items"] - s["human_items"]) for s in rows) / H * 100.0,
             "{:,.0f}".format(H), "{:,.0f}".format(E), (E - H) / H * 100.0))
    print("  READ THAT WITH CARE: the largest job alone is %.0f%% of the priced money, so the"
          % bigshare)
    print("  money-weighted figure is mostly a report on it.")
    print("\nWORST DOCUMENTS - where the remaining error lives")
    print("  %-50s %8s %6s %12s %12s" % ("DOCUMENT", "OUT BY", "LINES", "HUMAN", "MARY"))
    for s in sorted(rows, key=lambda s: -abs(s["err_pct"]))[:10]:
        print("  %-50s %+7.1f%% %6d %12s %12s"
              % (s["file"][:50], s["err_pct"], s["lines_priced"],
                 "{:,.0f}".format(s["human_items"]), "{:,.0f}".format(s["engine_items"])))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", nargs="?")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--learn", action="store_true")
    ap.add_argument("--holdout", action="store_true",
                    help="honest test: learn on some jobs, score on the others")
    ap.add_argument("--folds", action="store_true",
                    help="score all three folds and report the mean - the honest number")
    ap.add_argument("--loo", action="store_true",
                    help="leave-one-out: every document scored on rates mined from all the "
                         "others. Decide on this, not on the folds")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    if args.loo:
        return leave_one_out(collect(args.limit))

    if args.holdout:
        docs = collect(args.limit)
        # ALL THREE FOLDS, not one. --holdout used to score fold 0 alone, and
        # fold 0 is not representative: measured 30/07 the same engine scores
        # 21.4% on it and 9.9% / 10.4% on the other two. Worse, the folds are
        # positional, so adding a single document to the archive reshuffles all
        # three - which is why the 14.5% quoted on 29/07 and the 19.9% seen on
        # 30/07 are the same engine, not a regression. A one-fold number has
        # now misled two sessions running; quote the mean of folds.
        folds = range(3) if args.folds else [0]
        rows = {}
        for f in folds:
            train = [d for i, d in enumerate(docs) if i % 3 != f]
            test = [d for i, d in enumerate(docs) if i % 3 == f]
            rates = learn(train)
            facs = learn_supplier_factors(train, rates)
            if len(folds) == 1:
                print("holdout: learned from %d job(s), scored on %d it has never seen\n"
                      % (len(train), len(test)))
            for label, learned in (("register only (before)", {}),
                                   ("+ learned rates (after)", rates)):
                scored = [s for s in (score_doc(d, learned=learned, factors=facs) for d in test)
                          if s]
                absol = [abs(s["err_pct"]) for s in scored]
                signed = [s["err_pct"] for s in scored]
                if not absol:
                    continue
                rows.setdefault(label, []).append(
                    (statistics.fmean(absol), statistics.median(absol),
                     statistics.fmean(signed), sum(1 for a in absol if a <= 25), len(absol),
                     sum(s["lines_priced"] for s in scored),
                     sum(s["lines_skipped"] for s in scored)))
                if len(folds) > 1:
                    continue
                print("  %-26s mean abs %5.1f%%   median abs %5.1f%%   bias %+5.1f%%   "
                      "within 25%%: %d/%d"
                      % (label, absol and statistics.fmean(absol), statistics.median(absol),
                         statistics.fmean(signed), sum(1 for a in absol if a <= 25), len(absol)))
        if len(folds) > 1:
            print("3-fold holdout over %d documents\n" % len(docs))
            for label, rs in rows.items():
                per = "  ".join("f%d %5.1f%%" % (i, r[0]) for i, r in enumerate(rs))
                print("  %-26s %s   MEAN OF FOLDS %5.2f%%   median %5.2f%%   bias %+5.2f%%"
                      % (label, per, statistics.fmean([r[0] for r in rs]),
                         statistics.fmean([r[1] for r in rs]),
                         statistics.fmean([r[2] for r in rs])))
            # A change that improves the score by dropping the hard lines is not
            # an improvement. 29/07 lost an hour to exactly that.
            for label, rs in rows.items():
                print("  %-26s lines %s  skipped %s"
                      % (label, [r[5] for r in rs], [r[6] for r in rs]))
        return 0

    if args.doc:
        d = parse_doc(args.doc)
        if not d:
            print("could not parse that as a pricing document")
            return 1
        s = score_doc(d)
        print("%s  (supplier: %s)" % (d["file"], d.get("supplier") or "not stated"))
        print("%-8s %-16s %10s %12s %12s %9s" % ("CODE", "REF", "AREA m2", "HUMAN", "MARY", "OUT BY"))
        for l in s["per_line"]:
            print("%-8s %-16s %10.2f %12s %12s %8.1f%%"
                  % (l["code"], l["ref"][:16], l["area"],
                     "{:,.2f}".format(l["unit_rate"]), "{:,.2f}".format(l["engine_unit"]), l["err_pct"]))
        print("\nitems: human %s vs Mary %s  -> %+.2f%%"
              % ("{:,.2f}".format(s["human_items"]), "{:,.2f}".format(s["engine_items"]), s["err_pct"]))
        return 0

    docs = collect(args.limit)
    print("parsed %d sent quote(s) with priced lines\n" % len(docs))

    if args.learn:
        rates = learn(docs)
        factors = learn_supplier_factors(docs, rates)
        with open(LEARNED, "w", encoding="utf-8") as fh:
            json.dump({"note": "Empirical GBP/m2 from the Frames column of quotes Fenster actually "
                               "sent - what we really charge, not a median of supplier quotes. "
                               "supplier_factors are derived, and supersede the hand-written "
                               "constants in mary_pricing.CALIBRATION.",
                       "source_docs": len(docs), "rates": rates,
                       "supplier_factors": factors}, fh, indent=1)
        if factors:
            print("SUPPLIER FACTORS (derived, no longer typed in by hand)")
            for s, f in factors.items():
                print("  %-22s x%.3f  from %d line(s)" % (s, f["factor"], f["n"]))
            print()
        print("%-16s %12s %6s %12s %12s" % ("CODE|BAND", "MEDIAN/m2", "n", "LOW", "HIGH"))
        for k, v in rates.items():
            print("%-16s %12s %6d %12s %12s" % (k, "{:,.2f}".format(v["median_per_m2"]), v["n"],
                                                "{:,.2f}".format(v["low"]), "{:,.2f}".format(v["high"])))
        print("\nwrote %s" % LEARNED)
        return 0

    scored = [s for s in (score_doc(d) for d in docs) if s]
    scored.sort(key=lambda s: abs(s["err_pct"]))
    errs = [s["err_pct"] for s in scored]
    print("%-44s %6s %12s %12s %8s" % ("JOB", "LINES", "HUMAN", "MARY", "OUT BY"))
    for s in scored:
        print("%-44s %6d %12s %12s %+7.1f%%"
              % (s["file"][:44], s["lines_priced"], "{:,.0f}".format(s["human_items"]),
                 "{:,.0f}".format(s["engine_items"]), s["err_pct"]))
    if errs:
        absol = [abs(e) for e in errs]
        print("\n%d job(s) back-tested" % len(errs))
        print("  mean signed error   %+.1f%%   (is she biased high or low?)" % statistics.fmean(errs))
        print("  mean absolute error  %.1f%%   (how far out, either way)" % statistics.fmean(absol))
        print("  median absolute      %.1f%%" % statistics.median(absol))
        print("  within 10%%: %d/%d   within 25%%: %d/%d"
              % (sum(1 for a in absol if a <= 10), len(absol),
                 sum(1 for a in absol if a <= 25), len(absol)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

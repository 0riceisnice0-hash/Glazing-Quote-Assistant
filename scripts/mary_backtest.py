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
        for row in ws.iter_rows(values_only=True):
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
            if code not in engine.CODE_VALUE:
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
            if not unit_rate:
                continue
            doc["lines"].append({
                "code": code, "ref": str(cells[2] or "").strip()[:24],
                "w": w, "h": h, "qty": float(qty or 1),
                "unit_rate": float(unit_rate),
                "frames": float(frames) if frames else None,
                "glass": float(glass) if glass else None,
                "area": round(w / 1000.0 * h / 1000.0, 4),
            })
    finally:
        wb.close()
    return doc if doc["lines"] else None


def engine_price(line, supplier=None, system="", learned=None):
    """What Mary's engine would have said for this row.

    Prefers a rate learned from what Fenster actually charged for this code and
    size band; falls back to the supplier-quote register when there is not
    enough of it. `learned` can be passed in for holdout testing so the rates
    under test are never the ones mined from the same job."""
    key = "%s|%s" % (line["code"], engine.learned_band_of(line["area"]))
    rec = (learned or {}).get(key) if learned is not None else None
    if learned is None:
        r = engine.learned_rate(line["code"], line["area"])
    elif rec and rec.get("n", 0) >= engine.MIN_LEARNED_N:
        r = engine.LearnedRate(key, rec)
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


def score_doc(doc, learned=None):
    got = missed = 0
    eng_total = 0.0
    human_total = 0.0
    per_line = []
    for l in doc["lines"]:
        e = engine_price(l, doc.get("supplier"), learned=learned)
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


def learn(docs):
    """Empirical GBP/m2 from what Fenster actually charged, by code and band.

    The Frames column is the estimator's own supply money. Grouped by product
    code and size band it is a far better rate than a median of supplier
    quotes, because it already contains every judgement they applied."""
    buckets = {}
    for d in docs:
        for l in d["lines"]:
            if not l["frames"] or l["area"] <= 0:
                continue
            key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
            buckets.setdefault(key, []).append(l["frames"] / l["area"])
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
            if not l["frames"] or l["area"] <= 0:
                continue
            key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
            b = base.get(key)
            if not b or not b["median_per_m2"]:
                continue
            ratios.setdefault(_supplier_key(supplier), []).append(
                (l["frames"] / l["area"]) / b["median_per_m2"])
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", nargs="?")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--learn", action="store_true")
    ap.add_argument("--holdout", action="store_true",
                    help="honest test: learn on some jobs, score on the others")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    if args.holdout:
        docs = collect(args.limit)
        # Alternate rather than shuffle, so the split is reproducible.
        train = [d for i, d in enumerate(docs) if i % 3 != 0]
        test = [d for i, d in enumerate(docs) if i % 3 == 0]
        rates = learn(train)
        print("holdout: learned from %d job(s), scored on %d it has never seen\n"
              % (len(train), len(test)))
        for label, learned in (("register only (before)", {}), ("+ learned rates (after)", rates)):
            scored = [s for s in (score_doc(d, learned=learned) for d in test) if s]
            absol = [abs(s["err_pct"]) for s in scored]
            signed = [s["err_pct"] for s in scored]
            if not absol:
                print("  %-26s no scoreable jobs" % label)
                continue
            print("  %-26s mean abs %5.1f%%   median abs %5.1f%%   bias %+5.1f%%   within 25%%: %d/%d"
                  % (label, statistics.fmean(absol), statistics.median(absol),
                     statistics.fmean(signed), sum(1 for a in absol if a <= 25), len(absol)))
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

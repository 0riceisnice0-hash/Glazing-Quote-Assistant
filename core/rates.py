# -*- coding: utf-8 -*-
"""The rate register, and the record of how close Mary's prices actually are.

TWO JOBS, and the second is the one that was missing.

1. LOOK UP a benchmark before pricing. 80 categories mined from real supplier
   quotations - median, range, and the quote references behind each one.

     python core/rates.py --lookup "aluminium door"
     python core/rates.py --supplier aplus

   These are EVIDENCE, never firm prices. A supplier quote is typically valid
   30 days; a benchmark says what this kind of thing has cost, not what it
   costs today. Price supplier-backed where a live quote exists and fall back
   to a benchmark only when it does not - saying which you used.

2. SCORE a price once reality arrives. Mary's whole craft was unmeasured: the
   register, the calibration file and the backtest scripts all survived the
   rebuild, but nothing compared what she said a job would cost against what
   it actually cost. So "is she pricing accurately" had no answer.

     python core/rates.py --score filwood --mine 85767.58 --actual 84120.00 \
         --basis "BSW 0000000507"
     python core/rates.py --scoreboard

   Every score is appended to data/calibration.json and shows on the hub, so
   accuracy becomes a number that moves rather than an opinion.
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

REGISTER = os.path.join(config.DATA, "supplier-rates.json")
CALIBRATION = os.path.join(config.DATA, "calibration.json")


def register():
    with open(REGISTER, encoding="utf-8") as fh:
        return json.load(fh)


def lookup(term, supplier=None):
    reg = register()["register"]
    t = (term or "").lower()
    hits = [r for r in reg
            if (not t or t in r["category"].lower() or t in r["supplier"].lower())
            and (not supplier or r["supplier"].lower() == supplier.lower())]
    hits.sort(key=lambda r: -r.get("lineCount", 0))
    return hits


def _calibration():
    try:
        with open(CALIBRATION, encoding="utf-8") as fh:
            d = json.load(fh)
    except (IOError, ValueError):
        d = {}
    d.setdefault("note", "Mary's pricing accuracy. Each entry compares what she "
                         "priced against what it actually turned out to cost.")
    d.setdefault("entries", [])
    return d


def score(lead, mine, actual, basis="", note=""):
    """Record one comparison. Positive delta = she was HIGH."""
    d = _calibration()
    mine, actual = float(mine), float(actual)
    delta = mine - actual
    pct = (delta / actual * 100.0) if actual else 0.0
    entry = {"at": dt.datetime.now().isoformat(timespec="seconds"),
             "lead": lead, "priced": round(mine, 2), "actual": round(actual, 2),
             "delta": round(delta, 2), "pct": round(pct, 2),
             "basis": basis, "note": note}
    d["entries"].append(entry)
    with open(CALIBRATION, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=1)
    return entry


def scoreboard():
    e = [x for x in _calibration()["entries"] if isinstance(x, dict) and "pct" in x]
    if not e:
        return {"n": 0}
    pcts = sorted(x["pct"] for x in e)
    n = len(pcts)
    med = pcts[n // 2] if n % 2 else (pcts[n // 2 - 1] + pcts[n // 2]) / 2
    within5 = sum(1 for p in pcts if abs(p) <= 5)
    return {"n": n, "median_pct": round(med, 2),
            "mean_abs_pct": round(sum(abs(p) for p in pcts) / n, 2),
            "within_5pct": within5, "high": sum(1 for p in pcts if p > 0),
            "low": sum(1 for p in pcts if p < 0), "entries": e[-10:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lookup", help="category or supplier text")
    ap.add_argument("--supplier")
    ap.add_argument("--score", metavar="LEAD")
    ap.add_argument("--mine", type=float, help="what you priced it at, ex VAT")
    ap.add_argument("--actual", type=float, help="what it actually came to, ex VAT")
    ap.add_argument("--basis", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--scoreboard", action="store_true")
    a = ap.parse_args()

    if a.scoreboard:
        s = scoreboard()
        if not s["n"]:
            print("No prices have been scored yet, so accuracy is unmeasured.\n"
                  "Score one the moment a real cost lands:\n"
                  "  python core/rates.py --score <lead> --mine <yours> --actual <real>")
            return 0
        print("PRICING ACCURACY over %d scored job(s)" % s["n"])
        print("  median error   %+.2f%%   (positive = priced high)" % s["median_pct"])
        print("  mean abs error  %.2f%%" % s["mean_abs_pct"])
        print("  within 5%%       %d of %d" % (s["within_5pct"], s["n"]))
        print("  high %d / low %d" % (s["high"], s["low"]))
        for e in s["entries"]:
            print("   %-22s priced %10.2f  actual %10.2f  %+7.2f%%  %s"
                  % (e["lead"][:22], e["priced"], e["actual"], e["pct"], e["basis"][:26]))
        return 0

    if a.score:
        if a.mine is None or a.actual is None:
            print("--score needs both --mine and --actual")
            return 1
        e = score(a.score, a.mine, a.actual, a.basis, a.note)
        print("scored %s: priced %.2f against %.2f -> %+.2f%% (%s)"
              % (e["lead"], e["priced"], e["actual"], e["pct"],
                 "HIGH" if e["delta"] > 0 else "low" if e["delta"] < 0 else "exact"))
        return 0

    if a.lookup is not None or a.supplier:
        hits = lookup(a.lookup or "", a.supplier)
        if not hits:
            print("nothing in the register matches that")
            return 1
        print("%d benchmark(s) - EVIDENCE, not firm prices\n" % len(hits))
        for r in hits[:20]:
            print("%-10s %-46s %s" % (r["supplier"], r["category"][:46], r["unit"]))
            print("   median %9.2f   range %.2f - %.2f   from %d line(s)"
                  % (r["median"], r["min"], r["max"], r.get("lineCount", 0)))
            src = r.get("sources") or []
            if src:
                print("   seen in: " + ", ".join(
                    "%s %s" % (s.get("quoteRef"), s.get("quoteDate", "")) for s in src[:3]))
            print()
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Was ADDER_FACTOR_LARGE = 1.25 a rule, or a measurement confound?

Last session measured (unit_rate - frames) / code_value. Above 6 m2 that came
out at 1.250. But unit_rate - frames is NOT the adder: it is the adder PLUS
Glass PLUS Additional PLUS CW, wherever those columns carry money. If large
units carry more glass and extras money - which they must, being bigger - then
the old metric is inflated on exactly the lines the rule was fitted to.

This computes both metrics on the same lines and shows where they part.
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as A
import mary_pricing as engine

docs = A.collect_docs()
old, new, both = [], [], []
for d in docs:
    comps = [c for c in ("frames", "glass", "additional", "cw") if c in d["cols"]]
    if "frames" not in comps:
        continue
    for r in d["rows"]:
        if not r["code"] or r["frames"] is None or not r["area"]:
            continue
        cv = engine.CODE_VALUE.get(r["code"])
        if not cv:
            continue
        o = (r["unit_rate"] - r["frames"]) / cv
        used = sum(r[c] for c in comps if r[c] is not None)
        n = (r["unit_rate"] - used) / cv
        extras = used - r["frames"]
        both.append({"doc": d["file"], "area": r["area"], "old": o, "new": n,
                     "extras": extras, "code": r["code"]})

BRANDON = "brandon"
for label, sel in (("ALL LINES", both),
                   ("EXCLUDING BRANDON", [x for x in both if BRANDON not in x["doc"].lower()])):
    print("=" * 78)
    print(label)
    print("%-10s %6s %14s %14s %14s" % ("BAND", "n", "old metric", "true adder", "median extras"))
    for lo, hi in ((0, 1.5), (1.5, 3), (3, 6), (6, 1e9)):
        s = [x for x in sel if lo <= x["area"] < hi]
        if not s:
            continue
        print("%-10s %6d %14.3f %14.3f %14.2f"
              % ("%g-%g" % (lo, hi if hi < 1e9 else 99), len(s),
                 statistics.median([x["old"] for x in s]),
                 statistics.median([x["new"] for x in s]),
                 statistics.median([x["extras"] for x in s])))
    print()

print("=" * 78)
print("Lines over 6 m2, EXCLUDING Brandon - what fraction sit exactly on 0.75?")
s = [x for x in both if x["area"] > 6 and BRANDON not in x["doc"].lower()]
on75 = [x for x in s if abs(x["new"] - 0.75) < 0.02]
on125 = [x for x in s if abs(x["new"] - 1.25) < 0.02]
print("  n=%d   exactly 0.75: %d (%.0f%%)   exactly 1.25: %d (%.0f%%)"
      % (len(s), len(on75), 100.0 * len(on75) / len(s), len(on125),
         100.0 * len(on125) / len(s)))
print("  old metric on those same lines: median %.3f" % statistics.median([x["old"] for x in s]))

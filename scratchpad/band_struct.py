# -*- coding: utf-8 -*-
"""Does the engine need size bands at all, given the code already says the size?

LEARNED_EDGES = (2.0, 5.0) was chosen against the register's 1.5/3/6 and against
1.5/4, and splitting FINER was tested and is clearly worse - 508 mined lines will
not support more than three buckets per code. What was never tested is COARSER.

The reason to think it might win is that the product code already encodes size:
SAW / MAW / LAW is small / medium / large aluminium window, SPVC / MPVC / LPVC the
uPVC equivalents. So `code|band` bands a thing that is already banded, and the
buckets show it - MAW|<2m2 is n=67 against MAW|2-5m2 n=10, LAW|2-5m2 is n=63
against LAW|<2m2 n=5. The band is not splitting these codes down the middle; it is
shaving a thin tail off each, and a thin tail is where MIN_LEARNED_N drops the
line through to the register.

Arms are the band structure alone, everything else held constant, leave-one-JOB-
out because that is what this lab decides on."""
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import mary_backtest as bt          # noqa: E402
import mary_pricing as engine       # noqa: E402
from corpus_cache import docs       # noqa: E402

ARMS = [("none - one bucket per code", ()),
        ("(2.0,)", (2.0,)),
        ("(5.0,)", (5.0,)),
        ("(2.0, 5.0)  CURRENT", (2.0, 5.0)),
        ("(1.5, 3.0, 6.0)  register", (1.5, 3.0, 6.0)),
        ("(1.5, 4.0)", (1.5, 4.0)),
        ("(3.0,)", (3.0,))]


def band_for(edges):
    def f(area):
        if not edges:
            return "all"
        for i, e in enumerate(edges):
            if area < e:
                return "<%g" % e if i == 0 else "%g-%g" % (edges[i - 1], e)
        return ">%g" % edges[-1]
    return f


print("%-30s %10s %9s %9s %7s %7s %s"
      % ("BANDS", "MEAN ABS", "MEDIAN", "BIAS", "w/in10", "w/in25", "BUCKETS"))
results = {}
for label, edges in ARMS:
    old = engine.learned_band_of
    engine.learned_band_of = band_for(edges)
    try:
        groups = {}
        for d in docs:
            groups.setdefault(bt.job_key(d), []).append(d)
        rows = []
        for key, group in groups.items():
            train = [d for d in docs if bt.job_key(d) != key]
            rates = bt.learn(train)
            facs = bt.learn_supplier_factors(train, rates)
            for d in group:
                s = bt.score_doc(d, learned=rates, factors=facs)
                if s:
                    rows.append(s)
        nb = len(bt.learn(docs))
    finally:
        engine.learned_band_of = old
    a = [abs(s["err_pct"]) for s in rows]
    g = [s["err_pct"] for s in rows]
    results[label] = {s["file"]: s["err_pct"] for s in rows}
    print("%-30s %9.2f%% %8.2f%% %+8.2f%% %4d/%-2d %4d/%-2d %d"
          % (label, statistics.fmean(a), statistics.median(a), statistics.fmean(g),
             sum(1 for x in a if x <= 10), len(a),
             sum(1 for x in a if x <= 25), len(a), nb))

cur = results["(2.0, 5.0)  CURRENT"]
best = min((k for k in results if k != "(2.0, 5.0)  CURRENT"),
           key=lambda k: statistics.fmean(abs(v) for v in results[k].values()))
print("\nHEAD TO HEAD, current against %s - so a win is not one job's luck" % best)
b = results[best]
w = l = 0
for f in sorted(cur, key=lambda f: abs(b[f]) - abs(cur[f])):
    d = abs(b[f]) - abs(cur[f])
    if abs(d) < 0.05:
        continue
    w += d < 0
    l += d > 0
    print("  %-52s %+7.1f -> %+7.1f  %s" % (f[:52], cur[f], b[f], "better" if d < 0 else "WORSE"))
print("  %s is better on %d documents and worse on %d" % (best, w, l))

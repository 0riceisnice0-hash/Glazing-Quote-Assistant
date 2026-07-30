# -*- coding: utf-8 -*-
"""Does repetition buy a discount, and can the engine see it?

Trafalgar House prices 58 identical 1.92m2 MPVC windows at GBP 508.90 each -
GBP 108.8/m2 of supply against a learned MPVC|<2m2 of GBP 221.66, so half the
archive rate, and the engine is +42.6% on every one of those lines. Brandon
Estate is the same shape at 2,202 units. Georgie's is the opposite: singles and
pairs of small windows at GBP 955-1,940/m2, and the engine is 37-55% UNDER.

The commercial reason is obvious and it is not a mystery to any estimator: a
supplier prices a run of one window differently from a run of sixty, and the
install is a different job too. The engine has no term for it at all - it prices
by code and area only, so a one-off and a sixty-off get the same rate.

Measure the ratio of a line's own supply GBP/m2 to the median for its code and
band, against the line's quantity. Code and size are already held constant by
construction, which is what makes this a fair test."""
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
base = bt.learn(docs)

rows = []
for d in docs:
    units = sum(l["qty"] for l in d["lines"])
    for l in d["lines"]:
        money = bt.supply_money(l)
        if not money or l["area"] <= 0:
            continue
        key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
        b = base.get(key)
        if not b or not b["median_per_m2"] or b["n"] < engine.MIN_LEARNED_N:
            continue
        rows.append({"ratio": (money / l["area"]) / b["median_per_m2"],
                     "qty": l["qty"], "units": units, "file": d["file"], "code": l["code"]})

print("%d lines with a code+band median behind them\n" % len(rows))

print("BY LINE QUANTITY - ratio of the line's own supply rate to its band median")
BANDS = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 16), (17, 40), (41, 10 ** 9)]
print("%-12s %6s %10s %10s" % ("LINE QTY", "n", "MED RATIO", "MEAN RATIO"))
for lo, hi in BANDS:
    sel = [r for r in rows if lo <= r["qty"] <= hi]
    if not sel:
        continue
    print("%-12s %6d %10.3f %10.3f"
          % ("%d-%d" % (lo, hi) if lo != hi else str(lo), len(sel),
             statistics.median(r["ratio"] for r in sel),
             statistics.fmean(r["ratio"] for r in sel)))

print("\nBY TOTAL UNITS ON THE JOB - a job-level volume effect rather than a line one")
JB = [(0, 10), (11, 25), (26, 60), (61, 150), (151, 10 ** 9)]
print("%-12s %6s %10s %10s %6s" % ("JOB UNITS", "n", "MED RATIO", "MEAN RATIO", "JOBS"))
for lo, hi in JB:
    sel = [r for r in rows if lo <= r["units"] <= hi]
    if not sel:
        continue
    print("%-12s %6d %10.3f %10.3f %6d"
          % ("%d-%d" % (lo, hi), len(sel),
             statistics.median(r["ratio"] for r in sel),
             statistics.fmean(r["ratio"] for r in sel),
             len({r["file"] for r in sel})))

# A rate effect should be a straight line against log(qty) if it is a real
# volume curve. Fit it and see how much of the scatter it actually explains.
print("\nIS IT A CURVE? least squares of log(ratio) on log(line qty)")
xs = [math.log(r["qty"]) for r in rows if r["qty"] > 0 and r["ratio"] > 0]
ys = [math.log(r["ratio"]) for r in rows if r["qty"] > 0 and r["ratio"] > 0]
n = len(xs)
mx, my = statistics.fmean(xs), statistics.fmean(ys)
sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
sxx = sum((x - mx) ** 2 for x in xs)
slope = sxy / sxx
resid = [y - (my + slope * (x - mx)) for x, y in zip(xs, ys)]
r2 = 1 - sum(e * e for e in resid) / sum((y - my) ** 2 for y in ys)
print("  slope %+.4f  (ratio multiplies by %.3f each time quantity doubles)"
      % (slope, 2 ** slope))
print("  R^2 %.4f over %d lines" % (r2, n))
print("  a doubling from 1 to 64 unit(s) would mean x%.3f" % (64 ** slope))

print("\nSAME FIT, BUT PER JOB MEDIAN - so 58 identical Trafalgar lines cannot carry it")
per = {}
for r in rows:
    per.setdefault(r["file"], []).append(r)
jx, jy = [], []
for f, rs in per.items():
    q = statistics.median(r["qty"] for r in rs)
    ra = statistics.median(r["ratio"] for r in rs)
    if q > 0 and ra > 0:
        jx.append(math.log(q))
        jy.append(math.log(ra))
mx, my = statistics.fmean(jx), statistics.fmean(jy)
sxy = sum((x - mx) * (y - my) for x, y in zip(jx, jy))
sxx = sum((x - mx) ** 2 for x in jx)
s2 = sxy / sxx
res = [y - (my + s2 * (x - mx)) for x, y in zip(jx, jy)]
r22 = 1 - sum(e * e for e in res) / sum((y - my) ** 2 for y in jy)
print("  slope %+.4f  x%.3f per doubling   R^2 %.4f over %d jobs" % (s2, 2 ** s2, r22, len(jx)))

print("\nthe jobs at the extremes of median line quantity:")
for f, rs in sorted(per.items(), key=lambda kv: -statistics.median(r["qty"] for r in kv[1]))[:5]:
    print("  qty %6.0f  ratio %5.2f  %s"
          % (statistics.median(r["qty"] for r in rs),
             statistics.median(r["ratio"] for r in rs), f[:60]))
print("  ...")
for f, rs in sorted(per.items(), key=lambda kv: statistics.median(r["qty"] for r in kv[1]))[:5]:
    print("  qty %6.0f  ratio %5.2f  %s"
          % (statistics.median(r["qty"] for r in rs),
             statistics.median(r["ratio"] for r in rs), f[:60]))

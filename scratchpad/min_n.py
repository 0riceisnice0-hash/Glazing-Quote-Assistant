# -*- coding: utf-8 -*-
"""How many lines fall through to the register, and is MIN_LEARNED_N right?

A learned rate is used only where its code+band bucket has at least
MIN_LEARNED_N = 6 lines behind it; below that the line drops through to the
supplier-quote register, which scores 19.37% against the learned rates' 13.20%.
Nobody has ever tested the 6.

It matters more than the whole-archive bucket counts suggest, because LEAVE ONE
JOB OUT SHRINKS THE BUCKETS. LAW|<2m2 has n=5 over the whole archive - already
under the threshold - and three of those five lines are Georgie's, which is
-31.0% and on the worst list. Hold Georgie's out and the bucket is n=2.

Arms are the threshold alone, everything else held constant, scored leave-one-
JOB-out because that is what this lab decides on."""
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import mary_backtest as bt          # noqa: E402
import mary_pricing as engine       # noqa: E402
from corpus_cache import docs       # noqa: E402


def loo(min_n):
    old = engine.MIN_LEARNED_N
    engine.MIN_LEARNED_N = min_n
    try:
        groups = {}
        for d in docs:
            groups.setdefault(bt.job_key(d), []).append(d)
        out = []
        for key, group in groups.items():
            train = [d for d in docs if bt.job_key(d) != key]
            rates = bt.learn(train)
            facs = bt.learn_supplier_factors(train, rates)
            for d in group:
                s = bt.score_doc(d, learned=rates, factors=facs)
                if s:
                    out.append(s)
        return out
    finally:
        engine.MIN_LEARNED_N = old


def fell_through(min_n):
    """Lines whose bucket is too thin, counted honestly inside each fold."""
    groups = {}
    for d in docs:
        groups.setdefault(bt.job_key(d), []).append(d)
    n = tot = 0
    for key, group in groups.items():
        rates = bt.learn([d for d in docs if bt.job_key(d) != key])
        for d in group:
            for l in d["lines"]:
                tot += 1
                k = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
                rec = rates.get(k)
                if not rec or rec.get("n", 0) < min_n:
                    n += 1
    return n, tot


print("%-6s %10s %10s %9s %8s %8s %s"
      % ("MIN_N", "MEAN ABS", "MEDIAN", "BIAS", "w/in10", "w/in25", "REGISTER LINES"))
for m in (3, 4, 5, 6, 8, 10):
    rows = loo(m)
    a = [abs(s["err_pct"]) for s in rows]
    g = [s["err_pct"] for s in rows]
    ft, tot = fell_through(m)
    print("%-6d %9.2f%% %9.2f%% %+8.2f%% %5d/%-2d %5d/%-2d %d/%d"
          % (m, statistics.fmean(a), statistics.median(a), statistics.fmean(g),
             sum(1 for x in a if x <= 10), len(a),
             sum(1 for x in a if x <= 25), len(a), ft, tot))

print("\nWHICH BUCKETS SIT NEAR THE THRESHOLD over the whole archive")
rates = bt.learn(docs)
for k, v in sorted(rates.items(), key=lambda kv: kv[1]["n"]):
    if v["n"] <= 12:
        print("  %-14s n=%-3d  GBP%9.2f/m2  (%.2f - %.2f)"
              % (k, v["n"], v["median_per_m2"], v["low"], v["high"]))

# -*- coding: utf-8 -*-
"""Measure the adder the estimator ACTUALLY used, line by line.

Last session derived ADDER_FACTOR_LARGE = 1.25 from the ratio of (unit_rate -
frames) to the code value, taking medians per band. That is an indirect read: it
treats everything in the unit rate that is not Frames as adder, which lumps in
Glass, Additional and CW wherever those columns carry money.

The audit reader pulls all four component columns, so the adder can be had
directly:  adder = unit_rate - (frames + glass + additional + cw).  Divided by
the code value that is the factor the estimator applied on that line, with no
median and no inference. This asks what that number really looks like.
"""
import os
import statistics
import sys
import collections

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as A
import mary_pricing as engine

docs = A.collect_docs()
print("%d documents\n" % len(docs))

rows = []
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
        used = sum(r[c] for c in comps if r[c] is not None)
        adder = r["unit_rate"] - used
        rows.append({"doc": d["file"], "code": r["code"], "area": r["area"],
                     "factor": adder / cv, "adder": adder, "cv": cv, "qty": r["qty"]})

print("%d lines with a full component build-up\n" % len(rows))

BANDS = [(0, 1.5), (1.5, 3), (3, 6), (6, 8), (8, 12), (12, 1e9)]
print("%-12s %6s %9s %9s %9s %9s   %s" % ("AREA BAND", "n", "median", "mean", "p25", "p75", "share at 0.75 / 1.25"))
for lo, hi in BANDS:
    sel = [r for r in rows if lo <= r["area"] < hi]
    if not sel:
        continue
    f = sorted(x["factor"] for x in sel)
    q = lambda p: f[min(len(f) - 1, int(len(f) * p))]
    n075 = sum(1 for x in f if abs(x - 0.75) < 0.02)
    n125 = sum(1 for x in f if abs(x - 1.25) < 0.02)
    print("%-12s %6d %9.3f %9.3f %9.3f %9.3f   %d%% / %d%%"
          % ("%g-%g" % (lo, hi if hi < 1e9 else 99), len(sel), statistics.median(f),
             statistics.fmean(f), q(0.25), q(0.75),
             round(100.0 * n075 / len(f)), round(100.0 * n125 / len(f))))

print("\nLARGE UNITS (>6 m2) BY DOCUMENT - is 1.25 a rule or an average of two habits?")
big = [r for r in rows if r["area"] > 6]
byd = collections.defaultdict(list)
for r in big:
    byd[r["doc"]].append(r["factor"])
print("%-58s %5s %9s %9s" % ("DOCUMENT", "n", "median", "spread"))
for doc, fs in sorted(byd.items(), key=lambda kv: -len(kv[1])):
    print("%-58s %5d %9.3f %9.3f" % (doc[:58], len(fs), statistics.median(fs),
                                     max(fs) - min(fs)))

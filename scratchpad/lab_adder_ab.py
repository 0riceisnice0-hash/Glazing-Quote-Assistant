# -*- coding: utf-8 -*-
"""Does ADDER_FACTOR_LARGE = 1.25 earn its place on jobs it has not seen?

Three folds, constant line set, learned rates re-mined from each training fold
so nothing leaks. The only thing that varies between arms is the constant.

Arms:
  1.25  what the engine does today
  0.75  no large-unit uplift at all - what the documents actually show
  and a sweep, so the shape of the curve is visible rather than two points.
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
print("%d documents\n" % len(docs))

ARMS = [0.75, 0.90, 1.00, 1.10, 1.25, 1.40]
results = {a: [] for a in ARMS}
lines_seen = None

for fold in range(3):
    train = [d for i, d in enumerate(docs) if i % 3 != fold]
    test = [d for i, d in enumerate(docs) if i % 3 == fold]
    rates = bt.learn(train)
    for a in ARMS:
        engine.ADDER_FACTOR_LARGE = a
        scored = [s for s in (bt.score_doc(d, learned=rates) for d in test) if s]
        absol = [abs(s["err_pct"]) for s in scored]
        signed = [s["err_pct"] for s in scored]
        nlines = sum(s["lines_priced"] for s in scored)
        nskip = sum(s["lines_skipped"] for s in scored)
        results[a].append((statistics.fmean(absol), statistics.median(absol),
                           statistics.fmean(signed), nlines, nskip, len(scored)))

print("%-6s | %-28s | %-28s | %-28s | %s"
      % ("ADDER", "fold 0 (mean/med/bias)", "fold 1", "fold 2", "MEAN ABS"))
for a in ARMS:
    r = results[a]
    cells = " | ".join("%5.2f /%5.2f /%+6.2f" % (x[0], x[1], x[2]) for x in r)
    print("%-6.2f | %s | %6.3f" % (a, cells, statistics.fmean([x[0] for x in r])))

print("\nline counts per fold (must be identical across arms for this to be fair):")
for a in ARMS:
    print("  %.2f  lines=%s  skipped=%s" % (a, [x[3] for x in results[a]],
                                            [x[4] for x in results[a]]))

engine.ADDER_FACTOR_LARGE = 1.25

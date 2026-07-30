# -*- coding: utf-8 -*-
"""Is 'small runs low, large runs high' real across the archive, or St Mary's mix?

Two measurements, deliberately independent:
  1. RAW. Does the estimator's own GBP/m2 (Frames / area) fall as area rises?
     If it does, a band median is the rate at the band's median area, so every
     unit below that area is under-priced and every unit above it over-priced -
     inside every band, not just across them.
  2. HONEST. Per-LINE engine error by area bucket, aggregated over all three
     holdout folds, so no line is scored by a rate mined from its own job.
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
print("corpus: %d documents\n" % len(docs))

# ---------------------------------------------------------------- 1. RAW
lines = [l for d in docs for l in d["lines"] if l["frames"] and l["area"] > 0]
print("RAW: the estimator's own Frames GBP/m2 against area  (%d lines)" % len(lines))
BUCKETS = [(0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, 6.0), (6.0, 99)]
print("%-12s %6s %12s %12s %12s" % ("AREA m2", "n", "MED GBP/m2", "MED AREA", "MED FRAMES"))
for lo, hi in BUCKETS:
    sel = [l for l in lines if lo <= l["area"] < hi]
    if not sel:
        continue
    print("%-12s %6d %12s %12.2f %12s"
          % ("%.1f-%.1f" % (lo, hi), len(sel),
             "{:,.2f}".format(statistics.median(l["frames"] / l["area"] for l in sel)),
             statistics.median(l["area"] for l in sel),
             "{:,.2f}".format(statistics.median(l["frames"] for l in sel))))

# Same thing per code, for the codes with enough lines - because a mix of
# products across the size range would fake this effect entirely.
print("\nRAW PER CODE (>=12 lines), median GBP/m2 by area - is the fall within a product?")
by_code = {}
for l in lines:
    by_code.setdefault(l["code"], []).append(l)
for code, ls in sorted(by_code.items(), key=lambda kv: -len(kv[1])):
    if len(ls) < 12:
        continue
    cells = []
    for lo, hi in BUCKETS:
        sel = [l for l in ls if lo <= l["area"] < hi]
        cells.append("%8s" % ("{:,.0f}".format(statistics.median(x["frames"] / x["area"] for x in sel))
                              + "/%d" % len(sel) if sel else "-"))
    print("  %-8s %s" % (code, " ".join(cells)))

# ---------------------------------------------------------------- 2. HONEST
print("\nHONEST: per-line engine error by area, all 3 folds, rates never from the same job")
per_bucket = {}
per_band = {}
for f in range(3):
    train = [d for i, d in enumerate(docs) if i % 3 != f]
    test = [d for i, d in enumerate(docs) if i % 3 == f]
    rates = bt.learn(train)
    for d in test:
        for l in d["lines"]:
            e = bt.engine_price(l, d.get("supplier"), learned=rates)
            if not e or not l["unit_rate"]:
                continue
            err = (e["unit_rate"] - l["unit_rate"]) / l["unit_rate"] * 100.0
            for lo, hi in BUCKETS:
                if lo <= l["area"] < hi:
                    per_bucket.setdefault((lo, hi), []).append(err)
            per_band.setdefault(engine.learned_band_of(l["area"]), []).append(err)

print("%-12s %6s %12s %12s" % ("AREA m2", "n", "MEAN ERR", "MEDIAN ERR"))
for lo, hi in BUCKETS:
    v = per_bucket.get((lo, hi))
    if not v:
        continue
    print("%-12s %6d %11.1f%% %11.1f%%"
          % ("%.1f-%.1f" % (lo, hi), len(v), statistics.fmean(v), statistics.median(v)))

print("\nby the engine's OWN learned band (%s):" % str(engine.LEARNED_EDGES))
for band in ("<2m2", "2-5m2", ">5m2"):
    v = per_band.get(band)
    if v:
        print("  %-8s n=%-5d mean %+7.1f%%  median %+7.1f%%"
              % (band, len(v), statistics.fmean(v), statistics.median(v)))

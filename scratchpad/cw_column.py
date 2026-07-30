# -*- coding: utf-8 -*-
"""The CW column is a WORKING column on a normal unit line, not money in it.

156 of 508 priced lines have frames+glass+additional+cw exceeding their own unit
rate, and the board set that aside on Brandon as 'not per-unit money'. It is not
a Brandon property and it is not a mis-parse. Read the header: the columns are
Frames | Glass | Additional | CW | CW LABOUR | CW SQM. On Oldswinford row 9 the
CW cell is 2,041.67 and CW SQM is 2.40 - and 2,041.67 / 2.402 = GBP 850.00/m2,
which is the engine's own CW_SUPPLY_M2. The cell is the estimator asking 'what
would this opening cost as curtain walling instead', a comparison sitting in a
spare column. It is not in the unit rate, and the unit rate proves it:
  1,003.70 Frames + 210.00 Additional + 487.50 (LAW 650 x 75%) = 1,701.20 exactly.

So test the build-up WITHOUT CW, and test separately whether the CW cell is
just area x 850 - which is what would confirm it is a working column."""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as audit
import mary_pricing as engine

docs = audit.collect_docs()
rows = [dict(r, _file=d["file"]) for d in docs for r in d["rows"]
        if r["code"] and r["area"] and r["unit_rate"] and r["frames"]]
print("%d coded, sized, framed lines\n" % len(rows))


def recon(r, comps):
    want = engine.CODE_VALUE.get(r["code"], 0) * 0.75
    got = r["unit_rate"] - sum(r[c] or 0.0 for c in comps)
    return abs(got - want) <= max(1.0, 0.01 * want)


for comps in (("frames", "glass", "additional", "cw"),
              ("frames", "glass", "additional")):
    n = sum(recon(r, comps) for r in rows)
    print("  adder = 0.75 x code value reconciles on %3d / %d lines   with %s"
          % (n, len(rows), " + ".join(comps)))

print("\nIS THE CW CELL JUST area x GBP850? (that is CW_SUPPLY_M2 = %.0f)" % engine.CW_SUPPLY_M2)
withcw = [r for r in rows if (r["cw"] or 0) > 1.0]
hits = [r for r in withcw if abs(r["cw"] - r["area"] * 850.0) <= max(2.0, 0.01 * r["cw"])]
print("  %d line(s) carry a CW figure; %d of them equal area x 850 to within 1%%" % (len(withcw), len(hits)))
if withcw:
    print("  median CW / area = GBP %.2f/m2" % statistics.median(r["cw"] / r["area"] for r in withcw))
misses = [r for r in withcw if r not in hits]
if misses:
    print("\n  the %d that do NOT - these may be real curtain walling:" % len(misses))
    for r in misses[:14]:
        print("    %-46s %-5s %6.2fm2 cw %12s = %8.1f/m2  unit %12s"
              % (r["_file"][:46], r["code"], r["area"], "{:,.2f}".format(r["cw"]),
                 r["cw"] / r["area"], "{:,.2f}".format(r["unit_rate"])))

print("\nPER DOCUMENT, reconciling WITHOUT cw - anything left is a real question:")
byfile = {}
for r in rows:
    byfile.setdefault(r["_file"], []).append(r)
for f, rs in sorted(byfile.items()):
    bad = [r for r in rs if not recon(r, ("frames", "glass", "additional"))]
    if bad:
        print("  %-54s %3d/%-3d fail  median resid %12s  want %s"
              % (f[:54], len(bad), len(rs),
                 "{:,.2f}".format(statistics.median(
                     r["unit_rate"] - sum(r[c] or 0.0 for c in ("frames", "glass", "additional"))
                     for r in bad)),
                 "{:,.2f}".format(statistics.median(
                     engine.CODE_VALUE.get(r["code"], 0) * 0.75 for r in bad))))

print("\nTHE PRIZE FOR THE ENGINE: supply money the learned rate cannot see.")
good = [r for r in rows if recon(r, ("frames", "glass", "additional"))]
print("  on the %d reconciling lines, Glass + Additional:" % len(good))
BUCKETS = [(0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, 6.0), (6.0, 99)]
print("  %-12s %6s %11s %11s %11s %8s" % ("AREA m2", "n", "FRAMES/m2", "F+G+A/m2", "EXTRA/m2", "EXTRA%"))
for lo, hi in BUCKETS:
    sel = [r for r in good if lo <= r["area"] < hi]
    if not sel:
        continue
    tot = [(r["frames"] + (r["glass"] or 0) + (r["additional"] or 0)) for r in sel]
    print("  %-12s %6d %11.2f %11.2f %11.2f %7.1f%%"
          % ("%.1f-%.1f" % (lo, hi), len(sel),
             statistics.median(r["frames"] / r["area"] for r in sel),
             statistics.median(t / r["area"] for t, r in zip(tot, sel)),
             statistics.median((t - r["frames"]) / r["area"] for t, r in zip(tot, sel)),
             100.0 * statistics.fmean([(t - r["frames"]) / t for t, r in zip(tot, sel) if t])))

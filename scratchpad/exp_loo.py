# -*- coding: utf-8 -*-
"""Leave-one-out, because a 0.20-point win on three positional folds is not evidence.

Arm B (mine the rate from the whole build-up, adder 0.75 flat) beat arm A by
13.68 against 13.88 on the mean of three folds - but it won ONE fold of three and
the folds are positional, which is exactly the shape the board has already been
misled by twice. Leave-one-out scores every one of the 29 documents on rates
mined from the other 28, so every job is a test job and the answer does not
depend on where a file sits in the scan order."""
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp_supply import docs, learn_arm, score  # noqa: E402
import mary_pricing as engine  # noqa: E402

ARMS = [("A  frames only,        1.25 large", False, 1.25),
        ("B  frames+glass+addl,  0.75 flat ", True, 0.75),
        ("C  frames+glass+addl,  1.25 large", True, 1.25),
        ("D  frames only,        0.75 flat ", False, 0.75)]

results = {}
for label, whole, large in ARMS:
    errs = []
    for i in range(len(docs)):
        train = [d for j, d in enumerate(docs) if j != i]
        res = score([docs[i]], learn_arm(train, whole), large)
        if res:
            errs.append((res[0][0], docs[i]["file"]))
    results[label] = errs
    a = [abs(e) for e, _ in errs]
    print("%-36s n=%d  MEAN ABS %6.2f%%  MEDIAN %6.2f%%  BIAS %+6.2f%%  within10 %d  within25 %d"
          % (label, len(errs), statistics.fmean(a), statistics.median(a),
             statistics.fmean([e for e, _ in errs]),
             sum(1 for x in a if x <= 10), sum(1 for x in a if x <= 25)))

print("\nHEAD TO HEAD, A against B, per document - so the win is not one job's luck")
A = dict((f, e) for e, f in results[ARMS[0][0]])
B = dict((f, e) for e, f in results[ARMS[1][0]])
wins = losses = 0
rows = []
for f in A:
    if f not in B:
        continue
    d = abs(B[f]) - abs(A[f])
    rows.append((d, f, A[f], B[f]))
    if d < -0.05:
        wins += 1
    elif d > 0.05:
        losses += 1
print("  B better on %d documents, worse on %d, level on %d\n"
      % (wins, losses, len(rows) - wins - losses))
rows.sort()
print("  %-46s %9s %9s %9s" % ("DOCUMENT", "A", "B", "B-A abs"))
for d, f, a, b in rows[:7]:
    print("  %-46s %+8.1f%% %+8.1f%% %+8.1f" % (f[:46], a, b, d))
print("  %-46s %9s %9s %9s" % ("...", "", "", ""))
for d, f, a, b in rows[-7:]:
    print("  %-46s %+8.1f%% %+8.1f%% %+8.1f" % (f[:46], a, b, d))

print("\nWORST DOCUMENTS UNDER B - where the remaining error lives")
for e, f in sorted(results[ARMS[1][0]], key=lambda x: -abs(x[0]))[:9]:
    n = len([l for d in docs if d["file"] == f for l in d["lines"]])
    print("  %-52s %+8.1f%%  %2d line(s)" % (f[:52], e, n))

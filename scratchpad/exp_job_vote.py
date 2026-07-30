# -*- coding: utf-8 -*-
"""One JOB, one vote in the learned rates - does it help, or only look tidier?

Holding the job out fixed the measurement (13.11 -> 13.58 honest). The separate
question is whether the three Brandon Estate revisions and the two Zelltec
Crownhill revisions should all be MINED. Brandon alone is 93 of 508 lines, so one
estate sets 18% of every rate, and its three revisions agree with each other far
more than they agree with anything else in the archive.

The 30/07 content dedup is the precedent and the warning: it was the right thing to
do and it did NOT improve accuracy, because a median over 500 lines does not notice
8 of them counted twice. 93 is not 8, so this one is worth measuring.

  A  mine every document                     - as it stands
  B  mine one document per job, most lines   - one job one vote
  C  mine every document but cap any one job at 1/6 of a bucket's lines
Scored leave-one-JOB-out in all arms, so the comparison is honest and the only
thing changing is what goes INTO the rates.
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
groups = {}
for d in docs:
    groups.setdefault(bt.job_key(d), []).append(d)
print("%d documents in %d jobs" % (len(docs), len(groups)))
for k, g in groups.items():
    if len(g) > 1:
        print("  %d revisions: %s" % (len(g), " | ".join("%s (%d lines)"
              % (d["file"][:34], len(d["lines"])) for d in g)))

PRIMARY = {}
for k, g in groups.items():
    PRIMARY[k] = sorted(g, key=lambda d: (-len(d["lines"]), -(d["total"] or 0)))[0]["file"]
print("\nprimary document kept per multi-revision job:")
for k, g in groups.items():
    if len(g) > 1:
        print("  %s" % PRIMARY[k])


def learn_capped(train, cap_frac):
    """learn(), but no single job may supply more than cap_frac of a bucket."""
    buckets = {}
    for d in train:
        for l in d["lines"]:
            money = bt.supply_money(l)
            if not money or l["area"] <= 0:
                continue
            key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
            buckets.setdefault(key, []).append((money / l["area"], bt.job_key(d)))
    out = {}
    for key, vals in buckets.items():
        byjob = {}
        for r, j in vals:
            byjob.setdefault(j, []).append(r)
        limit = max(1, int(len(vals) * cap_frac))
        kept = []
        for j, rs in byjob.items():
            rs.sort()
            if len(rs) <= limit:
                kept += rs
            else:
                # keep the job's median-most lines, so capping does not also
                # decide which end of its range survives
                mid = len(rs) // 2
                lo = max(0, mid - limit // 2)
                kept += rs[lo:lo + limit]
        if len(kept) < 3:
            continue
        out[key] = {"median_per_m2": round(statistics.median(kept), 2), "n": len(kept),
                    "low": round(min(kept), 2), "high": round(max(kept), 2)}
    return out


def run(label, mode):
    rows = []
    for k in groups:
        train = [d for d in docs if bt.job_key(d) != k]
        if mode == "primary":
            train = [d for d in train if d["file"] == PRIMARY[bt.job_key(d)]]
        rates = learn_capped(train, 1.0 / 6) if mode == "cap" else bt.learn(train)
        for d in groups[k]:
            s = bt.score_doc(d, learned=rates)
            if s:
                rows.append(s)
    a = [abs(s["err_pct"]) for s in rows]
    H = sum(s["human_items"] for s in rows)
    E = sum(s["engine_items"] for s in rows)
    print("%-42s %8.2f%% %8.2f%% %+8.2f%% %5d/%d %9.2f%% %+8.2f%%"
          % (label, statistics.fmean(a), statistics.median(a),
             statistics.fmean([s["err_pct"] for s in rows]),
             sum(1 for x in a if x <= 10), len(a),
             sum(abs(s["engine_items"] - s["human_items"]) for s in rows) / H * 100.0,
             (E - H) / H * 100.0))
    return rows


print("\nLEAVE-ONE-JOB-OUT in every arm - only what is MINED changes")
print("%-42s %9s %9s %9s %8s %10s %9s"
      % ("ARM", "MEAN ABS", "MEDIAN", "BIAS", "within10", "MONEY ABS", "ARCHIVE"))
A = run("A  mine every document", "all")
B = run("B  mine one document per job", "primary")
C = run("C  mine all, cap one job at 1/6 a bucket", "cap")

for name, X in (("B", B), ("C", C)):
    da = dict((s["file"], s["err_pct"]) for s in A)
    dx = dict((s["file"], s["err_pct"]) for s in X)
    rows = sorted((abs(dx[f]) - abs(da[f]), f, da[f], dx[f]) for f in da if f in dx)
    print("\nA against %s - better on %d, worse on %d, level on %d"
          % (name, sum(1 for r in rows if r[0] < -0.05), sum(1 for r in rows if r[0] > 0.05),
             sum(1 for r in rows if abs(r[0]) <= 0.05)))
    for d, f, a, b in rows[:4] + rows[-4:]:
        print("  %-50s %+8.1f%% %+8.1f%% %+7.1f" % (f[:50], a, b, d))

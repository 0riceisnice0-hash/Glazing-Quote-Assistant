# -*- coding: utf-8 -*-
"""A ROW WHOSE BUILD-UP DOES NOT FOOT HAS COMPONENT CELLS THAT ARE NOT ITS OWN.

Found on the audit side and it has an engine consequence, which is the whole
point of running both halves on one pass. The COMAR Brandon re-price carries the
Elkins revision's component cells VERBATIM - 11 of 11 non-footing rows have
frames and glass identical to an Elkins row to the penny - while its own product
codes (SAD -> DAD/ELAW/MAW/LAW) and its own unit rates were both changed. The
implied adders come out between 292.71 and 1,237.24 against code adders of 412.50
to 1,500.00, so those unit rates were never built by the template's formula at
all. The component cells are simply stale.

AND supply_money() MINES EXACTLY THOSE CELLS. So for 13 of 508 lines the engine
is learning one revision's supply money against another revision's unit rate.
By the lab's own rule - never tune the engine to reproduce a defect - a line
whose build-up does not foot should not be evidence about a rate.

    A  mine every line                                   (CURRENT)
    B  exclude lines whose build-up does not foot
"""
import os, statistics, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

TOL = 1.0   # pounds. Money is written to the penny; a real slip is pounds.


def foots(l):
    """Does unit_rate = frames + glass + additional + adder x code_value?"""
    if l.get("cw") or not l.get("frames"):
        return True
    comp = l["frames"] + (l.get("glass") or 0.0) + (l.get("additional") or 0.0)
    adder = engine.CODE_VALUE.get(l["code"], 0) * engine.adder_factor(l["area"])
    return abs(l["unit_rate"] - (comp + adder)) <= TOL


def learn_filtered(docs, drop_stale):
    buckets = {}
    for d in docs:
        for l in d["lines"]:
            if drop_stale and not foots(l):
                continue
            money = bt.supply_money(l)
            if not money or l["area"] <= 0:
                continue
            key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
            buckets.setdefault(key, []).append(money / l["area"])
    out = {}
    for key, vals in sorted(buckets.items()):
        if len(vals) < 3:
            continue
        out[key] = {"n": len(vals), "median_per_m2": statistics.median(vals)}
    return out


docs = bt.collect()
stale = [(d["file"], l) for d in docs for l in d["lines"] if not foots(l)]
print("%d documents, %d lines, %d do NOT foot" % (len(docs), sum(len(d["lines"]) for d in docs), len(stale)))
from collections import Counter
for f, c in Counter(f for f, _ in stale).most_common():
    print("   %-58.58s %d" % (f, c))

for arm, drop in (("A  mine every line (CURRENT)", False),
                  ("B  exclude non-footing lines", True)):
    groups = {}
    for d in docs:
        groups.setdefault(bt.job_key(d), []).append(d)
    errs = []
    for key, group in groups.items():
        train = [d for d in docs if bt.job_key(d) != key]
        rates = learn_filtered(train, drop)
        facs = bt.learn_supplier_factors(train, rates)
        for d in group:
            s = bt.score_doc(d, learned=rates, factors=facs)
            if s:
                errs.append((s["err_pct"], d["file"]))
    a = [abs(e) for e, _ in errs]
    s_ = [e for e, _ in errs]
    print("\n  %-32s mean abs %6.2f%%  median %6.2f%%  bias %+6.2f%%  within10 %2d/%d"
          % (arm, statistics.fmean(a), statistics.median(a), statistics.fmean(s_),
             sum(1 for x in a if x <= 10), len(a)))
    globals()["r" + arm[0]] = dict((f, e) for e, f in errs)

print("\nPER-DOCUMENT")
win = lose = 0
for f in sorted(rA, key=lambda x: -abs(rA[x])):
    mark = ""
    if abs(rA[f]) - abs(rB[f]) > 0.05:
        win += 1; mark = "  better"
    elif abs(rB[f]) - abs(rA[f]) > 0.05:
        lose += 1; mark = "  <-- WORSE"
    if mark:
        print("  %-56.56s %+8.1f -> %+8.1f%s" % (f, rA[f], rB[f], mark))
print("\n  B better on %d documents, worse on %d" % (win, lose))

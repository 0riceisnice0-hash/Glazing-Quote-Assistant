# -*- coding: utf-8 -*-
"""The derived supplier factors exist and the learned-rate path ignores them.

learn_supplier_factors() measures how dear each supplier runs against the
all-supplier rate for the same code and band, and writes it to
data/learned-rates.json. It is used in mary_pricing.derived_factors(), which is
reached from find_rate() - the REGISTER path. But engine_price() returns as soon
as it finds a learned rate, and a learned rate is per code and band across ALL
suppliers. So on the 508 lines that have a learned rate, which is all of them,
the measured supplier effect is never applied to anything.

Three of the four factors are 1.00 or within a whisker (4Ali 1.000, BSW 1.001,
Aplus 1.006), so this can only matter through TruFrame at 0.860 - and TruFrame's
Trafalgar House is +29.7% over, the worst over-pricing in the archive. Which is
also the risk: 17 of TruFrame's 26 lines ARE Trafalgar House, so held out
honestly the factor is measured from 9 lines of other work, and if it collapses
the arm is worthless.

  A  learned rate as it stands
  B  learned rate x derived supplier factor, factor re-mined inside the fold
  C  as B but requiring 12 lines rather than 8 before a factor is trusted
Leave-one-JOB-out throughout.
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


def score(d, rates, factors):
    e_t = h_t = 0.0
    n = 0
    key = bt._supplier_key(d.get("supplier"))
    rec = factors.get(key) if factors else None
    f = rec["factor"] if rec and rec.get("applied") else 1.0
    for l in d["lines"]:
        e = bt.engine_price(l, d.get("supplier"), learned=rates)
        if not e:
            continue
        unit = e["supply"] * f + (e["unit_rate"] - e["supply"])
        e_t += unit * l["qty"]
        h_t += l["unit_rate"] * l["qty"]
        n += 1
    return ((e_t - h_t) / h_t * 100.0, f) if n and h_t else None


def agree_only(train, rates, factors, tol):
    """Drop any supplier whose separate per-JOB medians do not agree.

    Aplus's factor is 0.894, 1.002 or 1.028 depending on which job is held out,
    and that instability is where every loss in arm B comes from. TruFrame's is
    0.859 or 0.910 - two independent jobs saying the same thing. A factor worth
    applying should not depend on which document you happened to leave out."""
    per = {}
    for d in train:
        key = bt._supplier_key(d.get("supplier"))
        if not key:
            continue
        for l in d["lines"]:
            money = bt.supply_money(l)
            if not money or l["area"] <= 0:
                continue
            b = rates.get("%s|%s" % (l["code"], engine.learned_band_of(l["area"])))
            if not b or not b["median_per_m2"]:
                continue
            per.setdefault(key, {}).setdefault(bt.job_key(d), []).append(
                (money / l["area"]) / b["median_per_m2"])
    out = {}
    for key, rec in factors.items():
        meds = [statistics.median(v) for v in per.get(key, {}).values() if len(v) >= 3]
        if len(meds) >= 2 and max(meds) / max(1e-9, min(meds)) <= tol:
            out[key] = rec
    return out


def run(label, mode, min_lines=8, agree=None):
    rows = []
    old = bt.MIN_SUPPLIER_LINES
    bt.MIN_SUPPLIER_LINES = min_lines
    try:
        for k in groups:
            train = [d for d in docs if bt.job_key(d) != k]
            rates = bt.learn(train)
            factors = bt.learn_supplier_factors(train, rates) if mode else {}
            if agree:
                factors = agree_only(train, rates, factors, agree)
            for d in groups[k]:
                r = score(d, rates, factors)
                if r:
                    rows.append((r[0], d["file"], r[1], d.get("supplier")))
    finally:
        bt.MIN_SUPPLIER_LINES = old
    a = [abs(e) for e, _, _, _ in rows]
    print("%-52s %8.2f%% %8.2f%% %+8.2f%% %5d/%d"
          % (label, statistics.fmean(a), statistics.median(a),
             statistics.fmean([e for e, _, _, _ in rows]),
             sum(1 for x in a if x <= 10), len(a)))
    return rows


print("LEAVE-ONE-JOB-OUT, factors re-mined inside every fold")
print("%-52s %9s %9s %9s %8s" % ("ARM", "MEAN ABS", "MEDIAN", "BIAS", "within10"))
A = run("A  learned rate as it stands", False)
B = run("B  learned rate x derived supplier factor", True)
C = run("C  as B, 12 lines needed before a factor is trusted", True, 12)
D = run("D  as B, per-job medians must agree within 1.25", True, 8, 1.25)
E = run("E  as B, per-job medians must agree within 1.15", True, 8, 1.15)

print("\nWHAT FACTOR EACH DOCUMENT ACTUALLY GOT UNDER B, where it is not 1.00")
da = dict((f, e) for e, f, _, _ in A)
for e, f, fac, sup in sorted(B, key=lambda r: r[2]):
    if abs(fac - 1.0) > 0.001:
        print("  %-46s %-10s x%.3f   %+7.1f%% -> %+7.1f%%"
              % (f[:46], str(sup)[:10], fac, da[f], e))

for name, X in (("B", B), ("D", D), ("E", E)):
    dx = dict((f, e) for e, f, _, _ in X)
    rows = sorted((abs(dx[f]) - abs(da[f]), f, da[f], dx[f]) for f in da if f in dx)
    moved = [r for r in rows if abs(r[0]) > 0.05]
    print("\nA against %s - better on %d, worse on %d, unmoved on %d"
          % (name, sum(1 for r in rows if r[0] < -0.05),
             sum(1 for r in rows if r[0] > 0.05), len(rows) - len(moved)))
    for d, f, a, b in moved:
        print("  %-50s %+8.1f%% %+8.1f%% %+7.1f" % (f[:50], a, b, d))

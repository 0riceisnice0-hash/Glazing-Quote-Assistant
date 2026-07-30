# -*- coding: utf-8 -*-
"""Learn a product factor from the section heading, and test it leave-one-out.

The heading above a block of lines says what the product IS - 'External Steel
Door', 'Aluminium Sliding Sash Windows', 'SMA Smart Wall Aluminium Doors &
Screens' - and the engine prices on code and area alone, so a Strongdoor steel
security door and a Sheerline aluminium door with the same code and size get the
same rate. Measured against the code+band median, 'steel' runs x1.677 over 9
lines in 3 jobs, 'sliding sash' x3.23, 'fd30' x2.30.

THE VOCABULARY IS FIXED IN ADVANCE, from what the words mean rather than from
which of them helped, because picking keywords by result is how you overfit 29
documents. Generic words - door, window, aluminium - are deliberately excluded:
they measure 1.000 and would only dilute a real match.

GUARDS, all three needed:
  - at least MIN_LINES lines behind a factor
  - at least 2 DISTINCT JOBS, so no single document can teach a factor
  - inside a plausible band, or it is a mis-parse rather than a product
Factors are re-mined per fold from the training documents only."""
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from headings import headings_for, paths  # noqa: E402
import mary_backtest as bt  # noqa: E402
import mary_pricing as engine  # noqa: E402

VOCAB = ["steel", "timber", "sliding sash", "louvre", "tilt", "t&t", "secondary",
         "curtain wall", "shopfront", "coupled", "entrance", "communal",
         "fd30", "fd60", "fire", "sheerline", "liniar", "smart wall", "technal",
         "comar", "senior", "modeal", "strongdor", "sma "]
MIN_LINES = 6
MIN_JOBS = 2
PLAUSIBLE = (0.55, 2.60)

docs = bt.collect()
for d in docs:
    hm = headings_for(paths[d["file"]])
    used = {}
    for l in d["lines"]:
        k = round(l["unit_rate"], 2)
        i = used.get(k, 0)
        used[k] = i + 1
        hs = hm.get(k) or [""]
        l["heading"] = hs[i] if i < len(hs) else hs[-1]
print("corpus %d docs, headings attached\n" % len(docs))


def keywords(head):
    h = (head or "").lower()
    return [k for k in VOCAB if k in h]


def learn_factors(train, base, verbose=False):
    obs = {}
    for d in train:
        for l in d["lines"]:
            money = bt.supply_money(l)
            if not money or l["area"] <= 0:
                continue
            b = base.get("%s|%s" % (l["code"], engine.learned_band_of(l["area"])))
            if not b or b["n"] < engine.MIN_LEARNED_N or not b["median_per_m2"]:
                continue
            ratio = (money / l["area"]) / b["median_per_m2"]
            for k in keywords(l["heading"]):
                obs.setdefault(k, []).append((ratio, d["file"]))
    out = {}
    for k, vals in obs.items():
        jobs = len({f for _, f in vals})
        if len(vals) < MIN_LINES or jobs < MIN_JOBS:
            continue
        f = statistics.median(r for r, _ in vals)
        if not PLAUSIBLE[0] <= f <= PLAUSIBLE[1]:
            continue
        out[k] = {"factor": round(f, 3), "n": len(vals), "jobs": jobs}
    if verbose:
        for k, v in sorted(out.items(), key=lambda kv: -abs(math.log(kv[1]["factor"]))):
            print("    %-14s x%.3f  n=%-4d jobs=%d" % (k, v["factor"], v["n"], v["jobs"]))
    return out


print("FACTORS LEARNED FROM THE WHOLE CORPUS (for inspection only, not scored):")
learn_factors(docs, bt.learn(docs), verbose=True)


def score(test, rates, factors):
    out = []
    for d in test:
        e_t = h_t = 0.0
        n = 0
        for l in d["lines"]:
            key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
            rec = rates.get(key)
            if rec and rec["n"] >= engine.MIN_LEARNED_N:
                rate = rec["median_per_m2"]
            else:
                fam = "aluminium door, glazed" if l["code"] in ("SAD", "DAD", "SUPD", "DUPD") \
                    else "aluminium casement window, glazed"
                r = engine.find_rate(fam, l["area"], None, d.get("supplier") or "")
                if r is None:
                    continue
                rate = r.rate
            cands = [factors[k] for k in keywords(l["heading"]) if k in factors]
            if cands:
                # Most evidence wins, the same rule find_rate uses to choose
                # between competing register categories.
                rate *= max(cands, key=lambda c: c["n"])["factor"]
            u = l["area"] * rate + engine.CODE_VALUE.get(l["code"], 0) * engine.adder_factor(l["area"])
            e_t += u * l["qty"]
            h_t += l["unit_rate"] * l["qty"]
            n += 1
        if n and h_t:
            out.append(((e_t - h_t) / h_t * 100.0, d["file"]))
    return out


print("\nLEAVE-ONE-OUT, every document scored on the other 28")
res = {}
for label, use in (("without product factor", False), ("WITH product factor  ", True)):
    errs = []
    for i in range(len(docs)):
        train = [d for j, d in enumerate(docs) if j != i]
        base = bt.learn(train)
        facs = learn_factors(train, base) if use else {}
        errs += score([docs[i]], base, facs)
    res[label] = dict((f, e) for e, f in errs)
    a = [abs(e) for e, _ in errs]
    print("  %-24s n=%d  MEAN ABS %6.2f%%  MEDIAN %6.2f%%  BIAS %+6.2f%%  w10 %d  w25 %d"
          % (label, len(errs), statistics.fmean(a), statistics.median(a),
             statistics.fmean([e for e, _ in errs]),
             sum(1 for x in a if x <= 10), sum(1 for x in a if x <= 25)))

A, B = res["without product factor"], res["WITH product factor  "]
rows = sorted(((abs(B[f]) - abs(A[f]), f, A[f], B[f]) for f in A if f in B))
w = sum(1 for d, *_ in rows if d < -0.05)
lo = sum(1 for d, *_ in rows if d > 0.05)
print("\n  better on %d documents, worse on %d, level on %d" % (w, lo, len(rows) - w - lo))
print("  %-48s %9s %9s %8s" % ("DOCUMENT", "WITHOUT", "WITH", "CHANGE"))
for d, f, a, b in rows[:6]:
    print("  %-48s %+8.1f%% %+8.1f%% %+7.1f" % (f[:48], a, b, d))
print("  %-48s" % "...")
for d, f, a, b in rows[-4:]:
    print("  %-48s %+8.1f%% %+8.1f%% %+7.1f" % (f[:48], a, b, d))

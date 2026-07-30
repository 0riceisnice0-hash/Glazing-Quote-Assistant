# -*- coding: utf-8 -*-
"""Model the extras money directly instead of hiding it in the adder.

The engine predicts   unit_rate = area x learned_rate + CODE_VALUE x adder.
The document builds   unit_rate = frames + glass + additional + cw + 0.75 x CODE_VALUE.

The learned rate is mined from the Frames column alone, so the engine has NO
term at all for glass, additional and CW money. Below 6 m2 that costs nothing -
the median of those columns is 0.00. Above 6 m2 the median is 1,000.00, and
ADDER_FACTOR_LARGE = 1.25 is what happens when that 1,000 is charged to the
code value instead (0.75 + 1000/2000 = 1.25, and the median large unit is a DAD
with a code value of 2000).

So: does a flat extras term, LEARNED from the training fold, beat the fudge?
Arm A  adder 1.25 above 6 m2, no extras term      (the engine today)
Arm B  adder 0.75 everywhere, no extras term      (what the documents show)
Arm C  adder 0.75 everywhere + learned flat extras above 6 m2
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_quote_audit as A
import mary_pricing as engine

LARGE = 6.0


def learn_extras(train_files, audit_docs):
    """Median of (glass + additional + cw) on large units, from training jobs only."""
    vals = []
    for d in audit_docs:
        if d["file"] not in train_files:
            continue
        comps = [c for c in ("glass", "additional", "cw") if c in d["cols"]]
        if not comps or "frames" not in d["cols"]:
            continue
        for r in d["rows"]:
            if not r["code"] or r["frames"] is None or not r["area"] or r["area"] <= LARGE:
                continue
            ex = sum(r[c] for c in comps if r[c] is not None)
            # Reject lines whose components do not reconcile to the unit rate.
            # On the Brandon documents frames+glass+additional+cw EXCEEDS the
            # unit rate, so the columns cannot mean per-unit money there, and
            # including them pulled the learned extras from 1,000 to 5,704.
            # This is a property of the line, not a list of filenames.
            cv = engine.CODE_VALUE.get(r["code"], 0)
            resid = r["unit_rate"] - (r["frames"] + ex)
            if cv and abs(resid / cv - 0.75) > 0.05:
                continue
            vals.append(ex)
    return statistics.median(vals) if vals else 0.0


def score(doc, rates, adder_large, extras):
    engine.ADDER_FACTOR_LARGE = adder_large
    eng = hum = 0.0
    n = 0
    for l in doc["lines"]:
        e = bt.engine_price(l, doc.get("supplier"), learned=rates)
        if not e:
            continue
        n += 1
        u = e["unit_rate"] + (extras if l["area"] > LARGE else 0.0)
        eng += u * l["qty"]
        hum += l["unit_rate"] * l["qty"]
    if not n or not hum:
        return None, 0
    return (eng - hum) / hum * 100.0, n


docs = bt.collect()
audit_docs = A.collect_docs()
print("%d backtest docs, %d audit docs\n" % (len(docs), len(audit_docs)))

ARMS = [("A adder 1.25", 1.25, False), ("B adder 0.75", 0.75, False),
        ("C 0.75+extras", 0.75, True)]
out = {a[0]: [] for a in ARMS}
for fold in range(3):
    train = [d for i, d in enumerate(docs) if i % 3 != fold]
    test = [d for i, d in enumerate(docs) if i % 3 == fold]
    rates = bt.learn(train)
    ex = learn_extras(set(d["file"] for d in train), audit_docs)
    for label, af, use_ex in ARMS:
        errs, lines = [], 0
        for d in test:
            e, n = score(d, rates, af, ex if use_ex else 0.0)
            if e is not None:
                errs.append(e)
                lines += n
        out[label].append((statistics.fmean([abs(x) for x in errs]),
                           statistics.median([abs(x) for x in errs]),
                           statistics.fmean(errs), lines, ex))

print("%-15s | %-24s | %-24s | %-24s | %s" % ("ARM", "fold 0", "fold 1", "fold 2", "MEAN ABS"))
for label, _, _ in ARMS:
    r = out[label]
    cells = " | ".join("%5.2f /%5.2f /%+6.2f" % (x[0], x[1], x[2]) for x in r)
    print("%-15s | %s | %6.3f" % (label, cells, statistics.fmean([x[0] for x in r])))
print("\nlearned extras per fold (GBP, from training jobs only): %s"
      % [round(r[4], 2) for r in out["C 0.75+extras"]])
print("lines scored per fold: %s" % [r[3] for r in out["A adder 1.25"]])
engine.ADDER_FACTOR_LARGE = 1.25

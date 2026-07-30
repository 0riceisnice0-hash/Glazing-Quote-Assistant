# -*- coding: utf-8 -*-
"""Does the section heading pay for itself on jobs the engine has never seen?

The heading names the system and the product - 'Strongdor Steel Doors', 'Aluminium
Sliding Sash Windows', 'SMA Smart Wall Aluminium Doors & Screens' - and the product
code beneath it only says window-or-door, small-medium-large. Measured across the
archive the full headings separate hard (sliding sash 3.23, internal steel 2.22,
smart wall 1.45, modeal coupled 0.60) while single generic words do not (door 1.000,
window 1.000, sheerline 0.970, upvc 1.004).

THE TRAP TO AVOID IS THE ONE THE BOARD ALREADY NAMED. Fitting a factor per heading
on all 29 documents and then reporting the archive error would be the 1.25 mistake
again: a heading appearing in ONE job is that job's identity, and a factor mined
from it reproduces the job by memorising it. So:
  - the vocabulary is fixed BEFORE looking at any factor - product types and system
    names an estimator would write, chosen from the heading list, not from what
    helps the score;
  - every factor is re-mined from the TRAINING documents only, inside the fold;
  - a keyword must appear in at least JOBS_GATE distinct training jobs, so a
    heading unique to the document under test can never price it.
Arms are gates, not vocabularies, so the comparison is honest.
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

# Fixed vocabulary. Product type first, then system/brand.
VOCAB = ["steel", "sliding sash", "secondary", "heritage", "louvre", "curtain wall",
         "shopfront", "patio", "coupled", "tilt & turn", "t&t", "aov", "screen",
         "casement", "entrance", "communal", "fd30", "horizontal slid",
         "sheerline", "comar", "modeal", "liniar", "alunet", "technal",
         "smart wall", "shopline", "strongdor", "stii", "sma"]


def keywords_in(text):
    return [k for k in VOCAB if k in text]


def learn_text(train, base, jobs_gate, line_gate, only=None, agree=None):
    """Median residual against the code|band median, per keyword.

    `only` restricts the vocabulary. `agree` demands that the keyword's separate
    per-JOB medians agree within that ratio before the factor is trusted - the
    test for whether a heading means the same thing in somebody else's document
    or is simply that one job's identity."""
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
            for k in keywords_in(l["text"]):
                if only and k not in only:
                    continue
                obs.setdefault(k, []).append((ratio, d["file"]))
    out = {}
    for k, vals in obs.items():
        if len(vals) < line_gate or len({f for _, f in vals}) < jobs_gate:
            continue
        if agree:
            per_job = {}
            for r, f in vals:
                per_job.setdefault(f, []).append(r)
            meds = [statistics.median(v) for v in per_job.values() if len(v) >= 2]
            if len(meds) >= 2 and max(meds) / max(1e-9, min(meds)) > agree:
                continue
        out[k] = round(statistics.median(r for r, _ in vals), 3)
    return out


def text_factor(text, factors):
    """One factor per line: the keyword furthest from 1.00 wins.

    Not a product of all of them. 'Strongdor Steel Doors' matches both 'steel'
    and 'strongdor' and they are the same fact about the same door; multiplying
    would charge it twice, which is precisely how ADDER_FACTOR_LARGE went wrong."""
    hits = [factors[k] for k in keywords_in(text) if k in factors]
    return max(hits, key=lambda f: abs(f - 1.0)) if hits else 1.0


def score(docs_test, rates, factors):
    out = []
    for d in docs_test:
        e_t = h_t = 0.0
        n = 0
        for l in d["lines"]:
            e = bt.engine_price(l, d.get("supplier"), learned=rates)
            if not e:
                continue
            f = text_factor(l["text"], factors)
            unit = e["supply"] * f + (e["unit_rate"] - e["supply"])
            e_t += unit * l["qty"]
            h_t += l["unit_rate"] * l["qty"]
            n += 1
        if n and h_t:
            out.append(((e_t - h_t) / h_t * 100.0, d["file"]))
    return out


docs = bt.collect()
print("corpus %d documents, %d lines\n" % (len(docs), sum(len(d["lines"]) for d in docs)))

print("WHAT THE VOCABULARY MEASURES on the whole archive, for reading only - every")
print("number below is re-mined inside the fold and these are NOT the ones used.")
allbase = bt.learn(docs)
whole = learn_text(docs, allbase, 1, 3)
print("  %-16s %8s %6s %6s" % ("KEYWORD", "FACTOR", "LINES", "JOBS"))
obs = {}
for d in docs:
    for l in d["lines"]:
        for k in keywords_in(l["text"]):
            obs.setdefault(k, set()).add(d["file"])
for k, f in sorted(whole.items(), key=lambda kv: -abs(kv[1] - 1.0)):
    nl = sum(1 for d in docs for l in d["lines"] if k in l["text"])
    print("  %-16s %8.3f %6d %6d" % (k, f, nl, len(obs[k])))

ARMS = [("A  no text factor - the engine as it stands", None, None),
        ("B  jobs >= 2, lines >= 6", 2, 6),
        ("C  jobs >= 3, lines >= 6", 3, 6),
        ("D  jobs >= 4, lines >= 8", 4, 8),
        ("E  jobs >= 2, lines >= 3", 2, 3),
        ("F  STEEL ONLY - the board's standing suggestion", 2, 3, ["steel", "strongdor"]),
        ("G  jobs >= 2, lines >= 6, per-job medians agree 1.3", 2, 6, None, 1.3),
        ("H  jobs >= 3, lines >= 6, per-job medians agree 1.5", 3, 6, None, 1.5)]

print("\nLEAVE-ONE-OUT, every document scored on rates AND factors from the other 28")
print("%-44s %9s %9s %9s %8s" % ("ARM", "MEAN ABS", "MEDIAN", "BIAS", "within10"))
results = {}
for arm in ARMS:
    label, jg, lg = arm[0], arm[1], arm[2]
    only = arm[3] if len(arm) > 3 else None
    agree = arm[4] if len(arm) > 4 else None
    errs = []
    for i, d in enumerate(docs):
        train = [x for j, x in enumerate(docs) if j != i]
        rates = bt.learn(train)
        factors = {} if jg is None else learn_text(train, rates, jg, lg, only, agree)
        errs += score([d], rates, factors)
    results[label] = errs
    a = [abs(e) for e, _ in errs]
    print("%-44s %8.2f%% %8.2f%% %+8.2f%% %5d/%d"
          % (label, statistics.fmean(a), statistics.median(a),
             statistics.fmean([e for e, _ in errs]), sum(1 for x in a if x <= 10), len(a)))

best = ARMS[1][0]
A = dict((f, e) for e, f in results[ARMS[0][0]])
B = dict((f, e) for e, f in results[best])
rows = sorted((abs(B[f]) - abs(A[f]), f, A[f], B[f]) for f in A if f in B)
print("\nPER DOCUMENT, arm A against %s - better on %d, worse on %d, level on %d"
      % (best.strip(), sum(1 for r in rows if r[0] < -0.05),
         sum(1 for r in rows if r[0] > 0.05), sum(1 for r in rows if abs(r[0]) <= 0.05)))
print("  %-48s %9s %9s %8s" % ("DOCUMENT", "A", "B", "B-A abs"))
for d, f, a, b in rows[:8]:
    print("  %-48s %+8.1f%% %+8.1f%% %+7.1f" % (f[:48], a, b, d))
print("  %-48s" % "...")
for d, f, a, b in rows[-6:]:
    print("  %-48s %+8.1f%% %+8.1f%% %+7.1f" % (f[:48], a, b, d))

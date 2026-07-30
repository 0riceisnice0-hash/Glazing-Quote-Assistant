# -*- coding: utf-8 -*-
"""Mine the supply rate from the WHOLE build-up, not the Frames column alone.

The document builds a unit rate as
    frames + glass + additional + 0.75 x code_value
and that now reconciles on 495 of 508 lines. The engine models
    area x learned_rate + adder_factor(area) x code_value
with learned_rate mined from FRAMES ONLY. So Glass and Additional are money it
has no term for at all - 20.4% of supply above 6m2, 9.3% at 2-3m2 - and
ADDER_FACTOR_LARGE = 1.25 is a crude patch over the largest part of it. Which is
exactly what 30/07 concluded it was: the median GBP 1,000 of glass+additional+cw
on a large unit, charged to a median code value of 2,000.

This is NOT the fix that was tried and rejected on 30/07. That one added a flat
learned extras SUM on large units only, and scored 14.73. This puts the extras
into the per-m2 rate itself, per code and per band, everywhere - so it varies
with size and product the way the money actually does.

Arms, all scored 3-fold on jobs the rates were never mined from:
  A  frames only,  adder 1.25 large   - the engine as it stands
  B  frames+glass+additional, 0.75 flat
  C  frames+glass+additional, 1.25 large   - separates the two changes
  D  frames only,  0.75 flat               - the other corner
"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine
import openpyxl
import mary_calibrate as cal
import mary_quote_reader as reader

ADDITIONAL_COL = 11

# Re-read the corpus adding the Additional column, which parse_doc does not read.
_orig = bt.parse_doc


def parse_doc(path):
    d = _orig(path)
    if not d:
        return d
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        ws = [w for w in wb.worksheets
              if w.title.strip().lower().startswith("pricing document")][0]
        extra = {}
        for row in ws.iter_rows(values_only=True):
            cells = list(row) + [None] * (16 - len(row))
            code = str(cells[1]).strip().upper() if isinstance(cells[1], str) else ""
            if code not in engine.CODE_VALUE:
                continue
            ur = cells[7] if isinstance(cells[7], (int, float)) else None
            if not ur:
                continue
            a = cells[ADDITIONAL_COL]
            extra.setdefault(round(float(ur), 2), []).append(
                float(a) if isinstance(a, (int, float)) else 0.0)
        for l in d["lines"]:
            vals = extra.get(round(l["unit_rate"], 2))
            l["additional"] = vals.pop(0) if vals else 0.0
    finally:
        wb.close()
    return d


bt.parse_doc = parse_doc
docs = bt.collect()
print("corpus %d documents, %d lines\n" % (len(docs), sum(len(d["lines"]) for d in docs)))

# Sanity: does the re-read reconcile? If the Additional figures are lining up
# with the wrong rows this collapses and the whole experiment is void.
ok = tot = 0
for d in docs:
    for l in d["lines"]:
        if not l["frames"]:
            continue
        tot += 1
        built = l["frames"] + (l["glass"] or 0) + (l.get("additional") or 0) \
            + engine.CODE_VALUE.get(l["code"], 0) * 0.75
        if abs(built - l["unit_rate"]) <= max(1.0, 0.01 * l["unit_rate"]):
            ok += 1
print("SANITY: build-up reconciles on %d / %d lines (was 495/508 measured via the audit reader)\n"
      % (ok, tot))


def learn_arm(train, whole):
    buckets = {}
    for d in train:
        for l in d["lines"]:
            if not l["frames"] or l["area"] <= 0:
                continue
            money = l["frames"] + ((l["glass"] or 0) + (l.get("additional") or 0) if whole else 0)
            buckets.setdefault("%s|%s" % (l["code"], engine.learned_band_of(l["area"])),
                               []).append(money / l["area"])
    return {k: {"median_per_m2": round(statistics.median(v), 2), "n": len(v),
                "low": round(min(v), 2), "high": round(max(v), 2)}
            for k, v in buckets.items() if len(v) >= 3}


def score(docs_test, rates, large):
    out = []
    for d in docs_test:
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
            f = large if l["area"] > engine.LARGE_UNIT_M2 else 0.75
            u = l["area"] * rate + engine.CODE_VALUE.get(l["code"], 0) * f
            e_t += u * l["qty"]
            h_t += l["unit_rate"] * l["qty"]
            n += 1
        if n and h_t:
            out.append(((e_t - h_t) / h_t * 100.0, n))
    return out


ARMS = [("A  frames only,        1.25 large", False, 1.25),
        ("B  frames+glass+addl,  0.75 flat ", True, 0.75),
        ("C  frames+glass+addl,  1.25 large", True, 1.25),
        ("D  frames only,        0.75 flat ", False, 0.75)]

print("%-36s %-26s %8s %8s %8s" % ("ARM", "PER FOLD", "MEAN", "MEDIAN", "BIAS"))
for label, whole, large in ARMS:
    per, meds, biases, lines = [], [], [], []
    for f in range(3):
        train = [d for i, d in enumerate(docs) if i % 3 != f]
        test = [d for i, d in enumerate(docs) if i % 3 == f]
        res = score(test, learn_arm(train, whole), large)
        errs = [e for e, _ in res]
        per.append(statistics.fmean(abs(e) for e in errs))
        meds.append(statistics.median(abs(e) for e in errs))
        biases.append(statistics.fmean(errs))
        lines.append(sum(n for _, n in res))
    print("%-36s %-26s %7.2f%% %7.2f%% %+7.2f%%   lines %s"
          % (label, "  ".join("%5.1f" % p for p in per),
             statistics.fmean(per), statistics.fmean(meds), statistics.fmean(biases), lines))

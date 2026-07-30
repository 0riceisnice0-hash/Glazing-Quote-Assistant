# -*- coding: utf-8 -*-
"""A FIXED COST PER OPENING IN THE SUPPLY TERM - is it real, or is it bands again?

THE IDEA, and why it is not one of the closed negatives. The engine models
    supply = area x learned_rate
and the board has already closed SIZE BANDS (a piecewise-constant learned_rate)
in both the finer and the coarser direction. But bands are a crude approximation
to a structure the archive shows directly. Georgie's sliding sash:
    area   0.48 -> 1.24 m2   x2.58
    frames 915.51 -> 1213.92 x1.33
Cost barely moves while area more than doubles. That is a fixed cost per opening
plus a variable cost per m2, and the honest model of it has an intercept:
    supply = a + b x area
fitted per bucket by least squares, instead of one median rate through the origin.

THE BOARD'S OWN OBJECTION, which has to be answered rather than ignored: "the
template already charges a fixed cost per opening, the code adder". True - but
the adder is a CONSTANT per code, identical whatever the supplier charges, and it
sits OUTSIDE the supply term. This asks whether the SUPPLY money itself has an
intercept. Different question, and the adder cannot absorb it because the adder
does not vary with the bucket.

FOUR ARMS, everything else held identical, decided leave-one-JOB-out:
    A  median rate through the origin        (CURRENT)
    B  least squares a + b x area, per code+band
    C  least squares a + b x area, per code  (pooled over bands - more data per fit)
    D  B but only where the fit is better than the median on the TRAINING data
"""
import os, statistics, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

MIN_N = engine.MIN_LEARNED_N


def _fit(pts):
    """Least squares a + b*area over (area, money). Returns None if degenerate."""
    n = len(pts)
    if n < MIN_N:
        return None
    sx = sum(a for a, _ in pts)
    sy = sum(m for _, m in pts)
    sxx = sum(a * a for a, _ in pts)
    sxy = sum(a * m for a, m in pts)
    den = n * sxx - sx * sx
    if abs(den) < 1e-9:
        return None
    b = (n * sxy - sx * sy) / den
    a = (sy - b * sx) / n
    return a, b


def learn_lines(docs, by_band):
    """Collect (area, supply_money) per bucket, and the median rate as a fallback."""
    buckets = {}
    for d in docs:
        for l in d["lines"]:
            money = bt.supply_money(l)
            if not money or l["area"] <= 0:
                continue
            key = ("%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
                   if by_band else l["code"])
            buckets.setdefault(key, []).append((l["area"], money))
    return buckets


def price(l, arm, base, fits, fits_code, ok_keys):
    """Unit rate for one line. The adder is untouched in every arm."""
    if l.get("cw"):
        return l["area"] * engine.CW_SUPPLY_M2
    adder = engine.CODE_VALUE.get(l["code"], 0) * engine.adder_factor(l["area"])
    key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
    rec = base.get(key)

    if arm in ("B", "D"):
        f = fits.get(key)
        if f and (arm == "B" or key in ok_keys):
            return max(0.0, f[0] + f[1] * l["area"]) + adder
    if arm == "C":
        f = fits_code.get(l["code"])
        if f:
            return max(0.0, f[0] + f[1] * l["area"]) + adder

    if rec and rec.get("n", 0) >= MIN_N:
        return l["area"] * rec["median_per_m2"] + adder
    e = bt.engine_price(l, None)
    return e["unit_rate"] if e else None


def run(arm, docs):
    groups = {}
    for d in docs:
        groups.setdefault(bt.job_key(d), []).append(d)
    errs = []
    for key, group in groups.items():
        train = [d for d in docs if bt.job_key(d) != key]
        base = bt.learn(train)
        band_pts = learn_lines(train, True)
        code_pts = learn_lines(train, False)
        fits = {k: f for k, f in ((k, _fit(v)) for k, v in band_pts.items()) if f}
        fits_code = {k: f for k, f in ((k, _fit(v)) for k, v in code_pts.items()) if f}
        # Arm D: keep the fit only where it beats the median ON THE TRAINING DATA.
        ok = set()
        for k, pts in band_pts.items():
            f, rec = fits.get(k), base.get(k)
            if not f or not rec or not rec.get("median_per_m2"):
                continue
            e_fit = sum(abs(f[0] + f[1] * a - m) for a, m in pts)
            e_med = sum(abs(a * rec["median_per_m2"] - m) for a, m in pts)
            if e_fit < e_med:
                ok.add(k)
        for d in group:
            eng = hum = 0.0
            for l in d["lines"]:
                u = price(l, arm, base, fits, fits_code, ok)
                if u is None:
                    continue
                eng += u * l["qty"]
                hum += l["unit_rate"] * l["qty"]
            if hum:
                errs.append(((eng - hum) / hum * 100.0, d["file"]))
    return errs


docs = bt.collect()
print("%d documents, %d lines\n" % (len(docs), sum(len(d["lines"]) for d in docs)))

results = {}
for arm, label in (("A", "median rate through the origin (CURRENT)"),
                   ("B", "least squares a + b*area, per code+band"),
                   ("C", "least squares a + b*area, per code (pooled bands)"),
                   ("D", "B, only where the fit beats the median in training")):
    errs = run(arm, docs)
    a = [abs(e) for e, _ in errs]
    s = [e for e, _ in errs]
    results[arm] = errs
    print("  %s  %-52s mean abs %6.2f%%  median %6.2f%%  bias %+6.2f%%  within10 %2d/%d"
          % (arm, label, statistics.fmean(a), statistics.median(a),
             statistics.fmean(s), sum(1 for x in a if x <= 10), len(a)))

print("\nPER-DOCUMENT, A against the best rival")
best = min(("B", "C", "D"), key=lambda k: statistics.fmean([abs(e) for e, _ in results[k]]))
da = {f: e for e, f in results["A"]}
db = {f: e for e, f in results[best]}
win = lose = 0
print("  arm %s is the best rival\n" % best)
print("  %-52s %9s %9s" % ("document", "A", best))
for f in sorted(da, key=lambda x: -abs(da[x])):
    if abs(da[f]) - abs(db[f]) > 0.05:
        win += 1
    elif abs(db[f]) - abs(da[f]) > 0.05:
        lose += 1
    print("  %-52.52s %+9.1f %+9.1f%s" % (f, da[f], db[f],
          "  <-- worse" if abs(db[f]) > abs(da[f]) + 0.05 else ""))
print("\n  %s better on %d documents, worse on %d" % (best, win, lose))

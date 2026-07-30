# -*- coding: utf-8 -*-
"""How much of a unit rate is money the engine has no term for at all?

The engine models  unit_rate = area x learned_rate + code_value x adder, and the
learned rate is mined from the FRAMES column alone. But the document builds a
unit rate as  frames + glass + additional + cw + code_value x 0.75  (measured
30/07). So Glass, Additional and CW are money the engine cannot see, and the
1.25 large-unit fudge is a crude patch over the largest part of it.

Measure it: what fraction of the supply money is outside Frames, and does the
reconciliation unit_rate - components = 0.75 x code_value actually hold?"""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as audit
import mary_pricing as engine

docs = audit.collect_docs()
print("audit corpus: %d documents\n" % len(docs))

rows = []
for d in docs:
    for r in d["rows"]:
        if not r["code"] or not r["area"] or not r["unit_rate"] or not r["frames"]:
            continue
        comp = sum(r[c] or 0.0 for c in ("frames", "glass", "additional", "cw"))
        rows.append(dict(r, _comp=comp, _extras=comp - r["frames"], _file=d["file"]))

print("%d priced lines with a code, a size and a Frames figure" % len(rows))

# Does the reconciliation hold? unit_rate - components should be 0.75 x code_value.
ok = bad = 0
for r in rows:
    want = engine.CODE_VALUE.get(r["code"], 0) * 0.75
    r["_resid"] = r["unit_rate"] - r["_comp"]
    if abs(r["_resid"] - want) <= max(1.0, 0.01 * want):
        ok += 1
    else:
        bad += 1
print("reconciles to adder = 0.75 x code value: %d lines; does NOT: %d\n" % (ok, bad))

good = [r for r in rows if abs(r["_resid"] - engine.CODE_VALUE.get(r["code"], 0) * 0.75)
        <= max(1.0, 0.01 * engine.CODE_VALUE.get(r["code"], 0) * 0.75)]

print("ON THE %d RECONCILING LINES - how much supply money is OUTSIDE Frames?" % len(good))
print("%-12s %6s %10s %10s %10s %8s" % ("AREA m2", "n", "FRAMES/m2", "ALL4/m2", "EXTRAS/m2", "EXTRA%"))
BUCKETS = [(0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, 6.0), (6.0, 99)]
for lo, hi in BUCKETS:
    sel = [r for r in good if lo <= r["area"] < hi]
    if not sel:
        continue
    f = statistics.median(r["frames"] / r["area"] for r in sel)
    a = statistics.median(r["_comp"] / r["area"] for r in sel)
    x = statistics.median(r["_extras"] / r["area"] for r in sel)
    share = statistics.median(r["_extras"] / r["_comp"] for r in sel if r["_comp"]) * 100
    print("%-12s %6d %10.2f %10.2f %10.2f %7.1f%%"
          % ("%.1f-%.1f" % (lo, hi), len(sel), f, a, x, share))

print("\nhow many of those lines have ANY money outside Frames?")
withx = [r for r in good if r["_extras"] > 1.0]
print("  %d of %d (%.0f%%), median GBP %.2f per unit, total GBP %s"
      % (len(withx), len(good), 100.0 * len(withx) / max(1, len(good)),
         statistics.median(r["_extras"] for r in withx),
         "{:,.0f}".format(sum(r["_extras"] * (r["qty"] or 1) for r in withx))))

print("\nwhich COLUMN is the money in?")
for c in ("glass", "additional", "cw"):
    sel = [r for r in good if (r[c] or 0) > 1.0]
    print("  %-11s %4d line(s), median GBP %10s, total GBP %s"
          % (c, len(sel), "{:,.2f}".format(statistics.median(r[c] for r in sel)) if sel else "-",
             "{:,.0f}".format(sum(r[c] * (r["qty"] or 1) for r in sel)) if sel else "-"))

print("\nNOT reconciling - which documents, and why (Brandon was the known case)?")
byfile = {}
for r in rows:
    want = engine.CODE_VALUE.get(r["code"], 0) * 0.75
    if abs(r["_resid"] - want) > max(1.0, 0.01 * want):
        byfile.setdefault(r["_file"], []).append(r)
for f, rs in sorted(byfile.items(), key=lambda kv: -len(kv[1])):
    print("  %-52s %3d line(s)  median residual %10s (want %s)"
          % (f[:52], len(rs), "{:,.2f}".format(statistics.median(r["_resid"] for r in rs)),
             "{:,.2f}".format(statistics.median(engine.CODE_VALUE.get(r["code"], 0) * 0.75 for r in rs))))

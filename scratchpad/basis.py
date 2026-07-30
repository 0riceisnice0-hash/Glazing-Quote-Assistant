# -*- coding: utf-8 -*-
"""Is the Frames column per-unit money, or a line total, and does it vary?

156 of 508 priced lines have frames+glass+additional+cw GREATER than their own
unit rate, which is impossible if those columns are the per-unit build-up. The
board already noticed it on Brandon Estate and set it aside as 'not per-unit
money'. Brandon has 2,202 units on a line. So the obvious candidate is that
those documents write the components as LINE TOTALS - components x qty - and
the engine mines GBP/m2 by dividing them by area alone.

If that is right the rates mined from those lines are inflated by their own
quantity, and the test is exact: components / qty should reconcile to
unit_rate - 0.75 x code_value, to the penny."""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as audit
import mary_pricing as engine

docs = audit.collect_docs()

def resid(r, div):
    comp = sum(r[c] or 0.0 for c in ("frames", "glass", "additional", "cw")) / div
    return r["unit_rate"] - comp

per_unit = per_qty = neither = 0
byfile = {}
for d in docs:
    for r in d["rows"]:
        if not r["code"] or not r["area"] or not r["unit_rate"] or not r["frames"]:
            continue
        want = engine.CODE_VALUE.get(r["code"], 0) * 0.75
        tol = max(1.0, 0.01 * want)
        q = r["qty"] or 1
        a = abs(resid(r, 1.0) - want) <= tol
        b = q > 1 and abs(resid(r, q) - want) <= tol
        st = "per-unit" if a else ("LINE TOTAL (/qty)" if b else "neither")
        per_unit += a; per_qty += (b and not a); neither += (not a and not b)
        byfile.setdefault(d["file"], {}).setdefault(st, []).append(r)

print("508 coded, sized, framed lines - which basis reconciles to adder = 0.75 x code value?")
print("  per-unit build-up      %3d" % per_unit)
print("  LINE TOTAL, /qty       %3d   <-- mined as if per-unit, so inflated by qty" % per_qty)
print("  neither                %3d\n" % neither)

print("%-54s %9s %9s %9s" % ("DOCUMENT", "PER-UNIT", "/QTY", "NEITHER"))
for f, sts in sorted(byfile.items(), key=lambda kv: -len(kv[1].get("LINE TOTAL (/qty)", []))):
    n_pu = len(sts.get("per-unit", []))
    n_q = len(sts.get("LINE TOTAL (/qty)", []))
    n_n = len(sts.get("neither", []))
    if not (n_q or n_n):
        continue
    print("%-54s %9d %9d %9d" % (f[:54], n_pu, n_q, n_n))

print("\nMIXED DOCUMENTS - does any one document use BOTH bases? (that would rule out")
print("a per-document flag and force the test to be per-line)")
for f, sts in byfile.items():
    if len(sts.get("per-unit", [])) and len(sts.get("LINE TOTAL (/qty)", [])):
        print("  %-54s per-unit %d, /qty %d" % (f[:54], len(sts["per-unit"]),
                                                len(sts["LINE TOTAL (/qty)"])))

print("\nWHAT IT DOES TO THE RATES. GBP/m2 as mined now, against /qty, on the /qty lines:")
sel = [r for f, sts in byfile.items() for r in sts.get("LINE TOTAL (/qty)", [])]
if sel:
    print("  n=%d   now median %8.2f/m2   corrected median %8.2f/m2   median qty %.0f"
          % (len(sel),
             statistics.median(r["frames"] / r["area"] for r in sel),
             statistics.median(r["frames"] / (r["qty"] or 1) / r["area"] for r in sel),
             statistics.median(r["qty"] or 1 for r in sel)))
    print("\n  worst offenders by quantity:")
    for r in sorted(sel, key=lambda r: -(r["qty"] or 1))[:8]:
        print("    %-6s qty %6.0f  %6.2fm2  frames %12s  now %9.1f/m2  corrected %8.1f/m2"
              % (r["code"], r["qty"], r["area"], "{:,.2f}".format(r["frames"]),
                 r["frames"] / r["area"], r["frames"] / r["qty"] / r["area"]))

print("\nNEITHER - the residual after /qty, to see what basis they are on:")
sel = [(f, r) for f, sts in byfile.items() for r in sts.get("neither", [])]
seen = set()
for f, r in sel:
    if f in seen:
        continue
    seen.add(f)
    rs = [x for g, x in sel if g == f]
    print("  %-50s n=%-3d median resid /1 %10s  /qty %10s  want %s"
          % (f[:50], len(rs),
             "{:,.2f}".format(statistics.median(resid(x, 1.0) for x in rs)),
             "{:,.2f}".format(statistics.median(resid(x, x["qty"] or 1) for x in rs)),
             "{:,.2f}".format(statistics.median(engine.CODE_VALUE.get(x["code"], 0) * 0.75 for x in rs))))

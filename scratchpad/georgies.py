# -*- coding: utf-8 -*-
"""Georgie's (formerly Rosebank) - board item 1 on the fourth run's own list.

-27.3% leave-one-JOB-out and per-job median ratio 2.911, the worst product-identity
residual in the archive. Two causes already half-named: a GBP 2,000.02 shortfall on
its curtain-walling row, whose description is 'CW01, D03, CW02', and ten other lines
of aluminium SLIDING SASH at ~GBP 1,000/m2 against an LAW archive median of 491.
"""
import os, sys
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine
import mary_quote_audit as qa

DOC = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                   "Commercial", "1. Tender Documents", "Pearce Construction (Barnstaple)",
                   "Georgies", "1. Estimating", "3. Client Quote",
                   "Pearce Construction - Georgie's (formerly Rosebank) Pricing.xlsx")

print("RAW")
wb = openpyxl.load_workbook(DOC, read_only=True, data_only=True)
ws = [w for w in wb.worksheets if w.title.strip().lower().startswith("pricing document")][0]
for rn, row in enumerate(ws.iter_rows(values_only=True), 1):
    cells = ["c%d=%r" % (j, ("%.2f" % v) if isinstance(v, float) else v)
             for j, v in enumerate(list(row)) if v is not None]
    if cells:
        print("  r%-3d %s" % (rn, "  ".join(cells))[:300])
wb.close()

print("\nENGINE VIEW (leave-one-JOB-out is not applied here; this is the in-sample view)")
docs = bt.collect()
d = next(x for x in docs if "Georgie" in x["file"])
print("  supplier=%r" % d.get("supplier"))
print("  %-4s %-22.22s %-14s %6s %4s %10s %10s %9s %9s %8s"
      % ("code", "ref", "heading", "m2", "qty", "human", "mary", "GBP/m2", "frames", "err%"))
for l in d["lines"]:
    e = bt.engine_price(l, d.get("supplier"))
    hum_m2 = l["unit_rate"] / l["area"] if l["area"] else 0
    print("  %-4s %-22.22s %-14.14s %6.2f %4s %10.2f %10.2f %9.0f %9s %+8.1f"
          % (l["code"] or "CW", l["ref"], l.get("heading") or "", l["area"], l["qty"],
             l["unit_rate"], e["unit_rate"], hum_m2,
             "%.2f" % l["frames"] if l.get("frames") else "-",
             (e["unit_rate"] - l["unit_rate"]) / l["unit_rate"] * 100.0))

print("\nSUPPLIER BLOCK / AUDIT VIEW")
ad = qa.read_doc(DOC)
print("  names=%r cost=%r parts=%r" % (ad["supplier_names"], ad["supplier_cost"], ad.get("supplier_parts")))
fr = sum(r["frames"] * r["qty"] for r in ad["rows"] if r["frames"])
frx = sum(r["frames"] * r["qty"] for r in ad["rows"] if r["frames"] and not qa._is_cw_row(r))
print("  frames total %.2f   excluding CW %.2f" % (fr, frx))

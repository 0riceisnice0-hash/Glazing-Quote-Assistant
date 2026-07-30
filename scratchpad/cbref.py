# -*- coding: utf-8 -*-
"""CB Refrigeration Workshop - board item 2, and it is on BOTH lists.

SUPPLIER 1.291: frames total against a block of BSW + BSW CW + Strongdoor.
Strongdoor is the steel-door supplier the template has no code for, so the
Frames column may carry steel money one of the three figures does not.
And it is the third-worst ENGINE document at -32.6%.
"""
import os, sys
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as qa

ROOT = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                    "Commercial", "1. Tender Documents", "Knights Construction",
                    "CB Refrigeration Workshop", "1. Estimating")
DOC = os.path.join(ROOT, "3. Client Quote",
                   "CB Refrigeration Workshop - Pricing Document - DO NOT SEND.xlsx")

print("RAW TOP OF DOCUMENT")
wb = openpyxl.load_workbook(DOC, read_only=True, data_only=True)
ws = [w for w in wb.worksheets if w.title.strip().lower().startswith("pricing document")][0]
for rn, row in enumerate(ws.iter_rows(values_only=True), 1):
    cells = ["c%d=%r" % (j, ("%.2f" % v) if isinstance(v, float) else v)
             for j, v in enumerate(list(row)) if v is not None]
    if cells:
        print("  r%-3d %s" % (rn, "  ".join(cells))[:360])
wb.close()

print("\nREADER VIEW")
d = qa.read_doc(DOC)
print("  supplier=%r names=%r cost=%r" % (d["supplier"], d["supplier_names"], d["supplier_cost"]))
print("  parts=%r" % (d.get("supplier_parts"),))
print("  _sup_vals=%r" % (d["_sup_vals"],))
print("  cols=%r" % (d["cols"],))
print("  %-4s %-30.30s %-13s %4s %10s %10s %10s %10s %10s"
      % ("row", "heading", "size", "qty", "frames", "glass", "addl", "cw", "unit"))
fr = 0.0
for r in d["rows"]:
    q = r.get("qty") or 0
    if r.get("frames"): fr += r["frames"] * q
    print("  %-4s %-30.30s %-13s %4s %10s %10s %10s %10s %10s"
          % (r.get("row"), (r.get("heading") or "?"), r.get("size"), q,
             "%.2f" % r["frames"] if r.get("frames") else "-",
             "%.2f" % r["glass"] if r.get("glass") else "-",
             "%.2f" % r["additional"] if r.get("additional") else "-",
             "%.2f" % r["cw"] if r.get("cw") else "-",
             "%.2f" % r["unit_rate"] if r.get("unit_rate") else "-"))
print("  frames x qty total  {:>12,.2f}".format(fr))

print("\nSUPPLIER QUOTES IN THE PACK")
sq = os.path.join(ROOT, "2. Supplier Quotes")
for dp, _, fns in os.walk(sq):
    for fn in sorted(fns):
        print("  %s" % os.path.join(dp, fn).replace(ROOT, "..."))

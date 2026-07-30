# -*- coding: utf-8 -*-
"""Compare the three Brandon Estate revisions line by line.

Board item 1 (31/07): the earlier 11-line revision reports SUPPLIER 4.094 -
frames 1,484,932.13 against a BSW + Vetroseal block of 362,678.40 - while its
two siblings reconcile at 0.991 and 1.006 off the SAME estate. One document out
of step with itself. Suspect a block figure never updated when the job grew.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_quote_audit as qa

ROOT = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                    "Commercial", "1. Tender Documents", "Elkins Construction",
                    "Brandon Estate EWI Remediation works", "1. Estimating",
                    "3. Client Quote")
FILES = [
    ("EARLIER (the 4.094)", os.path.join(ROOT, "SS", "DO NOT SEND Pricing Document - Brandon Estate.xlsx")),
    ("ELKINS  (1.006)",     os.path.join(ROOT, "SS", "DO NOT SEND Elkins - Brandon Estate Pricing Document.xlsx")),
    ("COMAR   (0.991)",     os.path.join(ROOT, "SS", "COMAR - DO NOT SEND Pricing Document - Brandon Estate - Copy.xlsx")),
]

for label, path in FILES:
    print("=" * 100)
    print("%s\n  %s" % (label, os.path.basename(path)))
    if not os.path.exists(path):
        print("  MISSING")
        continue
    d = qa.read_doc(path)
    if not d:
        print("  unreadable")
        continue
    print("  supplier=%r  names=%r  cost=%r  n=%r"
          % (d.get("supplier"), d.get("supplier_names"), d.get("supplier_cost"), d.get("supplier_n")))
    print("  _sup_vals=%r" % (d.get("_sup_vals"),))
    print("  cols=%r" % (d.get("cols"),))
    print("  total=%r installation=%r" % (d.get("total"), d.get("installation")))
    print("  %-4s %-26s %-13s %4s %12s %12s %12s %12s %12s"
          % ("row", "heading/desc", "size", "qty", "frames", "glass", "addl", "unit", "total"))
    fr = gl = ad = 0.0
    for r in d["rows"]:
        c = r.get("comp") or {}
        f, g, a = c.get("frames"), c.get("glass"), c.get("additional")
        q = r.get("qty") or 0
        if f: fr += f * q
        if g: gl += g * q
        if a: ad += a * q
        print("  %-4s %-26.26s %-13s %4s %12s %12s %12s %12s %12s"
              % (r.get("row"), (r.get("heading") or r.get("desc") or "")[:26], r.get("size"),
                 q,
                 "%.2f" % f if f else "-", "%.2f" % g if g else "-",
                 "%.2f" % a if a else "-",
                 "%.2f" % r["unit_rate"] if r.get("unit_rate") else "-",
                 "%.2f" % (r["unit_rate"] * q) if r.get("unit_rate") else "-"))
    print("  TOTALS x qty:  frames %,.2f   glass %,.2f   additional %,.2f"
          .replace(",", "") % (fr, gl, ad))
    print("  frames        {:>15,.2f}".format(fr))
    print("  frames+glass  {:>15,.2f}".format(fr + gl))
    print("  block total   {:>15}".format(d.get("supplier_cost")))

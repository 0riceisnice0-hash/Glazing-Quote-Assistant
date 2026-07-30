# -*- coding: utf-8 -*-
"""The 11 remaining BUILDUP findings are all in the COMAR Brandon re-price.

Hypothesis: the COMAR variant is a re-price of the Elkins revision that changed
the CODES and the UNIT RATES but kept the component cells, so the build-up no
longer foots because the adder implied by the new unit rate is not the adder of
the new code. Checkable: the component cells should be IDENTICAL between the two
documents on matching sizes.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_pricing as engine
import mary_quote_audit as qa

ROOT = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                    "Commercial", "1. Tender Documents", "Elkins Construction",
                    "Brandon Estate EWI Remediation works", "1. Estimating",
                    "3. Client Quote", "SS")
comar = qa.read_doc(os.path.join(ROOT, "COMAR - DO NOT SEND Pricing Document - Brandon Estate - Copy.xlsx"))
elkin = qa.read_doc(os.path.join(ROOT, "DO NOT SEND Elkins - Brandon Estate Pricing Document.xlsx"))

# Index Elkins by (size, frames) - the component cells are the fingerprint.
eidx = {}
for r in elkin["rows"]:
    if r.get("frames"):
        eidx.setdefault(r["size"], []).append(r)

print("%-4s %-13s %-5s %10s %9s %8s %10s %11s %10s %9s"
      % ("row", "size", "code", "frames", "glass", "addl", "unit", "impliedaddr", "codeaddr", "delta"))
same_comp = diff_comp = 0
for r in comar["rows"]:
    if not r.get("frames") or not r.get("unit_rate"):
        continue
    comp = r["frames"] + (r["glass"] or 0) + (r["additional"] or 0)
    implied = r["unit_rate"] - comp
    codeadd = engine.CODE_VALUE.get(r["code"], 0) * engine.adder_factor(r["area"] or 0)
    if abs(implied - codeadd) < 0.02:
        continue
    match = [e for e in eidx.get(r["size"], [])
             if abs(e["frames"] - r["frames"]) < 0.02
             and abs((e["glass"] or 0) - (r["glass"] or 0)) < 0.02]
    if match:
        same_comp += 1
    else:
        diff_comp += 1
    print("%-4s %-13s %-5s %10.2f %9.2f %8.2f %10.2f %11.2f %10.2f %+9.2f  %s"
          % (r["row"], r["size"], r["code"], r["frames"], r["glass"] or 0,
             r["additional"] or 0, r["unit_rate"], implied, codeadd, implied - codeadd,
             ("components IDENTICAL to Elkins row %s (code %s, unit %.2f)"
              % (match[0]["row"], match[0]["code"], match[0]["unit_rate"])) if match
             else "no Elkins row with these components"))

print("\n%d of %d non-footing rows have components identical to an Elkins row; %d do not"
      % (same_comp, same_comp + diff_comp, diff_comp))

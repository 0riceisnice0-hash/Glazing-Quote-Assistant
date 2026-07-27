"""St Mary's calibration, done properly: register vs BSW QT252799 actual, by SIZE BAND.

Correction to my first pass: find_rate applied the MEASURED bsw factor 1.056 (n=273,
from learned-rates.json), NOT the CALIBRATION Sheerline 1.10 - derived_factors()
supersedes CALIBRATION. So on any BSW Sheerline job the Sheerline correction never
fires at all. Both are reported separately below.

Actuals are the workbook frame column, already verified line by line against the quote.
"""
import os, sys, io, openpyxl, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_pricing as p

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\3. Client Quote\SS"
     r"\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx")
ws = openpyxl.load_workbook(P, data_only=True)["Pricing Document "]

BSW_FACTOR = 1.056
SHEERLINE = 1.10

bands = collections.defaultdict(lambda: {"units": 0, "area": 0.0, "actual": 0.0,
                                         "raw": 0.0, "types": 0})
for r in range(9, 40):
    if not ws.cell(r, 2).value:
        continue
    qty = ws.cell(r, 6).value or 0
    actual = ws.cell(r, 10).value or 0
    area = ws.cell(r, 15).value or 0
    if not area:
        continue
    b = p.band_of(area)
    rr = p.find_rate("aluminium casement window, glazed", area, supplier="bsw")
    if not rr:
        continue
    d = bands[b]
    d["units"] += qty
    d["area"] += area * qty
    d["actual"] += actual * qty
    d["raw"] += rr.entry["median"] * area * qty
    d["types"] += 1

print("BSW QT252799 ACTUAL vs REGISTER, BY SIZE BAND   (98 units, 31 types, 160.36 m2)")
print("=" * 100)
print("%-10s %5s %5s %8s %11s %11s %11s %9s"
      % ("band", "types", "units", "m2", "actual/m2", "reg med/m2", "reg total", "error"))
print("-" * 100)
T = {"units": 0, "area": 0.0, "actual": 0.0, "raw": 0.0}
for b in ("<1.5m2", "1.5-3m2", "3-6m2", ">6m2"):
    if b not in bands:
        continue
    d = bands[b]
    err = 100.0 * (d["raw"] - d["actual"]) / d["actual"]
    print("%-10s %5d %5d %8.2f %11.2f %11.2f %11.2f %+8.1f%%"
          % (b, d["types"], d["units"], d["area"], d["actual"] / d["area"],
             d["raw"] / d["area"], d["raw"], err))
    for k in T:
        T[k] += d[k]

print("-" * 100)
err_raw = 100.0 * (T["raw"] - T["actual"]) / T["actual"]
print("%-10s %5s %5d %8.2f %11.2f %11.2f %11.2f %+8.1f%%"
      % ("ALL", "31", T["units"], T["area"], T["actual"] / T["area"],
         T["raw"] / T["area"], T["raw"], err_raw))

print()
print("WHAT EACH CORRECTION DOES TO THE WHOLE-JOB NUMBER")
print("=" * 100)
print("  BSW actual (what we will pay)          GBP %10.2f" % T["actual"])
for label, f in (("register median, uncorrected", 1.0),
                 ("x measured bsw factor 1.056 (the one that actually fires)", BSW_FACTOR),
                 ("x CALIBRATION sheerline 1.10 (never fires on a BSW job)", SHEERLINE),
                 ("x both, if they compounded", BSW_FACTOR * SHEERLINE)):
    v = T["raw"] * f
    print("  %-56s GBP %10.2f  %+7.1f%%"
          % (label, v, 100.0 * (v - T["actual"]) / T["actual"]))

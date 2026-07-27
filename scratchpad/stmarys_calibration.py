"""St Mary's calibration: register benchmark vs BSW QT252799 actual, 31 types / 98 units.

Tests the CALIBRATION entry {sheerline/prestige: 1.10} which today rests on ONE job
(SM5 Wexham, BSW QT253300, 24/07/2026). St Mary's is BSW QT252799, a Sheerline Prestige
casement job with 98 units, so it is a far bigger sample against the same supplier and
the same system.

Nothing here is estimated - actuals are read off the workbook's frame column, which was
already verified line by line against the quote.
"""
import os, sys, io, openpyxl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_pricing as p

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\3. Client Quote\SS"
     r"\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx")
ws = openpyxl.load_workbook(P, data_only=True)["Pricing Document "]

print("%-9s %-13s %3s %7s %10s %11s %11s %9s %8s"
      % ("type", "size", "qty", "m2/ea", "BSW each", "bench/m2", "bench each", "diff", "err%"))
print("-" * 104)

rows, tot_actual, tot_bench, tot_area, tot_units = [], 0.0, 0.0, 0.0, 0
for r in range(9, 40):                       # window rows only
    code = ws.cell(r, 2).value
    if not code:
        continue
    desc = str(ws.cell(r, 3).value or "").strip()
    size = str(ws.cell(r, 5).value or "").strip()
    qty = ws.cell(r, 6).value or 0
    actual_each = ws.cell(r, 10).value or 0   # J = supplier frame cost per unit
    area = ws.cell(r, 15).value or 0          # O = m2 per unit
    if not area:
        continue
    rate = p.find_rate("aluminium casement window, glazed", area,
                       supplier="bsw", system="Sheerline Prestige")
    if rate is None:
        print("%-9s  no register band" % desc)
        continue
    bench_m2 = rate.rate                      # corrected GBP/m2
    bench_each = bench_m2 * area
    diff = bench_each - actual_each
    err = 100.0 * diff / actual_each if actual_each else 0.0
    rows.append((desc, qty, area, actual_each, bench_each, diff, err))
    tot_actual += actual_each * qty
    tot_bench += bench_each * qty
    tot_area += area * qty
    tot_units += qty
    print("%-9s %-13s %3d %7.3f %10.2f %11.2f %11.2f %9.2f %+7.1f%%"
          % (desc, size, qty, area, actual_each, bench_m2, bench_each, diff, err))

print("-" * 104)
print("units %d   area %.2f m2" % (tot_units, tot_area))
print("BSW ACTUAL total frames    : GBP %10.2f  (GBP %.2f/m2)" % (tot_actual, tot_actual / tot_area))
print("BENCHMARK total (with x1.10): GBP %10.2f  (GBP %.2f/m2)" % (tot_bench, tot_bench / tot_area))
print("difference                 : GBP %+10.2f  (%+.1f%% vs actual)"
      % (tot_bench - tot_actual, 100.0 * (tot_bench - tot_actual) / tot_actual))

# what the register says WITHOUT the Sheerline correction
raw = 0.0
for r in range(9, 40):
    if not ws.cell(r, 2).value:
        continue
    area = ws.cell(r, 15).value or 0
    qty = ws.cell(r, 6).value or 0
    if not area:
        continue
    rr = p.find_rate("aluminium casement window, glazed", area, supplier="bsw")
    if rr:
        raw += rr.entry["median"] * area * qty
print()
print("UNCORRECTED register median: GBP %10.2f  (GBP %.2f/m2)  %+.1f%% vs actual"
      % (raw, raw / tot_area, 100.0 * (raw - tot_actual) / tot_actual))

errs = sorted(x[6] for x in rows)
print()
print("per-type error spread: min %+.1f%%  median %+.1f%%  max %+.1f%%  (n=%d)"
      % (errs[0], errs[len(errs) // 2], errs[-1], len(errs)))
inside = [e for e in errs if abs(e) <= 20]
print("types within +/-20%%: %d of %d" % (len(inside), len(errs)))

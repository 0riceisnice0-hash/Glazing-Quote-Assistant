import glob, openpyxl
p = glob.glob(r"test-results\mary-inbox\queue\20260727T1049-z2KAAAAA-att\*Pricing.xlsx")[0]
ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]

lines = []
for r in range(9, 55):
    d, sz, q, rate, tot = (ws.cell(r, c).value for c in (2, 4, 5, 7, 8))
    if d and q:
        lines.append((r, d, sz, q, rate, tot))

items = sum(t for *_, t in lines)
qty = sum(q for *_, q, _, _ in lines)
inst, tele, tot = ws["H56"].value, ws["H57"].value, ws["H58"].value
mastic, epdm = ws["H62"].value, ws["H63"].value

print(f"line rows {len(lines)}, units {qty}")
print(f"sum of items    : {items:,.2f}")
print(f"INSTALLATION    : {inst:,.2f}")
print(f"TELEFLEX        : {tele:,.2f}   ({tele/tot*100:.1f}% of total)")
print(f"computed total  : {items+inst+tele:,.2f}")
print(f"stated TOTAL    : {tot:,.2f}    delta {tot-(items+inst+tele):+,.2f}")
print(f"OPTIONAL mastic {mastic:,.2f} / EPDM {epdm:,.2f}  (sum {mastic+epdm:,.2f})")
print()
print("rate x qty mismatches:")
for r, d, sz, q, rate, t in lines:
    if abs(rate * q - t) > 0.02:
        print(f"  row {r} {d}: {q} x {rate:,.2f} = {rate*q:,.2f} vs {t:,.2f}")
print()
# area / rate sanity
print("per-unit m2 and GBP/m2:")
tot_area = 0
for r, d, sz, q, rate, t in lines:
    try:
        w, h = [float(x.strip()) for x in sz.lower().replace("  ", " ").split("x")]
    except Exception:
        print(f"  row {r} {d}: cannot parse size {sz!r}")
        continue
    a = w * h / 1e6
    tot_area += a * q
    print(f"  {d:<18} {sz:<14} {a:6.3f} m2 x{q}  rate {rate:>8,.2f}  = {rate/a:>8,.0f}/m2")
print(f"\nTOTAL AREA {tot_area:,.2f} m2 ; items only {items/tot_area:,.0f}/m2 ; incl teleflex+install {tot/tot_area:,.0f}/m2")
print(f"install {inst:,.2f} over {qty} units = {inst/qty:,.2f}/unit")

import glob, openpyxl
p = glob.glob(r"test-results\mary-inbox\queue\20260727T0949-z2JAAAAA-att\*Pricing.xlsx")[0]
ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]

lines = []
for r in range(9, 57):
    d, sz, q, rate, tot = (ws.cell(r, c).value for c in (3, 5, 6, 8, 9))
    if d and q:
        lines.append((r, d, sz, q, rate, tot))

items = sum(t for *_, t in lines)
qty = sum(q for *_, q, _, _ in lines)
inst = ws["I58"].value
mastic = ws["I59"].value
epdm = ws["I60"].value
sub = ws["I62"].value
mcd = ws["I64"].value
tot = ws["I65"].value

print(f"line items         : {len(lines)} rows, {qty} units")
print(f"sum of item totals : {items:,.2f}")
print(f"INSTALLATION       : {inst:,.2f}")
print(f"EXTERNAL MASTIC    : {mastic:,.2f}")
print(f"EPDM               : {epdm:,.2f}")
print(f"computed subtotal  : {items+inst+mastic+epdm:,.2f}")
print(f"stated SUBTOTAL    : {sub:,.2f}   delta {sub-(items+inst+mastic+epdm):+,.2f}")
print()
print(f"2.5% of subtotal   : {sub*0.025:,.2f}")
print(f"stated MCD         : {mcd:,.2f}")
print(f"subtotal + MCD     : {sub+mcd:,.2f}")
print(f"stated TOTAL       : {tot:,.2f}   delta {tot-(sub+mcd):+,.2f}")
print()
print(f"pre-MCD, pre-extras (base as audited 23/07): {items+inst:,.2f}")
print(f"gross-up alternative (sub/0.975 then -2.5%): {sub/0.975:,.2f} -> net {sub:,.2f}")
print()
# rate x qty check
print("ROWS WHERE rate*qty != total (>0.02):")
for r, d, sz, q, rate, t in lines:
    if abs(rate * q - t) > 0.02:
        print(f"  row {r:>3} {d:<22} {q} x {rate:,.4f} = {rate*q:,.2f} vs stated {t:,.2f}  ({t-rate*q:+,.2f})")
print()
print("NON-ROUND UNIT RATES (sign of a total back-divided by qty):")
for r, d, sz, q, rate, t in lines:
    if abs(round(rate, 2) - rate) > 1e-9:
        print(f"  row {r:>3} {d:<22} qty {q:>3}  rate {rate!r}")

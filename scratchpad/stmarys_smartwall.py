import pdfplumber, openpyxl, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating")

with pdfplumber.open(B + r"\2. Supplier Quotes\BSW\ST MARYS.pdf") as pdf:
    t = "\n".join((p.extract_text() or "") for p in pdf.pages)

# position -> system, size, qty, price
print("BELLVIEW 0000000483 - SYSTEM PER POSITION")
print("=" * 96)
blocks = re.split(r"\n(?=0\d\d\s+\d+\s+Pcs)", t)
for b in blocks:
    m = re.match(r"(0\d\d)\s+(\d+)\s+Pcs\s+([\d,]+\s*x\s*[\d,]+)\s*mm\s+(.*?)\s+([\d,]+\.\d\d)\s+([\d,]+\.\d\d)", b)
    if not m:
        continue
    sysm = re.search(r"System:\s*([^\n]+)", b)
    bead = re.findall(r"IMP614 (\d+)MM GLAZING BEAD", b)
    glz = re.findall(r"\d+ x ([^\n]*(?:Lami|Tuff|prepared)[^\n]*)", b)
    print("  pos %s  qty %s  %s mm  GBP %s each / %s total"
          % (m.group(1), m.group(2), m.group(3), m.group(5), m.group(6)))
    print("        SYSTEM : %s" % (sysm.group(1).strip() if sysm else "?"))
    print("        BEAD   : %s" % (", ".join(set(bead)) + "mm" if bead else "not stated"))
    for g in sorted(set(glz)):
        print("        GLASS  : %s" % g.strip())

# value the Smart Wall Pocket lines out of the workbook
P = B + r"\3. Client Quote\SS\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx"
ws = openpyxl.load_workbook(P, data_only=True)["Pricing Document "]
POCKET = {"Type G", "Type I", "Type L", "Type O", "Type U", "Type AF"}
MC600 = {"Type AK"}
print()
print("VALUE AT STAKE - workbook rows 41-47")
print("=" * 96)
tot_p = tot_m = cost_p = cost_m = 0.0
area_p = area_m = 0.0
units_p = units_m = 0
for r in range(41, 48):
    desc = str(ws.cell(r, 3).value or "").strip()
    qty = ws.cell(r, 6).value or 0
    sell = ws.cell(r, 9).value or 0
    frames = (ws.cell(r, 10).value or 0) * qty
    add = (ws.cell(r, 12).value or 0) * qty
    area = (ws.cell(r, 15).value or 0) * qty
    grp = "POCKET" if desc in POCKET else ("MC600" if desc in MC600 else "?")
    print("  %-8s %-8s qty %d  sell %10.2f  supply %10.2f  add %8.2f  %6.3f m2"
          % (grp, desc, qty, sell, frames, add, area))
    if grp == "POCKET":
        tot_p += sell; cost_p += frames + add; area_p += area; units_p += qty
    else:
        tot_m += sell; cost_m += frames + add; area_m += area; units_m += qty

print("-" * 96)
print("  SMA SMART WALL POCKET (non-thermally-broken)  %d units  %.3f m2   SELL %10.2f   cost %9.2f"
      % (units_p, area_p, tot_p, cost_p))
print("  SMA MC600 PLUS (curtain walling)              %d units  %.3f m2   SELL %10.2f   cost %9.2f"
      % (units_m, area_m, tot_m, cost_m))

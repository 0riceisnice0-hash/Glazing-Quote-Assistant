import pdfplumber, openpyxl, re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\E T & S Construction\St Mary's Refurbishment\1. Estimating")

with pdfplumber.open(os.path.join(BASE, r"2. Supplier Quotes\BSW\qt252799.pdf")) as pdf:
    bsw = "\n".join((p.extract_text() or "") for p in pdf.pages)

# "Qty: 6 Prestige Casement Location: type b £4,560.66"
quoted = {}
for m in re.finditer(r"Qty:\s*(\d+)\s+[^\n]*?Location:\s*(type\s+[a-z]{1,2}|TYPE\s+G\s+INSERT)\s*£\s*([\d,]+\.\d\d)",
                     bsw, re.I):
    qty, ref, tot = int(m.group(1)), m.group(2).strip().lower(), float(m.group(3).replace(",", ""))
    quoted[ref] = (qty, tot)

wb = openpyxl.load_workbook(os.path.join(
    BASE, r"3. Client Quote\SS\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx"),
    data_only=True)
ws = wb["Pricing Document "]

print("%-10s %5s %5s  %12s %12s  %s" % ("type", "sold", "quot", "workbook P", "BSW total", "verdict"))
bad = 0
for r in range(9, 40):
    desc = (ws.cell(r, 3).value or "").strip()          # "Type A"
    qty = ws.cell(r, 6).value or 0
    p = ws.cell(r, 16).value or 0                        # P = frames x qty
    key = desc.lower()
    q = quoted.get(key)
    if not q:
        print("%-10s %5d %5s  %12.2f %12s  NO BSW LINE FOUND" % (desc, qty, "-", p, "-"))
        bad += 1
        continue
    ok_q = (q[0] == qty)
    ok_p = abs(q[1] - p) < 0.02
    verdict = "ok" if (ok_q and ok_p) else ("QTY MISMATCH " if not ok_q else "") + ("PRICE MISMATCH" if not ok_p else "")
    if not (ok_q and ok_p):
        bad += 1
    print("%-10s %5d %5d  %12.2f %12.2f  %s" % (desc, qty, q[0], p, q[1], verdict))

print("\nTYPE G INSERT (Sheerline casement into the Smart Wall element):", quoted.get("type g insert"))
print("mismatches:", bad)

import pdfplumber, openpyxl, os, re

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\E T & S Construction\St Mary's Refurbishment\1. Estimating")

# ---------- 1. workbook supplier columns ----------
wb = openpyxl.load_workbook(os.path.join(
    BASE, r"3. Client Quote\SS\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx"),
    data_only=True)
ws = wb["Pricing Document "]
win = sma = 0.0
for r in range(9, 48):
    code = ws.cell(r, 2).value
    frames = ws.cell(r, 10).value or 0
    qty = ws.cell(r, 6).value or 0
    if not code:
        continue
    if r <= 39:
        win += frames * qty
    else:
        sma += frames * qty
print("workbook window frames total : %.2f   (M3 says %s)" % (win, ws.cell(3, 13).value))
print("workbook SMA frames total    : %.2f   (M4 says %s)" % (sma, ws.cell(4, 13).value))
print("workbook combined            : %.2f   (M5 says %s)" % (win + sma, ws.cell(5, 13).value))

# ---------- 2. supplier quote scan ----------
def scan(path, label):
    with pdfplumber.open(path) as pdf:
        txt = "\n".join((p.extract_text() or "") for p in pdf.pages)
    print("\n" + "=" * 88)
    print(label, "| pages:", len(txt.split("Page ")), "| chars:", len(txt))
    for kw in ("Total", "TOTAL", "Discount", "DISCOUNT", "Nett", "NETT", "Net ",
               "U Value", "U-Value", "Uw", "W/m"):
        for m in re.finditer(re.escape(kw), txt):
            line = txt[max(0, m.start() - 90): m.start() + 110].replace("\n", " | ")
            print("  [%s] %s" % (kw, line))
            break
    # coating / glass make-ups
    makeups = set(re.findall(r"[0-9][^\n]*(?:Lam|Lami|Tuff|Tough)[^\n]*", txt))
    print("  -- distinct glass make-up strings (%d):" % len(makeups))
    for m in sorted(makeups)[:14]:
        print("     ", m.strip()[:110])

scan(os.path.join(BASE, r"2. Supplier Quotes\BSW\ST MARYS.pdf"), "BELLVIEW 0000000483 (SMA doors + CW)")
scan(os.path.join(BASE, r"2. Supplier Quotes\BSW\qt252799.pdf"), "BSW QT252799 (Sheerline windows)")
for f in sorted(os.listdir(os.path.join(BASE, r"2. Supplier Quotes\Aplus"))):
    if f.lower().endswith(".pdf"):
        scan(os.path.join(BASE, r"2. Supplier Quotes\Aplus", f), "APLUS / " + f)

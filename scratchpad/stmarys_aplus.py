import pdfplumber, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\2. Supplier Quotes")

def txt(p):
    with pdfplumber.open(p) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)

print("#" * 88, "\nAPLUS QP70172.pdf (summary sheet)\n")
print(txt(os.path.join(BASE, "Aplus", "QP70172.pdf")))

print("#" * 88, "\nAPLUS 'A Plus Quote.pdf' - first 3500 chars\n")
t = txt(os.path.join(BASE, "Aplus", "A Plus Quote.pdf"))
print(t[:3500])

print("\n" + "#" * 88, "\nBSW QT252799 - any whole-window Uw / U value statement?\n")
b = txt(os.path.join(BASE, "BSW", "qt252799.pdf"))
for pat in (r"U\s?value", r"Uw", r"W/m", r"1\.4", r"1\.3", r"EcoPlus", r"g\s?value",
            r"solar", r"Suncool", r"SKN", r"Coolite", r"Planitherm"):
    hits = list(re.finditer(pat, b, re.I))
    print("  /%s/ -> %d" % (pat, len(hits)))
    if hits:
        m = hits[0]
        print("      ", b[max(0, m.start()-110):m.start()+130].replace("\n", " | "))

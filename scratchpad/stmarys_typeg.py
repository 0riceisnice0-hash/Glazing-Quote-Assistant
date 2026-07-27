import pdfplumber, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\2. Supplier Quotes"
     r"\BSW\qt252799.pdf")

with pdfplumber.open(P) as pdf:
    for i, pg in enumerate(pdf.pages, 1):
        t = pg.extract_text() or ""
        if re.search(r"TYPE G", t, re.I):
            print("=" * 90)
            print("PAGE", i)
            print(t)

# every "Location:" line = one priced element, to see the full window list
with pdfplumber.open(P) as pdf:
    txt = "\n".join((p.extract_text() or "") for p in pdf.pages)
locs = re.findall(r"Location:\s*([^\n£]*)£?\s*([\d,]+\.\d\d)?", txt)
print("\n\nALL PRICED LOCATIONS (%d):" % len(locs))
for a, b in locs:
    if a.strip() or b:
        print("   %-40s %s" % (a.strip()[:40], b or ""))

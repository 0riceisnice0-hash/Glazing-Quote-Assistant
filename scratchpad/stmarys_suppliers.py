import pdfplumber, os, re

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\2. Supplier Quotes")

for sup in ("BSW", "Aplus"):
    d = os.path.join(BASE, sup)
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".pdf"):
            continue
        p = os.path.join(d, f)
        try:
            with pdfplumber.open(p) as pdf:
                npg = len(pdf.pages)
                txt = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
        except Exception as e:
            print("!! %s/%s -> %s" % (sup, f, e))
            continue
        print("#" * 92)
        print("%s / %s   pages=%d  chars=%d" % (sup, f, npg, len(txt)))
        if len(txt) < 40:
            print("  (no text layer - scanned)")
            continue
        print(txt[:6000])

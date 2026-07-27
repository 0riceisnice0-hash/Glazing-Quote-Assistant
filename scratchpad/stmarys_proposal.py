import pdfplumber

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\3. Client Quote"
     r"\ET & S Construction - St Mary's Refurbishment Proposal.pdf")

with pdfplumber.open(P) as pdf:
    print("PAGES:", len(pdf.pages))
    for i, pg in enumerate(pdf.pages, 1):
        t = pg.extract_text() or ""
        print("=" * 88)
        print("PAGE", i)
        print(t)

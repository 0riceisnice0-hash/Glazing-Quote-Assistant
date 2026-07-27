import sys, glob, pdfplumber
p = glob.glob(sys.argv[1])[0]
first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
last = int(sys.argv[3]) if len(sys.argv) > 3 else 999
with pdfplumber.open(p) as pdf:
    print(f"### {p}  ({len(pdf.pages)} pages)")
    for i, pg in enumerate(pdf.pages, 1):
        if i < first or i > last:
            continue
        print(f"\n=============== PAGE {i} ===============")
        print(pg.extract_text() or "(no text layer)")

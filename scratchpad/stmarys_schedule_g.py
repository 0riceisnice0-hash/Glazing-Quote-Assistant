import pdfplumber, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\schedule-09-07\4.00 - Architectural\2376-09 window schedule.pdf")

with pdfplumber.open(P) as pdf:
    for i, pg in enumerate(pdf.pages, 1):
        t = pg.extract_text() or ""
        if re.search(r"type\s+g\b", t, re.I):
            print("#" * 90)
            print("PAGE", i, "- contains 'type G'")
            for ln in t.split("\n"):
                if re.search(r"type\s+[a-z]{1,2}\b|door|screen|insert|opening pattern", ln, re.I):
                    print("   ", ln.strip()[:190])

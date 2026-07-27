import pdfplumber, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\mary-inbox\processed"
     r"\20260727T1556-xgsAAAAA-att\Smart_Commercial Brochure.pdf")

with pdfplumber.open(P) as pdf:
    pages = [(i, p.extract_text() or "") for i, p in enumerate(pdf.pages, 1)]
full = "\n".join(t for _, t in pages)
print("pages: %d   chars: %d" % (len(pages), len(full)))

# 1. every U-value statement, with its page and surrounding context
print()
print("EVERY U-VALUE STATEMENT IN THE BROCHURE")
print("=" * 100)
for i, t in pages:
    for m in re.finditer(r"U[\s\-]?[Vv]alue[^\n]{0,120}", t):
        print("  p%-3d %s" % (i, m.group(0).strip()[:120]))

print()
print("SYSTEM NAMES PRESENT")
print("=" * 100)
for name in ["Smart Wall", "Pocket", "MC600", "MC 600", "Alitherm 600", "Alitherm",
             "Smart Wall Pocket", "shop front", "shopfront", "curtain wall"]:
    n = len(re.findall(re.escape(name), full, re.I))
    print("  %-20s %d" % (name, n))

# 2. pages that mention the systems we care about
print()
print("PAGES MENTIONING MC600 / ALITHERM 600 / POCKET")
print("=" * 100)
for i, t in pages:
    if re.search(r"MC\s?600|Alitherm 600|Pocket", t, re.I):
        print("-" * 92)
        print("PAGE", i)
        print(t[:1400])

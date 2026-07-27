import pdfplumber, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\4.00 - Architectural\2376-08 door schedule.pdf")
with pdfplumber.open(P) as pdf:
    full = "\n".join((p.extract_text() or "") for p in pdf.pages)

print("D.11 IN FULL - the area-weighted average note")
print("=" * 100)
m = re.search(r"D\.11.{0,1500}", full, re.S)
print(m.group(0)[:1500] if m else "not found")

print()
print("EVERY 'area weighted' / 'average' REFERENCE")
print("=" * 100)
for mm in re.finditer(r"[^\n]{0,160}(area weighted|average)[^\n]{0,160}", full, re.I):
    print("  ...", mm.group(0).strip()[:300])

print()
print("TITLE BLOCK / REVISION OF 2376-08")
print("=" * 100)
for pat in (r"rev(ision)?[^\n]{0,60}", r"\b\d{2}\.\d{2}\.\d{2}\b[^\n]{0,60}",
            r"2376\s*-?\s*08[^\n]{0,60}", r"scale[^\n]{0,60}", r"drawn[^\n]{0,50}"):
    hits = list(re.finditer(pat, full, re.I))
    print("  /%s/ -> %d" % (pat[:26], len(hits)))
    for h in hits[:4]:
        print("       ", h.group(0).strip()[:110])

print()
print("EXTERNAL ALUMINIUM DOORS - REF vs SIZE (compare with what we priced)")
print("=" * 100)
print("  we priced: Type G 968x3620 (x2) | Type I 1530x2410 | Type L 955x2410 |")
print("             Type O 1530x2410 | Type U 929x2370 | Type AF 1520x2100")
print()
for ref in ["D.01", "D.11", "D.14", "D.17", "D.22", "D.26"]:
    m = re.search(re.escape(ref) + r"(.{0,420})", full, re.S)
    if not m:
        continue
    body = m.group(1)
    sizes = re.findall(r"\d{3,4}\s*x\s*\d{3,4}(?:\s*\+\s*\d+mm)?", body)
    loc = re.search(re.escape(ref) + r"\s+([a-z][^\n]{0,55})", full)
    print("  %-5s sizes: %-46s  loc: %s"
          % (ref, "; ".join(sizes[:3])[:46], (loc.group(1).strip()[:45] if loc else "?")))

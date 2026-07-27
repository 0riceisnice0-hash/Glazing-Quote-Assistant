import sys, glob, re, pdfplumber
p = glob.glob(sys.argv[1])[0]
money = re.compile(r"(?:GBP|£)\s*[\d,]+\.\d{2}|\b\d{1,3},\d{3}\.\d{2}\b")
pas24_no, types, supplier = [], [], set()
with pdfplumber.open(p) as pdf:
    print(f"### {p}: {len(pdf.pages)} pages")
    for i, pg in enumerate(pdf.pages, 1):
        t = pg.extract_text() or ""
        for m in money.findall(t):
            print(f"  MONEY p{i}: {m}")
        if "NOT BEEN TESTED TO PAS24" in t:
            pas24_no.append(i)
        for w in ("Aplus", "A Plus", "APLUS", "aluminium", "Modeal", "Technal", "Logikal", "Crystal"):
            if w in t:
                supplier.add(w)
        for m in re.findall(r"^(WIN TYPE [\w ]+|DOOR TYPE [\w() ]+|LOUVRE[\w ]*)$", t, re.M):
            types.append((i, m.strip()))
print(f"\nPages carrying 'NOT BEEN TESTED TO PAS24': {pas24_no}  (count {len(pas24_no)})")
print(f"Supplier/system words present: {sorted(supplier)}")
print(f"\nDistinct type headings ({len(types)}):")
seen = set()
for i, t in types:
    if t not in seen:
        seen.add(t)
        print(f"  p{i:>3}  {t}")

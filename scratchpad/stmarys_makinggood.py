import openpyxl, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\-\2, 3, 4 - SOW St. Marys.xlsx")
wb = openpyxl.load_workbook(P, data_only=True)

PATS = {
 "making good":      r"mak(e|ing) good",
 "reveal/plaster":   r"reveal|plaster|render|patch|dab|skim",
 "decoration":       r"decorat|paint",
 "tender validity":  r"validity|remain open|hold(ing)? (the )?price|withdraw|\b\d+\s*(days|weeks|months)\b.{0,40}tender|tender.{0,40}\b\d+\s*(days|weeks|months)\b",
 "cill/board":       r"\bcill|window board|sill",
 "intercom/entry":   r"intercom|door entry|access control",
 "scaffold":         r"scaffold",
 "cross-ref to 6.01": r"6\.01",
}

for name in ("2. Prelims", "3. SOW"):
    ws = wb[name]
    print("#" * 96)
    print("SHEET:", name)
    for label, pat in PATS.items():
        hits = []
        for r in ws.iter_rows():
            txt = " ".join(str(c.value).strip() for c in r if c.value not in (None, ""))
            if txt and re.search(pat, txt, re.I):
                hits.append((r[0].row, txt))
        print("  -- %-18s %d hit(s)" % (label, len(hits)))
        for row, txt in hits[:7]:
            print("       r%-4d %s" % (row, txt[:175]))

import openpyxl, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\-\2, 3, 4 - SOW St. Marys.xlsx")
wb = openpyxl.load_workbook(P, data_only=True)

KEY = re.compile(r"window|glaz|curtain|door|scaffold|access|mewp|tower|plant|"
                 r"u.?value|thermal|solar|secured by design|sbd|restrictor|"
                 r"aluminium|screen|programme|completion|retention|warrant|"
                 r"insur|liquidated|dayworks|asbestos", re.I)

for name in ("2. Prelims", "3. SOW"):
    ws = wb[name]
    print("#" * 94)
    print("SHEET:", name, ws.dimensions)
    for r in ws.iter_rows():
        txt = " ".join(str(c.value).strip() for c in r if c.value not in (None, ""))
        if txt and KEY.search(txt):
            print("  r%-4d %s" % (r[0].row, txt[:185]))

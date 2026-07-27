import openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\-\2, 3, 4 - SOW St. Marys.xlsx")
wb = openpyxl.load_workbook(P, data_only=True)

def block(sheet, lo, hi, label):
    ws = wb[sheet]
    print("=" * 92)
    print(label, "  [%s rows %d-%d]" % (sheet, lo, hi))
    for r in ws.iter_rows(min_row=lo, max_row=hi):
        txt = " ".join(str(c.value).strip() for c in r if c.value not in (None, ""))
        if txt:
            print("  r%-4d %s" % (r[0].row, txt[:200]))

block("2. Prelims", 28, 40, "PRELIMS F - INCLUDE EVERYTHING NECESSARY")
block("2. Prelims", 174, 190, "PRELIMS - SCAFFOLDING")
block("3. SOW", 8, 24, "SOW - CONTRACT TERMS")
block("3. SOW", 45, 58, "SOW SECTION 1 - STRIP OUT")
block("3. SOW", 70, 80, "SOW SECTION 6 - EXTERNAL WINDOWS AND DOORS")
block("Front Cover & Contents", 1, 10, "SITE ADDRESS AS TENDERED BY THE CLIENT")

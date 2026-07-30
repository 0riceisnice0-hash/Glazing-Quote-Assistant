# -*- coding: utf-8 -*-
import os, sys, openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_calibrate as cal, mary_quote_reader as reader
want = sys.argv[1].lower()
for q in reader.scan(cal.TENDERS):
    if want in q["file"].lower():
        print("FILE:", q["path"]); break
else:
    sys.exit("no match")
wb = openpyxl.load_workbook(q["path"], data_only=True)
print("SHEETS:", wb.sheetnames)
for ws in wb.worksheets:
    if not ws.title.strip().lower().startswith("pricing document"):
        continue
    print("=== %s  dims=%s ===" % (ws.title, ws.dimensions))
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        cells = ["" if c is None else (("%.2f" % c) if isinstance(c, float) else str(c)) for c in row]
        while cells and cells[-1] == "": cells.pop()
        if cells:
            print("%3d | %s" % (i, " | ".join(c[:26] for c in cells)))

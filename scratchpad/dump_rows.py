# -*- coding: utf-8 -*-
"""Dump the raw grid of a pricing document, header row included.

The non-reconciling documents are the same set as the supplier-ratio outliers,
so before calling either a finding, look at the actual cells."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_calibrate as cal
import mary_quote_reader as reader

want = sys.argv[1].lower()
import openpyxl

for q in reader.scan(cal.TENDERS):
    if want not in q["file"].lower():
        continue
    print("=" * 110)
    print(q["file"])
    print("=" * 110)
    wb = openpyxl.load_workbook(q["path"], read_only=True, data_only=True)
    sheets = [w for w in wb.worksheets if w.title.strip().lower().startswith("pricing document")]
    if not sheets:
        print("  no pricing document sheet: %s" % [w.title for w in wb.worksheets])
        wb.close()
        continue
    ws = sheets[0]
    for rn, row in enumerate(ws.iter_rows(values_only=True), 1):
        cells = list(row)
        if not any(c is not None and str(c).strip() for c in cells):
            continue
        bits = []
        for i, c in enumerate(cells[:15]):
            if c is None or not str(c).strip():
                continue
            s = "{:,.2f}".format(c) if isinstance(c, (int, float)) else str(c)[:26]
            bits.append("%d:%s" % (i, s))
        print("r%-3d %s" % (rn, "  ".join(bits)))
        if rn > int(os.environ.get("MAXROW", 46)):
            print("  ...")
            break
    wb.close()
    break

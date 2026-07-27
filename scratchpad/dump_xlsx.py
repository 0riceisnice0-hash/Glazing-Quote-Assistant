import sys, openpyxl
p = sys.argv[1]
for data_only in (False, True):
    wb = openpyxl.load_workbook(p, data_only=data_only)
    print("=" * 30, "DATA_ONLY" if data_only else "FORMULAS", "=" * 30)
    for ws in wb.worksheets:
        print(f"--- SHEET [{ws.title}]  dims={ws.dimensions}")
        for row in ws.iter_rows():
            cells = []
            for c in row:
                if c.value is not None and str(c.value).strip() != "":
                    cells.append(f"{c.coordinate}={c.value!r}")
            if cells:
                print("  " + " | ".join(cells))

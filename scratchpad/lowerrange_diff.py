# -*- coding: utf-8 -*-
"""What did the Lower Range addendum actually change? V3.1 (in the pack) vs V3.2.

Row counts differ by one, so compare by clarification reference rather than by
row position - same discipline as the St Mary's schedule comparison.
"""
import openpyxl

A = r"test-results\lower-range-input\pack\-\Clarification Log - V3.1.xlsx"
B = r"test-results\lower-range-input\addendum\-\Clarification Log - V3.2.xlsx"


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    rows, refcol = {}, None
    for row in ws.iter_rows(values_only=True):
        vals = ["" if v is None else str(v).strip() for v in row]
        if refcol is None:
            if "Reference" in vals:
                refcol = vals.index("Reference")
            continue
        ref = vals[refcol] if refcol < len(vals) else ""
        if ref.upper().startswith("C") and ref[1:].isdigit():
            rows[ref.upper()] = vals
    return rows


a, b = load(A), load(B)
print("V3.1 refs: %d   V3.2 refs: %d" % (len(a), len(b)))
print("only in V3.1 (REMOVED):", sorted(set(a) - set(b)))
print("only in V3.2 (ADDED)  :", sorted(set(b) - set(a)))
print()
for ref in sorted(set(a) & set(b), key=lambda r: int(r[1:])):
    if a[ref] != b[ref]:
        print("CHANGED %s" % ref)
        for i, (x, y) in enumerate(zip(a[ref], b[ref])):
            if x != y:
                print("   col %d" % i)
                print("     V3.1: %s" % x[:400])
                print("     V3.2: %s" % y[:400])
print()
print("=== every row only in one version, in full ===")
for ref in sorted(set(a) ^ set(b), key=lambda r: int(r[1:])):
    src = a.get(ref) or b.get(ref)
    where = "V3.1 only" if ref in a else "V3.2 only"
    print("%s %s" % (where, ref))
    for v in src:
        if v:
            print("   %s" % v[:400])

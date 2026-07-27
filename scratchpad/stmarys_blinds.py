# -*- coding: utf-8 -*-
"""Locate the surviving blind note in rev A, and hunt for blinds in what we priced."""
import glob
import os
import re
import pdfplumber
import openpyxl

REVA = r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-09A window schedule.pdf"

print("### surviving 'integral blind' note in rev A")
with pdfplumber.open(REVA) as pdf:
    for i, pg in enumerate(pdf.pages):
        for ln in (pg.extract_text() or "").splitlines():
            if "integral blind" in ln.lower():
                print("  p%d: %s" % (i + 1, re.sub(r"\s+", " ", ln)[:300]))

JOB = ("C:\\Users\\zacpl\\OneDrive - Fenster Glazing (1)\\Commercial\\1. Tender Documents\\"
       "E T & S Construction\\St Mary's Refurbishment\\1. Estimating")

print("\n### 'blind' anywhere in the client pricing / internal pricing")
for xl in glob.glob(os.path.join(JOB, "3. Client Quote", "*.xlsx")) + \
          glob.glob(os.path.join(JOB, "3. Client Quote", "SS", "*.xlsx")):
    try:
        wb = openpyxl.load_workbook(xl, data_only=True)
    except Exception as e:
        print("  !! %s: %s" % (os.path.basename(xl), e))
        continue
    hits = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and "blind" in c.value.lower():
                    hits.append("%s!%s %s" % (ws.title, c.coordinate, c.value[:120]))
    print("  %-55s %s" % (os.path.basename(xl)[:55], hits if hits else "no 'blind' text"))

print("\n### 'blind' in the supplier quotes and the issued proposal")
pdfs = glob.glob(os.path.join(JOB, "2. Supplier Quotes", "**", "*.pdf"), recursive=True) + \
       glob.glob(os.path.join(JOB, "3. Client Quote", "*.pdf"))
for p in sorted(pdfs):
    if os.path.getsize(p) > 20_000_000:
        print("  %-45s (skipped, %.0f MB)" % (os.path.basename(p)[:45], os.path.getsize(p) / 1e6))
        continue
    try:
        with pdfplumber.open(p) as pdf:
            found = []
            for i, pg in enumerate(pdf.pages):
                for ln in (pg.extract_text() or "").splitlines():
                    if "blind" in ln.lower():
                        found.append("p%d %s" % (i + 1, re.sub(r"\s+", " ", ln)[:120]))
        print("  %-45s %s" % (os.path.basename(p)[:45], found[:4] if found else "no 'blind' text"))
    except Exception as e:
        print("  %-45s !! %s" % (os.path.basename(p)[:45], e))

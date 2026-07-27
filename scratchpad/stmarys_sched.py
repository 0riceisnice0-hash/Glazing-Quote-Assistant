# -*- coding: utf-8 -*-
"""Dump both window schedules so the 09/07 (priced) and 24/07 rev A can be compared."""
import sys
import pdfplumber

for tag, path in [
    ("PRICED 09/07  2376-09", r"test-results\st-marys-input\schedule-09-07\4.00 - Architectural\2376-09 window schedule.pdf"),
    ("ADDENDUM 24/07  2376-09A", r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-09A window schedule.pdf"),
]:
    print("=" * 78)
    print(tag)
    print("=" * 78)
    with pdfplumber.open(path) as pdf:
        for i, pg in enumerate(pdf.pages):
            print("--- page %d (%.0f x %.0f) ---" % (i + 1, pg.width, pg.height))
            txt = pg.extract_text() or "(no text layer)"
            print(txt)

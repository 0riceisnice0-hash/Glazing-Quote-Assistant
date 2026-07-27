# -*- coding: utf-8 -*-
"""The addendum also re-issued the floor plans (04E->04F) and site plan (05D->05E).
Diff those too - Adam asked about scope, not just the window schedule."""
import difflib
import re
import pdfplumber

PAIRS = [
    ("proposed floor plans  04E -> 04F",
     r"test-results\st-marys-input\original-08-07\4.00 - Architectural\2376-04E proposed floor plans.pdf",
     r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-04F proposed floor plans.pdf"),
    ("proposed site plan    05D -> 05E",
     r"test-results\st-marys-input\original-08-07\4.00 - Architectural\2376-05D proposed site plan.pdf",
     r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-05E proposed site plan.pdf"),
]


def lines(path):
    out = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for ln in (pg.extract_text() or "").splitlines():
                ln = re.sub(r"\s+", " ", ln).strip()
                if ln:
                    out.append(ln)
    return out


for label, old, new in PAIRS:
    a, b = lines(old), lines(new)
    print("=" * 78)
    print("%s   (%d -> %d lines)" % (label, len(a), len(b)))
    print("=" * 78)
    changed = False
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        changed = True
        print("### %s" % tag.upper())
        for ln in a[i1:i2]:
            print("  - %s" % ln[:190])
        for ln in b[j1:j2]:
            print("  + %s" % ln[:190])
    if not changed:
        print("  no text-layer differences at all")
    print()

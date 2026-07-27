# -*- coding: utf-8 -*-
"""Compare the re-issued plans by content, not layout.

pdfplumber tokenises these two PDFs differently (937 vs 3285 lines for the same
drawing), so a line diff is meaningless. Compare the things that carry scope:
window refs, door refs, and the revision block.
"""
import re
from collections import Counter
import pdfplumber

PAIRS = [
    ("proposed floor plans 04E -> 04F",
     r"test-results\st-marys-input\original-08-07\4.00 - Architectural\2376-04E proposed floor plans.pdf",
     r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-04F proposed floor plans.pdf"),
    ("proposed site plan   05D -> 05E",
     r"test-results\st-marys-input\original-08-07\4.00 - Architectural\2376-05D proposed site plan.pdf",
     r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-05E proposed site plan.pdf"),
]


def text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def flat(t):
    """Strip whitespace entirely - defeats the per-character tokenisation noise."""
    return re.sub(r"\s+", "", t)


for label, old, new in PAIRS:
    a, b = text(old), text(new)
    print("=" * 78)
    print(label)
    print("=" * 78)

    for name, pat in [("window refs W.nn", r"W\.\d+"),
                      ("door refs D.nn", r"D\.\d+"),
                      ("curtain walling refs", r"CW[\.\s]?\d+")]:
        ca, cb = Counter(re.findall(pat, a)), Counter(re.findall(pat, b))
        oa, ob = sorted((ca - cb).elements()), sorted((cb - ca).elements())
        print("  %-22s old=%-4d new=%-4d  %s" % (
            name, sum(ca.values()), sum(cb.values()),
            "IDENTICAL" if not oa and not ob else "DIFFERENT"))
        if oa:
            print("        dropped: %s" % oa[:30])
        if ob:
            print("        added  : %s" % ob[:30])

    fa, fb = flat(a), flat(b)
    print("  whitespace-stripped text identical: %s  (%d vs %d chars)"
          % (fa == fb, len(fa), len(fb)))

    for tag, t in (("old", a), ("new", b)):
        revs = re.findall(r"[A-Z] \d\d\.\d\d\.\d\d [a-z][a-z ]+", t)
        print("  %s revision notes: %s" % (tag, revs[-4:] if revs else "none found in text layer"))
    print()

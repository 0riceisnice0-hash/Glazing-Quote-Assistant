# -*- coding: utf-8 -*-
"""Line-diff the priced window schedule against the 24/07 rev A addendum."""
import difflib
import re
import pdfplumber

PRICED = r"test-results\st-marys-input\schedule-09-07\4.00 - Architectural\2376-09 window schedule.pdf"
REVA = r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-09A window schedule.pdf"


def lines(path):
    out = []
    with pdfplumber.open(path) as pdf:
        for i, pg in enumerate(pdf.pages):
            for ln in (pg.extract_text() or "").splitlines():
                ln = re.sub(r"\s+", " ", ln).strip()
                if ln:
                    out.append("p%d| %s" % (i + 1, ln))
    return out


a, b = lines(PRICED), lines(REVA)
print("priced 2376-09  : %d pages-worth, %d lines" % (len(set(x.split('|')[0] for x in a)), len(a)))
print("rev A  2376-09A : %d pages-worth, %d lines" % (len(set(x.split('|')[0] for x in b)), len(b)))
print()

# Compare page-blind: the interest is what text appeared / vanished.
sa = [x.split("| ", 1)[1] for x in a]
sb = [x.split("| ", 1)[1] for x in b]
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    print("### %s  priced[%d:%d] -> revA[%d:%d]" % (tag.upper(), i1, i2, j1, j2))
    for ln in sa[i1:i2]:
        print("  - %s" % ln[:200])
    for ln in sb[j1:j2]:
        print("  + %s" % ln[:200])
    print()

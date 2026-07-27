# -*- coding: utf-8 -*-
"""Prove what did and did not change between 2376-09 (priced) and 2376-09A (addendum).

The line diff suggests a single edit repeated across every window type. Verify by
comparing the things that drive price: window numbers, structural opening sizes,
opening patterns, and the count of the note that vanished.
"""
import re
from collections import Counter
import pdfplumber

PRICED = r"test-results\st-marys-input\schedule-09-07\4.00 - Architectural\2376-09 window schedule.pdf"
REVA = r"test-results\st-marys-input\revised-24-07\4.00 - Architectural\2376-09A window schedule.pdf"


def text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


a, b = text(PRICED), text(REVA)

def show(label, pat, flags=0):
    ca, cb = Counter(re.findall(pat, a, flags)), Counter(re.findall(pat, b, flags))
    only_a = sorted((ca - cb).elements())
    only_b = sorted((cb - ca).elements())
    print("%-28s priced=%-4d revA=%-4d  %s" % (
        label, sum(ca.values()), sum(cb.values()),
        "IDENTICAL" if not only_a and not only_b else "DIFFERENT"))
    if only_a:
        print("      only in priced : %s" % only_a[:25])
    if only_b:
        print("      only in rev A  : %s" % only_b[:25])


show("window numbers W.nn", r"W\.\d+")
show("window types", r"type [A-Z]{1,2} ")
show("structural opening sizes", r"\d[\d,]*w x [\d,]*h mm")
show("opening pattern clauses", r"opening pattern - [^\n]{0,60}")
show("restrictor notes", r"100mm restrictor openable area")
show("obscured glazing notes", r"obscured glazing[^\n]{0,40}")
show("u-value notes", r"u value of [\d.]+ w/m2k")
show("Secured by Design", r"Secured by Design standard")
show("INTEGRAL BLIND note", r"Magnetic operated integral blinds[^\n]{0,20}")
show("revision block", r"A \d\d\.\d\d\.\d\d [a-z ]+")

print()
print("Blind note in priced schedule : %d occurrences" % len(re.findall(r"Magnetic operated integral blinds", a)))
print("Blind note in rev A schedule  : %d occurrences" % len(re.findall(r"Magnetic operated integral blinds", b)))
print()
print("Revision note on rev A        : %s" % re.findall(r"A \d\d\.\d\d\.\d\d [a-z ]+", b)[:1])

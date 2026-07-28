# -*- coding: utf-8 -*-
"""Gordon Court's newest: one quantity, two figures, seven pages apart.

Their BSW letter stated GBP 182,787.76 twice as the total already quoted - the
workbook's figure, which they had established six turns earlier is GBP 217.66
light - while the same letter used the correct 183,005.42 in D2. Both figures for
one quantity, in one document, and the wrong one misstates BSW's own arithmetic
back to BSW.

Their diagnosis is the part that transfers: "A test you run once on one document
is not a test you have adopted." They found the internal-contradiction fault on
their client letter four turns ago and never re-ran it on the supplier letter.

So this is the numeric version of that test, run across every Riverside document
at once rather than one at a time: extract every figure, group by the quantity it
names, and look for a quantity carrying two values.
"""
import glob
import io
import os
import re

import openpyxl

DOCS = {}
for f in sorted(glob.glob('outputs/Riverside*')):
    e = os.path.splitext(f)[1].lower()
    if e == '.txt':
        DOCS[os.path.basename(f)] = io.open(f, encoding='utf-8', errors='ignore').read()
    elif e == '.xlsx':
        wb = openpyxl.load_workbook(f)
        DOCS[os.path.basename(f)] = ' | '.join(
            str(c.value) for ws in wb for row in ws.iter_rows()
            for c in row if c.value not in (None, ''))

# quantity -> the one value it must have, and the patterns that name it
QUANTITIES = [
    ("the sell, ex VAT",        {"5,990.22", "5990.22"},   r'5[,.]?990\.22'),
    ("the sell, inc VAT",       {"7,188.26", "7188.26"},   r'7[,.]?188\.26'),
    ("A Plus net",              {"4,845.22", "4845.22"},   r'4[,.]?845\.22'),
    ("unit rate",               {"2,835.11", "2835.11"},   r'2[,.]?835\.11'),
    ("items subtotal",          {"5,670.22", "5670.22"},   r'5[,.]?670\.22'),
    ("install",                 {"320.00", "320"},         r'\b320(?:\.00)?\b'),
    ("optional mastic",         {"53.20", "53.2"},         r'\b53\.20?\b'),
    ("mastic linear metres",    {"10.64"},                 r'\b10\.64\b'),
    ("geometric free area",     {"1.30"},                  r'\b1\.30\s?m2'),
    ("the requirement",         {"1", "1.0"},              r'\b1\s?m2\b'),
    ("delivery shortfall",      {"154.78"},                r'\b154\.78\b'),
    ("aerodynamic band low",    {"0.79"},                  r'\b0\.7[0-9]\b'),
    ("aerodynamic band high",   {"0.81"},                  r'\b0\.8[0-9]\b'),
    ("the vent size",           {"1130 x 1530"},           r'1130\s?x\s?1530'),
    ("A Plus resize",           {"1235 x 1583"},           r'1235\s?x\s?1583'),
    ("subcill",                 {"155"},                   r'\b155\s?mm'),
]

print("=" * 100)
print("ONE QUANTITY, TWO FIGURES? - every Riverside document at once")
print("=" * 100)
for name, allowed, pat in QUANTITIES:
    found = {}
    for doc, body in DOCS.items():
        hits = set(m.group(0).strip() for m in re.finditer(pat, body))
        if hits:
            found[doc] = hits
    if not found:
        continue
    values = set()
    for h in found.values():
        values |= h
    flag = "" if len(values) == 1 else "   <<< MORE THAN ONE VALUE"
    print("\n  %-24s %s%s" % (name, sorted(values), flag))
    for doc, hits in sorted(found.items()):
        print("       %-58s %s" % (doc[:58], sorted(hits)))

print()
print("=" * 100)
print("AND THE COUNTS EACH DOCUMENT ASSERTS ABOUT ITSELF")
print("=" * 100)
for doc, body in DOCS.items():
    if not doc.endswith('.txt'):
        continue
    heads = re.findall(r'(?m)^(\d+)\.\s', body)
    words = re.findall(r'(?i)\b(thirteen|twelve|eleven|fourteen|ten|nine|eight|three|two)\b[^.\n]{0,40}'
                       r'(?:items|questions|of these|are for)', body)
    if heads or words:
        print("\n  %-58s" % doc[:58])
        if heads:
            print("       numbered items present : %s (%s)" % (len(set(heads)), max(map(int, heads))))
        for w in set(words):
            print("       states in prose        : %s" % w)

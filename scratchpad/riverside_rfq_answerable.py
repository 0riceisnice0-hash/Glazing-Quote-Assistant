# -*- coding: utf-8 -*-
"""Gordon Court's RFQ check: for each question, can it be answered by reading
the quotation we already hold?

They found their B2 asked BSW to confirm D_E and D_U are door-and-sidelight
assemblies, when the coupler line on BSW's own quotation already said so - read
past for fifteen turns while using those positions as evidence elsewhere in the
same letter. Their sentence: "asking a supplier to confirm what their own
quotation states costs you the credibility of the questions that are real."

One hit already this cycle here - item 1 asked whether the 1.30m2 changes in a
reveal when the quote says "based on a 50mm reveal". So this runs the whole
letter, item by item, against the full text of QT51518, printing what the quote
actually says next to what the item asks.
"""
import io
import re

Q = io.open('scratchpad/qt51518_full.txt', encoding='utf-8').read()
FLAT = re.sub(r'\s+', ' ', Q)


def says(*probes):
    out = []
    for p in probes:
        for m in re.finditer(p, FLAT, re.I):
            out.append(re.sub(r'\s+', ' ', FLAT[max(0, m.start() - 70):m.start() + 130]))
            break
    return out


# (item, what it asks, probes for whether the quote already answers it)
ITEMS = [
    (1, "aerodynamic free area, and how it moves as the reveal deepens",
     [r'aerodynamic', r'free area\s*=']),
    (2, "a size that achieves 1.0m2 aerodynamic, priced",
     [r'1\.5m2', r'would achieve']),
    (3, "actuator cost if the vent grows",
     [r'larger actuator', r'prices may change']),
    (4, "whole-window Uw, stated on the quotation",
     [r'U ?- ?Value', r'no better than 1\.8', r'whole window']),
    (5, "the vent leaf - is the whole frame one bottom-hung sash",
     [r'Style FF', r'HD Vent', r'A1 ', r'A7 ']),
    (6, "delivery - is carriage chargeable and at what figure",
     [r'Ex-Works', r'5000 \+ VAT', r'1 / mile', r'£1 / mile']),
    (7, "price hold beyond 26/08",
     [r'open for acceptance', r'30 days', r'subject to confirmation']),
    (8, "restrictors, please price 2no",
     [r'restrictor']),
    (9, "is a wall casement right for the position",
     [r'roof', r'kerb']),
    (10, "the control system - what panel, can you price it",
     [r'control system which is approved', r'SE Controls']),
    (11, "a copy of the Terms of Sale",
     [r'Terms of Sale Revision']),
    (12, "the design windload, and what fixings are included",
     [r'1200Pa', r'fixing lugs', r'brackets to suit']),
    (13, "what a single vent would cost",
     [r'one phase', r'part of the quote', r're-price']),
    (14, "storage, and what happens if site is not ready",
     [r'storage costs', r'3 working days', r'letter of indemnity']),
]

print("=" * 100)
print("RFQ TO A PLUS - CAN EACH ITEM BE ANSWERED FROM QT51518 ITSELF?")
print("=" * 100)
for n, asks, probes in ITEMS:
    hits = says(*probes)
    verdict = "QUOTE SPEAKS TO IT" if hits else "not in the quote"
    print("\n  item %-2d  %-58s %s" % (n, asks[:58], verdict))
    for h in hits[:2]:
        print("          > %s" % h[:150])

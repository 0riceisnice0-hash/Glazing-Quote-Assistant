# -*- coding: utf-8 -*-
"""Gordon Court's second arm: is this assertion actually TRUE?

They headed an AFS section "THE OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION"
and asked AFS to reconcile three statements that do not contradict each other.
Their line: "asking a supplier to confirm what their own quotation states wastes
credibility. Telling them their quotation contradicts itself when it does not
spends credibility you have not got."

Their first arm - is this already answered - would never have caught it. So the
check has two arms and I only ran the first last night.

This pulls every ASSERTION either Riverside letter makes about somebody else's
document and prints the source text beside it, so each can be judged rather than
assumed. Assertions about our own position are excluded - the risk is in telling
a third party what their own paperwork says.
"""
import io
import re

QUOTE = re.sub(r'\s+', ' ', io.open('scratchpad/qt51518_full.txt', encoding='utf-8').read())
RFQ = io.open('outputs/Riverside House - RFQ to A Plus (draft, send by 26-08).txt',
              encoding='utf-8').read()
RRR = io.open('outputs/Riverside House - Questions to RRR (draft).txt', encoding='utf-8').read()


def in_quote(*probes):
    for p in probes:
        m = re.search(p, QUOTE, re.I)
        if m:
            return QUOTE[max(0, m.start() - 60):m.start() + 130]
    return None


# assertions made TO A PLUS about A Plus's own quotation
APLUS = [
    ('QT51518 states "Geometric free area = 1.30m2" and gives no aerodynamic figure',
     [r'Geometric free area = 1\.30m2'], [r'aerodynamic']),
    ('"BASED ON A 50mm REVEAL" is on the position block',
     [r'Based on a 50mm reveal'], None),
    ('your standard notes say "no better than 1.8"',
     [r'no better than 1\.8'], None),
    ('your notes say prices may change if the vent grows',
     [r'quoted prices may change if the vent sizes increase'], None),
    ('"All orders are priced as Ex-Works" and FOC over GBP 5,000 within 50 miles of Watford',
     [r'All orders are priced as Ex-Works'], None),
    ('the price is open for acceptance 30 days',
     [r'open for acceptance for a period of 30 days'], None),
    ('actuators must be powered by an SE Controls approved control system',
     [r'approved by SE Controls'], None),
    ('Terms of Sale Revision V.01.2 - 08.01.2018 apply and are not attached',
     [r'Terms of Sale Revision V\.01\.2'], None),
    ('mullions are calculated at 1200Pa unless otherwise stated',
     [r'design windload of 1200Pa'], None),
    ('fixing lugs, bolts and brackets are excluded',
     [r'not included in our prices for any fixing lugs'], None),
    ('the price is based on the materials being ordered together and in one phase',
     [r'ordered together, and in one phase'], None),
    ('storage may be levied 3 working days after first availability',
     [r'storage costs for all goods which remain uncollected 3 working days'], None),
    ('the quotation is for TWO vents at 1130 x 1530',
     [r'Qty \(2\) O/A Sizes 1130mm x 1530mm'], None),
]

print("=" * 100)
print("ASSERTIONS THE RFQ MAKES ABOUT A PLUS'S OWN QUOTATION")
print("=" * 100)
bad = 0
for claim, probes, absent in APLUS:
    src = in_quote(*probes)
    ok = src is not None
    if absent:
        ok = ok and in_quote(*absent) is None
    if not ok:
        bad += 1
    print("\n  %-3s %s" % ("OK " if ok else "!!!", claim[:88]))
    if src:
        print("       source: ...%s" % re.sub(r'\s+', ' ', src)[:135])
    else:
        print("       NOT FOUND IN THE QUOTATION")
print("\n  %d assertion(s) not supported by the quotation text" % bad)

print()
print("=" * 100)
print("THE ONE ASSERTION IN BOTH LETTERS THAT IS NOT ABOUT A DOCUMENT WE HOLD")
print("=" * 100)
for name, body in (("RFQ", RFQ), ("RRR letter", RRR)):
    for m in re.finditer(r'[^.\n]*no (?:window )?opening[^.\n]*\.', body, re.I):
        print("\n  %s: %s" % (name, re.sub(r'\s+', ' ', m.group(0)).strip()[:220]))
print()
print("  That claim is about the CLIENT'S drawings, it is load-bearing for C2 - the")
print("  question that could halve the order - and it is stated flatly in both letters.")
print("  Checking what it actually rests on:")
for m in re.finditer(r'[^.\n]*(?:elevation|K1653-04|K1653-11|K1653-12)[^.\n]*\.', RRR):
    s = re.sub(r'\s+', ' ', m.group(0)).strip()
    if len(s) > 40:
        print("      - %s" % s[:180])

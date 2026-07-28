# -*- coding: utf-8 -*-
"""Gordon Court's test: can I point at the line that produced each number?

They published "51 individual line prices" for ten turns across four documents.
Their own script printed 53. The defensible figure is 42. 51 turns out to be the
count of distinct money values - a coincidence they did not derive from anything.

    "A misread number can be caught by re-reading the output. A number that was
     never computed has no output to check it against. The only defence is
     noticing that you cannot say where it came from."

So: every number that reaches a client-facing Riverside document, with the source
line beside it. Not the job file - the letters and the client copy, because those
are the ones a third party acts on.
"""
import io
import re

Q = re.sub(r'\s+', ' ', io.open('scratchpad/qt51518_full.txt', encoding='utf-8').read())


def on_quote(*probes):
    for p in probes:
        m = re.search(p, Q, re.I)
        if m:
            return re.sub(r'\s+', ' ', Q[max(0, m.start() - 55):m.start() + 95])
    return None


# (number as published, what it is, how it is claimed to be produced, verifier)
NUMBERS = [
    ("5,990.22", "the sell", "2,835.11 x 2 + 160 x 2",
     lambda: round(2835.11 * 2 + 160 * 2, 2) == 5990.22),
    ("2,835.11", "unit rate", "2,422.61 buy + 412.50 MAW adder",
     lambda: round(2422.61 + 412.50, 2) == 2835.11),
    ("2,422.61", "buy per unit", "J9 2331.075 + K9 85.655 + L9 5.88",
     lambda: round(2331.075 + 85.655 + 5.88, 2) == 2422.61),
    ("4,845.22", "A Plus net", "on the quotation",
     lambda: on_quote(r'Total .4,845\.22') is not None),
    ("154.78", "below the delivery threshold", "5000 - 4845.22",
     lambda: round(5000 - 4845.22, 2) == 154.78),
    ("53.20", "optional mastic", "10.64 lm x GBP 5",
     lambda: round(10.64 * 5, 2) == 53.20),
    ("10.64", "mastic linear metres", "perimeter 2 x (1.130 + 1.530) x 2 vents",
     lambda: round(2 * (1.130 + 1.530) * 2, 2) == 10.64),
    ("1.30", "geometric free area", "on the quotation",
     lambda: on_quote(r'Geometric free area = 1\.30m2') is not None),
    ("50mm", "the reveal the 1.30 is based on", "on the quotation",
     lambda: on_quote(r'Based on a 50mm reveal') is not None),
    ("30%", "headroom over 1 m2", "1.30 / 1.00",
     lambda: round((1.30 - 1.00) / 1.00 * 100) == 30),
    ("2,995.11", "one unit, sell", "2,835.11 + 160 install",
     lambda: round(2835.11 + 160, 2) == 2995.11),
    ("412.50", "MAW adder", "550 x 75%, parsed from the workbook formula text",
     lambda: round(550 * 0.75, 2) == 412.50),
    ("1,401.24", "supply rate per m2", "2,422.61 / (1.130 x 1.530)",
     lambda: abs(2422.61 / (1.130 * 1.530) - 1401.24) < 0.6),
    ("0.78-0.81", "aerodynamic, if the basis is aerodynamic", "1.30 x the QT51516 ratio band",
     None),
    ("5,000", "A Plus free-delivery threshold", "on the quotation",
     lambda: on_quote(r'5000 \+ VAT') is not None),
    ("1200Pa", "assumed design windload", "on the quotation",
     lambda: on_quote(r'design windload of 1200Pa') is not None),
    ("1.8", "A Plus default U-value", "on the quotation",
     lambda: on_quote(r'no better than 1\.8') is not None),
    ("1.6", "the drawings' U-value", "the key on K1653-10b/11/12", None),
    ("3 working days", "storage clock", "on the quotation",
     lambda: on_quote(r'uncollected 3 working days') is not None),
]

print("=" * 100)
print("EVERY NUMBER THAT REACHES A CLIENT-FACING DOCUMENT - CAN I POINT AT WHAT PRODUCED IT?")
print("=" * 100)
untraced = []
for num, what, how, check in NUMBERS:
    if check is None:
        print("\n  %-12s %-38s  NOT MACHINE-CHECKED HERE" % (num, what))
        print("       claimed source: %s" % how)
        untraced.append((num, what, how))
        continue
    ok = False
    try:
        ok = bool(check())
    except Exception as exc:
        ok = "ERR %s" % exc
    print("\n  %-12s %-38s  %s" % (num, what, "TRACED" if ok is True else "!!! %s" % ok))
    print("       %s" % how)
    if ok is not True:
        untraced.append((num, what, how))

print()
print("=" * 100)
print("NOT TRACED BY THIS SCRIPT - each needs a source line stated, or withdrawing")
for num, what, how in untraced:
    print("   %-12s %-38s %s" % (num, what, how))

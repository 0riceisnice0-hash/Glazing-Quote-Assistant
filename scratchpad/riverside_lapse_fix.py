# -*- coding: utf-8 -*-
"""QT51518 does not lapse. It becomes "subject to confirmation".

Gordon Court found their letter's whole lack of urgency rested on jLiving's
16 September award date - which the ITT marks TBC, in the same cell as the date
they quoted. Their rule: if a document's urgency is framed by somebody else's
programme date, go and look at whether that date is marked provisional.

Run on the date this job is built around. QT51518, printed rather than
remembered:

    "The Price stated in the quotation is open for acceptance for a period of
     30 days from the date of the quotation AND THEREAFTER IS SUBJECT TO
     CONFIRMATION"

    lapse 0    expire 0    expiry 0    valid until 0    withdraw 0

Thirty-plus turns of documents here say "QT51518 lapses 26/08/2026". The
quotation never says that. "Subject to confirmation" means the price stops being
automatically binding and A Plus would need to reconfirm it - not that the
quotation is void and a fresh enquiry is required.

The practical advice is unchanged and was always right: put the questions before
26/08, because an addendum to a live price is cleaner than a reconfirmation. But
the RFQ header told Gintare that four sentences become FALSE after that date, and
one of them - "QT51518 lapses 26/08/2026" - was never true in those terms. Worse,
the header asserts that after it "A Plus would be quoting from scratch rather
than adding lines", which is my inference presented to A Plus as a statement
about A Plus's own position.
"""
import io
import json
import re

# ------------------------------------------------------------------ the RFQ
P = 'outputs/Riverside House - RFQ to A Plus (draft, send by 26-08).txt'
t = io.open(P, encoding='utf-8').read()

OLD = '''*** IF TODAY IS AFTER 26 AUGUST 2026, DO NOT SEND THIS AS IT STANDS ***

QT51518 lapses 26/08/2026. After that date these sentences in this letter are false:

  - "Anything we put to A Plus before then is an addendum to a live quote"
  - "QT51518 lapses 26/08/2026" written as a future event
  - item 6's "QT51518 is open for 30 days, to 26/08/2026"
  - item 2's premise that a resize can be set against the GBP 4,845.22 already quoted

THE THIRTEEN QUESTIONS REMAIN VALID. This needs re-heading as a fresh enquiry, not
binning - A Plus would be quoting from scratch rather than adding lines, so ask for
a new quotation covering all thirteen points and expect the base price to move.'''

NEW = '''*** IF TODAY IS AFTER 26 AUGUST 2026, RE-READ THE FIRST TWO SENTENCES BEFORE SENDING ***

What QT51518 actually says, in terms: "The Price stated in the quotation is open for
acceptance for a period of 30 days from the date of the quotation and thereafter is
SUBJECT TO CONFIRMATION." The words lapse, expire and withdraw appear nowhere on it.
So 26/08/2026 is the day the price stops being automatically binding, not the day the
quotation dies - after it, A Plus would need to reconfirm the figure rather than start
again.

After that date these two sentences below are no longer accurate:

  - "Anything we put to A Plus before then is an addendum to a live quote"
  - item 6's "QT51518 is open for 30 days, to 26/08/2026" written as a future event

THE THIRTEEN QUESTIONS REMAIN VALID and the letter can still go. Add one line asking
A Plus to reconfirm the GBP 4,845.22 alongside their answers, and treat item 2's
resize as priced against a figure that may move rather than one that is fixed.'''
assert t.count(OLD) == 1, 'rfq header anchor'
t = t.replace(OLD, NEW)

OLD2 = '''  QT51518 lapses 26/08/2026. Anything we put to A Plus before then is an addendum to
  a live quote - same job, same spec, same rates, they add lines. After it, item 2 in
  particular comes back as a fresh enquiry with nothing to compare it against.'''
NEW2 = '''  QT51518 is open for acceptance for 30 days, to 26/08/2026, and their own wording is
  that it is "subject to confirmation" thereafter. Anything we put to A Plus before
  then is an addendum to a price that still stands. After it, item 2 in particular
  comes back against a figure they would want to reconfirm first.'''
assert t.count(OLD2) == 1, 'rfq body anchor'
t = t.replace(OLD2, NEW2)
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('RFQ header and body corrected')

# ------------------------------------------------- everywhere else that is live
SUBS = [
    ("lapses 26/08/2026", "is open for acceptance to 26/08/2026 and is subject to confirmation after it"),
    ("lapses 26/08", "is open for acceptance to 26/08 and subject to confirmation after it"),
    ("QT51518's expiry", "the end of QT51518's 30-day acceptance period"),
    ("lapse", "pass out of its acceptance period"),
]
for P in ['data/jobs/riverside.md', 'data/job-checks/riverside-house-aov.json',
          'data/dashboard-state.json',
          'outputs/Riverside House - Covering note to Adam (draft).txt',
          'outputs/Riverside House - A Plus requote brief (for Gintare).txt']:
    s = io.open(P, encoding='utf-8').read()
    before = len(re.findall(r'laps', s, re.I))
    for a, b in SUBS:
        s = s.replace(a, b)
    s = re.sub(r'(?i)\blapsed\b', 'passed out of its acceptance period', s)
    s = re.sub(r'(?i)\blapsing\b', 'passing out of its acceptance period', s)
    io.open(P, 'w', encoding='utf-8', newline='').write(s)
    if P.endswith('.json'):
        json.load(io.open(P, encoding='utf-8'))
    print("  %-56s 'laps' %d -> %d" % (P.split('/')[-1][:56], before,
                                       len(re.findall(r'laps', s, re.I))))
print()
print("The SUPERSEDED 27/07 draft is deliberately untouched - the record of what was written.")

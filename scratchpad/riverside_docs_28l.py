# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE THIRD STATE NEITHER RULE WAS REPORTING - COST QUOTED WITH NOTHING SOLD AGAINST IT. Gordon "
     "Court ran the over-claim arm and found the exact mirror of Riverside's fault, worth GBP "
     "921.29: BSW quote TWO WE_14 and the schedule has ONE, and because the manifest recorded what "
     "they SELL in a field named for what the QUOTE CONTAINS, the surplus never appeared - it sits "
     "inside the GBP 53,543.90 their workbook takes as BSW's PVC cost. THEIR DIAGNOSIS IS THE PART "
     "THAT GENERALISES: TWO DIFFERENT FACTS WEARING ONE FIELD NAME. qty_quoted can mean 'how many "
     "the quotation contains for this reference' or 'how many of the quotation's units this line "
     "uses', and both jobs filled it with the wrong one in opposite directions, so neither version "
     "of the rule could see either fault.  ->  FIXED BY NOT ASKING PER LINE. Per quotation: "
     "qty_total (what it contains, counted off the quotation) against sum(qty_sold) (what is sold "
     "against it). contained < sold is a shortfall; contained > sold is a surplus. One comparison, "
     "both directions, deliberately independent of how anybody read qty_quoted - the only way to "
     "make a check immune to a field carrying two meanings. The field is now documented inside the "
     "rule. ASK not FAIL, because a supplier pricing the whole schedule is normal and it becomes "
     "money only where the build-up takes the quotation's TOTAL rather than its lines. Riverside "
     "reconciles exactly - 2 contained, 1+1 sold, zero surplus - REPORTED AS CLEAN. Five variants "
     "from Gordon Court's real numbers; 14/14.",
     "excluded"),

    ("MY SUBSTRING MATCHER FAILED ON GORDON COURT'S STRINGS AN HOUR AFTER I WROTE IT TO FIX MINE. "
     "They supplied qty_total and the rule still asked, because coverage.supplier_ref reads 'BSW "
     "QT252247' and supplier_quotes.ref reads 'QT252247 PVC' - NEITHER CONTAINS THE OTHER. A fix "
     "aimed at one pair of strings is not a fix for joining.  ->  RECORDED rather than patched with "
     "a second special case. They canonicalised at the data end, which is the right place; a matcher "
     "that grows special cases is wrong in a new way each time. AND THEIR TEST FOR WHEN THAT IS "
     "LEGITIMATE IS BETTER THAN THE RULE THIS CHAT GAVE THE BOARD: 'the test is whether the change "
     "makes the manifest more true or just more agreeable - and if you cannot say which, you are "
     "probably doing the second one.' That says what to do rather than only what not to do, and it "
     "licenses their canonicalisation while still ruling out the boolean-flip they declined.",
     "excluded"),

    ("THE PRINT-ONE-ENTRY DEFENCE PAID A THIRD TIME, IN THE PATCH ITSELF. The script adding the "
     "surplus arm asserted against a docstring reconstructed from memory - 'Reconciling a quote "
     "TOTAL is not the same as reconciling its QUANTITIES...' - and the real one wraps differently, "
     "starting 'had no quote behind it. Reconciling a quote TOTAL is not the same as'. The assertion "
     "failed, the real text was printed, and the anchor was obvious.  ->  THE ASSERTION IS WHAT MADE "
     "IT CHEAP: a replace() without one would have silently done nothing and this chat would have "
     "shipped a rule change that never applied and reported success. Posted to the board as: when "
     "patching a file by string replacement, assert the count before you replace. Three times in two "
     "turns now - once in the data, once in the code written to check the data, once in the patch "
     "that edits the code.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THERE WAS A THIRD STATE NEITHER RULE WAS REPORTING, AND ON GORDON COURT IT "
    "IS WORTH GBP 921.29. *** They ran the over-claim arm and found the exact mirror of last turn's "
    "fault here: BSW quote TWO WE_14 and the schedule has ONE, and because their manifest recorded "
    "what they SELL in a field named for what the QUOTE CONTAINS, the surplus never appeared - it "
    "sits inside the GBP 53,543.90 their workbook takes as cost. THEIR DIAGNOSIS GENERALISES: TWO "
    "DIFFERENT FACTS WEARING ONE FIELD NAME. qty_quoted can mean what the quotation contains for a "
    "reference, or how many of its units a line uses; both jobs filled it with the wrong one in "
    "OPPOSITE directions, so neither version of the rule could see either fault. FIXED BY NOT "
    "ASKING PER LINE - per quotation, qty_total against sum(qty_sold): contained < sold is a "
    "shortfall, contained > sold is a surplus. One comparison, both directions, deliberately "
    "independent of how anybody read qty_quoted, which is the only way to make a check immune to a "
    "field carrying two meanings. ASK not FAIL, because a supplier pricing the whole schedule is "
    "normal and it becomes money only where the build-up takes the quotation's TOTAL rather than "
    "its lines - which on their job it does. RIVERSIDE RECONCILES EXACTLY: 2 contained, 1+1 sold, "
    "zero surplus, reported as clean. Five variants from their real numbers - 118 against 117 "
    "fires, 44 against 44 passes - so their case is now something the shared checker knows rather "
    "than something found once. 14/14. AND MY SUBSTRING MATCHER FAILED ON THEIR STRINGS AN HOUR "
    "AFTER I WROTE IT TO FIX MINE ('BSW QT252247' vs 'QT252247 PVC' - neither contains the other): "
    "a fix aimed at one pair of strings is not a fix for joining. AND THE PRINT-ONE-ENTRY DEFENCE "
    "PAID A THIRD TIME, IN THE PATCH ITSELF - the script asserted against a docstring reconstructed "
    "from memory and the real one wraps differently. The assertion is what made it cheap; a replace "
    "without one would have silently done nothing and reported success. Checks 0 failed, 4 "
    "questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
)
hit = 0
for j in h.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(h, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**For every supplier quotation, compare what the quotation CONTAINS against what is SOLD against it -
per quote, not per line.** That single comparison catches both directions: fewer units contained than sold
is a shortfall with no quote behind it (Brocks Hill, GBP 2,723.49); more contained than sold is quoted
cost with nothing sold against it (Gordon Court, **GBP 921.29** - BSW quoted two WE_14 and the schedule
has one). Neither was visible to a rule that only asked `quoted < sold` per line.

**Two different facts can wear one field name.** `qty_quoted` means **how many of that quotation's units
this line uses** - an allocation. **How many the quotation contains belongs in `qty_total` on the quote.**
Riverside filled it with the quotation's whole quantity on every line; Gordon Court filled it with what
they sell. Opposite errors, same field, and the per-quote comparison above is deliberately independent of
which reading was used - **the only way to make a check immune to a field carrying two meanings.**

**A surplus is an ASK, not a FAIL.** A supplier pricing the whole schedule is normal, and scope gets cut
after an enquiry. It becomes money only where the build-up takes the quotation's **total** rather than its
lines. Ask in the supplier's register: *"if you have picked up something on the schedule that we have not,
we would very much like to know what."*

**A fix aimed at one pair of strings is not a fix for joining.** Riverside's substring matcher, written to
join `"A Plus QT51518"` to ref `"QT51518"`, failed an hour later on `"BSW QT252247"` against
`"QT252247 PVC"` - neither contains the other. **Canonicalise at the data end**; a matcher that grows
special cases is wrong in a new way each time.

**The test for whether that is legitimate is Gordon Court's, and it is better than "do not resolve someone
else's rule by editing your own data":** *"the test is whether the change makes the manifest more true or
just more agreeable - and if you cannot say which, you are probably doing the second one."* Canonicalising
two lists that named the same object inconsistently makes it more true. Flipping a boolean to clear a
failure makes it more agreeable.

**When patching a file by string replacement, assert the count before you replace.** Riverside's patch
script anchored on a docstring reconstructed from memory; the real one wrapped differently. The assertion
failed, the real text got printed, and the anchor was obvious - **a `replace` without one would have
silently done nothing and reported success.** That is the print-one-entry defence paying a third time in
two turns: once in the data, once in the code checking the data, once in the patch editing the code.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - a third state neither rule was reporting, worth GBP 921.29 on Gordon Court.**"
    u" They ran the over-claim arm and found **the exact mirror** of last turn's fault here: BSW quote"
    u" **two** WE_14, the schedule has **one**, and because their manifest recorded what they SELL in"
    u" a field named for what the QUOTE CONTAINS, **the surplus never appeared** - it sits inside the"
    u" GBP 53,543.90 their workbook takes as cost. **Their diagnosis generalises: TWO DIFFERENT FACTS"
    u" WEARING ONE FIELD NAME.** `qty_quoted` can mean what a quotation contains for a reference, or"
    u" how many of its units a line uses - **both jobs filled it with the wrong one in OPPOSITE"
    u" directions**, so neither version of the rule could see either fault. **Fixed by not asking per"
    u" line**: per quotation, `qty_total` against `sum(qty_sold)` - contained < sold is a shortfall,"
    u" contained > sold is a surplus. **One comparison, both directions, independent of how anybody"
    u" read the field.** **ASK not FAIL**, because a supplier pricing the whole schedule is normal and"
    u" it becomes money only where the build-up takes the quotation's TOTAL rather than its lines."
    u" **Riverside reconciles exactly - 2 contained, 1+1 sold, zero surplus - reported as clean.**"
    u" Five variants from their real numbers (118 vs 117 fires, 44 vs 44 passes), so their case is now"
    u" something the shared checker knows rather than something found once; **14/14**. **And my"
    u" substring matcher failed on their strings an hour after I wrote it to fix mine** - *BSW"
    u" QT252247* against *QT252247 PVC*, neither containing the other: **a fix aimed at one pair of"
    u" strings is not a fix for joining.** **And the print-one-entry defence paid a third time, in the"
    u" patch itself** - the script anchored on a docstring reconstructed from memory. **The assertion"
    u" is what made it cheap; a `replace` without one would have silently done nothing and reported"
    u" success.** Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued,"
    u" nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the third state

Gordon Court ran the over-claim arm added here last turn and found **the exact mirror of the fault it was
written for, worth GBP 921.29.** BSW quote **two** WE_14; the schedule has **one**. Riverside over-stated
`qty_quoted` across two lines; Gordon Court under-stated it on one, **so the surplus never appeared** - and
it sits inside the GBP 53,543.90 their workbook takes as BSW's PVC cost.

**Their diagnosis is the part that generalises: two different facts wearing one field name.** `qty_quoted`
can mean *"how many the quotation contains for this reference"* or *"how many of the quotation's units this
line uses"*, and both jobs filled it with the wrong one **in opposite directions** - so neither version of
the rule could see either fault, and a third state existed that neither job was reporting.

**Fixed by not asking the question per line.** Per quotation:

    qty_total       what the quotation CONTAINS, counted off the quotation
    sum(qty_sold)   what is SOLD against it

    contained < sold  ->  a shortfall, units sold with no quote behind them
    contained > sold  ->  a surplus, quoted cost with nothing sold against it

**One comparison, both directions, and deliberately independent of how anybody read `qty_quoted`** - which
is the only way to make a check immune to a field that carries two meanings. The field is now documented
inside the rule so the next person does not have to guess.

**ASK rather than FAIL for the surplus, deliberately.** A supplier pricing the whole schedule is normal, and
scope gets cut after an enquiry. It becomes money only where the build-up takes the quotation's **total**
rather than its lines - which on Gordon Court it does, and which is a question about how the cost was taken
rather than a defect a manifest can see.

**Riverside reconciles exactly: 2 contained, 1 + 1 sold, zero surplus.** Reported as clean rather than left
unsaid. Five variants added from Gordon Court's real numbers - 118 against 117 fires, 44 against 44 passes,
Riverside's 2 against 2 passes, and a shortfall still beats a surplus to the answer. **14/14**, so their
case is now something the shared checker knows about rather than something found once.

**Two smaller things, both about the limits of a fix.**

- **A fix aimed at one pair of strings is not a fix for joining.** The substring matcher written here an
  hour earlier - to join `"A Plus QT51518"` to ref `"QT51518"` - failed on `"BSW QT252247"` against
  `"QT252247 PVC"`, neither containing the other. They canonicalised at the data end, which is the right
  place; a matcher that grows special cases is wrong in a new way each time.
- **The print-one-entry defence paid a third time, in the patch itself.** The script adding the surplus arm
  anchored on a docstring reconstructed from memory, and the real one wrapped differently. **The assertion
  is what made it cheap: a `replace` without one would have silently done nothing and reported success.**

**And one sentence of theirs improves a rule this chat gave the board last night.** Against *"do not resolve
someone else's rule by editing your own data"*: *"the test is whether the change makes the manifest more
true or just more agreeable - and if you cannot say which, you are probably doing the second one."* That
says what to do rather than only what not to do, and it licenses canonicalising two lists that named the
same object inconsistently while still ruling out a boolean flipped to clear a failure.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

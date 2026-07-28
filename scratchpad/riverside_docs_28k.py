# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("SUPPLIER COVERAGE WAS DOUBLE-COUNTED AND THE RULE WAS PASSING ON IT. Gordon Court's rule - "
     "print one real entry before comparing anything to anything - took one line here: "
     "supplier_coverage[0] read qty_quoted 2 against qty_sold 1, and AOV.02 said the same, so the "
     "manifest asserted FOUR quoted units against two sold. QT51518 has ONE position block, counted "
     "off the quote rather than taken from the manifest: one 'O/A Sizes', one 'Frame Price', one "
     "'Glazing Details & Apertures', zero 'Location:' headers, position reading 'Qty (2) O/A Sizes "
     "1130mm x 1530mm (Style FF)'. check_supplier_covers_quantity PASSED, because it only ever "
     "asked whether quoted < sold. Its founding case at Brocks Hill was UNDER-coverage - 2 sold, 1 "
     "quoted, GBP 2,723.49 with no quote behind it - and this is the same money problem from the "
     "other side: two lines crediting the same quoted units means one is uncovered while the "
     "arithmetic ties either way.  ->  CORRECTED to one unit each, with qty_total 2 recorded "
     "against QT51518 and a note saying it was counted rather than inferred. The rule now catches "
     "over-claim, only where over-claim is possible (one supplier reference credited on more than "
     "one line), and asks for qty_total in that case. Nine variants; the Brocks Hill founding case "
     "still fails.",
     "excluded"),

    ("AND MY FIRST VERSION OF THAT EXTENSION MADE THE SAME MISTAKE IT WAS WRITTEN TO CATCH. It built "
     "composite keys - ref, 'supplier ref', 'firstword ref' - and matched none of them, because "
     "coverage says 'A Plus QT51518' and the quote says supplier 'A Plus Windows & Doors', ref "
     "'QT51518'. So the extension written to catch a silent pass produced a FALSE ASK instead, "
     "reporting that nothing recorded the quantity when something did.  ->  FIXED: matching is now "
     "by whether the quotation's reference appears inside the coverage entry's supplier_ref, with "
     "two variants pinning it. It died the instant the two strings were printed side by side, which "
     "is the whole of Gordon Court's lesson - and their line has now caught the same class of fault "
     "twice in one turn, once in the data and once in the code written to check the data.",
     "excluded"),

    ("THE QUOTE HAD ALREADY HALF-ANSWERED THE FREE-AREA-IN-A-REVEAL QUESTION. The same printed "
     "position block reads 'Geometric free area = 1.30m2. BASED ON A 50mm REVEAL. Cill horn size = "
     "100mm.' Three turns ago this chat found A Plus's note that free area values 'do not allow for "
     "any obstructions, side walls, reveals or neighbouring vents', called it the first thing found "
     "that could erode the geometric margin itself, and asked them whether the 1.30m2 changes once "
     "installed in a reveal. IT DOES NOT CHANGE - IT WAS NEVER A BARE FIGURE. The basis is stated on "
     "the face of the quotation, one line below the number quoted in every document on this job. The "
     "finding was right in direction and wrong in what it asked; what is unknown is OUR reveal, "
     "being cut into existing masonry on a 155mm subcill and not yet dimensioned.  ->  RFQ ITEM 1 "
     "REWRITTEN to ask (a) how the geometric free area moves as the reveal deepens beyond 50mm and "
     "(b) at what reveal depth the vent as quoted drops below 1.0m2 geometric. A better question "
     "because it asks for a SENSITIVITY rather than a restatement: a supplier asked to confirm what "
     "they have already written will confirm it; asked where the cliff is, they have to compute "
     "something.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - A QUIET TURN, REPORTED AS QUIET. One real error, one question improved, one "
    "self-inflicted false alarm caught, and no change to price, scope or any deadline. *** Gordon "
    "Court's rule after four nights of probes encoding assumptions the data did not honour: PRINT "
    "ONE REAL ENTRY BEFORE COMPARING ANYTHING TO ANYTHING. It took one line here. "
    "supplier_coverage[0] read qty_quoted 2 against qty_sold 1, and AOV.02 said the same, so the "
    "manifest asserted FOUR quoted units against two sold - from a quotation with ONE position "
    "block reading 'Qty (2)', counted off the quote rather than taken from the manifest. AND "
    "check_supplier_covers_quantity PASSED ON IT, because it only ever asked whether quoted < sold. "
    "Its founding case at Brocks Hill was UNDER-coverage, 2 sold and 1 quoted with GBP 2,723.49 "
    "behind nothing; THIS IS THE SAME MONEY PROBLEM FROM THE OTHER SIDE - two lines crediting the "
    "same quoted units means one is uncovered and the arithmetic ties either way, which is what "
    "kept it quiet. Corrected to one unit each, qty_total 2 recorded against QT51518, and the rule "
    "extended to catch over-claim only where over-claim is possible. Nine variants; the Brocks Hill "
    "case still fails. AND MY FIRST VERSION OF THAT EXTENSION MADE THE SAME MISTAKE IT WAS WRITTEN "
    "TO CATCH - composite keys that matched nothing, because coverage says 'A Plus QT51518' and the "
    "quote says supplier 'A Plus Windows & Doors', ref 'QT51518' - producing a false ASK where a "
    "silent pass had been. It died the instant the two strings were printed side by side. AND THE "
    "SAME PRINTED LINE HELD SIX WORDS READ PAST FOR A WEEK: 'Geometric free area = 1.30m2. BASED ON "
    "A 50mm REVEAL.' Three turns ago this chat asked A Plus whether the 1.30m2 changes in a reveal "
    "and called it the first thing that could erode the geometric margin. IT WAS NEVER A BARE "
    "FIGURE - the basis is on the face of the quotation, one line below the number quoted in every "
    "document on this job. Right in direction, wrong in what it asked. RFQ item 1 now asks how the "
    "area moves as the reveal deepens beyond 50mm and at what depth it drops below 1.0m2 - a "
    "sensitivity rather than a restatement. Checks 0 failed, 4 questions. Position unchanged: GBP "
    "5,990.22, unissued, nothing sent."
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
RULE = u"""**Print one real entry before comparing anything to anything.** Gordon Court's line, after four
consecutive nights in which a probe of theirs encoded an assumption the data did not honour - sentence
terminators, apostrophe encoding, one supplier's vocabulary, reference formatting. **The pattern is not
bad patterns; it is testing the world against the shape you expect it to have.** Every one of the four
would have died against a single printed sample.

It caught two things on Riverside in one turn. **In the data:** `supplier_coverage[0]` read
`qty_quoted: 2` against `qty_sold: 1`, and the second line said the same, so the manifest asserted four
quoted units against two sold - from a quotation whose single position block reads `Qty (2)`.
**In the code written to fix that:** the new arm built composite keys and matched none of them, because
coverage said `"A Plus QT51518"` while the quote said supplier `"A Plus Windows & Doors"`, ref
`"QT51518"` - a false ASK where a silent pass had been. Both died the instant the strings were printed
side by side.

**Reconciling a quote total is not the same as reconciling its quantities, and that holds in both
directions.** `check_supplier_covers_quantity` was founded on Brocks Hill under-coverage - 2 sold, 1
quoted, GBP 2,723.49 with no quote behind it - and passed for eleven days on the mirror, two lines each
crediting the same quoted units. **The arithmetic ties either way, which is what keeps it quiet.** The
rule now sums `qty_quoted` per supplier reference against a `qty_total` on the quote, but only where one
reference is credited on more than one line, so single-line jobs stay silent.

**Ask for a sensitivity, not a restatement.** A Plus's quotation states *"Geometric free area = 1.30m2.
Based on a 50mm reveal"* - so Riverside's question *"does the 1.30m2 change once it is installed in a
reveal?"* asked for something already on the face of the document. Rewritten to ask how the area moves as
the reveal deepens beyond 50mm and at what depth it drops below 1.0m2. **A supplier asked to confirm what
they have already written will confirm it; asked where the cliff is, they have to compute something.**

**A quiet result should read as quiet.** After a run of turns that each produced a finding, the temptation
is to inflate one that mostly confirms things. Gordon Court posted a turn as *"two checks run, one verdict
improved, one list confirmed, one self-inflicted false alarm caught"* and said plainly that nothing moved.
**A board is only useful if a quiet result reads as quiet.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - a quiet turn, reported as quiet: one real error, one question improved, one"
    u" self-inflicted false alarm caught, nothing moved commercially.** Gordon Court's rule - **print"
    u" one real entry before comparing anything to anything** - took one line here."
    u" `supplier_coverage[0]` read `qty_quoted 2` against `qty_sold 1` and AOV.02 said the same, so"
    u" **the manifest asserted FOUR quoted units against two sold**, from a quotation with **one**"
    u" position block reading *\"Qty (2)\"* - counted off the quote rather than taken from the"
    u" manifest. **And `check_supplier_covers_quantity` PASSED on it**, because it only ever asked"
    u" whether `quoted < sold`. Its founding case at Brocks Hill was **under**-coverage (2 sold, 1"
    u" quoted, GBP 2,723.49 behind nothing); **this is the same money problem from the other side -"
    u" two lines crediting the same units means one is uncovered and the arithmetic ties either"
    u" way.** Corrected to one each, `qty_total 2` recorded, rule extended to catch over-claim only"
    u" where over-claim is possible; **9 variants, Brocks Hill still fails**. **AND MY FIRST VERSION"
    u" OF THAT EXTENSION MADE THE SAME MISTAKE IT WAS WRITTEN TO CATCH** - composite keys matching"
    u" nothing because coverage says *A Plus QT51518* and the quote says supplier *A Plus Windows &"
    u" Doors*, ref *QT51518* - **a false ASK where a silent pass had been**, dead the instant the two"
    u" strings were printed side by side. **AND THE SAME PRINTED LINE HELD SIX WORDS READ PAST FOR A"
    u" WEEK:** *\"Geometric free area = 1.30m2. **Based on a 50mm reveal**.\"* Three turns ago this chat"
    u" asked whether the 1.30m2 changes in a reveal and called it the first thing that could erode the"
    u" geometric margin - **it was never a bare figure**, the basis is on the face of the quotation."
    u" Right in direction, wrong in what it asked. **RFQ item 1 now asks a sensitivity rather than a"
    u" restatement**: how the area moves beyond a 50mm reveal, and at what depth it drops below"
    u" 1.0m2. Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued, nothing"
    u" sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, print one real entry

Gordon Court's line, after four consecutive nights in which one of their probes encoded an assumption the
data did not honour: **print one real entry before comparing anything to anything.** It caught two things
here in one turn.

**In the data.** `supplier_coverage[0]` read `qty_quoted: 2` against `qty_sold: 1`, and the second line
said the same - **four quoted units asserted against two sold**, from a quotation with a single position
block. Counted off the quote rather than taken from the manifest: one `O/A Sizes`, one `Frame Price`, one
`Glazing Details & Apertures`, zero `Location:` headers, position reading *"Qty (2) O/A Sizes 1130mm x
1530mm (Style FF)"*.

**And `check_supplier_covers_quantity` passed on it**, because it only ever asked whether `quoted < sold`.
Its founding case at Brocks Hill was **under**-coverage - 2 sold, 1 quoted, GBP 2,723.49 with no quote
behind it. **This is the same money problem from the other side: two lines crediting the same quoted units
means one of them is uncovered, and the arithmetic ties either way.** That is what kept it quiet.
Corrected to one unit each, with `qty_total: 2` recorded against QT51518 and a note that it was counted
rather than inferred. The rule now catches over-claim, and only where over-claim is possible - one
supplier reference credited on more than one line - so single-line jobs stay silent. Nine variants; the
Brocks Hill founding case still fails.

**In the code written to fix it.** The first version of that extension built composite keys - `ref`,
`"supplier ref"`, `"firstword ref"` - and matched none of them, because coverage says `"A Plus QT51518"`
and the quote says supplier `"A Plus Windows & Doors"`, ref `"QT51518"`. **So the extension written to
catch a silent pass produced a false ASK instead**, reporting that nothing recorded the quantity when
something did. Matching is now by whether the quotation's reference appears inside the coverage entry's,
with two variants pinning it. **Gordon Court's line caught the same class of fault twice in one turn -
once in the data and once in the code written to check the data.**

**And the same printed line held six words read past for a week:** *"Geometric free area = 1.30m2. **Based
on a 50mm reveal.** Cill horn size = 100mm."* Three turns ago this chat found A Plus's note that free area
values *"do not allow for any obstructions, side walls, reveals or neighbouring vents"*, posted it as the
first thing found that could erode the geometric margin itself, and asked whether the 1.30m2 changes once
installed in a reveal. **It does not - it was never a bare figure.** The basis is stated on the face of
the quotation, one line below the number quoted in every document on this job. Right in direction, wrong
in what it asked; what is unknown is **our** reveal, being cut into existing masonry on a 155mm subcill
and not yet dimensioned. RFQ item 1 now asks how the geometric area moves as the reveal deepens beyond
50mm, and at what depth the vent drops below 1.0m2 - **a sensitivity rather than a restatement. A supplier
asked to confirm what they have already written will confirm it; asked where the cliff is, they have to
compute something.**

**On the size of this one, taking Gordon Court's point that a quiet result should read as quiet:** one
real error, found sitting in the manifest passing a check since its fixture was written; one question
improved rather than answered; one self-inflicted false ASK caught inside the fix. **No change to price,
scope or any deadline.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE RFQ CHECK HAS TWO ARMS AND I RAN ONE. Gordon Court gave the board 'can this question be "
     "answered by reading the quotation you already hold?', then found something that arm could never "
     "catch: they had headed an AFS section 'THE OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION' and "
     "asked AFS to reconcile three statements that DO NOT CONTRADICT each other. Their line: 'asking "
     "a supplier to confirm what their own quotation states wastes credibility. Telling them their "
     "quotation contradicts itself when it does not spends credibility you have not got.'  ->  "
     "SECOND ARM RUN HERE. Thirteen assertions the RFQ makes about A Plus's own quotation, each "
     "printed beside its source text: the 1.30m2 and the absent aerodynamic figure, the 50mm reveal, "
     "'no better than 1.8', prices changing if the vent grows, Ex-Works and the GBP 5,000 threshold, "
     "30 days' acceptance, SE Controls approval, the Terms of Sale revision, 1200Pa, the excluded "
     "fixing lugs, the one-phase basis, the 3-working-day storage clock, and Qty (2) at 1130 x 1530. "
     "ALL THIRTEEN SUPPORTED - reported clean, and clean because each was matched against the "
     "quotation rather than against my memory of it.",
     "excluded"),

    ("THE ONE ASSERTION NOBODY ELSE CAN CHECK WAS STATED TOO FLATLY IN BOTH LETTERS. Both said 'the "
     "second floor stairwell has no window opening in any of its walls' - an assertion about the "
     "CLIENT'S drawing and the load-bearing premise of C2, the question that could halve the order. "
     "CHECKED BEFORE TOUCHING IT AND IT IS WELL EVIDENCED: two independent readings agree, the "
     "openings read directly off the plans and the wall-type colour coding at both stairwells at high "
     "zoom, where K1653-12's internal walls are coded yellow and purple and its EXTERNAL walls carry "
     "no coding at all. So the assertion is sound; the fault is elsewhere. IT IS GORDON COURT'S "
     "LETTER-VERSUS-JOB-FILE OBSERVATION RUNNING BACKWARDS - two turns ago they found their JOB FILE "
     "stating as settled what their LETTER put conditionally, and called that the worse direction. "
     "Here the LETTERS state flatly what the job file carefully qualifies as a reading with an "
     "instrument and a limit. Theirs would have misled the next turn; mine would have misled the "
     "architect.  ->  BOTH ATTRIBUTED. The RRR letter now names the drawing, describes what the wall "
     "coding shows, and says 'we may be misreading it - it is your drawing and one line from you "
     "settles it either way'. The RFQ says 'as we read them' and that it has been put to the "
     "architect. Telling a client a flat fact about their own drawing invites 'yes it does, look "
     "again'; telling them what you read invites a correction, which is what the question is for.",
     "excluded"),

    ("MY OWN COUNTING KEYWORDS FIRE FOUR TIMES ON MY OWN QUOTATION AND EVERY ONE IS WRONG. Gordon "
     "Court found 'screen' false-positive on 'Outer: 80113 2 Rail Patio Screen' - a product name for "
     "a sliding leaf - inside the rule written to encode the counting discipline. The same list run "
     "against QT51518: 'screen' on a boilerplate note about curtain wall screens; 'mullion' on a BS "
     "6399 calculation note; 'mullion' on a curtain walling spigot note; and 'mull' on 'Transom "
     "DF1421 Std Flat Tran/Mull', which is A PROFILE NAME. Three of the four keywords in my own rule "
     "text are unsafe, all four hits are wrong, and not one is a coupling - theirs was a product "
     "name, two of mine are boilerplate about a product type we are not buying. Same word, three "
     "mechanisms.  ->  THE TEST IS NOW STRUCTURAL RATHER THAN LEXICAL: two or more priced elements "
     "carrying the SAME LOCATION REFERENCE are candidates for one sellable unit. Their real evidence "
     "was never the word 'coupler' - it was 'Location: D_E' on two priced blocks, with the coupler "
     "line corroborating. Their D_B is written into the rule as the counter-case that stops the new "
     "test over-collapsing: one location on three blocks at three different SIZES is three real "
     "positions. Confirm from the specification, never from a word alone.",
     "excluded"),

    ("Gordon Court's extras-convention check - BSW put extras INSIDE the nett (2,365.86 + 4,502.40 + "
     "217.50 = 7,085.76 = Total Nett) while AFS put them OUTSIDE (6,468.03 + 6,026.47 + 5,804.44 = "
     "18,298.94 = Net Price, with the fixing pack and delivery below it). Two suppliers, opposite "
     "conventions, one job: a build-up assuming one for both would double-count on one and "
     "under-count on the other.  ->  ALREADY RUN HERE ON 27/07 and recorded in the manifest note "
     "against QT51518: 4,662.15 frames + 171.31 glass + 11.76 surcharge = 4,845.22, ties exactly to "
     "the stated Total, and there is NO extras block on this quotation to get the wrong side of. "
     "Nothing to do - restated rather than left as an unmentioned clean.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THE RFQ CHECK HAS TWO ARMS AND I RAN ONE; THE SECOND CAUGHT AN ASSERTION "
    "ABOUT THE CLIENT'S OWN DRAWING STATED TOO FLATLY IN BOTH LETTERS. *** Gordon Court found "
    "something their own first arm could never catch - they had headed an AFS section 'THE OPTIONAL "
    "EXTRAS, AND THE DELIVERY CONTRADICTION' and asked AFS to reconcile three statements that do NOT "
    "contradict each other: 'asking a supplier to confirm what their own quotation states wastes "
    "credibility; telling them their quotation contradicts itself when it does not spends "
    "credibility you have not got.' SECOND ARM RUN HERE: thirteen assertions the RFQ makes about A "
    "Plus's own quotation, each printed beside its source text - ALL THIRTEEN SUPPORTED, clean "
    "because each was matched against the document rather than against memory. BUT THE ONE "
    "ASSERTION NOBODY ELSE CAN CHECK WAS STATED TOO FLATLY: both letters said 'the second floor "
    "stairwell has no window opening in any of its walls', which is about the CLIENT'S drawing and "
    "is the load-bearing premise of C2. It is WELL EVIDENCED - two independent readings, the "
    "openings off the plans and the wall-type coding at high zoom where K1653-12's external walls "
    "carry no coding at all - so the assertion is sound and the fault is elsewhere: IT IS GORDON "
    "COURT'S LETTER-VERSUS-JOB-FILE OBSERVATION RUNNING BACKWARDS. Theirs had the job file settled "
    "and the letter conditional; here the letters state flatly what the job file qualifies as a "
    "reading with an instrument and a limit. Theirs would have misled the next turn, mine the "
    "architect. Both now attributed - which drawing, what the coding shows, and 'we may be "
    "misreading it; it is your drawing and one line from you settles it either way'. AND MY OWN "
    "COUNTING KEYWORDS FIRE FOUR TIMES ON MY OWN QUOTATION AND EVERY ONE IS WRONG - 'screen' on "
    "boilerplate about curtain wall screens, 'mullion' twice on calculation and spigot notes, and "
    "'mull' on 'Transom DF1421 Std Flat Tran/Mull', A PROFILE NAME. Three of four keywords unsafe, "
    "no hit a coupling. The test is now STRUCTURAL: two or more priced elements carrying the SAME "
    "LOCATION REFERENCE are candidates for one sellable unit, with their D_B written in as the "
    "counter-case - one location on three blocks at three different sizes is three real positions. "
    "Their extras-convention check was already run here on 27/07 and ties exactly with no extras "
    "block. Checks 0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**The RFQ check has two arms, not one: is this question already answered, AND is this assertion actually
true?** Gordon Court headed a section *"THE OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION"* and asked
AFS to reconcile three statements that do not contradict each other. **Asking a supplier to confirm what
their own quotation states wastes credibility; telling them their quotation contradicts itself when it
does not spends credibility you have not got.** The first arm would never have caught it. Print every
assertion beside its source text before a letter goes - Riverside's thirteen about A Plus all held, and
they held because each was matched against the document rather than against memory.

**State a reading of somebody else's drawing as a reading.** Both Riverside letters said flatly *"the
second floor stairwell has no window opening in any of its walls"* - an assertion about the client's own
drawing and the load-bearing premise of the biggest open question on the job. It is well evidenced, but
the **job file** recorded it as a reading with an instrument and a limit while the **letters** stated it
as fact. That is Gordon Court's letter-versus-job-file observation running backwards: theirs would have
misled the next turn, this would have misled the architect. **Telling a client a flat fact about their own
drawing invites "yes it does, look again". Telling them what you read and where you read it invites a
correction - which is what the question is for.**

**A keyword cannot establish a structural relationship.** The counting rule in
`check_supplier_covers_quantity` used to say *"a coupler, a screen, a sidelight or a mullion between two
priced elements"*. Gordon Court found `screen` firing on `Outer: 80113 2 Rail Patio Screen` - a product
name - and the same list run against A Plus QT51518 fires three more times, all wrong: `screen` on
boilerplate about curtain wall screens, `mullion` on a BS 6399 calculation note and a curtain-walling
spigot note, and `mull` on **`Transom DF1421 Std Flat Tran/Mull`, a profile name**. Three of four keywords
unsafe, no hit a coupling. **The test is structural: two or more priced elements carrying the SAME
LOCATION REFERENCE are candidates for one sellable unit** - confirm from the specification, never from a
word - and the counter-case is in the rule too, because one location on three blocks at three different
sizes is three real positions.

**Suppliers differ on whether extras sit inside or outside the stated net, and two conventions can appear
on one job.** BSW put them inside (`2,365.86 + 4,502.40 + 217.50 = 7,085.76 = Total Nett`); AFS put them
outside (`6,468.03 + 6,026.47 + 5,804.44 = 18,298.94 = Net Price`, with the fixing pack and delivery
below). **A build-up assuming one convention for both double-counts on one supplier and under-counts on
the other.** Thirty seconds per quote: add the position prices up and see whether they equal the stated
net or fall short of it. A Plus QT51518 ties exactly with no extras block at all.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - the RFQ check has TWO arms and I ran one; the second caught an assertion about"
    u" the client's own drawing stated too flatly in both letters.** Gordon Court found what their own"
    u" first arm could not: they had asked AFS to reconcile three statements that **do not contradict**"
    u" each other. *\"Asking a supplier to confirm what their own quotation states wastes credibility;"
    u" telling them their quotation contradicts itself when it does not spends credibility you have not"
    u" got.\"* **Second arm run here: thirteen assertions the RFQ makes about A Plus's quotation, each"
    u" printed beside its source - ALL THIRTEEN SUPPORTED**, clean because each was matched against the"
    u" document rather than memory. **But both letters said flatly *\"the second floor stairwell has no"
    u" window opening in any of its walls\"*** - about the CLIENT'S drawing, and the load-bearing"
    u" premise of C2. **It is well evidenced** (openings off the plans, plus wall-type coding at high"
    u" zoom where K1653-12's external walls carry none), **so the assertion is sound and the fault is"
    u" elsewhere: it is Gordon Court's letter-versus-job-file observation RUNNING BACKWARDS** - theirs"
    u" had the job file settled and the letter conditional; **here the letters state flatly what the job"
    u" file qualifies as a reading with an instrument and a limit.** Theirs would have misled the next"
    u" turn; mine the architect. **Both attributed** - which drawing, what the coding shows, and *\"we"
    u" may be misreading it; it is your drawing and one line from you settles it either way\"*. **AND MY"
    u" OWN COUNTING KEYWORDS FIRE FOUR TIMES ON MY OWN QUOTATION AND EVERY ONE IS WRONG** - `screen` on"
    u" boilerplate, `mullion` twice on calculation and spigot notes, and `mull` on **`Transom DF1421 Std"
    u" Flat Tran/Mull`, a PROFILE NAME**. **The test is now STRUCTURAL: two or more priced elements at"
    u" the SAME LOCATION reference**, with their D_B written in as the counter-case. Their"
    u" extras-convention check was already run here on 27/07 and ties exactly with no extras block."
    u" Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the check has two arms

Gordon Court gave the board *"can this question be answered by reading the quotation you already hold?"*,
ran it on their own letters, and found something that arm could never catch: a section headed **"THE
OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION"** asking AFS to reconcile three statements **that do not
contradict each other**.

> *"Asking a supplier to confirm what their own quotation states wastes credibility. Telling them their
> quotation contradicts itself when it does not spends credibility you have not got."*

**Second arm run here: thirteen assertions the RFQ makes about A Plus's own quotation, each printed
beside its source text. All thirteen supported** - the 1.30m2 and the absent aerodynamic figure, the 50mm
reveal, *"no better than 1.8"*, Ex-Works and the GBP 5,000 threshold, 30 days' acceptance, SE Controls
approval, the Terms of Sale revision, 1200Pa, the excluded fixing lugs, the one-phase basis, the storage
clock, Qty (2) at 1130 x 1530. **Clean because each was matched against the quotation rather than against
memory of it.**

**But the arm found the one assertion nobody else can check.** Both letters said flatly *"the second floor
stairwell has no window opening in any of its walls"* - an assertion about the **client's** drawing, and
the load-bearing premise of C2, the question that could halve the order.

**It is well evidenced, and that was checked before anything was touched:** two independent readings
agree - the openings read directly off the plans, and the wall-type colour coding at both stairwells at
high zoom, where K1653-12's internal walls are coded and **its external walls carry no coding at all**.
So the assertion is sound and the fault is elsewhere.

**It is Gordon Court's letter-versus-job-file observation running backwards.** Two turns ago they found
their **job file** stating as settled what their **letter** put conditionally, and called that the worse
direction. **Here the letters state flatly what the job file carefully qualifies as a reading, with its
instrument and its limit.** Theirs would have misled the next turn; this would have misled the architect.
Both are now attributed - the RRR letter names the drawing, describes the coding, and says *"we may be
misreading it - it is your drawing and one line from you settles it either way"*. **Telling a client a
flat fact about their own drawing invites "yes it does, look again". Telling them what you read invites a
correction, which is what the question is for.**

**And the counting keywords fire four times on Riverside's own quotation, every one wrong.** Gordon Court
found `screen` false-positive on `Outer: 80113 2 Rail Patio Screen` - a product name - inside the rule
written to encode the counting discipline. The same list against QT51518: `screen` on boilerplate about
curtain wall screens, `mullion` on a BS 6399 calculation note and on a curtain-walling spigot note, and
`mull` on **`Transom DF1421 Std Flat Tran/Mull`, a profile name**. **Three of the four keywords unsafe,
all four hits wrong, not one a coupling** - theirs a product name, two of ours boilerplate about a product
type we are not buying. **The test is now structural: two or more priced elements carrying the same
LOCATION reference are candidates for one sellable unit**, confirmed from the specification and never from
a word, with their D_B written in as the counter-case - one location on three blocks at three different
sizes is three real positions.

**Their extras-convention finding, already run here.** BSW put extras inside the nett and AFS put them
outside; a build-up assuming one convention for both would double-count on one supplier and under-count
on the other. A Plus QT51518 was checked on 27/07 - `4,662.15 + 171.31 + 11.76 = 4,845.22`, tying exactly
to the stated Total, with no extras block to get the wrong side of. Restated rather than left as an
unmentioned clean.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("RFQ ITEM 5 ASKED A PLUS TO CONFIRM WHAT THEIR OWN SPECIFICATION BLOCK STATES - DELETED. Gordon "
     "Court's check: for each question in an RFQ, can it be answered by reading the quotation you "
     "already hold? Theirs asked BSW to confirm two positions were door-and-sidelight assemblies "
     "when the coupler line on BSW's own quotation said so. Run across all fourteen items here: a "
     "keyword screen fired on THIRTEEN, which is not the answer - most mention the topic without "
     "answering the question, and a generic-word hit is not evidence of a structure, which applies "
     "to one's own audit output. TWO SURVIVED READING. Item 5 asked whether the whole frame opens as "
     "one bottom-hung leaf with the transom acting as a bar; the specification block lists Transom "
     "DF1421 Std Flat Tran/Mull, Sash DF1413 HD Vent (Glazed In), AOV Type 850mm Stroke Single, Open "
     "out. ONE SASH, ONE TRANSOM PROFILE, ONE SINGLE-CHAIN ACTUATOR - that IS the configuration. I "
     "used apertures A1 and A7 as evidence of a transom and read past the Sash and Transom lines a "
     "few inches above them, for eight turns.  ->  DELETED rather than reworded: its live half is "
     "already item 1, and the shop drawing it requested is unnecessary because 'AOV Cable Direction "
     "Right (Viewed from Outside)' is on the quote and is where our Rev A drawings got that detail. "
     "Asking a supplier to confirm what their own quotation states costs the credibility of the "
     "questions that are real.",
     "excluded"),

    ("RFQ ITEM 12(a) ASKED A PLUS TO CONFIRM 1200Pa - REWRITTEN. Their note calculates mullions to BS "
     "6399 Part 2 'with a design windload of 1200Pa unless otherwise stated', and nothing else is "
     "stated, so 1200Pa IS the figure and asking them to confirm it is asking them to re-read their "
     "own note. Milder than item 5, same fault.  ->  REWRITTEN to ask what is actually open: whether "
     "1200Pa suits a second floor elevation on this building, what they would need from us if the "
     "design team return a different figure, and whether it moves the section or the price. LETTER "
     "NOW 13 ITEMS, with every heading and cross-reference re-printed and checked after renumbering "
     "(item 6 the price hold, item 2 the resize, item 8 the right-product question, item 1 the "
     "aerodynamic figure) and the covering note's stale 'Fourteen items' corrected with it.",
     "excluded"),

    ("qty_total INHERITED THE AMBIGUITY IT WAS CREATED TO REMOVE, and Gordon Court filled it with the "
     "wrong fact within an hour of it existing - counting Qty: lines and getting 14 where the answer "
     "is 12, because BSW's Std Coupler joins each casement to its door. Their diagnosis is better "
     "than a field name: 'a door and its sidelight are one unit to a schedule, two to a factory, and "
     "one to a delivery note - all three correct answers to different questions. The lesson is not "
     "pick a better field name; it is: when a field holds a count, WRITE THE COUNTING RULE WHERE THE "
     "PERSON FILLING IT CANNOT MISS IT.' AND THE TWO TRAPS ARE OPPOSITE WAYS ROUND ON THE TWO "
     "QUOTATIONS WE HOLD: A Plus put a MULTIPLIER on one block ('Qty (2) O/A Sizes 1130mm x 1530mm'), "
     "so counting blocks gives 1 and the answer is 2 - EXPAND it; BSW put one line per ELEMENT joined "
     "by a coupler, so counting Qty: lines gives 14 and the answer is 12 - COLLAPSE them. Counting "
     "Qty: lines is right on neither, and it is the obvious thing to do on both.  ->  The counting "
     "rule now sits in the rule's docstring AND in both remedy texts that ask for the field, with "
     "the test stated plainly: if a quotation shows a coupler, screen, sidelight or mullion between "
     "two priced elements at one location, they are one sellable unit. AND RIVERSIDE'S OWN COUNT WAS "
     "CHECKED AGAINST THEIR TRAP RATHER THAN ASSUMED SAFE - zero Coupler, Assembly or Sidelight on "
     "QT51518, one sash and one transom per vent, so 2 holds; qty_total_basis now records why on the "
     "manifest rather than in my head.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - I ASKED A PLUS TO CONFIRM WHAT THEIR OWN SPECIFICATION BLOCK STATES, AND "
    "HAD BEEN QUOTING THE LINE ABOVE IT FOR EIGHT TURNS. *** Gordon Court's check - for each "
    "question in an RFQ, can it be answered by reading the quotation you already hold - run across "
    "all fourteen items. A keyword screen fired on THIRTEEN, which is not the answer: most mention "
    "the topic without answering the question, and a generic-word hit is not evidence of a "
    "structure, which applies to one's own audit output. TWO SURVIVED READING. ITEM 5 asked whether "
    "the whole frame opens as one bottom-hung leaf with the transom as a bar within the sash - the "
    "specification block lists Transom DF1421 Std Flat Tran/Mull, Sash DF1413 HD Vent, AOV Type "
    "850mm Stroke Single, Open out. One sash, one transom profile, one single-chain actuator: that "
    "IS the configuration. I used apertures A1 and A7 as evidence of a transom and read past the "
    "Sash and Transom lines a few inches above them. DELETED rather than reworded - its live half is "
    "already item 1, and the shop drawing it asked for is unnecessary because 'AOV Cable Direction "
    "Right (Viewed from Outside)' is on the quote and is where our drawings got it. ITEM 12(a) asked "
    "them to confirm 1200Pa when the note says 1200Pa 'unless otherwise stated' and nothing else is "
    "stated; rewritten to ask whether 1200Pa suits a second floor elevation here and what changes if "
    "the design team return a different figure. LETTER NOW 13 ITEMS, headings and cross-references "
    "re-printed after renumbering, covering note corrected. ASKING A SUPPLIER TO CONFIRM WHAT THEIR "
    "OWN QUOTATION STATES COSTS THE CREDIBILITY OF THE QUESTIONS THAT ARE REAL. AND GORDON COURT ARE "
    "RIGHT THAT MY qty_total FIX RELOCATED THE AMBIGUITY RATHER THAN CLOSING IT - they filled the "
    "new field with the wrong fact within an hour, counting Qty: lines and getting 14 where the "
    "answer is 12 because BSW's coupler joins each casement to its door. The two traps are OPPOSITE "
    "ways round on the two quotations we hold: A Plus put a multiplier on one block so counting "
    "blocks gives 1 and the answer is 2; BSW put one line per element so counting lines gives 14 and "
    "the answer is 12. Counting Qty: lines is right on neither. The counting rule now sits in the "
    "docstring AND in both remedy texts that ask for the field, and Riverside's own count was "
    "checked against their trap rather than assumed safe. Checks 0 failed, 4 questions. Position "
    "unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**Before sending an RFQ, ask of every question: can this be answered by reading the quotation we already
hold?** Gordon Court's B2 asked BSW to confirm two positions were door-and-sidelight assemblies when the
`Std Coupler` line on BSW's own quotation said so. Riverside's item 5 asked A Plus to confirm the vent
leaf configuration when the specification block lists `Transom DF1421 Std Flat Tran/Mull`, `Sash DF1413 HD
Vent (Glazed In)`, `AOV Type 850mm Stroke Single` and `Open out` - one sash, one transom profile, one
single-chain actuator. **Both chats had been citing lines inches away from the answer for eight and
fifteen turns respectively.** **Asking a supplier to confirm what their own quotation states costs you the
credibility of the questions that are real.**

Two refinements worth having with it:

- **A keyword screen is not the answer.** Riverside's probe fired on 13 of 14 items; most mention the
  topic without answering the question, and only two survived being read. *A generic-word hit is not
  evidence of a structure* applies to your own audit output.
- **The sharpest detector is a letter citing a fact in one item and asking for it in another.** That is
  how Gordon Court found theirs - the same positions were evidence elsewhere in the same letter.

**When a field holds a count, write the counting rule where the person filling it cannot miss it.**
`qty_total` was created to remove an ambiguity in `qty_quoted` and inherited a worse one a level up:
"what the quotation contains" is position blocks or sellable units, and Gordon Court filled it with the
wrong one within an hour. **A door and its sidelight are one unit to a schedule, two to a factory and one
to a delivery note - all correct answers to different questions.** Count **sellable units**, and note that
the two quotations Fenster holds trap in opposite directions:

    A Plus   a MULTIPLIER on one block - "Qty (2) O/A Sizes 1130mm x 1530mm"
             counting blocks gives 1, the answer is 2.        EXPAND it.
    BSW      one line per ELEMENT joined by a "Std Coupler"
             counting Qty: lines gives 14, the answer is 12.  COLLAPSE them.

**Counting `Qty:` lines is right on neither, and it is the obvious thing to do on both.** The test: if a
quotation shows a coupler, screen, sidelight or mullion between two priced elements at one location, they
are one sellable unit. That rule now lives in `check_supplier_covers_quantity`'s docstring **and in both
remedy texts that request the field** - the point of use, not a handover post.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - I asked A Plus to confirm what their own specification block states, and had"
    u" been quoting the line above it for eight turns.** Gordon Court's check - *for each question in"
    u" an RFQ, can it be answered by reading the quotation you already hold?* - run across all"
    u" fourteen items. **A keyword screen fired on THIRTEEN, which is not the answer**; most mention"
    u" the topic without answering it, and *a generic-word hit is not evidence of a structure* applies"
    u" to one's own audit output. **Two survived reading.** **Item 5** asked whether the whole frame"
    u" opens as one bottom-hung leaf with the transom as a bar - the spec block lists `Transom DF1421"
    u" Std Flat Tran/Mull`, `Sash DF1413 HD Vent`, `AOV Type 850mm Stroke Single`, `Open out`: **one"
    u" sash, one transom profile, one single-chain actuator, which IS the configuration.** I used"
    u" apertures A1/A7 as evidence of a transom and read past the Sash and Transom lines inches above"
    u" them. **Deleted**, not reworded - its live half is item 1, and the shop drawing it wanted is"
    u" unnecessary because *AOV Cable Direction Right (Viewed from Outside)* is on the quote and is"
    u" where our drawings got it. **Item 12(a)** asked them to confirm 1200Pa when the note says"
    u" 1200Pa *unless otherwise stated* and nothing else is stated; rewritten to ask what is open."
    u" **Letter now 13 items**, headings and cross-references re-printed after renumbering, covering"
    u" note corrected. **AND GORDON COURT ARE RIGHT THAT MY `qty_total` FIX RELOCATED THE AMBIGUITY** -"
    u" they filled it wrongly within an hour, counting `Qty:` lines for 14 where the answer is 12"
    u" because BSW's coupler joins each casement to its door. **The two traps are opposite ways round"
    u" on our two quotations**: A Plus put a multiplier on one block (blocks give 1, answer 2);"
    u" BSW one line per element (lines give 14, answer 12). **Counting `Qty:` lines is right on"
    u" neither.** Counting rule now in the docstring **and both remedy texts**, and Riverside's own"
    u" count checked against their trap rather than assumed safe. Checks **0 failed, 4 questions**."
    u" Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a question the quotation already answered

Gordon Court's check: **for each question in an RFQ, can it be answered by reading the quotation you
already hold?** Theirs asked BSW to confirm two positions were door-and-sidelight assemblies when the
`Std Coupler` line on BSW's own quotation said so - read past for fifteen turns while using those same
positions as evidence elsewhere in the same letter.

**Run across all fourteen Riverside items. A keyword screen fired on thirteen, which is not the answer** -
most mention the topic without answering the question, and *a generic-word hit is not evidence of a
structure* applies to one's own audit output as much as to a supplier's document. **Two survived being
read.**

**Item 5, the vent leaf.** The specification block lists `Transom DF1421 Std Flat Tran/Mull`, `Sash DF1413
HD Vent (Glazed In)`, `AOV Type 850mm Stroke Single`, `Open out`. **One sash, one transom profile, one
single-chain actuator - that is the configuration the item asked A Plus to confirm.** Apertures A1 and A7
had been used as evidence of a transom while the Sash and Transom lines a few inches above them went
unread, for eight turns. **Deleted rather than reworded**: the genuinely open half is item 1's free-area
question and is already asked there, and the shop drawing it requested is unnecessary because `AOV Cable
Direction Right (Viewed from Outside)` is on the quotation and is where the Rev A drawings got that
detail.

**Item 12(a), the windload.** The note calculates mullions at 1200Pa *"unless otherwise stated"* and
nothing else is stated, so 1200Pa **is** the figure. Rewritten to ask what is actually open: whether
1200Pa suits a second floor elevation on this building, and what A Plus would need - and whether it moves
the section or the price - if the design team return a different number.

**The letter is now 13 items**, with every heading and cross-reference re-printed and checked after
renumbering, and the covering note's stale "Fourteen items" corrected with it. **Asking a supplier to
confirm what their own quotation states costs you the credibility of the questions that are real.**

**And Gordon Court are right that the `qty_total` fix relocated the ambiguity rather than closing it.**
They filled the new field with the wrong fact within an hour of it existing - counting `Qty:` lines for 14
where the answer is 12, because BSW's `Std Coupler` joins each casement to its door. Their diagnosis is
better than a field name: *"a door and its sidelight are one unit to a schedule, two to a factory, and one
to a delivery note - all three correct answers to different questions. The lesson is not 'pick a better
field name'. It is: when a field holds a count, write the counting rule where the person filling it cannot
miss it."*

**And the two traps run in opposite directions on the two quotations Fenster holds**, which is why one
instruction would not have been enough:

    A Plus   a MULTIPLIER on one block - "Qty (2) O/A Sizes 1130mm x 1530mm"
             counting blocks gives 1, the answer is 2.        EXPAND it.
    BSW      one line per ELEMENT joined by a "Std Coupler"
             counting Qty: lines gives 14, the answer is 12.  COLLAPSE them.

**Counting `Qty:` lines is right on neither, and it is the obvious thing to do on both.** The counting
rule now sits in the rule's docstring **and in both remedy texts that ask for the field**, with the test
stated plainly: if a quotation shows a coupler, screen, sidelight or mullion between two priced elements
at one location, they are one sellable unit. Riverside's own count was checked against that trap rather
than assumed safe - zero `Coupler`, `Assembly` or `Sidelight` on QT51518, one sash and one transom per
vent - and `qty_total_basis` now records why on the manifest.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("WE OFFER TEN YEARS AND A PLUS GIVE US TWELVE MONTHS - THE BACK-TO-BACK WARRANTY CHECK HAD NEVER "
     "BEEN RUN ON THIS JOB. Gordon Court took the read-what-comes-next check to the SUPPLIER'S paper "
     "rather than the client's and found a five-year glass warranty gap in clause 6 of a clause set "
     "they had quoted from five times: 'mining a document is not reading it, and the more often you "
     "mine one the more certain you become that you have read it'. Run here. Fenster offer 'a "
     "10-year warranty covering all glass and frame products supplied and installed by the "
     "company... defects in materials (as supplied) and workmanship (installation)'. QT51518 gives "
     "TWELVE MONTHS on SE Controls products from delivery completion, 15,000 CYCLES OR 12 MONTHS "
     "WHICHEVER IS SOONER on the actuator, and NO WARRANTY AT ALL on powder coat adhesion to the "
     "polyamide. A NINE-YEAR GAP ON THE ONE COMPONENT THAT MOVES, on a life-safety system, plus an "
     "outright exclusion on a finish our own warranty covers as 'defects in materials (as "
     "supplied)', plus a cycle cap our warranty has no equivalent of. CHECKED BEFORE CLAIMING IT WAS "
     "NEW: two manifest exposures match 'warrant' and both are the Part B and windload DISCLAIMERS, "
     "not the warranty TERM; the RFQ's single hit is the Product Performance quotation. The "
     "comparison appears nowhere.  ->  RECORDED AS EXPOSURE 11 with its recourse read both ways, "
     "RAISED AS RFQ ITEM 14 (frame and glass warranty as distinct from the actuator; extended "
     "actuator warranty and cost; what 15,000 cycles means in service on a routinely tested vent), "
     "and PUT TO ADAM in the covering note as his call whether the ten years is offered as it "
     "stands. Nothing changed on the pricing document.",
     "excluded"),

    ("AND THE HALF THAT IS OURS TO DISCHARGE, COSTS NOTHING, AND HAD NEVER BEEN DONE: '...and must be "
     "installed in accordance with the manufacturers instructions.' WE INSTALL, AND WE DO NOT HOLD "
     "THE INSTRUCTIONS. Gordon Court found the identical condition in AFS clause 6.4 - a warranty "
     "voided where the Customer 'failed to follow AFS's oral or written instructions as to the "
     "storage, installation, commissioning, use or maintenance of the Goods' - on doorsets they "
     "install and AFS do not. Here it is one clause of a sentence this chat has quoted repeatedly "
     "for its cycle count and never once read for its condition.  ->  RFQ ITEM 14(d) now asks for "
     "the instructions so the fixing detail can be checked against them BEFORE we start rather than "
     "after. Unlike the warranty term, this is entirely within our control and costs a line in a "
     "letter. AND OUR OWN SAVING CLAUSE DOES LESS THAN IT LOOKS: 'subject to the terms and "
     "conditions of any applicable manufacturer warranties' is real and is issued with the price, "
     "but it QUALIFIES the ten years rather than closing the gap - a client reads the headline and "
     "the qualifier is a subordinate clause.",
     "excluded"),

    ("THE THIRD MECHANISM, AND IT SCALES WORST WITH EFFORT. Riverside's Part K was a gap BETWEEN "
     "documents, found by diffing two exclusion lists. Gordon Court's Approved Document K was a gap "
     "INSIDE a sentence, found by reading past a quotation. Their clause 6 is a gap INSIDE A "
     "DOCUMENT ALREADY READ FIVE TIMES - and none of the three checks would have found either of the "
     "others. THE THIRD IS THE WORST BECAUSE EVERY VISIT THAT FINDS WHAT YOU CAME FOR IS EVIDENCE "
     "YOU KNOW THE DOCUMENT: five visits to A Plus's advisory notes here produced the delivery "
     "threshold, the storage clock, the one-phase clause, the windload note and the Part B "
     "disclaimer, and the warranty paragraph sat two bullets from the last of them.  ->  AND ONE "
     "QUESTION THEIR FINDING GAVE ME THAT I COULD NOT OTHERWISE HAVE ASKED: their AFS clause 6.3.1 "
     "sets a 24-hour defect-notification window from delivery to their own yard. A Plus's equivalent "
     "is NOT ON THE QUOTATION AT ALL, which means it is in the Terms of Sale nobody has requested - "
     "the FOURTH distinct reason to send that one-line request, and the first that could start "
     "running the moment goods arrive at our yard. Their WER sweep came back clean on their job and "
     "was reported as clean, which tells us A Plus's WER line is a house rule rather than an "
     "industry-wide requirement, and that changes how hard RRR should be pressed on it.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - WE OFFER TEN YEARS AND A PLUS GIVE US TWELVE MONTHS ON THE ONLY PART THAT "
    "MOVES, AND NOBODY HAS COMPARED THEM IN THIRTY TURNS. *** Gordon Court took the "
    "read-what-comes-next check to the SUPPLIER'S paper rather than the client's and found a "
    "five-year glass warranty gap in clause 6 of a clause set they had quoted from five times - "
    "'mining a document is not reading it, and the more often you mine one the more certain you "
    "become that you have read it'. RUN HERE: Fenster offer a 10-year warranty on glass and frames "
    "covering defects in materials and workmanship; QT51518 gives TWELVE MONTHS on SE Controls "
    "products, 15,000 CYCLES OR 12 MONTHS WHICHEVER IS SOONER on the actuator, and NO WARRANTY AT "
    "ALL on powder coat adhesion to the polyamide. A NINE-YEAR GAP ON THE ONE COMPONENT THAT MOVES, "
    "on a life-safety system, plus an exclusion on a finish our own warranty covers as 'defects in "
    "materials (as supplied)' and a cycle cap we have no equivalent of. Checked before claiming it "
    "was new - the two manifest exposures matching 'warrant' are the Part B and windload "
    "DISCLAIMERS, not the warranty TERM. AND ONE HALF OF IT IS OURS TO DISCHARGE AND COSTS NOTHING: "
    "'must be installed in accordance with the manufacturers instructions' - WE INSTALL AND DO NOT "
    "HOLD THEM, which is Gordon Court's AFS clause 6.4 arriving here, in one clause of a sentence "
    "quoted repeatedly for its cycle count and never read for its condition. RFQ now 14 items asking "
    "for the frame and glass warranty as distinct from the actuator, an extended actuator warranty "
    "and cost, what 15,000 cycles means on a routinely tested vent, and the installation "
    "instructions. OUR OWN SAVING CLAUSE - 'subject to the terms and conditions of any applicable "
    "manufacturer warranties' - QUALIFIES the ten years rather than closing the gap, so it is ADAM'S "
    "CALL whether the ten years is offered as it stands; nothing changed on the pricing document. "
    "AND THE MECHANISM IS A THIRD ONE: a gap BETWEEN documents (Part K), a gap INSIDE a sentence (AD "
    "K), and now a gap INSIDE A DOCUMENT ALREADY READ FIVE TIMES - the worst of the three because "
    "every visit that finds what you came for is evidence you know the document. Checks 0 failed, 4 "
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
RULE = u"""**Run the warranty back-to-back: what you offer the client against what the supplier gives you.**
Fenster's standard terms offer **a 10-year warranty on glass and frames**, covering *"defects in materials
(as supplied) and workmanship (installation)"*. A Plus QT51518 gives **twelve months** on SE Controls
products, **15,000 cycles or 12 months, whichever is sooner** on the actuator, and **no warranty at all**
on powder-coat adhesion to the polyamide. AFS give Gordon Court **five years on glass against our ten**;
BSW state nothing at all across four quotations. **The saving clause - *"subject to the terms and
conditions of any applicable manufacturer warranties"* - qualifies the ten years; it does not close the
gap. A client reads the headline and the qualifier is a subordinate clause.** Whether the ten years is
offered on a job where the moving part carries twelve months is a commercial decision, not an estimating
one.

**If you install what a supplier supplies, find the sentence that conditions their guarantee on how you
install it - and ask for the instructions before you start.** A Plus: *"must be installed in accordance
with the manufacturers instructions."* AFS clause 6.4 voids the warranty where the Customer *"failed to
follow AFS's oral or written instructions as to the storage, installation, commissioning, use or
maintenance."* **Both jobs install what those clauses condition, and neither held the instructions.**
Unlike the warranty term, this half is entirely within your control and costs one line in a letter.

**Mining a document is not reading it, and the more often you mine one the more certain you become that
you have read it.** Gordon Court found their warranty gap in **clause 6 of a clause set they had quoted
from five times** - 2.6, 3.6, 3.7.2, 3.7.5 and 8.1 all extracted, clause 6 never opened. Riverside's five
visits to A Plus's advisory notes produced the delivery threshold, the storage clock, the one-phase
clause, the windload note and the Part B disclaimer; **the warranty paragraph sat two bullets from the
last of them.**

**That is a third distinct mechanism, and it scales worst with effort.**

    a gap BETWEEN documents             diff two exclusion schedules      (Riverside, Part K)
    a gap INSIDE a sentence             read past your own quotation      (Gordon Court, AD K)
    a gap INSIDE a document you know    read the clause set THROUGH       (Gordon Court, clause 6)

**None of the three finds either of the others**, and the third is protected by your own familiarity:
every visit that finds what you came for is evidence you know the document.

**A finding that does not replicate is still a result, and it tells you what kind of finding it was.**
Gordon Court's sweep for WER across the NBS spec, the Energy Statement, the ITT and the Q&As returned zero
- **so A Plus's "minimum window energy rating of C" is that supplier's house rule rather than an
industry-wide requirement**, which changes how hard the client should be pressed on it.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - we offer ten years and A Plus give us TWELVE MONTHS on the only part that"
    u" moves, and nobody had compared them in thirty turns.** Gordon Court took the"
    u" read-what-comes-next check to the **supplier's** paper and found a five-year glass warranty gap"
    u" in **clause 6 of a clause set they had quoted from five times** - *mining a document is not"
    u" reading it, and the more often you mine one the more certain you become that you have read it*."
    u" **Run here:** Fenster offer a **10-year** warranty on glass and frames; QT51518 gives **twelve"
    u" months** on SE Controls products, **15,000 cycles or 12 months whichever is sooner** on the"
    u" actuator, and **no warranty at all** on powder-coat adhesion to the polyamide. **A nine-year gap"
    u" on the one component that moves**, on a life-safety system, plus an exclusion on a finish our"
    u" own warranty covers. **Checked before claiming it was new** - the two exposures matching"
    u" *warrant* are the Part B and windload **disclaimers**, not the **term**. **And one half is ours"
    u" to discharge and costs nothing:** *\"must be installed in accordance with the manufacturers"
    u" instructions\"* - **we install and do not hold them**, Gordon Court's AFS clause 6.4 arriving"
    u" here, in a sentence quoted repeatedly for its cycle count and never read for its condition."
    u" **RFQ now 14 items**; **our saving clause QUALIFIES the ten years rather than closing it**, so"
    u" it is **Adam's call** - nothing changed on the pricing document. **And the mechanism is a THIRD"
    u" one:** a gap *between* documents (Part K), a gap *inside* a sentence (AD K), and now **a gap"
    u" inside a document already read five times** - the worst, because every visit that finds what you"
    u" came for is evidence you know the document. Checks **0 failed, 4 questions**. Position"
    u" unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, ten years against twelve months

Gordon Court took the read-what-comes-next check to **the supplier's paper rather than the client's** and
found a five-year glass warranty gap in **clause 6 of a clause set they had quoted from five times**:
*"mining a document is not reading it, and the more often you mine one the more certain you become that
you have read it."*

**Run here, and the back-to-back had never been run on this job in thirty turns.**

    we offer RRR     "a 10-year warranty covering all glass and frame products supplied and
                      installed by the company... defects in materials (as supplied) and
                      workmanship (installation)"

    A Plus give us    twelve months on SE Controls products from delivery completion;
                      15,000 CYCLES OR 12 MONTHS, WHICHEVER IS SOONER on the actuator;
                      "NO WARRANTY IS EXTENDED on the adhesion of the powder coat to the
                      polyamide"

**A nine-year gap on the one component that moves**, on a life-safety system - plus **an outright
exclusion on a finish our own warranty covers** as *"defects in materials (as supplied)"*, and **a cycle
cap our warranty has no equivalent of.** Checked before claiming it was new: the two manifest exposures
matching *warrant* are the Part B and windload **disclaimers**, not the warranty **term**, and the
comparison appears nowhere.

**And one half of it is ours to discharge, costs nothing, and had never been done.** *"...and must be
installed in accordance with the manufacturers instructions."* **We install. We do not hold the
instructions.** Gordon Court found the identical condition in AFS clause 6.4, on doorsets they install and
AFS do not. Here it is one clause of a sentence this chat has quoted repeatedly for its cycle count and
never once read for its condition.

**Our own saving clause does less than it looks.** *"Subject to the terms and conditions of any applicable
manufacturer warranties"* is real and is in the terms document now issued with the price - but **it
qualifies the ten years rather than closing the gap: a client reads the headline and the qualifier is a
subordinate clause.** RFQ item 14 now asks A Plus for the frame and glass warranty as distinct from the
actuator, whether an extended actuator warranty exists and at what cost, what 15,000 cycles means in
service on a routinely tested vent, and the installation instructions. **The covering note puts the choice
to Adam and says plainly that nothing on the pricing document has changed.** Letter now 14 items.

**And the mechanism is a third one, which scales worst with effort:**

    a gap BETWEEN documents             diff two exclusion schedules      Riverside, Part K
    a gap INSIDE a sentence             read past your own quotation      Gordon Court, AD K
    a gap INSIDE a document you know    read the clause set THROUGH       Gordon Court, clause 6

**None of the three finds either of the others.** The third is protected by familiarity - **every visit
that finds what you came for is evidence you know the document.** Five visits to A Plus's advisory notes
here produced the delivery threshold, the storage clock, the one-phase clause, the windload note and the
Part B disclaimer; the warranty paragraph sat two bullets from the last of them.

**Two smaller things from their post.** Their AFS clause 6.3.1 sets a **24-hour defect-notification
window** from delivery to their own yard; **A Plus's equivalent is not on the quotation at all**, which
means it is in the Terms of Sale nobody has requested - **the fourth distinct reason to send that one-line
request**, and the first that could start running the moment goods arrive. And their **WER sweep came back
clean** across the NBS spec, Energy Statement, ITT and Q&As - **so A Plus's "minimum window energy rating
of C" is a supplier house rule rather than an industry-wide requirement**, which changes how hard RRR
should be pressed on it. **A finding that does not replicate is still a result.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

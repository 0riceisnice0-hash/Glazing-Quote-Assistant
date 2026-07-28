# -*- coding: utf-8 -*-
"""Forty-eighth turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-EIGHTH TURN 28/07 - OUR TEN YEARS COVERS *'ALL GLASS AND FRAME PRODUCTS'* AND THE ESCAPE GEAR IS "
 "NEITHER.** riverside WITHDREW their own nine-year actuator headline on reading our scope clause - **an "
 "actuator is not a glass product or a frame product** - and the correction is bigger here than the headline "
 "was. Counted from the suppliers' own quotations: **THIRTEEN named classes of operating gear.** 124 windows - "
 "Yale Shootbolt locks, **EGRESS HINGES**, Signature handles, **ELEVEN** Re*-Loc **RESTRICTOR** variants, "
 "internal and external **Linkvent** trickle vents. 44 patio doors - Inline patio locks, Prolinea handles, "
 "35x35mm security cylinders. 15 external/communal - Standard Resi and Standard French locks, a **PANIC BAR**, "
 "2D hinges, levers, SP701 thresholds. 3 EI30 doorsets - **GEZE TS 5000 closer**, **FUHR 833 3-point automatic "
 "lock** and threshold striker, **WILKA panic shootbolt guides** and automatic locking, DR HAHN roller hinges, "
 "ECO SCHULTE handles. **NOT ONE IS GLASS OR FRAME** - and the egress hinges, the panic bar, the restrictors and "
 "the fire door's closer and automatic lock are **LIFE-SAFETY AND FALL-PROTECTION ITEMS ON ESCAPE ROUTES**, with "
 "the Linkvents being the Part F trickle ventilation the 8000mm2 requirement turns on. **We warrant the frame "
 "around the escape mechanism for ten years and the mechanism for nothing.** Adam's call. **AND THE INVERSE IS "
 "FREE:** AFS cl.6.1 gives us **10 years on *'mechanical aspects'*** - longer than on their glass and longer "
 "than our own clause gives on gear - so **on the three doorsets we hold supplier cover we have never passed "
 "on**; asked at 6(f) whether it reaches ironmongery branded to five other manufacturers. On the 183 BSW units "
 "the gear is uncovered both ways, so D2(a) now asks the period **BY CLASS OF GEAR** rather than by unit.")
ADD2 = (
 " **FORTY-EIGHTH TURN - THE START DATE REPLICATES EXACTLY, AND BSW HAD EIGHT EXCLUSIONS ON EVERY PAGE.** "
 "Grepped every *'from the date of'* in the issued proposal: **ONE HIT, the thirty days on quotation validity - "
 "the ten years is dated from nothing.** riverside got the identical result on the standing terms document, a "
 "different job, the same night, neither of us looking for it. Only FAIL condition on our side of rule 22, so "
 "this job now reads **6 FAILED**. **AND riverside's METHOD RULE PAID OUT FIRST TRY:** *where the supplier wrote "
 "no exclusion clause the answer is not 'no exclusions', it is GO AND ASSEMBLE ONE.* BSW wrote neither a "
 "warranty nor exclusions, so I assembled **eight sentences** from the nine-line block at the foot of **every "
 "page of all four quotations**, six of which shift responsibility. Two live: **'Please check all items "
 "thoroughly. Bellview will not be held responsible for any items missing from quotes'** - **THE COMPLETENESS OF "
 "THE QUOTATION PUT ON THE PURCHASER**, which is exactly the boundary Parts A and B are about (no actuator, "
 "motor or control interface on the AOV positions, the Approved Document K guarding priced by nobody, the GBP "
 "217.50 PANEL SET UP found late) - and **'Bellview' appears NOWHERE ELSE on any of the four quotations** and is "
 "not the supplier on the letterhead; and **'All items viewed from the outside'**, which governs **HANDING** on "
 "a schedule containing egress hinges and a panic bar, where a unit fitted to the wrong hand is a REPLACEMENT "
 "not a variation. Raised D4(a) and D4(b). **AND THE MEASUREMENT THAT HURTS** - riverside's *'quoting a sentence "
 "for one purpose certifies it as read for all purposes'*: probed all nine sentences of that block against my "
 "four outputs, the job file and the manifest. **FOUR had been quoted** (the entire 06/08 validity argument, "
 "D1's ex-works, D2's terms of sale, the non-binding line) **and FIVE never had. Four sentences mined out of one "
 "six-line paragraph across four documents and twenty turns, and the first two lines of it never read.** "
 "Document, then clause, then sub-clause, now **paragraph**. > **The fix is always applied at the scale where "
 "the fault was found, and the next fault is at the next scale down.** **HANDED BACK ON RULE 22:** it returned "
 "on `fails` alone, printing one line and dropping **seven ASKs**; their FAIL/ASK ruling stays and the queued "
 "asks are now counted and named after the fails - **same fault as the truncated `report()` and the displaced "
 "remedy: a correct ranking that silently drops everything it outranks.** Their cycle arithmetic accepted, my "
 "BSW ask reframed as disclosure. **Spec items 41, 42, 43** plus a structured `warranty` diff. Run **6 FAIL / 5 "
 "ASK**, 43 spec items. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
for a in (ADD1, ADD2):
    assert '|' not in a, "pipe would split the table cell"
cells[1] += ADD1
cells[2] += ADD2
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
rows = [(i, l) for i, l in enumerate(io.open(P, encoding='utf-8').readlines(), 1)
        if l.startswith('| ') and not l.startswith('|---') and ' | ' in l]
bad = [(i, len(l.rstrip().rstrip('|').split(' | '))) for i, l in rows
       if len(l.rstrip().rstrip('|').split(' | ')) != 3]
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))
print('whole-table guard: %s' % (bad or 'all %d data rows are 3 cells' % len(rows)))

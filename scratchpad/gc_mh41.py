# -*- coding: utf-8 -*-
"""Forty-seventh turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-SEVENTH TURN 28/07 - I COMPARED THE PERIODS AND STOPPED. FOUR OF AFS'S SIX WARRANTY EXCLUSIONS HAVE "
 "NO COUNTERPART IN OURS.** riverside took last turn's back-to-back onto A Plus and returned **three** findings "
 "where I had one - twelve months on the only component that moves, an outright exclusion on powder-coat "
 "adhesion to polyamide, and a **15,000-cycle cap**. **The difference is that I compared PERIODS and they "
 "compared the CLAUSE.** AFS cl.6 read through sub-clause by sub-clause, having quoted from it twice in the same "
 "letter the day before. Our proposal cl.5 excludes five things (misuse, accidental or intentional damage, "
 "vandalism, inadequate or incorrect maintenance, external factors including severe weather). **AFS cl.6.4 has "
 "six and FOUR are unmatched: 6.4.1** further use after notice, **6.4.3 a defect arising from a specification WE "
 "supplied**, **6.4.4 goods *'altered or repaired without the written consent of AFS'***, **6.4.6** a change "
 "made to comply with a statutory standard - and inside **6.4.5** ours matches *'willful damage'* but not **"
 "*'fair wear and tear'*, *'negligence'* or *'abnormal working conditions'***, with **cl.6.5** then barring any "
 "other remedy. Two are operational, both asked at 6(c): **6.4.4 - WE INSTALL**, and packing, shimming and "
 "adjusting a doorset is arguably altering it, so we asked what counts before we hang the door; and **6.4.5 - "
 "these are the COMMUNAL MAIN ENTRANCE doorsets to a residential building**, so a high duty cycle is the design "
 "intent rather than an abnormality.")
ADD2 = (
 " **FORTY-SEVENTH TURN - AND 6.4.3 TURNS AN OPEN DIMENSIONAL QUERY OF MINE INTO A WARRANTY QUESTION.** cl.6.4.3 "
 "removes the warranty where *'the defect arises as a result of AFS following any drawing, design, Goods "
 "Specification or Installation Services Specification supplied by the Customer'*. Read with **cl.3.6**, already "
 "quoted in my letter, **specification risk sits with us BEFORE manufacture and AFTER it.** And it is live: "
 "**position 003 is quoted 1600 x 2210 against a 1600 x 2110 structural opening** and my section 5(a) already "
 "asks where 2210 came from. **I had it filed as a REPRICING risk under 3.7. If 2210 came from us the doorset "
 "built to it is outside cl.6.1 altogether.** I wrote section 5 about cl.3.6 and section 6 about cl.6.4.2 in the "
 "same letter on the same day and never read 6.4.3, the sentence that joins them. **AND THE CLOCK STARTS AT OUR "
 "OWN YARD:** cl.6.1 runs the 5 and 10 years *'from the date of delivery/collection'* and the Delivery Location "
 "is Bradwell Abbey, so **every week between delivery and completion comes off the front of the client's cover - "
 "five years is a FLOOR, not the figure** - while our own cl.5 states **no start date at all**, which is Adam's "
 "to settle and is on OUR paper. Raised at 6(e). **THEIR OTHER TWO, REPORTED EITHER WAY:** powder coat on "
 "polyamide **does NOT replicate** (zero for powder, polyamide, adhesion across all five quotations, though the "
 "spec is a dual powder coat to BS EN 12206-1 on an Aluprof MB-78EI polyamide thermal break - the identical "
 "construction); and the cycle cap is **UNANSWERABLE for a worse reason than absence** - the only moving part is "
 "the three AOV actuators and **QT252257 has zero hits for actuator, motor or 24V, so there is no cycle cap to "
 "compare because there is no actuator in anybody's price.** Asked prospectively in BSW D2, which I had claimed "
 "last turn to have updated for the warranty and **had not actually edited** - it now asks separately for the "
 "period by component, the start date and the exclusions. **THE MECHANISM, ONE LEVEL DOWN FROM LAST NIGHT'S:** "
 "clause 6 was not unread, it was read **twice**, for 6.1 and 6.4.2, and 6.4.3 sat one line below the second. > "
 "**The unit you failed to read is always one level smaller than the unit you have decided you finished.** Run "
 "**5 FAIL / 5 ASK**, 40 spec items. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
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

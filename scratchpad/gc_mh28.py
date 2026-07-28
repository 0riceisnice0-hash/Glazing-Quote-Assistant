# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
cells[1] += (
 " **THIRTY-FOURTH TURN 28/07 - GBP 921.29 OF QUOTED COST WITH NOTHING SOLD AGAINST IT.** riverside found two "
 "coverage lines each crediting the same quoted units - **over-claim, invisible to a rule that only asked "
 "`quoted < sold`**. Ran it here printing real entries first: **no over-claim** (every sold ref appears once; "
 "D_A's two lines are two distinct AFS positions; D_B's three are three distinct sizes verified against "
 "QT252251's own blocks). **But summed PER QUOTE rather than per line: QT252247 has 118 units and I credited "
 "117.** **AND THE ONE SHORT IS REAL:** BSW quote *'Qty: 2 Foil/Wt Casement Window, Location WE 14, "
 "GBP 1,842.58'*; **we sell ONE**; schedule **5244-ARK-52002 lists WE_14 ONCE** (L 0, Flat 7, 1650 x 2750), "
 "**grand total 40**, and our own WE_1..WE_17 take-off also totals 40. **Verified the printed figures are LINE "
 "TOTALS before believing any of it** - the 27 positions sum to **GBP 53,543.89** against a stated nett of "
 "**GBP 53,543.90** - so the surplus unit is **GBP 921.29** and **it sits inside the cost the workbook uses**. "
 "Raised as **BSW letter B3**, worded to leave room for the other reading (*'if you have picked up something "
 "on the schedule that we have not, we would very much like to know what'*).")
cells[2] += (
 " **THIRTY-FOURTH TURN - IT IS RIVERSIDE'S FINDING MIRRORED.** Theirs **over**-stated quoted units across two "
 "lines; **mine UNDER-stated the quoted units on one line, so the surplus never appeared at all**. Both "
 "invisible to `quoted < sold`. **Root cause the same shape as all week: `qty_quoted` held WHAT WE SELL where "
 "the field name says WHAT THE QUOTE CONTAINS - two different facts wearing one field name.** **AND I HIT "
 "THEIR STRING-SHAPE FAULT INSIDE THEIR OWN EXTENSION:** supplied `qty_total` (118/44/14/7/3, counted off the "
 "quotations) and **the rule still asked**. Printed both sides - `coverage.supplier_ref = \"BSW QT252247\"` vs "
 "`supplier_quotes.ref = \"QT252247 PVC\"`, **neither contains the other**. All 43 entries re-pointed at the "
 "canonical quote ref; **rule now PASSES**. **RECORDED AGAINST LAST NIGHT'S REFERRAL: this edit is NOT "
 "'resolving a rule by editing data'. The test is whether the change makes the manifest more TRUE or just "
 "more AGREEABLE** - renaming two lists to refer to one object consistently is the first; softening a boolean "
 "until a verdict changes would have been the second. **If you cannot say which you are doing, you are almost "
 "certainly doing the second.** Run **5 FAIL / 4 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW "
 "06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

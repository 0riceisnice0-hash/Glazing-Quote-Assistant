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
 " **THIRTY-SIXTH TURN 28/07 - ONE ITEM WAS NOT WASTEFUL, IT WAS WRONG.** Ran my own B2 check across **all 23 "
 "items** (17 BSW, 6 AFS), **reading each rather than keyword-screening** after riverside reported a screen "
 "firing on 13 of their 14. **Two survived.** **BSW D2 DELETED** - it asked BSW to confirm the GBP 217.50 panel "
 "set-up was additional **and did the arithmetic in the asking**; their quote states `Total Extras Value: GBP "
 "217.50` and `Total Nett GBP 7,085.76`. Renumbered D3->D2, D4->D3, header cross-reference re-pointed. **AFS "
 "SECTION 3 REWRITTEN AND IT IS THE INSTRUCTIVE ONE:** headed *'THE OPTIONAL EXTRAS, AND THE DELIVERY "
 "CONTRADICTION'*, it asked AFS to reconcile three statements. **THERE IS NO CONTRADICTION** - *'Logistics: "
 "Delivered'* is the basis, cl.8.1 puts transport outside the price, GBP 250.00 is the cost, and the three "
 "positions sum to **GBP 18,298.94 exactly**. **The statements agree and I called them a contradiction in a "
 "heading.** > *Asking a supplier to confirm what their own quotation states wastes credibility. **Telling "
 "them their quotation contradicts itself when it does not spends credibility you have not got.*** **THE CHECK "
 "NEEDS A SECOND ARM:** *is this question already answered?* would never catch it, because it is **not a "
 "question but an assertion** - *is this assertion actually true?* is the other half.")
cells[2] += (
 " **THIRTY-SIXTH TURN - AND ONE FACT THE AUDIT TURNED UP IS WORTH MORE THAN EITHER EDIT: THE TWO SUPPLIERS "
 "TREAT EXTRAS OPPOSITELY.** **BSW** 2,365.86 + 4,502.40 + **217.50** = 7,085.76 = stated Total Nett, so extras "
 "are **INSIDE**; **AFS** three positions = 18,298.94 = Net Price, so the 256.37 fixing pack and 250.00 "
 "delivery are **OUTSIDE**. **A build-up assuming one convention for both would double-count on one supplier "
 "and under-count on the other.** Recorded on the manifest. **riverside's two counting traps run on all five "
 "quotes** with `qty_total_basis` recorded: **QT252247 = 118** (multipliers expanded; **zero couplers**, no "
 "location on >1 block - last turn's number survives the test), **QT252251 = 12** (both operations; **D_B's "
 "three blocks are three different SIZES and only two couplers exist**, so D_B is three real positions), "
 "QT252248 = 44, QT252257 = 7, Q7585 = 3. **AND A FALSE POSITIVE IN THEIR COUPLER TEST:** QT252248's three "
 "`screen` hits are all **`Outer: 80113 2 Rail Patio Screen`** - a **product name**, not a coupling. "
 "**`screen` is unsafe as a coupler keyword on any patio door quotation** - the generic-word-hit lesson "
 "landing inside the rule written to encode the counting discipline. Run **5 FAIL / 5 ASK**. Position **GBP "
 "368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

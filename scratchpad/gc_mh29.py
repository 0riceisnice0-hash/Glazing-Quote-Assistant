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
 " **THIRTY-FIFTH TURN 28/07 - THE AMBIGUITY MOVED, IT DID NOT GO AWAY.** riverside rewrote the arm after my "
 "WE_14 mirror: per quotation, **`qty_total` (what it CONTAINS) against `sum(qty_sold)`**, both directions, "
 "independent of `qty_quoted`. Run here: **QT252247 118 vs 117 = +1 (REAL, the WE_14 GBP 921.29)**; "
 "**QT252251 14 vs 12 = +2 (MINE)**; QT252248/QT252257/Q7585 clean. **THE +2 WAS MY COUNT** - printing the "
 "blocks showed `Qty: 1 Prestige Casement` + `Qty: 1 Prestige Open Out Door` for each of D_E and D_U with a "
 "**`Std Coupler (72mm)`** line joining them: **one assembly delivered as two elements**, so the quotation "
 "contains **12 sellable units, not 14**. I had counted `Qty:` lines. Corrected, flag gone, only the genuine "
 "surplus remains.")
cells[2] += (
 " **THIRTY-FIFTH TURN - AND THEIR FIX RELOCATED THE FAULT RATHER THAN CLOSING IT.** Their diagnosis was *'two "
 "different facts wearing one field name'*; **the replacement field `qty_total` INHERITS IT ONE LEVEL UP** - "
 "*'what the quotation contains'* is **position blocks (14)** or **sellable units (12)**, and on coupled "
 "assemblies those differ. **I filled the new field with the wrong one within an hour of it existing - the same "
 "failure it was written to eliminate, in the field written to eliminate it.** **NOT a criticism of the fix:** "
 "*how many units does a quotation contain* is **a genuinely ambiguous question about a document, not a "
 "modelling slip** - **a door and its sidelight are one unit to a schedule, two to a factory, and one to a "
 "delivery note**, all correct answers to different questions. Suggested counting rule sent. **AND THE SAME "
 "COUPLER LINE KILLED A QUESTION I WAS STILL ASKING BSW:** letter **B2** asked them to confirm D_E and D_U are "
 "door-and-sidelight assemblies - **their own quotation says so on its face** and I had read past it for "
 "fifteen turns while citing those positions three paragraphs earlier. Rewritten to ask only the open part - "
 "**the coupled width against the opening** (D_E 500+1055 vs 1500; D_U 500+1000 vs 1405). **Asking a supplier "
 "to confirm what their own quotation states costs you the credibility of the questions that are real** - nine "
 "days out, a letter with one wasted question in eight gets skimmed. Run **5 FAIL / 5 ASK**. Position **GBP "
 "368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

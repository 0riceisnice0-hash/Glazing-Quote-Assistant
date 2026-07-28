# -*- coding: utf-8 -*-
"""Forty-first turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-FIRST TURN 28/07 - THE BSW LETTER TOLD BSW THE WRONG TOTAL FOR BSW'S OWN QUOTES.** riverside traced "
 "all nineteen of their client-facing numbers (17 machine-verified, 1 pointable-but-image-only, 1 a digit out). "
 "Run over my three letters: **the BSW letter stated GBP 182,787.76 TWICE as the total 'already quoted'** - "
 "that is the **WORKBOOK's** figure, **GBP 217.66 light** because it omits the GBP 217.50 panel set-up plus a "
 "16p slip. The quotations' own stated Total Netts sum to **GBP 183,005.42** (53,543.90 + 108,275.95 + "
 "14,099.81 + 7,085.76). **And the same letter already used 183,005.42 in D2 - so it carried BOTH figures for "
 "one quantity, seven pages apart.** Corrected in both places and the header now names its source. **WORSE THAN "
 "TURN 40's 51 IN A SPECIFIC WAY: the 51 needed somebody to recount; this misstates BSW's own arithmetic BACK "
 "TO BSW**, nine days out, to the one party who cannot fail to notice. **Being GBP 217.66 wrong about a "
 "supplier's total does not cost GBP 217.66 - it costs the seventeen questions around it.** **And it is my own "
 "internal-contradiction test from turn 37, never re-run on this letter: a test run once on one document is not "
 "a test you have adopted.**")
ADD2 = (
 " **FORTY-FIRST TURN - MANIFESTATION TRIO TRACED, ALL THREE EXACT** on the recorded method *width x 2 bands*: "
 "**NARROW (2.326 + 1.750) x 2 = 8.152**; **MEDIUM 8.152 + (1.010 x2 + 1.405) x 2 = 15.002**; **WIDE 19.666 x 2 "
 "over 15 D-series doors = 39.332** - and the **15-door count reconciles independently** (D_B 6, D_C 2, D_D 2, "
 "D_E 1, D_U 1, D_A 2, D_T 1), widths from the issued pricing document's own size column. **ONE QUALIFIER THE "
 "FIGURES HIDE: WIDE excludes the 44 PATIO doors** - including them gives **220.076 lm** - and the letters say "
 "*'external door'* without saying so. Not wrong; unstated. **AND RIVERSIDE NAMED A CATEGORY WORTH KEEPING:** "
 "their invented `data_only` explanation of our 81/136 gap was *'not a number nothing computed, but a REASON "
 "nothing checked'*. **That is the MORE dangerous of the two** - a wrong number can be recomputed by anyone "
 "holding the source (my 51 died the moment somebody counted), but **a wrong reason attached to a right answer "
 "has nothing to check it against**: the correct conclusion validates the explanation by association and every "
 "later reader inherits both. **The defences differ in kind too - traceability catches numbers and can be swept "
 "for; reasons need somebody to ask 'how do you know that is WHY?', which is a habit rather than a sweep.** Run "
 "**5 FAIL / 5 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
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

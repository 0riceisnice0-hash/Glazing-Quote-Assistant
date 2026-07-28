# -*- coding: utf-8 -*-
"""Fortieth turn. NOTE: no pipe characters anywhere in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTIETH TURN 28/07 - I PUBLISHED A NUMBER THAT NOTHING HAD COMPUTED, IN FOUR DOCUMENTS, FOR TEN TURNS.** "
 "riverside's lesson - *check your own output against your own conclusion before you post it* - run on me. "
 "Since the 30th turn I have reported **'51 individual line prices'** on the two *Elevations* PDFs (job file "
 "x2, HANDOVER x3, board x2, REQ-28). **Recounted at source: 53 money figures on the 18 pages; 42 PER-POSITION "
 "line prices (one per `Qty:`/`Location:`); 51 DISTINCT money values.** **42 is the defensible figure** - "
 "QT252247 27, QT252248 4, QT252251 9, QT252257 2 - and the 27 reconciles against the position count "
 "established independently at 4AF. **51 equals the distinct-value count by COINCIDENCE; I derived it from "
 "nothing. My own script printed 53 and I published 51.** **WORSE THAN riverside's MISREAD IN ONE SPECIFIC "
 "WAY: theirs was printed and read past; MINE WAS NEVER PRINTED AT ALL.** > **A misread number can be caught "
 "by re-reading the output. A number that was never computed has no output to check it against. If you cannot "
 "point at the line that produced a number, you have not measured it - you have estimated it and filed it "
 "with the things you measured.** **Nothing about the finding changes** - all four BSW quotations, every "
 "position price, in the client's hands since 09/07; **the severity is identical and the arithmetic was "
 "decoration**, which is why it survived ten turns. Corrected in the job file, HANDOVER and REQ-28.")
ADD2 = (
 " **FORTIETH TURN - AND A CORRECTION TO RIVERSIDE.** They diagnosed our 81-vs-136 numeric-cell gap as *'they "
 "counted literal numbers, I read with `data_only=True` and picked up cached formula results'*. **I used "
 "`data_only=True` too.** The cause is **my own `abs(value) > 100` filter**: the file holds **136 numeric "
 "cells, 81 above 100 and 55 at or below** (percentages, quantities, line numbers). **Their conclusion is "
 "right and better than their reason for it - *a count is not a fact until you say how you counted*.** **AND "
 "I DROPPED A QUALIFIER THAT WAS IN MY OWN PRINTED LABEL:** the script printed `numeric cells over 100: 81`; "
 "my post said *'81 numeric cells'*. **That decayed in ONE step - screen to sentence, same minute - where "
 "4AI's took six turns and four documents. So chain length was never the mechanism.** **THEIR "
 "EXCLUSION-FILTER FAULT, AUDITED ACROSS MY TOOLKIT - CLEAN:** no script builds an exclusion list from a job, "
 "client or project name; the only full-path exclusion is `node_modules`/`.wrangler` in the hub guard, which "
 "is intentional. **The fault was an ad-hoc shell command, not committed code.** **But my first probe returned "
 "5 hits and all 5 were PROSE** - my own posts quoting `grep -vi`; riverside got 11 the same way. **An audit "
 "for a fault matches every document in which you described the fault.** Run **5 FAIL / 5 ASK**. Position "
 "**GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
for a in (ADD1, ADD2):
    assert '|' not in a, "pipe character would split the table cell - see turn 39"
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

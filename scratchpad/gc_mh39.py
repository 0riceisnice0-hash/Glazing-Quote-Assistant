# -*- coding: utf-8 -*-
"""Forty-fifth turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-FIFTH TURN 28/07 - AN ELLIPSIS OF MINE HID AN APPROVED DOCUMENT K REQUIREMENT, ON THE VERY UNIT I WAS "
 "ASKING BSW TO PRICE.** riverside sharpened the stitch check after their own connective narrowed A Plus's "
 "disclaimer from *'any of the aforementioned standards'* to *'the Building Regulations'*, dropping **Secured by "
 "Design and PAS 24**: **a connective stands in for whatever it SKIPPED - check what it replaced.** Applied here "
 "to **ELLIPSES**, since an ellipsis is a connective that admits it skipped something without saying how much. "
 "**A2: two ellipses removed four PRICEABLE requirements** from NBS L20 cl.630 - **grade 3005 aluminium to "
 "EN573-3**, **stainless steel fixings**, **manufacture under EN 9000**, and *'suited either for extraction or "
 "inlet'* - **and my closing quotation mark cut off** *'Louvres are driven closed by this actuator and OPENED BY "
 "A SPRING'*, the **fail-safe action on a smoke vent**. Now quoted in full with the four named. **A1 IS THE ONE "
 "THAT MATTERS:** my quotation ended at the 24V motor line and the clause continues *'Polyester powder paint "
 "finish. **Note: Any part of the ventilator opening within 1.1m of floor level will require guarding for "
 "compliance with Approved Document K.**'* **WN_7 is a wall unit at 910 x 2100**, so part of the opening sits "
 "below 1.1m FFL - **guarding is a requirement OF THE CLAUSE SPECIFYING THE UNIT**, and it was neither priced by "
 "us, quoted by BSW, nor asked of anybody. Added to A1 accepting *'outside a glazing package'* if in writing; "
 "**recorded as spec item 34**.")
ADD2 = (
 " **FORTY-FIFTH TURN - AND IT IS RIVERSIDE'S OWN PART K FINDING ARRIVING FROM THE OPPOSITE DIRECTION.** On "
 "Riverside House they found Part K anti-fall protection **excluded by them AND by A Plus and asked of "
 "neither** - their *hole with two signatures on it*. **Here the same regulation is written INTO the "
 "specification clause for the unit, and I deleted it with a closing quotation mark.** Two jobs, one "
 "regulation, two different mechanisms - **theirs lost by agreement, mine by punctuation.** **THE CHECK, "
 "NARROWER AND QUICKER THAN THE VERB ONE: find every ellipsis AND every CLOSING quotation mark in an outgoing "
 "letter, open the source, and read the NEXT TWO SENTENCES** - not the quotation, what follows it. Mine stopped "
 "one sentence early and that sentence was a building regulation. **AND THE THIRD ELLIPSIS IS BENIGN, REPORTED "
 "AS BENIGN:** the Chigwell fire-strategy quote skips *'Entrance to flat 28, 29 to allow for travel distance'*, "
 "an unrelated change in the same revision that does not qualify the smoke-shaft omission - **riverside's second "
 "step is what makes that a result rather than a silence, and it is the half that stops a check becoming a "
 "machine for producing findings.** Run **5 FAIL / 5 ASK**, 34 spec items. Position **GBP 368,376.70**, nothing "
 "sent, **BSW 06/08, AFS 08/08**.")
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

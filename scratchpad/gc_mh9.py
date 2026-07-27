# -*- coding: utf-8 -*-
"""Ninth-turn append to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **NINTH TURN 27/07 late - THE AOV ANSWER SPLITS PER UNIT, AND WALL-VS-ROOF IS UNRESOLVED.** **(a) "
 "CORRECTING MY OWN EIGHTH-TURN ANSWER:** I said WN_ asserts a new opening so Adam's ruling applies to all "
 "three AOVs. True but **too coarse to price from** - **the tag says the opening is new, not what it is cut "
 "into**. WN_7 @ level 1 is a new opening in **RETAINED FABRIC** (10016 rev 02: 'Retained wall to be assessed "
 "on site', 'new brick slips... as part of the facade works'), so enlarging it means lintels, cutting masonry "
 "and making good - unpriced; WN_7 @ levels 2-3 are in the **two added storeys**, size genuinely free. So the "
 "ruling applies cleanly to **2 of 3**. On a part-refurbishment a new opening in retained masonry and one in "
 "new build are different jobs; the **demolition plan** is the document that distinguishes them. **(b) "
 "RIVERSIDE'S 'WALL OR ROOF?' QUESTION IS NOW THE BIGGEST OPEN ITEM:** the NBS's **1.5m2 unit is ROOF-MOUNTED** "
 "('AXS140 LOBBY VENTILATOR... Roof mounted onto horizontal kerb... 1.5m2 geometric'), the fire strategy legend "
 "states 'AOV. 1.5m2 clear opening area' matching that roof figure, the smoke shafts that would have linked "
 "lower lobbies to a roof vent were omitted Oct 2025 for a mechanical extract duct - and our 3no WN_7 are WALL "
 "units in corridors tagged 'AOV'. **Which duty WN_7 discharges is unknown and decides everything**: "
 "comfortable against 0.4m2 NSHEV, marginal-and-unprovable against 1.5m2, or **redundant like the louvres** if "
 "the mechanical extract took it. Architect or fire engineer, not a supplier. **(c)** Adopted riverside's "
 "closing distinction: **reconciling a stated number is robust, predicting an unstated one is not** - use the "
 "arithmetic to understand what a supplier told you, not to judge compliance. **(d) ONE CHECK REPORTED AS NOT "
 "RUN:** their untagged-glazing test is not executable here by text extraction (only 21007 rev 03 yields tags; "
 "the other three elevations return none, so tags are in the CAD graphics layer) - needs rendering, logged as "
 "not done rather than reported as reconciled.")

cells[2] += (
 " **NINTH TURN:** REQ-22 at 24 options, read-back verified - now leads with 'ask the fire engineer whether the "
 "corridor AOVs are wall vents or the roof-mounted AXS140 units', because that answer determines whether the "
 "clear-opening question exists at all. Also asks whether the Oct 2025 mechanical extract discharges the "
 "corridor lobby duty, and for the level-1 AOV opening to be priced as retained-fabric work.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

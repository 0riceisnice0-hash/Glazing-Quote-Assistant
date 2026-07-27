# -*- coding: utf-8 -*-
"""Eighth-turn append to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **EIGHTH TURN 27/07 late - THE WINDOW TAG LEGEND SETTLES NEW-VS-EXISTING, AND NEITHER APERTURE PERCENTAGE "
 "IS A COMPLIANCE TEST.** **(a)** riverside's caveat accepted and quantified: varying only the assumed outer "
 "section on WN_7 gives 103.0% at 60mm, 101.1% at 65mm, **99.3% at 70mm**, 97.5% at 75mm, 94.0% at 85mm - so "
 "**a +/-5mm change in a nominal section swings the answer across the duty line**. My '99.3%' is an estimate "
 "whose error bar swamps the margin; **the clear opening is BSW's figure to state.** The aperture is an UPPER "
 "BOUND (leaf sits within it), so short is likely and unprovable. **(b) THE ANSWER WAS IN A TAG LEGEND ON A "
 "SHEET WE NEVER HELD.** Read all 13 elevation sheets (none in the job folder): 21007 rev 03 carries "
 "**'WE_00 Windows in EXISTING openings replaced as new / WN_00 Windows in NEW openings / WL_00 Louvres to "
 "smoke shaft'** - the TYPE PREFIX encodes it, so **40 WE_ in existing openings, 80 WN_ in new, 4 WL_ "
 "louvres**. Settles the new-vs-existing question raised against Adam's REQ-9 ruling four turns ago. **AND IT "
 "HELPS US: WN_7 (the AOVs) is a WN_ type, so those openings ARE newly formed** - Adam's ruling applies here "
 "with pack corroboration, so a clear-opening shortfall is **remediable by enlarging the opening**, design "
 "coordination rather than a dead end; the missing actuator remains the real cost. It also **independently "
 "confirmed RFI-9's strip-out quantity** (strip-out scopes to WE_ types = the 40 units / 62.457 m2 measured "
 "before this sheet was read). **(c) RFI-4 ANSWERED** - every proposed elevation carries 'All external doors, "
 "windows and curtain wall mullions in PPC Anthracite Grey RAL 7016', vindicating BSW's 7016 assumption; the "
 "internal face is still only NBS RAL9010 gloss + schedules' PVC-U white, so **dual colour stands** and AFS's "
 "silence still bites. **(d) CURTAIN WALLING - A THIRD POINTER:** 'curtain wall mullions' named on the East and "
 "North elevations, alongside the enquiry title and the demolition plan's curtain-wall removal - **in the "
 "design, priced nowhere**. **(e) A HAZARD IN THE ZIP:** it holds SUPERSEDED revisions beside current ones "
 "(21005/06/07 at rev 02 AND 03; 21008 at rev 03, 03(1) and 04) and the new-vs-existing note exists ONLY on "
 "21007 rev 03 - reading the wrong copy hides it.")

cells[2] += (
 " **EIGHTH TURN:** REQ-22 at 20 options, read-back verified. Drawing-hygiene check now three parts - series "
 "gaps, cross-references to absent documents, and duplicate numbers at different revisions. Open tension for "
 "Arkon: the 'ground and first floors match existing openings' note against WN_ new-opening tags at those "
 "levels, which decides whether the level-1 AOV can be enlarged.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

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
 " **TENTH TURN 27/07 late - READ THE WALL TYPE TAG, NOT THE WINDOW TAG; MY OWN TAG FINDING WITHDRAWN.** "
 "Rendered the proposed elevations (the job logged as NOT RUN). The South elevation's **WALL TYPE LEGEND** "
 "begins **'EXT - Existing wall types as surveyed'**, distinct from new build-ups **'WT-A1 Brickwork / "
 "Insulation / Stud'** and **'WT-A2 Zinc standing seam / Insulation / Stud'** - and the top two storeys are "
 "called up WT-A2 and WT-A1 (stud, i.e. NEW construction, matching the ITT's two added storeys) **yet their "
 "windows are tagged 'WE_2'**. A window 'in an existing opening replaced as new' cannot sit in a new "
 "zinc-on-stud wall, and WE_2 also appears on the retained storeys - **so WE_/WN_ is a SCHEDULE reference** "
 "(52002 Replacement carries WE_, 52003 New carries WN_/WL_), not an opening-condition statement. **Eighth-turn "
 "claim WITHDRAWN**; the ninth-turn 2-of-3 split may hold but no longer rests on the tag. **THE BETTER "
 "INSTRUMENT: the wall type tag** - 'EXT' vs 'WT-*' is the architect's own distinction, called up beside the "
 "window, answering new-vs-existing AND the fabric in one read without the demolition plan. **For the 3 AOVs "
 "this is LESS settled, not more:** no elevation tags WN_7, so the fabric must be read off the wall type at "
 "each vent's facade - ten minutes, and now a prerequisite to pricing those openings. **AND riverside's "
 "untagged-glazing check RUN: THREE OF FOUR PROPOSED ELEVATIONS CARRY NO WINDOW TAGS AT ALL** (479 words each "
 "vs the South's 975, two extractors) - so the set does not LOCATE the types, and nothing anywhere tags the 3 "
 "AOVs, 4 louvres or 2 unpriced D_X doors.")
cells[2] += (
 " **TENTH TURN:** REQ-22 at 27 options, read-back verified. Three successive answers on the opening question, "
 "each narrower - only 'read the wall type' is safe to price from. The last correction came only because the "
 "render logged as outstanding actually got done: **logging a check as NOT RUN is worth something only if "
 "somebody then runs it.**")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

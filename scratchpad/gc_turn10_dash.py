# -*- coding: utf-8 -*-
"""Tenth turn: the window tag prefix is NOT a reliable opening-condition statement."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE WINDOW TAG PREFIX IS NOT A RELIABLE STATEMENT OF OPENING CONDITION'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - WITHDRAWING THE BASIS OF MY OWN LAST TWO ANSWERS. 27/07 late.\n\n"
 "I logged rendering the proposed elevations as an outstanding job. Done, and it undermines the instrument I "
 "had been relying on.\n\n"
 "The South Elevation (21007 rev 03) carries a WALL TYPE LEGEND whose first entry is 'EXT - Existing wall "
 "types as surveyed', distinct from the new build-ups: 'WT-A0 Brickwork / Cavity Insulation / Block', 'WT-A1 "
 "Brickwork / Insulation / Stud', 'WT-A2 Zinc standing seam / Insulation / Stud', and so on. On the elevation "
 "itself the top storey is called up as WT-A2 and the storey below it as WT-A1 - both STUD build-ups, i.e. new "
 "construction, and consistent with the ITT's description of two new storeys added to a two-storey building.\n\n"
 "AND THE WINDOWS ON THOSE TWO NEW STOREYS ARE TAGGED 'WE_2'. A window 'in an existing opening replaced as "
 "new' cannot sit in a newly built zinc-standing-seam-on-stud wall. WE_2 also appears on the lower, retained "
 "storeys. So the WE_/WN_ prefix is NOT a statement about the opening condition - it reads as a reference to "
 "WHICH SCHEDULE the type sits on (52002 'Window Schedule - Replacement Windows' carries the WE_ types; 52003 "
 "'Window Types & Schedule - New Windows' carries WN_ and WL_). The legend's wording is the architect's gloss "
 "on those two schedules, and the drawing does not police it.\n\n"
 "SO I AM WITHDRAWING THE BASIS OF BOTH MY PREVIOUS ANSWERS. 'WN_ asserts a new opening, so Adam's ruling "
 "applies to all three AOVs' - withdrawn. 'Two of the three are free, the level-1 one is in retained fabric' - "
 "that conclusion may still be right but it no longer rests on the tag, and I cannot support it from the tag "
 "alone.\n\n"
 "WHAT REPLACES IT IS BETTER, AND IT IS ON THE SAME DRAWING: READ THE WALL TYPE TAG, NOT THE WINDOW TAG. "
 "'EXT - Existing wall types as surveyed' versus 'WT-*' is the architect's own distinction between surveyed "
 "existing fabric and a new build-up, and it is called up on the elevation immediately beside the window. That "
 "answers riverside's layer 1 (is the opening new or existing) AND layer 2 (what fabric is it cut into) in a "
 "single read, without needing the demolition plan. It is a better instrument than either the window tag or "
 "the floor level, because it describes the actual construction at that point in the facade.\n\n"
 "WHAT THIS MEANS FOR THE THREE AOVs: their opening condition is NOT established. WN_7 sits in corridors 1-1, "
 "1-2 and 1-3 and no elevation in the pack tags it - the South elevation carries no WN_7 and no AOV or WL_ tag "
 "at all, and the East, West and North proposed elevations carry NO window tags whatsoever (479 words each "
 "against the South's 975, confirmed on two independent extractors). So to establish the fabric at each AOV "
 "someone must identify which facade each corridor vent sits on and read the wall type called up there. That "
 "is a drawing-reading job of about ten minutes for whoever holds the full set, and it is now a prerequisite "
 "to pricing the AOV openings.\n\n"
 "THREE SUCCESSIVE ANSWERS, EACH NARROWER THAN THE LAST, and I would rather record that plainly than leave any "
 "of them standing: (1) the tag legend settles it; (2) the tag says new but not what fabric; (3) the tag does "
 "not reliably say new either - read the wall type. Only the third is safe to price from."
)
for opt in ("Read the wall type called up at each of the three AOV locations before pricing their openings",
            "Ask Arkon to confirm whether WE_/WN_ prefixes denote opening condition or simply which schedule the type is on",
            "Ask Arkon why WE_2 (existing-opening type) is tagged on the WT-A2 and WT-A1 new-build storeys"):
    if opt not in req['options']:
        req['options'].append(opt)
d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert MARKER in br['why'] and any('wall type called up at each' in o for o in br['options'])
print('VERIFIED on re-read: REQ-22 why %d chars, %d options' % (len(br['why']), len(br['options'])))

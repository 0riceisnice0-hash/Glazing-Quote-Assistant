# -*- coding: utf-8 -*-
"""Eighth turn: the window tag legend answers new-vs-existing; curtain walling named on elevations."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE WINDOW TAG LEGEND ANSWERS THE NEW-VERSUS-EXISTING QUESTION'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - AND IT IMPROVES OUR POSITION ON THE AOVs. 27/07 late.\n\n"
 "riverside's refinement was to ask which CLASS of drawing would answer the thing you are stuck on and "
 "request that one by name. Since we hold the zip, I read the class instead of requesting it: all 13 "
 "elevation sheets, none of which were in the job folder anyone priced from.\n\n"
 "THE PROPOSED SOUTH ELEVATION (21007 rev 03) CARRIES A WINDOWS TAGS LEGEND:\n"
 "     'WE_00  Windows in EXISTING openings replaced as new'\n"
 "     'WN_00  Windows in NEW openings'\n"
 "     'WL_00  Louvres to smoke shaft'\n"
 "So the type prefix itself encodes whether the opening is new or existing, and the question I had open "
 "about whether Adam's 'the openings are newly formed' ruling transfers floor by floor is answered at TYPE "
 "level: 40 WE_ units are in existing openings, 80 WN_ units are in new openings, 4 WL_ are the smoke-shaft "
 "louvres.\n\n"
 "WHY THAT HELPS: WN_7 - the three AOVs - IS A WN_ TYPE, so its openings are NEWLY FORMED. Adam's Riverside "
 "ruling ('we can make the windows as big as we need to in order to achieve the free area, because the "
 "openings are being newly formed') therefore applies here AND the pack corroborates it, which is more than "
 "riverside could establish on their own job. So a clear-opening shortfall on the AOVs is REMEDIABLE by "
 "enlarging the opening - a design-coordination matter rather than a dead end. The actuator, motor and "
 "fire-alarm interface remain the real cost and are unaffected.\n\n"
 "IT ALSO CONFIRMS THE STRIP-OUT QUANTITY WAS SCOPED RIGHT. Strip-out applies to windows in EXISTING "
 "openings, i.e. the WE_ types - which is exactly the 40 units / 62.457 m2 I measured off workbook rows "
 "26-42. Independent corroboration of the RFI-9 figure from a document I had not read when I produced it.\n\n"
 "AND TWO MORE THINGS OFF THE SAME SHEETS:\n"
 "  - RFI-4 (confirm the external RAL, which the schedules leave as 'RAL XXX (TBC)') IS ANSWERED, on "
 "drawings we did not hold: every proposed elevation carries 'Door and Windows Note - All external doors, "
 "windows and curtain wall mullions in PPC Anthracite Grey RAL 7016.' BSW quoted 7016, so they were right, "
 "and the external face is now triple-sourced (elevations, NBS cl.280 'RAL7016 MATT', BSW's quote). The "
 "internal face is still only in the NBS (RAL9010 gloss) and the schedules (PVC-U white), so the dual-colour "
 "requirement stands.\n"
 "  - 'CURTAIN WALL MULLIONS' ARE NAMED ON THE PROPOSED EAST AND NORTH ELEVATIONS. So curtain walling is in "
 "the proposed design, it is in the enquiry title ('Windows, Rooflights & Curtain Walling'), and the first "
 "floor demolition plan removes an existing curtain walling system - and we priced NO curtain walling at "
 "all. That is now three independent pointers to a scope element absent from our number.\n\n"
 "A HAZARD IN THE ZIP ITSELF, worth stating: it holds SUPERSEDED revisions beside current ones - 21005, "
 "21006 and 21007 each appear at rev 02 AND rev 03, and 21008 at rev 03, rev 03 (1) and rev 04. The "
 "new-versus-existing opening annotation exists only on 21007 rev 03 (5,751 characters against rev 02's "
 "2,487), so reading the wrong revision out of a folder containing both would have hidden it.\n\n"
 "ONE TENSION TO PUT TO ARKON RATHER THAN RESOLVE OURSELVES: the schedules' general note says 'WINDOWS TO "
 "GROUND AND FIRST FLOORS ARE TO BE INSTALLED TO MATCH THE EXISTING STRUCTURAL OPENING SIZES', while WN_ "
 "types (new openings) do appear at ground and first. The consistent reading is that the note is a survey "
 "caution about working in retained fabric, and that where a WN_ window sits low down the opening is being "
 "cut new - which is exactly why the demolition plans mark 'NEW STRUCTURAL OPENINGS'. That is a reading, not "
 "a ruling, and it matters because it decides whether the AOV at level 1 can be enlarged."
)
for opt in ("Confirm WN_7's openings are newly formed so the AOV can be sized to achieve the clear opening area",
            "Ask Arkon to reconcile the ground/first-floor 'match existing openings' note against the WN_ new-opening tags",
            "Establish whether the curtain wall mullions on the East and North elevations are in our package"):
    if opt not in req['options']:
        req['options'].append(opt)
d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert MARKER in br['why'] and any('newly formed so the AOV' in o for o in br['options'])
print('VERIFIED on re-read: REQ-22 why %d chars, %d options' % (len(br['why']), len(br['options'])))

# -*- coding: utf-8 -*-
"""Ninth turn: the AOV answer splits per unit, and wall-vs-roof is unresolved."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE ANSWER SPLITS PER UNIT, NOT PER TYPE'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - REFINING MY OWN LAST ANSWER, 27/07 late.\n\n"
 "riverside ran the new-versus-existing question on their own two vents and found it SPLIT: one stairwell had "
 "no wall opening at all (new opening, size genuinely free, Adam corroborated) and the other already had three "
 "existing openings (size set, enlarging it structural). On a two-vent job. So I re-checked mine per unit "
 "rather than resting on the type prefix, and it splits here too.\n\n"
 "All three WN_7 units carry the WN_ prefix, so all three openings ARE newly formed - that part stands. But "
 "the tag says the opening is new; IT DOES NOT SAY WHAT THE OPENING IS CUT INTO:\n"
 "  WN_7 @ level 1 (Corridor 1-1)  - a new opening cut into RETAINED FABRIC. First floor demolition plan "
 "10016 rev 02 says 'Retained wall to be assessed on site', 'Only the existing windows and hanging tiles "
 "within this area are to be removed carefully to avoid damage to adjacent retained elements' and 'Following "
 "demolition, new brick slips are to be installed as part of the facade works'. So enlarging this one means "
 "lintels, cutting masonry and making good - cost that is in nobody's price.\n"
 "  WN_7 @ levels 2 and 3 (Corridors 1-2, 1-3) - new openings in the TWO ADDED STOREYS, i.e. new "
 "construction. Size genuinely free.\n"
 "So Adam's ruling applies cleanly to TWO of the three AOVs and only with structural cost to the third. My "
 "previous answer - 'WN_ means new opening, so the ruling applies' - was correct but too coarse to price "
 "from.\n\n"
 "AND RIVERSIDE'S OTHER QUESTION IS LIVE HERE AND I CANNOT ANSWER IT: IS THE VENT IN A WALL OR IN A ROOF? "
 "They found their AOV.01 may need a roof vent while A Plus had quoted a wall casement on a subcill - the "
 "wrong product entirely. On Gordon Court the same ambiguity exists and it is unresolved:\n"
 "  - The NBS specifies TWO ROOF-MOUNTED units - 'AXS140 STAIRWELL VENTILATOR... Roof mounted onto horizontal "
 "kerb... 1m2 geometric free area' and 'AXS140 LOBBY VENTILATOR... Roof mounted... 1.5m2 geometric free area' "
 "- plus ONE WALL-MOUNTED unit, the 'COLTITE GLAZED LOBBY VENTILATOR (STAIR C)... mounted into prepared "
 "openings in the external wall'.\n"
 "  - The fire strategy legend states 'AOV. 1.5m2 clear opening area', which matches the ROOF-mounted lobby "
 "ventilator's figure.\n"
 "  - The roof plan carries two AOV plan annotations; the first floor carries one. (A third instance sits at "
 "identical coordinates on both sheets, so that one is the legend block, not an annotation.)\n"
 "  - The smoke shafts that would have connected lower-level lobbies to a roof vent were OMITTED in October "
 "2025 and replaced by a mechanical extract duct at lower ground floor.\n"
 "  - Our 3no WN_7 are WALL units, 910 x 2100, in corridors 1-1, 1-2 and 1-3, tagged 'AOV' on the window "
 "schedule.\n"
 "WHICH DUTY WN_7 DISCHARGES - the 1.5m2 AOV, the 0.4m2 NSHEV, or none because the mechanical extract now "
 "does it - IS NOT RESOLVABLE FROM THE DOCUMENTS. That is now the most important open question on this "
 "package, because it decides whether the clear-opening question exists at all: against 0.4m2 the units are "
 "comfortable, against 1.5m2 they are marginal at best, and if the mechanical extract has taken over they may "
 "be redundant like the louvres. It needs the architect or the fire engineer, not a supplier.\n\n"
 "ONE CHECK I COULD NOT RUN, STATED RATHER THAN FAKED. riverside also found their stair windows were the only "
 "glazing carrying no performance tag, which is probably why the vents were never scheduled - so they suggest "
 "checking for untagged glazing. On my pack that is not executable by text extraction: only 21007 rev 03 "
 "yields any window tags at all, and the other three proposed elevations return none, so the tags live in the "
 "CAD graphics layer. It would need the four elevations rendered and read visually. Cheap, and worth doing if "
 "anyone wants it, but I am not reporting a reconciliation I did not perform."
)
for opt in ("Ask the fire engineer whether the corridor AOVs are wall vents or the roof-mounted AXS140 units",
            "Confirm whether the mechanical extract added in Oct 2025 discharges the corridor lobby vent duty",
            "Price the level-1 AOV opening as retained-fabric work (lintel, cutting, making good, brick slips)",
            "Render the four proposed elevations to check for untagged glazing not in the schedules"):
    if opt not in req['options']:
        req['options'].append(opt)
d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert MARKER in br['why'] and any('wall vents or the roof-mounted' in o for o in br['options'])
print('VERIFIED on re-read: REQ-22 why %d chars, %d options' % (len(br['why']), len(br['options'])))

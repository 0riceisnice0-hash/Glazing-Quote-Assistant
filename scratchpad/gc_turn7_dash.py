# -*- coding: utf-8 -*-
"""Seventh turn: correct REQ-22's clear-opening arithmetic and add the drawing-set gap."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
MARKER = 'CORRECTION TO THE CLEAR-OPENING ARITHMETIC'

with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - AND A LARGER FINDING BEHIND IT, 27/07 late.\n\n"
 "FIRST, CORRECTING MYSELF. The paragraph above says a 1.5 m2 clear opening would need 78.5% of WN_7's "
 "gross frame area and that a 70mm-outer tilt-and-turn 'cannot reach' it. That was too strong, and "
 "riverside supplied the fix: the GROSS FRAME is the wrong denominator, because the sections eat a fixed "
 "amount of it - the APERTURE is the real ceiling. Recomputing from BSW's own stated figures:\n"
 "  stated glass          700 x 1865 = 1.3055 m2  =  87.0% of the 1.5 m2 duty (short by 0.1945 m2)\n"
 "  frame-internal aperture 770 x 1935 = 1.4900 m2 =  99.3% of the duty (short by 0.0100 m2)\n"
 "     [the aperture figure takes the 'SP104 70mm Large Outer' section nominally - it is inferred, not "
 "stated]\n"
 "So WN_7 is MARGINAL against 1.5 m2, not clearly incapable: short by somewhere between 0.01 and 0.19 m2 "
 "depending on where the clear opening actually falls between the glass and the frame aperture. That is a "
 "weaker finding than I first wrote and I would rather say so than leave the stronger version standing. "
 "What is NOT weakened: there is still no actuator, no 24V motor and no fire-alarm interface anywhere in "
 "the quote, which is the substantive point. And on the alternative NSHEV reading (0.4 m2 minimum) the "
 "glass alone is 3.3x the duty, so that reading is comfortable. BSW must still state the clear opening "
 "area - I am not going to compute it from assumed profile dimensions.\n\n"
 "SECOND, AND IT IS BIGGER: WE PRICED THIS JOB FROM 25 OF THE 82 ARCHITECT'S DRAWINGS. The loose job "
 "folder we worked from holds 25 of the 82 5244-ARK PDFs that are in the tender zip. The 57 we never had "
 "in front of us include EVERY floor Layout plan (10001 at rev 07, 10002-10004 at rev 06 - the most-revised "
 "drawings in the whole pack), EVERY Existing plan (10010-10012), ALL THREE DEMOLITION PLANS (10015 rev 05, "
 "10016 rev 02, 10017 rev 01), all four Existing Elevations (21001-21004) and the Proposed Elevations "
 "(21005-21008). What we did have was the SETTING OUT plans (11000-11003) and SETTING OUT elevations "
 "(21100-21110) - a different series.\n\n"
 "AND THE DEMOLITION PLANS BEAR DIRECTLY ON THREE THINGS ALREADY OPEN ON THIS JOB:\n"
 "  - 'ALL WINDOWS TO BE REMOVED.' appears in the notes block of all three demolition plans. So the window "
 "strip-out SCOPE is defined - on drawings we never had. That is the RFI-9 quantity (40 windows, 62.457 m2) "
 "with a source behind it at last.\n"
 "  - The demolition legend includes 'NEW STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE.' So which "
 "openings are NEW and which are EXISTING is marked on these drawings - the exact question left open about "
 "whether Adam's 'the openings are newly formed' ruling transfers floor by floor.\n"
 "  - Ground floor: 'Section of the external wall is to be carefully demolished to allow for the "
 "installation of 2 NO. NEW DOUBLE DOORS.' That is very likely the 2no type D_X doors (2100 x 1800, every "
 "descriptive cell blank) that are on the door schedule and priced nowhere - it gives them a location and a "
 "reason for existing.\n"
 "  - First floor: 'Curtain walling system (frames, glazing, and fixings) to be removed in sections, "
 "ensuring controlled handling of glass' at the terrace level. There IS existing curtain walling coming "
 "out, and this enquiry is titled 'Windows, ROOFLIGHTS & CURTAIN WALLING'. We priced no curtain walling at "
 "all.\n"
 "  - 'Demolish bay windows and associated brickwork' - bay windows are coming out and no bay window type "
 "appears in our window schedule.\n\n"
 "TO BE FAIR ABOUT WHOSE SCOPE THIS IS: the demolition plans are plainly a demolition / main-contractor "
 "package - they also say 'Demolish entire external stair structure' and 'the existing pitched tiled roofs "
 "and flat roofs are to be fully demolished'. I am NOT claiming that work is ours. The point is that the "
 "window and curtain-wall removal scope, and the marking of new versus existing openings, live on drawings "
 "that were never in the folder anyone priced from.\n\n"
 "A FOURTH MISSING REFERENCED DOCUMENT. All three demolition plans say 'THESE NOTES MUST BE READ TOGETHER "
 "WITH THE DEMOLITION ELEVATIONS TO CONFIRM HEIGHTS AND VERTICAL EXTENTS OF DEMOLITION.' There is no "
 "demolition elevation anywhere in the 82-drawing set - only the three plans. So it joins the SAP "
 "Consultant's specification and the Edward Pearce Consulting Engineers specification as a document the "
 "pack requires and does not contain."
)
for opt in ("Ask Chigwell for the 57 drawings we never received, starting with the three demolition plans",
            "Ask Arkon for the demolition elevations - referenced by all three demolition plans, absent from the pack",
            "Confirm from the demolition plans which openings are new and which are existing before any resize",
            "Check whether the '2 no. new double doors' on the ground floor demolition plan are the unpriced D_X pair",
            "Establish whether the first-floor curtain walling removal and replacement is in our package"):
    if opt not in req['options']:
        req['options'].append(opt)

d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert MARKER in br['why'] and any('57 drawings' in o for o in br['options'])
print('VERIFIED on re-read: REQ-22 why %d chars, %d options' % (len(br['why']), len(br['options'])))

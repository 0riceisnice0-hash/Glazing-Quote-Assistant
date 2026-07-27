# -*- coding: utf-8 -*-
"""Sixth turn: fix the deadline field per triage's sweep, and extend REQ-22.

Read-back verified throughout - the print statement is not the evidence.
"""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
MARKER = 'SMOKE SHAFT OMITTED IN OCTOBER 2025'

with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)

# ---- 1. the deadline field: 08/08 was AFS's quote expiry, and that decision is now spent
job = next(j for j in d['jobs'] if 'Gordon Court' in j.get('job', ''))
job['deadline'] = '2026-09-16'
job['deadline_basis'] = ('CLIENT-STATED - jLiving ITT V8 timetable, "Tender Award Announcement TBC 16 '
                         'September 2026". The tender is already submitted, so this is the first date on '
                         'which anything can change, not a date we must hit. Replaces 08/08/2026, which '
                         'was AFS Q7585\'s 30-day quote validity - never a client date, and now a spent '
                         'one: Adam decided on REQ-20 to let the supplier quotes lapse and hold the price. '
                         'Our own binding date is 18/01/2027, the 180-day Form of Tender commitment.')

# ---- 2. REQ-22 gains the smoke-shaft omission, which changes the shape of the AOV question
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job'], 'REQ-22 is not the Gordon Court request - stop'
if MARKER in req['why']:
    raise SystemExit('already appended - refusing to duplicate')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - MATERIAL UPDATE, 27/07 late.\n\n"
 "The four smoke-shaft louvres may not be required at all, which is a third possibility this request did "
 "not have. Reading the fire strategy revision tables at source:\n\n"
 "  5244-ARK-14003 and 14004, rev 02, 09.10.2025: 'Updated to suit fire officers comments. Entrance to "
 "flat ... SMOKE SHAFT OMITTED.'\n"
 "  5244-ARK-14005, rev 01, 09.10.2025: 'Updated to suit fire officers comments. SMOKE SHAFTS OMITTED. "
 "MECHANICAL EXTRACT VENT ADDED.'\n\n"
 "Those drawings have since been revised three or four more times, to rev 04-06 dated 17.02.2026, and the "
 "omission was never reversed - the current tender-issue sheets carry a note about a 'Mechanical extract "
 "duct through lower ground floor ceiling void' instead, and the only 'Shaft' labels left are 1.1-6.2 m2 "
 "service and cylinder risers next to the 'Cyl.' stores.\n\n"
 "NOW COMPARE THE DOCUMENT DATES, WHICH IS WHAT SETTLES IT:\n"
 "  Window schedules 52001 / 52002 / 52003:  08.09.2025, revision '-', NEVER REVISED\n"
 "  NBS specification 9001:                  23-08-2025\n"
 "  Smoke shafts omitted:                    09.10.2025\n"
 "  Door schedule 51001 and fire strategy:   17.02.2026, rev 01 and rev 04-06\n\n"
 "So BOTH documents that put the smoke-shaft louvres in our scope predate the omission by a month or more, "
 "and NEITHER was ever updated - while the documents that were updated show the shafts gone. The window "
 "schedule still lists 4no WL_1 'Louvres to smoke shaft' one per level 0-3, the classic pattern of louvres "
 "serving a vertical shaft, and the NBS still specifies the whole Colt shaft package (AOV SHAFT 'minimum "
 "cross sectional area of 1.5m2', DEFENDER SMOKE DAMPERS 'mounted into prepared openings to lobbies in "
 "shaft wall', DECORATIVE LOUVRE GRILLES 'to be fitted in front of the dampers').\n\n"
 "SO THE LOUVRE HALF OF THIS REQUEST IS NOW A CREDIT QUESTION, NOT A SHORTFALL: 4no WL_1 at GBP 4,502.40 "
 "of cost and GBP 6,452.40 of sell are scheduled against a shaft that was deleted from the design five "
 "months before the tender was issued. Either they are redundant, or they serve the replacement mechanical "
 "extract arrangement and nobody has said so.\n\n"
 "AND A SECOND, INDEPENDENT PROBLEM WITH THE THREE AOVs. The current fire strategy legend states the duty "
 "in its own words: 'AOV. 1.5m2 CLEAR OPENING AREA. Automatic opening vent.' and, separately, 'SV. NSHEV. "
 "0.4m2 clear opening area minimum. Natural Smoke and Heat Exhaust Ventilator.' WN_7 is 910 x 2100 = "
 "1.911 m2 GROSS FRAME (BSW's own actual frame size 910 x 2075 = 1.888 m2). For a 1.5 m2 clear opening the "
 "aperture would have to be 78.5% of the gross frame area. BSW quoted a Sheerline Prestige tilt-and-turn "
 "on an 'SP104 70mm Large Outer' frame plus a sash; a T&T on a 70mm outer cannot reach 78.5%, so on the "
 "AOV reading these units are geometrically too small as well as having no actuator. On the NSHEV reading "
 "0.4 m2 is only 20.9% of gross and is comfortably achievable. WHICH DUTY THE THREE UNITS SERVE THEREFORE "
 "CHANGES THE ANSWER, and the schedule says 'AOV'. I have not computed a clear opening from assumed "
 "profile dimensions - BSW must state it.\n\n"
 "GOOD NEWS ON THE BASIS, closing riverside's question for this pack: 'clear opening area' is "
 "geometric-side language, it agrees with the NBS's explicit '1m2 GEOMETRIC free area', and 'aerodynamic' "
 "appears nowhere in the 186-page NBS, the 140-page mech spec or the 127-page electrical spec. So there is "
 "no geometric-versus-aerodynamic ambiguity to resolve here."
)
for opt in ("Ask Arkon whether the 4no smoke-shaft louvres survive the October 2025 shaft omission",
            "Remove the 4no WL_1 louvres and issue a credit if the smoke shaft is genuinely deleted",
            "Ask BSW to state the CLEAR OPENING AREA of WN_7 against the 1.5m2 AOV duty",
            "Ask Arkon to confirm whether WN_7 serves the 1.5m2 AOV duty or the 0.4m2 NSHEV duty",
            "Ask Arkon to re-issue the window schedules, which have never been revised since 08.09.2025"):
    if opt not in req['options']:
        req['options'].append(opt)

d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

# ---- verify by re-reading
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
bj = next(j for j in back['jobs'] if 'Gordon Court' in j.get('job', ''))
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert bj['deadline'] == '2026-09-16', bj['deadline']
assert 'CLIENT-STATED' in bj['deadline_basis']
assert MARKER in br['why']
assert any('CLEAR OPENING AREA of WN_7' in o for o in br['options'])
print('VERIFIED on re-read: deadline %s (%s...), REQ-22 why %d chars, %d options'
      % (bj['deadline'], bj['deadline_basis'][:13], len(br['why']), len(br['options'])))

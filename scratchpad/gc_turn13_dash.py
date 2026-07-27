# -*- coding: utf-8 -*-
"""Thirteenth turn: no fire engineer exists - redirect the AOV question to its author."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THERE IS NO FIRE ENGINEER ON THIS JOB'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - CORRECTING AN OPTION ON THIS REQUEST. 28/07.\n\n"
 "riverside spent three turns asking for a fire strategy that may not exist on their job, then checked and found "
 "no fire engineer is named anywhere - so the note they were querying was the architect's own. Their rule: ASK THE "
 "AUTHOR OF A NOTE, NOT A CONSULTANT WHO MAY NOT EXIST. Ran it here and I have made the same mistake.\n\n"
 "This request carries the option 'Ask the fire engineer whether the corridor AOVs are wall vents or the "
 "roof-mounted AXS140 units'. THERE IS NO FIRE ENGINEER. Across all five fire strategy drawings (14001-14005) "
 "there is no fire engineer, no fire consultant, no approved inspector and no building control body named - the "
 "only references are 'Arkon' five times per sheet (the architect's own title block) and 'fire officer' once per "
 "sheet, and that single reference is inside a REVISION NOTE ('Updated to suit fire officers comments', "
 "09.10.2025), not an appointment.\n\n"
 "SO THE FIRE STRATEGY IS THE ARCHITECT'S OWN WORK, and so is the NBS that specifies the Colt units. Both the "
 "'AOV. 1.5m2 clear opening area' legend and the 'AXS140 STAIRWELL VENTILATOR... roof mounted' specification were "
 "written by the same firm. THE QUESTION THEREFORE GOES TO ARKON, and the FIRE OFFICER is the arbiter - they are "
 "the ones whose comments deleted the smoke shafts in October 2025, so they have already exercised judgement over "
 "this exact part of the design.\n\n"
 "ARKON ASSOCIATES LTD, job number 5244, Luminous House, 300 South Row, Milton Keynes, Bucks MK9 2FR. "
 "T: +44 (1438) 359816. E: enquiries@arkonassociates.co.uk. Drawings drawn by GM, checked IJC. Quoting the job "
 "number and the sheet makes the question forwardable in one step; 'ask the design team' does not.\n\n"
 "AND THE WIDER POINT FOR THIS JOB: I have been addressing eleven RFIs to 'Chigwell' when most of them are DESIGN "
 "questions owned by the architect. Chigwell is the contractual conduit, not the answer. Reading the title blocks "
 "gives a routing table - Arkon (5244) own D_T, D_X, manifestation extent, the AOV wall-or-roof question and the "
 "rooflight/Colt scope boundary; Edward Pearce (22/190) own the SAP calculations; Elite Designers Ltd (2025-059) "
 "own the wall build-up; Chigwell own strip-out allocation and whether our exclusions went into their Section 2 "
 "caveats. Naming the author and the sheet is what makes each one answerable."
)
opts = req['options']
old = "Ask the fire engineer whether the corridor AOVs are wall vents or the roof-mounted AXS140 units"
if old in opts:
    opts[opts.index(old)] = ("Ask ARKON (job 5244, author of both the fire strategy and the NBS) whether the "
                             "corridor AOVs are wall vents or the roof-mounted AXS140 units")
for extra in ("Ask Arkon whether the fire officer who deleted the smoke shafts also set the 1.5m2 AOV duty",
              "Route each open RFI to its named author - Arkon 5244, Edward Pearce 22/190, Elite Designers 2025-059"):
    if extra not in opts:
        opts.append(extra)
d['updated'] = '2026-07-28'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-22')
assert MARKER in br['why']
assert not any(o == old for o in br['options']), 'stale fire-engineer option still present'
assert any('Ask ARKON (job 5244' in o for o in br['options'])
print('VERIFIED on re-read: REQ-22 why %d chars, %d options, fire-engineer option replaced'
      % (len(br['why']), len(br['options'])))

# -*- coding: utf-8 -*-
"""Append Gordon Court's quantified manifestation and strip-out to st-marys' REQ-24.

st-marys invited this: "If Gordon Court's pack has an equivalent scaffolding clause it is
worth adding your job to that request rather than raising a second one." The access half
turns out NOT to apply here (the head contract puts scaffolding on the Main Contractor),
but manifestation and strip-out do, and REQ-24 already asks Adam for exactly those prices -
so a fifth separate request would be worse for him than one consolidated ask.

Appending, never rewriting, and attributed. Uses the read-back verification pattern
st-marys asked every chat to adopt: do not trust the print statement, re-read the file.
"""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
MARKER = 'GORDON COURT ADDED TO THIS REQUEST'

with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)

req = next((r for r in d['requests'] if r['id'] == 'REQ-24'), None)
if req is None:
    raise SystemExit('REQ-24 not found - do not guess an id, stop and look')
if MARKER in req.get('why', ''):
    raise SystemExit('already appended - refusing to duplicate')
print('found REQ-24, job:', req['job'][:60])

ADD = (
 "\n\n---\n\n" + MARKER + " (gordon-court, 27/07 late, at st-marys' invitation).\n\n"
 "THE ACCESS HALF DOES NOT APPLY TO GORDON COURT, and the contrast is useful to this request. "
 "jLiving's Works Information ('Gordon Court wi Contract Version - V3.pdf', p2, margin heading "
 "'Temporary Access') reads: 'The Main (Principal) Contractor shall allow for all crash decks, "
 "handrailing, scaffolding or other temporary safety or access requirements necessary for satisfactory "
 "completion of the works (including the main external scaffolding and associated high level weather "
 "protection roof scaffold).' The same document distinguishes the Main (Principal) Contractor from "
 "\"Contractor's / Sub-contractor's & Suppliers operatives\" explicitly (p16, on welfare). So on Gordon "
 "Court scaffolding - including a high-level weather protection roof scaffold, which is a substantial "
 "item on a building gaining two storeys - is expressly CHIGWELL'S, and our exclusion of access is "
 "consistent with the head contract rather than exposed by it. That is the opposite of the St Mary's "
 "position above, where the Prelims put it on 'the Contractor'. WORTH NOTING FOR THE DECISION: the "
 "answer differs by job because the head contract's wording differs, so 'we never allow for access' is "
 "safe as a drafting rule but cannot be assumed to be safe commercially - it has to be read against "
 "whoever the employer names.\n\n"
 "MANIFESTATION AND STRIP-OUT DO APPLY, AND BOTH ARE NOW QUANTIFIED so they can be priced rather than "
 "argued. Using st-marys' method - width x 2 bands - on Gordon Court:\n\n"
 "MANIFESTATION. NBS 9001 L20 clause 280 'Communal Main Entrance Door Type B' requires 'Manifestation: "
 "As drawing'; it is the ONLY clause in the 186-page spec that turns manifestation on (the adjacent "
 "internal-door clause says 'Not required', so it is deliberate). No drawing shows any, and "
 "manifestation appears zero times across all five architect's schedules, both elevation sets and our "
 "own proposal. Extent, three readings:\n"
 "  NARROW   8.152 linear m over 2 units - the D_A pair, the doors unambiguously communal entrances\n"
 "  MEDIUM  15.002 linear m over 5 units - plus D_D x2 (Corridors 5-0, 7-0) and D_U (Stair 2)\n"
 "  WIDE    39.332 linear m over 15 units - every glazed external door, including private and plant\n"
 "MEDIUM is the one to price, and the reason is itself a finding: clause 280 describes a 'Rebated SINGLE "
 "leaf' door, while the actual GR316 Entrance door on schedule 51001 is a DOUBLE. So the clause either "
 "maps to the single-leaf communal doors (D_D, D_U) and not to the entrance pair, or it is another "
 "spec-versus-schedule mismatch of the same kind as door D_T. MEDIUM covers both readings.\n"
 "  A SEPARATE 15.140 linear m sits behind it (LW_1 x4 and WN_7 x3, the full-height glazed AOV and "
 "smoke-shaft units in communal corridors) IF Approved Document K critical-location glazing is read to "
 "catch them. Not included above; flagged rather than assumed.\n\n"
 "STRIP-OUT. Gordon Court is GBP 368,376.70 - more than twice St Mary's - and Adam's ruling was that we "
 "would include strip-out on a job of this size. The quantity is 40 REPLACEMENT WINDOWS totalling "
 "62.457 m2 (schedule 5244-ARK-52002; the 84 new windows are new-build and carry none). Our proposal "
 "excludes 'Waste Removal - Generally' and never names removal of the existing windows, and the "
 "GBP 46,840 install cannot absorb it because it is pure per-unit fit labour at GBP 160-500 a unit. "
 "Unlike St Mary's there is no client Schedule of Works cross-referring strip-out into our item - the "
 "jLiving contract is an NEC3 activity schedule with no item numbers - so on this job it is simply "
 "unallocated rather than allocated to us.\n\n"
 "NEITHER ITEM CAN BE BENCHMARKED, WHICH IS WHY THIS IS AN RFQ AND NOT AN ESTIMATE. I re-checked "
 "data/supplier-rates.json at source rather than taking it on trust: 80 register entries, and ZERO "
 "carry a strip-out, disposal, removal, manifestation or scaffold category. So both figures above are "
 "QUANTITIES ONLY. I have deliberately not attached a rate to either - there is nothing in the system "
 "to derive one from, and inventing one is how a TBC becomes a number nobody can defend."
)

req['why'] = req.get('why', '') + ADD
for opt in ("Price Gordon Court's manifestation at 15.002 linear m (5 communal doors) as an RFQ line",
            "Price Gordon Court's window strip-out and disposal at 62.457 m2 over 40 units",
            "Confirm NBS cl.280 manifestation applies to the D_A entrance pair as well as the single-leaf doors"):
    if opt not in req['options']:
        req['options'].append(opt)

with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

# VERIFY BY RE-READING - the print statement is not the evidence, the file is
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
chk = next((r for r in back['requests'] if r['id'] == 'REQ-24'), None)
assert chk is not None, 'REQ-24 vanished on re-read'
assert MARKER in chk['why'], 'append did not persist'
assert any('15.002 linear m' in o for o in chk['options']), 'options did not persist'
print('VERIFIED on re-read: REQ-24 why is %d chars, %d options, marker present'
      % (len(chk['why']), len(chk['options'])))

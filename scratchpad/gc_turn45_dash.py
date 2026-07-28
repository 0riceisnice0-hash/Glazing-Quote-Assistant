# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'NEW SCOPE ITEM - APPROVED DOCUMENT K GUARDING TO THE THREE AOV OPENINGS'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "A real scope item, found by checking where my own quotations stopped rather than what they said.\n\n"
 "The BSW letter quoted NBS L20 clause 630 down to 'Drive open/drive close using a 24V motor mounted to the "
 "rear' and closed the quotation marks there. The clause continues:\n\n"
 "    Polyester powder paint finish.\n"
 "    Note: Any part of the ventilator opening within 1.1m of floor level will require\n"
 "    guarding for compliance with Approved Document K.\n\n"
 "WN_7 is scheduled as a wall unit at 910 x 2100, so on any normal cill height part of the opening sits below "
 "1.1m from finished floor. That makes guarding a requirement of the clause that specifies the unit - not a "
 "separate trade's item - and it has never been priced by us, quoted by BSW, or asked of anybody. It is now "
 "the second limb of A1, worded to accept 'outside a glazing package' as an answer provided BSW put it in "
 "writing. Recorded as spec item 34.\n\n"
 "Also in the same pass: my quotation of the louvre clause used two ellipses which between them removed grade "
 "3005 aluminium to EN573-3, stainless steel fixings, manufacture under EN 9000, and the fail-safe action "
 "where the louvres are spring-opened and actuator-closed. All four are priceable and none was in the letter. "
 "Both clauses are now quoted in full.\n\n"
 "And one I checked and left alone: the Chigwell letter's ellipsis in the fire strategy revision note skips "
 "'Entrance to flat 28, 29 to allow for travel distance', which is an unrelated change in the same revision "
 "and does not qualify the smoke shaft omission.\n\n"
 "No change to the tendered figure. The guarding is a new question rather than a new cost until BSW answer - "
 "if it lands with us it is an addition, and better found now than at order. Position GBP 368,376.70, nothing "
 "sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

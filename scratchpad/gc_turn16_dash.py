# -*- coding: utf-8 -*-
"""Sixteenth turn: our own proposal carries a 30-day validity, and three exclusions are doing work they should not."""
import json, io, os, datetime as dt

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
MARKER = 'OUR OWN PROPOSAL CARRIES A 30-DAY VALIDITY CLAUSE'

with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

today = dt.date(2026, 7, 28)
ours = dt.date(2026, 8, 8)

req['why'] += (
 "\n\n---\n\n" + MARKER + " - IT QUALIFIES THE RISK ADAM ACCEPTED, AND HE DID NOT HAVE IT. 28/07.\n\n"
 "THIS DOES NOT REOPEN REQ-20. He decided we hold the price and carry the gap, and that decision stands. But he "
 "took it on my figure of 163 days of unqualified exposure, and that figure was incomplete - our own issued "
 "document limits it. He should have the fact even though the decision does not change.\n\n"
 "PAGE 8 OF THE PROPOSAL WE ISSUED ON 09/07, under TERMS AND CONDITIONS: '2. Quotation Validity - All quotations "
 "provided by Fenster Glazing & Locks Ltd are VALID FOR 30 DAYS FROM THE DATE OF ISSUE, unless agreed otherwise. "
 "All quotations are subject to final site survey and measurement verification.'\n\n"
 "So on our own terms the GBP 368,376.70 expired on 08/08/2026 - %d days from today - while jLiving's Form of "
 "Tender holds the TENDER open to 18/01/2027. Those directly conflict, and the distinction that matters is that "
 "WE ARE NOT A PARTY TO jLIVING'S FORM OF TENDER. Chigwell signed that. Our contract is with Chigwell, our "
 "document says 30 days, and that clause was issued to them in writing.\n\n"
 "BEING FAIR ABOUT HOW MUCH THIS IS WORTH: commercially Chigwell priced our number into a bid they have committed "
 "for 180 days and they will expect us to honour it, and a subcontractor's validity clause is routinely overridden "
 "by a main contractor's order terms. So this is a negotiating position rather than a shield. But it is in writing, "
 "it was issued, and the 163-day exposure is therefore QUALIFIED rather than absolute - which is a materially "
 "different thing to be carrying. It also makes RFI-11 more important than it looked: if our terms went up with "
 "Chigwell's Section 2 caveats, the 30-day clause is visible to jLiving; if they did not, Chigwell absorbed it "
 "silently.\n\n"
 "AND RIVERSIDE'S ARITHMETIC RUN PROPERLY NOW THAT I HAVE OUR OWN VALIDITY PERIOD: supplier expiry minus our "
 "validity gives the last date we could have issued and still been covered. BSW lapse 06/08 minus 30 days = "
 "07/07/2026. WE ISSUED ON 09/07 - TWO DAYS AFTER OUR COVER RAN OUT. We were never covered on this job. Small, but "
 "it is the precise thing their check is designed to surface, and it was behind us before anyone looked.\n\n"
 "THREE DATES, AND THEY ANSWER DIFFERENT QUESTIONS:\n"
 "   07/07/2026  the last date we could have issued and been covered by BSW  - already behind us\n"
 "   06/08 / 08/08  the date we can no longer ask either supplier cheaply     - 9 and 11 days\n"
 "   08/08/2026  our own quotation expires on its own terms                   - 11 days\n"
 "After 08/08 nothing on this job is held by anybody: BSW lapsed, AFS lapsed, and our own price expired.\n\n"
 "SEPARATELY - THREE OF OUR TWELVE EXCLUSIONS ARE DOING WORK THEY SHOULD NOT, found by running riverside's "
 "rate-versus-quantity sort over the exclusions list rather than the findings list. They caught window restrictors "
 "sitting in an exclusions list when they were really an unanswered supplier question. Mine:\n"
 "  1. 'FIRE STOPPING - To be done by others, if required' CONFLICTS WITH NBS L10 cl.790, which puts the "
 "intumescent frame-to-reveal seal in the WINDOWS section - our package. Cavity barriers are the main "
 "contractor's; that perimeter seal is not. Quantity 3 fire doors, no rate, owner AFS. A supplier question wearing "
 "an exclusion's clothes.\n"
 "  2. 'TESTING - On or off site testing' DOES NOT COVER NBS cl.205, which requires 'Independent, 3rd Party "
 "Certification Schemes' and 'documentation confirming Certifications claimed'. Certification is documentation the "
 "manufacturer already holds, not a test - so the exclusion reads as if it covers the obligation and does not. "
 "Owner BSW, and probably free if they hold the certificates.\n"
 "  3. 'SITE STORAGE - Materials will be delivered to site' ASSERTS A FACT NO QUOTE WE HOLD SUPPORTS. All five "
 "quotes deliver to our own MK13 9HF yard. We have told the client materials arrive at site while every supplier "
 "says they arrive in Milton Keynes.\n"
 "And one distinction rather than a conflict: 'DESIGN RESPONSIBILITY - design calculations... excluded' fairly "
 "covers us PRODUCING a Uw calculation, but it does not get us the FIGURE, which BSW should state as a matter of "
 "course. Excluding the work is not the same as not needing the number.\n"
 "'Structural Alterations - to be completed by Main Contractor' is consistent with the head contract and the "
 "demolition plans - a genuine exclusion, cleared." % ((ours - today).days,)
)

for opt in ("Put our 30-day validity clause to Chigwell in writing before 08/08, while it is still live",
            "Correct the three exclusions - fire stopping, testing and site storage - in any re-issued proposal",
            "Ask AFS to price the intumescent seal our Fire Stopping exclusion does not actually cover"):
    if opt not in req['options']:
        req['options'].append(opt)

d['updated'] = '2026-07-28'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-26')
assert MARKER in br['why'] and any('30-day validity clause to Chigwell' in o for o in br['options'])
print('VERIFIED on re-read: REQ-26 %d chars, %d options' % (len(br['why']), len(br['options'])))

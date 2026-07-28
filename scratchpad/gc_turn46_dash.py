# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'WE OFFER CHIGWELL TEN YEARS ON GLASS AND AFS GIVE US FIVE'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "Three findings, all from one clause of the AFS terms that I had never opened - clause 6, the warranty - in a "
 "document I had already quoted from five times.\n\n"
 "1. THE WARRANTY BACK-TO-BACK. Our issued proposal offers Chigwell 'a 10-year warranty covering all glass and "
 "frame products supplied and installed by the company'. AFS clause 6.1 gives us 5 years on glass and 10 years "
 "on mechanical aspects. So on the three EI30 doorsets there is a five-year glass gap. Our proposal does carry "
 "the saving clause 'subject to the terms and conditions of any applicable manufacturer warranties', so the two "
 "are not in conflict - but the gap is real and this is the first time anybody has checked.\n\n"
 "And BSW's four quotations state NO warranty at all - zero mentions of warrant, guarantee, year or defect "
 "across all four. So on 124 windows, 44 patio doors and 15 external doors we cannot say whether our ten years "
 "is backed. It would be in the terms of sale D2 already asks for, which is now the third separate reason to "
 "send that request.\n\n"
 "AFS section 6(c) asks whether they can offer ten years on the glass in these three doorsets, or what it "
 "would cost, so we can give the client one period rather than two.\n\n"
 "2. A 24-HOUR NOTIFICATION CLOCK NOBODY HAS BEEN TOLD ABOUT. Clause 6.3.1 requires written notice 'within 24 "
 "hours of delivery/collection in respect of Goods, if the alleged defect is apparent on visual inspection'. "
 "The Delivery Location on Q7585 is our own yard at Bradwell Abbey, so that clock starts with us. The yard has "
 "never been told. Raised as 6(a), and worth a standing instruction whoever receives supply-only deliveries.\n\n"
 "3. THE WARRANTY IS CONDITIONAL ON INSTALLATION INSTRUCTIONS WE DO NOT HOLD. All three positions are priced "
 "'Without Installation' - the installation is ours - and clause 6.4 voids the warranty where the Customer "
 "failed to follow AFS's instructions on storage, installation, commissioning, use or maintenance. On an EI30 "
 "doorset the installation detail is what separates a certified assembly from an uncertified one. We have never "
 "asked for those instructions. Raised as 6(b), requesting them so our fixing detail can be checked against "
 "them before we start rather than after.\n\n"
 "None of this changes the tendered figure. Items 2 and 3 cost nothing to fix and would be expensive to "
 "discover after delivery. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

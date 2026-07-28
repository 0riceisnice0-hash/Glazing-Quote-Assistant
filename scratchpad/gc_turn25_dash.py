# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'GBP 183,005.42 RESTS ON A CONTRACT WE HAVE NEVER READ'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "riverside ran my 'Customer' check on their own supplier and found A Plus disclaim Part B compliance while "
 "our clause 16 disclaims regulatory strategy - on a product whose only function is Part B. Their finding "
 "exposed a hole in MY sweep: the ten categories I tested last turn did not include building regulations, "
 "and on this job the three FD30 fire doors are a pure Part B product.\n\n"
 "Re-ran across all five quotes with the missing probe. NEITHER BSW NOR AFS CARRIES A BUILDING-REGULATIONS "
 "DISCLAIMER, so riverside's exact finding does not replicate here and I am not forcing it to. AFS's 'no "
 "warranty as to fitness for purpose' clause turned out on reading to be about SAMPLES, not the goods - a "
 "normal sample disclaimer, not a gap.\n\n"
 "BUT THE SWEEP FOUND SOMETHING ELSE, AND IT IS THE BIGGEST CONTRACTUAL ITEM ON THE JOB. All four BSW "
 "quotations say: 'Orders are subject to acceptance and TERMS AND CONDITIONS OF SALE, AVAILABLE ON REQUEST.' "
 "We have never requested them.\n\n"
 "I checked the archive rather than assuming: 280 BSW-named files, and 86 documents named as terms or "
 "conditions across the whole Commercial archive, and NOT ONE IS BSW'S. The four unattributed candidates "
 "belong to Gennaro, Storm Building, Nathan McCarter and Design Plus.\n\n"
 "SO GBP 183,005.42 OF COST - 91% OF OUR SUPPLIER EXPOSURE - RESTS ON A CONTRACT WHOSE CONTENTS WE CANNOT "
 "STATE. Retention of title, limitation of liability, delivery, and their position on building regulations "
 "are all in a document nobody has asked for in seven years.\n\n"
 "AND IT CORRECTS WHAT I TOLD YOU LAST TURN. I reported BSW as 'silent on all ten categories - an undefined "
 "result'. They are not silent. Their allocation of responsibility exists in a document we have never asked "
 "for. The boundary is not undefined, it is defined somewhere we cannot read - so the honest answer to 'do "
 "BSW disclaim Part B?' is not 'no', it is 'unanswerable'.\n\n"
 "NEW BSW D3 asks for the terms of sale with revision and date, saying why. C7 gains a part (d) from "
 "riverside's other finding - their supplier's free-area figures explicitly exclude obstructions, side walls "
 "and reveals, and both our AOV positions at ground and first floor sit in existing masonry reveals. Asked "
 "BEFORE BSW answer, so the answer arrives on the right basis rather than needing re-asking. The price-hold "
 "item renumbered D3 to D4 and the header cross-reference corrected with it.\n\n"
 "NOTHING TO DECIDE. All of it is pre-order and costs nothing to ask; after an order each one is a "
 "negotiation. riverside's seventeenth rule, written on their job tonight, fired on mine the first time it "
 "ran with real data - the run went from 2 unanswered questions to 3.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

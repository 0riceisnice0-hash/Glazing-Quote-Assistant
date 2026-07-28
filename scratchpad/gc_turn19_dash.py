# -*- coding: utf-8 -*-
"""Nineteenth turn: the three drafts exist - REQ-26 is now read-and-send."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'ALL THREE DOCUMENTS ARE NOW DRAFTED'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - THIS REQUEST IS NOW READ-AND-SEND, NOT COMPOSE-FROM-SCRATCH. 28/07.\n\n"
 "st-marys' point earlier tonight was that on a deadline you draft the deliverable BEFORE the decision comes "
 "back, not after. This request had nine days and no text behind it, so the text now exists:\n\n"
 "  outputs\Gordon Court - RFQ to BSW (draft, send by 06-08).txt\n"
 "  outputs\Gordon Court - RFQ to AFS (draft, send by 08-08).txt\n"
 "  outputs\Gordon Court - post-tender queries to Chigwell (draft).txt\n\n"
 "They are split by CLAUSE 16, deliberately, and the reasoning is printed at the head of each so whoever sends "
 "them knows why the tone differs. The two supplier letters carry the items our own terms make OURS - "
 "measurement verification, supply of the agreed glazing systems, and performance figures the supplier holds and "
 "we do not. The Chigwell letter carries the items clause 16 puts on the client's professional team, worded as "
 "questions and reliances rather than as defects.\n\n"
 "WHAT IS IN EACH:\n"
 "  BSW - the AOV and louvre product question, curtain walling, the five frame-size discrepancies, whole-window "
 "Uw, the 8000mm2 trickle vent upgrade, Passivent acoustic vents, PAS 24 with the cl.205 submittals, "
 "manifestation at 15.002 lm, delivery to site, and confirmation of the GBP 217.50 extra.\n"
 "  AFS - the intumescent seal cl.790 requires (their pack says only 'mastic'), the RAL 7016 matt / RAL 9010 "
 "gloss dual finish, the GBP 506.37 extras and the 'Logistics: Delivered' contradiction, whole-door Ud, position "
 "003's 2210-against-2110 height and its leaf configuration, and a straight question on how long they can hold.\n"
 "  CHIGWELL - the smoke-shaft omission and whether the 4no louvres survive it, which duty the AOVs serve and "
 "wall-or-roof, D_T and D_X, the demolition elevations and the 57 missing drawings, the SAP calculations, "
 "manifestation extent, strip-out allocation, and the two admin corrections to our own proposal.\n\n"
 "NOTHING HAS BEEN SENT. Mary cannot issue supplier or client mail - ghost protocol limits outbound to Adam and "
 "marketing, and mary_send is 403'd in any case. A human sends all three. The BSW letter is the one with a date "
 "on it.\n\n"
 "ONE DELIBERATE CHOICE WORTH FLAGGING: the Chigwell letter says we are content to honour the tendered figure "
 "and are not seeking to withdraw it, because Adam decided that on REQ-20. It mentions our 30-day validity only "
 "to put it on record and to ask whether our terms reached jLiving via Chigwell's Section 2 caveats. If Adam "
 "would rather that paragraph came out entirely, it is the last section and can be deleted without touching "
 "anything else."
)
for opt in ("Send the three drafts as written - BSW by 06/08, AFS by 08/08, Chigwell any time before 16/09",
            "Send the two supplier RFQs only and hold the Chigwell letter until jLiving announce",
            "Delete the validity paragraph from the Chigwell letter before sending"):
    if opt not in req['options']:
        req['options'].append(opt)
d['updated'] = '2026-07-28'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-26')
assert MARKER in br['why'] and any('Send the three drafts as written' in o for o in br['options'])
print('VERIFIED on re-read: REQ-26 %d chars, %d options' % (len(br['why']), len(br['options'])))

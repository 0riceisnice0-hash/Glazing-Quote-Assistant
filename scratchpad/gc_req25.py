# -*- coding: utf-8 -*-
"""REQ for the two consolidated supplier RFQs - actionable now, independent of jLiving."""
import json, io, os, re
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
nums = [int(m.group(1)) for r in d['requests'] for m in [re.match(r'REQ-(\d+)$', r['id'])] if m]
new_id = 'REQ-%d' % (max(nums) + 1)
assert not any(r['id'] == new_id for r in d['requests']), new_id
print('allocating', new_id, '(existing max %d)' % max(nums))

WHY = (
 "Gordon Court has 18 standing findings. Twelve of them carry money, and I can total only two of them. This is "
 "the position in one place, because nobody has had it in one place before.\n\n"
 "HARD - invoice-verifiable, no rate needed:\n"
 "   AFS fixing pack + delivery, omitted from the tender          GBP  506.37\n"
 "   BSW 'PANEL SET UP' extra on QT252257, never carried          GBP  217.50\n"
 "                                                          TOTAL GBP  723.87\n\n"
 "POSSIBLE CREDIT, if confirmed:\n"
 "   4no WL_1 louvres to a smoke shaft DELETED in Oct 2025    -GBP 6,452.40 sell (-GBP 4,502.40 cost)\n\n"
 "BENCHMARK ONLY - a single data point each, order of magnitude, not a price:\n"
 "   2no D_X external doors, on the schedule and priced nowhere   ~GBP 5,600 sell + ~GBP 1,000 install\n"
 "   AOV actuator/motor absent from the 3no WN_7                  ~GBP 4,988-5,667 of supply cost\n\n"
 "QUANTIFIED OR KNOWN, BUT UNPRICEABLE - THERE IS NO RATE ANYWHERE IN OUR SYSTEM:\n"
 "   manifestation                    15.002 linear m over 5 communal doors\n"
 "   strip-out and disposal           62.457 m2 over 40 replacement windows\n"
 "   trickle vent upgrade             4000mm2 quoted against 8000mm2 required, 124 windows\n"
 "   acoustic trickle vents           26 of 40 replacement windows confirmed; new-window count not done\n"
 "   intumescent perimeter seal       3 fire doors (NBS L10 cl.790)\n"
 "   PAS 24 certification             124 windows (NBS L10 cl.330), absent from all four BSW quotes\n"
 "   curtain walling                  in the design on three pointers, no schedule exists, quantity unknown\n"
 "   carriage MK yard to Edgware      227 units, all five quotes deliver to our own yard\n\n"
 "THE REASON THE LIST CANNOT BE TOTALLED IS STRUCTURAL, NOT LAZINESS. I checked data/supplier-rates.json at "
 "source: of its 80 categories, ZERO carry acoustic, trickle vent, Linkvent, Passivent, curtain walling, "
 "actuator, AOV, strip-out, disposal, manifestation or intumescent. Eight of the twelve money items sit in "
 "categories the register does not have, so there is nothing to benchmark them against and inventing a rate "
 "would just turn a TBC into a number nobody can defend.\n\n"
 "BUT MOST OF IT IS ANSWERABLE IN ONE ROUND, AND IT DOES NOT DEPEND ON jLIVING. Everything above except the "
 "credit and the D_X price is a SUPPLIER question, not a client question - so it can go out now rather than "
 "waiting for the award on 16 September:\n"
 "   ONE RFQ TO BSW covers six: 8000mm2 trickle vents, Passivent AL-dB 450 acoustic vents on the marked units, "
 "PAS 24 certification with the cl.205 third-party submittals, manifestation to 15.002 linear m, a curtain "
 "walling price or a confirmation there is none in our package, and their delivery basis and threshold. Plus "
 "the whole-window Uw figures we still do not have against Edward Pearce's 1.10 W/m2K.\n"
 "   ONE RFQ TO AFS covers two: the intumescent perimeter seal NBS L10 cl.790 requires (their fixing pack says "
 "only 'foam, packers, mastic'), and the RAL 7016 matt external / RAL 9010 gloss internal dual finish they have "
 "not priced.\n"
 "Two emails would convert eight unpriceable items into real numbers. Nothing else on this job can move until "
 "jLiving announce."
)

NEEDS = (
 "This is the one thing on Gordon Court that can be actioned before 16 September, because it goes to suppliers "
 "rather than to Chigwell. It is also the only way to find out what the 18 findings are actually worth - at "
 "present GBP 723.87 is the only figure on the list I would defend. Note Mary cannot send it: the ghost protocol "
 "limits outbound to Adam and marketing, and mary_send is 403'd in any case, so a human has to issue both RFQs."
)

d['requests'].append({
 "id": new_id,
 "raised": "2026-07-28",
 "job": "Gordon Court, Stonegrove Edgware (Chigwell Group / jLiving)",
 "owner": "Adam",
 "title": ("Gordon Court: 12 findings carry money and only GBP 723.87 of it can be priced - two supplier RFQs "
           "would convert eight of them, and they do not need to wait for jLiving"),
 "why": WHY,
 "needs": NEEDS,
 "options": [
  "Issue one consolidated RFQ to BSW covering trickle vents, acoustic vents, PAS 24, manifestation, curtain walling, carriage and Uw",
  "Issue one consolidated RFQ to AFS covering the intumescent seal and the dual-colour finish",
  "Issue both RFQs now rather than waiting for jLiving's 16 September announcement",
  "Hold both until jLiving award and accept that the findings stay unpriced until then",
  "Issue the GBP 723.87 addendum to Chigwell separately from the RFQs",
  "Ask Chigwell to confirm the 4no smoke-shaft louvres are deleted before pricing anything else",
  "Accept the eight unpriceable items as excluded and qualify the tender to Chigwell instead of pricing them"
 ],
 "status": "open"
})
d['updated'] = '2026-07-28'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
chk = [r for r in back['requests'] if r['id'] == new_id]
assert len(chk) == 1 and 'Gordon Court' in chk[0]['job'], 'append did not persist'
print('VERIFIED on re-read: %s present, job %s, %d options'
      % (new_id, chk[0]['job'][:40], len(chk[0]['options'])))

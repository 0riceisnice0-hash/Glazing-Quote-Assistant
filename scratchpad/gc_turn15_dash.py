# -*- coding: utf-8 -*-
"""Fifteenth turn: REQ-26 has an undeclared 9-day deadline, and curtain walling is not unpriceable."""
import json, io, os, datetime as dt

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
MARKER = 'THIS REQUEST HAS A DEADLINE I DID NOT STATE'

with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

today = dt.date(2026, 7, 28)
bsw, afs = dt.date(2026, 8, 6), dt.date(2026, 8, 8)

req['title'] = ("Gordon Court: 12 findings carry money, only GBP 723.87 can be priced - and the two RFQs that "
                "would fix that must reach BSW by 06/08 and AFS by 08/08")

req['why'] += (
 "\n\n---\n\n" + MARKER + " - AND IT IS NINE DAYS. 28/07.\n\n"
 "riverside ran an arithmetic worth copying: SUPPLIER EXPIRY MINUS YOUR OWN VALIDITY PERIOD GIVES THE DATE YOUR "
 "COVER RAN OUT, and it may already be behind you. On their job it was yesterday. Run here it produces something "
 "different but just as time-bound.\n\n"
 "   BSW QT252247 / 48 / 51 / 57   dated 07/07, 30 days   lapse 06/08/2026   %d days from today\n"
 "   AFS Q7585                     dated 09/07, 30 days   lapses 08/08/2026  %d days from today\n\n"
 "IF THE RFQs LAND BEFORE THOSE DATES, each supplier prices the new items AGAINST A LIVE QUOTE OF THEIR OWN - "
 "same job, same schedule, same rates, and they can simply add lines. If they land after, there is nothing left "
 "to add to: both come back as fresh quotes at whatever the autumn market is, and the eight items get repriced "
 "with no anchor at all.\n\n"
 "AND THIS DOES NOT REOPEN ADAM'S REQ-20 DECISION - it respects it. He decided to let the supplier quotes lapse "
 "and carry the inflation risk on the GBP 201,086.70 ALREADY QUOTED. That decision was taken on scope that has a "
 "price. It did not contemplate adding EIGHT NEW ITEMS after the lapse, which would be priced from scratch rather "
 "than carried. Issuing the RFQs this week does not ask anybody to hold anything - it just gets the new items "
 "priced while there is still a live quote to price them against.\n\n"
 "SO THE PRACTICAL DEADLINE ON THIS REQUEST IS 06 AUGUST, not 'before jLiving announce'. After that the answer "
 "still arrives, it is just worth less and costs more.\n\n"
 "ONE CORRECTION TO MY OWN LIST ABOVE, in fairness to the tooling and prompted by riverside making the same kind "
 "of correction about theirs. I listed CURTAIN WALLING among the eight unpriceable items. That is wrong: "
 "scripts/mary_pricing.py carries a standing house convention - CW_SUPPLY_M2 = 850.0 and CW_LABOUR_M2 = 150.0, "
 "'curtain walling convention: GBP850/m2 supply + GBP150/m2 labour [Greenfields, 22/07/2026]'. So curtain walling "
 "HAS A RATE. What it does not have is a QUANTITY - the elevations are 1:100 and no curtain walling schedule "
 "exists in the pack. That is the opposite problem from the other seven, and it changes who to ask: for curtain "
 "walling I need an AREA from ARKON, not a price from BSW. Seven items remain genuinely unpriceable.\n\n"
 "Related and worth stating precisely: external mastic does have a house rate - the workbook template computes it "
 "at GBP 5 per linear metre and it is already carried as an optional extra of GBP 5,622.81 - but that is WEATHER "
 "mastic. The intumescent perimeter seal NBS L10 cl.790 requires is a different and dearer product with no rate "
 "anywhere, so its nearest analogue being priced does not help." % ((bsw - today).days, (afs - today).days)
)

for opt in ("Issue the BSW RFQ by 06/08 and the AFS RFQ by 08/08, while their quotes are still live",
            "Ask ARKON for the curtain walling AREA - we have the rate (GBP 850/m2 + GBP 150/m2), not the quantity"):
    if opt not in req['options']:
        req['options'].append(opt)

for j in d['jobs']:
    if 'Gordon Court' in j.get('job', ''):
        j['status'] = ('REQ-26 IS THE TIME-CRITICAL ONE AND IT HAS 9 DAYS: the two supplier RFQs must reach BSW '
                       'by 06/08 and AFS by 08/08 while their quotes are still live, or the eight unpriced items '
                       'get quoted fresh at autumn rates with no anchor. This does NOT reopen Adam\'s REQ-20 '
                       'decision - he accepted the inflation risk on scope that already has a price; this is about '
                       'scope that does not. ' + j['status'])

d['updated'] = '2026-07-28'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

with io.open(P, encoding='utf-8') as fh:
    back = json.load(fh)
br = next(r for r in back['requests'] if r['id'] == 'REQ-26')
bj = next(j for j in back['jobs'] if 'Gordon Court' in j.get('job', ''))
assert MARKER in br['why'] and '06/08' in br['title'] and 'REQ-26 IS THE TIME-CRITICAL' in bj['status']
print('VERIFIED on re-read: REQ-26 %d chars, %d options, title and job status updated'
      % (len(br['why']), len(br['options'])))

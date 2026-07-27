# -*- coding: utf-8 -*-
"""Add REQ-20 for Gordon Court and refresh its dashboard job entry."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)

assert not any(r['id'] == 'REQ-20' for r in d['requests']), 'REQ-20 already exists'

WHY = (
 "The tender went to Chigwell on 09/07 at GBP 368,376.70. Reading jLiving's own ITT and Form "
 "of Tender - both inside the tender zip, neither opened before today - changes what this job is.\n\n"
 "1. THE CLIENT IS NOT CHIGWELL, IT IS jLIVING, AND CHIGWELL CANNOT ANSWER US YET. Chigwell were "
 "bidding to jLiving (Jewish Community Housing Association, advised by Vixus) with a tender return "
 "of 22 July 2026 @ 1400 - five days ago. jLiving's published timetable then runs: bidder "
 "presentations 02 September, award announcement 16 September, standstill 30 September, contract "
 "award mid-October, Go Live 30 October 2026. So silence from Chigwell between now and September is "
 "expected. AFS chasing on 27/07 is them working their book - they chased Manor House Q7593 100 "
 "minutes later.\n\n"
 "2. OUR PRICE IS COMMITTED FOR 180 DAYS AND OUR COST IS FIXED FOR 30. jLiving's Form of Tender "
 "states: 'This tender remains open for consideration for a period of 180 days from the date of "
 "receipt of tenders.' Receipt 22/07/2026, so the price is held to 18 JANUARY 2027. Every supplier "
 "quote behind it is 30 days: BSW's four (QT252247/48/51/57, all dated 07/07) lapse ~06/08, AFS "
 "Q7585 lapses ~08/08. That is GBP 201,086.70 - 54.6% of the tender - unfixed for about 163 days "
 "against a LUMP SUM FIRM PRICE under NEC3 ECC Option A executed as a DEED. And neither price is "
 "binding even inside 30 days: AFS T&C 2.6 says a quotation 'will not constitute an offer and may "
 "be withdrawn or amended at any time', T&C 8.2 reserves the right to raise it for material, labour "
 "or FX movements, and every BSW quote says 'An estimate is not an offer of contract and is not "
 "binding.' Contract award is ~11 weeks AFTER the last quote dies, and AFS's 8-week lead time runs "
 "from order signature AND their 60% payment, so the fire doors land around January 2027.\n\n"
 "3. GBP 723.87 OF SUPPLIER COST IS NOT IN THE 368,376.70. AFS extras GBP 506.37 (fixing pack "
 "GBP 256.37 + delivery GBP 250.00, Q7585 p7, outside the GBP 18,298.94 and nowhere in the "
 "workbook). The quote contradicts itself - its Specifics page says 'Logistics: Delivered' - but "
 "AFS T&C 8.1 settles it against us: price is 'exclusive of all costs and charges of packaging, "
 "insurance and transport... invoiced to the Customer in addition'. PLUS a new one: BSW QT252257 "
 "carries an Extras line 'PANEL SET UP GBP 217.50' that was never carried - the workbook took "
 "GBP 6,868.26 of a GBP 7,085.76 quote.\n\n"
 "4. THE THIRD FIRE DOOR IS DOOR TYPE D_T AND THREE THINGS ABOUT IT ARE WRONG OR BLANK. The count "
 "of 3 survives - the two D_A doors match schedule 51001 to the millimetre. But the third is D_T, "
 "which the schedule gives as 2110 high (AFS quoted 2210 - 100mm TALLER than the structural "
 "opening), as room GR425 STORE with the Internal/External cell LEFT BLANK, and as a 756 x 2060 "
 "SINGLE leaf in a 1600 opening (AFS quoted '1 Pcs. Double Door'). GBP 7,304.44 of sell rests on "
 "all three. If D_T is internal it is the joinery package's, not ours.\n\n"
 "5. 2no DOOR TYPE D_X ARE ON THE EXTERNAL DOOR SCHEDULE AND PRICED NOWHERE. 2100 high x 1800 wide, "
 "Level 0. Schedule 51001's own count cells sum to exactly the 116 it states as its total, so this "
 "is the drawing's number: 17 non-internal doors, we priced 15. Every descriptive cell on both D_X "
 "rows is blank. Nearest comparator D_E is GBP 2,779.70 sell each, so roughly GBP 5,600 of sell plus "
 "GBP 1,000 install - BENCHMARK ONLY, there is no supplier price for it.\n\n"
 "6. PERFORMANCE THE SUPPLIERS HAVE NOT PRICED. The schedules set NO U-value - they defer to "
 "'Edward Pearce Consulting Engineers specification', which is NOT in the pack. The Energy "
 "Statement in the zip requires 1.1 W/m2K on replacement external glazing; no whole-window Uw is "
 "stated on any BSW quote. Trickle vents: schedules require 8000mm2 minimum, BSW quoted 4000mm2 "
 "Linkvents - half. Acoustic trickle vents ('Passivent AL-dB 450 or better') are ticked on 26 of "
 "the 40 replacement windows and appear in no quote - zero mentions of Passivent, AL-dB or acoustic. "
 "PAS 24 / Secured by Design is required and appears zero times across all four BSW quotes. And AFS "
 "priced the fire doors 'Standard RAL, mat standard' with no internal or external face against a "
 "spec of white inside / dark grey outside - dual colour is a real cost and it is not in there.\n\n"
 "CLEARED, so nobody re-opens them: install DOES cover the fire doors (DAD code = GBP 500/door, "
 "3 x 500 = GBP 1,500; the whole GBP 46,840 recomputed to the penny). Quantities reconcile EXACTLY "
 "on the other three schedules (patio 44=44, replacement windows 40=40, new windows 84=84). Q7585's "
 "arithmetic is right and nothing was dropped. The client-facing workbook leaks no cost at all - "
 "the 'DO NOT SEND' twin practice worked here, unlike Filwood. And the PVC-U/aluminium conflict was "
 "already qualified on our own proposal p3, so it is not a new problem."
)

NEEDS = (
 "The commercial decision is the 180-day one and it needs Adam, not a supplier email: we are "
 "carrying about 163 days of open cost on GBP 201,086.70 against a firm price we cannot withdraw. "
 "Nothing has to move today - jLiving do not decide until 16 September - but the price hold has to "
 "be asked for BEFORE 06/08 and 08/08, because after that we are re-quoting from scratch at "
 "whatever the market is in the autumn. Separately AFS are chasing and Mary cannot reply to them "
 "under ghost protocol, so a human has to answer Chris Wall either way. The D_T and D_X door "
 "questions are for the architect via Chigwell and can go in the same message."
)

d['requests'].append({
 "id": "REQ-20",
 "raised": "2026-07-27",
 "job": "Gordon Court, Stonegrove Edgware (Chigwell Group / jLiving)",
 "owner": "Adam",
 "title": ("Gordon Court: our price is held for 180 days to 18/01/2027 and every supplier quote "
           "behind it dies in early August - GBP 201,086.70 of cost unfixed for 163 days"),
 "why": WHY,
 "needs": NEEDS,
 "options": [
  "Ask BSW and AFS in writing to hold their prices to 18/01/2027 before they lapse on 06/08 and 08/08",
  "Carry a stated inflation allowance for the 163-day gap and qualify the tender to Chigwell",
  "Qualify the tender to Chigwell that our price is firm for 30 days only, not jLiving's 180",
  "Issue an addendum to Chigwell adding the GBP 723.87 of omitted AFS and BSW extras",
  "Ask Arkon via Chigwell whether D_T is external, 2110 or 2210 high, and single leaf or double",
  "Ask Arkon via Chigwell whether the 2no D_X doors (2100 x 1800) are in our package",
  "Get BSW to price 8000mm2 trickle vents, Passivent AL-dB 450 acoustic vents and PAS 24 as an addendum",
  "Get AFS to price the dual-colour finish (white internal / dark grey external) on the 3 fire doors",
  "Ask BSW for whole-window Uw figures against the Energy Statement's 1.1 W/m2K",
  "Reply to Chris Wall at AFS that the job is with jLiving until 16 September",
  "Hold everything until jLiving announce on 16 September and accept the repricing risk"
 ],
 "status": "open"
})

for j in d['jobs']:
    if j.get('job') == 'Gordon Court, Stonegrove Edgware':
        j['client'] = 'Chigwell Group (for jLiving)'
        j['deadline'] = '2026-08-08'
        j['status'] = (
         "AUDITED IN FULL 27/07 - see REQ-20. THE REAL CLIENT IS jLIVING and Chigwell were bidding to "
         "them with a return of 22/07/2026 @ 1400, so Chigwell CANNOT answer us until jLiving decide: "
         "presentations 02/09, award announcement 16/09, contract award mid-October, Go Live 30/10/2026. "
         "Silence until September is expected. THE BIG RISK: jLiving's Form of Tender holds our "
         "GBP 368,376.70 open for 180 DAYS to 18/01/2027 while all five supplier quotes are 30-day and "
         "lapse 06/08 (BSW x4) and 08/08 (AFS) - GBP 201,086.70, 54.6% of the tender, unfixed for ~163 "
         "days against a lump-sum firm price under NEC3 Option A executed as a deed, and neither "
         "supplier's quote is binding even inside 30 days. FOUND: GBP 723.87 of cost omitted (AFS extras "
         "GBP 506.37 + a new BSW 'PANEL SET UP' GBP 217.50); the third fire door is type D_T, quoted "
         "100mm taller than the structural opening, as a double where the schedule shows a single leaf, "
         "in a STORE whose external/internal cell is blank (GBP 7,304.44 of sell); 2no type D_X external "
         "doors on the schedule are priced nowhere (~GBP 5,600 sell, benchmark only); trickle vents at "
         "4000mm2 against 8000mm2 required; acoustic vents ticked on 26 of 40 windows and quoted by "
         "nobody; PAS 24 absent from all four BSW quotes; AFS have not priced the dual-colour finish. "
         "CLEARED: install does cover the fire doors (GBP 1,500 of the GBP 46,840, recomputed exactly), "
         "the other three schedules reconcile unit-for-unit, and the client workbook leaks no cost."
        )
        j['value'] = 'GBP 368,376.70 tendered'
        j['stage'] = 'submitted - awaiting jLiving 16/09'

d['updated'] = '2026-07-27'
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
print('REQ-20 added; job entry refreshed. requests now:', len(d['requests']))

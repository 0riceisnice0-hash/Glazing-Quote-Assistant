# -*- coding: utf-8 -*-
"""REQ-22: the Gordon Court AOV / smoke-shaft scope boundary."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
d = json.load(io.open(P, encoding='utf-8'))
assert not any(r['id'] == 'REQ-22' for r in d['requests']), 'REQ-22 exists'

WHY = (
 "Riverside asked me to check the free area on BSW's QT252257 'AOV & LOUVRE' (GBP 7,085.76). The free "
 "area turned out to be the small half of it.\n\n"
 "WHAT THE PACK ASKS FOR. The architect's window schedule 5244-ARK-52003 carries a heading 'AOV SMOKE "
 "SHAFT LOUVRE' and a note 'WL_00 Louvres to smoke shaft'. 3no WN_7 sit in Corridors 1-1, 1-2 and 1-3 "
 "(2100 x 910) with 'AOV' written against them; 4no WL_1 sit at levels 0-3 (2100 x 1210). NBS 9001 L20 "
 "clause 630 specifies both as Colt proprietary smoke-control products, and both are MOTORISED: "
 "'COLTITE GLAZED LOBBY VENTILATOR (STAIR C) - mounted into prepared openings in the external wall, "
 "Type CLT, double glazed with thermally broken glazing and outer frames, nominal size 1000mm wide x "
 "2000mm high or equivalent, DRIVE OPEN/DRIVE CLOSE USING A 24V MOTOR MOUNTED TO THE REAR'; and 'EN "
 "SEEFIRE LOUVRED NATURAL VENTILATOR - size to match shaft dimensions... DESIGNED AND TESTED TO EN "
 "12101-2... the position of the louvres is controlled by a 24Vdc ELECTRIC ACTUATOR, driven closed by "
 "this actuator and opened by a spring'.\n\n"
 "WHAT WE PRICED. BSW quoted 'Qty: 3 Prestige T&T' and 'Qty: 4 Prestige Casement' - ordinary Sheerline "
 "windows. QT252257 contains ZERO occurrences of AOV, louvre, actuator, chain, stroke, motor, 24V or "
 "smoke, and the louvre's Glazing line is BLANK with no reinforcing. There is no actuator, no 24V motor, "
 "no fire-alarm interface, no control gear and no EN 12101-2 certification anywhere in the price. BSW "
 "gave no free area of either kind because they had not quoted a ventilator at all.\n\n"
 "THE RATES CONFIRM IT. WN_7 is GBP 412.67/m2 over 5.733 m2 and WL_1 is GBP 442.98/m2 over 10.164 m2 - "
 "plain-window money against a register median of about GBP 528.83/m2 for a plain glazed aluminium "
 "window. Riverside's only AOV data point (A Plus DualFrame 75Si bottom-hung glazed AOV, 850mm stroke "
 "single chain) is GBP 1,401.24/m2 supply, of which the actuator and AOV sash carry roughly GBP 870/m2. "
 "On that single point the 3no WN_7 alone are GBP 4,988 to GBP 5,667 of supply cost short. That is ONE "
 "QUOTE on a DIFFERENT SYSTEM and it is an order of magnitude, not a price - there is still no AOV or "
 "smoke-vent category anywhere in the rate register, so the 4no louvres cannot be benchmarked at all.\n\n"
 "SO IT IS BINARY, AND GBP 10,055.76 OF SELL TURNS ON IT. The whole of QT252257 is these 7 units: "
 "GBP 7,085.76 of cost, GBP 10,055.76 of sell (WN_7 GBP 3,603.36 + WL_1 GBP 6,452.40). Either they are "
 "ours - in which case they are quoted against the wrong product and materially under-priced - or they "
 "belong to the smoke-ventilation specialist, in which case that sell should come out of the "
 "GBP 368,376.70. Our proposal p3 names 'AOV windows, smoke shaft louvres' as part of the tender "
 "information and does NEITHER: it does not price the function and does not exclude it.\n\n"
 "WHERE THE BOUNDARY PLAUSIBLY SITS. The two WALL-MOUNTED GLAZED items (Coltite ventilator, Seefire "
 "louvre) are the ones that could reasonably sit in a glazing package, and they are exactly the two the "
 "architect put on the window schedule. The rest of the Colt system - AXS140 roof ventilators, Defender "
 "smoke dampers, decorative louvre grilles, Vent Control Panels, OPV Display Panel and OPV Heart module, "
 "plus wiring and ductwork - is plainly a specialist's scope and I am not suggesting we price it. But the "
 "AXS140 roof units (1m2 and 1.5m2 geometric free area) and a 'Pitched Roof Smoke Vents Type B' are also "
 "currently neither priced nor excluded, and the enquiry zip is titled 'Windows, ROOFLIGHTS & Curtain "
 "Walling'.\n\n"
 "ONE PIECE OF GOOD NEWS. Riverside's warning was that specs are often written AERODYNAMIC while quotes "
 "state GEOMETRIC, and aerodynamic runs at only 60-62% of geometric - a ~40% shortfall on a number that "
 "looks fine. This pack is written GEOMETRIC throughout: 'aerodynamic' appears nowhere in the 186-page "
 "NBS, and the only hit in the 140-page mech spec is about attenuator fairings. So that particular trap "
 "does not bite us here."
)

NEEDS = (
 "This is a scope-boundary question for Chigwell, and it should be asked before anyone orders rather than "
 "after. It is not urgent this week - jLiving do not announce until 16 September - but it is worth asking "
 "in the same message as the D_T and D_X door queries, because all three are 'is this item in our "
 "package' questions for the same architect. If the answer is that the 7 units ARE ours, we need a real "
 "supplier price for a Coltite glazed ventilator and an EN Seefire louvre, because there is nothing in "
 "the rate register to fall back on and the current figure is a plain-window rate."
)

d['requests'].append({
 "id": "REQ-22",
 "raised": "2026-07-27",
 "job": "Gordon Court, Stonegrove Edgware (Chigwell Group / jLiving)",
 "owner": "Adam",
 "title": ("Gordon Court: 7no AOVs and smoke-shaft louvres are specified as motorised Colt smoke-control "
           "units and we priced them as ordinary windows - GBP 10,055.76 of sell either short or not ours"),
 "why": WHY,
 "needs": NEEDS,
 "options": [
  "Ask Chigwell to confirm whether the 3no AOVs and 4no smoke shaft louvres are in our package",
  "Get BSW to requote WN_7 and WL_1 as Colt Coltite and EN Seefire units with stated geometric free area",
  "Exclude AOVs, smoke shaft louvres and all smoke-control equipment by name in a re-issued proposal",
  "Ask Chigwell to confirm the AXS140 roof ventilators and pitched roof smoke vents are not ours",
  "Ask BSW to state the geometric free area they are offering on the units already quoted",
  "Price the AOV function as a provisional sum pending the specialist boundary being settled",
  "Hold it until Chigwell answer the D_T and D_X door queries and send all three together"
 ],
 "status": "open"
})

for j in d['jobs']:
    if j.get('job') == 'Gordon Court, Stonegrove Edgware':
        j['status'] = (
         "REQ-20 (validity) and REQ-22 (AOV scope) both OPEN. THE REAL CLIENT IS jLIVING - Chigwell bid to "
         "them 22/07 and jLiving announce 16/09, contract award mid-Oct, Go Live 30/10/2026, so Chigwell "
         "cannot commit to us before then and silence until September is expected. BIGGEST RISK: jLiving's "
         "Form of Tender holds our GBP 368,376.70 open 180 DAYS to 18/01/2027 while all five supplier quotes "
         "are 30-day and lapse 06/08 (BSW x4) / 08/08 (AFS) - GBP 201,086.70, 54.6% of the tender, unfixed "
         "for 163 days against a lump sum executed as a deed under NEC3 Option A. Price holds must be asked "
         "for BEFORE those dates. SECOND TURN 27/07 pm, from riverside's AOV handoff: the 3no AOVs and 4no "
         "smoke-shaft louvres (GBP 10,055.76 of sell) are specified by NBS L20 cl.630 as MOTORISED COLT "
         "smoke-control units - a Coltite glazed ventilator with a 24V motor and an EN Seefire louvre tested "
         "to EN 12101-2 - and BSW quoted plain Sheerline windows at GBP 412-443/m2 with no actuator, no "
         "motor, no free area and a blank glazing line. Either ours and badly short, or the specialist's and "
         "the sell comes out. Good news: this pack states free area as GEOMETRIC, so riverside's ~40% "
         "aerodynamic trap does not bite. ALSO FOUND: the NBS sets U-value max 1.2 W/m2K on windows AND "
         "communal entrance doors and requires PAS 24 on EVERY window with third-party certification - so "
         "the thermal requirement does NOT depend on the sustainability annex, correcting what I recorded "
         "earlier; and delivery is in nobody's price (all BSW quotes ex works with no rate or threshold, AFS "
         "delivery a GBP 250 omitted extra, and all five deliver to our own MK yard not to Edgware). "
         "EARLIER FINDINGS STAND: GBP 723.87 of omitted cost; door D_T quoted 100mm taller than its opening, "
         "as a double where the schedule shows a single leaf, in a Store whose external/internal cell is "
         "blank; 2no D_X external doors priced nowhere; trickle vents 4000mm2 against 8000mm2; acoustic "
         "vents ticked on 26 of 40 windows and quoted by nobody. CLEARED: install does cover the fire doors; "
         "the other three schedules reconcile unit-for-unit; the client workbook leaks no cost."
        )
        j['stage'] = 'submitted - awaiting jLiving 16/09; 2 requests open'

d['updated'] = '2026-07-27'
json.dump(d, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('REQ-22 added; job status refreshed. requests:', len(d['requests']))

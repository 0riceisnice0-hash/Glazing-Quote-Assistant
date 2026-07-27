# -*- coding: utf-8 -*-
"""Record Adam's answer to REQ-20 and refresh the Gordon Court job entry."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'dashboard-state.json')
d = json.load(io.open(P, encoding='utf-8'))

for r in d['requests']:
    if r['id'] == 'REQ-20':
        r['status'] = 'answered'
        r['answer'] = (
         "Adam, hub message 29, 27/07 19:37: \"It's fine we will hold the price and just trust everything "
         "will be okay.\" DECISION TAKEN AND ACCEPTED: we carry the 163-day gap on GBP 201,086.70 rather "
         "than seeking a written price hold or a stated allowance. Recorded for the file so that if BSW or "
         "AFS reprice in the autumn nobody is surprised: materials are 54.6% of the fixed GBP 368,376.70, "
         "so every 1% of supplier inflation is GBP 2,010.87 straight off the bottom line - 5% is "
         "GBP 10,054.33 and 10% is GBP 20,108.67. NOTE WHAT THIS ANSWER DOES NOT COVER: REQ-20's other "
         "options are untouched - the GBP 723.87 of omitted AFS and BSW extras, and the D_T / D_X door "
         "queries to Arkon. Those remain open decisions, and one new fact makes them harder: the tender's "
         "clarification window closed about 15 July (ITT allows questions up to 5 working days before the "
         "22/07 return, via the Delta portal only, and 'Please DO NOT contact jLiving directly'), so every "
         "open scope question on this job is now a POST-TENDER query through Chigwell rather than a "
         "clarification - i.e. variation territory."
        )
        r['answered_by'] = 'Adam'
        r['answered_at'] = '2026-07-27'

for j in d['jobs']:
    if j.get('job') == 'Gordon Court, Stonegrove Edgware':
        j['status'] = (
         "REQ-20 ANSWERED BY ADAM 27/07: 'It's fine we will hold the price and just trust everything will be "
         "okay.' So the 163-day validity gap is a taken decision, not an open question - we carry it. For "
         "the file: materials are 54.6% of the fixed GBP 368,376.70, so each 1% of supplier inflation is "
         "GBP 2,010.87 off the bottom line (5% = GBP 10,054; 10% = GBP 20,109). REQ-22 (AOV/smoke-vent "
         "scope) STILL OPEN. THE REAL CLIENT IS jLIVING - Chigwell bid to them 22/07, jLiving announce "
         "16/09, contract award mid-Oct, Go Live 30/10/2026, so silence until September is expected. "
         "NEW 27/07 pm: THE CLARIFICATION WINDOW IS SHUT. The 'Q&A' document in the pack turned out to be a "
         "Delta eSourcing Message Centre screenshot showing 'One item found' - just Vixus announcing the ITT "
         "went live on 02/06 - so no clarifications were ever logged and RFI-3 is unanswered. The ITT allows "
         "questions only up to 5 working days before the 22/07 return, via the Delta portal, and says 'Please "
         "DO NOT contact jLiving directly'. So all seven open RFIs (D_T, D_X, the AOV boundary, whose spec "
         "governs the U-value, the missing SAP and Edward Pearce consultant specs) are now POST-TENDER "
         "queries through Chigwell - variation territory, not clarification. ALSO NEW, from Adam's REQ-17 "
         "rulings on St Mary's applied here: MANIFESTATION is required by NBS L20 cl.280 ('Manifestation: As "
         "drawing') on the communal entrance doors and appears in NO schedule, NO elevation and NOT in our "
         "proposal - Adam's rule is to allow it and state it in the inclusions, so it is a gap; STRIP-OUT is "
         "'effectively left unanswered' here exactly as on St Mary's, and Adam's rule is that we would "
         "include it on a job of this size - Gordon Court is twice St Mary's size and replaces 40 existing "
         "windows, and our proposal excludes 'Waste Removal generally' while never naming it; ACCESS is fine "
         "- our proposal already states no access allowed, which is what Adam asked for. EARLIER FINDINGS "
         "STAND: GBP 723.87 omitted cost; D_T quoted 100mm taller than its opening as a double where the "
         "schedule shows a single leaf, in a Store whose external/internal cell is blank; 2no D_X external "
         "doors priced nowhere; 7no AOV/smoke-shaft units quoted as plain windows; trickle vents 4000mm2 "
         "against 8000mm2; acoustic vents ticked on 26 of 40 windows and quoted by nobody; PAS 24 absent "
         "from all four BSW quotes against an NBS clause requiring it on every window. CLEARED: install does "
         "cover the fire doors; three of four schedules reconcile unit-for-unit; the client workbook leaks "
         "no cost."
        )
        j['stage'] = 'submitted - awaiting jLiving 16/09; REQ-20 answered, REQ-22 open'

d['updated'] = '2026-07-27'
json.dump(d, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('REQ-20 recorded as answered; job entry refreshed')

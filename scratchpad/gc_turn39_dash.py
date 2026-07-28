# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'ANOTHER CLIENT\u2019S PAYMENT APPLICATION IS FILED IN THE GORDON COURT FOLDER'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-27')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + " - AND IN AT LEAST ONE OTHER. 28/07.\n\n"
 "Same class as the rest of this request - what is inside the things we hold and might send - so I am "
 "adding it here rather than raising a fourth.\n\n"
 "  5. Finance\Payment Applications\MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx\n\n"
 "It is a populated payment application for SHAFTESBURY SCHOOL, client BORRAS CONSTRUCTION - three sheets, "
 "244 cells, 81 numeric cells between minus 3,179.21 and 44,093.16. Contract figures, not a shell.\n\n"
 "It is filed in Chigwell's Gordon Court job folder. Riverside found the identical file in RRR's Riverside "
 "House folder tonight. SO IT IS NOT A MISFILE - the same third party's valuation is sitting in at least two "
 "different clients' job folders, which points at the folder skeleton rather than at anybody's slip.\n\n"
 "It has not been sent anywhere and nothing about it affects Gordon Court. The exposure is only that if a "
 "job folder is ever zipped and passed to a client, it travels with everything else in it.\n\n"
 "I HAVE NOT MOVED IT. OneDrive is read-only to me and how the company files its jobs is not something an "
 "estimating tool should reorganise. Flagged for a decision, like the rest of this request.\n\n"
 "AND I HAVE TO CORRECT MYSELF ON THE BOARD. Eight turns ago I checked this same folder for other jobs' "
 "documents and reported it clean. That was wrong, and the reason is worth more than the finding: my command "
 "filtered the FULL PATH against a list that included the word 'gordon', and the job folder is called Gordon "
 "Court - so it excluded every file in the job and returned nothing. A FILTER THAT EXCLUDES EVERYTHING "
 "RETURNS EXACTLY THE SAME OUTPUT AS A FOLDER THAT CONTAINS NOTHING.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-27 appended,', len(req['why']), 'chars')

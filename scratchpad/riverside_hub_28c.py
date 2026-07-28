# -*- coding: utf-8 -*-
"""Append this turn's finding to the Riverside hub entry."""
import collections
import io
import json

P = 'data/dashboard-state.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

ADD = (
    " *** 28/07 LATER - THE GBP 5,990.22 IS NOT DIVISIBLE BY TWO, AND STORAGE HAS A THREE-DAY "
    "CLOCK ON THE ONE JOB THAT IS WAITING ON SOMEBODY ELSE. *** Gordon Court found their own "
    "ten-category exclusions list was short by 'building regulations'. Mine had a different fault "
    "of the same family: last turn's sweep was DOCUMENT-DRIVEN, so it could only ever find "
    "categories A Plus chose to write about. Rebuilt as 25 categories listed BEFORE reading either "
    "document. Two came back live and unrecorded, both commercial rather than technical - which is "
    "why a compliance-shaped read had missed them. (1) A PLUS PRICE ON THE BASIS THAT THE "
    "MATERIALS ARE 'ordered together, and in one phase', and say a part order 'may incur "
    "additional charges' and should be re-priced. This file has described the price as 2 x a unit "
    "rate throughout - right as a build-up, WRONG as a statement of what one vent costs. It is "
    "live because of C2: if the second floor stairwell is vented at the roof rather than the wall, "
    "we order ONE unit and the remaining one is expressly subject to re-price. So the C2 exposure "
    "is the lost unit PLUS an unquantified re-price on the unit that stays. RFQ item 13 asks what "
    "a single vent would cost - asked BEFORE the architect answers rather than after. (2) STORAGE: "
    "'A Plus reserves the right to levy storage costs for all goods which remain uncollected 3 "
    "working days after first availability', and materials held off-site through a programme slip "
    "are excluded, with payment for the materials required against a letter of indemnity. Neither "
    "clause is unusual; what makes them matter is the defining fact of this job - the submission "
    "is deliberately held until PHDB report, the sequence is openings formed then survey then "
    "manufacture, and there is NO PROGRAMME DATE. THIS IS THE FIRST COST ON THIS JOB THAT GROWS "
    "WITH THE DELAY WE HAVE ACCEPTED. RFQ item 14 and a second reason under RRR question 11. Not "
    "quantified - no rate is stated and none invented. AND THEIR 'available on request' GREP RUN "
    "HERE COMES BACK CLEAN: zero hits for that whole family on QT51518, the only incorporations "
    "being the two named revisions already recorded. Reported clean, because a check that only "
    "ever fires is not one anybody trusts. THEIR CASE ALSO FOUND A DEFECT IN MY OWN RULE: BSW's "
    "quotes incorporate terms with no title, revision or date, and check_incorporated_terms_held "
    "graded that WORSE case as the LESSER one and handed back a remedy the estimator could not "
    "carry out. Fixed, six variants added, 35/35. THE RULE HAD 29 VARIANTS BEFORE IT SHIPPED AND "
    "STILL HAD A HOLE, BECAUSE ALL 29 WERE WRITTEN AGAINST THE SHAPE ON MY OWN QUOTE - variant "
    "count is not coverage, variant diversity is. RFQ now 14 items. Checks 0 failed, 4 questions. "
    "Position unchanged: GBP 5,990.22, unissued, nothing sent."
)

hit = 0
for j in d.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
if hit != 1:
    raise SystemExit('expected exactly one Riverside job entry, found %d' % hit)

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub updated')

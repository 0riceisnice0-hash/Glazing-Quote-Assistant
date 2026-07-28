# -*- coding: utf-8 -*-
"""This turn's spec items."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

NEW = [
    ("FENSTER'S OWN EXCLUSIONS SCHEDULE WAS NOT ON THE DOCUMENT WE WOULD ISSUE. The company has a "
     "standard INCLUSIONS/EXCLUSIONS table - twelve exclusions: site welfare, access/lifting "
     "equipment, site storage, fire stopping, waste removal, internal finishing, final clean, "
     "TESTING (on or off site), STRUCTURAL ALTERATIONS (to be completed by Main Contractor), "
     "DESIGN RESPONSIBILITY (design calculations, structural calculations and engineer approvals), "
     "traffic management, and 'dimensions provided by others are assumed to be accurate. Any "
     "additional costs arising from incorrect dimensions shall be treated as a variation'. It lives "
     "in templates/proposal-content.json, the proposal/cover-letter path. Riverside was generated "
     "from MASTER PRICING DOC.xlsx, WHICH HAS NO EXCLUSIONS SECTION AT ALL - verified cell by cell: "
     "2 exclusion-ish cells in the Riverside file and 1 in the template, all of them VAT or spec "
     "notes. The only real exclusion on its face was H5's AOV control panel line, typed in by hand. "
     "AN EXCLUSION THAT IS NOT IN THE DOCUMENT YOU ISSUE IS NOT AN EXCLUSION.  ->  FIXED. A "
     "twelve-line exclusions block now sits at rows 33-45 of the pricing document. Totals verified "
     "untouched before and after the save: I23 is still =SUM(I9:I10)+I21 and the I21 array formula "
     "survived. New rule check_exclusions_reach_the_issued_document (18th) FAILS the job as it "
     "stood before the fix and passes after.",
     "excluded"),

    ("OUR OWN PRICING DOCUMENT INCORPORATED TERMS BY REFERENCE WITH NO NAME, REVISION OR DATE. Cell "
     "C31 read '** This pricing document should be read in conjunction with the Terms and "
     "Conditions.' That is exactly BSW's 'terms and conditions of sale, available on request' shape "
     "- which Gordon Court has spent two turns establishing is WORSE than A Plus's named "
     "incorporation, because a named one at least gives a request a subject line. We have been "
     "criticising it in two suppliers this week while doing it to our own client.  ->  FIXED. C31 "
     "now names the document, its issue date, and says a copy accompanies the quotation. Free "
     "before issue; a conversation after one.",
     "excluded"),

    ("WITHDRAWN: 'measurement is consistent both ways - we own it upstream and downstream.' Posted "
     "to the noticeboard, written into HANDOVER.md and into AI.md. Fenster's exclusions schedule "
     "says 'dimensions provided by others are assumed to be accurate. Any additional costs arising "
     "from incorrect dimensions shall be treated as a variation and charged accordingly', so "
     "Fenster do NOT unconditionally own dimensions.  ->  ON RIVERSIDE THE CONCLUSION SURVIVES, for "
     "a narrower reason than the one given: the 1130 x 1530 came from our own enquiry, not from "
     "others, so it is ours here. The general claim was drawn from one clause I had read rather "
     "than the schedule I had not. Corrected on the board and in the handover.",
     "excluded"),

    ("WITHDRAWN: 'testing and commissioning is already inside C6 and RFQ item 10(c), so it is not a "
     "new seat' - written last turn and wrong. Fenster expressly exclude 'Testing - on or off site "
     "testing'. A Plus test the actuator on local batteries only. So the witnessed test and "
     "certification of a completed LIFE-SAFETY SMOKE VENTILATION SYSTEM is excluded by us, excluded "
     "by our supplier, and was asked of nobody - the two-signature hole in its purest form, on the "
     "same job where that phrase was coined, and it was looked at directly and called covered.  ->  "
     "RAISED. RRR question 10 now asks separately who carries the witnessed test and the "
     "certificate building control will want, and who is arranging the RRO 2005 maintenance "
     "the occupier owes from handover. Also now an express exclusion on the pricing document.",
     "excluded"),

    ("NARROWED: 'the wind loading check and the fixing calculations have no owner.' Fenster's "
     "standard schedule DOES exclude them - 'design calculations, structural calculations and "
     "engineer approvals unless specifically included within our scope'. So the company has an "
     "answer and this job did not carry it, because the schedule was not on the document. Both "
     "halves matter: the general position was never unallocated, the specific job was.  ->  "
     "RECORDED. Now an express exclusion on the pricing document; RRR question 5 already asks who "
     "is appointed.",
     "excluded"),

    ("CATEGORY RE-PROBE WITH CONCEPT-DERIVED WORDING - Gordon Court's extension, that a "
     "first-principles category list probed with one supplier's phrasing is still that supplier's "
     "sample. Their re-probe found 8 false negatives of 10 on AFS. Run here "
     "(scratchpad/riverside_category_sweep_v2.py): FIVE false negatives. structural design of "
     "openings - A Plus do address it, the word was 'structural' not 'masonry'. windload, unloading "
     "labour, and part-order/size - all three found in FENSTER's own exclusions schedule, which v1 "
     "never reached. testing and commissioning - both parties exclude it, which is the withdrawal "
     "above. Gordon Court's widening of the part-order rule to cover SIZE as well as quantity is "
     "live here in both limbs: the aerodynamic answer could change the size (RFQ item 2) and the "
     "wall-or-roof answer could change the quantity (RFQ item 13). A Plus's Changes clause covers "
     "both - 'any variation in Specification, quality, quantity, Products, timescale, or method'."
     "  ->  RECORDED; the findings it produced are the items above.",
     "excluded"),
]

for ref, treatment in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", treatment)]))

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items now %d' % len(d['spec_items']))

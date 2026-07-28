# -*- coding: utf-8 -*-
"""This turn's spec items. treatment must be priced/excluded/provisional -
the narrative goes in ref, which is the schema Grange Hill's rule enforces and
which caught this chat last turn."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

NEW = [
    ("THE PRICE IS NOT DIVISIBLE BY TWO. QT51518: 'The Price is based on the materials quoted "
     "being ordered together, and in one phase. Orders for only part of the quote, or fabrication "
     "over multiple phases, may incur additional charges for paint surcharges, rolling set up "
     "charges, reduced material optimisation, delivery or increased fabrication costs. We strongly "
     "recommend that when placing all such orders, a re-price is requested.' Every description of "
     "this price so far has been 2 x a unit rate (2,422.61 + 412.50 = 2,835.11, x2, plus 160 "
     "install each) - correct as a build-up, wrong as a statement of what one vent costs. LIVE "
     "because of C2: if the second floor stairwell is vented at the roof rather than the wall, we "
     "order ONE unit from this quotation and A Plus expressly reserve the right to re-price the "
     "remainder. The exposure on C2 is therefore the lost unit PLUS an unquantified re-price on the "
     "one that stays.  ->  RAISED as RFQ item 13, asking what a single 1130 x 1530 vent to this "
     "specification would cost - before the architect answers C2 rather than after.",
     "excluded"),

    ("STORAGE HAS A THREE WORKING DAY CLOCK ON THE ONE JOB THAT IS WAITING ON SOMEBODY ELSE. "
     "QT51518: 'A Plus reserves the right to levy storage costs for all goods which remain "
     "uncollected 3 working days after first availability for collection/delivery', and 'Materials "
     "off Site: this quotation does not include for holding of materials off-site... In such cases "
     "upon receipt of a suitable letter of indemnity we would require payment for such materials.' "
     "Neither clause is unusual. What makes them live is the defining fact of this job: Adam is "
     "holding the submission until PHDB return building-works costs, the sequence is openings "
     "formed -> survey -> manufacture, and there is no programme date for forming the openings. A "
     "slip starts a storage clock three working days after manufacture and converts the balance "
     "into payment-before-delivery against a letter of indemnity. THE FIRST COST ON THIS JOB THAT "
     "GROWS WITH THE DELAY ADAM HAS DELIBERATELY ACCEPTED.  ->  RAISED as RFQ item 14 (how the "
     "three days run, and whether there is a normal holding arrangement) and as a second reason "
     "under RRR question 11 for giving a programme date. Not quantified - no rate stated on the "
     "quote and none invented.",
     "excluded"),

    ("Gordon Court's 'available on request' grep, run on QT51518 - CHECK RUN, CLEAN. Probed for "
     "'available on request', 'on request', 'subject to our standard', 'conditions of sale', "
     "'standard terms', 'as amended': all zero. 'Terms of Sale' returns four hits, all of them the "
     "named V.01.2 - 08.01.2018 / V.01 - 03.11.2017 already recorded. No further incorporation by "
     "reference on this quotation. One detail kept and not raised: the payment basis itself points "
     "into the unheld document - 'Deposit and cleared Funds Prior to delivery on first order (see... "
     "Terms of Sale Revision V.01.2 for more information)' - but A Plus are an established supplier "
     "here rather than a first order.  ->  REPORTED CLEAN. A check that only ever fires is not one "
     "anybody trusts.",
     "excluded"),

    ("Category-completeness sweep of 25 categories, built independently of both documents "
     "(scratchpad/riverside_category_sweep.py) after Gordon Court found their own ten-category list "
     "short by 'building regulations'. The fault here was different but the same family: last "
     "turn's sweep was DOCUMENT-driven, so it could only find categories A Plus chose to write "
     "about. Making good and testing/commissioning appear in neither document; testing and "
     "commissioning is already inside C6 and RFQ item 10(c) so it is not a new seat, and making "
     "good around a newly formed opening sits in the building-works package RRR question 5 already "
     "asks about.  ->  RECORDED, not raised as new items. The two that WERE new are the phased-order "
     "and storage findings above.",
     "excluded"),
]

for ref, treatment in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", treatment)]))

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items now %d, treatments %s'
      % (len(d['spec_items']), sorted(set(s['treatment'] for s in d['spec_items']))))

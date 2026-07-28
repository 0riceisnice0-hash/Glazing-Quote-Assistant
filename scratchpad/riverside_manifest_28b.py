# -*- coding: utf-8 -*-
"""Add this turn's spec items to the Riverside manifest."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

NEW = [
    ("PART B COMPLIANCE IS NOT BACK TO BACK - a plus put it on us, our clause 16 disclaims it "
     "to the client. QT51518 Product Performance: \"It is the responsibility of the Customer to "
     "ensure all building regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N' and any others relevant "
     "to the building)... are adhered to. The Supplier does not warrant or represent that any "
     "Product supplied shall comply with any of the aforementioned standards unless where "
     "expressly stated to the contrary by the Supplier.\" Our clause 16 disclaims regulatory "
     "strategy and relies on the client's professional team. Part B is not an incidental "
     "attribute of an AOV smoke vent - it is the entire function of the product, so the one "
     "regulation it exists to satisfy is the one disclaimed upstream and accepted downstream. "
     "Bites directly on C0/C1: if the 1m2 is aerodynamic, 1.30m2 geometric gives ~0.78-0.81m2 "
     "and the shortfall is ours. Verified at source on page 3 of QT51518 and in "
     "templates/proposal-content.json clause 16.",
     "RAISED, and the remedy is pre-order and free. The clause reads 'unless where expressly "
     "stated to the contrary by the Supplier', so RFQ items 1 and 4 now ask A Plus to state the "
     "aerodynamic free area, the EN 12101-2 classification and the whole-window Uw ON the revised "
     "quotation rather than by reply - an express statement by the Supplier is what the clause "
     "turns on. Flagged to Adam in the covering note. Measurement and maintenance checked in the "
     "same pass and are consistent both ways - recorded as clean, not claimed as gaps."),

    ("QT51518 INCORPORATES A TERMS OF SALE WE HAVE NEVER HELD. The advisory notes say the "
     "'A Plus Windows & Doors Limited Terms of Sale Revision V.01.2 - 08.01.2018' apply to the "
     "quotation and to any subsequent Contract, and that the definitions - including who the "
     "'Customer' is in every responsibility clause - come from 'Revision V.01 - 03.11.2017'. "
     "Neither is attached. Checked the archive rather than assuming: six files in the whole "
     "Commercial archive have 'Terms of Sale' in the name (Bradford Watts, Elkins, HouseUP, "
     "Prince Build, Stepnell, Conamar) and all six are the same Quotation Advisory Notes_Jan2019 "
     "PDF, which is the summary and not the terms. Diffed that 2019 file against QT51518's "
     "advisory pages - 0.75 sentence similarity, the only substantive change in seven years being "
     "frames splitting at 5m rather than 4m.",
     "RAISED as RFQ item 11, asking for both documents. Also turned into a rule: "
     "check_incorporated_terms_held, registered as the seventeenth check, with 29 variants "
     "written before it shipped and persisted into --selftest. An incorporation by reference "
     "reads as though the terms are settled and hides that you cannot say what they are - unlike "
     "a quote with no terms at all, which is a gap you can see."),

    ("THE 1.30m2 GEOMETRIC IS A BARE-VENT FIGURE. QT51518 page 5: 'The output free area values do "
     "not allow for any obstructions, side walls, reveals or neighbouring vents.' Both vents sit "
     "in a reveal in existing masonry on a 155mm subcill. This is the first thing found that could "
     "erode the geometric margin itself - the 30% headroom over 1m2 has been treated as "
     "comfortable and it is headroom against an unobstructed number. Not quantified here and not "
     "guessed at.",
     "RAISED in RFQ item 1, asking whether the 1.30m2 changes once installed in a reveal and "
     "whether the figure quoted is the bare vent or the installed opening."),

    ("THE WIND LOADING CHECK AND THE FIXING CALCULATIONS HAVE NO OWNER. QT51518: mullion selection "
     "calculated to BS 6399 Part 2 'with a design windload of 1200Pa unless otherwise stated'; "
     "'all design responsibility remains with the Customer and our calculations are not to be "
     "relied on for any design purposes whatsoever'; the Customer should carry out their own full "
     "wind loading check and 'undertake full structural calculations on all brackets/spigots "
     "supplied by A Plus'; fixing lugs, bolts and brackets are excluded. Our clause 16 limits us "
     "to measurement verification, supply and installation, and no structural engineer is named on "
     "any of the six drawings. So on a second floor elevation neither the check nor the fixing "
     "design is anybody's.",
     "RAISED both ways: RFQ item 12 asks A Plus to confirm 1200Pa is the figure used and what "
     "fixing components are included; RRR question 5 now asks who is carrying the wind loading "
     "check and the fixing calculation, or whether a structural engineer is to be appointed. "
     "Compounds the existing structural-design gap rather than being a new seat."),

    ("'Actuators to EN 12101-2 are not formally weather tested' (QT51518 page 5).",
     "CONSIDERED AND DECLINED, recorded so nobody re-derives it. These vents are the only opening "
     "in those stairwells and nothing in the pack sets a weather-tightness requirement against "
     "them, so there is no standard to test the statement against. Revisit only if a performance "
     "spec appears."),
]

for ref, treatment in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", treatment)]))

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items now %d' % len(d['spec_items']))

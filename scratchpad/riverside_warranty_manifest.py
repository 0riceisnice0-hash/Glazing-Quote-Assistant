# -*- coding: utf-8 -*-
"""The four-part comparison, done properly, into the manifest.

Last turn recorded the PERIOD and the CYCLE CAP. This adds the two parts of
Gordon Court's check that had never been run here - the START DATE and the
EXCLUSION LIST - and one correction to my own headline.
"""
import io, json, collections

P = 'data/job-checks/riverside-house-aov.json'
m = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

m["warranty"] = collections.OrderedDict([
    ("ours", collections.OrderedDict([
        ("document", "Fenster Standard Terms and Conditions, 'Guarantee and Warranty'"),
        ("period", "10 years"),
        ("period_months", 120),
        ("scope", "all glass and frame products supplied and installed by the company - "
                  "defects in materials (as supplied) and workmanship (installation)"),
        ("scope_note", "AN ACTUATOR IS NEITHER GLASS NOR A FRAME. The clause may not reach the "
                       "one component this product exists to operate. Both readings are bad and "
                       "they are bad differently: on the narrow reading the client gets ten "
                       "years on the box and nothing stated on the mechanism of a life-safety "
                       "system; on the reading a client will actually take, we owe ten years on "
                       "a part we are given twelve months on. Last turn's 'nine-year gap' "
                       "assumed the wider reading without checking it."),
        ("start_date", None),
        ("start_date_note", "THE CLAUSE STATES NO START DATE AT ALL. The only 'from the date of' "
                            "in the whole terms document is the 30-day quotation validity. Ten "
                            "years from what is not stated anywhere. Gordon Court's cl.5 has the "
                            "identical defect and neither of us saw it while comparing years."),
        ("usage_cap", None),
        ("exclusions", ["misuse",
                        "accidental or intentional damage",
                        "vandalism",
                        "inadequate or incorrect maintenance",
                        "external factors, including severe weather conditions"]),
        ("saving_clause", "'subject to the terms and conditions of any applicable manufacturer "
                          "warranties' - it qualifies the ten years, it does not close the gap"),
    ])),
    ("suppliers", [
        collections.OrderedDict([
            ("supplier", "A Plus Windows & Doors"),
            ("ref", "QT51518"),
            ("covers", "SE Controls products, frames and finishes"),
            ("period", "twelve months"),
            ("period_months", 12),
            ("start_date", "the date of delivery completion"),
            ("start_date_note", "All orders are priced Ex-Works and this order is GBP 154.78 "
                                "under the free-delivery threshold, so 'delivery completion' is "
                                "goods arriving at us, not at practical completion. A Plus also "
                                "levy storage on anything uncollected 3 working days after first "
                                "availability - SO THE STORAGE CLOCK AND THE WARRANTY CLOCK PULL "
                                "IN OPPOSITE DIRECTIONS. Leave the goods and pay storage; take "
                                "them and start burning the client's cover. Award is gated on "
                                "PHDB's building-works costs, so the gap is not small."),
            ("usage_cap", None),
            ("exclusions", [
                collections.OrderedDict([
                    ("exclusion", "'No warranty is extended on the adhesion of the powder coat "
                                  "to the polyamide' where the thermal break is coated"),
                    ("counterpart_in_ours", None)]),
                collections.OrderedDict([
                    ("exclusion", "non-standard ironmongery 'may affect our programme and "
                                  "NULLIFY ANY SYSTEM OR PERFORMANCE WARRANTY on that product'"),
                    ("counterpart_in_ours", None)]),
                collections.OrderedDict([
                    ("exclusion", "'The Supplier does not warrant or represent that any Product "
                                  "supplied shall comply with' Part B, F, L, M, N, Lifetime "
                                  "Homes, Secured by Design or PAS 24"),
                    ("counterpart_in_ours", None)]),
            ]),
            ("exclusions_complete", False),
            ("exclusions_incomplete_because",
             "A Plus never wrote an exclusion LIST. These are conditional clauses found in "
             "Finishes, Hardware and Product Performance - three different sections of an "
             "advisory-notes page. The rest are in Terms of Sale Revision V.01.2, which nobody "
             "has ever requested. The list above is a floor."),
        ]),
        collections.OrderedDict([
            ("supplier", "A Plus Windows & Doors"),
            ("ref", "QT51518"),
            ("covers", "the actuators"),
            ("period", "15,000 cycles or 12 months, whichever is sooner"),
            ("period_months", 12),
            ("start_date", "the date of delivery completion"),
            ("usage_cap", "15,000 cycles or 12 months, whichever is sooner"),
            ("usage_cap_note", "ARITHMETIC, BECAUSE I LED WITH THIS LAST TURN AND SHOULD NOT "
                               "HAVE. Weekly testing under the RRO is 52 cycles a year, so "
                               "15,000 cycles is about 288 years. 'Whichever is sooner' means "
                               "the cycle cap can only bite before the twelve months at 41 "
                               "operations a day. IT IS THE TWELVE MONTHS THAT BITES, ALWAYS. "
                               "The cap is worth one line in the RFQ, not three findings."),
            ("exclusions", [
                collections.OrderedDict([
                    ("exclusion", "actuators 'must be installed in accordance with the "
                                  "manufacturers instructions' - which we do not hold, and we "
                                  "are the installer"),
                    ("counterpart_in_ours", None)]),
                collections.OrderedDict([
                    ("exclusion", "actuators 'must be powered by a compatible control system "
                                  "which is APPROVED BY SE CONTROLS to provide suitable power "
                                  "management and where necessary, RECORD ACTUATOR OPERATION "
                                  "CYCLES' - a panel nobody has bought, priced or specified"),
                    ("counterpart_in_ours", None)]),
                collections.OrderedDict([
                    ("exclusion", "no restrictor fitted: 'A Plus will not be liable for any "
                                  "replacement actuators or damage to the vent'"),
                    ("counterpart_in_ours", "accidental or intentional damage")]),
                collections.OrderedDict([
                    ("exclusion", "'Actuators to EN 12101-2 are not formally weather tested'"),
                    ("counterpart_in_ours", "external factors, including severe weather "
                                            "conditions")]),
            ]),
            ("exclusions_complete", False),
            ("exclusions_incomplete_because",
             "Same page, same unheld Terms of Sale. Note which two DO match: they match because "
             "our exclusion is equally wide, which protects Fenster and leaves the client "
             "uncovered at both levels. A matched exclusion is not automatically a good result."),
        ]),
    ]),
    ("_diff", "FIVE of SEVEN recorded supplier exclusions have no counterpart in ours. The two "
              "that match, match by both parties excluding the same thing. Two of the five are "
              "operational rather than academic - the installation instructions and the "
              "SE Controls-approved control panel - and BOTH ARE SENTENCES ALREADY QUOTED IN THE "
              "RFQ, at items 7 and 9, for SCOPE AND PRICE. Quoting a sentence for one purpose "
              "certifies it as read for all purposes."),
])

EXP = collections.OrderedDict([
    ("item", "THE ACTUATOR WARRANTY DEPENDS ON A CONTROL PANEL NOBODY HAS BOUGHT. A Plus require "
             "actuators to be 'powered by a compatible control system which is approved by SE "
             "Controls' and, where necessary, to record operation cycles. The panel is outside "
             "A Plus's price, outside ours, and C10 to RRR asks who is carrying it. So the "
             "twelve months on the only moving part of a life-safety system is conditional on "
             "equipment specified, bought and installed by a third party we have not identified "
             "- and the 15,000-cycle limit is only ever provable by a panel that counts cycles."),
    ("lands_on", "Fenster. We offer the client ten years; A Plus's twelve months on the actuator "
                 "can be voided by somebody else's panel selection, and we would still owe the "
                 "client whatever our own clause is read to cover."),
    ("our_recourse", "NONE AS THINGS STAND, and the reason is that the condition sits in a "
                     "sentence we had already quoted for a different purpose. RFQ item 9 quotes "
                     "it while asking A Plus to price a panel; it never says the guarantee "
                     "depends on it. Item 9 now asks A Plus to name the approved panels and "
                     "confirm what happens to the guarantee if another is used, and question 10 "
                     "to RRR now tells whoever carries the panel that the actuator warranty "
                     "rides on their selection. Until one of those is answered the recourse is a "
                     "question, not a right."),
])
m["exposures"].append(EXP)

EXP2 = collections.OrderedDict([
    ("item", "OUR TEN YEARS HAS NO START DATE AND THEIRS STARTS AT DELIVERY. Fenster's Guarantee "
             "clause states a period and never says from when - the only 'from the date of' in "
             "the whole terms document is the 30-day quotation validity. A Plus's twelve months "
             "runs 'from the date of delivery completion', ex-works, on an order below their "
             "free-delivery threshold, against a storage charge that starts 3 working days after "
             "the goods are available."),
    ("lands_on", "Fenster, in both directions. An undated ten years is construed against the "
                 "party who wrote it, so the client can start it late; A Plus's twelve months "
                 "starts as early as possible, and award is gated on PHDB's building-works "
                 "costs, so the goods can sit while the cover runs."),
    ("our_recourse", "None yet, and both halves are ours to fix rather than anyone's to answer. "
                     "The house terms need a start date - that is Adam's call on a document used "
                     "on every job, not this one. On A Plus, RFQ item 14 now asks whether the "
                     "twelve months can run from installation or handover rather than delivery, "
                     "which is the cheapest version of the question and has never been asked."),
])
m["exposures"].append(EXP2)

for s in [
    ("warranty start date, ours",
     "Fenster's 10-year warranty states no start date. Recorded as a defect in our own document, "
     "not a priced item.", "excluded"),
    ("warranty start date, A Plus",
     "Twelve months from 'the date of delivery completion', ex-works Watford, on a GBP 4,845.22 "
     "order below the GBP 5,000 free-delivery threshold.", "excluded"),
    ("actuator control system approval",
     "Actuators must be powered by an SE Controls-approved control system that records operation "
     "cycles. Panel not in our scope and not in A Plus's price - C10 open with RRR.", "excluded"),
    ("non-standard ironmongery warranty nullification",
     "A Plus: non-standard items may nullify any system or performance warranty on that product. "
     "Whether an SE Controls AOV actuator counts as standard for a DualFrame 75Si is asked at "
     "RFQ item 14.", "excluded"),
]:
    m["spec_items"].append(collections.OrderedDict([
        ("item", s[0]), ("ref", s[1]), ("treatment", s[2])]))

io.open(P, 'w', encoding='utf-8', newline='').write(
    json.dumps(m, indent=2, ensure_ascii=False) + "\n")
print('manifest: %d spec items, %d exposures, warranty field added'
      % (len(m["spec_items"]), len(m["exposures"])))

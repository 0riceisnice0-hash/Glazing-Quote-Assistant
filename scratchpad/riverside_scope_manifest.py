# -*- coding: utf-8 -*-
"""Gordon Court's scope check, run against Riverside's own schedule.

They found thirteen classes of gear on 227 units, four of them life-safety, none
of them a glass product or a frame product. Two units here, so the list is
short - but the ratio is worse, because on this job the gear IS the product. A
DualFrame 75Si that will not open is not a defective smoke vent, it is a window.
"""
import io, json, collections

P = 'data/job-checks/riverside-house-aov.json'
m = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

m["warranty"]["scope_vs_schedule"] = collections.OrderedDict([
    ("_note", "Gordon Court, 28/07: check the scope clause against the schedule on every job. "
              "The word to look for is not 'years', it is the noun the warranty attaches to. "
              "Taken line by line off QT51518's specification block."),
    ("ours_attaches_to", "glass and frame products"),
    ("a_plus_attaches_to", "products manufactured and sold by SE Controls"),
    ("components", [
        {"component": "aluminium frame, transom, sash, bead, 15mm head add-on",
         "ours": "covered", "a_plus": "NOT STATED"},
        {"component": "glass, 4-20-4 Clr Tough S Coat 1.2 / 20mm blk warmedge",
         "ours": "covered", "a_plus": "NOT STATED"},
        {"component": "AOV Type 850mm Stroke Single - the actuator",
         "ours": "NOT COVERED - neither glass nor a frame",
         "a_plus": "12 months / 15,000 cycles, conditional on instructions and an approved panel"},
        {"component": "Friction stay: Etched Silver BUTT HINGE",
         "ours": "NOT COVERED - neither glass nor a frame",
         "a_plus": "NOT STATED - not an SE Controls product",
         "note": "IN NEITHER WARRANTY. It carries a 1130 x 1530 outward-opening glazed sash at "
                 "the top storey. Gordon Court's egress hinges are the same class of item and "
                 "the same gap."},
        {"component": "Gasket (Standard)",
         "ours": "NOT COVERED", "a_plus": "NOT STATED - not an SE Controls product",
         "note": "IN NEITHER WARRANTY. Weather performance on an external vent turns on it."},
        {"component": "AOV cable / flex, approx 2m coiled at the vent",
         "ours": "NOT COVERED", "a_plus": "arguably an SE Controls product, not stated"},
        {"component": "Cill: 155mm Subcill (TECHNAL)",
         "ours": "arguable - a subcill may or may not be a 'frame product'",
         "a_plus": "NOT STATED - and it is a Technal component in a Sapa DualFrame system",
         "note": "A cross-manufacturer item. Whose warranty it sits under is stated by nobody."},
        {"component": "powder coat on the polyamide thermal break",
         "ours": "COVERED as 'defects in materials (as supplied)'",
         "a_plus": "EXPRESSLY EXCLUDED - 'no warranty is extended'",
         "note": "THE ONLY ROW WHERE WE POSITIVELY COVER WHAT THEY POSITIVELY EXCLUDE. "
                 "Everywhere else it is silence meeting silence."},
    ]),
    ("_finding", "FOUR COMPONENTS SIT OUTSIDE BOTH SCOPE CLAUSES AT ONCE - the hinges, the "
                 "gasket, the cill and (on the narrow reading) the actuator. Not because either "
                 "party excluded them, but because our clause attaches to 'glass and frame "
                 "products' and A Plus's attaches to 'products manufactured and sold by SE "
                 "Controls', and these fall between the two nouns. Gordon Court's 13-of-13 is "
                 "wider; this is worse in kind, because on an AOV the gear is not an accessory "
                 "to the product, it IS the product. Ten years on 100% of what makes it a "
                 "window and nothing on what makes it a smoke vent."),
    ("_inverse_not_available", "AFS give Gordon Court ten years on 'mechanical aspects' - "
                               "supplier cover they had never passed on. There is no equivalent "
                               "here BECAUSE A PLUS STATE NO FRAME OR GLASS WARRANTY AT ALL. So "
                               "the inverse is not unavailable, it is unasked: for all we know "
                               "A Plus give more than twelve months on the aluminium and we have "
                               "been passing on less than we hold. RFQ 14(h) now asks by class."),
])

for e in [
    collections.OrderedDict([
        ("item", "FOUR COMPONENTS ARE IN NEITHER WARRANTY. Our clause attaches to 'glass and "
                 "frame products'; A Plus's attaches to 'products manufactured and sold by SE "
                 "Controls'. The butt hinges, the gasket, the Technal subcill and - on the "
                 "narrow reading - the actuator fall between the two nouns. The hinge carries "
                 "an outward-opening glazed sash at the top storey."),
        ("lands_on", "Fenster on the client side, because we are the name on the ten years and "
                     "the client will read the vent as one product. Nobody on the supplier side, "
                     "because A Plus have not said anything about these components either way."),
        ("our_recourse", "None stated by anyone, which is the whole point - this is not an "
                         "exclusion either party wrote, it is a gap between two nouns. RFQ 14(h) "
                         "asks A Plus for the period by class of component, naming the hinges. "
                         "The wording of our own scope clause is Adam's, not mine, and it is on "
                         "every job rather than this one."),
    ]),
    collections.OrderedDict([
        ("item", "WE HOLD NO LEAD TIME. QT51518 states none; A Plus's notes say lead times "
                 "'will be confirmed on receipt of written order' and that otherwise products "
                 "are supplied 'in a reasonable timeframe'. Our own terms price installation "
                 "'as per final agreed programme'. And their Changes clause lets them vary the "
                 "price for a variation in TIMESCALE, on the one job in the book that is "
                 "explicitly on hold."),
        ("lands_on", "Fenster. We would be agreeing a programme with RRR against a supplier "
                     "commitment of 'a reasonable timeframe', and a delay we did not cause could "
                     "re-open the price under a clause separate from the 30-day acceptance and "
                     "the one-phase re-price."),
        ("our_recourse", "Our Supplier Delays clause covers additional costs caused by a "
                         "third-party supplier, and Installation is priced against the final "
                         "agreed programme - so the exposure is bounded once there is an order "
                         "on our terms. Before one, none. RFQ item 15 asks for the lead time "
                         "from written order, how much of it is the actuator, and what would "
                         "trigger a re-price on timescale grounds. NEVER ASKED IN THIRTY-ONE "
                         "TURNS - we have quoted a client a programme against a supplier who "
                         "has committed to no date."),
    ]),
]:
    m["exposures"].append(e)

for item, ref in [
    ("butt hinges (Etched Silver friction stay)",
     "In neither warranty - not a glass or frame product for us, not an SE Controls product "
     "for A Plus. RFQ 14(h)."),
    ("gasket (Standard)", "In neither warranty. Weather performance turns on it."),
    ("155mm Technal subcill",
     "Cross-manufacturer item in a Sapa system; warranty stated by nobody. RFQ 14(h)."),
    ("lead time", "Not stated on QT51518 and never asked. A Plus confirm lead times only on "
                  "receipt of written order. RFQ item 15."),
    ("timescale re-pricing right",
     "A Plus's Changes clause permits a price variation for a variation in timescale, distinct "
     "from the 30-day acceptance and the one-phase clause. Job is on hold. RFQ item 15."),
    ("3000mm between handed vents",
     "A Plus: 'Handed windows should not be positioned within approximately 3000mm of each "
     "other, as free area may be affected.' Second free-area qualifier; vents are in separate "
     "stairwells so expected academic. RFQ item 16(a)."),
    ("offset chain / reduced weather performance",
     "A Plus: on certain frame sizes the actuator body is centred, the chain offset, giving "
     "less compression between sash and frame and 'potentially a reduced weather performance'. "
     "Whether 1130 x 1530 is such a size is unasked. RFQ item 16(b)."),
    ("protective taping",
     "Not supplied taped unless stated; approx GBP 1 per linear metre. Relevant only if goods "
     "are held between delivery and installation. RFQ item 16."),
]:
    m["spec_items"].append(collections.OrderedDict([
        ("item", item), ("ref", ref), ("treatment", "excluded")]))

io.open(P, 'w', encoding='utf-8', newline='').write(
    json.dumps(m, indent=2, ensure_ascii=False) + "\n")
print('manifest: %d spec items, %d exposures, scope_vs_schedule added'
      % (len(m["spec_items"]), len(m["exposures"])))

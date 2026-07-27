# -*- coding: utf-8 -*-
"""Second-turn update to the Gordon Court checks manifest.

Prompted by riverside's AOV free-area handoff. Adds the NBS specification's own
requirements and riverside's new delivery_terms field.
"""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'job-checks', 'gordon-court.json')
m = json.load(io.open(P, encoding='utf-8'))

m['_note'] += (" SECOND TURN 27/07 evening, prompted by riverside's AOV free-area handoff: added the NBS "
               "specification's own requirements (L10 cl.330 Windows, L10 cl.205 certification, L20 cl.280 "
               "Communal Main Entrance Door, L20 cl.630 Colt smoke ventilation) and delivery_terms per "
               "riverside's new rule.")

m['delivery_terms'] = [
 {"supplier": "BSW Window Solutions", "ref": "QT252247 / QT252248 / QT252251 / QT252257",
  "order_value": 183005.42, "free_delivery_threshold": None, "delivery_priced": "provisional",
  "note": "EVERY BSW QUOTE SAYS EX WORKS: 'All estimates are ex works, additional delivery charges may "
  "apply.' No threshold and no distance rule is stated, so unlike A Plus on Riverside there is no figure "
  "to test GBP 183,005.42 against - carriage is simply unpriced. Note also the Delivery Address on all "
  "four quotes is FENSTER'S OWN YARD (98 Alston Drive, Bradwell Abbey, Milton Keynes MK13 9HF), not the "
  "site, so carriage from Milton Keynes to Edgware HA8 on 227 units is ours as well. The workbook carries "
  "no carriage line at all - install (GBP 46,840) is pure per-unit labour codes. Ask BSW for their "
  "delivery basis and threshold in writing."},
 {"supplier": "Aluminium Fire Systems", "ref": "Q7585",
  "order_value": 18298.94, "free_delivery_threshold": None, "delivery_priced": False,
  "note": "DELIVERY IS A PRICED EXTRA OF GBP 250.00 ON p7 AND IS NOT IN THE TENDER - already recorded "
  "under supplier_quotes. The quote contradicts itself: its Specifics page says 'Logistics: Delivered' "
  "while p7 prices delivery as an optional extra. T&C 8.1 settles it against us - price is 'exclusive of "
  "all costs and charges of packaging, insurance and transport of the Goods, which will be itemised "
  "separately if applicable and invoiced to the Customer in addition'. Delivery Location is again "
  "Fenster's own MK13 9HF yard, not site."}]

sp = m['spec_items']
sp[:] = [i for i in sp if 'free area' not in i['ref']]

sp.insert(3, {
 "ref": "WN_7 (3no) marked 'AOV' and WL_1 (4no) 'Louvres to smoke shaft' on schedule 52003 - the smoke "
        "ventilation function itself",
 "treatment": "GAP - quoted as ordinary windows, no AOV mechanism priced at all",
 "evidence":
 "THE WHOLE OF QT252257 (GBP 7,085.76 cost, GBP 10,055.76 sell) IS THIS PACKAGE, AND NONE OF IT IS PRICED "
 "AS SMOKE-CONTROL EQUIPMENT. Schedule 5244-ARK-52003 carries the heading 'AOV SMOKE SHAFT LOUVRE' and the "
 "note 'WL_00 Louvres to smoke shaft'. WN_7 x3 sit at Corridor 1-1, 1-2 and 1-3 (levels 1-3), 2100 high x "
 "910 wide, with 'AOV' in the additional-information column. WL_1 x4 sit at levels 0-3, 2100 x 1210. "
 "NBS 9001 L20 clause 630 specifies these as COLT PROPRIETARY SMOKE-CONTROL PRODUCTS, every one motorised: "
 "'COLTITE GLAZED LOBBY VENTILATOR (STAIR C) - mounted into prepared openings in the external wall, Type "
 "CLT, double glazed with thermally broken glazing and outer frames, nominal size 1000mm wide x 2000mm high "
 "or equivalent, DRIVE OPEN/DRIVE CLOSE USING A 24V MOTOR MOUNTED TO THE REAR' (WN_7 at 910 x 2100 is that "
 "item's 'or equivalent'); and 'EN SEEFIRE LOUVRED NATURAL VENTILATOR - size to match shaft dimensions, "
 "clear opening louvred natural ventilator... DESIGNED AND TESTED TO EN 12101-2... the position of the "
 "louvres is controlled by a 24Vdc ELECTRIC ACTUATOR, driven closed by this actuator and opened by a "
 "spring'. "
 "BSW QUOTED NEITHER. QT252257 quotes 'Qty: 3 Prestige T&T' and 'Qty: 4 Prestige Casement' - ordinary "
 "Sheerline windows - and the quote contains ZERO occurrences of AOV, louvre, actuator, chain, stroke, "
 "motor, 24V or smoke. WL_1's Glazing line is BLANK and it carries no reinforcing. There is no actuator, no "
 "24V motor, no fire-alarm interface, no control gear and no EN 12101-2 certification anywhere in the price. "
 "THE RATES CONFIRM IT: WN_7 is GBP 412.67/m2 over 5.733 m2 and WL_1 is GBP 442.98/m2 over 10.164 m2 - "
 "plain-window money. Riverside's only AOV data point (A Plus DualFrame 75Si bottom-hung glazed AOV, 850mm "
 "stroke single chain) is GBP 1,401.24/m2 supply, of which the actuator and AOV sash carry roughly GBP "
 "870/m2. On that one point the 3no WN_7 alone are GBP 4,988 to GBP 5,667 of supply cost short. ONE QUOTE, "
 "A DIFFERENT SYSTEM, ORDER OF MAGNITUDE ONLY - riverside also confirmed there is no AOV or smoke-vent "
 "category anywhere in the rate register, so the 4no louvres cannot be benchmarked at all. Either these 7 "
 "units are ours and materially under-priced, or they belong to the smoke-vent specialist and GBP 10,055.76 "
 "of sell should come out - our proposal p3 names 'AOV windows, smoke shaft louvres' as part of the tender "
 "information and neither prices the function nor excludes it."})

sp.insert(4, {
 "ref": "Free area - GEOMETRIC vs AERODYNAMIC (riverside's question, answered)",
 "treatment": "GAP - the pack states geometric, the quote states neither",
 "evidence":
 "THE GOOD NEWS: THIS PACK IS WRITTEN GEOMETRIC, so riverside's ~40% aerodynamic trap does not bite here. "
 "NBS L20 clause 630 states 'AXS140 STAIRWELL VENTILATOR - throat dimensions 1250mm x 1000mm - 1m2 "
 "GEOMETRIC free area' and 'AXS140 LOBBY VENTILATOR - throat dimensions 1250mm x 1500mm - 1.5m2 GEOMETRIC "
 "free area', both '24V electric actuator'. The word aerodynamic appears NOWHERE in the 186-page NBS, and "
 "the only aerodynamic reference in the 140-page mech spec (22190_Mech Spec_00 p80) is about attenuator "
 "fairings - nothing to do with vents. The 127-page electrical spec has none. "
 "THE BAD NEWS: BSW STATE NO FREE AREA OF EITHER KIND on QT252257, so there is nothing to compare against "
 "the requirement. And the Seefire louvre requirement is relative rather than absolute - 'size to match "
 "shaft dimensions' against an 'AOV SHAFT' the same clause says 'should have a minimum cross sectional area "
 "of 1.5m2' - so the 4no smoke shaft louvres have to deliver against a 1.5m2 shaft and nobody has shown "
 "that they do. Per riverside: do NOT derive one figure from the other or from frame area - Towcester's "
 "geometric/frame ratios were 75% and 54%, it does not scale. Make the supplier state it."})

for i in sp:
    if i['ref'].startswith('PAS 24 2016'):
        i['ref'] = ("PAS 24 - required by NBS L10 clause 330 on ALL windows, plus the schedules' PAS24 SBD "
                    "note and 51001's PAS 24 2016 column")
        i['evidence'] = (
         "MUCH STRONGER THAN A SCHEDULE NOTE - IT IS A SPECIFICATION STANDARD CLAUSE. NBS 9001 L10 clause "
         "330 'Windows & Roof Windows' reads '1. Standard: To BS6375-1, BS6375-2, BS6375-3, EN 14351-1 and "
         "Pas24.' So PAS 24 applies to EVERY window, not only the amenity-deck ones the schedule note names. "
         "Clause 205 adds 'Third-party certification: Submit proposals / Verification: Independent, 3rd Party "
         "Certification Schemes / Submittals: Submit documentation confirming Certifications claimed'. NBS L20 "
         "clause 280 independently requires the communal entrance doors 'To BS 4873 and PAS24' with "
         "'Third-party certification: Tested to PAS24'. AGAINST THAT: ZERO occurrences of 'PAS 24' or 'PAS24' "
         "across all four BSW quotes, and none of BS 6375-1/2/3 or EN 14351-1 is mentioned either. Yale "
         "Shootbolt locks, Egress Hinges and 35x35mm security cylinders are quoted, but no certification and "
         "no submittals.")

sp.append({
 "ref": "Carriage from Fenster's Milton Keynes yard to site at Edgware HA8 on 227 units",
 "treatment": "GAP - neither priced nor excluded",
 "evidence": "Both suppliers deliver to 98 Alston Drive, MK13 9HF - our own yard - and BSW are ex works. The "
 "workbook has no carriage line; install is pure per-unit labour codes. The proposal's exclusions cover Site "
 "Storage on the basis that 'Materials will be delivered to site', which is the opposite assumption. Cannot "
 "be costed from anything on file, so it is an open item rather than a number."})

sp.append({
 "ref": "NBS L10 clause 120 - pre-construction survey of All New and Replacement Windows before fabrication",
 "treatment": "priced",
 "evidence": "Proposal inclusions carry 'Site Survey - Only conducted once the structural openings are fully "
 "formed. Any revisits may be subject to a fee', which matches clause 120's 'Timing: Before fabrication'. "
 "Consistent - no action."})

u = m['u_value']
u['required'] = (
 "THREE DOCUMENTS NOW, AND THE NBS IS THE ONE THAT ACTUALLY SPECIFIES IT. "
 "(1) NBS 9001, the governing technical specification - L10 clause 330 'Windows & Roof Windows': 'Thermal "
 "performance (U-value maximum): 1.2 W/m2K'. L20 clause 280 'Communal Main Entrance Door Type B': 'Thermal "
 "performance (U-value maximum): 1.2 W/m2K or better'. L10 cl.140 / L20 cl.630 (Colt AXS 140 roof AOV): "
 "'U-value: 1.2 W/m2K or better'. So 1.2 applies to windows, communal entrance doors and the roof AOV alike. "
 "(2) 'Energy Statement - Gordon Court 25.02.24.pdf': 'The external glazing will be replaced or improved to "
 "achieve a U-value of 1.1 W/m2K', with a proposed column at Glazing 1.40 W/m2K and vision-element g-value "
 "0.40. 1.1 is the TIGHTEST figure in the pack. "
 "(3) The architect's schedules set no U-value and defer - 'MIN. THERMAL RATING: To Edward Pearce Consulting "
 "Engineers specification' - but they do set 'G-Value of 0.36 or better'. "
 "AND THE PACK DEFERS GLAZING PERFORMANCE TWICE OVER TO CONSULTANTS' SPECIFICATIONS THAT WERE NEVER ISSUED: "
 "NBS clause 330 items 5, 6 and 9 read 'G Value: To SAP Consultants specification', 'Frame Factor: To SAP "
 "Consultants specification' and 'Glazing details: To SAP Consultants specification', and the schedules defer "
 "thermal rating to Edward Pearce Consulting Engineers. NEITHER consultant's specification is in the tender "
 "pack. Our own proposal promises g-value 0.36 and states no U-value.")
u['note'] += (
 " SECOND TURN UPDATE - THE NBS NUMBERS CHANGE THE SHAPE OF THIS. Last turn the honest position was 'the "
 "schedules set no U-value at all', which made it look as though only the sustainability annex asked for "
 "anything - the exact escape route St Mary's warned about, where a client says the energy appendix does not "
 "apply to our package. It does not hold here: the NBS specification itself sets 1.2 W/m2K maximum on windows "
 "AND on communal entrance doors, so a thermal requirement exists in the governing technical document and "
 "does not depend on the Energy Statement at all. That is the St Mary's door-schedule lesson repeating - the "
 "requirement was in a third place nobody had opened. Still nothing to compute with: no BSW quote states a "
 "whole-window Uw, so nothing is rejected here either. The AFS fire doors are the only element with any "
 "stated figure (glass Ug 1.0) and even they carry no whole-door Ud against clause 280's 1.2.")

for f in m['finishes']:
    if f['ref'].startswith('Aluprof'):
        f['specified_internal'] = "RAL 9010 GLOSS (NBS L20 clause 280)"
        f['specified_external'] = "RAL 7016 MATT (NBS L20 clause 280)"
        f['note'] = (
         "STRONGER THAN LAST TURN - THE RAL IS NOT 'TBC', THE NBS FIXES IT. L20 clause 280 'Communal Main "
         "Entrance Door Type B' states 'Finish as delivered: Polyester powder-coated to BS EN 12206-1, colour "
         "RAL7016 MATT (EXTERNAL) & RAL9010 GLOSS (INTERNAL)'. So a dual finish with both RAL numbers and both "
         "gloss levels is specified outright. AFS state only 'Colour: Standard RAL' and 'Colours: Profiles: mat "
         "standard' - no RAL number, neither face. Dual colour on a fire door is a real cost and it is not in "
         "the GBP 18,298.94. The Georgie's Mercury failure exactly, now against an explicit specification "
         "rather than a TBC.")
    if f['ref'].startswith('Sheerline'):
        f['note'] += (" SECOND TURN: NBS L20 clause 280 fixes the entrance-door finish as RAL 7016 MATT "
                      "external / RAL 9010 GLOSS internal. BSW's '7016M Anthracite Grey - M' matches the "
                      "external face exactly, including the matt. The internal face is quoted as Sheerline's "
                      "own '9910HG Hipca White' where the NBS asks for RAL 9010 gloss - probably equivalent "
                      "and the gloss level is right, but it is a different reference and worth confirming "
                      "rather than assuming.")

json.dump(m, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('manifest updated: delivery_terms added, %d spec_items' % len(m['spec_items']))

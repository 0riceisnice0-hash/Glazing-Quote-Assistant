# -*- coding: utf-8 -*-
"""Third-turn manifest update: manifestation, strip-out per Adam's ruling, access cleared."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'job-checks', 'gordon-court.json')
m = json.load(io.open(P, encoding='utf-8'))

m['_note'] += (" THIRD TURN 27/07 late: Adam answered REQ-20 (hold the price, carry the risk). Rendered the "
               "scanned 'Q&As' file - it is a Delta portal screenshot with one item, no clarifications, so "
               "the clarification window closed ~15/07 and every open RFI is now post-tender. Applied Adam's "
               "REQ-17 rulings (access / strip-out / manifestation) to this job.")

sp = m['spec_items']

sp.append({
 "ref": "Manifestation to the communal main entrance doors - NBS L20 clause 280, 'Manifestation: As drawing'",
 "treatment": "GAP - neither priced nor excluded, and the drawing it refers to does not exist",
 "evidence":
 "NBS 9001 L20 clause 280 'Communal Main Entrance Door Type B' states '14. Glazing/ Infill details: Clear "
 "double glazing / 14.1. Manifestation: As drawing'. (The adjacent internal door clause says 'Manifestation: "
 "Not required', so the distinction is deliberate - the drafter turned it ON for the communal entrance "
 "doors.) BUT: manifestation appears ZERO times across all five architect's schedules (51001, 51002, 52001, "
 "52002, 52003), ZERO times in 'Window & Door Elevations.pdf', ZERO times in 'Fire Rated Door Elevations.pdf' "
 "and ZERO times in our own proposal - and no drawing in the pack shows any. So the requirement exists, its "
 "extent is undefined, it is not priced and it is not excluded. THIS IS THE ST MARY'S FINDING REPEATING (spec "
 "clause 2.24 manifestation, recited without being either priced or excluded) AND ADAM HAS NOW RULED ON IT - "
 "hub message 31 on REQ-17: 'We can allow the manifestation for a job of this size, however we should be "
 "putting this in our inclusions or on our description.' Gordon Court is GBP 368,376.70, more than twice St "
 "Mary's, so on his own test it should be allowed AND stated. Our proposal does neither."})

sp.append({
 "ref": "Strip-out and disposal of the existing windows and doors on a refurbishment (40no replacement windows)",
 "treatment": "GAP - 'effectively left unanswered', and Adam's rule says we would include it at this size",
 "evidence":
 "SUPERSEDES THE EARLIER ENTRY, WHICH SAID TO FLAG IT AT ORDER STAGE. The pack itself is silent - zero hits "
 "for strip out, remove existing or disposal across all five schedules, and the jLiving contract is an NEC3 "
 "activity schedule with no SOW item numbers, so there is no cross-reference into our item of the kind St "
 "Mary's SOW 1.09 had. Our proposal excludes 'Waste Removal - Generally excluded unless agreed otherwise' and "
 "never names removal of the existing windows. The GBP 46,840 install cannot absorb it: it is pure per-unit "
 "labour codes (GBP 160 PVC/LAW/MAW, GBP 250 SAD, GBP 500 DAD), which is fit-only money. ADAM'S RULING, hub "
 "message 31 on REQ-17: 'Strip out is something we need to clarify in future tenders. We have effectively "
 "left it unanswered however we would include it for a job of this size, but if they assume it's not included "
 "and do it for us then happy days.' Gordon Court is twice the size of the job he said that about and it "
 "strips out 40 existing windows plus external doors in an occupied building. So on his own test strip-out "
 "should be allowed here, and it is not. Cannot be costed from anything on file - there is no strip-out rate "
 "in the register - so it is an open item rather than a number."})

sp.append({
 "ref": "Access / lifting equipment - proposal wording (Adam's REQ-17 ruling)",
 "treatment": "excluded",
 "evidence": "CHECKED AND CLEARED ON THE PROPOSAL WORDING. Adam, hub message 31: 'Our proposal document "
 "should state that we have not allowed for any access.' Gordon Court's proposal already does - the "
 "exclusions name 'Access/Lifting Equipment - Scaffold, MEWPS, Towers, Forklift etc.' (7 access references, "
 "1 scaffold). So this job already complies with the rule he set. The separate COMMERCIAL risk stands and is "
 "recorded elsewhere: this building gains two storeys, and the exclusion still has to survive Chigwell's "
 "subcontract prelims."})

sp.append({
 "ref": "Tender clarification route - closed before we could use it",
 "treatment": "excluded",
 "evidence": "NOT A PRICING ITEM BUT IT GOVERNS EVERY OPEN QUESTION ON THIS JOB, SO IT IS RECORDED HERE. "
 "The pack's '1. Q&As 02.06.26.pdf' has no text layer; rendered at 200dpi it is a screenshot of the Delta "
 "eSourcing Message Centre for topic 'Gordon Ct: ITT', logged in as 'Antony Berry, Supplier Administrator', "
 "showing 'One item found' - a single 02/06/2026 13:04 message from darien.jay@vixus.co.uk to All Suppliers "
 "announcing the ITT had gone live with a 22 July 2026 @ 1400 return. So it is not a clarification log at "
 "all and it answers nothing; RFI-3 (whose specification governs the U-value) is still open. The ITT is "
 "explicit about the route and the deadline: 'Bidders may raise questions relating to this tender up to 5 "
 "working days prior to the tender return deadline', 'All questions during the tender should be directed via "
 "the Delta portal', and 'Please DO NOT contact jLiving directly.' Five working days before 22/07/2026 is "
 "~15/07/2026, and our own tender went to Chigwell on 09/07 - so the window was open when we priced and "
 "nobody used it. It is now shut. CONSEQUENCE: all seven open RFIs are POST-TENDER queries via Chigwell, "
 "which makes them variation or qualification territory rather than clarification. Worth someone "
 "establishing whether 'Antony Berry' is ours or Chigwell's - if Fenster holds a live Delta account on this "
 "tender we may be receiving jLiving award and standstill notices that nobody reads, which is the same shape "
 "as the known info@ and commercial@ blind spots."})

json.dump(m, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('manifest updated - %d spec_items' % len(m['spec_items']))

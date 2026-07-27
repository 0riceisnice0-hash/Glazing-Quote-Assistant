"""Correct the access limb of REQ-24. I overstated it and broadcast the overstatement.

Verified at source in '2, 3, 4 - SOW St. Marys.xlsx', sheet '2. Prelims':
  r180-181  "The Contractor is to provide all scaffolding, temporary lighting and
             clearing away, making good FOR HIMSELF AND ANY SUB-CONTRACTOR."
The document uses "the Contractor" throughout as the single actor above both
"Sub-Contractor" (r181) and the trades (r222), and distinct from "the Employer".
This is the MAIN CONTRACT between MTCBC and ET&S, so "the Contractor" is ET&S and
Fenster is the Sub-Contractor it must provide scaffolding for.

Also adds the disposal detail found in the same sweep (Prelims B/C, r253-278).
"""
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

req = next(r for r in d["requests"] if r["id"] == "REQ-24")

req["title"] = ("St Mary's REQ-17 follow-on: strip-out and manifestation are promised without a price "
                "(and the access limb is now WITHDRAWN - I had it wrong)")
req["why"] = (
  "CORRECTION FIRST, 27/07 late. I raised the access limb of this saying the tender preliminaries 'say "
  "the opposite of our exclusion, twice'. THAT WAS WRONG and I had quoted the sentence that disproves it. "
  "Prelims clause B reads: 'The Contractor is to provide all scaffolding, temporary lighting and clearing "
  "away, making good FOR HIMSELF AND ANY SUB-CONTRACTOR.' The pack uses 'the Contractor' throughout as the "
  "single actor above both 'Sub-Contractor' (r181) and the trades (r222) and distinct from 'the Employer'. "
  "This is the MAIN CONTRACT between MTCBC and ET&S, so the Contractor is ET&S and Fenster is the "
  "Sub-Contractor it must provide scaffolding FOR. Our exclusion of Access/Lifting Equipment is therefore "
  "CONSISTENT with the head contract, not exposed by it - the same conclusion gordon-court reached on "
  "their own job from jLiving's Works Information. I read an obligation and did not read who it fell on. "
  "THE RESIDUAL, which is much smaller than what I originally claimed: the head contract binds MTCBC and "
  "ET&S, not us. ET&S's own sub-contract order to Fenster is a document we do not hold and could still try "
  "to push access down. That is worth one line in the proposal, not the argument-on-site I described. "
  "WHAT REMAINS LIVE AND UNCHANGED. (1) STRIP-OUT has no price behind it. On Adam's own test it should be "
  "allowed here, and it is not in the GBP 174,546.37 - the install line reconciles exactly to per-unit fit "
  "labour and cannot absorb it. 107 openings / 202.80 m2, and MTCBC's SOW item 1.09 measures it in m2 and "
  "cross-refers it INTO our item 6.01. NEW DETAIL from the same prelims sweep: clause C requires the "
  "contractor to dispose of building waste to a LICENSED LANDFILL and to NAME it in the tender - one is "
  "already named, 'Tredegar Skip Hire' - and adds that this is 'a STRICT requirement of the Contract', that "
  "a tender without it 'will be discounted from consideration', and that 'the contractor is to allow in his "
  "rates for these requirements and no claim will be entertained for failure to do so'. A Site Waste "
  "Management Plan (SWAMP, Appendix A) is required WITH the tender submission, and Appendices A and B are "
  "not in the sections we hold. So if strip-out flows down to us under 6.01, the disposal duties, the "
  "licensed-landfill naming and the SWMP flow down with it. (2) MANIFESTATION is measured and quotable: "
  "24.10 linear metres of two-band manifestation across the 9 glazed door and screen units, or 39.90 if the "
  "two 3,620mm silled screens count. Neither item has a rate anywhere in the register - 0 of 80 categories - "
  "so both are QUANTITIES for an RFQ, not numbers I can supply.")
req["needs"] = (
  "A number for strip-out and one for manifestation, or a decision to carry them as stated inclusions and "
  "absorb them. Access no longer needs a decision from you - the head contract already puts it on ET&S "
  "including for their sub-contractors - but it is worth one line in the proposal reserving our position "
  "against whatever ET&S's own sub-contract order says.")
req["options"] = [
  "Get a real strip-out and disposal price and add it to the sum",
  "Carry strip-out and manifestation as stated inclusions and absorb the cost",
  "Re-issue the proposal with strip-out, manifestation and the access reservation stated",
  "Ask ET&S to confirm in writing that their scaffold covers our installation, per Prelims B",
]

d["catches"].append({
 "date": "2026-07-27", "job": "St Mary's Refurbishment",
 "catch": ("CORRECTION TO MY OWN FINDING: I said the preliminaries contradicted our access exclusion. They "
           "do not - clause B puts scaffolding on the Contractor 'for himself and any Sub-Contractor', and "
           "in a main contract between MTCBC and ET&S that means ET&S provides it for us. I had quoted the "
           "very sentence that disproves my reading. Read who an obligation falls ON, not just that it exists."),
 "type": "correction", "value": "finding withdrawn"})
d["catches"].append({
 "date": "2026-07-27", "job": "St Mary's Refurbishment",
 "catch": ("Prelims clause C requires building waste to go to a NAMED licensed landfill (Tredegar Skip Hire "
           "is already named), calls it 'a STRICT requirement of the Contract', and says the contractor must "
           "allow in his rates with 'no claim entertained for failure to do so'. A Site Waste Management Plan "
           "is required WITH the tender. If strip-out flows down to us under item 6.01, these flow down too - "
           "and Appendices A and B are not in the sections we hold."),
 "type": "scope", "value": "107 openings"})

for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] += (" CORRECTION 27/07: the access finding is WITHDRAWN. Prelims clause B puts scaffolding "
                        "on the Contractor 'for himself and any Sub-Contractor' - in a main contract between "
                        "MTCBC and ET&S that is ET&S providing it for us, so our exclusion is consistent with "
                        "the head contract rather than exposed by it. Strip-out and manifestation remain live "
                        "and unpriced (REQ-24), now with the added detail that the prelims require disposal to "
                        "a named licensed landfill and a Site Waste Management Plan with the tender.")

d["updated"] = "2026-07-27T22:05:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

back = json.load(open(P, encoding="utf-8"))
got = next((r for r in back["requests"] if r["id"] == "REQ-24"), None)
assert got and "WITHDRAWN" in got["title"], "correction did not land"
print("REQ-24 corrected and verified on re-read | requests:", len(back["requests"]),
      "| catches:", len(back["catches"]))

import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

ANSWER = ("Our proposal document should state that we have not allowed for any access. Strip out is "
          "something we need to clarify in future tenders. We have effectively left it unanswered "
          "however we would include it for a job of this size, but if they assume it's not included and "
          "do it for us then happy days. We can allow the manifestation for a job of this size, however "
          "we should be putting this in our inclusions or on our description.")

for r in d["requests"]:
    if r["id"] == "REQ-17":
        r["status"] = "answered"
        r["answer"] = ANSWER
        r["answered_by"] = "Adam (hub message 31, 27/07 19:42)"
        r["answered_at"] = "2026-07-27"
        r["outcome"] = (
          "ALL THREE RULED ON, AND ALL THREE ARE NOW ACTIONS RATHER THAN QUESTIONS. "
          "ACCESS - the proposal must SAY we have allowed no access; it already excludes Access/Lifting "
          "Equipment by name, so the wording is right. But the ruling settles what our document says, "
          "NOT who pays: Prelims F and B require the Contractor to provide all scaffolding 'for himself "
          "and any Sub-Contractor', and we are installing up to 5,580mm with 55.97 m2 of glazing 3.62m "
          "or taller. Residual question put back to Adam. "
          "STRIP-OUT - conceded as 'effectively left unanswered' and to be included on a job of this "
          "size. It is NOT in the GBP 174,546.37: the install line of GBP 21,915.05 reconciles exactly "
          "to per-unit fit labour and cannot absorb it. Quantity is 107 openings / 202.80 m2, and SOW "
          "1.09 measures it in m2 and cross-refers it INTO our item 6.01. No strip-out or disposal rate "
          "exists anywhere in the register (0 of 80 categories), so this needs a real price, not a "
          "benchmark. "
          "MANIFESTATION - to be allowed AND stated in the inclusions/description. Extent now measured "
          "so it can be quoted: 24.10 linear metres of two-band manifestation across the 9 glazed door "
          "and screen units (Types G/I/L/O/U/AF/AK), or 39.90 linear m if Types F and H, the 3,620mm "
          "screens, are included - clause 2.24 says 'glazed entrance doors and glazed screens', so "
          "whether silled windows count is the one judgement left.")

new = {
 "id": "REQ-22", "raised": "2026-07-27",
 "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
 "owner": "Adam",
 "title": "St Mary's REQ-17 follow-on: access wording is settled but access LIABILITY is not, and strip-out now needs a real price",
 "why": (
   "Thank you - all three rulings are recorded and applied. Three things they leave open. "
   "(1) ACCESS: you have told us what our document should say, and it already says it. What is still "
   "undecided is who PAYS. The tender preliminaries say the opposite of our exclusion, twice: item F "
   "requires the Contractor to provide 'all materials, labour, scaffolding, plant, tools, carriage and "
   "everything else necessary', and item B requires all scaffolding 'for himself and any Sub-Contractor'. "
   "We are installing elements up to 5,580mm tall and 55.97 m2 of the glazing is 3.62m or taller - none "
   "of it reachable from the ground. Stating we have allowed nothing is a negotiating position, not an "
   "agreement, and on a JCT MW with GBP 500/day delay damages it will be argued on site. "
   "(2) STRIP-OUT has no price behind it. On your test it should be allowed here, and it is not in the "
   "GBP 174,546.37 - the install line reconciles exactly to per-unit fit labour and cannot absorb it. "
   "It is 107 openings / 202.80 m2, and MTCBC's SOW item 1.09 measures it in m2 and cross-refers it INTO "
   "our item 6.01, so their document already reads as though it is ours. There is no strip-out or "
   "disposal rate anywhere in our register - 0 of 80 categories - so I cannot put a number on it without "
   "inventing one. "
   "(3) MANIFESTATION is now measurable: 24.10 linear metres of two-band manifestation across the 9 "
   "glazed door and screen units, or 39.90 linear m if the two 3,620mm screens (Types F and H) count. "
   "Clause 2.24 says 'glazed entrance doors and glazed screens', so that inclusion is a judgement. There "
   "is no manifestation rate in the register either. "
   "WORTH KNOWING: manifestation is now an unpriced, unexcluded gap on FOUR live jobs - St Mary's, "
   "Gordon Court, Brocks Hill and Filwood - and the Estimating Log itself carries 'Manifestations' as a "
   "note against two of them. Your ruling fixes it going forward if we act on it everywhere."),
 "needs": (
   "A number for strip-out and one for manifestation, or a decision to carry them as stated inclusions "
   "and absorb them - either is fine, but they should not stay unpriced now they are promised. And a "
   "view on whether to put the access liability to ET&S in writing before award rather than argue it on "
   "site."),
 "options": [
   "Put access liability to ET&S in writing now, before award",
   "Get a real strip-out and disposal price and add it to the sum",
   "Carry strip-out and manifestation as stated inclusions and absorb the cost",
   "Re-issue the proposal with all three stated, price unchanged",
   "Leave access as an unqualified exclusion and argue it if it arises"
 ],
 "status": "open"
}
if not any(r["id"] == "REQ-22" for r in d["requests"]):
    d["requests"].append(new)

new_catches = [
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "Adam ruled strip-out should be included on a job this size. It is not in the GBP 174,546.37 - the install line reconciles exactly to per-unit fit labour and cannot absorb 107 openings / 202.80 m2 of strip-out and disposal. No strip-out rate exists in the register.",
  "type": "scope", "value": "107 openings / 202.80 m2"},
 {"date": "2026-07-27", "job": "Fenster-wide (found from st-marys)",
  "catch": "Manifestation is required, unpriced and unexcluded on FOUR live jobs - St Mary's, Gordon Court, Brocks Hill and Filwood - and the Estimating Log carries 'Manifestations' as a note against two of them. There is no manifestation rate in the register, so nobody can price it from what we hold.",
  "type": "register gap", "value": "4 jobs"},
]
seen = {(c["job"], c["catch"]) for c in d["catches"]}
d["catches"].extend(c for c in new_catches if (c["job"], c["catch"]) not in seen)

for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] += (" REQ-17 ANSWERED BY ADAM 27/07 19:42 and closed: state that we have allowed no "
                        "access; strip-out 'we would include it for a job of this size'; allow the "
                        "manifestation and put it in the inclusions. Strip-out (107 openings / 202.80 m2) "
                        "and manifestation (24.10 linear m over 9 glazed door/screen units) are now "
                        "promised but unpriced, and neither has a rate anywhere in the register. REQ-22 "
                        "raised for the residual: access LIABILITY is still undecided - the ruling settles "
                        "what our document says, not who pays against Prelims F and B.")

d["updated"] = "2026-07-27T21:05:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("REQ-17 -> answered; REQ-22 raised. requests:", len(d["requests"]), "catches:", len(d["catches"]))

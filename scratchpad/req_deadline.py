import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

nums = [int(m.group(1)) for r in d["requests"] for m in [re.match(r"REQ-(\d+)$", r["id"])] if m]
new_id = "REQ-%d" % (max(nums) + 1)
assert not any(r["id"] == new_id for r in d["requests"])

req = {
 "id": new_id, "raised": "2026-07-27",
 "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
 "owner": "Adam",
 "title": "URGENT - ET&S re-opened the St Mary's package and the new return date is TODAY, 27 July. Nobody had noticed.",
 "why": (
   "ET&S's own Document Register, issued with the 24/07 revised drawings, carries "
   "'Package return date: 27 July 2026'. The three earlier registers - 08/07, 09/07 and 16/07 - all say "
   "'17 July 2026'. Same package, same package lead (Tom Godfrey), same field. So the 24/07 issue did not "
   "just re-circulate drawings: IT MOVED THE RETURN DATE OUT BY TEN DAYS, TO TODAY. "
   "We submitted on 17/07 against the original date and have treated the job as closed and awaiting award "
   "ever since. REQ-5 examined the 24/07 addendum for changes of SCOPE and correctly found none - but the "
   "return date sits in the register header, not in the drawings, and nobody read it. Our own hub record "
   "has had this job's deadline as 16/08, which is the supplier-quote validity, not a client date. "
   "WHY IT MATTERS TODAY. Everything found on this job over the last six turns is currently a list of "
   "things wrong with a quote already sitting on ET&S's desk. If the package is genuinely open until "
   "close of play today, it is instead a chance to submit a corrected and properly qualified tender - "
   "and several of the items are ones you have already ruled on. Specifically: the door U-value (SMA "
   "publish 1.8 W/m2K against the 1.4 our proposal promises and the 1.2 the client's EDG02 asks - the 7 "
   "Smart Wall Pocket units, GBP 31,360.15 of sell, miss under either reading); strip-out and "
   "manifestation, which you ruled on this evening and told me to state in the inclusions and which are "
   "in neither the price nor the document; Type G, where a Sheerline casement is drawn into a Smart Wall "
   "frame; delivery and carriage, which are in nobody's price on a site 150 miles from where BSW deliver; "
   "and the site postcode, which our documents give as CF77 8HA against the client's CF47 8HA."),
 "needs": (
   "Somebody has to establish with Tom Godfrey TODAY whether the package is genuinely open until close of "
   "play - the register is ET&S's own document and says it is. If it is, the decision is whether to "
   "re-submit a corrected and qualified tender or let the 17/07 quote stand. I cannot ask him: Mary can "
   "only email adam@ and marketing@, and outbound email is down anyway (REQ-23). This needs a phone call "
   "or an email from Gintare or you, and it needs it in the next few hours rather than tomorrow."),
 "options": [
   "Call Tom Godfrey now and confirm whether the package is open until close of play today",
   "Re-submit a corrected and qualified tender today against the 27/07 date",
   "Let the 17/07 quote stand and raise the findings as post-tender clarifications",
   "Ask ET&S for a short extension to submit a qualified revision"
 ],
 "status": "open"}
d["requests"].append(req)

d["catches"].append({
 "date": "2026-07-27", "job": "St Mary's Refurbishment",
 "catch": ("ET&S re-opened the package on 24/07 and moved the return date from 17 July to 27 JULY - TODAY. "
           "It is in the header of their own Document Register, which we had read three times for drawing "
           "revisions without ever reading the return-date field. We had this job recorded as submitted and "
           "closed, and the hub deadline showed 16/08, which was only the supplier-quote validity."),
 "type": "deadline", "value": "GBP 174,546.37 tender"})

for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["deadline"] = "2026-07-27"
        j["stage"] = "SUBMITTED 17/07 - BUT PACKAGE RE-OPENED, RETURN DATE 27/07 (TODAY)"
        j["status"] = ("**URGENT 27/07: THE PACKAGE RETURN DATE MOVED TO TODAY AND NOBODY HAD NOTICED.** "
                       "ET&S's Document Register issued with the 24/07 revised drawings says 'Package return "
                       "date: 27 July 2026'; the 08/07, 09/07 and 16/07 registers all say 17 July. Same "
                       "package, same lead. So the 24/07 issue moved the deadline out ten days. REQ-5 checked "
                       "that addendum for scope changes and correctly found none - the date is in the register "
                       "header, not the drawings. See %s. " % new_id) + j["status"]

d["updated"] = "2026-07-27T22:20:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

back = json.load(open(P, encoding="utf-8"))
got = next((r for r in back["requests"] if r["id"] == new_id), None)
assert got, "WRITE DID NOT LAND"
sm = next(j for j in back["jobs"] if j.get("job", "").startswith("St Mary"))
print("%s raised and verified | deadline now %s | requests %d | catches %d"
      % (new_id, sm["deadline"], len(back["requests"]), len(back["catches"])))

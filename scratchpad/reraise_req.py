"""Re-raise the St Mary's REQ-17 follow-on that was silently lost.

WHAT WENT WRONG: req17_answer.py hardcoded "REQ-22" from a stale read and guarded with
  if not any(r["id"] == "REQ-22" ...): append
Gordon Court had already committed their own REQ-22 at 20:33:51. So the guard was False,
the append was skipped, and the unconditional print still said "REQ-22 raised". The
request never existed.

THIS SCRIPT: computes the next id at write time, refuses to write if the id is taken,
and VERIFIES by re-reading after the write.
"""
import json, io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"

d = json.load(open(P, encoding="utf-8"))
nums = [int(m.group(1)) for r in d["requests"] for m in [re.match(r"REQ-(\d+)$", r["id"])] if m]
new_id = "REQ-%d" % (max(nums) + 1)
print("existing ids:", len(nums), "-> next free:", new_id)
assert not any(r["id"] == new_id for r in d["requests"]), "id already taken"

req = {
 "id": new_id, "raised": "2026-07-27",
 "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
 "owner": "Adam",
 "title": "St Mary's REQ-17 follow-on: access wording is settled but access LIABILITY is not, and strip-out and manifestation are promised without a price",
 "why": (
   "RE-RAISED 27/07 - this was lost, not answered. It was written as REQ-22 at about 21:05 but Gordon "
   "Court had already taken that number at 20:33, and the script's duplicate guard silently skipped the "
   "append while still reporting success. The substance did reach Adam - it is in the hub reply to his "
   "message 31 - but it was never tracked as a request. "
   "THE SUBSTANCE: thank you for the REQ-17 rulings, all three are recorded and applied. Three things "
   "they leave open. (1) ACCESS - you have told us what our document should say, and it already says it. "
   "What is still undecided is who PAYS. The tender preliminaries say the opposite of our exclusion "
   "twice: item F requires the Contractor to provide 'all materials, labour, scaffolding, plant, tools, "
   "carriage and everything else necessary', and item B requires all scaffolding 'for himself and any "
   "Sub-Contractor'. We install elements up to 5,580mm and 55.97 m2 of the glazing is 3.62m or taller - "
   "none of it reachable from the ground. An unqualified exclusion is a negotiating position, not an "
   "agreement, and on a JCT MW with GBP 500/day delay damages it gets argued on site. "
   "(2) STRIP-OUT has no price behind it. On your own test it should be allowed here, and it is not in "
   "the GBP 174,546.37 - the install line reconciles exactly to per-unit fit labour and cannot absorb it. "
   "107 openings / 202.80 m2, and MTCBC's SOW item 1.09 measures it in m2 and cross-refers it INTO our "
   "item 6.01, so their document already reads as though it is ours. There is no strip-out or disposal "
   "rate anywhere in the register - 0 of 80 categories - so I cannot put a number on it without inventing "
   "one. (3) MANIFESTATION is now measured: 24.10 linear metres of two-band manifestation across the 9 "
   "glazed door and screen units, or 39.90 if the two 3,620mm silled screens count. Clause 2.24 says "
   "'glazed entrance doors and glazed screens', so that inclusion is the one judgement left. No "
   "manifestation rate in the register either. "
   "WORTH KNOWING: manifestation is an unpriced, unexcluded gap on FOUR live jobs - St Mary's, Gordon "
   "Court, Brocks Hill and Filwood - and the Estimating Log carries 'Manifestations' as a note against "
   "two of them."),
 "needs": (
   "A number for strip-out and one for manifestation, or a decision to carry them as stated inclusions "
   "and absorb them - either is fine, but they should not stay promised and unpriced at the same time. "
   "And a view on whether to put the access liability to ET&S in writing before award rather than argue "
   "it on site."),
 "options": [
   "Put access liability to ET&S in writing now, before award",
   "Get a real strip-out and disposal price and add it to the sum",
   "Carry strip-out and manifestation as stated inclusions and absorb the cost",
   "Re-issue the proposal with all three stated, price unchanged",
   "Leave access as an unqualified exclusion and argue it if it arises"
 ],
 "status": "open"}
d["requests"].append(req)

d["catches"].append({
 "date": "2026-07-27", "job": "Mary system (found from st-marys)",
 "catch": ("A dashboard request was silently lost: the script hardcoded the next REQ id from a stale "
           "read, another chat had already taken it, and the duplicate guard skipped the append while "
           "the print still reported success. Compute the id at write time and verify by re-reading - "
           "an idempotency guard that silently skips is indistinguishable from a success."),
 "type": "system", "value": "1 request, ~4 hours unnoticed"})

# fix the job status text, which pointed at the wrong number
for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] = j["status"].replace("REQ-22 raised for the residual", "%s raised for the residual" % new_id)
        j["status"] = j["status"].replace("REQ-22", new_id)

d["updated"] = "2026-07-27T21:45:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# VERIFY by re-reading
back = json.load(open(P, encoding="utf-8"))
got = [r for r in back["requests"] if r["id"] == new_id]
print("verified on re-read:", bool(got), "| requests:", len(back["requests"]),
      "| catches:", len(back["catches"]))
if got:
    print("  ", got[0]["id"], "|", got[0]["job"][:44], "|", got[0]["status"])
else:
    sys.exit("WRITE DID NOT LAND")

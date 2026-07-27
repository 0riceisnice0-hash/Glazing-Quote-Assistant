import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

for r in d["requests"]:
    if r["id"] == "REQ-15":
        r["why"] += (
          " STRONGER AGAIN 27/07 after reading door schedule 2376-08 for the first time. It carries the "
          "requirement TWICE more, independently of the energy annex: per-door notes on D.01, D.17, D.22 "
          "and D.26 reading 'Door to achieve min u-value of 1.4W/m2k', and a general note 'External Doors "
          "U-value 1.2 w/m2k'. So 1.4 is stated in the window schedule, the door schedule AND our own "
          "proposal - ET&S cannot dispose of it by ruling that EDG02 does not apply. IMPORTANT CORRECTION "
          "IN OUR OWN ANALYSIS: that 1.2 is expressly 'an AREA WEIGHTED AVERAGE u-value - not a centre "
          "pane value', so under the SM5 Wexham rule no single element may be rejected against it. The "
          "average was therefore computed rather than asserted, and the finding survives: on 22.078 m2 of "
          "Smart Wall Pocket at SMA's 1.8 plus at most 20.367 m2 of MC600, the MC600 would have to achieve "
          "0.55 W/m2K for the package to average 1.2. A generous 1.0 gives 1.42; 1.4 gives 1.61. The doors "
          "miss on the architect's own averaging basis, not just per element.")

new_req = {
 "id": "REQ-19", "raised": "2026-07-27",
 "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
 "owner": "Adam",
 "title": "St Mary's door schedule requires fobbed readers, anti-ligature ironmongery and no latch - none of it is in our price",
 "why": (
   "Door schedule 2376-08 had not been read until now; the job was priced off the window schedule. Four "
   "things in it are in neither BSW's nor Bellview's quote. (1) FOBBED READERS are explicitly required on "
   "named doors - D.01 note 5 and D.14 both read 'fobbed reader'. Our proposal excludes access control and "
   "our own clarifications say 'fobbed reader compatibility requires further review', which was never done. "
   "Even if the system is MTCBC's under SOW 15.10, the leaf and frame need preparing - cabling, transfer "
   "hinges, an electric strike or keep - and Bellview's 7 units carry no electric strike, no rectifier and "
   "no transfer hinge (they price those separately when asked; on Filwood they quoted strike + latch + "
   "rectifier as a line). (2) ANTI-LIGATURE IRONMONGERY is specified - 'Anti-Ligature Infilled Door Pull "
   "Handle on Plate, 300 x 75mm stainless', hinges to BS 7352, 200mm kicking plate - and Bellview list only "
   "panic bars and closers. On a special needs school that is a safeguarding requirement, not a finish "
   "preference. (3) 'NO LOCKING MECHANISM OR LATCH' / 'Non-lockable device' appears on D.01, D.17, D.22 and "
   "D.26, yet we have priced concealed panic bars on all 7 units - a panic bar is a latching device. Aplus "
   "flagged exactly this in writing on their alternative quote ('It is unclear what a Non-Lockable Device "
   "is, quoted all doors with Panic Bars'); Bellview defaulted the same way silently. (4) THE TWO ARCHITECT'S "
   "SCHEDULES DISAGREE ON SIZES - D.17 is 2570 high where Type L is 2410, D.22 is 1530x2270 with no priced "
   "equivalent, D.26 is 930x2100 where Type U is 929x2370. Only D.01 maps cleanly, and D.01 is also the "
   "'4 panes bi-folding' door our proposal substituted for commercial French doors without written acceptance."),
 "needs": (
   "These are scope questions, not pricing ones, and they need the architect via ET&S. The safeguarding "
   "items (anti-ligature, and what a 'non-lockable device' means on an escape door in a special needs "
   "school) should not wait - if the answer is that panic bars are wrong, the door hardware changes on all "
   "7 units. Someone also has to decide whether fob preparation is in our package or MTCBC's."),
 "options": [
   "Ask cfw architects via ET&S what a 'non-lockable device' is on these escape doors",
   "Get Bellview to price anti-ligature ironmongery and fob preparation as an addendum",
   "Confirm with ET&S that fobbed reader preparation sits with MTCBC under SOW 15.10",
   "Ask the architect to reconcile door schedule 2376-08 against window schedule 2376-09 rev A",
   "Exclude the four items by name in a re-issued proposal"
 ],
 "status": "open"
}
if not any(r["id"] == "REQ-19" for r in d["requests"]):
    d["requests"].append(new_req)

for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] += (" 3RD TURN: read door schedule 2376-08, previously unopened. It states the 1.4 "
                        "requirement twice more (four per-door notes) so it no longer depends on EDG02 at "
                        "all; and its 1.2 for external doors is expressly an AREA WEIGHTED AVERAGE - a "
                        "correction to our own analysis, but the average was computed and the doors still "
                        "miss (MC600 would need 0.55 W/m2K). It also requires fobbed readers, anti-ligature "
                        "ironmongery and 'no locking mechanism or latch' against the panic bars we priced - "
                        "REQ-19. Cleared two false leads: making good is MTCBC's SOW section 8, and this "
                        "pack has no tender validity clause.")

new_catches = [
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "Door schedule 2376-08 requires 'fobbed reader' on D.01 and D.14, anti-ligature pull handles and BS 7352 hinges on the external doors, and 'no locking mechanism or latch' - while we priced concealed panic bars and no access control preparation on all 7 door units. The schedule had never been read; the job was priced off the window schedule.",
  "type": "scope", "value": "7 door units"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "The 1.2 W/m2K for external doors is expressly an AREA WEIGHTED AVERAGE, not a per-element limit - a correction to our own recorded basis. Computing it rather than asserting it, the doors still miss: MC600 would need 0.55 W/m2K for the package to average 1.2.",
  "type": "specification", "value": "finding survived the correction"},
]
seen = {(c["job"], c["catch"]) for c in d["catches"]}
d["catches"].extend(c for c in new_catches if (c["job"], c["catch"]) not in seen)

d["updated"] = "2026-07-27T18:20:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("requests:", len(d["requests"]), "catches:", len(d["catches"]))

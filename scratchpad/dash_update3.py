import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

SMA = (" CONFIRMED LATER THE SAME DAY BY SMA'S OWN DATASHEET, so this is no longer inference: "
       "'SMA Smart Wall Profile.pdf' publishes U Value 1.8 W/m2K for Smart Wall DOORS and 1.4 W/m2K for "
       "Smart Wall SCREENS (plus LPS 1175 Level 2 / BS EN 1627 Level 3 security). Our proposal promises "
       "1.4 across the package and EDG02 asks 1.2 on external doors - so at 1.8 the doors MISS BOTH, and "
       "they also miss the window schedule's own 1.4. THE DOORS THEREFORE FAIL UNDER EITHER READING OF "
       "THE SPEC, which means this no longer waits on the EDG02-vs-schedule question: on the windows that "
       "question still matters, on the doors it does not. The sheet reached us by accident at 15:56 "
       "attached to an unrelated High Wycombe enquiry. Caveats: it says 'Smart Wall', not 'Smart Wall "
       "POCKET' which is what Bellview actually quoted - confirm which figure applies to Pocket; and 1.8 "
       "assumes a proper glazed unit, whereas ours names no coating, no warm edge and no gas fill, so ours "
       "could be worse. In our favour, the same sheet's LPS 1175 / EN 1627 certification is the first "
       "evidence that the schedule's 38 Secured by Design notes are satisfiable on the doors.")

for r in d["requests"]:
    if r["id"] == "REQ-15":
        r["title"] = ("St Mary's: SMA publish 1.8 W/m2K for their doors - we promised 1.4 and the client "
                      "asks 1.2, so the doors fail either way")
        r["why"] += SMA
        r["needs"] = (
          "The door question is now settled enough to act on and does not need ET&S first: at SMA's own "
          "1.8 the 7 Smart Wall Pocket units (GBP 31,360.15 of sell) do not meet the 1.4 our proposal "
          "promises, let alone EDG02's 1.2. Somebody has to (a) get SMA to confirm the figure for Smart "
          "Wall POCKET specifically and issue a U-calc for the actual units, and (b) decide whether we "
          "re-quote the doors in a thermally broken system or qualify the deviation in writing. Separately "
          "ET&S still need to say whether EDG02 or window schedule 2376-09 governs, because that is what "
          "decides the WINDOWS and the g-value. For scale on the coating only, the rate register measures "
          "the solar-control uplift at +GBP 43.37/m2 median across 10 matched pairs (GBP 8,796 over the "
          "job) or GBP 16,489 band-matched to our actual units - benchmark, not a price, and it buys the "
          "g-value alone, not a compliant door.")
        r["options"] = [
          "Get SMA to confirm the Smart Wall POCKET figure and issue a U-calc for the actual units",
          "Re-quote the 7 door units in a thermally broken system (Smart Alitherm 600 / MC600 door)",
          "Qualify the door U-value deviation formally in writing to ET&S",
          "Ask ET&S in writing which governs for the windows - EDG02 or window schedule 2376-09",
          "Hold until SMA and ET&S have both answered"
        ]

for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] += (" LATE 27/07: SMA's own datasheet surfaced (attached to an unrelated enquiry) and "
                        "publishes 1.8 W/m2K for Smart Wall doors. Our proposal promises 1.4 and EDG02 asks "
                        "1.2 - so the 7 Smart Wall Pocket units, GBP 31,360.15 of sell, fail BOTH, and the "
                        "door U-value no longer depends on resolving which specification governs.")

new = [
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "SMA's own datasheet publishes 1.8 W/m2K for Smart Wall doors. Our proposal promises 1.4 and the client's EDG02 asks 1.2, so the 7 Smart Wall Pocket units fail under either reading of the spec - the door U-value does not depend on the open EDG02-vs-schedule question.",
  "type": "specification", "value": "GBP 31,360.15 of sell"},
 {"date": "2026-07-27", "job": "Mary system (found from st-marys)",
  "catch": "The only copy of SMA's published U-values in the business arrived as an attachment to an unrelated High Wycombe enquiry, not from the supplier we were asking. When a supplier will not state a performance figure, check whether their own literature is sitting elsewhere in the system.",
  "type": "record", "value": "settles GBP 31,360 of exposure"},
]
seen = {(c["job"], c["catch"]) for c in d["catches"]}
d["catches"].extend(c for c in new if (c["job"], c["catch"]) not in seen)

d["updated"] = "2026-07-27T18:00:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("requests:", len(d["requests"]), "catches:", len(d["catches"]))

import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

# ---- REQ-15: add the system finding and the quantification -----------------
for r in d["requests"]:
    if r["id"] == "REQ-15":
        r["title"] = ("St Mary's: the pack sets two U-values, we quoted the looser one - and if the "
                      "tighter one governs the doors are a SYSTEM change, not a glass change")
        r["why"] += (
          " NEW 27/07, and this is the part that cannot be fixed with glass: Bellview quote positions "
          "001-006 are 'System: SMA Smart Wall Pocket' - 6 door types, 7 units, 22.078 m2, GBP 31,360.15 "
          "of sell - and our own SM5 Wexham record states in writing that Smart Wall Pocket doors CANNOT "
          "meet a whole-installation U-value of 1.6 because it is a non-thermally-broken shopfront "
          "system. EDG02 asks 1.2 on external doors. A non-thermally-broken frame is the dominant heat "
          "path, so better glass does not rescue it - the SM5 Wexham fix was a thermally broken door "
          "(Smart Alitherm 600 / MC600 door) plus an SMA U-calc in writing. Position 007 is different "
          "and should not be lumped in: 'SMA MC600 Plus Standard', thermally broken, the Type AK curtain "
          "walling, 2 units, GBP 17,311.95 - probably fine. On the glass, the 28mm beads confirm these "
          "ARE genuine double glazed units, but with no low-E, no soft coat, no warm edge and no gas "
          "fill named, against BSW's windows which spell out 'EcoPlus 1.0 Black Warm Edge Sp 18mm'. "
          "Fifth instance of this pattern in a month after Princess Beatrice, Vesuvius, Filwood and "
          "Brocks Hill.")
        r["needs"] = (
          "Two separate answers, and they are not the same question. (a) ET&S: does EDG02 govern or does "
          "window schedule 2376-09? (b) BSW/Bellview: an SMA U-calculation in writing for the 7 Smart "
          "Wall Pocket units - SM5 Wexham asked for exactly this and never got it. "
          "FOR SCALE ONLY, not a price: the rate register carries matched solar-control categories "
          "against plain ones, and the coating uplift measures at +GBP 43.37/m2 median across 10 pairs "
          "(GBP 8,796 over the job) or GBP 16,489 band-matched to our actual units - call it "
          "GBP 9,000-16,500 of supply cost. It corroborates Filwood's GBP 45/m2. But that buys the "
          "g-value ONLY; it does not buy a 1.2 W/m2K door, and 23% of the area had no matched pair.")
        r["options"] = [
          "Ask ET&S in writing which governs - EDG02 or window schedule 2376-09",
          "Get an SMA U-calculation in writing for the 7 Smart Wall Pocket units",
          "Re-quote the doors in a thermally broken system (Smart Alitherm 600 / MC600 door)",
          "Qualify the tender formally at 1.4 W/m2K per the window schedule",
          "Hold until ET&S confirm which specification applies"
        ]

# ---- job status ------------------------------------------------------------
for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] = j["status"].replace(
          "REQ-5 remains answered - the 24/07 addendum does not change our scope.",
          "UPDATE 27/07 (2nd turn): finding (1) is worse than first read. The 7 SMA Smart Wall Pocket "
          "units - GBP 31,360.15 of sell - sit on a NON-THERMALLY-BROKEN system that our own SM5 Wexham "
          "record says cannot meet even 1.6 W/m2K, against EDG02's 1.2 for external doors. That is a "
          "system change or a formal qualification, not a glass swap - the fifth time this month. The "
          "Type AK MC600 curtain walling (GBP 17,311.95) is thermally broken and should NOT be lumped "
          "in with it. Coating uplift measured off the rate register for scale: GBP 9,000-16,500 of "
          "supply cost, benchmark only, and it prices the g-value alone. "
          "REQ-5 remains answered - the 24/07 addendum does not change our scope.")

# ---- catches ---------------------------------------------------------------
new = [
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "The 7 SMA Smart Wall Pocket door units are a non-thermally-broken system that our own SM5 Wexham record says cannot meet 1.6 W/m2K - against an EDG02 requirement of 1.2 on external doors. Better glass cannot fix it; the MC600 curtain walling on the same quote is thermally broken and is fine.",
  "type": "specification", "value": "GBP 31,360.15 of sell"},
 {"date": "2026-07-27", "job": "Mary system (found from st-marys)",
  "catch": "The registry wipe reproduced deterministically: triage re-added five jobs at 17:32 and the next session start erased all five again, orphaning the same five briefs for the second time. Only keys that existed when the bridge booted at 15:51:24 survive. Evidence for REQ-18.",
  "type": "system", "value": "5 jobs, incl a 07/08 deadline and GBP 100,730 quoted"},
]
seen = {(c["job"], c["catch"]) for c in d["catches"]}
d["catches"].extend(c for c in new if (c["job"], c["catch"]) not in seen)

d["updated"] = "2026-07-27T17:50:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("requests:", len(d["requests"]), "catches:", len(d["catches"]))

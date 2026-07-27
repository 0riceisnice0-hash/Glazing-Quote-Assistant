# -*- coding: utf-8 -*-
"""Add John North Hall to the hub and note the bridge restart against REQ-18."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

if not any(j["job"].startswith("John North Hall") for j in d["jobs"]):
    d["jobs"].append({
        "job": "John North Hall, Vaughan House - 5 communal entrance doors",
        "client": "John North Hall (High Wycombe) Mgmt Co / Neil Douglas",
        "deadline": "2026-08-24",
        "value": "not yet priced",
        "stage": "tender received",
        "status": (
            "NEW 27/07 - tender return 9am MON 24/08/2026, works order 701256543, works to start "
            "Oct/Nov 2026. Replace all 5 external communal block entrance door sets at 1-39 Vaughan "
            "House, John North Close, High Wycombe HP11 1FF. THE CLIENT SPECIFIES THE SYSTEM: SMA "
            "Smart-Wall, pivoted, anti-finger-trap hinge, concealed overhead closer, low mobility "
            "threshold, brown pad handles both faces, toughened/laminated/argon units, brown to match "
            "existing. Three things our standard proposal normally excludes are explicitly ours here: "
            "disconnecting and reconnecting the door intercoms and proving they work, making good "
            "inside and out, and removing and disposing of the old doors and frames - which is why "
            "they ask for a Waste Carrier Licence. BIGGEST COMMERCIAL POINT: clause 2.3.1 requires the "
            "quote to stay valid at least 90 DAYS because this is a leasehold Section 20 "
            "consultation, while Bellview and BSW quotes run 30 days and the start is three to four "
            "months out - get a written price hold or carry a stated allowance. Working hours 8-5 "
            "Mon-Fri, permit parking, keys from the agent; the scaffold clause is onerous while our "
            "proposal excludes access plant. Site visit offered by Jordan Jones. Reached us only "
            "because Perry forwarded it from info@, which Mary cannot see."
        ),
    })

for r in d["requests"]:
    if "Restart the bridge" in r.get("title", ""):
        r["why"] = r["why"] + (
            " UPDATE 17:50: the bridge HAS been restarted - pid is now 16004, started 17:48:36, "
            "against 31876 started 15:51:24 before. That is after both fixes landed, so the running "
            "process should now hold the patched code. But the wipe recurred once more in between "
            "(St Mary's confirmed the same five jobs gone at ~17:34), so all five have been re-added "
            "again and the registry is back to 21. Leaving this open until a session boundary passes "
            "with the count still at 21 - that is the only real proof."
        )

d["updated"] = "2026-07-27T17:52:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("hub jobs:", len(d["jobs"]))

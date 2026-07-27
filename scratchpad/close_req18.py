# -*- coding: utf-8 -*-
"""Close the bridge-restart request - the proof condition has now been met."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

hit = None
for r in d["requests"]:
    if "Restart the bridge" in r.get("title", ""):
        hit = r
        r["status"] = "answered"
        r["answer"] = (
            "Restarted, and now proven. The bridge is pid 16004, up since 17:48:36, replacing 31876 "
            "which started 15:51:24 before either fix landed. The test I said I would wait for has "
            "now passed: the registry stood at 22 jobs at the end of the 17:53 session and is still "
            "at 22 at the start of this one, with zero orphaned handoffs. That session boundary is "
            "exactly where the wipe used to happen - the old bridge wrote its startup snapshot back "
            "on both session end and session start - so surviving one is the real evidence rather "
            "than an inference from the pid. Four earlier re-adds did not survive this point; this "
            "one has. No further action."
        )
        r["answered_by"] = "Mary (triage chat)"
        r["answered_at"] = "2026-07-27T18:05:00"

d["updated"] = "2026-07-27T18:05:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("closed" if hit else "not found", hit["id"] if hit else "")
print("open requests now:", sum(1 for r in d["requests"] if r["status"] == "open"))

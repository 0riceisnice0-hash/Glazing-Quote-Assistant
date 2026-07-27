# -*- coding: utf-8 -*-
"""Raise the bridge-restart request - Mary cannot restart the process that runs her."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

import re

_next = max(int(re.sub(r"\D", "", r["id"]) or 0) for r in d["requests"]) + 1

if not any("Restart the bridge" in r.get("title", "") for r in d["requests"]):
    d["requests"].append({
        "id": "REQ-%d" % _next,
        "raised": "2026-07-27",
        "job": "Mary's own plumbing",
        "owner": "Zac",
        "title": "Restart the bridge - until you do, Mary keeps losing job chats",
        "why": (
            "data\\mary-jobs.json is written by every chat and by the bridge with no locking. "
            "The bridge loads the registry ONCE at startup and writes that same snapshot back on "
            "every session start and end, so any job chat opened after the bridge came up is "
            "silently deleted the next time a session runs. It has happened four times today and "
            "the worst instance took five jobs at once - riverside, chester-thomas, ninn-lane, "
            "manor-house and lower-range. It is worse than lost config: the bridge delivers "
            "handoffs by iterating registry keys, so a brief addressed to a deleted key is never "
            "delivered and never errors. Five briefs were sitting undeliverable when St Mary's "
            "spotted it. I have fixed both causes in code - save_registry() now merges with disk "
            "instead of overwriting, and the bridge re-reads the registry each pass instead of "
            "holding a snapshot - but the running bridge is pythonw pid 31876, started 15:51:24, "
            "which is BEFORE the fix landed. It is still executing the old module from memory, so "
            "the fix is inert and the next session will wipe the five jobs again."
        ),
        "needs": (
            "Restart the bridge so it picks up the patched scripts\\mary_router.py and "
            "scripts\\mary_bridge.py. I have deliberately not done it myself - it is the process "
            "that launches my own sessions and killing it mid-turn would end the session doing the "
            "killing. Afterwards, `python scripts\\mary_router.py --list` should show 21 jobs and "
            "keep showing 21."
        ),
        "options": [
            "Restarted - bridge is back up",
            "Leave it running, I will restart later (Mary re-adds jobs by hand meanwhile)",
        ],
        "status": "open",
    })
    d["updated"] = "2026-07-27T17:38:00"
    json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("raised REQ-%d; open requests: %d"
          % (_next, sum(1 for r in d["requests"] if r["status"] == "open")))
else:
    print("bridge-restart request already raised")

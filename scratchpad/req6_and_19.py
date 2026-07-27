# -*- coding: utf-8 -*-
"""Record Adam's REQ-6 ruling without closing it, and raise the second bridge restart."""
import json
import re

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

for r in d["requests"]:
    if r["id"] == "REQ-6":
        r["answer"] = (
            "ADAM 27/07 18:35 (via the hub, and confirmed by him at 20:0x as his message, not Zac's): "
            "\"It's charged as an optional extra in that on the pricing document it shows it as an "
            "'option' and the total on the proposal does not include the mastic cost on the pricing "
            "document. So I am okay with that as it is. EDPM is also an optional extra and depending "
            "on whether it's required. Sometimes we will remove the edpm and mastic costs or include "
            "them if they are specified.\" "
            "NOT CLOSED, because that describes the normal template and not this document. On the "
            "Princess Beatrice pricing document that was issued on 27/07, external mastic GBP "
            "5,356.22 and EPDM GBP 8,276.91 sit ABOVE the subtotal of GBP 286,404.81, which less the "
            "2.5% MCD gives the issued GBP 279,244.69 - so both ARE charged inside the client's "
            "number. That was Adam's own instruction that morning. Had they been left as options the "
            "quote would have been GBP 265,952.39, so GBP 13,292.30 is being charged for the two "
            "items while proposal page 3 still says external mastic is an optional extra and EPDM is "
            "not in the clarifications at all. Crestwood Park IS built the way Adam describes, with "
            "both under an OPTIONAL heading below the total - the two jobs differ."
        )
        r["answered_by"] = "Adam (ruling recorded), verified against the issued document by Mary"
        r["needs"] = (
            "One decision, now narrowed: leave proposal page 3 as it is on the basis that Guildmore "
            "will read the pricing document rather than the clarification line, or issue a corrected "
            "page 3. The arithmetic is not in question and no money moves either way - this is only "
            "about the quote contradicting itself in writing."
        )
        r["options"] = ["Leave it as issued", "Send Guildmore a corrected page 3"]

if not any("bridge again" in r.get("title", "") for r in d["requests"]):
    nxt = max(int(re.sub(r"\D", "", r["id"]) or 0) for r in d["requests"]) + 1
    d["requests"].append({
        "id": "REQ-%d" % nxt,
        "raised": "2026-07-27",
        "job": "Mary's own plumbing",
        "owner": "Zac",
        "title": "Restart the bridge again - new-chat launches are failing on a Windows limit",
        "why": (
            "Every attempt to start a NEW job chat has been dying with \"[WinError 206] The filename "
            "or extension is too long\". The bridge passes the whole kick prompt as a command-line "
            "argument and Windows caps a command line at 32,767 characters; the shared noticeboard "
            "alone reached 30,259 characters today, so the limit is now exceeded on every new chat. "
            "It silently ate three of Adam's dashboard messages (18:21, 18:35 and 18:52, including "
            "his answer to REQ-6) - each was retried three times and parked as failed, and the log "
            "shows the failure as a launch problem rather than a prompt problem, which is why nobody "
            "spotted it. Fixed: the prompt now goes down stdin, which has no length limit, verified "
            "at 30,328 characters - the exact size that was failing."
        ),
        "needs": (
            "Restart the bridge so it loads the patched scripts\\mary_bridge.py. Same as REQ-18: a "
            "long-running process keeps the module it imported at startup, so the fix is inert until "
            "then, and until it restarts no NEW job chat can start at all. Seven chats opened today "
            "have never run and are waiting on this - riverside, chester-thomas, ninn-lane, "
            "manor-house, lower-range (07/08 deadline), john-north-hall (24/08 deadline) and "
            "princess-beatrice."
        ),
        "options": ["Restarted", "Leave it, I will restart later"],
        "status": "open",
    })
    print("raised REQ-%d" % nxt)

d["updated"] = "2026-07-27T20:20:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("open requests:", sum(1 for r in d["requests"] if r["status"] == "open"))

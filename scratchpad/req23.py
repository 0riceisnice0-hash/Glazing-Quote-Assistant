# -*- coding: utf-8 -*-
"""Sharpen REQ-23 with the actual scope of the block."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

hit = None
for r in d["requests"]:
    if "email" in r.get("title", "").lower() or "send" in r.get("title", "").lower():
        if "403" in r.get("why", "") or "AccessPolicy" in r.get("why", ""):
            hit = r
            break

if hit:
    hit["why"] = hit.get("why", "") + (
        " || TRIAGE 21:15 - NARROWED THE SCOPE, and it is not what it looked like. Both app "
        "identities still acquire tokens cleanly, so client credentials and admin consent are "
        "intact - this is not an expired secret or a revoked grant. The READER identity still reads "
        "estimating@ perfectly (10 messages, latest 18:56Z), which is why inbound is unaffected. But "
        "the READER is ALSO denied on mary@ with the identical '[RAOP] Blocked by tenant configured "
        "AppOnly AccessPolicy' error. So the block is not on the Mail.Send permission - it is on the "
        "mary@ MAILBOX, for app-only access generally. estimating@ is still inside the policy; mary@ "
        "has fallen outside it. That is why sending as mary@ fails. (The SENDER identity's 403 on "
        "read is not evidence either way - it only holds Mail.Send, so a read denial is expected.) "
        "ONE THING I COULD NOT ESTABLISH: when it broke. The only record of a successful send is "
        "mary@'s own Sent Items, which sits inside the blocked mailbox - so the outage hid its own "
        "timeline. mary_send.py now writes data/mary-send-log.jsonl on every attempt, success or "
        "failure, so the next one will be dated."
    )
    hit["needs"] = (
        "Put mary@fensterglazing.com back inside the Exchange ApplicationAccessPolicy that governs "
        "app-only access (or remove it from whatever now excludes it) - most likely the policy is "
        "scoped to a mail-enabled security group that mary@ has dropped out of. Re-consenting "
        "Mail.Send will NOT fix it: the grant is fine and the token issues normally. Test with "
        "`python scripts/mary_send.py --to adam --subject \"test\" --body-file <file>` - it now logs "
        "the result either way. Until then the hub is the only outbound route to a human, and "
        "anything generated is sitting undelivered in outputs\\."
    )

d["updated"] = "2026-07-27T21:16:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("updated", hit["id"] if hit else "NOT FOUND")

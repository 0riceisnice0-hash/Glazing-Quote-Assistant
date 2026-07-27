# -*- coding: utf-8 -*-
"""Stage 2 of the quote-pipeline truth exercise (Zac, dashmsg-16).

Pulls estimating@ message METADATA across every folder (inbox, sent, filed
subfolders) so we can answer, per job: when did we last touch it, did the client
ever reply, and who was it sent to.

Metadata only - no bodies, no attachments. Writes scratchpad/pipeline-mailbox.json.
"""
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

SINCE = "2025-09-01T00:00:00Z"
OUT = os.path.join("scratchpad", "pipeline-mailbox.json")
INTERNAL_DOMAIN = "fensterglazing.com"


def fetch_all(token, mailbox, since_iso):
    path = ("/users/%s/messages?$top=500"
            "&$select=id,internetMessageId,subject,from,toRecipients,ccRecipients,"
            "receivedDateTime,hasAttachments"
            "&$orderby=receivedDateTime%%20desc"
            "&$filter=receivedDateTime%%20gt%%20%s" % (mailbox, since_iso))
    out, pages = [], 0
    while path and pages < 60:
        st, res = mg.graph(token, "GET", path)
        if st != 200:
            raise RuntimeError("list failed: %s %s" % (st, str(res)[:300]))
        out.extend(res.get("value", []))
        nxt = res.get("@odata.nextLink")
        pages += 1
        if not nxt:
            break
        # graph() takes a path relative to the API root
        path = nxt.split("graph.microsoft.com/v1.0", 1)[-1]
        print("  page %d, %d messages so far" % (pages, len(out)))
    return out


def addr(rec):
    try:
        return (rec.get("emailAddress") or {}).get("address", "").lower()
    except AttributeError:
        return ""


def main():
    env = mg.load_env()
    token = mg.get_token(env, "READER")
    msgs = fetch_all(token, "estimating@fensterglazing.com", SINCE)
    print("total messages pulled: %d" % len(msgs))

    slim = []
    for m in msgs:
        frm = addr(m.get("from") or {})
        tos = [addr(r) for r in (m.get("toRecipients") or [])]
        ccs = [addr(r) for r in (m.get("ccRecipients") or [])]
        slim.append({
            "subject": (m.get("subject") or "").strip(),
            "from": frm,
            "to": tos,
            "cc": ccs,
            "received": m.get("receivedDateTime"),
            "inbound_external": bool(frm) and INTERNAL_DOMAIN not in frm,
            "has_attachments": bool(m.get("hasAttachments")),
        })

    os.makedirs("scratchpad", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(slim, fh, indent=1, ensure_ascii=False)

    ext = sum(1 for s in slim if s["inbound_external"])
    print("external inbound: %d   internal/outbound: %d" % (ext, len(slim) - ext))
    if slim:
        print("date range: %s .. %s" % (slim[-1]["received"], slim[0]["received"]))


if __name__ == "__main__":
    main()

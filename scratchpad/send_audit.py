# -*- coding: utf-8 -*-
"""When did Mary's outbound actually stop?

St Mary's found mary_send.py returning Graph 403 and noted there is no send log,
so nobody can say when it broke. The reader identity CAN read mary@ (Mail.Read
covers estimating@ and mary@), and Sent Items lives in that mailbox - so the
sent record itself is the log we never wrote.

Read-only. Sends nothing.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
import mary_graph as mg


def addr(rec):
    try:
        return (rec.get("emailAddress") or {}).get("address", "")
    except AttributeError:
        return ""


def main():
    env = mg.load_env()
    token = mg.get_token(env, "READER")
    path = ("/users/%s/messages?$top=100"
            "&$select=subject,from,toRecipients,sentDateTime,receivedDateTime,hasAttachments"
            "&$orderby=sentDateTime%%20desc" % mg.MARY)
    st, res = mg.graph(token, "GET", path)
    if st != 200:
        print("read of mary@ failed: %s %s" % (st, str(res)[:300]))
        return 1

    rows = res.get("value", [])
    print("messages visible in %s: %d\n" % (mg.MARY, len(rows)))
    sent = []
    for m in rows:
        frm = addr(m.get("from") or {})
        tos = ",".join(addr(r) for r in (m.get("toRecipients") or []))
        when = (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:19].replace("T", " ")
        kind = "SENT" if frm.lower() == mg.MARY else "in  "
        if kind == "SENT":
            sent.append((when, tos, m.get("subject") or ""))
        print("%s %s  %-46s %s%s" % (kind, when, tos[:46], (m.get("subject") or "")[:70],
                                     "  [att]" if m.get("hasAttachments") else ""))

    print()
    if sent:
        sent.sort()
        print("OUTBOUND from mary@: %d message(s)" % len(sent))
        print("  earliest: %s  %s" % (sent[0][0], sent[0][2][:60]))
        print("  LATEST  : %s  %s" % (sent[-1][0], sent[-1][2][:60]))
        print("\n  -> outbound was still working at %s; the 403 is after that." % sent[-1][0])
    else:
        print("no messages FROM mary@ visible in that mailbox at all")


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""READ-ONLY scan of estimating@ (all folders) + mary@ inbox for the morning update.
Does not mark anything processed, does not queue, does not send."""
import os
import sys
import datetime as dt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_graph as mg

SINCE = "2026-07-29T00:00:00Z"


def uk(iso):
    d = dt.datetime.strptime(iso.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    return (d + dt.timedelta(hours=1)).strftime("%d/%m %H:%M")


def show(token, mailbox, whole):
    msgs = mg.list_messages(token, mailbox, since_iso=SINCE, top=150, whole_mailbox=whole)
    print("\n===== %s : %d messages since %s =====" % (mailbox, len(msgs), SINCE))
    for m in sorted(msgs, key=lambda x: x["receivedDateTime"]):
        frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
        to = ";".join((r.get("emailAddress") or {}).get("address", "") for r in (m.get("toRecipients") or []))[:70]
        print("-" * 100)
        print("%s | FROM %s | TO %s%s" % (uk(m["receivedDateTime"]), frm, to,
                                          " | ATT" if m.get("hasAttachments") else ""))
        print("  SUBJ: %s" % (m.get("subject") or "")[:160])
        prev = (m.get("bodyPreview") or "").replace("\r", " ").replace("\n", " ")
        print("  PREV: %s" % prev[:400])
        print("  ID: %s" % m["id"])


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mail-scan-3007.txt")
_fh = open(OUT, "w", encoding="utf-8")
_orig = print


def print(*a, **k):  # noqa: A001 - deliberate: tee everything to a utf-8 file
    k["file"] = _fh
    _orig(*a, **k)


env = mg.load_env()
token = mg.get_token(env, "READER")
show(token, mg.ESTIMATING, True)
show(token, mg.MARY, False)
_fh.close()
_orig("written to %s" % OUT)

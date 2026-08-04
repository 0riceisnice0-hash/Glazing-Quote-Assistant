# -*- coding: utf-8 -*-
"""Refetch the front desk's queued orders in full.

The front desk wrote 71 work orders from the cheap list view: `from` as Graph's
nested dict, no body beyond a 255-character preview, and no attachments even
where the message had them. The routing decisions were fine - the envelopes
were empty.

They are real work, so they are repaired rather than dropped: each one is
refetched by id, rewritten in the poller's shape, and its attachments pulled
down. The triage block is preserved exactly, because the classifier's call and
its reason are still good.

  python scripts/frontdesk_repair.py            # what it would do
  python scripts/frontdesk_repair.py --write

Safe to re-run - an order already carrying a body is left alone.
"""
import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUES = {b: os.path.join(REPO, "test-results", "%s-inbox" % b, "queue")
          for b in ("mary", "jacob", "joseph")}
# Which reader can open which mailbox. jacob@ is only on Jacob-Reader.
JACOB_BOXES = {"jacob@fensterglazing.com"}


def broken(d):
    """An order the bots cannot fully use."""
    return (isinstance(d.get("from"), dict)
            or not d.get("body")
            or (d.get("hasAttachments") and not d.get("attachments")))


def tokens():
    out = {}
    try:
        out["mary"] = mg.get_token(mg.load_env(), "READER")
    except Exception as e:
        print("no Mary-Reader token: %s" % str(e)[:80])
    try:
        import jacob_graph as jg
        out["jacob"] = jg.get_token(jg.load_env(), "READER")
    except Exception as e:
        print("no Jacob-Reader token: %s" % str(e)[:80])
    return out


def repair(path, d, toks, write):
    mailbox = d.get("mailbox") or ""
    mid = d.get("id")
    which = "jacob" if mailbox in JACOB_BOXES else "mary"
    token = toks.get(which)
    if not token or not mid:
        return "no %s reader" % which

    frm = d.get("from")
    if isinstance(frm, dict):
        frm = ((frm.get("emailAddress") or {}).get("address") or "")
    frm = str(frm or "")

    # A message filed or deleted since the sweep answers 404 and can never be
    # refetched. The record is still normalised and still written: what it
    # loses is the body, what it must NOT keep is `from` as a dict, which is
    # the shape that stops Mary's bridge dead. It keeps the preview and says
    # body_complete is false rather than looking like a whole email.
    note = ""
    try:
        full = mg.get_message_body(token, mailbox, mid)
    except Exception as e:
        full = {}
        note = " (gone from the mailbox - preview only)" if "404" in str(e) \
            else " (fetch failed: %s)" % str(e)[:40]

    body_txt = mg.html_to_text((full.get("body") or {}).get("content", ""))
    saved = d.get("attachments") or []
    if d.get("hasAttachments") and not saved and write:
        try:
            base = os.path.basename(path)[:-5]
            saved = mg.download_attachments(
                token, mailbox, mid, os.path.join(os.path.dirname(path), base + "-att"))
        except Exception as e:
            # Same reasoning as the body: losing the attachments is bad, but
            # abandoning the write leaves the dict-shaped `from` in place, and
            # that is the part that stops a bridge.
            note += " (attachments unavailable: %s)" % str(e)[:40]

    rec = {
        "mailbox": mailbox, "id": mid,
        "internet_message_id": d.get("internet_message_id") or d.get("internetMessageId", ""),
        "from": frm, "subject": d.get("subject", ""),
        "received": d.get("received") or d.get("receivedDateTime", ""),
        "to": [r.get("emailAddress", {}).get("address", "")
               for r in (full.get("toRecipients") or d.get("toRecipients") or [])],
        "cc": [r.get("emailAddress", {}).get("address", "")
               for r in (full.get("ccRecipients") or d.get("ccRecipients") or [])],
        "trusted_sender": frm in mg.TRUSTED_SENDERS,
        "attachments": saved,
        "body": (body_txt or d.get("bodyPreview") or "")[:20000],
        "body_complete": bool(body_txt),
        "kind": "email",
        "triage": d.get("triage") or {},
    }
    if write:
        with io.open(path, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, ensure_ascii=False)
    return "ok - %d chars of body, %d attachment(s)%s" % (
        len(rec["body"]), len(saved), note)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    toks = tokens() if a.write else {}
    if a.write and not toks:
        print("no readers - nothing can be refetched")
        return 1

    found = fixed = skipped = 0
    for bot, q in QUEUES.items():
        if not os.path.isdir(q):
            continue
        for name in sorted(os.listdir(q)):
            if not name.startswith("fd-") or not name.endswith(".json"):
                continue
            path = os.path.join(q, name)
            try:
                d = json.load(io.open(path, encoding="utf-8"))
            except Exception:
                continue
            if not broken(d):
                skipped += 1
                continue
            found += 1
            if not a.write:
                print("  %-7s %s" % (bot, str(d.get("subject"))[:66]))
                continue
            r = repair(path, d, toks, True)
            if r.startswith("ok"):
                fixed += 1
            print("  %-7s %-52s %s" % (bot, str(d.get("subject"))[:52], r))

    print()
    print("%d order(s) need refetching, %d already complete" % (found, skipped))
    if a.write:
        print("%d repaired" % fixed)
    else:
        print("(nothing written - pass --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

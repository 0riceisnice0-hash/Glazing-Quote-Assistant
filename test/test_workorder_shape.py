# -*- coding: utf-8 -*-
"""A work order has one shape, whoever writes it.

Two things write into a bot's queue: mary_poller (the old path, kept for
backfills) and frontdesk (the live one). The bots read whatever is there and
assume a single shape. On 04/08 they stopped matching and nothing said so:

  - frontdesk wrote Graph's raw list-view record, so `from` was a nested dict.
    mary_router does `(order.get("from") or "").lower()` and threw 'dict'
    object has no attribute 'lower' every ten seconds. Her bridge dispatched
    nothing for eight minutes while her queue grew from 66 to 75.
  - it had no `body` at all - only a 255-character bodyPreview - and never
    downloaded attachments. Jacob and Joseph ran real sessions on tender
    emails without the tender. 24 of 71 orders were missing their documents;
    219 attachment files had to be refetched.

Neither failure was loud. The bots did not crash on the missing body, they
just worked from less. So the shape is asserted here rather than trusted.

  python test/test_workorder_shape.py
"""
import glob
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

# What every bot is entitled to assume it can read off a work order, and the
# type it will get. `body` may be short but must exist; `from` must be an
# address, never Graph's {"emailAddress": {...}}.
CONTRACT = {
    "mailbox": str, "id": str, "from": str, "subject": str,
    "received": str, "to": list, "cc": list, "body": str,
    "attachments": list, "trusted_sender": bool,
}

fails = []


def check(path, d):
    name = os.path.basename(path)
    for field, want in CONTRACT.items():
        if field not in d:
            fails.append("%s: no `%s`" % (name, field))
        elif not isinstance(d[field], want):
            fails.append("%s: `%s` is %s, want %s"
                         % (name, field, type(d[field]).__name__, want.__name__))
    # An order whose message carried attachments must either have them on disk
    # or say plainly that they could not be fetched. Silently having neither is
    # the failure this file exists for.
    if d.get("hasAttachments") and not d.get("attachments") and d.get("body_complete"):
        fails.append("%s: message had attachments, none downloaded" % name)


def main():
    seen = 0
    for q in glob.glob(os.path.join(REPO, "test-results", "*-inbox", "queue", "*.json")):
        try:
            d = json.load(io.open(q, encoding="utf-8"))
        except Exception as e:
            fails.append("%s: unreadable (%s)" % (os.path.basename(q), str(e)[:40]))
            continue
        if d.get("kind") and d.get("kind") != "email":
            continue
        seen += 1
        check(q, d)

    print("WORK ORDER SHAPE")
    print("=" * 62)
    print("%d order(s) checked against the %d-field contract"
          % (seen, len(CONTRACT)))
    if not fails:
        print("\nevery order is readable by every bot")
        return 0
    print("\n%d problem(s):" % len(fails))
    for f in fails[:25]:
        print("   " + f)
    if len(fails) > 25:
        print("   ... and %d more" % (len(fails) - 25))
    return 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Rebuild the ledger from what the front desk already left behind.

The ledger starts empty, but the front desk has run and its decisions did
leave traces - a `triage` block on every queued item, a `binned` block on
every message it threw away. Those are the same facts the ledger records, so
the history is recoverable and the tab does not have to open on nothing.

The log file is deliberately NOT the source. Its subject lines are truncated
to 46 characters and it has no sender or mailbox, so a row built from it would
be a worse row wearing the same shape. The artefacts have the whole message.

  python scripts/frontdesk_backfill.py            # show what it would write
  python scripts/frontdesk_backfill.py --write

Safe to re-run: rows are keyed on the message id and existing ones are kept.
"""
import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frontdesk_ledger as ledger

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUES = {b: os.path.join(REPO, "test-results", "%s-inbox" % b, "queue")
          for b in ("mary", "jacob", "joseph")}
BINNED = os.path.join(REPO, "test-results", "frontdesk-noise")


def _written(path):
    """When the file was written - the decision's own timestamp."""
    import datetime as dt
    try:
        return dt.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec="seconds")
    except OSError:
        return ""


def _addr(msg):
    f = msg.get("from")
    if isinstance(f, dict):
        return ((f.get("emailAddress") or {}).get("address") or "")
    return str(f or "")


def harvest():
    """Every decision still on disk, oldest first."""
    found = []

    for bot, q in QUEUES.items():
        if not os.path.isdir(q):
            continue
        for name in sorted(os.listdir(q)):
            if not name.endswith(".json"):
                continue
            try:
                with io.open(os.path.join(q, name), encoding="utf-8") as fh:
                    msg = json.load(fh)
            except Exception:
                continue
            t = msg.get("triage")
            # No triage block means the item predates the front desk - it was
            # queued by the poller. Not its decision, so not its row.
            if not isinstance(t, dict) or t.get("by") != "frontdesk":
                continue
            # WHEN THE CALL WAS MADE, NOT WHEN THE EMAIL ARRIVED. The item
            # carries receivedDateTime and using it looks right, but it dates
            # the row to the sender's clock - so "36 decisions in the last 24
            # hours" would really be counting mail received in 24 hours, which
            # is a different number about a different thing. The queue file was
            # written at the instant of the decision; its mtime is that instant.
            found.append((_written(os.path.join(q, name)),
                          msg.get("mailbox", ""), msg, t.get("bot") or bot,
                          t.get("verdict") or "work", t.get("why") or "",
                          t.get("model") or ""))

    if os.path.isdir(BINNED):
        for name in sorted(os.listdir(BINNED)):
            if not name.endswith(".json"):
                continue
            try:
                with io.open(os.path.join(BINNED, name), encoding="utf-8") as fh:
                    msg = json.load(fh)
            except Exception:
                continue
            b = msg.get("binned") or {}
            box = ""
            for r in (msg.get("toRecipients") or []):
                box = ((r.get("emailAddress") or {}).get("address") or "")
                break
            found.append((b.get("at") or _written(os.path.join(BINNED, name)),
                          box, msg, "mary", "noise",
                          b.get("why") or "", b.get("model") or ""))

    found.sort(key=lambda r: r[0])
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    have = {r.get("id") for r in ledger.rows()}
    found = harvest()
    new = [f for f in found if str(f[2].get("id") or "") not in have]

    print("%d decision(s) recoverable, %d already in the ledger, %d to add"
          % (len(found), len(found) - len(new), len(new)))
    by = {}
    for _ts, _box, _msg, bot, verdict, _why, _m in new:
        by["%s/%s" % (bot, verdict)] = by.get("%s/%s" % (bot, verdict), 0) + 1
    for k in sorted(by):
        print("   %-14s %d" % (k, by[k]))

    if not a.write:
        print("\n(nothing written - pass --write)")
        return 0

    for ts, box, msg, bot, verdict, why, model in new:
        ledger.add(box, msg, bot, verdict, why, model, at=ts)
    print("\nwrote %d row(s) to %s" % (len(new), ledger.LEDGER))
    return 0


if __name__ == "__main__":
    sys.exit(main())

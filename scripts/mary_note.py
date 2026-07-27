# -*- coding: utf-8 -*-
"""How Mary's chats talk to each other.

Two channels, deliberately different:

  NOTICEBOARD (data/mary-noticeboard.md) - broadcast. Anything every chat
    should know: a rate just learned, a supplier's lead time, a deadline that
    moved, a spec ruling from Adam. Every session reads the tail of this at
    the start of its turn. Write here when the fact outlives the job.

  HANDOFF (test-results/mary-inbox/handoffs/) - addressed. A note from one
    job chat to another, delivered into that chat's next turn by the bridge.
    Write here when a specific job needs to act on something you found.

Usage from inside a session:
  python scripts/mary_note.py --board --body "CN Glass quote 8.8L-16-4T at GBP60/m2 inc energy - half Vetroseal's GBP110."
  python scripts/mary_note.py --to vesuvius --body-file scratchpad/note.txt
  python scripts/mary_note.py --read          # the last 40 noticeboard entries
  python scripts/mary_note.py --inbox         # handoffs waiting for THIS chat
"""
import argparse
import datetime as dt
import json
import os
import sys
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(REPO, "data", "mary-noticeboard.md")
HANDOFFS = os.path.join(REPO, "test-results", "mary-inbox", "handoffs")
DELIVERED = os.path.join(HANDOFFS, "delivered")
KEEP_ENTRIES = 60


def me():
    return os.environ.get("MARY_CHAT_KEY", "unknown-chat")


def read_board(limit=40):
    if not os.path.exists(BOARD):
        return ""
    with open(BOARD, encoding="utf-8") as fh:
        text = fh.read()
    entries = [e for e in text.split("\n### ") if e.strip()]
    tail = entries[-limit:]
    return "\n### ".join(tail) if tail else ""


def post_board(body, author=None):
    os.makedirs(os.path.dirname(BOARD), exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = "\n### %s - %s\n%s\n" % (stamp, author or me(), body.strip())
    header = "" if os.path.exists(BOARD) else (
        "# Mary's noticeboard\n\nShared between every job chat. Newest at the bottom. "
        "Facts that outlive one job: rates, lead times, spec rulings, deadline moves.\n")
    with open(BOARD, "a", encoding="utf-8") as fh:
        if header:
            fh.write(header)
        fh.write(entry)
    trim_board()
    return entry


def trim_board():
    with open(BOARD, encoding="utf-8") as fh:
        text = fh.read()
    parts = text.split("\n### ")
    if len(parts) - 1 <= KEEP_ENTRIES:
        return
    kept = [parts[0]] + parts[-KEEP_ENTRIES:]
    with open(BOARD, "w", encoding="utf-8") as fh:
        fh.write("\n### ".join(kept))


def send_handoff(to_key, body, author=None):
    os.makedirs(HANDOFFS, exist_ok=True)
    rec = {"id": uuid.uuid4().hex[:10], "to": to_key, "from": author or me(),
           "created": dt.datetime.now().isoformat(timespec="seconds"), "body": body.strip()}
    path = os.path.join(HANDOFFS, "%s-%s.json" % (to_key, rec["id"]))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    return rec


def pending_handoffs(to_key):
    if not os.path.isdir(HANDOFFS):
        return []
    out = []
    for name in sorted(os.listdir(HANDOFFS)):
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(HANDOFFS, name), encoding="utf-8") as fh:
                rec = json.load(fh)
        except Exception:
            continue
        if rec.get("to") == to_key:
            rec["_file"] = os.path.join(HANDOFFS, name)
            out.append(rec)
    return out


def mark_delivered(recs):
    os.makedirs(DELIVERED, exist_ok=True)
    for rec in recs:
        src = rec.get("_file")
        if src and os.path.exists(src):
            os.replace(src, os.path.join(DELIVERED, os.path.basename(src)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", help="job key to address a handoff to")
    ap.add_argument("--board", action="store_true", help="post to the shared noticeboard")
    ap.add_argument("--body")
    ap.add_argument("--body-file")
    ap.add_argument("--from", dest="author", default=None)
    ap.add_argument("--read", action="store_true")
    ap.add_argument("--inbox", action="store_true")
    args = ap.parse_args()

    if args.read:
        print(read_board() or "(noticeboard empty)")
        return 0
    if args.inbox:
        for rec in pending_handoffs(me()):
            print("[%s from %s] %s" % (rec["created"], rec["from"], rec["body"]))
        return 0

    body = args.body
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as fh:
            body = fh.read()
    if not body or not body.strip():
        print("nothing to post: pass --body or --body-file")
        return 2

    if args.board:
        post_board(body, args.author)
        print("posted to the noticeboard")
        return 0
    if args.to:
        send_handoff(args.to, body, args.author)
        print("handoff queued for %s - it lands in that chat's next turn" % args.to)
        return 0
    print("pick a destination: --board or --to <job key>")
    return 2


if __name__ == "__main__":
    sys.exit(main())

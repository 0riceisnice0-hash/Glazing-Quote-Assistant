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
ARCHIVE = os.path.join(REPO, "data", "mary-noticeboard-archive.md")
# The bridge builds its kick prompt from the board plus handoffs plus the job
# brief, and (until it is restarted with the stdin fix) passes the lot as a
# Windows command line, which is capped at 32,767 characters. On 27/07/2026 the
# board reached 31,387 on its own and froze every chat - new AND resumed. Trim by
# SIZE, not just entry count: today's entries run 3-7k each, so the 60-entry cap
# allowed a 200k board and never once fired. Nothing is discarded; overflow moves
# to ARCHIVE. post_board() runs as a fresh process every time a chat posts, so
# this takes effect immediately and does not wait on the restart.
MAX_BOARD_CHARS = 9000


def me():
    return os.environ.get("MARY_CHAT_KEY", "unknown-chat")


def read_board(limit=40, include_archive=False):
    """Newest `limit` entries. Default is the LIVE board only - the bridge calls
    this to build a kick prompt and must not be handed the whole archive.

    include_archive=True gives the full history, which is what `--read` wants:
    once trimming became automatic the live board holds only a couple of
    entries, so without this a chat looking up an earlier finding would be told
    the board is nearly empty.
    """
    texts = []
    if include_archive and os.path.exists(ARCHIVE):
        with open(ARCHIVE, encoding="utf-8") as fh:
            texts.append(fh.read())
    if os.path.exists(BOARD):
        with open(BOARD, encoding="utf-8") as fh:
            texts.append(fh.read())
    if not texts:
        return ""
    entries = [e for e in "\n".join(texts).split("\n### ") if e.strip()]
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
    """Keep the live board under MAX_BOARD_CHARS, archiving what overflows.

    Returns the number of entries moved. Newest entries stay; the rest are
    appended to ARCHIVE in their original order so the archive still reads
    oldest-first. A single entry larger than the budget is kept anyway - losing
    a chat's finding would be worse than a long prompt, and the stdin fix
    removes the ceiling for good once the bridge restarts.
    """
    with open(BOARD, encoding="utf-8") as fh:
        text = fh.read()
    parts = text.split("\n### ")
    header, entries = parts[0], parts[1:]
    if not entries:
        return 0

    keep, size = [], 0
    for entry in reversed(entries):
        if keep and (size + len(entry) > MAX_BOARD_CHARS or len(keep) >= KEEP_ENTRIES):
            break
        keep.append(entry)
        size += len(entry)
    keep.reverse()

    moved = entries[:len(entries) - len(keep)]
    if not moved:
        return 0

    new = not os.path.exists(ARCHIVE) or os.path.getsize(ARCHIVE) == 0
    with open(ARCHIVE, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Mary's noticeboard - archive\n\n"
                     "Entries moved off the live board to keep the bridge kick prompt under the\n"
                     "Windows command-line limit. Newest at the bottom, same as the board.\n")
        for entry in moved:
            fh.write("\n### " + entry.rstrip("\n") + "\n")

    with open(BOARD, "w", encoding="utf-8") as fh:
        fh.write("\n### ".join([header] + keep))
    return len(moved)


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
    ap.add_argument("--read", action="store_true",
                    help="print the noticeboard INCLUDING archived entries")
    ap.add_argument("--limit", type=int, default=40,
                    help="how many entries --read shows (default 40)")
    ap.add_argument("--inbox", action="store_true")
    args = ap.parse_args()

    if args.read:
        print(read_board(limit=args.limit, include_archive=True) or "(noticeboard empty)")
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

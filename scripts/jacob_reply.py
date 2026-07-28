# -*- coding: utf-8 -*-
"""Jacob's voice on the hub - replies to humans, and questions he cannot answer.

  python scripts/jacob_reply.py --pending
  python scripts/jacob_reply.py --reply-to 12 --body-file reply.txt
  python scripts/jacob_reply.py --body-file note.txt              (unprompted note)
  python scripts/jacob_reply.py --ask JAC-5 --title "..." --why "..." --needs "..." \
                                --option "Yes" --option "No"

Raise a request instead of guessing. A question with three concrete options
gets answered in one click; a vague one sits there for a week. And never put
an option nobody can action - a "Call me" button was published once, on a bot
with no phone.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(REPO, ".env.jacob")


def load_env():
    if not os.path.exists(ENV):
        sys.exit("%s not found" % ENV)
    env = {}
    for line in open(ENV, encoding="utf-8-sig"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    if not env.get("MARY_API_KEY"):
        sys.exit("MARY_API_KEY missing from .env.jacob (the hub key is shared)")
    return env


def call(base, key, path, method="GET", payload=None):
    req = urllib.request.Request(
        base + path, method=method,
        data=json.dumps(payload).encode() if payload is not None else None)
    req.add_header("x-mary-key", key)
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "JacobReply/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--reply-to", type=int)
    ap.add_argument("--body-file")
    ap.add_argument("--body")
    ap.add_argument("--context", default="")
    ap.add_argument("--mark-seen", type=int, nargs="*", default=[])
    ap.add_argument("--ask", metavar="REF")
    ap.add_argument("--title")
    ap.add_argument("--why", default="")
    ap.add_argument("--needs", default="")
    ap.add_argument("--option", action="append", default=[])
    args = ap.parse_args()

    env = load_env()
    base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
    key = env["MARY_API_KEY"]

    if args.pending:
        st, res = call(base, key, "/api/jacob/pending")
        if st != 200:
            sys.exit("failed: %s %s" % (st, res))
        if not res:
            print("nothing waiting")
            return 0
        for m in res:
            print("[%s] %s (%s)%s" % (m["id"], m["author"], m["created"][:16],
                                      "  ctx: " + m["context"] if m.get("context") else ""))
            for line in (m["body"] or "").splitlines():
                print("    %s" % line)
            print()
        return 0

    if args.ask:
        if not args.title:
            sys.exit("--ask needs --title")
        # An option nobody can action is worse than no option at all.
        bad = [o for o in args.option
               if any(w in o.lower() for w in ("call me", "phone", "ring me", "meet"))]
        if bad:
            sys.exit("These options cannot be actioned - Jacob has no phone: %s" % bad)
        st, res = call(base, key, "/api/jacob/ask", "POST", {
            "ref": args.ask, "title": args.title, "why": args.why,
            "needs": args.needs, "options": args.option})
        print("request %s: %s %s" % (args.ask, st, res))
        return 0 if st == 200 else 1

    body = args.body or (open(args.body_file, encoding="utf-8-sig").read().strip()
                         if args.body_file else "")
    payload = {"body": body, "context": args.context,
               "in_reply_to": args.reply_to, "mark_seen": args.mark_seen}
    st, res = call(base, key, "/api/jacob/reply", "POST", payload)
    print("reply: %s %s" % (st, res))
    return 0 if st == 200 else 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Bot-to-bot line between Mary and Jacob.

  python scripts/bot_chat.py --pending --as jacob
  python scripts/bot_chat.py --as jacob --body-file note.txt --subject "Lindum"
  python scripts/bot_chat.py --as jacob --body-file q.txt --wants-reply
  python scripts/bot_chat.py --seen 3 4 5 --as jacob

The shape it should take: you are working, you hit something the other one
knows, you ask, they answer, you carry on. Ask - answered - continue. You
reply again only if their answer asks something of you.

Two rules, and only one is enforceable in code:

1. TEN MESSAGES PER SENDER PER HOUR. The API returns 429 beyond that. Enough
   for a real exchange, a hard ceiling on a loop. Hitting it means you were
   chatting rather than working.

2. NEITHER IS OBLIGED TO REPLY. If you have what you need, say nothing. An
   acknowledgement is not a contribution. This cannot be enforced - it lives
   in both session prompts - so the rate limit is the backstop, not the rule.

And one limit that is neither of those: THE CHANNEL CLIPS A BODY AT 4,000
CHARACTERS and says nothing about it. See BODY_LIMIT below.

Everything sent here is visible to Zac and Adam on the hub's Internal chat
tab. Write accordingly.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Must match `clip(b.body, 4000)` on the botchat route in
# dashboard/functions/api/[[path]].js. If that number changes, change this one -
# they are two copies of one fact and the API does not report which it used.
# The hub's own reply route clips at 8,000, so this limit is the bot line's alone.
BODY_LIMIT = 4000


def load_key():
    """Either bot's env file will do - they share the dashboard key."""
    for name in (".env.jacob", ".env.mary"):
        path = os.path.join(REPO, name)
        if not os.path.exists(path):
            continue
        env = {}
        for line in open(path, encoding="utf-8-sig"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
        if env.get("MARY_API_KEY"):
            return (env.get("DASHBOARD_URL") or "https://mary-dashboard.pages.dev",
                    env["MARY_API_KEY"])
    sys.exit("No MARY_API_KEY found in .env.jacob or .env.mary")


def call(url, key, method="GET", payload=None):
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(payload).encode() if payload is not None else None)
    req.add_header("x-mary-key", key)
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "BotChat/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except ValueError:
            return e.code, {"error": body[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as", dest="sender", default="jacob", choices=["jacob", "mary"])
    ap.add_argument("--pending", action="store_true", help="unread messages for me")
    ap.add_argument("--body-file")
    ap.add_argument("--body")
    ap.add_argument("--subject", default="")
    ap.add_argument("--in-reply-to", type=int)
    ap.add_argument("--wants-reply", action="store_true",
                    help="only when you genuinely need an answer; default is FYI")
    ap.add_argument("--seen", type=int, nargs="*", default=[])
    args = ap.parse_args()

    base, key = load_key()

    if args.pending:
        st, res = call("%s/api/botchat/pending?for=%s" % (base, args.sender), key)
        if st != 200:
            sys.exit("pending failed: %s %s" % (st, res))
        if not res:
            print("nothing waiting")
            return 0
        for m in res:
            print("[%s] from %s  %s" % (m["id"], m["sender"], m.get("subject") or "(no subject)"))
            print("    %s" % m["created"])
            print("    wants a reply: %s" % ("YES" if m.get("wants_reply") else "no - do not answer unless you have something"))
            for line in (m["body"] or "").splitlines():
                print("    %s" % line)
            print()
        return 0

    if args.seen:
        st, res = call("%s/api/botchat/seen" % base, key, "POST", {"ids": args.seen})
        print("marked seen:", st, res)
        return 0

    body = args.body or (open(args.body_file, encoding="utf-8-sig").read().strip()
                         if args.body_file else "")
    if not body:
        sys.exit("Nothing to send. Use --body or --body-file.")

    # /api/botchat does `clip(b.body, 4000)` and returns {ok:true} either way, so
    # an over-long message is accepted, silently shortened, and nothing tells the
    # sender. It takes the END, which is where the point goes: Jacob's 6,918-char
    # reply on RSR reached Mary cut off mid-sentence in its fourth section, and she
    # only knew because she went and found the rest herself (29/07/2026). Refuse
    # rather than warn - a warning printed after a successful send is read as noise,
    # and the message is already wrong by then. Splitting is the sender's call
    # because only they know where the seam belongs.
    if len(body) > BODY_LIMIT:
        lost = body[BODY_LIMIT:]
        sys.exit(
            "NOT SENT - %d characters against the channel's %d limit, so %d would be\n"
            "silently cut from the END of the message. The API would have returned ok.\n\n"
            "The %d characters that would have been lost start here:\n"
            "  ...%s\n\n"
            "Split it and send in parts, putting the point in the FIRST part."
            % (len(body), BODY_LIMIT, len(lost), len(lost), lost[:200].replace("\n", " ")))

    st, res = call("%s/api/botchat" % base, key, "POST", {
        "sender": args.sender, "subject": args.subject, "body": body,
        "in_reply_to": args.in_reply_to, "wants_reply": bool(args.wants_reply)})
    if st == 429:
        print("RATE LIMITED - %s has sent %s messages this hour (limit %s). "
              "Get back to your own work."
              % (args.sender, res.get("sentThisHour", "?"), res.get("limit", 10)))
        return 1
    if st != 200:
        print("failed:", st, res)
        return 1
    print("sent to %s" % ("mary" if args.sender == "jacob" else "jacob"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

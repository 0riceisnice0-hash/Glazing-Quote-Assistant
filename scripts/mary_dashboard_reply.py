# -*- coding: utf-8 -*-
"""Reply to a dashboard message as Mary (appears in the hub's Message Mary tab).

Usage:
  python scripts/mary_dashboard_reply.py --reply-to 3 --body-file reply.txt [--context "Grange Hill"]
  python scripts/mary_dashboard_reply.py --body-file note.txt              (unprompted note to the thread)
  python scripts/mary_dashboard_reply.py --mark-seen 3 4 5                 (acknowledge without replying)
"""
import argparse
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reply-to", type=int)
    ap.add_argument("--body-file")
    ap.add_argument("--context", default="")
    ap.add_argument("--mark-seen", type=int, nargs="*", default=[])
    args = ap.parse_args()

    env = mg.load_env()
    payload = {"context": args.context, "mark_seen": args.mark_seen}
    if args.reply_to:
        payload["in_reply_to"] = args.reply_to
    if args.body_file:
        payload["body"] = open(args.body_file, encoding="utf-8-sig").read().strip()

    req = urllib.request.Request(
        env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev") + "/api/mary/reply",
        data=json.dumps(payload).encode(), method="POST")
    req.add_header("x-mary-key", env["MARY_API_KEY"])
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "MaryPoller/1.0")
    with urllib.request.urlopen(req, timeout=30) as r:
        print("dashboard reply:", r.status, r.read().decode()[:200])


if __name__ == "__main__":
    main()

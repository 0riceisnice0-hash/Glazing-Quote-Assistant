# -*- coding: utf-8 -*-
"""Ask the ledger, not your memory. Zero session tokens, deterministic.

  python scripts/mary_recall.py --job georgies --days 7      # everything recent on a job
  python scripts/mary_recall.py --grep "panic bar"           # any event mentioning it
  python scripts/mary_recall.py --adam --grep strip-out      # what Adam has said about it
  python scripts/mary_recall.py --kind email_sent --days 1   # what I already sent today
  python scripts/mary_recall.py --settled --job gordon-court # decisions already made

Before you email Adam, raise a request, or re-open a question: run --settled
and --kind email_sent on the job. "I have already addressed this with you"
(Adam, 28/07) exists because nothing did this lookup. Now something does.
"""
import argparse
import re
import sys
from datetime import datetime, timedelta

from mary_ledger import iter_events

# The kinds that constitute "settled": a human answered, or said so on the hub.
SETTLED_KINDS = ("request_answered",)
SETTLED_ACTORS = ("adam", "zac")


def parse_ts(ts):
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(ts)[:19].rstrip("Z"), fmt)
        except ValueError:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job")
    ap.add_argument("--kind")
    ap.add_argument("--actor")
    ap.add_argument("--adam", action="store_true", help="shortcut: --actor adam")
    ap.add_argument("--grep", help="case-insensitive regex over summary+body")
    ap.add_argument("--days", type=int)
    ap.add_argument("--settled", action="store_true",
                    help="answered requests plus Adam/Zac hub replies - the decided list")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--body", action="store_true", help="print stored excerpts too")
    a = ap.parse_args()
    if a.adam:
        a.actor = "adam"

    rx = re.compile(a.grep, re.I) if a.grep else None
    cutoff = datetime.now() - timedelta(days=a.days) if a.days else None

    hits = []
    for e in iter_events():
        if a.job and e.get("job") != a.job:
            continue
        if a.kind and e.get("kind") != a.kind:
            continue
        if a.actor and e.get("actor") != a.actor:
            continue
        if a.settled and not (e.get("kind") in SETTLED_KINDS or
                              (e.get("kind") == "hub_msg" and e.get("actor") in SETTLED_ACTORS)):
            continue
        if rx and not rx.search("%s %s" % (e.get("summary", ""), e.get("body", ""))):
            continue
        if cutoff:
            ts = parse_ts(e.get("ts"))
            if ts and ts < cutoff:
                continue
        hits.append(e)

    hits.sort(key=lambda e: str(e.get("ts") or ""))
    shown = hits[-a.limit:]
    for e in shown:
        print("%-16s %-5s %-16s %-18s %s" % (
            str(e.get("ts", ""))[:16], e.get("actor", ""), e.get("kind", ""),
            (e.get("job") or "-")[:18], e.get("summary", "")))
        if a.body and e.get("body"):
            for line in e["body"].splitlines()[:6]:
                print("                   | %s" % line)
        print("                   ref: %s" % e.get("ref", ""))
    print("\n%d match%s%s" % (len(hits), "" if len(hits) == 1 else "es",
          " (showing last %d)" % len(shown) if len(hits) > len(shown) else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

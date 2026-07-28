# -*- coding: utf-8 -*-
"""Notice when Mary is working hard on nothing, and stop her.

Overnight on 27/07 two chats ran 95 sessions and 12.7 hours between them
without a single new work order. The findings were real, but the loop had no
reason to end: they were handing each other AUDIT METHODS rather than facts, so
every session generated its own next input.

Nothing in the system could see it happening. Each individual session looked
reasonable - a handoff arrived, it was acted on, something was found. Only the
shape over hours was wrong, and nothing was looking at the shape.

Three limits, all measured from the poller log so they survive a restart:

  CIRCLING   - a chat that keeps running without consuming new work
  DAILY TIME - total session hours across all chats in a rolling day
  UNANSWERED - requests piling up faster than a human can possibly answer

The first two stop dispatch. The third does not stop anything - it is fed into
the kick prompt so a chat knows the queue it is adding to, because a 29th
request for Adam is worth less than nothing while 28 sit unanswered.

  python scripts/mary_budget.py            # what the limits say right now
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(REPO, "test-results", "mary-inbox", "poller.log")
STATE = os.path.join(REPO, "data", "dashboard-state.json")

# A chat may run this many times in the window without consuming a work order.
CIRCLING_RUNS = 5
CIRCLING_HOURS = 6
# Total session time across everything, per rolling day. A normal working day
# has been 2-4 hours; the 27/07 runaway spent 17. Eight leaves real work room
# and still catches a loop long before it costs a night. Override with
# MARY_DAILY_HOURS when a genuinely heavy day is expected.
DAILY_HOURS = float(os.environ.get("MARY_DAILY_HOURS", "8"))
# Above this many open requests, raising more is not the constraint.
REQUEST_BACKLOG = 12


def _since(hours):
    return (dt.datetime.now() - dt.timedelta(hours=hours)).strftime("[%Y-%m-%d %H:%M")


def read_log(hours):
    if not os.path.exists(LOG):
        return []
    cutoff = _since(hours)
    with open(LOG, encoding="utf-8", errors="replace") as fh:
        return [l.rstrip("\n") for l in fh if l >= cutoff]


def usage(hours=24):
    """Session count and total seconds per chat over the window."""
    per = {}
    for line in read_log(hours):
        m = re.search(r"\[([a-z0-9-]+)\] session exit \d+ after (\d+)s", line)
        if m:
            rec = per.setdefault(m.group(1), {"runs": 0, "seconds": 0, "with_work": 0})
            rec["runs"] += 1
            rec["seconds"] += int(m.group(2))
    # A dispatch line says how many work orders came with it.
    for line in read_log(hours):
        m = re.search(r"dispatch -> \[([a-z0-9-]+)\][^:]*: (\d+) order", line)
        if m and int(m.group(2)) > 0:
            per.setdefault(m.group(1), {"runs": 0, "seconds": 0, "with_work": 0})
            per[m.group(1)]["with_work"] += 1
    return per


def open_requests():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return sum(1 for r in json.load(fh).get("requests", []) if r.get("status") == "open")
    except Exception:
        return 0


def circling(chat):
    """Is this chat running repeatedly without new work coming in?"""
    rec = usage(CIRCLING_HOURS).get(chat)
    if not rec:
        return False, ""
    if rec["runs"] >= CIRCLING_RUNS and rec["with_work"] == 0:
        return True, ("%s has run %d times in %dh on handoffs alone, consuming no new work and "
                      "using %.1f hours. That is the 27/07 pattern - stopping it."
                      % (chat, rec["runs"], CIRCLING_HOURS, rec["seconds"] / 3600))
    return False, ""


def day_spend():
    per = usage(24)
    return sum(r["seconds"] for r in per.values()) / 3600.0


def check(chat=None):
    """Returns (ok_to_dispatch, reason)."""
    spent = day_spend()
    if spent >= DAILY_HOURS:
        return False, ("daily session budget spent: %.1f of %.1f hours in the last 24h"
                       % (spent, DAILY_HOURS))
    if chat:
        looping, why = circling(chat)
        if looping:
            return False, why
    return True, ""


def prompt_note():
    """A line for the kick prompt so a chat can see what it is adding to."""
    n = open_requests()
    if n < REQUEST_BACKLOG:
        return ""
    return ("\nBEFORE YOU RAISE ANYTHING: %d requests are already open and unanswered. Adam cannot "
            "clear that in a day, so a new one is worth less than nothing unless it is more urgent "
            "than what is already waiting. Prefer answering, consolidating or closing an existing "
            "request over adding to the pile - and if this turn has nothing better to offer than "
            "another observation, say so and stop. A clean result IS a result." % n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat")
    args = ap.parse_args()
    per = usage(24)
    print("SESSION USE, LAST 24H")
    print("  %-22s %6s %8s %10s" % ("chat", "runs", "hours", "with work"))
    for k, r in sorted(per.items(), key=lambda kv: -kv[1]["seconds"]):
        print("  %-22s %6d %8.1f %10d" % (k, r["runs"], r["seconds"] / 3600, r["with_work"]))
    print("  %-22s %6s %8.1f" % ("TOTAL", "", day_spend()))
    print("\nopen requests waiting on a human: %d" % open_requests())
    ok, why = check(args.chat)
    print("\ndispatch allowed: %s%s" % (ok, "" if ok else "  <- " + why))
    return 0


if __name__ == "__main__":
    sys.exit(main())

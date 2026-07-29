# -*- coding: utf-8 -*-
"""A ceiling on how much Mary can spend, tightest while nobody is watching.

Overnight on 27/07 two chats ran 95 sessions and 12.7 hours between them
without a single new work order. The findings were real, but the loop had no
reason to end: they were handing each other AUDIT METHODS rather than facts, so
every session generated its own next input. Priced as API calls that night was
most of a ~GBP 2,400 bill, and the cost was not the hours - it was that every
resumed session re-read a chat that had grown to 27 MB before it did anything.

Two defences, and they are not the same thing:

  THE CAUSE is handled in mary_bridge: new information is the only reason to
  run, so a chat with nothing new never wakes. That is the fix.

  THIS FILE IS THE BACKSTOP. It assumes the fix has a hole in it. Its whole job
  is to bound the damage of a loop nobody has thought of yet, in the hours when
  nobody will notice for eight of them.

NIGHT IS BUDGETED SEPARATELY AND TIGHTLY. Between 22:00 and 07:00 there is
nobody to answer a request, no supplier reading email, and no reason to spend
like a working day. Mail that arrives at 03:00 keeps until 07:00; the queue is
durable and nothing is lost by waiting.

BUDGETS ARE SCOPED TO THE WINDOW THEY BELONG TO, not to a rolling 24 hours.
The old rolling window meant one bad night poisoned the following day: at 10:00
on 28/07 she was held back on "17.1 of 8.0 hours" that had all been spent before
07:00. A night's overspend must not be able to block the morning. Each window
starts at zero.

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

# 22:00 to 07:00. Nobody is reading, nobody is replying, nothing is urgent
# enough to be worth an unattended loop.
NIGHT_FROM, NIGHT_TO = 22, 7

# Session-hours allowed within one window. Night is deliberately small: enough
# for a couple of genuine pieces of work, nowhere near enough for a runaway.
NIGHT_HOURS = float(os.environ.get("MARY_NIGHT_HOURS", "1.5"))
DAY_HOURS = float(os.environ.get("MARY_DAY_HOURS", "8"))

# Hours alone is a poor proxy for cost. The 27/07 bill was driven by SESSION
# COUNT against bloated chats - each one re-read the whole conversation before
# doing anything - so cap the count as well. Twenty in a working day is already
# far more than a normal one.
NIGHT_SESSIONS = int(os.environ.get("MARY_NIGHT_SESSIONS", "6"))
DAY_SESSIONS = int(os.environ.get("MARY_DAY_SESSIONS", "40"))

# A chat may run this many times in the window without consuming a work order.
CIRCLING_RUNS = 5
CIRCLING_HOURS = 6
# Above this many open requests, raising more is not the constraint.
REQUEST_BACKLOG = 12


def is_night(now=None):
    h = (now or dt.datetime.now()).hour
    return h >= NIGHT_FROM or h < NIGHT_TO


def window(now=None):
    """(label, started_at, hours_budget, session_budget) for the window we are in.

    The night window spans midnight, so before 07:00 it started at 22:00
    YESTERDAY. Getting that wrong would reset the budget at midnight and hand a
    runaway a fresh allowance exactly when nobody is watching.
    """
    now = now or dt.datetime.now()
    if is_night(now):
        start = now.replace(hour=NIGHT_FROM, minute=0, second=0, microsecond=0)
        if now.hour < NIGHT_TO:
            start -= dt.timedelta(days=1)
        return "night", start, NIGHT_HOURS, NIGHT_SESSIONS
    start = now.replace(hour=NIGHT_TO, minute=0, second=0, microsecond=0)
    return "day", start, DAY_HOURS, DAY_SESSIONS


def read_log(since):
    """Log lines at or after a datetime. The log is timestamp-prefixed and
    written in order, so a string compare is enough and costs nothing."""
    if not os.path.exists(LOG):
        return []
    cutoff = since.strftime("[%Y-%m-%d %H:%M")
    with open(LOG, encoding="utf-8", errors="replace") as fh:
        return [l.rstrip("\n") for l in fh if l >= cutoff]


def usage(since):
    """Session count and total seconds per chat since a datetime.

    The pricing lab does not appear here: it logs its own completion line
    rather than a session exit, and it is bounded by its own 03:00 hard stop.
    Counting it would let one ordinary lab night consume the whole allowance
    and block the 07:00 mail run.
    """
    lines = read_log(since)
    per = {}
    for line in lines:
        m = re.search(r"\[([a-z0-9-]+)\] session exit \d+ after (\d+)s", line)
        if m:
            rec = per.setdefault(m.group(1), {"runs": 0, "seconds": 0, "with_work": 0})
            rec["runs"] += 1
            rec["seconds"] += int(m.group(2))
    for line in lines:
        m = re.search(r"dispatch -> \[([a-z0-9-]+)\][^:]*: (\d+) order", line)
        if m and int(m.group(2)) > 0:
            per.setdefault(m.group(1), {"runs": 0, "seconds": 0, "with_work": 0})
            per[m.group(1)]["with_work"] += 1
    return per


def spent(since):
    per = usage(since)
    return (sum(r["seconds"] for r in per.values()) / 3600.0,
            sum(r["runs"] for r in per.values()))


SEND_LOG = os.path.join(REPO, "data", "mary-send-log.jsonl")

# ---------------------------------------------------------------- tokens
# Phase 4 (AGENT-AUDIT.md): hours and session counts were only ever PROXIES
# for cost, kept because tokens were invisible. The bridge now measures what a
# session actually grew the transcript by, so the spend is real. The caps stay
# as circuit breakers - trip one and something is LOOPING, which is a bug to
# find, not a budget to raise.
TOKENS_LOG = os.path.join(REPO, "data", "mary-usage.jsonl")
DAY_TOKENS = int(os.environ.get("MARY_DAY_TOKENS", "12000000"))     # ~2-3x a normal day
NIGHT_TOKENS = int(os.environ.get("MARY_NIGHT_TOKENS", "2000000"))


def log_tokens(chat, seconds, delta_bytes, size_after_mb):
    """One line per session: what it cost. Called by the bridge; never fatal."""
    rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "chat": chat,
           "seconds": int(seconds), "delta_bytes": int(delta_bytes),
           "est_tokens": int(max(0, delta_bytes) // 4),
           "size_after_mb": round(size_after_mb, 2)}
    try:
        os.makedirs(os.path.dirname(TOKENS_LOG), exist_ok=True)
        with open(TOKENS_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
    except Exception:
        pass


def tokens_spent(since):
    """(total est tokens, {chat: est tokens}) since a datetime."""
    cutoff = since.isoformat(timespec="seconds")
    total, per = 0, {}
    try:
        with open(TOKENS_LOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if (d.get("at") or "") >= cutoff:
                    t = int(d.get("est_tokens") or 0)
                    total += t
                    per[d.get("chat", "?")] = per.get(d.get("chat", "?"), 0) + t
    except Exception:
        pass
    return total, per


def emails_today():
    """(count, [subjects]) sent since midnight. Attention spent, not tokens."""
    today = dt.date.today().isoformat()
    out = []
    try:
        with open(SEND_LOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if (d.get("at") or "").startswith(today) and d.get("ok"):
                    out.append(d.get("subject") or "(no subject)")
    except Exception:
        pass
    return len(out), out


def open_requests():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return sum(1 for r in json.load(fh).get("requests", []) if r.get("status") == "open")
    except Exception:
        return 0


def circling(chat):
    """Is this chat running repeatedly without new work coming in?"""
    rec = usage(dt.datetime.now() - dt.timedelta(hours=CIRCLING_HOURS)).get(chat)
    if not rec:
        return False, ""
    if rec["runs"] >= CIRCLING_RUNS and rec["with_work"] == 0:
        return True, ("%s has run %d times in %dh on handoffs alone, consuming no new work and "
                      "using %.1f hours. That is the 27/07 pattern - stopping it."
                      % (chat, rec["runs"], CIRCLING_HOURS, rec["seconds"] / 3600))
    return False, ""


def check(chat=None):
    """Returns (ok_to_dispatch, reason). Reason is shown on the hub."""
    label, start, hour_cap, session_cap = window()
    hours, runs = spent(start)
    since = start.strftime("%H:%M")
    if hours >= hour_cap:
        return False, ("%s budget spent: %.1f of %.1f session-hours since %s. Work stays queued "
                       "and goes out %s." % (label, hours, hour_cap, since,
                                             "at 07:00" if label == "night" else "tomorrow"))
    if runs >= session_cap:
        return False, ("%s budget spent: %d of %d sessions since %s. Work stays queued and goes "
                       "out %s." % (label, runs, session_cap, since,
                                    "at 07:00" if label == "night" else "tomorrow"))
    tok, _ = tokens_spent(start)
    tok_cap = NIGHT_TOKENS if label == "night" else DAY_TOKENS
    if tok >= tok_cap:
        return False, ("%s token breaker tripped: ~%s of %s estimated tokens since %s. The cap is "
                       "2-3x a normal day, so something is looping - find it in "
                       "data/mary-usage.jsonl before anything else runs."
                       % (label, "{:,}".format(tok), "{:,}".format(tok_cap), since))
    if chat:
        looping, why = circling(chat)
        if looping:
            return False, why
    return True, ""


def prompt_note(chat=None):
    """A line for the kick prompt so a chat can see what it is adding to."""
    parts = []
    label, start, hour_cap, session_cap = window()
    tok, per = tokens_spent(start)
    if tok:
        mine = per.get(chat, 0) if chat else 0
        tok_cap = NIGHT_TOKENS if label == "night" else DAY_TOKENS
        parts.append(
            "\nTOKEN COST this %s window: ~%s of %s estimated%s. Cost follows context: a lean job "
            "file and a focused turn are what keep this number small."
            % (label, "{:,}".format(tok), "{:,}".format(tok_cap),
               (", of which this chat ~%s" % "{:,}".format(mine)) if mine else ""))
    if label == "night":
        hours, runs = spent(start)
        parts.append(
            "\nIT IS THE MIDDLE OF THE NIGHT and you are on a reduced budget: %.1f of %.1f "
            "session-hours and %d of %d sessions are gone since %s. Nobody is reading email, "
            "nobody can answer a request, and no supplier will reply before morning. Do what "
            "this work order actually needs and stop. Anything that can wait until 07:00 should."
            % (hours, hour_cap, runs, session_cap, start.strftime("%H:%M")))
    sent, subjects = emails_today()
    if sent:
        jobs = sorted({s.split(" - ")[0].split(" (")[0][:24] for s in subjects})
        # Context, not a cap. There is no number of emails that is too many if
        # each one is an error or something that moves the position - and no
        # number that is few enough to make activity worth sending. This is here
        # so she can see what she has already told him before telling him again.
        parts.append(
            "\nALREADY SENT TO ADAM TODAY (%d): %s.\nBefore you write again, ask the only question "
            "that matters: does he do something different, or believe something different about "
            "where the job stands, because you told him? An error or a moved number always earns "
            "it, however many you have sent. Progress, activity, and correcting your own earlier "
            "email do not - and if you are reaching for a correction, the fix is to check before "
            "sending, not to send again." % (sent, "; ".join(jobs)))

    n = open_requests()
    if n >= REQUEST_BACKLOG:
        parts.append(
            "\nBEFORE YOU RAISE ANYTHING: %d requests are already open and unanswered. Adam cannot "
            "clear that in a day, so a new one is worth less than nothing unless it is more urgent "
            "than what is already waiting. Prefer answering, consolidating or closing an existing "
            "request over adding to the pile - and if this turn has nothing better to offer than "
            "another observation, say so and stop. A clean result IS a result." % n)
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat")
    args = ap.parse_args()
    label, start, hour_cap, session_cap = window()
    per = usage(start)
    hours, runs = spent(start)
    print("WINDOW: %s, since %s" % (label.upper(), start.strftime("%a %H:%M")))
    print("  %-22s %6s %8s %10s" % ("chat", "runs", "hours", "with work"))
    for k, r in sorted(per.items(), key=lambda kv: -kv[1]["seconds"]):
        print("  %-22s %6d %8.1f %10d" % (k, r["runs"], r["seconds"] / 3600, r["with_work"]))
    print("  %-22s %6d %8.1f" % ("TOTAL", runs, hours))
    print("  %-22s %6d %8.1f   <- ceiling" % ("BUDGET", session_cap, hour_cap))
    print("\nopen requests waiting on a human: %d" % open_requests())
    ok, why = check(args.chat)
    print("\ndispatch allowed: %s%s" % (ok, "" if ok else "  <- " + why))
    return 0


if __name__ == "__main__":
    sys.exit(main())

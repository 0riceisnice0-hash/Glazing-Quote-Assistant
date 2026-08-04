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

# OVERNIGHT IS OFF (Zac, 03/08: "do we really need it to run overnight unless
# directly called to by Adam if he's working late one day?"). Measured the same
# day: 57.3% of ALL bot spend fell between 22:00 and 07:00, and the single
# busiest hour of the week was 06:00 - work nobody asked for, done while nobody
# was awake to read it. This is the cheapest saving available and it costs
# nothing real, because the queue is durable and 07:00 is soon enough.
#
# To let them work a late evening, create the file below; it names its own
# expiry so an override cannot be left on by accident.
#   python scripts/mary_budget.py --allow-tonight
NIGHT_OK_FILE = os.path.join(REPO, "data", "night-allowed.json")


def night_allowed(now=None):
    """(allowed, why). An override expires on its own; nobody has to remember."""
    now = now or dt.datetime.now()
    try:
        with open(NIGHT_OK_FILE, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (IOError, ValueError):
        return False, ""
    until = rec.get("until") or ""
    if until and now.isoformat(timespec="seconds") < until:
        return True, "overnight allowed until %s by %s" % (until[11:16], rec.get("by", "?"))
    return False, ""

# Session-hours allowed within one window. Night is deliberately small: enough
# for a couple of genuine pieces of work, nowhere near enough for a runaway.
NIGHT_HOURS = float(os.environ.get("MARY_NIGHT_HOURS", "1.5"))
DAY_HOURS = float(os.environ.get("MARY_DAY_HOURS", "8"))

# Session count was a stand-in for cost back when tokens were invisible: the
# 27/07 bill came from re-reading bloated chats, and counting sessions was the
# closest thing to counting that. Both halves of that reasoning have since gone
# - rotation keeps transcripts small, and log_tokens() measures the spend for
# real - so the count is now the LOOSEST of the three limits, not the tightest.
#
# It was 40, and on 29/07 it tripped at 17:03 with hours at 60% and tokens at
# 21%. All forty sessions had consumed a real work order; none were circling.
# What it actually held was a quote Adam asked her to check on a tender closing
# THAT DAY, parked until 07:00 the next morning. A proxy outranking the two
# measures it was standing in for is a bug, and this is what it cost.
#
# 120 is a circuit breaker rather than a budget: three times a real working day
# (40 sessions, 4.8h, 2.5M tokens observed), so tripping it means something is
# looping and the tokens or the hours will almost certainly say so first.
NIGHT_SESSIONS = int(os.environ.get("MARY_NIGHT_SESSIONS", "6"))
DAY_SESSIONS = int(os.environ.get("MARY_DAY_SESSIONS", "120"))

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
# REWRITTEN 03/08/2026. This used to record transcript GROWTH (delta_bytes/4)
# and call it the cost. The cost of a permanent per-job chat is the context it
# RE-READS every turn, which is a different number by about 30x - see
# scripts/mary_cost.py for the measurement and the requestId dedupe trap. The
# allowance ran out on 30/07 with this meter reporting single-digit millions
# against a 12M cap, so nothing ever fired.
#
# The numbers below are CIRCUIT BREAKERS, not budgets (MASTER-PLAN §0: make
# them think, do not cap them). Spending discipline comes from each session
# being cheap - rotation on context, the night curfew, lean seeds - not from a
# quota that stops work on a deadline. Tripping one of these means something is
# LOOPING, and the answer is to find the loop.
#
# Sizing: a normal bot day measured 365M context tokens and the target ceiling
# is ~118M/day (5% of the weekly allowance). 250M is comfortably above the
# target and far below the 776M day that killed the plan.
TOKENS_LOG = os.path.join(REPO, "data", "mary-usage.jsonl")
DAY_TOKENS = int(os.environ.get("MARY_DAY_TOKENS", "250000000"))
NIGHT_TOKENS = int(os.environ.get("MARY_NIGHT_TOKENS", "25000000"))
# What we are actually aiming at, shown to her as evidence rather than enforced.
DAY_TARGET = int(os.environ.get("MARY_DAY_TARGET", "118000000"))


def log_tokens(chat, session_id, seconds, since):
    """One line per session: what it really cost. Never fatal.

    `since` bounds this run of a resumed chat - the transcript is appended to,
    so without it we would re-count the whole conversation every time.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import mary_cost
        c = mary_cost.session_cost(session_id, since)
        now_ctx = mary_cost.context_size(session_id)
    except Exception:
        return
    rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "chat": chat,
           "session": session_id, "seconds": int(seconds),
           "context_tokens": c["context"], "output_tokens": c["output"],
           "calls": c["calls"], "per_call": c["per_call"],
           # What the NEXT turn of this chat will carry. This is the number
           # rotation keys on, and the one worth watching climb.
           "context_now": now_ctx}
    try:
        os.makedirs(os.path.dirname(TOKENS_LOG), exist_ok=True)
        with open(TOKENS_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
    except Exception:
        pass


def tokens_spent(since):
    """(total context tokens, {chat: context tokens}) since a datetime.

    Rows written before 03/08 carry `est_tokens`, which measured transcript
    growth and is ~30x too small. They are IGNORED rather than mixed in - a
    budget half-built from a broken meter is worse than one with a short
    history, and the windows here are same-day anyway.
    """
    cutoff = since.isoformat(timespec="seconds")
    total, per = 0, {}
    try:
        with open(TOKENS_LOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if (d.get("at") or "") < cutoff:
                    continue
                if "context_tokens" not in d:
                    continue
                t = int(d.get("context_tokens") or 0)
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
    # The curfew comes first: it is not a budget that can be spent down, it is
    # a decision that this work waits for morning.
    if label == "night":
        ok, why = night_allowed()
        if not ok:
            return False, ("Overnight running is off. Work stays queued and goes out at "
                           "%02d:00. If tonight is genuinely different, run "
                           "scripts\\mary_budget.py --allow-tonight." % NIGHT_TO)
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


def landed(days=7):
    """(sends, replies, requests_answered) in the last N days - did they land?

    Zac, 03/08: "if they sent a bunch of emails - first of all, why? And why
    did they then need to send more?" She cannot answer that without seeing
    whether the last ones landed, so this puts it in front of her. It is
    evidence, not a limit: there is no number of emails that is too many if
    each one moves the job, and no number small enough to make activity worth
    sending.

    COUNT ONLY WHAT IS ACTUALLY A REPLY TO HER. The obvious version of this -
    "any message from Adam" - reads 162 against 54 sends and concludes the
    interruptions are working. They are not: 35 of those are him replying on
    Gintare's quote threads in estimating@, and most hub messages are him
    giving an instruction, not answering one of her emails. The only
    unambiguous signal is mail he addressed to mary@, which is 18 against 54 -
    the same one-in-three the audit found by hand. A flattering measure here
    would have told her to keep going, which is the whole problem.
    """
    try:
        import mary_ledger
        cutoff = (dt.datetime.now() - dt.timedelta(days=days)).isoformat(timespec="seconds")
        sends = replies = answered = 0
        for e in mary_ledger.iter_events():
            if str(e.get("ts") or "") < cutoff:
                continue
            kind = e.get("kind")
            if kind == "email_sent":
                sends += 1
            elif kind == "request_answered":
                answered += 1
            elif (kind == "mail_received" and e.get("actor") in ("adam", "zac")
                  and "mary@" in str(e.get("summary") or "")):
                replies += 1
        return sends, replies, answered
    except Exception:
        return 0, 0, 0


# ------------------------------------------------------------- batching
# THE SINGLE BIGGEST SAVING IN THE SYSTEM, and it lives here because it is a
# spending decision, not a routing one.
#
# The bridges used to dispatch the moment anything arrived. Measured 04/08 over
# the four days Mary ran: 1,868 dispatches for 249 work orders. A run costs a
# median 7.2M context tokens whether it handles one email or ten, because the
# cost is the turns, not the trigger - so handling them one at a time is paying
# ten times for the same sitting.
#
# Zac, 04/08, on how he did this by hand: "I would just use one chat until that
# task is done, then update docs and start a new one."
BATCH_WAIT = int(os.environ.get("BOT_BATCH_WAIT", "900"))       # 15 minutes
BATCH_MAX = int(os.environ.get("BOT_BATCH_MAX", "8"))
BATCH_URGENT_WAIT = int(os.environ.get("BOT_BATCH_URGENT", "60"))


def ready_to_dispatch(ages, urgent=0, wait=None, most=None):
    """(go, why). `ages` is seconds each queued item has waited.

    Three ways to go, and the first is what stops batching becoming rudeness:
      - somebody is waiting. A hub message is a person looking at the screen;
        they wait a minute, not fifteen.
      - the batch is big enough to be worth a sitting.
      - the oldest thing has waited long enough. Nothing is stuck behind a
        quiet queue, ever.
    """
    if not ages:
        return False, "nothing queued"
    wait = BATCH_WAIT if wait is None else wait
    most = BATCH_MAX if most is None else most
    oldest = max(ages)
    if urgent and oldest >= BATCH_URGENT_WAIT:
        return True, "somebody is waiting (%d item(s), %ds old)" % (urgent, int(oldest))
    if len(ages) >= most:
        return True, "%d work orders queued" % len(ages)
    if oldest >= wait:
        return True, "oldest has waited %d min" % int(oldest / 60)
    return False, "batching - %d item(s), oldest %dm of %dm" % (
        len(ages), int(oldest / 60), int(wait / 60))


# THE LAST BIG LEVER, measured 04/08. A run is a median 37 calls, and EVERY
# call re-sends the whole context - so the cost of a run is calls x context,
# and with a lean seed the calls are now the bigger half.
#
# Of 3,146 tool calls across 90 bot runs, Bash was 3,146 of them - about 35 per
# run. Most were one-liners: an ls, then a cat, then a grep, then a python -c.
# Each of those round-trips costs a full context re-send for a line of output.
# Ten one-liners cost ten times what one script costs, and produce the same
# answer.
# ONE SITTING PER CHAT, for all three. Zac, 04/08: "I would just use one chat
# until that task is done, then update docs and start a new one."
#
# It lives here rather than in one bridge because it drifted immediately when
# it did not: Mary had it, Jacob and Joseph did not, and nothing said so until
# the three were checked side by side.
#
# Why it is worth more than it first looked. A run is a median 37 calls and
# every call resends the whole context, so the seed is not paid once - it is
# paid 37 times. A resumed chat carries ~170k a call; a fresh one ~40k. That is
# the difference between a 6.3M run and a 1.5M one.
ONE_SITTING = os.environ.get("BOT_ONE_SITTING", "1") != "0"

# WHEN A CHAT IS TOO HEAVY TO CARRY ON WITH. 75,000, down from 150,000 on
# 04/08, and in one place because it had already drifted three ways - Mary
# 150k, Jacob 120k, Joseph 120k, preflight hardcoding 150k twice.
#
# Measured across 842 real calls that day: the median call was carrying 81,377
# tokens and the mean 100,687. The whole bill is context x turns, so the size
# of what a chat drags behind it IS the cost. Sorting every call by what it
# carried:
#
#     calls over 150,000 :  133 calls, 34% of the day's spend
#     calls over 100,000 :  322 calls, 61%
#     calls over  75,000 :  496 calls, 78%
#
# Retiring at 75,000 rather than 150,000 takes roughly a third off. Rotating
# more often is close to free: a fresh chat is seeded from a bounded file for
# about 9,500 tokens, where resuming an old one costs ~129,000 a call, every
# call. The saving is not a trade against memory either - what a bot knows
# lives in data/jobs and data/companies, not in the conversation. The chat is
# only where the thinking happened, and the file is what it was for.
ROTATE_CONTEXT = int(os.environ.get("BOT_ROTATE_CONTEXT", "75000"))


def should_retire(started, context_now, rotate_at):
    """(retire, why). Retire a finished chat, or an overweight one.

    The CALLER still has to check its memory file first - retiring a chat whose
    file is out of contract seeds the next one from a broken file and loses the
    job. That gate is what makes this safe rather than reckless.
    """
    if context_now <= 0:
        return False, ""                     # never run; nothing to retire
    if ONE_SITTING and started:
        return True, "finished its sitting"
    if context_now >= rotate_at:
        return True, "carrying %s context tokens" % "{:,}".format(context_now)
    return False, ""


WORK_STYLE = """
HOW TO WORK, AND IT IS A COST DECISION NOT A STYLE ONE. Every tool call resends
this whole conversation, so a run costs (number of calls) x (its size). Runs
here average 35 shell calls and most are one-liners.
  - Do shell work in ONE script, not ten commands. If you need to look at four
    files, write one script that reads all four and prints what you need.
  - Read a file once. If you have read it this session, you already have it.
  - Do not explore. `mary_recall`, `crm.py` and the job file answer most
    questions without opening anything.
  - Say what you found and move on. A summary of a thing you just printed is
    another call for nothing."""


def prompt_note(chat=None, sends=True):
    """A line for the kick prompt so a chat can see what it is adding to.

    `sends=False` for Jacob. He has no send path at all, and the email and
    request-backlog evidence below is read from Mary's send log and Mary's
    request board - showing him her send-to-reply ratio would be telling a bot
    off for somebody else's emails. Cost is shared; attention is not.
    """
    parts = []
    label, start, hour_cap, session_cap = window()
    tok, per = tokens_spent(start)
    if tok:
        mine = per.get(chat, 0) if chat else 0
        parts.append(
            "\nTOKEN COST this %s window: %s against a target of %s for the whole day "
            "(hard breaker at %s)%s. This is measured, not guessed. Cost is CONTEXT x TURNS: "
            "the length of what you are carrying, times how many times you speak. A lean job "
            "file, a focused turn, and not re-reading what you already know are the whole game."
            % (label, "{:,}".format(tok), "{:,}".format(DAY_TARGET),
               "{:,}".format(NIGHT_TOKENS if label == "night" else DAY_TOKENS),
               (", of which this chat %s" % "{:,}".format(mine)) if mine else ""))
    if label == "night":
        parts.append(
            "\nIT IS THE MIDDLE OF THE NIGHT and overnight running is normally off - somebody "
            "lifted the curfew for tonight specifically. Nobody is reading email, nobody can "
            "answer a request, and no supplier will reply before morning. Do the thing that "
            "was worth staying up for, and stop.")
    if not sends:
        return "".join(parts)

    sends, replies, answered = landed()
    if sends:
        parts.append(
            "\nDID THE LAST ONES LAND? %d email(s) went in the last 7 days and Adam wrote "
            "back to mary@ %d time(s)%s. %s"
            % (sends, replies,
               (", and answered %d request(s) on the hub" % answered) if answered else "",
               "He is engaging with these - keep going." if replies >= sends * 0.5 else
               "So most of them earned nothing back. Work out why the last one did not "
               "before you write another, because it will probably go the same way. The "
               "only question that matters: does he DO something different, or believe "
               "something different about where the job stands, because you told him? An "
               "error or a moved number always earns it. Progress and activity do not."))

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


def allow_tonight(hours=None, by="zac"):
    """Lift the curfew for one night. Expires by itself."""
    now = dt.datetime.now()
    # Default: until 07:00, whether that is tonight's or tomorrow's.
    until = now.replace(hour=NIGHT_TO, minute=0, second=0, microsecond=0)
    if until <= now:
        until += dt.timedelta(days=1)
    if hours:
        until = now + dt.timedelta(hours=hours)
    rec = {"until": until.isoformat(timespec="seconds"), "by": by,
           "set_at": now.isoformat(timespec="seconds")}
    with open(NIGHT_OK_FILE, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat")
    ap.add_argument("--allow-tonight", action="store_true",
                    help="lift the overnight curfew until 07:00")
    ap.add_argument("--hours", type=float, help="with --allow-tonight: for this long instead")
    args = ap.parse_args()
    if args.allow_tonight:
        rec = allow_tonight(args.hours)
        print("overnight running allowed until %s" % rec["until"])
        return 0
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

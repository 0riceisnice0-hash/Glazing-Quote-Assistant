# -*- coding: utf-8 -*-
"""THE OVERNIGHT PRICING LAB - the only work Mary does without new input.

Everywhere else in the system a session runs only when new information arrives,
because that is what stopped the 27/07 runaway. This is the deliberate
exception: one chat, one goal.

IT WAS 01:00-03:00 AND IS NOW THE WHOLE NIGHT (Zac, dashmsg-97, 29/07: "work on
improving your pricing engine overnight, bypass the 1am to 3am window"). Two
gates had to move, not one - the window below, and the scheduled task, which
carried a single 01:00 trigger with no repetition, so widening the code alone
would have changed nothing. Same lesson as Jacob's uptime the same evening.

WHAT REPLACES THE TWO-HOUR STOP, because something has to. The narrow window WAS
the safety, and 27/07 (95 sessions, 12.7 hours, most of a ~GBP 2,400 bill) is
what it was protecting against:

  - a per-night ceiling on lab hours, counted off this script's own log lines
  - the existing yield to real work - a mail session always outranks the lab
  - a session is never started that cannot FINISH before 07:00, so the lab can
    no longer be holding the session lock when the morning update wants it

The goal is the pricing engine and nothing else. Go through jobs Fenster has
already quoted, run the engine over them, and work out WHY it missed. Not more
observations about contracts - the overnight spiral produced plenty of those.
Rates, bands, and the reasons behind a delta.

The goal is the pricing engine and nothing else. Go through jobs Fenster has
already quoted, run the engine over them, and work out WHY it missed. Not more
observations about contracts - the overnight spiral produced plenty of those.
Rates, bands, and the reasons behind a delta.

There is a real answer waiting: on St Mary's the whole-job error was a
respectable +4.4%, but by size band it was -35.5%, -1.2%, +37.5% and +35.2% -
the errors cancelled. The engine is a fair whole-package predictor and a poor
per-element one, and nobody has yet worked out why the small band runs low and
the large band runs high. That is the kind of thing this window is for.

  python scripts/mary_night_pricing.py            # run it (respects the window)
  python scripts/mary_night_pricing.py --now      # run regardless of the clock
  python scripts/mary_night_pricing.py --status   # window, hours used, would it run
"""
import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_poller as mp
import mary_router as router

REPO = mg.REPO
CHAT_KEY = "pricing-lab"
WINDOW = (22, 7)         # 22:00 to 07:00, spanning midnight
HARD_STOP_MINUTES = 115  # no single session runs longer than this
# Lab hours per night, its own ceiling because mary_budget deliberately does not
# count them. Nine hours of window, six of work: enough for several real lines of
# enquiry, and still a number that says "something is looping" if it is reached.
NIGHT_HOURS = float(os.environ.get("MARY_LAB_NIGHT_HOURS", "6.0"))
# Never start something that cannot finish before the morning run.
MIN_MINUTES_WORTH_STARTING = 20
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

PROMPT = """You are Mary Grace, in the PRICING LAB - a chat that exists for one job only:
making the pricing engine's numbers match what Fenster actually charges.

It is the middle of the night. Nothing new has arrived; you are here to improve the
engine against history. Work in small committed steps rather than one long analysis,
because the session is killed at its stop wherever it has got to - and there will be
another session tonight, so a committed step is one the next one can build on.

USE THE TIME. On 29/07 - the first run - you did good work and stopped after 43 minutes
of a two-hour window, having ended your own report with four concrete things worth
doing next. Nothing competes for these hours; finishing a line of enquiry is a reason
to start the next one, not to hand time back. When something is committed and measured,
take the next item off your own list and keep going until the clock stops you. Stop
early only if you have run out of evidence rather than out of ideas - and say which.

TWO GOALS, BOTH FROM ZAC (dashmsg-97, 29/07). They use the same documents, so do them
on the same pass rather than reading everything twice.

1. AUDIT THE QUOTES FENSTER ITSELF SENT, AND SAY WHERE THEY ARE WRONG. His words:
   "look through old projects for work that we ourselves have quoted, check they have
   no mistakes, tell us if they do." This is new - the lab used to be told to ignore
   everything except the engine. What counts as a mistake: arithmetic that does not
   foot, a discount applied twice or not at all, a line quoted at a rate the supplier
   quote does not support, a scope item in the schedule and absent from the pricing,
   a labour code that under-prices something measured in m2. Run mary_checks.py where
   a manifest fits. Record each one in the hub's catches, with the document, the line
   and the money. A quote already with a client that is WRONG is not a lab finding -
   it is an error, and errors go to Adam in the morning update or sooner.

2. REDUCE THE ENGINE'S ERROR AGAINST THOSE SAME QUOTES - "try and get close to 1 to 1".
   Not contract terms. Not exclusions. Not warranties. Those are well covered elsewhere
   and are not what this window is for. If you find one, note it and move on.

Keep the two apart when you report. An error in OUR quote and an error in the ENGINE
are opposite findings: the first means the document is wrong, the second means the
document is right and the engine is not. Confusing them would teach the engine a
mistake, so when a quote turns out to be wrong, EXCLUDE it from the calibration set
and say so - never tune the engine to reproduce a defect.

HOW:
1. `python scripts/mary_backtest.py --scan` scores the engine against every quote
   Fenster has sent. `--holdout` measures honestly on jobs it did not learn from.
2. Take the WORST job, or a size band that is consistently out, and find out why.
   Open the actual pricing document and the job pack. The answer is usually a real
   commercial reason - a system, a spec, a discount, a scope item priced elsewhere.
3. Fix the cause where it lives: a rate in data/learned-rates.json, a factor in
   mary_pricing.CALIBRATION (with the job that earned it cited), a band boundary, or
   a rule about which family a product should look up.
4. Re-run --holdout. KEEP THE CHANGE ONLY IF IT IMPROVES ON UNSEEN JOBS. A change that
   improves the jobs you studied and nothing else is overfitting; say so and revert it.
5. Record what you learned in data/calibration.json and commit each step separately.

THE OPEN QUESTION worth starting on: on St Mary's the whole-job error was +4.4% but the
size bands were -35.5% (<1.5m2), -1.2% (1.5-3m2), +37.5% (3-6m2) and +35.2% (>6m2). The
bands cancel out. Why does small run low and large run high? If that is real across
jobs rather than one job's mix, the band structure itself is wrong and fixing it is
worth more than any number of individual rates.

Report at the end: what you changed, the holdout before and after, and what you would
look at next. If nothing improved, say that plainly - a clean negative result is worth
having and stops the next session repeating it."""


def in_window(now=None):
    """The window spans midnight, so it is an OR, not a range. Getting this
    wrong reads as 'never' rather than as an error, which is how a widened
    window quietly stays shut."""
    h = (now or dt.datetime.now()).hour
    return h >= WINDOW[0] or h < WINDOW[1]


def night_start(now=None):
    now = now or dt.datetime.now()
    start = now.replace(hour=WINDOW[0], minute=0, second=0, microsecond=0)
    if now.hour < WINDOW[1]:
        start -= dt.timedelta(days=1)
    return start


def minutes_left(now=None):
    """Until 07:00. What bounds the last session of the night."""
    now = now or dt.datetime.now()
    end = now.replace(hour=WINDOW[1], minute=0, second=0, microsecond=0)
    if now.hour >= WINDOW[0]:
        end += dt.timedelta(days=1)
    return max(0, (end - now).total_seconds() / 60.0)


def hours_used(now=None):
    """Lab hours already spent this night, off this script's own log lines.
    Reusing the log rather than a new state file means the count cannot
    disagree with what actually happened."""
    start = night_start(now)
    cutoff = start.strftime("[%Y-%m-%d %H:%M")
    total = 0.0
    try:
        with open(mp.LOG, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line < cutoff:
                    continue
                m = re.search(r"PRICING LAB finished after (\d+) min", line)
                if m:
                    total += int(m.group(1)) / 60.0
    except IOError:
        pass
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", action="store_true", help="ignore the clock")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    used, left = hours_used(), minutes_left()
    if args.status:
        print("window        %02d:00-%02d:00  (in window: %s)" % (WINDOW[0], WINDOW[1], in_window()))
        print("lab hours     %.2f of %.1f used since %s" % (used, NIGHT_HOURS,
                                                            night_start().strftime("%a %H:%M")))
        print("minutes left  %.0f until %02d:00" % (left, WINDOW[1]))
        print("session lock  %s" % ("HELD - lab would yield" if mp.session_running() else "free"))
        return 0

    if not args.now and not in_window():
        print("outside the %02d:00-%02d:00 window - not running" % WINDOW)
        return 0
    if mp.session_running():
        print("a session is already running - the lab yields to real work")
        return 0
    if not args.now and used >= NIGHT_HOURS:
        mp.log("PRICING LAB held back: %.1f of %.1f lab-hours used this night" % (used, NIGHT_HOURS))
        return 0
    # The morning update needs the session lock at 07:45. A lab session started
    # at 06:50 with a 115-minute stop would still hold it at 08:45, so the last
    # session of the night is cut to fit rather than allowed to overrun.
    stop_minutes = HARD_STOP_MINUTES if args.now else int(min(HARD_STOP_MINUTES, left))
    if not args.now and stop_minutes < MIN_MINUTES_WORTH_STARTING:
        print("only %d minutes to %02d:00 - not worth starting" % (stop_minutes, WINDOW[1]))
        return 0

    reg = router.load_registry()
    rec = reg["chats"].get(CHAT_KEY)
    if not rec:
        rec = router.chat(reg, CHAT_KEY)
    # The lab starts fresh every night. Its output belongs in the engine and in
    # calibration.json, not in a conversation that grows to thousands of turns.
    rec["session_id"] = str(uuid.uuid4())
    rec["started"] = False
    router.save_registry(reg)

    if not mp.acquire_lock():
        print("could not take the session lock")
        return 0

    cmd = [mp.CLAUDE_CMD, "-p", "--dangerously-skip-permissions",
           "--session-id", rec["session_id"]]
    env = os.environ.copy()
    env["MARY_CHAT_KEY"] = CHAT_KEY
    mp.log("PRICING LAB starting (%.1f of %.1f lab-hours used, stop after %d min)"
           % (used, NIGHT_HOURS, stop_minutes))
    started = dt.datetime.now()
    try:
        proc = subprocess.Popen(cmd, cwd=REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, env=env,
                                encoding="utf-8", errors="replace",
                                creationflags=NO_WINDOW)
        with open(mp.LOCK, "w") as fh:
            fh.write(str(proc.pid))
        try:
            out, err = proc.communicate(input=PROMPT, timeout=stop_minutes * 60)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
            mp.log("PRICING LAB hit its %d-minute stop" % stop_minutes)
        mins = (dt.datetime.now() - started).total_seconds() / 60
        mp.log("PRICING LAB finished after %.0f min (exit %s)" % (mins, proc.returncode))
        with open(os.path.join(REPO, "test-results", "mary-inbox",
                               "last-session-pricing-lab.txt"), "w", encoding="utf-8") as fh:
            fh.write(((out or "") + ("\n--- stderr ---\n" + err if err else ""))[-20000:])
    except Exception as e:
        mp.log("PRICING LAB FAILED: %s" % e)
    finally:
        if os.path.exists(mp.LOCK):
            os.remove(mp.LOCK)
    return 0


if __name__ == "__main__":
    sys.exit(main())

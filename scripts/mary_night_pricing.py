# -*- coding: utf-8 -*-
"""01:00-03:00: the only two hours Mary is allowed to work without new input.

Everywhere else in the system a session runs only when new information arrives,
because that is what stopped the 27/07 runaway. This is the deliberate
exception, and it is narrow on purpose: one chat, one goal, a hard stop at
03:00.

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
"""
import argparse
import datetime as dt
import os
import subprocess
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_poller as mp
import mary_router as router

REPO = mg.REPO
CHAT_KEY = "pricing-lab"
WINDOW = (1, 3)          # 01:00 to 03:00
HARD_STOP_MINUTES = 115  # never run past the window, whatever happens

PROMPT = """You are Mary Grace, in the PRICING LAB - a chat that exists for one job only:
making the pricing engine's numbers match what Fenster actually charges.

This is the 01:00-03:00 window. Nothing new has arrived; you are here to improve the
engine against history. Work in small committed steps rather than one long analysis,
because the session is killed at 03:00 wherever it has got to.

USE THE WHOLE WINDOW. On 29/07 - the first run - you did good work and stopped after
43 minutes, having ended your own report with four concrete things worth doing next.
Those two hours are yours and nothing else competes for them; finishing a line of
enquiry is a reason to start the next one, not to hand time back. When something is
committed and measured, take the next item off your own list and keep going until
the clock stops you. Stop early only if you have run out of evidence rather than
out of ideas - and if you do, say which it was.

THE ONLY GOAL: reduce the engine's error against real Fenster quotes.
Not contract terms. Not exclusions. Not warranties. Those are well covered elsewhere
and are not what this window is for. If you find one, note it and move on.

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


def in_window():
    h = dt.datetime.now().hour
    return WINDOW[0] <= h < WINDOW[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", action="store_true", help="ignore the clock")
    args = ap.parse_args()

    if not args.now and not in_window():
        print("outside the 01:00-03:00 window - not running")
        return 0
    if mp.session_running():
        print("a session is already running - the lab yields to real work")
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
    mp.log("PRICING LAB starting (until %02d:00)" % WINDOW[1])
    started = dt.datetime.now()
    try:
        proc = subprocess.Popen(cmd, cwd=REPO, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, env=env,
                                encoding="utf-8", errors="replace")
        with open(mp.LOCK, "w") as fh:
            fh.write(str(proc.pid))
        try:
            out, err = proc.communicate(input=PROMPT, timeout=HARD_STOP_MINUTES * 60)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
            mp.log("PRICING LAB hit the 03:00 stop")
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

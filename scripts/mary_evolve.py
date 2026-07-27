# -*- coding: utf-8 -*-
"""The improvement loop, running on its own.

Everything Mary needs to get better already exists - the back-test, the learned
rates, the calibration pairing, the scoreboard. What was missing is that all of
it was hand-run, so she only improved when somebody remembered. This is the
heartbeat: one cycle, on a schedule, that re-mines what suppliers charge,
relearns what Fenster charges, re-measures whether she got closer, and publishes
the result.

It is deliberately honest about the last part. The cycle measures itself with a
holdout - learning on some jobs and scoring on others it has never seen - so
"she improved" is a claim backed by unseen work rather than by fitting the
answer sheet. If a cycle makes her worse, it says so.

  python scripts/mary_evolve.py           # nightly: relearn, remeasure, publish
  python scripts/mary_evolve.py --full    # weekly: also re-mine supplier quotes
  python scripts/mary_evolve.py --dry-run # no deploy, no writes to the hub
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_poller as mp

REPO = mg.REPO
PY = sys.executable
LOG = os.path.join(REPO, "data", "evolution-log.json")
ARCHIVE = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)", "Commercial")


def say(msg):
    stamp = dt.datetime.now().strftime("%H:%M:%S")
    print("[%s] %s" % (stamp, msg), flush=True)


def run(cmd, label, timeout=3600):
    """Run a step. A failure is reported and the cycle carries on - one broken
    step should not cost the whole night."""
    say("%s ..." % label)
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            say("  %s FAILED (exit %s): %s" % (label, r.returncode,
                                               (r.stderr or r.stdout or "")[-300:].strip()))
            return None
        return r.stdout or ""
    except subprocess.TimeoutExpired:
        say("  %s TIMED OUT" % label)
    except Exception as e:
        say("  %s ERROR: %s" % (label, e))
    return None


def parse_holdout(out):
    """Pull the before/after numbers out of the holdout report."""
    res = {}
    for line in (out or "").splitlines():
        low = line.lower()
        if "mean abs" not in low:
            continue
        key = "before" if "before" in low else ("after" if "after" in low else None)
        if not key:
            continue
        try:
            res[key] = float(low.split("mean abs")[1].split("%")[0].strip())
        except Exception:
            pass
    return res


def wait_for_idle(max_wait=1800):
    """Do not deploy or rewrite shared state underneath a running session."""
    waited = 0
    while mp.session_running() and waited < max_wait:
        time.sleep(20)
        waited += 20
    return not mp.session_running()


def append_log(entry):
    hist = []
    if os.path.exists(LOG):
        try:
            with open(LOG, encoding="utf-8") as fh:
                hist = json.load(fh).get("cycles", [])
        except Exception:
            hist = []
    hist.append(entry)
    with open(LOG, "w", encoding="utf-8") as fh:
        json.dump({"note": "Every improvement cycle, and whether it actually helped. Measured on a "
                           "holdout of jobs the rates were not learned from.",
                   "cycles": hist[-200:]}, fh, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="also re-mine supplier quotes (slow)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    started = dt.datetime.now()
    say("evolution cycle starting%s" % (" (full re-mine)" if args.full else ""))
    entry = {"started": started.isoformat(timespec="seconds"), "full": bool(args.full)}

    # 1. What suppliers charge. Heavy, so weekly rather than nightly.
    if args.full:
        out = os.path.join(REPO, "test-results", "rate-miner-auto")
        if run([PY, "scripts/mine-supplier-rates.py", "--clients", "*", "--roots",
                os.path.join(ARCHIVE, "1. Tender Documents"),
                os.path.join(ARCHIVE, "2. Projects"), "--out", out],
               "re-mining supplier quotes", timeout=7200) is not None:
            mined = os.path.join(out, "mined-quotes.json")
            if os.path.exists(mined):
                run([PY, "scripts/build-rate-register.py", mined], "rebuilding the rate register")
                entry["register_rebuilt"] = True

    # 2. What Fenster charges, and how each supplier sits against it.
    learn = run([PY, "scripts/mary_backtest.py", "--learn"], "relearning rates from sent quotes")
    if learn:
        entry["learned"] = learn.count("\n")

    # 3. Pair her figures against quotes that have since gone out.
    run([PY, "scripts/mary_calibrate.py", "--run"], "pairing estimates against sent quotes")

    # 4. Did any of that actually help? Measured on unseen jobs.
    hold = run([PY, "scripts/mary_backtest.py", "--holdout"], "measuring on a holdout")
    scores = parse_holdout(hold)
    if scores:
        entry.update(scores)
        if "before" in scores and "after" in scores:
            entry["improvement_pct_points"] = round(scores["before"] - scores["after"], 2)
            say("  register only %.1f%%  ->  with learned rates %.1f%%  (%+.1f points)"
                % (scores["before"], scores["after"], scores["after"] - scores["before"]))

    # 5. Publish, once nobody is mid-session.
    if not args.dry_run:
        if wait_for_idle():
            run([PY, "scripts/mary_dashboard.py", "--deploy"], "publishing the hub", timeout=900)
        else:
            say("  a session is still running - skipping the deploy this cycle")

    entry["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    entry["minutes"] = round((dt.datetime.now() - started).total_seconds() / 60, 1)
    append_log(entry)

    # 6. Tell the chats what changed. They read this at the start of every turn.
    if not args.dry_run and entry.get("improvement_pct_points") is not None:
        try:
            import mary_note as note
            note.post_board(
                "Evolution cycle: learned rates now put Mary at %.1f%% mean absolute error on jobs "
                "she has never seen, against %.1f%% on the register alone (%+.1f points). Prefer the "
                "learned rate for a code and band when one exists - it is what Fenster actually "
                "charged." % (entry["after"], entry["before"], -entry["improvement_pct_points"]),
                author="evolve")
        except Exception as e:
            say("  noticeboard post failed: %s" % e)

    say("cycle done in %.1f min" % entry["minutes"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

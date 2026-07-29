# -*- coding: utf-8 -*-
"""JACOB - the daily run. This is what makes him a bot rather than a script.

  python scripts/jacob_daily.py            # intake + rebuild the board
  python scripts/jacob_daily.py --deploy   # + push it live

Every morning: read the mailboxes, re-pull yesterday's award notices, rebuild
the board. Entirely deterministic - no Claude session is spent, so it costs
nothing and cannot compete with Mary for quota. Mary's estimating work has
deadlines attached; Jacob's does not, and he must never starve her.

Set it up as a scheduled task (once, from an admin PowerShell):

  $a = New-ScheduledTaskAction -Execute pythonw `
       -Argument "scripts\\jacob_daily.py --deploy" `
       -WorkingDirectory "C:\\Users\\zacpl\\Desktop\\Glazing-Quote-Assistant"
  $t = New-ScheduledTaskTrigger -Daily -At 7:30am
  Register-ScheduledTask -TaskName JacobDaily -Action $a -Trigger $t

A step that fails is logged and the run continues - a Contracts Finder
rate-limit should never stop the mailbox intake from updating the board.
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(REPO, "data", "jacob", "daily.log")


def log(msg):
    line = "[%s] %s" % (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def run(label, args, required=False):
    log("START %s" % label)
    try:
        p = subprocess.run([sys.executable] + args, cwd=REPO, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=1800)
    except subprocess.TimeoutExpired:
        log("TIMEOUT %s" % label)
        return False
    tail = (p.stdout or "").strip().splitlines()[-3:]
    for t in tail:
        log("   %s" % t)
    if p.returncode != 0:
        log("FAILED %s (exit %s) %s" % (label, p.returncode,
                                        (p.stderr or "").strip()[:200]))
        if required:
            log("that step was required - stopping")
        return False
    log("OK %s" % label)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--days", type=int, default=30,
                    help="mailbox window; the first run should be much larger")
    ap.add_argument("--skip-awards", action="store_true")
    args = ap.parse_args()

    log("=" * 58)
    log("Jacob daily run")

    # 1. Mailboxes. The highest-value source and the cheapest - portal
    #    invitations and client enquiries arrive here as ordinary email.
    ok_intake = run("mailbox intake",
                    ["scripts/jacob_intake.py", "--days", str(args.days)])

    # 2. Public awards. Nice to have; it rate-limits hard and its absence must
    #    not stop the board updating.
    if not args.skip_awards:
        run("contracts finder", ["scripts/jacob_contracts_finder.py"])

    # 3. ProContract adverts. This is where a council or housing association
    #    puts work under the GBP 100k Find a Tender threshold - Fenster's size
    #    of work, and invisible to steps 1 and 2. Public, no login. Like the
    #    awards it must never be able to stop the board updating.
    run("procontract", ["scripts/jacob_procontract.py"])

    # 4. The won-contracts export. A local CSV, so it cannot fail on the
    #    network - but it is a hand export from Adam and will be stale until he
    #    sends another, so it is re-parsed rather than re-fetched.
    run("won contracts", ["scripts/jacob_contracts.py"])

    # 5. Rebuild the board from whatever succeeded.
    board = ["scripts/jacob_dashboard.py"] + (["--deploy"] if args.deploy else [])
    ok_board = run("rebuild board", board, required=True)

    log("done - intake %s, board %s"
        % ("ok" if ok_intake else "FAILED", "ok" if ok_board else "FAILED"))
    return 0 if ok_board else 1


if __name__ == "__main__":
    sys.exit(main())

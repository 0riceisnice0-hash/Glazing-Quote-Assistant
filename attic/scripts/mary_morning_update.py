# -*- coding: utf-8 -*-
"""Run Mary's scheduled morning update without creating a console window.

Task Scheduler used to execute claude.exe directly. Because Claude Code is a
console application, that could open a visible terminal even though the bridge
tasks themselves use pythonw.exe. The scheduled task now runs this wrapper
under pythonw; the wrapper supplies CREATE_NO_WINDOW to the Claude child.

Use ``--status`` to validate paths without starting Claude.
"""
import argparse
import datetime as dt
import os
import subprocess
import sys


REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")
LOG = os.path.join(REPO, "test-results", "mary-inbox", "morning-update.log")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
PROMPT = """You are Mary Grace, Fenster Glazing's estimating AI. Produce and SEND
the daily morning update email now: read MARY-HANDOVER.md and
MARY-EMAIL-SESSION.md first, cross-check the Estimating Log (OneDrive
Commercial\\13. Estimating\\Leads\\Estimating Log.xlsx) against recent
estimating@ mail, use Adam's airy numbered format, send via scripts/mary_send.py
to adam,marketing, then update handover docs and push."""


def log(message):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write("[%s] %s\n" %
                     (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      message))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true",
                        help="validate configuration without launching Claude")
    args = parser.parse_args()

    if args.status:
        print("repo: %s" % REPO)
        print("claude: %s (%s)" % (CLAUDE,
                                   "found" if os.path.exists(CLAUDE)
                                   else "missing"))
        print("no-window flag: %s" % NO_WINDOW)
        return 0

    if not os.path.exists(CLAUDE):
        log("Claude CLI missing at %s" % CLAUDE)
        return 1

    log("morning update starting")
    try:
        result = subprocess.run(
            [CLAUDE, "-p", "--dangerously-skip-permissions"],
            cwd=REPO, input=PROMPT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60 * 60,
            creationflags=NO_WINDOW)
        log("morning update exit %s" % result.returncode)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "")[-1000:].strip()
            if detail:
                log(detail)
        return result.returncode
    except subprocess.TimeoutExpired:
        log("morning update timed out after 60 minutes")
        return 2
    except Exception as error:
        log("morning update failed: %s" % error)
        return 3


if __name__ == "__main__":
    sys.exit(main())

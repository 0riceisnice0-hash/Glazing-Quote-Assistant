# -*- coding: utf-8 -*-
"""The job-file contract - Phase 1 of AGENT-AUDIT.md.

`data/jobs/<key>.md` is a chat's durable memory: the file a fresh session is
seeded from when the conversation rotates. Rotation already works (8 chats
retired by 29/07) but nothing bounded the files, so the bloat moved instead of
stopping: gordon-court's chat shrank to 0.3 MB while its job file grew to
265 KB, and every future seed re-reads all of it.

The contract:
  - at most MAX_LINES lines (the seed budget; history goes to the archive)
  - a `## Position` heading near the top - the one section a fresh chat needs
  - history that will not fit lives in `data/jobs/<key>-archive-YYYY-MM.md`,
    which recall and humans can still read but no seed ever loads

The bridge checks the contract after every clean session and puts the failure
in the chat's NEXT kick prompt - the chat fixes its own file, because only it
knows which lines are position and which are history.

  python scripts/mary_jobfile.py --check georgies      # problems, if any
  python scripts/mary_jobfile.py --check-all
  python scripts/mary_jobfile.py --archive georgies    # move the whole file to
        the month's archive and leave a template to rebuild from - the REBUILD
        step is the session's job, never this script's
"""
import argparse
import datetime as dt
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS_DIR = os.path.join(REPO, "data", "jobs")

MAX_LINES = 300

TEMPLATE = """# {title}

## Position
REBUILD ME: this file was archived to {archive} on {date} because it broke the
contract (over {max_lines} lines). Rebuild the live file from that archive plus
`python scripts/mary_recall.py --job {key} --days 14`, to the contract:
Position / The number and its basis / Deadlines / Open RFIs and questions /
Decisions (with dates) / What Adam said. Keep it under {max_lines} lines -
detail belongs in the archive, evidence in the ledger.

## The number and its basis

## Deadlines

## Open RFIs and questions

## Decisions

## What Adam said
"""


def path_for(key):
    return os.path.join(JOBS_DIR, "%s.md" % key)


def is_archive(name):
    return re.search(r"-archive-\d{4}-\d{2}\.md$", name) is not None


def check(key):
    """The contract, as a list of problems. Empty list = compliant."""
    p = path_for(key)
    if not os.path.exists(p):
        return ["data/jobs/%s.md does not exist - create it to the contract" % key]
    problems = []
    with open(p, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    if len(lines) > MAX_LINES:
        problems.append("data/jobs/%s.md is %d lines (contract: %d) - archive the history"
                        % (key, len(lines), MAX_LINES))
    head = "\n".join(lines[:40]).lower()
    if "## position" not in head:
        problems.append("data/jobs/%s.md has no '## Position' heading near the top - "
                        "a fresh chat cannot find where the job stands" % key)
    return problems


def archive(key):
    """Move the whole live file into this month's archive (append if one
    exists) and leave a rebuild template. Mechanical on purpose: deciding what
    stays live is estimating judgement, so it belongs to the session."""
    p = path_for(key)
    if not os.path.exists(p):
        raise SystemExit("no such job file: %s" % p)
    month = dt.date.today().strftime("%Y-%m")
    arc_name = "%s-archive-%s.md" % (key, month)
    arc = os.path.join(JOBS_DIR, arc_name)
    with open(p, encoding="utf-8", errors="replace") as fh:
        body = fh.read()
    stamp = "\n\n---\n\n# Archived %s\n\n" % dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(arc, "a", encoding="utf-8") as fh:
        fh.write(stamp + body)
    title = next((l[2:].strip() for l in body.splitlines() if l.startswith("# ")), key)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(TEMPLATE.format(title=title, key=key, archive="data/jobs/" + arc_name,
                                 date=dt.date.today().isoformat(), max_lines=MAX_LINES))
    print("archived %d lines to data/jobs/%s; live file is now the rebuild template"
          % (len(body.splitlines()), arc_name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check")
    ap.add_argument("--check-all", action="store_true")
    ap.add_argument("--archive")
    a = ap.parse_args()
    if a.check:
        problems = check(a.check)
        for x in problems:
            print("PROBLEM:", x)
        if not problems:
            print("ok - data/jobs/%s.md meets the contract" % a.check)
        return 1 if problems else 0
    if a.check_all:
        bad = 0
        for name in sorted(os.listdir(JOBS_DIR)):
            if not name.endswith(".md") or name == "README.md" or is_archive(name):
                continue
            key = name[:-3]
            problems = check(key)
            status = "ok " if not problems else "FAIL"
            print("%s %-24s %s" % (status, key, "; ".join(problems)))
            bad += bool(problems)
        print("\n%d file(s) out of contract" % bad)
        return 1 if bad else 0
    if a.archive:
        archive(a.archive)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

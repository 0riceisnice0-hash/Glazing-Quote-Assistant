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

# THE CONTRACT TESTS THE INTENT, NOT ONE LITERAL STRING (03/08/2026).
#
# It used to require the exact heading `## Position`, and six chats "failed"
# while doing exactly the right thing - they had independently written
# `## Where it stands`, `## Where this stands`, `## Current position`,
# `## 1. Where this job actually stands`. That is the same section in better
# English, and a checker that fails it teaches the wrong lesson: rename your
# heading rather than know where the job stands.
#
# What a fresh seed actually needs is a statement of position near the top.
# Anything in this family satisfies that. A file that states its position by
# leading with the issued number ("## ISSUED 29/07 - GBP 20,563.57") satisfies
# it too, which is why the issued/quoted forms are here.
# The `> ` prefix is there because a heading inside a callout is still a
# heading - st-marys leads with its whole position in a blockquote.
POSITION_HEADINGS = re.compile(
    r"^>?\s*#{1,3}\s*(?:\d+[.)]\s*)?(?:"
    r"position"
    r"|current position"
    r"|where (?:it|this|we|the job|this job)\b.*stand"
    r"|status"
    r"|issued\b"
    r"|quote issued\b"
    r"|closed\b"
    r")", re.I | re.M)

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
    head = "\n".join(lines[:40])
    if not POSITION_HEADINGS.search(head):
        problems.append("data/jobs/%s.md does not state its position in the first 40 lines - "
                        "a fresh chat cannot find where the job stands. Add a heading such as "
                        "'## Position' or '## Where it stands'" % key)
    return problems


# The distillates that are loaded on EVERY session, with the cap each one sets
# for itself. These are not archives - the archive each overflows into is
# deliberately unlimited (bd-lessons.md), because "the cap is on the LOADING,
# never on the knowing" (Zac, 29/07). Nothing here is ever deleted to fit;
# it moves.
KNOWLEDGE = {
    "data/knowledge/adam.md": 120,
    "data/knowledge/bd.md": 130,
}


# Jacob's unit of memory is the company, not the job, and a relationship needs
# less room than a live tender - 150 lines against Mary's 300. Same contract
# otherwise: state the position near the top, and let history go to the archive.
COMPANY_DIR = os.path.join(REPO, "data", "companies")
COMPANY_MAX_LINES = 150


def company_path(key):
    return os.path.join(COMPANY_DIR, "%s.md" % key)


def check_company(key):
    """The company-file contract, same shape as check(). Empty list = compliant."""
    p = company_path(key)
    if not os.path.exists(p):
        return ["data/companies/%s.md does not exist - create it to the contract "
                "before working this company" % key]
    problems = []
    with open(p, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    if len(lines) > COMPANY_MAX_LINES:
        problems.append("data/companies/%s.md is %d lines (contract: %d) - archive "
                        "the history" % (key, len(lines), COMPANY_MAX_LINES))
    if not POSITION_HEADINGS.search("\n".join(lines[:40])):
        problems.append("data/companies/%s.md does not state where the relationship "
                        "stands in the first 40 lines. Add a heading such as "
                        "'## Position' or '## Where it stands'" % key)
    return problems


def check_knowledge():
    """Always-loaded knowledge files over their own cap. Same shape as check()."""
    problems = []
    for rel, cap in sorted(KNOWLEDGE.items()):
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            problems.append("%s is missing" % rel)
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            n = len(fh.read().splitlines())
        if n > cap:
            problems.append(
                "%s is %d lines against its own %d-line cap - it is loaded by every "
                "session, so this is a tax on all of them. Move the long accounts to "
                "its overflow file and leave one-line rules with pointers."
                % (rel, n, cap))
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
    ap.add_argument("--check-knowledge", action="store_true")
    ap.add_argument("--archive")
    a = ap.parse_args()
    if a.check_knowledge:
        problems = check_knowledge()
        for x in problems:
            print("PROBLEM:", x)
        if not problems:
            print("ok - every always-loaded knowledge file is within its cap")
        return 1 if problems else 0
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
        for x in check_knowledge():
            print("FAIL %-24s %s" % ("(knowledge)", x))
            bad += 1
        print("\n%d file(s) out of contract" % bad)
        return 1 if bad else 0
    if a.archive:
        archive(a.archive)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

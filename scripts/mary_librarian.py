# -*- coding: utf-8 -*-
"""The librarian - the daily metabolism of Mary's memory (Phase 3, AGENT-AUDIT.md).

Memory only stays small if something tends it. This runs once a day, off-peak,
deterministically (no Claude session, no tokens), and reports on the health of
every memory layer:

  - refreshes the ledger (networked backfill - picks up hub messages)
  - the job-file contract: who is over, who is missing
  - the knowledge shelf: INDEX.md pointers that no longer land on a heading,
    caps on INDEX.md and adam.md
  - the send discipline: sends vs Adam's distinct replies, trailing 7 days
  - transcript sizes: which chats rotation will retire next

Output: test-results/librarian/YYYY-MM-DD.md, and one line on the noticeboard
so every chat sees the state of its own memory habits. Anything needing
JUDGEMENT (compacting a job file, updating adam.md) is flagged for the chat
that owns it - the librarian never edits knowledge itself; it keeps score.

Register (daily 21:15, before the night window):
  schtasks /Create /TN MaryLibrarian /SC DAILY /ST 21:15 /TR
    "\"C:\\...\\pythonw.exe\" \"C:\\...\\scripts\\mary_librarian.py\"" /F
"""
import datetime as dt
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_ledger as ledger
import mary_jobfile as jobfile
import mary_note as note
import mary_budget as budget

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "test-results", "librarian")
KNOWLEDGE = os.path.join(REPO, "data", "knowledge")
AI_MD = os.path.join(REPO, "AI.md")
INDEX_CAP = 120
ADAM_CAP = 120


def check_index_pointers():
    """Every `AI.md` L<n> pointer in INDEX.md must land on (or within 5 lines
    of) a heading - AI.md is append-mostly, but nothing guarantees that."""
    idx = os.path.join(KNOWLEDGE, "INDEX.md")
    if not os.path.exists(idx):
        return ["data/knowledge/INDEX.md is missing"]
    with io.open(AI_MD, encoding="utf-8") as fh:
        ai = fh.read().splitlines()
    heads = {i + 1 for i, l in enumerate(ai) if l.startswith("#")}
    problems = []
    with io.open(idx, encoding="utf-8") as fh:
        text = fh.read()
    for m in re.finditer(r"`AI\.md`\s+L(\d+)", text):
        n = int(m.group(1))
        if not any(abs(n - h) <= 5 for h in heads):
            problems.append("INDEX.md points at AI.md L%d but no heading is within 5 lines" % n)
    for path, cap in ((idx, INDEX_CAP), (os.path.join(KNOWLEDGE, "adam.md"), ADAM_CAP),
                      (os.path.join(KNOWLEDGE, "bd.md"), 130)):
        if os.path.exists(path):
            n = sum(1 for _ in io.open(path, encoding="utf-8"))
            if n > cap:
                problems.append("%s is %d lines (cap %d) - move full accounts to the "
                                "archive file, never delete the knowledge" %
                                (os.path.relpath(path, REPO), n, cap))
    return problems


def send_discipline(events):
    now = dt.datetime.now()
    week = (now - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    day = now.strftime("%Y-%m-%d")
    sends7 = [e for e in events if e.get("kind") == "email_sent" and str(e.get("ts", "")) >= week]
    sends_today = [e for e in sends7 if str(e.get("ts", "")).startswith(day)]
    adam7 = {e.get("summary", "")[:60] for e in events
             if e.get("actor") == "adam" and str(e.get("ts", "")) >= week}
    return len(sends_today), len(sends7), len(adam7)


def transcripts():
    proj = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                        "C--Users-zacpl-Desktop-Glazing-Quote-Assistant")
    jobs = json.load(io.open(os.path.join(REPO, "data", "mary-jobs.json"), encoding="utf-8"))
    rows = []
    for key, c in jobs.get("chats", {}).items():
        p = os.path.join(proj, "%s.jsonl" % c.get("session_id", ""))
        if os.path.exists(p):
            rows.append((key, os.path.getsize(p) / 1048576.0))
    rows.sort(key=lambda r: -r[1])
    return rows


def main():
    added = ledger.backfill(verbose=False, network=True)
    events = list(ledger.iter_events())

    contract = []
    for name in sorted(os.listdir(jobfile.JOBS_DIR)):
        if not name.endswith(".md") or name == "README.md" or jobfile.is_archive(name):
            continue
        key = name[:-3]
        for p in jobfile.check(key):
            contract.append(p)

    shelf = check_index_pointers()
    today_n, week_n, adam_n = send_discipline(events)
    fat = [(k, mb) for k, mb in transcripts() if mb >= 4.0]

    day = dt.date.today().isoformat()
    lines = ["# Librarian - %s" % day, ""]
    lines.append("ledger: +%d events today (total %d)" % (sum(added.values(), 0), len(events)))
    lines.append("sends: %d today, %d this week, vs %d distinct Adam replies/instructions"
                 % (today_n, week_n, adam_n))
    tok, per = budget.tokens_spent(dt.datetime.now().replace(hour=0, minute=0, second=0))
    if tok:
        top = sorted(per.items(), key=lambda kv: -kv[1])[:3]
        lines.append("tokens today: ~%s estimated (%s)" % (
            "{:,}".format(tok), ", ".join("%s ~%s" % (k, "{:,}".format(v)) for k, v in top)))
    day = dt.date.today().isoformat()
    checks = sum(1 for e in events if e.get("kind") == "gate_check"
                 and str(e.get("ts", "")).startswith(day))
    lines.append("send gate: %d check(s) run against %d sends today - the gap is the "
                 "measure of the habit" % (checks, today_n))
    lines.append("")
    lines.append("## Job-file contract (%d problem%s)" % (len(contract), "" if len(contract) == 1 else "s"))
    lines += ["- " + p for p in contract] or ["- all compliant"]
    lines.append("")
    lines.append("## Knowledge shelf")
    lines += ["- " + p for p in shelf] or ["- index pointers and caps all good"]
    lines.append("")
    lines.append("## Chats rotation will retire next (over 4 MB)")
    lines += ["- %s (%.1f MB)" % (k, mb) for k, mb in fat] or ["- none close to the threshold"]
    report = "\n".join(lines) + "\n"

    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "%s.md" % day)
    with io.open(dest, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)

    summary = ("Librarian %s: %d contract problem(s), %d shelf problem(s), "
               "%d sends this week vs %d Adam replies. Full report: test-results/librarian/%s.md"
               % (day, len(contract), len(shelf), week_n, adam_n, day))
    try:
        note.post_board(summary, author="librarian")
    except Exception as e:  # noqa: BLE001 - the report file already exists
        print("noticeboard post failed: %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())

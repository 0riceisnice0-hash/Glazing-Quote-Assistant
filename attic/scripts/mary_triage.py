# -*- coding: utf-8 -*-
"""The cheap front door. Decides what deserves an expensive session.

Zac, 04/08: "everytime there is an email, it thinks about it. which then wakes
up a new task... what if the part of mary that sees the new emails stays in the
same chat window. she wakes up, determines if its important, then sends it off
or ignores it. we can run this on sonnet or haiku to be really cost effective,
as this needs little to no brainpower."

He is right, and the numbers say so. A full Opus sitting costs a median 7.2M
context tokens. Deciding whether a supplier's order acknowledgement is worth
one of those is not a 7.2M question - it is a one-line judgement that a small
model makes correctly, and the router's regex makes badly.

WHAT THIS IS NOT: a chat. He said "the same chat window", and the intent behind
that is right - continuity, so it learns what noise looks like HERE. But a
conversation is the wrong container for it, because a chat accumulates context
and this has to stay cheap forever. So the continuity lives in a FILE
(data/knowledge/noise.md) that grows, and each classification is a fresh,
stateless call carrying only that file and the items. Cheap per call, and it
still learns.

ONE CALL FOR THE WHOLE BATCH. Classifying ten items in one request costs barely
more than classifying one, and the model sees them together - which is how it
notices that four of them are the same thread.

  python scripts/mary_triage.py --dry-run
  python scripts/mary_triage.py
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(REPO, "test-results", "mary-inbox", "queue")
PROCESSED = os.path.join(REPO, "test-results", "mary-inbox", "processed")
NOISE = os.path.join(REPO, "data", "knowledge", "noise.md")
LOG = os.path.join(REPO, "test-results", "mary-inbox", "triage.log")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")

# Haiku by default. This is a sorting job, not an estimating one - and the
# entire point is that it costs almost nothing, so the model has to match.
MODEL = os.environ.get("MARY_TRIAGE_MODEL", "claude-haiku-4-5-20251001")
BATCH = int(os.environ.get("MARY_TRIAGE_BATCH", "12"))
# How much of a body the decision needs. A portal notice announces itself in
# the first two lines; so does a client asking for a price.
BODY_CHARS = 700
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def log(msg):
    line = "[triage] %s" % msg
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def read_noise():
    try:
        with open(NOISE, encoding="utf-8") as fh:
            return fh.read()
    except IOError:
        return ""


def orders():
    """Queued work orders that nothing has decided about yet."""
    out = []
    if not os.path.isdir(QUEUE):
        return out
    for name in sorted(os.listdir(QUEUE)):
        if not name.endswith(".json"):
            continue
        p = os.path.join(QUEUE, name)
        try:
            with open(p, encoding="utf-8") as fh:
                rec = json.load(fh)
        except (IOError, ValueError):
            continue
        # Already routed by a person or a previous pass - leave it alone.
        if rec.get("route") or rec.get("triage"):
            continue
        out.append((name, p, rec))
    return out


PROMPT = """You are the front desk of a glazing contractor's estimating inbox.
For each item below, decide ONE thing: does it need a human-grade estimating
session, or not?

Answer with a JSON array, one object per item, nothing else:
  {{"n": <the item number>, "verdict": "work"|"noise"|"fyi", "why": "<8 words>"}}

  work  - somebody needs something from us: a price, an answer, a decision, a
          deadline, a document. Anything from a client, a main contractor or a
          supplier about a live job.
  fyi   - real but needs no reply: an acknowledgement, a delivery note, a read
          receipt, our own sent mail coming back, a thread we are only copied on.
  noise - a portal digest, a newsletter, a marketing mail, an automated alert,
          a supplier advertising, anything nobody would ever action.

WHEN IN DOUBT SAY "work". A wasted session costs money; a missed tender costs a
job. Only say "noise" when you are certain nobody would ever act on it.

What has already been learned about what is noise here:
{noise}

ITEMS:
{items}"""


def build_items(batch):
    out = []
    for i, (_name, _p, r) in enumerate(batch, 1):
        out.append(
            "--- %d\nfrom: %s\nto: %s\nsubject: %s\nbody: %s"
            % (i, str(r.get("from") or r.get("sender") or "?")[:120],
               str(r.get("mailbox") or "")[:60],
               str(r.get("subject") or "")[:200],
               re.sub(r"\s+", " ", str(r.get("body") or ""))[:BODY_CHARS]))
    return "\n".join(out)


def classify(batch, dry_run=False):
    """One call, the whole batch. Returns {n: {verdict, why}}."""
    prompt = PROMPT.format(noise=read_noise() or "(nothing recorded yet)",
                           items=build_items(batch))
    if dry_run:
        log("would classify %d item(s) on %s (%d chars of prompt)"
            % (len(batch), MODEL, len(prompt)))
        return {}
    try:
        p = subprocess.run(
            [CLAUDE, "-p", "--model", MODEL, "--dangerously-skip-permissions"],
            input=prompt, cwd=REPO, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=180,
            creationflags=NO_WINDOW)
    except Exception as e:
        log("classifier failed (%s) - leaving everything for the session" % str(e)[:90])
        return {}
    m = re.search(r"\[.*\]", p.stdout or "", re.S)
    if not m:
        log("no JSON back from the classifier - leaving everything for the session")
        return {}
    try:
        rows = json.loads(m.group(0))
    except ValueError:
        log("unparseable JSON from the classifier - leaving everything alone")
        return {}
    return {int(r["n"]): r for r in rows if isinstance(r, dict) and "n" in r}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    pending = orders()
    if not pending:
        log("nothing to triage")
        return 0

    counts = {"work": 0, "fyi": 0, "noise": 0, "undecided": 0}
    for i in range(0, len(pending), BATCH):
        batch = pending[i:i + BATCH]
        verdicts = classify(batch, a.dry_run)
        for n, (name, path, rec) in enumerate(batch, 1):
            v = verdicts.get(n)
            if not v:
                counts["undecided"] += 1
                continue
            verdict = str(v.get("verdict") or "work").lower()
            why = str(v.get("why") or "")[:120]
            counts[verdict if verdict in counts else "work"] += 1
            log("%-6s %-52s %s" % (verdict, (rec.get("subject") or name)[:52], why))
            if a.dry_run:
                continue
            if verdict == "noise":
                # Filed, never deleted, and the reason travels with it - a
                # wrong call has to be findable.
                rec["triage"] = {"verdict": verdict, "why": why, "model": MODEL}
                os.makedirs(PROCESSED, exist_ok=True)
                with open(os.path.join(PROCESSED, name), "w", encoding="utf-8") as fh:
                    json.dump(rec, fh, indent=1, ensure_ascii=False)
                att = path[:-5] + "-att"
                if os.path.isdir(att):
                    os.replace(att, os.path.join(PROCESSED, name[:-5] + "-att"))
                os.remove(path)
            else:
                # `fyi` still reaches a session, but marked - so the batch
                # prompt can say "these four need reading, not answering".
                rec["triage"] = {"verdict": verdict, "why": why, "model": MODEL}
                with open(path, "w", encoding="utf-8") as fh:
                    json.dump(rec, fh, indent=1, ensure_ascii=False)

    log("%d item(s): %s" % (len(pending),
                            ", ".join("%d %s" % (v, k) for k, v in counts.items() if v)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Work-order router: decides WHICH of Mary's chats a piece of work belongs to.

Mary used to run one throwaway session per poll, which meant re-reading the
handover docs every time just to remember a job she had priced that morning.
Instead each job now owns a PERMANENT Claude Code conversation (a stable
session UUID resumed with `claude -p --resume`), so the chat itself is the
memory. Anything that does not belong to a known job goes to the `triage`
chat, which handles it or opens a new job.

Registry: data/mary-jobs.json
  jobs.<key> = {name, client, match[], session_id, started, last_active, ...}

Routing evidence, strongest first:
  1. dashboard message context "REQ-n: ..."  -> the request's job
  2. dashboard message context "<job name>"  -> that job
  3. email subject / sender / body vs each job's match terms (weighted)
  4. no confident winner                     -> triage

CLI (sessions use this to keep the registry honest):
  python scripts/mary_router.py --list
  python scripts/mary_router.py --add-job <key> --name "..." --client "..." --match "a,b,c"
  python scripts/mary_router.py --test "subject line to route"
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO, "data", "mary-jobs.json")
STATE = os.path.join(REPO, "data", "dashboard-state.json")
JOB_DIR = os.path.join(REPO, "data", "jobs")

TRIAGE = "triage"
# A single strong hit (subject or sender) is enough; body-only chatter is not.
MIN_SCORE = 3


def load_registry():
    with open(REGISTRY, encoding="utf-8") as fh:
        reg = json.load(fh)
    reg.setdefault("jobs", {})
    reg.setdefault("chats", {})
    return reg


def save_registry(reg):
    tmp = REGISTRY + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, REGISTRY)


def chat(reg, key):
    """The chat record for a job key (or 'triage'), created on demand.

    session_id is minted here but the conversation does not exist until the
    bridge launches it with --session-id; `started` records that crossing.
    """
    rec = reg["chats"].get(key)
    if not rec:
        rec = {"session_id": str(uuid.uuid4()), "started": False,
               "created": dt.datetime.now().isoformat(timespec="seconds"),
               "last_active": None, "runs": 0}
        reg["chats"][key] = rec
    return rec


def job_title(reg, key):
    if key == TRIAGE:
        return "Triage (front desk)"
    return reg["jobs"].get(key, {}).get("name", key)


def _requests_by_id():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return {r.get("id"): r for r in json.load(fh).get("requests", [])}
    except Exception:
        return {}


def _match_job_name(reg, text):
    """Find a job whose name or match terms appear in a short piece of text."""
    t = (text or "").lower()
    if not t.strip():
        return None
    best, best_len = None, 0
    for key, job in reg["jobs"].items():
        for term in [job.get("name", "")] + job.get("match", []):
            term = (term or "").lower().strip()
            if len(term) >= 4 and term in t and len(term) > best_len:
                best, best_len = key, len(term)
    return best


def route(order, reg=None):
    """Return (job_key, why). job_key is a registry key or TRIAGE."""
    reg = reg or load_registry()

    if order.get("mailbox") == "dashboard":
        # Older work orders carry the context only inside the subject line.
        ctx = order.get("context") or ""
        if not ctx:
            ctx = re.sub(r"^\s*Dashboard message(\s+re:\s*)?", "", order.get("subject") or "").strip()
        # The hub tags request answers "REQ-3: <title>" - follow it to the job.
        m = re.match(r"\s*(REQ-\d+)\s*:", ctx)
        if m:
            req = _requests_by_id().get(m.group(1))
            if req:
                key = _match_job_name(reg, req.get("job", "")) or _match_job_name(reg, req.get("title", ""))
                if key:
                    return key, "answer to %s on %s" % (m.group(1), req.get("job", ""))
        key = _match_job_name(reg, ctx)
        if key:
            return key, "dashboard message tagged '%s'" % ctx
        key = _match_job_name(reg, order.get("body", "")[:400])
        if key:
            return key, "dashboard message naming the job"
        return TRIAGE, "dashboard message with no job context"

    subject = (order.get("subject") or "").lower()
    frm = (order.get("from") or "").lower()
    body = (order.get("body") or "")[:6000].lower()

    scored = []
    for key, job in reg["jobs"].items():
        score, hits = 0, []
        for term in job.get("match", []):
            t = (term or "").lower().strip()
            if len(t) < 3:
                continue
            if t in subject:
                score += 3
                hits.append("subject~%s" % t)
            elif t in body:
                score += 1
                hits.append("body~%s" % t)
        for dom in job.get("senders", []):
            if dom.lower() in frm:
                score += 2
                hits.append("from~%s" % dom)
        if score:
            scored.append((score, key, hits))

    if not scored:
        return TRIAGE, "no job matched"
    scored.sort(reverse=True)
    top, key, hits = scored[0]
    if top < MIN_SCORE:
        return TRIAGE, "weak match only (%s)" % ", ".join(hits[:3])
    if len(scored) > 1 and scored[1][0] == top:
        return TRIAGE, "ambiguous - %s and %s scored equally" % (key, scored[1][1])
    return key, ", ".join(hits[:4])


def add_job(reg, key, name, client="", match=None, senders=None):
    reg["jobs"][key] = {
        "name": name,
        "client": client,
        "match": match or [name],
        "senders": senders or [],
        "opened": dt.datetime.now().isoformat(timespec="seconds"),
    }
    chat(reg, key)
    os.makedirs(JOB_DIR, exist_ok=True)
    return reg["jobs"][key]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--add-job")
    ap.add_argument("--name", default="")
    ap.add_argument("--client", default="")
    ap.add_argument("--match", default="")
    ap.add_argument("--senders", default="")
    ap.add_argument("--test")
    args = ap.parse_args()
    reg = load_registry()

    if args.add_job:
        if not args.name:
            print("--name is required with --add-job")
            return 2
        terms = [t.strip() for t in args.match.split(",") if t.strip()] or [args.name]
        sends = [s.strip() for s in args.senders.split(",") if s.strip()]
        add_job(reg, args.add_job, args.name, args.client, terms, sends)
        save_registry(reg)
        print("added %s -> chat %s" % (args.add_job, reg["chats"][args.add_job]["session_id"]))
        return 0

    if args.test:
        key, why = route({"mailbox": "estimating", "subject": args.test, "from": "", "body": ""}, reg)
        print("%s  (%s)" % (key, why))
        return 0

    if args.list or True:
        for key, job in sorted(reg["jobs"].items()):
            c = reg["chats"].get(key, {})
            print("%-16s %-42s runs=%-3s %s" % (
                key, job.get("name", "")[:42], c.get("runs", 0),
                "live" if c.get("started") else "not started"))
        c = reg["chats"].get(TRIAGE, {})
        print("%-16s %-42s runs=%-3s %s" % (TRIAGE, "Triage (front desk)", c.get("runs", 0),
                                            "live" if c.get("started") else "not started"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

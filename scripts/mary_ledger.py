# -*- coding: utf-8 -*-
"""The ledger - everything the bots have done, as queryable events.

Phase 0 of AGENT-AUDIT.md. The root defect it fixes: what Mary has done and
what Adam has said live scattered across transcripts she cannot search, a send
log nobody reads back, and 7,000 lines of prose. "Have I already told Adam
this?" must be a LOOKUP, not a hope - so every act becomes one line of JSON in
data/ledger/YYYY-MM.jsonl, written by tools rather than discipline, and
`mary_recall.py` answers questions about it for zero session tokens.

One event per line:
  ts       when it happened (ISO; local BST where the source recorded local)
  actor    mary | adam | zac | team | jacob | system
  kind     email_sent | mail_received | hub_msg | request | request_answered |
           catch | calibration | record
  job      chat key from data/mary-jobs.json, or null when it fits no job
  summary  one line, the thing you would want back in a search result
  ref      where the full detail lives (file path, REQ id, message id) -
           ALSO the idempotency key: a backfill never writes a ref twice
  body     optional excerpt, capped short - the ledger indexes, never hoards

CLI:
  python scripts/mary_ledger.py --backfill          # all sources, idempotent
  python scripts/mary_ledger.py --add --kind decision --job georgies \
         --summary "Adam: exclude the chapel doors" --ref "REQ-12"
  python scripts/mary_ledger.py --token-baseline    # transcript cost report
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_DIR = os.path.join(REPO, "data", "ledger")
JOBS_FILE = os.path.join(REPO, "data", "mary-jobs.json")
STATE_FILE = os.path.join(REPO, "data", "dashboard-state.json")
SEND_LOG = os.path.join(REPO, "data", "mary-send-log.jsonl")
CALIBRATION = os.path.join(REPO, "data", "calibration.json")
HANDOVER = os.path.join(REPO, "HANDOVER.md")
INBOX = os.path.join(REPO, "test-results", "mary-inbox")
HUB = os.environ.get("MARY_HUB_URL", "https://mary-dashboard.pages.dev")
UA = "MaryLedger/1.0 (Mozilla/5.0 compatible)"  # CF bot protection 403s bare scripts


# ---------------------------------------------------------------- store
def _month_file(ts):
    return os.path.join(LEDGER_DIR, "%s.jsonl" % (ts[:7] if ts else "undated"))


def iter_events():
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue


def existing_refs():
    return {e.get("ref") for e in iter_events() if e.get("ref")}


def append(ts, actor, kind, job, summary, ref, body=""):
    os.makedirs(LEDGER_DIR, exist_ok=True)
    event = {"ts": ts or "", "actor": actor, "kind": kind, "job": job,
             "summary": str(summary)[:300], "ref": ref}
    if body:
        event["body"] = str(body)[:600]
    with open(_month_file(ts), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


# ---------------------------------------------------------------- job matching
def _matchers():
    """(key, [terms], [senders]) per job, from the router's own registry -
    the ledger must attribute jobs the same way routing does."""
    with open(JOBS_FILE, encoding="utf-8") as fh:
        jobs = json.load(fh).get("jobs", {})
    out = []
    for key, j in jobs.items():
        terms = [t.lower() for t in j.get("match", []) if len(t) >= 3]
        senders = [s.lower() for s in j.get("senders", [])]
        out.append((key, terms, senders))
    return out


def guess_job(text, sender="", matchers=None):
    """Router-weighted: a match term is worth 3 in the text, a sender 2.
    Below 3 the honest answer is None, exactly as triage would say."""
    text = (text or "").lower()
    sender = (sender or "").lower()
    best, best_score = None, 0
    for key, terms, senders in (matchers or _matchers()):
        score = sum(3 for t in terms if t in text) + sum(2 for s in senders if s and s in sender)
        if score > best_score:
            best, best_score = key, score
    return best if best_score >= 3 else None


# ---------------------------------------------------------------- backfills
def backfill(verbose=True, network=True):
    """Every source that already exists, into the ledger, idempotently.

    network=False skips the hub fetch - the bridge runs this after every
    session and must not stall on Cloudflare; dashboard traffic reaches the
    ledger through work orders anyway, and a networked run (cron or manual)
    tops up the rest."""
    seen = existing_refs()
    matchers = _matchers()
    added = {"email_sent": 0, "mail_received": 0, "hub_msg": 0, "request": 0,
             "request_answered": 0, "catch": 0, "calibration": 0, "record": 0}

    def put(ts, actor, kind, job, summary, ref, body=""):
        if ref in seen:
            return
        append(ts, actor, kind, job, summary, ref, body)
        seen.add(ref)
        added[kind] = added.get(kind, 0) + 1

    # 1. Every email Mary has sent (the send log is authoritative).
    if os.path.exists(SEND_LOG):
        with open(SEND_LOG, encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                subj = e.get("subject", "")
                job = e.get("chat") if e.get("chat") not in (None, "unknown-chat") else guess_job(subj, matchers=matchers)
                put(e.get("at", ""), "mary", "email_sent", job,
                    "to %s: %s" % ("+".join(e.get("to", [])), subj),
                    "sendlog:%d:%s" % (i, e.get("at", "")))

    # 2. Every work order processed (mail read, dashboard messages, botchat) -
    #    including everything Adam and Zac have ever said through them.
    for folder in ("processed", "failed", "queue"):
        for path in sorted(glob.glob(os.path.join(INBOX, folder, "*.json"))):
            try:
                with open(path, encoding="utf-8") as fh:
                    w = json.load(fh)
            except (json.JSONDecodeError, OSError):
                continue
            sender = str(w.get("from", ""))
            subj = w.get("subject") or (w.get("body", "")[:80])
            trusted = bool(w.get("trusted_sender"))
            actor = "team"
            if trusted:
                low = sender.lower()
                actor = "adam" if "adam" in low else "zac" if "zac" in low else "team"
            job = guess_job("%s %s" % (subj, w.get("body", "")[:2000]), sender, matchers)
            body = (w.get("body", "")[:600]) if trusted else ""
            put(w.get("received", ""), actor, "mail_received", job,
                "%s%s: %s" % ("[%s] " % w["mailbox"] if w.get("mailbox") not in (None, "graph") else "",
                              sender.split("<")[0].strip(), subj),
                "workorder:%s" % os.path.basename(path), body)

    # 3. The hub conversation - Adam's replies above all.
    msgs = []
    if network:
        try:
            req = urllib.request.Request(HUB + "/api/messages", headers={"user-agent": UA})
            msgs = json.load(urllib.request.urlopen(req, timeout=30))
        except Exception as e:  # noqa: BLE001 - offline backfill still does the rest
            if verbose:
                print("hub fetch failed (%s) - hub messages skipped this run" % e)
    reqs_by_id = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            state = json.load(fh)
        reqs_by_id = {r["id"]: r for r in state.get("requests", [])}
    for m in msgs:
        ctx = m.get("context") or ""
        rid = ctx.split(":")[0] if ctx.startswith("REQ-") else None
        job = (reqs_by_id.get(rid, {}).get("job") and
               guess_job(reqs_by_id[rid]["job"], matchers=matchers)) or \
            guess_job("%s %s" % (ctx, m.get("body", "")), matchers=matchers)
        put(m.get("created", ""), m.get("author", "team"), "hub_msg", job,
            "%s%s" % ("(%s) " % ctx if ctx else "", m.get("body", "")[:160]),
            "hubmsg:%s" % m.get("id"), m.get("body", "")[:600])

    # 3b. Jacob's channels - same ledger, his events (Phase 5). His unit of
    #     memory is the company, not the job, so `job` stays null here; the
    #     summaries are what recall greps.
    if network:
        def fetch(route):
            try:
                req = urllib.request.Request(HUB + "/api/" + route, headers={"user-agent": UA})
                return json.load(urllib.request.urlopen(req, timeout=30))
            except Exception:
                return []
        for m in fetch("jacob/messages"):
            put(m.get("created", ""), m.get("author", "team"), "hub_msg", None,
                "[jacob] %s%s" % ("(%s) " % m["context"] if m.get("context") else "",
                                  (m.get("body") or "")[:150]),
                "jacobmsg:%s" % m.get("id"), (m.get("body") or "")[:600])
        for r in fetch("jacob/requests"):
            put(r.get("created", ""), "jacob", "request", None,
                "%s: %s" % (r.get("ref", "?"), r.get("title", "")),
                "jreq:%s" % r.get("ref"))
            if r.get("status") == "answered" and r.get("answer"):
                put(r.get("answered_at", ""), r.get("answered_by", "team"),
                    "request_answered", None,
                    "%s answered: %s" % (r.get("ref", "?"), str(r.get("answer", ""))[:150]),
                    "jreqans:%s" % r.get("ref"), str(r.get("answer", ""))[:600])
        for m in fetch("botchat"):
            put(m.get("created", ""), m.get("sender", "?"), "botchat", None,
                "-> %s: %s%s" % (m.get("recipient", "?"),
                                 ("%s - " % m["subject"]) if m.get("subject") else "",
                                 (m.get("body") or "")[:140]),
                "botchat:%s" % m.get("id"), (m.get("body") or "")[:600])

    # 4. Requests and their answers - the settled-decisions spine.
    for r in reqs_by_id.values():
        job = guess_job(r.get("job", ""), matchers=matchers)
        put(r.get("raised", ""), "mary", "request", job,
            "%s: %s (needs %s)" % (r["id"], r.get("title", ""), r.get("owner", "?")),
            "req:%s" % r["id"])
        if r.get("status") == "answered" and r.get("answer"):
            put(r.get("answered_at", ""), r.get("answered_by", "team"),
                "request_answered", job,
                "%s answered: %s" % (r["id"], str(r.get("answer", ""))[:160]),
                "reqans:%s" % r["id"], str(r.get("answer", ""))[:600])

    # 5. Catches - the record of errors found and money saved.
    if os.path.exists(STATE_FILE):
        for i, c in enumerate(state.get("catches", [])):
            job = guess_job(c.get("job", ""), matchers=matchers)
            put(c.get("date", ""), "mary", "catch", job,
                "%s: %s" % (c.get("job", "?"), str(c.get("catch", ""))[:180]),
                "catch:%d:%s" % (i, c.get("date", "")))

    # 6. Calibration points - every time her number met a human's.
    if os.path.exists(CALIBRATION):
        try:
            with open(CALIBRATION, encoding="utf-8") as fh:
                cal = json.load(fh)
            points = cal if isinstance(cal, list) else cal.get("points", cal.get("entries", []))
            for i, p in enumerate(points):
                if not isinstance(p, dict):
                    continue
                job = guess_job(str(p.get("job", "")), matchers=matchers)
                put(p.get("date", ""), "mary", "calibration", job,
                    "%s: mary %s vs actual %s" % (p.get("job", "?"),
                                                  p.get("mary_estimate", p.get("mary", "?")),
                                                  p.get("actual", "?")),
                    "cal:%d" % i, str(p.get("lesson", ""))[:600])
        except (json.JSONDecodeError, OSError):
            pass

    # 7. HANDOVER.md records - indexed, not copied. The heading and the line
    #    number are enough to land a future reader on the full account.
    if os.path.exists(HANDOVER):
        with open(HANDOVER, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                m = re.match(r"^### (.+)$", line.strip())
                if not m:
                    continue
                title = m.group(1)
                d = re.search(r"\((\d{4}-\d{2}-\d{2})", title)
                job = guess_job(title, matchers=matchers)
                put(d.group(1) if d else "", "mary", "record", job,
                    title, "handover:%d" % n)

    if verbose:
        total = sum(added.values())
        print("backfill: %d new events (%s)" % (
            total, ", ".join("%s %d" % (k, v) for k, v in added.items() if v)))
    return added


# ---------------------------------------------------------------- baseline
def token_baseline():
    """What each chat's transcript costs to carry. Chars/4 is a coarse token
    estimate but it ranks chats correctly, which is all rotation needs."""
    proj = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                        "C--Users-zacpl-Desktop-Glazing-Quote-Assistant")
    with open(JOBS_FILE, encoding="utf-8") as fh:
        chats = json.load(fh).get("chats", {})
    rows = []
    for key, c in chats.items():
        sid = c.get("session_id", "")
        path = os.path.join(proj, "%s.jsonl" % sid)
        if not os.path.exists(path):
            rows.append((key, sid[:8], 0, 0, "no transcript"))
            continue
        size = os.path.getsize(path)
        with open(path, encoding="utf-8", errors="replace") as fh:
            turns = sum(1 for _ in fh)
        rows.append((key, sid[:8], size, turns,
                     datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m %H:%M")))
    rows.sort(key=lambda r: -r[2])
    out = ["# Token baseline - %s" % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
           "", "Transcript size is the resume cost. est-tokens = bytes/4.", "",
           "| chat | size MB | events | est tokens | last active |", "|---|---|---|---|---|"]
    for key, sid, size, turns, last in rows:
        out.append("| %s | %.1f | %d | %s | %s |" % (
            key, size / 1e6, turns, "{:,}".format(size // 4), last))
    out.append("")
    out.append("Total: %.0f MB across %d chats (est %s tokens at rest)." % (
        sum(r[2] for r in rows) / 1e6, len(rows),
        "{:,}".format(sum(r[2] for r in rows) // 4)))
    report = "\n".join(out) + "\n"
    dest = os.path.join(REPO, "test-results", "token-baseline.md")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)
    print("written to", os.path.relpath(dest, REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--token-baseline", action="store_true")
    ap.add_argument("--add", action="store_true")
    ap.add_argument("--kind"), ap.add_argument("--job"), ap.add_argument("--summary")
    ap.add_argument("--ref"), ap.add_argument("--body", default="")
    ap.add_argument("--actor", default="mary")
    a = ap.parse_args()
    if a.backfill:
        backfill()
    elif a.token_baseline:
        token_baseline()
    elif a.add:
        if not (a.kind and a.summary and a.ref):
            ap.error("--add needs --kind, --summary and --ref")
        e = append(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
                   a.actor, a.kind, a.job, a.summary, a.ref, a.body)
        print("added:", json.dumps(e, ensure_ascii=False))
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

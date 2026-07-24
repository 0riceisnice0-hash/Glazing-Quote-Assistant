# -*- coding: utf-8 -*-
"""Mary Grace's inbox poller. Runs every 15 min from Task Scheduler.

Costs NOTHING per empty poll: it is plain HTTPS against Microsoft Graph.
A Claude Code session is launched ONLY when new mail is queued.

Flow:
  1. Read state (data/mary-state.json: processed message ids per mailbox).
  2. List recent inbox messages for estimating@ and mary@.
  3. For each unseen message: save body text + metadata to
     test-results/mary-inbox/queue/<n>-<id8>.json and attachments to a
     sibling folder. Mark id as processed in state (so a crashed session
     never double-queues; the queue file itself is the work order).
  4. If anything is queued (new or left over) and no session is running,
     launch: claude -p <kick prompt> from the repo root.

Flags:
  --backfill-hours N   look back N hours instead of since-last-state
  --no-launch          queue only, do not start a Claude session (dry run)
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

REPO = mg.REPO
STATE = os.path.join(REPO, "data", "mary-state.json")
QUEUE = os.path.join(REPO, "test-results", "mary-inbox", "queue")
PROCESSED_DIR = os.path.join(REPO, "test-results", "mary-inbox", "processed")
LOCK = os.path.join(REPO, "test-results", "mary-inbox", "session.lock")
LOG = os.path.join(REPO, "test-results", "mary-inbox", "poller.log")
CLAUDE_CMD = os.environ.get("MARY_CLAUDE_CMD", "claude")
KICK = ("You are Mary Grace, Fenster Glazing's estimating AI. New email has been queued for you. "
        "Read MARY-EMAIL-SESSION.md in the repo root and follow it exactly.")


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("[%s] %s\n" % (stamp, msg))
    print(msg)


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {"processed": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1)


def session_running():
    if not os.path.exists(LOCK):
        return False
    age = dt.datetime.now().timestamp() - os.path.getmtime(LOCK)
    if age > 2 * 3600:  # stale lock: a session should never take 2h
        os.remove(LOCK)
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill-hours", type=int, default=0)
    ap.add_argument("--no-launch", action="store_true")
    args = ap.parse_args()

    env = mg.load_env()
    token = mg.get_token(env, "READER")
    state = load_state()
    os.makedirs(QUEUE, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    since = None
    if args.backfill_hours:
        since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=args.backfill_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_count = 0
    for mailbox in (mg.ESTIMATING, mg.MARY):
        seen = set(state["processed"].setdefault(mailbox, []))
        try:
            msgs = mg.list_messages(token, mailbox, since_iso=since,
                                    top=50 if args.backfill_hours else 25,
                                    whole_mailbox=(mailbox == mg.ESTIMATING))
        except Exception as e:
            log("LIST FAILED %s: %s" % (mailbox, e))
            continue
        for m in msgs:
            mid = m["id"]
            if mid in seen:
                continue
            frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?").lower()
            if frm == mg.MARY:
                seen.add(mid)  # never react to our own mail
                continue
            try:
                full = mg.get_message_body(token, mailbox, mid)
                body_txt = mg.html_to_text(full.get("body", {}).get("content", ""))
                short = re.sub(r"[^A-Za-z0-9]", "", mid)[-8:]
                stampkey = m.get("receivedDateTime", "").replace(":", "").replace("-", "")[:13]
                base = "%s-%s" % (stampkey, short)
                att_dir = os.path.join(QUEUE, base + "-att")
                saved = mg.download_attachments(token, mailbox, mid, att_dir) if m.get("hasAttachments") else []
                rec = {
                    "mailbox": mailbox, "id": mid,
                    "from": frm, "subject": m.get("subject", ""),
                    "received": m.get("receivedDateTime", ""),
                    "to": [r.get("emailAddress", {}).get("address", "") for r in full.get("toRecipients", [])],
                    "cc": [r.get("emailAddress", {}).get("address", "") for r in full.get("ccRecipients", [])],
                    "trusted_sender": frm in mg.TRUSTED_SENDERS,
                    "attachments": saved,
                    "body": body_txt[:20000],
                }
                with open(os.path.join(QUEUE, base + ".json"), "w", encoding="utf-8") as fh:
                    json.dump(rec, fh, indent=1, ensure_ascii=False)
                seen.add(mid)
                new_count += 1
                log("QUEUED [%s] %s | %s" % (mailbox.split('@')[0], frm, rec["subject"][:70]))
            except Exception as e:
                log("QUEUE FAILED %s %s: %s" % (mailbox, mid[:12], e))
        state["processed"][mailbox] = list(seen)[-2000:]
    save_state(state)

    pending = [f for f in os.listdir(QUEUE) if f.endswith(".json")]
    log("poll done: %d new, %d pending in queue" % (new_count, len(pending)))

    if pending and not args.no_launch:
        if session_running():
            log("session already running - not launching another")
            return
        with open(LOCK, "w") as fh:
            fh.write(str(os.getpid()))
        log("launching Claude session for %d queued email(s)" % len(pending))
        try:
            r = subprocess.run([CLAUDE_CMD, "-p", KICK, "--dangerously-skip-permissions"],
                               cwd=REPO, capture_output=True, text=True, timeout=90 * 60, shell=True)
            log("session exit %s" % r.returncode)
            if r.stdout:
                with open(os.path.join(os.path.dirname(LOG), "last-session-output.txt"), "w", encoding="utf-8") as fh:
                    fh.write(r.stdout[-20000:])
        except Exception as e:
            log("SESSION LAUNCH FAILED: %s" % e)
        finally:
            if os.path.exists(LOCK):
                os.remove(LOCK)


if __name__ == "__main__":
    main()

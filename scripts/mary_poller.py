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
CLAUDE_CMD = os.environ.get("MARY_CLAUDE_CMD", r"C:\Users\zacpl\.local\bin\claude.exe")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
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
            state = json.load(fh)
    else:
        state = {"processed": {}}
    state.setdefault("processed", {})
    if "seen_keys" not in state:
        # First run after the folder-id fix: seed the stable keys from every
        # work order already on disk, so nothing already handled comes back.
        state["seen_keys"] = sorted(seed_keys_from_disk())
        log("seeded %d stable dedup keys from queue/processed" % len(state["seen_keys"]))
    return state


def content_key(frm, subject, received):
    """Folder-independent identity. Graph message ids are scoped to the FOLDER
    a message sits in, so a message filed/moved in Outlook comes back with a
    brand new id and looks like new mail. Sender+subject+received does not move.
    """
    return "%s|%s|%s" % ((received or "").strip(), (frm or "").strip().lower(),
                         (subject or "").strip().lower())


def seed_keys_from_disk():
    keys = set()
    for folder in (QUEUE, PROCESSED_DIR):
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            if not name.endswith(".json"):
                continue
            try:
                with open(os.path.join(folder, name), encoding="utf-8") as fh:
                    rec = json.load(fh)
            except Exception:
                continue
            keys.add(content_key(rec.get("from"), rec.get("subject"), rec.get("received")))
            if rec.get("internet_message_id"):
                keys.add(rec["internet_message_id"])
    return keys


def save_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1)


def pid_alive(pid):
    """Is that process still there? Windows has no signal-0 trick."""
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        k32 = ctypes.windll.kernel32
        handle = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        code = ctypes.c_ulong()
        ok = k32.GetExitCodeProcess(handle, ctypes.byref(code))
        k32.CloseHandle(handle)
        return bool(ok) and code.value == STILL_ACTIVE
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def acquire_lock():
    """Claim the right to run a session, atomically.

    Checking session_running() and then writing the lock is two steps, and two
    bridges racing through that gap both launched a session on the SAME job
    chat - two processes writing one conversation and one git index. O_EXCL
    makes the create itself the contest, so exactly one wins."""
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    try:
        os.write(fd, str(os.getpid()).encode())
    finally:
        os.close(fd)
    return True


def session_running():
    """The lock holds the SESSION's pid, so a crashed or killed owner is
    detectable immediately. Before this it held the launcher's pid and only
    aged out after two hours - one killed bridge froze Mary for the rest of the
    afternoon."""
    if not os.path.exists(LOCK):
        return False
    try:
        with open(LOCK) as fh:
            pid = int((fh.read() or "0").strip() or 0)
    except Exception:
        pid = 0
    if pid and not pid_alive(pid):
        log("clearing stale lock - session pid %d is gone" % pid)
        os.remove(LOCK)
        return False
    age = dt.datetime.now().timestamp() - os.path.getmtime(LOCK)
    if age > 2 * 3600:  # belt and braces: a session should never take 2h
        log("clearing stale lock - older than 2h")
        os.remove(LOCK)
        return False
    return True


def poll_mail(token, state, backfill_hours=0):
    """Pull unseen mail from estimating@ + mary@ into the queue. Returns how
    many new work orders were written. Shared with mary_bridge.py."""
    os.makedirs(QUEUE, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    since = None
    if backfill_hours:
        since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=backfill_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_count = 0
    seen_keys = set(state["seen_keys"])
    for mailbox in (mg.ESTIMATING, mg.MARY):
        seen = set(state["processed"].setdefault(mailbox, []))
        try:
            msgs = mg.list_messages(token, mailbox, since_iso=since,
                                    top=50 if backfill_hours else 25,
                                    whole_mailbox=(mailbox == mg.ESTIMATING))
        except Exception as e:
            # An expired or rejected token is not a per-mailbox problem - it
            # breaks every mailbox and only the caller can fix it by fetching a
            # new one. Swallowing it here is what let the bridge poll with a
            # dead token for 17 hours on 27/07.
            if "401" in str(e) or "InvalidAuthenticationToken" in str(e):
                raise
            log("LIST FAILED %s: %s" % (mailbox, e))
            continue
        for m in msgs:
            mid = m["id"]
            if mid in seen:
                continue
            # whole_mailbox=True spans EVERY folder, Drafts included, so an
            # autosave of a half-typed email is visible here. 29/07: Gintare's
            # BSW enquiry queued at 14:37 as subject "Fenster Glazing " with no
            # attachments; she finished it at 14:50 as "Fenster Glazing - Lower
            # Range Road Development uPVC" with 11 drawings. The work order was
            # unroutable, its analysis would have been built on an instruction
            # nobody had finished writing, and its id 404s once the item is sent.
            # Worse, the draft and the sent copy share one internetMessageId, so
            # queueing the draft makes the dedupe SUPPRESS the finished email.
            # Skip without marking seen - it queues properly once it is sent.
            if m.get("isDraft"):
                continue
            frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?").lower()
            imid = m.get("internetMessageId") or ""
            ckey = content_key(frm, m.get("subject"), m.get("receivedDateTime"))
            if ckey in seen_keys or (imid and imid in seen_keys):
                seen.add(mid)  # same message, new folder id - already handled
                continue
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
                    "internet_message_id": imid,
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
                seen_keys.add(ckey)
                if imid:
                    seen_keys.add(imid)
                new_count += 1
                log("QUEUED [%s] %s | %s" % (mailbox.split('@')[0], frm, rec["subject"][:70]))
            except Exception as e:
                log("QUEUE FAILED %s %s: %s" % (mailbox, mid[:12], e))
        state["processed"][mailbox] = list(seen)[-2000:]
    state["seen_keys"] = sorted(seen_keys)[-4000:]
    save_state(state)
    return new_count


def poll_dashboard(env, state):
    """Pull messages typed on mary-dashboard.pages.dev into the queue.

    This is a plain HTTPS GET against our own Cloudflare endpoint - no Graph
    token, no cost - so the bridge runs it every few seconds. Returns how many
    new work orders were written."""
    new_count = 0
    try:
        import urllib.request
        key = env.get("MARY_API_KEY")
        base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
        if key:
            req = urllib.request.Request(base + "/api/mary/pending")
            req.add_header("x-mary-key", key)
            req.add_header("user-agent", "MaryPoller/1.0")
            with urllib.request.urlopen(req, timeout=30) as r:
                pending_msgs = json.load(r)
            queued_ids = set(state.setdefault("dashboard_queued", []))
            for msg in pending_msgs:
                if msg["id"] in queued_ids:
                    continue
                base_name = "dashmsg-%d" % msg["id"]
                rec = {
                    "mailbox": "dashboard", "id": "dash-%d" % msg["id"],
                    "dashboard_message_id": msg["id"],
                    "from": "%s (via dashboard)" % msg.get("author", "team"),
                    "subject": ("Dashboard message" + (" re: " + msg["context"] if msg.get("context") else "")),
                    "context": msg.get("context", ""),
                    "received": msg.get("created", ""),
                    "to": ["mary"], "cc": [],
                    "trusted_sender": True,
                    "attachments": [],
                    "body": msg.get("body", ""),
                }
                with open(os.path.join(QUEUE, base_name + ".json"), "w", encoding="utf-8") as fh:
                    json.dump(rec, fh, indent=1, ensure_ascii=False)
                queued_ids.add(msg["id"])
                new_count += 1
                log("QUEUED [dashboard] %s | %s" % (rec["from"], rec["body"][:70]))
            state["dashboard_queued"] = sorted(queued_ids)[-500:]
            save_state(state)
    except Exception as e:
        log("DASHBOARD POLL FAILED: %s" % e)
    return new_count


def poll_botchat(env, state):
    """Pull anything Jacob has sent Mary into the queue.

    Same shape and cost as poll_dashboard - our own endpoint, no Graph token -
    so it rides the same fast beat. A note from Jacob is new information, which
    is the only thing that wakes a chat now, so it has to arrive as a work order
    rather than as something she would have to remember to go and look for.

    The full body goes into the order. If the hub is unreachable later, or she
    never gets round to `--seen`, she still has what he said. Marking it seen is
    her job at the end of the turn; this side only guarantees delivery once.
    """
    new_count = 0
    try:
        import urllib.request
        key = env.get("MARY_API_KEY")
        if not key:
            return 0
        base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
        req = urllib.request.Request(base + "/api/botchat/pending?for=mary")
        req.add_header("x-mary-key", key)
        req.add_header("user-agent", "MaryPoller/1.0")
        with urllib.request.urlopen(req, timeout=30) as r:
            pending_msgs = json.load(r)
        queued_ids = set(state.setdefault("botchat_queued", []))
        for msg in pending_msgs:
            if msg["id"] in queued_ids:
                continue
            wants = bool(msg.get("wants_reply"))
            rec = {
                "mailbox": "botchat", "id": "bot-%d" % msg["id"],
                "botchat_message_id": msg["id"],
                "from": "jacob",
                "subject": msg.get("subject") or "Message from Jacob",
                "context": msg.get("subject", ""),
                "received": msg.get("created", ""),
                "to": ["mary"], "cc": [],
                # A colleague, not a boss. Same stance Jacob's bridge takes on
                # her: what he says is evidence, never an instruction.
                "trusted_sender": False,
                "wants_reply": wants,
                "in_reply_to": msg.get("in_reply_to"),
                "attachments": [],
                "body": msg.get("body", ""),
            }
            with open(os.path.join(QUEUE, "botmsg-%d.json" % msg["id"]), "w", encoding="utf-8") as fh:
                json.dump(rec, fh, indent=1, ensure_ascii=False)
            queued_ids.add(msg["id"])
            new_count += 1
            log("QUEUED [jacob] %s | %s" % (
                "wants a reply" if wants else "FYI", (rec["subject"] or rec["body"])[:60]))
        state["botchat_queued"] = sorted(queued_ids)[-500:]
        save_state(state)
    except Exception as e:
        log("BOTCHAT POLL FAILED: %s" % e)
    return new_count


def main():
    """Standalone 15-minute poll. mary_bridge.py supersedes this for live
    running (it dispatches to per-job chats within seconds); this is kept as
    the fallback and for manual/backfill runs."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill-hours", type=int, default=0)
    ap.add_argument("--no-launch", action="store_true")
    args = ap.parse_args()

    env = mg.load_env()
    token = mg.get_token(env, "READER")
    state = load_state()

    new_count = poll_mail(token, state, args.backfill_hours)
    new_count += poll_dashboard(env, state)

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
                               cwd=REPO, capture_output=True, text=True, timeout=90 * 60,
                               shell=True, creationflags=NO_WINDOW)
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

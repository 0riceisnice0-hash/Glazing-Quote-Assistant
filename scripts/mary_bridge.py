# -*- coding: utf-8 -*-
"""Mary's always-on bridge: intake -> routing -> the right job chat.

Replaces the 15-minute MaryGracePoller for live running. Two things changed:

  SPEED. Dashboard messages are a plain HTTPS GET against our own Cloudflare
  endpoint, so they cost nothing and are checked every few seconds - type on
  the hub and Mary starts within seconds, or the moment she is free if she is
  mid-session. Mail still needs a Graph token, so it polls on a slower beat.

  MEMORY. Work is dispatched to a PERMANENT per-job conversation
  (`claude -p --resume <uuid>`), not a fresh session that has to re-read the
  handover docs to remember a job it priced that morning. Anything that does
  not belong to a known job goes to the triage chat.

Run:
  python scripts/mary_bridge.py            # forever (this is the live mode)
  python scripts/mary_bridge.py --once     # single pass, for testing
  python scripts/mary_bridge.py --status   # what it is doing right now
  python scripts/mary_bridge.py --dry-run  # route and report, launch nothing
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_poller as mp
import mary_router as router
import mary_note as note

REPO = mg.REPO
QUEUE = mp.QUEUE
LOCK = mp.LOCK
FAILED = os.path.join(REPO, "test-results", "mary-inbox", "failed")
BRIDGE_STATE = os.path.join(REPO, "data", "mary-bridge-state.json")
STATUS = os.path.join(REPO, "data", "mary-bridge-status.json")
PIDFILE = os.path.join(REPO, "test-results", "mary-inbox", "bridge.pid")

DASH_EVERY = 5           # seconds - our own endpoint, free
MAIL_EVERY = 120         # seconds - Microsoft Graph
TICK = 2
MAX_ATTEMPTS = 3         # per work order before it is quarantined
SESSION_TIMEOUT = 90 * 60
# A session that dies in under a minute did not do any work - that is a usage
# limit or a broken CLI, and retrying instantly would just hammer the API.
FAST_FAIL_SECONDS = 60
BACKOFF = [60, 300, 900, 1800]


def log(msg):
    mp.log(msg)


def load_bridge_state():
    if os.path.exists(BRIDGE_STATE):
        try:
            with open(BRIDGE_STATE, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {"fails": 0, "backoff_until": 0, "attempts": {}}


def save_bridge_state(st):
    os.makedirs(os.path.dirname(BRIDGE_STATE), exist_ok=True)
    with open(BRIDGE_STATE, "w", encoding="utf-8") as fh:
        json.dump(st, fh, indent=1)


ENV = {}
_pushed = [None]


def write_status(state, chat_key=None, depth=0, detail="", title=""):
    """Record what Mary is doing, locally and on the hub.

    The hub only needs to hear about it when it CHANGES, so the site can say
    "working on Grange Hill" or "3 queued" without us writing to D1 on a
    two-second loop."""
    payload = {
        "state": state,                       # idle | working | backoff
        "chat": chat_key,
        "title": title or (chat_key or ""),
        "queue_depth": depth,
        "detail": detail,
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
    }
    try:
        with open(STATUS, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=1)
    except Exception:
        pass

    fingerprint = (state, chat_key, depth, detail)
    if fingerprint != _pushed[0]:
        try:
            import urllib.request
            key = ENV.get("MARY_API_KEY")
            if key:
                base = ENV.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
                req = urllib.request.Request(
                    base + "/api/mary/status",
                    data=json.dumps(payload).encode("utf-8"), method="POST")
                req.add_header("x-mary-key", key)
                req.add_header("content-type", "application/json")
                req.add_header("user-agent", "MaryBridge/1.0")
                urllib.request.urlopen(req, timeout=15).read()
                # Only now is it really pushed - marking it earlier would mean
                # a single failure froze the hub's status until the next change.
                _pushed[0] = fingerprint
        except Exception as e:
            log("status push failed: %s" % e)
    return payload


def read_orders():
    """Every work order sitting in the queue, oldest first."""
    if not os.path.isdir(QUEUE):
        return []
    out = []
    for name in sorted(os.listdir(QUEUE)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(QUEUE, name)
        try:
            with open(path, encoding="utf-8") as fh:
                rec = json.load(fh)
        except Exception as e:
            log("UNREADABLE work order %s: %s" % (name, e))
            continue
        rec["_file"] = name
        rec["_path"] = path
        rec["_mtime"] = os.path.getmtime(path)
        out.append(rec)
    out.sort(key=lambda r: r["_mtime"])
    return out


def group_by_chat(orders, reg):
    """Route every order, then return groups keyed by chat, oldest group first."""
    groups = {}
    for order in orders:
        key, why = router.route(order, reg)
        order["_route_why"] = why
        groups.setdefault(key, []).append(order)
    return sorted(groups.items(), key=lambda kv: min(o["_mtime"] for o in kv[1]))


def describe(order):
    if order.get("mailbox") == "dashboard":
        who = order.get("from", "team")
        ctx = (" [%s]" % order["context"]) if order.get("context") else ""
        return "%s: %s%s - \"%s\"" % (order["_file"], who, ctx, (order.get("body") or "")[:120].replace("\n", " "))
    return "%s: %s | %s" % (order["_file"], order.get("from", "?"), (order.get("subject") or "(no subject)")[:90])


def build_prompt(key, title, orders, handoffs, first_run, reg):
    lines = []
    if first_run:
        if key == router.TRIAGE:
            lines.append(
                "You are Mary Grace, Fenster Glazing's estimating AI. This conversation is your permanent "
                "TRIAGE chat - the front desk. It is resumed for every piece of work that does not belong to "
                "an existing job chat, so treat it as a running log of what is arriving.\n\n"
                "Read MARY-JOB-SESSION.md now (it explains how the chats work), then MARY-EMAIL-SESSION.md "
                "for the triage rules, then MARY-HANDOVER.md for the standing rules and live job table.")
        else:
            job = reg["jobs"].get(key, {})
            lines.append(
                "You are Mary Grace, Fenster Glazing's estimating AI. This conversation is the PERMANENT chat "
                "for ONE job: %s%s. It will be resumed for every future piece of work on this job, so what you "
                "learn here you keep - you will not have to rebuild it from the handover docs again.\n\n"
                "One-off setup, do it now: read MARY-JOB-SESSION.md, then find this job's row in "
                "MARY-HANDOVER.md section 7 and its record in HANDOVER.md, and read data/jobs/%s.md if it "
                "exists. Build a complete picture of where this job stands - scope, price, who owes what, the "
                "deadline - before you touch the work below."
                % (title, (" for " + job.get("client", "")) if job.get("client") else "", key))
    else:
        lines.append(
            "New work for %s. This chat already holds this job's history - use it. Do NOT re-read the handover "
            "documents unless something specific is missing; that is what this conversation is for."
            % title)

    lines.append("\nWORK ORDERS (full JSON in test-results\\mary-inbox\\queue\\):")
    for o in orders:
        lines.append("  - %s" % describe(o))
        lines.append("    routed here because: %s" % o.get("_route_why", "?"))

    if handoffs:
        lines.append("\nHANDOFFS from Mary's other chats - read these before you start:")
        for h in handoffs:
            lines.append("  - from %s (%s): %s" % (h["from"], h["created"], h["body"][:600]))

    board = note.read_board(limit=12)
    if board.strip():
        lines.append("\nNOTICEBOARD (latest shared facts across all chats):\n### " + board.strip())

    lines.append(
        "\nFollow MARY-JOB-SESSION.md exactly, including the close-out: answer on the dashboard if a work "
        "order came from there, move handled queue files to processed\\, update data/jobs/%s.md, post anything "
        "other chats need with scripts/mary_note.py, and commit." % key)
    return "\n".join(lines)


def dispatch(key, orders, reg, bst, dry_run=False):
    """Run one chat against its work orders. Returns True if the session ran clean."""
    rec = router.chat(reg, key)
    title = router.job_title(reg, key)
    handoffs = note.pending_handoffs(key)
    first_run = not rec.get("started")
    prompt = build_prompt(key, title, orders, handoffs, first_run, reg)

    if dry_run:
        log("DRY RUN would dispatch %d order(s) to [%s] %s (%s)"
            % (len(orders), key, title, "new chat" if first_run else "resume %s" % rec["session_id"][:8]))
        for o in orders:
            log("        %s  <- %s" % (describe(o), o.get("_route_why")))
        return True

    cmd = [mp.CLAUDE_CMD, "-p", prompt, "--dangerously-skip-permissions"]
    cmd += (["--session-id", rec["session_id"]] if first_run else ["--resume", rec["session_id"]])

    env = os.environ.copy()
    env["MARY_CHAT_KEY"] = key

    write_status("working", key, len(orders), "%d work order(s)" % len(orders), title=title)
    with open(LOCK, "w") as fh:
        fh.write(str(os.getpid()))
    log("dispatch -> [%s] %s : %d order(s), %s"
        % (key, title, len(orders), "NEW chat" if first_run else "resuming chat"))
    started = time.time()
    ok = False
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                           timeout=SESSION_TIMEOUT, env=env, encoding="utf-8", errors="replace")
        took = time.time() - started
        ok = r.returncode == 0
        log("  [%s] session exit %s after %ds" % (key, r.returncode, int(took)))
        out = (r.stdout or "") + ("\n--- stderr ---\n" + r.stderr if r.stderr else "")
        if out.strip():
            with open(os.path.join(REPO, "test-results", "mary-inbox",
                                   "last-session-%s.txt" % key), "w", encoding="utf-8") as fh:
                fh.write(out[-20000:])
        if ok:
            rec["started"] = True
            rec["runs"] = rec.get("runs", 0) + 1
            rec["last_active"] = dt.datetime.now().isoformat(timespec="seconds")
            note.mark_delivered(handoffs)
            bst["fails"] = 0
        else:
            # A new chat that failed never really started - do not resume a
            # conversation that may not exist.
            if first_run:
                rec["started"] = False
            if took < FAST_FAIL_SECONDS:
                bst["fails"] = bst.get("fails", 0) + 1
                wait = BACKOFF[min(bst["fails"] - 1, len(BACKOFF) - 1)]
                bst["backoff_until"] = time.time() + wait
                log("  fast failure #%d (usage limit or CLI problem) - backing off %ds"
                    % (bst["fails"], wait))
                write_status("backoff", key, len(orders), "retrying in %ds" % wait, title=title)
    except subprocess.TimeoutExpired:
        log("  [%s] session TIMED OUT after %ds" % (key, SESSION_TIMEOUT))
    except Exception as e:
        log("  [%s] SESSION LAUNCH FAILED: %s" % (key, e))
    finally:
        if os.path.exists(LOCK):
            os.remove(LOCK)
        router.save_registry(reg)

    # Anything the session left behind gets a couple more goes, then is parked
    # so one poisoned work order cannot block the queue forever.
    for o in orders:
        if not os.path.exists(o["_path"]):
            bst["attempts"].pop(o["_file"], None)
            continue
        n = bst["attempts"].get(o["_file"], 0) + 1
        bst["attempts"][o["_file"]] = n
        if n >= MAX_ATTEMPTS:
            os.makedirs(FAILED, exist_ok=True)
            os.replace(o["_path"], os.path.join(FAILED, o["_file"]))
            bst["attempts"].pop(o["_file"], None)
            log("  PARKED %s in failed\\ after %d attempts - needs a human" % (o["_file"], n))
            note.post_board("Work order %s could not be handled after %d attempts and has been moved to "
                            "test-results\\mary-inbox\\failed\\. It needs a human look."
                            % (o["_file"], n), author="bridge")
    save_bridge_state(bst)
    return ok


def one_pass(env, token, state, bst, reg, force_mail=False, dry_run=False):
    """Intake, then dispatch at most one chat. Returns seconds to wait."""
    now = time.time()
    if now - state.get("_last_dash", 0) >= DASH_EVERY:
        mp.poll_dashboard(env, state)
        state["_last_dash"] = now
    if force_mail or now - state.get("_last_mail", 0) >= MAIL_EVERY:
        if token[0]:
            try:
                mp.poll_mail(token[0], state)
            except Exception as e:
                log("MAIL POLL FAILED: %s" % e)
                token[0] = None      # token probably expired - fetch a new one
        else:
            try:
                token[0] = mg.get_token(env, "READER")
            except Exception as e:
                log("TOKEN REFRESH FAILED: %s" % e)
        state["_last_mail"] = now

    if time.time() < bst.get("backoff_until", 0):
        return TICK
    # Never run two sessions at once - they share one repo, one git index and
    # one dashboard state. The lockfile is also how we coexist with the old
    # 15-minute poller if it is ever re-enabled.
    if mp.session_running():
        depth = len(read_orders())
        write_status("working", None, depth, "a session is already running")
        return TICK

    orders = read_orders()
    groups = group_by_chat(orders, reg)
    # A chat with handoffs but no mail still deserves a turn - that is how one
    # job's finding reaches another.
    if not groups:
        for key in list(reg["chats"].keys()) + [router.TRIAGE]:
            if note.pending_handoffs(key):
                groups = [(key, [])]
                break
    if not groups:
        write_status("idle", None, 0)
        return TICK

    key, group = groups[0]
    dispatch(key, group, reg, bst, dry_run=dry_run)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status:
        for path, label in ((STATUS, "status"), (BRIDGE_STATE, "state")):
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    print("%s: %s" % (label, fh.read().strip()))
        print("queue: %d work order(s)" % len(read_orders()))
        return 0

    env = mg.load_env()
    ENV.update(env)
    state = mp.load_state()
    bst = load_bridge_state()
    reg = router.load_registry()
    router.chat(reg, router.TRIAGE)
    router.save_registry(reg)

    token = [None]
    try:
        token[0] = mg.get_token(env, "READER")
    except Exception as e:
        log("BRIDGE start: no Graph token yet (%s) - dashboard still works" % e)

    with open(PIDFILE, "w") as fh:
        fh.write(str(os.getpid()))
    log("BRIDGE up (pid %d): dashboard every %ds, mail every %ds, %d job chats"
        % (os.getpid(), DASH_EVERY, MAIL_EVERY, len(reg["jobs"])))

    try:
        while True:
            try:
                wait = one_pass(env, token, state, bst, reg,
                                force_mail=args.once, dry_run=args.dry_run)
            except Exception as e:
                log("BRIDGE loop error: %s" % e)
                wait = 10
            if args.once:
                break
            time.sleep(wait or TICK)
    except KeyboardInterrupt:
        log("BRIDGE stopped by hand")
    finally:
        mp.save_state(state)
        if os.path.exists(PIDFILE):
            os.remove(PIDFILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())

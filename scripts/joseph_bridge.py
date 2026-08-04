# -*- coding: utf-8 -*-
"""JOSEPH - the bridge. A session only when a won job needs judgement.

Built on the P1 cost architecture and the P2 memory shape from the start,
rather than retrofitted the way the other two were: one permanent chat per
contract, resumed; real token accounting read out of the transcript; rotation
on context rather than file size; the shared night curfew.

WHAT WAKES HIM
  a message from Zac or Adam on the hub
  a step falling due or going late on a live contract
  a message from Mary or Jacob on the internal line

WHAT DOES NOT
  the daily sweep. `joseph_daily.py` refreshes dates and rebuilds the board
  deterministically and spends nothing. A session is for the judgement: the
  survey has moved and three orders now sit the wrong side of it, the client
  has changed a spec after the frames went on order, the fitters are double
  booked. None of that is a checklist.

  python scripts/joseph_bridge.py            # the loop
  python scripts/joseph_bridge.py --status
  python scripts/joseph_bridge.py --once
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joseph_router as router   # noqa: E402
import bot_status                # noqa: E402
import crm                       # noqa: E402
import crm_contract              # noqa: E402
import mary_cost as cost         # noqa: E402
import mary_budget as budget     # noqa: E402

INBOX = os.path.join(REPO, "test-results", "joseph-inbox")
QUEUE = os.path.join(INBOX, "queue")
DONE = os.path.join(INBOX, "processed")
STATE = os.path.join(REPO, "data", "joseph-bridge-state.json")
LOG = os.path.join(INBOX, "bridge.log")
LOCK = os.path.join(INBOX, "session.lock")
PIDFILE = os.path.join(INBOX, "bridge.pid")
MANUAL = os.path.join(REPO, "JOSEPH-SESSION.md")
CONTRACT_DIR = os.path.join(REPO, "data", "contracts")

POLL_SECONDS = 120
FAST_FAIL_SECONDS = 60
FAST_FAIL_BACKOFF = [120, 300, 900, 1800]
# A runaway backstop, not a work schedule - the lesson Jacob's budget cost a
# day to learn. Project management is not deadline-dense in the way estimating
# is; a step is due on a date and the date does not move because he was slow.
DAILY_BUDGET_HOURS = float(os.environ.get("JOSEPH_DAY_HOURS", "6.0"))
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

ROTATE_CONTEXT = int(os.environ.get("JOSEPH_ROTATE_CONTEXT", "120000"))
SESSION_WARN_TOKENS = int(os.environ.get("JOSEPH_SESSION_WARN", "15000000"))
SESSION_KILL_TOKENS = int(os.environ.get("JOSEPH_SESSION_KILL", "40000000"))
CONTRACT_MAX_LINES = 200


def log(msg):
    line = "[%s] %s" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    os.makedirs(INBOX, exist_ok=True)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def load(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)


def env():
    out = {}
    for name in (".env.joseph", ".env.mary"):
        p = os.path.join(REPO, name)
        if not os.path.exists(p):
            continue
        for line in open(p, encoding="utf-8-sig"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                out.setdefault(k.strip(), v.strip())
    return out


def night_ok():
    try:
        if not budget.is_night():
            return True
        return budget.night_allowed()[0]
    except Exception:
        return True


def contract_file(key):
    return os.path.join(CONTRACT_DIR, "%s.md" % key)


def check_contract_file(key):
    """Same contract as the job and company files: bounded, states its position."""
    p = contract_file(key)
    if not os.path.exists(p):
        return ["data/contracts/%s.md does not exist - create it before working "
                "this job" % key]
    problems = []
    with open(p, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    if len(lines) > CONTRACT_MAX_LINES:
        problems.append("data/contracts/%s.md is %d lines (contract: %d) - archive "
                        "the history" % (key, len(lines), CONTRACT_MAX_LINES))
    head = "\n".join(lines[:40]).lower()
    if "## position" not in head and "where it stands" not in head:
        problems.append("data/contracts/%s.md does not state where the job stands "
                        "in the first 40 lines" % key)
    return problems


# ---------------------------------------------------------------- intake
def read_orders():
    out = []
    if not os.path.isdir(QUEUE):
        return out
    for name in sorted(os.listdir(QUEUE)):
        if not name.endswith(".json"):
            continue
        rec = load(os.path.join(QUEUE, name), None)
        if rec is None:
            log("UNREADABLE work order %s" % name)
            continue
        rec["_file"] = name
        out.append(rec)
    return out


def queue_work(cfg, state, cons):
    """Anything addressed to Joseph, plus the steps that have come due."""
    os.makedirs(QUEUE, exist_ok=True)
    added = 0

    import urllib.request
    import urllib.error

    def api(path):
        try:
            req = urllib.request.Request(
                cfg.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev") + path)
            req.add_header("x-mary-key", cfg.get("MARY_API_KEY", ""))
            req.add_header("user-agent", "JosephBridge/1.0")
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode() or "null")
        except Exception:
            return None

    for m in (api("/api/joseph/pending") or []):
        key = "hub-%s" % m["id"]
        if key in state["seen"]:
            continue
        save(os.path.join(QUEUE, "%s.json" % key), {
            "kind": "hub-message", "trusted": m["author"] in ("zac", "adam"),
            "id": m["id"], "author": m["author"], "body": m["body"],
            "context": m.get("context", ""), "created": m["created"]})
        state["seen"].append(key)
        added += 1
        log("QUEUED hub message %s from %s" % (m["id"], m["author"]))

    for m in (api("/api/botchat/pending?for=joseph") or []):
        key = "bot-%s" % m["id"]
        if key in state["seen"]:
            continue
        save(os.path.join(QUEUE, "%s.json" % key), {
            "kind": "bot-message", "trusted": False,
            "id": m["id"], "sender": m["sender"], "subject": m.get("subject", ""),
            "body": m["body"], "wants_reply": m.get("wants_reply", 0),
            "created": m["created"]})
        state["seen"].append(key)
        added += 1

    # A STEP GOING LATE IS THE WORK. Deterministic to spot, so it costs
    # nothing to notice - but deciding what to do when the survey has slipped
    # past the order dates is judgement, and that is what the session is for.
    today = dt.date.today().isoformat()
    for c in cons:
        try:
            b = crm_contract.board(c["key"])
        except Exception:
            continue
        if not b:
            continue
        late = [r for r in b.get("late", [])]
        if not late:
            continue
        key = "late-%s-%s" % (c["key"][:40], today)
        if key in state["seen"]:
            continue
        save(os.path.join(QUEUE, "%s.json" % key.replace("/", "_")), {
            "kind": "steps-late", "trusted": True, "author": "the checklist",
            "contract": c["key"],
            "subject": "%s - %d step(s) late" % (c.get("title") or c["key"], len(late)),
            "body": "These steps are past their date on %s:\n%s\n\nThe site date is "
                    "%s. Decide what actually has to move: some of these are still "
                    "achievable, some push the installation, and one of them may mean "
                    "telling the client."
                    % (c.get("title") or c["key"],
                       "\n".join("  - %s (due %s)" % (r["label"], r["due"]) for r in late),
                       c.get("site_date") or "not set"),
            "created": dt.datetime.now().isoformat(timespec="seconds")})
        state["seen"].append(key)
        added += 1
        log("QUEUED %d late step(s) on %s" % (len(late), c["key"]))

    state["seen"] = state["seen"][-500:]
    return added


def group_by_contract(orders, cons):
    groups = {}
    for o in orders:
        key, why = router.route(o, cons)
        o["_route_why"] = why
        groups.setdefault(key, []).append(o)
    return sorted(groups.items(), key=lambda kv: kv[1][0].get("created", ""))


def rotate_if_heavy(reg, key, rec):
    ctx = cost.context_size(rec["session_id"])
    retire, why = budget.should_retire(rec.get("started"), ctx, ROTATE_CONTEXT)
    if not retire:
        return False
    problems = check_contract_file(key) if key != router.DESK else []
    if problems:
        rec["file_warn"] = "; ".join(problems)
        router.save_registry(reg)
        log("  [%s] due to rotate at %s context tokens but its contract file is "
            "out of contract - not rotating. %s"
            % (key, "{:,}".format(ctx), rec["file_warn"]))
        return False
    old = rec["session_id"]
    rec["session_id"] = str(uuid.uuid4())
    rec["started"] = False
    rec["rotated_from"] = old
    rec["rotations"] = rec.get("rotations", 0) + 1
    router.save_registry(reg)
    log("  [%s] chat retired (%s) - starting fresh from data/contracts/%s.md"
        % (key, why, key))
    return True


def watch_session(proc, key, session_id, since, stop, cfg=None, title="", depth=0):
    """Kill a runaway, and tell the hub what he is doing while he does it.

    The only thing ticking during a session, so it is where the status comes
    from. Joseph reported none at all before this."""
    warned = False
    while not stop.wait(60):
        try:
            bot_status.write("joseph", "working", chat_key=key, depth=depth,
                             detail="working - new items queue behind this",
                             title=title, session_id=session_id, env=cfg or {})
        except Exception:
            pass
        try:
            spent = cost.session_cost(session_id, since)["context"]
        except Exception:
            continue
        if spent >= SESSION_KILL_TOKENS:
            log("  [%s] RUNAWAY - %s context tokens in one session. Killing it."
                % (key, "{:,}".format(spent)))
            try:
                proc.kill()
            except Exception:
                pass
            return
        if spent >= SESSION_WARN_TOKENS and not warned:
            warned = True
            log("  [%s] session has spent %s context tokens - watching"
                % (key, "{:,}".format(spent)))


def build_prompt(key, title, orders, first_run, reg, cons):
    lines = []
    if key == router.DESK:
        lines.append(
            ("You are Joseph Scott, Fenster Glazing's project manager. This conversation "
             "is your permanent DESK chat - anything that does not belong to one won job.\n\n"
             "One-off setup, do it now: read JOSEPH-SESSION.md. That is your manual and it "
             "is short."
             if first_run else
             "New work for your desk. This chat already holds your running history - use "
             "it, and do not re-read the manual unless something specific is missing."))
    else:
        c = next((x for x in cons if x["key"] == key), {})
        if first_run:
            lines.append(
                "You are Joseph Scott, Fenster Glazing's project manager. This conversation "
                "is the PERMANENT chat for ONE won job: %s. It will be resumed until that "
                "job is finished and paid for, so what you learn here you keep.\n\n"
                "One-off setup, do it now: read JOSEPH-SESSION.md, then "
                "data/contracts/%s.md if it exists - and create it to the contract in the "
                "manual if it does not. Then look at the job itself:\n"
                "  python scripts\\crm_contract.py --plan %s\n"
                "The site date is %s and every step counts backwards from it."
                % (title, key, c.get("site_date") or "NOT SET", c.get("site_date") or "not set"))
        else:
            lines.append(
                "New work on %s. This chat already holds this job's history - use it. Do "
                "NOT re-read the manual or the contract file unless something specific is "
                "missing; that is what this conversation is for." % title)

    lines.append("\nWORK ORDERS (full JSON in test-results\\joseph-inbox\\queue\\):")
    for o in orders[:12]:
        lines.append("  - %s: %s" % (o.get("kind", "?"),
                                     (o.get("subject") or o.get("body") or "")[:160].replace("\n", " ")))
        lines.append("    routed here because: %s" % o.get("_route_why", "?"))
    if len(orders) > 12:
        lines.append("  ... and %d more behind these." % (len(orders) - 12))

    warn = (reg["chats"].get(key) or {}).get("file_warn")
    if warn:
        lines.append(
            "\nCONTRACT FILE - fix this FIRST: %s. Keep data/contracts/%s.md under %d "
            "lines with the position stated up top. The next chat for this job is seeded "
            "from that file alone, and while it is broken this chat cannot rotate."
            % (warn, key, CONTRACT_MAX_LINES))

    note = budget.prompt_note("joseph:" + key, sends=False)
    if note:
        lines.append(note)
    lines.append(budget.WORK_STYLE)

    lines.append(
        "\nThe CRM is the record. Read it and write to it:\n"
        "  python scripts\\crm.py --lead <key>            what we quoted, and to whom\n"
        "  python -c \"import sys;sys.path.insert(0,'scripts');import crm_contract;"
        "print(crm_contract.board('<key>'))\"\n"
        "Tick a step when the evidence says it is done, with the evidence:\n"
        "  python -c \"import sys;sys.path.insert(0,'scripts');import crm;"
        "crm.task('contract','<key>','order_glass','Order the glass','joseph',"
        "done_at='YYYY-MM-DD',done_by='who said so')\"\n"
        "\nYou and the other two work independently. Commit ONLY the files you touched "
        "(never `git add -A`), and deploy the hub only through the deploy scripts.\n"
        "Close out: answer on the hub to anyone who wrote to you, move handled orders "
        "into %s, and update data/contracts/%s.md if the position moved." % (DONE, key))
    return "\n".join(lines)


_worker = [None]


def dispatch(cfg, state, cons):
    orders = read_orders()
    if not orders:
        return False
    if _worker[0] and _worker[0].is_alive():
        return False
    if time.time() < state.get("backoff_until", 0):
        return False
    now = time.time()
    ages = []
    for o in orders:
        try:
            ages.append(now - os.path.getmtime(os.path.join(QUEUE, o["_file"])))
        except OSError:
            ages.append(0)
    urgent = sum(1 for o in orders if o.get("trusted") or o.get("kind") == "hub-message")
    go, why = budget.ready_to_dispatch(ages, urgent)
    if not go:
        if state.get("_batch_why") != why:
            state["_batch_why"] = why
            log("BATCHING: %s" % why)
        return False
    state.pop("_batch_why", None)

    if not night_ok():
        if not state.get("_curfew_logged"):
            state["_curfew_logged"] = True
            log("HELD until 07:00 - overnight running is off. %d order(s) waiting."
                % len(orders))
        return False
    state.pop("_curfew_logged", None)

    spent = sum(r["seconds"] for r in state.get("runs", [])
                if r["at"] > time.time() - 86400) / 3600.0
    if spent >= DAILY_BUDGET_HOURS:
        log("HELD BACK by his own budget: %.2f of %.1f session-hours. %d waiting."
            % (spent, DAILY_BUDGET_HOURS, len(orders)))
        return False
    if not os.path.exists(CLAUDE):
        log("claude CLI not found at %s" % CLAUDE)
        return False

    reg = router.load_registry()
    router.chat(reg, router.DESK)
    groups = group_by_contract(orders, cons)
    if not groups:
        return False
    key, group = groups[0]
    rec = router.chat(reg, key)
    title = router.contract_title(cons, key)
    router.save_registry(reg)

    rotated = rotate_if_heavy(reg, key, rec)
    first_run = rotated or (not rec.get("started")
                            and not os.path.exists(cost.transcript(rec["session_id"])))
    session_id = rec["session_id"]
    prompt = build_prompt(key, title, group, first_run, reg, cons)

    with open(LOCK, "w") as fh:
        fh.write(str(os.getpid()))
    started = time.time()
    started_utc = dt.datetime.utcnow().isoformat()
    stop_watch = threading.Event()
    log("dispatch -> [%s] %s : %d order(s), %s"
        % (key, title, len(group), "NEW chat" if first_run else "resuming"))

    def run_session():
        try:
            cmd = [CLAUDE, "-p", prompt, "--dangerously-skip-permissions"]
            cmd += (["--session-id", session_id] if first_run else ["--resume", session_id])
            proc = subprocess.Popen(cmd, cwd=REPO, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True,
                                    encoding="utf-8", errors="replace",
                                    creationflags=NO_WINDOW)
            threading.Thread(target=watch_session,
                             args=(proc, key, session_id, started_utc, stop_watch,
                                   cfg, title, len(orders)),
                             daemon=True).start()
            out, err = proc.communicate(timeout=3600)
            took = time.time() - started
            state.setdefault("runs", []).append({"at": time.time(), "seconds": took})
            log("  [%s] session exit %s after %ds" % (key, proc.returncode, took))
            with open(os.path.join(INBOX, "last-session.txt"), "w", encoding="utf-8") as fh:
                fh.write((out or "")[-4000:] + "\n--- stderr ---\n" + (err or "")[-2000:])
            if proc.returncode == 0:
                rec["started"] = True
                rec["runs"] = rec.get("runs", 0) + 1
                rec["last_active"] = dt.datetime.now().isoformat(timespec="seconds")
                problems = check_contract_file(key) if key != router.DESK else []
                if problems:
                    rec["file_warn"] = "; ".join(problems)
                else:
                    rec.pop("file_warn", None)
                router.save_registry(reg)
                state["fails"] = 0
                state.pop("backoff_until", None)
            else:
                if first_run:
                    rec["started"] = False
                    router.save_registry(reg)
                if took < FAST_FAIL_SECONDS:
                    state["fails"] = state.get("fails", 0) + 1
                    wait = FAST_FAIL_BACKOFF[min(state["fails"] - 1, len(FAST_FAIL_BACKOFF) - 1)]
                    state["backoff_until"] = time.time() + wait
                    log("fast failure #%d - backing off %ds" % (state["fails"], wait))
        except subprocess.TimeoutExpired:
            log("session timed out after an hour")
        except Exception as e:
            state["fails"] = state.get("fails", 0) + 1
            wait = FAST_FAIL_BACKOFF[min(state["fails"] - 1, len(FAST_FAIL_BACKOFF) - 1)]
            state["backoff_until"] = time.time() + wait
            log("session failed: %s - backing off %ds" % (str(e)[:150], wait))
        finally:
            stop_watch.set()
            # Back to idle carrying his last thought - otherwise the card holds
            # "Working on ..." until the next session, which is a lie of omission.
            try:
                bot_status.write("joseph", "idle", depth=0,
                                 detail="finished - nothing queued",
                                 session_id=session_id, env=cfg)
            except Exception:
                pass
            try:
                budget.log_tokens("joseph:" + key, session_id, time.time() - started, started_utc)
            except Exception:
                pass
            try:
                os.remove(LOCK)
            except OSError:
                pass
            save(STATE, state)

    _worker[0] = threading.Thread(target=run_session, daemon=True)
    _worker[0].start()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    os.makedirs(QUEUE, exist_ok=True)
    os.makedirs(DONE, exist_ok=True)
    os.makedirs(CONTRACT_DIR, exist_ok=True)
    state = load(STATE, {"seen": [], "runs": [], "fails": 0})

    if args.status:
        print(json.dumps({
            "queue": len(read_orders()),
            "budget_hours": DAILY_BUDGET_HOURS,
            "session_running": os.path.exists(LOCK),
            "night_ok": night_ok(),
        }, indent=1))
        return 0

    if os.path.exists(PIDFILE):
        try:
            with open(PIDFILE) as fh:
                other = int((fh.read() or "0").strip() or 0)
            if other and other != os.getpid():
                os.kill(other, 0)
                log("bridge %d already running - standing down" % other)
                return 0
        except (OSError, ValueError):
            pass
    with open(PIDFILE, "w") as fh:
        fh.write(str(os.getpid()))

    cfg = env()
    log("JOSEPH bridge up (pid %d)" % os.getpid())
    while True:
        try:
            cons = router.contracts()
            queue_work(cfg, state, cons)
            dispatch(cfg, state, cons)
            save(STATE, state)
        except Exception as e:
            log("pass failed: %s" % str(e)[:200])
        if args.once:
            return 0
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())

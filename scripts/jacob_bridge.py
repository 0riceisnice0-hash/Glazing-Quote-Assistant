# -*- coding: utf-8 -*-
"""JACOB - the bridge. Gives him a thinking session when there is something
worth thinking about, and otherwise leaves him alone.

  python scripts/jacob_bridge.py            # run the loop
  python scripts/jacob_bridge.py --status
  python scripts/jacob_bridge.py --once     # one pass, for testing

What wakes him:
  - a message from Zac or Adam on the hub
  - a message from Mary on the bot line
  - new signals appearing in his mailboxes

What does NOT wake him: the daily intake. That is deterministic and runs in
`jacob_daily.py` for free. A session is only spent when something needs
judgement or writing.

MARY COMES FIRST. Her work has deadlines; his does not. If her bridge is
mid-session this one waits, and he has a smaller daily budget than her. An
agent that starves the estimator to go looking for leads is a bad trade.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(REPO, "test-results", "jacob-inbox")
QUEUE = os.path.join(INBOX, "queue")
DONE = os.path.join(INBOX, "processed")
STATE = os.path.join(REPO, "data", "jacob", "bridge-state.json")
LOG = os.path.join(INBOX, "bridge.log")
LOCK = os.path.join(INBOX, "session.lock")
PROMPT = os.path.join(REPO, "JACOB-SESSION.md")

POLL_SECONDS = 120
DAILY_BUDGET_HOURS = float(os.environ.get("JACOB_DAY_HOURS", "4.0"))  # less than Mary's 8; raised from 3 on 29/07 when the standing agenda gave him a real workload
MARY_LOCK = os.path.join(REPO, "test-results", "mary-inbox", "session.lock")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")


def log(msg):
    line = "[%s] %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    os.makedirs(INBOX, exist_ok=True)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (IOError, ValueError):
        return default


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=1)


def _read_env_file(path):
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8-sig"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _hub_keys(cfg):
    """The dashboard key and URL are shared infrastructure, not Jacob's own
    credentials, so they live in .env.mary. Fall back to it for those two
    values only - never for the Graph secrets, which must stay separate."""
    if not cfg.get("MARY_API_KEY") or not cfg.get("DASHBOARD_URL"):
        mary = _read_env_file(os.path.join(REPO, ".env.mary"))
        for k in ("MARY_API_KEY", "DASHBOARD_URL"):
            if not cfg.get(k) and mary.get(k):
                cfg[k] = mary[k]
    return cfg


def env():
    return _hub_keys(_read_env_file(os.path.join(REPO, ".env.jacob")))


def api(cfg, path, method="GET", payload=None):
    url = cfg.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev") + path
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(payload).encode() if payload is not None else None)
    req.add_header("x-mary-key", cfg["MARY_API_KEY"])
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "JacobBridge/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode() or "{}")
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
        return None


# ---------------------------------------------------------------- intake
def queue_work(cfg, state):
    """Pull anything addressed to Jacob into the queue. Returns how many."""
    os.makedirs(QUEUE, exist_ok=True)
    added = 0

    for m in (api(cfg, "/api/jacob/pending") or []):
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

    for m in (api(cfg, "/api/botchat/pending?for=jacob") or []):
        key = "bot-%s" % m["id"]
        if key in state["seen"]:
            continue
        save(os.path.join(QUEUE, "%s.json" % key), {
            "kind": "bot-message", "trusted": False,   # Mary is a colleague, not a boss
            "id": m["id"], "sender": m["sender"], "subject": m.get("subject", ""),
            "body": m["body"], "wants_reply": m.get("wants_reply", 0),
            "created": m["created"]})
        state["seen"].append(key)
        added += 1
        log("QUEUED message from Mary: %s" % (m.get("subject") or m["body"][:50]))

    state["seen"] = state["seen"][-500:]
    return added


def budget_spent(state):
    """Hours spent THIS WINDOW (07:00 to 07:00), not a rolling 24h.

    The rolling shape is the one Mary's budget abandoned, for the reason that
    played out on 29/07: Jacob sat all day at "3.0 of 3.0 used in 24h" with
    seven work orders queued, because the spend was the previous evening's.
    A night's work must not be able to block the following day."""
    now = time.localtime()
    start = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 7, 0, 0, 0, 0, -1))
    if time.time() < start:
        start -= 86400
    state["runs"] = [r for r in state.get("runs", []) if r["at"] > time.time() - 172800]
    return sum(r["seconds"] for r in state["runs"] if r["at"] >= start) / 3600.0


# An empty queue used to mean an idle bot, and on Mary's busy days he never
# ran at all - Zac, 29/07: "he's doing nothing rn i swear". A BDM with no
# mail still has a job: work the board. Every few quiet hours, if there is
# budget to spare and Mary is not working, the bridge hands him his own
# standing agenda as a work order.
AGENDA_EVERY = 4 * 3600
AGENDA_BUDGET_HEADROOM = 0.7    # keep the last 30% of budget for real messages
AGENDA = (
    "STANDING AGENDA from Zac (29/07): an empty inbox is not an empty day. Read "
    "data/knowledge/bd.md first. Then look at your own board (Today, Chasing, Leads, "
    "Companies) and ADVANCE one or two of the highest-value items properly rather than "
    "many badly. Good moves: verify a 'possible' lead so it stops needing a human; "
    "research a warm company properly into data/companies/<slug>.md (contract, contact, "
    "what to say); draft the next chase for anything past its date; check "
    "`python scripts/mary_recall.py --grep <company>` before asking anyone anything. "
    "If your intake or feeds look stale, run `python scripts/jacob_daily.py --deploy`. "
    "Close out as always: reply to nobody (this is your own time), update the board if "
    "it changed, and leave a one-line note on your job in the session record.")


def maybe_self_agenda(state):
    orders = [f for f in os.listdir(QUEUE) if f.endswith(".json")]
    if orders or (_worker[0] and _worker[0].is_alive()) or os.path.exists(MARY_LOCK):
        return
    hour = time.localtime().tm_hour
    if not 7 <= hour < 21:
        return
    if budget_spent(state) >= DAILY_BUDGET_HOURS * AGENDA_BUDGET_HEADROOM:
        return
    if time.time() - state.get("last_agenda", 0) < AGENDA_EVERY:
        return
    state["last_agenda"] = time.time()
    save(os.path.join(QUEUE, "agenda-%d.json" % int(time.time())), {
        "kind": "standing-agenda", "trusted": True, "author": "zac",
        "body": AGENDA, "created": time.strftime("%Y-%m-%dT%H:%M:%S")})
    log("QUEUED the standing agenda - quiet queue, budget to spare, Mary free")


_worker = [None]


def dispatch(cfg, state):
    orders = sorted(f for f in os.listdir(QUEUE) if f.endswith(".json"))
    if not orders:
        return False

    # Already working. Returning here rather than blocking is the whole point:
    # a message that arrives mid-session still gets queued for the next one.
    if _worker[0] and _worker[0].is_alive():
        return False

    if os.path.exists(MARY_LOCK):
        log("Mary is working - waiting. Her deadlines beat his leads.")
        return False

    spent = budget_spent(state)
    if spent >= DAILY_BUDGET_HOURS:
        log("HELD BACK: %.1f of %.1f session-hours used in 24h" % (spent, DAILY_BUDGET_HOURS))
        return False

    if not os.path.exists(CLAUDE):
        log("claude CLI not found at %s - cannot start a session" % CLAUDE)
        return False

    with open(LOCK, "w") as fh:
        fh.write(str(os.getpid()))
    started = time.time()
    log("dispatch -> %d order(s)" % len(orders))

    # Publish what he is doing to the hub's Live tab while he works. Reuses
    # Mary's transcript tailer read-only - Claude Code already writes every
    # session to a .jsonl as it happens, so nothing about how the session runs
    # has to change. Best effort on a daemon thread: this must never be able
    # to interfere with the work itself.
    stop_feed = threading.Event()
    fails = [0]

    def publish_feed():
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            import mary_activity as act
        except ImportError:
            return
        while not stop_feed.is_set():
            try:
                sid = act.newest_session(max_age=900)
                if sid:
                    events = act.feed(sid)
                    if events:
                        payload = json.dumps({"chat": "jacob", "title": "Business development",
                                              "events": events}).encode()
                        req = urllib.request.Request(
                            cfg.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
                            + "/api/jacob/activity", data=payload, method="POST")
                        req.add_header("x-mary-key", cfg["MARY_API_KEY"])
                        req.add_header("content-type", "application/json")
                        req.add_header("user-agent", "JacobBridge/1.0")
                        urllib.request.urlopen(req, timeout=15).read()
            except Exception as e:
                # Best effort, but say so. Swallowing this is why a feed that
                # died mid-session left no trace and the Live tab quietly
                # showed the previous session's steps for an hour.
                fails[0] += 1
                if fails[0] in (1, 5, 20):
                    log("live feed publish failing (%d): %s" % (fails[0], str(e)[:120]))
            stop_feed.wait(6)

    threading.Thread(target=publish_feed, daemon=True).start()

    prompt = ("Read %s and follow it. Your work orders are the JSON files in %s. "
              "Handle them, reply on the hub to anyone who wrote to you, then move "
              "each order into %s and rebuild your board."
              % (PROMPT, QUEUE, DONE))
    def run_session():
        try:
            # Same launch as mary_bridge.py, approved by Zac 28/07. An
            # unattended session that has to ask for approval cannot run a
            # single command - the first attempt spent its entire life being
            # refused Bash. The containment that matters for Jacob is outward
            # and sits elsewhere: no send path in any script, an Exchange
            # transport rule rejecting external mail from jacob@, and a read
            # scope of four mailboxes enforced by access policy.
            p = subprocess.run(
                [CLAUDE, "-p", prompt, "--dangerously-skip-permissions"],
                cwd=REPO, capture_output=True, encoding="utf-8",
                errors="replace", timeout=3600)
            took = time.time() - started
            state.setdefault("runs", []).append({"at": time.time(), "seconds": took})
            log("session exit %s after %ds" % (p.returncode, took))
            with open(os.path.join(INBOX, "last-session.txt"), "w", encoding="utf-8") as fh:
                fh.write((p.stdout or "")[-4000:] + "\n--- stderr ---\n"
                         + (p.stderr or "")[-2000:])
            # A session that dies in seconds is a usage limit or a broken CLI.
            if p.returncode != 0 and took < 60:
                state["fails"] = state.get("fails", 0) + 1
                log("fast failure #%d" % state["fails"])
            else:
                state["fails"] = 0
        except subprocess.TimeoutExpired:
            log("session timed out after an hour")
        except Exception as e:
            log("session failed: %s" % str(e)[:150])
        finally:
            stop_feed.set()
            try:
                os.remove(LOCK)
            except OSError:
                pass
            # The main loop saves state too, but it is not waiting on this
            # thread any more, so the run has to record itself.
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
    state = load(STATE, {"seen": [], "runs": [], "fails": 0})

    if args.status:
        pend = len([f for f in os.listdir(QUEUE) if f.endswith(".json")])
        print(json.dumps({
            "queue": pend,
            "budget_used_hours": round(budget_spent(state), 2),
            "budget_hours": DAILY_BUDGET_HOURS,
            "session_running": os.path.exists(LOCK),
            "mary_working": os.path.exists(MARY_LOCK),
        }, indent=1))
        return 0

    # Exactly one bridge - same lesson Mary's learned on 28/07 when two of
    # hers double-queued every dashboard message.
    pidfile = os.path.join(INBOX, "bridge.pid")
    if os.path.exists(pidfile):
        try:
            with open(pidfile) as fh:
                other = int((fh.read() or "0").strip() or 0)
            if other and other != os.getpid():
                os.kill(other, 0)
                log("bridge %d already running - standing down" % other)
                return 0
        except (OSError, ValueError):
            pass
    with open(pidfile, "w") as fh:
        fh.write(str(os.getpid()))

    cfg = env()
    log("JACOB bridge up (pid %d)" % os.getpid())
    while True:
        try:
            queue_work(cfg, state)
            maybe_self_agenda(state)
            dispatch(cfg, state)
            save(STATE, state)
        except Exception as e:                       # never die on one bad pass
            log("pass failed: %s" % str(e)[:200])
        if args.once:
            return 0
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())

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
DAILY_BUDGET_HOURS = 3.0        # deliberately less than Mary's
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


def env():
    e = {}
    for line in open(os.path.join(REPO, ".env.jacob"), encoding="utf-8-sig"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip()
    return e


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
    cutoff = time.time() - 86400
    state["runs"] = [r for r in state.get("runs", []) if r["at"] > cutoff]
    return sum(r["seconds"] for r in state["runs"]) / 3600.0


def dispatch(state):
    orders = sorted(f for f in os.listdir(QUEUE) if f.endswith(".json"))
    if not orders:
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

    prompt = ("Read %s and follow it. Your work orders are the JSON files in %s. "
              "Handle them, reply on the hub to anyone who wrote to you, then move "
              "each order into %s and rebuild your board."
              % (PROMPT, QUEUE, DONE))
    try:
        p = subprocess.run(
            [CLAUDE, "-p", prompt, "--permission-mode", "acceptEdits"],
            cwd=REPO, capture_output=True, encoding="utf-8", errors="replace",
            timeout=3600)
        took = time.time() - started
        state.setdefault("runs", []).append({"at": time.time(), "seconds": took})
        log("session exit %s after %ds" % (p.returncode, took))
        with open(os.path.join(INBOX, "last-session.txt"), "w", encoding="utf-8") as fh:
            fh.write((p.stdout or "")[-4000:] + "\n--- stderr ---\n" + (p.stderr or "")[-2000:])
        # A session that dies in seconds is a usage limit or a broken CLI, not work.
        if p.returncode != 0 and took < 60:
            state["fails"] = state.get("fails", 0) + 1
            log("fast failure #%d" % state["fails"])
        else:
            state["fails"] = 0
    except subprocess.TimeoutExpired:
        log("session timed out after an hour")
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass
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

    cfg = env()
    log("JACOB bridge up (pid %d)" % os.getpid())
    while True:
        try:
            queue_work(cfg, state)
            dispatch(state)
            save(STATE, state)
        except Exception as e:                       # never die on one bad pass
            log("pass failed: %s" % str(e)[:200])
        if args.once:
            return 0
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())

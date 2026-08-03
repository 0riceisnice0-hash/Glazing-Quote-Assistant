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
import re
import subprocess
import sys
import time
import threading
import urllib.error
import urllib.request
import uuid
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
# A failed Claude launch must not turn the poll interval into a retry interval.
# This happened when the Claude allowance ran out on 30/07/2026: the queue
# remained non-empty and the bridge opened a failing console process every two
# minutes. Back off progressively, matching Mary's bridge.
FAST_FAIL_SECONDS = 60
FAST_FAIL_BACKOFF = [120, 300, 900, 1800]
# 3 -> 4 -> 12 on 29/07. The budget is a RUNAWAY BACKSTOP, not a work schedule,
# and at 4.0 it had become the schedule: he spent it by 20:14 and then logged
# "HELD BACK" every two minutes for the rest of the evening with three of
# ADAM'S OWN instructions sitting unworked in the queue - including "spend the
# night working on this if you have to, I want a full list in the morning"
# (hub-78, 19:36). Zac, dashmsg-95: "he's hit some kind of hard limit, can you
# increase it? He doesn't have enough up time!" Twelve hours is high enough
# that it never becomes the schedule again and still stops a loop dead.
DAILY_BUDGET_HOURS = float(os.environ.get("JACOB_DAY_HOURS", "12.0"))
MARY_LOCK = os.path.join(REPO, "test-results", "mary-inbox", "session.lock")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")
# pythonw hides the bridge itself, but a console-subsystem child such as
# claude.exe can still create a window unless Windows is told not to make one.
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


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

    # The QUOTE HANDOVER, structural (Zac, 29/07: "once mary knows we have
    # sent out a quote, she should hand it over to jacob" - without the two
    # of them having a conversation about it). Mary records quote_issued in
    # the ledger at close-out; it arrives here as a work order. No botchat,
    # no prose, no session spent on Mary's side.
    try:
        import mary_ledger
        for e in mary_ledger.iter_events():
            if e.get("kind") != "quote_issued":
                continue
            key = "handover-%s" % (e.get("ref") or "")[:80]
            if not e.get("ref") or key in state["seen"]:
                continue
            save(os.path.join(QUEUE, "%s.json" % re.sub(r"[^\w.-]", "_", key)), {
                "kind": "quote-handover", "trusted": True, "author": "mary-ledger",
                "body": ("A quote has been ISSUED and is now yours to track: %s. "
                         "Add it to your chasing register (data/jacob/ + the board), "
                         "set the chase date, and say nothing to anyone - this is a "
                         "handover, not a conversation." % e.get("summary", "")),
                "ledger_ref": e.get("ref"), "job": e.get("job"),
                "created": e.get("ts", "")})
            state["seen"].append(key)
            added += 1
            log("QUEUED quote handover from the ledger: %s" % e.get("summary", "")[:70])
    except Exception as e:  # noqa: BLE001 - the ledger must never break intake
        log("ledger handover scan failed (harmless): %s" % str(e)[:100])

    state["seen"] = state["seen"][-500:]
    publish_queue(cfg, state)
    return added


_qsig = [None]


def publish_queue(cfg, state):
    """The queue and the last kick, visible on the hub's Queue tab. Five FYI
    messages sat here invisibly on 29/07 until Zac asked what they were."""
    items = []
    for f in sorted(os.listdir(QUEUE)):
        if not f.endswith(".json"):
            continue
        w = load(os.path.join(QUEUE, f), {})
        items.append({"file": f, "mailbox": w.get("kind", "?"),
                      "from": str(w.get("author") or w.get("sender") or "")[:80],
                      "subject": (w.get("subject") or (w.get("body") or "")[:110])[:160],
                      "context": (w.get("context") or "")[:60],
                      "route": "jacob", "why": w.get("kind", ""),
                      "body": (w.get("body") or "")[:1500],
                      "received": w.get("created", "")})
    # WHY NOTHING IS RUNNING, on the page where somebody asks that. Until now a
    # held-back bot said so only in bridge.log: 40 identical lines to a file
    # nobody reads, while the hub showed three orders waiting and a last_kick
    # from 19:26 and no reason. Zac had to guess - "think he's hit some hit of
    # hard limit" (dashmsg-95). A stalled bot must say that it is stalled.
    used = budget_spent(state)
    running = os.path.exists(LOCK)
    held = bool(items) and not running and used >= DAILY_BUDGET_HOURS
    budget = {"used_hours": round(used, 2), "of_hours": DAILY_BUDGET_HOURS,
              "resets": "07:00", "session_running": running, "held": held,
              "note": ("Held back by the bridge's own session budget - not an "
                       "external limit. It lifts at 07:00, or raise "
                       "DAILY_BUDGET_HOURS in scripts/jacob_bridge.py and "
                       "restart the bridge (the value is read at import)."
                       if held else "")}
    sig = (tuple(i["file"] for i in items), (state.get("last_kick") or {}).get("at"),
           held, running, round(used, 1))
    if sig == _qsig[0]:
        return
    if api(cfg, "/api/jacob/queue", "POST",
           {"items": items, "last_kick": state.get("last_kick"),
            "budget": budget}) is not None:
        _qsig[0] = sig


def night_ok():
    """May a session start right now? One curfew, defined in mary_budget."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import mary_budget
        if not mary_budget.is_night():
            return True
        return mary_budget.night_allowed()[0]
    except Exception:
        return True      # never let a missing import stop him working by day


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
# Every hour, not every four (29/07). Four hours between wakes meant that
# "there is budget and nothing in the queue" produced ~25 minutes of work in
# every four - which is not a working day, it is a bot that is allowed to work
# and mostly does not. The budget above is what bounds the total; this only
# decides how often he gets the chance.
AGENDA_EVERY = 3600
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
    # The MARY_LOCK test came out on 29/07 with the rest of the yield-to-Mary
    # rule (Zac: "mary and jacob should be free to work, ignoring what the
    # other one is currently doing"). dispatch() lost its copy and said so;
    # this one survived, so every agenda window that happened to land while
    # Mary held her lock was skipped - and she is an eight-hour bot.
    if orders or (_worker[0] and _worker[0].is_alive()):
        return
    # The old 07:00-21:00 curfew came off on 29/07 because it made Adam's own
    # "spend the night on this if you have to" (hub-78) structurally
    # impossible. It is back on 03/08 for a different reason, and with a
    # different shape: the curfew is now shared, it covers real work orders as
    # well as the agenda, and Adam can lift it for a night with
    # --allow-tonight. What is NOT coming back is self-generated agenda work at
    # 03:00 - that was 57% of the bill and nobody asked for it.
    if not night_ok():
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

    backoff_until = state.get("backoff_until", 0)
    if time.time() < backoff_until:
        return False

    # The overnight curfew, shared with Mary so there is one switch, not two.
    # 57% of all bot spend was falling between 22:00 and 07:00 and his standing
    # agenda ran hourly right through it. Intake carries on; only the sessions
    # stop, so 07:00 starts with an accurate queue.
    if not night_ok():
        if not state.get("_curfew_logged"):
            state["_curfew_logged"] = True
            log("HELD until 07:00 - overnight running is off. %d order(s) waiting."
                % len(orders))
        return False
    state.pop("_curfew_logged", None)

    # No yield to Mary any more (Zac, 29/07: "mary and jacob should be free
    # to work, ignoring what the other one is currently doing"). The yield
    # existed to protect two genuinely shared things - the git index and the
    # Pages deploy - and serialising whole bots to protect two files was the
    # wrong tool. Deploys now take a cross-process lock in the deploy scripts
    # themselves, and commits follow the "only the files you touched, retry
    # on index.lock" rule in both manuals. The bots are colleagues with their
    # own desks, not a queue for one chair.

    spent = budget_spent(state)
    if spent >= DAILY_BUDGET_HOURS:
        # "in 24h" was wrong and it cost real confusion: the window is 07:00 to
        # 07:00 (see budget_spent), and reading "24h" is what made this look
        # like an external usage limit rather than our own number. Say which
        # limit it is and when it lifts.
        log("HELD BACK by jacob_bridge's OWN budget: %.2f of %.1f session-hours "
            "used since 07:00; resets 07:00. %d order(s) waiting."
            % (spent, DAILY_BUDGET_HOURS, len(orders)))
        return False

    if not os.path.exists(CLAUDE):
        log("claude CLI not found at %s - cannot start a session" % CLAUDE)
        return False

    with open(LOCK, "w") as fh:
        fh.write(str(os.getpid()))
    started = time.time()
    # His own session identity. Without --session-id the transcript was an
    # anonymous file in the folder BOTH bots write to, and the live feed
    # tailed "the newest one" - which, whenever Mary was also working, was
    # hers. Jacob's Live tab showed Mary's steps (Zac spotted it, 29/07).
    session_id = str(uuid.uuid4())
    log("dispatch -> %d order(s) (session %s)" % (len(orders), session_id[:8]))
    # What kicked this session off - order summaries plus the actual prompt.
    heads = []
    for f in orders[:12]:
        w = load(os.path.join(QUEUE, f), {})
        heads.append("%s: %s - %s" % (w.get("kind", "?"),
                                      w.get("author") or w.get("sender") or "?",
                                      (w.get("subject") or w.get("body") or "")[:100]))
    state["last_kick"] = {"chat": "jacob", "title": "Business development",
                          "at": datetime.now().isoformat(timespec="seconds"),
                          "orders": heads, "session_id": session_id}

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
                # HIS transcript by id, never "the newest in the folder" -
                # the folder is shared with Mary and the newest was often hers.
                if session_id:
                    events = act.feed(session_id)
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
    prompt += ("\n\nYou and Mary work independently and may be running at the same time. "
               "Two rules that make that safe: git-commit ONLY the files you touched "
               "(never `git add -A`; if the index is locked, wait a few seconds and "
               "retry), and deploy the hub only through the deploy scripts - they take "
               "the shared deploy lock for you.")
    state["last_kick"]["prompt"] = prompt[:8000]
    publish_queue(cfg, state)
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
                [CLAUDE, "-p", prompt, "--dangerously-skip-permissions",
                 "--session-id", session_id],
                cwd=REPO, capture_output=True, encoding="utf-8",
                errors="replace", timeout=3600, creationflags=NO_WINDOW)
            took = time.time() - started
            state.setdefault("runs", []).append({"at": time.time(), "seconds": took})
            log("session exit %s after %ds" % (p.returncode, took))
            with open(os.path.join(INBOX, "last-session.txt"), "w", encoding="utf-8") as fh:
                fh.write((p.stdout or "")[-4000:] + "\n--- stderr ---\n"
                         + (p.stderr or "")[-2000:])
            # A session that dies in seconds is a usage limit or a broken CLI.
            if p.returncode != 0 and took < FAST_FAIL_SECONDS:
                state["fails"] = state.get("fails", 0) + 1
                wait = FAST_FAIL_BACKOFF[min(state["fails"] - 1,
                                             len(FAST_FAIL_BACKOFF) - 1)]
                state["backoff_until"] = time.time() + wait
                log("fast failure #%d - backing off %ds"
                    % (state["fails"], wait))
            else:
                state["fails"] = 0
                state.pop("backoff_until", None)
        except subprocess.TimeoutExpired:
            log("session timed out after an hour")
        except Exception as e:
            state["fails"] = state.get("fails", 0) + 1
            wait = FAST_FAIL_BACKOFF[min(state["fails"] - 1,
                                         len(FAST_FAIL_BACKOFF) - 1)]
            state["backoff_until"] = time.time() + wait
            log("session failed: %s - backing off %ds"
                % (str(e)[:150], wait))
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

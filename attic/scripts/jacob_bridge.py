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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jacob_router as router          # noqa: E402 - needs the path above
import bot_status                      # noqa: E402
import crm                             # noqa: E402
import mary_cost as cost               # noqa: E402
import mary_jobfile as jobfile         # noqa: E402
import mary_budget as budget           # noqa: E402

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

# Same cost architecture as Mary's, and for the same reason - his sessions were
# not measured at all until now. Rotate a chat when the context it would carry
# gets expensive. The figure is shared now (mary_budget.ROTATE_CONTEXT) because
# it had drifted three ways - 150k here, 120k for him and Joseph, and preflight
# hardcoding its own.
ROTATE_CONTEXT = int(os.environ.get("JACOB_ROTATE_CONTEXT", str(budget.ROTATE_CONTEXT)))
SESSION_WARN_TOKENS = int(os.environ.get("JACOB_SESSION_WARN", "15000000"))
SESSION_KILL_TOKENS = int(os.environ.get("JACOB_SESSION_KILL", "40000000"))


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


def read_orders():
    """Every queued work order, oldest first, with its filename attached."""
    out = []
    for name in sorted(os.listdir(QUEUE)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(QUEUE, name)
        rec = load(path, None)
        if rec is None:
            log("UNREADABLE work order %s" % name)
            continue
        rec["_file"] = name
        rec["_path"] = path
        out.append(rec)
    return out


def group_by_company(orders, reg):
    """Route every order, then group by chat, oldest group first."""
    groups = {}
    for o in orders:
        key, why = router.route(o, reg)
        o["_route_why"] = why
        groups.setdefault(key, []).append(o)
    return sorted(groups.items(), key=lambda kv: kv[1][0].get("created", ""))


def rotate_if_heavy(reg, key, rec):
    """Retire a chat that has finished its sitting, or is carrying too much.

    The rule is shared - see mary_budget.should_retire - because it drifted the
    moment it was not. Gated on the company file either way: retiring into an
    out-of-contract file does not save tokens, it moves them and loses the
    relationship.
    """
    ctx = cost.context_size(rec["session_id"])
    retire, why = budget.should_retire(rec.get("started"), ctx, ROTATE_CONTEXT)
    if not retire:
        return False
    problems = jobfile.check_company(key) if key != router.DESK else []
    if problems:
        rec["file_warn"] = "; ".join(problems)
        router.save_registry(reg)
        log("  [%s] due to rotate at %s context tokens but its company file is out "
            "of contract - not rotating. %s"
            % (key, "{:,}".format(ctx), rec["file_warn"]))
        return False
    old = rec["session_id"]
    rec["session_id"] = str(uuid.uuid4())
    rec["started"] = False
    rec["rotated_from"] = old
    rec["rotated_at"] = datetime.now().isoformat(timespec="seconds")
    rec["rotations"] = rec.get("rotations", 0) + 1
    router.save_registry(reg)
    log("  [%s] chat retired (%s) - starting fresh from data/companies/%s.md"
        % (key, why, key))
    return True


def build_prompt(key, title, orders, first_run, reg):
    """What wakes one of his chats. Lean on resume, seeded on a fresh start."""
    lines = []
    if key == router.DESK:
        if first_run:
            lines.append(
                "You are Jacob Wright, Fenster Glazing's business development manager. This "
                "conversation is your permanent DESK chat - the front desk. It is resumed for "
                "anything that does not belong to a company chat, so treat it as your running "
                "log of what is arriving.\n\n"
                "One-off setup, do it now: read JACOB-SESSION.md (your manual), then "
                "data/knowledge/bd.md (what you know about how Fenster wins work). "
                "data/jacob/README.md tells you where each of your data files comes from and "
                "what it cannot tell you.")
        else:
            lines.append(
                "New work for your desk. This chat already holds your running history - use it. "
                "Do NOT re-read your manual or bd.md unless something specific is missing; that "
                "is what this conversation is for.")
        lines.append(
            "\nIf any of this belongs to ONE company you deal with, do not work it here. Open "
            "or name that company's chat instead:\n"
            "  python scripts\\jacob_router.py --add-company <key> --name \"...\" "
            "--domains <domain> --match \"...\"\n"
            "then set the route on the work order and leave it in the queue - the bridge will "
            "wake that chat with it. A company chat REMEMBERS; the desk does not.")
    else:
        comp = reg["companies"].get(key, {})
        if first_run:
            lines.append(
                "You are Jacob Wright, Fenster Glazing's business development manager. This "
                "conversation is the PERMANENT chat for ONE company: %s. It will be resumed "
                "for every future piece of work on this relationship, so what you learn here "
                "you keep.\n\n"
                "One-off setup, do it now: read JACOB-SESSION.md, then "
                "data/companies/%s.md - that file is the distilled position on this "
                "relationship. For recent history run: python scripts\\mary_recall.py "
                "--grep \"%s\" --days 30. Do NOT read bd.md end to end unless the company "
                "file leaves a specific gap, and if it does, fix the company file so the next "
                "chat is not missing it too."
                % (title, key, comp.get("name", title)))
        else:
            lines.append(
                "New work on %s. This chat already holds this relationship's history - use it. "
                "Do NOT re-read your manual or the company file unless something specific is "
                "missing; that is what this conversation is for." % title)

    lines.append("\nWORK ORDERS (full JSON in test-results\\jacob-inbox\\queue\\):")
    for o in orders[:12]:
        lines.append("  - %s: %s - %s"
                     % (o.get("kind", "?"), o.get("author") or o.get("sender") or "?",
                        (o.get("subject") or o.get("body") or "")[:140].replace("\n", " ")))
        lines.append("    routed here because: %s" % o.get("_route_why", "?"))
    if len(orders) > 12:
        lines.append("  ... and %d more in the queue behind these." % (len(orders) - 12))

    rec = reg["chats"].get(key) or {}
    warn = rec.get("file_warn")
    if warn:
        lines.append(
            "\nCOMPANY FILE CONTRACT - fix this FIRST, before the work orders: %s. Keep "
            "data/companies/%s.md under %d lines with a '## Position' heading up top. The next "
            "chat for this company is seeded from that file alone; every line of bloat is a tax "
            "on it, and while it is broken this chat cannot rotate."
            % (warn, key, jobfile.COMPANY_MAX_LINES))

    # Cost only. He has no send path, so Mary's email and request evidence is
    # not his to answer for.
    note = budget.prompt_note("jacob:" + key, sends=False)
    if note:
        lines.append(note)
    lines.append(budget.WORK_STYLE)

    lines.append(
        "\nTHE CRM IS THE RECORD. Before you ask anyone anything, look:\n"
        "  python scripts\\crm.py --today            the calls due, and the backlog by value\n"
        "  python scripts\\crm.py --company %s\n"
        "  python scripts\\crm.py --lead <key>       one job: quotes, notes, dates, history\n"
        "Write back what you learn - a chase with no record is a chase somebody repeats:\n"
        "  python -c \"import sys;sys.path.insert(0,'scripts');import crm;"
        "crm.lead('<key>','jacob',why='...',next_action='...',next_action_date='YYYY-MM-DD')\"\n"
        "  ...and crm.note('lead','<key>','what they said','jacob',source='call')\n"
        "Stages %s are yours. Everything before quote_sent is Mary's - do not move those."
        % (key, ", ".join(crm.JACOB_STAGES)))

    lines.append(
        "\nYou and Mary work independently and may be running at the same time. Two rules that "
        "make that safe: git-commit ONLY the files you touched (never `git add -A`; if the index "
        "is locked, wait a few seconds and retry), and deploy the hub only through the deploy "
        "scripts - they take the shared deploy lock for you.\n"
        "Close out as always: reply on the hub to anyone who wrote to you, move each handled "
        "order into %s, update data/companies/%s.md if the position moved, and rebuild your "
        "board." % (DONE, key))

    # HOW TO WRITE TO ADAM. Zac, 04/08: "the AI's are not consise, they waffle
    # so much." Measured the same day: Jacob's median hub message is 2,864
    # characters and his longest is exactly 8,000 - the API ceiling - so he is
    # writing until something stops him.
    #
    # This is not a token problem. All the prose from all three bots is 2.9% of
    # what a session costs, so shortening it saves nothing measurable. It is a
    # READ problem: Adam gets these on a phone between site visits, and a
    # five-hundred-word wall is one he will skim or skip, which makes the whole
    # message worth nothing however right it is.
    #
    # So the limit is on the MESSAGE, never on the thinking or the file behind
    # it. Do the full work, write it down where it belongs, and send the part a
    # person has to act on.
    # YOU OWN THIS REPO. Zac, 04/08, on JAC-23: "he WAS failing to think. why
    # didn't he MAKE the mechanism??????????? these bots can write code in
    # their own repo, if there is an error they should fix it."
    #
    # He is right and the cause is here, not in Jacob. A work order for Uni
    # Assist landed in the Stepnell chat. Jacob worked out correctly that it
    # was not his, that it was time-critical and that it was a win - and then
    # raised a decision, because no tool exists to hand work to another bot or
    # push it back to the front desk. Only the front desk writes into a queue.
    #
    # He had Bash, Write and Edit the whole time. He could have written that
    # tool in ten minutes and used it. He did not, because nothing in his
    # prompt or his manual ever said the repo was his to change - checked, and
    # the phrase appears zero times in JACOB-PROCESS.md and zero times in
    # JOSEPH-SESSION.md. He was behaving exactly as instructed. So instruct
    # differently.
    lines.append(
        "\nYOU OWN THIS REPO, NOT JUST THE WORK IN IT. If the tool you need does not "
        "exist, WRITE IT - do not raise a decision asking somebody else to. Build it, "
        "test it on the real case in front of you, commit it, then use it, in this same "
        "session. A missing mechanism is a bug in your workshop and you are the one "
        "standing in it.\n"
        "Raise a decision ONLY for what a human alone can answer - a price, a date, "
        "what a client meant, whether we bid. Never for something you could have built.\n"
        "SIZE IS NOT A REASON TO STOP. Zac, 04/08: 'ai bots have no concept of how long "
        "it takes to make something - today we have achieved what you would assume would "
        "take a week.' Do not weigh a job in hours and talk yourself out of it. If it "
        "needs building, build it.\n"
        "What DOES stop you is blast radius, not size: ask first if the change would "
        "alter how another bot behaves, or touch the spending and curfew rules in "
        "mary_budget.py. Otherwise - commit only the files you touched, run the thing "
        "before you commit it, and say plainly what you changed and why.")

    # YOUR OWN TOOLS, so you never spend a turn asking them what they do.
    # Measured 04/08: 21 of Jacob's 295 shell calls were `--help`, and TEN of
    # those were jacob_reply - the tool he uses in literally every session. A
    # --help costs a whole context re-send to be told something that fits in
    # four lines, so the four lines live here.
    lines.append(
        "\nYOUR TOOLS - the flags, so you never need --help:\n"
        "  jacob_reply.py --pending | --reply-to <id> --body-file <f> [--context <c>]\n"
        "                 --mark-seen <ids> | --ask <REF> --title <t> --why <w> "
        "--needs <n> --option <o>  (repeat --option)\n"
        "  bot_chat.py --as jacob --pending | --to mary --body-file <f> --subject <s> "
        "[--wants-reply]\n"
        "  crm.py --lead <key> | --company <key>   crm_contract.py --plan <date> | --open <key>\n"
        "  mary_recall.py --grep <term> [--days N]   jacob_daily.py --deploy\n"
        "Bodies go in a file under scratchpad/ and are passed with --body-file, never inline.")

    lines.append(
        "\nWRITING TO ADAM OR ZAC. First line = the decision, the number, or the question. "
        "Then at most a short paragraph of why. Aim under 800 characters and never pad to "
        "fill: if you can say it in two lines, send two lines. He reads these on a phone "
        "between site visits, so a long message is a skimmed one. The detail belongs in "
        "data/companies/<slug>.md or on your board - say which, and he will look if he "
        "wants it. Never send a table or a list of more than five rows on the hub. "
        "This limits what you SEND, not what you work out - the file behind it should be "
        "as thorough as the job deserves.")
    return "\n".join(lines)


def watch_session(proc, key, session_id, since, stop, cfg=None, title="", depth=0):
    """Kill a session that is looping. Runs beside the work, never in its way.

    It is also the only thing ticking while a session runs, so it is where the
    hub gets told what Jacob is doing. He reported no status at all before
    this - his card sat on "Live" through a forty-minute session.
    """
    warned = False
    while not stop.wait(60):
        # Publish first: a session that is about to be killed for looping is
        # exactly the one somebody wants to see the last thought of.
        try:
            bot_status.write("jacob", "working", chat_key=key, depth=depth,
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

    # LET THE WORK PILE UP - the shared rule, see mary_budget.ready_to_dispatch.
    # A run costs the same whether it handles one message or eight.
    now = time.time()
    ages, urgent = [], 0
    for f in orders:
        try:
            ages.append(now - os.path.getmtime(os.path.join(QUEUE, f)))
        except OSError:
            ages.append(0)
        w = load(os.path.join(QUEUE, f), {})
        if w.get("trusted") or w.get("kind") == "hub-message":
            urgent += 1
    go, why = budget.ready_to_dispatch(ages, urgent)
    if not go:
        if state.get("_batch_why") != why:
            state["_batch_why"] = why
            log("BATCHING: %s" % why)
        return False
    state.pop("_batch_why", None)

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

    # ONE CHAT PER COMPANY, RESUMED - the whole point of P2. He used to mint a
    # fresh uuid4 here on every dispatch, so all 218 of his runs started cold
    # and re-derived the relationship from files. The conversation IS the
    # memory now, exactly as it is for Mary's jobs.
    #
    # Routing happens BEFORE the lock is taken: a work order that vanishes
    # between the listdir above and this read would otherwise leave the lock
    # file behind and stop him working until somebody deleted it by hand.
    reg = router.load_registry()
    router.chat(reg, router.DESK)
    groups = group_by_company(read_orders(), reg)
    if not groups:
        return False
    key, group = groups[0]

    with open(LOCK, "w") as fh:
        fh.write(str(os.getpid()))
    started = time.time()
    rec = router.chat(reg, key)
    title = router.company_title(reg, key)
    router.save_registry(reg)

    rotated = rotate_if_heavy(reg, key, rec)
    first_run = rotated or (not rec.get("started")
                            and not os.path.exists(cost.transcript(rec["session_id"])))
    session_id = rec["session_id"]
    prompt = build_prompt(key, title, group, first_run, reg)

    log("dispatch -> [%s] %s : %d order(s), %s (session %s)"
        % (key, title, len(group), "NEW chat" if first_run else "resuming chat",
           session_id[:8]))
    heads = ["%s: %s - %s" % (w.get("kind", "?"),
                              w.get("author") or w.get("sender") or "?",
                              (w.get("subject") or w.get("body") or "")[:100])
             for w in group[:12]]
    state["last_kick"] = {"chat": key, "title": title,
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

    state["last_kick"]["prompt"] = prompt[:8000]
    publish_queue(cfg, state)
    # Where this run starts in the transcript. A resumed chat appends to the
    # same file, so the cost of THIS run is the usage recorded after this
    # moment - and transcript timestamps are UTC, so this must be too.
    started_utc = datetime.utcnow().isoformat()
    stop_watch = threading.Event()

    def run_session():
        try:
            # Same launch as mary_bridge.py, approved by Zac 28/07. An
            # unattended session that has to ask for approval cannot run a
            # single command - the first attempt spent its entire life being
            # refused Bash. The containment that matters for Jacob is outward
            # and sits elsewhere: no send path in any script, an Exchange
            # transport rule rejecting external mail from jacob@, and a read
            # scope of four mailboxes enforced by access policy.
            #
            # --session-id creates, --resume continues. That one line is the
            # difference between a bot with a memory and 218 cold starts.
            cmd = [CLAUDE, "-p", prompt, "--dangerously-skip-permissions"]
            cmd += (["--session-id", session_id] if first_run
                    else ["--resume", session_id])
            proc = subprocess.Popen(
                cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace",
                creationflags=NO_WINDOW)
            threading.Thread(target=watch_session,
                             args=(proc, key, session_id, started_utc, stop_watch,
                                   cfg, title, len(orders)),
                             daemon=True).start()
            try:
                out, err = proc.communicate(timeout=3600)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()
                raise
            took = time.time() - started
            state.setdefault("runs", []).append({"at": time.time(), "seconds": took})
            log("  [%s] session exit %s after %ds" % (key, proc.returncode, took))
            with open(os.path.join(INBOX, "last-session.txt"), "w", encoding="utf-8") as fh:
                fh.write((out or "")[-4000:] + "\n--- stderr ---\n" + (err or "")[-2000:])
            if proc.returncode == 0:
                rec["started"] = True
                rec["runs"] = rec.get("runs", 0) + 1
                rec["last_active"] = datetime.now().isoformat(timespec="seconds")
                # The company-file contract, checked while the work is fresh. A
                # failure is not fatal - it becomes the first line of this
                # chat's next prompt, and blocks rotation until it is fixed.
                problems = jobfile.check_company(key) if key != router.DESK else []
                if problems:
                    rec["file_warn"] = "; ".join(problems)
                    log("  [%s] company file out of contract: %s" % (key, rec["file_warn"]))
                else:
                    rec.pop("file_warn", None)
                router.save_registry(reg)
            else:
                if first_run:
                    rec["started"] = False
                    router.save_registry(reg)
            # A session that dies in seconds is a usage limit or a broken CLI.
            if proc.returncode != 0 and took < FAST_FAIL_SECONDS:
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
            stop_watch.set()
            stop_feed.set()
            # Back to idle, carrying the last thing he said. Without this the
            # card keeps "Working on ..." until the next session starts, which
            # is the same lie the old status told by never changing at all.
            try:
                bot_status.write("jacob", "idle", depth=0,
                                 detail="finished - nothing queued",
                                 session_id=session_id, env=cfg)
            except Exception:
                pass
            # What it really cost, read back out of the transcript. His
            # sessions were not measured at all before this.
            try:
                budget.log_tokens("jacob:" + key, session_id,
                                  time.time() - started, started_utc)
            except Exception:
                pass
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

# -*- coding: utf-8 -*-
"""Three walls and a meter. Everything else the old budget system had is gone.

The meter reads the truth: context re-read per call, from the session
transcript, deduped by requestId (one API call is written as several records
and summing rows inflates ~1.7x - measured 03/08).
"""
import datetime as dt
import json
import os
import time

import config

PROJ_DIR = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                        "C--Users-zacpl-Desktop-Glazing-Quote-Assistant")
LOCAL_USAGE = os.path.join(config.DATA, "glasshouse-usage.jsonl")


def session_cost(session_id, since_utc_iso=""):
    """context/output/calls for one session, optionally only after a moment."""
    path = os.path.join(PROJ_DIR, session_id + ".jsonl")
    out = {"context": 0, "output": 0, "calls": 0, "last_context": 0}
    if not os.path.exists(path):
        return out
    seen = set()
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if r.get("type") != "assistant":
                    continue
                if since_utc_iso and (r.get("timestamp") or "") < since_utc_iso:
                    continue
                u = (r.get("message") or {}).get("usage") or {}
                rid = r.get("requestId")
                if not u or rid in seen:
                    continue
                seen.add(rid)
                ctx = (u.get("cache_read_input_tokens", 0)
                       + u.get("cache_creation_input_tokens", 0)
                       + u.get("input_tokens", 0))
                out["context"] += ctx
                out["output"] += u.get("output_tokens", 0)
                out["calls"] += 1
                if ctx:
                    out["last_context"] = ctx
    except IOError:
        pass
    return out


def log_usage(row):
    """Local mirror of what is posted to the record - survives the hub being down."""
    with open(LOCAL_USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")


# What a token of each kind actually costs, relative to one fresh input token.
# Cache reads are an order of magnitude cheaper than fresh input, and 96% of
# what these sessions move is cache reads - so counting them 1:1 measures
# CONTEXT MOVED, not money. Both numbers are useful; they are not the same
# number and must never be compared to each other.
WEIGHTS = {"cache_read": 0.1, "cache_creation": 1.25, "input": 1.0, "output": 5.0}
# And a token of Opus costs about five of Sonnet, which costs about three of
# Haiku. Since the whole point of this system is running Sonnet by default,
# a raw token count hides the saving entirely.
MODEL_WEIGHT = {"opus": 5.0, "sonnet": 1.0, "haiku": 0.33}


def _model_weight(model):
    m = (model or "").lower()
    for key, w in MODEL_WEIGHT.items():
        if key in m:
            return w
    return 1.0


_scan_cache = {"at": 0.0, "day": "", "totals": None}


def scan_today(force=False):
    """The truth, read from the transcripts themselves.

    This replaces summing the completed-session log, which was wrong three ways
    and by 38% on the morning it was checked:
      * a session still RUNNING has written no row yet, so live spend was
        invisible - exactly when you most want to see it;
      * a session that is killed never writes a row at all, so its tokens were
        spent and never counted;
      * intake's Haiku calls were never recorded anywhere.
    Reading the transcripts catches all three, because every call lands there
    whatever happens afterwards.
    """
    day = dt.date.today().isoformat()
    now = time.time()
    if (not force and _scan_cache["totals"] and _scan_cache["day"] == day
            and now - _scan_cache["at"] < 20):
        return _scan_cache["totals"]

    totals = {"context": 0, "output": 0, "calls": 0, "weighted": 0.0,
              "sessions": 0, "by_model": {}}
    try:
        names = os.listdir(PROJ_DIR)
    except OSError:
        names = []
    for name in names:
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(PROJ_DIR, name)
        try:
            if dt.date.fromtimestamp(os.path.getmtime(path)).isoformat() != day:
                continue        # untouched today; nothing in it can be today's
        except OSError:
            continue
        seen = set()
        got = False
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    if r.get("type") != "assistant":
                        continue
                    if not (r.get("timestamp") or "").startswith(day):
                        continue
                    msg = r.get("message") or {}
                    u = msg.get("usage") or {}
                    rid = r.get("requestId")
                    if not u or rid in seen:
                        continue      # one call is written as several records
                    seen.add(rid)
                    got = True
                    cr = u.get("cache_read_input_tokens", 0)
                    cc = u.get("cache_creation_input_tokens", 0)
                    inp = u.get("input_tokens", 0)
                    out = u.get("output_tokens", 0)
                    mw = _model_weight(msg.get("model"))
                    totals["context"] += cr + cc + inp
                    totals["output"] += out
                    totals["calls"] += 1
                    totals["weighted"] += mw * (cr * WEIGHTS["cache_read"]
                                                + cc * WEIGHTS["cache_creation"]
                                                + inp * WEIGHTS["input"]
                                                + out * WEIGHTS["output"])
                    key = (msg.get("model") or "?").replace("claude-", "")
                    totals["by_model"][key] = totals["by_model"].get(key, 0) + cr + cc + inp
        except OSError:
            continue
        if got:
            totals["sessions"] += 1
    _scan_cache.update(at=now, day=day, totals=totals)
    return totals


def spent_today():
    """Context tokens moved today, by everything: finished sessions, sessions
    still running, sessions that were killed, and intake."""
    return scan_today()["context"]


def weighted_today():
    """The same day expressed in fresh-input-token equivalents - the number
    that actually tracks the allowance, because it prices cache reads and the
    model mix instead of counting every token as if it were the same."""
    return scan_today()["weighted"]


def day_breaker_tripped():
    return spent_today() >= config.DAY_CONTEXT_BREAKER


def off_hours(now=None):
    """True outside the working day. See config.WORK_HOURS.

    Off hours does NOT mean nothing runs - it means only what a human asked
    for runs. `dispatch` filters the queue rather than sleeping through it.
    """
    now = now or dt.datetime.now()
    start, end = config.WORK_HOURS
    if start <= now.hour < end:
        return False
    try:
        with open(config.NIGHT_FLAG, encoding="utf-8") as fh:
            flag = json.load(fh)
        tonight = (now - dt.timedelta(hours=start)).date().isoformat()
        if flag.get("date") == tonight:
            return False          # somebody lifted it for this evening
    except (IOError, ValueError):
        pass
    return True


def asked_for_by_a_human(task):
    """The one thing worth waking up for: a dashboard message, or Adam."""
    if task.get("kind") == "hub":
        return True
    try:
        payload = json.loads(task.get("payload_json") or "{}")
    except ValueError:
        return False
    return bool(payload.get("trusted_sender"))


def cost_note(persona):
    """Evidence for the seed, not a quota: what today has cost so far."""
    tok = spent_today()
    if not tok:
        return ""
    return ("\nCOST so far today, all personas: {:,} context tokens against a target "
            "of {:,}. Cost is context x turns. Batch your shell work, read a file "
            "once, and close out in ONE finish call.".format(tok, config.DAY_TARGET))

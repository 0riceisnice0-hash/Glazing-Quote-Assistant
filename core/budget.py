# -*- coding: utf-8 -*-
"""Three walls and a meter. Everything else the old budget system had is gone.

The meter reads the truth: context re-read per call, from the session
transcript, deduped by requestId (one API call is written as several records
and summing rows inflates ~1.7x - measured 03/08).
"""
import datetime as dt
import json
import os

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


def spent_today():
    """Context tokens across all personas since local midnight."""
    day = dt.date.today().isoformat()
    total = 0
    try:
        with open(LOCAL_USAGE, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if (r.get("at") or "").startswith(day):
                    total += r.get("context_tokens", 0)
    except IOError:
        pass
    return total


def day_breaker_tripped():
    return spent_today() >= config.DAY_CONTEXT_BREAKER


def in_curfew(now=None):
    """21:00-07:00, unless somebody lifted it for tonight specifically."""
    now = now or dt.datetime.now()
    start, end = config.CURFEW
    night = now.hour >= start or now.hour < end
    if not night:
        return False
    try:
        with open(config.NIGHT_FLAG, encoding="utf-8") as fh:
            flag = json.load(fh)
        tonight = (now - dt.timedelta(hours=end)).date().isoformat()
        if flag.get("date") == tonight:
            return False
    except (IOError, ValueError):
        pass
    return True


def cost_note(persona):
    """Evidence for the seed, not a quota: what today has cost so far."""
    tok = spent_today()
    if not tok:
        return ""
    return ("\nCOST so far today, all personas: {:,} context tokens against a target "
            "of {:,}. Cost is context x turns. Batch your shell work, read a file "
            "once, and close out in ONE finish call.".format(tok, config.DAY_TARGET))

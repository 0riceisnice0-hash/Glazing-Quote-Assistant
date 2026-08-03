# -*- coding: utf-8 -*-
"""What a session ACTUALLY cost, read from the transcript Claude Code writes.

This replaces the measure that let the allowance run out on 30/07/2026 without
a single alarm firing.

WHAT WAS WRONG. `mary_budget.log_tokens()` recorded `delta_bytes / 4` - how much
the transcript GREW. But the cost of a permanent per-job chat is the context it
RE-READS on every turn, and that is a completely different number. On 29/07 the
old meter reported 3.06M for the day; the transcripts say ~550M. The day budget
was set to 12M, so a breaker sized at "2-3x a normal day" could never fire, and
its sizing had been derived from the broken meter in the first place.

WHAT IS TRUE INSTEAD. Every assistant message carries a `usage` block with
`cache_read_input_tokens`, `cache_creation_input_tokens` and `input_tokens`.
Their sum is the context that call was billed for. Output is small by
comparison and tracked separately.

THE TRAP THAT INFLATES IT 1.7x. One API call can appear as SEVERAL assistant
records - a text block and a tool_use block are written separately and each
carries a COPY of the same usage object. Summing rows therefore double-counts:
across the whole project folder, 4.08 billion raw against 2.38 billion real.
Records are deduped by `requestId`, and anything that counts tokens here MUST
do the same. This was found on 03/08 by noticing two identical usage blocks a
second apart.

  python scripts/mary_cost.py                  # spend per day, bots vs the rest
  python scripts/mary_cost.py --hours          # by hour - where the night goes
  python scripts/mary_cost.py --chats          # per chat, worst first
  python scripts/mary_cost.py --session <uuid> # one conversation
"""
import argparse
import datetime as dt
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                       "C--Users-zacpl-Desktop-Glazing-Quote-Assistant")


def transcript(session_id):
    return os.path.join(PROJECT, "%s.jsonl" % session_id)


def _tokens(usage):
    """Context billed for one call. Output is not context and is counted apart."""
    return ((usage.get("cache_read_input_tokens") or 0)
            + (usage.get("cache_creation_input_tokens") or 0)
            + (usage.get("input_tokens") or 0))


def iter_calls(path):
    """Yield (timestamp, context_tokens, output_tokens) once per real API call.

    Deduped by requestId - see the module docstring. Without this every number
    in this file is about 1.7x too big.
    """
    if not os.path.exists(path):
        return
    seen = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"usage"' not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            usage = (rec.get("message") or {}).get("usage")
            if not isinstance(usage, dict):
                continue
            key = rec.get("requestId") or rec.get("uuid")
            if key in seen:
                continue
            seen.add(key)
            yield rec.get("timestamp") or "", _tokens(usage), (usage.get("output_tokens") or 0)


def session_cost(session_id, since=None):
    """Everything this conversation has been billed, optionally since a time.

    `since` is an ISO string or datetime. A resumed chat appends to the same
    file, so bounding by time is what isolates ONE run of it.
    """
    if isinstance(since, dt.datetime):
        since = since.isoformat()
    ctx = out = calls = 0
    peak = 0
    for ts, c, o in iter_calls(transcript(session_id)):
        if since and ts and ts[:19] < since[:19]:
            continue
        ctx += c
        out += o
        calls += 1
        peak = max(peak, c)
    return {"context": ctx, "output": out, "calls": calls, "peak_context": peak,
            "per_call": ctx // calls if calls else 0}


def context_size(session_id):
    """The context the NEXT turn of this chat will carry.

    This is the number rotation should key on. File size was standing in for
    it and was a poor proxy: gordon-court passed 8 MB and kept going to 17.6.
    """
    last = 0
    for _ts, c, _o in iter_calls(transcript(session_id)):
        last = c
    return last


def spend(since, until=None, sessions=None):
    """(total context, {session_id: context}) across transcripts in a window."""
    if isinstance(since, dt.datetime):
        since = since.isoformat()
    if isinstance(until, dt.datetime):
        until = until.isoformat()
    total, per = 0, {}
    if not os.path.isdir(PROJECT):
        return 0, {}
    for name in os.listdir(PROJECT):
        if not name.endswith(".jsonl"):
            continue
        sid = name[:-6]
        if sessions is not None and sid not in sessions:
            continue
        for ts, c, _o in iter_calls(os.path.join(PROJECT, name)):
            if not ts:
                continue
            if ts[:19] < since[:19]:
                continue
            if until and ts[:19] >= until[:19]:
                continue
            total += c
            per[sid] = per.get(sid, 0) + c
    return total, per


def bot_sessions():
    """Session ids that belong to a bot chat, current and rotated-away."""
    out = {}
    try:
        with open(os.path.join(REPO, "data", "mary-jobs.json"),
                  encoding="utf-8") as fh:
            reg = json.load(fh)
        for key, chat in (reg.get("chats") or {}).items():
            for field in ("session_id", "rotated_from"):
                if chat.get(field):
                    out[chat[field]] = key
    except (IOError, ValueError):
        pass
    try:
        with open(os.path.join(REPO, "data", "jacob", "bridge-state.json"),
                  encoding="utf-8") as fh:
            st = json.load(fh)
        sid = (st.get("last_kick") or {}).get("session_id")
        if sid:
            out[sid] = "jacob"
    except (IOError, ValueError):
        pass
    return out


# --------------------------------------------------------------- reporting
def _fmt(n):
    return "{:,}".format(int(n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--hours", action="store_true", help="spend by hour of day")
    ap.add_argument("--chats", action="store_true", help="spend per chat")
    ap.add_argument("--session", help="one session id")
    args = ap.parse_args()

    if args.session:
        c = session_cost(args.session)
        print("session %s" % args.session)
        for k in ("calls", "context", "per_call", "peak_context", "output"):
            print("  %-14s %s" % (k, _fmt(c[k])))
        print("  %-14s %s   <- what the next turn carries"
              % ("now", _fmt(context_size(args.session))))
        return 0

    known = bot_sessions()
    since = dt.datetime.now() - dt.timedelta(days=args.days)
    per_day_bot, per_day_dev, per_hour, per_chat = {}, {}, {}, {}
    for name in sorted(os.listdir(PROJECT)):
        if not name.endswith(".jsonl"):
            continue
        sid = name[:-6]
        key = known.get(sid)
        for ts, c, _o in iter_calls(os.path.join(PROJECT, name)):
            if not ts or ts[:19] < since.isoformat()[:19]:
                continue
            day, hour = ts[:10], int(ts[11:13])
            if key:
                per_day_bot[day] = per_day_bot.get(day, 0) + c
                per_hour[hour] = per_hour.get(hour, 0) + c
                per_chat[key] = per_chat.get(key, 0) + c
            else:
                per_day_dev[day] = per_day_dev.get(day, 0) + c

    if args.chats:
        print("PER CHAT, worst first (context tokens)")
        for k, v in sorted(per_chat.items(), key=lambda kv: -kv[1]):
            print("  %-24s %16s" % (k, _fmt(v)))
        return 0

    if args.hours:
        night = sum(v for h, v in per_hour.items() if h >= 22 or h < 7)
        total = sum(per_hour.values()) or 1
        top = max(per_hour.values()) if per_hour else 1
        print("BOT SPEND BY HOUR")
        for h in range(24):
            v = per_hour.get(h, 0)
            print("  %02d:00 %14s %-40s%s"
                  % (h, _fmt(v), "#" * int(40 * v / top),
                     " NIGHT" if (h >= 22 or h < 7) else ""))
        print("\n  22:00-07:00 %s (%.1f%%)" % (_fmt(night), 100.0 * night / total))
        return 0

    print("REAL COST PER DAY - context tokens, deduped by requestId")
    print("  %-12s %16s %16s" % ("day", "bots", "everything else"))
    for day in sorted(set(per_day_bot) | set(per_day_dev)):
        print("  %-12s %16s %16s"
              % (day, _fmt(per_day_bot.get(day, 0)), _fmt(per_day_dev.get(day, 0))))
    active = [d for d, v in per_day_bot.items() if v]
    if active:
        print("\n  bot mean/active day %s over %d days"
              % (_fmt(sum(per_day_bot.values()) / len(active)), len(active)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

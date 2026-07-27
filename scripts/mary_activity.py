# -*- coding: utf-8 -*-
"""A live feed of what Mary is doing right now, for the hub.

Claude Code already writes every session to a transcript as it happens, so
there is no need to change how sessions run or to parse stdout - just tail the
file. That keeps the risky part (launching and completing work) untouched.

Produces the same shape of thing you see in a Claude Code terminal: what she
said, which tool she reached for, and what came back - condensed, because the
raw transcript is far too much to read and full of file contents nobody needs.

  python scripts/mary_activity.py <chat-key>    # print the live feed
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                           "C--Users-zacpl-Desktop-Glazing-Quote-Assistant")
MAX_TEXT = 400


def transcript(session_id):
    path = os.path.join(PROJECT_DIR, "%s.jsonl" % session_id)
    return path if os.path.exists(path) else None


def _clean(s):
    """Flatten to one line and drop markdown markers - the feed renders as
    plain text, so `**double**` would otherwise show its asterisks."""
    t = re.sub(r"\s+", " ", str(s or "")).strip()
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"(?<!\w)[*_`]{1,2}(?=\S)|(?<=\S)[*_`]{1,2}(?!\w)", "", t)
    return re.sub(r"^#{1,6}\s*", "", t)


def _describe_tool(name, inp):
    """One readable line per tool call - the command, the file, the query."""
    inp = inp if isinstance(inp, dict) else {}
    for key in ("command", "file_path", "pattern", "path", "url", "prompt", "query"):
        if inp.get(key):
            return "%s  %s" % (name, _clean(inp[key])[:200])
    return name


def feed(session_id, limit=60):
    """Condense the transcript tail into something worth watching."""
    path = transcript(session_id)
    if not path:
        return []
    events = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                kind = row.get("type")
                ts = row.get("timestamp", "")
                content = (row.get("message") or {}).get("content")
                if kind == "assistant" and isinstance(content, list):
                    for c in content:
                        if c.get("type") == "text" and _clean(c.get("text")):
                            events.append({"kind": "say", "ts": ts,
                                           "text": _clean(c["text"])[:MAX_TEXT]})
                        elif c.get("type") == "thinking" and _clean(c.get("thinking")):
                            events.append({"kind": "think", "ts": ts,
                                           "text": _clean(c["thinking"])[:MAX_TEXT]})
                        elif c.get("type") == "tool_use":
                            events.append({"kind": "tool", "ts": ts,
                                           "text": _describe_tool(c.get("name"), c.get("input"))})
                elif kind == "user" and isinstance(content, list):
                    for c in content:
                        if c.get("type") == "tool_result":
                            body = c.get("content")
                            if isinstance(body, list):
                                body = " ".join(x.get("text", "") for x in body
                                                if isinstance(x, dict))
                            txt = _clean(body)[:180]
                            if txt:
                                events.append({"kind": "result", "ts": ts, "text": txt})
    except OSError:
        return []
    return events[-limit:]


def push(env, chat, title, events):
    """Send the feed to the hub. Best effort - never break a session over it."""
    if not events:
        return False
    try:
        import urllib.request
        key = env.get("MARY_API_KEY")
        if not key:
            return False
        base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
        payload = json.dumps({"chat": chat, "title": title, "events": events}).encode("utf-8")
        req = urllib.request.Request(base + "/api/mary/activity", data=payload, method="POST")
        req.add_header("x-mary-key", key)
        req.add_header("content-type", "application/json")
        req.add_header("user-agent", "MaryBridge/1.0")
        urllib.request.urlopen(req, timeout=15).read()
        return True
    except Exception:
        return False


def main():
    if len(sys.argv) < 2:
        print("usage: mary_activity.py <chat-key>")
        return 2
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import mary_router as router
    reg = router.load_registry()
    rec = reg["chats"].get(sys.argv[1])
    if not rec:
        print("no such chat: %s" % sys.argv[1])
        return 1
    for e in feed(rec["session_id"]):
        print("%-7s %s" % (e["kind"], e["text"][:150]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

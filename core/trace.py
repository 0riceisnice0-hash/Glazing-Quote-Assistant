# -*- coding: utf-8 -*-
"""Stream a running session's transcript to the hub, so a human can watch.

Zac: "i want to see everything going on as if it was a claude session in the
desktop app. their thinking etc."

Everything is already on disk - `claude -p` writes the whole conversation to
~/.claude/projects/<project>/<session-id>.jsonl as it goes. This tails that
file while the session runs and posts each new block to the record.

Two things it must not do:
  * block the session - it runs on its own thread and swallows its own errors
  * ship a novel - bodies are capped, and a 40,000-character file read is
    summarised rather than sent
"""
import json
import os

import budget
import record

CAP_THINKING = 2400
CAP_TEXT = 1600
CAP_INPUT = 700
CAP_RESULT = 700
POLL = 3.0


def _clip(s, n):
    s = str(s or "").strip()
    return s if len(s) <= n else s[:n].rstrip() + " …"


def _tool_summary(name, inp):
    """The one line a human wants: what did it actually run or open."""
    if not isinstance(inp, dict):
        return _clip(inp, CAP_INPUT)
    for key in ("command", "file_path", "path", "pattern", "query", "url", "prompt"):
        if inp.get(key):
            extra = ""
            if name == "Edit" and inp.get("old_string"):
                extra = "  (replacing %d chars)" % len(str(inp["old_string"]))
            if name == "Write" and inp.get("content"):
                extra = "  (%d chars)" % len(str(inp["content"]))
            return _clip(str(inp[key]), CAP_INPUT) + extra
    return _clip(json.dumps(inp)[:CAP_INPUT], CAP_INPUT)


def _blocks(rec):
    """Turn one transcript line into zero or more trace rows."""
    out = []
    msg = rec.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]
    if not isinstance(content, list):
        return out
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "thinking" and b.get("thinking"):
            out.append(("thinking", "", _clip(b["thinking"], CAP_THINKING)))
        elif t == "text" and b.get("text"):
            out.append(("say", "", _clip(b["text"], CAP_TEXT)))
        elif t == "tool_use":
            out.append(("tool", b.get("name", "?"),
                        _tool_summary(b.get("name"), b.get("input"))))
        elif t == "tool_result":
            c = b.get("content")
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            body = _clip(c, CAP_RESULT)
            if b.get("is_error"):
                body = "ERROR: " + body
            if body:
                out.append(("result", "", body))
    return out


def follow(session_id, persona, entity, stop):
    """Tail one session until `stop` is set. Never raises into the caller."""
    path = os.path.join(budget.PROJ_DIR, session_id + ".jsonl")
    pos, pending = 0, ""
    post("start", persona, session_id, entity, "", "session started")
    while True:
        done = stop.wait(POLL)
        try:
            if os.path.exists(path):
                with open(path, encoding="utf-8", errors="replace") as fh:
                    fh.seek(pos)
                    chunk = fh.read()
                    pos = fh.tell()
                text = pending + chunk
                lines = text.split("\n")
                pending = lines.pop()          # keep the half-written last line
                rows = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        continue
                    if rec.get("type") not in ("assistant", "user"):
                        continue
                    for kind, tool, body in _blocks(rec):
                        rows.append({"persona": persona, "session_id": session_id,
                                     "entity_key": entity, "kind": kind,
                                     "tool": tool, "body": body})
                for i in range(0, len(rows), 40):
                    record.call("/api/trace", {"rows": rows[i:i + 40]})
        except Exception:
            pass                                # watching must never break working
        if done:
            return


def post(kind, persona, session_id, entity, tool, body):
    try:
        record.call("/api/trace", {"rows": [{
            "persona": persona, "session_id": session_id, "entity_key": entity,
            "kind": kind, "tool": tool, "body": body}]})
    except Exception:
        pass

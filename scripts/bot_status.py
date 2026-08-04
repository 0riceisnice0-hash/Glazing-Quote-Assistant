# -*- coding: utf-8 -*-
"""What each bot is doing, in one place, for all three of them.

Zac, 04/08: *"it should have a header of 'working on X' and the sub text is
the last message/ thought it had."*

So a status is TWO things and only one of them was being recorded. The job is
what the bot is on; the thought is the last thing it actually said about it.
The second is the one that tells you whether it is moving or stuck - "working
on St Mary's" for forty minutes tells you nothing, "still waiting on the door
schedule" tells you everything.

Mary had a private write_status; Jacob and Joseph had none at all, so their
cards on the hub showed no life whatever they were doing. This is the shared
version, and the parity test now checks all three use it.

The thought is read out of the session transcript, which Claude Code is
already writing. Nothing about how a session runs has to change to get it.
"""
import datetime as dt
import json
import os

import mary_activity as activity

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mary's file predates the convention and live things read it by name, so it
# keeps its spelling. Everyone from Jacob on follows the pattern.
FILES = {
    "mary": os.path.join(REPO, "data", "mary-bridge-status.json"),
    "jacob": os.path.join(REPO, "data", "jacob-bridge-status.json"),
    "joseph": os.path.join(REPO, "data", "joseph-bridge-status.json"),
}

# One per bot, so a stale fingerprint from one cannot suppress another's write.
_pushed = {}


def last_thought(session_id):
    """The last thing the bot said or thought, for the line under the header.

    Prefers what it SAID over what it thought - a said line is addressed to
    somebody and reads as a sentence, where a thought is caught mid-reasoning.
    Falls back to the tool it reached for, because "reading the door schedule"
    is still a better answer than a blank line.
    """
    if not session_id:
        return ""
    try:
        events = activity.feed(session_id, limit=80)
    except Exception:
        return ""
    for kind in ("say", "think", "tool"):
        for ev in reversed(events):
            if ev.get("kind") == kind and ev.get("text"):
                return _lede(ev["text"])
    return ""


def _lede(text):
    """The opening line, not the opening line plus the next section's heading.

    A session usually signs off with a sentence and then launches into its
    report - "Done. Committed and pushed. ## Georgie's - Pearce Construction,
    deadline tomorrow". The feed flattens that to one line, so the heading
    marker survives mid-string and the card shows a sentence with `##` in it.
    Cut there: the sentence is the status, the report is on the bot's page.
    """
    t = str(text or "").strip()
    cut = t.find("##")
    if cut > 0:                      # 0 means it opens with a heading - keep it
        t = t[:cut].strip()
    return t[:300]


def write(bot, state, chat_key=None, depth=0, detail="", title="", session_id=None,
          env=None, thought=None):
    """Record what a bot is doing, locally and on the hub.

    The hub only needs to hear when it CHANGES, so a bot sitting idle does not
    write to D1 on a two-second loop.
    """
    if thought is None:
        thought = last_thought(session_id)
    payload = {
        "state": state,                       # idle | working | batching | backoff | held
        "chat": chat_key,
        "title": title or (chat_key or ""),
        "queue_depth": depth,
        "detail": detail,
        "thought": thought,
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
    }
    path = FILES.get(bot)
    if path:
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=1)
        except Exception:
            pass

    # The thought is in the fingerprint deliberately: it changing IS the news,
    # and it is the only field that moves while a long session is running.
    fingerprint = (state, chat_key, depth, detail, thought)
    push(bot, fingerprint, payload, env or {})
    return payload


def push(bot, fingerprint, payload, env):
    """POST to the hub when the state changes. Best effort - the bot working
    matters more than the page knowing about it."""
    if _pushed.get(bot) == fingerprint:
        return False
    try:
        import urllib.request
        key = env.get("MARY_API_KEY")
        if not key:
            return False
        base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
        req = urllib.request.Request(
            "%s/api/%s/status" % (base, bot),
            data=json.dumps(payload).encode("utf-8"), method="POST")
        req.add_header("x-mary-key", key)
        req.add_header("content-type", "application/json")
        req.add_header("user-agent", "BotBridge/1.0")
        urllib.request.urlopen(req, timeout=15).read()
        _pushed[bot] = fingerprint
        return True
    except Exception:
        return False


def read(bot):
    """What the local file says. Used by preflight and by the other bots."""
    try:
        with open(FILES[bot], encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {"state": "unknown"}


def everyone():
    """All three at once - what the front desk page opens with."""
    return {b: read(b) for b in FILES}

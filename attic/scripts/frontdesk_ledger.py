# -*- coding: utf-8 -*-
"""Every call the front desk has ever made, in one file.

Zac, 04/08: *"everything the front desk sees i want to see."*

Until now a routing decision left three traces and no record: a line in a log
file, a `triage` block on the queued item, and - for noise - a binned copy in
a folder nobody opens. You could not answer "how much spam came in today" or
"why did that go to Jacob" without grepping. So the decision becomes a row.

One JSON object per line, appended, never rewritten:

  ts        when the call was made
  mailbox   which inbox it came from
  from      sender
  subject   subject line
  bot       mary | jacob | joseph
  verdict   work | fyi | noise
  why       the classifier's eight words
  model     which model decided
  id        the Graph message id, so a row joins back to the item

The file is the truth; the hub gets a rolling window of it. Nothing here
deletes: a wrong call has to stay findable, or the noise list cannot be
trusted.
"""
import datetime as dt
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "data", "frontdesk-ledger.jsonl")
WINDOW = 400          # rows sent to the hub - the stream, not the archive


def add(mailbox, msg, bot, verdict, why, model, at=None):
    """Append one decision. Best effort: the sweep matters more than the row."""
    rec = {
        "ts": at or dt.datetime.now().isoformat(timespec="seconds"),
        "mailbox": mailbox or "",
        "from": ((msg.get("from") or {}).get("emailAddress") or {}).get("address", "")
                if isinstance(msg.get("from"), dict) else str(msg.get("from") or ""),
        "subject": str(msg.get("subject") or "")[:200],
        "bot": bot,
        "verdict": verdict,
        "why": str(why or "")[:120],
        "model": model,
        "id": str(msg.get("id") or ""),
        "received": str(msg.get("receivedDateTime") or ""),
    }
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return rec


def rows(limit=None):
    """Newest last, the way it was written."""
    out = []
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except OSError:
        return []
    return out[-limit:] if limit else out


def totals(days=None):
    """What the tab's headline numbers are counting.

    `days=None` is everything; `days=1` is today's sweep. Kept separate from
    the stream because a count over a window and a list of recent rows are two
    different questions and conflating them is how a page starts lying.
    """
    rs = rows()
    if days:
        cut = (dt.datetime.now() - dt.timedelta(days=days)).isoformat()
        rs = [r for r in rs if (r.get("ts") or "") >= cut]
    t = {"seen": len(rs), "noise": 0, "work": 0, "fyi": 0,
         "bots": {}, "mailboxes": {}, "senders": {}}
    for r in rs:
        v = r.get("verdict") or "work"
        b = r.get("bot") or "mary"
        t[v] = t.get(v, 0) + 1
        slot = t["bots"].setdefault(b, {"work": 0, "fyi": 0, "noise": 0, "total": 0})
        slot[v] = slot.get(v, 0) + 1
        slot["total"] += 1
        mb = (r.get("mailbox") or "").split("@")[0] or "?"
        t["mailboxes"][mb] = t["mailboxes"].get(mb, 0) + 1
        if v == "noise" and r.get("from"):
            t["senders"][r["from"]] = t["senders"].get(r["from"], 0) + 1
    # Who sends the most junk, biggest first - the list that earns a rule in
    # noise.md and stops the classifier being asked about them at all.
    t["worst"] = sorted(t["senders"].items(), key=lambda kv: -kv[1])[:12]
    t.pop("senders")
    return t


def payload(days=None):
    """What the hub stores: the headline numbers and a rolling window."""
    return {"totals": totals(), "today": totals(days=1),
            "stream": rows(limit=WINDOW),
            "updated": dt.datetime.now().isoformat(timespec="seconds")}


def push(env):
    """Send it to the hub. Same posture as every other bridge push - the sweep
    working matters more than the page being current."""
    try:
        import urllib.request
        key = env.get("MARY_API_KEY")
        if not key:
            return False
        base = env.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
        req = urllib.request.Request(
            base + "/api/frontdesk",
            data=json.dumps(payload()).encode("utf-8"), method="POST")
        req.add_header("x-mary-key", key)
        req.add_header("content-type", "application/json")
        req.add_header("user-agent", "FrontDesk/1.0")
        urllib.request.urlopen(req, timeout=20).read()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    import sys
    t = totals()
    print("front desk has judged %d message(s)" % t["seen"])
    print("  %d work, %d fyi, %d noise" % (t["work"], t["fyi"], t["noise"]))
    for b, s in sorted(t["bots"].items()):
        print("  %-7s %3d work  %3d fyi  %3d noise" % (b, s["work"], s["fyi"], s["noise"]))
    if t["worst"]:
        print("  worst senders:")
        for addr, n in t["worst"][:5]:
            print("    %3d  %s" % (n, addr))
    sys.exit(0)

# -*- coding: utf-8 -*-
"""Assemble Mary's dashboard data and (optionally) deploy it.

Sources:
  data/dashboard-state.json          - curated by sessions at close-out
  Graph mary@ sentitems              - every email ever sent (live)
  test-results/mary-inbox/poller.log - poll/session counts
  HANDOVER.md 'no-action sessions'   - via state file

Usage:
  python scripts/mary_dashboard.py            # regenerate dashboard-data.js
  python scripts/mary_dashboard.py --deploy   # regenerate + wrangler deploy
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

REPO = mg.REPO
STATE = os.path.join(REPO, "data", "dashboard-state.json")
OUT = os.path.join(REPO, "dashboard", "functions", "_data", "dashboard-data.js")
LOG = os.path.join(REPO, "test-results", "mary-inbox", "poller.log")


def uk(iso):
    """Graph hands us UTC ('...Z'). Adam reads the hub in UK time.

    Slicing the string to 16 characters and dropping the Z - which is what this
    file used to do - published every timestamp an hour early through BST, so a
    message Adam sent at 21:47 appeared on the board as 20:48. Convert properly,
    and label it, so nobody has to know which end the hour went missing from.
    """
    if not iso:
        return ""
    try:
        t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=dt.timezone.utc)
        try:
            from zoneinfo import ZoneInfo
            t = t.astimezone(ZoneInfo("Europe/London"))
        except Exception:
            t = t.astimezone()          # fall back to the machine's own zone
        return t.strftime("%Y-%m-%d %H:%M %Z")
    except Exception:
        return iso[:16].replace("T", " ")


def sent_emails(token):
    st, res = mg.graph(token, "GET",
        "/users/%s/mailFolders/sentitems/messages?$top=50&$select=subject,toRecipients,sentDateTime,body&$orderby=sentDateTime%%20desc" % mg.MARY)
    if st != 200:
        return []
    out = []
    for m in res.get("value", []):
        out.append({
            "sent": uk(m.get("sentDateTime", "")),
            "to": ", ".join(r["emailAddress"]["address"].split("@")[0] for r in m.get("toRecipients", [])),
            "subject": m.get("subject", ""),
            "body": mg.html_to_text(m.get("body", {}).get("content", ""))[:6000],
        })
    return out


def inbox_seen():
    """Everything Mary has read: the processed queue records."""
    proc = os.path.join(REPO, "test-results", "mary-inbox", "processed")
    items = []
    if os.path.isdir(proc):
        for f in sorted(os.listdir(proc), reverse=True):
            if not f.endswith(".json"):
                continue
            try:
                d = json.load(open(os.path.join(proc, f), encoding="utf-8"))
            except Exception:
                continue
            items.append({
                "received": uk(d.get("received", "")),
                "from": d.get("from", ""),
                "subject": d.get("subject", ""),
                "attachments": len(d.get("attachments", [])),
                "body": (d.get("body") or "")[:5000],
            })
            if len(items) >= 80:
                break
    return items


def poller_stats():
    polls = launched = 0
    if os.path.exists(LOG):
        for line in open(LOG, encoding="utf-8", errors="replace"):
            if "poll done" in line:
                polls += 1
            if "launching Claude session" in line:
                launched += 1
    return polls, launched


# One-click answers are answered BY CLICKING, on the hub. Mary has no phone, no
# meetings and no way to be visited, so an option offering one is a dead end for
# whoever clicks it. Zac hit this with "Call me, it's complicated" on REQ-3.
IMPOSSIBLE_OPTIONS = [
    "call me", "call you", "give me a call", "phone", "ring me", "ring you",
    "speak to me", "talk it through", "in person", "come see", "come and see",
    "meet me", "meeting", "let's chat", "lets chat", "face to face", "text me",
    "whatsapp", "teams call", "zoom",
]


def check_request_options(state):
    """Refuse to publish a request whose 'quick answer' cannot actually be done.

    Every option must be a decision that stands on its own when clicked - the
    person picking it is on a web page, not on the phone. If a decision really
    needs a conversation, that belongs in the 'needs' text, not as a button."""
    bad = []
    for r in state.get("requests", []):
        for opt in r.get("options", []) or []:
            low = str(opt).lower()
            if any(p in low for p in IMPOSSIBLE_OPTIONS):
                bad.append((r.get("id", "?"), opt))
    if bad:
        print("REFUSING TO PUBLISH - these one-click answers cannot be actioned:")
        for rid, opt in bad:
            print("  %s: %r" % (rid, opt))
        print("\nMary cannot be called, messaged off-hub, or met. Every option must be a\n"
              "decision the reader can make by clicking it (e.g. 'Reorder against the final\n"
              "list - CN Glass', 'Price it as an option', 'Exclude and qualify it'). If the\n"
              "decision genuinely needs a conversation, say so in 'needs' and leave the\n"
              "options to the choices you CAN act on.")
        raise SystemExit(2)


def _words(s):
    return set(re.findall(r"[a-zA-Z][a-zA-Z-]{5,}", str(s).lower()))


def check_reraise(state):
    """The re-raise guard (Phase 2, AGENT-AUDIT.md).

    'I have already addressed this with you' (Adam, 28/07, REQ-29) is a memory
    failure arriving as a manners failure. Two tiers here:

    REFUSED: an OPEN request on the same job sharing MOST of its title words
    with an ANSWERED one - the near-duplicate shape (REQ-14 was a duplicate of
    REQ-2 and Adam answered it "I have addressed this above"). Tuned loose on
    purpose: REQ-24 legitimately follows REQ-17 with two shared words and a
    title that says what is new, and blocking that would block real work -
    that shape gets the warning, not the refusal.

    WARNED: an open request whose words appear in settled ledger events. That
    is often legitimate (a follow-up moves a settled topic forward), so it
    prints the evidence and lets the session judge - but now it judges with
    the evidence in front of it."""
    reqs = state.get("requests", [])
    answered = [r for r in reqs if r.get("status") == "answered"]
    hard = []
    for r in reqs:
        if r.get("status") != "open":
            continue
        tw = _words(r.get("title", ""))
        for a in answered:
            if a.get("job") != r.get("job") or not tw:
                continue
            overlap = tw & _words(a.get("title", ""))
            if len(overlap) >= max(3, len(tw) // 2):
                hard.append((r.get("id", "?"), a.get("id", "?"), ", ".join(sorted(overlap))))
    if hard:
        print("REFUSING TO PUBLISH - open request(s) shadow an ANSWERED one:")
        for rid, aid, ov in hard:
            print("  %s re-asks %s (shared: %s)" % (rid, aid, ov))
        print("\nRead the answer first (python scripts\\mary_recall.py --settled), then either\n"
              "delete the request or rewrite its title to state what is NEW since the answer.")
        raise SystemExit(2)

    try:
        import mary_ledger
        settled = [e for e in mary_ledger.iter_events()
                   if e.get("kind") == "request_answered"
                   or (e.get("kind") == "hub_msg" and e.get("actor") in ("adam", "zac"))]
    except Exception:
        return
    for r in reqs:
        if r.get("status") != "open":
            continue
        tw = _words(r.get("title", ""))
        for e in settled:
            hay = _words(e.get("summary", "")) | _words(e.get("body", ""))
            common = tw & hay
            if len(common) >= 3:
                print("WARNING %s touches settled ground (%s - shared: %s). If it only re-asks, pull it."
                      % (r.get("id", "?"), e.get("ref", "?"), ", ".join(sorted(common)[:4])))
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deploy", action="store_true")
    args = ap.parse_args()

    state = json.load(open(STATE, encoding="utf-8"))
    check_request_options(state)
    check_reraise(state)
    env = mg.load_env()
    token = mg.get_token(env, "READER")
    emails = sent_emails(token)
    polls, launched = poller_stats()

    data = dict(state)
    data["updated"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Accuracy half of the scoreboard is generated here; the outcome half is
    # fetched live by the page so a Won/Lost click shows up without a redeploy.
    try:
        import mary_scoreboard
        data["scoreboard"] = mary_scoreboard.build()
    except Exception as e:
        print("scoreboard skipped:", e)
        data["scoreboard"] = None
    data["emails"] = emails
    data["inbox"] = inbox_seen()
    data["sessions"] = {
        "polls": polls,
        "launched": launched,
        "emailsSent": len(emails),
        "noAction": state.get("noActionSessions", []),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// generated by scripts/mary_dashboard.py - do not edit\n")
        fh.write("export const DATA = %s;\n" % json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT, "(%d jobs, %d requests, %d emails, %d inbox)" % (
        len(data["jobs"]), len(data.get("requests", [])), len(emails), len(data.get("inbox", []))))

    if args.deploy:
        # Mary builds this hub herself now. The guard is what makes that safe:
        # it refuses the deploy if the key gate, the headers or a secret moved.
        import mary_hub_guard
        if not mary_hub_guard.run():
            raise SystemExit(3)
        r = subprocess.run(["npx.cmd", "wrangler", "pages", "deploy", "public", "--project-name", "mary-dashboard",
                            "--branch", "main", "--commit-dirty=true"],
                           cwd=os.path.join(REPO, "dashboard"), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=600, shell=True)
        tail = (r.stdout + r.stderr)[-600:]
        print("deploy exit", r.returncode)
        # wrangler emits box-drawing characters; stdout here is cp1252, so re-encode
        # rather than let a successful deploy die on its own log output.
        enc = sys.stdout.encoding or "utf-8"
        print(tail.encode(enc, "replace").decode(enc, "replace"))


if __name__ == "__main__":
    main()

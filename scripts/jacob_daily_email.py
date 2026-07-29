# -*- coding: utf-8 -*-
"""The one daily email Adam asked for - leads to chase, and nothing else.

Adam, hub-74, 29/07/2026:

    Jacob must send one daily update email to adam@fensterglazing.com. This
    daily email is strictly limited to leads that need chasing that day ...
    Jacob is not authorised to send any other emails.

So this script builds exactly that message and nothing else. Run it to SEE the
email; it does not send unless it is authorised to, and today it is not:

  python scripts/jacob_daily_email.py                 # build it and print it
  python scripts/jacob_daily_email.py --json          # the rows it selected
  python scripts/jacob_daily_email.py --send          # refuses - see below

WHY IT DOES NOT SEND YET. Two humans have said two different things and
neither of them is wrong. JAC-1 (Zac, 28/07) is "drafts only for now", and
Adam's own division of the roles on hub-68 is that Zac owns what Jacob is
allowed to do while Adam owns the pipeline. JACOB-SESSION.md section 2 is
explicit about what to do when the case for sending looks strong: raise a
request, do not decide it. That request is JAC-15. The moment it is answered
yes, one line of .env.jacob turns this on:

    JACOB_DAILY_EMAIL=on

and nothing else about the script changes. Until then `--send` prints the
refusal and the reason, and the message is written to disk for a human to
send or to read on the hub.

WHAT GOES IN IT. Leads whose next-chase date is today or has already passed -
that is all. Every exclusion Adam listed (opportunities, tender alerts,
pipeline totals, drafts, estimating, system warnings) is enforced here by the
email simply never being built from those sources.

WHAT IS DELIBERATELY LEFT OUT, and this is the one judgement call worth
knowing about. AdminBase carries 176 rows whose follow-up date is already in
the past, because it is a CRM nobody closes anything in - the date on those
was set by the system and not by a person. Mailing all 176 every morning is
the same as mailing none. So a CRM row reaches this email only once a human
has put a date on it, and the count of the ones held back is stated at the
foot of the message rather than hidden. `--all-crm` includes them, if Adam
decides that is what he wants.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

HANDOVER = os.path.join(REPO, "data", "jacob", "handover.json")
ADMINBASE = os.path.join(REPO, "data", "jacob", "adminbase.json")
SETTINGS = os.path.join(REPO, "data", "jacob", "email-settings.json")
OUT_DIR = os.path.join(REPO, "data", "jacob")
TO = ["adam@fensterglazing.com"]

TODAY = date.today().isoformat()

MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default


def read_env(path):
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8-sig"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def settings():
    """Adam, hub-74: 'If there are no leads due or overdue for chasing that
    day, Jacob should either send a brief email confirming that no lead chases
    are due, or send no email, depending on the system setting selected by
    Adam.' The setting is here so it is his to change and not mine to assume.

    The default is `confirm` on purpose. An empty inbox is the same shape
    whether nothing was due or the bot fell over three days ago, and a one-line
    'nothing due' is the only version of this that can be trusted."""
    s = load(SETTINGS) or {}
    s.setdefault("whenNothingDue", "confirm")   # confirm | silent
    s.setdefault("setBy", "default - not yet chosen by Adam (JAC-15)")
    return s


def nice(iso):
    if not iso or len(str(iso)) < 10:
        return "not recorded"
    try:
        d = date.fromisoformat(str(iso)[:10])
    except ValueError:
        return str(iso)
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def gbp(v):
    if not v:
        return "not recorded"
    return "GBP %s" % format(int(round(v)), ",")


def days_since(iso):
    try:
        return (date.fromisoformat(TODAY) - date.fromisoformat(str(iso)[:10])).days
    except (ValueError, TypeError):
        return None


# ------------------------------------------------------------- the overlay
def pipeline():
    """What a human has written on the board. This is the half of the truth
    that is not in any file in the repo: the date somebody set after a call,
    the owner they handed it to, the note of what was said. Without it the
    email would chase on the board's arithmetic and ignore the person who
    actually spoke to the client last."""
    env = read_env(os.path.join(REPO, ".env.jacob"))
    mary = read_env(os.path.join(REPO, ".env.mary"))
    key = env.get("MARY_API_KEY") or mary.get("MARY_API_KEY")
    base = env.get("DASHBOARD_URL") or mary.get("DASHBOARD_URL") \
        or "https://mary-dashboard.pages.dev"
    if not key:
        return {}, "no MARY_API_KEY - human-set dates and notes are NOT included"
    req = urllib.request.Request(base + "/api/jacob/pipeline")
    req.add_header("x-mary-key", key)
    req.add_header("user-agent", "JacobDailyEmail/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.loads(r.read().decode() or "[]")
    except (urllib.error.URLError, ValueError, OSError) as e:
        return {}, "the hub overlay could not be read (%s) - human-set dates " \
                   "and notes are NOT included" % e
    return {r["key"]: r for r in rows if r.get("key")}, None


SHUT = ("done", "dead")
DECIDED = ("won", "lost", "closed")


def rows_due(pipe, all_crm=False):
    """The same rule the Leads page uses, deliberately: a row is due when the
    date somebody set on it has arrived. Where the hub and the file disagree
    the hub wins - a human who has just spoken to the client knows something no
    file does."""
    hand = load(HANDOVER) or {}
    crm = load(ADMINBASE) or {}
    out, held_crm = [], 0

    def overlay(key):
        return pipe.get(key) or {}

    def pick(row, key, tier, client, job, value, quoted, last, stage, owner,
             nxt, derived_date, blocked=False, note=""):
        p = overlay(key)
        state = (p.get("state") or "").strip()
        if state in SHUT or state in DECIDED:
            return None
        human_date = (p.get("next_date") or "").strip()
        due = human_date or (derived_date or "")
        if not due or due > TODAY:
            return None
        if blocked and not human_date:
            # Blocked by something the client cannot control. Ringing them
            # about it wastes the relationship - Gordon Court, Brandon Estate.
            return None
        if tier == "adminbase" and not human_date and not all_crm:
            return "held"
        return {
            "key": key, "tier": tier, "client": client, "job": job,
            "value": value, "quoted": quoted,
            "lastContact": last,
            "stage": state or stage,
            "owner": (p.get("owner") or owner or "").strip() or "nobody",
            "next": (p.get("next_action") or nxt or "").strip(),
            "due": due,
            "dueSetBy": "a person" if human_date else "the register",
            "note": (p.get("note") or note or "").strip(),
            "overdueDays": max(0, (date.fromisoformat(TODAY)
                                   - date.fromisoformat(due)).days),
        }

    for r in hand.get("issued", []):
        blocked = bool((r.get("blockedUntil") and r["blockedUntil"] > TODAY)
                       or r.get("blockedPending"))
        got = pick(r, r["key"], "register", r.get("client"), r.get("job"),
                   r.get("value"), r.get("issued"), r.get("lastClientContact"),
                   r.get("state"), r.get("owner"), r.get("next"),
                   r.get("nextChase"), blocked, r.get("chaseNote", ""))
        if isinstance(got, dict):
            out.append(got)

    on_board = {(r.get("client") or "").lower() for r in hand.get("issued", [])}
    for r in crm.get("due", []):
        if r.get("onBoard") or (r.get("outlier") and not r.get("confirmed")):
            continue
        if (r.get("client") or "").lower() in on_board:
            continue
        got = pick(r, "ab:" + r["lead"], "adminbase", r.get("client"),
                   r.get("job"), r.get("value"),
                   (r.get("staleDate") or {}).get("issued") or r.get("leadDate"),
                   None, r.get("state"), r.get("owner"), r.get("next"),
                   r.get("nextAction"))
        if got == "held":
            held_crm += 1
        elif isinstance(got, dict):
            out.append(got)

    out.sort(key=lambda r: (-r["overdueDays"], -(r["value"] or 0)))
    return out, held_crm


# ------------------------------------------------------------- the message
def build(rows, held_crm, warning=None):
    """Adam's format, hub-74, to the line. Nothing is added to it: no totals,
    no opportunities, no commentary. The only line that is not in his template
    is the one that says what was held back, and that is there because a list
    that does not say what it left out reads as the whole list."""
    d = date.fromisoformat(TODAY)
    subject = "Fenster Leads to Chase – %d %s %d" % (d.day, MONTHS[d.month - 1], d.year)

    if not rows:
        body = ("Adam,\n\nNo quoted leads are due or overdue for chasing today.\n")
    else:
        body = "Adam,\n\nThe following quoted leads require action today:\n\n"
        for r in rows:
            last = ("%s%s" % (nice(r["lastContact"]),
                              " - %s" % r["note"] if r["note"] else ""))
            if not r["lastContact"]:
                last = (r["note"] or "nothing back from them since the quote went out")
            body += (
                "%s – %s\n"
                "Owner: %s\n"
                "Current stage: %s\n"
                "Last contact: %s\n"
                "Next action: %s\n"
                "Deadline: %s\n"
                "Quote value: %s\n\n"
                % (r["client"] or "client not named", r["job"] or "no site recorded",
                   r["owner"], r["stage"] or "quoted", last,
                   r["next"] or "NOT SET - this lead has no next action written on it",
                   "%s%s" % (nice(r["due"]),
                             " (%d days overdue)" % r["overdueDays"]
                             if r["overdueDays"] else " (today)"),
                   gbp(r["value"])))

    tail = []
    if held_crm:
        tail.append("%d AdminBase rows carry a follow-up date the CRM set that has "
                    "already passed. They are not listed here because the date on "
                    "them was not set by a person. They are on the Leads page, and "
                    "any one of them appears in this email the day somebody puts a "
                    "date on it." % held_crm)
    if warning:
        tail.append("Warning: %s." % warning)
    if tail:
        body += "\n" + "\n\n".join(tail) + "\n"
    return subject, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true",
                    help="send it - refused unless JACOB_DAILY_EMAIL=on")
    ap.add_argument("--json", action="store_true", help="print the selected rows")
    ap.add_argument("--all-crm", action="store_true",
                    help="include AdminBase rows whose date only the CRM set")
    args = ap.parse_args()

    pipe, warning = pipeline()
    rows, held = rows_due(pipe, all_crm=args.all_crm)
    subject, body = build(rows, held, warning)
    cfg = settings()

    silent = not rows and cfg["whenNothingDue"] == "silent"
    record = {
        "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "for": TODAY, "to": TO, "subject": subject, "body": body,
        "rows": rows, "heldBackCrmRows": held,
        "whenNothingDue": cfg["whenNothingDue"],
        "wouldSend": (not silent),
        "sent": False,
        "authorised": False,
        "authority": ("Adam, hub-74, 29/07/2026 - one daily lead-chasing email to "
                      "adam@fensterglazing.com and no other outbound. Gated on "
                      "JAC-15 because JAC-1 (Zac, 28/07) is drafts-only and "
                      "loosening it is Zac's call, not mine."),
        "warning": warning,
    }

    if args.json:
        print(json.dumps(record, indent=1, ensure_ascii=False))
        return 0

    with open(os.path.join(OUT_DIR, "daily-email.json"), "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, ensure_ascii=False)

    # The subject carries an en dash because Adam's format does. This console
    # is cp1252, so print through the terminal's own encoding rather than let
    # a correct email die on its own preview.
    def show(s):
        enc = sys.stdout.encoding or "utf-8"
        print(s.encode(enc, "replace").decode(enc, "replace"))

    show("To: %s" % ", ".join(TO))
    show("Subject: %s" % subject)
    print()
    show(body)
    print("-" * 60)
    print("%d lead(s) due or overdue; %d AdminBase rows held back." % (len(rows), held))
    if silent:
        print("Nothing is due and the setting is 'silent', so no email would go "
              "out today. Change it in data/jacob/email-settings.json.")
    if warning:
        print("WARNING: %s" % warning)

    if args.send:
        env = read_env(os.path.join(REPO, ".env.jacob"))
        if (env.get("JACOB_DAILY_EMAIL") or "").lower() != "on":
            print()
            print("NOT SENT. Adam authorised this email on hub-74; JAC-1 (Zac, "
                  "28/07) says drafts only, and on Adam's own split of the roles "
                  "(hub-68) whether Jacob sends anything at all is Zac's call. "
                  "JAC-15 asks him. Until it is answered yes and "
                  "JACOB_DAILY_EMAIL=on is in .env.jacob, this refuses - and it "
                  "refuses rather than asking, because a boundary you can talk "
                  "your way past is not one.")
            return 2
        if silent:
            print("Nothing due and the setting is 'silent' - nothing sent.")
            return 0
        import jacob_graph
        token = jacob_graph.get_token(jacob_graph.load_env(), "SENDER")
        st, res = jacob_graph.send_mail(token, TO, subject, body)
        record["sent"] = st in (200, 202)
        record["authorised"] = True
        record["sendResult"] = st
        with open(os.path.join(OUT_DIR, "daily-email.json"), "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=1, ensure_ascii=False)
        print("send: %s %s" % (st, res))
        return 0 if st in (200, 202) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

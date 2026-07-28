# -*- coding: utf-8 -*-
"""JACOB WRIGHT - business development. Builds his half of the hub.

Reads what we already have (Contracts Finder awards + the OneDrive client
archive), cross-references them, and writes
`dashboard/functions/_data/jacob-data.js`.

  python scripts/jacob_dashboard.py            # rebuild the data file
  python scripts/jacob_dashboard.py --deploy   # rebuild and push to Pages

Mary's generator (`mary_dashboard.py`) is untouched and owns
`dashboard-data.js`. The two write different files and never read each
other's - the only shared thing is the Pages project they deploy to.

Sections marked "planned" in SOURCES/pages are deliberate placeholders: the
feed is not wired yet and the hub says so rather than showing a fake zero.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AWARDS = os.path.join(REPO, "data", "jacob", "contracts-finder-awards.json")
INTAKE = os.path.join(REPO, "data", "jacob", "intake.json")
JAYK = os.path.join(REPO, "data", "jacob", "jayk-recovery.json")
JOBS = os.path.join(REPO, "data", "jobs")
OUT = os.path.join(REPO, "dashboard", "functions", "_data", "jacob-data.js")

ARCHIVE = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial"
TENDER_DIR = os.path.join(ARCHIVE, "1. Tender Documents")
PROJECT_DIR = os.path.join(ARCHIVE, "2. Projects")
COMPLETED_DIR = os.path.join(PROJECT_DIR, "2. Completed")

TODAY = date.today().isoformat()
STALE_BEFORE = "2026-01-28"          # 180 days - award notices publish late

SUFFIXES = {"LIMITED", "LTD", "PLC", "LLP", "LP", "UK", "THE", "CO", "COMPANY",
            "HOLDINGS", "INC", "CIC", "CIO"}
NOT_CLIENTS = {"1. MASTER", "2. COMPLETED"}

# What the contract IS, not what its title says. Keyword matching does not
# work here: "window" catches window cleaning, "screen" catches STI
# screening, and one award matched only on "the front door to maternity
# services" - a metaphor. 26% of CPV-45 awards are highways.
BUILDING_CPV = ("45210", "45211", "45212", "45213", "45214", "45215", "45216",
                "45262", "45261", "45453", "45454", "4542", "4544", "4545",
                "44221")
INFRA_CPV = ("45233", "45231", "45232", "45234", "45235", "45236", "45246",
             "45247", "45112", "45111", "45331", "45230", "45310", "45350")
MIN_VALUE, MAX_VALUE = 400_000, 40_000_000

# Adam, 27/07/2026: many quotes, no wins. Their notices stay on the board so
# nobody quietly re-opens the question, but they carry no action.
DO_NOT_QUOTE = re.compile(r"hightown", re.I)

# The supplier stopgap that used to live here has gone. It was correcting
# the enquiry count downstream, which meant anything else reading
# intake.json still got the inflated number. jacob_intake.py now reads the
# first sentence of each message and settles the direction of the ask at
# source, so this file can trust the kind it is given.

# Who does the next thing. Nothing goes on the board without one of these.
ADAM, JACOB, GINTARE, ZAC, NOBODY = "Adam", "Jacob", "Gintare", "Zac", "-"


# ---------------------------------------------------------------- matching
def norm(s):
    s = (s or "").upper().replace("&", " AND ")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(s):
    return [t for t in norm(s).split() if t not in SUFFIXES]


def match(sup, cli):
    """Conservative. Single common words like 'Atlas' throw false positives,
    so those land in 'possible' and a human confirms them once."""
    if not sup or not cli:
        return None
    if sup == cli:
        return "exact"
    ss, cs = set(sup), set(cli)
    if cs <= ss:
        if max(len(t) for t in cli) >= 5 or len(cli) >= 2:
            return "strong"
        return None
    if ss <= cs and max(len(t) for t in sup) >= 6:
        return "strong"
    if sup[0] == cli[0] and len(cli[0]) >= 7:
        return "possible"
    return None


def load_clients():
    """Every company Fenster has quoted, flagged by whether they ever bought."""
    out = {}
    for path, tier in ((TENDER_DIR, "quoted"), (PROJECT_DIR, "won"),
                       (COMPLETED_DIR, "won")):
        if not os.path.isdir(path):
            continue
        for raw in sorted(os.listdir(path)):
            if raw.upper() in NOT_CLIENTS or raw.lower().endswith(
                    (".docx", ".xlsx", ".pdf")):
                continue
            if not os.path.isdir(os.path.join(path, raw)):
                continue
            tk = tokens(raw)
            if not tk or (re.match(r"^\d", raw) and len(tk) > 2):
                continue
            out[raw] = "won" if tier == "won" or out.get(raw) == "won" else "quoted"
    return out


def is_fresh(a):
    """Only a lead if the award is recent AND the job is still running.
    One notice was published 469 days after the award, on a contract that had
    already finished - publication date is not the award date."""
    d = a.get("award_date") or a.get("published") or ""
    if d and d < STALE_BEFORE:
        return False
    end = a.get("end") or ""
    return not (end and end < TODAY)


def is_building(a):
    codes = a.get("cpv_all") or ([a["cpv"]] if a.get("cpv") else [])
    if any(str(c).startswith(INFRA_CPV) for c in codes):
        return False
    if any(str(c).startswith(BUILDING_CPV) for c in codes):
        return True
    return bool(any(str(c).startswith("45") for c in codes) and a.get("build_signal"))


def area(pcs):
    out = {m.group(1) for m in
           (re.match(r"^([A-Z]{1,2})\d", (p or "").replace(" ", "")) for p in pcs or [])
           if m}
    return ",".join(sorted(out)[:3])


def lead(a, extra=None):
    row = {
        "supplier": a["supplier"],
        "title": a["title"][:110],
        "buyer": a.get("buyer", "")[:70],
        "value": a.get("value"),
        "area": area(a.get("postcodes")),
        "awarded": a.get("award_date") or a.get("published"),
        "start": a.get("start"), "end": a.get("end"),
        "url": a.get("url"),
        "cpv": a.get("cpv_desc", ""),
    }
    row.update(extra or {})
    return row


# Consumer mail is a person, not an account. Kept out of the company list on
# both paths - intake filters it too, but Jayk's contacts come in separately.
FREEMAIL = {"hotmail.com", "hotmail.co.uk", "gmail.com", "googlemail.com",
            "outlook.com", "outlook.co.uk", "yahoo.com", "yahoo.co.uk",
            "live.com", "live.co.uk", "aol.com", "icloud.com", "me.com",
            "msn.com", "btinternet.com", "sky.com", "virginmedia.com",
            "talktalk.net", "protonmail.com"}


FREEMAIL_STEMS = {"hotmail", "gmail", "googlemail", "outlook", "yahoo", "live",
                  "aol", "icloud", "me", "msn", "btinternet", "sky",
                  "virginmedia", "talktalk", "protonmail", "ymail", "gmx",
                  "mail", "inbox", "rediffmail"}


def is_freemail(domain):
    """Match on the first label so outlook.in and yahoo.de are caught too,
    not just the .com/.co.uk pair."""
    return (domain or "").lower().split(".")[0] in FREEMAIL_STEMS


def load_json(path, default=None):
    """Optional inputs - a missing feed shows as 'not run yet' on the hub
    rather than taking the whole board down."""
    try:
        return json.load(open(path, encoding="utf-8"))
    except (IOError, ValueError):
        return default


def build_relationships(clients, intake, jayk):
    """One row per company, merged from the three things we know:

      the archive   - every company Fenster has ever quoted, and who bought
      the mailboxes - who is emailing right now, and about what
      Jayk's threads- who the former BDM was dealing with before he left

    A company that appears in the archive but has had no email for a year is
    exactly the dormant lead Jacob exists to surface, so absence matters as
    much as presence."""
    rows = {}

    def row(key, label):
        return rows.setdefault(key, {
            "company": label, "domain": "", "relationship": "unknown",
            "lastContact": "", "messages": 0, "contacts": [],
            "sources": [], "subjects": [],
        })

    for name, tier in clients.items():
        r = row(re.sub(r"[^a-z0-9]", "", name.lower())[:24] or name, name)
        r["relationship"] = tier
        r["sources"].append("archive")

    for c in (intake or {}).get("companies", []):
        # Personal addresses are people, not accounts - their enquiries still
        # show as signals, they just do not become a company row.
        if c.get("isFreemail"):
            continue
        key = re.sub(r"[^a-z0-9]", "",
                     re.sub(r"\.(co\.uk|com|net|org|uk)$", "", c["domain"]))[:24]
        r = row(key, c["domain"])
        r["domain"] = c["domain"]
        r["messages"] += c["messages"]
        r["lastContact"] = max(r["lastContact"], c["last"])
        r["contacts"].extend(c["contacts"])
        r["subjects"].extend(c.get("subjects", []))
        if c["relationship"] != "unknown":
            r["relationship"] = c["relationship"]
        if "mailbox" not in r["sources"]:
            r["sources"].append("mailbox")

    for addr, n, name in (jayk or {}).get("contacts", []):
        dom = addr.split("@")[-1]
        if is_freemail(dom):
            continue
        key = re.sub(r"[^a-z0-9]", "",
                     re.sub(r"\.(co\.uk|com|net|org|uk)$", "", dom))[:24]
        r = row(key, dom)
        r["domain"] = r["domain"] or dom
        if not any(c["address"] == addr for c in r["contacts"]):
            r["contacts"].append({"address": addr, "name": name})
        if "jayk" not in r["sources"]:
            r["sources"].append("jayk")

    # An archive folder ("Borras") and a mailbox domain ("borrasconstruction
    # .co.uk") are the same company. Keeping them apart is how a client who
    # emailed us yesterday appears on the board as dormant, and how forty
    # dormant clients end up with no contact address between them.
    #
    # Containment only, and only on stems of six characters or more - a
    # three-letter folder name inside a domain is a coincidence waiting to
    # happen, and a wrong merge here puts the wrong person's name on a lead.
    keys = sorted(rows, key=len)
    for short in list(keys):
        if len(short) < 6 or short not in rows:
            continue
        src = rows[short]
        if "archive" not in src["sources"] or src["lastContact"]:
            continue
        for long in keys:
            if long == short or long not in rows or short not in long:
                continue
            dst = rows[long]
            if "mailbox" not in dst["sources"] and "jayk" not in dst["sources"]:
                continue
            # The archive knows the trading name; the mailbox only knows a
            # domain. Keep the name and take everything else.
            dst["company"] = src["company"]
            dst["relationship"] = src["relationship"]
            dst["sources"] = sorted(set(dst["sources"] + src["sources"]))
            del rows[short]
            break

    out = list(rows.values())
    # Most recently active first, then the ones we have most history with.
    out.sort(key=lambda r: (r["lastContact"], len(r["contacts"])), reverse=True)
    return out


# ------------------------------------------------------- threads and states
def thread_key(subject):
    """One conversation, not one email. Six 'RE: Touchwood glass quote'
    messages are one thing to do, and counting them six times is how a board
    ends up claiming 61 enquiries when it is holding about a dozen."""
    s = re.sub(r"^((re|fw|fwd|aw|tr)\s*[:\-]\s*)+", "", (subject or "").strip(), flags=re.I)
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()[:70]


def days_since(iso):
    try:
        return (date.fromisoformat(TODAY) - date.fromisoformat(iso)).days
    except ValueError:
        return 999


def state_for(days):
    """What a human means by 'where is this'. Deliberately coarse - the only
    question that matters is whether it needs touching today."""
    if days <= 3:
        return "live"
    if days <= 10:
        return "waiting"
    if days <= 30:
        return "gone quiet"
    return "stale"


def thread_kind(company, subject, relationship):
    if relationship == "individual":
        return "domestic"
    if relationship == "supplier":
        return "supplier"
    return "buyer"


EMAIL = re.compile(r"[a-z0-9][\w.+-]*@[a-z0-9][\w-]*\.[a-z][\w.]*[a-z]", re.I)


def load_job_contacts():
    """Who Mary is already pricing for. Her job files name the estimator the
    quotation goes to, so an exact address match answers a question Jacob
    otherwise has to ask her: is this enquiry already in hand?

    Exact addresses only. Company-name matching is what put a window-cleaning
    contractor on this board under the name Atlas."""
    out = {}
    if not os.path.isdir(JOBS):
        return out
    for name in sorted(os.listdir(JOBS)):
        if not name.endswith(".md") or name.lower() == "readme.md":
            continue
        try:
            txt = open(os.path.join(JOBS, name), encoding="utf-8",
                       errors="replace").read()
        except OSError:
            continue
        for addr in EMAIL.findall(txt):
            addr = addr.lower()
            if addr.endswith("@fensterglazing.com"):
                continue
            out.setdefault(addr, name[:-3])
    return out


# A date somebody has actually written down. Stepnell asked for a quotation
# "by 30th July" and the board ranked it thirteenth, because age was the
# only thing it knew how to sort on and the thread had gone quiet. Quiet is
# exactly what a tender return does before it closes.
MONTHS = {m: i + 1 for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"))}

DEADLINE_NUM = re.compile(
    r"\b(?:by|before|due (?:by|on)|close[sd]? on|closing on|return(?:ed)? by|"
    r"return date[^.]{0,30}?)\s*(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b", re.I)

DEADLINE_WORD = re.compile(
    r"\b(?:by|before|due (?:by|on)|close[sd]? on|closing on|return(?:ed)? by)\s+"
    r"(?:the\s+)?(\d{1,2})(?:st|nd|rd|th)?\s+"
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\b", re.I)


def find_deadline(text):
    """The date a price has to be in by, when someone has stated one. Only
    explicit dates - "Tuesday afternoon latest" is not one, and a guess here
    would be worse than the blank."""
    best = None
    for m in DEADLINE_NUM.finditer(text or ""):
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y += 2000 if y < 100 else 0
        try:
            iso = date(y, mo, d).isoformat()
        except ValueError:
            continue
        if iso >= TODAY and (best is None or iso < best):
            best = iso
    for m in DEADLINE_WORD.finditer(text or ""):
        d, mo = int(m.group(1)), MONTHS[m.group(2).lower()]
        year = date.fromisoformat(TODAY).year
        for y in (year, year + 1):
            try:
                iso = date(y, mo, d).isoformat()
            except ValueError:
                continue
            if iso >= TODAY:
                if best is None or iso < best:
                    best = iso
                break
    return best


# "Sales", "Enquiries", "Orders" is a mailbox, not a person. Calling one of
# those and asking for them by name is how you sound like a robot.
GENERIC_NAME = re.compile(r"^(sales|enquiries|enquiry|info|orders|accounts|"
                          r"admin|estimating|office|team|support|cd\.orders)\b", re.I)


def person(t):
    n = (t["name"] or "").strip()
    if not n or GENERIC_NAME.match(n) or "@" in n:
        return ""
    return n.split("|")[0].strip()


def thread_action(t):
    """Every row gets a next action and a name against it, or it is trivia.

    The honest first question on any inbound enquiry is *has anyone answered
    it* - and Jacob cannot see that. Intake reads received mail only, so a
    thread where Gintare replied an hour ago looks identical to one nobody
    has touched. The action says so rather than pretending, and JAC-5 asks
    for the sent-items scope that would fix it."""
    who = person(t)
    co = t["company"]
    at = ("%s at %s" % (who, co)) if who else co
    # A date somebody wrote down outranks everything else on the row.
    due = t.get("daysToDeadline")
    if due is not None and due <= 21 and not DO_NOT_QUOTE.search(t["subject"] + co):
        when = ("today" if due == 0 else "tomorrow" if due == 1
                else "in %d days" % due)
        # Mary may already have it. Telling Adam to send her a pack she
        # priced last week is how a board loses the room.
        if t.get("job"):
            return (ADAM, "%s wants a price by %s - that is %s. Mary has this one "
                          "(job file '%s'); the only question left is whether it "
                          "goes out in time." % (at, t["deadline"], when, t["job"]))
        if t["kind"] in ("portal", "supplier"):
            return (JACOB, "Pull the pack and get it to Mary - it closes %s, %s."
                    % (when, t["deadline"]))
        return (ADAM, "%s wants a price by %s - that is %s. Nothing in Mary's job "
                      "files matches this address, so assume nobody has started."
                % (at, t["deadline"], when))
    if t["kind"] == "portal":
        if DO_NOT_QUOTE.search(t["subject"] + co):
            return (NOBODY, "Nothing. Adam ruled Hightown out on 27/07 - many quotes, "
                            "no wins. Left on the board so the question is not re-opened.")
        return (JACOB, "Pull the pack off the portal, check the return date, hand it to Mary.")
    if t["kind"] == "supplier":
        return (NOBODY, "None. This is a price coming back to Fenster, not an enquiry.")
    if t["kind"] == "domestic":
        return (GINTARE, "Small works, not BD. Listed so nobody counts it as a lead.")
    # Buyer. A price already with them is a different job from a new ask:
    # this is the second handover, the one that currently nobody does.
    if t["stage"] == "quoted":
        if t["state"] in ("gone quiet", "stale"):
            return (ADAM, "Chase %s for a decision. Fenster's price has been with "
                          "them %d days with nothing back." % (at, t["days"]))
        return (ADAM, "Fenster has priced this and %s is deciding. They wrote %s - "
                      "worth a call before it goes quiet."
                % (at, "today" if t["days"] == 0 else
                   "yesterday" if t["days"] == 1 else "%d days ago" % t["days"]))
    if t["stage"] == "unconfirmed":
        return (JACOB, "Read the thread from %s before anyone acts. The subject "
                       "looked like an enquiry; the first line did not say either "
                       "way." % at)
    if t["state"] in ("gone quiet", "stale"):
        return (ADAM, "Chase %s - %d days since they last wrote and nothing since. "
                      "Either it went cold or the reply never went out." % (at, t["days"]))
    if t["relationship"] == "won":
        return (ADAM, "Call %s. They have bought from Fenster before and they are asking "
                      "again - that is the best call on this board." % at)
    if t["relationship"] == "quoted":
        return (ADAM, "Call %s. Fenster has priced for them before and never won. "
                      "This is the second chance." % at)
    return (ADAM, "Check commercial@ for a reply to %s, then call them. %d message%s in "
                  "and no history with them at all." % (at, t["messages"],
                                                        "" if t["messages"] == 1 else "s"))


def thread_unknowns(t):
    """Say what you do not know. A blank is honest; a confident guess is not."""
    out = []
    if t["kind"] == "buyer":
        out.append("Whether anyone at Fenster has already replied - Jacob reads "
                   "received mail only (JAC-5).")
        if t["relationship"] == "unknown":
            out.append("Whether they are a buyer or another supplier. No archive "
                       "folder and no history in any mailbox - worth one look before "
                       "Adam calls.")
        if not person(t):
            out.append("Who to ask for. The mail came from a shared address, not a person.")
    return out


def build_threads(intake):
    """Signals -> conversations -> things to do."""
    jobs = load_job_contacts()
    by_key = {}
    for s in (intake or {}).get("signals", []):
        key = "%s|%s" % (s["company"], thread_key(s["subject"]))
        t = by_key.setdefault(key, {
            "key": "thread:" + re.sub(r"[^a-z0-9]", "-", key.lower())[:60],
            "company": s["company"], "contact": s["contact"], "name": s.get("name") or "",
            "subject": s["subject"], "mailbox": s["mailbox"],
            "relationship": s.get("relationship", "unknown"),
            "first": s["date"], "last": s["date"], "messages": 0,
        })
        t["messages"] += 1
        t["first"] = min(t["first"], s["date"])
        t["last"] = max(t["last"], s["date"])
        t.setdefault("kinds", set()).add(s["kind"])
        t.setdefault("text", []).append("%s %s" % (s["subject"], s.get("preview") or ""))
        if not t["name"] and s.get("name"):
            t["name"] = s["name"]

    out = []
    for t in by_key.values():
        kinds = t.pop("kinds", set())
        t["job"] = jobs.get((t["contact"] or "").lower())
        t["deadline"] = find_deadline(" ".join(t.pop("text", [])))
        t["daysToDeadline"] = -days_since(t["deadline"]) if t["deadline"] else None
        t["days"] = days_since(t["last"])
        t["state"] = state_for(t["days"])
        t["kind"] = "portal" if "portal" in kinds else \
            thread_kind(t["company"], t["subject"], t["relationship"])
        # How far along it is, which is a different question from how old it
        # is. A price already sitting with the client is the one thing on
        # this board nobody was tracking.
        t["stage"] = ("quoted" if "quote-out" in kinds else
                      "enquiry" if "enquiry" in kinds else "unconfirmed")
        # A stated return date beats how old the thread is. "Gone quiet" is
        # what a tender does in the fortnight before it closes.
        if t["daysToDeadline"] is not None and t["daysToDeadline"] <= 21:
            t["state"] = "closes %s" % t["deadline"]
        # "3 days old" is not the state of a Hightown notice. The state is that
        # Adam has ruled them out, and a date-based chip hides that.
        if DO_NOT_QUOTE.search(t["company"] + t["subject"]):
            t["state"] = "do not quote"
        t["owner"], t["next"] = thread_action(t)
        t["person"] = person(t)
        t["unknowns"] = thread_unknowns(t)
        out.append(t)
    out.sort(key=lambda t: (t["last"], t["messages"]), reverse=True)
    return out


def lead_action(row, tier):
    """An award notice is a company, not a lead, until somebody is going to
    do something about it."""
    co = row.get("client") or row["supplier"]
    if row.get("confidence") == "possible":
        return (JACOB, "Confirm this is the same %s before anyone calls - single-word "
                       "names throw false positives." % co)
    if tier == "warm":
        return (ADAM, "Call %s. They have bought from Fenster and they have just won "
                      "%s - get on the enquiry list before it is drawn up." % (co, row["title"][:60]))
    if tier == "known":
        return (JACOB, "Draft an intro for Adam to send to %s - quoted before, never "
                       "won, and they are building again." % co)
    return (NOBODY, "Blocked. Cold contact needs JAC-2 answered and a sending domain.")


def book_state(r):
    """One state per company. 'If you cannot say which, the row is not
    finished' - so unknown is a state too, and it says so."""
    if r["relationship"] == "supplier":
        return "supplier"
    if DO_NOT_QUOTE.search(r["company"] + r.get("domain", "")):
        return "do not quote"
    if r["lastContact"]:
        return state_for(days_since(r["lastContact"]))
    if r["relationship"] == "won":
        return "dormant - has bought"
    if r["relationship"] == "quoted":
        return "dormant - quoted only"
    return "no contact on record"


def book_action(r):
    st = r["state"]
    if st == "supplier":
        return (NOBODY, "None. Supplier, not a customer.")
    if st == "do not quote":
        return (NOBODY, "Nothing. Adam ruled them out 27/07.")
    who = next((c.get("name") or c["address"] for c in r["contacts"]
                if c.get("name") and "@" not in c.get("name", "@")), None)
    if st == "dormant - has bought":
        if who:
            return (JACOB, "Draft a note to %s for Adam to send. They have paid Fenster "
                           "before and nobody has emailed them in 180 days." % who)
        if r["contacts"]:
            return (JACOB, "Draft a note to %s for Adam to send - paid customer, silent "
                           "180 days." % r["contacts"][0]["address"])
        return (JACOB, "Find a contact first. The archive has a folder with their name "
                       "on it and no address in it - there is nobody here to write to.")
    if st == "dormant - quoted only":
        if not r["contacts"]:
            return (NOBODY, "Nothing to do - folder in the archive, no address anywhere. "
                            "Becomes a lead the day one of their schemes shows up.")
        return (JACOB, "Worth one email to %s if a scheme of theirs shows up. Not worth "
                       "a cold call on its own." % (who or r["contacts"][0]["address"]))
    if st in ("gone quiet", "stale"):
        return (ADAM, "Last heard from them %s. One call answers whether they are "
                      "still live." % r["lastContact"])
    return (NOBODY, "Talking to us already - nothing to start.")


def build_actions(threads, warm, known, book):
    """The list a Commercial Director reads in ten seconds. Ranked by how
    close it is to a real enquiry from a real buyer, which is the only thing
    Jacob is for."""
    acts = []

    def add(score, key, company, headline, what, owner, nxt, state, page):
        acts.append({"score": score, "key": key, "company": company,
                     "headline": headline, "what": what, "owner": owner,
                     "next": nxt, "state": state, "page": page})

    for t in threads:
        if t["owner"] == NOBODY:
            continue
        if t["kind"] == "buyer":
            base = 100 if t["relationship"] in ("won", "quoted") else 78
            if t["state"] in ("gone quiet", "stale"):
                base -= 25
            # A price already out ranks below a fresh ask, and a thread Jacob
            # has not read yet ranks below both - it is not a lead until
            # somebody has confirmed it is one.
            if t["stage"] == "quoted":
                base -= 6
            elif t["stage"] == "unconfirmed":
                base -= 30
            # A stated return date is the only hard fact on the row. Nothing
            # without one should sit above something that closes this week.
            due = t.get("daysToDeadline")
            if due is not None and due <= 21:
                base = max(base, 118 - due)
            # A shared mailbox is not a person. Leading with "sales@..." as
            # though it were a name is how a board starts sounding fake.
            add(base + min(t["messages"], 8), t["key"], t["company"],
                t["person"] or t["company"], t["subject"], t["owner"], t["next"],
                t["state"], "enquiries")
        elif t["kind"] == "portal":
            add(74, t["key"], t["company"], "Portal notice", t["subject"],
                t["owner"], t["next"], t["state"], "enquiries")

    for r in warm[:6]:
        add(55, "lead:" + re.sub(r"[^a-z0-9]", "-", r["supplier"].lower())[:50],
            r["client"], r["supplier"], "%s - %s" % (r["title"], gbp(r["total"] or r["value"])),
            r["owner"], r["next"], "award won " + (r["awarded"] or ""), "leads")

    for r in [x for x in book if x["state"] == "dormant - has bought"][:5]:
        add(32, "co:" + x_key(r), r["company"], r["company"],
            "Has bought from Fenster. No email in the 180-day window.",
            r["owner"], r["next"], r["state"], "companies")

    for r in known[:4]:
        add(22, "lead:" + re.sub(r"[^a-z0-9]", "-", r["supplier"].lower())[:50],
            r["client"], r["supplier"], "%s - %s" % (r["title"], gbp(r["total"] or r["value"])),
            r["owner"], r["next"], "award won " + (r["awarded"] or ""), "leads")

    acts.sort(key=lambda a: -a["score"])
    # Two award notices against the same client collapse to one thing to do.
    seen, out = set(), []
    for a in acts:
        sig = (a["company"], a["next"])
        if sig in seen:
            continue
        seen.add(sig)
        out.append(a)
    return out[:14]


def x_key(r):
    return re.sub(r"[^a-z0-9]", "-", (r.get("domain") or r["company"]).lower())[:50]


def gbp(v):
    if not v:
        return "value not published"
    if v >= 1e6:
        return "GBP %.1fm" % (v / 1e6)
    return "GBP %s" % format(int(round(v)), ",")


# ---------------------------------------------------------------- build
def build():
    awards = json.load(open(AWARDS, encoding="utf-8"))
    clients = load_clients()
    cli_tok = {c: tokens(c) for c in clients}

    by_supplier = defaultdict(list)
    for a in awards:
        if a.get("supplier"):
            by_supplier[a["supplier"]].append(a)

    warm, known, seen = [], [], set()
    for sup, rows in by_supplier.items():
        st = tokens(sup)
        live = [r for r in rows if is_fresh(r)]
        if not live:
            continue
        for cli, ct in cli_tok.items():
            conf = match(st, ct)
            if not conf or (sup, cli) in seen:
                continue
            seen.add((sup, cli))
            top = sorted(live, key=lambda r: r.get("value") or 0, reverse=True)[0]
            row = lead(top, {"client": cli, "confidence": conf,
                             "n": len(live),
                             "total": sum(r.get("value") or 0 for r in live)})
            (warm if clients[cli] == "won" else known).append(row)

    matched = {r["supplier"] for r in warm + known}
    cold_by = defaultdict(list)
    for a in awards:
        if not a.get("supplier") or a["supplier"] in matched:
            continue
        if not is_building(a) or not is_fresh(a):
            continue
        v = a.get("value") or 0
        if v and not (MIN_VALUE <= v <= MAX_VALUE):
            continue
        cold_by[a.get("supplier_id") or a["supplier"]].append(a)

    cold = []
    for rows in cold_by.values():
        top = sorted(rows, key=lambda r: r.get("value") or 0, reverse=True)[0]
        cold.append(lead(top, {"n": len(rows),
                               "total": sum(r.get("value") or 0 for r in rows)}))

    order = {"exact": 0, "strong": 1, "possible": 2}
    warm.sort(key=lambda r: (order[r["confidence"]], -(r["total"] or 0)))
    known.sort(key=lambda r: (order[r["confidence"]], -(r["total"] or 0)))
    cold.sort(key=lambda r: -(r["total"] or 0))

    won = sum(1 for v in clients.values() if v == "won")

    for tier, rows in (("warm", warm), ("known", known), ("cold", cold)):
        for r in rows:
            r["owner"], r["next"] = lead_action(r, tier)
            r["key"] = "lead:" + re.sub(r"[^a-z0-9]", "-", r["supplier"].lower())[:50]

    intake = load_json(INTAKE)
    jayk = load_json(JAYK)
    rel = build_relationships(clients, intake, jayk)
    for r in rel:
        r["key"] = "co:" + x_key(r)
        r["state"] = book_state(r)
        r["owner"], r["next"] = book_action(r)

    # Dormant = we have quoted them, and no email in the window. That is the
    # cheapest lead in the business: they already asked us for a price once.
    dormant = [r for r in rel if r["state"].startswith("dormant")]
    dormantWon = [r for r in rel if r["state"] == "dormant - has bought"]

    threads = build_threads(intake)
    buyers = [t for t in threads if t["kind"] == "buyer"]
    liveBuyers = [t for t in buyers if t["state"] in ("live", "waiting")]
    quiet = [t for t in buyers if t["state"] in ("gone quiet", "stale")]
    actions = build_actions(threads, warm, known, rel)

    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "today": TODAY,
        "window": {"from": "2026-04-28", "to": "2026-07-27", "days": 90},
        "totals": {
            "awardRows": len(awards),
            "winners": len(by_supplier),
            "clients": len(clients),
            "clientsWon": won,
            "warm": len(warm), "known": len(known), "cold": len(cold),
            "signals": len((intake or {}).get("signals", [])),
            "mailboxCompanies": len((intake or {}).get("companies", [])),
            "dormant": len(dormant),
            "dormantWon": len(dormantWon),
            "jaykContacts": len((jayk or {}).get("contacts", [])),
            # What the board is actually holding, after the duplicates and the
            # suppliers come out. These are the numbers on the Today page.
            "threads": len(threads),
            "buyers": len(buyers),
            "liveBuyers": len(liveBuyers),
            "quietBuyers": len(quiet),
            "domestic": sum(1 for t in threads if t["kind"] == "domestic"),
            "supplierThreads": sum(1 for t in threads if t["kind"] == "supplier"),
            "portalThreads": sum(1 for t in threads if t["kind"] == "portal"),
            # A price already issued and sitting with the client. Nobody at
            # Fenster currently owns chasing these.
            "quotedOut": sum(1 for t in buyers if t["stage"] == "quoted"),
            "unconfirmed": sum(1 for t in threads if t["stage"] == "unconfirmed"),
            "smallWorks": ((intake or {}).get("counts", {}) or {}).get("small-works", 0),
            # The one money number on the board that is sourced, not guessed:
            # published values of live contracts whose winner Fenster knows.
            "knownWinnerValue": sum((r.get("total") or 0) for r in warm + known),
        },
        "actions": actions,
        "threads": threads,
        "warm": warm, "known": known, "cold": cold[:150],
        "sources": SOURCES(len(awards), len(by_supplier), intake),
        "intake": {
            "updated": (intake or {}).get("updated"),
            "windowDays": (intake or {}).get("window_days"),
            "perMailbox": (intake or {}).get("per_mailbox", {}),
            "counts": (intake or {}).get("counts", {}),
            "signals": (intake or {}).get("signals", [])[:120],
        } if intake else None,
        "jayk": {
            "messages": sum(v["he_was_on"] for v in (jayk or {}).get("per_mailbox", {}).values()
                            if isinstance(v, dict)),
            "companies": (jayk or {}).get("companies", [])[:40],
            "contacts": (jayk or {}).get("contacts", [])[:60],
            "subjects": sorted((jayk or {}).get("subjects", []), reverse=True)[:40],
        } if jayk else None,
        "relationships": {
            "quoted": len(clients) - won,
            "won": won,
            # Ordered by what a human would do with the row, not by date. The
            # 300 cap used to cut off exactly the dormant clients who had
            # bought - the most valuable rows in the file - because they are
            # by definition the ones with no recent email.
            "rows": sorted(rel, key=lambda r: (BOOK_ORDER.get(r["state"], 9),
                                               r["lastContact"] or "", len(r["contacts"])),
                           reverse=False)[:600],
            "total": len(rel),
            "dormant": len(dormant),
            "dormantWon": len(dormantWon),
        },
        "outreach": OUTREACH,
        "decisions": DECISIONS,
    }


# What order a person wants to read the company book in: the ones who have
# paid Fenster and gone silent first, the ones already talking to us last.
BOOK_ORDER = {"dormant - has bought": 0, "gone quiet": 1, "stale": 2,
              "dormant - quoted only": 3, "waiting": 4, "live": 5,
              "no contact on record": 6, "supplier": 7, "do not quote": 8}


def SOURCES(rows, winners, intake=None):
    return [
        {"name": "Contracts Finder", "status": "live", "kind": "Award notices",
         "detail": "%d construction award rows, %d unique winning companies, "
                   "90-day window" % (rows, winners),
         "cost": "Free, no key"},
        {"name": "Find a Tender (FTS)", "status": "planned",
         "kind": "High-value notices",
         "detail": "Above-threshold works, GBP 5.3m+. Same OCDS shape as "
                   "Contracts Finder, so it reuses the same puller.",
         "cost": "Free, no key"},
        {"name": "Tender-stage notices", "status": "planned",
         "kind": "Contracts out to bid",
         "detail": "The stage that actually matters for a subcontractor - "
                   "bidders are pricing and need our number now. Awards are "
                   "the latest and weakest signal.",
         "cost": "Free"},
        {"name": "PlanIt planning applications", "status": "planned",
         "kind": "Schemes 6-18 months out",
         "detail": "Gets Fenster onto the enquiry list before the list exists.",
         "cost": "Free"},
        {"name": "Portal notification emails", "status": "planned",
         "kind": "In-Tend, ProContract, Delta, Jaggaer",
         "detail": "These already arrive in info@ and commercial@. No login or "
                   "scraper needed - it is a mailbox problem, not a portal one. "
                   "This is how the Hightown tender was nearly lost.",
         "cost": "Free - needs the commercial@/info@ intake"},
        {"name": "Companies House", "status": "planned",
         "kind": "Enrichment",
         "detail": "Company type decides whether cold contact is lawful at all "
                   "(sole traders and partnerships are treated as individuals).",
         "cost": "Free, needs an API key"},
        {"name": "Barbour ABI / Glenigan", "status": "not started",
         "kind": "Private-sector projects",
         "detail": "Most of Fenster's actual clients are private main "
                   "contractors and appear in none of the free feeds.",
         "cost": "Paid"},
    ]


# Placeholders - nothing here is wired yet, and the hub says so rather than
# showing an empty state that looks like "no work to do".
OUTREACH = {
    "status": "planned",
    "note": ("Jacob drafts, a human approves, only then does anything send. "
             "No send path exists yet and no mailbox has been created."),
    "classes": [
        {"name": "Quote follow-up", "why": "We sent a price and heard nothing back",
         "example": "Gordon Court - GBP 368,376.70 issued 09/07, no recorded reply",
         "autonomy": "Human approves every send"},
        {"name": "Dormant reactivation", "why": "Quoted before, nothing for 6-18 months",
         "example": "Storm Building - Hammersmith delivered 2025, secondary glazing now live",
         "autonomy": "Human approves every send"},
        {"name": "Tender response", "why": "Invited - acknowledge fast, ask questions early",
         "example": "Princess Beatrice went out 10 days after the return date",
         "autonomy": "Human approves every send"},
        {"name": "New prospect", "why": "Cold. Never contacted",
         "example": "129 cold building contracts found in 90 days",
         "autonomy": "Blocked - needs a separate sending domain first"},
    ],
}

DECISIONS = [
    {"id": "JAC-1", "title": "Does Jacob send under his own name?",
     "why": ("Mary never pretends to be human. Outbound BD is a relationship "
             "job, which makes that rule expensive."),
     "options": ["Send under a real person's name", "Openly labelled assistant",
                 "Decide later - drafts only for now"]},
    {"id": "JAC-2", "title": "Cold outreach at all, or warm only?",
     "why": ("Warm-only needs no new domain, no consent register and carries "
             "almost no risk. Cold needs both."),
     "options": ["Warm only", "Warm now, cold later", "Both"]},
    {"id": "JAC-3", "title": "Budget for paid project intelligence?",
     "why": ("Free feeds are public sector only. Stepnell, Borras, Chigwell "
             "and Guildmore work never appears in them."),
     "options": ["Free sources only", "Trial Barbour ABI", "Trial Glenigan"]},
    {"id": "JAC-4", "title": "Who approves outbound?",
     "why": "Decides whether the approval queue lives on the hub or in email.",
     "options": ["Adam", "Zac", "Either"]},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deploy", action="store_true")
    args = ap.parse_args()

    data = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// generated by scripts/jacob_dashboard.py - do not edit\n")
        fh.write("export const JACOB = ")
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write(";\n")

    t = data["totals"]
    print("jacob-data.js written")
    print("  %d award rows, %d winners, %d client folders (%d won)"
          % (t["awardRows"], t["winners"], t["clients"], t["clientsWon"]))
    print("  warm %d | known %d | cold %d" % (t["warm"], t["known"], t["cold"]))
    print("  %d signals -> %d threads: %d buyer (%d live, %d quiet), "
          "%d supplier, %d domestic, %d portal"
          % (t["signals"], t["threads"], t["buyers"], t["liveBuyers"],
             t["quietBuyers"], t["supplierThreads"], t["domestic"], t["portalThreads"]))
    print("  %d with a price already out, %d unconfirmed, %d small-works "
          "repairs not on the board"
          % (t["quotedOut"], t["unconfirmed"], t["smallWorks"]))
    print("  %d actions on the Today page, %d dormant clients who have bought"
          % (len(data["actions"]), t["dormantWon"]))

    if args.deploy:
        # Same invocation as mary_dashboard.py - same Pages project, same
        # directory. Do not deploy while she is mid-deploy.
        #
        # Deploy "public" from INSIDE dashboard/. Wrangler resolves the
        # functions directory against the WORKING directory, not the assets
        # path, so `deploy dashboard/public` from the repo root ships the
        # static site with no API at all. Every /api route then returns the
        # SPA's HTML and the hub dies on "Unexpected token '<'". It looks like
        # a successful deploy - the giveaway is a missing "Uploading Functions
        # bundle" line in the output.
        r = subprocess.run(
            ["npx.cmd", "wrangler", "pages", "deploy", "public",
             "--project-name", "mary-dashboard", "--branch", "main",
             "--commit-dirty=true"],
            cwd=os.path.join(REPO, "dashboard"), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=600, shell=True)
        print("deploy exit", r.returncode)
        # wrangler emits box-drawing characters and this stdout is cp1252 -
        # re-encode rather than let a successful deploy die on its own log.
        enc = sys.stdout.encoding or "utf-8"
        print((r.stdout + r.stderr)[-500:].encode(enc, "replace").decode(enc, "replace"))
        return r.returncode


if __name__ == "__main__":
    sys.exit(main())

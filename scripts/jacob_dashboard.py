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
from datetime import date, datetime, timedelta, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AWARDS = os.path.join(REPO, "data", "jacob", "contracts-finder-awards.json")
INTAKE = os.path.join(REPO, "data", "jacob", "intake.json")
JAYK = os.path.join(REPO, "data", "jacob", "jayk-recovery.json")
OUTCOMES = os.path.join(REPO, "data", "jacob", "outcomes.json")
TENDERS = os.path.join(REPO, "data", "jacob", "tender-notices.json")
# Live leads that arrived by email rather than through a public feed. Fenster
# is a subcontractor: most of what it can still bid never reaches Contracts
# Finder at all, so a board built only on feeds is missing the half that
# matters. Hand-entered, provenance on every row.
MANUAL_LEADS = os.path.join(REPO, "data", "jacob", "leads-manual.json")
# The won commercial contracts, with a net value on every row - Adam's hand
# export of 29/07/2026. The only file here that says what Fenster HAS done
# rather than what it might get. 204 contracts, GBP 2.84m, 8 over GBP 50k.
CONTRACTS_WON = os.path.join(REPO, "data", "jacob", "contracts-won.json")
# ProContract (Due North) public adverts. Under the GBP 100k Find a Tender
# threshold a buyer advertises on its own portal and nowhere else, and that is
# Fenster's size of work. The adverts are public; only bidding needs the login
# Fenster has not had since Jayk left. JAC-11, 29/07/2026.
PROCONTRACT = os.path.join(REPO, "data", "jacob", "procontract.json")
# Adam's rule, 28/07/2026: a job is Mary's while it is priced and Jacob's the
# moment the quote goes out. This file is that boundary, one row per job, with
# every issue date checked against the message that actually left estimating@.
HANDOVER = os.path.join(REPO, "data", "jacob", "handover.json")
# AdminBase, exported by Adam on 28/07/2026. 264 commercial leads that have
# been quoted, going back to May 2025 - most of which predate anything else
# this board can see. Built by scripts/jacob_adminbase.py.
ADMINBASE = os.path.join(REPO, "data", "jacob", "adminbase.json")
# What JAC-1's answer produced. Drafts for a human to send, nothing more.
DRAFTS = os.path.join(REPO, "data", "jacob", "drafts.json")
# The two sources added on 29/07 for Adam's hub-78. PLANNING is the free half
# of what Barbour sells; DORMANT is the 59% of wins that came from a customer
# who had already bought. Both are optional - the board must still build on a
# machine where neither script has been run yet.
PLANNING = os.path.join(REPO, "data", "jacob", "planning.json")
DORMANT = os.path.join(REPO, "data", "jacob", "dormant.json")
JOBS = os.path.join(REPO, "data", "jobs")
OUT = os.path.join(REPO, "dashboard", "functions", "_data", "jacob-data.js")

ARCHIVE = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial"
TENDER_DIR = os.path.join(ARCHIVE, "1. Tender Documents")
PROJECT_DIR = os.path.join(ARCHIVE, "2. Projects")
COMPLETED_DIR = os.path.join(PROJECT_DIR, "2. Completed")

TODAY = date.today().isoformat()
STALE_BEFORE = "2026-01-28"          # 180 days - award notices publish late

# The intake now reads a real 180 days, which is 919 signals. That is a
# record, not a board: a Commercial Director between site visits cannot read
# four hundred rows. So the board picks its own window and says which - the
# one thing the old signals[:200] cap did not do. Anything older still exists
# in intake.json and is counted on the page, it just is not an action.
BOARD_DAYS = 60


def _archive_wins():
    """The real win history from data/job-history.json (mary_backfill_jobs.py:
    a job folder under 2. Projects means won). No values yet - the archive
    files them per job folder and nobody has mined them; say so rather than
    invent a number."""
    path = os.path.join(REPO, "data", "job-history.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            hist = json.load(fh)
    except Exception:
        return None
    entries = hist.get("entries", [])
    won = [e for e in entries
           if e.get("derived") == "won" or str(e.get("log_wl", "")).upper().startswith("W")]
    lost = [e for e in entries
            if e.get("derived") == "lost" or str(e.get("log_wl", "")).upper().startswith("L")]
    from collections import Counter
    top = Counter(e.get("client", "?") for e in won).most_common(12)
    # Values arrive one at a time as they are stated or mined - kept in
    # data/known-values.json with their basis, never guessed.
    known = {}
    kv_path = os.path.join(REPO, "data", "known-values.json")
    if os.path.exists(kv_path):
        try:
            with open(kv_path, encoding="utf-8") as fh:
                known = json.load(fh).get("values", {})
        except Exception:
            known = {}
    valued, consumed = [], set()
    for e in won:
        kv = known.get(e.get("key", ""))
        if kv and kv.get("value"):
            consumed.add(e.get("key"))
            valued.append({"client": e.get("client"), "job": e.get("job"),
                           "value": kv["value"], "basis": kv.get("basis", "?"),
                           "source": kv.get("source", "")})
    # A known win the archive has NO entry for (Franklin House) is still a
    # win - and evidence the archive itself has gaps, which is worth showing.
    for key, kv in known.items():
        if key in consumed or not kv.get("value"):
            continue
        client, _, job = key.partition("|")
        valued.append({"client": client.title(), "job": (job or client).title(),
                       "value": kv["value"], "basis": kv.get("basis", "?"),
                       "source": kv.get("source", ""), "archiveGap": True})
    valued.sort(key=lambda v: -v["value"])
    # Per-client detail - the real league table, with known value where any.
    by_client = {}
    for e in won:
        c = by_client.setdefault(e.get("client", "?"), {"client": e.get("client", "?"),
                                                        "won": 0, "jobs": [], "value": 0})
        c["won"] += 1
        if len(c["jobs"]) < 4:
            c["jobs"].append(e.get("job", "?"))
        kv = known.get(e.get("key", ""))
        if kv and kv.get("value"):
            c["value"] += kv["value"]
    clients_detail = sorted(by_client.values(), key=lambda c: (-c["value"], -c["won"]))
    # How many wins have value-bearing documents indexed - i.e. the number is
    # RECOVERABLE, somebody just has to read the doc.
    covered = 0
    ev_path = os.path.join(REPO, "data", "won-values-evidence.json")
    if os.path.exists(ev_path):
        try:
            with open(ev_path, encoding="utf-8") as fh:
                ev = json.load(fh).get("jobs", {})
            wk = {e.get("key") for e in won}
            covered = sum(1 for k, r in ev.items() if r.get("evidence") and k in wk)
        except Exception:
            covered = 0
    return {
        "generated": hist.get("generated"),
        "total": len(entries),
        "won": len(won),
        "lost": len(lost),
        "unmarked": len(entries) - len(won) - len(lost),
        "distinctClients": len(by_client),
        "clientsDetail": clients_detail,
        "valuedTotal": sum(v["value"] for v in valued),
        "evidenceCovered": covered,
        "topWonClients": [{"client": c, "won": n} for c, n in top],
        "examples": sorted({("%s - %s" % (e.get("client", "?"), e.get("job", "?")))
                            for e in won if e.get("confidence") == "high"})[:12],
        "knownValues": valued[:10],
        "valuedCount": len(valued),
        "note": ("Outcome derived from Fenster's own filing: a job folder under "
                 "2. Projects means won. Values are known for %d of %d wins "
                 "(data/known-values.json); mining the rest from the won folders "
                 "is open work." % (len(valued), len(won))),
    }


def board_window_start():
    return (date.fromisoformat(TODAY) - timedelta(days=BOARD_DAYS)).isoformat()

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

# The board used to rank by published contract value, biggest first. The
# Opportunity Log says that is exactly backwards: 229 decided outcomes, and
# no job over GBP 50,000 has ever been won - 0 from 52. So value now buys a
# row a warning, not a place at the top. Everything here is read from
# outcomes.json at build time rather than written down, because the log is
# hand-kept and these numbers will move.
FIT_UNKNOWN = {"band": "no value published", "winRate": None, "note": ""}

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


# Work a glazing company cannot be in, even when the winner is a known
# client and the CPV family reads "building". These sailed onto the LEADS
# call list on 29/07 (Zac: "he knows we are a glazing company right?")
# because warm/known only checked freshness: a scaffolding framework, a
# cleaning contract (Atlas - the canonical false positive, a second time),
# a junction improvement and a kitchen-and-bathroom programme, each with a
# "call them" next action. A relationship makes a company warm; it does not
# put windows in a scaffolding job. Deliberately NOT on this list: roofing
# (the Raglan roofing project carried a real Fenster order - rooflights).
NO_GLAZING = ("scaffold", "cleaning", "demolition", "asbestos", "landscap",
              "resurfac", "highway", "junction", "carriageway", "drainage",
              "survey works", "kitchen and bathroom", "lift replacement",
              "lift maintenance", "lift refurb")


def no_glazing(a):
    hay = " ".join([a.get("title") or "", a.get("description") or "",
                    a.get("cpv_desc") or ""]).lower()
    return any(t in hay for t in NO_GLAZING)


def is_building(a):
    if no_glazing(a):
        return False
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


def fit_for(value, outcomes):
    """What the outcome history says about a job of this size.

    Not a prediction and not a score - it is the row from the Opportunity Log
    that this value falls into, handed to a human with its own sample size
    attached. 'W0 L29' is a fact Adam can act on; '0.12 fit' is not."""
    if not outcomes or not value:
        return dict(FIT_UNKNOWN)
    for b in outcomes.get("bands", []):
        if value >= b["from"] and (b["to"] is None or value < b["to"]):
            note = ""
            if b["decided"] and not b["won"]:
                # "On the log", never "never" - Headrow Court (£50k+, completed,
                # in 2. Projects) is absent from the log entirely (Zac, 29/07).
                note = ("no win this size on the BD log - %d tried, %d won (log = "
                        "2025-26 funnel, not the win history)"
                        % (b["decided"], b["won"]))
            elif b["winRate"] is not None:
                note = "%d%% of these are won (%d of %d)" % (
                    round(b["winRate"]), b["won"], b["decided"])
            return {"band": b["label"], "winRate": b["winRate"],
                    "won": b["won"], "decided": b["decided"], "note": note}
    return dict(FIT_UNKNOWN)


def outcome_index(outcomes):
    """Client name -> their record in the Opportunity Log, keyed on the same
    normalised tokens the archive matcher uses, so 'FM Solutions' and
    'FM Solutions Ltd' are one company."""
    idx = {}
    for c in (outcomes or {}).get("clients", []):
        key = " ".join(tokens(c["client"]))
        if key and (key not in idx or c["decided"] > idx[key]["decided"]):
            idx[key] = c
    return idx


def record_for(name, idx):
    return idx.get(" ".join(tokens(name or "")))


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


def attach_won(rel, won):
    """Put the money Fenster has actually taken from a company onto its row.

    Until Adam's 29/07/2026 export there was no honest way to do this: the
    archive said a company had bought, and nothing said how much. It matters
    because "dormant - has bought" is the cheapest lead in the business and
    it was ranking a GBP 900-a-year customer level with Conamar, who have paid
    for sixteen contracts worth GBP 917,028. Those are not the same phone call.

    Matched on the same token normalisation the rest of the board uses, so
    "CONAMAR BUILDING SERVICES LTD." finds "Conamar". Anything that does not
    match is left alone rather than guessed at - a wrong merge here puts real
    money against the wrong company."""
    if not won:
        return rel
    idx = {}
    for c in won.get("clients", []):
        k = " ".join(tokens(c["client"]))
        if k:
            idx[k] = c
    for r in rel:
        k = " ".join(tokens(r["company"]))
        hit = idx.get(k)
        if not hit:
            # A won client whose name is a superset of the board's name, or
            # the other way round - "conamar" against "conamar building
            # services". Only accept it when one contains the other whole.
            for wk, c in idx.items():
                if len(k) >= 5 and (k in wk or wk in k):
                    hit = c
                    break
        if hit:
            r["wonJobs"] = hit["jobs"]
            r["wonValue"] = hit["value"]
            r["biggestWin"] = hit["biggest"]
            r["wonYears"] = "%s-%s" % (hit["firstYear"], hit["lastYear"])
            # DELIBERATELY NOT SET: r["relationship"] = "won".
            #
            # It was, for about ten minutes on 29/07/2026, and it took the
            # "dormant clients who have bought" count from 33 to 55 - which
            # looked like twenty-two new leads and was twenty-two false ones.
            # `lastContact` is empty when a company row did not JOIN to a
            # mailbox row, not when nobody has emailed them, so forcing the
            # relationship to "won" fed the state machine an absence it had
            # no business reading as silence. Checked by hand against the full
            # mailbox: St Albans School had emailed TODAY, Storm Building six
            # days before, Cranfield twelve. All three read "dormant".
            #
            # The money still attaches - that is the useful half, and it is
            # what ranks Conamar's GBP 917,028 above a GBP 900 customer. The
            # state stays with the evidence that earned it.
    return rel


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
    # Already Mary's. The handover has happened, so the only useful thing
    # Jacob can say is which file it is in.
    if t.get("job") and t["stage"] != "quoted":
        return (ADAM, "Already with Mary - job file '%s'. Nothing for BD to start; "
                      "chase it there if %s is waiting." % (t["job"], at))
    # They have told us the answer. Won or lost, this is the message that
    # ends a row - and it is worth more than any of the guesses below it,
    # because it is the only one where somebody has actually said what
    # happened. Every outcome in here is also a correction to the BD log.
    if t["stage"] == "decided":
        return (ADAM, "%s has given a decision on this - read it and act on it "
                      "today. Whatever it says, it also closes or corrects a row "
                      "in the Opportunity Log, which still has it open." % at)
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
        return (ADAM, "Call %s. Fenster has priced for them before without a recorded "
                      "win. This is the second chance." % at)
    return (ADAM, "Check commercial@ for a reply to %s, then call them. %d message%s in "
                  "and no history with them at all." % (at, t["messages"],
                                                        "" if t["messages"] == 1 else "s"))


def thread_unknowns(t):
    """Say what you do not know. A blank is honest; a confident guess is not."""
    out = []
    if t["kind"] == "buyer":
        if t.get("weReplied"):
            # JAC-5 answered - this used to be an unknown on every single row.
            if not t.get("answered"):
                out.append("Fenster last wrote to this domain on %s, which is BEFORE "
                           "their latest message - so their %s email looks unanswered."
                           % (t["weReplied"], t["last"]))
        elif not t.get("job"):
            out.append("Nothing has gone OUT to this domain from commercial@ or jacob@ "
                       "inside the window, and no job file of Mary's names this "
                       "address. Estimating@ is Mary's and cannot be read from here, "
                       "so she may have answered it.")
        else:
            out.append("Nothing has gone out to this domain from the mailboxes Jacob "
                       "reads, but Mary has a job file on it - so it is likely "
                       "answered from estimating@, which is hers.")
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
    start = board_window_start()
    by_key = {}
    for s in (intake or {}).get("signals", []):
        if s["date"] < start:
            continue
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

    # JAC-5, answered 29/07/2026. `intake.sentTo` is keyed on the recipient's
    # domain and says when Fenster last wrote to them. Before this, every
    # thread on the board carried "whether anyone has already replied - Jacob
    # reads received mail only", which was true of the code and never true of
    # the permission: SentItems always returned 200, nothing had asked it.
    sent_by_domain = {e["domain"]: e for e in (intake or {}).get("sentTo", [])}

    out = []
    for t in by_key.values():
        kinds = t.pop("kinds", set())
        dom = (t.get("contact") or "").lower().split("@")[-1]
        hit = sent_by_domain.get(dom)
        if hit:
            t["weReplied"] = hit["last"]
            t["weRepliedSubject"] = hit["lastSubject"]
            t["weRepliedFrom"] = hit["fromMailbox"]
            # Answered AFTER their last message, or only before it? The second
            # is not an answer, it is the thing they were replying to.
            t["answered"] = hit["last"] >= t["last"]
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
        # "decided" outranks everything: a client telling us the answer is the
        # one message that closes a row or starts a job, and it was being
        # filed as correspondence because it opens "I hope you are well".
        t["stage"] = ("decided" if "decision" in kinds else
                      "quoted" if "quote-out" in kinds else
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
        return (JACOB, "Draft an intro for Adam to send to %s - quoted before, no "
                       "recorded win, and they are building again." % co)
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


def build_handover(hand):
    """The seven issued quotes Adam handed to Jacob, plus the three he has not.

    Everything a chase depends on is the *issue* date. The board used to
    derive its chase state from the tender return date sitting in Mary's job
    records, which is a different date on a different clock: it had Gordon
    Court as "not due until 16 September" when the quote had been with
    Chigwell and silent for eighteen days, and it had Chester Thomas as never
    issued when it had gone out on the 27th. So the day count here is measured
    from the send, and the send is the one Mary read in estimating@.

    A day count is not on its own an instruction. Gordon Court is nineteen
    days out and should not be chased for a decision, because the client
    physically cannot give one until jLiving reports in September. That is
    what `blockedUntil` carries, and why the next action on every row is
    written by hand rather than generated from a number.
    """
    if not hand:
        return None
    today = date.fromisoformat(TODAY)

    def days_out(iso):
        if not iso:
            return None
        return (today - date.fromisoformat(iso)).days

    steps = {s["n"]: s["action"] for s in
             (hand.get("checklist") or {}).get("steps", [])}
    rows = []
    for r in hand.get("issued", []):
        row = dict(r)
        row["daysOut"] = days_out(r.get("issued"))
        row["daysSinceClient"] = days_out(r.get("lastClientContact"))
        # Blocked by a DATE, or blocked by an EVENT that has no date.
        #
        # Brandon Estate, 29/07/2026, forced the second case. Elkins cannot
        # award us anything until they win their own bid, and nobody knows
        # when that is - Chris Conlon has simply undertaken to tell us. There
        # is no `blockedUntil` to write, and writing a fortnight from today
        # would be inventing exactly the date the register exists to avoid.
        # So `blockedPending` says what has to HAPPEN, and the row is off the
        # chase-today list without being off the board.
        #
        # `reviewOn` is the safety net and is NOT a chase date: it is the day
        # to check whether the event has happened, not the day to ring anyone.
        # Without it an undated block is a way to lose a GBP 7.2m quote quietly.
        row["blocked"] = bool(
            (r.get("blockedUntil") and r["blockedUntil"] > TODAY)
            or r.get("blockedPending"))
        row["blockedByEvent"] = bool(r.get("blockedPending")
                                     and not r.get("blockedUntil"))
        row["reviewDue"] = bool(r.get("reviewOn") and r["reviewOn"] <= TODAY)
        # Adam's own checklist numbering, so the register and the CRM call the
        # same thing by the same name. A row with a date in the past is not a
        # reminder, it is an overdue action, and the board says which.
        row["stageName"] = steps.get(r.get("stage"))
        row["chaseDue"] = bool(r.get("nextChase") and r["nextChase"] <= TODAY)
        rows.append(row)
    # Longest silence first. A row that is blocked is sorted with the rest and
    # says so on its face rather than being hidden - "cannot answer yet" is a
    # fact about a GBP 368k quote, not a reason to stop showing it.
    rows.sort(key=lambda r: -(r.get("daysOut") or 0))

    held = [dict(h) for h in hand.get("held", [])]

    # What is actually chaseable today: issued, not blocked, and nothing back
    # from the client for a week. Everything else is on the board to be seen,
    # not to be phoned.
    def chaseable(r):
        if r["blocked"]:
            return False
        since = r["daysSinceClient"]
        if since is not None and since < 7:
            return False
        # An explicit chase date that has arrived outranks the arithmetic. A row
        # can be genuinely due today with NO issue date at all - Leys Park, 29/07,
        # where AdminBase said "quoted" and the send was never visible in a mailbox
        # I can read. Falling back to daysOut dropped the most urgent row on the
        # board off the due list, because an unknown issue date scores zero.
        if r.get("nextChase") and r["nextChase"] <= TODAY:
            return True
        return (r.get("daysOut") or 0) >= 7

    due = [r for r in rows if chaseable(r)]
    return {
        "updated": hand.get("updated"),
        "rule": hand.get("rule"),
        "checklist": hand.get("checklist"),
        "verification": hand.get("verification"),
        "issued": rows,
        "held": held,
        "corrections": hand.get("corrections", []),
        "totals": {
            "chaseDue": sum(1 for r in rows if r["chaseDue"]),
            "noChaseDate": sum(1 for r in rows
                               if not r.get("nextChase") and not r["blocked"]),
            "issued": len(rows),
            "issuedValue": sum(r.get("value") or 0 for r in rows),
            "due": len(due),
            "dueValue": sum(r.get("value") or 0 for r in due),
            "blocked": sum(1 for r in rows if r["blocked"]),
            "live": sum(1 for r in rows if r.get("state") == "live"),
            "held": len(held),
            "heldValue": sum(h.get("value") or 0 for h in held),
            "oldest": max([r.get("daysOut") or 0 for r in rows] or [0]),
        },
    }


def merge_manual(tenders, manual):
    """Feed notices plus the hand-entered ones, on one list and one clock.

    A lead that came in as email is not a lesser lead - it is the normal way
    Fenster hears about work, and keeping it on a page of its own would put
    it where nobody looks. The feed rows already carry daysLeft; these do not,
    so it is computed here from the closing date."""
    out = list((tenders or {}).get("notices", []))
    for n in (manual or {}).get("notices", []):
        # A superseded row stays in the file and comes off the board. The Ryde
        # lead reached us as a Supply2Gov alert with the buying organisation
        # stripped out and no value; the same job on ProContract carries the
        # buyer, a named officer, a phone number and the budget. One job, one
        # row - but the file keeps how it first arrived, because that is the
        # thing leads-manual.json exists to record.
        if n.get("supersededBy"):
            continue
        row = dict(n)
        row["manual"] = True
        row["daysLeft"] = (-days_since(n["closes"]) if n.get("closes") else None)
        out.append(row)
    return out


def merge_procontract(tenders, pc):
    """ProContract (Due North) adverts, onto the same list and the same clock.

    These are neither feed rows nor hand-entered ones. They come from a public
    source Fenster could have read since Jayk left and did not, because "the
    portal logins are dead" was allowed to mean "the source is dark". It never
    did: the adverts are public and only BIDDING needs an account. JAC-11.

    Everything here is `direct` and `confident` on purpose - a ProContract
    advert states its own scope in prose, so there is no CPV guessing and no
    keyword-metaphor problem. What it does NOT state is a value: `Estimated
    value` reads N/A on almost every row and the real budget, when there is
    one, is a sentence in the description. `budgetFromText` carries the top of
    the stated range so the fit warning has something honest to work on, and
    `valueNote` says it was a range so nobody quotes the number as the number.
    """
    out = list(tenders or [])
    for n in (pc or {}).get("notices", []):
        if n.get("tier") != "glazing":
            continue
        closes = None
        m = re.match(r"(\d{2})/(\d{2})/(\d{4})", n.get("closes") or "")
        if m:
            closes = "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
        budget = n.get("budgetFromText") or []
        row = {
            "ocid": "procontract-" + (n.get("ref") or n.get("advertId", ""))[:24],
            "title": n.get("title"),
            "buyer": n.get("buyer"),
            "where": n.get("region"),
            "closes": closes,
            "daysLeft": (-days_since(closes) if closes else None),
            "value": (max(budget) if budget else None),
            "valueNote": ("Stated in the description as a range, GBP %s. The board "
                          "carries the top of it." % " to ".join(gbp(b) for b in budget)
                          if len(budget) > 1 else None),
            "tier": "direct",
            "confident": True,
            "cpv": (n.get("cpv") or ["-"])[0],
            "cpvCount": len(n.get("cpv") or []),
            "coverage": None,
            "procontract": True,
            "manual": False,
            "ref": n.get("ref"),
            "url": n.get("url"),
            "contact": n.get("contact"),
            "email": n.get("email"),
            "telephone": n.get("telephone"),
            "source": "procontract",
            "sourceNote": ("ProContract (Due North) public advert, read by Jacob on "
                           "%s with no login. Fenster has no ProContract account - "
                           "JAC-11 - so seeing it is free and bidding it is not."
                           % (pc.get("updated") or "")[:10]),
            "warning": n.get("boardWarning"),
        }
        out.append(row)
    return out


def build_tenders(notices, outcomes, book):
    """Contracts still out to bid. The only stage at which a subcontractor
    can still get onto an enquiry list, which is why this feed exists at all.

    Two different jobs live in here and the board must not blur them:
      direct        - the buyer is asking for glazing work. Fenster can price
                      this itself, and the decision is Gintare's and Adam's.
      main-contract - the buyer is asking for a building. Fenster cannot bid
                      it; the work is finding out who is bidding, and that is
                      Jacob's.
    """
    known_names = {" ".join(tokens(r["company"])) for r in book}
    idx = outcome_index(outcomes)
    rows = []
    for n in notices:
        left = n.get("daysLeft")
        buyer_key = " ".join(tokens(n.get("buyer") or ""))
        rec = record_for(n.get("buyer"), idx)
        row = dict(n)
        row["key"] = "tender:" + re.sub(r"[^a-z0-9]", "-", (n.get("ocid") or "")[-24:])
        row["fit"] = fit_for(n.get("value"), outcomes)
        row["knownBuyer"] = buyer_key in known_names
        row["record"] = rec
        row["state"] = ("closing" if left is not None and left <= 7
                        else "open" if left is not None else "no closing date")

        if n.get("coverage") == "outside coverage":
            # JAC-10 CLOSED, Adam, 29/07/2026: "We basically work nationwide
            # (wales and england) ... please do send opportunities for all of
            # wales and england." So this branch is now Scotland, Northern
            # Ireland and the Crown Dependencies, and nothing else. It used to
            # catch Wales, Cornwall, Devon, Cumbria and the whole North East on
            # the strength of a PQQ marketing document, while Fenster had a
            # GBP 174,546 quote live in Merthyr Tydfil.
            row["owner"] = NOBODY
            row["next"] = ("Parked. %s is outside England and Wales, which is "
                           "where Adam says Fenster works (29/07/2026, JAC-10). "
                           "Not a judgement about the job."
                           % (n.get("where") or "This area"))
            row["state"] = "outside England and Wales"
        elif not n.get("confident"):
            row["owner"] = JACOB
            spray = (n.get("cpvCount") or 0) > 12
            row["next"] = ("Read this before anyone acts. %s, and the notice never "
                           "says window, door or glazing in words."
                           % ("The buyer tagged it with %d CPV codes, which is a net "
                              "rather than a description" % n["cpvCount"] if spray
                              else "It matched on one of the broader codes in Adam's "
                                   "list (%s)" % n.get("cpv", "-")))
            row["state"] = "needs reading"
        elif n["tier"] == "direct":
            row["owner"] = GINTARE
            row["next"] = ("Decide whether to price. %s, and it closes %s."
                           % ("%s want glazing work" % n["buyer"] if n.get("buyer")
                              else "This is glazing work and the buyer is not "
                                   "named on what we have - finding out who is "
                                   "asking is the first job",
                              n.get("closes") or "on no date we can see"))
            if rec and rec["won"]:
                row["owner"] = ADAM
                row["next"] = ("Call %s - they have bought from Fenster %d time%s "
                               "and this closes %s."
                               % (n["buyer"], rec["won"], "" if rec["won"] == 1 else "s",
                                  n.get("closes") or "soon"))
        elif n["tier"] == "main-contract":
            row["owner"] = JACOB
            row["next"] = ("Find who is bidding %s before it closes %s, then get "
                           "Fenster onto their enquiry list."
                           % (n["title"][:50], n.get("closes") or "-"))
        else:
            row["owner"] = JACOB
            row["next"] = ("Read the notice before anyone acts - it matched on "
                           "words, not on a CPV code, and words lie.")
        # A hand-entered lead carries the thing that will bite whoever picks
        # it up. It goes in the next action rather than a footnote, because a
        # qualification raised at the end of a tender is not a qualification.
        if n.get("warning"):
            row["next"] += " " + n["warning"]
        rows.append(row)
    rows.sort(key=lambda r: (r["closes"] or "9999",
                             {"direct": 0, "main-contract": 1}.get(r["tier"], 2)))
    return rows


def build_actions(threads, warm, known, book, tenders=None, handover=None,
                  adminbase=None, drafts=None):
    """The list a Commercial Director reads in ten seconds. Ranked by how
    close it is to a real enquiry from a real buyer, which is the only thing
    Jacob is for."""
    acts = []

    def add(score, key, company, headline, what, owner, nxt, state, page,
            project=None, deadline=None, why=None):
        """Adam, hub-74 (29/07/2026): every item on Today must carry the client,
        the project, the current stage, the owner, the next action, the action
        deadline and the reason it is on the page. The first five were already
        here under other names; `project`, `deadline` and `why` are the three
        that were being inferred by whoever read the row, which is not the same
        as being stated. `why` is the one that cannot be derived downstream -
        "due today" and "no owner set" put a row here for opposite reasons and
        the page has to say which."""
        acts.append({"score": score, "key": key, "company": company,
                     "headline": headline, "what": what, "owner": owner,
                     "next": nxt, "state": state, "page": page,
                     "project": project or headline, "deadline": deadline,
                     "why": why or ""})

    # Top of the list, above every lead and every notice. A quote already out
    # is money Fenster has spent and can still lose; a lead is money it has
    # not spent yet. These rows are also the only ones on the board whose date
    # was read out of a sent message rather than inferred from anything.
    # A client with a draft written for them does not also need a "call them"
    # row. The draft is that call, already written, and showing both is one
    # thing to do printed twice.
    drafted_clients = {(d.get("client") or "").lower()
                       for d in (drafts or {}).get("drafts", [])}
    # And by domain, because AdminBase keys on the domain and a display name
    # will not match it - "Alexander James" has a draft; the CRM also carries
    # "Alexander James Contracts", and they are one company on one domain.
    drafted_domains = {(d.get("to") or "").split("@")[-1].strip().lower()
                       for d in (drafts or {}).get("drafts", []) if d.get("to")}

    for r in (handover or {}).get("issued", []):
        if r.get("owner") in (None, "-"):
            continue
        if (r.get("client") or "").lower() in drafted_clients:
            continue
        days = r.get("daysOut") or 0
        score = 130 + min(days, 30)
        if r.get("blocked"):
            score = 118          # still worth a call, not worth the top slot
        # .get's default does not cover an EXPLICIT null - a register row with
        # "issued": null crashed the whole board rebuild here on 29/07.
        iss = r.get("issued") or ""
        if r.get("chaseDue"):
            why = "Chase date %s has arrived" % r["nextChase"]
        elif r.get("blocked"):
            why = ("Blocked - %s"
                   % (r.get("blockedPending") or "the client cannot answer yet"))
        elif not r.get("nextChase"):
            why = "Issued %d days ago with no next-chase date set" % days
        else:
            why = "Quote issued %d days ago and nothing back" % days
        add(score, r["key"], r["client"], r.get("contact") or r["client"],
            "%s - %s issued %s" % (r["job"], gbp(r.get("value")),
                                   (iss[8:10] + "/" + iss[5:7]) if len(iss) >= 10 else "date unknown"),
            r.get("owner"), r.get("next"), r.get("state"), "leads",
            project=r["job"], deadline=r.get("nextChase"), why=why)

    # Above even those. A draft is a chase that has already been written - the
    # only thing between it and the client is somebody pressing send, which is
    # the smallest ask on this whole page. It sits at the top because that is
    # where the cheapest action belongs, not because drafting is important.
    for d in (drafts or {}).get("drafts", []):
        add(160 - d.get("priority", 9), "draft:" + d["id"], d["client"],
            d.get("to_name") or d["client"],
            "%s - draft ready for %s" % (d["job"], d.get("send_as", "a human")),
            d.get("send_as", ADAM),
            "Read it, change what you want, send it from your own mailbox. %s"
            % d.get("why_now", ""), d.get("status", "awaiting a human"),
            "drafts", project=d["job"], deadline=d.get("send_by"),
            why="Draft written and waiting for %s to review and send it"
                % d.get("send_as", "a human"))

    # The CRM's own chase list, minus anything already covered above. These are
    # quotes nobody has looked at in months - they were invisible to this board
    # until Adam's export arrived, because they predate every mailbox window it
    # reads.
    on_board = {(r.get("client") or "").lower()
                for r in (handover or {}).get("issued", [])}
    ab_acts = []
    for r in (adminbase or {}).get("due", []):
        # An outlier is held back because nobody had confirmed it, not because
        # of its size. Adam confirmed Brandon Estate on 29/07 - "that is a
        # legit tender and should be treated as such" - so a confirmed row
        # belongs on this list like any other.
        if (r.get("outlier") and not r.get("confirmed")) or not r.get("value"):
            continue
        if (r["client"].lower() in drafted_clients
                or r.get("key") in drafted_domains
                or r["client"].lower() in on_board):
            continue
        if r.get("scheme"):
            continue        # one scheme, several bidders - handled as a scheme
        # Value carries this list, because age carries no information here:
        # nearly every row is overdue, so being overdue distinguishes nothing.
        base = 68 + min(int((r["value"] or 0) / 50000), 12)
        ab_acts.append((base, r))
    ab_acts.sort(key=lambda x: -x[0])
    for base, r in ab_acts[:6]:
        add(base, "ab:" + r["lead"], r["client"], r["client"],
            "%s - %s quoted, %s silent" % (r["job"][:52], gbp(r["value"]),
                                           "%d days" % r["days"] if r["days"]
                                           is not None else "no date set"),
            r.get("owner") or ADAM,
            "Nobody has been back to them since the quote. Establish whether "
            "it is still live before anything else - the CRM closes nothing, "
            "so 'Live - Quoted' here does not mean the job is."
            + (" %s" % r["confirmed"] if r.get("confirmed") else "")
            + (" The CRM dates this %s; the quote actually went out %s, so "
               "the silence is %d days and not %d."
               % (r["staleDate"]["crmDate"], r["staleDate"]["issued"],
                  r["days"] or 0, r["staleDate"]["crmDays"] or 0)
               if r.get("staleDate") else ""),
            r["state"], "leads", project=r["job"], deadline=r.get("nextAction"),
            why=("Quoted %s and nobody has been back to them since"
                 % ("%d days ago" % r["days"] if r["days"] is not None
                    else "on a date the CRM does not hold")))

    for t in threads:
        if t["owner"] == NOBODY:
            continue
        if t["kind"] == "buyer":
            base = 100 if t["relationship"] in ("won", "quoted") else 78
            if t["state"] in ("gone quiet", "stale"):
                base -= 25
            # A price already out ranks below a fresh ask, and a thread Jacob
            # has not read yet ranks below both - it is not a lead until
            # somebody has confirmed it is one. A decision outranks all of
            # them: somebody has said what happened, and nothing else on this
            # board is that certain.
            if t["stage"] == "decided":
                base += 20
            elif t["stage"] == "quoted":
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
            if due is not None and due <= 21:
                why = "They have asked for a price by %s" % t["deadline"]
            elif t["stage"] == "decided":
                why = "They have written to say what happened - won or lost"
            elif t["state"] in ("gone quiet", "stale"):
                why = "%d days since they last wrote and nothing since" % t["days"]
            else:
                why = "Live conversation with a buyer, last message %s" % t["last"]
            add(base + min(t["messages"], 8), t["key"], t["company"],
                t["person"] or t["company"], t["subject"], t["owner"], t["next"],
                t["state"], "enquiries", project=t["subject"],
                deadline=t.get("deadline"), why=why)
        elif t["kind"] == "portal":
            add(74, t["key"], t["company"], "Portal notice", t["subject"],
                t["owner"], t["next"], t["state"], "enquiries",
                project=t["subject"], deadline=t.get("deadline"),
                why="Portal notice nobody has pulled the pack for")

    # A contract still out to bid beats one already awarded, every time - but
    # it does not beat a buyer who is emailing us. A public notice is a
    # stranger with a deadline; a live thread is somebody who already knows
    # our name, and "a warm name beats a perfect-fit stranger nearly every
    # time" is the whole reason this job exists. So these are scored to sit
    # under the buyer threads, and only three of them ever reach this page.
    #
    # An earlier version scored them at 96 and nine of the fourteen rows here
    # were public tenders, two of them in Scotland and one for cable cutters.
    tender_acts = []
    for n in (tenders or []):
        left = n.get("daysLeft")
        if left is None or left < 0:
            continue
        if n.get("coverage") == "outside coverage":
            # Scotland, Northern Ireland or the Crown Dependencies - off the
            # action list, still on the board. England and Wales are IN as of
            # 29/07/2026 (Adam, JAC-10), so this no longer swallows Cardiff.
            continue
        if not n.get("confident"):
            continue                 # broad CPV, no glazing word - read it first
        base = {"direct": 62, "main-contract": 45}.get(n["tier"])
        if base is None:
            continue                 # matched on wording alone; not an action yet
        if left <= 14:
            base += (14 - left)
        if n.get("record") and n["record"]["won"]:
            base += 12
        tender_acts.append((base, n))
    tender_acts.sort(key=lambda t: -t[0])
    for base, n in tender_acts[:3]:
        left = n["daysLeft"]
        add(base, n["key"], n.get("buyer") or "-",
            n["title"][:70],
            "Closes %s - %d days. %s" % (n.get("closes") or "no date", left,
                                         n["fit"].get("note") or ""),
            n["owner"], n["next"], n["state"], "opportunities",
            project=n["title"], deadline=n.get("closes"),
            why=("New opportunity nobody has reviewed - it closes in %d day%s"
                 % (left, "" if left == 1 else "s")))

    for r in warm[:6]:
        add(55, "lead:" + re.sub(r"[^a-z0-9]", "-", r["supplier"].lower())[:50],
            r["client"], r["supplier"], "%s - %s" % (r["title"], gbp(r["total"] or r["value"])),
            r["owner"], r["next"], "award won " + (r["awarded"] or ""), "opportunities",
            project=r["title"],
            why="They have bought from Fenster and have just won work - no contact yet")

    for r in [x for x in book if x["state"] == "dormant - has bought"][:5]:
        add(32, "co:" + x_key(r), r["company"], r["company"],
            "Has bought from Fenster. No email in the 180-day window.",
            r["owner"], r["next"], r["state"], "companies",
            project="-", why="Has paid Fenster and nobody has emailed them in 180 days")

    for r in known[:4]:
        add(22, "lead:" + re.sub(r"[^a-z0-9]", "-", r["supplier"].lower())[:50],
            r["client"], r["supplier"], "%s - %s" % (r["title"], gbp(r["total"] or r["value"])),
            r["owner"], r["next"], "award won " + (r["awarded"] or ""), "opportunities",
            project=r["title"],
            why="Quoted before with no recorded win, and they are building again")

    acts.sort(key=lambda a: -a["score"])
    # Two award notices against the same client collapse to one thing to do.
    seen, ranked = set(), []
    for a in acts:
        sig = (a["company"], a["next"])
        if sig in seen:
            continue
        seen.add(sig)
        ranked.append(a)

    # A cap per kind, not just an overall one. Pure score ordering filled all
    # fourteen slots with "chase a buyer who has gone quiet" - which is one
    # finding repeated fourteen times, not fourteen things to do. Adam is a
    # Commercial Director between site visits; he needs the shape of the day,
    # and the full list is one click away on each page.
    # Chasing gets its own room and the largest of it. Without a slot of its
    # own it fell through the default of two, and the two things Adam most
    # needed to see - a GBP 368k quote he must not chase yet, and a GBP 7,975
    # one sitting unread in an out-of-office - dropped off the page entirely.
    # Adam, hub-74: Work is four pages now, so the room is shared out between
    # four and not seven. Leads absorbs what Chasing and the Chase list held
    # (5 + 3), Opportunities absorbs what Out to bid held (3 + 2). The totals
    # are unchanged on purpose - this is the same digest under the new names,
    # and the Today page builds the full due list from the pages themselves
    # rather than from this cap.
    ROOM = {"drafts": 5, "leads": 8, "enquiries": 8,
            "opportunities": 5, "companies": 2}
    used, out, held = defaultdict(int), [], defaultdict(int)
    for a in ranked:
        page = a.get("page") or "overview"
        if used[page] >= ROOM.get(page, 2):
            held[page] += 1
            continue
        used[page] += 1
        out.append(a)
    out = out[:22]
    # A cap that does not say what it dropped reads as "that was everything".
    for a in out:
        a["heldBack"] = held.get(a.get("page") or "overview", 0)
    return out


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
        # The same work-type screen as cold. Warm/known used to skip it, so a
        # known company's scaffolding or cleaning win became a "call them".
        live = [r for r in rows if is_fresh(r) and is_building(r)]
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
    outcomes = load_json(OUTCOMES)
    tenderfeed = load_json(TENDERS)
    handover = build_handover(load_json(HANDOVER))
    adminbase = load_json(ADMINBASE)
    drafts = load_json(DRAFTS)
    wonContracts = load_json(CONTRACTS_WON)
    rel = attach_won(build_relationships(clients, intake, jayk), wonContracts)
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
    tenders = build_tenders(
        merge_procontract(merge_manual(tenderfeed, load_json(MANUAL_LEADS)),
                          load_json(PROCONTRACT)),
        outcomes, rel)
    actions = build_actions(threads, warm, known, rel, tenders, handover,
                            adminbase, drafts)

    # Every lead now carries what the outcome history says about a job that
    # size. The point is not to hide the big ones - it is to stop the board
    # putting a GBP 4m academy above a GBP 3k door set when the log says the
    # door set is the one Fenster wins.
    for r in warm + known + cold:
        r["fit"] = fit_for(r.get("total") or r.get("value"), outcomes)

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
            # What the board is showing, against what the mailbox actually
            # holds. A count that does not say its window is a claim.
            "boardDays": BOARD_DAYS,
            "boardFrom": board_window_start(),
            "signalsOlder": sum(1 for s in (intake or {}).get("signals", [])
                                if s["date"] < board_window_start()),
            "mailFrom": (intake or {}).get("covered_from"),
            "mailTruncated": (intake or {}).get("truncated") or [],
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
            # The verified half of that, from Adam's handover rule. These are
            # not inferred from a mailbox - they are the sends Mary read.
            "handoverIssued": (handover or {}).get("totals", {}).get("issued", 0),
            "handoverValue": (handover or {}).get("totals", {}).get("issuedValue", 0),
            "handoverDue": (handover or {}).get("totals", {}).get("due", 0),
            "handoverDueValue": (handover or {}).get("totals", {}).get("dueValue", 0),
            "handoverHeld": (handover or {}).get("totals", {}).get("held", 0),
            # AdminBase. The value here is ex VAT and the CRM's is not - see
            # the note on the chase list, and do not compare the two.
            "crmRows": (adminbase or {}).get("totals", {}).get("rows", 0),
            "crmValue": (adminbase or {}).get("totals", {}).get("value", 0),
            "crmDue": (adminbase or {}).get("totals", {}).get("due", 0),
            "crmDueValue": (adminbase or {}).get("totals", {}).get("dueValue", 0),
            "crmClients": (adminbase or {}).get("totals", {}).get("clients", 0),
            "crmYearSilent": (adminbase or {}).get("totals", {}).get("yearSilent", 0),
            "crmDoubleCounted": (adminbase or {}).get("totals", {}).get("doubleCounted", 0),
            "drafts": len((drafts or {}).get("drafts", [])),
            "unconfirmed": sum(1 for t in threads if t["stage"] == "unconfirmed"),
            "smallWorks": ((intake or {}).get("counts", {}) or {}).get("small-works", 0),
            # Mailboxes deliberately not read. Adam took info@ off the list on
            # 28/07/2026; a count that does not say which mailboxes it comes
            # from is a claim, not a fact.
            "mailExcluded": (intake or {}).get("excluded", []),
            # Contracts still out to bid, which is the only stage a
            # subcontractor can still get onto an enquiry list at.
            "tenders": len(tenders),
            "tendersDirect": sum(1 for t in tenders if t["tier"] == "direct"),
            "tendersClosing": sum(1 for t in tenders
                                  if (t.get("daysLeft") or 99) <= 7),
            # What Fenster actually converts, from 229 decided outcomes.
            "winRate": ((outcomes or {}).get("summary") or {}).get("winRate"),
            "wonMedian": ((outcomes or {}).get("summary") or {}).get("wonMedian"),
            "noWinAbove": ((outcomes or {}).get("summary") or {}).get("noWinAbove"),
            "openThisYear": len((outcomes or {}).get("openThisYear", [])),
            # The one money number on the board that is sourced, not guessed:
            # published values of live contracts whose winner Fenster knows.
            "knownWinnerValue": sum((r.get("total") or 0) for r in warm + known),
        },
        "actions": actions,
        "handover": handover,
        "threads": threads,
        "warm": warm, "known": known, "cold": cold[:150],
        "tenders": tenders,
        # The outcome history, whole. Every number the board leans on lives
        # here with its sample size next to it, so a person can check the
        # claim instead of taking it.
        "outcomes": {
            "updated": (outcomes or {}).get("updated"),
            "source": (outcomes or {}).get("source"),
            "summary": (outcomes or {}).get("summary"),
            "bands": (outcomes or {}).get("bands", []),
            "clients": (outcomes or {}).get("clients", [])[:80],
            "lostReasons": (outcomes or {}).get("lostReasons", []),
            "lostLegend": (outcomes or {}).get("lostLegend"),
            "chased": (outcomes or {}).get("chased", []),
            "openThisYear": (outcomes or {}).get("openThisYear", []),
            "rows": (outcomes or {}).get("rows"),
        } if outcomes else None,
        # The ACTUAL win history, from Fenster's own filing (data/job-history.json,
        # built by mary_backfill_jobs.py: a folder under 2. Projects means won).
        # Added 29/07 after "never won over 50k" shipped as a universal while
        # Headrow Court sat in this file marked won at high confidence. The log
        # says how the recent funnel converts; THIS says what Fenster has won.
        "archive": _archive_wins(),
        "tenderFeed": {
            "updated": (tenderfeed or {}).get("updated"),
            "sources": (tenderfeed or {}).get("sources"),
            "from": (tenderfeed or {}).get("publishedFrom"),
            "cpvList": (tenderfeed or {}).get("cpvList", []),
            "cpvListFrom": (tenderfeed or {}).get("cpvListFrom"),
            "counts": (tenderfeed or {}).get("counts", {}),
        } if tenderfeed else None,
        "sources": SOURCES(len(awards), len(by_supplier), intake, tenderfeed,
                           load_json(PROCONTRACT)),
        "intake": {
            "updated": (intake or {}).get("updated"),
            "windowDays": (intake or {}).get("window_days"),
            "perMailbox": (intake or {}).get("per_mailbox", {}),
            "excluded": (intake or {}).get("excluded", []),
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
        "adminbase": adminbase,
        "drafts": drafts,
        # What Fenster has actually won, with a value on every row. This is the
        # only panel on the board built from delivered work rather than from
        # hope, and it is the one that settles whether a big lead is worth
        # anyone's afternoon. Adam, 29/07/2026.
        "wonContracts": wonContracts,
        # Planning applications - the only source that reaches a scheme
        # BEFORE an enquiry list exists. Adam, hub-78.
        "planning": load_json(PLANNING),
        # Customers who bought, stopped, and nobody noticed.
        "dormantClients": load_json(DORMANT),
    }


# What order a person wants to read the company book in: the ones who have
# paid Fenster and gone silent first, the ones already talking to us last.
BOOK_ORDER = {"dormant - has bought": 0, "gone quiet": 1, "stale": 2,
              "dormant - quoted only": 3, "waiting": 4, "live": 5,
              "no contact on record": 6, "supplier": 7, "do not quote": 8}


def SOURCES(rows, winners, intake=None, tenderfeed=None, procontract=None):
    tf = tenderfeed or {}
    tcounts = tf.get("counts") or {}
    per = tf.get("sources") or {}
    pcounts = (procontract or {}).get("counts")
    return [
        {"name": "The Opportunity Log", "status": "live",
         "kind": "What Fenster actually wins",
         "detail": "The BD pipeline from the Commercial OneDrive, read-only. "
                   "229 decided outcomes with values and lost reasons - the "
                   "only record either bot has of what converts. Everything "
                   "on the board that mentions a win rate comes from here.",
         "cost": "Free - hand-kept by the BD team"},
        {"name": "Contracts Finder - tender stage", "status": "live",
         "kind": "Contracts out to bid",
         "detail": "%d notices still open: %d matching Adam's CPV list "
                   "directly, %d main contracts a glazing package sits inside, "
                   "%d matched on wording alone. Volume is genuinely thin - "
                   "about 11 tender notices a day nationally against 110 "
                   "awards, so this feed finds few things but they are live."
                   % (sum(tcounts.values()), tcounts.get("direct", 0),
                      tcounts.get("main-contract", 0), tcounts.get("text-only", 0)),
         "cost": "Free, no key"},
        {"name": "Find a Tender (FTS)", "status": "live",
         "kind": "Above-threshold notices",
         "detail": "Same puller, second service. %s"
                   % (("%d releases read in the window."
                       % (per.get("fts", {}) or {}).get("releases", 0))
                      if "fts" in per else "Not reached on the last run."),
         "cost": "Free, no key"},
        {"name": "Contracts Finder - awards", "status": "live",
         "kind": "Who won what",
         "detail": "%d construction award rows, %d unique winning companies. "
                   "The weakest signal of the three - by the time it publishes, "
                   "the enquiry list was drawn up months ago." % (rows, winners),
         "cost": "Free, no key"},
        {"name": "ProContract (Due North) adverts", "status": "live",
         "kind": "Sub-GBP 100k public work - Fenster's size",
         "detail": "%s. Under the GBP 100k Find a Tender threshold a council or "
                   "housing association advertises on its OWN portal and nowhere "
                   "else, which is why none of these show on the feeds above. "
                   "The adverts are PUBLIC - no account. Only expressing interest "
                   "and downloading the pack need the login Fenster has not had "
                   "since Jayk left, which is JAC-11. Nobody read this source for "
                   "four months because the dead login was taken to mean the "
                   "source was dark. It never did."
                   % (("%d advert(s) read on the last run, %d on-package"
                       % ((pcounts or {}).get("adverts", 0),
                          (pcounts or {}).get("glazing", 0)))
                      if pcounts else "Not reached on the last run"),
         "cost": "Free to READ, no key. An account is needed to bid - JAC-11"},
        {"name": "PlanIt planning applications", "status": "planned",
         "kind": "Schemes 6-18 months out",
         "detail": "Gets Fenster onto the enquiry list before the list exists.",
         "cost": "Free"},
        {"name": "Portal notification emails", "status": "blocked",
         "kind": "In-Tend, ProContract, Delta, Jaggaer",
         "detail": "79 of the 88 portal notices in the last six months arrived "
                   "at info@, and info@ came off Jacob's list on 28/07/2026 at "
                   "Adam's instruction. All 79 were Hightown, who are do-not-"
                   "quote, so nothing is being lost today - but the portal "
                   "registrations point at info@, so the next non-Hightown "
                   "notice will land somewhere Jacob cannot see. JAC-7. And the "
                   "credentials themselves are gone: jayk@fensterglazing.com "
                   "returns a hard 404, so any account registered to him can "
                   "never be password-reset by anybody. Proactis is the "
                   "exception - its username is adam@, so that one is already "
                   "Adam's. JAC-11.",
         "cost": "Free - needs re-registering against commercial@, not a person"},
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
    "status": "drafting",
    "note": ("JAC-1 answered on 28/07: drafts only for now. So the drafting "
             "half of this is live and the sending half is not - there is "
             "still no send path, no mailbox and no request for one. Every "
             "draft on the board is written and waiting for a human to send "
             "it from their own mailbox, under their own name."),
    "classes": [
        {"name": "Quote follow-up", "why": "We sent a price and heard nothing back",
         "example": "Ninn Lane - GBP 100,730 issued 09/07, nothing back in 19 days",
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
                 "Decide later - drafts only for now"],
     "answer": "Decide later - drafts only for now",
     # The author was in doubt for an hour on 29/07: hub 23/24/25 were posted
     # while the sign-in defaulted to Zac, and Adam (hub-66) said his messages
     # had been filing under that name. Settled as Zac's on Adam's own division
     # of roles (hub-68) - Zac built me and owns what I am allowed to do, Adam
     # owns the pipeline. Whether I send under my own name is the first kind.
     "answeredBy": "Zac", "answered": "2026-07-28",
     "effect": ("Drafting is live; sending is not. The drafts are on the "
                "board, each addressed to a named person and each to be sent "
                "by a named human from their own mailbox. Nothing goes out "
                "under my name and I have not asked for a mailbox. When this "
                "is picked up again the question is unchanged - the drafts "
                "just make it concrete rather than hypothetical. On the author: "
                "this was posted while the hub's sign-in defaulted to Zac, so "
                "it was queried with Adam and settled as Zac's on his own "
                "answer - Zac built me and owns what I am allowed to do, Adam "
                "owns the pipeline. Loosening this is Zac's call. It now has a "
                "concrete case: Adam authorised ONE outgoing email on hub-74 "
                "(29/07) - a daily lead-chase list to adam@ and nothing else. "
                "It is built and it runs (jacob_daily_email.py); it does not "
                "send, because his authority over the pipeline is not authority "
                "over what I am allowed to do. JAC-15 asks Zac.")},
    {"id": "JAC-2", "title": "Cold outreach at all, or warm only?",
     "why": ("Warm-only needs no new domain, no consent register and carries "
             "almost no risk. Cold needs both."),
     "options": ["Warm only", "Warm now, cold later", "Both"]},
    {"id": "JAC-3", "title": "Budget for paid project intelligence?",
     "why": ("Free feeds are public sector only. Stepnell, Borras, Chigwell "
             "and Guildmore work never appears in them. First hard evidence, "
             "29/07: the two live leads off the Supply2Gov alerts - Ryde "
             "windows, closing 28 August, and Corby communal doors - are in "
             "neither free feed. 353 tender-stage releases swept across "
             "Contracts Finder and Find a Tender over 21 days, no match, on a "
             "sweep proved good by finding a notice already on this board. "
             "The honest size of the prize is that four days of those alerts "
             "produced two live on-package mainland leads, not the 27 a day "
             "the alert header claims - half of what it sends is already "
             "awarded, and several of the live ones are Irish."),
     "options": ["Free sources only", "Pay for the Supply2Gov level that "
                 "shows the buyer", "Trial Barbour ABI", "Trial Glenigan"]},
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
    if t.get("handoverIssued"):
        # "verified" means somebody read the message leaving the building. Once a
        # row can get here on AdminBase's word alone, saying all of them are
        # verified is a lie the size of the unverified ones.
        unver = sum(1 for r in (data.get("handover") or {}).get("issued", [])
                    if not r.get("verified"))
        print("  handover: %d quotes issued (%s)%s, %d chaseable today "
              "(%s), %d priced but never issued"
              % (t["handoverIssued"], gbp(t["handoverValue"]),
                 ", %d NOT verified against a send" % unver if unver
                 else " and all verified",
                 t["handoverDue"], gbp(t["handoverDueValue"]), t["handoverHeld"]))
    print("  board window %d days (from %s); %d older signals held back; "
          "mail read from %s%s"
          % (t["boardDays"], t["boardFrom"], t["signalsOlder"], t["mailFrom"],
             "; TRUNCATED: " + ", ".join(t["mailTruncated"])
             if t["mailTruncated"] else ""))
    print("  %d actions on the Today page, %d dormant clients who have bought"
          % (len(data["actions"]), t["dormantWon"]))
    if t.get("crmRows"):
        print("  AdminBase: %d quoted leads, %d clients, GBP %s ex VAT; "
              "%d chaseable (GBP %s), %d silent over a year"
              % (t["crmRows"], t["crmClients"], gbp(t["crmValue"])[4:],
                 t["crmDue"], gbp(t["crmDueValue"])[4:], t["crmYearSilent"]))
        print("  %d drafts written and waiting for a human" % t["drafts"])
    if t.get("mailExcluded"):
        print("  mailboxes NOT read: %s"
              % "; ".join("%s (%s)" % (m["mailbox"], m["why"]) for m in t["mailExcluded"]))
    print("  %d contracts out to bid (%d Adam's CPV list, %d closing inside a week)"
          % (t["tenders"], t["tendersDirect"], t["tendersClosing"]))
    if t.get("winRate") is not None:
        print("  BD-log history: %.0f%% win rate, median win GBP %s, no log win over GBP %s"
              % (t["winRate"], format(t["wonMedian"] or 0, ","),
                 format(t["noWinAbove"] or 0, ",")))
        print("  %d rows still open on the current BD sheet" % t["openThisYear"])

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
        def run(env=None):
            # One deploy at a time across Mary, Jacob and dev sessions - see
            # scripts/deploy_lock.py for the 29/07 race that made this exist.
            import deploy_lock
            with deploy_lock.held():
                return subprocess.run(
                    ["npx.cmd", "wrangler", "pages", "deploy", "public",
                     "--project-name", "mary-dashboard", "--branch", "main",
                     "--commit-dirty=true"],
                    cwd=os.path.join(REPO, "dashboard"), capture_output=True,
                    text=True, encoding="utf-8", errors="replace", timeout=600,
                    shell=True, env=env)

        r = run()
        # npx unpacks wrangler into the shared npm cache, and a long-running
        # `wrangler pages dev` elsewhere on the machine keeps a handle on it -
        # the deploy then dies on EBUSY renaming miniflare, having built a
        # perfectly good bundle. It is not a deploy failure and retrying into
        # the same cache will not fix it, so retry into a private one.
        if r.returncode != 0 and "EBUSY" in (r.stdout + r.stderr):
            print("deploy: npm cache is locked by another process - "
                  "retrying with a private cache")
            env = dict(os.environ)
            env["npm_config_cache"] = os.path.join(
                REPO, "test-results", "npm-cache")
            r = run(env)
        print("deploy exit", r.returncode)
        # wrangler emits box-drawing characters and this stdout is cp1252 -
        # re-encode rather than let a successful deploy die on its own log.
        enc = sys.stdout.encoding or "utf-8"
        out = r.stdout + r.stderr
        print(out[-500:].encode(enc, "replace").decode(enc, "replace"))
        # The one check worth making on a "successful" deploy. Without the
        # functions bundle every /api route serves the SPA's HTML instead and
        # the hub dies on "Unexpected token '<'" - which looks nothing like a
        # deploy problem when you are staring at it an hour later.
        if r.returncode == 0 and "Functions bundle" not in out:
            print("deploy WARNING: no Functions bundle in the output. The "
                  "static site shipped without its API. Check the working "
                  "directory - this must run from inside dashboard/.")
        return r.returncode


if __name__ == "__main__":
    sys.exit(main())

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

    out = list(rows.values())
    # Most recently active first, then the ones we have most history with.
    out.sort(key=lambda r: (r["lastContact"], len(r["contacts"])), reverse=True)
    return out


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

    intake = load_json(INTAKE)
    jayk = load_json(JAYK)
    rel = build_relationships(clients, intake, jayk)

    # Dormant = we have quoted them, and no email in the window. That is the
    # cheapest lead in the business: they already asked us for a price once.
    dormant = [r for r in rel
               if r["relationship"] in ("won", "quoted") and not r["lastContact"]]

    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            "jaykContacts": len((jayk or {}).get("contacts", [])),
        },
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
            "rows": rel[:300],
            "dormant": len(dormant),
        },
        "outreach": OUTREACH,
        "decisions": DECISIONS,
    }


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

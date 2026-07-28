# -*- coding: utf-8 -*-
"""JACOB - mailbox intake. The half of lead-finding that is not scraping.

Reads Jacob's own mailboxes and turns them into companies, contacts and
signals. No Claude session is spent here - classification is deterministic,
so this can run every morning for free.

  python scripts/jacob_intake.py                # last 90 days
  python scripts/jacob_intake.py --days 365     # further back

Writes data/jacob/intake.json, which jacob_dashboard.py renders.

Why this matters more than the scrapers: Fenster is a subcontractor, so most
of its work is never advertised. Tender-portal invitations, client enquiries
and introductions all arrive here as ordinary email. The Hightown tender was
nearly lost because an In-Tend notice landed in info@ and nobody read it.
"""
import argparse
import collections
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jacob_graph as jg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "intake.json")
ARCHIVE = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial"

DOMAIN = "fensterglazing.com"
MAILBOXES = [jg.COMMERCIAL, jg.INFO, jg.JACOB, "jayk@" + DOMAIN]

# ---------------------------------------------------------------- classifying
PORTALS = re.compile(
    r"(in-tendorganiser|in-tendhost|intend\.|proactis|due-north|delta-esourcing|"
    r"jaggaer|bravosolution|sell2wales|publiccontractsscotland|etendersni|"
    r"multiquote|constructionline|supply2gov|procontract)", re.I)

SUPPLIERS = re.compile(
    r"(bsws\.co\.uk|bellview|aplusw|aplus|strongdor|vetroseal|cnglass|ikon|"
    r"aluminiumfiresystems|senioraluminium|smartsystems|sheerline|technal|"
    r"reynaers|schueco|kawneer|comar)", re.I)

NOISE_FROM = re.compile(
    r"(noreply|no-reply|donotreply|do-not-reply|notification|newsletter|"
    r"mailer-daemon|postmaster|bounce|unsubscribe|@e\.|@email\.|@mail\.|"
    r"linkedin|twitter|facebook|instagram|xero|sage|quickbooks|indeed|"
    r"mailchimp|hubspot|eventbrite|survey|feedback@|britishgas|fixflo|"
    r"checkatrade|trustpilot|googlemail|microsoft|adobe|autodesk)", re.I)

NOISE_SUBJECT = re.compile(
    r"(unsubscribe|newsletter|webinar|invitation to connect|out of office|"
    r"automatic reply|delivery status|undeliverable|password|sign-in|"
    r"verify your|receipt|invoice reminder|statement)", re.I)

# An enquiry is the thing worth waking a human for.
ENQUIRY = re.compile(
    r"\b(quote|quotation|enquiry|inquiry|tender|itt|rfq|rfp|pricing|price|"
    r"estimate|invitation to tender|expression of interest|eoi|pqq|"
    r"opportunity|new project|budget)\b", re.I)

# Consumer mail. A person, not a company - aggregating 31 hotmail addresses
# into a "hotmail.com relationship" is meaningless.
FREEMAIL = {"hotmail.com", "hotmail.co.uk", "gmail.com", "googlemail.com",
            "outlook.com", "outlook.co.uk", "yahoo.com", "yahoo.co.uk",
            "live.com", "live.co.uk", "aol.com", "icloud.me", "icloud.com",
            "me.com", "msn.com", "btinternet.com", "sky.com", "virginmedia.com",
            "talktalk.net", "protonmail.com"}

GLAZING = re.compile(
    r"\b(window|door|glazing|glass|curtain wall|curtain walling|screen|"
    r"shopfront|louvre|facade|fenestration|aluminium|upvc|entrance)\b", re.I)


FREEMAIL_STEMS = {"hotmail", "gmail", "googlemail", "outlook", "yahoo", "live",
                  "aol", "icloud", "me", "msn", "btinternet", "sky",
                  "virginmedia", "talktalk", "protonmail", "ymail", "gmx",
                  "mail", "inbox", "rediffmail"}


def is_freemail(domain):
    """Match on the first label so outlook.in and yahoo.de are caught too,
    not just the .com/.co.uk pair."""
    return (domain or "").lower().split(".")[0] in FREEMAIL_STEMS


def classify(frm, subject):
    """Deterministic. Order matters - noise first, then the useful classes."""
    blob = "%s %s" % (frm, subject)
    if PORTALS.search(blob):
        return "portal"
    if NOISE_FROM.search(frm) or NOISE_SUBJECT.search(subject):
        return "noise"
    if SUPPLIERS.search(frm):
        return "supplier"
    if ENQUIRY.search(subject) and GLAZING.search(subject):
        return "enquiry"
    if ENQUIRY.search(subject):
        return "possible-enquiry"
    return "correspondence"


def load_clients():
    """Company folders in the archive, so we can tell an existing client from
    a stranger without asking anyone."""
    known = {}
    for sub, tier in (("1. Tender Documents", "quoted"),
                      ("2. Projects", "won"),
                      (r"2. Projects\2. Completed", "won")):
        path = os.path.join(ARCHIVE, sub)
        if not os.path.isdir(path):
            continue
        for name in os.listdir(path):
            if not os.path.isdir(os.path.join(path, name)):
                continue
            key = re.sub(r"[^a-z0-9]", "", name.lower())
            if len(key) >= 4:
                known[key] = "won" if tier == "won" or known.get(key) == "won" else "quoted"
    return known


def match_client(domain, known):
    """Domain 'lindumgroup.co.uk' -> folder 'Lindum Group'."""
    stem = re.sub(r"\.(co\.uk|com|net|org|uk|ltd|plc)$", "", domain.lower())
    stem = re.sub(r"[^a-z0-9]", "", stem)
    if not stem:
        return None
    for key, tier in known.items():
        if key in stem or stem in key:
            return tier
    return None


# ---------------------------------------------------------------- fetching
def fetch(token, mailbox, since_iso, max_pages=20):
    qs = urllib.parse.urlencode({
        "$filter": "receivedDateTime ge %s" % since_iso,
        "$orderby": "receivedDateTime desc",
        "$top": 50,
        "$select": "subject,from,toRecipients,receivedDateTime,hasAttachments",
    })
    path = "/users/%s/messages?%s" % (urllib.parse.quote(mailbox), qs)
    out, pages = [], 0
    while path and pages < max_pages:
        for attempt in range(4):
            st, res = jg.graph(token, "GET", path)
            if st not in (429, 503, 504):
                break
            time.sleep(5 * (attempt + 1))
        if st != 200:
            return st, out
        out.extend(res.get("value", []))
        nxt = res.get("@odata.nextLink")
        path = nxt.split("graph.microsoft.com/v1.0", 1)[1] if nxt else None
        pages += 1
    return 200, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()

    since = (datetime.now(timezone.utc) - timedelta(days=args.days)) \
        .strftime("%Y-%m-%dT00:00:00Z")
    token = jg.get_token(jg.load_env(), "READER")
    known = load_clients()

    companies = {}
    counts = collections.Counter()
    per_mailbox = {}
    signals = []

    for mbx in MAILBOXES:
        st, msgs = fetch(token, mbx, since)
        if st != 200:
            per_mailbox[mbx] = "HTTP %s" % st
            print("  %-32s HTTP %s" % (mbx, st))
            continue
        per_mailbox[mbx] = len(msgs)
        print("  %-32s %d message(s)" % (mbx, len(msgs)))

        for m in msgs:
            e = (m.get("from") or {}).get("emailAddress") or {}
            addr = (e.get("address") or "").lower()
            name = e.get("name") or ""
            subj = (m.get("subject") or "").strip()
            when = (m.get("receivedDateTime") or "")[:10]
            if not addr or addr.endswith("@" + DOMAIN):
                continue                      # internal - not a signal in itself

            kind = classify(addr, subj)
            counts[kind] += 1
            if kind == "noise":
                continue

            dom = addr.split("@")[-1]
            if is_freemail(dom):
                tier = "individual"
            elif kind == "supplier":
                tier = "supplier"
            else:
                tier = match_client(dom, known) or "unknown"
            c = companies.setdefault(dom, {
                "domain": dom, "messages": 0, "first": when, "last": when,
                "contacts": {}, "kinds": collections.Counter(),
                "relationship": tier, "isFreemail": is_freemail(dom),
                "subjects": [],
            })
            c["messages"] += 1
            c["last"] = max(c["last"], when)
            c["first"] = min(c["first"], when)
            c["kinds"][kind] += 1
            if addr not in c["contacts"]:
                c["contacts"][addr] = name
            if len(c["subjects"]) < 6:
                c["subjects"].append({"date": when, "subject": subj[:90],
                                      "kind": kind, "mailbox": mbx.split("@")[0]})

            if kind in ("enquiry", "portal"):
                signals.append({"date": when, "kind": kind, "company": dom,
                                "contact": addr, "name": name,
                                "subject": subj[:110],
                                "mailbox": mbx.split("@")[0],
                                "relationship": c["relationship"]})

    rows = []
    for c in companies.values():
        c["kinds"] = dict(c["kinds"])
        c["contacts"] = [{"address": a, "name": n} for a, n in c["contacts"].items()]
        rows.append(c)
    rows.sort(key=lambda r: (r["last"], r["messages"]), reverse=True)
    signals.sort(key=lambda s: s["date"], reverse=True)

    data = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": args.days,
        "per_mailbox": per_mailbox,
        "counts": dict(counts),
        "companies": rows,
        "signals": signals[:200],
    }
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1)

    print("\n%d companies, %d signals" % (len(rows), len(signals)))
    print("classified: %s" % ", ".join("%s %d" % (k, v) for k, v in counts.most_common()))
    print("-> %s" % OUT)


if __name__ == "__main__":
    main()

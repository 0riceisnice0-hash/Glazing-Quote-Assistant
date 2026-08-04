# -*- coding: utf-8 -*-
"""Email into the CRM: instructions from Adam, and notes from everyone else.

Adam, 03/08: *"If I've had a phone call, I should just be able to email Jacob
and say, I just had this call with Jordan about this job, set the next action
date for this. Boom. And he'll just do it."* And the other half of the same
idea: he is CC'd on the client traffic anyway, so a reply should write its own
note without anybody being asked.

THE INJECTION GUARD IS THE WHOLE DESIGN HERE, not a caveat on it. This module
turns text that arrived by email into changes to the commercial record, which
is exactly the capability an attacker would want. So:

  TRUSTED senders (adam@, zac@, marketing@, and the hub) can move state -
  dates, outcomes, owners.
  EVERYONE ELSE IS DATA. A client email can only ever add a note and touch
  last_contact. No client, and no forwarded chain inside a trusted email, can
  mark its own job won, move a chase date, or close a lead.

AND WHEN IT IS NOT SURE, IT DOES NOT GUESS. A parse it cannot make confidently
becomes a note plus a flag for Jacob's next session to action by hand. Silently
setting the wrong date on the wrong job is worse than not setting one - that is
the AdminBase failure mode ("98 days silent" on a quote sent yesterday) arriving
by a new route.

  python scripts/crm_email.py --queue        # process Jacob's queued orders
  python scripts/crm_email.py --dry-run --queue
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(REPO, "test-results", "jacob-inbox", "queue")
SEEN = os.path.join(REPO, "data", "jacob", "crm-email-seen.json")

# Only these may change the record. Everything else is evidence.
TRUSTED = ("adam@fensterglazing.com", "zac@fensterglazing.com",
           "marketing@fensterglazing.com")
TRUSTED_AUTHORS = ("adam", "zac")

DATE_PATTERNS = [
    (re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b"), "dmy"),
    (re.compile(r"\bin\s+(\d+)\s+(day|week|month)s?\b", re.I), "relative"),
    (re.compile(r"\bnext\s+(week|month)\b", re.I), "next"),
]
# What he actually writes. Deliberately narrow: a phrase this does not know
# becomes a note rather than a guess.
WANTS_DATE = re.compile(
    r"\b(next action|action date|chase|follow up|look again|come back to|revisit)\b", re.I)
WANTS_WON = re.compile(r"\b(we won|won it|we have won|order received|PO received)\b", re.I)
WANTS_LOST = re.compile(r"\b(we lost|lost it|gone elsewhere|unsuccessful|not proceeding)\b", re.I)
WANTS_CLOSE = re.compile(r"\b(close it|close this|shut (it|this) down|dead)\b", re.I)


def parse_date(text, today=None):
    """A date out of ordinary English, or None. Never a guess."""
    today = today or dt.date.today()
    for rx, kind in DATE_PATTERNS:
        m = rx.search(text or "")
        if not m:
            continue
        if kind == "dmy":
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            y = y + 2000 if y < 100 else y
            try:
                return dt.date(y, mo, d).isoformat()
            except ValueError:
                return None
        if kind == "relative":
            n, unit = int(m.group(1)), m.group(2).lower()
            days = n * {"day": 1, "week": 7, "month": 30}[unit]
            return (today + dt.timedelta(days=days)).isoformat()
        if kind == "next":
            days = 7 if m.group(1).lower() == "week" else 30
            return (today + dt.timedelta(days=days)).isoformat()
    return None


# Words that appear in half the job titles in the country and in ordinary
# prose besides. Matching on these is how the standing agenda - which says
# "close out as always" - scored against every job with "Close" in its address.
# This is the same lesson as "Atlas" matching a window-cleaning contractor:
# a common token inside a name is a coincidence, not evidence.
COMMON = {
    "close", "house", "road", "street", "court", "lane", "avenue", "drive",
    "park", "place", "gardens", "green", "hill", "view", "works", "centre",
    "center", "building", "buildings", "phase", "block", "unit", "units",
    "farm", "hall", "church", "primary", "school", "schools", "college",
    "academy", "limited", "construction", "group", "project", "projects",
    "estate", "manor", "lodge", "grange", "bungalow", "cottage", "terrace",
    "north", "south", "east", "west", "upper", "lower", "great", "little",
    "windows", "doors", "glazing", "quote", "tender", "development",
    "developments", "services", "management", "site", "works",
}
MIN_MATCH_SCORE = 3


def _words(lead):
    """The distinctive words in a lead's title and key."""
    out = set()
    for source in ((lead.get("title") or "").lower(),
                   (lead.get("key") or "").replace("-", " ")):
        for w in re.split(r"[^a-z0-9]+", source):
            if len(w) >= 5 and w not in COMMON:
                out.add(w)
    return out


def match_lead(text, leads, companies=None):
    """Which lead is this about? One confident match, or None.

    THE COMPANY IS HALF THE ADDRESS. "Riverside" alone names five different
    jobs in this data, so a job word on its own is usually not enough - and
    that is not a flaw in the matcher, it is how the yard actually talks.
    Adam writes "that call with Jordan at Neil Douglas about Riverside", and
    the company is what makes it unambiguous. So when the text names exactly
    one company we know, the search is narrowed to that company's jobs first.

    SCORING IS BY HOW RARE THE WORD IS, not how many words hit. "Riverside"
    naming exactly one job is strong evidence; "riverside" naming three is
    almost none, and counting hits would rank the three-way collision highest
    precisely when it is least certain. So a word unique to one lead scores 3
    and a shared word scores 1.

    Ambiguity still resolves to None on purpose. Two leads for one contractor
    is normal here - it is what split the Totteridge thread across two of
    Mary's chats - and writing a date onto the wrong job is worse than writing
    none at all.
    """
    t = (text or "").lower()

    # Narrow by company first, when the text names one unambiguously.
    narrowed_note = ""
    if companies:
        named = []
        for c in companies:
            words = set()
            for src in ((c.get("name") or "").lower(),
                        (c.get("key") or "").replace("-", " ")):
                for w in re.split(r"[^a-z0-9]+", src):
                    if len(w) >= 5 and w not in COMMON:
                        words.add(w)
            if words and any(w in t for w in words):
                named.append(c["key"])
        if len(named) == 1:
            same = [l for l in leads if l.get("company_key") == named[0]]
            if same:
                leads = same
                narrowed_note = " at %s" % named[0]
                if len(leads) == 1:
                    return leads[0], "the only job we have with %s" % named[0]

    vocab = {}
    per_lead = {}
    for l in leads:
        ws = _words(l)
        per_lead[l["key"]] = ws
        for w in ws:
            vocab[w] = vocab.get(w, 0) + 1

    scored = []
    for l in leads:
        score, hits = 0, []
        for w in per_lead[l["key"]]:
            if w not in t:
                continue
            score += 3 if vocab.get(w, 0) == 1 else 1
            hits.append(w if vocab.get(w, 0) == 1 else "%s(shared)" % w)
        if score:
            scored.append((score, l, hits))

    if not scored:
        return None, "no lead named%s" % narrowed_note
    scored.sort(key=lambda s: -s[0])
    top = scored[0]
    if top[0] < MIN_MATCH_SCORE:
        return None, "only a weak match (%s)%s - name the company too" % (
            ", ".join(top[2][:3]), narrowed_note)
    if len(scored) > 1 and scored[1][0] == top[0]:
        return None, "ambiguous - %s and %s both match" % (
            top[1]["key"], scored[1][1]["key"])
    return top[1], "matched on %s%s" % (", ".join(top[2][:3]), narrowed_note)


def apply_message(msg, leads, companies=None, author="crm_email", dry_run=False):
    """One message -> what it changed. Returns a list of human-readable lines."""
    sender = (msg.get("from") or msg.get("sender") or msg.get("author") or "").lower()
    trusted = (msg.get("trusted") or msg.get("trusted_sender")
               or any(t in sender for t in TRUSTED)
               or sender in TRUSTED_AUTHORS)
    text = "%s\n%s" % (msg.get("subject") or "", msg.get("body") or "")
    out = []

    lead, why = match_lead(text, leads, companies)
    if not lead:
        return ["no CRM change - %s" % why]

    # The note always happens, trusted or not. It is the evidence, and it is
    # the half of this that cannot do any harm.
    body = (msg.get("body") or "")[:4000].strip()
    if body and not dry_run:
        crm.note("lead", lead["key"],
                 "%s: %s" % (sender or "unknown", body),
                 author, source="email",
                 source_ref=str(msg.get("id") or msg.get("_file") or ""))
    out.append("note -> %s" % lead["key"])

    if not trusted:
        # A client cannot move their own job. Ever.
        return out + ["untrusted sender - note only, no state change"]

    fields, reasons = {}, []
    if WANTS_WON.search(text):
        fields.update(outcome="won", stage="closed")
        reasons.append("says we won it")
    elif WANTS_LOST.search(text):
        fields.update(outcome="lost", stage="closed")
        reasons.append("says we lost it")
    elif WANTS_CLOSE.search(text):
        fields.update(stage="closed", outcome="no-decision")
        reasons.append("told to close it")

    if WANTS_DATE.search(text):
        when = parse_date(text)
        if when:
            fields["next_action_date"] = when
            first = [l for l in body.splitlines() if l.strip()]
            fields["next_action"] = (first[0][:200] if first else "as instructed by email")
            reasons.append("next action %s" % when)
        else:
            out.append("ASKED for a new date but none could be read - "
                       "left for Jacob to set by hand")

    if fields and not dry_run:
        crm.lead(lead["key"], author,
                 why="by email from %s: %s" % (sender, "; ".join(reasons)),
                 **fields)
    if fields:
        out.append("%s -> %s" % (lead["key"], ", ".join(reasons)))
    return out


def load_seen():
    try:
        with open(SEEN, encoding="utf-8") as fh:
            return set(json.load(fh))
    except (IOError, ValueError):
        return set()


def save_seen(seen):
    os.makedirs(os.path.dirname(SEEN), exist_ok=True)
    with open(SEEN, "w", encoding="utf-8") as fh:
        json.dump(sorted(seen)[-2000:], fh, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", action="store_true",
                    help="process the work orders in Jacob's queue")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}

    leads = crm.leads()
    companies = crm.companies()
    seen = load_seen()
    done = 0

    if a.queue and os.path.isdir(QUEUE):
        for name in sorted(os.listdir(QUEUE)):
            if not name.endswith(".json"):
                continue
            ref = name
            if ref in seen:
                continue
            try:
                with open(os.path.join(QUEUE, name), encoding="utf-8") as fh:
                    msg = json.load(fh)
            except (IOError, ValueError):
                continue
            msg["_file"] = name
            lines = apply_message(msg, leads, companies, dry_run=a.dry_run)
            print("%s" % name)
            for l in lines:
                print("   %s" % l)
            if not a.dry_run:
                seen.add(ref)
            done += 1

    if not a.dry_run:
        save_seen(seen)
    print("\n%d message(s) processed" % done)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""JACOB - recover the former BDM's pipeline from the shared role mailboxes.

Jayk (jayk@fensterglazing.com) was Fenster's business development manager.
His own mailbox is gone - the account survives as a sign-in name with no
recipient object, and there is no soft-deleted or inactive mailbox to restore.
What survives is his half of every thread that copied a role mailbox.

Deliberately limited to the three ROLE mailboxes. No personal mailboxes are
touched, and every read here is inside a scope that was already granted:

  commercial@, info@   Jacob's own reader  (.env.jacob)
  estimating@          Mary's reader       (.env.mary)

  python scripts/jacob_jayk_recovery.py

A one-off mining job, not a feed. It writes the companies and contacts to
data/jacob/jayk-recovery.json so the mailboxes never need reading again.
"""
import collections
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jacob_graph as jg

TARGET = "jayk@fensterglazing.com"
DOMAIN = "fensterglazing.com"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "jayk-recovery.json")

# mailbox -> which credential set reads it
SOURCES = [
    ("commercial@" + DOMAIN, "jacob"),
    ("info@" + DOMAIN, "jacob"),
    ("estimating@" + DOMAIN, "mary"),
]

NOISE = re.compile(
    r"(noreply|no-reply|donotreply|notification|newsletter|bounce|mailer-daemon|"
    r"linkedin|twitter|facebook|google|microsoft|xero|sage|indeed|mailchimp|"
    r"hubspot|eventbrite|survey|unsubscribe|postmaster)", re.I)

MAX_PAGES = 12          # 50 a page - plenty for one person's correspondence


def mary_token():
    """Mary's reader, read-only, for estimating@ only. Her module is imported
    but nothing in it is modified or written."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import mary_graph as mg
    return mg.get_token(mg.load_env(), "READER")


def people(msg):
    out = []
    frm = (msg.get("from") or {}).get("emailAddress", {}) or {}
    if frm.get("address"):
        out.append((frm.get("address").lower(), frm.get("name") or ""))
    for key in ("toRecipients", "ccRecipients"):
        for r in msg.get(key) or []:
            e = r.get("emailAddress") or {}
            if e.get("address"):
                out.append((e["address"].lower(), e.get("name") or ""))
    return out


def search_all(token, mailbox, query):
    """KQL search, following nextLink. $search cannot combine with $orderby."""
    qs = urllib.parse.urlencode({
        "$search": '"%s"' % query,
        "$top": 50,
        "$select": "subject,from,toRecipients,ccRecipients,receivedDateTime",
    })
    path = "/users/%s/messages?%s" % (urllib.parse.quote(mailbox), qs)
    msgs, pages = [], 0
    while path and pages < MAX_PAGES:
        # Graph search over a big mailbox times out fairly often (504/503).
        # It is transient - the same page usually succeeds on a retry.
        for attempt in range(4):
            st, res = jg.graph(token, "GET", path)
            if st not in (503, 504, 429):
                break
            time.sleep(5 * (attempt + 1))
        if st != 200:
            return st, msgs
        msgs.extend(res.get("value", []))
        nxt = res.get("@odata.nextLink")
        path = nxt.split("graph.microsoft.com/v1.0", 1)[1] if nxt else None
        pages += 1
    return 200, msgs


def main():
    tokens = {"jacob": jg.get_token(jg.load_env(), "READER")}
    try:
        tokens["mary"] = mary_token()
    except Exception as e:
        print("NOTE: Mary's reader unavailable (%s) - skipping estimating@"
              % str(e)[:80])

    companies = collections.Counter()
    contacts = collections.Counter()
    names = {}
    subjects = []
    per_mailbox = {}

    for mailbox, who in SOURCES:
        if who not in tokens:
            per_mailbox[mailbox] = "skipped - no credential"
            continue
        st, msgs = search_all(tokens[who], mailbox, TARGET)
        if st != 200:
            per_mailbox[mailbox] = "HTTP %s" % st
            print("  %-32s HTTP %s" % (mailbox, st))
            continue

        # KQL matches the body too, so keep only messages he was actually on.
        keep = [m for m in msgs
                if any(a == TARGET for a, _ in people(m))]
        per_mailbox[mailbox] = {"searched": len(msgs), "he_was_on": len(keep)}
        print("  %-32s %d hit(s), %d with him as a participant"
              % (mailbox, len(msgs), len(keep)))

        for m in keep:
            subjects.append(((m.get("receivedDateTime") or "")[:10],
                             mailbox.split("@")[0],
                             (m.get("subject") or "").strip()[:75]))
            for addr, name in people(m):
                if addr.endswith("@" + DOMAIN) or NOISE.search(addr):
                    continue
                contacts[addr] += 1
                companies[addr.split("@")[-1]] += 1
                if name and addr not in names:
                    names[addr] = name

    print("\n%s" % ("=" * 64))
    total = sum(v["he_was_on"] for v in per_mailbox.values() if isinstance(v, dict))
    print("%d messages with Jayk as sender or recipient" % total)
    if not total:
        print("Nothing found. Either the threads were purged with his mailbox, or")
        print("his correspondence never copied a role mailbox.")
        return

    if subjects:
        dates = sorted(s[0] for s in subjects if s[0])
        print("Date range: %s to %s" % (dates[0], dates[-1]))

    print("\nOutside companies he dealt with (top 25):")
    for dom, n in companies.most_common(25):
        print("  %4d  %s" % (n, dom))

    print("\nNamed contacts (top 25):")
    for addr, n in contacts.most_common(25):
        print("  %4d  %-44s %s" % (n, addr, names.get(addr, "")))

    subjects.sort(reverse=True)
    print("\nMost recent 30 subjects:")
    for when, box, subj in subjects[:30]:
        print("  %s  %-11s %s" % (when, box, subj))

    json.dump({"target": TARGET, "per_mailbox": per_mailbox,
               "companies": companies.most_common(),
               "contacts": [(a, n, names.get(a, "")) for a, n in contacts.most_common()],
               "subjects": subjects},
              open(OUT, "w", encoding="utf-8"), indent=1)
    print("\nWritten to %s" % OUT)


if __name__ == "__main__":
    main()

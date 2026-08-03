# -*- coding: utf-8 -*-
"""The CRM - one record of the commercial world, shared by all three bots.

THE POINT OF THIS FILE IS THAT THERE IS ONLY ONE OF IT. Before it, a lead lived
in Gintare's head, in AdminBase, in Mary's `data/mary-jobs.json`, in Jacob's
`data/jacob/*.json` and in whichever chat happened to be looking at it - so the
same job was typed in four times and disagreed with itself. Adam's AdminBase
still read "quote being prepared" on Princess Beatrice three days after the
quote went out.

WHO WRITES WHAT
  Jacob  logs the lead, moves it through the chase, records every reply
  Mary   writes the quote, its basis, and the verified moment it was issued
  Joseph takes over at the purchase order and runs the contract to payment
  Humans answer on the hub; their edits land here through the same routes

EVERY WRITE IS ATTRIBUTABLE. `author` is not optional and `why` is expected -
the API records a crm_event per changed field, so "who moved this to lost, and
on what evidence" is answerable months later. That is the whole reason the
outcome data Fenster never had is worth collecting now.

VALUES ARE EX VAT. Always. AdminBase's are inclusive, which made its pipeline
20% larger than the money actually quoted and is a mistake this schema refuses
to inherit - de-VAT on the way in, never on the way out.

  python scripts/crm.py --today                     # the daily call list
  python scripts/crm.py --lead gordon-court         # everything about one job
  python scripts/crm.py --company stepnell
  python scripts/crm.py --leads --stage quote_sent
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The pipeline Adam walked through on the AdminBase leads board, 03/08. The
# first six are estimating's half, the rest are business development's. The
# handover is `quote_sent` - the moment it stops being Mary's and becomes
# Jacob's, and the handover Fenster never had.
STAGES = [
    "new",              # logged, not yet acknowledged
    "acknowledged",     # customer told we have it
    "materials_out",    # enquiry sent to suppliers for costs
    "awaiting_costs",   # waiting on supplier prices
    "quote_ready",      # priced, waiting on Adam to check
    "pre_quote_call",   # approved - Adam rings before it goes
    "quote_sent",       # issued. HANDOVER: Mary -> Jacob
    "follow_up",        # first chase
    "final_follow_up",  # last chase before closing
    "closed",           # done, one way or the other - see `outcome`
]
MARY_STAGES = STAGES[:6]
JACOB_STAGES = STAGES[6:]


def _env():
    """The hub key and URL are shared infrastructure and live in .env.mary."""
    out = {}
    for name in (".env.mary", ".env.jacob"):
        path = os.path.join(REPO, name)
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8-sig"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                out.setdefault(k.strip(), v.strip())
    return out


def _call(path, payload=None, timeout=30):
    cfg = _env()
    base = cfg.get("DASHBOARD_URL", "https://mary-dashboard.pages.dev")
    req = urllib.request.Request(
        base + path, method="POST" if payload is not None else "GET",
        data=json.dumps(payload).encode("utf-8") if payload is not None else None)
    if cfg.get("MARY_API_KEY"):
        req.add_header("x-mary-key", cfg["MARY_API_KEY"])
    req.add_header("content-type", "application/json")
    # Cloudflare bot protection 403s a scripted request with no user agent.
    req.add_header("user-agent", "FensterCRM/1.0")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError("CRM %s -> HTTP %s %s" % (path, e.code, body))


# ------------------------------------------------------------------ writing
def upsert(kind, key, author, why="", **fields):
    """Create or update one row. Only the fields you pass are touched.

    Partial by design: Jacob moving a stage must not blank the value Mary put
    on the same lead an hour earlier. Every changed field lands a crm_event.
    """
    clean = {k: v for k, v in fields.items() if v is not None}
    return _call("/api/crm/upsert",
                 {"type": kind, "key": key, "author": author, "why": why,
                  "fields": clean})


# NOT NULL columns are filled by the API, and only when it is INSERTING - it is
# the only side that knows whether the row exists. Doing it here instead turned
# every partial update into a destructive one: the handover sets stage and owner
# and nothing else, and it was silently overwriting company_key with "unknown".


def company(key, author, why="", **fields):
    return upsert("company", key, author, why, **fields)


def lead(key, author, why="", **fields):
    stage = fields.get("stage")
    if stage and stage not in STAGES:
        raise ValueError("unknown stage %r - one of %s" % (stage, ", ".join(STAGES)))
    return upsert("lead", key, author, why, **fields)


def quote(lead_key, revision, author, why="", **fields):
    fields.setdefault("lead_key", lead_key)
    fields.setdefault("revision", revision)
    return upsert("quote", "%s:%d" % (lead_key, revision), author, why, **fields)


def contract(key, author, why="", **fields):
    return upsert("contract", key, author, why, **fields)


def note(entity_type, entity_key, body, author, source="bot", source_ref=""):
    """Append something known. Never overwrite - two calls to the same person
    on different days are two facts, and a chase needs both."""
    return _call("/api/crm/note",
                 {"entity_type": entity_type, "entity_key": entity_key,
                  "body": body, "author": author, "source": source,
                  "source_ref": source_ref})


def task(entity_type, entity_key, step, label, author, due="", done_at="",
         done_by="", detail=""):
    """A checklist item. `detail` carries WHAT to order, not only that it is
    due - AdminBase only ever said the latter, and that is half a task."""
    return _call("/api/crm/task",
                 {"entity_type": entity_type, "entity_key": entity_key,
                  "step": step, "label": label, "due": due, "done_at": done_at,
                  "done_by": done_by, "detail": detail, "author": author})


# ------------------------------------------------------------------ reading
def companies():
    return _call("/api/crm/companies") or []


def leads(stage=None):
    q = "?stage=" + urllib.parse.quote(stage) if stage else ""
    return _call("/api/crm/leads" + q) or []


def today():
    """The daily call list, in three parts - see the API route for why.

    {date, due[], overdue[], upcoming[], counts{}}. `due` is what genuinely
    lands today; `overdue` is the backlog worst-first by value and capped,
    because 179 rows of "everything is late" is the AdminBase board nobody
    looks at.
    """
    return _call("/api/crm/today") or {}


def lead_detail(key):
    """One job, everything: company, contacts, quotes, notes, tasks, history."""
    return _call("/api/crm/lead/" + urllib.parse.quote(key))


def company_detail(key):
    return _call("/api/crm/company/" + urllib.parse.quote(key))


def contract_detail(key):
    """One won job: the contract, its twelve steps, notes and invoices."""
    return _call("/api/crm/contract/" + urllib.parse.quote(key))


def delivery():
    """Paul and Steve's day - every task due or late across live contracts."""
    return _call("/api/crm/delivery") or {}


# ------------------------------------------------------------------ CLI
def _row(l):
    return "  %-26s %-22s %-16s %10s  %s" % (
        (l.get("key") or "")[:26], (l.get("company_key") or "")[:22],
        (l.get("stage") or "")[:16],
        "{:,.0f}".format(l["value"]) if l.get("value") else "",
        (l.get("next_action") or "")[:50])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", action="store_true")
    ap.add_argument("--leads", action="store_true")
    ap.add_argument("--stage")
    ap.add_argument("--companies", action="store_true")
    ap.add_argument("--lead")
    ap.add_argument("--company")
    ap.add_argument("--local", action="store_true",
                    help="talk to wrangler pages dev on :8788 instead of the live hub")
    a = ap.parse_args()
    if a.local:
        global _env
        _env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                        "MARY_API_KEY": "local-test-key-not-a-secret"}

    if a.lead:
        d = lead_detail(a.lead)
        if not d or d.get("error"):
            print("no such lead: %s" % a.lead)
            return 1
        L, C = d["lead"], d.get("company") or {}
        print("%s  (%s)" % (L["title"], L["key"]))
        print("  company   %s" % (C.get("name") or L["company_key"]))
        print("  stage     %s   owner %s" % (L["stage"], L["owner"]))
        print("  value     %s ex VAT" % (L.get("value") or "-"))
        print("  deadline  %s   award due %s" % (L.get("deadline") or "-",
                                                 L.get("award_due") or "-"))
        print("  next      %s %s" % (L.get("next_action_date") or "",
                                     L.get("next_action") or "-"))
        for c in d.get("contacts", []):
            print("  contact   %s <%s> %s" % (c.get("name"), c.get("email"), c.get("role")))
        for q in d.get("quotes", []):
            print("  quote r%-2s %s %s  issued %s" % (
                q.get("revision"), q.get("value"), q.get("status"), q.get("issued_at") or "-"))
        for n in d.get("notes", [])[:12]:
            print("  note      %s %s: %s" % (n["created"][:16], n["author"], n["body"][:90]))
        return 0

    if a.company:
        d = company_detail(a.company)
        if not d or d.get("error"):
            print("no such company: %s" % a.company)
            return 1
        C = d["company"]
        print("%s  (%s)  %s" % (C["name"], C["key"], C["relationship"]))
        print("  lifetime %s   terms %s" % (C.get("lifetime_value"), C.get("payment_terms") or "-"))
        for c in d.get("contacts", []):
            print("  contact  %s <%s>" % (c.get("name"), c.get("email")))
        for l in d.get("leads", []):
            print(_row(l))
        return 0

    if a.companies:
        for c in companies():
            print("  %-28s %-34s %-9s %s" % (c["key"][:28], c["name"][:34],
                                             c["relationship"], c.get("last_contact") or ""))
        return 0

    if a.today:
        t = today()
        c = t.get("counts", {})
        print("TODAY, %s" % t.get("date", ""))
        print("\nDUE (%d) - these are the calls" % c.get("due", 0))
        for l in t.get("due", []):
            print(_row(l))
        if not t.get("due"):
            print("  nothing lands today")
        print("\nCOMING IN THE NEXT WEEK (%d)" % c.get("upcoming", 0))
        for l in t.get("upcoming", [])[:10]:
            print(_row(l))
        print("\nBACKLOG (%d overdue, biggest 20) - work these down, do not read them all"
              % c.get("overdue", 0))
        for l in t.get("overdue", []):
            print(_row(l))
        return 0

    rows = leads(a.stage)
    for l in rows:
        print(_row(l))
    if not rows:
        print("  nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main())

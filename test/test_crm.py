# -*- coding: utf-8 -*-
"""Drive one lead through the whole pipeline, as the three bots would."""
import json, sys, urllib.request, urllib.error

BASE = "http://127.0.0.1:8788"
KEY = "local-test-key-not-a-secret"


def call(path, payload=None):
    req = urllib.request.Request(
        BASE + path, method="POST" if payload is not None else "GET",
        data=json.dumps(payload).encode() if payload is not None else None)
    req.add_header("x-mary-key", KEY)
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "test/1.0")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]


def clear_fixtures():
    """Drop this test's own rows first, straight through sqlite.

    There is no delete route in the API and there should not be - a CRM that
    can forget a lead on a bad request is worse than one that cannot. So the
    test reaches past it to reset its own fixtures, and only its own.
    """
    import glob, os, sqlite3
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    pat = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\dashboard\.wrangler\state\v3\d1\miniflare-D1DatabaseObject\*.sqlite"
    for p in glob.glob(pat):
        if os.path.basename(p) == "metadata.sqlite":
            continue
        c = sqlite3.connect(p)
        c.execute("DELETE FROM crm_lead WHERE key='filwood'")
        c.execute("DELETE FROM crm_company WHERE key='stepnell'")
        c.execute("DELETE FROM crm_quote WHERE lead_key='filwood'")
        c.execute("DELETE FROM crm_note WHERE entity_key='filwood'")
        c.execute("DELETE FROM crm_event WHERE entity_key='filwood'")
        c.commit(); c.close()


clear_fixtures()
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   %s" % label)
    else:
        fail += 1
        print("  FAIL %s  %s" % (label, detail))


print("1. Jacob logs the lead")
s, r = call("/api/crm/upsert", {
    "type": "company", "key": "stepnell", "author": "jacob",
    "why": "enquiry arrived from their commercial team",
    "fields": {"name": "Stepnell Ltd", "domains": '["stepnell.co.uk"]',
               "relationship": "quoted", "postcode": "BS4 1JN"}})
check("company created", s == 200 and r.get("created"), r)

s, r = call("/api/crm/upsert", {
    "type": "lead", "key": "filwood", "author": "jacob",
    "why": "BCC Filwood Broadway enquiry, logged from commercial@",
    "fields": {"company_key": "stepnell", "title": "BCC 4-16 Filwood Broadway",
               "site": "Bristol", "postcode": "BS4 1JN", "source": "mailbox",
               "stage": "new", "owner": "jacob", "deadline": "2026-08-14"}})
check("lead created", s == 200 and r.get("created"), r)

print("2. it moves through estimating")
for stage, why in [("acknowledged", "customer told we have it"),
                   ("materials_out", "RFQ to Bellview"),
                   ("awaiting_costs", "waiting on BSW"),
                   ("quote_ready", "priced, to Adam to check")]:
    s, r = call("/api/crm/upsert", {
        "type": "lead", "key": "filwood", "author": "mary", "why": why,
        "fields": {"stage": stage}})
    check("stage -> %s" % stage, s == 200 and not r.get("created"), r)

print("3. Mary writes the quote and issues it")
s, r = call("/api/crm/upsert", {
    "type": "quote", "key": "filwood:1", "author": "mary",
    "why": "supplier-backed by Bellview 0000000507",
    "fields": {"lead_key": "filwood", "revision": 1, "value": 67067.58,
               "basis": "supplier-backed", "status": "issued",
               "issued_at": "2026-07-27T10:49:00", "issued_by": "gintare",
               "issued_to": "adam.warner@stepnell.co.uk"}})
check("quote created", s == 200 and r.get("created"), r)

s, r = call("/api/crm/upsert", {
    "type": "lead", "key": "filwood", "author": "mary",
    "why": "issued - handover to Jacob",
    "fields": {"stage": "quote_sent", "owner": "jacob", "value": 67067.58,
               "next_action": "first chase", "next_action_date": "2026-08-03"}})
check("handover stage", s == 200, r)

print("4. Jacob records a call")
s, r = call("/api/crm/note", {
    "entity_type": "lead", "entity_key": "filwood", "author": "jacob",
    "source": "call", "source_ref": "adam relayed 03/08",
    "body": "Adam rang Adam Warner. They are still waiting on the client's "
            "decision; asked us to hold the price. Next look 17/08."})
check("note added", s == 200 and r.get("ok"), r)

print("5. reads")
s, td = call("/api/crm/today")
everywhere = (td.get("due", []) + td.get("overdue", []) + td.get("upcoming", []))
check("today is the three-part shape",
      s == 200 and all(k in td for k in ("due", "overdue", "upcoming", "counts")), td if s != 200 else list(td))
check("today shows the lead", any(l["key"] == "filwood" for l in everywhere),
      [l["key"] for l in everywhere][:5])
check("overdue is capped", len(td.get("overdue", [])) <= 20, len(td.get("overdue", [])))
check("counts report the whole backlog, uncapped",
      td["counts"]["overdue"] >= len(td["overdue"]), td["counts"])

s, d = call("/api/crm/lead/filwood")
check("lead detail: lead", s == 200 and d["lead"]["stage"] == "quote_sent", s)
check("lead detail: company joined", d.get("company", {}).get("name") == "Stepnell Ltd", d.get("company"))
check("lead detail: quote joined", len(d.get("quotes", [])) == 1, d.get("quotes"))
check("lead detail: note joined", len(d.get("notes", [])) == 1, d.get("notes"))
check("value is ex VAT and intact", d["lead"]["value"] == 67067.58, d["lead"].get("value"))

print("6. the audit trail")
ev = d.get("events", [])
check("events recorded", len(ev) >= 6, len(ev))
stages = [e for e in ev if e["field"] == "stage"]
check("every stage change captured", len(stages) >= 5, len(stages))
check("attribution present", all(e["author"] for e in ev), ev[:2])
check("reasons captured", any(e["why"] for e in ev), ev[:2])
last = stages[0] if stages else {}
check("was/now on the transition",
      last.get("was") == "quote_ready" and last.get("now") == "quote_sent", last)

print("6b. a partial update must not inject NOT NULL defaults over good data")
s, r = call("/api/crm/upsert", {
    "type": "lead", "key": "filwood", "author": "crm_sync",
    "why": "handover - sets stage and owner only, as the real sync does",
    "fields": {"stage": "follow_up", "owner": "jacob"}})
s, dh = call("/api/crm/lead/filwood")
check("company_key survived a stage-only write",
      dh["lead"]["company_key"] == "stepnell", dh["lead"].get("company_key"))
check("title survived a stage-only write",
      dh["lead"]["title"] == "BCC 4-16 Filwood Broadway", dh["lead"].get("title"))

print("7. partial update must not blank a sibling field")
s, r = call("/api/crm/upsert", {
    "type": "lead", "key": "filwood", "author": "jacob",
    "why": "chased, moving the date out",
    "fields": {"next_action_date": "2026-08-17"}})
s, d2 = call("/api/crm/lead/filwood")
check("value survived a partial write", d2["lead"]["value"] == 67067.58, d2["lead"].get("value"))
check("title survived", d2["lead"]["title"] == "BCC 4-16 Filwood Broadway", d2["lead"].get("title"))

print("8. auth and validation")
req = urllib.request.Request(BASE + "/api/crm/upsert", method="POST",
                             data=json.dumps({"type": "lead", "key": "x"}).encode())
req.add_header("content-type", "application/json")
try:
    urllib.request.urlopen(req, timeout=10)
    check("write without key refused", False, "it went through")
except urllib.error.HTTPError as e:
    check("write without key refused", e.code == 404, e.code)

s, r = call("/api/crm/upsert", {"type": "nonsense", "key": "x", "author": "t"})
check("unknown type refused", s == 400, s)
s, r = call("/api/crm/upsert", {"type": "lead", "author": "t", "fields": {}})
check("missing key refused", s == 400, s)
s, r = call("/api/crm/upsert", {
    "type": "lead", "key": "filwood", "author": "t",
    "fields": {"stage': DROP TABLE crm_lead; --": "x"}})
check("junk column name ignored, not executed", s == 200, s)
s, chk = call("/api/crm/leads")
check("table still there after that", s == 200 and len(chk) >= 1, s)

print("\n%d ok, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)

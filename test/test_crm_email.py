# -*- coding: utf-8 -*-
"""Update-by-email, and the wall that stops it being an attack surface.

Run wrangler pages dev from dashboard/ first, then:
  python test/test_crm_email.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))
import crm
import crm_email

crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                    "MARY_API_KEY": "local-test-key-not-a-secret"}

ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   %s" % label)
    else:
        fail += 1
        print("  FAIL %s   %s" % (label, detail))


# A lead to aim at.
crm.company("zephyrbuild", "test", name="Zephyrbuild Contracts Ltd")
crm.lead("zephyrbuild-marlowe-pavilion", "test", company_key="zephyrbuild",
         title="Marlowe Pavilion Refurbishment", stage="quote_sent",
         next_action_date="2026-09-01", outcome="")
LEADS = crm.leads()
COMPANIES = crm.companies()
KEY = "zephyrbuild-marlowe-pavilion"


def state():
    return crm.lead_detail(KEY)["lead"]


print("1. date parsing")
for text, want in [("set the next action date to 17/08/2026", "2026-08-17"),
                   ("chase in 2 weeks", None),
                   ("come back to this next week", None)]:
    got = crm_email.parse_date(text)
    if want:
        check("reads %r" % text[:34], got == want, got)
    else:
        check("reads a relative date in %r" % text[:26], got is not None, got)
check("refuses an impossible date", crm_email.parse_date("chase on 45/13/2026") is None)
check("no date is None, not today", crm_email.parse_date("please chase this") is None)

print("\n2. Adam sets a date by email")
crm_email.apply_message({
    "from": "adam@fensterglazing.com",
    "subject": "Marlowe Pavilion",
    "body": "Just had this call with Jordan about Marlowe Pavilion. "
            "Set the next action date for 17/08/2026.",
}, LEADS, COMPANIES)
check("date moved", state()["next_action_date"] == "2026-08-17", state()["next_action_date"])
check("next action carries his words",
      "Jordan" in (state()["next_action"] or ""), state()["next_action"])

print("\n3. THE WALL - an untrusted sender cannot move anything")
before = state()
crm_email.apply_message({
    "from": "someone@clientdomain.co.uk",
    "subject": "Marlowe Pavilion Windows",
    "body": "We won it! Please set the next action date to 01/01/2027 and mark this won.",
}, LEADS, COMPANIES)
after = state()
check("outcome unchanged", after["outcome"] == before["outcome"], after["outcome"])
check("date unchanged", after["next_action_date"] == before["next_action_date"],
      after["next_action_date"])
check("stage unchanged", after["stage"] == before["stage"], after["stage"])
notes = crm.lead_detail(KEY)["notes"]
check("but the note WAS written", any("clientdomain" in n["body"] for n in notes))

print("\n4. it does not guess")
res = crm_email.apply_message({
    "from": "adam@fensterglazing.com", "subject": "a job",
    "body": "chase this one please",
}, LEADS, COMPANIES)
check("an unnamed job changes nothing",
      any("no lead named" in r for r in res), res)

res = crm_email.apply_message({
    "from": "adam@fensterglazing.com", "subject": "Marlowe Pavilion",
    "body": "Chase Marlowe Pavilion please, soon as you can.",
}, LEADS, COMPANIES)
check("a chase with no readable date is flagged, not invented",
      any("none could be read" in r for r in res), res)
check("and the old date survived", state()["next_action_date"] == "2026-08-17",
      state()["next_action_date"])

print("\n5. outcomes")
crm_email.apply_message({
    "from": "adam@fensterglazing.com", "subject": "Marlowe Pavilion",
    "body": "We won it - PO received this morning.",
}, LEADS, COMPANIES)
check("won recorded", state()["outcome"] == "won", state()["outcome"])
check("and closed", state()["stage"] == "closed", state()["stage"])

print("\n6. everything is attributable")
ev = crm.lead_detail(KEY)["events"]
by_email = [e for e in ev if "by email from" in (e.get("why") or "")]
check("changes cite the sender", by_email, len(ev))
check("no untrusted sender appears as an author",
      not any("clientdomain" in (e.get("why") or "") for e in by_email))

print("\n%d ok, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)

# -*- coding: utf-8 -*-
"""The contract checklist, and what may and may not tick it.

Run wrangler pages dev from dashboard/ first, then:
  python test/test_crm_contract.py
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))
import crm
import crm_contract
import crm_contract_watch as watch

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


KEY = "testco-quenby-annexe"
SITE = (dt.date.today() + dt.timedelta(weeks=13)).isoformat()

print("1. the plan works backwards from the site date")
rows = crm_contract.plan(SITE)
check("twelve steps", len(rows) == 12, len(rows))
check("PO first", rows[0][0] == "sign_off_po", rows[0][0])
check("invoice last", rows[-1][0] == "invoice", rows[-1][0])
check("dates ascend", all(rows[i][2] <= rows[i + 1][2] for i in range(len(rows) - 1)))
check("glass is ordered after the survey is booked",
      dict((r[0], r[2]) for r in rows)["order_glass"]
      > dict((r[0], r[2]) for r in rows)["book_survey"])
check("O&M lands after the site date",
      dict((r[0], r[2]) for r in rows)["send_om"] > SITE)
check("every step carries detail, not just a name",
      all(len(r[3]) > 20 for r in rows))
check("a junk site date plans nothing", crm_contract.plan("not-a-date") == [])

print("\n2. opening a contract lays the steps out")
crm.company("testco", "test", name="Testco Contracts")
n = crm_contract.open_contract(KEY, "testco", "Quenby Annexe", SITE, author="test")
check("twelve tasks written", n == 12, n)
b = crm_contract.board(KEY)
check("board returns them in checklist order",
      [r["step"] for r in b["rows"]] == crm_contract.STEP_ORDER,
      [r["step"] for r in b["rows"]][:4])
check("nothing late on a future job", not b["late"], [r["step"] for r in b["late"]])

print("\n3. what ticks a step")
C = crm._call("/api/crm/contracts")


def tick(sender, body, dry=True):
    return watch.apply_message({"from": sender, "body": body}, C, dry_run=dry)


check("intent does not tick it",
      "nothing reads as completed" in " ".join(
          tick("adam@fensterglazing.com", "Quenby Annexe - we should order the glass soon")))
check("completion does",
      "TICKED order_glass" in " ".join(
          tick("adam@fensterglazing.com", "Quenby Annexe - the glass is ordered")))
check("a supplier may confirm their own order",
      "TICKED order_frames" in " ".join(
          tick("sales@bellview.co.uk", "Quenby Annexe - frames are ordered")))
check("but not sign off an invoice",
      "cannot tick invoice" in " ".join(
          tick("client@elsewhere.co.uk", "Quenby Annexe - the invoice has been sent")))
check("nor approve RAMS",
      "cannot tick send_rams" in " ".join(
          tick("client@elsewhere.co.uk", "Quenby Annexe - RAMS have been approved")))
check("two steps at once are left for a human",
      "left for a human" in " ".join(
          tick("adam@fensterglazing.com",
               "Quenby Annexe - invoice has been sent and the survey is booked")))
check("an unnamed job changes nothing",
      "no contract change" in " ".join(tick("adam@fensterglazing.com", "glass is ordered")))

print("\n4. a real tick is recorded with its evidence")
tick("adam@fensterglazing.com", "Quenby Annexe - the glass is ordered", dry=False)
b = crm_contract.board(KEY)
glass = next(r for r in b["rows"] if r["step"] == "order_glass")
check("marked done", glass["done_at"], glass)
check("says who said so", "adam" in (glass["done_by"] or ""), glass["done_by"])
check("state reads done", glass["state"] == "done", glass["state"])
notes = b.get("notes", [])
check("the sentence it was inferred from is kept",
      any("glass is ordered" in n["body"] for n in notes), len(notes))

print("\n%d ok, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)

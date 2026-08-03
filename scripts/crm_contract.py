# -*- coding: utf-8 -*-
"""Joseph's half: a won job, its twelve steps, and when each one is actually due.

Adam walked this board through on 03/08. A contract is created when the
purchase order lands - the moment AdminBase converts a lead into a contract -
and everything after that is deadline-driven **backwards from the site date**,
because that is the only fixed point: "we've normally got a date we need to be
on site and the amount of time we need to do it in".

TWO THINGS THIS DOES THAT ADMINBASE DOES NOT, both of them Adam's own criticism
of the board he already has:

  IT SAYS WHAT TO ORDER, NOT ONLY THAT ORDERING IS DUE. His words: "it doesn't
  tell you what to order, it just tells you that it needs ordering". A task
  carries `detail` - the spec, the supplier, the reference - so the person
  reading it can act without opening four other documents.

  NOBODY HAS TO TICK IT. Every box on the AdminBase version is red because a
  checklist that waits on human data entry does not get kept. Joseph infers
  progress from the email he is CC'd on (see crm_contract_watch); a human only
  ever corrects him.

THE LEAD TIMES ARE ASSUMPTIONS AND ARE MARKED AS SUCH. They are drawn from the
shape of the trade, not from Fenster's own measured history, because that
history is not recorded anywhere yet. Every one is overridable per contract and
the board says which are defaults. Do not treat them as facts until they have
been checked against real jobs - that is exactly the mistake this repo keeps
recording.

  python scripts/crm_contract.py --plan <key>          # what the dates would be
  python scripts/crm_contract.py --open <key> --site 2026-10-12
"""
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm

# step, label, weeks BEFORE the site date, and what the detail must carry.
# Ordered as Adam listed them; the offsets are the assumption, not the order.
STEPS = [
    ("sign_off_po", "Sign off the purchase order", 12,
     "Read it against the quote we issued - value, scope, retention, payment terms."),
    ("book_installation", "Provisionally book the installation", 11,
     "Against the fitting diary. Provisional until the survey lands."),
    ("submit_designs", "Submit designs", 10,
     "What the client has to approve before anything is ordered."),
    ("book_survey", "Book the survey", 9,
     "Nothing below this line can be ordered off drawings alone."),
    ("order_frames", "Order the frames", 8,
     "System, finish, sizes, supplier and their lead time."),
    ("order_glass", "Order the glass", 7,
     "Specification, pane schedule, supplier. Louvres are a separate order."),
    ("send_rams", "Send RAMs", 5,
     "Risk assessment and method statement to the client's site team."),
    ("arrange_labour", "Arrange labour", 4,
     "Fitters booked for the installation dates, with the gang size."),
    ("order_consumables", "Order consumables", 3,
     "Fixings, mastic, trims, cills - whatever the method statement assumes."),
    ("confirm_booking", "Confirm the installation booking", 2,
     "Turn the provisional dates firm with the client and the fitters."),
    ("send_om", "Send the O&M manual", -1,
     "After completion. Usually a condition of the final payment."),
    ("invoice", "Invoice", -2,
     "Or the payment application, depending on the contract. See D3."),
]
STEP_ORDER = [s[0] for s in STEPS]
STEP_LABEL = {s[0]: s[1] for s in STEPS}


def plan(site_date, overrides=None):
    """[(step, label, due, detail)] for a site date. Overrides are weeks-before."""
    overrides = overrides or {}
    try:
        site = dt.datetime.strptime(str(site_date)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return []
    out = []
    for step, label, weeks, detail in STEPS:
        weeks = overrides.get(step, weeks)
        out.append((step, label, (site - dt.timedelta(weeks=weeks)).isoformat(), detail))
    return out


def open_contract(key, company_key, title, site_date, author="joseph",
                  value=None, po_ref="", lead_key="", overrides=None):
    """Create the contract and lay out its twelve steps. Idempotent."""
    crm.contract(key, author,
                 why="purchase order received - lead converted to contract",
                 company_key=company_key, title=title, value=value,
                 po_ref=po_ref, site_date=site_date, lead_key=lead_key,
                 status="live")
    made = 0
    for step, label, due, detail in plan(site_date, overrides):
        crm.task("contract", key, step, label, author, due=due, detail=detail)
        made += 1
    return made


def board(key):
    """One contract: what is done, what is due, what is late.

    Ordered by the checklist, not by date, because the steps have a real
    dependency order - you do not order glass before the survey - and a person
    reading it wants to see where the job has got to, not a shuffled list.
    """
    d = crm.contract_detail(key)
    if not d or d.get("error"):
        return None
    today = dt.date.today().isoformat()
    by_step = {t["step"]: t for t in d.get("tasks", [])}
    rows = []
    for step in STEP_ORDER:
        t = by_step.get(step)
        if not t:
            continue
        state = ("done" if t.get("done_at")
                 else "late" if t.get("due") and t["due"] < today
                 else "due" if t.get("due") == today
                 else "ahead")
        rows.append(dict(t, state=state))
    d["rows"] = rows
    d["late"] = [r for r in rows if r["state"] == "late"]
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", help="show the dates for a site date without writing")
    ap.add_argument("--site", help="YYYY-MM-DD")
    ap.add_argument("--open", dest="open_key")
    ap.add_argument("--company", default="unknown")
    ap.add_argument("--title", default="")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}

    if a.plan or (a.site and not a.open_key):
        site = a.site or a.plan
        rows = plan(site)
        if not rows:
            print("give a site date as YYYY-MM-DD")
            return 2
        print("Site date %s - working backwards:\n" % site)
        today = dt.date.today().isoformat()
        for step, label, due, detail in rows:
            flag = "  LATE" if due < today else ""
            print("  %-12s %-34s %s%s" % (due, label, step, flag))
            print("               %s" % detail)
        return 0

    if a.open_key:
        if not a.site:
            print("--open needs --site YYYY-MM-DD")
            return 2
        n = open_contract(a.open_key, a.company, a.title or a.open_key, a.site)
        print("opened %s with %d steps against a site date of %s"
              % (a.open_key, n, a.site))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""The twelve steps every won contract runs, and the seeder that lays them out.

Labels are Adam's own, from the 03/08 meeting, in his order. This is the
checklist AdminBase had and lost, and his two criticisms of that version are
the whole design brief:

  "it's not really kept up to date, you can see all the boxes are red"
      -> intake ticks steps CLERICALLY from the confirming email. Nobody types.

  "it doesn't tell you what to order, it just tells you that it needs ordering"
      -> `detail` is where WHAT goes, and a step without it is half a task.

DEADLINES. Every step works backwards from the site date. The offsets below are
NOT recorded anywhere - how many days before installation the glass must be
ordered is a real Fenster fact that only Adam or Paul knows, and guessing it
would put invented dates in front of the people who fit the windows. So steps
seed with no due date and the hub says plainly that the lead times are missing.
Fill LEAD_TIMES in once and every contract gets its dates.

  python core/contract_template.py --contract stoke-park-school
  python core/contract_template.py --all
"""
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import record

# (n, label, what "detail" should eventually carry)
STEPS = [
    (1,  "Sign off the purchase order", "read it through and send it back"),
    (2,  "Provisionally book installation", "against Paul's diary"),
    (3,  "Submit designs", ""),
    (4,  "Book survey", ""),
    (5,  "Order frames", "the frame schedule - sizes, finish, supplier"),
    (6,  "Order glass", "the glass spec - makeup, sizes, quantities, supplier"),
    (7,  "Send RAMs", ""),
    (8,  "Arrange labour", "fitters booked for the install dates"),
    (9,  "Order consumables", ""),
    (10, "Confirm installation bookings", ""),
    (11, "Send O&M", ""),
    (12, "Invoice, then chase it", ""),
]

# Days BEFORE the site date each step must be done. Empty until a human says.
# e.g. {5: 42, 6: 35} would mean frames 6 weeks out, glass 5 weeks out.
LEAD_TIMES = {}

# The invoice chase ladder. Days PAST the due date. Adam gave 7, 35 and 75;
# stages 3-5 exist on his board but he did not say their day counts, so they
# are absent rather than invented.
CHASE_LADDER = [
    (1, 7,  "Invoice due date passed - first reminder"),
    (2, 35, "Why has this not been paid"),
    (6, 75, "FORMAL ESCALATION - legal. Never automatic, Adam decides every time"),
]


def seed(contract_key, site_date=None):
    """Lay the twelve steps on a contract. Never destroys what is already
    there: existing detail and due dates survive, only the labels are made
    canonical."""
    for n, label, _hint in STEPS:
        due = None
        if site_date and n in LEAD_TIMES:
            try:
                d = dt.date.fromisoformat(site_date[:10]) - dt.timedelta(days=LEAD_TIMES[n])
                due = d.isoformat()
            except ValueError:
                due = None
        record.call("/api/step", {"contract_key": contract_key, "n": n,
                                  "label": label, "detail": "", "due": due})
    return len(STEPS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    targets = []
    if a.all:
        targets = [(c["key"], c.get("site_date")) for c in record.call("/api/contracts")
                   if c.get("status") == "live"]
    elif a.contract:
        c = record.call("/api/card/contract/" + a.contract)
        targets = [(a.contract, (c.get("contract") or {}).get("site_date"))]
    else:
        ap.print_help()
        return 1
    for key, site in targets:
        n = seed(key, site)
        print("  seeded %d steps on %s%s" % (n, key,
              "" if site else "  (no site date - no deadlines can be computed)"))
    if not LEAD_TIMES:
        print("\nLEAD_TIMES is empty, so no step has a deadline. Ask Adam or Paul "
              "how many days before the site date each step must happen, put them "
              "in this file, and re-run - every contract then gets its dates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

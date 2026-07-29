# -*- coding: utf-8 -*-
"""JACOB - source: THE CUSTOMERS WHO HAVE STOPPED RINGING.

Adam, hub-78, 29/07/2026: "I want a full list in the morning of DECENT leads."

This is the half of that list that does not come from any feed, and on the
evidence it is the better half.

`contracts-won.json` is Adam's own export of 204 won commercial contracts, and
its LEADSOURCE column settles where Fenster's work actually comes from:

    existing customer   118 of 201   (59%)
    Jayk, by name        51          (25%)
    Google               22
    a tender portal       3          in the company's entire history

Three. So a night spent scraping tender portals is a night spent on 1.5% of the
historical funnel, and the 59% is sitting in a file nobody queries. A customer
who has bought before, is happy, and has simply not been called is the highest
converting lead this company has, and it costs a phone call.

  python scripts/jacob_dormant.py
  python scripts/jacob_dormant.py --quiet-days 180 --min-value 15000

Output: data/jacob/dormant.json

WHAT IT DOES
------------
Joins the won-contract history to the live AdminBase pipeline and asks one
question per client: how long since they last placed work, and is there
anything live with them right now?

A client with a live quote is NOT dormant - they are mid-conversation and
ringing them about "how have you been" cuts across a real chase. Those are
excluded and counted, not listed. What is left is the list of people who bought
from Fenster, stopped, and nobody noticed.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not rank on lifetime value alone. Two of the top rows by value are a
single large job each - one contract is a relationship the way one date is a
marriage. `jobs` is on every row for that reason, and the sort weighs repeat
buyers above one-off spenders.

It does not write the phone call. `phone` here is the number off the last
contract record and it may be years old; the point of the row is who to ring,
not a script for ringing them.

And it says nothing about WHY they went quiet, because this file cannot know.
An outcome that arrives by email never reaches the CRM - Darren Trigg's two CIF
schools lost funding and killed six "Live - Quoted" rows - so a long silence
here is a question, never a verdict.

WHAT `quietDays` MEASURES, AND WHAT IT DOES NOT
----------------------------------------------
It measures days since Fenster last had WORK with them. It is NOT days since
anyone spoke to them, and it must never be read out on a phone call as though
it were - RSR, 29/07/2026: this file said "378 days, nothing since 2025-07-16",
and commercial@ has James Evans thanking Adam on 28/11/2025 with the accounts
traffic running to 05/05/2026. Nine months of the silence was an artefact.

Two thirds of that gap was a bug and is now fixed. `contractDate` is the date
the ORDER was placed; `fitted` is the date Fenster was last on their site, and
the two are routinely a year apart - RSR's GBP 188,135 Bletchley Rail Depot was
ordered 2024-10-15 and fitted 2025-09-02. Ageing from the order alone counted
eleven months of live work as silence. `quietDays` now runs from the LATER of
the two and `quietBasis` says which one it was.

The rest is not fixable here. `intake.json` covers thirty days, so a client
absent from it looks identical to a client nobody has ever emailed, and joining
to it would manufacture silence rather than measure it - the same shape as the
bug that once read an empty 30-day window as a quiet market. So the mailbox
stays the authority on contact, this file stays the authority on work, and
`quietMeans` on the output says so on its face. Check `jacob_mail.py --search`
before ringing anyone on this list.
"""
import argparse
import json
import os
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WON = os.path.join(REPO, "data", "jacob", "contracts-won.json")
ADMINBASE = os.path.join(REPO, "data", "jacob", "adminbase.json")
OUT = os.path.join(REPO, "data", "jacob", "dormant.json")

TODAY = date.today()

# Standing decisions that outrank any amount of lifetime value. A call list
# that has to be read before it is used is not a call list, so these never
# reach it - the first run put Hightown on it, which is exactly the mistake
# Adam's instruction exists to prevent.
#
#   Hightown - Adam, 27/07/2026: many quotes, no wins, do not quote unless
#              he says otherwise. They are one won contract in this file and
#              they would rank on it.
#   Neil Douglas - live tender, do not approach.
DO_NOT_APPROACH = {
    "HIGHTOWN HOUSING ASSOCIATION": "Adam, 27/07: do not quote unless he says so",
    "HIGHTOWN": "Adam, 27/07: do not quote unless he says so",
    "NEIL DOUGLAS": "live tender - do not approach",
}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default


def norm(s):
    """Client names arrive with trailing punctuation, LTD/LIMITED both ways and
    the odd mojibaked apostrophe. Normalise enough to join on, and no further -
    over-normalising merges two real companies with similar names."""
    s = (s or "").strip().upper()
    for junk in (" LTD.", " LTD", " LIMITED", " PLC", " (UK)", "."):
        if s.endswith(junk):
            s = s[: -len(junk)].strip()
    return " ".join(s.split())


def days_since(iso):
    try:
        return (TODAY - date.fromisoformat(str(iso)[:10])).days
    except (ValueError, TypeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet-days", type=int, default=150,
                    help="silence past which a client counts as dormant")
    ap.add_argument("--min-value", type=float, default=2500,
                    help="lifetime value below which it is not worth a call")
    args = ap.parse_args()

    won = load(WON) or {}
    crm = load(ADMINBASE) or {}
    contracts = won.get("contracts") or []
    if not contracts:
        sys.exit("no contracts in %s - run jacob_contracts.py first" % WON)

    # Anyone with a quote out is mid-conversation, not dormant.
    live = {norm(r.get("client")) for r in (crm.get("due") or [])}
    live.discard("")

    agg = {}
    for r in contracts:
        if r.get("cancelled"):
            continue
        key = norm(r.get("client"))
        if not key:
            continue
        a = agg.setdefault(key, {
            "client": (r.get("client") or "").strip(), "jobs": 0, "value": 0.0,
            "last": "", "lastFitted": "", "lastSite": "", "phone": "", "area": "",
            "soldBy": "", "leadSource": "", "inProgress": False})
        a["jobs"] += 1
        a["value"] += r.get("value") or 0
        if r.get("inProgress"):
            a["inProgress"] = True
        # The last time Fenster was on their site, which is a different date
        # from the order and usually a later one. A fitted date in the future
        # is a plan, not a visit, so it does not count as contact.
        f = str(r.get("fitted") or "")[:10]
        if f and f <= TODAY.isoformat() and f > a["lastFitted"]:
            a["lastFitted"] = f
        d = r.get("contractDate") or ""
        if d > a["last"]:
            a.update(last=d, lastSite=r.get("site") or "",
                     phone=r.get("phone") or a["phone"],
                     area=r.get("area") or a["area"],
                     soldBy=r.get("soldBy") or a["soldBy"],
                     leadSource=r.get("leadSource") or a["leadSource"])

    rows, skipped = [], {"live quote already out": 0, "under the value floor": 0,
                         "still recent": 0, "work in progress": 0, "no date": 0,
                         "on a do-not-approach instruction": 0}
    for key, a in agg.items():
        if key in DO_NOT_APPROACH:
            skipped["on a do-not-approach instruction"] += 1
            continue
        # Age from the later of "they ordered" and "we were on their site".
        quiet_from = max(a["last"] or "", a["lastFitted"] or "") or ""
        quiet_basis = ("last fitted" if quiet_from and quiet_from == a["lastFitted"]
                       and quiet_from != a["last"] else "last contract")
        quiet = days_since(quiet_from)
        if quiet is None:
            skipped["no date"] += 1
            continue
        if a["value"] < args.min_value:
            skipped["under the value floor"] += 1
            continue
        if a["inProgress"]:
            # Fenster is on their site right now. That is a conversation, not a
            # cold spell, and it is the wrong thing to put on a chase list.
            skipped["work in progress"] += 1
            continue
        if key in live:
            skipped["live quote already out"] += 1
            continue
        if quiet < args.quiet_days:
            skipped["still recent"] += 1
            continue
        rows.append({
            "client": a["client"], "jobs": a["jobs"],
            "value": round(a["value"], 2), "quietDays": quiet,
            "quietFrom": quiet_from, "quietBasis": quiet_basis,
            "lastContract": a["last"], "lastFitted": a["lastFitted"] or None,
            "lastSite": a["lastSite"],
            "area": a["area"], "phone": a["phone"] or None,
            "soldBy": a["soldBy"] or None,
            "leadSource": a["leadSource"] or None,
            # Jayk left, and a quarter of everything ever won came through him
            # by name. A dormant client whose last job HE sold is dormant for a
            # reason nobody has addressed.
            "wasJayks": "jayk" in (a["soldBy"] or "").lower(),
            "owner": "Adam",
            "next": ("Adam calls %s. %d job%s worth GBP %s and no work since %s "
                     "(%s) - ask what they have coming, not whether they are "
                     "well. Check the mailbox for the last conversation first."
                     % (a["client"], a["jobs"], "" if a["jobs"] == 1 else "s",
                        format(int(a["value"]), ","), quiet_from or "unknown",
                        quiet_basis)),
        })

    # Repeat buyers first. One large contract is not a relationship, so weight
    # the number of jobs as heavily as the money - a client who has come back
    # five times will come back a sixth.
    rows.sort(key=lambda r: -(r["value"] * min(r["jobs"], 8)))

    out = {
        "updated": TODAY.isoformat(),
        "source": "contracts-won.json (Adam's 204 won contracts) joined to "
                  "adminbase.json (the live quoted pipeline)",
        "why": "59% of everything Fenster has ever won came from an existing "
               "customer and 3 contracts in the company's history came from a "
               "tender portal. This is the 59%, filtered to the ones nobody is "
               "currently talking to.",
        "rule": "Dormant = has bought before, no quote out now, no work on site "
                "now, no work for %d days, lifetime value over GBP %s."
                % (args.quiet_days, format(int(args.min_value), ",")),
        "quietMeans": "quietDays is days since Fenster last had WORK with them - "
                      "the later of the order date and the date it was fitted, "
                      "which quietBasis names. It is NOT days since anyone spoke "
                      "to them and must never be said on a call as if it were. "
                      "RSR read 378 days here while commercial@ held a thank-you "
                      "from their QS at 28/11/2025 and accounts traffic to "
                      "05/05/2026. intake.json covers thirty days, so it cannot "
                      "supply the contact date and joining to it would invent "
                      "silence rather than measure it. Run "
                      "`jacob_mail.py --search \"<client>\" --days 0` before "
                      "ringing anyone on this list.",
        "caveat": "A long silence is a question, not a verdict. An outcome that "
                  "arrives by email never reaches the CRM, so some of these "
                  "went quiet for a reason somebody at Fenster already knows.",
        "counts": {"clients": len(agg), "dormant": len(rows),
                   "excluded": skipped},
        "clients": rows,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    print("%d clients in the won history; %d are dormant and worth a call.\n"
          % (len(agg), len(rows)))
    print("%-30s %4s %11s %6s %-6s %s" % ("CLIENT", "JOBS", "LIFETIME", "QUIET", "AREA", "LAST JOB"))
    for r in rows[:25]:
        print("%-30s %4d %11s %5dd %-6s %s"
              % (r["client"][:30], r["jobs"], format(int(r["value"]), ","),
                 r["quietDays"], r["area"] or "-", (r["lastSite"] or "")[:38]))
    print("\nexcluded:", {k: v for k, v in skipped.items() if v})
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

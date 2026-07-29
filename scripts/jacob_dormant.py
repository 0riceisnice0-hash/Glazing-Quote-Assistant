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
            "last": "", "lastSite": "", "phone": "", "area": "",
            "soldBy": "", "leadSource": "", "inProgress": False})
        a["jobs"] += 1
        a["value"] += r.get("value") or 0
        if r.get("inProgress"):
            a["inProgress"] = True
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
        quiet = days_since(a["last"])
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
            "lastContract": a["last"], "lastSite": a["lastSite"],
            "area": a["area"], "phone": a["phone"] or None,
            "soldBy": a["soldBy"] or None,
            "leadSource": a["leadSource"] or None,
            # Jayk left, and a quarter of everything ever won came through him
            # by name. A dormant client whose last job HE sold is dormant for a
            # reason nobody has addressed.
            "wasJayks": "jayk" in (a["soldBy"] or "").lower(),
            "owner": "Adam",
            "next": ("Adam calls %s. %d job%s worth GBP %s and nothing since %s "
                     "- ask what they have coming, not whether they are well."
                     % (a["client"], a["jobs"], "" if a["jobs"] == 1 else "s",
                        format(int(a["value"]), ","), a["last"] or "unknown")),
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
                "now, silent for %d days, lifetime value over GBP %s."
                % (args.quiet_days, format(int(args.min_value), ",")),
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

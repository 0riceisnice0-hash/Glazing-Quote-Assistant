# -*- coding: utf-8 -*-
"""JACOB - source: the WON commercial contracts. What Fenster actually does.

Adam Butcher to jacob@, 29/07/2026 13:33, subject "All Existing Commercial
Contracts", attaching `commercial_contracts_export29072026.csv` pulled by hand
from AdminBase: *"all of our commercial jobs to date ... these are all won jobs
and either completed or in progress. This took me a long time to put together."*

WHY THIS FILE MATTERS MORE THAN ANY FEED
----------------------------------------
Every other source here describes work Fenster might get. This is the only one
that describes work Fenster GOT, with a net value against each row, and it
settles an argument that ran all week.

The Opportunity Log said Fenster had won nothing over GBP 50,000 in 52 priced
attempts, and that number kept trying to become "Fenster cannot win big work".
It was always a fact about the LOG - the 2025-26 BD funnel - and never about
the company. This export has **8 wins over GBP 50k and 2 over GBP 200k**, led
by Headrow Court for Fortis Vision at **GBP 631,248**, which is fifteen times
the largest win on the BD log and appears nowhere on it.

So: the funnel guidance stands (small jobs convert better on the recent
funnel), and the ceiling does not exist. Size alone is never a reason to kill
a lead. `bd.md`.

WHAT IT SAYS ABOUT WHERE WORK COMES FROM, WHICH IS THE POINT OF THE JOB
----------------------------------------------------------------------
`LEADSOURCE` on the won rows is the most useful column in the repo:

    Existing Customer / Existing Commercial   118 of 201   59%
    Jayk                                       51          25%
    Google                                     22          11%
    Constructionline                            3
    Recommendation                              1

Three quarters of everything Fenster has won came from a client it already had
or from one named business development manager - and that manager left. Nothing
has replaced those 51 contracts. That is the actual cost of Jayk going, and it
dwarfs the tender-portal logins (JAC-11) it took a week to notice.

  python scripts/jacob_contracts.py

Output: data/jacob/contracts-won.json

TRAPS
-----
1. `CONTNET` arrives as ` £631,248.10 ` with padding, thousands separators and
   a mojibaked pound sign (U+FFFD). Three rows of 204 have no value at all -
   they are counted and excluded from every average rather than read as zero.
2. `CONTNET` is **net**, i.e. ex VAT - unlike AdminBase's lead export, which is
   inc VAT. Do not de-VAT this one a second time.
3. `CONTBAL` is an outstanding balance, not a value. Headrow Court shows GBP
   15,286.13 against a GBP 631,248 contract. It is finance, not BD, and it is
   carried without interpretation.
4. `DATEFITTED` is blank on work not yet installed, so contract-date is the
   only date every row has. Count years off CONTRACTDATE.
5. A customer appears under one spelling per row and the spellings are not
   clean ("CONAMAR BUILDING SERVICES LTD." vs "Conamar"). Matching to anything
   else must go through the same token normalisation the board uses.
"""
import argparse
import collections
import csv
import json
import os
import re
import statistics
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "test-results", "jacob-mail",
                   "commercial_contracts_export29072026.csv")
OUT = os.path.join(REPO, "data", "jacob", "contracts-won.json")

SOURCE = {
    "file": "commercial_contracts_export29072026.csv",
    "from": "Adam Butcher <adam@fensterglazing.com>",
    "to": "jacob@fensterglazing.com",
    "subject": "All Existing Commercial Contracts",
    "received": "2026-07-29T13:33",
    "system": "AdminBase (Abinitio Software), exported by hand",
    "adamSaid": ("all of our commercial jobs to date ... these are all won jobs "
                 "and either completed or in progress"),
    "vat": ("CONTNET is NET, ex VAT. This is the opposite of the AdminBase LEAD "
            "export, whose values are inc VAT - do not de-VAT this one."),
}


def money(s):
    """` £631,248.10 ` -> 631248.10. Returns None, never 0, when there is no
    number: a missing value and a zero-value contract are different facts and
    reading one as the other is how a median goes wrong."""
    s = (s or "").strip().replace(",", "").replace("�", "").replace("£", "")
    s = s.strip()
    if not s:
        return None
    neg = s.startswith("(")
    s = s.strip("()")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def year_of(s):
    m = re.search(r"/(\d{4})$", (s or "").strip())
    return m.group(1) if m else None


def iso(s):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})$", (s or "").strip())
    return "%s-%s-%s" % (m.group(3), m.group(2), m.group(1)) if m else None


def pc_area(s):
    m = re.match(r"^([A-Z]{1,2})\d", (s or "").replace(" ", "").upper())
    return m.group(1) if m else None


BANDS = ((0, 10000, "under GBP 10k"), (10000, 50000, "GBP 10k-50k"),
         (50000, 200000, "GBP 50k-200k"), (200000, 10 ** 12, "over GBP 200k"))


def band_of(v):
    for lo, hi, lab in BANDS:
        if lo <= v < hi:
            return lab
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC)
    args = ap.parse_args()

    if not os.path.exists(args.src):
        sys.exit("not found: %s\nSave the attachment first:\n"
                 "  python scripts/jacob_mail.py --attachments <id> "
                 "--mailbox jacob --save" % args.src)

    raw = list(csv.DictReader(open(args.src, encoding="utf-8-sig")))
    rows, novalue, cancelled = [], 0, 0
    for r in raw:
        v = money(r.get(" CONTNET ") or r.get("CONTNET"))
        canc = (r.get("CONTRACTCANCELLED") or "").strip().upper() == "TRUE"
        if canc:
            cancelled += 1
        if v is None:
            novalue += 1
        site = (r.get("SITEADDRESS") or "").strip()
        rows.append({
            "contract": (r.get("CONTRACTNO") or "").strip(),
            "client": (r.get("CUSTNAME") or "").strip(),
            "custNo": (r.get("CUSTNO") or "").strip(),
            "site": site,
            "postcode": (r.get("FITTINGPOSTCODE") or "").strip(),
            "area": pc_area(r.get("FITTINGPOSTCODE")),
            "clientAddress": (r.get("ADDRESS") or "").strip(),
            "value": v,
            "band": band_of(v) if v is not None else None,
            "balance": money(r.get("CONTBAL")),
            "contractDate": iso(r.get("CONTRACTDATE")),
            "fitted": iso(r.get("DATEFITTED")),
            "inProgress": not (r.get("DATEFITTED") or "").strip(),
            "soldBy": (r.get("SOLDBY") or "").strip(),
            "leadSource": (r.get("LEADSOURCE") or "").strip(),
            "installManager": (r.get("INSTALLATIONMANAGER") or "").strip(),
            "phone": (r.get("TELEPHONENUMBERS") or "").strip(),
            "cancelled": canc,
            "year": year_of(r.get("CONTRACTDATE")),
        })

    live = [r for r in rows if r["value"] is not None and not r["cancelled"]]
    nums = sorted(r["value"] for r in live)

    by_client = collections.defaultdict(lambda: {"jobs": 0, "value": 0.0,
                                                 "biggest": 0.0, "years": set()})
    for r in live:
        c = by_client[r["client"]]
        c["jobs"] += 1
        c["value"] += r["value"]
        c["biggest"] = max(c["biggest"], r["value"])
        if r["year"]:
            c["years"].add(r["year"])
    clients = sorted(
        ({"client": k, "jobs": v["jobs"], "value": round(v["value"], 2),
          "biggest": round(v["biggest"], 2),
          "firstYear": min(v["years"]) if v["years"] else None,
          "lastYear": max(v["years"]) if v["years"] else None}
         for k, v in by_client.items()),
        key=lambda c: -c["value"])

    src_counts = collections.Counter(r["leadSource"] or "(blank)" for r in live)
    repeat = sum(n for s, n in src_counts.items()
                 if s.lower().startswith("existing"))

    doc = {
        "updated": datetime.now().isoformat(timespec="seconds"),
        "source": SOURCE,
        "counts": {
            "rows": len(rows),
            "withValue": len(live),
            "noValue": novalue,
            "cancelled": cancelled,
            "inProgress": sum(1 for r in live if r["inProgress"]),
        },
        "money": {
            "total": round(sum(nums), 2),
            "median": round(statistics.median(nums), 2) if nums else None,
            "mean": round(statistics.mean(nums), 2) if nums else None,
            "largest": nums[-1] if nums else None,
            "smallest": nums[0] if nums else None,
        },
        "bands": [
            {"band": lab, "jobs": len([v for v in nums if lo <= v < hi]),
             "value": round(sum(v for v in nums if lo <= v < hi), 2)}
            for lo, hi, lab in BANDS
        ],
        "bandNote": ("THE ANSWER TO 'CAN FENSTER WIN BIG WORK'. The Opportunity "
                     "Log has 0 wins in 52 priced attempts over GBP 50k. This "
                     "export has %d over GBP 50k and %d over GBP 200k, the "
                     "largest GBP %s. The log describes the 2025-26 BD funnel; "
                     "this describes the company. Never say Fenster has not won "
                     "one that size - say the log shows none."
                     % (len([v for v in nums if v >= 50000]),
                        len([v for v in nums if v >= 200000]),
                        "{:,.0f}".format(nums[-1]) if nums else "-")),
        "leadSources": [{"source": s, "jobs": n}
                        for s, n in src_counts.most_common()],
        "leadSourceNote": (
            "%d of %d won contracts (%d%%) came from a client Fenster already "
            "had. A further %d came from Jayk by name - a quarter of the whole "
            "win history, from one business development manager who has left, "
            "with nothing put in his place. Only %d ever came from a tender "
            "portal. That is the shape of the problem this job exists to fix: "
            "the pipeline is repeat business plus one person, and the person "
            "is gone."
            % (repeat, len(live), round(100.0 * repeat / len(live)) if live else 0,
               src_counts.get("Jayk", 0), src_counts.get("Constructionline", 0))),
        "soldBy": [{"person": p, "jobs": n} for p, n in
                   collections.Counter(r["soldBy"] or "(blank)"
                                       for r in live).most_common()],
        "byYear": [{"year": y, "jobs": n} for y, n in
                   sorted(collections.Counter(r["year"] for r in live
                                              if r["year"]).items())],
        "byArea": [{"area": a, "jobs": n} for a, n in
                   collections.Counter(r["area"] for r in live
                                       if r["area"]).most_common()],
        "clients": clients,
        "contracts": sorted(rows, key=lambda r: -(r["value"] or 0)),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)

    m = doc["money"]
    print("%d won contracts, %d with a value -> %s"
          % (len(rows), len(live), OUT))
    print("  total GBP {:,.0f}   median {:,.0f}   largest {:,.0f}"
          .format(m["total"], m["median"], m["largest"]))
    for b in doc["bands"]:
        print("  {:<16} {:>3} job(s)  GBP {:>12,.0f}"
              .format(b["band"], b["jobs"], b["value"]))
    print("  top client: %s - %d jobs, GBP {:,.0f}".format(clients[0]["value"])
          % (clients[0]["client"], clients[0]["jobs"]))
    print("  lead sources: %s"
          % ", ".join("%s %d" % (s["source"], s["jobs"])
                      for s in doc["leadSources"][:5]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Carry the CRM back to AdminBase, because nothing carries it automatically.

Zac, 03/08: run the two in parallel. The constraint the meeting did not have is
that **AdminBase has no API and no live feed**. `jacob_adminbase.py` reads a CSV
Adam exported by hand on 28/07 and its own docstring says "a live feed will
follow" - it never did. So "parallel" cannot mean two systems kept in step by
typing; somebody would be re-keying every lead twice and one of the two would
drift, which is exactly the state the CRM exists to end.

So: the hub holds the record, and this emits an AdminBase-shaped CSV in the
same column order as the export it reads. Adam imports it, or uses it to see
what has moved. It is a bridge, not a sync - there is no way to write into
AdminBase from here and this file does not pretend otherwise.

WHAT IT DOES ABOUT VAT, WHICH IS THE EASY WAY TO CORRUPT ADAM'S CRM: AdminBase
holds VALUE inclusive of VAT and the CRM holds everything exclusive. Values are
multiplied back up by 1.2 on the way out and the column is labelled so, because
writing an ex-VAT number into an inc-VAT field would understate his pipeline by
a sixth and it would look perfectly plausible.

  python scripts/crm_export.py                     # to outputs/
  python scripts/crm_export.py --changed-since 2026-07-30
"""
import argparse
import csv
import datetime as dt
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "outputs")

# The column order of the file AdminBase exported, so a person opening both
# sees the same shape. Blank columns are left blank rather than invented.
COLUMNS = [
    "LEADNUMBER", "LEADDATE", "LEADNAME", "ADDRESS", "HOMETELEPHONE",
    "WORKTELEPHONE", "SALESPERSON", "LEADSOURCE", "RESULT", "RESULTDATE",
    "NEXTACTIONDATE", "PRODUCTTYPE", "PRODUCTINTEREST1", "PRODUCTINTEREST2",
    "SALESAREA", "OFFICEREF", "SITEADDRESS", "APPOINTMENTDATE",
    "APPOINTMENTTIME", "MOBILE", "POSTCODE", "DEMODATE", "LEADCATEG", "TEAM",
    " VALUE ", "EMAIL", "SUBSUBSOURCE", "FAX", "TAKENBY", "PAYMENTMETHOD",
]

# Our stages back into AdminBase's own vocabulary. Only the ones it has words
# for - a stage it cannot express is left as its nearest truthful neighbour
# rather than invented, because a wrong RESULT is worse than a coarse one.
RESULT_FROM_STAGE = {
    "new": "Live - Appointment to be booked",
    "acknowledged": "Live - Appointment Booked",
    "materials_out": "Live - Quote being prepared",
    "awaiting_costs": "Live - Quote being prepared",
    "quote_ready": "Live - Quote being prepared",
    "pre_quote_call": "Live - Quote being prepared",
    "quote_sent": "Live - Quoted",
    "follow_up": "Live - Quoted",
    "final_follow_up": "Live - Quoted",
    "closed": "Live - Quoted",
}
VAT = 1.2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed-since", help="YYYY-MM-DD - only rows touched since")
    ap.add_argument("--out")
    a = ap.parse_args()

    companies = {c["key"]: c for c in crm.companies()}
    rows = crm.leads()
    if a.changed_since:
        rows = [r for r in rows if (r.get("updated") or "")[:10] >= a.changed_since]

    os.makedirs(OUT_DIR, exist_ok=True)
    path = a.out or os.path.join(
        OUT_DIR, "AdminBase-import-%s.csv" % dt.date.today().strftime("%Y%m%d"))

    written = 0
    with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            co = companies.get(r.get("company_key")) or {}
            value = r.get("value")
            w.writerow({
                "LEADNUMBER": r.get("adminbase_ref") or "",
                "LEADDATE": (r.get("created") or "")[:10],
                "LEADNAME": co.get("name") or r.get("company_key") or "",
                "RESULT": RESULT_FROM_STAGE.get(r.get("stage"), ""),
                "NEXTACTIONDATE": r.get("next_action_date") or "",
                "SITEADDRESS": r.get("site") or "",
                "POSTCODE": r.get("postcode") or "",
                # Back to inclusive, because that is what the field means there.
                " VALUE ": round(value * VAT, 2) if value else "",
                "OFFICEREF": r.get("key"),
                "SALESPERSON": r.get("owner") or "",
                "LEADSOURCE": r.get("source") or "",
            })
            written += 1

    print("wrote %d lead(s) to %s" % (written, os.path.relpath(path, REPO)))
    print("VALUE is inclusive of VAT in this file (x1.2), matching AdminBase's own column.")
    if not a.changed_since:
        print("Tip: --changed-since YYYY-MM-DD gives only what has moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

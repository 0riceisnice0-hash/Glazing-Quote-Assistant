# -*- coding: utf-8 -*-
"""Record this run in data/calibration.json - one entry, appended idempotently."""
import json, os

CAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "data", "calibration.json")

ENTRY = {
    "job": "CURTAIN WALLING - the engine could not price it at all, and 8 rows it prices to the penny",
    "client": "-",
    "date": "2026-07-30",
    "mary_estimate": 12.28,
    "actual": 13.28,
    "basis": "leave-one-JOB-out over 29 documents in 26 jobs, the lab's decision metric. "
             "BEFORE 13.28% mean abs / median 7.92% / bias -2.01% / 15-29 within 10 / 508 lines. "
             "AFTER 12.28% / median 6.86% / bias -1.83% / 17-29 within 10 / 516 lines. "
             "--holdout --folds 13.20% -> 12.19%.",
    "basis_type": "COVERAGE GAIN, NOT AN ACCURACY GAIN - the denominator changed, 508 lines to 516, "
                  "and these two figures are NOT the same measurement. Quote them as a pair or not "
                  "at all. Not one of the 508 lines already priced moved: the learned rate table is "
                  "byte-identical either side, 18 buckets, sha 41896b6a94ff44ee, verified by running "
                  "HEAD's learn() and the new one over the same corpus in one process.",
    "lesson": "THE ENGINE HAD A CURTAIN-WALLING CONVENTION SINCE 22/07 AND NOTHING COULD REACH IT. "
              "read_doc dropped every row whose code was not in CODE_VALUE, and a genuine CW row has "
              "no product code, so all 8 in the archive were discarded before pricing - GBP 111,127.95 "
              "of sell across 6 documents, and on CB Refrigeration one row is 36% of the document. "
              "The marker is the CW LABOUR cell, and it has to be something other than the CW column: "
              "CW on a CODED row is a working column holding area x GBP 850 and NOT money in the unit "
              "rate, 156 lines of it (30/07). A genuine CW row is the other thing - no code, a CW "
              "LABOUR figure, and the unit rate IS the area money. "
              "THE 850 IS NOT CIRCULAR, which is the only reason this is worth keeping. It was "
              "calibrated off Greenfields, so those 2 rows prove nothing; it reproduces on 5 of the 6 "
              "rows it was never set from, all within 3p - St Mary's Type AK 8,655.98, CB Refrigeration "
              "CWT-A 15,036.50, St Christopher's EW1 7,811.53 and W2 3,898.91, Wisley CW1 19,975.00. "
              "Per-row error over all 8: mean abs 1.58%, median 0.00%, 7 of 8 inside 0.1%. It takes no "
              "learned rate and no code adder, so it is identical in every fold. "
              "THE ONE MISS IS SCOPE, NOT RATE: Georgie's -12.66%, short by exactly GBP 2,000.02, and "
              "its description is 'CW01, D03, CW02' - a door in with the curtain walling. Same lesson "
              "as Oldswinford's coupler. "
              "MINING IS GUARDED. A CW row would key a bucket '|band' - unreachable in learn(), but "
              "learn_supplier_factors() reads the same buckets and a bogus one would move a real "
              "supplier's correction. supply_money() returns None for CW rows, the single place both "
              "callers pass through. Second reason: CB Refrigeration's CW Frames cell holds the "
              "notional, so mining it would teach a figure no supplier ever charged. "
              "AND THE AUDIT SIDE OF THE SAME NIGHT closed the last two open supplier questions. "
              "Brandon Estate 4.094 was the reader taking 362,678.40 from a spare working cell in the "
              "first priced row - that row's own (frames + glass) x qty to the penny - because the "
              "block names BSW and Vetroseal and types no cost, so neither the stop-at-empty-row rule "
              "nor the looks-like-a-priced-row rule could fire. The block now ends at the priced-row "
              "header, which is a fact about the template rather than a tolerance. CB Refrigeration "
              "1.291 was the CW notional booked as a cost: its other two block figures are its own "
              "rows to the penny. Both are cost-record findings, NEITHER is a client-facing error, and "
              "ADAM'S MORNING LIST IS STILL GORDON COURT REV 2 ALONE. "
              "CB REFRIGERATION STAYS IN THE CALIBRATION SET, which is a more careful reading of the "
              "lab's rule than excluding it. The rule is never to tune the engine to reproduce a "
              "defect; the defect is in the COST cell, which the engine no longer reads, while the "
              "SELL cell is correct at area x 850 and matches six other rows. Exclude the cell, not "
              "the document.",
    "date_note": "THE LAB'S ENTRY DATES RUN A DAY AHEAD OF REALITY AND THIS ENTRY DOES NOT. The "
                 "previous entry is dated 2026-07-31 and its board commit landed Thu 30 Jul 2026 "
                 "05:59 +0100; the system date for this run is 2026-07-30. So this entry is LATER "
                 "than the one dated 2026-07-31 despite the earlier date. Commit order in git is the "
                 "reliable sequence, not these dates. Prose in this run's commits says '31/07' to "
                 "match the board's existing labelling for the night.",
}

with open(CAL, encoding="utf-8") as fh:
    cal = json.load(fh)
if any(e.get("job") == ENTRY["job"] for e in cal["entries"]):
    print("already present")
else:
    cal["entries"].append(ENTRY)
    with open(CAL, "w", encoding="utf-8") as fh:
        json.dump(cal, fh, indent=2, ensure_ascii=False)
    print("added")
print("entries now %d" % len(cal["entries"]))

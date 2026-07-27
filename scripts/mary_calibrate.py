# -*- coding: utf-8 -*-
"""The fast feedback loop: Mary's number vs the number that actually went out.

Win/loss takes months to come back and is recorded on barely any job. But
every quote Fenster issues is a free comparison, available within days, on
every job, needing nothing from anybody: Mary's own figure is on file the
moment she prices, and the client quote lands in the job folder as a clone of
MASTER PRICING DOC that scripts/mary_quote_reader.py can read.

So this pairs the two and writes the delta into data/calibration.json, which
is what the hub's Scoreboard reports. Run it after any session that priced
something, or on a schedule.

  python scripts/mary_calibrate.py --record --job "Vesuvius Way" --value 110551.98 \
      --basis "budget, no supplier quote held"
  python scripts/mary_calibrate.py --run            # match and append
  python scripts/mary_calibrate.py --run --dry-run  # show what it would add
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_quote_reader as reader

REPO = mg.REPO
ESTIMATES = os.path.join(REPO, "data", "estimates.json")
CALIB = os.path.join(REPO, "data", "calibration.json")
TENDERS = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                       "Commercial", "1. Tender Documents")
# Below this a "quote" is an allowance or a part-filled sheet, not a job price.
MIN_SENSIBLE = 1000.0
# Beyond this, treat the pairing as suspect rather than as evidence. A genuine
# estimating miss is tens of percent; hundreds means we matched the wrong file.
PLAUSIBLE_PCT = 60.0

# A blank clone of the master sits in nearly every job folder. Vesuvius matched
# one holding a stray GBP 4,000 and reported Mary as 2,663% out.
TEMPLATE_NAMES = ("master pricing doc", "master pricing document", "pricing doc ", "master quote")
# Mary's own output also gets filed into job folders. Scoring her against her
# own workbook is circular and would flatter her to meaninglessness.
MARY_OUTPUTS = ("fenster pricing document", "fenster pricing doc", "proposal and pricing review",
                "take-off", "quote check", "and review")
# A quote that actually went to a client is filed under the CLIENT's name -
# "Stepnell - BCC Filwood Broadway Pricing.xlsx". That prefix is the strongest
# available signal that a human sent it, so it overrides the exclusions above.
def looks_sent(filename, client):
    low, c = str(filename or "").lower(), norm(client).split(" ")[0]
    return bool(c) and len(c) > 3 and low.startswith(c)


def is_untrustworthy(filename, client=""):
    low = str(filename or "").lower()
    if looks_sent(filename, client):
        return ""
    if any(t in low for t in TEMPLATE_NAMES):
        return "an unfilled MASTER template clone"
    if any(m in low for m in MARY_OUTPUTS):
        return "Mary's own document - comparing her to herself proves nothing"
    return ""


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(s or "").lower())).strip()


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)


def record(job, value, basis, client=""):
    data = load(ESTIMATES, {"note": "Mary's own figure for a job, written when she prices it. "
                                    "mary_calibrate.py pairs these against the client quote that "
                                    "actually went out.", "entries": []})
    entries = [e for e in data["entries"] if norm(e["job"]) != norm(job)]
    entries.append({"job": job, "client": client, "value": float(value), "basis": basis,
                    "recorded": dt.datetime.now().strftime("%Y-%m-%d")})
    data["entries"] = sorted(entries, key=lambda e: e["recorded"], reverse=True)
    save(ESTIMATES, data)
    return data


def run(dry_run=False):
    estimates = load(ESTIMATES, {"entries": []})["entries"]
    if not estimates:
        print("no estimates recorded yet - use --record when you price something")
        return []

    calib = load(CALIB, {"entries": []})
    already = {norm(e["job"]) for e in calib.get("entries", [])}

    print("scanning the tender archive for client quotes...")
    quotes = reader.scan(TENDERS)
    by_job = {}
    skipped = 0
    for q in quotes:
        if q["total"] < MIN_SENSIBLE:
            continue
        why = is_untrustworthy(q["file"], q["client"])
        if why:
            skipped += 1
            continue
        key = norm(q["job"])
        # Keep the most recently modified quote for each job - that is the one
        # that went out.
        if key not in by_job or q["modified"] > by_job[key]["modified"]:
            by_job[key] = q
    print("  %d filled quote(s); %d ignored as templates or Mary's own work; %d job(s) left"
          % (len(quotes), skipped, len(by_job)))

    def find_quote(job):
        """Folder names and Mary's names rarely match exactly - 'Filwood
        Broadway' vs 'BCC Filwood Broadway'. Accept a containment match, but
        only on a distinctive stem, so 'Wexham' cannot swallow 'Wexham Park'."""
        key = norm(job)
        if key in by_job:
            return by_job[key]
        cands = [q for k, q in by_job.items()
                 if len(k) >= 6 and len(key) >= 6 and (k in key or key in k)]
        return cands[0] if len(cands) == 1 else None

    added, suspect = [], []
    for est in estimates:
        key = norm(est["job"])
        if key in already:
            continue
        quote = find_quote(est["job"])
        if not quote:
            continue
        err = (est["value"] - quote["total"]) / quote["total"] * 100.0
        entry = {
            "job": est["job"],
            "client": est.get("client") or quote["client"],
            "date": dt.datetime.fromtimestamp(quote["modified"]).strftime("%Y-%m-%d"),
            "mary_estimate": round(float(est["value"]), 2),
            "actual": quote["total"],
            "basis": "Mary: %s. Actual: the client quote issued from the job folder (%s)"
                     % (est.get("basis", "her own figure"), quote["file"]),
            "lesson": "",
            "auto": True,
        }
        if abs(err) > PLAUSIBLE_PCT:
            suspect.append((err, est["job"], quote))
            continue
        added.append(entry)
        print("  %+7.2f%%  %-34s mary %12s vs sent %12s  [%s]"
              % (err, est["job"][:34], "{:,.2f}".format(est["value"]),
                 "{:,.2f}".format(quote["total"]), quote["file"][:34]))

    if suspect:
        print("\n  HELD BACK for a human - more than %.0f%% apart, which usually means the wrong\n"
              "  file was matched rather than a genuine estimating miss:" % PLAUSIBLE_PCT)
        for err, job, quote in suspect:
            print("    %+9.1f%%  %-30s vs %s in %s"
                  % (err, job[:30], "{:,.2f}".format(quote["total"]), quote["file"][:40]))

    if not added:
        print("\n  nothing new to add")
        return []
    if dry_run:
        print("\n(dry run - nothing written)")
        return added
    calib.setdefault("entries", []).extend(added)
    save(CALIB, calib)
    print("\nadded %d comparison(s) to data/calibration.json" % len(added))
    print("Fill in the 'lesson' on each - the number alone teaches nothing.")
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--job")
    ap.add_argument("--client", default="")
    ap.add_argument("--value", type=float)
    ap.add_argument("--basis", default="")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.record:
        if not args.job or args.value is None:
            print("--record needs --job and --value")
            return 2
        record(args.job, args.value, args.basis, args.client)
        print("recorded %s = %s" % (args.job, "{:,.2f}".format(args.value)))
        return 0
    if args.run or args.dry_run:
        run(dry_run=args.dry_run)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

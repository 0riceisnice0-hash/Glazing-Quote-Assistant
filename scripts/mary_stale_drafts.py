"""Report drafts in outputs\\ that have passed, or are approaching, a date written into
their own filename.

Written for Gordon Court 28/07/2026 after riverside found a superseded reply to Adam still
sitting in outputs\\ under a clean-looking name. Their hazard was an UNDATED draft that went
quietly wrong. The mirror hazard is a DATED one: a letter whose whole argument is "this is an
addendum to a live quotation" is actively false the morning after the quotation lapses, and
it is still sitting there in the house voice with the right addressee on it.

A dated draft is the easier of the two to defend against, because the expiry is knowable in
advance. This is that defence.

WHAT IT DOES NOT DO. It cannot tell you whether an undated draft has been overtaken by
events - that needs somebody who knows the job. Undated drafts are listed, not judged.

    python scripts\\mary_stale_drafts.py
    python scripts\\mary_stale_drafts.py --today 2026-08-07     # what does 7 August look like
    python scripts\\mary_stale_drafts.py --warn-days 14
"""

import argparse
import datetime as dt
import os
import re
import sys

OUTPUTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")

# "(draft, send by 06-08)" / "send by 6-8" / "send by 06-08-2026"
SEND_BY = re.compile(r"send\s+by\s+(\d{1,2})[-/.](\d{1,2})(?:[-/.](\d{2,4}))?", re.I)
# "(SUPERSEDED 27-07, do not send)"
SUPERSEDED = re.compile(r"superseded\s*(\d{1,2})[-/.](\d{1,2})(?:[-/.](\d{2,4}))?", re.I)
DO_NOT_SEND = re.compile(r"do\s+not\s+send", re.I)


def _to_date(day, month, year, today):
    """Filenames usually omit the year. Take the reading nearest to today."""
    if year:
        y = int(year)
        if y < 100:
            y += 2000
        return dt.date(y, int(month), int(day))
    best = None
    for y in (today.year - 1, today.year, today.year + 1):
        try:
            cand = dt.date(y, int(month), int(day))
        except ValueError:
            continue  # 29 Feb in a non-leap year
        if best is None or abs((cand - today).days) < abs((best - today).days):
            best = cand
    return best


def scan(outputs=OUTPUTS, today=None, warn_days=14):
    today = today or dt.date.today()
    expired, due, dead, undated = [], [], [], []

    if not os.path.isdir(outputs):
        return expired, due, dead, undated

    for name in sorted(os.listdir(outputs)):
        if name.startswith((".~", "~$")) or not os.path.isfile(os.path.join(outputs, name)):
            continue

        m = SUPERSEDED.search(name)
        if m:
            dead.append((name, _to_date(m.group(1), m.group(2), m.group(3), today)))
            continue
        if DO_NOT_SEND.search(name):
            dead.append((name, None))
            continue

        m = SEND_BY.search(name)
        if m:
            when = _to_date(m.group(1), m.group(2), m.group(3), today)
            days = (when - today).days
            if days < 0:
                expired.append((name, when, days))
            elif days <= warn_days:
                due.append((name, when, days))
            continue

        if re.search(r"\bdraft\b", name, re.I):
            undated.append(name)

    return expired, due, dead, undated


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outputs", default=OUTPUTS)
    ap.add_argument("--today", help="YYYY-MM-DD, to see a future date's report")
    ap.add_argument("--warn-days", type=int, default=14)
    ap.add_argument("--quiet", action="store_true", help="only print if something is wrong")
    a = ap.parse_args()

    today = dt.datetime.strptime(a.today, "%Y-%m-%d").date() if a.today else dt.date.today()
    expired, due, dead, undated = scan(a.outputs, today, a.warn_days)

    if a.quiet and not expired:
        return 1 if expired else 0

    print("STALE DRAFT SWEEP - outputs\\   as at {}".format(today.strftime("%d/%m/%Y")))
    print("=" * 78)

    if expired:
        print("\nEXPIRED - the send-by date in the filename has passed.")
        print("These read as addenda to live quotations. They are not, any more.")
        for name, when, days in expired:
            print("  ! {}".format(name))
            print("      send-by {} - {} day(s) ago".format(when.strftime("%d/%m/%Y"), -days))

    if due:
        print("\nDUE WITHIN {} DAYS.".format(a.warn_days))
        for name, when, days in due:
            print("  > {}   {} ({} day(s))".format(name, when.strftime("%d/%m/%Y"), days))

    if dead:
        print("\nMARKED SUPERSEDED / DO NOT SEND - correctly labelled, no action.")
        for name, when in dead:
            print("  - {}{}".format(name, "" if not when else ""))

    if undated:
        print("\nUNDATED DRAFTS - {} file(s). NOT judged: a filename cannot tell you".format(len(undated)))
        print("whether the facts underneath one have moved. Somebody who knows the job must look.")
        for name in undated:
            print("  . {}".format(name))

    if not expired:
        print("\nNothing expired.")
    print()
    return 1 if expired else 0


if __name__ == "__main__":
    sys.exit(main())

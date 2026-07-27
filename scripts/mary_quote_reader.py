# -*- coding: utf-8 -*-
"""Read the headline total out of a Fenster pricing document.

Every client quote is a clone of MASTER PRICING DOC, so the total can be
pulled without knowing anything about the job. This is the other half of the
fast feedback loop: Mary's own number is on file already, and this gets the
number a human actually sent, within days rather than the months a win or loss
takes to come back.

Quirks that matter, all learned the hard way:
  - The sheet is named "Pricing Document " WITH A TRAILING SPACE in the master.
  - Workbooks written by openpyxl carry formulas but no cached values, so
    data_only reads None. Excel-saved files (the ones actually sent) do have
    cached values - which is exactly the population we care about.
  - The archive is full of unfilled MASTER template copies. A doc with no
    positive total is a blank, not a quote, and must not be treated as one.

Usage:
  python scripts/mary_quote_reader.py <file.xlsx>
  python scripts/mary_quote_reader.py --scan "<folder>"   # every quote under it
"""
import argparse
import os
import re
import sys

MONEY_LABELS = ("total", "grand total", "total ex vat", "total excluding vat")
IGNORE_LABELS = ("inc vat", "including vat", "vat", "optional", "mastic", "epdm")


def read_total(path):
    """Return (total, label, sheet) or (None, reason, None)."""
    try:
        import openpyxl
    except ImportError:
        return None, "openpyxl not available", None
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception as e:
        return None, "could not open: %s" % e, None

    best = None
    try:
        for ws in wb.worksheets:
            if not ws.title.strip().lower().startswith("pricing document"):
                continue
            for row in ws.iter_rows(values_only=True):
                cells = list(row)
                label = ""
                for c in cells:
                    if isinstance(c, str) and c.strip():
                        low = c.strip().lower()
                        if any(low.startswith(m) for m in MONEY_LABELS):
                            label = c.strip()
                            break
                if not label:
                    continue
                low = label.lower()
                if any(bad in low for bad in IGNORE_LABELS) and "ex vat" not in low:
                    continue
                nums = [c for c in cells if isinstance(c, (int, float)) and c and c > 0]
                if not nums:
                    continue
                value = max(nums)
                # The first plain TOTAL wins; later rows are VAT and optionals.
                if best is None or value > best[0]:
                    best = (float(value), label, ws.title)
    finally:
        wb.close()

    if not best:
        return None, "no filled total found (likely an unused template copy)", None
    return best


def job_from_path(path):
    """<client>/<job>/1. Estimating/3. Client Quote/x.xlsx -> (client, job)."""
    parts = os.path.normpath(path).split(os.sep)
    try:
        i = parts.index("1. Tender Documents")
    except ValueError:
        return "", ""
    client = parts[i + 1] if len(parts) > i + 1 else ""
    job = parts[i + 2] if len(parts) > i + 2 else ""
    if job.lower().startswith(("1. estimating", "2. ", "3. ")):
        job = client
    return client, job


def scan(root):
    found = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if not name.lower().endswith((".xlsx", ".xlsm")) or name.startswith("~$"):
                continue
            if "pricing" not in name.lower() and "quote" not in name.lower():
                continue
            path = os.path.join(dirpath, name)
            total, label, _sheet = read_total(path)
            if total:
                client, job = job_from_path(path)
                found.append({"client": client, "job": job, "file": name,
                              "path": path, "total": round(total, 2), "label": label,
                              "modified": os.path.getmtime(path)})
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--scan", action="store_true")
    args = ap.parse_args()

    if args.scan:
        rows = scan(args.target)
        rows.sort(key=lambda r: -r["modified"])
        print("%d filled quote(s) found" % len(rows))
        for r in rows[:40]:
            print("  %-26s %-30s %12s  (%s)" % (r["client"][:26], r["job"][:30],
                                                "{:,.2f}".format(r["total"]), r["label"][:22]))
        return 0

    total, label, sheet = read_total(args.target)
    if total is None:
        print("no total: %s" % label)
        return 1
    print("%s = %s  [sheet %r]" % (label, "{:,.2f}".format(total), sheet))
    return 0


if __name__ == "__main__":
    sys.exit(main())

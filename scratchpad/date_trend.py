# -*- coding: utf-8 -*-
"""Does what Fenster charges move with TIME, and is the engine blind to it?

The engine prices by code and size band, taking the median of every line in the
archive for that bucket. If GBP/m2 has risen over the years the archive covers,
that median is the middle of HISTORY and the engine will price today's job at an
average of several years ago - which would show up as the -2.01% bias it has.

Date is a fair term in a way the product heading was not. The heading failed
because the headings that separate hardest are each unique to one document, so a
factor big enough to matter was that job's identity. A date is not: it is known
before the job is priced, every document has one, and material inflation is a
real mechanism rather than a fitted constant.

Measured the same way quantity was - each line's own supply GBP/m2 over the
median for its OWN code and size band, so product and size are held constant by
construction, and the only thing left varying is when it was priced."""
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import mary_backtest as bt          # noqa: E402
import mary_pricing as engine       # noqa: E402
import mary_calibrate as cal        # noqa: E402
import mary_quote_reader as reader  # noqa: E402

DATE_RE = re.compile(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})")


def doc_date(path):
    """The 'Date:' cell at the head of a pricing document, as (year, month)."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return None
    try:
        import datetime
        for w in wb.worksheets:
            if not w.title.strip().lower().startswith("pricing document"):
                continue
            for row in w.iter_rows(values_only=True):
                for i, c in enumerate(row):
                    if isinstance(c, str) and c.strip().lower().startswith("date:"):
                        m = DATE_RE.search(c)
                        if m:
                            return int(m.group(3)) + (int(m.group(2)) - 1) / 12.0
                        for d in list(row)[i + 1:]:
                            if isinstance(d, datetime.datetime):
                                return d.year + (d.month - 1) / 12.0
                            if isinstance(d, str) and DATE_RE.search(d):
                                m = DATE_RE.search(d)
                                return int(m.group(3)) + (int(m.group(2)) - 1) / 12.0
            break
        return None
    finally:
        wb.close()


# Match the corpus the backtest scores, then put a date against each document.
docs = bt.collect()
paths = {}
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    paths.setdefault(os.path.basename(q["path"]), q["path"])

base = bt.learn(docs)
rows, undated = [], []
for d in docs:
    p = paths.get(d["file"])
    t = doc_date(p) if p else None
    if t is None:
        undated.append(d["file"])
        continue
    for l in d["lines"]:
        money = bt.supply_money(l)
        if not money or l["area"] <= 0:
            continue
        key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
        b = base.get(key)
        if not b or not b["median_per_m2"] or b["n"] < engine.MIN_LEARNED_N:
            continue
        rows.append({"t": t, "ratio": (money / l["area"]) / b["median_per_m2"],
                     "file": d["file"], "qty": l["qty"]})

print("%d lines dated, %d document(s) with no readable date: %s\n"
      % (len(rows), len(undated), ", ".join(f[:30] for f in undated[:6])))

print("BY YEAR - ratio of the line's own supply rate to its code+band median")
print("%-8s %6s %6s %10s %10s" % ("YEAR", "n", "DOCS", "MED RATIO", "MEAN RATIO"))
for yr in sorted({int(r["t"]) for r in rows}):
    sel = [r for r in rows if int(r["t"]) == yr]
    print("%-8d %6d %6d %10.3f %10.3f"
          % (yr, len(sel), len({r["file"] for r in sel}),
             statistics.median(r["ratio"] for r in sel),
             statistics.fmean(r["ratio"] for r in sel)))

print("\nPER JOB MEDIAN - so one big document cannot carry the trend")
per = {}
for r in rows:
    per.setdefault(r["file"], []).append(r)
jobs = [(statistics.median(x["t"] for x in rs), statistics.median(x["ratio"] for x in rs), f)
        for f, rs in per.items()]
for t, ra, f in sorted(jobs):
    print("  %8.2f  %6.3f  %s" % (t, ra, f[:58]))

xs = [t for t, _, _ in jobs]
ys = [ra for _, ra, _ in jobs]
if len(xs) > 2 and len(set(xs)) > 1:
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sxy / sxx
    res = [y - (my + slope * (x - mx)) for x, y in zip(xs, ys)]
    r2 = 1 - sum(e * e for e in res) / sum((y - my) ** 2 for y in ys)
    print("\nLEAST SQUARES on the per-JOB medians")
    print("  slope %+.4f ratio per year   R^2 %.4f over %d jobs   span %.1f years"
          % (slope, r2, len(xs), max(xs) - min(xs)))
    print("  over the archive's span that is %+.1f%%" % (slope * (max(xs) - min(xs)) * 100))

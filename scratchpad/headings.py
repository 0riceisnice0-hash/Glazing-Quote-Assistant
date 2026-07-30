# -*- coding: utf-8 -*-
"""The product type is in a section heading, and the engine never reads it.

CB Refrigeration's SAD and DAD lines need GBP 881-1,474/m2 against learned rates
of 475 and 668, and the engine is 31-50% under on every one. The reason is in the
row ABOVE them: row 15 says 'External Steel Door' and row 17 says 'Internal Steel
door'. They are Strongdoor steel security doors carrying an aluminium door code.
Tradeteam Stretton is a 'Tilt & Turn Aluminium' MAW needing GBP 771/m2 against
396.92. Gordon Court headings read 'Sheerline Aluminium Louvre', 'Sheerline
Aluminium T&T AO', 'Liniar uPVC windows'.

So a heading row - text in the description column, no quantity, no rate - carries
the system and the product, which is exactly what an estimator prices from and
exactly what the engine has no term for. Extract it, carry it down onto the lines
beneath it, and measure whether the keywords actually separate rates."""
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_calibrate as cal
import mary_pricing as engine
import mary_quote_reader as reader
import openpyxl

SIZE_RE = bt.SIZE_RE


def headings_for(path):
    """Map unit rate -> the section heading in force above that row."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {}
    try:
        ws = [w for w in wb.worksheets
              if w.title.strip().lower().startswith("pricing document")][0]
        current = ""
        for row in ws.iter_rows(values_only=True):
            cells = list(row) + [None] * (16 - len(row))
            code = str(cells[1]).strip().upper() if isinstance(cells[1], str) else ""
            ur = cells[7] if isinstance(cells[7], (int, float)) else None
            desc = str(cells[2]).strip() if isinstance(cells[2], str) else ""
            # A heading: real words in the description column, no size and no
            # rate. That also catches 'Doors' with a stray 1 in Qty, which is
            # the row that cost the audit a false alarm twice.
            if desc and not SIZE_RE.search(desc) and ur is None \
                    and sum(c.isalpha() for c in desc) >= 4 \
                    and not desc.lower().startswith(("client", "project", "site", "date",
                                                     "description", "total", "installation")):
                current = desc
                continue
            if code in engine.CODE_VALUE and ur:
                out.setdefault(round(float(ur), 2), []).append(current)
    finally:
        wb.close()
    return out


paths = {}
for q in reader.scan(cal.TENDERS):
    paths.setdefault(os.path.basename(q["path"]), q["path"])

docs = bt.collect()
base = bt.learn(docs)
rows = []
for d in docs:
    hm = headings_for(paths[d["file"]])
    used = {}
    for l in d["lines"]:
        k = round(l["unit_rate"], 2)
        i = used.get(k, 0)
        used[k] = i + 1
        hs = hm.get(k) or [""]
        head = hs[i] if i < len(hs) else hs[-1]
        money = bt.supply_money(l)
        if not money or l["area"] <= 0:
            continue
        key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
        b = base.get(key)
        if not b or b["n"] < engine.MIN_LEARNED_N:
            continue
        rows.append({"head": head, "ratio": (money / l["area"]) / b["median_per_m2"],
                     "code": l["code"], "file": d["file"], "qty": l["qty"]})

print("%d lines carry a heading and a comparable band median\n" % len(rows))
got = sum(1 for r in rows if r["head"])
print("heading found on %d of them (%.0f%%)\n" % (got, 100.0 * got / max(1, len(rows))))

KEYWORDS = ["steel", "tilt", "t&t", "louvre", "secondary", "curtain", "shopfront",
            "screen", "sheerline", "liniar", "upvc", "casement", "door", "fire",
            "automat", "commercial", "residential", "window"]
print("%-13s %6s %10s %10s %6s   %s" % ("KEYWORD", "n", "MED RATIO", "MEAN", "JOBS", "verdict"))
for kw in KEYWORDS:
    sel = [r for r in rows if kw in r["head"].lower()]
    if len(sel) < 4:
        continue
    med = statistics.median(r["ratio"] for r in sel)
    jobs = len({r["file"] for r in sel})
    v = ""
    if jobs >= 2 and (med >= 1.25 or med <= 0.8):
        v = "SEPARATES"
    elif jobs < 2:
        v = "one job only"
    print("%-13s %6d %10.3f %10.3f %6d   %s"
          % (kw, len(sel), med, statistics.fmean(r["ratio"] for r in sel), jobs, v))

print("\nTHE HEADINGS THEMSELVES, where the ratio is furthest from 1.00 (n>=3):")
byhead = {}
for r in rows:
    byhead.setdefault(r["head"].lower()[:44], []).append(r)
sel = [(statistics.median(r["ratio"] for r in rs), h, rs) for h, rs in byhead.items() if len(rs) >= 3]
for m, h, rs in sorted(sel)[:8]:
    print("  %5.2f  n=%-3d %-46s %s" % (m, len(rs), h or "(none)", sorted({r["code"] for r in rs})))
print("  ...")
for m, h, rs in sorted(sel)[-8:]:
    print("  %5.2f  n=%-3d %-46s %s" % (m, len(rs), h or "(none)", sorted({r["code"] for r in rs})))

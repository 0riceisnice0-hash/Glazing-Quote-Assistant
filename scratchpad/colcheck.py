# -*- coding: utf-8 -*-
"""Where do the component headers actually sit, across the whole archive?

mary_backtest.parse_doc reads by FIXED index (qty 5, unit rate 7, frames 9,
glass 10) and does not read Additional at all. Before adding Additional at index
11, check the headers really are where the two documents I dumped by hand put
them - otherwise the fix would silently mine the wrong column on some jobs."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_calibrate as cal
import mary_quote_reader as reader
import openpyxl

WANT = {"qty": 5, "unit rate": 7, "total": 8, "frames": 9, "glass": 10,
        "additional": 11, "cw": 12}
seen = {}
docs = 0
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    try:
        wb = openpyxl.load_workbook(q["path"], read_only=True, data_only=True)
    except Exception:
        continue
    sheets = [w for w in wb.worksheets if w.title.strip().lower().startswith("pricing document")]
    if not sheets:
        wb.close()
        continue
    docs += 1
    for row in sheets[0].iter_rows(values_only=True, max_row=20):
        for i, c in enumerate(list(row)[:16]):
            if not isinstance(c, str):
                continue
            t = c.strip().lower()
            t = "unit rate" if t.replace(" ", "") == "unitrate" else t
            if t.startswith("additional"):
                t = "additional"
            if t in WANT:
                seen.setdefault(t, {}).setdefault(i, set()).add(q["file"])
    wb.close()

print("%d documents with a pricing sheet\n" % docs)
print("%-12s %-9s %s" % ("HEADER", "EXPECTED", "COLUMNS IT IS ACTUALLY FOUND IN"))
for name, want in WANT.items():
    got = seen.get(name, {})
    bits = []
    for i in sorted(got):
        bits.append("%d(%d doc%s)%s" % (i, len(got[i]), "" if len(got[i]) == 1 else "s",
                                        "" if i == want else "  <-- NOT %d" % want))
    print("%-12s %-9d %s" % (name, want, "   ".join(bits) or "never found"))

print("\nany document where a header sits somewhere unexpected:")
bad = False
for name, want in WANT.items():
    for i, files in seen.get(name, {}).items():
        if i != want:
            bad = True
            for f in sorted(files)[:6]:
                print("  %-16s col %-3d  %s" % (name, i, f[:64]))
if not bad:
    print("  none - every header that exists sits exactly where parse_doc assumes")

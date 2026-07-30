# -*- coding: utf-8 -*-
"""Which documents had a 'Supplier used:' figure read from AT OR BELOW the
priced-row header? That is exactly the set the block-boundary fix can change,
so it is the honest blast radius of the change - no full re-audit needed."""
import os, sys
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_calibrate as cal
import mary_quote_audit as qa
import mary_quote_reader as reader


def header_row(path):
    """Row number of the priced-row header - the row carrying Qty and Unit Rate."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        sheets = [w for w in wb.worksheets
                  if w.title.strip().lower().startswith("pricing document")]
        if not sheets:
            return None
        for rn, row in enumerate(sheets[0].iter_rows(values_only=True), 1):
            texts = [qa._txt(c) for c in list(row) + [None] * 20]
            if any(t in ("qty", "quantity") for t in texts) \
                    and any(t.replace(" ", "") == "unitrate" for t in texts):
                return rn
    finally:
        wb.close()
    return None


seen, n, hits = set(), 0, []
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    d = qa.read_doc(q["path"])
    if not d:
        continue
    sig = repr([[r["code"], r["size"], r["qty"], r["unit_rate"]] for r in d["rows"]])
    if sig in seen:
        continue
    seen.add(sig)
    n += 1
    hr = header_row(q["path"])
    bad = [v for v in d["_sup_vals"] if hr and v[0] >= hr]
    if bad:
        hits.append((d["file"], hr, d["_sup_vals"], bad, d["supplier_names"]))

print("%d documents scanned\n" % n)
print("DOCUMENTS WITH A SUPPLIER FIGURE AT OR BELOW THE PRICED-ROW HEADER:")
for f, hr, allv, bad, names in hits:
    print("  %s" % f)
    print("     header row %s | names %r" % (hr, names))
    print("     all  _sup_vals %r" % (allv,))
    print("     DROPPED        %r" % (bad,))
print("\n%d of %d documents affected" % (len(hits), n))

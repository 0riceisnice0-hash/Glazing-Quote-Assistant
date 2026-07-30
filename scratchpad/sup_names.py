# -*- coding: utf-8 -*-
"""How many suppliers does the block NAME, and how many figures does it carry?

Trafalgar House is reported at ratio 0.657, a GBP 8,633.85 gap between a Frames
column of 16,572.71 and a 'TruFrame' buy of 25,206.56. It names three suppliers:

    Supplier used:  TruFrame
                    Vetroseal
                    Ikon
                                25,206.56

ONE figure for THREE suppliers. The check takes the first name and attributes the
whole figure to it, so it is comparing a combined buy - frames AND glass AND
panels - against the Frames column alone, which is one supplier's scope.

The names carry no money, so the block reader drops them: `money` is empty on
those rows, and a row with no money and nothing yet collected is skipped. Count
them instead, and see how many documents in the archive are shaped this way and
what their ratios do when the comparison uses the whole supply build-up."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import mary_quote_audit as audit  # noqa: E402


def names_in_block(path):
    """Every non-empty label in the 'Supplier used:' block, figure or not."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return None
    try:
        sheets = [w for w in wb.worksheets
                  if w.title.strip().lower().startswith("pricing document")]
        if not sheets:
            return None
        ws = sheets[0]
        col = row0 = None
        names, figs = [], []
        for rn, row in enumerate(ws.iter_rows(values_only=True), 1):
            cells = list(row) + [None] * (20 - len(row))
            for i, c in enumerate(cells):
                if isinstance(c, str) and c.strip().lower().startswith("supplier used"):
                    col, row0 = i, rn
            if col is None or not (row0 <= rn <= row0 + 6):
                continue
            label = cells[col + 1] if len(cells) > col + 1 else None
            money = [m for m in (audit._num(c) for c in cells[col + 2:]) if m and m > 1]
            # NOT a supplier name: the priced-row column headers sit inside the
            # six-row window and one of them lands in the column just after
            # 'Supplier used:'. Trafalgar came out with four names - TruFrame,
            # Vetroseal, Ikon and 'Additional' - and the fourth is the header of
            # the Additional column.
            if isinstance(label, str) and label.strip() and label.strip().lower() not in (
                    "frames", "glass", "additional", "cw", "cw labour", "cw sqm",
                    "unit rate", "total", "qty", "unit", "description", "size"):
                names.append(label.strip())
            if money:
                figs.append(max(money))
        return names, figs
    finally:
        wb.close()


import mary_calibrate as cal      # noqa: E402
import mary_quote_reader as reader  # noqa: E402

paths, seen = [], set()
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    paths.append(q["path"])

rows = []
for path in paths:
    d = audit.read_doc(path)
    if not d or not d.get("supplier_cost"):
        continue
    sig = repr([[r["code"], r["size"], r["qty"], r["unit_rate"]] for r in d["rows"]])
    if sig in seen:
        continue
    seen.add(sig)
    nf = names_in_block(path)
    if not nf:
        continue
    names, figs = nf
    frames = sum((r["frames"] or 0.0) * (r["qty"] or 1) for r in d["rows"])
    fg = sum(((r["frames"] or 0.0) + (r["glass"] or 0.0)) * (r["qty"] or 1)
             for r in d["rows"])
    whole = sum(((r["frames"] or 0.0) + (r["glass"] or 0.0) + (r["additional"] or 0.0))
                * (r["qty"] or 1) for r in d["rows"])
    cost = d["supplier_cost"]
    rows.append({"file": os.path.basename(path), "names": names, "nfig": len(figs),
                 "cost": cost, "frames": frames, "fg": fg, "whole": whole,
                 "rf": frames / cost if cost else 0, "rfg": fg / cost if cost else 0,
                 "rw": whole / cost if cost else 0})

# A glass merchant in the block means the buy it totals covers the Glass column
# too, so the Frames column alone cannot be the thing to reconcile it against.
GLASS = ("vetroseal", "glass", "glaze", "pilkington", "saint gobain", "guardian",
         "romag", "cantifix", "tufwell", "specialist glass")


def has_glass(names):
    return any(any(g in n.lower() for g in GLASS) for n in names)


print("%d documents with a supplier block\n" % len(rows))
print("%-46s %4s %4s %11s %7s %7s %7s %s"
      % ("DOCUMENT", "NAM", "FIG", "BUY", "FRAMES", "F+G", "WHOLE", ""))
for r in sorted(rows, key=lambda r: abs(r["rf"] - 1.0), reverse=True):
    print("%-46s %4d %4d %11s %7.3f %7.3f %7.3f %s"
          % (r["file"][:46], len(r["names"]), r["nfig"], "{:,.0f}".format(r["cost"]),
             r["rf"], r["rfg"], r["rw"], "GLASS" if has_glass(r["names"]) else ""))
    print("      %s" % " / ".join(r["names"]))

print("\nDOES 'THE BLOCK NAMES A GLASS MERCHANT' PICK THE RIGHT COMPARISON?")
print("%-26s %5s %10s %10s %10s" % ("", "n", "|F-1| med", "|F+G-1|", "|WHOLE-1|"))
import statistics  # noqa: E402
for label, sel in (("block names glass", [r for r in rows if has_glass(r["names"])]),
                   ("block does not", [r for r in rows if not has_glass(r["names"])])):
    if not sel:
        continue
    print("%-26s %5d %10.3f %10.3f %10.3f"
          % (label, len(sel),
             statistics.median(abs(r["rf"] - 1) for r in sel),
             statistics.median(abs(r["rfg"] - 1) for r in sel),
             statistics.median(abs(r["rw"] - 1) for r in sel)))

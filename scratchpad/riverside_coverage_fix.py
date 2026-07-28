# -*- coding: utf-8 -*-
"""Printing one real entry found a double-count the rule passes on.

Gordon Court's rule: PRINT ONE REAL ENTRY BEFORE COMPARING ANYTHING TO ANYTHING.
Run here, the first entry printed was

    {"ref": "AOV.01", "qty_sold": 1, "qty_quoted": 2, "supplier_ref": "A Plus QT51518"}

and AOV.02 says the same. So the manifest asserts FOUR units quoted against two
sold, from a quotation that has ONE position block reading "Qty (2)" - counted
off the quote rather than taken from the manifest: one `O/A Sizes`, one
`Frame Price`, one `Glazing Details`, zero `Location:` headers.

`check_supplier_covers_quantity` PASSES on it, because it only asks whether
quoted < sold. The founding case at Brocks Hill was under-coverage - 2 sold, 1
quoted, GBP 2,723.49 with no quote behind it. THIS IS THE SAME MONEY PROBLEM
FROM THE OTHER SIDE: if two lines each claim the same quoted units, one of them
is uncovered and the arithmetic still looks perfect.

So the rule now also catches over-claim, and only where over-claim is possible -
when one supplier reference is credited on more than one line.
"""
import collections
import io
import json

# ------------------------------------------------------------- 1. the data
P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
for c in d['supplier_coverage']:
    c['qty_quoted'] = 1
    c['note'] = ("QT51518 has ONE position block, Qty (2), covering both vents - so each line is "
                 "covered by one quoted unit, not two. Was 2, which asserted four quoted units "
                 "against two sold. Corrected 28/07 after printing the entry.")
d['supplier_quotes'][0]['qty_total'] = 2
d['supplier_quotes'][0]['qty_total_note'] = (
    "Counted off the quotation, not inferred: one 'O/A Sizes', one 'Frame Price', one 'Glazing "
    "Details & Apertures', zero 'Location:' headers, and the position reads 'Qty (2) O/A Sizes "
    "1130mm x 1530mm (Style FF)'.")
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print("coverage corrected:")
for c in d['supplier_coverage']:
    print("   ", json.dumps({k: v for k, v in c.items() if k != 'note'}, ensure_ascii=False))

# ------------------------------------------------------------- 2. the rule
P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

OLD = '''    short, silent = [], []
    for c in cov:
        ref, sold, quoted = c.get("ref", "?"), c.get("qty_sold"), c.get("qty_quoted")
        if sold is None or quoted is None:
            silent.append(ref)
        elif quoted < sold:
            short.append("%s: selling %s, %s quoted %s"
                         % (ref, sold, c.get("supplier_ref", "the supplier"), quoted))'''

NEW = '''    short, silent = [], []
    claimed = {}
    for c in cov:
        ref, sold, quoted = c.get("ref", "?"), c.get("qty_sold"), c.get("qty_quoted")
        if sold is None or quoted is None:
            silent.append(ref)
        elif quoted < sold:
            short.append("%s: selling %s, %s quoted %s"
                         % (ref, sold, c.get("supplier_ref", "the supplier"), quoted))
        else:
            key = c.get("supplier_ref")
            if key:
                claimed.setdefault(key, []).append((ref, quoted))
    # Riverside, 28/07. The Brocks Hill case is under-coverage - 2 sold, 1
    # quoted, GBP 2,723.49 with no quote behind it. This is the same money
    # problem from the other side: two lines each crediting the SAME quoted
    # units, so one of them is uncovered while the arithmetic still ties. It
    # was live here - both vents claimed qty_quoted 2 from a quotation whose
    # single position reads "Qty (2)", asserting four units against two sold -
    # and the rule passed, because it only ever asked whether quoted < sold.
    # Checked only where over-claim is possible: one supplier reference
    # credited on more than one line.
    totals = {}
    for q in (m.get("supplier_quotes") or []):
        if isinstance(q, dict) and q.get("qty_total") is not None:
            for k in (q.get("ref"), "%s %s" % (q.get("supplier", ""), q.get("ref", "")),
                      "%s %s" % (q.get("supplier", "").split()[0] if q.get("supplier") else "",
                                 q.get("ref", ""))):
                if k:
                    totals[str(k).strip()] = q["qty_total"]
    over, unbounded = [], []
    for key, lines in claimed.items():
        if len(lines) < 2:
            continue
        total = totals.get(str(key).strip())
        asked = sum(n for _, n in lines)
        if total is None:
            unbounded.append("%s is credited on %d lines (%s) with no qty_total recorded for it"
                             % (key, len(lines), ", ".join("%s x%s" % (r, n) for r, n in lines)))
        elif asked > total:
            try:
                over.append("%s: %d line(s) claim %s units between them but the quotation covers "
                            "%s" % (key, len(lines), asked, total))
            except Exception:
                pass
    if over:
        return result("supplier quote covers every unit sold", FAIL,
                      "The same quoted units are credited to more than one line, so at least one "
                      "line is not actually covered: " + "; ".join(over)
                      + ". The arithmetic ties either way - that is what makes it quiet.",
                      "Brocks Hill",
                      remedy="Split the quoted quantity across the lines it actually covers, or "
                             "get the missing units quoted.")'''

assert t.count(OLD) == 1, 'coverage rule anchor'
t = t.replace(OLD, NEW)

OLD2 = '''    if short:
        return result("supplier quote covers every unit sold", FAIL,'''
NEW2 = '''    if unbounded and not short and not silent:
        return result("supplier quote covers every unit sold", UNKNOWN,
                      "One supplier quotation is credited on several lines and nothing records "
                      "how many units it actually contains: " + "; ".join(unbounded)
                      + ". Without that, double-counting cannot be ruled out.",
                      "Brocks Hill",
                      remedy="Add 'qty_total' to that entry in 'supplier_quotes', counted off the "
                             "quotation rather than inferred.")
    if short:
        return result("supplier quote covers every unit sold", FAIL,'''
assert t.count(OLD2) == 1, 'short anchor'
t = t.replace(OLD2, NEW2)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print("\nrule extended to catch over-claim")

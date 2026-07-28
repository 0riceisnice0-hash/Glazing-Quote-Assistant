# -*- coding: utf-8 -*-
"""The third state: cost quoted with nothing sold against it.

Gordon Court ran the over-claim arm and found the mirror of Riverside's fault.
Mine over-stated `qty_quoted` across two lines. Theirs UNDER-stated it on one -
BSW quote two WE_14, the schedule has one, and because the manifest recorded
what we SELL in a field named for what the QUOTE CONTAINS, the surplus never
appeared. GBP 921.29 of quoted cost with nothing sold against it, sitting inside
the GBP 53,543.90 their workbook takes as BSW's PVC total.

Their diagnosis is the important part: TWO DIFFERENT FACTS WEARING ONE FIELD
NAME. `qty_quoted` can mean "how many the quotation contains for this reference"
or "how many of the quotation's units this line uses", and both jobs filled it
with the wrong one in opposite directions.

So the new arm deliberately does not depend on which reading anyone used. It
compares, per quotation:

    qty_total  - what the quotation contains, counted off the quotation
    sum of qty_sold across the lines credited to it

That single comparison catches BOTH directions:

    contained < sold    a shortfall - units sold with no quote behind them
    contained > sold    a surplus - quoted cost with nothing sold against it

Riverside reconciles exactly: 2 contained, 1 + 1 sold, zero surplus. Reported as
clean rather than left unsaid.

ASK rather than FAIL for the surplus, deliberately. Quoting more than you sell is
often correct - a supplier prices the whole schedule, or the client cuts scope
after the enquiry. It only becomes money when the build-up takes the quotation's
TOTAL rather than its lines, which is exactly what happened on Gordon Court and
is a question about how the cost was taken, not a defect visible in a manifest.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

# ------------------------------------------------------- document the field
OLD_DOC = '''    had no quote behind it. Reconciling a quote TOTAL is not the same as
    reconciling its QUANTITIES - the total ties either way."""'''
NEW_DOC = '''    had no quote behind it. Reconciling a quote TOTAL is not the same as
    reconciling its QUANTITIES - the total ties either way.

    WHAT `qty_quoted` MEANS, because Gordon Court found on 28/07 that it had been
    carrying two different facts on two jobs. It is HOW MANY OF THAT QUOTATION'S
    UNITS THIS LINE USES - an allocation. It is NOT "how many the quotation
    contains for this reference"; that belongs in `qty_total` on the quote. Both
    jobs filled it with the wrong one, in opposite directions: Riverside credited
    every line with the quotation's whole quantity, and Gordon Court recorded
    what they SELL, which hid a surplus.

    The surplus arm below deliberately does not depend on which reading was used
    - it compares `qty_total` against the sum of `qty_sold`, which is the same
    question asked in a way that cannot be answered two ways."""'''
assert t.count(OLD_DOC) == 1, 'docstring anchor'
t = t.replace(OLD_DOC, NEW_DOC)

# ------------------------------------------------------------ the new arm
OLD = '''    if unbounded and not short and not silent:'''
NEW = '''    # Gordon Court, 28/07 - the mirror of the over-claim above, and the third
    # state neither version of this rule reported. BSW quote two WE_14 and the
    # schedule has one, so GBP 921.29 of quoted cost had nothing sold against it
    # and sat inside the quotation total their workbook takes as cost. The
    # comparison below is deliberately independent of how `qty_quoted` was
    # read: what the quotation CONTAINS, against what is SOLD against it.
    sold_per_quote = {}
    for c in cov:
        key, sold = c.get("supplier_ref"), c.get("qty_sold")
        if key and isinstance(sold, (int, float)):
            sold_per_quote.setdefault(str(key).strip(), []).append(sold)
    surplus = []
    for key, sold_list in sold_per_quote.items():
        total = total_for(key)
        if total is None:
            continue
        try:
            gap = float(total) - float(sum(sold_list))
        except (TypeError, ValueError):
            continue
        if gap > 0:
            surplus.append("%s contains %s unit(s) and only %s are sold against it - %s quoted "
                           "unit(s) with nothing sold behind them"
                           % (key, total, sum(sold_list), int(gap) if gap == int(gap) else gap))
    if surplus and not short and not silent and not over:
        return result("supplier quote covers every unit sold", UNKNOWN,
                      "A supplier quotation contains more units than this job sells against it: "
                      + "; ".join(surplus)
                      + ". That is often right - a supplier prices the whole schedule, or scope "
                        "was cut after the enquiry. It becomes money only where the build-up "
                        "takes the quotation's TOTAL rather than its lines.",
                      "Brocks Hill",
                      remedy="Check how the cost was taken. If the build-up uses the quotation "
                             "total, the surplus units are in your cost with nothing sold against "
                             "them - ask the supplier what they picked up that you did not.")
    if unbounded and not short and not silent:'''
assert t.count(OLD) == 1, 'unbounded anchor'
t = t.replace(OLD, NEW)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('surplus arm added')

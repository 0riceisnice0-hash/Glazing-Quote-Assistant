# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### PRINTING ONE REAL ENTRY FOUND A DOUBLE-COUNT THE RULE WAS PASSING ON (28/07)"

SEC = u"""### THE THIRD STATE: COST QUOTED WITH NOTHING SOLD AGAINST IT (28/07)

Gordon Court ran the over-claim arm and found **the exact mirror of my fault, worth GBP 921.29.** BSW
quote **two** WE_14 and the schedule has **one**. Mine over-stated `qty_quoted` across two lines; theirs
under-stated it on one, **so the surplus never appeared** - and it sits inside the GBP 53,543.90 their
workbook takes as BSW's PVC cost.

**Their diagnosis is the part that generalises: TWO DIFFERENT FACTS WEARING ONE FIELD NAME.**
`qty_quoted` can mean *"how many the quotation contains for this reference"* or *"how many of the
quotation's units this line uses"*, and both jobs filled it with the wrong one **in opposite
directions**.

**So neither version of the rule could see either fault, and a third state existed that neither of us
was reporting.** Riverside's arm asked whether the lines claim more than the quotation holds. Theirs
needed the reverse. Both are the same question if you stop asking it per line:

    qty_total   what the quotation CONTAINS, counted off the quotation
    sum(qty_sold)  what is SOLD against it

    contained < sold   ->  a shortfall, units sold with no quote behind them
    contained > sold   ->  a surplus, quoted cost with nothing sold against it

**That single comparison catches both directions and is deliberately independent of how anybody read
`qty_quoted`** - which is the only way to make a check immune to a field that carries two meanings.
The field is now documented in the rule itself so nobody fills it with the other fact.

**Run on Riverside it reconciles exactly: 2 contained, 1 + 1 sold, zero surplus.** Reported as clean
rather than left unsaid.

**ASK rather than FAIL for the surplus, deliberately.** Quoting more than you sell is often correct - a
supplier prices the whole schedule, or scope is cut after the enquiry. **It only becomes money where the
build-up takes the quotation's TOTAL rather than its lines**, which is exactly what happened on Gordon
Court and is a question about how the cost was taken rather than a defect visible in a manifest. Their
own letter wording is the right register: *"if you have picked up something on the schedule that we have
not, we would very much like to know what."*

Five variants added from their real numbers - 118 against 117 fires, 44 against 44 passes, Riverside's
2 against 2 passes, and a shortfall still beats a surplus to the answer. **14/14.**

### AND THE PRINT-ONE-ENTRY LESSON CAUGHT ME A THIRD TIME, IN THE PATCH ITSELF (28/07)

The script that added the arm asserted against a docstring I had reconstructed from memory:

    mine     "Reconciling a quote TOTAL is not the same as reconciling its QUANTITIES - the
              total ties either way."
    actual   "had no quote behind it. Reconciling a quote TOTAL is not the same as
              reconciling its QUANTITIES - the total ties either way."

**Different line wrapping. The assertion failed, I printed the real text, and the anchor was obvious.**
That is three times in two turns that the same one-line defence has paid - once in the data, once in the
code written to check the data, and now in the patch that edits the code. **The assertion is what made
it cheap: a `replace` without one would have silently done nothing.**

### Their join failure, and the line I want to keep from it (28/07)

They supplied `qty_total` and the rule still asked, because:

    coverage.supplier_ref   "BSW QT252247"
    supplier_quotes.ref     "QT252247 PVC"

**Neither contains the other** - so my substring match, written an hour earlier to fix exactly this class
of failure on my own strings, failed on theirs. **A fix aimed at one pair of strings is not a fix for
joining.** Theirs is now canonicalised at the data end, which is the right place; the alternative is a
matcher that keeps growing special cases.

And the sentence worth keeping, because it is the answer to a question I ruled on last night:

> *"That is not editing data to make a rule go green. The rule was asking for a fact I had; the only
> defect was that my own two lists named the same object inconsistently. **The test is whether the change
> makes the manifest more true or just more agreeable** - and if you cannot say which, you are probably
> doing the second one."*

**That is a better test than the rule I gave them** - *"do not resolve someone else's rule by editing
your own data"* - because it says what to do rather than only what not to do.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

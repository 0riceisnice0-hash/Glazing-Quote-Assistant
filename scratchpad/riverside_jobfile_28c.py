# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### A PLUS'S CONDITIONS PUT PART B ON US, AND OUR OWN TERMS DISCLAIM IT TO THE CLIENT (28/07)"

SEC = u"""### MY SWEEP WAS DOCUMENT-DRIVEN, NOT CATEGORY-DRIVEN - AND IT COST TWO LIVE ITEMS (28/07)

Gordon Court found their ten-category exclusions list was **short by "building regulations"**, which on
a fire product is the category that matters most. Mine has a different fault of the same family, and
theirs is what exposed it.

**I READ A PLUS'S CONDITIONS AND DIFFED WHAT THEY SAY AGAINST CLAUSE 16.** That can only ever find
categories **A Plus chose to write about**. It cannot find a responsibility that neither document
mentions, and it cannot find a term whose consequence lands on us for a reason the term itself does not
state. **A document-driven sweep is a sample of the supplier's drafting priorities, not a sweep.**

So the list was built first, from what a glazing sub-contract actually allocates, and then probed
against both documents - **25 categories**, `scratchpad/riverside_category_sweep.py`. Two came back
live and unrecorded, and both are commercial rather than technical, which is why a compliance-shaped
read had missed them.

### THE PRICE IS NOT DIVISIBLE BY TWO, AND C2 COULD MAKE THAT MATTER (28/07)

> *"The Price is based on the materials quoted being ordered together, and in one phase. Orders for
> only part of the quote, or fabrication over multiple phases, may incur additional charges for paint
> surcharges, rolling set up charges, reduced material optimisation, delivery or increased fabrication
> costs. We strongly recommend that when placing all such orders, a re-price is requested."*

**Everything in this file has described the price as 2 x a unit rate** - 2,422.61 + 412.50 = 2,835.11,
x 2, + 160 install each. That is how the pricing document builds it and it is right as a build-up. **It
is wrong as a statement about what one vent costs.**

**C2 IS THE REASON IT IS LIVE.** If the second floor stairwell is vented at the roof rather than the
wall - which is what the note says and what that stairwell's lack of any wall opening suggests - we
would be ordering **ONE** of the two units from QT51518, and A Plus expressly reserve the right to
re-price a part order. So the exposure on C2 is not "we lose one unit at 2,995.11"; it is that number
**plus an unquantified re-price on the unit that remains**.

RFQ item 13 now asks what a single 1130 x 1530 vent to this specification would cost. **Asked before
the architect answers rather than after** - which is Gordon Court's C7(d) discipline applied here
rather than the other way round.

### THE ONE JOB IN THE BOOK THAT IS WAITING ON SOMEBODY ELSE, AND STORAGE HAS A THREE-DAY CLOCK (28/07)

> *"A Plus reserves the right to levy storage costs for all goods which remain uncollected 3 working
> days after first availability for collection/delivery."*
>
> *"Materials off Site: This quotation does not include for holding of materials off-site that have
> been properly purchased to conform with your projected commencement date and which becomes subject to
> delays to programme beyond our control. In such cases upon receipt of a suitable letter of indemnity
> we would require payment for such materials."*

Neither clause is unusual. **What makes them matter here is the one fact that defines this job: Adam is
holding the submission until PHDB return building-works costs, the sequence is openings formed ->
survey -> manufacture, and there is no programme date for forming the openings.** So a slip does not
just delay us - it starts a storage clock three working days after manufacture and converts the balance
into payment-before-delivery against a letter of indemnity.

**This is the first cost on this job that grows with the delay Adam has deliberately accepted**, and it
had not been written down anywhere. RFQ item 14 asks how the three days run in practice and whether
there is a normal holding arrangement; RRR question 11 now gives the programme date a second reason
beyond the price hold.

### Their "available on request" check, run here - and it comes back clean (28/07)

Gordon Court's one-liner: **grep supplier quotations for "available on request", "subject to our
standard", "terms of sale" and "conditions of sale".** Run on QT51518:

    available on request       0
    on request                 0
    subject to our standard    0
    conditions of sale         0
    standard terms             0
    terms of sale              4   - all four the named V.01.2 / V.01 already recorded

**No further incorporation. Reported clean**, because a check that only ever fires is not one anybody
trusts. One detail worth keeping: the payment basis itself points into the unheld document -
*"Deposit and cleared Funds Prior to delivery on first order (see... Terms of Sale Revision V.01.2 -
08.01.2018 for more information)"*. A Plus are an established supplier here rather than a first order,
so it is recorded and not raised.

### Their case is worse than mine, and it found a defect in my own rule (28/07)

BSW's four quotations read *"Orders are subject to acceptance and terms and conditions of sale,
available on request"* - **no title, no revision, no date**. Gordon Court's point: with mine, a request
has a subject line; with theirs, you cannot say which version you have not read.

**`check_incorporated_terms_held` shipped last turn had no branch for that shape, and got it backwards
in two ways:**

1. **It graded the worse case as the lesser one.** An unnamed incorporation fell into the
   *"cannot tell whether the incorporated terms are held"* bucket, which reads as a manifest-filling
   problem. It is not - we can tell perfectly well: we hold nothing, and cannot name what is missing.
2. **Its remedy could not be carried out.** *"Say WHICH terms are incorporated"* asks the estimator for
   a fact only the supplier holds, when the quotation names nothing. **A remedy nobody can act on is
   the same family of defect as an assertion made from a value the rule did not understand** - the
   thing that broke `check_free_delivery_threshold` two turns ago.

Fixed: unnamed incorporations get their own bucket, are reported **first**, and carry their own remedy -
ask for the title, revision and date where the quote names one, and for whatever the quotation refers
to where it does not. Six variants added, **35/35 persisted**.

**The rule was 29-variants-tested before it shipped and still had a hole, because every one of the 29
was written against the shape on MY quote.** Variant count is not coverage; variant *diversity* is, and
the diversity only arrived when the rule met another job's data.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

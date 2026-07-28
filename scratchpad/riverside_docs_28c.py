# -*- coding: utf-8 -*-
"""AI.md rules, MARY-HANDOVER.md row append, HANDOVER.md record."""
import io

AI_RULE = u"""**Build the category list before you read the document.** Gordon Court's ten-category exclusions sweep
was short by "building regulations" - the category that matters most on the fire and smoke products this
business sells. Riverside's fault was the same family and larger: its back-to-back sweep was
**document-driven**, reading A Plus's conditions and diffing what they said against clause 16. That can
only ever surface categories the supplier chose to write about. It cannot surface a responsibility
neither document mentions, and it cannot surface a clause whose consequence lands on you for a reason
the clause never states. **A document-driven sweep is a sample of the supplier's drafting priorities.**
Rebuilt as 25 categories listed first, from what a glazing sub-contract actually allocates, it returned
two live items that a compliance-shaped read had walked straight past - both commercial rather than
technical. `scratchpad/riverside_category_sweep.py`.

Two findings from that rebuild, both worth running on any job:

- **If any open question could REDUCE the order, check whether the supplier priced on the whole.**
  A Plus price on the basis that materials are "ordered together, and in one phase" and reserve the
  right to re-price a part order. Riverside's price had been described everywhere as 2 x a unit rate -
  right as a build-up, wrong as a statement of what one vent costs - while its largest open question
  (wall vent or roof vent) could halve the order. The exposure is the lost unit **plus an unquantified
  re-price on the unit that stays**. Quantity-break and one-phase clauses are common; they turn a scope
  reduction into two costs, not one.
- **If your job is waiting on somebody else's programme, read the supplier's storage and
  off-site-materials clauses before agreeing to wait.** A Plus levy storage on goods uncollected more
  than three working days after first availability, and exclude holding materials off-site through a
  programme slip - requiring payment for the materials against a letter of indemnity. Neither clause is
  unusual. What made them bite on Riverside is that the submission is deliberately held pending another
  party's costs with no programme date, so a slip starts a three-day clock and converts the balance into
  payment-before-delivery. **The first cost on that job that grows with a delay the business chose to
  accept** - and the clause pricing it is never in the section you were reading.

**Variant count is not coverage; variant diversity is.** `check_incorporated_terms_held` shipped with 29
variants written before it, and still had a hole: every one of the 29 was written against the shape on
the quote that produced the rule. Gordon Court populated the field on their job and exposed the missing
branch immediately - BSW's quotations incorporate terms "available on request", with no title, no
revision and no date. The rule **graded that worse case as the lesser one** (an unnamed incorporation
fell into "cannot tell whether they are held", which reads as a form-filling problem when the answer is
in fact known: nothing is held and the missing document cannot even be named) and **its remedy could not
be carried out** - "say WHICH terms are incorporated" asks the estimator for a fact only the supplier
holds. **A remedy nobody can act on is the same family of defect as an assertion made from a value the
rule did not understand.** Fixed; unnamed incorporations get their own bucket, are reported first, and
ask for title, revision and date. **A rule that has only ever run on the job that produced it is still a
one-case rule however many variants sit under it** - which is an argument for populating each other's
manifest fields early rather than at the end.

**A cross-reference is a claim, and it goes stale when you edit around it.** Gordon Court renumbered a
letter item from D3 to D4 and left the letter's own header describing the wrong item. Riverside added two
RFQ items and left the covering note to Adam saying "Twelve items". After any renumbering or insertion,
grep the whole document set for "item N", "question N" and the written-out counts.

## Development Rules For Future Agents"""

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, AI_RULE))
print('AI.md ok')

ROW_ADD = (
    u" **28/07 LATER - MY SWEEP WAS DOCUMENT-DRIVEN, AND IT COST TWO LIVE COMMERCIAL ITEMS.** Gordon"
    u" Court's ten-category list was short by *building regulations*; mine had the larger fault of"
    u" method - reading A Plus's conditions and diffing them against clause 16 can only find categories"
    u" **A Plus chose to write about**. Rebuilt as **25 categories listed before reading either"
    u" document**. Two live and unrecorded, both commercial rather than technical, which is why a"
    u" compliance-shaped read missed them. **(1) THE PRICE IS NOT DIVISIBLE BY TWO.** QT51518: the"
    u" price *\"is based on the materials quoted being ordered together, and in one phase\"*, a part"
    u" order *\"may incur additional charges\"* and *\"a re-price is requested\"*. Every description of"
    u" this price has been **2 x a unit rate** - right as a build-up, wrong as what one vent costs -"
    u" and **C2 could halve the order**: if the second floor stairwell is vented at the roof we buy ONE"
    u" unit and the survivor is expressly re-priceable. **C2's exposure is the lost unit PLUS an"
    u" unquantified re-price on the one that stays.** RFQ item 13 asks the single-vent price, before"
    u" the architect answers rather than after. **(2) STORAGE HAS A THREE-WORKING-DAY CLOCK.** A Plus"
    u" levy storage on goods uncollected 3 working days after first availability and exclude holding"
    u" materials off-site through a programme slip, wanting payment against a letter of indemnity."
    u" Neither clause is unusual - **what makes them bite is the defining fact of this job**: the"
    u" submission is deliberately held until PHDB report, the sequence is openings formed -> survey ->"
    u" manufacture, and there is **no programme date**. **The first cost on this job that grows with a"
    u" delay we chose to accept.** RFQ item 14 and a second reason under RRR question 11. Not"
    u" quantified - no rate stated, none invented. **Their \"available on request\" grep run here comes"
    u" back CLEAN** - zero hits for that family on QT51518. **And their BSW data found a defect in my"
    u" own new rule**: an unnamed incorporation (no title, revision or date) was graded as the LESSER"
    u" case and given a remedy the estimator cannot carry out. Fixed, six variants, **35/35**. **That"
    u" rule had 29 variants written before it shipped and still had a hole, because all 29 were written"
    u" against the shape on my own quote - variant count is not coverage, variant diversity is.** RFQ"
    u" now **14 items**; the covering note's stale \"Twelve items\" caught by Gordon Court's"
    u" cross-reference lesson. Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22,"
    u" unissued, nothing sent.** |")

p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW_ADD
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, row %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a document-driven sweep is not a sweep

Gordon Court found their ten-category exclusions list was short by **building regulations** - on a fire
product, the category that matters most. Looking for the same fault here found a larger one: **the
back-to-back sweep run last turn was DOCUMENT-driven.** It read A Plus's conditions and diffed what they
said against clause 16, so it could only ever surface categories A Plus chose to write about. It could
not surface a responsibility neither document mentions, nor a clause whose consequence lands on us for a
reason the clause never states. **A document-driven sweep is a sample of the supplier's drafting
priorities.**

Rebuilt as **25 categories listed before reading either document**
(`scratchpad/riverside_category_sweep.py`). Two came back live and unrecorded, and both are commercial
rather than technical - which is exactly why a compliance-shaped read had walked past them.

**1. The price is not divisible by two.** QT51518: *"The Price is based on the materials quoted being
ordered together, and in one phase. Orders for only part of the quote... may incur additional charges...
We strongly recommend that when placing all such orders, a re-price is requested."* Every description of
this price - job file, hub, handover - has been **2 x a unit rate**. That is correct as a build-up and
wrong as a statement of what one vent costs. **It is live because the largest open question could halve
the order**: if the second floor stairwell is vented at the roof rather than the wall, we order ONE unit
and the survivor is expressly subject to re-price. So C2's exposure is not "lose one unit at
GBP 2,995.11" - it is that **plus an unquantified re-price on the unit that stays**. RFQ item 13 asks
what a single vent costs, **before the architect answers rather than after**.

**2. Storage has a three-working-day clock, on the one job in the book that is waiting on somebody
else.** *"A Plus reserves the right to levy storage costs for all goods which remain uncollected 3
working days after first availability"*, and materials held off-site through a programme slip are
excluded, with payment for the materials required against a letter of indemnity. **Neither clause is
unusual.** What makes them bite is the defining fact of this job: the submission is deliberately held
until PHDB return building-works costs, the sequence is openings formed -> survey -> manufacture, and
there is no programme date. A slip starts the clock three working days after manufacture and converts
the balance into payment-before-delivery. **The first cost on this job that grows with a delay the
business chose to accept**, and it was written down nowhere. Not quantified - no rate stated on the
quote and none invented. RFQ item 14, and a second reason under RRR question 11 for giving a date.

**Their "available on request" grep, run here, comes back clean** - zero hits on QT51518 for *available
on request*, *on request*, *subject to our standard*, *conditions of sale*, *standard terms* or *as
amended*; the only incorporations are the two named revisions already recorded. Reported clean, because
a check that only ever fires is not one anybody trusts.

**And their data found a defect in `check_incorporated_terms_held`, one turn after it shipped.** BSW's
four quotations incorporate terms *"available on request"* - **no title, no revision, no date**. The
rule had no branch for that shape and got it backwards twice: it **graded the worse case as the lesser
one** (unnamed fell into "cannot tell whether they are held", which reads as a form-filling problem when
the answer is known - nothing is held, and the missing document cannot even be named), and **its remedy
could not be carried out**, because *"say WHICH terms are incorporated"* asks the estimator for a fact
only the supplier holds. **A remedy nobody can act on is the same family of defect as an assertion made
from a value the rule did not understand.** Fixed: unnamed incorporations get their own bucket, are
reported first, and ask for title, revision and date where a quote names one and for whatever it refers
to where it does not. Six variants added; **35/35**.

**The uncomfortable part, recorded deliberately: that rule shipped with 29 variants written before it
and still had a hole, because every one of the 29 was written against the shape on this job's own
quote. Variant count is not coverage; variant diversity is** - and the diversity only arrived when the
rule met another job's data. A rule that has only ever run on the job that produced it is still a
one-case rule however many variants sit under it.

**Gordon Court's cross-reference lesson caught something here immediately**: adding two RFQ items left
the covering note to Adam saying "Twelve items". A cross-reference is a claim and it goes stale when you
edit around it; the whole document set is now grepped for item and question numbers after any
renumbering.

RFQ now 14 items, RRR letter 11, covering note updated. Checks **0 failed, 4 questions**. Position
unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""

p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
marker = u'\n\n## Next Best Work'
i = t.rindex(marker)
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

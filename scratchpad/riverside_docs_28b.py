# -*- coding: utf-8 -*-
"""AI.md rule, MARY-HANDOVER.md row append, HANDOVER.md record."""
import io

# ---------------------------------------------------------------- AI.md
AI_RULE = u"""**Read your supplier's conditions for the word "Customer" and list what it makes you responsible for;
read your own terms for what you have disclaimed to the client; the gap between those two lists is your
unbacked-off risk.** Gordon Court found AFS warranting drawing fitness-for-purpose downstream while
Fenster's clause 16 disclaims it upstream. Riverside ran it on A Plus and found the same shape on
Part B: their Product Performance clause makes Building Regulations compliance the Customer's and
expressly does not warrant that any product complies, while clause 16 disclaims regulatory strategy to
the client's professional team. **Neither document is wrong on its own** - one is a normal design
carve-out, the other a normal supplier disclaimer - which is why five readings of the quote did not
surface it. The exposure exists only between two unremarkable paragraphs.

Four things that make this check pay:

- **Weigh it by what the product is FOR.** Part B is not an incidental attribute of an AOV smoke vent;
  it is the entire function. A responsibility gap on the one regulation a product exists to satisfy is
  worth more than a gap on five peripheral ones.
- **Look for the door in the clause.** A Plus's disclaimer is conditional - *"unless where expressly
  stated to the contrary by the Supplier"* - so it can be discharged for the price of one sentence
  before an order. Riverside's RFQ had already asked for the aerodynamic free area, but as an answer
  rather than a quotation entry, and the clause turns on what the Supplier expressly states. **Ask for
  performance figures ON the revised quotation, not in a reply.** Pre-order it is a line; post-order it
  is a variation.
- **Report the categories that come back clean.** Measurement was consistent both ways on Riverside
  (clause 16 expressly retains measurement verification) and so was the RRO 2005 maintenance duty.
  **Overclaiming a contractual conflict is worse than missing one.**
- **A supplier quote with no exclusions schedule at all is an UNDEFINED result, not a clean one.**
  Gordon Court recorded BSW's silence on all ten categories that way rather than as a pass.

**An incorporation by reference is worse than no terms at all.** A quote with no terms is a gap you can
see; a quote that says "our Terms of Sale Revision V.01.2 apply" reads as though the terms are settled
and hides that you cannot state them. A Plus's QT51518 incorporates two such documents, including the
one holding the DEFINITION of "Customer" that every responsibility clause turns on, and neither has ever
been held at Fenster - six files across the whole Commercial archive have "Terms of Sale" in the name
and all six are the same Advisory Notes summary. Now `check_incorporated_terms_held` in
`scripts/mary_checks.py`.

**Familiarity with a supplier quote is the reason to re-read it, not the reason not to.** Page 3 of
QT51518 - the whole responsibility page - had never been read after five turns on that quote, because
every previous read was for prices, apertures or product notes. If a job file has zero occurrences of
*Part B*, *Terms of Sale*, *windload* or *bracket* against a quote you consider well understood, you
have read it for one purpose only.

**And when a rule's test suite passes first time, treat that as a reason for suspicion rather than
confidence** - a suite written minutes after the implementation may be testing the code's own
assumptions back at it. `check_incorporated_terms_held` passed 17/17, so twelve more variants were
written from shapes the code was not written against (uppercase and padded truthy values, `held` as an
empty list or a dict or `2`, the field as an int, a tuple of entries, a numeric document, `[None]`).
All twelve held; 29/29 persisted into `--selftest`.

## Development Rules For Future Agents"""

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, AI_RULE))
print('AI.md ok')

# ------------------------------------------------------- MARY-HANDOVER.md row
ROW_ADD = (
    u" **28/07 - WE DISCLAIMED PART B TO THE CLIENT AND ACCEPTED IT FROM THE SUPPLIER, ON A PRODUCT"
    u" WHOSE ONLY FUNCTION IS PART B.** Gordon Court's generalised check run on A Plus: their Product"
    u" Performance clause makes it *\"the responsibility of the CUSTOMER to ensure all building"
    u" regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N'...) are adhered to\"* and states *\"the Supplier"
    u" does not warrant or represent that any Product supplied shall comply... unless where expressly"
    u" stated to the contrary by the Supplier\"*; our clause 16 disclaims **regulatory strategy** and"
    u" relies on the client's team. **Neither document is wrong on its own** - the exposure lives only"
    u" between two unremarkable paragraphs, which is why five readings missed it. **It bites on the"
    u" item already open**: if the 1 m2 is aerodynamic, 1.30 m2 geometric gives ~0.78-0.81 m2 and the"
    u" shortfall is ours. **The remedy is free and pre-order** - the clause is conditional, so RFQ"
    u" items 1 and 4 now ask A Plus to state the aerodynamic free area, the EN 12101-2 class and the"
    u" Uw **ON the revised quotation** rather than by reply, because the clause turns on what the"
    u" Supplier expressly states. **What it cost to find: page 3 of QT51518 had never been read** -"
    u" the job file held zero occurrences of *Part B*, *Terms of Sale*, *windload* or *bracket* after"
    u" five turns on that quote. **Three more off the same pages:** (1) *\"the output free area values"
    u" do not allow for any obstructions, side walls, reveals or neighbouring vents\"* - the 1.30 m2 is"
    u" a **bare-vent** figure and both vents sit in a reveal on a 155mm subcill, **the first thing"
    u" found that erodes the geometric margin itself**; (2) a **1200Pa** design windload assumed,"
    u" their calculations disclaimed, and the BS 6399-2 check plus bracket/spigot calculations put on"
    u" us - with **no structural engineer named on any drawing**, nobody is appointed to either;"
    u" (3) the quote **incorporates a Terms of Sale we have never held** (V.01.2 - 08.01.2018, plus"
    u" the V.01 - 03.11.2017 that DEFINES \"Customer\") - six files in the whole Commercial archive"
    u" have \"Terms of Sale\" in the name and **all six are the same Advisory Notes summary**. Measurement"
    u" and RRO 2005 maintenance checked in the same pass and are **consistent both ways - reported as"
    u" clean**. RFQ now **12 items**, RRR question 5 extended, covering note to Adam updated. New rule"
    u" **`check_incorporated_terms_held`** (17th), **29 variants written BEFORE it shipped**; it passed"
    u" 17/17 first time, which was treated as a reason for suspicion, so twelve more came from shapes"
    u" the code was not written against - all held. **And Grange Hill's oldest rule caught me**: prose"
    u" in a `treatment` field returned *1 FAILED - do not issue this quote*, correctly. Checks **0"
    u" failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")

p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW_ADD
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, row %d chars' % len(lines[121]))

# ---------------------------------------------------------- HANDOVER.md record
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the back-to-back gap on Part B

**Gordon Court's generalised check, run on A Plus:** read the supplier's conditions for the word
"Customer" and list what it makes you responsible for; read your own terms for what you have disclaimed
to the client; the gap between the two lists is your unbacked-off risk.

    A Plus QT51518, Product Performance:  "It is the responsibility of the CUSTOMER to ensure all
                                           building regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N'...)
                                           are adhered to. The Supplier does not warrant or represent
                                           that any Product supplied shall comply... unless where
                                           expressly stated to the contrary by the Supplier."
    Fenster, clause 16:                    not responsible for "regulatory strategy"; relies on the
                                           client's professional team.

**Neither document is wrong on its own** - one is a normal design-responsibility carve-out, the other a
normal supplier disclaimer. The exposure exists only in the space between them, which is why five
readings of this quotation did not surface it. **What makes it sharp: Part B is not an incidental
attribute of an AOV smoke vent, it is the entire function of the product** - so the one regulation the
thing exists to satisfy is the one disclaimed upstream and accepted downstream. It bites on the item
already top of the list: if the 1 m2 is aerodynamic, 1.30 m2 geometric gives about 0.78-0.81 m2, and
under their clause that shortfall is ours because they never warranted it.

**The remedy is free and pre-order, because the clause is conditional.** *"Unless where expressly
stated to the contrary by the Supplier."* The RFQ already asked for the aerodynamic figure - but as an
answer, not as a quotation entry, and the clause turns on what the Supplier expressly states. Items 1
and 4 now ask for the aerodynamic free area, the EN 12101-2 classification and the whole-window Uw **on
the revised quotation itself**. A line before an order; a variation after one.

**What it cost to find, which is the transferable part: page 3 of QT51518 had never been read.** The
job file held zero occurrences of *Part B*, *building regulation*, *Terms of Sale*, *windload*,
*BS 6399* or *bracket* before this turn - five turns on that quote, every one of them for prices,
apertures or product notes, none for its allocation of responsibility. **Familiarity with a supplier
quote is the reason to re-read it, not the reason not to.**

**Two categories came back clean and are reported as clean** - measurement is consistent both ways
(clause 16 expressly retains measurement verification, and the 1130 x 1530 came from our own enquiry),
and the RRO 2005 maintenance duty genuinely sits with the occupier. Overclaiming a contractual conflict
is worse than missing one.

**Three more findings off the same two pages:**

1. *"The output free area values do not allow for any obstructions, side walls, reveals or neighbouring
   vents."* The 1.30 m2 geometric is a **bare-vent** figure, and both vents sit in a reveal in existing
   masonry on a 155mm subcill. **The first thing found that erodes the geometric margin itself** - the
   30% headroom over 1 m2 has been treated as comfortable and it is headroom against an unobstructed
   number. Not quantified, not guessed at; RFQ item 1.
2. A **1200Pa** design windload assumed unless otherwise stated, the calculations expressly not to be
   relied on, and the BS 6399-2 check plus the bracket/spigot calculations put on the Customer -
   against a clause 16 that limits us to measurement, supply and installation, and **no structural
   engineer named on any of the six drawings**. Neither the check nor the fixing design is anybody's.
   RFQ item 12 and RRR question 5.
3. The quotation **incorporates a Terms of Sale we have never held** - Revision V.01.2 (08.01.2018),
   plus the V.01 (03.11.2017) that holds the DEFINITION of "Customer" every clause above turns on. Six
   files across the whole Commercial archive have "Terms of Sale" in the name and **all six are the
   same `Quotation Advisory Notes_Jan2019` summary**; diffed against QT51518's advisory pages at 0.75
   similarity, the only substantive change in seven years being frames splitting at 5m rather than 4m.
   **An incorporation by reference is worse than no terms at all**: no terms is a gap you can see, an
   incorporation reads as settled and hides that you cannot state it. RFQ item 11.

**New rule, `check_incorporated_terms_held`** - seventeenth in `RULES`, ASK when a supplier quote
incorporates a document we do not hold, NA when nothing is incorporated, UNKNOWN rather than an
assertion on any value it does not understand. **Its variants were written before it shipped**, 17 to
start with eight negatives. **It passed 17/17 first time, which was treated as a reason for suspicion
rather than confidence** - a suite written minutes after the implementation may be testing the code's
own assumptions back at it - so twelve more were written from shapes the code was not written against.
All twelve held; 29/29 persisted into `--selftest`.

**And Grange Hill's oldest rule caught this chat an hour later:** narrative prose written into a
`treatment` field instead of `priced`/`excluded`/`provisional` returned *1 FAILED - do not issue this
quote*. Correctly. Fixed; back to **0 failed, 4 questions**.

RFQ now 12 items, RRR letter 11, covering note to Adam updated. Position unchanged:
**GBP 5,990.22 ex VAT, unissued, nothing sent.** A Plus RFQ due by 26/08.
"""

p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
marker = u'\n\n## Next Best Work'
i = t.rindex(marker)
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

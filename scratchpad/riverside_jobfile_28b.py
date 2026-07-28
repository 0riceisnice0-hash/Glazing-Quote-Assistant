# -*- coding: utf-8 -*-
"""Insert this turn's sections into data/jobs/riverside.md.

Written to a file rather than piped through a heredoc: the section text is full
of backticks and quotes and the shell kept eating it.
"""
import io

P = 'data/jobs/riverside.md'
ANCHOR = '### I shipped a detector validated against one positive case (28/07)'

SEC = u"""### A PLUS'S CONDITIONS PUT PART B ON US, AND OUR OWN TERMS DISCLAIM IT TO THE CLIENT (28/07)

Gordon Court's generalised check, run here: **read your supplier's conditions for the word
"Customer" and list what it makes you responsible for; read your own terms for what you have
disclaimed to the client; the gap between those two lists is your unbacked-off risk.**

**First, what it cost to find: page 3 of QT51518 is a page of this quote I had never read.**
The job file had zero occurrences of *Part B*, *building regulation*, *Terms of Sale*, *windload*,
*BS 6399*, *bracket*, *interpretation* or *obstruction* before tonight. I have read this quotation
for its prices, its apertures and its AOV notes across five turns and never once for its
allocation of responsibility.

| A Plus QT51518 makes the CUSTOMER (us) responsible for | our clause 16 position | back to back? |
|---|---|---|
| the quote is "the interpretation by the Supplier of the design documents"; "the Customers responsibility to ensure that all items and interpretations are as desired" | cl.16 **retains** measurement verification | **measurement yes**, interpretation wider |
| "all design responsibility remains with the Customer and our calculations are not to be relied on for any design purposes whatsoever" | cl.16 **disclaims** design intent and architectural suitability | **NO** |
| windload and profile suitability; recommend the Customer do their own BS 6399-2 check; they assume **1200Pa unless otherwise stated** | nobody - **no structural engineer named on any of the six drawings** | **NO** |
| "full structural calculations on all brackets/spigots supplied by A Plus" | same | **NO** |
| **"ensure all building regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N'...) are adhered to. The Supplier does not warrant or represent that any Product supplied shall comply"** | cl.16 **disclaims regulatory strategy** | **NO - and this is the one** |
| front page: "It is your responsibility to ensure your installation complies... make sure it is clear on all quote requests and all orders what performance is required" | our enquiry asked for "1.5m2 free area" **with no basis stated** | the failure the clause is written for |
| acceptance box: "A Plus are not responsible for any variations or different interpretations made between my enquiry and the quote above" | - | the moment the transfer completes |
| "Unless otherwise stated, windows and doors will have a U-Value **no better than 1.8**" | 1.6 still open (RRR q7) | ours if we do not state it |
| Maintenance - RRO 2005 duty on "the occupier or agent" | the building owner's | **YES - clean, no gap** |
| Terms of Sale Rev V.01.2 (08.01.2018) incorporated; **definitions** from Rev V.01 (03.11.2017) | - | **we hold neither** |

**THE HEADLINE, AND IT IS SHARPER HERE THAN ON GORDON COURT'S JOB.** Theirs was fitness-for-purpose
of drawings. Mine is Part B - **and Part B is not an incidental attribute of an AOV smoke vent, it is
the entire function of the product.** So the one regulation this thing exists to satisfy is the one we
have disclaimed upstream to RRR and accepted downstream from A Plus. **Neither document is wrong on
its own.** Ours is a normal design-responsibility carve-out; theirs is a normal supplier disclaimer.
The exposure lives only in the space between them, which is why five readings of the quote did not
surface it.

**AND IT BITES ON THE ONE QUESTION THAT IS STILL OPEN.** If the 1m2 is aerodynamic, 1.30m2 geometric
delivers roughly 0.78-0.81m2 and does not satisfy the drawing. Under A Plus's Product Performance
clause that shortfall is ours, because they never warranted it. Under clause 16 we told the client we
rely on their team for regulatory strategy. **C0/C1 was already the most important open item; it is
now also the item where the contractual gap sits.**

**BUT THE CLAUSE HAS A DOOR IN IT, AND THAT IS THE USEFUL HALF.** It reads *"unless where expressly
stated to the contrary by the Supplier"*. If A Plus **state on the quotation** an aerodynamic free
area and the EN 12101-2 classification, the warranty exists. RFQ item 1 already asked for the
aerodynamic figure - **but as an answer, not as a quotation entry**, and the clause turns on what the
Supplier expressly states, not on what an estimator writes in an email. Item 1 and item 4 now ask for
both figures **on the revised quotation**. That is a free change to a letter nobody has sent.

**BE PRECISE ABOUT WHAT IS *NOT* A GAP**, because overclaiming a contractual conflict is worse than
missing one:

- **Measurement is consistent both ways.** Clause 16 expressly retains measurement verification, and
  the 1130 x 1530 came from our own enquiry. We own it upstream and downstream. No issue.
- **Maintenance is consistent.** The RRO 2005 duty genuinely sits with the occupier or agent.
- **Delivery is not a responsibility gap** - it is priced, provisional, and already recorded.

### Three things pages 3 and 5 carry that were not in this file at all (28/07)

1. **"The output free area values do not allow for any obstructions, side walls, reveals or
   neighbouring vents."** The 1.30m2 geometric is a **bare-vent** figure. Both vents sit in a reveal
   in existing masonry on a 155mm subcill. **This is the first thing found that could erode the
   geometric margin itself** - until now the 30% headroom has been treated as comfortable, and it is
   headroom against an unobstructed number. Not quantified and not guessed at; added to RFQ item 1.
2. **A design windload of 1200Pa assumed unless otherwise stated**, calculations expressly not to be
   relied on, and the BS 6399-2 check plus the bracket/spigot calculations put on us. On a second
   floor elevation, **nobody is appointed to do either.** RFQ item 12 asks A Plus to confirm 1200Pa
   and what fixings are included; RRR question 5 now asks who is carrying the check.
3. **"Actuators to EN 12101-2 are not formally weather tested."** Recorded, not raised: these vents
   are the only opening in those stairwells and nothing in the pack sets a weather-tightness
   requirement against them. Considered and declined so nobody re-derives it.

### The Terms of Sale has never been held here, on any job, in seven years (28/07)

QT51518 incorporates the *"A Plus Windows & Doors Limited Terms of Sale Revision V.01.2 - 08.01.2018"*
and takes its **definitions** - including who the "Customer" is in every clause above - from
*"Revision V.01 - 03.11.2017"*. Neither is attached.

**Checked the archive rather than assuming, because a failed search is not evidence of absence.** Six
files in the whole Commercial archive have "Terms of Sale" in the name - Bradford Watts, Elkins,
HouseUP, Prince Build, Stepnell, Conamar - and **all six are the same `Quotation Advisory
Notes_Jan2019` PDF**, which is the summary, not the terms. Diffed that 2019 file against QT51518's
advisory pages: 0.75 sentence similarity, and the only substantive change in seven years is frames
splitting at 5m rather than 4m. So the summary is stable and **the document it summarises has never
been read here**.

**This is not the same as a quote with no terms at all - that is a gap you can see.** An incorporation
by reference reads as though the terms are settled and hides that you cannot say what they are. RFQ
item 11 asks for both documents.

### New rule: `check_incorporated_terms_held` - and its tests were written first (28/07)

Registered as the seventeenth rule. `'incorporated_terms': [{supplier, ref, document, held}]` - ASK
when a supplier quote incorporates a document we do not hold, NA when nothing is incorporated by
reference, and UNKNOWN rather than an assertion on any value it does not understand.

**The variants were written BEFORE the rule shipped**, which is the whole point of this week's lesson
- 17 to start, eight of them negatives that must stay silent, including the three shapes that crash a
rule rather than answer it: a dict where a list belongs, a bare string, a non-dict entry.

**It passed 17/17 first time, and that is exactly when to be suspicious** - a suite written minutes
after the implementation may be testing the code's own assumptions back at it. So twelve more were
written from shapes the implementation was not written against: `"TRUE"`, `" yes "` padded, `held` as
an empty list, as a dict, as `2`, as `"n/a"`, the field as an int, a tuple of entries, a numeric
document, `[None]`. All twelve held. **29/29 persisted** into `--selftest`; it now reads
`incorporated terms  29/29 terms variants behave as intended`.

It fires on the live manifest. Riverside is now **0 failed, 4 questions**.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars' % (len(raw), len(out)))

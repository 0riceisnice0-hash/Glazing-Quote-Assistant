# Riverside House - AOV Smoke Vents (RRR Group)

Chat key `riverside`. Opened 27/07/2026 for a job that already existed.
**Watch out:** the archive holds two unrelated Riversides - "Riverside Way" (Bradford Watts) and
"Riverside Close" (Neil Douglas). This chat matches on `riverside`. Check the client before acting on
anything that lands here. RRR Group's other live job is Towcester Vale Local Centre, filed under
`Commercial\2. Projects\RRR-Group\Towcester Vale Local Centre` - do not mix them (its A Plus quote
QT51516 is a different job, though it is a useful comparator - see FREE AREA below).

## Where it stands (as at 27/07/2026)

**Priced and drawn. Not issued.** Adam is holding the submission until PHDB return costs for the
building works. No deadline.

| | |
|---|---|
| Client | RRR Group Limited (Adam's instruction 27/07 13:47, trusted, cc Commercial) |
| Deadline | **None client-stated.** The hub's 26/08 is A Plus QT51518's expiry, not a client date - `deadline_basis` says so. Adam: no urgency, gated by PHDB's building-works costs. |
| Site | Riverside House, 44 Wedgewood Street, Fairford Leys, Aylesbury, Bucks HP19 7HL |
| Planning ref | 24/02303/PAPCR. Planning applicant on the location plan is **Elderfern Ltd**, not RRR - RRR's associated companies are Primrose Property, Elderfern and SRP Investments |
| Scope | 2no bottom-hung AOV smoke vents, one per stairwell, at each stairwell's top storey |
| **Fenster sell** | **GBP 5,990.22 ex VAT** supply and fit (GBP 7,188.26 inc VAT) |
| Supplier cost | A Plus **QT51518**, 27/07/2026, **GBP 4,845.22 net** ex VAT, supply only delivered, glazed |
| Validity | A Plus to **26/08/2026**. Our house validity is 30 days from issue. |

### How the price is built

Frames 4,662.15 + glass 171.31 + energy surcharge 11.76 = 4,845.22 for the pair (ties exactly to the
quote's stated Total - **no extras block**, the Gordon Court element-lines-vs-total test passes).
Per unit 2,422.61 = **GBP 1,401.24/m2** over 1.729 m2.

Code **MAW** (1.729 m2 sits in the 1.5-3 m2 band; SM5 used SAW at 1.44 and MAW at 2.09, and
`band_of()` breaks at 1.5). Template adder 550 x 75% = 412.50. Labour 160/unit.

    unit rate  2,422.61 + 412.50 = 2,835.11
    items      2,835.11 x 2      = 5,670.22
    install    160 x 2           =   320.00
    TOTAL                          5,990.22 ex VAT
    optional external mastic 10.64 lm @ GBP 5 = 53.20

Engine and template agree to the penny (`mary_pricing.price_line("MAW", 1130, 1530, qty=2,
supply_rate=1401.24)` - note `supply_rate` is **GBP/m2**, not a unit price).

### Files

**Deliverables (done):**
- `outputs\Riverside House - Fenster Pricing Document (house format).xlsx`
- `outputs\Riverside House - AOV Smoke Vent Drawings.pdf` (2 sheets, Rev A)

**Ready to send - nothing has been sent, and Mary cannot send any of it:**
- `outputs\Riverside House - Covering note to Adam (draft).txt` - the reminder he asked for
- `outputs\Riverside House - RFQ to A Plus (draft, send by 26-08).txt` - 9 items, ours to fix
- `outputs\Riverside House - Questions to RRR (draft).txt` - design questions, theirs to answer

**Working / superseded:**
- `outputs\Riverside House - A Plus requote brief (for Gintare).txt` - the full working brief the
  two letters were split out of; keep as the reasoning behind them
- `outputs\Riverside House - Reply to Adam (SUPERSEDED 27-07, do not send).txt` - turn-one draft,
  wrong on the product question, the openings and the OneDrive folder. Header says so.
- `data\job-checks\riverside-house-aov.json` + fixture `_test-riverside.json`
- Generator: `scratchpad\riverside_drawings.py`; job json `test-results\riverside-run\`
- Quote: filed at `...\RRR\Riverside\1. Estimating\2. Supplier Quotes\Quotation_QT51518.PDF`
  (and at `test-results\mary-inbox\processed\20260727T0842-xgnwAAAA-att\`)
- Pack: `test-results\mary-inbox\processed\20260727T1500-xgqQAAAA-att\` - 6 drawings, filed nowhere

## THE FREE AREA - what changed on 27/07 and why it matters

Adam's enquiry of 24/07 said **"We need 1.5m2"**. A Plus returned 1.30 m2 and the answer that went to
Adam - and REQ-9 - was *no, 0.20 m2 short, requote at 1235 x 1583*.

**The pack says 1 m2, not 1.5 m2.** Drawings K1653-11 (first floor) and K1653-12 (second floor), both
CONSTRUCTION ISSUE, Campbell Ark, carry the identical red note:

> SMOKE VENT TO STAIRWELL ROOF - STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN
> AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2 OPERATED BY THE FIRE BRIGADE AT GROUND
> FLOOR ACCESS LEVEL IN THE STAIRS

It appears **once per stairwell, at that stairwell's top storey** - which is where the quantity of 2
comes from. Stairwell 1 tops out at second floor (K1653-12, leader 7); Stairwell 2 at first floor
(K1653-11, leader 3). So the requirement is **per vent**, settling the first of the two variables
triage flagged. A Plus's page 2 independently confirms they read it per vent: they size a *single*
frame (1235 x 1583) to reach 1.5 m2.

So on the pack, **1.30 m2 geometric clears 1 m2 with 30% to spare** and nothing needs resizing.
1.5 m2 appears nowhere in the pack; its source is unknown and needs confirming (RFI-3).

### ADAM HAS RULED ON SIZE (REQ-9, 27/07 evening)

> "We can make the windows as big as we need to in order to achieve the free area, because the
> openings are being newly formed. Drop me an email to remind me and I will ask Gintare to requote."

**Size is not a constraint** - the openings are newly formed and can grow, so if a resize is ever
needed there is no structural argument to have.

**AND THE ANSWER SPLITS PER VENT - read off the two stairwells 27/07 late, after Gordon Court found
their own pack encoded new-versus-existing in the window TAG PREFIX (WE_ = existing opening, WN_ =
new opening). Riverside has no such convention - W1 and W2 are performance tags, not opening tags -
but the floor plans show the openings directly:**

| | |
|---|---|
| **AOV.01** - second floor stairwell (K1653-12) | **NO window opening in any of its walls.** Every wall around the stairwell is drawn solid, so a new opening has to be formed. |
| **AOV.02** - first floor stairwell (K1653-11) | **THREE existing window openings** already in its external wall. If the vent takes one, its size is set by the existing opening. |

**CORRECTION, 27/07 latest - I said AOV.01's size was "genuinely free" and that Adam was corroborated
for that vent. That was too generous, and Gordon Court caught it by correcting the same error on their
own job: "THE TAG SAYS THE OPENING IS NEW, IT DOES NOT SAY WHAT THE OPENING IS CUT INTO."** Their WN_7
at level 1 is a new opening in *retained fabric* - lintels, cutting, making good - while the level 2
and 3 units sit in genuinely new added storeys and are free. **On Riverside there is no new-build half
at all.** The pack presents the whole building as existing: K1653-04 is a *single* "EXISTING /
PROPOSED ELEVATIONS" set of eight, with no added storey shown and no new construction annotated, and
the tower's cornice and pediment run continuously through all three storeys. So the second floor is
**retained fabric**, and AOV.01's new opening would be cut into existing masonry.

**Neither vent has a cost-free resize.** AOV.01 = new opening in retained masonry; AOV.02 = existing
opening whose size is set, or another new opening in retained masonry. Adam's "we can make them as big
as we need" carries structural cost on both, plus the planning question at C3. That is a materially
different answer from the one on the board an hour ago and it is now C2 in the brief.

**CORROBORATED BY A SECOND, INDEPENDENT INSTRUMENT (27/07, latest).** Gordon Court subsequently
withdrew the *window tag* as a reliable statement of opening condition - on their job WE_2 windows
turned out to sit in newly built stud walls, so the prefix is a schedule reference, not a rule the
drawing enforces. **That withdrawal does not touch this conclusion**, because Riverside has no
WE_/WN_ convention and none of the reasoning above used one: the openings were read directly off the
plans and the fabric off the elevations. The principle they gave - *"a new opening is not a free
opening; ask what it is cut into"* - stands, and they say so themselves.

What their correction *did* give me is a better instrument, and Riverside carries a version of it.
**Read the wall type coding.** The plans colour-code every wall that is new or altered - new partition
(purple), new separating wall upgrade (blue), separating wall upgrade to existing (yellow), dense
blockwork infill (hatch). Checked at both stairwells at high zoom:

| | |
|---|---|
| **K1653-12**, second floor stairwell | Internal walls coded yellow (Stairwell/Living) and purple. **External walls carry no coding at all**, and no opening. |
| **K1653-11**, first floor stairwell | Internal walls coded yellow with a hatched blockwork infill panel. **External wall carries no coding at all**, and holds the three existing openings. |

Uncoded = neither new nor upgraded = **retained existing fabric**, on both floors. So two independent
readings of the pack now agree, where before there was one.

**AND THE LIMIT, STATED HONESTLY.** Gordon Court's elevations carry an external wall build-up legend -
*"EXT - Existing wall types as surveyed"* against *"WT-A0 Brickwork / Cavity Insulation / Block"*,
*"WT-A1 Brickwork / Insulation / Stud"*, *"WT-A2 Zinc standing seam / Insulation / Stud"* - which tells
them the actual construction at each point of the facade. **Riverside has no such legend**: the key
covers separating walls and partitions only. So we know these external walls are not new, but **not
what they are made of** - and that decides the lintel, the fixing type and the cost of forming the
opening. Added to C2 as a document request alongside the demolition and existing plans.

*Still inference, not proof:* the coding convention marks change, so absence of a code is read as "no
change". It is used consistently and extensively across these drawings, which is what makes the reading
safe, but the existing plans would settle it outright.

### PART ONE DOES NOT WAIT FOR PHDB (28/07)

Gordon Court's challenge - *"when a job stalls waiting on a client, check which of your open items are
actually SUPPLIER questions; they do not need the award"* - run on Riverside. **All seven Part One items
are questions for A Plus about their own quote.** None needs RRR, Campbell Ark, PHDB or a decision from
anyone. The submission is gated; the brief's first half is not.

**Two of them decay while we wait:**

- **Item 7, the price hold.** QT51518 expires **26/08/2026** and our house document carries 30 days, so
  the last date we could issue and still be covered by A Plus was **27/07 - yesterday**. Issuing today
  puts our validity at 27/08, one day past their expiry. **The gap is one day now and grows by one for
  every further day of delay.** Asking A Plus to hold is the one action that becomes *more* valuable the
  longer the gate stays shut.
- **Item 1, the aerodynamic figure.** The single biggest open question on the job, and A Plus can answer
  it from their own system - they stated both figures on QT51516 three days earlier.

**Not wasted under any outcome:** if C4 resolves to "roof vent", only items 2 and 3 fall away, and only
for AOV.01. Items 1, 4, 5, 6 and 7 hold either way, and item 1 holds for AOV.02 regardless.

A "WHAT DOES NOT WAIT FOR PHDB" header now sits at the top of the brief so this is the first thing read.

### A SECOND, HARDER DEADLINE: 29 DAYS TO ASK A PLUS ANYTHING CHEAPLY (28/07)

Gordon Court took last night's validity arithmetic and found the sharper consequence: **a lapsing
supplier quote is not only a price risk, it is a deadline for every question you still want to ask that
supplier.** Anything sent before expiry is an addendum to a live quote - same job, same spec, same rates,
they add lines. Anything after is a fresh enquiry at whatever the market is by then. Theirs has nine
days; Riverside has more room but the same clock.

    QT51518 dated 27/07, 30 days   ->  lapses 26/08/2026  ->  29 days from today

**It matters most for brief item 2**, which asks A Plus to price a resized unit. Asked now it is a
revision we can set against GBP 4,845.22. Asked in September it is a new number with no anchor, and the
whole point of item 2 - knowing what a resize costs *relative to* what we hold - is lost.

So there are now two dates on this job and they answer different questions:

| | |
|---|---|
| **27/07 (past)** | the last date we could ISSUE and still be covered by A Plus. Gap grows by a day, daily. |
| **26/08 (29 days)** | the last date we can ASK A Plus anything as an addendum rather than a new enquiry. |

### I HAD NEVER READ FENSTER'S OWN EXCLUSIONS SCHEDULE, AND IT IS NOT ON THIS JOB'S DOCUMENT (28/07)

Gordon Court re-probed their 25 categories with concept-derived wording rather than A Plus's phrasing
and found **eight false negatives out of ten**. Run here, the re-probe found five false negatives - and
one of them opened something much larger than a regex fault.

**FENSTER HAS A STANDARD INCLUSIONS / EXCLUSIONS SCHEDULE. TWELVE EXCLUSIONS. I HAVE NEVER READ IT.**
It is in `templates/proposal-content.json`, a separate table from the Terms and Conditions:

    Site Welfare               facilities, power, water, lighting
    Access/Lifting Equipment   scaffold, MEWPs, towers, forklift etc.
    Site Storage               "materials will be delivered to site"
    Fire Stopping              to be done by others, if required
    Waste Removal              generally excluded unless agreed otherwise
    Internal Finishing         primarily excluded unless agreed otherwise
    Final Clean on handover    client's
    Testing                    "on or off site testing"
    Structural Alterations     "to be completed by Main Contractor"
    Design Responsibility      "design calculations, structural calculations and engineer
                               approvals unless specifically included within our scope"
    Traffic Management         road closures, street licences, parking suspensions
    Additional Limitations     "dimensions provided by others are assumed to be accurate. Any
                               additional costs arising from incorrect dimensions shall be
                               treated as a variation and charged accordingly"

**THREE TURNS OF BACK-TO-BACK ANALYSIS RESTED ON CLAUSE 16 ALONE.** I built the "what have we
disclaimed to the client" side of every diff from **one clause of the T&Cs** and never opened the
schedule that actually lists our exclusions. Gordon Court's fault was categories drawn from a document;
mine was worse - **my half of the comparison was a sample of one paragraph.**

### AND THE SCHEDULE IS NOT ON THE DOCUMENT WE WOULD ISSUE (28/07)

Checked at source rather than assumed. `outputs\Riverside House - Fenster Pricing Document (house
format).xlsx`, every cell:

    exclusion-ish cells in the Riverside document   2   (a total-excludes-VAT note, and a spec note)
    exclusion-ish cells in MASTER PRICING DOC.xlsx  1   (the same VAT note)

**The pricing template has no exclusions section at all.** The schedule lives in the proposal and
cover-letter path, and **Riverside was never generated from it**. So every exclusion this chat has
written down - structural alterations to the main contractor, design and structural calculations to
others, testing, storage, scaffold, waste, Part K anti-fall - **existed only in a template this job has
never produced and in a manifest the client will never see.**

The one exception, and it is worth stating precisely: **cell H5 does carry a real exclusion** -
*"AOV control panel, wiring, fire-brigade override and commissioning EXCLUDED - not in the A Plus
scope"*. Someone typed that in as a spec note. It is the only thing on the face of that document that
excludes anything.

**AN EXCLUSION THAT IS NOT IN THE DOCUMENT YOU ISSUE IS NOT AN EXCLUSION.** Fixed tonight: a twelve-line
exclusions block now sits at rows 33-45, and the totals are untouched - `I23` is still
`=SUM(I9:I10)+I21` and the `I21` array formula survived the save, checked before and after.

### WE WERE DOING TO RRR EXACTLY WHAT BSW DO TO US (28/07)

Cell C31 of the pricing document read:

> *"** This pricing document should be read in conjunction with the Terms and Conditions."*

**No title. No revision. No date.** That is BSW's *"terms and conditions of sale, available on request"*
shape - the one Gordon Court has just spent two turns describing as **worse than A Plus's named
incorporation**, because with a named one a request at least has a subject line. I have criticised it in
two suppliers this week while our own client-facing document did it.

Rewritten to name the document and say a copy accompanies it. **Free to fix before issue; a
conversation after one.**

### THREE THINGS I HAVE TO WITHDRAW OR NARROW (28/07)

**1. WITHDRAWN: "measurement is consistent both ways - we own it upstream and downstream."** Posted to
the board, put in the handover and written into AI.md. The exclusions schedule says *"dimensions
provided by others are assumed to be accurate. Any additional costs arising from incorrect dimensions
shall be treated as a variation and charged accordingly."* **Fenster do not unconditionally own
dimensions.** On Riverside the conclusion survives - the 1130 x 1530 came from our own enquiry, not from
others - but it survives for a **narrower reason than the one I gave**, and the general claim was drawn
from a clause I had read rather than the document I had not.

**2. WITHDRAWN: "testing and commissioning is already inside C6 and RFQ item 10(c), so it is not a new
seat."** That was last turn and it was wrong. Fenster expressly exclude **"Testing - on or off site
testing"**; A Plus test the actuator on local batteries only. So the witnessed test and certification of
a completed **life-safety smoke ventilation system** is excluded by us, excluded by our supplier, and
was asked of nobody - **the two-signature hole, in its purest form, and I looked straight at it and
called it covered.** Now on the RRR letter under question 10, with the RRO 2005 maintenance duty
alongside it.

**3. NARROWED: "the wind loading check and the fixing calculations have no owner."** More precisely:
**Fenster's standard schedule does exclude them** - "design calculations, structural calculations and
engineer approvals". So the company has an answer. **This job did not carry it**, because the schedule
was not on the document. Both halves matter: the general position was never unallocated, and the
specific job was.

### The re-probe itself, and what it changed (28/07)

`scratchpad/riverside_category_sweep_v2.py` - same 25 categories, each with its A Plus-derived patterns
plus wording written from the concept and from the phrasing Gordon Court quoted from AFS. **Five false
negatives**, and their content is the story:

| category | v1 said | the concept probe found |
|---|---|---|
| structural design of openings | A Plus silent | *"full structural calculations on all brackets/spigots"* - the word was `structural`, not `masonry` |
| windload / profile suitability | Fenster silent | our own **Design Responsibility exclusion** |
| unloading labour at delivery | Fenster silent | our **Access/Lifting Equipment exclusion** |
| part order / quantity **or size** | Fenster silent | our **dimensions-are-a-variation** clause |
| testing & commissioning | both silent | **both exclude it** - the withdrawal above |

**Gordon Court widened the part-order rule to cover size as well as quantity, and both limbs are live
here**: the aerodynamic answer could change the SIZE (RFQ item 2) and the wall-or-roof answer could
change the QUANTITY (RFQ item 13). A Plus's Changes clause covers both - *"any variation in
Specification, quality, quantity, Products, timescale, or method"*.

### New rule: `check_exclusions_reach_the_issued_document` (28/07)

Eighteenth in `RULES`. For every spec item carried as `excluded`, it asks whether the document that
actually goes to the client states any exclusions at all. **FAIL, not ASK** - this is a known-wrong
state rather than an open question.

Run against the manifest as it stood before tonight's workbook fix it returns
**"24 item(s) are being carried as EXCLUDED, and the document that goes to the client states none of
them"**. After the fix, PASS. Fifteen variants written before it shipped, seven of them negatives,
including a covering letter that carries the exclusions while the priced document does not - **which is
exactly the failure mode, and would otherwise read as fine**.

### And the hardening Gordon Court asked for (28/07)

They defeated the unnamed-incorporation branch **within an hour of it shipping**, by typing *"BSW terms
and conditions of sale, available on request - no revision, no date, no title"* into `document` - an
accurate, careful, human-readable description of the fact that there is no name, **in the field whose
emptiness was the signal**. `named = bool(doc)` read it as a name.

`_describes_absence()` now catches that. Eleven more variants, **six positives in three different
drafting voices and five negatives that must NOT trip** - including real document names containing
`NA/EU` and `National`, one of which did trip the first version of the pattern and forced it to narrow.
**46/46 terms variants, 15/15 issued-document variants.**

### MY SWEEP WAS DOCUMENT-DRIVEN, NOT CATEGORY-DRIVEN - AND IT COST TWO LIVE ITEMS (28/07)

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

### A PLUS'S CONDITIONS PUT PART B ON US, AND OUR OWN TERMS DISCLAIM IT TO THE CLIENT (28/07)

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

### I shipped a detector validated against one positive case (28/07)

Gordon Court turned last turn's sampling lesson on their own newest rule and found it had been shipped on
*"0 fires across 119 spec items in 13 manifests"* - **which measures precision and says nothing about
recall, because the validation set contained exactly one positive case: the one it was built from.**
Theirs caught 5 of 9 plausible phrasings. **`check_free_delivery_threshold` is mine, shipped 27/07 against
exactly one fixture.** Sixteen adversarial variants found **two real defects:**

| variant | was | now |
|---|---|---|
| `free_delivery_threshold: "5000"` - a number written as a string | **TypeError, aborting the whole run** | FAIL |
| `delivery_priced: "yes"` - an unrecognised truthy value | **FAIL, "delivery is not in the price"** | UNKNOWN, asks for the vocabulary |

**The crash is the worse one, and it is an interaction bug neither of us would have found alone.** The
field only became string-typed when Gordon Court added `"never"` last night - and a reader who sees one
string in a manifest reasonably writes another. My code then compared a float to a str and killed every
later rule in the run.

**The second is quieter and more dangerous:** an unrecognised value was read as *not priced*, so the rule
asserted something false about the world from a value it did not understand. **Misreading an affirmative
as a negative is the direction that costs money.** It now says it does not recognise the value.

All 16 variants persisted into `--selftest` as `DELIVERY_VARIANTS` - a test that lives only in a
transcript is worth nothing. Selftest passes, live run unchanged.

**The rule: if you shipped a detector this week, count the positive cases in what you validated it
against. If the answer is one, you have measured precision and called it quality.**

### The decision-versus-information check, run properly across both letters

Last turn's was run from memory and found the control system. Run properly as a diff of **14 topics**
against both letters - and worth saying that **12 came back clean**, because a check that only ever fires
is not one you can trust. Two failed:

- **The 1.6 W/m2K U-value - decision owner never asked.** A Plus are asked for the figure (item 4); nobody
  was ever asked whether 1.6 *binds these vents at all*. The stair vents are the only glazing on the
  drawings carrying **no W tag**, which is exactly why it is ambiguous and exactly why it needs asking. If
  it does not apply, A Plus's answer is moot; if it does, and their standard is *"no better than 1.8"*,
  there is a specification problem. **The exact mirror of last turn's finding** - then the information
  holder was missing, here the decision owner.
- **Cill height above FFL - asked of nobody at all.** A Plus flag a trap hazard under BS EN 60335-2 below
  2.5m and Part K anti-fall below 1100mm, and *exclude* the latter. We exclude it too. **So it is excluded
  by both parties and asked of neither**, on a life-safety system in a stairwell. It had sat as RFI-5
  since the first day and never reached a letter.

Both are now questions **7 and 8** of the RRR letter, which renumbers to eleven items.

**Considered and declined, recorded so nobody re-derives it:** the inferred 86.5mm frame section. Gordon
Court's companion rule is *if a calculation came out indeterminate, check whether somebody simply knows
the answer before recording it as unknowable*. That one is not indeterminate - the sensitivity table holds
across 150-200mm head+cill - and item 5 already asks A Plus to confirm the configuration it supports.

### I generalised a mechanism from a sample with no variation in it (28/07)

Gordon Court measured the truncation properly - **44 remedy sentences across 13 manifests** against my
three on one job - and corrected my explanation. I had said the rules are *written statement-first and
action-last*. They are not:

    details 400 chars or under    n=35    median remedy at   0% through     3 of 35 cut
    details over 400 chars        n= 9    median remedy at  84% through     9 of  9 CUT

**Most rules put the remedy FIRST.** What actually happens is that the remedy is **pushed backwards by
the list of offending items**, and that list grows with how much is wrong - while the truncation that
hides it is triggered by the same length. So *the instruction vanished exactly on the jobs where most had
gone wrong.* Their one-rule proof: `delivery actually included`, identical code, remedy at 0% on ten
one-supplier jobs (332 chars), **78% on Riverside** (447), 84% on St Mary's, 89% on Gordon Court (776).

**Riverside is a data point in their proof, and checking my own three shows why I was wrong:**

| rule | detail | remedy | combined | remedy position |
|---|---|---|---|---|
| system can meet the specified performance | 348 | 92 | 441 | 79% |
| supplier price held as long as ours | 219 | 78 | 298 | 73% |
| delivery actually included | 347 | 99 | 447 | 78% |

**All three of my samples were from the displaced regime. I never saw a short one.** So "the rules are
written action-last" was an artefact of a sample with no variation in the independent variable - every
finding on this job happened to be long enough to displace its own remedy.

**The lesson is better than the original one: three samples from one job cannot distinguish "the rules
are written this way" from "my job is in the regime where they behave this way."** Same family as
everything else tonight - a conclusion that looked clean because the evidence contained no counterexample.

Their fix is structural rather than cosmetic: `result()` now takes a separate **`remedy`** field printed
on its own `->` line where no future abridgement can displace it. Verified on this manifest - all three
ASKs now carry one.

### Their asymmetry check, run here - and it found something

Gordon Court diffed their two supplier letters and found they had asked the **GBP 18,298.94** supplier how
long it could hold its price and *explicitly not asked* the **GBP 183,005.42** one. The reasoning was that
Adam had decided we carry the risk, so asking seemed pointless - **which conflates a decision about
whether WE hold OUR price with whether we gather information from a SUPPLIER.**

Riverside has one supplier, so the literal diff does not apply. **The underlying shape does, and it
fired.** Checked both letters for the AOV control system - the single largest unowned item on this job:

- **Questions to RRR, item 8:** *"Who is carrying the AOV control system?"*
- **RFQ to A Plus:** no mention. Zero hits for control, panel, override, SE Controls, 24v or interface.

**I asked the party who owns the DECISION and never asked the party who holds the INFORMATION.** A Plus
supply the actuator; their own notes say it *"must be powered by a compatible control system which is
approved by SE Controls"*. They are the best-placed party in the chain to say what that system is, and I
excluded them because I had decided the scope boundary - **a scope boundary says what a supplier will
SUPPLY, not what they can TELL you.** Exactly Gordon Court's conflation with the parties swapped.

Fixed: **item 10** now asks A Plus what panel they would recommend for 2no 24v actuators on this duty,
whether they supply it or it is always a separate trade, and to price it if they can - so C6 can go to
RRR with a figure rather than a gap.

**The generalised check: for every open item, list who owns the DECISION and who holds the INFORMATION,
and confirm you have asked both.** They are often different parties, and a scope boundary is not a reason
to skip the second.

### The price gate was truncating every remedy (28/07)

Gordon Court took the *"a report that omits a category is worse than one that shows it wrongly"* form and
found a far worse instance than the one it came from: **`report()` in `mary_checks.py` - the thing that
decides whether a quote goes out - printed the first 200 characters of a FAIL and stopped.** On their job
that hid **GBP 201,304.36** of unfixed cost and a spec rule naming nineteen uncovered items of which three
reached the screen.

**Measured here, as they asked.** Riverside is a small job so the absolute loss is small - **586
characters across three ASKs** - but the pattern is sharper than a random cut:

| Rule | chars | lost | what was past the cut |
|---|---|---|---|
| system can meet the specified performance | 441 | 241 | the thermal requirement, and *"Get it in writing - on both founding jobs the answer existed and no one had gone and got it"* |
| supplier price held as long as ours | 298 | 98 | *"Confirm the supplier price at the point of issue, or carry a stated allowance"* |
| delivery actually included | 447 | 247 | the charge basis, and *"Get the supplier to confirm the charge or that the load is batched free before the price is issued"* |

**All three cuts removed the REMEDY, not the finding.** That is not luck - these rules are written
statement-first and action-last, so **a trailing truncation strips the instruction from every rule at
once.** For a week the screen showed what was wrong and never the sentence saying what to do about it.

**Being accurate about the harm on this job:** it cost nothing here, because the job is small enough that
the same ground had been worked by hand - the validity arithmetic and the delivery question both reached
the brief by independent derivation rather than by reading the remedy. On a job the size of Gordon
Court's it would have cost a great deal. The fix is theirs; the verification that it works on this
manifest is mine, and their new `check_spec_label_matches_evidence` passes on all 21 spec items.

**And their job-file contradiction check, run here:** 851 lines grepped for *not run / outstanding / not
done / cannot be run*. **One hit, and it is accurate** - the Excel recalculation, which is dealt with
immediately below rather than left sitting.

### The stale-draft tool was dropping our own letter - fixed (28/07)

Gordon Court built `scripts/mary_stale_drafts.py` off last night's finding and asked every chat to run it
on their own folder. Run here, **our A Plus letter was absent from the report entirely** - not under due,
not under undated, nowhere - while the sweep concluded *"Nothing expired"*. They had said the tool "sees
riverside's A Plus letter at 26/08"; it parses it, but the report never printed it.

**The bug:** `days < 0` to expired, `days <= warn_days` to due, and **no else**. Any dated draft more than
14 days out was parsed, dated, and silently dropped. Proved it rather than asserting it - the same file
appears correctly at 6 days on `--today 2026-08-20` and as expired on `2026-08-27`, so the parsing was
always fine and only the reporting was blind.

**Why it mattered rather than being cosmetic:** a sweep that shows a dated draft only in the last
fortnight of its life shows it exactly when acting has stopped being comfortable. Our letter's whole
argument is *send this while the quote is live*; 15 of its 29 days would have passed unmentioned.

Fixed by adding a **DATED, NOT YET DUE** bucket, with the reasoning in the docstring so nobody removes it
as noise. Verified across all three date views and the exit-1-on-expiry behaviour still fires. No other
code called `scan()`, so extending the return signature was safe - checked before changing it.

**The general form: a report that omits a category is worse than one that shows it wrongly.** *"Nothing
expired"* read as an all-clear over a file the tool had already read.

### Their mirror hazard, applied to our own dated letter

Last night's finding was that a draft goes stale when the *facts* move and nobody notices. Gordon Court
pointed out the mirror: **a draft can go stale on a date you typed into the filename yourself** - and
that is the easier of the two to defend against. Our A Plus letter argues in its own words that it is *"an
addendum to a live quote"*, which becomes false on 27/08.

It now opens with **`IF TODAY IS AFTER 26 AUGUST 2026, DO NOT SEND THIS AS IT STANDS`**, listing the four
sentences that go false and confirming the nine questions stay valid - it needs re-heading as a fresh
enquiry, not binning, with the base price expected to move.

### Their quote-parsing hazard, checked here rather than assumed

Gordon Court withdrew a turn-one finding after discovering they had attributed glass lines by proximity -
searching for a glass string and reading the nearest preceding `Location:` header. **On a quote where one
position carries five glass lines, the nearest header above a line is not the position it belongs to.**
Their obscure-glazing item was on the wrong position and understated by sixteen units.

**Checked on QT51518 rather than assumed safe.** The quote has exactly **one** position block - one
`O/A Sizes`, one `Frame Price`, one `Glazing Details & Apertures`, and **zero** `Location:` headers. With
a single position there is nothing to misattribute, so the A1/A7 apertures and the `4-20-4 Clr Tough
S Coat 1.2` make-up necessarily belong to the 1130 x 1530 unit, and the aperture reconciliation stands.

**The hazard scales with the number of position blocks:** impossible on a one-position quote, near-certain
on a multi-position quote parsed by proximity. Worth knowing which kind you are reading before trusting
an attribution.

### The brief is now two letters somebody can actually send (28/07)

Gordon Court turned their clause-16 sort into three drafts and made the fair point that an urgent item
with no text behind it is still a request for somebody else to write an email. **This chat had been
calling Part One urgent for two turns while leaving it inside a fifteen-item document someone would have
to disassemble first.** So it is split, along clause 16, each letter carrying its reasoning at the head:

| | |
|---|---|
| **RFQ to A Plus** (`send by 26-08`) | The nine items clause 16 makes **ours** - product suitability, the aerodynamic figure, the Uw, leaf configuration, delivery, restrictors, price hold. Dated, because QT51518 lapses 26/08 and after that it is a fresh enquiry rather than an addendum. |
| **Questions to RRR** (no date) | The items clause 16 puts on **their professional team** - free-area basis, wall or roof, the 1.5 m2 source, sheet currency, the openings, planning, the control system, the programme. Grouped by owner (Campbell Ark / HD Planning / RRR) so it can be forwarded rather than answered. |

**Two drafting choices taken from Gordon Court, both about not overclaiming:**

- **Ask a supplier what they priced against, not why they got it wrong.** It matters more here than on
  their job: the 1130 x 1530 came from *our* enquiry, so A Plus quoted exactly what we asked for. The
  letter says so in terms. Items 5 and 9 ask them to confirm what we think we are reading and whether the
  product suits the position - neither is a complaint.
- **When a decision has been taken, say so.** Adam ruled the openings can be sized to suit. The covering
  note states plainly that nothing here reopens that, and that if a bigger vent is needed his answer is
  exactly right - the point is only that we do not yet know whether one is.

**And the turn-one reply to Adam has been marked SUPERSEDED - DO NOT SEND**, with a header listing what
it gets wrong: it treats the vents as a settled wall-window purchase, repeats that size is unconstrained,
and says the OneDrive folder is empty. It was sitting in `outputs\` where somebody could have sent it.
**A stale draft in an outputs folder is a live hazard, not a harmless record.**

### CLAUSE 16 SPLITS EVERY FINDING INTO "OURS TO FIX" AND "OURS TO ASK" (28/07)

Gordon Court found the clause we had both been sitting on. **Verified independently from our own
`MASTER COVER LETTER 31.05.2026.docx` by enumerating the T&C headings - clause 2 is Quotation Validity,
clause 16 is Design Responsibility:**

> *"Fenster Glazing & Locks Ltd is not responsible for overall design intent, architectural suitability,
> or **REGULATORY STRATEGY** and relies on information, drawings, and specifications provided by the
> client or their professional team. **Responsibility is limited to MEASUREMENT VERIFICATION, SUPPLY, AND
> INSTALLATION** of the agreed glazing systems."*

This is a **third** sort over a findings list and the most useful yet. The others asked *what can you
cost?* (priced / benchmark / unpriceable) and *who do you ask?* (rate versus quantity). This one asks
**whose responsibility is it under our own terms** - and therefore how a finding should be raised.

| **THEIRS** - regulatory strategy / design intent, we rely on their team | **OURS** - the clause expressly retains it |
|---|---|
| **C0/C1** is the 1 m2 geometric, aerodynamic or clear opening area | **Item 1** obtaining the aerodynamic *figure* from A Plus |
| **C3** does enlarging an opening sit inside the prior approval | **Item 4** whether A Plus have stated a whole-window Uw *at all* |
| **C4** does the fire strategy require a roof vent | **Item 9** whether we have quoted the right *product* for the position |
| **C5** are K1653-11/12 still the current issue | **Item 5** the leaf configuration |
| **C6** who carries the AOV control system | **Items 6, 8** delivery destination, restrictors |
| **RFI-6** is 1.6 W/m2K the right target for a stair AOV | **The 1130 x 1530** - measurement verification |

**The split that stops it being a get-out, and it runs straight through this job's biggest question.**
*"Is the vent required in the roof?"* is regulatory strategy - **theirs**, and the position is reliance
rather than defect. *"Have we quoted a wall casement for a position the drawing puts on the roof?"* is
**supply - ours**, and clause 16 does not touch it. C4 previously mixed the two; it is now split, with the
supply half added to Part One as **item 9**.

Same shape on thermal: *is 1.6 the right target* is theirs; *has our supplier stated a Uw at all* is ours.

**AND IT CORRECTS MY OWN FRAMING FROM LAST NIGHT, in the direction that cuts against us.** I wrote that
clause 2's *"subject to final site survey and measurement verification"* **qualifies** the dimensional
risk. That is only half right. Clause 16 says our responsibility **is** measurement verification. So the
survey makes a dimensional discrepancy **fixable - it does not make it somebody else's**. The 1130 x 1530
came from an enquiry rather than a survey, and both clauses point at us. Gordon Court are right to temper
it and I have.

**Practical effect, now built into the brief:** ours-to-fix items belong in a supplier RFQ; theirs belong
in a client qualification framed as **reliance**, not as defects. Those are two documents with two tones,
and the brief's Part One / Part Two split now maps onto clause 16 deliberately rather than by accident -
with the reasoning written at the foot of it so whoever sends it knows why.

### CORRECTION: the OneDrive job folder is NOT empty, and never was (28/07)

**This chat reported "the OneDrive job folder is still empty" in the brief, the job file, the hub, the
noticeboard and the handover.** It is wrong. The folder carries the full job structure and real files:

    1. Estimating. Supplier Quotes\Quotation_QT51518.PDF        filed 27/07 15:46
    1. Estimating. Client Quote\MASTER COVER LETTER 31.05.2026.docx
    1. Estimating. Client Quote\MASTER PRICING DOC 10.07.2026.xlsx
    1. Estimating. Client Quote\Fenster Glazing - Tender Package\...   (QA, H&S, method statement)
    plus 1. PO, 2. Site Survey, 3. Drawings, 4. Orders, 5. Finance, 6. H&S, 7. Aftersales

**The cause is exactly the error Gordon Court described tonight.** Searches were run against
`OneDrive - Fenster Glazing & Locks Ltd`, which does not exist - the root is
`OneDrive - Fenster Glazing (1)`. Zero results were read as an empty folder. **A failed search is not
evidence of absence; it is evidence of a failed search.** The same class as their half-filled column,
their print statement and this chat's generator footer.

**What survives the correction:** the `3. Drawings` folder holds no files, so none of the six drawings we
are working from is filed anywhere - they exist only as email attachments. The pack-completeness finding
stands; only the "folder is empty" wording was wrong. And A Plus's quote **is** filed, so triage's
original "the only copy is the email attachment" is also out of date.

### Two clauses in the true source that the extraction did not carry

Having found the real folder, the **actual** `MASTER COVER LETTER 31.05.2026.docx` could be read rather
than `templates/proposal-content.json`, which is an extraction of it. **The extraction has 76 paragraphs;
the docx has 153.** The validity clause is faithful in both - so last night's figure was right - but two
clauses matter here and one is absent from the extraction entirely:

- **NOT IN THE EXTRACTION.** *"Site Survey - Only conducted once the structural openings are fully
  formed. Any revisits may be subject to a fee."* **Material.** AOV.01 needs a new opening cut in
  retained masonry, so the sequence is: PHDB form the opening, then we survey, then A Plus manufacture.
  Our survey cannot precede the builder's work, and **nobody has stated when that is**. It bears directly
  on the price hold - the further out the opening, the longer A Plus are being asked to hold, and it may
  exceed anything they will give. Now **C8** in the brief.
- **In the extraction, but not previously read.** *"Fenster Glazing & Locks Ltd is not responsible for
  overall design intent, architectural suitability, or **regulatory strategy** and relies on information,
  drawings, and specifications provided by the client or their professional team. Responsibility is
  limited to measurement verification, supply, and installation of the agreed glazing systems."*
  **The geometric-versus-aerodynamic question is regulatory strategy.** Our own terms disclaim
  responsibility for it and place reliance on the client's professional team. That does not make asking
  optional - asking is still right, and C0/C1 stand - but it changes the character of the exposure from
  "we may be liable for a non-compliant vent" to "we rely on the client's team, and we asked".

### The NOT RUN check, now run (28/07)

Logged four turns ago: **the GBP 5,990.22 had never been observed as a value computed by Excel.** It was
hand-derived from the workbook's stored formulas and reproduced by `mary_pricing` - two routes that agree,
but both resting on *this chat's reading of the same formula chain*. A live recalculation via Excel COM
would not start in this environment, and LibreOffice is not installed.

Gordon Court's own rule applies: **logging a check as outstanding is only worth something if somebody then
runs it.** So it is now run by a third route that removes the reading as the single point of failure - a
parser that extracts the maps **from the formula text itself** rather than being told them:

- the code-to-adder map read out of `H9`'s `IF(B9="MAW",550*75%...)` chain, giving **412.50**;
- the code-to-labour map read out of `I21`'s SUMPRODUCT, giving **160**;
- applied to the actual `B/F/J/K/L` cell values in the file.

    items          5,670.22
    installation     320.00
    TOTAL          5,990.22      (I23 = SUM(I9:I10) + I21)

**Three independent routes now agree.** The residual is genuinely smaller: what remains unverified is
only whether Excel would interpret those formulas differently from the parser, rather than whether one
person read them correctly. The template was separately confirmed identical to the live
`MASTER PRICING DOC 10.07.2026.xlsx`, and the code values are corroborated by Adam's table in
`MARY-HANDOVER.md` s6.

### Our own validity clause, verified at source - and its second half matters (28/07)

Gordon Court's lesson: **check your own terms and conditions page before you report a validity gap - the
answer may be in the document you sent.** They found their proposal's page 8 qualified an exposure they
had been reporting as absolute all night. Run here, because the 30-day figure underpinning every deadline
on this job had been taken from a generator footer rather than the house document.

**Verified at source** - `templates/proposal-content.json`, Terms and Conditions, *"Quotation Validity"*:

> *"All quotations provided by Fenster Glazing & Locks Ltd are valid for 30 days from the date of issue,
> unless agreed otherwise. **All quotations are subject to final site survey and measurement
> verification.**"*

So the 30 days is right and the deadline arithmetic stands. **But the second sentence is a genuine find
for this job.** Riverside's 1130 x 1530 came from Adam's enquiry of 24/07 - not from a survey, and not
from any dimensioned drawing, because the pack has no window schedule and no dimensioned opening. Our own
standard terms already make the price *"subject to final site survey and measurement verification"*.

That does not remove the need to settle C2 and C4 - a roof vent is not a measurement error, and neither
is a structural opening - but it does mean an issued price would not be a fixed commitment on unsurveyed
dimensions. Worth knowing before anyone treats the size question as a commercial exposure rather than a
technical one.

### A second exclusion of the same class - and a trap to avoid in the proposal

Gordon Court sharpened the test: **"we exclude X" is only safe if X is genuinely somebody else's under
the spec.** Three of their twelve failed it. Run over Riverside's list, most hold - builder's work is
PHDB's, access is Adam's standing rule, maintenance is the occupier's RRO duty, Part K balustrading is a
builder's item A Plus expressly exclude. **One fails:**

**Onward haulage MK13 9HF to HP19 7HL.** Excluded - but it is not somebody else's. **Fenster are the
installer, so moving material from our own yard to site is ours.** It was excluded because nobody had
priced it, not because it belongs to another package. Same shape as the restrictors: quantity known
(1 delivery), no rate anywhere, so a supplier figure is the route - already brief item 6(b), which asks
A Plus to quote delivery direct to site. Reclassified `excluded` to `provisional`.

**AND A TRAP TO AVOID RATHER THAN AN ERROR TO CORRECT.** Gordon Court's issued proposal excludes Site
Storage *on the basis that* *"Materials will be delivered to site"* - which contradicts every supplier
quote they hold, all five delivering to our own MK13 9HF yard. **Riverside has no proposal yet, so
nothing is wrong here - but that wording must not go in**, because A Plus deliver to Milton Keynes and we
would be telling RRR the opposite of what our own supplier says. Flagged now so it is caught at drafting
rather than after issue.

### Rate or quantity? The lens that surfaced the restrictors

Gordon Court corrected their own "unpriceable" list: curtain walling **has** a rate - `mary_pricing`
carries CW_SUPPLY_M2 850.0 and CW_LABOUR_M2 150.0 - what it lacks is a **quantity**. Verified here at
source. That is the opposite problem from a missing rate and it changes who to ask: an area from the
architect, not a price from the supplier.

Run on Riverside's items:

| Item | Rate? | Quantity? | Position |
|---|---|---|---|
| The 2 vents | supplier-backed | 2 | **priced**, GBP 5,990.22 |
| External mastic | house rate GBP 5/lm | 10.64 lm | **priced**, GBP 53.20 |
| **Window restrictors** | **none anywhere** | **2no, known** | **was excluded - now provisional, Part One item 8** |
| Onward haulage MK13 to HP19 | none | 1 delivery | supplier question, already item 6(b) |
| AOV control system | none | none | excluded, and another package's scope |
| Access equipment / scaffold | none | unknown | excluded |
| Structural opening work | none | no design exists | excluded |

**The restrictors are the one this surfaced, and they should not have sat quietly in an exclusions
list.** A Plus's own AOV notes put the duty on *"the facade contractor / fabricator"* - and on this job
**Fenster are the installer, so that is us**. They also disclaim liability for replacement actuators or
damage to the vent if no restrictor is fitted 50mm beyond the stroke, on a life-safety system. Excluding
them may still be the right answer, but it is a decision Adam should take against a number rather than a
gap. Quantity is known and no rate exists anywhere, so a supplier figure is the only route - now Part
One item 8, and reclassified in the checks manifest from `excluded` to `provisional`.

### The rate register prices frames and glass and almost nothing else

Gordon Court found that of the register's 80 categories, none covers the ancillaries. **Verified here at
source rather than taken on trust** - and it is broader than they stated. All 21 terms return **zero**:

    acoustic  trickle  Linkvent  Passivent  curtain  actuator  AOV  smoke  strip  disposal
    manifestation  intumescent  mastic  restrictor  scaffold  kerb  roof vent  secondary
    folding  sash  slider

The board already carried four missing categories - folding doors (Grange Hill), vertical sliders
(Georgie's), secondary glazing (Lower Range Road), AOV/smoke vents (Riverside). Those were unusual
**products**. Gordon Court add five that are not: **strip-out and disposal, manifestation, acoustic
trickle vents, intumescent seals, curtain walling** - ancillaries that appear on nearly every
refurbishment. My own check adds **mastic, restrictors, scaffold and kerbs**, all of which this job
carries.

**One correction to the framing, in fairness to the tooling:** a handful of standing rates *do* exist
outside the register - mastic GBP 5/lm, EPDM GBP 25/m2, install default GBP 140/unit - which is where
this job's mastic line comes from. So it is not that nothing exists; it is that the **register** does
frames and glass to size-banded, supplier-attributed depth and the ancillaries have only a few flat
house rates or nothing at all.

**Why it matters here:** on this job the unpriceable items are the AOV control system, the restrictors,
access equipment and any structural opening work. On a two-vent job that is tolerable because they are
all explicitly excluded. On a refurbishment where ancillaries are a large share of value, it means the
windows can be priced and none of the work around them - which is worth knowing before anyone quotes a
refurb off the register and reports the whole-job error as small.

### The routing table - who owns each open question

Gordon Court built one for their job off title blocks and found they had been addressing eleven RFIs to
the main contractor when most were design questions the contractor does not own. Built for Riverside,
all details verified at source (Campbell Ark's from the K1653-11 title block at high zoom; hd planning's
from the location plan's text layer). **Mary cannot approach any of them - the route is Adam or
Gintare.**

| Owner | Reference | Owns |
|---|---|---|
| **Campbell Ark** - author of the layouts, elevations, wall coding and the smoke-vent note | job **K1653**, drawn SC, 01234 709296, drawingoffice@aol.com | **C0, C1, C2, C4, C5, C7** - most of the list |
| **HD Planning Ltd** - planning consultant | plan ref **HD0-0197-01a**, application **24/02303/PAPCR**, Mrs H Doyle, hayley@hdplanning.co.uk, 07916276436 | **C3** - the prior-approval question |
| **RRR Group / PHDB** | building works package | **C6** - who carries the AOV control system |
| **A Plus** | quote **QT51518** | all of **Part One** |
| **Nobody** | - | Structural design of a new opening, and the wall build-up. **Cannot be chased, only raised.** |
| **Building control** | the drawings' own *"BUILDING INSPECTOR APPROVAL"* | Effective arbiter on the free-area basis if Campbell Ark took no advice |

Note the applicant named on the location plan is **Elderfern Ltd**, not RRR, so the planning
relationship may sit with a different company in the group.

**The contrast between the two jobs is what makes the test worth running.** Gordon Court's pack names a
full design team - architect, structural, services, electrical, heating - and every deferral they chased
turned out to be *administrative*. Riverside's names a heating engineer and an electrician as **roles**
and defers the rest to parties not yet appointed, so four of five are *design* gaps. Same test, opposite
answers, and it tells you which you are in: chase paperwork, or raise an alarm. And note their
"fire officer" appears only inside a revision note rather than as an appointment - the same pattern as
this job's "BUILDING INSPECTOR APPROVAL", which is a role reference, not a consultant.

### Whose gap is it? Administrative or design - and who to actually ask

Gordon Court turned the "is the consultant even appointed" question into a rule, having run it on their
own pack and got the opposite answer. Their Energy Statement's **title block** reads *"Edward Pearce...
Project No. 22/190"* - and that project number matches every M&E document they hold, so the architect's
deferral pointed at a document already in their possession. One title block closed their
longest-running question.

**The rule the pair of jobs produced:**

| | |
|---|---|
| Deferral to a **named, appointed** consultant whose other work is in the pack | **ADMINISTRATIVE gap.** Ask for the document, price on, qualify if it does not arrive. |
| Deferral to **nobody** - no consultant named, everything "to be site agreed" | **DESIGN gap.** There is no document to ask for. This is the one that should stop you. |

Same words on a drawing; entirely different problem. **Run on Riverside's deferrals:**

| Deferral | Points at | Class |
|---|---|---|
| *"SEE DETAIL 1 / 2 / 4 / 5 / 6"* | Campbell Ark's own **K1653** series | **Administrative** - ask by number |
| *"CONTRACTOR TO ESTABLISH EXACT DRAINAGE LAYOUT"* | A contractor not yet appointed (PHDB are still being priced) | **Design** |
| *"BOILER/HEATER LOCATION/S TO BE SITE AGREED WITH HEATING ENGINEER/ELECTRICIAN"* | A role, no firm named anywhere | **Design** |
| *"ELECTRICAL LAYOUTS ARE TO BE SITE AGREED WITH CLIENT"* | The client | **Design** |
| Wall build-up / structural opening | No structural engineer named anywhere | **Design** |

So only the DETAIL sheets are a paperwork problem. Everything that bears on our openings is a design
gap, and chasing will not produce a drawing.

### The title-block method run here - and it changes who we ask

Campbell Ark's title block, read at high resolution off K1653-11: **job number K1653**, drawn **SC**,
**Campbell Ark, 01234 709296, drawingoffice@aol.com**. Two things follow.

**1. K1653 is the handle for the missing sheets.** *"Please issue the K1653 drawing register and any
sheets we do not hold"* is a request that can be actioned in a minute, where "the rest of the pack" is
not. Now in C7.

**2. There may be no fire strategy to ask for, and C0 has been rewritten because of it.** We had been
requesting "the fire strategy". No fire engineer is named anywhere on the six drawings, and the
smoke-vent note is **Campbell Ark's own**, written in Approved Document B language on a sheet whose key
works *"TO AD B1"*. On a prior-approval conversion of this size the architect commonly carries the fire
strategy within the drawings. If that is the case here, requesting a document returns nothing and costs
a week. **So C0 now asks the author** - Campbell Ark, by name and contact - whether the 1m2 is
geometric, aerodynamic or clear opening area, whether the vent is wall or roof, and whether any fire
engineer or building control officer advised the note. If nobody independent set the figure, building
control becomes the arbiter - and these drawings defer to the building inspector repeatedly.

**Ask the author of a note, not a consultant who may not exist.**

### And the build-up gap has an owner: the structural engineer, not the architect

Gordon Court closed the same gap from the other side. Their wall legend's first entry - *"EXT -
Existing wall types as surveyed"* - **defers rather than describes**, and the answer was in a structural
sub-folder nobody had opened: *"Brick & mortar sampling in the internal SOLID wall. Brick & mortar
sampling in CAVITY wall. Take samples from BOTH THE INNER AND OUTER LEAVES of the cavity wall."* So
their external walls are cavity, two leaves, and the internal walls solid. **Asking the architect for a
wall build-up and asking the structural engineer for the investigation drawings are two different
requests, and on a refurbishment the second is usually where the answer is** - somebody had to sample
the masonry before designing anything.

**Run on Riverside, and the answer is a concern rather than a build-up.** No structural engineer is
named anywhere on the six drawings we hold. The notes name a heating engineer and an electrician, and
otherwise defer consistently to site:

> *"CONTRACTOR TO ESTABLISH EXACT DRAINAGE LAYOUT..."*
> *"BOILER/HEATER LOCATION/S TO BE SITE AGREED WITH HEATING ENGINEER/ELECTRICIAN & TO SUIT BUILDING
> INSPECTOR APPROVAL"*
> *"ELECTRICAL LAYOUTS ARE TO BE SITE AGREED WITH CLIENT"*

So on this pack there is no evidence anybody has surveyed the masonry or designed a structural opening.
**Adam's "make them as big as we need" may be committing to work that has neither a design nor a
price** - which is a different problem from it being expensive. Added to C2, framed as a concern to
raise rather than an accusation, since the engineer's drawings may simply not have reached us.

### Two items cleared rather than raised

Both from Gordon Court, both worth recording so they are knowing exclusions rather than silent gaps:

- **Cavity closers, cavity trays and jamb DPCs are NOT the glazing scope.** They sit in NBS **F30**
  *"Accessories/sundry items for brick/block/stone walling"* - a masonry section - so they are the
  bricklayer's even where a new opening is formed. **Check which NBS section an accessory sits in
  before deciding it is missing from your price.** If Riverside's walls prove to be cavity, these items
  will exist and belong to the builder's work package, not ours.
- **Intumescent perimeter seal - check run, not applicable here.** NBS **L10 cl.790** *"Fire-resisting
  frames"* requires the frame-to-reveal gap to be *"completely filled with INTUMESCENT mastic or tape"*,
  and L10 **is** the windows section - so on fire-rated frames it is our scope, and ordinary mastic
  buried in a supplier's fixings line does not comply. Not applicable on Riverside: these are smoke
  vents in the **external** wall of a protected stairwell, so the perimeter seal is weathering, not
  compartmentation - fire separation here runs between the stair and the flats (FD30s doors, fire
  collars, separating wall upgrades), not through the envelope. Our priced external mastic at
  10.64 lm x GBP 5 stands. Re-check if a vent is ever relocated into a compartment wall.

**And neither stairwell's glazing carries a W1 or W2 tag** - every habitable-room window on these
drawings does. The stair windows sit outside the tagged system entirely, which is probably why the
vents were never scheduled, and it bears on whether the drawings' 1.6 U-value binds them (RFI-6).

This is read off floor plans, so it is suggestive rather than conclusive - the demolition plan is still
the document that settles it. But it is a much better question than "confirm the openings are new",
and it is now C2 in the brief, split per vent.

**A CORRECTION TO MY OWN EARLIER FLAG.** I raised the risk that AOV.01 sits in an arched opening,
because Elevation F's tower top storey carries two arched-head windows. Those two arched windows line
up with the **Living room's** two W2 windows on K1653-12, not with the stairwell - the stairwell has no
windows on that face or any other. So the arched-head risk is withdrawn. What replaces it is sharper:
**the second-floor stairwell has no wall opening at all and the note says the stair is to be "VENTED AT
THE TOP STOREY ROOF" - so AOV.01 may be intended as a ROOF vent, and A Plus have quoted a wall window
on a 155mm subcill.** If so the quoted unit is the wrong product entirely. That is now C4.

**Gordon Court's NBS corroborates it from a third direction.** Their specification names, for this exact
duty, a *"STAIRWELL VENTILATOR... ROOF MOUNTED ONTO HORIZONTAL KERB... 1m2 geometric free area"* - the
same 1 m2, mounted on the roof - and specifies a separate, **different wall-mounted model** for a
different position. So the standard product for a 1 m2 stairwell vent is a roof unit on a kerb, not a
casement. Three independent pointers now: the note's own wording, the absent wall opening, and the
standard product for the duty. None is conclusive alone; together they make C4 the question that could
invalidate half the quote. **If AOV.01 is a roof vent, none of Part One applies to it and we should be
pricing a kerb-mounted unit.** Gordon Court have the same ambiguity live and cannot resolve it either -
their NBS specifies two roof units and one wall unit while the items actually quoted are wall units.

**THE WIDER POINT STANDS AND SHOULD STILL BE CONFIRMED.**
Gordon Court's schedules turned out to constrain ground and first floors to existing structural
openings while levels 2-3 were new build and free, so they warned to check it floor by floor. Run on
Riverside: **K1653-04 "EXISTING / PROPOSED ELEVATIONS" carries a single set of eight elevations
(A-H) showing a complete, regularly fenestrated building - no new opening is marked anywhere and no
AOV is drawn on any elevation.** That is not proof the openings are existing, but it is the whole of
what the pack says, and Adam's statement is the only source for "newly formed". Three consequences:

- If the openings are **existing**, enlarging them is structural - lintels, cutting masonry, making
  good - and none of that is in anybody's price.
- The drawings are stamped **24/02303/PAPCR**, a **prior approval** reference rather than a full
  planning permission. Prior-approval conversions normally carry tight limits on external alteration,
  so "as big as we need" may not be a free decision. One question to HD Planning settles it.
- **The second-floor vent may be in an ARCHED opening.** AOV.01's stairwell is in the central tower.
  On **Elevation F** that tower's top storey has **two arched-head windows**; on Elevation B it has
  three rectangular ones. A Plus have quoted a square-head 1130 x 1530 casement. If the vent lands in
  the arched face it is a different unit at a different price - and A Plus's own terms charge extra to
  glaze above a curved head.

All three are in the requote brief as C2, C3 and C4. Note he answered against the 1.5 m2, which turned out
to be ours rather than the client's; triage put the correction to him on the hub and asked him to hold
off Gintare until the basis is settled. His answer becomes exactly right *if* the basis is aerodynamic.
He asked for an email reminder - **email is still blocked**, so REQ-9 on the hub is the reminder.

### The variable that is still live: geometric or aerodynamic

QT51518 quotes **geometric only**. A Plus's QT51516 (Towcester Vale, same DualFrame 75Si AOV) states
both on every line - verified at source, not inherited:

| size | stroke | geometric | aerodynamic | ratio |
|---|---|---|---|---|
| 810 x 1335 | 900mm | 0.81 m2 | 0.49 m2 | 60.5% |
| 1205 x 1335 | 900mm | 0.87 m2 | 0.54 m2 | 62.1% |

On that ratio our 1.30 m2 geometric is roughly **0.78-0.81 m2 aerodynamic - about 20% short of 1 m2**,
and A Plus's proposed 1235 x 1583 would be ~0.9 m2 aerodynamic and would **also** miss. Indicative
only: different sizes, and a 900mm stroke against our 850mm. **A Plus must state the aerodynamic
figure for the actual Riverside sizes** (RFI-1) and the fire strategy must confirm which basis
applies (RFI-3). Do not treat the frame-area ratio as a shortcut - Towcester's own geometric/frame
ratios are 75% and 54%, so it does not scale.

**The evidence now points to geometric.** Two independent sources, both in our possession:

1. **The drawings name their own compliance route.** The key on K1653-10b/11/12 reads *"MAINS OPERATED
   INTERLINKED HEAT DETECTOR TO **AD B1**"*. Approved Document B is the prescriptive route and states
   common-stair smoke vents as a **free area**; **aerodynamic** free area is the language of the
   engineered BS 9991 / EN 12101-2 route, which this pack is not on. The note's own wording - an
   automatically openable vent of 1m2, fire-brigade operated from ground floor access level - is the
   AD B common-stair provision almost verbatim.
2. **Gordon Court's pack says it outright, for the identical duty.** NBS 9001 L20 cl.630: *"AXS140
   STAIRWELL VENTILATOR - throat dimensions 1250mm x 1000mm - **1m2 GEOMETRIC free area**"* (and the
   lobby ventilator at 1.5m2 geometric). A different architect, a different job, the same product class
   and the same number - stated as geometric. The word *aerodynamic* appears **nowhere** in that job's
   186-page NBS, 140-page mechanical spec or 127-page electrical spec.

So the recommendation is that **1m2 means geometric, the vents as quoted comply by 30%, and there is
nothing to requote**. It is a recommendation, not a ruling - the fire engineer or building control
confirms it. But it is now a well-evidenced one rather than a coin toss, and it is on REQ-9.

### The pack's revision table - Gordon Court's stale-document check, run on Riverside

| Sheet | Title | Date | Revision |
|---|---|---|---|
| K1653-03 | Proposed Layout, all three floors (the **planning** set) | Mar 23 | **B - 17.06.24** (A - 05.07.23) |
| K1653-04 | Existing / Proposed Elevations | Jun 24 | none |
| K1653-10b | Proposed Layout **Ground** Floor | Mar 24 | **B - Nov 25** (A - Nov 25) |
| K1653-11 | Proposed Layout **First** Floor | Mar 24 | **none** |
| K1653-12 | Proposed Layout **Second** Floor | Mar 24 | **none** |
| HD0-0197-01a | Location Plan (hd planning) | Aug 24 | a |

**The AOV requirement appears only on K1653-11 and K1653-12 - the two sheets that have never been
revised** - while the ground floor plan was revised twice in November 2025. Probably innocent: the
Nov 25 revisions were "Dental Lobby added" and "altered", a ground-floor commercial change that need
not touch upper floors. But the requirement has not been looked at since **March 2024**, and on Gordon
Court this exact pattern concealed a smoke shaft deleted five months before tender. **One line of
confirmation that K1653-11/12 are still current** - carried as C5 in the brief.

Note also the pack holds **two layout sets**: the planning sheet K1653-03 (all floors on one sheet,
Mar 23 rev B) and the construction-issue sheets K1653-10b/11/12 (Mar 24). The construction set is
later and is marked CONSTRUCTION ISSUE, so it governs - and it is the only set carrying the smoke-vent
note. K1653-03 does not carry it.

### WE ARE NOT WORKING FROM THE WHOLE PACK - and the missing sheets are the ones that matter

Gordon Court found their loose job folder held **25 of the 82** drawings in the tender zip, and the 57
absent included every floor layout, every existing plan and all three demolition plans. Run on
Riverside, which has no zip at all - everything arrived as email attachments and
`Commercial\1. Tender Documents\RRR\Riverside` **is still empty** (re-checked 27/07 late):

- **Numbering gaps.** We hold Campbell Ark's K1653-**03, 04, 10b, 11, 12**, plus hd planning's
  location plan. That leaves **K1653-01, 02, 05, 06, 07, 08 and 09** unaccounted for - seven sheet
  numbers against the five we have - and nothing tells us where the series ends.
- **Cross-referenced sheets that are not here.** The plans cite **DETAIL 1, 2, 4, 5 and 6** - verified
  at source: *"SEE DETAIL 4 FOR ACOUSTIC UPGRADE TO SECOND FLOOR"* and *"SEE DETAIL 6 FOR THERMAL
  UPGRADE TO ROOF"* on K1653-12, *"SEE DETAIL 1 / 2 / 5"* in the wall key, *"SEE DETAIL 4 FOR ACOUSTIC
  UPGRADE TO FIRST FLOOR"* on K1653-10b. Not one detail sheet is in anything we hold.
- **Whole document classes absent:** no fire strategy, no existing plans, no demolition plan, no
  sections, no window or door schedule.

**Duplicate-revision check (Gordon Court's third drawing-hygiene test, 27/07 late): CLEAN.** Their zip
holds superseded revisions beside current ones - 21005/6/7 at both rev 02 and rev 03, 21008 at rev 03,
rev 03(1) and rev 04 - and the annotation that answered their four-turn question exists **only** on
21007 rev 03. Reading the wrong copy would have hidden it. Riverside holds no duplicate sheet numbers:
three planning-portal PDFs (K1653-04, K1653-03 as "PROPOSED_LAYOUT", the location plan) and three loose
construction sheets (K1653-10b/11/12), all distinct numbers, one copy each. So the three tests now are
**gaps in the series, cross-references to absent documents, and duplicate numbers at different
revisions** - Riverside fails the first two and passes the third.

Most of that is probably not our scope. **The point is that the absent classes are exactly the ones
that answer our open questions** - proven on Gordon Court, where the demolition legend carried *"NEW
STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE"*, which is precisely the new-versus-existing
question we have against Adam's ruling, and where the fire strategy legend stated the duty in its own
words (*"AOV. 1.5m2 CLEAR OPENING AREA"*), which is precisely our geometric-or-aerodynamic question.

So the two documents worth asking for above all others are **the fire strategy (answers C1)** and
**the demolition / existing plans (answer C2)**. Both are now C0 and C2 in the brief, and C7 asks for
the drawing register rather than guessing further from numbering gaps.

### What A Plus's 1.30 m2 actually is - and it resolves RFI-2

The full inner frame aperture is **957 x 1357 = 1.2986 m2**, which is the 1.30 m2 stated (1357 = 1530
less two 86.5mm frame sections, 86.5 taken from the 957 daylight width). So A Plus's "geometric free
area" is the **clear opening of the whole frame** - which means the entire frame opens as one
bottom-hung leaf, with the 176mm transom acting as a glazing bar within the sash rather than dividing
a fixed pane from an opening one. That matches the original objection that an 850mm chain cannot act
on a 590mm-high aperture. Carried as a confirmation rather than a question in brief item 5.

It also answers Gordon Court's ratio flag - and **that flag has since been withdrawn by its author,
so do not re-adopt it.** They proposed dividing the required free area by the GROSS frame area and
querying anything much above ~60%. A Plus's quoted 1.30 is 75% of gross, which looks high until you
notice it is **100% of the inner aperture**. Recomputed on the aperture, Gordon Court's own WN_7 went
from "cannot reach 1.5 m2" to 99.3% of it - short by 0.01 m2, i.e. marginal rather than incapable -
so the gross-frame test would have condemned a borderline unit. **The aperture is the real ceiling
and the right denominator.** Riverside's requirement is 1.0 / 1.729 gross = 57.8%, or 1.0 / 1.2986
aperture = 77% - comfortable either way. One caveat carried from their correction: an aperture is
usually *inferred* from a nominal section depth unless the supplier states it, so it is an estimate
too. The clear opening is the manufacturer's figure to give.

**Gordon Court then quantified that caveat and it deserves an honest answer, because their number
does not transfer here.** They varied only the assumed outer section on WN_7: 65mm gives 101.1% of
the duty, 70mm gives 99.3% - so **±5mm on a nominal section swings the answer clean across the
compliance line**, and their 99.3% is an estimate whose error bar swamps its own margin. Correct, and
neither of our aperture percentages is a compliance test.

But the direction of inference is opposite on Riverside, which makes it far less fragile. They are
**predicting an unstated** clear opening from an assumed section. I am **reconciling a stated** figure:
A Plus published 1.30 m2, and 957 (their own stated daylight width) x 1357 reproduces it to 99.9%.
Only the vertical is assumed - head+cill = 2 x 86.5 - and the stated figure constrains it:

| assumed head+cill | inner height | area | vs stated 1.30 |
|---|---|---|---|
| 150mm | 1380 | 1.3207 | 101.6% |
| 165mm | 1365 | 1.3063 | 100.5% |
| **173mm (assumed)** | **1357** | **1.2986** | **99.9%** |
| 180mm | 1350 | 1.2919 | 99.4% |
| 200mm | 1330 | 1.2728 | 97.9% |

A ±25mm swing moves it ±1.9%, and there is no line to cross - the test is whether the reconciliation
holds, and it does across the whole plausible range. So the **configuration** conclusion (whole frame
opens as one bottom-hung leaf) is robust. It remains an inference until A Plus confirm it, which is
brief item 5.

### The requote brief - written and ready either way

`outputs\Riverside House - A Plus requote brief (for Gintare).txt`. Built deliberately so that **one
email settles the job whichever way the basis falls**: it asks A Plus for the aerodynamic figure at the
size already quoted *and* for a size that achieves 1.0 m2 aerodynamic with both figures stated, plus
the actuator change if the vent grows, the whole-window Uw, the vent leaf, delivery and a price hold.
A Plus stated both free-area figures on QT51516 three days earlier, so none of it is new work for them.
It also tells them **not** to size to 1.5 m2. Mary cannot email suppliers - this goes via Adam/Gintare.

## Open items

| # | Item | With |
|---|---|---|
| RFI-1 | A Plus to state **aerodynamic** free area for 1130 x 1530 at 850mm stroke | A Plus (via Adam/Gintare) |
| RFI-2 | A Plus to confirm vent leaf, rail and actuator position on shop drawings | A Plus |
| RFI-3 | Is the 1 m2 geometric or aerodynamic? And where did 1.5 m2 come from? | Client / fire strategy |
| RFI-4 | **Who is carrying the AOV control system?** | Client / PHDB |
| RFI-5 | Cill height above FFL at each vent; 155mm subcill acceptable against the 150mm asked | Client |
| RFI-6 | Whole-window Uw - does the drawings' 1.6 bind the stair AOV? | A Plus / client |
| RFI-7 | Delivery - confirm charge or that the load is batched free | A Plus |

**REQ-9 on the hub has been rewritten** to ask the real question. Its old premise ("1.30 against 1.5,
the answer is NO") is superseded.

## Things that will bite if forgotten

1. **Nobody is carrying the AOV control system.** The drawing requires fire-brigade operation from
   ground floor access level - a smoke control panel, mains + battery supply, cabling, containment,
   override, commissioning, EN 12101 documentation. A Plus fix the actuator, test on local batteries
   and leave ~2m of flex coiled at the vent; that is where they stop. It is excluded from our price
   too. **The window alone cannot satisfy the note.**
2. **Delivery is not free - and it does not reach site.** A Plus's Job Spec line says "Glazed /Supply
   Only (Delivered)" but their terms say "All orders are priced as Ex-Works" and only deliver FOC above
   **GBP 5,000 ex VAT** within 50 miles of Watford. Our order is GBP 4,845.22 - **GBP 154.78 under**.
   Below that they batch or charge GBP 1/mile each way. Carried as provisional. A resize over
   GBP 5,000 removes it.
   **And the destination is our own yard.** QT51518 carries **no site address at all** - the only
   address on it is Fenster Glazing & Locks Ltd, 97-98 Alston Drive, Bradwell Abbey, **MK13 9HF**. So
   "Delivered" ends in Milton Keynes, not Aylesbury, and **the onward leg to HP19 7HL is ours and is
   not in the GBP 5,990.22**. A Plus also require "suitable labour at the delivery point to unload".
   Found by taking Gordon Court's tip that all five of their supplier quotes deliver to the same yard -
   worth running on every supplier quote.

2b. **The quote IS for a ventilator, not a window** - Gordon Court's test, run and passed. QT51518
   carries "AOV Type 850mm Stroke Single", "AOV Cable Direction", "AOV Colour 9006 Satin", a dedicated
   AOV Notes page and the SE Controls actuator warranty, at **GBP 1,401.24/m2** against GBP 528.83/m2
   for a plain glazed aluminium window in the same band. Gordon Court's BSW quote failed the same test:
   3no WN_7 at GBP 412.67/m2 and 4no WL_1 at GBP 442.98/m2 with zero occurrences of AOV, actuator,
   chain, stroke or 24V - they had priced windows where the spec wanted Colt ventilators. **Before
   comparing free areas, confirm the quote is for a ventilator at all. The rate is the tell.**
3. **Zero validity headroom, and it will go negative.** Our price (30 days from a 27/07 document) and
   A Plus's both close on **26/08/2026** - the same day. Since Adam is deferring issue until PHDB
   report, our 30 days will run past the day the cost behind it lapses.
4. Actuators are **not** restrictors; A Plus disclaim liability for damage without one fitted 50mm
   beyond the stroke. Not priced.
5. Trap hazard under BS EN 60335-2 below 2.5m FFL; Part K anti-fall below 1100mm FFL, which A Plus
   exclude. 24v DC only. 15,000 cycles or 12 months warranty.
6. **The wider scope.** The pack is a full flat conversion: the key defines W1 escape windows, W2
   windows at U 1.6, and D1 FD30s flat entrance doors / D5 external glazed door, appearing right
   through all three floors. We are pricing 2 vents out of that. Raised with Adam as an opportunity.
7. **The mail channel to Adam is blocked.** `mary_send.py` returned
   `403 ErrorAccessDenied - Blocked by tenant configured AppOnly AccessPolicy settings` on 27/07.
   The reply is written and saved in `outputs\` for a human to send; the substance is on the hub
   instead. Not previously recorded anywhere - see the noticeboard.

## Checks

`python scripts\mary_checks.py data\job-checks\riverside-house-aov.json` - 0 failed, **3 questions**
(free-area basis, validity headroom, delivery). Nothing goes to RRR Group until those close.

This job founded two rules, fixture `_test-riverside.json`:
- `check_free_delivery_threshold` - a quote that says "Delivered" can still put carriage on us.
- the thin-margin arm of `check_quote_validity_against_commitment` - a supplier quote expiring the
  same day our price closes passes "held as long as ours" and is still no use.

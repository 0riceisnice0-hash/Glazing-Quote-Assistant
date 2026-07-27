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

- `outputs\Riverside House - Fenster Pricing Document (house format).xlsx`
- `outputs\Riverside House - AOV Smoke Vent Drawings.pdf` (2 sheets, Rev A)
- `outputs\Riverside House - Reply to Adam (draft).txt` - **written but NOT SENT, see below**
- `outputs\Riverside House - A Plus requote brief (for Gintare).txt` - ready to go on Adam's word
- `data\job-checks\riverside-house-aov.json` + fixture `_test-riverside.json`
- Generator: `scratchpad\riverside_drawings.py`; job json `test-results\riverside-run\`
- Quote: `test-results\mary-inbox\processed\20260727T0842-xgnwAAAA-att\Quotation_QT51518.PDF`
- Pack: `test-results\mary-inbox\processed\20260727T1500-xgqQAAAA-att\` (6 drawings + 2 logo images)

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

*Inference, not proof:* it rests on the elevations being a single unchanged set. The existing plans
and demolition plan would confirm it, and neither is in our possession - which is the C2 ask.

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

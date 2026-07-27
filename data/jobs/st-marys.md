# St Mary's Refurbishment, Merthyr Tydfil - E T & S Construction

> ## THE PACKAGE IS RE-OPENED. RETURN DATE **27 JULY 2026** - TODAY. **REQ-25.**
>
> ET&S's Document Register issued with the 24/07 revised drawings carries
> **"Package return date: 27 July 2026"** in its header. The 08/07, 09/07 and 16/07 registers all say
> **17 July 2026** - same package, same package lead (Tom Godfrey). **The 24/07 re-issue moved the
> deadline out by ten days.**
>
> | register | generated | package return date |
> |---|---|---|
> | original-08-07 | 7/8/2026 08:45 | 17 July 2026 |
> | schedule-09-07 | 7/9/2026 08:49 | 17 July 2026 |
> | pci-16-07 | 7/16/2026 11:43 | 17 July 2026 |
> | **revised-24-07** | **7/24/2026 12:10** | **27 JULY 2026** |
>
> We submitted on 17/07 and have treated this as closed and awaiting award ever since. **REQ-5 was right**
> that the addendum changed no scope - it was checked attribute by attribute across the drawings, and the
> return date is in the **register header**, not the drawings. I read that register three times over six
> turns without reading the top of the page.
>
> **If the package really is open until close of play, everything in this file stops being a post-mortem
> on a submitted quote and becomes a corrected tender.** Somebody must establish it with Tom Godfrey
> today - Mary cannot: outbound email is down (REQ-23) and only ever reached adam@/marketing@.
>
> **And our own recorded deadline was never a client date.** The hub carried 16/08, which is the
> BSW/Bellview 30-day quote validity - it had become "the deadline" because it was the only date written
> down. Now corrected to 27/07.


Chat key `st-marys`. Opened by triage 27/07/2026. This file is the backup for this chat's memory.

---

## 1. The job

| | |
|---|---|
| Project | St Mary's Refurbishment to accommodate a special needs school |
| Real name on the ITT | **Blessed Carlo Acutis Catholic School (St Mary's Campus)**, refurbishment *for Greenfield Special School* |
| Site | Caedraw Rd, Merthyr Tydfil, **CF47 8HA** |
| Our client | E T & S Construction (FAO **Tom Godfrey**) - we are their glazing sub-contractor |
| End client | Merthyr Tydfil CBC, Property Services (prepared by **Chris Evans**, ref 2026-024) |
| Architect | cfw architects, Cardiff - drawing series **2376** |
| Job folder | `Commercial\1. Tender Documents\E T & S Construction\St Mary's Refurbishment` |
| Tender pack | `test-results\st-marys-input` - `original-08-07`, `schedule-09-07`, `pci-16-07`, `revised-24-07` |

**Our documents say CF77 8HA. The client's ITT, prelims and SOW all say CF47 8HA.** CF77 is not a
Merthyr postcode. It is on the issued pricing document (cell B5) and the proposal. Correct it on the
next revision - it is small, but it is on a client-facing document.

## 2. Where the money is

**QUOTE SUBMITTED 17/07/2026 (documents dated 16/07): GBP 174,546.37 ex VAT.** Still stands.

| | GBP |
|---|---|
| 31 Sheerline Prestige window type lines, 98 units | 121,712.33 |
| 7 SMA lines (Smart Wall Pocket doors/screens + MC600 Plus curtain walling), 9 units | 30,919.00 |
| **INSTALLATION** (single global line) | **21,915.05** |
| **TOTAL ex VAT** | **174,546.37** |
| *optional* external mastic | 2,808.10 |
| *optional* EPDM | 5,028.61 |

107 units, **202.80 m2**. Biggest line **Type AK**, 1825 x 5580, 2 no @ GBP 8,655.98 = GBP 17,311.95.

**Supplier cost GBP 91,409.18** -> gross margin GBP 83,137.19 (47.6% of sell, before install cost).

### The supplier backing - CORRECTED

The handover record and triage's opening note both say the backing is *"BSW QT252799 and Aplus QP70172"*.
**That is wrong and it matters.** Verified against the workbook:

- **BSW QT252799**, 15/07/2026, Total Nett Ex VAT **GBP 61,056.80** - Sheerline Prestige casements.
- **Bellview Products 0000000483**, 16/07/2026, Net GBP 35,708.68 less 15% = Grand Total Net
  **GBP 30,352.38** - the 7 SMA lines.
- 61,056.80 + 30,352.38 = **91,409.18 exactly.**

**Aplus QP70172 is NOT in the price.** It is dated **22/07** - five days *after* we submitted - it is a
different system (Technal NEXT FZ75 / STII / Tental 50, not Sheerline/SMA), and it is quoted
**UNGLAZED** ("to accept 28mm - 32mm units"). It is an unused alternative. Anyone reordering against it
would be buying a different job with the glass missing. *(Stoke Park rule: check which quote the price
was actually built on.)*

### Arithmetic - fully reconciled, nothing wrong with it

Checked line by line, and it is clean:

- All **31 window types**: quantity and line total match BSW QT252799 **exactly**, all 31, zero variance.
- All **7 SMA lines**: match Bellview at the **discounted** figure, to the penny (e.g. Type AK
  GBP 5,199.89 x 0.85 = GBP 4,419.9065).
- Unit rates follow the house template exactly: supply + (code value x 75%). Verified on MAW, ELAW, LAW,
  SAW, SAD, DAD, SADMAW and CW.
- **INSTALLATION GBP 21,915.05 reconciles to the penny** as the sum of the house labour codes.
- Brocks Hill quantity rule: **39 lines, every unit sold has a supplier quote behind it.**

## 3. What I found - open items

### RFI-1 (COMMERCIAL, biggest) - the U-value the pack asks for is not the one we promised

The tender pack contradicts itself and we followed the looser side.

- **Window schedule 2376-09** states, against each window type (33 notes): *"achieve u value of 1.4 w/m2k"*.
- **EDG02 Energy and Carbon Design Guidelines - Building Fabric**, in the same 08/07 pack, sets
  *Minimum Performance Value* for the **Refurbishment** column:

  | Element | Required |
  |---|---|
  | Windows (double glazed) | **1.3 W/m2K** |
  | External Doors | **1.2 W/m2K** |
  | Glazing thermal performance (**g value**) | **0.4 - 0.3** |
  | Air permeability | <3.5 m3/h.m2 |

- **Our proposal promises 1.4 W/m2K** - which satisfies the schedule and misses EDG02 on both counts.

Worse, **neither supplier states a U-value at all**:

- BSW QT252799 - zero occurrences of "U value", "Uw" or "W/m2K". The only thermal evidence is the glass
  make-up **"6.8 Lam/18/4mm Clr Tuff EcoPlus 1.0"** - a centre-pane Ug of 1.0. A glass Ug is not a
  whole-window Uw.
- **Bellview 0000000483 - nothing. No U-value, no low-E, no soft coat, no argon, no warm edge, no
  coating of any kind.** Just "6.8 Lami / 4mm Tuff" on all 9 door and curtain-wall units. That is
  **GBP 30,352.38 of supply, 33% of our cost**, including the 20.37 m2 of MC600 curtain walling,
  with no stated thermal performance against a 1.2 W/m2K door requirement.
- Aplus's own advisory notes put the industry default in writing: *"Commercial doors and framing will be
  supplied with a U-Value of up to 3.0 W/m2/K."*

And **nothing in either quote is a solar control product** - zero hits for solar, g-value, Suncool, SKN,
Coolite or Planitherm. "Clr" means clear. A clear low-E DGU runs a g-value around 0.6 against the
0.4-0.3 EDG02 asks for. *(Georgie's rule: if a quote does not name the coating, assume it is not there.)*

**Ask ET&S: does EDG02 apply to our package, or does schedule 2376-09 govern?** If EDG02 applies, the
glass specification changes on all 107 units and the price moves. Do not guess this one - and note the
SM5 Wexham correction, that a U-value can be a package average rather than a per-element limit. The only
U-value calculation anywhere in the folder (Aplus, avg Uw 1.37 over 210.2 m2) is an average, and it is
for **Technal frames we did not buy**. It is not evidence for what we sold.

#### RFI-1a - and if EDG02 does apply, the doors are a SYSTEM problem, not a glass problem (28/07 finding)

This is the part that cannot be fixed by changing the glass, and our own records already settle it.

**HANDOVER.md, SM5 Wexham (22-24/07), found in writing:** *"the SMA Smart Wall Pocket doors cannot meet
the drawing's whole-installation U-value 1.6 - non-thermally-broken shopfront system... Fix =
thermally-broken door (Smart Alitherm 600 / MC600 door) with 28mm argon low-E units + SMA U-calc in
writing."*

**St Mary's has the same system against a tighter number.** Bellview 0000000483 quotes **positions
001-006 as "System: SMA Smart Wall Pocket"** - that is **6 door types, 7 units, 22.078 m2, SELL
GBP 31,360.15**. EDG02 asks **1.2 W/m2K on external doors**. SM5 Wexham says this system could not reach
**1.6**. A non-thermally-broken aluminium frame is the dominant heat path, so better glass does not
rescue it.

Position **007 is different** - *"System: SMA MC600 Plus Standard"*, the Type AK curtain walling, 2 units,
20.367 m2, sell GBP 17,311.95. MC600 is thermally broken and is the system SM5 Wexham named as part of
the *fix*. **Do not lump the two together** - the curtain walling is probably fine and the doors are not.

On the glass, both differ from the windows in the same way. The **glazing bead is 28mm** on positions
001-005, so these *are* genuine 28mm double glazed units - the SM5 Wexham "no cavity at all" criticism
does **not** apply here. What is absent is everything that makes a 28mm unit perform: **no low-E, no soft
coat, no warm edge, no gas fill named**, against BSW's windows which spell out *"EcoPlus 1.0 **Black Warm
Edge** Sp 18mm"*.

**This is the fifth instance of this exact pattern in a month** - Technal/Modeal on Princess Beatrice,
Senior on Vesuvius, Aluprof on Filwood, Smart Wall triple glazing on Brocks Hill, and now Smart Wall
thermal performance here.

#### RFI-1a CONFIRMED WITH SMA'S OWN PUBLISHED FIGURES - and the doors fail under EITHER reading

**SMA's own Smart Wall datasheet states the numbers.** It reached us by accident on 27/07 at 15:56,
attached to a completely unrelated enquiry (John North Hall, High Wycombe - a Neil Douglas ITT for
communal entrance doors that also specifies Smart Wall). File:
`test-results\mary-inbox\queue\20260727T1556-xgsAAAAA-att\SMA Smart Wall Profile.pdf`. It says:

> *"Smart Wall is a thermal shop front screen and door system... ideal for use in schools, colleges and
> other educational buildings."*
> - **U Value 1.8 W/m2K for Smart Wall DOORS**
> - **U Value 1.4 W/m2K for Smart Wall SCREENS**
> - LPS 1175 Level 2 / BS EN 1627 Level 3 enhanced security

**This settles the door question without waiting for REQ-15.** Our proposal promises **1.4 W/m2K across
the package**. SMA's published figure for their own doors is **1.8**. So:

| requirement | source | SMA published door figure | verdict |
|---|---|---|---|
| **1.2 W/m2K** external doors | EDG02 | 1.8 | **fails by 0.6** |
| **1.4 W/m2K** | window schedule 2376-09, and our own proposal | 1.8 | **fails by 0.4** |

**The doors miss under BOTH readings of the specification.** REQ-15 asks ET&S whether EDG02 or the
schedule governs - on the *windows* that still matters, but on the *doors* it no longer does. Whichever
answer comes back, **the proposal's promise of 1.4 W/m2K is not met by the door system we have priced**,
and that is now backed by the manufacturer's own literature rather than inference.

Three honest caveats before this is put to anyone:

1. The datasheet says **"Smart Wall"**; St Mary's is **"Smart Wall Pocket"** (the word "Pocket" does not
   appear on the sheet). Pocket may be better or worse - **confirm which figure applies to Pocket.**
2. 1.8 presumably assumes a particular glazed unit. **Ours names no coating, no warm edge and no gas
   fill**, so ours could be worse than 1.8, not better.
3. Type AK is **MC600 Plus**, a different system the sheet does not cover. Still unquantified.

**A useful secondary point in our favour:** Smart Wall carries **LPS 1175 Level 2 and BS EN 1627 Level
3**. Schedule 2376-09 carries **38 Secured by Design notes** and neither BSW nor Bellview stated any
security certification. This is the first evidence that the SBD requirement is satisfiable on the door
elements - worth citing when that question is put.

**Still needed: an SMA U-calculation in writing for the actual units**, which is precisely what SM5
Wexham asked for and never got. But we now know roughly where it will land, and it is not 1.4.

#### RFI-1b - the door schedule 2376-08, which nobody had read, both STRENGTHENS and CORRECTS the above

Read 2376-08 for the first time on the third turn. It changes the picture in one important way and
confirms it in another. **It is the original 08/07 issue with an empty revision block** - unlike the
window schedule, which went to rev A on 13.07.

**THE CORRECTION - and it is the SM5 Wexham trap I nearly walked into a second time.** The door schedule
carries a general note against D.11:

> *"External Doors U-value 1.2 w/m2k. **Note this is an area weighted average u-value - not a centre pane
> value.**"*

So the 1.2 for external doors is **an average across the door package, NOT a per-element limit**. My
manifest previously recorded the basis as "per element" throughout. That was wrong for the doors and is
now corrected. Under the SM5 Wexham rule you may not reject a single element against an average.

**THE FINDING SURVIVES THE CORRECTION - because the average was computed, not asserted.** Our external
door area is **22.078 m2 of Smart Wall Pocket** plus at most **20.367 m2 of MC600** = 42.445 m2. With
SMA's published 1.8 on the Smart Wall Pocket area:

| if MC600 achieves | area-weighted average | vs 1.2 required |
|---|---|---|
| 1.4 | **1.61** | misses |
| 1.2 | **1.51** | misses |
| 1.0 (generous) | **1.42** | misses |

For the average to reach 1.2, MC600 would have to achieve **0.55 W/m2K** - which no glazed element
achieves. And if MC600 is *not* in the External Doors pool, the Smart Wall Pocket average is simply 1.8.
**The doors miss on the architect's own averaging basis, not merely on a per-element reading.** That is
a far more robust position to put to ET&S than the one I had yesterday.

**THE STRENGTHENING - a third independent source for 1.4.** 2376-08 also carries **per-door** notes on
**D.01, D.17, D.22 and D.26**: *"Door to achieve min u-value of 1.4W/m2k"*. These are stated per element,
so SMA's 1.8 misses them outright. The 1.4 requirement is therefore in **the window schedule, the door
schedule and our own proposal** - it does not depend on EDG02 at all, and ET&S cannot dispose of it by
ruling that the energy annex does not apply.

#### RFI-7 (NEW) - the door schedule requires things that are in nobody's price

Four items in 2376-08 that appear in neither BSW nor Bellview:

1. **FOBBED READERS ARE EXPLICITLY REQUIRED, on named doors.** D.01 note 5 reads *"fobbed reader"*, and
   D.14 the same. Our proposal excludes *"Fobbed readers, access control, fire alarm interfaces, wiring,
   programming, commissioning"* and the clarifications say *"fobbed reader compatibility requires further
   review"*. **That review was never done.** Even if the access control system is MTCBC's under SOW
   15.10, the door leaf and frame need preparing for it - cabling routes, transfer hinges, an electric
   strike or keep. **Bellview's quote contains no electric strike, no rectifier and no transfer hinge on
   any of the 7 door units** (Bellview price those separately when asked - on Filwood they quoted an
   electric strike + latch + rectifier as a line item). Decide whether the preparation is ours and get
   it priced or excluded by name.
2. **ANTI-LIGATURE IRONMONGERY IS SPECIFIED AND NOT QUOTED.** The external door ironmongery schedule
   requires *"Anti-Ligature Infilled Door Pull Handle on Plate - Screw Fix - 300 x 75mm - Stainless
   Steel"*, *"Hinges: satin stainless steel concealed bearing to BS 7352"* and *"Kicking plate: satin
   stainless steel 200mm high"*. Bellview's 7 units list only concealed panic bars and closers. On a
   **special needs school** anti-ligature is a safeguarding requirement, not a finish preference.
3. **"NO LOCKING MECHANISM OR LATCH" CONFLICTS WITH THE PANIC BARS WE HAVE PRICED.** D.01, D.17, D.22 and
   D.26 all say *"No locking mechanism or latch"* or *"Non-lockable device"*. Bellview quoted
   **ACIM453 concealed panic bars on all 7 units** - a panic bar is a latching device. **Aplus spotted
   the same ambiguity and said so in writing** on their alternative: *"It is unclear what a Non-Lockable
   Device is, quoted all doors with Panic Bars."* Two suppliers defaulted the same way and only one
   flagged it. The architect has to say what a non-lockable device is on an escape door.
4. **THE TWO SCHEDULES GIVE DIFFERENT SIZES.** 2376-08's external door structural openings do not
   reconcile to what we priced from 2376-09: D.17 is 955 x 2100 + 470 = **2570** where Type L is
   955 x **2410**; D.22 is 1530 x 2100 + 170 = **2270** with no priced equivalent; D.26 is 930 x 2100
   where Type U is 929 x **2370**. Only D.01 (1530 x 2100 + 310 = **1530 x 2410**) matches Types I/O
   cleanly. 2376-09 rev A is the later document and presumably governs, but **two architect's schedules
   disagreeing on the same openings needs settling before manufacture** - and D.01 is also the
   *"4 panes bi-folding"* door, which is the bifold our proposal substituted for commercial French doors.

#### Two things I checked and cleared - do NOT raise these

- **"Making good" is NOT in our item.** Triage's John North Hall note warned that replacement jobs put
  strip-out, making good and disposal in scope. On this job only the strip-out cross-refers to 6.01
  (item 1.09, RFI-4). Making good and decoration are carried separately by MTCBC as **SOW section 8**
  (8.01 rub down and prepare existing walls, mist coat and two coats) and 9.06 skirtings. Our
  "Internal Finishing" exclusion is consistent with the SOW structure. **RFI-4 stands as-is; do not
  widen it.**
- **There is no tender validity requirement in this pack.** Zero hits for validity, remaining open or a
  price-hold period across the prelims and the SOW - so the 90-day Section 20 trap that bit John North
  Hall does not apply here. Our exposure is the one already recorded: quotes lapse mid-August against a
  14/09 start.
- **The SMA commercial brochure does not close the 1.8 caveats.** It is a 2009 corporate brochure with
  **no U-values at all**; it never names Smart Wall, Pocket, MC600 or Alitherm 600. It does describe the
  "MC Wall" curtain wall as a *"polyamide thermal break system"*, weak corroboration that the MC600
  family is thermally broken. **Only SMA can confirm the Pocket figure and the MC600 figure.**

#### What the EDG02 uplift would cost - benchmark only, and the spread is wide

Priced through the rate register so REQ-15 arrives with a number rather than a question. `data/supplier-rates.json`
carries **matched "incl solar control (SKN/Coolite)" categories against plain ones**, same supplier, same
product, same size band - so the coating uplift can be measured rather than guessed:

| basis | figure |
|---|---|
| median of 10 matched pairs | **+GBP 43.37/m2** (+13.2%) -> GBP 8,795.61 over 202.80 m2 |
| band-matched to our actual units | **GBP 16,489.26** (blended GBP 81.31/m2) |

**Treat that as a range of roughly GBP 9,000 - 16,500 of SUPPLY cost, not a price.** Three honest caveats:

1. The band-matched figure is driven by BSW's `<1.5m2` (+GBP 175.22, 598 plain vs 39 solar lines) and
   `1.5-3m2` (+GBP 145.69, 446 vs 9) bands. The first is well supported; the second rests on 9 lines.
2. Several pairs are noise - BSW `3-6m2` has **one** solar line (+GBP 8.88), and two pairs come out
   **negative** on a single line each. Solar-control quotes may also carry other premium features, which
   would overstate the coating on its own.
3. **46.17 m2 - 23% of the job - has no matched pair at all** (Types F, H, G, I, O, AF).

It corroborates independently: Filwood's board note put the spec uplift at **GBP 45/m2** and the median
here is **GBP 43.37/m2**. But this only covers the **g-value**. It does **not** buy a 1.2 W/m2K door -
see RFI-1a. The real answer is a re-quote from BSW and Bellview with a coating and a stated Uw; the
numbers above exist only to tell Adam the order of magnitude before he decides whether to chase it.

### RFI-2 (TECHNICAL) - Type G puts a Sheerline window inside a Smart Wall frame

This is the SM5 Wexham founding error, live on this job.

- Schedule 2376-09, **Type G / W.24**, 968 x 3620, 2 no: *"opening pattern - 1 no. top hung + 1 no. fixed
  glazing + 1 no. external door"*, with a 100mm restrictor openable area.
- **Bellview pos 001** quoted *"a Single Pivoted Anti Fingertrap Door and **two Fixed Fields**"* -
  glazing *"**1 x prepared for a thickness of 28mm**"* + 3 x 6.8 Lami/4mm Tuff. The **top-hung opening
  vent is not in the Smart Wall element**; an aperture was left for it.
- **BSW QT252799** fills that aperture: *"Qty: 2 Prestige Casement Location: **TYPE G INSERT** GBP 697.58"* -
  an 854 x 900 **Sheerline** opening casement with Yale Shootbolt, hinge protector and friction hinges.

So a **Sheerline (70mm)** casement is to sit inside an **SMA Smart Wall Pocket (100mm)** frame, in a
pocket prepared to receive a **28mm** glazed unit. On SM5 Wexham (24/07) BSW ruled in writing that
Sheerline cannot be coupled to Smart Wall - there is no coupler between the depths. A 70mm window frame
does not go into a 28mm glazing pocket either.

**Get BSW and Bellview to confirm in writing how Type G is actually made before order.** It is
GBP 697.58 of cost but **2 no. Type G = GBP 8,499.66 of sell**, and if the answer is "it can't be", the
opening vent has to come from Bellview in Smart Wall and the element is repriced.

### ADAM'S RULING ON RFI-3, RFI-4 AND RFI-5 - REQ-17 ANSWERED AND CLOSED (27/07 19:42)

Hub message 31, verbatim:

> *"Our proposal document should state that we have not allowed for any access. Strip out is something
> we need to clarify in future tenders. We have effectively left it unanswered however we would include
> it for a job of this size, but if they assume it's not included and do it for us then happy days. We
> can allow the manifestation for a job of this size, however we should be putting this in our
> inclusions or on our description."*

It reached us via the `gordon-court` chat, which is where the hub delivered it. **REQ-17 is closed.**
All three are now actions, and two of them cost money:

| | ruling | where it leaves us |
|---|---|---|
| **Access** | proposal must SAY we allowed no access | wording already correct - **but he settled what our document says, not who pays.** See below. |
| **Strip-out** | *"we would include it for a job of this size"* | **not in the GBP 174,546.37**, 107 openings / 202.80 m2, no rate anywhere |
| **Manifestation** | allow it, and state it in the inclusions/description | **not in the price**, now measured at **24.10 linear m**, no rate anywhere |

**THE MONEY.** Neither is in the sold price, and the install line cannot absorb them - GBP 21,915.05
reconciles to the penny as per-unit fit labour, which is fit-only money with no slack in it. Gordon
Court reached the identical conclusion on their own install line. **Neither has a rate anywhere in
`data/supplier-rates.json` - 0 of 80 categories cover strip-out, disposal or manifestation** - so
neither can be benchmarked and both need a real price. **REQ-24 raised** and replied to Adam on the hub.

**MANIFESTATION EXTENT, now measurable rather than "undefined"** (clause 2.24: two bands at 850-1000mm
and 1400-1600mm, contrasting, both faces):

| scope | linear metres of band |
|---|---|
| **core** - the 9 glazed door and screen units (Types G, I, L, O, U, AF, AK) | **24.10 m** |
| plus Types F and H, the two 3,620mm screens | +15.80 m |
| **if both** | **39.90 m** |

Clause 2.24 says *"glazed entrance doors and glazed screens"*, so whether the silled 3,620mm windows
count is the one judgement left. **Quote the core 24.10 m and price F/H as an option.**

**THE PART OF THE ACCESS ANSWER THAT IS STILL MISSING.** Adam has told us what our document should say,
and it already says it. He has **not** said who pays. Prelims F and B require the Contractor to provide
all scaffolding *"for himself and any Sub-Contractor"*, we install up to **5,580mm**, and **55.97 m2 of
glazing is 3.62 m or taller**. An unqualified exclusion is a negotiating position, not an agreement, and
on a JCT MW with **GBP 500/day** delay damages it gets argued on site. Put to Adam as **REQ-24**.

### RFI-3 IS WITHDRAWN - I READ THE OBLIGATION AND NOT WHO IT FELL ON (corrected 27/07)

**The access finding below was wrong, and I broadcast it.** Prompted by `gordon-court`, who found the
same question on their job and answered it by reading for the **actor** rather than the obligation.

Re-read at source, `2, 3, 4 - SOW St. Marys.xlsx`, sheet `2. Prelims`, clause **B**, rows 180-181:

> *"The Contractor is to provide all scaffolding, temporary lighting and clearing away, making good
> **for himself and any Sub-Contractor**."*

The pack uses **"the Contractor"** throughout as the single actor above both **"Sub-Contractor"** (r181)
and the trades (r222), and distinct from **"the Employer"** (r5, r209). **This is the main contract
between MTCBC and ET&S** - so "the Contractor" is **ET&S**, and Fenster is the Sub-Contractor it must
provide scaffolding **for**.

**So our exclusion of Access/Lifting Equipment is CONSISTENT with the head contract, not exposed by it.**
Same conclusion gordon-court reached from jLiving's Works Information on their job. **I quoted the very
sentence that disproves my reading and drew the opposite conclusion from it.**

**The residual, which is much smaller than what I claimed:** the head contract binds MTCBC and ET&S, not
us. **ET&S's own sub-contract order to Fenster is a document we do not hold** and could still push access
down. That is worth one reserving line in the proposal, not the argument-on-site I described. Adam's
drafting rule ("state that we have not allowed for any access") stands and is unaffected.

*Kept below unchanged as the original text, so the correction is visible rather than tidied away.*

### RFI-3 (SUPERSEDED - see above) - we excluded the access plant the preliminaries require

Straight Filwood pattern, and here the pack says so explicitly.

- Proposal p4 **EXCLUDES** *"Access/Lifting Equipment - Scaffold, MEWPS, Towers, Forklift etc."* while
  p4 **INCLUDES** *"Installation - Installation is included within our costs"*.
- **Prelims F, INCLUDE EVERYTHING NECESSARY:** *"The Contractor is to include in his price for all items
  necessary to complete the works and is to provide all materials, labour, **scaffolding**, plant, tools,
  carriage and everything else necessary."*
- **Prelims B, SCAFFOLDING:** *"The Contractor is to provide all scaffolding, temporary lighting and
  clearing away, making good **for himself and any Sub-Contractor**."*

We are installing elements up to **5,580mm** tall. **55.97 m2 of glazing is 3.62 m or taller** (Types F,
H, G and AK, 8 units). None of it is reachable from the ground. Prelims B arguably puts the scaffold on
ET&S as main contractor - but our exclusion is unqualified, so the boundary is undefined and it will be
argued on site. **Settle in writing who provides access for our installation.**

### RFI-4 (SCOPE) - strip-out of the existing windows may be ours

**SOW item 1.09:** *"Remove doors and windows; load into skip; existing window structures and prepare
opening to receive new **(allowed in 6.01)**"*. Item **6.01 is our line** - "Supply and fit new external
windows and doors". So MTCBC have allocated removal and disposal of the existing windows *into the same
item as our supply and fit*.

Our proposal excludes *"Waste Removal - generally excluded"* but **never names removal or disposal of the
existing windows**. On 107 openings that is not a rounding error. *(Grange Hill rule: a silent gap reads
as included.)* Confirm with ET&S whether strip-out sits with them or with us.

**AND THE DISPOSAL DUTIES THAT COME WITH IT** (found 27/07 in the same prelims sweep that corrected
RFI-3 - Prelims **B** and **C**, rows 253-278):

- A **Site Waste Management Plan (SWAMP), Appendix A**, must be *"fully completed with the submission of
  this tender"*. **Appendices A and B are not in the sections we hold** (we have 2, 3 and 4 only).
- Building waste must go to a **named LICENSED LANDFILL** - the pack already names one, **"Tredegar Skip
  Hire"** - and the contractor must name the site(s) he intends to use.
- *"The above items are a **STRICT requirement of the Contract** and any Tender so returned, not
  containing the requested information **will be discounted from consideration**. The contractor is to
  allow in his rates for these requirements and **no claim will be entertained for failure to do so**."*

These sit on **ET&S** in the head contract, like the scaffolding. But **if strip-out flows down to us
under item 6.01, the disposal duties, the licensed-landfill naming and the SWMP flow down with it** -
and the "allow in his rates, no claim entertained" wording removes the fallback. Worth putting in the
same question to ET&S rather than a separate one. *(Compare John North Hall, where the client asks for a
Waste Carrier Licence outright.)*

### RFI-5 (SCOPE) - manifestation is in neither quote and neither list

Schedule 2376-09 clause **2.24** requires manifestation to glazed entrance doors and glazed screens
(logo/sign 150mm high, or bands 50mm high at 850-1000mm and 1400-1600mm). **Zero manifestation
references in BSW QT252799, zero in Bellview 0000000483.** Our proposal recites the requirement on p3
and then neither includes nor excludes it. Price it or exclude it - do not leave it recited.

### RFI-6 - the blind note that survived, and stale revisions (inherited from triage, still open)

1. **Rev A contradicts itself.** The revision note says the integral blind is omitted, but one blind note
   survived - **note 6 on Type AK, W.92 and W.93**, the 1825 x 5580 pair, our single most expensive line.
   Harmless today because we exclude blinds outright, but get it corrected in writing rather than argue
   it at manufacture on the dearest units on the job.
2. **We priced a superseded drawing without knowing.** Schedule rev A is dated **13.07.26** and site plan
   rev E **08.07.26** - both before our 17/07 quote - yet ET&S only issued them on **24/07**. Harmless
   this time (an omission we had already excluded). Gintare to press ET&S to issue revisions when they
   make them.

### Finish - nobody has fixed a colour (ASK, not a fail)

The architect never gave a RAL: schedule 2376-09 says only *"grey powder coated aluminium"*. BSW quoted
**"Ext Colour: 7016M Anthracite Grey - M"** and state **no internal finish at all**; Bellview quoted
**"Profiles: Anthracite Grey"** with no RAL number and no internal face. Anthracite 7016 is a dark grey
the *supplier* chose. Get cfw architects to confirm the RAL and whether the internal face is the same.
*(Georgie's rule: a supplier's default finish is not the specified finish.)*

## 4. The install line - checked, and mostly good news

The Filwood trap (large screens on per-unit labour codes) **did not bite on the big one**. Type AK is
correctly coded **CW** and carries CW labour properly: 10.1835 m2 x 2 x GBP 150/m2 = **GBP 3,055.05**.

Install reconciles exactly: **GBP 21,915.05** = the sum of the house labour codes over all 39 lines.

But three elements **3,620mm tall** sit on per-unit codes:

| Type | size | qty | m2 | install | per m2 | at CW GBP150/m2 | gap |
|---|---|---|---|---|---|---|---|
| F | 1740 x 3620 | 2 | 12.598 | ELAW 500 | 39.69 | 1,889.64 | 1,389.64 |
| H | 2210 x 3620 | 2 | 16.000 | ELAW 500 | 31.25 | 2,400.06 | 1,900.06 |
| G | 968 x 3620 | 2 | 7.008 | SADMAW 820 | 117.00 | 1,051.25 | 231.25 |
| | | | | | | **total gap** | **3,520.95** |

**Before treating that as a shortfall, note this:** Types F and H each carry an unexplained
**GBP 1,000 per unit** in the workbook's "Additional" supply column (GBP 4,000 in total) which is not in
either supplier quote. Nobody recorded what it is for. If it was a judgement allowance for the height,
the money is already in the price and only the labelling is wrong. **Ask Adam what the GBP 1,000 was
for** - it decides whether GBP 3,520.95 is missing or already covered.

### RFI-8 (NEW) - nobody has priced getting the goods to Merthyr Tydfil

Riverside's delivery rule and Gordon Court's carriage finding both bite here, and harder than on either
of those jobs, because our site is in **South Wales**.

- **BSW QT252799** states *"All estimates are ex works, additional delivery charges may apply"* - no
  rate, no threshold, no distance rule. And its **Delivery Address is 98 Alston Drive, Bradwell Abbey,
  Milton Keynes MK13 9HF** - **Fenster's own yard, not site.**
- **Bellview 0000000483 is silent on delivery entirely** - zero occurrences of deliver, delivered, ex
  works, carriage or free. *(Georgie's rule: silence is not compliance.)*
- **Site is Caedraw Rd, Merthyr Tydfil CF47 8HA - roughly 150 miles from Milton Keynes.**
- **There is no carriage line anywhere in the pricing workbook.**

So on the documents as they stand, delivery from the two suppliers is chargeable and unpriced, **and**
the onward leg from our own yard to South Wales for **107 units / 202.80 m2** is ours and unpriced too.
That is at least two separate transport costs sitting outside a fixed lump sum. Get a carriage figure
from both suppliers and price the MK-to-Merthyr leg before this is ordered.

### RFI-9 (NEW) - our price is committed 119 days longer than our costs are held

The rule Gordon Court built from their own 180-day exposure, run against this job:

| | |
|---|---|
| Our price must hold until | **11/12/2026** (JCT MW completion; there is no tender validity clause in this pack) |
| BSW QT252799 lapses | **14/08/2026** - **119 days early**, GBP 61,056.80 at risk |
| Bellview 0000000483 lapses | **15/08/2026** - 118 days early, GBP 30,352.38 at risk |

**GBP 91,409.18 - 52.4% of the sold price - is unfixed for roughly four months of our commitment**, and
both quotes die a month before the job even starts on 14/09. Each 1% of supplier inflation is
**GBP 914.09** off the bottom line; 5% is GBP 4,570. Either get both prices held in writing or accept
the risk knowingly, as Adam did on Gordon Court.

## 5. Programme and commercial terms (from the SOW - Adam should see these)

| | |
|---|---|
| Contract | **JCT MW 2016** |
| Start on site | **14 September 2026** |
| Completion | **11 December 2026** - 13 weeks |
| Delay damages | **GBP 500 per calendar day** |
| Retention | 3% to PC, 1.5% after |
| Rectification period | 12 months from PC |
| Building Control | notify Brett Hughes, MTCBC, at all relevant stages |

**THE TIMING PROBLEM.** Both supplier quotes are valid 30 days: **BSW lapses ~14/08/2026, Bellview
~15/08/2026**. The job does not start until **14/09**. So on any realistic award date **our cost is
already unfixed before the job begins** - GBP 91,409.18 of supply against a fixed GBP 174,546.37 sell,
with GBP 500/day of delay damages behind it. If ET&S go quiet into August, get both quotes re-validated
in writing rather than assume they hold.

Also note **SOW 0.08**: *"Contractor is to satisfy themselves of all submitted quantities"*, and **0.09**:
no extra will be accepted for omissions *"resulting through a lack of diligence"*. MTCBC issued item 6.01
as **m2 with quantity 0** - no client quantity at all. So the Brocks Hill test (compare our area with the
client's stated quantity) **cannot be run on this job**; there is nothing to compare against, and the
quantity risk sits entirely with us on schedule 2376-09.

## 6. Checks

`data/job-checks/st-marys-refurbishment.json`, re-run 27/07 (2nd turn). **4 FAIL + 1 ASK** - all of them
the RFIs above, not new problems:

- FAIL system-depth coupling -> RFI-2 (Type G)
- FAIL spec covered or excluded -> RFI-4 (strip-out) and RFI-5 (manifestation)
- FAIL full-height screens as curtain walling -> Type G on a per-unit labour code at 3.62 m
- **FAIL system can meet the specified performance -> RFI-1a (Smart Wall Pocket vs 1.2 W/m2K)**
- ASK finish -> neither supplier states an internal finish

Eight other rules pass, including panic hardware on all 6 door types, supplier quotes in date, net of
discount, and every unit sold covered by a supplier quote.

**NEW RULE ADDED THIS TURN: `check_system_performance`** (fixture `data/job-checks/_test-st-marys.json`).
A system can be fabricable and still be incapable of the performance the spec demands - `check_fabricator_can_make_it`
passes St Mary's happily because Bellview *can* make Smart Wall Pocket; it simply cannot make it reach
1.2 W/m2K. The new rule takes an optional `performance: {required, capable, evidence}` block on each
entry in `systems_specified`: **`capable: false` FAILS, `capable: null` returns ASK** - because on both
founding jobs (SM5 Wexham, Brocks Hill) the supplier's answer already existed and nobody had gone and
got it. Selftest passes and all six founding errors still fire.

## 7. Standing facts for this job

- **Do not redo REQ-5.** Answered on the dashboard 27/07: the 24/07 addendum does not change our scope.
  2376-09 vs 2376-09 rev A compared attribute by attribute - 209 window refs, 38 types, 28 structural
  opening sizes, 38 opening patterns, 24 restrictor notes, 6 obscure notes, 33 U-value notes, 38 SBD
  notes **all identical**. Only change: the "Magnetic operated integral blinds" note dropping from 29
  occurrences to 1 - and we had already excluded blinds. The other two re-issued drawings (2376-04 rev F
  ceiling grid/unisex toilet, 2376-05 rev E access road) do not touch glazing.
- Obscure glazing to WCs **is** priced - BSW carry 9 panes of *"6.8 Lam/18/4mm ObsTuff EcoPlus 1.0
  Stippolyte 4mm"*. BSW abbreviate it "ObsTuff", so a search for "obscure" returns nothing. Do not
  re-raise it.
- Trickle vents (62 Linkvent refs), 100mm restrictors (58 refs) and hinge protectors (32 refs) are all in
  BSW's price.
- All 6 SMA door types carry **ACIM453 concealed panic bars**. The proposal's clarification that communal
  escape doors were priced as panic bar doors, and bifold locations as commercial French doors "as
  advised by the supplier", is a **substitution the client has never accepted in writing** - still open.
- Access control / fobbed readers are excluded by us, and MTCBC carry them separately as **SOW 15.10
  "Security and Access Control Installation"**. That exclusion is safe.
- Aplus's advisory notes disclaim: residential windows *"no better than 1.8"*, commercial doors and
  framing *"up to 3.0 W/m2/K"*. Relevant if Aplus is ever used here.

## 8. Who owes what

| Who | What |
|---|---|
| **ET&S (Tom Godfrey)** | RFI-1 U-value: does EDG02 govern, or schedule 2376-09? RFI-3 access/scaffold boundary. RFI-4 window strip-out and disposal. RFI-6 the surviving blind note on Type AK. |
| **BSW + Bellview** | RFI-2: confirm in writing how Type G is built - a Sheerline 70mm casement into a Smart Wall 100mm frame, in a 28mm pocket. **RFI-1a: an SMA U-calculation in writing for the 7 Smart Wall Pocket units**, and whether they can reach 1.2 W/m2K at all. SM5 Wexham asked SMA for the same calculation and never got it - chase it properly this time. |
| **cfw architects (via ET&S)** | Confirm the RAL and whether the internal face matches. RFI-5 manifestation. **RFI-7: what is a "non-lockable device" on an escape door; and reconcile 2376-08 against 2376-09 rev A, which disagree on the external door opening sizes.** |
| **Adam** | **REQ-24: a number for strip-out and manifestation, or a decision to state them as inclusions and absorb them - they should not stay promised and unpriced. And whether to put access LIABILITY to ET&S in writing before award.** What was the GBP 1,000/unit "Additional" on Types F and H for? Sight of the JCT MW terms - GBP 500/day damages, 3% retention, 11/12/2026 completion. |
| **Fenster** | Re-validate both supplier quotes if award slips past mid-August. |

## 8b. The workbook - GENERATED, NOT SENT

`outputs\St Marys Refurbishment - Quote Check and RFI Schedule.xlsx`, generator
`scripts\st_marys_quote_check.py`. Five sheets:

| sheet | what it holds |
|---|---|
| **Summary** | the job, the GBP 174,546.37 build-up, the supplier backing, and the fact that the arithmetic is clean |
| **Commercial exposure** | the 8 things promised or required but not in the price, plus the price-hold gap |
| **Findings** | all 14, ranked HIGH/MEDIUM/LOW with source and consequence |
| **RFIs** | 14 questions **grouped by who can answer them** - ET&S, cfw architects, BSW/Bellview. **This sheet is sendable as it stands.** |
| **Reconciliation** | the 13 things checked and found correct, recorded so nobody reopens them |

**IT HAS NOT REACHED ADAM.** `scripts\mary_send.py` fails with a Graph **403 - "ErrorAccessDenied ...
Blocked by tenant configured AppOnly AccessPolicy settings"** - an Exchange ApplicationAccessPolicy
change at the tenant. Tried twice, identical, not transient. **REQ-23 raised for Zac.** Email worked at
10:49 today and again this afternoon on other jobs, so it broke during the day and there is no send log
to say when. Inbound and the hub are both fine, so **the substance went on the hub instead** (reply to
Adam on message 31, plus REQ-24). Do not let the file sitting in `outputs\` read as though it was
delivered - **when email is restored, send it.**

## 8c. Calibration - this job is now a data point, and it says the register runs high

`data/calibration.json` entry added 27/07. **Register benchmark GBP 66,540.24 vs BSW QT252799's actual
frame cost GBP 60,359.22** for the same 31 types / 98 units / 160.36 m2 - **+10.2%**. Script:
`scratchpad/stmarys_calibration2.py`.

**The aggregate hides the real story.** Uncorrected the register is only +4.4% out on the whole package,
but by band:

| band | types | units | actual GBP/m2 | register GBP/m2 | error |
|---|---|---|---|---|---|
| <1.5m2 | 10 | 34 | 697.38 | 449.77 | **-35.5%** |
| 1.5-3m2 | 15 | 50 | 368.01 | 363.50 | **-1.2%** |
| 3-6m2 | 4 | 10 | 340.10 | 467.57 | **+37.5%** |
| >6m2 | 2 | 4 | 270.19 | 365.18 | **+35.2%** |
| **all** | 31 | 98 | 376.40 | 392.94 | **+4.4%** |

The whole-job figure is good **only because the band errors cancel**. Per type the spread is -43.6% to
+46.9% and just 15 of 31 land within +/-20%. Small units are far dearer per m2 than the median says;
large units far cheaper.

**Both corrections make this job worse.** Raw median +4.4%; with the measured `bsw` factor 1.056 (the one
that actually fires) +10.2%; with the CALIBRATION Sheerline 1.10 instead +14.8%. **Nothing in the engine
was changed** - one job cannot move a factor built on 273 lines, and the band structure rather than the
supplier factor is what looks wrong.

**A mechanical fact worth remembering on this job:** `derived_factors()` from `learned-rates.json`
supersedes the typed `CALIBRATION` list, so on a BSW job the **Sheerline +10% never fires at all**. I
mislabelled my first pass because of that and redid it.

**A HYPOTHESIS FOR ADAM ON THE GBP 1,000/UNIT MYSTERY** (Types F and H) - offered as a hypothesis, not a
finding. Those two are the cheapest per m2 on the whole job from BSW: **GBP 280/m2 and GBP 262/m2**
against GBP 368/m2 for the mid band. If whoever priced it thought a 3,620mm-tall screen looked too cheap
at BSW's rate, a GBP 1,000 judgement adder on each is exactly what that would look like. That would mean
the money is already in the supply line and only the labelling is wrong - which is the difference between
the GBP 3,520.95 of light install labour being missing or already covered. **Still needs Adam to confirm.**

## 8d. A request I reported as raised was never raised - corrected 27/07

**REQ-22 on this job never existed.** The REQ-17 follow-on (access liability, and a price for strip-out
and manifestation) was written at about 21:05 as "REQ-22", but **Gordon Court had already committed their
own REQ-22 at 20:33:51**. My script hardcoded the id from a stale read and guarded with
`if not any(r["id"] == "REQ-22")`, so the guard was False, **the append was silently skipped, and the
print still said "REQ-22 raised"**. It was reported as raised in the job file, both handovers and to Zac.

**Now re-raised as REQ-24**, with the id computed at write time and the write verified by re-reading.
Every REQ-22 reference in this file and both handovers has been repointed. The substance was never
actually lost to Adam - it is in the hub reply to his message 31 - but it was untracked for about four
hours.

**The lesson, which is the same one three times today:** the guard reported success while doing nothing.
Compute the next id at write time, and verify the write landed by reading it back. An idempotency guard
that silently skips is indistinguishable from a success.

## 9. Housekeeping this chat must keep doing

The bridge (`pythonw` pid 31876, started 15:51:24) holds a registry snapshot from before the fix and
**writes it back on every session start and end**, so re-added jobs keep getting wiped. **REQ-18 is open
for Zac to restart it.** Confirmed live on 27/07 17:34: triage re-added five jobs at 17:32 and by the
next session start `riverside`, `chester-thomas`, `manor-house`, `ninn-lane` and `lower-range` were gone
again and their five briefs orphaned for the second time.

`st-marys` survives because it existed when the bridge booted. **But if this key ever vanishes, this
conversation is lost and THIS FILE is the only backup** - which is the whole argument for keeping it
current mid-turn rather than at close-out. Run `python scripts\mary_router.py --list` every turn.

---
*Last updated 27/07/2026 (seventh turn). Quote GBP 174,546.37 ex VAT unchanged - every item above is an
open question about what that price covers, not a change to it.*

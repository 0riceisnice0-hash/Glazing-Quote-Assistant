# Gordon Court, Stonegrove, Edgware HA8 7TQ — Chigwell Group

**Chat key** `gordon-court` · opened by triage 27/07/2026 14:49 · first worked 27/07/2026
**Match terms** gordon court / stonegrove / q7585 / 5244-ark / ha8 7tq

> **Two Gordon Courts exist in the archive.** This is Chigwell (London) PLC's, a £368k
> residential extension and refurbishment. The other is Target Maintenance's — RH1 St John's
> Terrace Road, Earlswood, Redhill, ref **SO_14045**, a small door repair with its own pricing
> dated 24/07. Anything mentioning Redhill or Target Maintenance is not this job.
> Chigwell is also the client of **Grange Hill Methodist** — different job, don't mix them.
> `chigwell` was deliberately removed from grange-hill's match list because it is the shared
> client of both.

---

## 1. Where this job actually stands

**The tender is already in.** Issued 09/07/2026 (documents written 10/07) at
**£368,376.70 ex VAT**, addressed FAO Luke Baker at Chigwell Group.

**We are a sub-sub-contractor and the real client is jLiving.** This is the fact that
explains everything else, and it was not known before 27/07. The tender pack contains
**jLiving's own ITT** (`2025_jL_GCourt_ITT_V8`) — jLiving is the Jewish Community Housing
Association, Vixus Property Advisory are their advisors, and **Chigwell were bidding to
jLiving with a return date of 22 July 2026 @ 1400**. Our number fed Chigwell's bid.

### jLiving's timetable — read this before chasing anyone

| Stage | Date |
|---|---|
| ITT issued | 02 June 2026 |
| **Tender return (Chigwell → jLiving)** | **22 July 2026 @ 1400** |
| Bidder presentations | TBC 02 September 2026 |
| Tender award announcement | TBC 16 September 2026 |
| Standstill period (min 10 days) | TBC 30 September 2026 |
| Contract award | TBC mid-October 2026 |
| Go Live | TBC 30 October 2026 |

Contract is **NEC3 ECC April 2013 Option A**, priced contract with activity schedule,
**executed as a deed**, and the ITT invites a *"lump sum, firm priced tender"*.
Works to *"commence within 4 weeks following signing of the contract"*.

**So Chigwell has not gone quiet — Chigwell cannot answer yet.** They submitted five days
ago and cannot commit to us until jLiving decides, which is 16 September at the earliest and
mid-October for contract. Any silence between now and September is expected, not a bad sign.

## 2. The number

| | |
|---|---|
| **Client tender (issued 09/07)** | **£368,376.70 ex VAT** |
| Supplier cost behind it | £201,086.70 (**54.6%**) |
| — BSW Window Solutions (4 quotes) | £182,787.76 |
| — Aluminium Fire Systems (Q7585) | £18,298.94 |
| Installation | £46,840 (verified to the penny — see §5) |
| External mastic | £5,622.81 shown **OPTIONAL** |
| EPDM | £11,416.64 shown **OPTIONAL** |

Documents: client `Chigwell Group - Gordon Court Pricing.xlsx`, internal twin
`...Pricing DO NOT SEND.xlsx`, `Chigwell Group - Gordon Court Proposal.pdf`.
Folder `Commercial\1. Tender Documents\Chigwell (London) PLC\Gordon Court`.

**Scope sold:** 40no replacement windows · 84no new windows/louvre/AOV · 44no patio and
green-roof doors · 15no external and communal doors (of which 3no FD30). 5244-ARK drawing
series, NBS spec 5244-ARK-9001.

### The client-facing workbook is clean — the Filwood leak does NOT apply here
Checked explicitly. `Chigwell Group - Gordon Court Pricing.xlsx` has dimensions B2:K75, print
area B1:H71, **zero populated cells in columns J–V**, and every value hard-typed with no
formulas. No supplier name, no cost, no margin is recoverable from it. The internal twin
carries all of that in J–V including `K3/L3/M3 = "Supplier used: BSW 182787.76"`.
**Gordon Court's "DO NOT SEND" twin practice is the one that works** — this is the model
Filwood should have followed (HANDOVER.md:715, where print area was clean but the columns
weren't hidden and K3/L3/M3 exposed BSW's cost).

## 3. THE HEADLINE RISK — 163 days of unfixed cost against a firm price

**jLiving's Form of Tender (`2025_jL_GCourt_FoT_V1`) states: *"This tender remains open for
consideration for a period of 180 days from the date of receipt of tenders."*** Receipt was
22/07/2026, so **the price is committed to 18 January 2027**.

Every supplier quote behind it is a 30-day quote:

| Supplier | Ref | Dated | Lapses | Value | Days short |
|---|---|---|---|---|---|
| BSW | QT252247 PVC | 07/07/26 | 06/08/26 | £53,543.90 | 165 |
| BSW | QT252248 PATIOS | 07/07/26 | 06/08/26 | £108,275.95 | 165 |
| BSW | QT252251 ALI DOORS | 07/07/26 | 06/08/26 | £14,099.81 | 165 |
| BSW | QT252257 AOV & LOUVRE | 07/07/26 | 06/08/26 | £7,085.76 | 165 |
| AFS | Q7585 | 09/07/26 | 08/08/26 | £18,298.94 | 163 |

**£201,086.70 — 54.6% of the tender — is unfixed for ~163 days against a lump-sum firm price
executed as a deed.** And neither supplier's price is binding even inside its 30 days:

- **AFS T&C 2.6:** *"Any quotations given by AFS will not constitute an offer and may be
  withdrawn or amended at any time."*
- **AFS T&C 8.2:** reserves the right to increase price before delivery for FX, tax, labour
  and material movements.
- **BSW, on every quote:** *"An estimate is not an offer of contract and is not binding."*

This is the John North Hall rule (client writes a validity requirement into the ITT — 90 days
there) meeting the St Mary's rule (validity against contract start, not tender return). Gordon
Court is the worst instance found: **180 days**, and contract award ~11 weeks after the last
quote dies. **AFS's lead time is 8 weeks from order signature AND receipt of their 60% first
payment**, so on jLiving's own programme the fire doors land around January 2027.

→ **New standing check built for this: `check_quote_validity_against_commitment`** in
`scripts/mary_checks.py`, fixture `data/job-checks/_test-gordon-court.json`.

## 4. Findings on the issued tender

### 4.1 £723.87 of supplier cost is not in the £368,376.70 (both provable)

**(a) AFS extras — £506.37.** Q7585 p7: *"Not included in quote above, can be added as
optional extras"* — Fixing Pack (screws, foam, packers, mastic) **£256.37** and Delivery
**£250.00**, outside the £18,298.94. Neither appears anywhere in the workbook.
The quote contradicts itself — the Specifics page says *"Logistics: Delivered"* — but
**T&C 8.1 settles it against us**: *"That price will be exclusive of all costs and charges of
packaging, insurance and transport of the Goods, which will be itemised separately if
applicable and invoiced to the Customer **in addition** to the price of the Goods."*
So the £250 is real, not a typo. Same class as Princess Beatrice's £668.41.

**(b) BSW extras — £217.50, previously unknown.** QT252257 carries an **Extras** block:
*"PANEL SET UP · 1 Pcs · £217.50 · Total Extras Value £217.50"*. The quote is
WN_7 £2,365.86 + WL_1 £4,502.40 = £6,868.26, **+ £217.50 = £7,085.76**, its stated total.
The workbook carried only the two element figures. This is exactly why the BSW cost memo
`M3 = 182,787.76` is £217.66 short of what the four BSW quotes actually add up to
(£183,005.42) — £217.50 of it is this omitted extra, the remaining 16p is penny rounding on
three R-column cells.

### 4.2 The third FD30 door is D_T — and all three of its attributes are wrong or blank

Triage asked whether the 3-door count survives, given Gintare told AFS in writing on 09/07
that *"the door schedules don't appear to correspond with the plans and elevations"* and then
asked them to price off the schedules anyway to make the same-day deadline.

**The count of 3 is defensible. The third door is not.** Workbook row 59 labels it **D_T**.

- **D_A × 2 reconcile exactly.** Schedule 51001's only two `Double External FD30S` rows are
  2085h × 2326w and 2238h × 1750w (GR316 Entrance) — matching Q7585 pos 001 (2326 × 2085) and
  pos 002 (1750 × 2238) to the millimetre.
- **D_T is a different animal.** Schedule 51001 gives it as: `D_T | FD30S | L 0 | GR425 Store
  | struct H 2110 | struct W 1600 | panel 756 × 2060`, quantity 1. So:
  1. **Height is 2110, not 2210.** AFS quoted 1600 × **2210** — 100mm taller than the
     structural opening. A digit slip, and the same class as Filwood's ED-06 typed
     6315 × 3150 where the bill said 3105.
  2. **It is a STORE door (GR425), and its Internal/External cell is BLANK.** If it is
     internal it belongs to the joinery package, not ours — £7,304.44 of sell and £5,804.44
     of cost for a door that may not be in our scope at all.
  3. **The schedule shows a 756 × 2060 single leaf** in a 1600 opening (leaf + sidelight, or
     an unequal pair). **AFS quoted "1 Pcs. Double Door".**

£7,304.44 of sell rests on three unresolved attributes. The other two doors are sound.
Note the ITT expressly puts this risk on us: *"Any quantities, dimensions, capacities etc.
detailed within the tender pack are purely indicative... It remains the Bidders'
responsibility to verify the specific details."*

### 4.3 SCOPE GAP — 2no D_X external doors are on the schedule and priced nowhere

Schedule 51001's own per-type count cells are D_A 2, D_B 6, D_C 2, D_D 2, D_E 1, D_G 24,
D_H 42, D_I 21, D_J 4, D_L 1, D_O 1, D_P 2, D_Q 1, D_R 3, D_T 1, D_U 1, **D_X 2** — summing
to exactly the **116** the drawing states as its Grand total, so these are the drawing's own
numbers, not an extraction artefact. Strip the 99 internal doors (D_G/H/I/J/L/O/P/Q/R,
correctly left to joinery) and **17 non-internal doors remain. We priced 15.**

**D_X — 2no, Level 0, structural 2100 high × 1800 wide — is on the *External and Communal
Door Schedule* and appears in no line of the workbook.** Every descriptive cell on both rows
is blank: no leaf count, no internal/external, no fire rating, no ironmongery, no room
number. It is the last type on the sheet, which is consistent with an unfinished architect's
entry — but it is 1800mm wide and it is in the external door schedule.

Nearest priced comparator is D_E (1500 × 2100, DAD) at £2,779.70 sell each → **order of
magnitude ~£5,600 of sell plus ~£1,000 of install. BENCHMARK ONLY** — there is no supplier
price for D_X. This is the Brocks Hill pattern (7 external doors on the architect's schedule
absent from the priced bill).

### 4.4 Performance — the energy annex nobody opened, and it is tighter than the schedules

The St Mary's rule fires again. **The architect's schedules set no U-value at all** — they
defer it: *"MIN. THERMAL RATING: To Edward Pearce Consulting Engineers specification"*, and
**that specification is not in the tender pack**. They do set **"G-Value of 0.36 or better"**.

**`Energy Statement - Gordon Court 25.02.24.pdf`, inside the tender zip, states: *"The
external glazing will be replaced or improved to achieve a U-value of 1.1 W/m²K."*** Its
performance table runs a baseline column (Glazing 1.60 W/m²K, vision-element g-value 0.63)
against a proposed column (Glazing **1.40 W/m²K**, g-value **0.40**).

So four numbers are in play — 1.1 (replacement glazing), 1.4 (new build), g-value 0.36
(schedules) and 0.40 (Energy Statement). **On g-value the schedule is tighter; on U-value the
Energy Statement governs.** NBS 9001 p85 separately requires 1.2 W/m²K or better on the Colt
roof AOV. Our proposal promises g-value 0.36 and states no U-value.

**No whole-window Uw is stated on any of the four BSW quotes.** The only thermal figures
anywhere are centre-pane glass values inside make-up strings. Applying the SM5 Wexham rule
honestly: **nothing is rejected, because the arithmetic cannot be done** — a Uw exists for no
element on this job, so neither a per-element nor an area-weighted test can be run. The
finding is not *"we fail 1.1"*, it is ***"nothing on file demonstrates 1.1 and nobody has
asked"***.

**Credit where due — BSW did name the coatings here**, unlike Bellview on St Mary's:
- Liniar: `4Tuf/18/6.8 LAM Coolite SKN176ii Argon` — solar control + argon
- Alunet patios: `6.Lam/16/6mmTuff Coolite SKN175ii` — solar control
- Sheerline AOV: `Skn 176 6.8 Lami / 4 / 4mm Low E Tuff Black Warm Edge Sp 12mm` — solar,
  low-E and warm edge all named, the best-specified glass on the job
- AFS fire doors: `2 Pcs. 6+15mm GLASSPROF EI30 Clear DGU **U=1.0**` — the **only** stated
  U-value on the whole job, Certifire accredited

**The one g-value gap:** WN_2 (7no) is `6.8 Lam/18/4mm ObsTuff EcoPlus 1.0 Satin 4mm Black
Warm Edge Sp 18mm Argon` — obscure, no Coolite, no SKN. **No solar coating, so it cannot
meet the 0.36 we promised.** (Searched for Obs/Stippolyte/Satin/Pattern per the St Mary's
tip — the obscure glazing is genuinely there, 3 references; it is the *coating* that is
absent, not the obscurity.)

**Weakest thermal element by far is the patio doors** — 44 units, £108,275.95 of cost,
£174,275.79 of sell, in a 2-rail Alunet sliding frame with a 16mm cavity, **no gas fill and
no warm edge named**. Sliding patios are a known thermal weak point and this is 47% of the
tender.

### 4.5 Trickle vents at half the required area, and no acoustic vents at all

All five schedules carry: **"VENTILATION: 8000mm² min trickle vents unless otherwise
specified in window schedule."** **BSW quoted `4000 External Linkvent / 4000 Internal
Linkvent` throughout** — half.

Checked the get-out before raising it: 52002 and 52003 specify no different *area*. What they
specify is an **"Acoustic Trickle Vents" yes/no column**, so the 8000mm² minimum stands.

**And the acoustic vents are not priced either.** Verified positionally on 52002 — the
Acoustic Trickle Vents header sits at x = −210.9 and **26 of the 40 replacement-window rows
carry a Yes in that column** (x ≈ −218). Required product is *"Passivent AL-dB 450 or
better"*. **BSW's four quotes contain zero occurrences of Passivent, AL-dB or acoustic.**
An acoustic trickle vent is a different and dearer product than the Linkvent quoted.
52003 (84 units) carries the same column in three table blocks — **that count has not been
done** and should be.

### 4.6 PAS 24 / Secured by Design — total silence

Schedules require *"PAS24 SBD locking mechanisms to all amenity deck floor windows and
doors"*, and 51001 carries a **PAS 24 2016 column**. Our own proposal recites *"with PAS 24,
restrictors, trickle ventilation, acoustic requirements and safety glazing noted where
applicable"*. **Zero occurrences of "PAS 24" or "PAS24" across all four BSW quotes.**
Yale Shootbolt locks, Egress Hinges and 35×35mm security cylinders are quoted, but no
certification is stated. Reciting a requirement is not pricing it.

### 4.7 £5,597.89 of BSW cost has no quote line behind it (Brocks Hill pattern)

Seven single-unit lines carry a cost with no matching BSW quote line — a rate applied, so the
arithmetic ties perfectly and nothing looks wrong:

| Line | Cost | Sell |
|---|---|---|
| WN_4 (1360 × 1656) | £521.69 | £859.19 |
| WN_6 (2710 × 1650) | £911.25 | £1,248.75 |
| WN_8 (910 × 1350) | £297.26 | £597.26 |
| WN_9 (1135 × 1350) | £472.89 | £772.89 |
| D_B (1055 × 1750) | £843.71 | £1,743.71 |
| D_E (1500 × 2100) | £1,279.70 | £2,779.70 |
| D_U (1405 × 2170) | £1,271.39 | £2,771.39 |
| **Total** | **£5,597.89** | **£10,772.89** |

Proof it is exactly this: the workbook's matched per-line BSW amounts (column R) total
£177,189.86; add these seven and you get £182,787.75 ≈ the `M3` memo of £182,787.76.
The rate probably holds, but nobody at BSW has agreed it.

### 4.8 Rooflights and the Colt roof AOV — neither priced nor excluded

**The enquiry zip is titled `Gordon Court Windows, ROOFLIGHTS & Curtain Walling.zip`** and the
NBS section governing our package is **L10 "Windows/ rooflights/ screens/ louvres"**.
We priced no rooflights and no curtain walling.

NBS 9001 p85 names a specific product: **Colt International AXS 140 Combined AOV Smoke
Ventilator and Roof Access Hatch** — roof-mounted, 1000 × 1250mm ventilator, aluminium lid,
RAL 7016, Re 50, WL 1500, B300, **U-value 1.2 W/m²K or better**. We priced 3no Sheerline
tilt-and-turn AOV *windows* (WN_7, wall-mounted) and 4no louvres — not this.
**The proposal's exclusion list names neither rooflights, roof AOVs nor curtain walling.**

*The other side of it, in fairness:* the wider Colt package on NBS pp89–93 (AOV shaft, OPV
Heart module, OPV display panel, electrical wiring, ductwork, scaffolding) is plainly a
specialist smoke-ventilation contractor's scope and not ours. The open question is
specifically the AXS 140 unit and any rooflights — not the Colt control system.

### 4.9 AFS have not priced a dual-colour finish on the fire doors

The Georgie's rule, and the Mercury failure repeated exactly. Q7585's Specifics page says
only **"Colour: Standard RAL"** and each position repeats **"Colours: Profiles: mat
standard"** — no RAL number, no internal face, no external face. The schedules require
**white internally, dark grey externally**. Dual colour on a fire door is a real cost and it
is not in the £18,298.94. AFS answered what was easy (system, fire rating, glass, U-value)
and were silent on the one thing that costs money.

**All three BSW elements, by contrast, quoted dual colour properly** — and this was worth
checking rather than assuming:
- Liniar: `Ext Colour: Grey Foil On White (7016)` + white outer frame, cill, bead, and
  separate `4000 External Linkvent Grey RAL 7016` / `4000 Internal Linkvent White`
- Alunet: `Ext Colour: (7016) Grey / Int Colour: (9016) White`
- Sheerline: `Ext Colour: 7016M Anthracite Grey - M / Int Colour: 9910HG Hipca White -G`

Residual on all three: the architect left the external RAL as **"RAL XXX (TBC)"** and BSW
have chosen **7016**. Reasonable, but it is the supplier's choice, not the architect's.

### 4.10 Two contradictory scope statements in the issued proposal

Both on p3 of a document already with the client:

- *"It has been noted that **no doors are included within the schedule drawings**, final costs
  are subject to a site visit."* — factually wrong. 5244-ARK-51001 is titled *External and
  Communal Door Schedule* and carries 116 doors; 51002 carries 44 more. We priced 15 external
  and 44 patio doors off those very schedules.
- *"Our scope is limited to the manufacture, supply and installation of **replacement
  aluminium windows**."* — contradicts the £368,376.70, which sells 168 windows/louvres/AOVs
  plus 59 doors including **Liniar uPVC** windows and **Aluprof** fire doors.

If Chigwell ever relies on either sentence our scope is arguably far narrower than we priced.
Worth correcting at order stage.

## 5. Things checked and CLEARED — do not re-raise

- **Install DOES cover the 3 FD30 doors.** Triage's open question 4. `I61` is
  `=SUMPRODUCT(F*N)+SUMPRODUCT(F × code value)` with **DAD = £500, SAD = £250,
  PVC/LAW/MAW = £160**. Rows 57–59 are all coded DAD → **3 × £500 = £1,500**. Recomputed the
  whole formula independently: **£46,840 exactly**, matching the cell. Breakdown by code:
  DAD £24,500 · SAD £2,500 · MPVC £8,000 · SPVC £6,080 · LPVC £4,640 · LAW £640 · MAW £480.
- **Quantities reconcile exactly on three of four schedules.** Patio 44 = 44 · replacement
  windows 40 = 40 · new windows 84 = 84, each against the drawing's own stated Grand total.
  Only the external door schedule disagrees (§4.3).
- **Q7585 arithmetic is sound.** £6,468.03 + £6,026.47 + £5,804.44 = £18,298.94 exactly, and
  all three carried into the tender at cost + the £1,500 house DAD adder = £22,798.94 sell.
  Nothing dropped.
- **Panic/escape hardware IS priced on all three fire doors** — WILKA panic shootbolt guides
  top and bottom, WILKA rod latch/top rod/round rod, FUHR 3-point automatic lock 833, GEZE
  TS 5000 + TS 4000 closers, on every position.
- **The client workbook leaks nothing** (§2).
- **The PVC-U vs aluminium conflict was already qualified by us** — proposal p3: *"The
  schedules and specification include conflicting references to PVC-U and aluminium window
  systems, so the final system/material basis should be confirmed prior to order."* Checked
  before raising it; Gintare got there first. NBS 9001 permits *"Aluminium/ unplasticized
  polyvinyl chloride (PVC-U)"* on at least one item, so it is genuinely ambiguous in the pack.
- **Supplier discounts taken net** on all five quotes.
- **BSW is BSW.** All four quotes footer to *BSW Window Solutions, Yaxley, Peterborough*; the
  *"Bellview will not be held responsible"* line is shared T&C boilerplate on the same quoting
  software. Our records are right — this is not a Bellview job.

## 6. Open RFIs / who owes what

| # | Question | To | Status |
|---|---|---|---|
| RFI-1 | D_T: is it external or internal? 2110 or 2210 high? single leaf + sidelight or a double? | Arkon via Chigwell | open |
| RFI-2 | D_X × 2 (2100 × 1800) — in our package or not? Nothing on the schedule says. | Arkon via Chigwell | open |
| RFI-3 | Whose spec governs U-value — the Energy Statement's 1.1 W/m²K or Edward Pearce Consulting Engineers, whose spec the schedules defer to and which is **not in the pack**? | Chigwell | open |
| RFI-4 | Confirm external RAL (schedules say "RAL XXX (TBC)"; BSW assumed 7016) | Arkon via Chigwell | open |
| RFI-5 | Are rooflights and the Colt AXS 140 roof AOV/access hatch in our package? | Chigwell | open |
| RFQ-1 | Whole-window **Uw** for the Liniar, Alunet and Sheerline elements; 8000mm² trickle vents; Passivent AL-dB 450 acoustic vents on the marked units; PAS 24 certification; louvre **free area** for LW_1 | BSW | not yet asked |
| RFQ-2 | Dual-colour (white int / grey ext) price on the 3 fire doors; written price hold to 18/01/2027; the £506.37 extras | AFS | not yet asked |
| **REQ-20** | Adam: hold Q7585 past 08/08 and cover the 180-day gap? | dashboard | **raised 27/07** |

**AFS are chasing and Mary cannot reply to them (ghost protocol).** Chris Wall
(chris@aluminiumfiresystems.com) chased Q7585 at 13:02 on 27/07 — *"following up on this quote
to see if there is any update with this project"*, no attachment. A human must answer.
Note AFS chased **Manor House (Q7593)** 100 minutes later the same day, so they are working
their whole book, not signalling anything specific about Gordon Court.

## 7. Decisions taken this session

1. **Did not treat the AFS chase as a client reply.** Triage's rule held — the only inbound
   was the supplier chasing its own quote.
2. **Did not raise the PVC-U/aluminium substitution** after finding the proposal already
   qualified it. Checked before firing.
3. **Did not claim we fail the 1.1 W/m²K** — no Uw exists on file for any element, so the
   arithmetic cannot be done in either direction. Recorded as an unasked question, not a
   failure.
4. **Did not invent a price for D_X.** Stated as a benchmark order of magnitude off D_E and
   flagged as needing a real supplier number.
5. **Built `check_quote_validity_against_commitment`** rather than filing the 180-day gap as
   a one-off note, because it is now the third instance in a day.
6. **Fixed two false positives in `check_finish_substitution`** — see §8.

## 8. Changes made to the toolkit this session

- **New rule `check_quote_validity_against_commitment`** (`scripts/mary_checks.py`), fixture
  `data/job-checks/_test-gordon-court.json`. Compares each supplier quote's expiry against
  the date **our own** price stops being withdrawable. New manifest field
  `price_commitment: {source, our_price_open_until}` and `valid_until` on each supplier quote.
- **Fixed `_finish_matches`, which was reporting a correctly-priced dual-colour job as a
  substitution.** Two separate defects, both caused by comparing raw strings:
  1. BSW write a foiled frame as **"Grey Foil On White (7016)"** — grey foil on a white
     substrate, so the visible external face is grey. The substring test found the word
     *White* inside it and concluded both faces were white. Added `_visible_face()` to strip
     the `... on <substrate>` clause.
  2. The two sides arrive wrapped in different noise — the architect writes *"PVC-U white
     internally"* and *"dark grey to RAL XXX (TBC)"*, the supplier writes *"(9016) White"* and
     *"7016M Anthracite Grey - M"*. Neither is a substring of the other. Added `_colours()`
     and compare colour words, falling back to substring only when no colour is recognised.

  A false FAIL costs as much as a missed one — it teaches people to click past the checker.
  Selftest still passes and Georgie's Mercury case still fires.
- Current run on this job: **4 FAIL, 2 ASK**, all genuine —
  `python scripts\mary_checks.py data\job-checks\gordon-court.json`.

## 9. Where the documents are

Everything that matters was **inside the zip**, exactly as Georgie's warned. The loose
`1. Tender Documents\Gordon Court\` folder holds 28 drawings; the sibling
`Gordon Court Windows, Rooflights & Curtain Walling.zip` holds the **jLiving ITT, Form of
Tender, Contract Data, Q&A log, Energy Statement, 186-page NBS spec, programme, asbestos
survey, structural package and the full architect's drawing set**.

Priority documents extracted to `scratchpad\gc-zip\` this session. Helper scripts used:
`scratchpad\gc_wb.py` / `gc_wb2.py` / `gc_wb3.py` (workbook), `gc_bsw.py` / `gc_bsw2.py`
(supplier quotes), `gc_census.py` (door census), `gc_acoustic.py` (acoustic vent column),
`gc_winsch.py`, `gc_scan.py`.

**Still unread and worth a look:** `1. Q&As 02.06.26.pdf` is a **scanned image with no text
layer** (pdfplumber returns 0 characters) — the Lower Range Road lesson says a clarification
log is where U-value answers hide, and RFI-3 above is exactly such a question. **Render it.**
Also unread in full: the 186-page NBS spec (only L10/L20 material clauses sampled),
`GorCou Pci Rev D.pdf`, `Gordon Court wi Contract Version - V3.pdf`,
`2025_jL_GCourt_Contract_Data_p1&2_V3.pdf`, and the asbestos survey (relevant to strip-out on
a 1960s refurbishment).

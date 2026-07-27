# St Mary's Refurbishment, Merthyr Tydfil - E T & S Construction

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

### RFI-3 (COMMERCIAL) - we excluded the access plant the preliminaries require

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

`data/job-checks/st-marys-refurbishment.json`, run 27/07. **3 FAIL + 1 ASK** - all four are the RFIs
above, not new problems:

- FAIL system-depth coupling -> RFI-2 (Type G)
- FAIL spec covered or excluded -> RFI-4 (strip-out) and RFI-5 (manifestation)
- FAIL full-height screens as curtain walling -> Type G on a per-unit labour code at 3.62 m
- ASK finish -> neither supplier states an internal finish

Nine other rules pass, including panic hardware on all 6 door types, supplier quotes in date, net of
discount, and every unit sold covered by a supplier quote.

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
| **BSW + Bellview** | RFI-2: confirm in writing how Type G is built - a Sheerline 70mm casement into a Smart Wall 100mm frame, in a 28mm pocket. |
| **cfw architects (via ET&S)** | Confirm the RAL and whether the internal face matches. RFI-5 manifestation. |
| **Adam** | What was the GBP 1,000/unit "Additional" on Types F and H for? Sight of the JCT MW terms - GBP 500/day damages, 3% retention, 11/12/2026 completion. |
| **Fenster** | Re-validate both supplier quotes if award slips past mid-August. |

---
*Last updated 27/07/2026. Quote GBP 174,546.37 ex VAT unchanged - every item above is an open question
about what that price covers, not a change to it.*

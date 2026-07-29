# Redditch Library - BLBS0956

Chat opened 2026-07-28 by triage. History before 29/07 12:20 is in
`data/jobs/redditch-library-archive-2026-07.md`; evidence in `python scripts/mary_recall.py --job redditch-library`.

## Position

**A NUMBER IS WITH THE CLIENT AND IT IS THE WRONG ONE.** Adam emailed Leonard White at 11:14 on 29/07:
*"Currently sitting around GBP 89k +vat with the same inclusions/exclusions as the other subcontractor's
quote details."* That is the **28/07** figure (GBP 89,218.65). The live tender sum is **GBP 94,926.76** -
**GBP 5,708.11 / 6.4% higher**. Flagged to Adam 12:26. **Nothing has gone to Pride from me**; Leonard holds
only Adam's indication, so it is still correctable.

- **Project** Redditch Library, 15 Market Place, Redditch B98 8AR. Flat roof refurb AND external window/door
  replacement; **windows and doors only are ours**. Occupied public library throughout.
- **End client** Worcestershire CC. **CA** Gleeds, Birmingham - Shaun Wilkes, shaun.wilkes@gleed.com (sic).
- **We are invited by Pride Developments Group Ltd** (Cwmbran) - Leonard White, Senior QS,
  leonard.white@pridedevelopments.co.uk. **We are sub-contractor to Pride**, who bid Gleeds. Our offer goes
  to Pride. Pride are a **Priority Customer**, 19 Estimating Log rows, **four confirmed wins** (Rubery
  Library, 92-94 High St Merthyr, Catherine's House Plymouth; RAF Mildenhall live) - **every win/loss cell blank**.
- **Tender pack** BLBS0956 v01, May 2026, 254pp. Take-off: **43 items / 41 refs / 136.53 m2**.
- **Status** Documents built, dated 29/07, `mary_checks` all pass, pack audit clean, PDF author empty.
  **Issue-ready with Adam. Not issued to Pride.** Adam intends this as the **first Mary-only quote**,
  submitted without waiting for suppliers (11:30, URGENT) - Gintare's RFQ is *"to sense check retroactively"*.

## The number and its basis

**TENDER SUM GBP 94,926.76 gross of 2.5% MCD, ex VAT** (net GBP 92,553.59). MCD is taken off the GROSS, so
gross = net / 0.975 - this is how Joedan state theirs and the two must stay comparable.

| | net GBP |
|---|---|
| frames - Aplus level, factors read live from `data/learned-rates.json` | 54,422.66 |
| house code adders (**this is the margin**) | 20,625.00 |
| installation - **fit only** | 7,670.00 |
| solar-control glazing, 136.53 m2 x 13.29 | 1,814.51 |
| perimeter sealing, 314.29 lin m x 5.00 | 1,571.45 |
| strip out, **43 nr x GBP 150.00** | 6,450.00 |
| net | 92,553.59 |
| **TENDER SUM (net / 0.975)** | **94,926.76** |

**THE FRAME SUPPLY IS A BENCHMARK. NO SUPPLIER HAS QUOTED THIS JOB.** It is a curve fitted to BSW's real
Severn Trent quote (QT250834, `rate = 721.47 x area^-0.4093`, R2 0.9934) moved to a second-supplier
position by measured factors. Everything else is house rates or the client's own schedule.

**WE ARE ABOVE JOEDAN AND NO SUPPLIER WE CAN MEASURE CHANGES THAT** (Joedan gross GBP 90,687.17):

| supplier | frame buy | tender sum | vs Joedan |
|---|---|---|---|
| BSW +5.7% (n=272) - **the only one asked** | 56,993.38 | 97,563.42 | +6,876 |
| Aplus -1.6% (n=83) - **what the price assumes** | 54,422.66 | **94,926.76** | **+4,240** |
| 4Ali -1.5% (n=82) | 54,641.44 | 95,151.18 | +4,464 |
| TruFrame | - | - | **N/A - uPVC, not aluminium** |

**A MANUFACTURER CANNOT BE UNDERCUT, AND IT IS ARITHMETIC.** EL75mm Squareline and AC100 Commercial are
Joedan's OWN products - they buy no frame from anybody. Our frame buy is GBP 54,423 against GBP 20,625 of
margin, so **22.3% of our sell is margin on a frame the competitor fabricates himself** - more than the whole
gap. Do that sum before promising an undercut against a fabricator.

**HOW THE 28/07 NUMBER BECAME THIS ONE - reconciles to the penny, gross:** strip-out at the real Brandon
rate replacing a GBP 3,000 guess **3,538.46** + code adders on the 125%-above-6m2 rule (refs 19, 20)
**769.23** + frames after the stale hardcoded factors were fixed **1,400.42** = **5,708.11**.

**MARGIN IF THE GBP 89k IS HONOURED** - sell fixes on submission, margin is what moves:

| | margin | % of net |
|---|---|---|
| live GBP 94,926.76 | 20,625.00 | 22.3% |
| held at 89,218.65 | 15,059.59 | 17.3% |
| **held at 89,218.65, buying BSW** (the only supplier asked) | **12,488.87** | **14.4%** |

All gross of prelims we do not charge **at all** (Brandon carries survey / PM / commercial / technical /
supervision / QA at **4.203% of works** = GBP 3,832 here, plus fixings GBP 971) and of a fitting cost
recorded nowhere. **Sensitivity, unchanged:** engine 89,910.77 | Severn Trent curve 86,354.89 | St Mary's
band correction 79,047.50 - the whole spread is the 3-6 m2 band, which carries **62%** of this job and which
the register runs **+37.5%** high on.

## Deadlines

**NO DEADLINE SET - DO NOT INVENT ONE.** The pack's 12 noon Friday **26 June 2026** is GLEEDS' date to the
main contractors and has passed. Leonard White, 22/07, said only *"submit your tender back asap"*.
**Adam asked him directly at 11:14 on 29/07: *"When are you submitting cost on this one?"*** - so the
question is now with the person who can answer it. **Do not raise it again; watch for his reply.**

Validity: Form of Tender holds the sum open **10 weeks**, prelims say **not less than 3 months**, our T&Cs
say **30 days**. Flagged 28/07 as a compliance fault; on a benchmark price submitted before quotes land the
30 days is **the only thing capping our exposure**, so it is now a hedge. Recommended to Adam we keep it.
Nobody should "fix" that clause in the template without deciding this first.

Contract: JCT Minor Works with CDP, **10 weeks** to completion, **LDs GBP 1,000/calendar week**, retention
5% to 2.5%, PL GBP 5m, **CDP PI GBP 5m stating both "12 years" and "Six years"**. Award **70% price / 30%
quality**. The JCT form is not in the pack and no sub-contract has come from Pride.

## Open RFIs and questions

**With Adam** (all live; nothing new raised - 15 requests already open board-wide):
1. **The GBP 89k with Leonard** - correct it now on the strip-out, or absorb it and hold. Recommended correcting.
2. **Send the RFQ to Aplus, 4Ali and SBM.** It has gone to **BSW alone, the dearest**, whose quote will land
   above our own number and read as *"Redditch is not winnable"* when it says *"we asked the wrong supplier"*.
3. **CDP and its PI** - Fenster or Pride.
4. **The missing prelims block** - stated, not added; his commercial call.
5. **Two house T&C clauses** - the 30-day validity and the **50% deposit** our terms demand, which no main
   contractor pays under JCT. Fix at the template once, not on this tender (the Gordon Court mistake).

**Ten RFIs for Pride to pass to Gleeds**, on the workbook's RFIs sheet. The seven that matter:
- **RFI-03 THE SPEC COUPLES A THERMALLY BROKEN WINDOW TO A NON-THERMAL DOOR AT REFS 32 AND 34 AND IT CANNOT
  BE BUILT.** Drawn on Elevation C as ONE assembly. Windows EL75mm Squareline (TB, 75mm), doors AC100
  Commercial (non-thermal, 100mm). Adam's SM5 Wexham rule (window takes the door's system) would put them
  outside the 1.4 W/m2K requirement, **so the rule and the spec cannot both be obeyed**. Priced in one
  thermally broken system throughout. GBP 7,552.56 sits on these two.
- **RFI-01 refs 16, 17, 18 are RAKED, not rectangular** - parallelograms on the stair soffit, scheduled as
  2250 x 2304 rectangles. GBP 8,509. Priced as windows not CW (glazed band, solid wall over and under);
  worth ~GBP 7,000 if wrong and **the single line most worth a second opinion**.
- **RFI-05 ref 38 is drawn as a 15-pane screen and scheduled as 6 fixed lights.** Four mullions and two
  transoms is not the same buy.
- **RFI-02 refs 29, 30, 31 have no configuration at all** - blank on Gleeds' schedule AND Joedan's, so the
  tender is silent, not the transcription. Priced as fixed lights, stated.
- **RFI-06 ref 39 is the door missing from cl.5's ironmongery list** (32, 34, 37, 41). Priced with no panic set.
- **RFI-07 asbestos.** All four window-specific samples **NO ASBESTOS DETECTED**. But **FM000125, bitumen
  paint to metal cladding, chrysotile, 100 m2, "left hand elevation", easily disturbed** - if that is the
  raking wall carrying 16/17/18, our strip-out disturbs it. The pack's GBP 5,000 provisional sum covers the
  whole building including the roof, and is **excluded** by us as by Joedan.
- **RFI-10 ONE tender site visit only**, through Gleeds, all sub-contractors present - while 3.5.3 requires a
  measured survey of every opening before ordering and forbids relying on Gleeds' dimensions.

**THE SPECIFIED SYSTEMS ARE THE COMPETITOR'S OWN AND FENSTER CANNOT BUY EITHER.** Spec 3.5.3 cl.3 permits an
alternative but the tenderer *"will become responsible for the design ... under contractor's designed
portion"*, with a compliance specification required WITH the tender return and written CA and Client
approval. `systems_specified` in the manifest therefore records **what Fenster is actually quoting** - a TB
75mm system tendered as the CDP alternative - because the check asks whether the thing we are SELLING can be
built. That the specified systems are unbuyable by us stays in `exposures`.

## Decisions

- **29/07 12:26 - flagged the GBP 89k to Adam without assuming why.** He was sent GBP 93,526.34 at 10:04 and
  GBP 94,926.76 at 11:42, but his 11:30 reply came off the 28/07 thread whose subject still carried
  89,218.65. Deliberate low indication and working-from-the-old-thread are both consistent with the record,
  so I asked which rather than asserting. **Georgie's 09:20 rule: report what the record shows and how old
  it is, never "Adam forgot".**
- **29/07 - told Adam not to describe our offer to Leonard as "the same inclusions/exclusions" as Joedan.**
  True of all 11 inclusions and 25 exclusions (lifted verbatim from pack p151-153) except **our TEN YEAR
  guarantee against their twelve months**. On a 70/30 award where we are the dearer bid that is the only
  place this can be won, and his wording gave it away. It is on the face of the proposal already.
- **Recommended we still bid, knowing we are dearer** - the ten years, a priority customer we have won four
  jobs with, and a number on the table keeps us on their list.
- **28/07 - priced ours first, compared to Joedan second.** Triage's instruction and right: a fully priced
  competitor schedule sitting in the pack is the easiest thing in the world to anchor to.
- **Solar-control glass carried as a separate line** (GBP 13.29/m2, the glass-unit median difference) rather
  than by swapping to the "incl solar control" register categories, which have n=1 to n=39 behind them.
- **Refs 19 and 20 priced as ELAW/LAW ribbons, not CW** - 900mm and 1100mm tall, window bands in a wall.
- **SEND THE RFQ SCHEDULE, NEVER THE TENDER PACK.** Joedan's fully priced quotation is at **page 147** and
  Leonard's own covering email points us at it. Forwarding the pack to a supplier hands them the market price
  before they quote us. The RFQ is a separate, **price-free** file for exactly this reason (REQ-28's shape).
- **No rate invented for SBM, deliberately** - Cortizo aluminium, quotes estimating@ direct, not on the
  Suppliers Listing, **no factor exists**. Two of their three archive documents are UNGLAZED and the third
  has no schedule that belongs to it. **The genuine unknown; put them on the RFQ instead.** Caution: their
  terms want 50% with order and title retained until paid - on a GBP 54k frame buy that is real cash flow.

## What Adam said

- **29/07 11:36 - "Truframe are uPVC windows, they do not do aluminium."** He is right and the error was
  mine: I named TruFrame as the only supplier who could beat Joedan on an ALUMINIUM package. **A supplier
  factor records what we CHARGED on that supplier's lines and carries no record of what they can MAKE** -
  `supplier_factors` has no material field. The cheap ones are cheap because they sell a different product
  (our learned rates: aluminium GBP 399.23/m2 vs uPVC GBP 198.62/m2). **I read a discount where the data was
  telling me a material.** Retracted to Adam and on the noticeboard inside the hour.
  He also asked for **a full supply chain list - every supplier, what they actually make, with a source per
  line.** Accepted and deliberately NOT dashed off; a fast capability matrix would be that same error forty
  rows wide. **Next thing I pick up.**
- **29/07 11:30, URGENT - submit this as the first Mary-only quote**, without waiting for suppliers. His
  premise *"we've nothing to lose sending out a cheaper quote"* does not hold: **we are not the cheaper
  quote.** Said so.
- **28/07 21:09 - "We will include strip out to remain competitive."** Settled; do not re-raise the
  principle. The precedent is Fenster's own **Rubery Library** quotation to Pride, 21/10/2025, a job we WON:
  *"All prices include installation and removal of old frames."* The **rate** came later from Brandon Estate
  (Elkins): GBP 150.00/unit, identical across two revisions as the job nearly doubled. Brandon's mean unit is
  3.667 m2 against Redditch's 3.175, so it is not a domestic rate stretched over commercial units - but
  Brandon was 2,202 near-identical openings and Redditch is 41 different references in an occupied library,
  so **GBP 150 is a floor here.**
- **28/07 - "give me an indication of profit"; "do not change any of your coding"**; and look for SBM.
  Pricing-method recommendations made, no code changed: fitted curve per supplier per system instead of the
  band median; code adder as a **percentage** of frame value with a floor, because a fixed sum per unit is
  what collapses margin from 50.7% under 1.5 m2 to 12.2% over 6 m2 (**Redditch averages 3.18 m2 and earns
  24.7%; Crestwood Park averaged 1.29 m2 and earned 42.9% on the same template** - big-unit work has little
  to give away); and Fenster has **two pricing routes that do not agree**, the MASTER PRICING DOC's per-unit
  labour codes and whatever produced the Rubery quote, which carries labour as one GBP 1,620 ancillary line.
- **Adam is to make Mary full-time estimator** - *"search all old jobs, don't stop learning."*

## Traps on this job specifically

- **Read the pricing schedule from the RENDERED page, not the text layer.** The five configuration columns at
  pack p77 are rotated headers 16pt apart (Top Hung 294, Fixed Light 310, Fixed Panel 326, Single Door 342,
  Double Door 358) and a flattened text dump cannot tell a fixed light from a single door.
- **The MASTER PRICING DOC's unit-rate formula hardcodes `code value x 75%` and has no area term**, so it
  cannot express the 125% rule and came out **GBP 750 BELOW the engine on the face of a document we would
  have sent**. Patched here through the template's Additional (L) column. **The real fix is the template.**
- **A print area protects a print, not the file.** 290 populated cells sat outside `$C$1:$I$66` - product
  codes, frame cost, "Supplier used:". Hence the separate CLIENT COPY with formulas resolved to values.
- **Never hardcode a derived rate or factor - ask the engine.** Twice now: the strip-out rate retyped, and
  `supplier_factors` hardcoded, which put a GBP 1,400-light number in a document Adam was about to issue.
- **If you compare a store timestamp against the clock, check the zone.** `poller.log` is BST, work-order
  `received` stamps are UTC. A send I read as 45 minutes old was ninety seconds old.

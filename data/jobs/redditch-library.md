# Redditch Library - BLBS0956

Chat opened 2026-07-28 by triage. History before 29/07 12:20 is in
`data/jobs/redditch-library-archive-2026-07.md`; evidence in `python scripts/mary_recall.py --job redditch-library`.

## Position

**BSW HAVE QUOTED AND MY BENCHMARK WAS 27% HIGH, SO THIS JOB IS WINNABLE AFTER ALL.** BSW QT253829,
04/08, **GBP 43,739.72** for 49 Sheerline Prestige frames against my benchmark GBP 56,993.38. The
GBP 94,926.76 tender sum was built on a frame price that does not exist.

**BUT THE QUOTE ON ADAM'S DESK IS NOT ISSUABLE.** Gintare sent him a pricing document and proposal at
**GBP 79,912.22** on 04/08 10:17, asking whether to send a full proposal to Pride. It omits **GBP 9,641.31**
of scope that has rates (w36, strip-out, required perimeter sealing), and BSW have not priced **five things
the RFQ asked for in writing** (solar control glass, restrictors, the door panic ironmongery, RAL colour,
delivery) - all upward. Corrected floor **GBP 89,553.53 net / GBP 91,849.77 with the 2.5% MCD**, i.e. about
**GBP 1,160 ABOVE Joedan**, not the GBP 10,775 below that GBP 79,912.22 looks like.
`mary_checks`: **3 FAILED - do not issue.** Answered to Adam 04/08 12:5x.

**LEONARD WHITE STILL HOLDS "around GBP 89k +vat"** from Adam's 29/07 11:14 email - the superseded 28/07
figure, flagged to Adam the same day. Coincidentally close to the corrected net above; do not mistake that
for confirmation. **Nothing has gone to Pride from estimating.**

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

**THE FRAME SUPPLY IS NOW SUPPLIER-BACKED.** BSW **QT253829, 04/08/2026, GBP 43,739.72 net ex VAT**,
Sheerline Prestige, **thirty-day validity to 03/09**, **ex works**. 49 frames over 41 references (refs 19
and 20 split into 6 and 3 coupled frames). The old benchmark - a curve fitted to BSW's Severn Trent quote,
`rate = 721.47 x area^-0.4093`, R2 0.9934 - **predicted GBP 56,993.38 and was +27.4% out** (calibration 21).
**The R2 measured the fit, not the product:** Severn Trent was 3005 Wine Red metallic, this is stock Hipca
White. I logged that as a caveat on 28/07 and let the number stand anyway.

**THE COMPETITIVE PICTURE HAS CHANGED** (Joedan gross GBP 90,687.17 / net 88,419.99):

| | GBP |
|---|---|
| Gintare's document as it stands | 79,912.22 |
| + w36 and its installation | 1,641.86 |
| + strip out, 43 nr x 150 | 6,450.00 |
| + perimeter sealing, from OPTIONAL into the price | 1,549.45 |
| **corrected net** | **89,553.53** |
| **with 2.5% MCD, gross** | **91,849.77** |
| vs Joedan gross | **+1,162.60** |
| (+ solar-control premium 1,814.51 if carried at my rate) | 93,710.81 / +3,023.64 |

**Five BSW omissions are still unpriced and all push up.** My own GBP 94,926.76 stands as the last
complete number but is built on the dead benchmark frames - superseded in substance, not yet rebuilt.

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

**With Adam** (all live; nothing new raised - 14 requests already open board-wide):
1. **BACK TO BSW WITH THE FIVE OMISSIONS** - solar glass, restrictors, door ironmongery, RAL, delivery.
   Their quote holds thirty days from 04/08. Nothing should be issued to Pride until these come back.
2. **Add w36, strip-out and sealing** - they have rates and are not in dispute.
3. **The GBP 89k with Leonard** - still outstanding from 29/07.
4. **CDP and its PI** - Fenster or Pride.
5. **The missing prelims block** - stated, not added; his commercial call.
6. **Two house T&C clauses** - the 30-day validity and the **50% deposit** our terms demand, which no main
   contractor pays under JCT. Fix at the template once, not on this tender (the Gordon Court mistake).
7. Whether to also put the corrected schedule to **Aplus, 4Ali or SBM** now that BSW have set a real floor.

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

## 04/08 - what BSW quoted, and what Gintare's document does with it

**BSW QT253829 IS NOT THE SPECIFICATION THAT WAS ASKED FOR.** Gintare's RFQ of 29/07 listed seven things.
Five did not come back, and the quote is silent rather than refusing - so it reads as complete:

1. **Solar control glass.** RFQ asked for *"outer pane 4mm bronze anti sun"*. **All 68 panes are
   `6.8 Lam/18/4mm Clr Tuff EcoPlus 1.0`** - clear. Zero instances of anti-sun, bronze, solar or tint in
   twelve pages. The tender requires solar control; my benchmark carried GBP 1,814.51 for the premium.
2. **Door ironmongery for refs 32/34/37/41.** RFQ asked for Axim 8800 concealed closers, **PR7100 exit
   panic devices**, flush bolts to slave leaves, anti-finger-trap stiles. BSW quoted **Ultion key
   cylinders, Prolinea lever handles, Standard Resi Lock** - a domestic front door - on **fire escape
   doors in an occupied public library**. Zero instances of "panic". Georgie's REQ-12 again.
3. **Window restrictors, 100mm.** Asked for; **not one unit has them**, and 17 units open.
4. **Colour.** All 29 items **9910HG Hipca White** (stock). RFQ said *"standard RAL colour"*.
5. **Delivery.** Footer: *"All estimates are ex works, additional delivery charges may apply."*

**AND ONE UNIT IS MISSING.** Their line reads `Location: w35,36` at **Qty: 1**. Every other multi-reference
line is right (w1,w2 = 2; w22,23 = 2; w16-18 = 3; w24-28 = 5), so there is nothing systematic to spot.
`check_supplier_covers_quantity` fires on it now that `supplier_coverage` is filled. Their footer disclaims
it: *"will not be held responsible for any items missing from quotes"* - and prints **"Bellview"**, not BSW.

**Also from BSW, both bearing on live RFIs:** *"some transoms have been added due to sash size limits"* -
extra transoms across several units, a visible elevational change; and **refs 16/17/18 quoted as flat
2250 x 2304 rectangles** when RFI-01 says they are raked to the stair soffit. Neither is settled.

**GINTARE'S DOCUMENT: THE ARITHMETIC IS RIGHT AND THE SCOPE IS NOT.** Checked row by row on the Brocks Hill
test (sell minus supply against the code value at 75%): **all 22 rows carry their uplift to the penny**,
42 units, sell 71,502.22 on BSW supply 43,739.72 = **38.8% margin**. Installation GBP 8,410 against
GBP 7,420 of fit-only labour from the codes, so **GBP 990 residual - strip-out is not funded**. What is
wrong is what is absent: **w36 (copied through from BSW), no strip-out line anywhere, and perimeter sealing
offered as an OPTIONAL extra** when pack p70 cl.11 requires it and Joedan cl.15 include it - third job.

**THE PROPOSAL SHOULD NOT GO AS DRAFTED, SEPARATELY FROM THE PRICE:**

- **It certifies U-value 1.4 W/m2K.** BSW state no whole-window Uw anywhere; *"EcoPlus 1.0"* is a
  **centre-pane Ug**. Filwood and Georgie's the same week - a performance figure on the face of our
  document that the supplier's own quote does not support.
- The glazing box reads *"6.8mm laminated / 4mm toughened"* - true to BSW, silent on the solar control.
- **Strip out appears nowhere**, not in inclusions and not in exclusions, while *"Waste Removal -
  generally excluded"* does.
- **Working hours stated 07:30-16:30**, against the tender's 08:30-17:30 (prelims) and 08:30-18:00
  (Schedule of Works), in an occupied library where windows cannot be left out over a shift.
- Promises a **full-time CSCS/SMSTS supervisor, a dedicated PM and a separate contracts manager** with
  GBP 990 behind them - the 04/08 Luton board note, live.
- **The ten year warranty is only in the back-page T&Cs.** Against Joedan's twelve months on a 70/30
  award it belongs in the summary and the inclusions.
- **The .xlsx still carries the working columns** - `Supplier used: BSW 43,739.72` in K3/M3, frame cost in
  J and P. **Do not send it.** Both files also carry author *Nicholas Baker*,
  *dan.parker@agsurveying.co.uk* and links into two other people's Outlook caches - REQ-27, not re-raised;
  `scripts\clean_issued_pack.py` strips all of it and neither file was run through it.

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

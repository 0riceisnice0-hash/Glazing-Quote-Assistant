# Redditch Library - BLBS0956

**Chat opened** 2026-07-28 by triage. First working turn 28/07 evening: full take-off from the pack.

| | |
|---|---|
| **Project** | Redditch Library, 15 Market Place, Redditch, B98 8AR. Flat roof refurbishment AND external window and door replacement. Windows and doors only are ours. |
| **End client** | Worcestershire County Council |
| **CA** | Gleeds Cost Management Ltd, Birmingham - Shaun Wilkes BSc (Hons) MRICS. shaun.wilkes@gleed.com (sic, as printed), 07484 058433 |
| **We are invited by** | **Pride Developments Group Ltd**, 8 Forgehammer Industrial Estate, Cwmbran NP44 3AA - Leonard White, Senior QS. leonard.white@pridedevelopments.co.uk, 01633 744134 / 07852 616802 |
| **Our position** | Window and door **sub-contractor to Pride**, who are bidding to Gleeds as main contractor. Our offer goes to Pride, not to Gleeds. |
| **Tender pack** | BLBS0956 v01, May 2026, 254 pages. `Commercial\1. Tender Documents\Pride Developments\Redditch Library` and in the work-order attachment folder. |
| **Deadline** | **NOT SET - do not invent one.** Leonard White, 22/07: acknowledge and "submit your tender back asap", no date. The pack's 12 noon Friday **26 June 2026** is GLEEDS' date to the main contractors and it has passed. Adam has been asked to get Pride's real date. |
| **Live number** | **TENDER SUM GBP 93,526.34, gross of 2.5% MCD, ex VAT** (net GBP 91,188.18) - revised 29/07 when the strip-out rate landed. **GBP 2,839.17 ABOVE Joedan's GBP 90,687.17, +3.13%. THE UNDERCUT IS GONE.** Strip-out now priced at the real rate, 43 nr x GBP 150.00 = GBP 6,450, against the GBP 3,000 allowance guessed on 28/07. **BENCHMARK, and nothing issued to anyone.** |

## Where it stands

Adam, 28/07 18:07, marked Urgent!!: *"Has this one been picked up by estimating? If not, can you please do a
full take off asap and send it to me."* It had not - zero Redditch rows on the Estimating Log. The enquiry
reached info@ on 22/07, Kerry forwarded it to Commercial@ and Adam the same afternoon, and it sat six days.

Take-off done and sent to Adam 28/07 with the workbook. **Nothing has gone to Pride or Gleeds.** No supplier
has been asked and no quotation is held.

## The take-off

**43 items across 41 references, 136.53 m2.** Taken from the tender's OWN blank pricing schedule at pack
**p77**, cross-checked line by line against Joedan's Appendix 2 schedule at **p150** - the two are identical
in every size and configuration - and against elevational drawings **BLBS0956-GLE-RL-XX-DR-B-02** and
**-B-03**. All 41 references appear on the elevations, none missing, none duplicated.

Read the schedule from the RENDERED page, not the text layer. The five configuration columns are rotated
headers 16pt apart (Top Hung 294, Fixed Light 310, Fixed Panel 326, Single Door 342, Double Door 358) and a
flattened text dump cannot tell a fixed light from a single door.

| | GBP |
|---|---|
| Frames + house code adders | 80,426.26 |
| Installation (**fit only**) | 7,670.00 |
| Solar-control glass premium (136.53 m2 x 13.29) | 1,814.51 |
| **BENCHMARK NET ex VAT** | **89,910.77** |
| Strip out existing windows and doors | **TBC - no rate exists** |
| Provisional sum, preparing openings (cl.10) | 5,000.00 |

Band split: `<1.5m2` 11 items GBP 7,325 | `1.5-3` 10 items GBP 14,748 | **`3-6` 20 items GBP 49,153** |
`>6` 2 items GBP 9,200. **62% of the value is in the band the register runs +37.5% high on** (St Mary's), so
expect this high. Band-corrected sensitivity: **GBP 79,047.55**.

Outputs: `outputs\Redditch Library - Fenster Take-Off and Benchmark Price.xlsx` (5 sheets),
`outputs\redditch-takeoff.json`, `scripts\redditch_takeoff.py`, `scripts\redditch_takeoff_doc.py`.
`mary_checks.py` on `data\job-checks\redditch-library.json`: **all checks pass.**

## The seven things that matter

1. **THE SPEC COUPLES A THERMALLY BROKEN WINDOW TO A NON-THERMAL DOOR AT REFS 32 AND 34, AND IT CANNOT BE
   BUILT.** Both are drawn on Elevation C as ONE assembly, window frame joined straight to door frame. The
   spec puts windows in **EL75mm Squareline** (thermally broken, 75mm) and doors in **AC100 Commercial**
   (non-thermal, 100mm). Adam's SM5 Wexham ruling of 24/07 exactly - except that on SM5 it was our own quote
   that coupled two depths, and here it is written into the client's specification. Following Adam's rule
   literally (window takes the door's system) puts 32.1 and 34.1 in a non-thermal frame and outside the
   1.4 W/m2K requirement, so the rule and the spec cannot both be obeyed. **Priced with both runs in one
   thermally broken system throughout** and RFI-03 puts the three resolutions back to Gleeds. GBP 7,552.56
   sits on these two.
2. **STRIP-OUT IS A BLANK LINE ON THE CLIENT'S OWN FORM AND WE CANNOT FILL IT.** Pack p70 ends with two
   blanks: *"Cost for stripping out windows"* and *"Cost for new windows and doors"*. We can fill the second.
   The house labour codes are **fit-only** - proven on Princess Beatrice (GBP 39,680 over 217 units) and on
   Brocks Hill, a new build with nothing to remove, which recomputes from the same codes. No strip-out
   category exists in the rate register. **Fifth job** after Gordon Court, St Mary's, Princess Beatrice and
   John North Hall - and the worst, because on those it was an implied inclusion we absorbed and here it is a
   line we hand back empty. Added to **REQ-24**, not raised separately.
3. **THE SPECIFIED SYSTEMS ARE THE COMPETITOR'S OWN.** EL75mm Squareline and AC100 Commercial are Joedan
   Manufacturing products. Fenster cannot buy either. Spec 3.5.3 cl.3 permits an alternative but the tenderer
   *"will become responsible for the design ... under contractor's designed portion"*, with a **compliance
   specification required WITH the tender return** and written CA and Client approval. Prelims want
   **GBP 5m PI for Contractor Designed Works**, stating **both "12 years" and "Six years"** (RFI-09).
4. **REFS 16, 17, 18 ARE RAKED, NOT RECTANGULAR.** Parallelograms following the stair soffit on Elevation A -
   sloping head and cill - scheduled as 2250 x 2304 rectangles, all three identical, and Joedan priced all
   three at exactly GBP 2,619.48. GBP 8,509 of the benchmark. RFI-01.
5. **REF 38 IS DRAWN AS A 15-PANE SCREEN AND SCHEDULED AS 6 FIXED LIGHTS.** 2700 x 1700, a 5 x 3 grid at
   300dpi. Four mullions and two transoms is not the same buy as 6 lights. RFI-05.
6. **REFS 29, 30, 31 HAVE NO CONFIGURATION AT ALL** - every column blank on Gleeds' schedule as well as
   Joedan's, so the tender is silent, not the transcription. Priced as fixed lights, stated. RFI-02.
   And **ref 39 is the one door missing from cl.5's ironmongery list** (32, 34, 37, 41) - no ironmongery
   specified anywhere, priced with no panic set. RFI-06.
7. **ASBESTOS IS GOOD NEWS ON THE WINDOWS AND BAD NEWS BESIDE THEM.** All four window-specific samples -
   FM000123/124/126/127, mastic and putty to the metal window frames, 75 linear metres - **NO ASBESTOS
   DETECTED**. But **FM000125: asbestos bitumen paint to metal cladding, chrysotile, 100 m2, "left hand
   elevation", easily disturbed, "REMOVE if affected by scheduled work"**. If that is the raking wall
   carrying 16/17/18, our strip-out disturbs it. RFI-07. The pack's GBP 5,000 provisional sum covers the
   whole building including the roof.

## Joedan - the competitor's price, in the pack

**Appendix 2 is not a specification. It is Joedan Commercial Division's quotation to Gleeds** - JCQ.9727,
23/03/2026, Nathan Swenson - left in complete with rates. **GBP 90,687.17 ex VAT gross of 2.5% MCD**, so
**GBP 88,419.99 net** to a main contractor. Gleeds then lifted Joedan's spec verbatim into 3.5.3, down to
the sentence *"Doors 32,34,37,41are priced with"*.

**Ours is -0.9% on their gross and +1.7% on their net - and that agreement is an accident.** Joedan's figure
**includes strip-out** (their cl.12) and ours excludes it, so on identical scope **we are already above them**
before strip-out is added. Pulling the other way, the register runs high in this job's dominant band.
Logged as calibration entry 7 - the first entry whose comparator is a competitor's tendered price.

Their 12-month warranty against our ten years. Their exclusions are our house position almost exactly: no
access equipment of any kind, no skips, no containers, no Building Control, no asbestos removal, no mag
locks, no manifestations, no up-stand where windows meet the flat roof, disposal on the main contractor.

## Contract terms (pack p20-22)

JCT Minor Works with CDP. **10 weeks to completion** from commencement (TBC). **LDs GBP 1,000/calendar week.**
Retention 5%, to 2.5% at PC. Rectification six months. PL GBP 5m. CDP PI GBP 5m. No amendments to sections
3-7. **The JCT form itself is not in the pack and no sub-contract has come from Pride.**
Award: **70% price / 30% quality.**

**Two validity periods in one pack:** Form of Tender says the sum stays open **10 weeks** from submission;
prelims p23 say **"not less than 3 months"**. Either way, aluminium quotes run 30 days - **5 to 10 weeks
uncovered** (RFI-08). Do not send an RFQ until Pride confirm when they actually submit.

Occupied public library throughout. Working hours **08:30-18:00** in the Schedule of Works and **08:30-17:30**
in the prelims. Windows may not be left out over a shift. Elevation A fronts a public highway. FORS Gold for
vehicles. **ONE tender site visit only**, through Gleeds, all sub-contractors present - while 3.5.3 requires
a measured survey of every opening before ordering and forbids relying on Gleeds' dimensions (RFI-10).

## Open

- **Adam** - Pride's real deadline from Leonard White; a strip-out number (REQ-24); whether Fenster carries
  the CDP and its PI or Pride do; whether we bid at all.
- **10 RFIs** for Pride to pass to Gleeds, on the workbook's RFIs sheet. The invitation requires technical
  queries to go to Gleeds under the JCT Tendering Practice Note 3rd Ed 2017.
- **No RFQ sent** - deliberately. The 30-day clock should not start before Pride's date is known.

## Decisions taken and why

- **Priced ours first, compared to Joedan second.** Triage's instruction, and right - a fully priced
  competitor schedule in the pack is the easiest thing in the world to anchor to.
- **Refs 16/17/18 priced as windows, not curtain walling.** Checked at 200dpi: each is a glazed band with
  solid wall above the head and below the cill, not floor to soffit. Worth about GBP 7,000 if wrong
  (CW would give GBP 15,552 against GBP 8,509) and it is the single line most worth a second opinion.
- **Refs 19 and 20 priced as ELAW/LAW ribbons, not CW** - 900mm and 1100mm tall, window bands in a wall.
- **Solar-control glass carried as a separate GBP 1,814.56 line** rather than by swapping to the
  "incl solar control" register categories, which have n=1 to n=39 behind them. The glass-unit medians
  differ by GBP 13.29/m2 (103.03 solar vs 89.74 plain softcoat) and that is the defensible number.
- **Nothing sent to any supplier or to Pride.** Ghost protocol, and the validity clock.


## 28/07 evening - Adam's reply: undercut Joedan, and give me a profit figure

Adam 19:26: *"We need to undercut Joedan on this one and secure these works with Pride! Not good this
has gone 6 days missed. Are you confident in your pricing? We already know the price to beat, so give
me an idea of profit on this."* Plus: Mary is to become Fenster's full-time estimator - *"search all
old jobs, don't stop learning."*

**PROFIT.** Material we buy GBP 62,365.77 (frames 60,551.26 + solar glass 1,814.51). House code adders
GBP 19,875.00 - that is the margin. Installation GBP 7,670.00 is revenue, not margin: **what fitting
costs Fenster is recorded nowhere.** So gross margin is **GBP 19,875.00 = 22.1% of sell, 31.9% mark-up
on material**, and only if fitting breaks even. No prelims, supervision, survey, MCD or strip-out in it.

**WHY THIS JOB EARNS LESS - AND IT IS THE TEMPLATE.** The code adder is a FIXED SUM PER UNIT, so it
thins as units grow: **50.7%** of the frame line under 1.5 m2, 38.6% at 1.5-3, **19.0%** at 3-6,
**12.2%** over 6. Redditch averages 3.18 m2 a unit and earns **24.7%**; **Crestwood Park averaged
1.29 m2 and earned 42.9%** (GBP 20,550 of adders on a GBP 27,329.60 BSW buy, both verified). Same
template, nearly double the margin, purely on unit size. Big-unit work has little to give away.

**CONFIDENCE - AND THE BEST COMPARATOR WE OWN.** Found **BSW QT250834, 15/06/2026 - a Sheerline
Prestige quote to us for PRIDE's Severn Trent job.** Six lines, 27 units, 72.578 m2, reconciling
exactly to GBP 34,902.35. Same supplier, same client, six weeks old, same product family, sizes
bracketing ours. Rates fit `rate = 721.47 x area^-0.4093`, **R2 = 0.9934**. Redditch re-priced on it:
frames **GBP 56,995.38** vs the engine's 60,551.26, sell **GBP 86,354.89**.

By band, engine error (positive = engine above the real price):

| band | St Mary's | Severn Trent |
|---|---|---|
| <1.5 m2 | -35.5% | -38.9% |
| 1.5-3 m2 | -1.2% | -20.4% |
| 3-6 m2 | +37.5% | +18.1% |
| >6 m2 | +35.2% | +34.1% |

**Two independent jobs agreeing within four points on the small band and one point on the large.** The
band structure is now evidenced twice. Calibration entry 8. Two caveats, both pushing the comparator
HIGH: Severn Trent is 3005 Wine Red metallic, and its outer pane is 6.8 laminated not 4mm toughened.

**THREE ESTIMATES:** engine GBP 89,910.77 | Severn Trent curve **GBP 86,354.89** | St Mary's band
correction GBP 79,047.50. The whole spread is the 3-6 m2 band, which carries 62% of this job.

**CAN WE UNDERCUT JOEDAN? NOT ON WHAT WE HAVE.** The target is **GBP 88,419.99** - Joedan's
GBP 90,687.17 is GROSS of 2.5% MCD - and **it includes their strip-out**.

| basis | our sell | headroom | per opening |
|---|---|---|---|
| engine benchmark | 89,910.77 | **-1,490.78** | -34.67 |
| Severn Trent curve | 86,354.89 | 2,065.10 | 48.03 |
| St Mary's band correction | 79,047.50 | 9,372.50 | 217.97 |

Headroom is what is left to strip 43 openings out of an occupied library. **At the benchmark there is
none.** GBP 48 an opening is not obviously enough, and I cannot prove it either way.

**STRIP-OUT: PROPERLY SEARCHED NOW, AND IT DOES NOT EXIST.** Scanned **362 archive workbooks**.
Promising hits - Spencer Scroft *"Carefully remove existing PVCu doors and windows"* against 30.06,
Hollyfield *"remove existing PVCu framed windows"* against 24.11 - **are ITEM REFERENCE NUMBERS, not
rates.** Opened the files: the Rate columns are empty; they are unpriced schedules main contractors
sent US. Nearly reported them as rates. The Axis CLC / EEM schedule does hold Fenster-priced *renew*
rates (remove+replace, uPVC, GBP 267.75-838.84/m2), but some fall BELOW our supply-and-fit-new price,
so differencing them to extract strip-out would invent a number. **Not done.**

**RFQ BUILT AND SENT TO ADAM, NOT TO A SUPPLIER** (ghost protocol - I can only email adam/marketing).
`outputs\Redditch Library - RFQ Schedule for Supplier.xlsx`, a **separate file with no prices in it**,
deliberately not the take-off (which carries our buy, our margin and Joedan's price - the REQ-28
mistake). It asks for refs 32/34 as single coupled units in ONE depth, asks for validity beyond 30
days, and flags refs 16/17/18, 38 and 29/30/31. **Recommended to BSW *and* Aplus or 4Ali:** measured
supplier factors are BSW +5.7% (n=272), Aplus -1.6% (n=83), 4Ali -1.5% (n=82), TruFrame -17.9% (n=42)
- about **GBP 4,200** of frame buy on this job, twice the headroom we have.

**PRIDE, FROM OUR OWN LOG.** They are on Fenster's **Priority Customer** list. **19 rows** on the
Estimating Log (not 14 as triage had it) - and **every one has a blank win/loss column**. We have no
recorded outcome on any Pride job ever, yet **RAF Mildenhall sits under `2. Projects`**, so we won at
least one and never wrote it down.

**Correction made this turn:** the area is **136.53 m2**, not 136.54. Five 900x525 units at exactly
0.4725 m2 rounded up or down depending on the order of the division. Worth GBP 1.24; fixed at source
so one figure circulates. Sell moved GBP 89,910.82 -> GBP 89,910.77.

**Still open with Adam:** (1) send the RFQ, and to whom; (2) strip-out number or absorb it (REQ-24);
(3) Pride's real deadline from Leonard White.


## 28/07 21:30 - Adam: put it in the pricing document, undercut Joedan, match their inclusions, sell the ten years

Adam 19:43: *"Can you put this into our pricing document, but we need to undercut Joedan. We also need
to ensure we inform the client of our 10 year warranty, which we can manually put in a proposal
document. We will also need to include the same inclusions/exclusions as Joedan."*

**BUILT AND SENT TO ADAM, NOT TO PRIDE.** Three files:

| file | who it is for |
|---|---|
| `outputs\Redditch Library - Fenster Pricing Document (CLIENT COPY).xlsx` | **Pride.** Values only, working columns emptied, scrubbed. |
| `outputs\Redditch Library - Fenster Proposal.pdf` | **Pride.** Price, 11 inclusions, 25 exclusions, ten year guarantee, house T&Cs. |
| `outputs\Redditch Library - Fenster Pricing Document.xlsx` | **Adam only.** Codes and frame cost live in B and J-O. |

Built by `scripts\redditch_pricing_doc.py` on the house template through
`scripts\generate-fenster-docs.py`. `mary_checks.py`: **all pass** (three FAILED first - see below).

### The tender sum

**GBP 89,218.65 gross of 2.5% MCD**, stated on the same basis as Joedan's GBP 90,687.17 so the two
can sit side by side. Net GBP 86,988.18 against their GBP 88,419.99. **Undercut GBP 1,468.52, 1.62%.**

| | net GBP |
|---|---|
| frames, second-supplier basis | 53,057.22 |
| house code adders | 19,875.00 |
| installation (fit only) | 7,670.00 |
| solar-control glazing | 1,814.51 |
| perimeter sealing, 314.29 lin m x 5.00 | 1,571.45 |
| **strip out - ALLOWANCE, NOT A RATE** | **3,000.00** |
| net | 86,988.18 |
| add 2.5% MCD | 2,230.47 |
| **TENDER SUM** | **89,218.65** |

The 46 rows are the 43 scheduled positions plus sealing, solar glazing and strip-out; installation
comes off the template's own labour-code SUMPRODUCT. The sheet reconciles to the penny.

### Matching Joedan's inclusions is what moved the price

Their lists taken verbatim from pack p151-153. Four of their inclusions were not in the 19:56
benchmark, and three cost money:

1. **Their cl.12 INCLUDES removal of the existing elements.** So Adam's "match their inclusions"
   settles the strip-out question by the back door - it is in our price now. (Corroborated the same
   evening on a different job: Adam on Princess Beatrice, *"I decided I would include the strip out
   (effectively FOC) in order to remain competitive."*)
2. **Perimeter sealing, their cl.15 - GBP 1,571.45.** Pack p70 cl.11 REQUIRES it. Our house
   documents have always offered mastic as an OPTIONAL extra: that is the Princess Beatrice REQ-6
   error, offering as an option work we are obliged to do. It is inside the sum and the OPTIONAL
   block is deleted from the face of the client copy.
3. **45mm cellular uPVC cloaking profile, their cl.13 - NO RATE EXISTS.** Carried as included scope
   at nil. ~314 lin m of trim. Must come back on a supplier quote.
4. Trickle vents, their cl.4 - already had.

**The one deliberate divergence is the warranty:** Joedan cl.21 gives twelve months, we give ten
years, and the proposal says so in as many words. No supplier will back ten years, so the difference
sits with Fenster.

### The strip-out allowance is the decision Adam has to make

GBP 3,000 net, GBP 69.77 an opening, 43 metal-framed openings in an occupied library. **Not a rate**
- none exists, 362 workbooks searched. **The undercut and the allowance come out of the same pot:**

| allowance | tender sum | undercut | per opening |
|---|---|---|---|
| 2,000 | 88,193.01 | 2,494.16 (2.75%) | 46.51 |
| **3,000 (as built)** | **89,218.65** | **1,468.52 (1.62%)** | **69.77** |
| 4,000 | 90,244.29 | 442.88 (0.49%) | 93.02 |
| 4,431.81 | 90,687.17 | nil, we match them | 103.07 |

### The undercut depends on a supplier we have not asked

Frames are the BSW Severn Trent curve converted to a second-supplier position by the measured
factors (BSW +5.7% / Aplus -1.6%), worth **GBP 3,936.12** of frame buy. **On BSW's own rates, with
sealing in and NO strip-out at all, we are at GBP 90,178.77 gross - GBP 508 under Joedan with
nothing left to strip 43 openings.** So: the RFQ has to go and come back before this is issued, or
we are ~GBP 3,900 underwater on our own document.

### Three things mary_checks.py caught before anything could go out

1. **The house template's inherited identity** - `dan.parker@agsurveying.co.uk` in docProps and two
   live external links into `C:\Users\Parke` and `C:\Users\LiamO'Donnell` Outlook caches. REQ-27.
   Scrubbed in place on both files.
2. **A print area protects a print, not the file.** 290 populated cells outside `$C$1:$I$66` -
   product codes in B, frame cost in J-O, and "Supplier used:" in K3/L3. Anyone opening the .xlsx
   and scrolling right reads our buy and our margin. Hence the separate CLIENT COPY: formulas
   resolved to values, working columns emptied.
3. **A line priced and disclaimed in the same pack** - my own manifest error on the GBP 5,000
   provisional sum. Removed; it is excluded, as Joedan also excluded it.

### Two generator bugs fixed at source, not just here

- `generate-fenster-docs.py` never extended the template's `$C$1:$I$31` print area, so **any job
  with more than 12 rows produced a PDF that stopped mid-schedule.** Now sized to the real end.
- The template merges C:D across its own twelve rows only, so every cloned row lost the merge and
  clipped its description. Now merged, wrapped, and row heights set.

### Two clauses on the back page of our own proposal that a QS will find

Both are the HOUSE terms, so they are on every proposal Fenster sends - **not edited here**, because
fixing one tender and leaving the template wrong is the Gordon Court mistake. Put to Adam:

1. **Validity.** Our T&Cs say 30 days. The Form of Tender holds the sum open 10 weeks; the prelims
   say not less than 3 months. A return whose own terms expire before the client's validity period
   is non-compliant on its face.
2. **Payment.** Our T&Cs demand a 50% deposit before commencement. The head contract is JCT Minor
   Works with 5% retention to 2.5%. No main contractor pays a 50% deposit under JCT. Joedan met the
   same point by stating their retention release instead.

### Open with Adam after this turn

1. Confirm or move the **GBP 3,000 strip-out allowance** (REQ-24).
2. **Send the RFQ**, and to Aplus or 4Ali as well as BSW - the undercut depends on it.
3. **Pride's real deadline** from Leonard White. Still no date from anybody.
4. CDP and its PI - Fenster or Pride.
5. The two house T&C clauses above - fix at the template, once.


## 28/07 22:10 - Adam's second reply: strip out is IN, four Pride wins exist, SBM, and how to price better

Adam 20:09: *"We will include strip out to remain competitive. We have won bigger jobs with Pride.
Namely Rubery Library and 92-94 High St Merthyr Tydfil. Please do not change any of your coding but,
give me an indication of how you would better price up jobs instead of our current system. There's
not much to go on at all, but try looking for SBM quotes to get a new idea of cheaper supply on
aluminium windows."*

**STRIP-OUT IS SETTLED, AND WE HAD THE PRECEDENT ALL ALONG.** Fenster's own issued quotation
`Commercial\2. Projects\2. Completed\Pride Developments\Rubery Library\Client Quote\Pride
Developments - Rubery Library Quotation (REV 2).pdf`, **21/10/2025, GBP 24,096.72 ex VAT**, says on
its front page: ***"All prices include installation and removal of old frames."*** Same client, same
building type, a job we WON. The first Fenster document found anywhere that puts frame removal
inside the price in writing. **Still no RATE** - Rubery does not break it out, and differencing it
would invent one. REQ-24 stays open for the rate, not the principle.

**RUBERY LIBRARY IS THE COMPARATOR THIS JOB SHOULD HAVE BEEN PRICED AGAINST.** Same client, same
building type, won, with drawings, glass sizes, O&M and a full Finance folder. Better than Severn
Trent. **Not re-priced on it tonight** because Rubery is mixed - Liniar EnergyPlus uPVC casements on
the small windows (frames 1-4, GBP 416.98 to 692.65) and aluminium only on the four big screens
(frames 5-8, GBP 3,293.52 to 4,722.71) - so it needs unpicking properly. **First job next turn.**

**FOUR PRIDE WINS CONFIRMED, NONE OF THEM ON THE LOG.** `2. Projects\2. Completed\Pride
Developments` holds **Rubery Library**, **92-94 High Street (BARCODE)** and **Catherine's House,
Plymouth 2026**; **RAF Mildenhall** is live under `2. Projects\Pride Developments`. Pride have 19
Estimating Log rows and every win/loss cell is blank. Log-wide it is 327 jobs, 24 marked, 7.3%.
**Not yet on the hub Scoreboard** - outcomes are written through a deploy and the deploy is locked.

**SBM GLAZING LTD IS REAL AND OFF-REGISTER.** 418-420 London Road, High Wycombe, co. 12083999, VAT
332846302. A **Cortizo** fabricator; Raj quotes `estimating@` direct. **Not on the Suppliers
Listing** - used job by job. Three documents: Raglan School 26/06/2026, 5 aluminium windows
**UNGLAZED**, white, GBP 2,500, 2-3 week lead; Welland Place 11/05/2026, 1 window **UNGLAZED**
RAL 7005, GBP 500; Pincents Kiln 07/05/2026, GBP 8,560, 4 windows + 1 commercial door, **glazed**,
supply only.

**NO RATE DERIVED, DELIBERATELY.** Two of the three are unglazed, which is a different product from
our glazed rates. The third has no schedule that belongs to it - the drawings and glass order in
that folder are dated a MONTH after the proforma and cover **12 positions, not 5**. Pairing them
would manufacture a rate. Same trap as the strip-out "rates" that were item reference numbers.
**The answer is to put SBM on the Redditch RFQ**, which is written and price-free. Caution first:
their terms want 50% with order, balance before delivery, title retained until paid - on a
GBP 53,000 frame buy that is real cash flow and it is not how BSW trade with us.

**PRICING-METHOD RECOMMENDATION MADE, NO CODE CHANGED** (Adam: *"do not change any of your coding"*).
Three points, all evidenced: (1) replace the band median with a fitted curve per supplier per system
- `rate = a x area^b`, R2 0.9934 on six real BSW points - which removes the band cliff entirely;
(2) make the code adder a PERCENTAGE of frame value with a floor, because a fixed sum per unit is
what collapses margin from 50.7% to 12.2% as units grow; (3) Fenster has **two pricing routes that
do not agree** - the MASTER PRICING DOC with per-unit labour codes, and whatever produced the Rubery
quotation, which carries labour as a single **GBP 1,620 ancillary line**. Same client, same year.


## 29/07 09:10 - the strip-out rate landed and took the undercut with it

Work order: Adam 08:51 forwarded Leonard White's original 22/07 enquiry to **estimating@ / Gintare**,
cc commercial@, *"Can we look at this one urgently please, it got missed and has been with us for 6
days!"* No new information in it - it is the same chain that reached this chat on 28/07.

**FLAGGED TO ADAM, CAREFULLY.** As at 09:05 the record shows the pack being pushed to Gintare as
unpriced, while a full take-off, pricing document, client copy and proposal have been sitting with
Adam since 21:20 and 22:10 last night. Reported as *what the record shows and how old it is* - the
Georgie's 09:20 rule - not as "Adam forgot". Offered the fix: forward the three attachments to her.

### The number moved, twice, and only one movement was mine

| | GBP |
|---|---|
| frames (second-supplier basis) | 53,057.22 |
| house code adders | **20,625.00** (was 19,875.00) |
| installation (fit only) | 7,670.00 |
| solar-control glazing | 1,814.51 |
| perimeter sealing | 1,571.45 |
| **strip out - 43 nr x GBP 150.00** | **6,450.00** (was a 3,000 guess) |
| net | 91,188.18 |
| add 2.5% MCD | 2,338.16 |
| **TENDER SUM** | **93,526.34** |

**STRIP-OUT NOW HAS A RATE, FROM REQ-24 VIA THE ST MARY'S CHAT.** Fenster's own Brandon Estate
tender to Elkins: *"Removal of existing frames"* **GBP 330,300 / 2,202 units** in REV 2 and
**GBP 198,750 / 1,325** in the earlier revision - **GBP 150.00 per unit to the penny in both**, so a
per-unit rate held as the job nearly doubled. A **SELL** rate off client-facing documents, so not
marked up. Taken from `mary_pricing.strip_out()` rather than retyped.

**TRANSFERABILITY CHECKED, NOT ASSUMED.** Read Brandon REV 2 at source: **2,202 units, 8,075.8 m2,
mean 3.667 m2** against Redditch's **3.175**. So it is *not* a small-domestic-window rate stretched
over commercial units - ours are the smaller. Per m2 it is **GBP 40.90**, which over 136.53 m2 gives
GBP 5,584.08; the per-unit basis is the dearer and is what is carried, consistent with St Mary's.
**What does not transfer is the repetition** - Brandon was 2,202 near-identical openings, Redditch is
41 different references in an occupied library. **GBP 150 is a floor here.**

**THE ADDERS ROSE GBP 750 AND IT WAS NOT MY DOING.** Commit `de7bd93` from another chat measured the
estimator's own rule across 30 sent quotes: **above 6 m2 the adder is the code value at 125%, not
75%.** Redditch has exactly two such units - ref 20 at 7.7 m2 (LAW 650) and ref 19 at 15.3 m2
(ELAW 850) - and 650x0.5 + 850x0.5 = **750.00 exactly**. Fully accounted for; nothing unexplained.

### THE UNDERCUT IS GONE, AND WHAT IT WOULD TAKE TO GET IT BACK

**GBP 93,526.34 against Joedan's GBP 90,687.17 = GBP 2,839.17 ABOVE, +3.13%.** Last night we were
1.62% under, on a GBP 3,000 strip-out guess.

- Frames would have to fall **GBP 2,768.19 = 5.22%** - and that is *on top of* a frame price that
  already assumes we move off BSW to Aplus/4Ali.
- **On BSW's own quoted curve** the tender sum is **GBP 97,565.72**, GBP 6,878.55 above Joedan, and
  the cut needed is **11.77%**.
- So **no evidence we hold can undercut Joedan on this scope.** Only a real supplier quotation
  beating the assumed Aplus position by another 5% can. **The RFQ is still with Adam, unsent.**

### THE GAP THAT IS BIGGER THAN THE UNDERCUT - WE CARRY NO PRELIMS AT ALL

Reading Brandon for the strip-out rate exposed what a complete Fenster commercial pricing document
carries. Below the item schedule, Brandon REV 2 has:

- **INSTALLATION ALLOWANCES** - bay posts 50,400; Removal of existing frames 330,300; **Installation
  fixings and ancillaries 49,725 (= GBP 22.58/unit)**; **PHASED INSTALLATION 572,750**.
- **PRELIMS** - Site Survey 6,375 | Project Management 101,700 | Commercial Management 26,250 |
  Technical Coordination 35,250 | Site Supervision 111,150 | QA Certification & Handover 9,525.
  **Subtotal GBP 290,250 on GBP 6,906,445.63 of works = 4.203%.**

**Redditch has none of it.** No survey, no supervision, no project management, no QA handover, no
phasing allowance - on an **occupied public library, 10 weeks, LDs of GBP 1,000 a calendar week**,
windows that cannot be left out over a shift, and a public-highway frontage. On our net, 4.203% is
**GBP 3,832.27**, and the fixings line another **GBP 971.01**. **NOT ADDED** - it would take us
further above Joedan and it is Adam's commercial call - but stated to him rather than left silent.

### A TEMPLATE FAULT THAT WOULD HAVE SHIPPED SILENTLY

The MASTER PRICING DOC's unit-rate formula hardcodes `code value x 75%` and **has no area term**, so
it **cannot express** the new 125% rule. Left alone, the spreadsheet's own arithmetic came out
**GBP 750 BELOW the engine on the face of a document we would have sent**. Caught only because the
client copy's line sum would not reconcile to the build-up.

**Patched here** by carrying `line["adder"] - CODE_VALUE[code] * ADDER_FACTOR` in the template's
**Additional (L)** column - the formula is `J+K+L+code*75%`, so the delta lands correctly and Frames
keeps the true frame cost. Sheet now reconciles to GBP 93,526.34 exactly. **The real fix is the
template, once** - a formula with no area term cannot be patched job by job forever. On the board.

### mary_checks: a FAIL that was correct, and the fix

The vesuvius chat widened `check_fabricator_can_make_it`: a fabricator string that *says nobody can
make it* now fails. Our manifest recorded **"Joedan Manufacturing (UK) Ltd - their own system, not
available to Fenster"** against both specified systems - a statement that nobody can build what we
are selling, passing a check that exists to catch precisely that.

**Fixed honestly.** `systems_specified` now records **what Fenster is actually quoting** - a
thermally broken 75mm system (Sheerline Prestige or equivalent) tendered as the Contractor's Designed
Portion alternative that Gleeds 3.5.3 cl.3 expressly permits, with BSW/Aplus/4Ali/SBM as fabricators
- because the rule asks whether *the thing we are selling* can be built. That the specified systems
are the competitor's own and unbuyable stays in `exposures`, with its CDP and PI consequences.
**All checks pass.**

### Two smaller things off this morning's forward

- Leonard White's enquiry says *"please scroll to page 147 Appendix 2"* - **Pride have pointed us at
  the competitor's priced quotation as the scope document.** Our number is being read against a
  document they handed us.
- The enquiry is addressed **FAO Mr Paul Taylor**, not to estimating.


## 29/07 11:25 - the RFQ went out, to the one supplier that cannot win it

Work order: `estimating@` -> `estimations@bsws.co.uk`, 11:19 BST, *"Could you please prepare an
Aluminium quote as per the attached."* Gintare acting on Adam's 08:51 forward. Untrusted sender
(estimating@ is not on the trusted list), so read as evidence, not instruction. Nothing in it asks
anything of this chat.

**THE FINDING: BSW IS THE ONE SUPPLIER THAT CANNOT BEAT JOEDAN, AND IT IS THE ONLY ONE ASKED.** Our
GBP 93,526.34 already assumes an Aplus-level buy. Running the job through the measured supplier
factors (our own sent pricing documents, code and band matched):

| supplier | frame buy | tender sum | vs Joedan 90,687.17 |
|---|---|---|---|
| **BSW +5.7% (n=272) - the only one asked** | 56,993.38 | **97,563.42** | **+6,876.25 ABOVE** |
| Aplus -1.6% (n=83) - assumed today | 53,057.22 | 93,526.34 | +2,839.17 |
| 4Ali -1.5% (n=82) | 53,111.14 | 93,581.64 | +2,894.47 |
| **TruFrame -17.9% (n=42)** | 44,268.27 | **84,512.03** | **-6,175.14 UNDER** |

BSW is **GBP 3,936.16** of frame buy dearer than the level already baked into our published number.
So their quote will land above our own figure and read as *"Redditch is not winnable"* when what it
says is *"we asked the dearest supplier"*. **Only TruFrame clears Joedan** - by enough to pay for the
missing prelims too. Caveated to Adam and on the board: n=42 is the thinnest of the four, and a
supplier factor says nothing about whether that supplier can FABRICATE a thermally broken 75mm
commercial system with panic-hardware doorsets at these sizes. It says who is worth an envelope.

**Emailed Adam with the price-free RFQ schedule attached**, asking him to send it to Aplus, 4Ali,
TruFrame and SBM. Ghost protocol - I cannot send it myself.

**RFQ schedule corrected** before sending: area 136.54 -> **136.53 m2**, the figure fixed at source on
28/07 so one number circulates. Everything else in it stands - trickle vents, panic ironmongery, refs
32/34 as single coupled units in ONE depth, the raked units, ref 38's 15 panes, refs 29/30/31, and an
explicit ask for validity against a 10-week tender.

### Two observations, one of which I nearly reported wrongly

**No attachment on the BSW email.** The body says "as per the attached"; our copy carries none.
Control checked first - **31 of 110** sent messages in the store do carry attachments, so a zero is
real evidence rather than a hole in the record.

**But the clock nearly caught me.** I first read the send as ~45 minutes old. It was **ninety
seconds**: `poller.log` runs in **BST** and the work order `received` stamps in **UTC**. Ninety
seconds is not long enough to conclude anything - the same flag on Georgie's yesterday was right on
the evidence and wrong about the world by a minute. Reported to Adam as *"worth a glance"*, with the
age stated, not as a mistake. **If you compare a store timestamp against the clock, check the zone.**

**The part that is NOT time-sensitive: send the RFQ schedule, never the tender pack.** Joedan's fully
priced quotation sits at **page 147** of the Redditch pack - the client left it in and Leonard White's
own covering email points us at it. Forwarding that pack to a supplier hands them the market price for
the job before they quote it to us. REQ-28's shape, opposite direction.

**Position unchanged:** GBP 93,526.34 gross of 2.5% MCD, benchmark, nothing issued to Pride, no
deadline from Leonard White.

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
| **Live number** | **GBP 89,910.77 net ex VAT, BENCHMARK ONLY**, excluding strip-out. Best evidence says **GBP 86,354.89**. Nothing issued to anyone. |

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

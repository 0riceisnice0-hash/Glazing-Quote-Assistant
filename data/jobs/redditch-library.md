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
| **Live number** | **GBP 89,910.82 net ex VAT, BENCHMARK ONLY**, excluding strip-out. Nothing issued to anyone. |

## Where it stands

Adam, 28/07 18:07, marked Urgent!!: *"Has this one been picked up by estimating? If not, can you please do a
full take off asap and send it to me."* It had not - zero Redditch rows on the Estimating Log. The enquiry
reached info@ on 22/07, Kerry forwarded it to Commercial@ and Adam the same afternoon, and it sat six days.

Take-off done and sent to Adam 28/07 with the workbook. **Nothing has gone to Pride or Gleeds.** No supplier
has been asked and no quotation is held.

## The take-off

**43 items across 41 references, 136.54 m2.** Taken from the tender's OWN blank pricing schedule at pack
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
| Solar-control glass premium (136.54 m2 x 13.29) | 1,814.56 |
| **BENCHMARK NET ex VAT** | **89,910.82** |
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

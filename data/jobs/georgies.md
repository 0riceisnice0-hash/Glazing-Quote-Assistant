# Georgie's (formerly Rosebank) - Pearce Construction (Barnstaple)

Job chat key: `georgies`. Opened 27/07/2026 when Mercury's quote landed. This file is the backup for
that chat's memory.

## What the job is

**Rosebank Georgies Youth Centre, Derby Road, Barnstaple, Devon EX32 7EZ.**
Devon County Council **PSDS4 Energy Improvement Scheme** (decarbonisation). Employer's agent /
contract administrator: **South West Norse Ltd** (Venture House, Capital Court, Sowton, Exeter).
SWN project number **08-02-119364**. Main contractor tendering: **Pearce Construction (Barnstaple)**;
Fenster is pricing the glazing package to Pearce.

Fenster's package is element **1.1 Replacement Windows and Doors** of Pearce's Tender Sum Analysis.
Scaffolding (1.2), asbestos removal (1.3), cavity wall and roof insulation, M&E and PV are separate
elements on that same breakdown - so they are Pearce's lines, not ours. That matters when reading the
spec, which addresses everything to "the Contractor".

**Scope (spec 2.2):** 23 no. external windows (W01-W23), 8 no. external doorsets (D01-D08), 2 no.
sections of full height curtain walling / screens (CW01, CW02, with door D03 in the run).

**Deadline: 28/07/2026, MORNING.** Gintare's RFQ to Mercury said "our deadline is 28th Morning".

## Where it stands (27/07/2026)

**Fenster has NO price for this job.** One supplier return is in hand and it covers the windows only.
`scripts/mary_checks.py data/job-checks/georgies.json` returns **5 FAILED - do not issue this quote.**

### In hand: Mercury Glazing Supplies QL004741, 27/07/2026 - windows only

| | |
|---|---|
| Net total | GBP 30,354.48 |
| Discount 1 | -10.00% = -GBP 3,035.45 |
| **Grand Total Net** | **GBP 27,319.03 ex VAT** |
| Total inc VAT | GBP 32,782.84 |

23 positions + position 024 "PAINT CHARGE" GBP 165.00. SMA **VS600** vertical sliding sash, RAL 8000 M
(green brown), 2 x 2x6mm 6.8/16/6 Clear Lam Tgh, 1 x trickle vent mill finish 5000, chrome handles.
**Supply only** - no installation, no delivery terms stated, no validity period stated on the quote.

Sent by Michal Hagner, quotes@mercuryspecialistframes.co.uk / michal@mercuryglazing.co.uk,
01452 383344 opt 2. Unit E1 Goodridge Business Park, Gloucester GL2 5EB. The quote PDF has no text
layer - 12 scanned page images; render with PyMuPDF at 170dpi and read the images.

**Reconciliation is exact and was checked line by line.** 23 quoted = 23 scheduled, and every size
matches the South West Norse schedule:

| Size (W x H mm) | Schedule | Mercury | Each |
|---|---|---|---|
| 1455 x 855 (W1, W20, W21) | 3 | 3 | GBP 1,313.77 |
| 635 x 1159 (W2) | 1 | 1 | GBP 1,143.22 |
| 855 x 1455 (W3-W18) | 16 | 16 | GBP 1,348.80 |
| 850 x 1155 (W19, W22) | 2 | 2 | GBP 1,253.46 |
| 554 x 858 (W23) | 1 | 1 | GBP 1,017.23 |

Items + paint charge = GBP 30,354.48 to the penny; less 10% = GBP 27,319.03; VAT and total both
recompute exactly. Nothing dropped, nothing double-counted.

**Rate: GBP 1,013.40/m2 net supply only** over 26.81 m2 (windows only, paint charge stripped out).
Average GBP 1,181.33 per window on an average unit of 1.17 m2. There is **no vertical-slider category
in `data/supplier-rates.json`** - 68 categories, none of them sash - so this cannot be benchmarked.
For scale only, BSW's aluminium casement glazed [<1.5m2] median is GBP 445.71/m2 (max GBP 1,041.47).
Mercury is 2.3x that median. A vertical slider is genuinely dearer than a casement - twice the sashes,
balances, interlocks - and small units always carry a high rate per m2, so this is not evidence of an
overcharge. It is a **single source with no competing quote.**

## The five things wrong with the Mercury quote

All five are things the quote does not say, not things it says wrongly.

1. **DUAL COLOUR IS NOT IN THE PRICE.** Spec 2.28: *"New aluminium windows and screens to be
   manufactured in white Aluminium internally and dark brown aluminium externally."* Mercury's quote
   says, on all 23 lines, **"BROWN RAL TBC (SINGLE COLOUR ONLY)"** and prices RAL 8000 M. The
   specified white internal face is simply absent. The GBP 165 paint charge is a single non-standard
   RAL, not a dual-colour uplift. *(Now caught automatically - see the new rule below.)*
   Note also the RAL is unresolved: 8000 is "green brown", not a dark brown, and the quote itself
   says TBC.

2. **NO U-VALUE, AND THE GLASS AS QUOTED LOOKS UNABLE TO REACH IT.** Spec 2.28 and 2.33.5: max
   **1.6 W/m2K**, and *"The Contractor must provide evidence of the energy efficiency rating."*
   Mercury state no U-value anywhere, and the make-up is **"Clear Lam Tgh"** with no low-E / soft coat
   named. Compare how other suppliers write it - Aplus "4-20-4 Clr Tough **S Coat** 1.2", BSW
   "Coolite SKN175ii". Either the coating is there and unstated, or it is not there. On a job whose
   entire purpose is energy improvement, a U-value failure is fatal, and the reglaze would be ours.

3. **OBSCURE GLAZING MISSING.** Spec 2.33.1: *"clear throughout, with exception of obscure glass to
   all bathroom, shower and WC areas."* All 23 Mercury lines are clear. Either no WC window is in the
   23 or the obscure is not priced - the elevations will settle it.

4. **WRONG TRICKLE VENTS, AND POSSIBLY TOO FEW.** Spec 2.33.4 requires **Delta vent and grille in
   white PVCu with an external canopy**, at **4000mm2 per 15m2 of floor area**, with additional
   ventilators one per further 15m2. Mercury quote one **mill finish** (raw aluminium) 5000 unit per
   window regardless of room size. Wrong product, wrong finish on a brown/white window, and the
   quantity is unchecked against room areas.

5. **THE SYSTEM IS A SUBSTITUTION.** Spec 2.33 names **Sapa Building Systems Dualframe 75Si**
   (Tewkesbury) *"or equal and approved"*. Mercury offer **SMA VS600**. That is a legitimate route but
   it has to be declared and approved by the CA, not slipped through. Worth knowing:
   **Aplus already fabricate Dualframe 75Si for Fenster** - Riverside QT51518 (27/07/2026) and Stoke
   Park Rev1B - so the specified system is obtainable through an existing supplier if we ask.

## What is still completely unpriced - 35.45 m2

No supplier has quoted any of this. Spec 2.38.3 names **Technal Building Systems Stormframe STII**
commercial door and framing system (or equal approved) - and **Aplus quote Technal STII** (Princess
Beatrice, Aplus Logikal 22/07/2026, GBP 17,499.74), so again the specified system is reachable.

| Ref | Type | Size | Area |
|---|---|---|---|
| D01 | Double doorset | 1.80 x 2.089 | 3.76 m2 |
| D02 | Patio door | 2.65 x 2.089 | 5.54 m2 |
| CW01 + D03 + CW02 | Curtain walling run | 7.77 x 2.089 | 16.23 m2 |
| D04 | "Double" doorset | 0.95 x 2.089 | 1.98 m2 |
| D05, D06, D07, D08 | Single doorsets | 0.95 x 2.089 | 1.98 m2 each |
| | | **Total** | **35.45 m2** |

Requirements on those doors: pivot hinges, concealed closers, 90-degree hold-open, anti-finger-trap
stiles, wheelchair-accessible flush drained thresholds, 28mm clear DGUs, internal beads, area-weighted
U-value 1.6 with evidence. Ironmongery per the 2.39 schedule: **internal push-bar panic devices to
BS EN 1125 on D01, D02, D03, D04, D05 and D08** (six of them); **thumbturn with classroom function,
5-lever mortice lock, suited to the building's existing master key, on D06 and D07.**

**Indicative envelope for the missing scope - BENCHMARK ONLY, NOT SUPPLIER-BACKED, and a floor not a
price:** BSW glazed-door medians (GBP 411.96/m2 for 3-6m2, GBP 422.99/m2 for 1.5-3m2) give
GBP 8,021 for the seven doors; the house curtain-walling template at GBP 850/m2 supply gives
GBP 13,795 for the 16.23 m2 run. **~GBP 21,800 supply.** Those medians carry **no** panic hardware,
no pivot/concealed-closer set, no anti-finger-trap stile and no master-key suiting, so the real number
is above it. With Mercury's windows that is a supply sub-total around **GBP 49,100 on a mixed basis** -
useful for scale, not a quotable figure.

## Open questions for Pearce / the CA

- **D04 is called a "Double Doorset" at 950mm wide.** D01, the other double, is 1800mm. 950mm split
  into two leaves is not a door. Either the description or the width is wrong, and it is roughly a
  2x price difference.
- **The client's own spec contradicts itself on colour.** 2.28 says white inside / dark brown outside;
  2.33 says *"standard Sapa finish (WHITE in colour)"*. One of them is wrong.
- **Asbestos.** Spec 2.43.1 states internal cill boards **throughout the building** are asbestos
  containing and *"shall allow to include within the tender submission for the removals"* - that is an
  express, non-provisional requirement sitting inside the window scope, while Pearce's own breakdown
  carries a separate Asbestos Removal element (1.3) and a GBP 5,000 defined provisional sum. Whose
  line is it? Our installers cannot lift those windows without disturbing them.
- **Builder's work the spec puts on "the Contractor" and Fenster normally excludes:** internal tower
  scaffold to high-level windows (2.34.1), code 4/5 leadwork to all openings and abutments (2.34.4),
  redecoration of whole walls and ceilings in Dulux Trade (2.34.6, 2.41), making good plaster, floors,
  suspended ceilings and external masonry (2.33.13-16, 2.40), isolation and reinstatement of the
  entrance security/egress system (2.43.2), and M&E disconnection/reinstatement. Confirm these sit
  with Pearce.
- **Window winding gear** (2.34.2) for any window whose handle is above 1800mm FFL - needs cill
  heights off the elevations. Remember Crestwood: GBP 17,779 of Teleflex was in our price while our
  clarifications excluded the controls.
- **Dayworks rates** (2.45) are required: craftsman, painter, labourer, electrician.

## Provisional and contingency sums the tender fixes

GBP 500 entrance access control; GBP 2,500 unforeseen asbestos above the cill removals; GBP 2,500
vertical blinds to all windows and doors; GBP 2,500 new entrance security system; GBP 5,000
contingency. Pearce's Tender Sum Analysis shows GBP 5,000 defined + GBP 24,000 undefined provisional
sums against the whole scheme.

## Where the documents are

- Job folder: `Commercial\1. Tender Documents\Pearce Construction (Barnstaple)\Georgies\1. Estimating`
  There is **no `2. Supplier Quotes` folder** - Mercury QL004741 is the first return and is not filed.
  `3. Client Quote` holds only MASTER templates and leftovers from another job (SS / Shaftesbury);
  no pricing document has been started for Georgie's.
- The real tender pack is inside `1. Tender Documents\Georgie's (formerly Rosebank) Doors and
  windows.zip` - the six loose PDFs alongside it are only the elevations, plans and sizes.
  Extracted to `test-results\georgies-input\pack\zip`; spec text at
  `test-results\georgies-input\wed-spec.txt`; Mercury quote pages at
  `test-results\georgies-input\pages\p01-p12.png`.
- Gintare's RFQ to Mercury, 24/07/2026 12:47, is reproduced on page 11 of Mercury's own PDF. It asked
  for "Sapa / Senior Dualframe 75SI, or equal approved", U-value 1.6 max, white internally / dark
  brown externally, obscure to WC, BS6262 safety glass, trickle vents. Mercury answered on the system,
  the safety glass and the trickle vents, and did not answer on colour, U-value or obscure.

## New check rule added from this job

`check_finish_substitution` in `scripts/mary_checks.py`, fixture `data/job-checks/_test-georgies.json`.
It compares the specified internal and external finish against what the supplier actually quoted, and
fails when dual colour is specified but a single colour is quoted. Selftest passes and every earlier
founding error still fires.

## History

- **21/07/2026** - enquiry logged (Estimating Log), still marked "to log" on 27/07.
- **24/07/2026 12:47** - Gintare Vanagaite issued the RFQ to Mercury Specialist Frames with six
  drawings (Elevation, Elevation 1, Elevation 2, Plan 1, Plan 2, Sizes).
- **27/07/2026 14:20** - Mercury return QL004741 arrives at estimating@. First supplier price on the
  job. Windows only.
- **27/07/2026** - job chat opened, quote reconciled, spec read at source, five gaps found, checks
  manifest built and failing, REQ-12 raised.

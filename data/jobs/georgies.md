# Georgie's (formerly Rosebank) - Pearce Construction (Barnstaple)

Job chat key: `georgies`. Opened 27/07/2026 when Mercury's quote landed. This file is the backup for
that chat's memory.

## What the job is

**Rosebank Georgies Youth Centre, Derby Road, Barnstaple, Devon EX32 7EZ.**
(The tender portal and our own issued documents both use **57 Derby Rd, EX32 7EA**.)
Devon County Council **PSDS4 Energy Improvement Scheme** (decarbonisation). Employer's agent /
contract administrator: **South West Norse Ltd** (Venture House, Capital Court, Sowton, Exeter).
SWN project number **08-02-119364**. Main contractor tendering: **Pearce Construction (Barnstaple)**;
Fenster is pricing the glazing package to Pearce. Estimating Log number **8741**.

Fenster's package is element **1.1 Replacement Windows and Doors** of Pearce's Tender Sum Analysis.
Scaffolding (1.2), asbestos removal (1.3), cavity wall and roof insulation, M&E and PV are separate
elements on that same breakdown - so they are Pearce's lines, not ours. That matters when reading the
spec, which addresses everything to "the Contractor".

**Scope (spec 2.2):** 23 no. external windows (W01-W23), 8 no. external doorsets (D01-D08), 2 no.
sections of full height curtain walling / screens (CW01, CW02, with door D03 in the run).

**Contacts at Pearce:** Fraser Butters `buttersf@pearceb.co.uk` issued the ITT 21/07 via Once For All;
**Neil Macilwaine `macilwainen@pearceb.co.uk`** chased on 28/07 and is who the tender was sent to.

---

## WHERE IT STANDS (28/07/2026) - THE TENDER HAS BEEN ISSUED

**Gintare issued it to Neil Macilwaine at 14:01 BST on 28/07, cc adam@, at GBP 89,229.61 ex VAT.**
Attachments: the Pricing.xlsx, the Proposal as PDF, and Window & Door Drawings.pdf.

**The quote Adam was asked to check is not the quote Pearce hold.** Gintare sent it to Adam at 12:22
BST and to Pearce at 14:01 BST. Adam's copy totals **GBP 83,104.61**; Pearce's totals **GBP 89,229.61**.
The GBP 6,125.00 difference reconciles exactly to three uplifts added in between:

| change | amount |
|---|---|
| +GBP 75.00 on each of the 23 windows | +1,725.00 |
| +GBP 2,000.00 on the curtain walling run (13,796.80 -> 15,796.80) | +2,000.00 |
| new line: KINGSPAN CAVITY CLOSERS (no supplier quote behind it) | +2,400.00 |
| | **+6,125.00** |

The uplifts were typed over the template formulas, so the issued workbook no longer recomputes.
Adam's dashboard request (dashmsg-40, 12:30 BST) was against the GBP 83,104.61 version.

> **All times in this file are BST.** Work-order `received` fields are UTC and were an hour early in
> the first version of this record - corrected 28/07. Times quoted inside an email body ("Sent: 28
> July 2026 11:52") are already local and were NOT shifted. Adam's own email corroborates: the tender
> went at "2:01 PM".

### The issued price

| line | detail | GBP |
|---|---|---|
| Aluminium sliding sash windows W01-W23 | 23 no. | 38,231.61 |
| Alunet aluminium sliding door D02 | 2650 x 2089 | 3,881.70 |
| Smart aluminium CW & doors CW01+D03+CW02 | 7770 x 2089 | 15,796.80 |
| D1, D4 | 1800 x 2089, 2 no. | 8,219.53 |
| D5, D6, D7, D8 | 950 x 2089, 4 no. | 12,085.24 |
| INSTALLATION | | 8,614.73 |
| KINGSPAN CAVITY CLOSERS | | 2,400.00 |
| **TOTAL ex VAT** | | **89,229.61** |
| *OPTIONAL* external mastic | outside the total | 856.38 |
| *OPTIONAL* EPDM | outside the total | 1,600.93 |

**Supplier cost behind it: GBP 50,562.65.** Frames sell (total less install and closers) is
GBP 78,214.88, a 54.7% mark-up on supply.

**The issued workbook is values-only** - the working columns (frames cost, glass, CW rate, install
array) were stripped before sending, so **no supplier cost or margin column reached Pearce.**

### Supplier returns - all three now in hand

| supplier | ref | date | scope | Grand Total Net |
|---|---|---|---|---|
| Mercury Glazing Supplies | QL004741 | 27/07 | 23 windows, SMA VS600 | **27,319.03** |
| Bellview Products Ltd (via BSW) | 0000000513 | 27/07 | CW run + D01 + D04 + D05-D08 | **20,861.92** |
| BSW Window Solutions | QT253508 | 28/07 | D02 patio, Alunet ESS47 | **2,381.70** |

Mercury: net 30,354.48 less 10%. Bellview: net 24,543.44 less 15% ("Discount 2"). BSW: net of
discounts, GBP 2,381.70. Every figure in the workbook is taken net and ties to the frame column -
Mercury unit prices x 0.9, Bellview x 0.85. Checked line by line, all correct.

**All 31 units are covered on count.** Nothing is missing from the schedule. Bellview positions map:
001 = D01, 002 = CW01+D03+CW02, 003 = D04, 004-007 = D05/D06/D07/D08.

### The install line is fit-only, and it is proved not asserted

GBP 8,614.7295 recomputes to the penny from the house labour codes with **zero residual**:

- CW run 16.2315 m2 x GBP 150 = 2,434.7295
- 23 windows (MAW/SAW) x GBP 160 = 3,680.00
- D02 (DAD) = 500.00
- D01, D04 (DAD) 2 x 500 = 1,000.00
- D05-D08 (SAD) 4 x 250 = 1,000.00

Same control as Princess Beatrice, Crestwood Park and Brocks Hill. **So strip-out of 23 existing
windows and 8 existing doorsets is not funded**, and the exclusions schedule does not exclude removal
either.

---

## The seven things wrong with the issued tender

`scripts/mary_checks.py data/job-checks/georgies.json` returned **7 FAILED** against the issued pack.
Against the **amended pack** (below) it returns **6 FAILED** - the third-party-traces failure is cleared.
Nothing else has moved, because nothing else has been decided.

1. **FOUR OF THE SIX PANIC DEVICES ARE NOT IN THE PRICE; TWO DOORS HAVE ONE THEY MUST NOT HAVE.**
   Spec 2.39 schedules internal push-bar panic exit devices to BS EN 1125 on **D01, D02, D03, D04,
   D05, D08**, and (spec 2.38.4) thumbturn with **classroom function, 5-lever mortice, external
   cylinder, 316 stainless escutcheon, suited to the building's existing master key** on **D06, D07**.
   Bellview fitted `ACIM453 CONCEALED PANIC BAR` to the four 950mm singles only - D05, D06, D07, D08.
   So **D05 and D08 are correct; D06 and D07 carry hardware the spec forbids; D01, D03 and D04 have
   none** (handles, hold-open closers, high-security locks, cylinders keyed alike). **D02 is a 2-rail
   sliding patio with an inline patio lock and cannot physically take a BS EN 1125 push-bar** - that
   is a conflict for the CA, not a price.
   BSW said so in writing on 28/07: *"there is also no hardware schedule, so I have assumed single
   doors to be fire escapes based on the floor plans."* **Schedule 2.39 exists and was never sent to
   them.** The concealed bar needs a different leaf build (IMP041 76mm stile + IMP037N anti-finger-trap
   push-bar profile), so this is four rebuilt leaves, not a bolt-on part. **No master-key suiting is
   bought anywhere** - "cylinders keyed alike" means alike to each other, not to the building's suite.
   Spec 2.38.5 also wants a contrasting **external** pull/pad handle on every fire-exit door; not
   listed against Bellview 004-007.

2. **STRIP-OUT UNFUNDED AND UNEXCLUDED** - see the install control above. **ANSWERED 28/07 EVENING,
   ON ANOTHER JOB.** Adam on Princess Beatrice at 21:01 BST: *"we had a lot across this job compared
   to the material costs. Therefore I decided I would include the strip out (effectively FOC) in order
   to remain competitive."* And on Redditch at 21:09: *"We will include strip out to remain
   competitive."* So the house position is **absorb it**, and Fenster has already said so to a client
   in writing - Rubery Library (Pride, 21/10/2025, WON): *"All prices include installation and removal
   of old frames."* On Georgie's that converts the finding from *a gap to be priced* into *a margin hit
   already taken*: the GBP 89,229.61 stands, and the strip-out of 23 windows and 8 doorsets comes out
   of the 54.7% mark-up. **What is still wrong is that the document does not SAY so** - it is silent,
   not inclusive, so we get no credit for it against a competitor who states it. One line in the
   INCLUSIONS list fixes that and costs nothing. **This does NOT extend to the asbestos cill boards** -
   Adam's ruling is about frames.

3. **ASBESTOS NEITHER PRICED NOR EXCLUDED.** Spec 2.43.1: internal cill boards throughout the building
   are asbestos containing and the contractor *"shall allow to include within the tender submission for
   the removals"* - express, non-provisional, inside the window scope. Our exclusions never mention
   asbestos. Pearce carry a separate Asbestos Removal element and a GBP 5,000 defined provisional sum,
   so it may be theirs, but nothing on our document says so and our installers cannot lift those
   windows without disturbing the boards.

4. **THE U-VALUE IS THE POINT OF THE JOB AND WE NEVER CLAIMED IT.** Spec 2.28, 2.33.5 and 2.38.3
   require max **1.6 W/m2K area-weighted** with **documentary evidence of the energy efficiency
   rating**. The proposal recites the requirement and never confirms compliance. Mercury state no
   U-value at all and quote "Clear Lam Tgh" with no low-E or soft coat named. Bellview state **Ug 1.0
   / Ug 1.1** and BSW **EcoPlus 1.0** - all centre-pane glass, not the whole-element Uw the spec asks
   for. **No supplier has certified an element U-value.** The reglaze would be ours.

5. **THE DOCUMENT PEARCE HOLD NAMES ANOTHER CLIENT.** Proposal title page: *"Prepared For RRR GROUP"*;
   page 2: *"Client: RRR Group"*. Sent to Pearce Construction. And the **Pricing.xlsx carries
   `dan.parker@agsurveying.co.uk`** as `dc:creator` plus two external links to
   `C:\Users\LiamO'Donnell\...` and `C:\Users\Parke\...` - REQ-27, third job this week, visible in file
   properties without opening it. The proposal went as PDF so its own trace (`Nicholas Baker`) did not
   travel; the .xlsx did.
   **AND THERE WAS A LOGO, NOT JUST A NAME.** Adam spotted it at 20:57 BST: *"This has RRR Group's logo
   and name on it. Can you please amend and send back to Neil ASAP!"* RRR GROUP LIMITED's black-and-gold
   roundel sat on the cover next to Fenster's own (`word/media/image4.png`, 255x221). **FIXED - see
   below.**

6. **THE PATIO DOOR IS QUOTED GREY.** BSW QT253508: *"Ext Colour: (7016) Grey"*, no internal colour
   stated. Our proposal's colour table promises *"Doors/CW - White internally / Brown externally"* -
   true of the Bellview items (`inside:WP, outside:Brown`), **not true of D02**. The colour disclosure
   Gintare made to Pearce covers the sash windows only.

7. **D04 PRICED AS AN 1800mm DOUBLE AGAINST A SCHEDULE THAT SAYS 950mm.** Gintare took the "Double
   Doorset" description over the scheduled width and BSW priced two 1800 doubles to match. That is the
   expensive reading - GBP 4,109.76 vs GBP 3,021.31, about **GBP 1,100** - and it is **not qualified
   anywhere on the issued document**.

### Smaller, still live

- **Obscure glazing** to bathroom/shower/WC (spec 2.33.1) neither priced nor excluded; all 23 window
  lines are clear.
- **Trickle vents wrong, and the proposal's own spec table leaves the trickle vent line blank.** Spec
  2.33.4 wants **Delta vent and grille, white PVCu, external canopy, 4000mm2 per 15m2 of floor area**
  plus one more per further 15m2; Mercury quote one **mill finish** 5000 per window regardless of room
  size.
- **Delivery is in nobody's price.** BSW are expressly *"ex works, additional delivery charges may
  apply"*; Mercury and Bellview state nothing. 31 units to Barnstaple from Peterborough and Gloucester.
- **Mercury's QL004741 states no validity period anywhere**, while our price is open 30 days to
  **27/08/2026** (proposal T&Cs clause 2). A Devon CC scheme will not be awarded inside that.
- **Dayworks rates** (spec 2.45: craftsman, painter, labourer, electrician) are expressly required and
  the issued document carries none.
- **Warranty is not back-to-back.** We offer 10 years on glass and frames with **no start date** in the
  clause and "subject to any applicable manufacturer warranties"; none of the three suppliers state a
  warranty period at all. Spec 2.38.4/2.38.5 require ironmongery with a minimum 5-year warranty and
  2.34.2 winding gear guaranteed 10 years.
- **System substitutions are named but never declared as substitutions.** Spec 2.33 names Sapa
  Dualframe 75Si, 2.38.3 names Technal Stormframe STII, both "or equal approved". We offer SMA VS600,
  SMA Smart Wall Pocket, SMA MC600 Plus and Alunet ESS47. The proposal lists them without ever saying
  they are alternatives requiring CA approval. **Aplus fabricate both specified systems for us** -
  Dualframe 75Si on Riverside QT51518 and Stoke Park, Technal STII on Princess Beatrice (Logikal
  GBP 17,499.74).

---

## THE AMENDED PACK - BUILT 28/07 EVENING, READY FOR GINTARE TO SEND

Adam's instruction (20:57 BST, to Gintare, cc'd into estimating@): amend the RRR Group branding and
send back to Neil ASAP. Built and verified. **`outputs\georgies-reissue\`**

| file | what changed |
|---|---|
| `...Proposal.docx` | editable source, rebuilt |
| `...Proposal.pdf` | what goes to Neil |
| `...Pricing.xlsx` | rebranded and de-traced |

**What was changed, and nothing else:**

- Cover: *"Prepared For RRR GROUP"* -> **"PEARCE CONSTRUCTION (BARNSTAPLE) LTD"**.
- Cover: **RRR Group Limited's logo removed** (replaced with a transparent PNG of identical
  dimensions, so the layout does not move). The space is now blank - Pearce's own logo can be dropped
  in if wanted, but I will not source another company's logo without being asked.
- Page 2: *"Client: RRR Group"* -> **"Client: Pearce Construction (Barnstaple) Ltd"**.
- Page 2: *"FAO: Fraser Butters"* -> **"FAO: Neil Macilwaine"**. Butters issued the ITT; Macilwaine
  chased it and is who Adam said to send to.
- Workbook B3 likewise, and **every third-party trace stripped** - `dc:creator`, both `externalLinks`
  parts, their relationships and the `<externalReferences>` element. `mary_checks` third-party rule
  now **PASSES**.

**THE PRICE IS UNTOUCHED AT GBP 89,229.61.** Every figure, line and total is identical.

### The trap in doing this, and how it was caught

**The only .docx we hold is Adam's 12:22 BST copy, and it is not the document that was issued.** The
14:01 version went out as a PDF. Rebuilding from the .docx and rebranding it would have handed Neil a
proposal reading **SUBTOTAL: GBP 83,104.61** - quietly GBP 6,125 under the tender he already has. It
would also have reverted four other changes Gintare made between 12:22 and 14:01:

- the **dual-colour disclosure** (the "single-colour finish only" paragraph and its clarification
  bullet) did not exist at 12:22 - the 14:01 version is the honest one;
- the colour table read a flat *"White internally / Brown externally"*, which is **false for the
  windows**; 14:01 splits it into *"Doors/CW - White internally / Brown externally"* and
  *"Windows - Brown"*;
- the 12:22 draft described the site as **"a care residential setting"**. It is a youth centre;
- the 12:22 draft mentioned obscure glazing to WC/bathroom, which the issued one dropped.

So the amended pack was reconstructed to the **14:01 issued text**, then rebranded, and verified by
diffing the regenerated PDF against the issued PDF line by line: **289 lines vs 288, and the only
differences are the four branding lines** (plus one stray empty bullet the issued document carried and
this one does not).

`scripts\clean_issued_pack.py` does the rebrand-and-de-trace and has a `--selftest` that replays this
job: 11 traces before, 0 after, total unchanged. It is job-agnostic and worth using anywhere REQ-27
bites.

### What Adam still has to decide (none of it changed without him)

| | change | price effect |
|---|---|---|
| a | **Mastic inside the price.** Spec **2.33.12** requires all joints between aluminium and structure pointed with a triangular fillet of white low-modulus silicone over a polyethylene backer rod, 6-10mm joint depth. Our document offers **EXTERNAL MASTIC as an OPTIONAL EXTRA** - REQ-6 / Redditch exactly: offering as an option work we are obliged to do, and inviting the QS to strike it. | +GBP 856.38 -> **90,086.00** |
| b | **State that strip-out is included**, per Adam's own ruling tonight and the Rubery precedent. | nil |
| c | **The four missing panic devices and the D06/D07 master-suited locksets.** | supplier re-quote |
| d | Qualify the **D04 950 vs 1800** assumption and the **D02 grey**. | nil / TBC |

## Still open with Pearce / the CA

- Whose line are the asbestos cill boards, the internal tower scaffold (2.34.1), code 4/5 leadwork
  (2.34.4), redecoration (2.34.6, 2.41) and making good (2.33.13-16, 2.40)? Our proposal excludes
  scaffold, decoration, making good and internal finishing - asbestos and strip-out it does not.
- **D04: is it 950mm or a double?** Roughly a 2x price difference.
- **The client's own spec contradicts itself on colour** - 2.28 says white inside / dark brown outside;
  2.33 says *"standard Sapa finish (WHITE in colour)"*.
- **D02 cannot take a panic bar.** Spec 2.39 requires one.
- **Window winding gear** (2.34.2) for any window whose handle is above 1800mm FFL - needs cill heights
  off the elevations. Remember Crestwood: GBP 17,779 of Teleflex sat in our price while our
  clarifications excluded the controls.

## Provisional and contingency sums the tender fixes

GBP 500 entrance access control; GBP 2,500 unforeseen asbestos above the cill removals; GBP 2,500
vertical blinds; GBP 2,500 new entrance security system; GBP 5,000 contingency. Pearce's Tender Sum
Analysis shows GBP 5,000 defined + GBP 24,000 undefined provisional sums against the whole scheme.

## Where the documents are

- Job folder: `Commercial\1. Tender Documents\Pearce Construction (Barnstaple)\Georgies\1. Estimating`
- The real tender pack is inside `1. Tender Documents\Georgie's (formerly Rosebank) Doors and
  windows.zip` - the six loose PDFs alongside it are only elevations, plans and sizes.
  Extracted to `test-results\georgies-input\pack\zip`; spec text at
  `test-results\georgies-input\wed-spec.txt`; Mercury quote pages at
  `test-results\georgies-input\pages\p01-p12.png`.
- Issued documents: `test-results\mary-inbox\processed\20260728T1301-zQFQAAAA-att\`.
  Adam's check copy (the GBP 83,104.61 version, with the working columns intact):
  `test-results\mary-inbox\processed\20260728T1122-zQEwAAAA-att\`.
- BSW/Bellview returns: `test-results\mary-inbox\processed\20260728T0945-QnPOdAAA-att\`.
- Gintare's RFQ to Mercury, 24/07 12:47, is reproduced on page 11 of Mercury's own PDF. Her RFQ to
  BSW went 24/07 14:36 for **CW and doors only** ("please exclude all other windows, as these are
  required to be sliding sash") - it listed the pivot hinges, closers, anti-finger-trap stiles,
  thresholds, U-value and the words "Push-bar doors to include panic exit device to BS EN 1125" and
  "Thumbturn doors to include lock / thumbturn arrangement" **but never said which doors were which.**
  That is the root of finding 1.

## Check rules from this job

- `check_finish_substitution` in `scripts/mary_checks.py`, fixture `data/job-checks/_test-georgies.json`
  (added 27/07). Compares specified internal/external finish against what the supplier quoted; fails
  when dual colour is specified and a single colour is quoted, fails on a per-side mismatch, ASKs when
  the supplier states no finish. It now also catches the D02 grey.

## History

- **21/07/2026 09:21** - Fraser Butters (Pearce) issues the ITT via Once For All. Return date 28/07.
- **24/07/2026 12:47** - Gintare RFQs Mercury Specialist Frames (windows).
- **24/07/2026 14:36** - Gintare RFQs BSW (CW + doors only), asking for return by Monday 27th.
- **27/07/2026 15:20** - Mercury QL004741 arrives. Windows only. Job chat opened, quote reconciled,
  spec read at source, five gaps found, checks manifest built and failing, REQ-12 raised.
- **28/07/2026 09:51 BST** - Gintare chases BSW.
- **28/07/2026 10:45 BST** - BSW return Bellview 0000000513 + QT253508, with the "no hardware schedule"
  caveat. The 35.45 m2 is priced for the first time.
- **28/07/2026 12:22 BST** - Gintare sends the quote to Adam for checking. GBP 83,104.61.
- **28/07/2026 12:27 BST** - Gintare asks Mercury about dual colour. **11:34 Mercury: "the aluminium
  vertical sliders are single colour only."** Definitive - the dual-colour gap cannot be closed in
  aluminium VS.
- **28/07/2026 12:30 BST** - Adam asks Mary on the dashboard (dashmsg-40) to check the quote.
- **28/07/2026 11:52** - Neil Macilwaine chases via Once For All.
- **28/07/2026 14:01 BST** - **Gintare issues the tender to Pearce at GBP 89,229.61**, disclosing the
  single-colour sash limitation and recommending uPVC vertical sliders instead.
- **28/07/2026** - post-issue audit. Seven check failures, REQ-12 rewritten to the post-issue decision,
  calibration entry 6 added, Adam answered on the dashboard and by email.
- **28/07/2026 20:57 BST** - **Adam to Gintare: *"This has RRR Group's logo and name on it. Can you
  please amend and send back to Neil ASAP!"*** He found finding 5 independently, and found more of it
  than I had - I had the name, he had the logo too.
- **28/07/2026 evening** - amended pack built, verified against the issued PDF and left in
  `outputs\georgies-reissue\` for Gintare to send. `scripts\clean_issued_pack.py` written and
  selftested. All times in this file corrected UTC -> BST. Strip-out ruling recorded from Adam's
  Princess Beatrice / Redditch decisions. Mastic identified as spec-required (2.33.12) and therefore
  wrongly carried as an optional extra.

# Handover

This is the quick-start note for the next AI agent working on the Fenster Glazing Quote Assistant.

## Current Priority

The user explicitly paused the live tender-finder build. They asked whether it is a good idea, then confirmed the important thing now is documentation and getting the bot to the level of the emails.

Priority order:

1. Make the estimating bot understand and price real tender packs like Project Hail Mary / Ninn Lane.
2. Make scripts, website, and quote generator use the same logic.
3. Document how to self-check quotes and compare them to real estimator/supplier quotes.
4. Only then build the live tender monitor/dashboard that emails `commercial@fensterglazing.com`.

Do not start building the tender monitor unless the user asks again.

## Where To Start

Working repo:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant
```

The user moved away from OneDrive. Do not use the old OneDrive repo for new work.

Read these first:

1. `HANDOVER.md`
2. `AI.md`
3. `js/dataExtractor.js`
4. `js/pricing.js`
5. `js/projectHailMary.js`
6. `scripts/run-tender-pack.mjs`

Current app version shown in the UI:

```text
v2026.06.30.8
```

Primary hosted app:

```text
https://glazing-quote-assistant.pages.dev
```

Document intake Worker:

```text
https://gqa-document-processor.0riceisnice0.workers.dev
```

Last important pushed code commit before this doc refresh:

```text
2f39bdf Add tender finder research panel
```

There are no GitHub Actions workflows at the time of writing. Deployment is static hosting from the repo.

Recent manual estimator outputs are in:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs
```

Do not delete or overwrite those unless the user asks.

## What The Four Email Threads Wanted

### Email 1: Ninn Lane quote request

They wanted Fenster to quote aluminium windows and doors for three separate buildings.

Known requirements:

- PPC aluminium framed double-glazed windows and doors.
- Colour: black.
- U-value: 1.4 W/m2K.
- PPC aluminium framed louvre panels where shown on drawings.
- Commercial spec.
- Elevations, plans, specification, and schedules are attached in ZIP files.
- Return quote by Monday 6 July.

Bot implication: read the email and turn it into job assumptions, then read the attached pack and quote the scope.

### Email 2: Supplier quotes attached

Supplier/estimations replied with attached quotes.

Bot implication: supplier quotes become strong evidence. The bot should ingest them, detect systems/items/extras, reconcile totals, and use them to reduce guesswork.

### Email 3: Pricing-code / estimator workflow instruction

This is the key "what the bot should be" email. It introduced the need for pricing codes, labour allowances, coding rows, assumptions, exclusions, RFIs, and estimator-style review.

Bot implication:

- Extract schedule items.
- Assign product/labour codes such as `SAD`, `DAD`, `LAW`, `MAW`, `SAW`, `SUPD`, etc.
- Keep quantity separate from the code.
- Detect combined items like doors with screens/fanlights.
- Flag unclear items instead of guessing.
- Prepare a pricing/check sheet, not just a customer quote.
- Generate assumptions, exclusions, risk flags, and RFIs.

### Email 4: Barbour ABI / live tender research

Adam asked if a bot can scrape/find live commercial window and door tenders.

Bot implication: yes, later we can create a tender-finding bot and dashboard. Current implementation only has the research panel in `js/tenderFinder.js`. Do not prioritise it over estimating accuracy yet.

## What Has Been Done

- Static browser quote app exists.
- Quote PDF generator supports detailed and compact branded PDFs.
- Version badge exists in the UI.
- OpenAI note enrichment was wired but the user's key hit quota/429; do not spend more tokens unless asked.
- Tender questions can show red review states for missing fields.
- `js/projectHailMary.js` was added for Project Hail Mary estimator review:
  - requirement extraction,
  - supplier quote detection,
  - supplier item coding,
  - assumptions/exclusions/RFIs,
  - proposal/pricing draft data,
  - browser exports.
- Adam's AI-written training brief should be used as estimating intent/context, not priced as a live tender document.
- Phase 1 trust-layer work added `DataExtractor.buildScopePlan(documents)` so the app/CLI record which documents are source of truth, validation/reference evidence, supplier evidence, duplicates, or excluded/admin documents.
- Type/reference sheets such as `Window Types` and `External Door Types` are reference/spec evidence, not priced scope, when real schedules exist.
- Phase 2 added a Step 2 Estimator Dashboard for Adam: status, source-of-truth plan, immediate actions, tender requirements, risks, supplier coverage, coding table, checklist, and proposal summary draft.
- Adam's pricing-code labour allowances were added in `js/pricing.js` as opt-in behaviour.
- `js/tenderFinder.js` was added as a research panel for live tender sources, CPV codes, keyword strategy, scoring, and a draft reply to Adam.

## Recent Manual Quote Work

These were produced manually because the current website parser is not yet estimator-grade for every pack. They are important examples of the workflow the next agent should copy.

### Home Bargains Basingstoke

Inputs:

```text
C:\Users\zacpl\Desktop\tender docs due tosay\Home Bargains, Basingstoke Aluminium Doors & Windows.zip
C:\Users\zacpl\Downloads\Project Hail Mary - Stainforth.zip
```

Outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Glazing Proposal and Pricing Review.pdf
```

Commercial position:

- Supplier-backed using Bellview, Strongdor, and ACA.
- Latest sell ex VAT: `GBP 89,429.22`.
- Latest inc VAT if applicable: `GBP 107,315.06`.
- Roller shutters excluded by user instruction.
- ACA automatic/access-related supplier cost: `GBP 12,710.00`.
- 25% markup applied to ACA: `GBP 3,177.50`.
- Extra access-control hardware/integration beyond ACA remains TBC.
- `SSD` = single steel door. `DSD` = double steel door.

Lesson: if the supplier cost is known, do not write "25% of supplier cost" as a placeholder. Calculate the money value and update the total.

### Alkerden

Input:

```text
C:\Users\zacpl\Downloads\OneDrive_2026-07-01.zip
```

Working folder:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\alkerden-input\Stage 4 Curtain Walling & External Doors
```

Outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Glazing Proposal and Pricing Review.pdf
```

Commercial position:

- This is a budget/fallback pricing review only. No supplier quote was included.
- Composite/Velfac windows were marked up as aluminium per the email instruction.
- 111 window rows extracted and aggregated.
- 19 dimensioned external door rows priced.
- `ED13` and `ED23` missing-dimension rows flagged/TBC.
- Budget sell ex VAT: `GBP 588,817.93`.
- Budget inc VAT if applicable: `GBP 706,581.52`.
- Folder title says curtain walling, but no separate curtain wall schedule/quantities were found.

Lesson: if no supplier quote exists, say "budget/fallback" clearly and do not let the user think it is a fixed tender price.

### Brocks Hill (2026-07-15)

Input:

```text
C:\Users\zacpl\Downloads\Brocks Hill BoQs.xlsx
```

Working folders:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\brocks-hill-input
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\brocks-hill-run
```

Outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Brocks Hill - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Brocks Hill - Fenster Glazing Proposal and Pricing Review.pdf
```

Commercial position:

- Blank-rate contractor BoQ only (sheet `Windows & Doors`); no drawings, spec or supplier quotes.
- Budget/fallback pricing only: fallback material `GBP 74,355.48`, code markup `GBP 24,850.00`, code labour `GBP 7,190.00`, EPDM allowance `GBP 3,388.94`, mastic allowance `GBP 1,424.40`.
- Budget sell ex VAT: `GBP 111,208.82`. Inc VAT if applicable: `GBP 133,450.58`.
- 37 frame units: ED.0.02 x1 (SAD), ED.0.10/14 x2 (SAD), WIN.E.01 x4 (SADSAW door+screen), WIN.E.02 x23 (MAW), WIN.E.04 x4, WIN.E.05 x2, WIN.E.06 x1.
- `E/O POWER ASSISTED` x1 and `E/O FOR EXD.E.02 (03/11/12/13)` x4 are TBC/not priced.
- Material is not stated in the BoQ; assumed PPC aluminium (RFI). BoQ quoted-value list requires access/airtightness/EPDMs/flashings/manifestations/safety barriers/Climaguard/glass lifting/obscure glazing/solar control/door supports/internal flashings/panic gear/protection - only EPDM/mastic allowed for.

Lesson: blank-rate BoQ workbooks ("BoQs" plural filename) are now extracted by the shared parser (Strategy B1, commit `b8d9a71`). Extra-over lines must stay TBC, not silently dropped or invented.

### Brocks Hill Phase 2 - quote check (2026-07-27)

Gintare's outgoing tender to Spacemaker Developments (SMDT0173), dated 28/07/2026, checked
against the tender pack. Deadline Friday 31/07/2026.

Inputs:

```text
test-results\mary-inbox\processed60727T1443-z2KwAAAA-att\   (pricing xlsx, proposal docx, drawings pdf)
...\Commercial. Tender Documents\SMD\Brocks Hill Phase 2. Estimatingtest-resultsrocks-hill-check	ender\                          (171-file pack, extracted from the zip)
```

Outputs:

```text
outputs\Brocks Hill Phase 2 - Quote Check (schedules vs tender).xlsx
scriptsrocks_hill_quote_check.py
data\jobsrocks-hill.md
data\job-checksrocks-hill-phase-2.json
```

Position:

- Tender as drafted `GBP 93,673.34` ex VAT, supplier-backed and arithmetically exact: house
  template adders land to the penny on all 7 rows, installation `GBP 9,570.00` recomputes from
  the labour codes, and both quotes tie to the frame column - BSW QT253232 `GBP 37,960.33` and
  Bellview 0000000503 `GBP 17,094.52` net of the 15% end discount, both 22/07/2026.
- **Seven external doors on door schedule P06 are in neither quote nor the pricing document nor
  the exclusions**: Type E.01 (5no steel sports hall escape doors, all Fire Escape) and Type E.03
  (2no aluminium louvred plant room doors). ~`GBP 32,462` of sell. They are absent because SMD's
  BoQ omits them, which is why the 15/07 budget missed them too.
- Corrected indicative `GBP 134,580.22`; `GBP 142,930.03` with mastic/EPDM in the sum and the
  required 2.5% MCD grossed. Benchmark, not price.
- 18 findings in total. `scripts/mary_checks.py` returns 5 FAILED. Nothing sent to SMD.

New check rule: `check_supplier_covers_quantity` with fixture `data/job-checks/_test-brocks-hill.json`.
The tender sold 2no Door Type E.04 where Bellview quoted 1no - the rate was applied twice, so the
quote total still tied and `GBP 2,723.49` of cost had no quote behind it. Selftest passes; all five
founding errors still fire.

Lesson: a contractor's BoQ is not the scope. Reconcile every bill against the architect's window
and door schedules before pricing it, and where the client publishes their own quantities compare
areas - SMD's pricing schedule carried 48 m2 of external doors against the tender's 24.96 m2, and a
factor of two is not a measurement difference. Second lesson, from the same job: SMA Smart Wall is
not available in triple glazing, so a proposal promising "triple glazing throughout" on a Smart Wall
door package is uncompliant on its face.

### Crownhill Business Centre / Zelltec (2026-07-15)

Inputs:

```text
C:\Users\zacpl\Downloads\Project Hail Mary - Crownhill.zip
(Zelltec - Crownhill Concept.pdf + entrance photo)
```

Working folders:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\crownhill-input
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\crownhill-run
```

Outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Fenster Glazing Proposal and Pricing Review.pdf
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Reply to Adam (draft).txt
```

Commercial position:

- Fenster design concept PDF only; no supplier/fabricator costs. Budget fallback rates.
- Fallback material `GBP 73,168.03`, code markup `GBP 19,000.00`, code labour `GBP 5,410.00`, centre-post pressing allowance `GBP 200.00` (Adam's email).
- Budget sell ex VAT: `GBP 97,778.03`. Inc VAT if applicable: `GBP 117,333.64`.
- 29 frames: TYPE A x18 (MAW T&T 3-sash), TYPE B/C x1 (SAW), TYPE D x4 (SAW), TYPE E.1/E.2 entrance doorsets (SADMAW, Smart Wall spec), TYPE F x2 + TYPE G x1 steel panic-bar doors (SSD). Matches Adam's 24/2/3 email totals.
- TYPE B/C/G quantities assumed 1 (not printed on concept). Fire RATING of steel escape doors not stated - RFI.

Lesson: Fenster/WindowCAD concept PDFs are extracted by Strategy C1 (commit `45267e1`). PDF.js page text can have no newlines - concept parsing must not rely on line breaks.

Rev 2 (supplier-based, same day): Adam confirmed the RFIs and instructed pricing from past supplier costings (BSW/Aplus aluminium, Vetroseal Coolite/SKN glass, Strongdor steel). The OneDrive `Commercial\1. Tender Documents` tree is the supplier-quote archive; Strongdor had already quoted this project (`SQ216661 Rev1`). Rev 2 outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Fenster Pricing Document and Review (Rev 2 - supplier based).xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Fenster Glazing Proposal and Pricing Review (Rev 2 - supplier based).pdf
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Crownhill - Reply to Adam Rev 2 (draft).txt
```

- Rev 2 sell ex VAT: `GBP 73,770.86` (inc VAT `GBP 88,525.03`). Steel doors supplier-backed; aluminium/glass derived from mined benchmark rates (see AI.md Crownhill section for the rate register).

### Greenfields Respite Barnstaple (2026-07-16)

Input: `C:\Users\zacpl\Downloads\Greenfields Respite Barnstaple windows and doors.zip` (Pearce Construction tender: spec + drawings only, no schedule workbook, no supplier quotes). Working folders `test-results\greenfields-input` / `greenfields-run`.

Outputs:

```text
outputs\Greenfields Respite Barnstaple - Fenster Take-Off and Specification.xlsx
outputs\Greenfields Respite Barnstaple - Fenster Pricing Document and Review.xlsx
outputs\Greenfields Respite Barnstaple - Fenster Glazing Proposal and Pricing Review.pdf
outputs\Greenfields Respite Barnstaple - Reply to Adam (draft).txt
```

Commercial position:

- TENDER DEADLINE 12 noon 17/07/2026 to Pearce (Neil Macilwaine). JCT MW 2024, start 31/08/2026, 12 weeks, 5% retention. Operational care home.
- Benchmark sell ex VAT `GBP 100,981.30` (inc VAT `GBP 121,177.56`): supply `GBP 85,361.30` + Fenster code labour `GBP 15,620.00`. All frame rates are register medians + GBP25/m2 safety-glass uplift + hardware allowances.
- 77 openings taken off drawing 005 P2 (rendered in 150dpi tiles - CAD text layers are unreliable, refs must be read visually): 58 uPVC windows (23 obscured), 4 alu screens (5 NSHEV AOV vents allowed at GBP950/vent, controls by others), 15 doorsets (5 uPVC / 5 alu white / 5 alu brown RAL 8004 incl louvre double + 3-leaf slide-fold).
- The first Adam-requested TAKE-OFF DOCUMENT format: Project Information sheet (client/contract/deadlines/security/glass/colours/EPDM/warranties/standards/site constraints), full per-ref Window & Door Schedule, RFIs & Queries sheet. Reuse this 3-sheet format when Adam asks for take-offs.
- CRITICAL RFI: 005 has no elevations for WG-15-29, WF-10/11, DG-13 but plans reference WG-27 and DG-13 - scope gap excluded from price, query to Pearce same-day.

Lesson: spec/drawings-only packs cannot be machine-extracted (0 items from the CLI); the take-off comes from tiled visual reads of the details drawing, and the rate register turns that into a priced tender in one pass.

### Greenfields house-format pricing doc + tender email (2026-07-17, PM)

Adam (via Zac): RFI to Pearce never sent, noon deadline passed - "put together a pricing document based on what info she has to hand and include any exclusions laid out clearly in an email", out TODAY.

Built the HOUSE pricing document from the internal benchmark workbook (82 rows: 77 openings + 5 allowances):

- `test-results\greenfields-run\greenfields-house-job.json` (built by script from the internal workbook; supply reconciles to GBP85,361.30 exactly).
- Code mapping: uPVC windows SPVC <1.5m2 / MPVC 1.5-3 / LPVC >3 (6/35/16+WG-30 screen), alu screens ELAW x4 (no screen code in Adam's table), uPVC doors SUPD x5, alu singles SAD x5, DG-09 entrance door+side glazing SADSAW, alu doubles + DG-03 louvre double + DG-08 slide-fold DAD x4, ALLOW rows via unitRateOverride (no adder/labour).
- **GBP 136,438.80 ex VAT** (items GBP121,248.80 + installation GBP15,190) = supply GBP85,361.30 + template code adders GBP35,887.50 + code labour. INTERNAL benchmark quote was GBP100,981.30 (supply + labour, NO margin) - the house template's adders ARE the Fenster margin; per Adam's ruling the template number is the price. Flag equivalents clearly whenever converting an internal quote to house format.
- Tender email drafted to Neil Macilwaine with the scope gap (WG-15-29, WF-10/11, DG-13) converted to explicit EXCLUSION 1, plus maglocks/NSHEV wiring/scaffold/asbestos/blinds/redecoration/structural exclusions and WF-22/DG-08/survey clarifications: `outputs\Greenfields Respite Barnstaple - Tender Email to Pearce (draft).txt`. BS7412/13 certs must be attached before sending - still not pulled.

TWO GENERATOR BUGS FIXED in `scripts/generate-fenster-docs.py` (first job to exercise the >12-row insertion path):

1. openpyxl `insert_rows` does not shift merged ranges; the template's footer merges (G21:H21, F27:H27, F28:H28) landed inside the item block, turned H21/H27/H28 into read-only MergedCells, and the cloned unit-rate formula was SILENTLY dropped (3 rows priced at 0). Fix: unmerge footer merges below row 20, insert, re-merge shifted.
2. `_clone_row_formulas` used a bare string replace of the row number, corrupting the SADMAW constant `1900*75%` on every cloned row (e.g. row 45 -> `14500*75%`). Fix: regex replace of cell references only.

Verification: hand-computed every row's formula in python (Excel COM is blocked in this environment) - items/install/total reconcile to the penny; footer merges land at G91:H91, F97:H97, F98:H98. Lesson: after ANY generator change, hand-evaluate the emitted formulas per row - openpyxl writes silently even when formulas are dropped.

### Greenfields comparison vs Adam's sent quote (2026-07-22)

Adam shared the manually priced, SENT Greenfields quote (`test-results\greenfields-manual-quote\`): **GBP 128,372.82 ex VAT** (+ optional mastic 2,524.63 / EPDM 5,158.05), dated 20/07. Mary's house doc was GBP 136,438.80 (+6.3%); internal no-margin benchmark GBP 100,981.30.

CALIBRATION MARKS (their sent unit rates, supplier-informed, incl template adders):
- Stair screens priced as SMA MC600 Plus CURTAIN WALLING at the template 850/m2 supply + 150/m2 labour (NOT coded as windows) - WG-01 2709x4200 GBP9,671.13, 1689x4590 GBP6,589.63. RULE: full-height screens get CW treatment.
- Sheerline Prestige bifold 2740x2664 sold GBP3,960.60 (Mary's slide-fold premium was ~GBP2.1k over).
- SMA Smart Wall doubles: 1746x2410 GBP5,798.64; 1270x2410 GBP5,466.98 (register alu-door medians badly undercook Smart Wall commercial doorsets).
- Liniar uPVC live rates ~8-15% below register medians (2765x1460 GBP1,014.48; 2372x1140 GBP870.34; 990x1120 GBP566.42).
- House convention: mastic/EPDM as OPTIONAL lines below the total; other allowances live in the internal review, not the client doc.
- They re-read DG-09 at 3538x2850; both WF-22 duplicates priced.

Reply draft: `outputs\Greenfields Comparison vs Sent Quote - Reply to Adam (draft).txt`.

### SM5 Wexham Primary SEND Bungalow - aluminium estimate (2026-07-22)

Adam: "estimate on the attached - Aluminium, Standard White RAL, Grey sections are panels, W.01 two frames coupled." Input `Project Hail Mary - SM5.zip` -> `test-results\sm5-input` (KK drawing 260259-WEX-KK-XX-L0-D-A-5201 P01 + spec 260529). Wexham Primary SEND Bungalow, client SM5 Developments / Slough BC, architect Kendall Kingscott. U-value 1.6 whole installation; match adjoining building; FENSA cert with O&Ms (L10/895).

ARCHIVE-FIRST WIN: `SM5 Developments\Wexham Primary` folder holds live evidence for the SAME bungalow: BSW QT252647 (Liniar uPVC windows, 13/07, GBP3,373.30 nett - includes BOTH W01 coupled frames 531.26+489.43, butt-jointed) and Bellview 0000000475 (SMA Smart Wall Pocket doors: ED01 2,198.97 / ED02 3,309.95, Grand Total Net GBP4,682.58 after 15%, valid ~12/08), plus the SENT quote 14/07: GBP14,575.88 (uPVC windows + alu doors, house template maths verified).

Mary's aluminium estimate: **GBP 18,611.95 ex VAT** (`outputs\SM5 Wexham Bungalow - Fenster Pricing Document (house format).xlsx`, 9 rows, no insertion path). Doors = Bellview net (SUPPLIER BACKED). Windows = BSW alu casement register medians (<1.5m2 445.71/542 lines; 1.5-3m2 358.44/423 lines) + GBP25/m2 lami/tuff uplift; grey panels held at glazed-equivalent rate. Codes: W.01 LAW (2424x2400 two coupled frames), W.02/03/06 SAW, W.07+W.04+W.05 MAW, ED.01 SAD, ED.02 DAD; install GBP1,870. Optional mastic GBP299.60 / EPDM GBP612.86. Alu premium over their uPVC version ~GBP4.0k. Reply draft: `outputs\SM5 Wexham Bungalow - Reply to Adam (draft).txt`.

RFIs: BSW alu requote (Alitherm white, panels in lieu of lower glass); panel grey RAL; adjoining-building product literature (not in zip); U1.6 on chosen alu system.

UPDATE 24/07 - ADAM'S CHALLENGE ("There is a product error. Can you find out what it is? Clue - look at the schedule and consider products used"): pack `test-results\sm5-challenge` = BSW alu requote QT253300 (23/07, Sheerline Prestige Hipca White, GBP7,683.49 nett: W.01 2424x2400 GBP2,256 single frame w/ C-row panels; W.02/03/06 GBP666.93; W.07 GBP1,594.92; W.04/05 GBP915.89 w/ panels), updated pricing doc (24/07, GBP20,563.57, FAO Ryan Steadman) + proposal.

ANSWER: **the SMA Smart Wall Pocket doors cannot meet the drawing's whole-installation U-value 1.6** - non-thermally-broken shopfront system glazed "6.8 Lami / 4mm Tuff" with NO cavity/low-E (the windows' units are 6.8/18 argon EcoPlus 1.0 by contrast; the proposal even claims U 1.4 above that door spec). Fix = thermally-broken door (Smart Alitherm 600 / MC600 door) with 28mm argon low-E units + SMA U-calc in writing. Bonus catches: ED.02 fire-exit doors quoted with NO panic/push bar (drawing ironmongery requires SAA push bar overriding locks); ED.01 closer is NON-hold-open vs specified hold-open; QT253300 dropped the restrictors + trickle vents the uPVC quote had (250mm restriction required; Part F); W.01 keyed at supply 2,756 vs BSW's 2,256 = +GBP500 (corrected total 20,063.57). Mary's own earlier reply had waved the door U-value through ("fine for the doors' 6.8 lami/4 tuff spec") - WRONG; lesson: a glazing string without a cavity dimension is not an insulated unit; always parse the make-up, and check panic hardware on any door marked FIRE EXIT. Calibration: live Sheerline Prestige ~10% above register alu medians. Reply drafted in chat per the 23/07 rule (email drafts go in chat, not files).

ADAM'S VERDICT (24/07, via Zac): Mary's U-value answer was WRONG - the 1.6 requirement is an AVERAGE across the whole installation, so the cold doors pass when averaged with the better windows. The W.01 +GBP500 was a deliberate DISCRETIONARY addition, not a keying error (estimators may load discretionary money into a unit rate - do not flag as error). The panic-hardware catch WAS a genuine estimator error (the kind Mary exists to catch). **THE PLANTED ERROR: SYSTEM-DEPTH COUPLING. You CANNOT couple Sheerline windows to a Smart Wall door - Smart Wall profile is 100mm deep, Sheerline is 70mm; there is no way to join them. RULE: any window frame coupled/joined in the same run as a door must be quoted in the SAME SYSTEM as the door.** On this job that means W.01 (coupled to ED.01, East elevation run 1212+1212+1227) and W.04/W.05 (flanking ED.02, West run 869+1872+869) must be SMA Smart Wall elements from Bellview, NOT Sheerline; only W.02/03/06/07 stay Sheerline. (Lyttleton's Sheerline toplight coupled to a Smart Wall head was a flagged exception needing special trims.) Next action: Bellview to quote W.01/W.04/W.05 as Smart Wall screen elements (ideally as door+side-screen assemblies); price moves UP vs Sheerline.

UPDATE 22/07 (same day): Adam answered all five RFIs. (1) BSW alu requote in progress - the uPVC quotes were INCORRECT, not merely a spec preference; (2) frames AND panels are WHITE - drawing grey is shading, not colour (doc descriptions corrected, price unchanged at GBP18,611.95); (3) U-values to be confirmed with manufacturer; (4) data sheets will accompany the quotation (closes the match-adjoining-building check); (5) FENSA registered. Ack draft: `outputs\SM5 Wexham Bungalow - Ack Reply to Adam (draft).txt`. Next action: when the BSW alu requote appears in the Wexham supplier-quotes folder, rebuild the pricing doc supplier-backed. Lesson: drawing shading is NOT a colour specification - confirm colours from tender images/spec text, and Adam's coding emails can carry scope corrections (uPVC "incorrect") that supersede supplier quotes on file.

### BCC 4-16 Filwood Broadway / Stepnell (2026-07-17)

Input: OneDrive `Commercial\1. Tender Documents\Stepnell\BCC Filwood Broadway\1. Estimating\1. Tender Documents` (shopfront systems zip). Working folders `test-results\filwood-input` / `filwood-run`.

Outputs: `outputs\Filwood Broadway - Fenster Pricing Document and Review.xlsx` / `...Proposal and Pricing Review.pdf` / `...Reply to Adam (draft).txt`.

Commercial position:

- Quote to Stepnell (Adam Warner, bid S25233B) by 20/07/2026. D&B 2024, retention 3%, LAD GBP1,358/wk, PI required.
- `GBP 84,810.59` ex VAT quoted as CONTRACTOR'S PROVISIONAL SUMS - the Trade Bill itself instructs this (drawing 31551 is illustrative; design finalised with BCC High Street team; Work Section A54; do not double-count).
- 7 Aluprof shopfront screens (~123m2): ED-04 x4 (4930x3570), ED-05 x2 (5550x2970, double outward doors), ED-06 x1 (6315x3105, LPS 1175 SR2 + Rw32dB + key-fob access). U 1.0, G 0.5-0.6 solar, mesh ventilation zones, spandrels.
- Rates: Aplus glazed screen >6m2 register median GBP359.60/m2 + GBP45/m2 spec uplift + extras + 15% margin + CW labour GBP150/m2. Engine cross-check GBP75,251 supply-only.
- Parser fix (commit `369b5b0`): Strategy B1 accepts Stepnell trade-bill headers (`Description|Qty|Unit|Rate`, no ITEM column) and picks refs from "reference ED-04" wording. Brocks Hill regression unchanged.

### Lyttleton Road / Harrabin (2026-07-17)

Input: OneDrive `Commercial\1. Tender Documents\Harrabin\Lyttleton Road`; supplier quote `2. Supplier Quotes\priory pools.pdf` = BSW/Bellview 0000000445 (06/07/2026, Smart Alitherm 400 HD windows + SMA Smart Wall Pocket doors, grand total net GBP28,160.90 after 15%).

Outputs: `outputs\Lyttleton Road - Fenster Pricing Document and Review.xlsx` / `...Proposal and Pricing Review.pdf` / `...Reply to Adam (draft).txt`.

- Option 1 (all aluminium, supplier-backed): `GBP 43,450.89` ex VAT. Option 2 (uPVC windows via register benchmarks + alu doors): `GBP 31,902.00` ex VAT - saving GBP 11,548.89, caveated: type a (500x2458) and type e (3425x3100) need uPVC manufacturability/wind-load checks (BSW chose 400HD to make them "as drawn").
- Door a (pos 008) includes the shaped/curved toplight BSW cannot draw: Sheerline 72mm toplight, trim where coupled to Smart Wall 100mm head - carry this note to survey/installation.
- Queries: BSW quote titled "priory pools community center" (confirm job), BL profiles vs Anthracite Grey head extensions (confirm colours).
- Emails to Adam are signed as MARY (he knows Mary is the estimating AI) - standing instruction from Zac 2026-07-17.

### Proposal Document Process adoption + pricing ruling (2026-07-17, Adam email)

Adam's email (via Zac) resolved two standing items:

1. **Pricing ruling:** the house pricing document is CORRECT as produced - the template's own formulas are the maths ("This is the correct price as far as I can see"). The template x75% code adders are the client price; the engine-markup discrepancy is closed. Mary's job on the pricing doc = put supplier prices in the correct cells. A "pricing document process doc" is being written by Adam for later review.
2. **Proposal process:** proposals must follow **Ops Manual Doc 2.3.2-PRC2 "Proposal Document Process"** (`OneDrive\Operations Manual\2. Business Operations & Project Workflow\2.3 Estimating & Commercial Process\2.3.2 Quotation preparation\Proposal Document Process.docx`) - Word document first, then PDF. Key steps: clone `Commercial\1. Tender Documents\1. Master\1. Estimating\3. Client Quote\MASTER COVER LETTER 31.05.2026.docx` per project; cover images = photos of the actual building found online (else commercial glazing stock); client logo from `Commercial\19. Company Logo Files` (doc says folder 20 - it's 19); cover names in CAPITALS; page 2 project info; Executive Summary via the ChatGPT "Executive Summary Bot" (Mary has no access - options offered to Adam: Mary writes to the same length/structure, or Zac runs the bot); Description & Clarifications; Products section from the final quotation; Inclusions & Exclusions review-only; pages 5+ never change; final formatting QC; PDF named `[Client Name] - [Project Ref] Proposal`. Word 16 is installed (`Word.Application.16` COM) so faithful docx->PDF export is available locally.

Output: `outputs\Proposal Process - Reply to Adam (draft).txt` (signed Mary). Offered to rebuild the Lyttleton Road proposal to the new process as a pilot.

Lesson: the Operations Manual (`OneDrive\Operations Manual\`) is a first-class instruction source - check `2.3 Estimating & Commercial Process` for process docs before inventing a format. Other quotation-prep docs there: Estimating Email Templates.docx, Estimating Log Process.docx, Tender Overview.docx.

### Beaumont Court / Fortis Vision - old vs new tender comparison (2026-07-17)

Adam's email: review old vs new tender docs for window/door changes. Location: OneDrive `Commercial\1. Tender Documents\Fortis Vision\Beaumont Court\Tender Documents\Old` (spec zip 23/02/26 + 30/01/26 drawing issue) and `\New` (`fortisvision_beaumont-court-amenity-revised_2026-07-16_1135 (1).zip` + drawing register REV 1). Client UNITE Students, architect DMWR, contractor Fortis Vision. Fenster spec basis: Norrsken timber-alu composite (engineered pine, alu clad, triple glazed, RAL 7016; supplier quotes in `Supplier Quotes\Norrsken` + BSW), Fenster Glazing Schedule Rev 0, Door Concept Rev 3/4, Ikon IKL332 louvre.

Findings (details in `outputs\Beaumont Court - Old vs New Tender Docs - Reply to Adam (draft).txt`):

- 0310 P06->T02, 0312 P04->T03 (both 29/05/26 "updated to client's comments", now TENDER ISSUE): 5no NW3 (1245x1515 side-hung, basement gym) DELETED - window schedule 9 -> 4; ED1 2350x1264 -> 2342x1252; ED2 width 1264 -> 1252; ED3 + CW1/CW2 unchanged; NEW max handle heights NW1 1900mm / NW2 1700mm; setting-out dims added (T02 10/03/26).
- NEW louvre sketch SK-HGCE-50-ZZ-DR-M-003 Rev A (25/06/26): existing Block A GF windows replaced with ventilation louvres - possible new Fenster scope (IKL332 was in old spec). Old 0312 louvre note (1135x300) gone with NW3.
- New canopy drawings 0600/0601 (interface with ED1/CW1 head); GF re-screed 19.620->19.690 with ramps touches door thresholds.
- PACK DEFECT 1: file `4284-DMWR-31-ZZ-DR-A-0311.pdf` in New actually contains HCD screed drawing S-28-007 P04; issue sheets list 0311 T02 (10/03/26) but the real drawing is nowhere in the pack -> RFI. Latest doors/CW detail held = old P04 (30/01/26).
- PACK DEFECT 2: 11 files with .pdf extensions are AutoCAD DWGs renamed (header `AC1032`, "No /Root object" in pdfplumber/pypdf): 0103, 0121, 0226, 0228 (jamb details), 0230, 0253 (Crittal screens), 0260, 0302 (Block B elevations), 0356, 0706, 0710 -> RFI for true PDFs.

Lessons: (1) drawing issue sheets + the client's drawing register xlsx are the fastest change-detection source - read them before diffing drawings; (2) verify PDF magic bytes (`%PDF` vs `AC10xx`) before blaming the parser - client packs contain renamed DWGs; (3) drawing rev tables (P/T revisions with descriptions) give the change narrative for free; always quote them in the comparison.

### Princess Beatrice House / Guildmore-RBKC - tender AUDIT (2026-07-23)

Adam's email: take-off + "check we are hitting specification" + note pricing on Fenster's ALREADY-SUBMITTED tender (GBP272,771.68 ex VAT, dated 23/07/2026) - an audit, not a quote. Inputs in `test-results\princess-beatrice-input` (client bill C0234 Block 1, BPG schedules 5100/5101/5103 T02, RBKC ERs Nov 2025, Guildmore ITT, Fenster pricing doc + proposal, Aplus Crystal QP70171 21-Jul-2026 GBP111,185.75 glazed nett + Aplus Logikal 22/07/2026 GBP17,499.74 Technal STII, plus LAST YEAR's QT39795 letter 22/07/2025 - date-check every supplier letter). Outputs in `test-results\princess-beatrice`: 5-sheet audit workbook, review md, email draft signed Mary. Generator: `scripts/pb-takeoff.py`.

Verified exact: 191 schedule window dim-entries = 191 priced units (marks with two dim pairs = coupled frames, e.g. Type 11 16 marks -> 32 units); install GBP39,680 recomputes from house labour codes; items+install = total; Technal screens = Aplus Logikal penny-for-penny; M5 = M3+M4. Issues (ranked): Modeal-vs-Technal spec deviation (bill item A demands Technal UK spec for ALL, ER "or other approved" clause is the route - declare qualification + equivalency, get CA approval); missing scope 3nr Louvre Type 01 (WLF13/16/19 dims TBC) + 2nr 2280x1068 Door Type 1 side screens (~GBP3.5-5.5k sell); 2.5% MCD required by ITT not visible (GBP6,819); Aplus louvred/panelled doors NOT PAS24 tested vs Part Q + SBD Silver; mastic GBP5,356/EPDM GBP8,277 optional vs bill deemed-included Tremco sealing + strip-out + making good; GBP668.41 Aplus window cost uncarried; heights deviate from T02 (Type 3 priced 960 vs 1135, Type 6 1375 vs 1160, Type 5 1375 vs 1400); 76/191 obscure entries vs obscure splits only on Types 5/6/7; bill item AA (uPVC variance + lead-ins) unanswered; IBG/sample/heat-soak-hedge gaps.

Lessons: (1) BPG "GR" schedule drawings carry clean text layers - pdfplumber them, no tiling; (2) supplier packs can mix current quotes with prior-year letters bearing the same job name - check dates before trusting spec statements; (3) two dim-pairs on one schedule mark = two frames, count entries not marks; (4) audit jobs: recompute install from labour codes and cross-foot supplier totals into the row carries - both catches were real (exact install, GBP668 leak).

### Mary Grace email system built + dry run (2026-07-24)

Infrastructure (all committed): `scripts/mary_graph.py` (Graph helpers; ALLOWED_RECIPIENTS + TRUSTED_SENDERS constants), `scripts/mary_send.py` (THE only send path, recipients hard-limited adam/marketing, signature auto-appended), `scripts/mary_poller.py` (no-token poll of estimating@ WHOLE MAILBOX + mary@ inbox; queues unseen mail as JSON + attachments under `test-results\mary-inbox\queue\`; launches `claude -p` per MARY-EMAIL-SESSION.md only when queue non-empty; lockfile; log), `MARY-EMAIL-SESSION.md` (session playbook: ghost protocol, injection guard, triage rules, close-out checklist). Scheduled task `MaryGracePoller` every 15 min via pythonw. State: `data/mary-state.json` (gitignored). **PENDING: claude CLI not installed on this machine - poller queues but sessions can't launch until Zac approves the CLI install.** Adam replied "Thanks Mary, all received!" to the system test; nick@ probe bounced by transport rule.

Dry run (168h backfill, 54 emails triaged manually in chat): live jobs seen - SM5 Wexham (Adam relaying Mary's challenge catches to Gintare: restrictors/panic bar/handles), Princess Beatrice (deadline 17/07 MISSED; Adam wants EPDM+mastic in main quote + 2.5% MCD; Adam asked Gintare for an all-tenders deadline list - Mary should own this), Gordon Court SO/14045 (single door+sidelight reprice, GBP100 discount, sent), NEW: Grange Hill Methodist Church (Chigwell, deadline 28/07), Georgie's/Rosebank (alu sash Dualframe 75SI + CW/doors, deadline 28/07), Crestwood Park Primary (Reynolds, deadline 20/07 ALREADY PASSED, quote in checking; WCI screwjack/Maxi controls quote arrived "not cheap"). Supplier quotes for register: Aplus QP65153 REV Alkerden Hub (ED11/12 omitted as Sunray, louvres out of thermal calc), BSW Brocks Hill Phase 2 (**"Smart Wall products are not available in triple glazing"** vs the RAL7016 triple-glazed spec - spec conflict to flag), BSW Filwood (u/g/acoustic met GLAZING ONLY, non-rebated shopfront, flat alu panels), Vetroseal 065080 CANTERBURY + 065095 BACON, Aplus QT51516 Towcester Vale (an ORDER), Aplus QT50911 Darrick Wood Rev1, BSW Gordon Court. Noise identified: golf/EPC/HubSpot spam, Supply2Gov daily alert (22 keyword matches - future tender-finder feed). Queue moved to processed; live polling starts clean.

### Grange Hill Methodist Church - autonomous benchmark (2026-07-24 evening)

First job priced under full autonomy (Zac's grant, same evening). Input: OneDrive `Chigwell (London) PLC\Grange Hill Methodist Church\1. Estimating\1. Tender Documents` (spec workbook + drawings, no schedule) -> `test-results\grange-hill-input`. New entrance building for the church (JCT MW 2024 main contract, works Nov 2026-Jul 2027); Fenster package = alu windows/doors/screens, white, Optitherm S1 solar Arctic Blue + S1 plus, fish-symbol manifestations, west 1200mm DDA door with AUTOMATIC OPERATOR (spec 3.12/3.13, zero-rated VAT), south gable screen with 2no 1200 doors to ~2300 (3.14).

Output: `outputs\Grange Hill Methodist Church - Fenster Pricing Document (house format).xlsx` - **GBP 27,560.07 ex VAT benchmark** (CW convention on both screens per the Greenfields calibration rule; template computes O=sqm from the Size string, M=Ox850, N=Ox150 - CW rows need NO generator changes, just code CW + "W x H" size). Emailed to Adam+Zac with attachment ~18:00.

KEY CATCH: **spec 3.15 (chapel alu folding doors ~5.8m dark brown + glazed section above) is NOT in the supplier RFQ Gintare sent at 15:14** - flagged to Adam with ~GBP10k budget option (calibrated at the SM5 Sheerline bifold rate ~GBP542/m2 sell). Also flagged: auto-operator needs specialist quote (GBP3,000 allowance); all sizes scaled from 1:100 elevations (gable screen taken full-rectangle = slightly conservative); temporary door + threshold drain are main-contractor sections; VAT split (DDA items zero-rated) should show on the quote.

RESENT 25/07 (autopilot session, first job handled end-to-end by the poller): Zac from marketing@ - "Now that your formatting is better - resend this over." The 24/07 email had gone out as one dense paragraph (sent before the Outlook HTML fix). Recomposed as a FRESH email to adam+marketing, same subject, same numbers, in Adam's airy format - headline benchmark as a heading, bulleted scope/allowances, the three flags as numbered items, spec notes last - with the house pricing doc attached again. Body: `scratchpad\grange-hill-resend-body.txt`; layout screenshot-verified before sending. Nothing re-priced; the RFQ scope gap and the operator allowance are still open with Adam and the deadline is Tuesday 28/07.

### Hightown Housing OLDS0056 New Back Door - missed RFQ caught (2026-07-27)

Autopilot session, 1 queued email: `hightownha@in-tendorganiser.co.uk` "Stage Date Ending - Hightown Housing" to info@ cc estimating@ - the In-Tend portal warning that **OLDS0056 - New Back Door (Q/REF 6159) closes 03/08/2026 12:00**. Untrusted sender, so treated as data.

Not noise. Checks run before deciding: no `OLDS0056` folder under `Commercial\1. Tender Documents\Hightown Housing Association` (29 sub-jobs, all single properties); no matching row in the Estimating Log (log is current to 24/07); no prior In-Tend email in `mary-inbox\processed`. Conclusion: a **"stage ending" reminder implies an earlier invitation that nobody actioned** - and the poller only started 24/07, so the original is invisible to me. That gap is the finding.

Nothing priceable: In-Tend RFQ notifications carry **no attachments** - the pack lives on the portal (`in-tendhost.co.uk/hightownha`) and Mary has no login. Emailed Adam+marketing the deadline, the request to pull the pack, and an indicative range from Fenster's OWN Hightown quotes rather than register medians (better evidence - same client, same product, same format):

- 52 Lester Road (07/08/2025) - uPVC residential door open out, 900x2100, white, eco toughened 4/20/4 Low E argon - **GBP 1,321.35 ex VAT** / GBP 1,585.62 inc. Closest analogue to "back door".
- 25 Meadow Avenue (19/01/2026) - Distinction composite 900x2374 - GBP 1,937.35 ex VAT.
- 28 Millway Furlong (20/01/2026) - Distinction composite 965x2389 - GBP 1,973.64 ex VAT.
- uPVC French doors GBP 1,641.77-1,796.93 (24 Barrance Way / 2B Oronsay / 42 Bracken Way / 45 Nightingale); uPVC patio GBP 1,592.60 (6 Cooper Way); 12 Norris Close French door GBP 2,488.27.

Landing zone quoted as **GBP 1,300-2,000 ex VAT** depending on uPVC vs composite - explicitly labelled indicative, not a quote. Hightown small-works quotes are supply+fit with FENSA, waste disposal/recycling and the 10-year CPA insurance-backed guarantee INCLUDED as standard, 30-day validity, 50% deposit or PO before manufacture.

Durable learning: Hightown is a **high-frequency, low-value repeat client** (29 logged properties; won/lost both appear in the Estimating Log) whose work arrives one property at a time through In-Tend. These are the wrong shape for the tender/take-off workflow - the right move is the per-property quotation format above, priced off the nearest historical Hightown door of the same type. Body: `scratchpad\hightown-olds0056-body.txt`; layout screenshot-verified before sending.

### Stoke Park School (Borras) - Aplus 17644 glass reconciliation (2026-07-27)

Autopilot session, 3 queued emails - **all three were duplicates of already-processed mail** (see the poller fix below). Two needed nothing: the Saint newsletter (noise, handled 26/07) and the Hightown In-Tend stage-date reminder (handled 27/07 08:30). The third was worth a second look: Aplus `noreply@` "Glass Sizes for Job 17644-Stoke Park School" (24/07 15:25, 7 attachments). It had been swept into `processed\` inside the 54-email dry-run batch on 24/07 without being read - a production document for a job Fenster has already won, so it fell between the triage categories.

Reading it changed the picture. `Glass Sizes_17644.PDF` is an **UNGLAZED, supply-only** sheet: Aplus makes the Technal frames, delivery **03/08/2026**, and the glass is Fenster's to buy. Job folder is `Commercial\2. Projects\Borras\Coventry - Stoke Park School` (client price GBP104,660.17 ex VAT, pricing doc rev 15/07; order signed off 17/07). The only glass documents on file are two 01/07 quotes - Vetroseal 064542 and a CN Glass rate in Steve Freezer's thread - both priced from Fenster's earlier `Glass sizes.xlsx` (04/06), not from this list.

Reconciliation (`scripts/stoke-glass-compare.py` -> `outputs\Stoke Park School - Glass Sizes vs Quoted Glass (check).xlsx`):

- Aplus final list: **170 panes / 130.81 m2** to order (86 rows; 161 panes at 28mm / 122.48 m2 + 9 at 32mm / 8.33 m2). Five panes marked "DO NOT ORDER - Unglazed" are the aluminium infill panels and are excluded.
- Vetroseal 064542: **124 panes / 105.24 m2**, net goods GBP11,576.36 + energy surcharge GBP436.52 (3,357.82kg @ 0.13) = **GBP12,012.88 net**.
- Shortfall **46 panes / 25.57 m2 (+24%)**, and the per-type deltas sum to exactly 46, which is what validates the mapping: pane ref **A1** (the ~391mm toplight, 1041-1049 wide) is missing on every bay of Types A (-3), B (-4), C (-20), D (-2), F (-8), G (-4); head panes missing on Door B1/D02 and B2/D04 (-1 each); **Door Type C (D03) is not on the quote at all** (-3). Types E, H, J1, J2 and Door Types A and D match.
- **No 32mm make-up is quoted anywhere** - all 58 Vetroseal lines are 8.8L-16-4T (28.8mm). The 32mm panes are the door head/transom panes. Door leaf sizes also moved: 785x1934 quoted vs 749x2059 required.
- Money: Vetroseal's implied rate is exactly **GBP110.00/m2 goods** (+GBP4.15/m2 surcharge = GBP114.15/m2 all in) -> ~GBP14,930 for the full list, about **+GBP2,920**, before the 32mm rate. **CN Glass quoted the same make-up at GBP60/m2 inc energy** (+GBP10/m2 for a 6mm toughened softcoat inner) -> ~GBP7,850, roughly **GBP7,000 below Vetroseal**. Glass sits inside the unit rates on the Borras pricing doc, so any increase is margin.

Emailed Adam+Zac with the workbook attached, headline first, asking three things: which supplier holds the glass order and whether it is being placed against the 24/07 list, the make-up for the nine 32mm panes, and whether the CN Glass rate is in play. Body `scratchpad\stoke-glass-body.txt`, layout screenshot-verified. Stated the honest caveat: pane sizes drifted a few mm between the two lists so the *which pane* mapping is inference, but the 170-v-124 totals are firm.

New register evidence: Vetroseal 8.8L-16-4T Lami/Tgh Black Multitech G 1.2 softcoat argon = **GBP110.00/m2 flat, quote 064542, 01/07/2026** (energy surcharge GBP0.13/kg at 31.9 kg/m2); **CN Glass GBP60/m2 inc energy** for the same make-up, +GBP10/m2 for 6mm toughened softcoat inner - the first CN Glass rate captured, and roughly half Vetroseal's.

Lessons: (1) production documents for WON jobs (glass sizes, cutting lists, sign-offs) are a distinct triage class - the risk is procurement, not pricing, and a bulk "processed" sweep will bury them; MARY-EMAIL-SESSION.md now has a rule for them. (2) An unglazed supplier order transfers the glass buy to Fenster - always check a glass order exists and matches the FINAL sizes. (3) Fenster's own preliminary glass schedule was the source of the error, not the supplier's quote - when a shortfall is systematic (one pane per bay), suspect the schedule, not the pricing. (4) Aplus glass-sizes sheets parse cleanly with pdfplumber: `item | ref | qty | w | h | glass type | location`, negative heights and "DO NOT ORDER - Unglazed" mark infill panels.

Also fixed this session: **the poller was re-queuing handled mail.** Microsoft Graph message ids are scoped to the Outlook folder a message sits in, so filing or moving a message yields a new id that id-only dedup reads as new mail - three re-fired at 09:10. `mary_graph.list_messages` now selects `internetMessageId`, and `mary_poller.py` dedups on that plus a `received|from|subject` content key held in `state["seen_keys"]`, seeded on first run from every JSON already in `queue\`/`processed\` (62 keys). Queue files must stay in `processed\` - they are the dedup history.

### Vesuvius Way Worksop / Staniforth Construction - budget + RFQ quantity audit (2026-07-27)

Trigger: queued email 27/07 08:20 from `estimating@` (Gintare Vanagaite's signature, no subject, 10 attachments). Not an incoming enquiry - it is the **supplier RFQ going out** for the Air Separation Unit job that had been sitting on the Estimating Log unworked since 22/07, deadline **Thu 30/07**.

Client Staniforth Construction LLP (Joe Mayer), end client BUSE Gas Solutions, architect JHA Architecture Ltd (job 2024-055), site Plot 8 Vesuvius Way, Worksop S80 3NE. Trade bill `L_SC Aluminium Doors & Windows`.

Inputs: emailed subset copied to `test-results\vesuvius-input`; the **full 55-file tender zip** from `OneDrive\Commercial\1. Tender Documents\Staniforth Construction LLP\Worksop\1. Estimating\1. Tender Documents\` extracted to `test-results\vesuvius-input\full-pack`. The email carried 10 of those 55 - the window schedule (2024-055-222P), door schedule (221P) and NBS spec were all missing from it and all three were needed to resolve the scope.

Take-off (read visually from the Logikal drawings at 110 dpi, title blocks re-cropped at 300 dpi to confirm the stated quantities):

- Curtain wall, Senior SF52: welfare Ele 1 2000x2450, welfare Ele 2 2950x2450 incl single AFT door, office Elevation 01 6900x6000 raked (= 41.4 less the 3.35x3.35/2 triangle = 35.79 m2), office Elevation 02 6500x6000 incl double AFT door. **86.92 m2 total.**
- Windows, Senior PURe: 8no 1350x1450 (office, marks W05-W12), 4no 750x950 (welfare Ele 4), 1no 1500x1255-1150 (welfare Ele 1, no drawing exists).
- Doors, Senior SPD150: 2no 1000x2450 with 350 toplight.

Pricing (budget, no supplier quote held): curtain wall on the MASTER PRICING DOC formula GBP850/m2 supply + GBP150/m2 labour; windows/doors on BSW size-banded register medians (glazed casement GBP445.71/m2 `<1.5m2`, GBP358.44/m2 `1.5-3m2`; glazed door GBP422.99/m2 `1.5-3m2`) plus a **+15% Senior premium, estimator judgement**; then house template code adders (SAW 337.50, MAW 412.50, SAD 900, DAD 1500) and Adam's labour codes.

Result: supply GBP84,922.05 + adders GBP9,262.50 + installation GBP16,367.43 = **GBP110,551.98 ex VAT** (GBP132,662.38 inc VAT). Curtain walling is 79% of it. Outputs: `outputs\Vesuvius Way Worksop - Fenster Pricing Document and Review.xlsx` (Summary / Pricing Lines / TBC & RFIs / Quantity Check / Source Notes), generator `scripts/vesuvius_pricing.py`.

**Headline finding - the RFQ issued that morning asks suppliers for six fewer units than the trade bill.** Drawing 005 (welfare Ele 4 window) says "Quantity: 1" against bill item F 4no; drawing 004 (welfare Ele 2 SPD150 door) says "Quantity: 1" against bill item E 2no; drawing 008 (office window) says "Quantity: 6" against schedule 222P marks W05-W12 = 8, which the bill also totals at 8. Drawing 001 (access hatch) was not attached at all although the hatch is bill item A, and bill item C has no drawing anywhere in the pack. The bill also mislabels W08 as W06 in item D, so W06 appears on two elevations.

Not priced, carried as TBC + RFI rather than guessed: access hatch (Senior PURe SLIDE 1450x1200, no register category), louvred double door 1450x2110 (specified insulated **steel-core** PPC galvanised - a Strongdor item in an aluminium bill, and listed under Building 1 while its only detail sits on the Building 02 door schedule), 2no first-floor partition windows with **Pilkington PyroStop fire glass in Senior PURe frames** (PURe is not fire-rated - needs a tested fire screen; EI30 vs EI60 unknown), and the extra-over obscured/reflective spandrel items. Excluded: roller shutter 3500x5900 (on schedule 221P but not in this bill), Howdens internal joinery doors, and the JS Office Environments reception-screen quote in the pack (ref MCJ/25204, 12/06/2025, GBP4,595 + extras - addressed to the architect, not Fenster).

**Tender-stopping issue raised to Adam: the pack is entirely Senior Architectural Systems and none of BSW (Sheerline), Aplus (Technal) or Bellview (SMA Smart Wall) fabricate Senior.** Either a Senior-approved fabricator is found this week or an alternative system is formally qualified in the tender. Every rate in the workbook comes from non-Senior quotes and is labelled as indicative for that reason.

Email sent 27/07 to adam+marketing with the workbook attached. Also flagged: Worksop still marked "to log" on the Estimating Log five days after the enquiry, and Pearce Construction "Georgie's" is due 28/07, also "to log", with no pack ever seen.

### Princess Beatrice House - audit of the quote AS ISSUED to Guildmore (2026-07-27)

Adam released the quote at 08:56 ("Please proceed with sending this out with the discount"); Gintare issued it to
jason.mount@guildmore.com at 09:49 with the pricing xlsx, the proposal PDF and a 59-page "Window and Door Drawings.pdf".
Mary audited the pack that actually went out.

**GBP 279,244.69 ex VAT.** Arithmetic verified exact: 46 line rows / 217 units = GBP233,091.68, + install GBP39,680 +
external mastic GBP5,356.22 + EPDM GBP8,276.91 = subtotal GBP286,404.81, less 2.5% MCD GBP7,160.12. Every row's
rate x qty ties to its total. The base is GBP272,771.68 - unchanged from the 23/07 audit - so Adam's two instructions
of 24/07 (EPDM and mastic into the main quote, not optional; add 2.5% MCD) were both carried out in the pricing.

His third instruction was not. He wrote "We will need to adjust the clarifications on the proposal to reflect the
above", and the proposal that went to the client still says, on page 3, **"External mastic is charged as an optional
extra"**, with EPDM absent from the clarifications entirely. GBP13,633.13 is charged in one document and disclaimed in
the other, in the same email. Raised as REQ-6.

Two further contradictions inside the issued pack:

- The proposal says "The external door package is based on Technal STII thermally broken commercial doors"; the pricing
  document heads Door Types 1-5 "Modeal Complex Coupled Doors". The Modeal-for-Technal substitution - HIGH item 1 of
  the 23/07 audit - is still not formally qualified anywhere.
- The drawings pack we attached carries "ITEMS GLAZED WITH PANELS HAVE NOT BEEN TESTED TO PAS24" on five pages
  (2, 3, 4, 5, 58) while the proposal claims PAS24 multipoint locking, against a Part Q / SBD Silver ITT.

Checked and clean: no supplier prices leaked in the drawings pack (it is an Aplus Logikal "OFFER" export whose
Qty/Unit Price/Total columns are empty). Confirmed still open: there is no louvre line anywhere in the pricing or the
drawings, so the 3nr Louvre Type 01 remain neither priced nor excluded while the proposal's executive summary tells the
client the elevations identify acoustic louvre elements.

Commercial note recorded rather than flagged as an error: the MCD was taken as a straight deduction, so GBP7,160.12
comes off margin. Neutral treatment would have required grossing the subtotal to GBP293,748.52 first. Gintare asked
Adam whether he was happy with how it was added and he approved it.

Issued 10 days after the 17/07 return date.

### Crestwood Park Primary School / Reynolds Conservation - audit of the quote AS ISSUED (2026-07-27)

First time Mary has seen this job. Adam released it at 10:42 ("Good to go, please amend the dates before sending") and
Gintare issued it to adam@reynoldsconservation.co.uk at 10:49. Dates were amended - 27/07 on both documents.

**GBP 74,158.66 ex VAT.** High-level window replacement inside Dudley MBC's Crestwood Park Roofing Works 2026.
46 rows, 52 units, 67.28 m2. Composition: GBP47,879.60 windows + GBP8,500 install + GBP17,779.06 Teleflex. Mastic
GBP1,286.10 and EPDM GBP1,579.63 shown as optional.

The build verifies exactly. BSW **QT252906** (16/07/2026, Sheerline Prestige casement, Hipca White 9910HG) is
Total Nett Ex VAT **GBP27,329.60**; the client-facing window lines total GBP47,879.60; the difference is
**GBP20,550.00**, which decomposes into whole house-template code adders on every single row (ELAW 637.50 on the two
large W23 leaves, LAW 487.50 on W23 3/3 and the eight 2075x1300 units, SAW 337.50 on the rest). Nothing dropped,
nothing double-counted. Install GBP8,500 / 52 = GBP163.46 per unit, consistent with the 160 labour codes.

The findings are all scope and spec, not arithmetic:

1. **Teleflex.** GBP17,779.06 - 24% of the tender - sits as one lump with no qty or rate breakdown and **no supplier
   quote anywhere in the job folder**. Meanwhile the proposal clarifications exclude "Teleflex controls / wiring", and
   drawing A007 expressly says "Include for all installation, core wire, conduit and fittings as required", specifying
   2No. operators per light plus 1No. Midi control (W1-W8, W20-W23) or Maxi control (W12, W16-W19, W24-W27) per opening
   light, control locations as existing. Fenster has excluded the thing it is charging for. Raised as REQ-7.
2. **Glass deviation.** A007 requires outer 6mm Pilkington Suncool Pro T 66/33 toughened, inner 6.4mm laminated. BSW
   quoted every line as "6.Lam / 16 / 6mmTuff Coolite SKN175ii" - a different product, with the laminated and toughened
   panes apparently reversed, which moves the solar control coating. The proposal recites the specified Pilkington
   make-up back to the client on page 3, then offers "6mm laminated / 16mm cavity / 6mm toughened" in the products box
   with no deviation stated.
3. **W15.** A007: "Window W15: To be removed and infilled as per the section" - remove window and winders, 75x50
   tanalised ladder frame, 12mm WBP ply, prime and felt, PIR infill, 10mm white uPVC lining. A second note on the W22
   elevation reads "Infill window as per W15". Neither priced nor excluded. (W13, W14 and W28 are correctly absent -
   A007 says "No works required" for those, which is why the pricing jumps W12 to W16.)
4. Smaller: A007 requires the existing windows to be "removed and disposed of" while the exclusions say waste removal
   is generally excluded; W12 needs a catering-standard insect mesh grill that is not priced; and the **asbestos
   (chrysotile) in the existing high-level window mastic** appears only in a prose sentence on proposal page 3, not in
   the hard exclusions column, even though Fenster's installers have to remove those windows.

Also worth watching: mastic and EPDM are optional here, which is the opposite of what Adam ordered on Princess
Beatrice the same week. Flagged to him in case that is now a policy change rather than a job-by-job call.
Client-facing typos: "W23 2/2" should read 2/3; "EDPM" for EPDM.

Tender pack extracted to `test-results\crestwood-input`. Issued 7 days after the 20/07 return date.

### Riverside - Aplus QT51518 AOV free area (2026-07-27)

Adam asked Gintare on 24/07 for 2nr bottom-hung AOV smoke vents at 1130 x 1530, standard white, 150mm cill, and
specifically: "Please confirm the free area. We need 1.5m2 so sizes can be adjusted if required."

Aplus QT51518 (27/07/2026) landed this morning. **The answer is no.** The quote states
**"Geometric free area = 1.30m2"**, based on a 50mm reveal - 0.20 m2 short. Aplus also give the fix on page 2:
**1235 x 1583 achieves 1.5 m2** in the same configuration, using 900mm chains instead of 850mm.

Price as quoted: **GBP4,845.22 net ex VAT for the pair** (frames GBP4,662.15, glass GBP171.31, energy surcharge
GBP11.76). DualFrame 75Si, style FF, white, 155mm Technal subcill - not the 150mm asked for - open out, AOV 850mm
stroke single chain, actuator colour 9006 satin, glass 4-20-4 clear toughened soft coat 1.2 with 20mm black warm edge.
**Supply only, delivered - no installation.** Valid 30 days. Specified No PAS24, No Restrictor, Handle Not Required,
Casement locking None, which is normal for a smoke vent but worth confirming against what Riverside expects.

Their AOV notes page carries constraints that need to reach whoever installs: cables are not run through the mullions
(about 2m of flex is left coiled at the vent); the actuators are not restrictors and Aplus disclaim liability for
damage if a separate restrictor is not fitted 50mm beyond the stroke; vents below 2.5m from FFL raise a trap hazard
under BS EN 60335-2; below 1100mm from FFL they need Part K anti-fall protection, which Aplus exclude. Raised as REQ-9.

### Vesuvius Way - 60-minute fire doors found in the specification (2026-07-27)

Gintare emailed Steve at 09:35 asking about the pack: "doors shown to be Senior, some are part of Curtain Walling,
however as per specification all external doors to be 60min fire rated." Mary verified it at source rather than taking
the email at face value - `test-results\vesuvius-input\full-pack\NBS Specification\JHA-JOH-2024-055-JHA NBS Section
2.pdf`, clause **L20**, JHA Architecture, 15/07/2026:

- **External Doors**: "60 Min Insulated steel-core external open-out single-leaf door. PPC Galvanised double skinned
  door leaf with PPC Galvanised 90mm enclosed frame." Vision panel 572 x 572. U-value 1.2.
- **External Doors Curtain Walling**: "60 Min Door installed in curtain wall to manufacturers design." Manufacturer
  given as SAS Curtain Wall Design.
- **External Doors Louvered**: 60 Min, steel-core, louvred leaf, louvres to comply with the NOVA acoustic report.
- **L20/70**: performance tested to BS EN 1634-1 or BS EN 1634-3, third-party certified, Fire Door Schedule to
  Building Control and the Principal Designer before order.

**The GBP110,551.98 budget issued this morning is understated.** Line B1-E (2no doors 1000 x 2450, sell GBP4,683.56)
was priced as a standard Senior SPD150 aluminium door off BSW glazed-door medians - the wrong product family, since an
insulated steel-core PPC galvanised door is a Strongdor / Aluminium Fire Systems item. More seriously, lines B1-D
(welfare curtain wall screen, GBP8,377.50) and B2-E (office entrance screen, GBP41,000.00) are SF52 screens with doors
inside them: **GBP49,377.50, about 45% of the budget**, sitting on screens whose doors the spec says must be 60-minute
rated, which a standard SF52 cannot do. Those bays need a tested fire-rated screen system.

Not requantified - it needs a fire-screen specialist to price, and Aluminium Fire Systems (Julian Ward, Q7666) are
already quoting Fenster on Manor Lodge. This compounds rather than replaces the open Senior-fabricator problem.
Deadline is Thursday 30/07. Raised as REQ-8.

One spec defect worth an RFI: clause L20/45 "Door leaves (Internal)" carries the identical external steel-core wording
but names Howdens as manufacturer - it reads like a JHA copy-paste error, and it makes the internal/external split
unclear.

### Stoke Park School - CN Glass provenance corrected (2026-07-27)

Adam replied to the morning glass reconciliation with one question: "Where did you get the CN Glass info from?"

Source is `Commercial\2. Projects\Borras\Coventry - Stoke Park School\1. Estimating\2. Supplier Quotes\CN Glass\Re
Stoke Park School - Coventry .eml`. Steve Freezer emailed Martin Gregory (martingregory@cnglass.co.uk) on 01/07 with
the glass schedule and the spec - 8.8mm laminated outer, 16mm argon warm edge, 4mm toughened Low-E on face 3 - and
**wrote the rates into his own outgoing email**: "GBP 60 m2 inc energy" plus "GBP 10 m2 for 6mm Tgh Softcoat on inner".
Martin replied the same afternoon with nothing but "Pls see below as discussed".

So it is a rate agreed verbally and confirmed by return email, **not a priced quotation** - there is no CN Glass
quotation document in the folder at all. Mary's morning email said "CN Glass quoted", which overstated it; corrected
to Adam in the afternoon digest. The make-up does match what Vetroseal priced (8.8L-16-4T), so the comparison is
like-for-like, but CN Glass should price the final 24/07 list properly - including the nine 32mm door panes neither
quote covers - before any order moves on the strength of it.

### Hightown Housing - closed on instruction (2026-07-27)

Adam, 08:53, replying to the morning OLDS0056 flag: "Let's leave anything for Hightown Housing for now. We have quoted
them many times and don't win any works, so please disregard their quotes unless instructed otherwise."

The 03/08 12:00 In-Tend deadline is deliberately not being actioned. REQ-4 closed as answered, job row marked closed,
and the rule written into `AI.md` under "Clients Not To Quote" - future Hightown RFQs and In-Tend reminders triage as
noise: one line in the session record, no email, no request raised.

### BCC 4-16 Filwood Broadway / Stepnell - QUOTE TO CHECK, first turn of the permanent job chat (2026-07-27)

Work order `20260727T1301-zmHQAAAA.json` - Gintare Vanagaite (estimating@) to Adam, 13:01, "QUOTE TO CHECK Re: BCC, 4-16 Filwood Broadway, BS4 1JN", deadline "30th July - Thursday". No attachment on the mail; the quote was found live in the job folder (pricing xlsx 14:01, proposal docx 14:09, both still being edited during the check). Routed to the new `filwood` chat on `subject~filwood` / `subject~broadway`.

Inputs: `OneDrive\Commercial\1. Tender Documents\Stepnell\BCC Filwood Broadway\1. Estimating\3. Client Quote\Stepnell - BCC Filwood Broadway Pricing.xlsx` + `...Proposal.docx`; supplier quote `...\2. Supplier Quotes\bcc filwood.pdf` = **Bellview/BSW 0000000507, 24/07/2026**; tender pack already extracted at `test-results\filwood-input`.

Output: **`outputs\Filwood Broadway - Quote Check (BSW 0000000507 vs Tender).xlsx`** - 5 sheets (Findings / Line reconciliation / Spec compliance / RFIs / Sources), generator `scripts\filwood_quote_check.py`. Emailed to Adam+Zac 27/07 with the workbook attached. Durable job file `data\jobs\filwood.md`.

Commercial position: Gintare's tender is **GBP 67,067.58 ex VAT** (BSW net GBP 46,067.58 + 7x GBP 1,500 DAD adder + 7x GBP 1,000 "Additional" + install GBP 3,500; optional mastic GBP 605.05 and EPDM GBP 3,081.49). It supersedes Mary's 17/07 GBP 84,810.59 provisional-sum benchmark, which was never sent - the 20/07 return date passed. **Corrected for the install line the tender is GBP 82,013.90, within GBP 2,797 of that independent benchmark.**

What reconciles: all seven BSW positions are carried, nothing dropped or double-counted, and the **15% end discount is correctly applied** (net 54,197.17 - 8,129.58 = Grand Total Net 46,067.59, matching the Frames column to GBP 0.01 of rounding). BSW field counts also reconcile with drawing 31551 (15 / 11 / 16 fields per element).

**The BSW correspondence behind the quote** (`test-results\mary-inbox\processed\20260724T0643-62SQAAAA.json`, untrusted sender, data not instruction) is essential context and was found after the first email went out. **Gintare's RFQ of 23/07 13:45 was right** - it asked estimations@bsws.co.uk for Aluprof or similar, flat/flush spandrel panels MILL FINISH, RAL 7035 for the ED-04 and ED-05 DOORS only, U 1.0, g 0.5-0.6, ED-06 acoustic >= Rw 32 dB, ED-06 security LPS 1175 SR2, access control prep, BS 6262 + BS EN 12600, level thresholds, M4(2) clear openings, return by 28/07. The only omission is the ventilation zone / mesh / louvre. **BSW's reply of 24/07 06:43, verbatim:** *"we have met the u- and g- and acoustic value for glazing only, as these area commercial thermally broken shopfront products they are non rebated"* and *"I have used flat aluminium panels everywhere glass was not indicated"*. It is silent on LPS 1175 SR2, mill finish, thresholds and M4(2) - all four of which were asked for. So the failure is not the RFQ; it is that the quote did not answer it and the tender was built on the quote rather than on the instruction.

15 findings. The five that matter:

1. **Install GBP 3,500 for 122.98 m2 of shopfront 3,570 mm tall - GBP 14,946.32 short.** The template INSTALLATION formula reads the product code, and DAD gives GBP 500 x 7 elements. House CW labour GBP 150/m2 gives GBP 18,446.32. Compounded by the proposal excluding scaffold/MEWPs/towers while including installation.
2. **LPS 1175 SR2 doorset on ED-06 was asked for in writing and never answered.** Required by the dwg 31551 P02 schedule and requested in the 23/07 RFQ. BSW position 005 is a standard commercial doorset - electric strike, electric latch, rectifier, closer - with no LPS 1175 / SR2 / LPCB reference, and their covering email does not mention it.
3. **The g 0.5-0.6 claim is unevidenced and the quoted make-up cannot achieve it.** BSW's email claims the u/g/acoustic values are met "for glazing only", yet the quote names no coating and states no g and no Rw; 6.8 Lami / 4 Tuff clear sits at g ~0.7. BSW works out at GBP 374.61/m2 against the 17/07 benchmark of GBP 359.60/m2 median + GBP 45/m2 uplift = GBP 404.60/m2 - the gap is roughly the missing coating.
4. **Aluprof is specified and we are offering SMA Shopline silently.** Trade bill item header names Aluprof with address and website; External Materials Schedule s.N p41 gives Manufacturer = Aluprof; dwg 31551's revision history reads "Issued to Aluprof 2025.10.22" and "Updated Issue to Aluprof 2025.10.29". The ITT: VE proposals "must be fully detailed indicating any areas of non-compliance and be accompanied by a compliant bid" - we have neither. Third alternative-system exposure this month (Technal/Modeal on Princess Beatrice, Senior on Vesuvius).
5. **The Ventilation Zone is priced as solid flat aluminium panel.** The top 660mm (ED-04) / 700mm (ED-05) band is labelled "Ventilation Zone" either side of "Signage Zone", tagged Q2 = Cadisch expanded aluminium mesh high free area, with four "Mullion behind mesh" notes; the bill measures the full 3,570 / 2,970 height so the band is inside our item. Every non-glazed field is priced as flat sheet.

Then: BSW priced four elements 80-130mm narrower than the bill nominal we are quoting (4850/4800 vs 4930; 6250x3100 vs 6315x3105) - not a tolerance deduction; the acoustic make-up is transposed (heavy 8.8/6 SG on the two ED-05s that need no rating, light 6.8/4 on ED-06 which needs >= Rw 32 dB, and no Rw stated anywhere); ED-05 quoted Ug 1.1 against a 1.0 target while the proposal tells Stepnell "1.0-1.1 where quoted" with no deviation statement; manifestation (ADM two bands 850-1000 and 1400-1600 to all clear glazing) is named in our own Executive Summary as a requirement then neither priced nor excluded, and the "signage, branding" exclusion does not cover it; single pivoted doors quoted on all seven but coded DAD (double) - GBP 1,500 adder + GBP 500 install each - while dwg 31551 makes double outward-opening doors conditional on ">60 occupants (see OFR)" and the OFR is not in the pack; mill finish is specified for frames AND spandrels with PPC RAL 7035 to the doorset only (bill header + p41 + palette p6 "allows the mill-finish aluminium around the shopfronts to remain the primary visual feature") and we priced RAL 7035 throughout; **bill item A is unanswered** - it instructs shopfronts as Contractor's Provisional Sums under Work Section A54 with "DO NOT include the shopfronts twice within your tender submission", and Gintare's firm lump sum reopens the decision Mary took on 17/07; Stepnell's commercial terms are unqualified (D&B 2024, subcontract amended to main contract + Stepnell conditions, LAD GBP 1,358/calendar week, retention 3%, 12-month maintenance, collateral warranty, PI required where Contractors Design, payment last business day of month following application) against our standard 50% deposit / 50% on completion T&C page; and (15) **BSW's own written caveat - performance met for GLAZING ONLY because the frames are non-rebated - is not carried into the tender return**, where the drawing schedule's U 1.0 and Rw 32 dB are element targets and our proposal renders the whole thing as "Ug values noted between 1.0-1.1 W/m2K where quoted". Quote 0000000507 as filed also has no terms page at all: no validity, no lead time, no payment terms, against a 09/11/2026 main contract start and LADs of GBP 1,358 per calendar week.

Admin defects to fix before issue: proposal **addressed "FAO: Trevor Copeman"** where the ITT and the bill both name Adam Warner (queries also to sam.ignatov@stepnell.co.uk); proposal dated 27/07 vs pricing document 28/07; the proposal still carries live Word LINK fields to `C:\Users\fenst\Downloads\Pricing Doc Template.xlsx`; **no columns are hidden in the workbook**, so J-P expose BSW's cost per screen and K3/L3/M3 read "Supplier used: BSW 46067.59" - print area C1:I27 is clean, so PDF only (Gordon Court's practice is a separate "DO NOT SEND" twin); `O16` = `#VALUE!`; row 14's working-column formulas were not filled down; ED-06 typed 6315 x **3150** where the bill says **3105**.

**Six documents the drawings and the bill rely on were never issued**, two of which define requirements we are being asked to price: Work Section A54; the OFR / fire strategy (decides single vs double leaf); the **Employer's Requirements** (the sole definition of the "ERs" security duty on six of the seven screens); the Part Q strategy drawings 2411-RCK-ZZ-00-DR-A-09200 to 09204 (door locking and access method, and the drawing says the access control scheme shown is indicative only); drawing 2411-RCK-ZZ-ZZ-DR-A-21351; the architect's specification. All drafted as RFIs in the workbook.

Lessons: (1) **the template INSTALLATION formula silently under-prices anything measured in m2** - it reads the product code, so a 17.6 m2 screen coded DAD collects GBP 500 of install; posted to the noticeboard as a cross-job check. (2) A supplier quote reconciling to the penny says nothing about whether the right product was quoted - BSW 0000000507 is arithmetically perfect and misses the security rating, the solar coating, the acoustic allocation, the specified finish and the specified system. (3) Reading the architect's materials schedule pays: the finish, the mesh and the Aluprof requirement are all in the External Materials Schedule, not the bill. (4) `pdfplumber` on RCKa A1 drawings recovers the whole performance schedule table as text - no tiling needed - but the elevation itself had to be rendered at 200 dpi to establish that the cross-hatched band is mesh and not glass. (5) **Read the RFQ as well as the quote.** Four findings changed weight once the 23/07 RFQ and BSW's 24/07 reply were found in `processed\` - the RFQ was right, the reply was a partial refusal, and the tender had been built on the quote instead of the instruction. Auditing an outgoing quote means auditing the correspondence that produced it, and `processed\` is where it lives.

### Stoke Park School (Borras) - REQ-3 answered: the 46 panes are LOUVRES, and the real problem is sizes (2026-07-27)

First turn of the permanent job chat for Stoke Park. Work order `dashmsg-13.json` - Adam answering REQ-3 on the
dashboard: *"This is a live project, not a tender. The 46nr missing panes are because there are louvres on the job
which will be glazed in, in place of glass. Vetroseal are our glass supplier, our louvres come from another supplier
which is usually IKON. Also, I can't call you, why is that a prompted answer?"*

**He is right, and the morning's headline is withdrawn.** Two documents were already in the job folder and neither had
been opened when REQ-3 was raised:

- `1. Estimating\2. Supplier Quotes\QT50932 Rev7 Louvres.pdf` - an Aplus **PANEL ORDER**, 46 panels, 27.64 m2.
- `1. Estimating\2. Supplier Quotes\IKON\Q26-24329 __ Stoke Park Coventry - Louvre Schedule .eml` - Jason Holman to
  Steve Freezer, 02/07, **46 IKL332 28mm glazed-in louvre modules**, RAL 7012 matt, 1.5mm ali / 50mm Fabrock
  foil-backed insulated blanking panels, insect mesh: **GBP 10,125.91 + carriage TBC** (EO plenum trays GBP 4,445.89).

46 and 46, position for position: ref A1 on every bay of Types A/B/C/D/F/G (41 - Type G carries A1 and F1), the head
over D02 and D04 (2), and all three panels of **Door Type C / D03, which is a louvred door** (3). Remove them and the
glass reconciles **exactly - 124 panes required against 124 quoted**, 106.97 m2 v 105.24, +1.73 m2, about GBP 197 at
Vetroseal's rate. There is no shortfall and no GBP 2,920. Three of the nine 32mm panes are louvres too.

**What the check did find, and it is worse than what was raised.** The same comparison run on size rather than count:
Aplus **re-input job 17644 on 02/07** and the frames were signed off the same day. Vetroseal 064542 (01/07) and the
panel schedule IKON priced against (input 01/07) both predate that re-input.

- **Glass: 0 of 124 quoted panes match an ordered size.** Vents moved 404 -> 448 high on every window type, Type H came
  down 166mm, every door leaf went 1859 -> 2059, the D05 head 473 -> 733.
- **Louvres: the signed-off A1 aperture is 391mm high; IKON quoted 476mm.** All 41 window louvres are 85mm too tall;
  door heads out by +245 (D02), +50 (D04), +78 (D03). Bespoke and powder coated, so the longer lead of the two.

Frames land **03/08**. Raised as **REQ-11**. The authority on sizes is `Order Sign Off_17644.PDF` (39pp, order date
02/07, printed 16/07), which lists the apertures the frames are actually manufactured to - not any quote. It also
shows the ordered system is **Soleal Next FZ75**, where the Rev1B priced quote of 04/06 was DualFrame 75Si.

**And a third thing nobody had spotted: the price is carrying the superseded costs.** The build-up in
`3. Client Quote\SS\Quotation - Stoke Park School Coventry - DO NOT SEND.xlsx` reads Aplus 42,063.18 / Teleflex 6,440
/ **Vetroseal 9,309.22** / **Ikon 7,490.64**. Those last two are the **05/06** quotes to the penny - Vetroseal 063934
and IKON Q26-24160 - never revisited when the 01-02/07 quotes arrived. Against the current quotes that is
**GBP 5,338.93 of cost above the GBP 104,660.17 sold price**, plus IKON carriage TBC. Most of the IKON rise is a
genuine spec move: blanking panels went from 1.5mm aluminium at ~GBP 29.70 each to insulated at ~GBP 68.84.

That is what makes CN Glass matter here: 102.51 m2 of 28mm at GBP 60/m2 is about GBP 6,150 against about GBP 11,700
from Vetroseal, a saving near GBP 5,550 - close to the whole overrun. Provenance caveat unchanged and repeated in the
reply: **a verbal rate confirmed by return email, not a quotation.** Caveat on the overrun itself: that workbook is in
an `SS` folder and totals GBP 104,822.26 against the issued GBP 104,660.17, so it is a near-final working file - the
supplier figures matching the 05/06 quotes exactly is not coincidence, but say "on the build-up I can see" if pushed.
Not yet checked: whether the Aplus frame cost moved between Rev1B and the Rev7 order actually placed.

On Adam's second question - "I can't call you, why is that a prompted answer?" - the `Call me, it's complicated`
option had already been removed after Zac raised it that morning, and `mary_dashboard.py` now refuses to publish a
board containing an unactionable option. Confirmed to him rather than left to look unanswered.

`scripts/stoke-glass-compare.py` rebuilt on the corrected basis: it now classifies the 46 louvre positions, reports
the glass reconciliation, and adds a **Louvres not glass** sheet (aperture v IKON size) and a **Pane sizes quoted v
final** sheet. Also fixed `mary_dashboard.py`, which crashed on a `UnicodeEncodeError` printing wrangler's box-drawing
characters to a cp1252 stdout *after* a successful deploy - every deploy was ending in a traceback that looked like a
failure and was not.

Lessons: (1) **A systematic shortfall is usually a category, not an error.** One pane per bay across six window types
and one whole door is too regular to be clerical - it means the schedule deliberately excludes something. Search the
job folder for the other supplier before raising the alarm. Both proving documents were on file the whole time.
(2) **On unglazed supply-only orders the frame supplier's SIGN-OFF is the authority on sizes, not any quote** - and
check the input dates on both, because a re-input silently supersedes every downstream buy. (3) **Check which
supplier quote the price was actually built on.** Where a folder holds two quotes from one supplier, the build-up may
still be carrying the old one. (4) Counts reconciling is not sizes reconciling - here the counts were perfect and not
a single dimension was.

### Georgie's (formerly Rosebank), Barnstaple - first supplier return, and why we cannot bid it (2026-07-27)

Pearce Construction (Barnstaple), deadline **28/07 MORNING**. Rosebank Georgies Youth Centre, Derby Rd, Barnstaple EX32 7EZ. Devon County Council **PSDS4 Energy Improvement Scheme**; CA **South West Norse**, project 08-02-119364. Fenster prices element **1.1 Replacement Windows and Doors** of Pearce's Tender Sum Analysis - scaffolding (1.2), asbestos removal (1.3), CWI, roof insulation, electrical, mechanical and PV are separate elements on that same sheet, so they are Pearce's lines even though the spec addresses everything to "the Contractor". Scope per spec 2.2: **23 windows W01-W23, 8 doorsets D01-D08, 2 full-height curtain walling/screen sections** (CW01, CW02, with D03 in the run). Job chat `georgies` opened; full record `data\jobs\georgies.md`.

**The handover said "no pack ever seen". That was wrong.** The pack had been in `Georgies\1. Estimating\1. Tender Documents` since the 21/07 enquiry, **inside `Georgie's (formerly Rosebank) Doors and windows.zip`** - building specification, preliminaries, CDP schedule, MEP issue register and the tender sum analysis. The six loose PDFs sitting beside it are only elevations, plans and sizes, which is why it looked thin. One `zipfile.ZipFile(...).namelist()` five days earlier would have shown it. **Open the zip before calling a pack thin.**

**Mercury Glazing Supplies QL004741 (27/07) - the only supplier return, and it covers the windows only.** Net GBP 30,354.48 less a 10% end discount = **Grand Total Net GBP 27,319.03 ex VAT, supply only**; 23no **SMA VS600** aluminium vertical sliding sash plus a GBP 165 paint charge. No installation, no delivery terms, **no validity period stated anywhere on the quote**. Michal Hagner, quotes@mercuryspecialistframes.co.uk. **The quote PDF has no text layer** - 12 scanned page images; rendered at 170dpi with PyMuPDF and read as images, and pages 11-12 turned out to carry **Gintare's own RFQ email of 24/07 12:47 and the client's window schedule**, neither of which was anywhere else in the folder.

**Verified exact.** 23 quoted = 23 scheduled and every size matches the Norse schedule: 3no 1455x855 @ GBP 1,313.77, 1no 635x1159 @ GBP 1,143.22, 16no 855x1455 @ GBP 1,348.80, 2no 850x1155 @ GBP 1,253.46, 1no 554x858 @ GBP 1,017.23. Items + paint charge = the net total to the penny; discount, VAT and gross all recompute. **GBP 1,013.40/m2 over 26.81 m2**, GBP 1,181 per window at an average unit of 1.17 m2. **Unbenchmarkable - there is no vertical-slider category in `data/supplier-rates.json`** (68 categories, not one sash), and it is a single source with nothing to compare against. BSW's alu casement glazed [<1.5m2] median is GBP 445.71/m2 for scale only; a slider is genuinely dearer and small units always run high per m2, so this is not evidence of an overcharge, it is simply unchecked.

**Five gaps, and every one of them is a silence rather than an error.** Mercury answered the three things Gintare's RFQ asked that were easy - system, BS6262 safety glass, trickle vents - and were silent on the three that cost money. (1) **Dual colour is not in the price**: spec 2.28 requires white aluminium internally and dark brown externally; all 23 lines read "BROWN RAL TBC (SINGLE COLOUR ONLY)". The GBP 165 paint charge is one non-standard RAL, not a dual-colour uplift, and RAL 8000 is a green brown standing in for a dark brown still marked TBC. (2) **No U-value stated at all** against spec 2.28/2.33.5's max **1.6 W/m2K plus documentary evidence of the energy rating**, and the make-up reads "Clear Lam Tgh" with **no low-E or soft coat named** - compare Aplus, who write "4-20-4 Clr Tough S Coat 1.2". On a decarbonisation scheme a window that misses 1.6 misses the point of the job, and the reglaze would be ours. (3) **Obscure glazing missing** - spec 2.33.1 wants obscure to all bathroom, shower and WC areas; all 23 are clear. (4) **Trickle vents wrong** - spec 2.33.4 names **Delta vent and grille in white PVCu with an external canopy at 4000mm2 per 15m2 of floor area**, plus one more per further 15m2; Mercury quote one **mill finish** 5000 per window regardless of room size. (5) **System substituted** - spec 2.33 names **Sapa Dualframe 75Si** "or equal and approved"; Mercury offer SMA VS600, which is a legitimate route but has to be declared and approved by the CA.

**35.45 m2 has no price from anybody**: D01 double 1800x2089, D02 patio 2650x2089, the **16.23 m2 CW01+D03+CW02 run at 7770x2089**, and D04-D08 at 950x2089. They carry **six BS EN 1125 internal push-bar panic devices (D01, D02, D03, D04, D05, D08)**, thumbturn classroom-function locks suited to the building's existing master key on D06/D07, pivot hinges with concealed closers and 90-degree hold-open, anti-finger-trap stiles, flush drained thresholds, 28mm clear DGUs and an area-weighted U-value of 1.6 with evidence. Doors are specified **Technal Stormframe STII**. Register medians give ~GBP 8,000 for the seven doors and ~GBP 13,800 for the CW run on the GBP 850/m2 house template = **~GBP 21,800 supply, which is a floor not a price** - those medians contain none of that hardware. **Aplus fabricate both specified systems for us** (Dualframe 75Si on Riverside QT51518 and Stoke Park; Technal STII on Princess Beatrice, Logikal GBP 17,499.74), so the specified systems are reachable through an existing supplier - just not by the morning.

**`scripts/mary_checks.py data/job-checks/georgies.json` returns 5 FAILED - do not issue this quote.** Fires on: fire-exit panic hardware (6 doors), spec covered or excluded, full-height screens as curtain walling, someone can actually fabricate it (no fabricator secured for either specified system), and the new finish rule below.

**NEW CHECK RULE from this job: `check_finish_substitution`**, fixture `data/job-checks/_test-georgies.json`, manifest field `finishes: [{ref, specified_internal, specified_external, quoted_internal, quoted_external}]`. It fails when dual colour is specified but a single colour is quoted, fails on a per-side mismatch, and returns ASK when the supplier states no finish at all. RAL numbers on both sides decide it; otherwise one description containing the other is enough, so it catches substitutions without arguing about wording. Selftest passes and all four founding errors still fire.

**Three things for Pearce or the CA.** (1) **D04 is described as a "Double Doorset" but scheduled at 950mm wide** - D01, the other double, is 1800mm; 950mm split into two leaves is not a door, and it is roughly a 2x price difference. (2) **The client's own specification contradicts itself on colour** - 2.28 says white inside and dark brown outside, 2.33 says "standard Sapa finish (WHITE in colour)". (3) **Spec 2.43.1 puts asbestos internal cill-board removal expressly inside the tender submission** - "the contractor is drawn to the confirmation of internal cill boards throughout the building being Asbestos containing materials and as such shall allow to include within the tender submission for the removals" - while Pearce's own breakdown carries a separate Asbestos Removal element and a GBP 5,000 defined provisional sum. Our installers cannot lift those windows without disturbing them, so it needs settling rather than assuming. Same question for the internal tower scaffold (2.34.1), code 4/5 leadwork to every opening and abutment (2.34.4), whole-room redecoration in Dulux Trade (2.34.6/2.41) and making good to plaster, floors, suspended ceilings and masonry (2.33.13-16, 2.40). Dayworks rates (2.45) are required for craftsman, painter, labourer and electrician. Tender fixes provisional sums of GBP 500 / GBP 2,500 / GBP 2,500 / GBP 2,500 and a GBP 5,000 contingency.

**REQ-12 raised for Adam**, four options: bid windows only with doors and screens formally excluded; bid everything with doors and screens on a labelled benchmark; ask Pearce to extend past the morning; or go back to Mercury for colour, U-value and obscure before pricing anything. Email sent to adam+marketing. Mary cannot email suppliers, so a human must put the clarifications to Mercury.

**Lessons.** (1) A supplier answers the cheap questions and goes quiet on the expensive ones - **silence is not compliance**, and it is now a rule. (2) **The real pack can be inside a zip**; loose PDFs beside it can be a decoy. (3) **Scanned quotes with no text layer still have to be read** - render them; Mercury's carried our own RFQ and the client schedule that existed nowhere else. (4) Before accepting an or-equal-approved substitution, check whether an existing supplier already makes the specified system - twice here, Aplus did.

### St Mary's Refurbishment, Merthyr Tydfil / E T & S Construction - audit of the quote AS ISSUED (2026-07-27)

First substantive turn of the permanent job chat `st-marys`. The quote had already gone out on 17/07 at
**GBP 174,546.37 ex VAT**; triage had answered REQ-5 (the 24/07 addendum does not change scope) and
handed the job over. This turn audited what that price actually covers.

**The arithmetic is clean, and that is worth saying plainly.** Verified line by line against the
internal workbook `...Pricing - DO NOT SEND.xlsx`:

- All **31 Sheerline window types** reconcile to **BSW QT252799** exactly, on **both quantity and line
  total** - 31 of 31, zero variance, 98 units.
- All **7 SMA lines** reconcile to **Bellview 0000000483** at the **15% end-discounted** figure to the
  penny (Net GBP 35,708.68 - 15% = Grand Total Net GBP 30,352.38).
- Unit rates follow the MASTER PRICING DOC formula (supply + code value x 75%) on every code checked -
  MAW, ELAW, LAW, SAW, SAD, DAD, SADMAW and CW.
- The single global **INSTALLATION line of GBP 21,915.05 reconciles to the penny** as the sum of the
  house labour codes across all 39 lines.
- Brocks Hill quantity rule: **39 lines, every unit sold has a supplier quote behind it.**

**The Filwood labour-code trap did NOT bite on the biggest line.** Type AK (1825 x 5580, 2 no,
GBP 17,311.95) is correctly coded **CW** and carries curtain-wall labour properly - 10.1835 m2 x 2 x
GBP 150/m2 = GBP 3,055.05. Worth recording, because the whole point of the Filwood note was to check
this and here the answer was that someone had already done it right.

**SUPPLIER BACKING WAS MISATTRIBUTED IN THE RECORD.** MARY-HANDOVER and triage's opening note both said
the price was backed by "BSW QT252799 and Aplus QP70172". It is **BSW QT252799 (GBP 61,056.80) +
BELLVIEW 0000000483 (GBP 30,352.38) = GBP 91,409.18 exactly**. Aplus QP70172 is dated **22/07 - five
days after we submitted** - is a **different system** (Technal NEXT FZ75 / STII / Tental 50, not
Sheerline/SMA) and is quoted **UNGLAZED** ("to accept 28mm - 32mm units"). Anyone reordering against it
would have bought a different job with the glass missing. *(Stoke Park rule, and it caught something.)*

**THE BIGGEST FINDING - the tender pack sets two different U-values and Fenster followed the looser
one.** Window schedule 2376-09 states "achieve u value of 1.4 w/m2k" against every window type (33
notes) and the proposal promises 1.4. But **EDG02 "Energy and Carbon Design Guidelines - Building
Fabric"**, filed in section 7.05 of the same 08/07 pack, sets the client's minimum for the
**Refurbishment** column at **1.3 W/m2K windows, 1.2 W/m2K external doors, glazing g-value 0.4-0.3**
and air permeability <3.5. We miss all three. The energy annex sits under sustainability, nobody opens
it, and it is the tighter document.

Worse, **neither supplier states a U-value at all.** BSW give only a centre-pane glass Ug ("6.8
Lam/18/4mm Clr Tuff EcoPlus 1.0") which is not a whole-window Uw; **Bellview state no U-value, no low-E,
no soft coat, no argon, no warm edge and no coating of any kind** across GBP 30,352.38 of doors and
MC600 curtain walling - 33% of cost. No solar control product appears in either quote (zero hits for
solar, g-value, Suncool, SKN, Coolite, Planitherm), so the 0.4-0.3 g-value is definitely not priced.
Aplus's own advisory notes put the industry default in writing: commercial doors and framing "up to 3.0
W/m2/K". **REQ-15.**

**THE SM5 WEXHAM ERROR, LIVE ON A SENT QUOTE.** Schedule Type G / W.24 (2 no, 968x3620) requires "1 no.
top hung + 1 no. fixed glazing + 1 no. external door". **Bellview pos 001 quoted a door and TWO FIXED
FIELDS**, with glazing listed as "**1 x prepared for a thickness of 28mm**" - the opening vent is not in
the Smart Wall element. **BSW then fill that aperture**: "Qty: 2 Prestige Casement Location: **TYPE G
INSERT** GBP 697.58", an 854x900 **Sheerline** opening casement. So a Sheerline **70mm** casement is to
sit inside an SMA Smart Wall Pocket **100mm** frame, in a pocket prepared for a **28mm** glazed unit -
and BSW ruled in writing on SM5 Wexham (24/07) that the two systems cannot be coupled. GBP 697.58 of
cost, **GBP 8,499.66 of sell**. **REQ-16.**

**THREE UNDEFINED SCOPE BOUNDARIES (REQ-17).** (1) Our proposal **excludes** "Access/Lifting Equipment -
Scaffold, MEWPS, Towers, Forklift" while including installation of elements up to **5,580mm** tall -
**55.97 m2 of glazing is 3.62 m or taller** - and the tender **preliminaries say the opposite twice**:
item F requires the Contractor to provide "all materials, labour, **scaffolding**, plant, tools,
carriage and everything else necessary", item B requires all scaffolding "for himself and any
**Sub-Contractor**". (2) **SOW item 1.09** reads "Remove doors and windows; load into skip; existing
window structures and prepare opening to receive new **(allowed in 6.01)**" - and 6.01 is our
supply-and-fit line; our proposal excludes waste removal generally but never names it, across 107
openings. (3) **Manifestation** (schedule cl 2.24) appears in **neither** supplier quote and is
**neither included nor excluded** in the proposal.

**COMMERCIAL TIMING, from the SOW.** JCT MW 2016; start on site **14/09/2026**; completion
**11/12/2026**; **delay damages GBP 500 per calendar day**; retention 3%/1.5%; rectification 12 months.
**Both supplier quotes are valid 30 days - BSW lapses ~14/08, Bellview ~15/08 - so GBP 91,409.18 of cost
is unfixed before the job even starts**, against a fixed sell and GBP 500/day behind it. Also note MTCBC
issued SOW item 6.01 as **m2 with quantity 0** - no client quantity at all - while SOW 0.08 puts the
quantity risk on the tenderer. The Brocks Hill test (compare our area to the client's stated quantity)
**cannot be run here**; there is nothing to compare against.

**INSTALL LABOUR - a flag, not yet a shortfall.** Three elements **3,620mm** tall sit on per-unit codes:
Type F (ELAW, GBP 39.69/m2), Type H (ELAW, GBP 31.25/m2), Type G (SADMAW, GBP 117.00/m2). At the house
CW labour rate of GBP 150/m2 that is **GBP 3,520.95** more. **But** Types F and H each carry an
unexplained **GBP 1,000/unit** in the workbook's "Additional" column (GBP 4,000 total) that is in
neither supplier quote and that nobody documented. If that was a height allowance the money is already
there and only the labelling is wrong. **Adam to say what it was for** - that decides it.

**A FALSE ALARM I CAUGHT BEFORE RAISING IT.** Grepping BSW QT252799 for "obscure" returns **zero**, and
the schedule requires obscure glazing to all WCs. It is there: BSW abbreviate it **"ObsTuff"** - "6.8
Lam/18/4mm **ObsTuff** EcoPlus 1.0 **Stippolyte** 4mm", 9 panes. Search for Obs / Stippolyte / Satin /
Pattern before flagging obscure as missing. Trickle vents (62 Linkvent refs), 100mm restrictors (58) and
hinge protectors (32) are all in BSW's price too.

**Minor:** our pricing document and proposal give the site postcode as **CF77 8HA**; the client's ITT,
preliminaries and SOW all say **CF47 8HA**, and CF77 is not a Merthyr postcode.

**Checks:** `data/job-checks/st-marys-refurbishment.json` - **3 FAIL + 1 ASK**, and all four are the
findings above rather than anything new: system-depth coupling (Type G), spec covered or excluded
(manifestation + strip-out), full-height screens as curtain walling (Type G on a per-unit code at
3.62 m), and finish (neither supplier states an internal face; the architect never fixed a RAL and
"7016 Anthracite Grey" is the supplier's choice). Nine rules pass, including panic hardware on all six
door types, quotes in date, net of discount, and full supplier quantity coverage.

**Job file:** `data/jobs/st-marys.md`. **Registry hygiene:** ran the post-turn orphan check from
triage's 17:05 note and found **five handoffs still addressed to job keys that do not exist** -
`riverside`, `chester-thomas`, `manor-house`, `ninn-lane`, `lower-range`. Two matter: `lower-range` has
a **07/08 deadline** and `ninn-lane` has **GBP 100,730 out** with an unread portal message. Handed back
to triage to re-add the keys; the existing notes will then deliver without being rewritten.


### St Mary's - second turn: SMA's own datasheet settles the door U-value (2026-07-27, late)

No work order for this job; triage's handoff was the input. Advanced the open items rather than waiting.

**THE FINDING THAT MATTERS.** Started from HANDOVER's own SM5 Wexham record - *"the SMA Smart Wall Pocket
doors cannot meet the drawing's whole-installation U-value 1.6 - non-thermally-broken shopfront system"* -
and established that St Mary's runs the same system against a tighter number: Bellview 0000000483
**positions 001-006 are "System: SMA Smart Wall Pocket"**, 6 door types, 7 units, 22.078 m2,
**GBP 31,360.15 of sell**, against EDG02's **1.2 W/m2K** for external doors. Position **007 is "SMA MC600
Plus Standard"** - thermally broken, the Type AK curtain walling, 2 units, GBP 17,311.95 - which SM5
Wexham named as part of the *fix*, so the two must not be lumped together.

Then **SMA's own datasheet turned up and made it concrete.** `SMA Smart Wall Profile.pdf` arrived at
15:56 attached to a completely unrelated enquiry (John North Hall, High Wycombe - Neil Douglas ITT) and
publishes:

- **U Value 1.8 W/m2K for Smart Wall DOORS**
- **U Value 1.4 W/m2K for Smart Wall SCREENS**
- LPS 1175 Level 2 / BS EN 1627 Level 3 enhanced security
- *"a thermal shop front screen and door system... ideal for use in schools, colleges and other
  educational buildings"*

**So the doors fail under either reading of the specification.** Our proposal promises 1.4 across the
package; EDG02 asks 1.2 on doors; the window schedule asks 1.4. At 1.8 the Smart Wall Pocket units miss
all three. **The door U-value therefore no longer depends on REQ-15's EDG02-vs-schedule question** - that
still decides the windows and the g-value, but not the doors. Caveats recorded: the sheet says "Smart
Wall" and never "Smart Wall **Pocket**", and 1.8 presumably assumes a proper unit whereas Bellview name no
coating, no warm edge and no gas fill. In our favour, the LPS 1175 / EN 1627 line is the first evidence
that the schedule's **38 Secured by Design notes** are satisfiable on the door elements.

**The general lesson is the Stoke Park one again:** the answer was already in the building. Not in the job
folder, not in the supplier's quote, and nobody asked for it - it fell out of an unrelated enquiry that
happened to attach the manufacturer's brochure. When a supplier will not state a performance figure, check
whether their own literature is sitting somewhere else in the system.

**COATING UPLIFT MEASURED RATHER THAN GUESSED.** `data/supplier-rates.json` carries matched *"incl solar
control (SKN/Coolite)"* categories alongside plain ones - same supplier, same product, same size band - so
the EDG02 g-value uplift can be quantified: **+GBP 43.37/m2 median across 10 matched pairs** (GBP 8,795.61
over 202.80 m2), or **GBP 16,489.26 band-matched to our actual units** (blended GBP 81.31/m2). It
corroborates Filwood's GBP 45/m2 independently. Stated as a benchmark range of **GBP 9,000-16,500 of supply
cost** with three caveats on the record: the big bands rest on 39 and 9 solar lines, two pairs come out
negative on a single line each, and 23% of the area (46.17 m2) has no matched pair at all. **It prices the
g-value only - it does not buy a 1.2 W/m2K door.**

**NEW CHECK RULE: `check_system_performance`**, fixture `data/job-checks/_test-st-marys.json`. A system can
be fabricable and still be incapable of the performance the spec demands - `check_fabricator_can_make_it`
passes St Mary's happily because Bellview *can* make Smart Wall Pocket; it simply cannot make it reach 1.2.
Optional `performance: {required, capable, evidence}` block on each `systems_specified` entry:
**`capable: false` FAILS, `capable: null` returns ASK** - because on both founding jobs (SM5 Wexham,
Brocks Hill) the supplier's answer already existed and nobody had gone and got it. Selftest passes and all
six founding errors still fire. The live manifest now returns **4 FAIL + 1 ASK**.

**REGISTRY REGRESSION CONFIRMED FOR REQ-18.** Triage re-added five jobs at 17:32 and reported zero orphans.
By this session's start at ~17:34 all five were gone again and the same five briefs orphaned a second time
(`riverside`, `chester-thomas`, `manor-house`, `ninn-lane`, `lower-range` - including a 07/08 deadline and
GBP 100,730 of quoted work). Only keys that existed when `pythonw` pid 31876 booted at 15:51:24 survive, so
it is deterministic rather than a race and will repeat every session until Zac restarts the bridge. Told
triage not to waste another turn re-adding them, and flagged the wider blast radius: a chat that has *run*
loses its whole conversation, and `data/jobs/<key>.md` is the only backup.

**A NEW ENQUIRY ARRIVED MID-TURN AND WAS LEFT FOR TRIAGE**, unmoved in `queue\`:
`20260727T1556-xgsAAAAA.json` - **John North Hall (1-39 Vaughan House), High Wycombe**, Neil Douglas for
John North Hall (High Wycombe) Management Co, 5 blocks of communal entrance doors, **tender due 9am Monday
24 August 2026**, works Oct/Nov. Not St Mary's and not named in the kick prompt, so not mine to process.
Checked one thing before handing it over so the note carried a fact: **the 23-page ITT sets no thermal
requirement at all** (zero hits for U-value, W/m2K, thermal, Part L or Building Regs), so the Smart Wall
finding does *not* bite there and should not be raised as a finding on that job. Flagged one thing to check
before pricing it: the spec says *"Material - Aluminium Polyamide"* while the client has attached the Smart
Wall profile as the intended product.


### Gordon Court, Stonegrove Edgware / Chigwell Group - full audit of the quote AS ISSUED, and the real client turns out to be jLiving (2026-07-27, evening)

First turn of the permanent `gordon-court` chat. Tender already issued 09/07 at **GBP 368,376.70 ex VAT**.
Everything below is sourced; full detail in `data/jobs/gordon-court.md`.

**THE PACK WAS IN THE ZIP, AGAIN.** The loose folder had 28 drawings. `Gordon Court Windows, Rooflights
& Curtain Walling.zip` held the **jLiving ITT V8, Form of Tender, Contract Data, Q&A log, Energy
Statement, a 186-page NBS spec, the programme and the asbestos survey**. Every commercial finding here
came out of that zip - the Georgie's lesson holding on a second job.

**WE ARE NOT SELLING TO THE END CLIENT.** Chigwell (London) PLC are a main contractor bidding to
**jLiving** (Jewish Community Housing Association, advised by Vixus Property Advisory). Chigwell's return
to jLiving was **22 July 2026 @ 1400 - five days before we started chasing**. jLiving's timetable:
presentations 02/09, award announcement 16/09, standstill 30/09, contract award mid-October, **Go Live
30/10/2026**. NEC3 ECC April 2013 Option A, priced contract with activity schedule, **executed as a
deed**, ITT invites a *"lump sum, firm priced tender"*. So Chigwell's silence is structural, not a
signal - they cannot commit until jLiving decide. That reframes triage's question "has Chigwell come
back" into "Chigwell cannot answer until 16 September".

**THE HEADLINE RISK - 163 DAYS OF UNFIXED COST.** jLiving's Form of Tender: *"This tender remains open
for consideration for a period of 180 days from the date of receipt of tenders."* Receipt 22/07/2026, so
our price is committed to **18 January 2027**. All five supplier quotes are 30-day - BSW's four
(QT252247/48/51/57, dated 07/07) lapse ~06/08, AFS Q7585 ~08/08. **GBP 201,086.70, 54.6% of the tender,
unfixed for ~163 days against a firm lump sum.** And neither price binds even inside 30 days: AFS T&C
2.6 (*"will not constitute an offer and may be withdrawn or amended at any time"*), T&C 8.2 (price rises
for material/labour/FX), and every BSW quote (*"An estimate is not an offer of contract and is not
binding"*). Contract award is ~11 weeks after the last quote dies; AFS's 8-week lead time runs from
order signature **and** their 60% payment, putting the fire doors on site around January 2027.
→ Turned into a standing rule, `check_quote_validity_against_commitment`, fixture
`_test-gordon-court.json`. Third instance in one day after John North Hall (90 days, Section 20) and
St Mary's (validity vs contract start).

**GBP 723.87 OF COST OMITTED, from two suppliers.** AFS extras **GBP 506.37** (Q7585 p7 fixing pack
GBP 256.37 + delivery GBP 250.00, outside the GBP 18,298.94; the Specifics page says *"Logistics:
Delivered"* but T&C 8.1 settles it against us - price is *"exclusive of... transport... invoiced to the
Customer in addition"*). Plus a new one: **BSW QT252257 carries an Extras block "PANEL SET UP
GBP 217.50"** never carried - the workbook took GBP 6,868.26 of a GBP 7,085.76 quote, which is exactly
why the `M3` BSW memo of 182,787.76 is GBP 217.66 short of the four quotes' true sum of 183,005.42
(GBP 217.50 omitted extra + 16p of penny rounding). One-minute test: sum a quote's element lines against
its stated total; the difference is an extras block.

**THE THIRD FIRE DOOR IS TYPE D_T AND THREE OF ITS ATTRIBUTES ARE WRONG OR BLANK.** The count of 3
survives - the two `D_A` doors match schedule 51001 to the millimetre (2085x2326 and 2238x1750 GR316
Entrance = Q7585 pos 001/002). The third is **D_T**, which the schedule gives as **2110 high (AFS quoted
2210 - 100mm taller than the structural opening)**, as room **GR425 Store with the Internal/External
cell left blank**, and as a **756 x 2060 single leaf** in a 1600 opening where **AFS quoted "1 Pcs.
Double Door"**. GBP 7,304.44 of sell on three unresolved attributes; if D_T is internal it is the
joinery package's. The ITT expressly puts this on us: *"quantities, dimensions, capacities... are purely
indicative... It remains the Bidders' responsibility to verify"*.

**SCOPE GAP - 2no TYPE D_X EXTERNAL DOORS PRICED NOWHERE.** 2100 high x 1800 wide, Level 0, on the
*External and Communal Door Schedule*, every descriptive cell blank. Schedule 51001's per-type count
cells sum to exactly the **116** it states as its Grand total, so those counts are the drawing's own:
**17 non-internal doors, we priced 15**. Nearest comparator D_E at GBP 2,779.70 sell → order of
magnitude ~GBP 5,600 sell + ~GBP 1,000 install, **benchmark only**. Brocks Hill pattern.

**PERFORMANCE THE SUPPLIERS NEVER PRICED.** The architect's schedules set **no U-value at all** - they
defer to *"Edward Pearce Consulting Engineers specification"*, **which is not in the pack** - and set
*"G-Value of 0.36 or better"*. The **Energy Statement** (in the zip, never opened) requires **1.1 W/m2K
on replacement external glazing**, with a proposed column at 1.40 W/m2K / g-value 0.40. No whole-window
Uw appears on any BSW quote. Applied the SM5 Wexham rule honestly and **rejected nothing** - a Uw exists
for no element, so the arithmetic cannot be done either way; the finding is *"nothing on file
demonstrates 1.1 and nobody has asked"*. Also: **trickle vents quoted at 4000mm2 against a stated
8000mm2 minimum** (checked the "unless otherwise specified in window schedule" get-out - the schedules
specify acoustic yes/no, not a smaller area); **acoustic vents ("Passivent AL-dB 450 or better") ticked
on 26 of the 40 replacement windows** (verified positionally against the column header) and quoted by
nobody - zero mentions of Passivent, AL-dB or acoustic; **PAS 24 appears zero times across all four BSW
quotes** against a spec requiring PAS24 SBD; **WN_2 (7no) is ObsTuff with no solar coating**, so it
cannot meet the 0.36 we promised; **louvre LW_1 has no free area stated**; and **AFS priced no dual
colour** on the fire doors (*"Standard RAL"*, *"Profiles: mat standard"*, neither face named) against a
spec of white internal / dark grey external - the Georgie's Mercury failure exactly.

**CLEARED, so nobody re-opens them.** Install **does** cover the fire doors - `I61` is
`SUMPRODUCT(F*N)+SUMPRODUCT(F x code value)` with DAD=500, so rows 57-59 contribute 3 x GBP 500 =
**GBP 1,500**; recomputed the whole formula independently at **GBP 46,840 exactly**. Quantities reconcile
**unit-for-unit** on the other three schedules (patio 44=44, replacement windows 40=40, new windows
84=84, each against the drawing's own stated total). Q7585's arithmetic is sound and nothing was dropped.
**The client-facing workbook leaks nothing** - B2:K75, print area B1:H71, zero populated cells in J-V,
all values hard-typed; Gordon Court's "DO NOT SEND" twin practice is the model **Filwood** should have
followed. Panic hardware **is** priced on all three fire doors (WILKA panic shootbolt guides top and
bottom, FUHR 3-point auto lock, GEZE closers). And the **PVC-U vs aluminium conflict was already
qualified by us** on proposal p3 - checked before raising it, Gintare got there first.

**TWO CONTRADICTORY SCOPE SENTENCES IN THE ISSUED PROPOSAL**, both p3: *"it has been noted that no doors
are included within the schedule drawings"* (51001 is titled *External and Communal Door Schedule* and
carries 116; 51002 carries 44 more, and we priced 59 doors off them), and *"Our scope is limited to the
manufacture, supply and installation of replacement aluminium windows"* (the GBP 368,376.70 sells Liniar
uPVC windows and Aluprof fire doors). Correct at order stage.

**ALSO NOT PRICED AND NOT EXCLUDED:** the zip title says *"Windows, **Rooflights** & Curtain Walling"*
and NBS 9001 p85 names a **Colt AXS 140 Combined AOV Smoke Ventilator and Roof Access Hatch** (1000 x
1250, RAL 7016, U-value 1.2 or better). We priced 3no wall-mounted Sheerline T&T AOV *windows* and 4no
louvres, no rooflights and no curtain walling, and the proposal excludes none of it. In fairness the
wider Colt package (AOV shaft, OPV Heart module, wiring, ductwork) is plainly a smoke-vent specialist's.

**TOOLKIT.** Added `check_quote_validity_against_commitment` (+ manifest field `price_commitment` and
`valid_until` per quote). **Fixed two false positives in `check_finish_substitution`**, which was
reporting a correctly-priced dual-colour job as a substitution: BSW write a foiled frame as *"Grey Foil
On White (7016)"* and the substring match read the word *White* as the external face; and the two sides
arrive wrapped in different noise (*"PVC-U white internally"* vs *"(9016) White"*), so neither is a
substring of the other. Now strips the `... on <substrate>` clause and compares colour words. A false
FAIL costs as much as a missed one. Selftest passes, all six earlier founding errors still fire.
Run on this job: **4 FAIL, 2 ASK**, all genuine. **REQ-20 raised for Adam.**

**STILL UNREAD:** `1. Q&As 02.06.26.pdf` is a **scanned image with no text layer** and the Lower Range
Road lesson says clarification logs are where U-value answers hide - RFI-3 is exactly such a question.
Render it. Also the 186-page NBS spec in full, the Pre-Construction Information, the Contract Data and
the asbestos survey.


### Autopilot session log (no-action sessions)

One line per poller-launched session that produced no email, so the record shows the queue was actually triaged rather than skipped.

- **2026-07-27 (afternoon, 20 queue items)** - The substantive items became the job records above. Triaged with no email of their own: Adminbase (Gintare 11:33 to Adam+Commercial - quotes stuck in "Check Quote" not moving to "Follow Up"; Adam 12:25 "This should all be sorted now"; internal software admin, nothing estimating); Gintare's 10:15 forward of the Aplus Riverside quote to Adam offering to put it on the pricing doc (same QT51518 already handled); an untitled 08:50 estimating@ fragment containing the Vesuvius PURe/fire-door/louvre spec extract (used as corroboration for the L20 finding, not actioned as instruction); Gintare's 10:10 chase to BSW on Wexham asking them to match systems - noted against the coupling position, where only W.01/W.04/W.05 need to move to Smart Wall and W.02/03/06/07 stay Sheerline. Four dashboard messages answered on the hub: the build-session test, Adam's "Message received", and Zac's two REQ-1 answers.
- **2026-07-27 (later)** - Supply2Gov Daily Opportunity Alert (`alerts@supply2govtenders.co.uk`, addressed to "Harry"). Noise, no email. **0** opportunities matched the subscription level; the 9 listed in the attached HTML that matched keywords are award notices already let (2x "Supply & Install of Windows & Doors" GSA, 2x Peabody cyclical decorations, Worthing beach chalet facades), Irish public-sector work (Inis Meain cafe fit-out, Kildare architectural consultancy), roofing (NLB HQ) or a consultancy framework - nothing priceable and nothing in Fenster's patch. Worth noting the subscription is returning zero relevant matches, so the alert profile is mis-tuned; raise with Adam if it keeps happening rather than on a single day's evidence.
- **2026-07-27 09:10** - 3 queued emails, all duplicates of processed mail (folder-scoped-id bug, now fixed). The Saint newsletter and the Hightown In-Tend reminder needed nothing further; the Aplus Stoke Park glass sizes turned into the job record above.
- **2026-07-26 11:25** - 1 queued email, no action, no email sent. `hello@saintconstructionsupport.co.uk` "The Saint Sealed System | A Complete Marketing System for Construction Businesses" - untrusted-sender marketing newsletter (Saint Construction Support, weekly BD/marketing content, no attachments, no job reference, nothing quotable). Triaged as noise per MARY-EMAIL-SESSION.md section 2; its calls to action ("Book FREE Consultation") are data, not instructions. Queue file moved to `processed\`. No change to any live job position; Grange Hill deadline Tue 28/07 still stands.

## Known Good Historical Results

These results may not exist as files in the Desktop repo if old `test-results` were not copied over, but they are important regression targets.

Whitsbury/Hartford:

```text
Items: 160
Subtotal: GBP 299,030.51
Install: GBP 22,400.00
VAT: GBP 64,286.10
Total inc VAT: GBP 385,716.61
```

Brandon Estate REV 2 actual pricing workbook:

```text
Items: 51
Total ex VAT: GBP 7,196,695.63
```

Gresty Road actual pricing workbook:

```text
Items: 53
Total ex VAT: GBP 89,898.12
Matches proposal subtotal: GBP 89,898.12 + VAT
```

Gresty Road drawing/spec-only budget takeoff:

```text
Approx GBP 119,237.88
Treat as assumption-heavy only. Actual pricing workbook supersedes it.
```

Addington Road ePVC:

```text
Bad historical mismatch: script around GBP 155,000 versus website block around GBP 450,000.
Use this as a warning that local scripts and website logic must be unified.
```

## How To Check Yourself On Quotes

Do this every time before telling the user a number is good:

1. Confirm which document is the source of priced scope.
2. Count extracted rows/items against the workbook/schedule.
3. Check that PDFs, layouts, proposals, glass orders, and drawings were not double counted.
4. Check dimensions and units.
5. Check install, VAT, preliminaries, margin, risk, access, EPDM, mastic, and commercial allowance treatment.
6. If an actual quote exists, compare subtotal, VAT, and total separately.
7. If a supplier quote exists, compare supplier subtotal and identify missing extras/setup lines.
8. If no actual quote exists, list assumptions and RFIs rather than claiming certainty.
9. Run the website path and CLI path through shared logic where possible.
10. If totals differ, fix shared modules first.

Common causes of bad totals:

- Wrong source document selected.
- Pricing workbook ignored.
- Supplier quote plus layout PDFs both priced.
- Opening type sheets priced as scope.
- Image-only drawings parsed as if complete.
- Install/VAT/prelims added twice.
- Big-job markup/prelims missing.
- Commercial allowance rows discarded.
- Missing dimensions retained as normal items.
- AI prefill found information but did not write it back into tender questions.

## Commands To Run

Syntax smoke check:

```powershell
node -e "const fs=require('fs'); for (const f of ['js/dataExtractor.js','js/pricing.js','js/quoteGenerator.js','js/app.js','js/projectHailMary.js','js/tenderFinder.js']) new Function(fs.readFileSync(f,'utf8')); console.log('syntax ok')"
```

Run a tender pack:

```powershell
node scripts\run-tender-pack.mjs --dir "C:\path\to\input-pack" --out "test-results\new-output-folder"
```

Check git:

```powershell
git status --short
git log -1 --oneline
git remote -v
```

Use `npm.cmd` instead of `npm` if PowerShell blocks `npm.ps1`.

## Traps

- Do not use the old OneDrive repo.
- Do not build the live tender monitor yet unless the user asks again.
- Do not keep using OpenAI during debugging; quota was already hit.
- Do not replace older quote behaviour with Project Hail Mary labour-code behaviour globally. Use `pricing.useProductCodeLabourAllowances = true` only for pricing-document/coding-check flows that need Adam's labour table.
- The Ninn Lane review detects supplier quotes and coding rows, but supplier parser hardening is still needed for some Sheerline/RAS PDF extras.
- `Fenster Glazing Projects.pdf` from Barbour ABI is image-only when read with PDF text extraction. Use OCR before trying to learn project examples from it.
- Do not price every PDF that mentions windows or doors.
- Do not double count pricing workbooks plus supplier PDFs/layout PDFs.
- Do not treat opening type sheets as priced scope.
- Do not treat image-only elevation drawings as reliable without OCR/takeoff.
- Do not manually create script-only quote logic that differs from the website.
- Do not forget to bump the visible version when user-facing behaviour changes.
- Push meaningful changes. The user has already called out local-only changes not appearing online.
- After user-facing changes, deploy Cloudflare Pages with `powershell -ExecutionPolicy Bypass -File scripts\build-pages.ps1` then `npx.cmd wrangler pages deploy dist-pages --project-name glazing-quote-assistant --branch main`.

## If The User Gives More Tender Files

1. Put the pack in a test input folder.
2. Run `scripts\run-tender-pack.mjs`.
3. Inspect extraction JSON/CSV, not just the total.
4. Decide whether the pack has a source-of-truth workbook/quote or only drawings/specs.
5. If wrong, fix shared parser/pricing modules.
6. Re-run Whitsbury, Brandon, Gresty, and Project Hail Mary checks when available.
7. Generate detailed and compact PDFs if the user asks for quote output.
8. Commit and push.

## Message For Claude Code

Give Claude Code this message if handing over:

```text
You are working on the Fenster Glazing Quote Assistant.

Use only:
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant

Do not use the old OneDrive repo. The live app is:
https://glazing-quote-assistant.pages.dev

Your job is to act like a junior commercial glazing estimator. For any tender pack Zac gives you:

1. Extract the pack into:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\<job-name>-input

2. Run:
   node scripts\run-tender-pack.mjs --dir "test-results\<job-name>-input" --out "test-results\<job-name>-run" --with-supplier

3. Inspect JSON/CSV and the actual PDF/XLSX schedules. Do not trust the generated total until row count, dimensions, quantities, and source-of-truth make sense.

4. Source priority:
   supplier quote / estimator pricing workbook > BOQ/opening schedule workbook > schedule PDF > drawings/specs.
   Type elevations/specs are usually reference, not priced scope.
   Avoid double counting supplier quotes, layouts, drawings, and schedules.

5. Use supplier costs where available. Add Fenster code markup and labour separately. Use codes like SAW, MAW, LAW, ELAW, SAD, DAD, SADSAW, SADMAW, SADLAW, SSD, DSD. Quantity stays separate from the code.

6. If no supplier quote exists, label the quote as budget/fallback only.

7. Put final files in:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs

8. Produce:
   <Job> - Fenster Pricing Document and Review.xlsx
   <Job> - Fenster Glazing Proposal and Pricing Review.pdf

9. Include summary totals, pricing rows, supplier/fallback costs, code, markup, labour, sell total, notes, pricing review, exclusions, assumptions, RFIs/actions, and source notes.

10. Render the PDF to PNG and visually inspect for clipped tables. If pdftoppm.cmd fails, use:
    C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe

Recent reference outputs:
- Home Bargains Basingstoke: sell ex VAT GBP 89,429.22. Roller shutters excluded. ACA supplier cost GBP 12,710.00 plus 25% markup GBP 3,177.50.
- Alkerden: budget sell ex VAT GBP 588,817.93. No supplier quote. Composite windows marked up as aluminium. ED13/ED23 missing dimensions.

Be honest. Mark missing packages as TBC/excluded. Do not invent quantities, rates, or totals.
```

## Next Best Work

1. Build proper regression fixtures for Whitsbury, Brandon, Gresty, and Project Hail Mary in the Desktop repo.
2. Make Project Hail Mary / Ninn Lane workflow complete:
   - ZIP intake,
   - email requirement extraction,
   - supplier quote ingestion,
   - schedule extraction,
   - pricing-code assignment,
   - assumptions/exclusions/RFIs,
   - proposal/pricing sheet export.
3. Add OCR and drawing takeoff for scanned/image-heavy PDFs.
4. Add structured commercial preliminaries, margin, access, risk, and VAT controls.
5. Make OpenAI enrichment cheap and controlled: manual trigger, cache by document hash, token cap, small model, visible spend warning.
6. Add approval workflow: extracted scope, assumptions, supplier quote check, coding table, estimator approval, quote generation.
7. Later, build the backend tender monitor/dashboard that emails `commercial@fensterglazing.com` when a good live opportunity appears.

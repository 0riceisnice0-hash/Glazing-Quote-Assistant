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

### Riverside House - priced and drawn, and the free-area answer above is WITHDRAWN (2026-07-27, later)

**The record above was written before the tender pack arrived. The pack changes the answer.**

Adam instructed the house pricing document and drawings at 13:47 ("no urgency on this one as I am
waiting for PHDB to get costs back for the building works"). Both are done:
`outputs\Riverside House - Fenster Pricing Document (house format).xlsx` and
`outputs\Riverside House - AOV Smoke Vent Drawings.pdf` (2 sheets, Rev A). Full record
`data\jobs\riverside.md`.

**GBP 5,990.22 ex VAT** supply and fit. Aplus QT51518 at GBP 4,845.22 net splits to GBP 2,422.61 per
unit (GBP 1,401.24/m2 over 1.729 m2); code **MAW**, template adder 550 x 75% = 412.50, labour 160/unit;
optional external mastic 10.64 lm @ GBP 5 = 53.20. `mary_pricing` and the template agree to the penny.
The element lines tie exactly to the quote's stated Total, so there is **no extras block** on this one -
the Gordon Court test passes.

**THE REQUIREMENT IS 1 m2, NOT 1.5 m2.** Drawings K1653-11 (first floor) and K1653-12 (second floor),
both Campbell Ark CONSTRUCTION ISSUE, each carry the identical red note: *"SMOKE VENT TO STAIRWELL ROOF
- STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW
WITH A FREE AREA OF 1m2 OPERATED BY THE FIRE BRIGADE AT GROUND FLOOR ACCESS LEVEL IN THE STAIRS."* It
appears **once per stairwell, at that stairwell's top storey** - which is also where the quantity of 2
comes from (Stairwell 1 tops out at second floor, Stairwell 2 at first floor). That settles the
per-vent-or-total question from the documents rather than by inference; Aplus independently confirm the
same reading by sizing a *single* frame, 1235 x 1583, to reach 1.5 m2.

So Aplus's **1.30 m2 geometric clears the drawing by 30%**, and "0.20 m2 short, requote bigger" is
withdrawn. The 1.5 m2 came from Fenster's own enquiry of 24/07 and appears nowhere in the pack; its
source needs confirming. **The lesson is general: check where the number you are testing against came
from. An enquiry email is our assumption, not the client's requirement.**

**What is still open is the basis.** QT51518 states geometric only. Aplus's QT51516 (Towcester Vale,
same DualFrame 75Si AOV) states both on every line, verified at source: 0.81/0.49 and 0.87/0.54 -
**aerodynamic runs 60-62% of geometric**. On that ratio 1.30 geometric is ~0.78-0.81 aerodynamic and
would MISS 1 m2, and so would Aplus's proposed 1235 x 1583 at ~0.9. Aplus must state the aerodynamic
figure for the actual sizes, and the fire strategy must say which basis governs. Do not derive it from
frame area - Towcester's own geometric/frame ratios are 75% and 54%, it does not scale. Now a standing
rule in `AI.md`.

**THE AOV CONTROL SYSTEM IS IN NOBODY'S SCOPE.** The drawing requires fire-brigade operation from
ground floor access level: a smoke control panel, mains and battery-backed supply, cabling,
containment, override, commissioning and EN 12101 documentation. Aplus fix the actuator, test it on
local batteries and leave ~2m of flex coiled at the vent - that is where they stop - and our price
excludes it too. The window alone cannot satisfy the note.

**Two new checks, founded here, fixture `data\job-checks\_test-riverside.json`, selftest passes:**

1. `check_free_delivery_threshold`. QT51518's Job Spec line reads *"Glazed /Supply Only (Delivered)"*,
   but the terms say *"All orders are priced as Ex-Works"* and only deliver FOC on loads **over
   GBP 5,000 ex VAT** within 50 miles of Watford; below that Aplus batch or charge GBP 1/mile each way.
   Our order is GBP 4,845.22 - **GBP 154.78 under**. Same shape as AFS on Gordon Court. New manifest
   field `delivery_terms`; `delivery_priced: "provisional"` asks where carriage is genuinely
   contingent, a silent omission still FAILS.
2. A **thin-margin arm** on `check_quote_validity_against_commitment`. Gordon Court failed that rule by
   163 days; Riverside *passes* it by zero - our 30-day validity and Aplus's both close 26/08/2026, the
   same day - which is not the same as being covered. Under 14 days of headroom now asks. It matters
   here precisely because Adam is deferring issue until PHDB report, so the headroom goes negative
   while we wait.

`mary_checks.py data\job-checks\riverside-house-aov.json` = 0 failed, **3 questions** (free-area basis,
validity headroom, delivery). Nothing goes to RRR Group until those close.

**Two other things worth carrying.** The pack is a full flat conversion - its key defines W1 escape
windows, W2 windows at U 1.6 and D1/D5 doors right through all three floors - and we are pricing two
vents out of it; flagged to Adam as an opportunity. And the planning applicant on the location plan is
**Elderfern Ltd**, not RRR Group; Primrose Property, Elderfern and SRP Investments are RRR's associated
companies, so one client can arrive under several names.

**The reply to Adam could not be sent.** `scripts\mary_send.py` returned
`403 ErrorAccessDenied - "Access to OData is disabled: [RAOP] : Blocked by tenant configured AppOnly
AccessPolicy settings."` That is an Exchange ApplicationAccessPolicy change on the tenant, not a
transient, and nothing in the repo had recorded it. Reading still works. The draft is saved at
`outputs\Riverside House - Reply to Adam (draft).txt` for a human to send, and the substance went onto
the hub instead (REQ-9 rewritten, job status updated, two catches added). **Zac needs to re-grant the
app's send scope.**

### Riverside House - the free-area basis now has evidence, and it points to geometric (2026-07-27, evening)

**Adam answered REQ-9:** *"We can make the windows as big as we need to in order to achieve the free
area, because the openings are being newly formed. Drop me an email to remind me and I will ask Gintare
to requote."* So **size is not a constraint** - a free-area shortfall here is a repricing question, not
a design fight. Worth establishing early on any job with a performance-driven opening size. He answered
against the 1.5 m2 that turned out to be ours rather than the client's; triage put the correction to him
and asked him to hold off Gintare until the basis is settled. Email is still blocked, so REQ-9 on the
hub is the reminder he asked for.

**The geometric-vs-aerodynamic question now has two independent answers, both from documents we already
held.** This is the Stoke Park lesson again - the answer was in the building.

1. **The pack names its own compliance route, and the route decides the basis.** The key on K1653-10b/11/12
   reads *"MAINS OPERATED INTERLINKED HEAT DETECTOR TO **AD B1**"*. Approved Document B is the
   **prescriptive** route and states common-stair smoke vents as a **free area**; **aerodynamic** free
   area is the language of the **engineered** route, BS 9991 / BS EN 12101-2, which this pack is not on.
   The smoke-vent note itself is the AD B common-stair provision almost verbatim.
2. **Gordon Court's NBS says it outright for the identical duty** - L20 cl.630, *"AXS140 STAIRWELL
   VENTILATOR - throat dimensions 1250mm x 1000mm - **1m2 GEOMETRIC free area**"*, plus the lobby
   ventilator at 1.5 m2 geometric. Different architect, different job, same product class, same numbers.
   *Aerodynamic* appears nowhere in their 186-page NBS, 140-page mechanical or 127-page electrical spec.

**So the recommendation is that 1m2 means geometric, A Plus's 1.30 m2 clears it by 30%, and there is
nothing to requote** - a recommendation for the fire engineer or building control to confirm, not a
ruling to make. The general rule is now in `AI.md`: do not guess the basis and do not derive one figure
from the other, but *do* look at what standard the pack cites, because it usually tells you.

**A requote brief is written and ready either way** -
`outputs\Riverside House - A Plus requote brief (for Gintare).txt`. Built so that **one email settles
the job whichever way the basis falls**: the aerodynamic figure at the size already quoted, *and* a size
that achieves 1.0 m2 aerodynamic with both figures stated, plus the actuator change if the vent grows,
the whole-window Uw, the vent leaf, delivery and a price hold. A Plus stated both free-area figures on
QT51516 three days earlier, so none of it is new work for them. It explicitly tells them **not** to size
to 1.5 m2. This is the St Mary's lesson - draft the deliverable before the decision comes back.

**Two more, both found by running Gordon Court's checks back on our own quote:**

- **The ventilator-not-window test - Riverside passes.** QT51518 carries "AOV Type 850mm Stroke Single",
  "AOV Cable Direction", "AOV Colour 9006 Satin", a dedicated AOV Notes page and the SE Controls actuator
  warranty, at **GBP 1,401.24/m2**. Gordon Court's BSW quote failed the same test - 3no WN_7 at
  GBP 412.67/m2 and 4no WL_1 at GBP 442.98/m2, with zero occurrences of AOV, actuator, chain, stroke or
  24V, against positions the spec required to be Colt motorised ventilators. **Before comparing free
  areas, confirm the quote is for a ventilator at all; the rate is the tell.** A quote with no ventilator
  in it states no free area of either kind and reads as merely silent.
- **QT51518 carries NO SITE ADDRESS AT ALL.** The only address on it is Fenster's own yard, 97-98 Alston
  Drive, Bradwell Abbey, **MK13 9HF**. So "Glazed /Supply Only (Delivered)" ends in Milton Keynes, not at
  the Aylesbury site, and **the onward leg to HP19 7HL is ours and is in nobody's price**. A Plus also
  require "suitable labour at the delivery point to unload". All five of Gordon Court's supplier quotes
  deliver to the same yard. This is a **separate** miss from the free-delivery threshold and it survives
  clearing it - a load can be delivered FOC and still not reach site.

Gordon Court also extended `check_free_delivery_threshold` with `free_delivery_threshold: "never"` for
suppliers who never carry delivery; re-run clean against the Riverside manifest and the selftest passes.
`mary_checks.py data\job-checks\riverside-house-aov.json` = 0 failed, 3 questions, unchanged.

### Riverside House - the pack does not corroborate "the openings are new" (2026-07-27, late)

Gordon Court took the compliance-route rule and sent back three checks. All three paid out here, and one
of them contradicts a ruling this chat had broadcast an hour earlier.

**1. "THE OPENINGS ARE BEING NEWLY FORMED" IS NOT IN THE PACK.** Adam's REQ-9 answer said the vents can
be any size because the openings are new. Gordon Court warned that this is often true of only part of a
building - their own schedules constrain ground and first floors to *"the existing structural opening
sizes"* while levels 2-3 are new build. Run on Riverside, the answer is not "half" but "not at all":
**K1653-04 "EXISTING / PROPOSED ELEVATIONS" is a SINGLE set of eight elevations (A-H) showing a
complete, regularly fenestrated building, with no new opening marked anywhere and no AOV drawn on any
elevation.** That is not proof the openings are existing, but it is the whole of what the pack says, and
the verbal assurance is the only other source. Three consequences:

- If they are existing, enlarging one is structural - lintel, cutting masonry, making good - and is in
  nobody's price.
- **The drawings are stamped 24/02303/PAPCR - a PRIOR APPROVAL reference, not a full planning
  permission.** Prior-approval conversions normally carry tight limits on external alteration, so "as
  big as we need" may not be available at all. One question to HD Planning settles it. **Check the
  application TYPE before assuming any elevation can change.**
- **The second-floor vent may be going into an ARCHED opening.** AOV.01's stairwell is in the central
  tower; on **Elevation F** that tower's top storey carries **two arched-head windows**, while Elevation
  B's carries three rectangular. A Plus quoted a square-head 1130 x 1530 casement, and their own terms
  charge extra to glaze above a curved head.

**2. THE STALE-DOCUMENT CHECK WORKS ON A SIX-DRAWING PACK.** Gordon Court's rule - list every sheet with
its revision and date, and treat an outlier at rev "-" as suspect:

| Sheet | Title | Date | Revision |
|---|---|---|---|
| K1653-03 | Proposed Layout, all floors (**planning** set) | Mar 23 | B - 17.06.24 |
| K1653-04 | Existing / Proposed Elevations | Jun 24 | none |
| K1653-10b | Proposed Layout **Ground** Floor | Mar 24 | **B - Nov 25** |
| K1653-11 | Proposed Layout **First** Floor | Mar 24 | **none** |
| K1653-12 | Proposed Layout **Second** Floor | Mar 24 | **none** |

**The AOV requirement appears only on K1653-11 and K1653-12, the two sheets that have never been
revised**, while the ground floor was revised twice in November 2025. Probably innocent - those
revisions were "Dental Lobby added" and "altered", a ground-floor commercial change - but the
requirement has not been reviewed since March 2024, and on Gordon Court this exact pattern concealed a
smoke shaft deleted five months before tender. Carried as one line of confirmation.

Also: **the pack holds two layout sets.** The planning sheet K1653-03 puts all three floors on one sheet;
the construction-issue sheets K1653-10b/11/12 are separate. Only the construction set carries the
smoke-vent note - and the tidier revision history belongs to the sheet that does *not* mention the
requirement.

**3. THE RIGHT DENOMINATOR FOR A CLEAR-OPENING RATIO IS THE APERTURE, NOT THE GROSS FRAME.** Gordon
Court's ten-second test flags anything much above ~60% of gross. Riverside's requirement is
1.0 / 1.729 = **57.8%**, inside it. A Plus's quoted 1.30 m2 is 75% of gross, which looks alarming until
the aperture is computed: **957 x 1357 = 1.2986 m2**, so the quoted figure is exactly 100% of the inner
aperture (1357 = 1530 less two 86.5mm sections, 86.5 taken from the 957 daylight width). The aperture is
the real ceiling; the 60% figure is a proxy for how much of the gross the sections eat, and they eat far
more on a tilt-and-turn than on a fixed-light frame.

**That arithmetic also resolves RFI-2.** Because the quoted free area *is* the whole inner aperture, the
entire frame opens as one bottom-hung leaf and the 176mm transom is a glazing bar within the sash - which
is why a single 850mm chain works on a frame whose individual apertures are only 590mm high. Carried in
the brief as a confirmation rather than an open question.

The requote brief now runs to two parts: seven items for A Plus and **six client-side questions C1-C6**
for RRR / Campbell Ark / the fire engineer. `mary_checks` unchanged at 0 failed, 3 questions; selftest
passes.

### Riverside House - we priced from 5 of at least 12 drawings, and a withdrawn rule (2026-07-27, late)

**A RULE THIS CHAT HELPED CREATE HAS BEEN WITHDRAWN - do not re-adopt it.** Gordon Court proposed a
ten-second AOV test: required free area ÷ GROSS frame area, query anything much above ~60%. Riverside
showed the aperture is the real ceiling, and recomputing their own unit on that basis moved WN_7 from
*"cannot reach 1.5 m2"* to **99.3% of it - short by 0.01 m2**. Marginal, not incapable; the gross-frame
version would have condemned a borderline unit, which is the false-alarm failure mode. **Divide by the
aperture.** Riverside's A Plus figure is 75% of gross but exactly 100% of the 957 x 1357 = 1.2986 m2
aperture. **One caveat this chat owes back:** an aperture is normally *inferred* from a nominal section
depth unless the supplier states it - ours included, where 86.5mm comes from (1130-957)/2 - so an
aperture ratio is an estimate, not a compliance test. The clear opening is the manufacturer's figure.

**AND WE ARE NOT WORKING FROM THE WHOLE PACK.** Gordon Court ran this chat's "watch for two layout
sets" lesson at scale and found their loose job folder held **25 of the 82** architect's drawings in
the tender zip - the 57 absent including every floor layout, every existing plan and all three
demolition plans. Run back on Riverside, which has no zip at all:

- **Held:** Campbell Ark K1653-**03, 04, 10b, 11, 12**, plus hd planning's location plan.
- **Numbering gaps:** K1653-**01, 02, 05, 06, 07, 08, 09** unaccounted for - seven sheet numbers
  against five held, with nothing to say where the series ends.
- **Cross-referenced and absent:** **DETAIL 1, 2, 4, 5 and 6**. Verified at source - *"SEE DETAIL 4 FOR
  ACOUSTIC UPGRADE TO SECOND FLOOR"* and *"SEE DETAIL 6 FOR THERMAL UPGRADE TO ROOF"* on K1653-12,
  *"SEE DETAIL 1 / 2 / 5"* in the wall key, *"SEE DETAIL 4 ... TO FIRST FLOOR"* on K1653-10b. Not one
  detail sheet is in anything we have been sent.
- **Whole classes absent:** no fire strategy, no existing plans, no demolition plan, no sections, no
  window or door schedule.
- `Commercial\1. Tender Documents\RRR\Riverside` **is still empty** (re-checked). Everything priced
  arrived as email attachments.

**The check works without a zip to diff against** - sheet numbering gaps and cross-references both fire
on a six-drawing pack. Two one-minute tests for any pack: list the numbers held and look for gaps; grep
the drawings for "see detail", "refer to", "read together with" and confirm each named document exists.
Gordon Court found three of four referenced documents absent; Riverside five of five.

**THE PART THAT MATTERS MORE THAN THE COUNT - retarget the ask.** Both of this job's open questions live
on drawing classes we do not hold, and Gordon Court proved which:

- the **fire strategy** states the free-area basis in the author's own words - theirs reads *"AOV.
  1.5m2 CLEAR OPENING AREA"* - which is the geometric-or-aerodynamic question answered in one line;
- the **demolition plan** legend marks *"NEW STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE"* -
  precisely the new-versus-existing question raised against Adam's "the openings are newly formed".

So the ask has moved from *"confirm the openings are new"* to **the fire strategy and the demolition
plan, requested by name** - now C0 and C2 of the brief, with a line saying that if only two things get
asked for, make it those. C7 asks for the drawing register rather than guessing further from gaps.
Asking for "the rest of the pack" gets a shrug; naming the drawing that holds the answer does not.

`mary_checks` unchanged at 0 failed, 3 questions - the missing sheets are now an explicit exclusion
rather than a silent gap. Selftest passes.

### Riverside House - one vent's opening is new, the other's is not, and one may be a roof vent (2026-07-27, late)

Gordon Court found that their pack encodes new-versus-existing in the **window tag prefix** - a WINDOWS
TAGS legend on one elevation sheet reading *"WE_00 Windows in EXISTING openings replaced as new / WN_00
Windows in NEW openings / WL_00 Louvres to smoke shaft"*. The lesson generalises: **a naming convention
is usually documented somewhere, and the legend may not be on the sheet you are working from.**

Riverside has no such convention - W1 and W2 are *performance* tags - so the two stairwells were read
directly off K1653-11 and K1653-12. **The answer splits per vent, exactly as Gordon Court's
floor-by-floor warning predicted, even on a two-vent job:**

| | |
|---|---|
| **AOV.01** - second floor stairwell | **No window opening in any of its walls.** A new opening must be formed, so the size is genuinely free. **Adam's REQ-9 ruling is corroborated here.** |
| **AOV.02** - first floor stairwell | **Three existing window openings** already in the external wall. If the vent takes one, its size is set and enlarging it is structural work in nobody's price. **Not corroborated here.** |

So a blanket *"the openings are being newly formed"* was right for one vent and wrong for the other.
Read off floor plans, so suggestive rather than conclusive - the demolition plan still settles it.

**A related catch: the stair windows are the only glazing on these drawings carrying no W tag at all**,
while every habitable-room window has one. Untagged glazing is invisible to a schedule, which is
probably why the vents were never scheduled - and it bears on whether the drawings' 1.6 U-value binds
them.

**A FLAG THIS CHAT RAISED LAST TURN IS WITHDRAWN.** The suggestion that AOV.01 might sit in an
arched-head opening was wrong: the two arched windows on Elevation F's tower top storey line up with the
**Living room's** two W2 windows, not the stairwell, which has no windows on any face. What replaces it
is more expensive. The second-floor stairwell has **no wall opening at all**, and the note says the stair
is to be vented *"AT THE TOP STOREY ROOF"* - so **AOV.01 may be intended as a roof vent**, while A Plus
have quoted a wall casement on a 155mm subcill. If so we have priced the wrong product for one of the two
units. Now C4 in the brief: *establish wall or roof before accepting a window quote for an AOV.*

**AND NO APERTURE PERCENTAGE IS A COMPLIANCE TEST.** Gordon Court quantified the caveat this chat gave
them by varying only the assumed nominal section on their unit against a 1.5 m2 duty: 60mm 103.0%,
65mm 101.1%, 70mm 99.3%, 75mm 97.5%, 85mm 94.0%. **±5mm swings the answer across the duty line**, so a
computed "99.3%" is an estimate whose error bar swamps its margin. Accepted in full.

One distinction survives and is worth keeping, because it decides when the arithmetic is worth doing:
**reconciling a figure the supplier has stated is robust; predicting one they have not is not.** Riverside
reconciles A Plus's published 1.30 m2 - 957 x 1357 reproduces it to 99.9%, and across head+cill from
150mm to 200mm it only moves 101.6% to 97.9%, with no line to cross because the test is whether the
reconciliation holds. Use the arithmetic to understand what a supplier has told you, not to decide
whether they comply.

**Drawing hygiene is now three one-minute tests** - gaps in the sheet-number series, cross-references to
absent documents, and **duplicate numbers at different revisions**. That third one nearly cost Gordon
Court everything: their zip holds 21005/6/7 at both rev 02 and rev 03 and the tag legend exists only on
21007 rev 03 (5,751 characters against rev 02's 2,487 - comparing extracted text length between
revisions is a fast way to spot it). Riverside fails the first two and **passes the third**: six
drawings, all distinct numbers, one copy each.

`mary_checks` unchanged at 0 failed, 3 questions. Selftest passes.

### Riverside House - "a new opening" is not "a free opening", and the vent may not be a window at all (2026-07-27, latest)

**A correction to this chat's own answer from an hour earlier.** The previous record said AOV.01's size
was *"genuinely free"* because the second-floor stairwell has no existing opening, so a new one must be
formed, and that Adam's REQ-9 ruling was corroborated for that vent. That was too generous.

Gordon Court caught the same error on their own job and stated it better than we did: **the tag says the
opening is NEW, it does not say what the opening is CUT INTO.** Their WN_7 at level 1 is a new opening in
**retained fabric** - demolition plan 10016 rev 02 reads *"Retained wall to be assessed on site"* and
*"new brick slips are to be installed as part of the facade works"* - so lintels, cutting and making
good, none of it priced. The same type at levels 2 and 3 sits in their **two added storeys** and is
genuinely free. Adam's ruling applies cleanly to two of their three AOVs and only with structural cost
to the third.

**Riverside has no new-build half at all.** The pack presents the whole building as existing: K1653-04 is
a *single* "EXISTING / PROPOSED ELEVATIONS" set of eight, with no added storey shown and no new
construction annotated, and the tower's cornice and pediment run continuously through all three storeys.
So the second floor is retained fabric and AOV.01's new opening would be cut into existing masonry, while
AOV.02 would reuse one of three existing openings. **Neither vent has a cost-free resize.** Adam's *"we
can make them as big as we need"* carries structural cost on both, on top of the prior-approval question
at C3. This is an inference from the elevations being a single unchanged set, not proof - the existing
and demolition plans would settle it, and we hold neither, which is the C2 ask.

**So the question is three deep, and each layer caught the one above it:**

1. Is the opening **new or existing**? - tag prefix if there is one, otherwise read the plans.
2. If new, **what fabric is it cut into** - retained masonry or new build? - the demolition plan.
3. Is it a **wall** opening at all, or a roof vent?

**AND LAYER 3 IS NOW THE BIGGEST OPEN ITEM ON THE JOB.** Gordon Court's NBS names the standard product
for this exact duty as a *"STAIRWELL VENTILATOR... ROOF MOUNTED ONTO HORIZONTAL KERB... 1m2 geometric
free area"* - the same duty and the same 1 m2 as Riverside's requirement, mounted on the roof - and
specifies a separate, different **wall-mounted** model where a wall unit is wanted. So for a 1 m2
stairwell vent the standard answer is a kerb-mounted roof unit, not a casement.

Three independent pointers now say AOV.01 may be a roof vent, none conclusive alone: the note's own
wording (*"vented at the TOP STOREY ROOF"*), the stairwell having no wall opening to put a window in, and
the standard product for the duty. **If it is a roof vent, A Plus's 1130 x 1530 casement on a 155mm
subcill is the wrong product and none of Part One of the brief applies to AOV.01 - roughly half the
quote.** Gordon Court have the identical ambiguity live and cannot resolve it either: their NBS specifies
two roof units and one wall unit, and the items actually quoted are wall units. Neither job can settle it
from a supplier; it is the architect or the fire engineer.

`mary_checks` unchanged at 0 failed, 3 questions. Selftest passes.

### Riverside House - read the wall type, not the window tag (2026-07-27, latest)

**Gordon Court withdrew the instrument, not the principle - and this job's finding rested on the
principle.** They had told the board that a window tag prefix settles whether an opening is new or
existing. Rendering their proposed elevations killed it: the South elevation's WALL TYPE LEGEND calls
up *"WT-A2 Zinc standing seam / Insulation / Stud"* on the top storey, and **the windows on that new
storey are tagged WE_2** - "windows in existing openings replaced as new". A window in an existing
opening cannot sit in a newly built stud wall, so **WE_/WN_ is a schedule reference** (which of two
schedules the type lives in), not a rule the drawing enforces. Nobody should price off a window tag
prefix.

This chat withdrew *"AOV.01's size is genuinely free"* on the strength of their **principle** - a new
opening is not a free opening, ask what it is cut into - not their tag. Riverside has no WE_/WN_
convention; the openings were read directly off the plans and the fabric off the elevations. **The
withdrawal stands.** Worth separating the two when adopting a finding from another chat: which part is
the idea and which part is the tool.

**THEIR REPLACEMENT INSTRUMENT IS BETTER AND RIVERSIDE CARRIES A VERSION OF IT.** *"Read the wall
type."* Their legend - *"EXT - Existing wall types as surveyed"* against *"WT-A0 Brickwork / Cavity
Insulation / Block"*, *"WT-A1 Brickwork / Insulation / Stud"*, *"WT-A2 Zinc standing seam / Insulation
/ Stud"* - answers *both* "is the opening new" and "what is it cut into" in one read, from the actual
construction at that point of the facade.

Riverside's plans colour-code every wall that is **new or altered** - new partition, new separating
wall upgrade, separating wall upgrade to existing, dense blockwork infill. Checked at both stairwells
at high zoom:

| | |
|---|---|
| **K1653-12**, second floor stairwell | Internal walls coded yellow and purple. **External walls carry no coding at all**, and no opening. |
| **K1653-11**, first floor stairwell | Internal walls coded yellow with a hatched blockwork infill panel. **External wall carries no coding at all**, and holds the three existing openings. |

Uncoded = neither new nor upgraded = **retained existing fabric**, on both floors. Two independent
readings of the pack now agree, where before there was one, and neither vent has a cost-free resize.

**The generalisable form, which works without a build-up legend: a drawing that colour-codes CHANGE
tells you what is existing by omission.** If the key defines codes for new and altered walls and uses
them consistently, an uncoded wall is unchanged. Available on most refurbishment layouts and it does
not need the demolition plan. Weaker than a build-up legend, because it says "not changed" rather than
naming the construction.

**AND THE LIMIT.** Riverside has **no external wall build-up legend** - the key covers separating walls
and partitions only. So we know these walls are not new but **not what they are made of**, and that
decides the lintel, the fixing type and the cost of forming the opening. **Knowing a wall is existing
is not the same as knowing you can cut it.** A wall type schedule or a section is now requested at C2
alongside the demolition and existing plans.

`mary_checks` unchanged at 0 failed, 3 questions. Selftest passes.

### Riverside House - nobody is named to design the opening (2026-07-28)

**"As surveyed" is a deferral, and the wall build-up belongs to the structural engineer.** Gordon Court
closed the gap this chat had left open - *knowing a wall is existing is not the same as knowing you can
cut it* - by going to a structural sub-folder nobody had opened. Their *"Brick & mortar sampling
locations"* drawing reads *"sampling in the internal SOLID wall... in CAVITY wall... take samples from
BOTH THE INNER AND OUTER LEAVES of the cavity wall"*. That is the build-up, and the same folder held GPR
surveys, a resin-injection methodology and a workmanship spec covering cavity walls and lintels.
**Asking the architect for a wall build-up and asking the structural engineer for the investigation
drawings are two different requests, and on a refurbishment the second is usually where the answer is.**

**Run on Riverside, the answer is a concern rather than a build-up. No structural engineer is named
anywhere on the six drawings we hold.** The notes name a heating engineer and an electrician and
otherwise defer everything to site:

> *"CONTRACTOR TO ESTABLISH EXACT DRAINAGE LAYOUT AROUND BUILDING..."*
> *"BOILER/HEATER LOCATION/S TO BE SITE AGREED WITH HEATING ENGINEER/ELECTRICIAN & TO SUIT BUILDING
> INSPECTOR APPROVAL"*
> *"ELECTRICAL LAYOUTS ARE TO BE SITE AGREED WITH CLIENT"*

So the new opening in retained masonry that Adam authorised enlarging appears to have **neither a
structural design nor a price behind it**. That is a different problem from it being expensive, and it
is now raised at C2 as a concern rather than an accusation - the engineer's drawings may simply not have
reached us. **The generalisation: if you cannot find the consultant who owns a question, check whether
one has been appointed at all. A pack that defers everything to "site agreed" may be telling you the
design is not finished.**

**TWO ITEMS CLEARED RATHER THAN RAISED**, both from Gordon Court and both now recorded as *knowing*
exclusions rather than silent gaps:

- **Cavity closers, cavity trays and jamb DPCs at openings are not the glazing scope.** They sit in NBS
  **F30** *"Accessories/sundry items for brick/block/stone walling"* - masonry, so the bricklayer's,
  even where a new opening is formed. Gordon Court nearly raised their absence from four quotes as a
  gap. **Check which NBS section an accessory sits in before deciding it is missing from your price.**
- **But an intumescent perimeter seal is ours - checked here and not applicable.** NBS **L10 cl.790**
  *"Fire-resisting frames"* requires the frame-to-reveal gap to be *"completely filled with INTUMESCENT
  mastic or tape"*, and L10 is the windows section - so on fire-rated frames a supplier's fixing pack of
  *"screws, foam, packers, mastic"* does not comply. It is a fire-rating requirement, not a finish.
  **Grep any fire-rated frame quote for "intumescent"; it hides inside a fixings line.** Not applicable
  on Riverside: these vents sit in the **external envelope** of a protected stairwell, so the perimeter
  seal is weathering, not compartmentation - fire separation here runs between stair and flats via FD30s
  doors, fire collars and separating wall upgrades. Our priced external mastic at 10.64 lm x GBP 5
  stands; re-check if a vent is ever relocated into a compartment wall.

**AND A CROSS-CHAT PRACTICE, NOW IN `AI.md`: SEPARATE THE IDEA FROM THE TOOL.** A handoff carries a
principle and an instrument, and usually only one transfers. Gordon Court told the board twice to use
their window-tag prefix and then withdrew it; this chat had taken the **principle** (*a new opening is
not a free opening; ask what it is cut into*) and never the **instrument**, because Riverside has no
such tag for it to break - so their error cost this job nothing. Label the transferable part when you
post; and **when a chat withdraws something you built on, check which part you used before you withdraw
too - a false withdrawal costs as much as a false finding**, because it teaches people to discount the
board.

`mary_checks` 0 failed, 3 questions, now across 21 spec items. Selftest passes.

### Riverside House - we were asking for a document that does not exist (2026-07-28)

**Gordon Court closed their longest-running deferral by reading a title block**, and the method run here
produced the opposite - and more useful - answer. Their Energy Statement's block reads *"Edward
Pearce... Project No. 22/190"*, and that project number matches every M&E document in their pack, so the
architect's deferral pointed at a document they had held since turn one.

**The rule the pair of jobs produced:**

| | |
|---|---|
| Deferral to a **named, appointed** consultant whose other work is in the pack | **ADMINISTRATIVE gap.** Ask for the document, price on, qualify if it does not arrive. |
| Deferral to **nobody** - no consultant named, everything *"to be site agreed"* | **DESIGN gap.** There is nothing to ask for. This is the one that should stop you. |

**Run on Riverside's five deferrals, only one is administrative:**

| Deferral | Points at | Class |
|---|---|---|
| *"SEE DETAIL 1 / 2 / 4 / 5 / 6"* | Campbell Ark's own **K1653** series | **Administrative** |
| *"CONTRACTOR TO ESTABLISH EXACT DRAINAGE LAYOUT"* | A contractor not yet appointed | **Design** |
| *"BOILER/HEATER... SITE AGREED WITH HEATING ENGINEER/ELECTRICIAN"* | A role, no firm named | **Design** |
| *"ELECTRICAL LAYOUTS... SITE AGREED WITH CLIENT"* | The client | **Design** |
| Wall build-up / structural opening | No structural engineer named anywhere | **Design** |

So chasing paperwork produces exactly one thing on this job, and nothing bearing on our openings.

**AND THE SAME METHOD CHANGED WHO WE ARE ASKING, WHICH MATTERS MORE THAN THE CLASSIFICATION.** This chat
spent three turns requesting *"the fire strategy"*. **There probably is not one.** No fire engineer is
named anywhere on the six drawings, and the smoke-vent note is **Campbell Ark's own** - written in
Approved Document B language on a sheet whose key works *"TO AD B1"*. On a prior-approval conversion of
this size the architect commonly carries the fire strategy inside the drawings. Requesting a document
that does not exist returns nothing and costs a week.

So **C0 now asks the author**, by name off their own title block: **Campbell Ark, job number K1653,
drawn SC, 01234 709296, drawingoffice@aol.com** - is the 1 m2 geometric, aerodynamic or clear opening
area; is the vent in the wall or the roof; and did a fire engineer or building control officer advise
the note. That last part decides who the arbiter is: **if nobody independent set the figure, building
control does**, and these drawings defer to the building inspector repeatedly.

**Ask the author of a note, not a consultant who may not exist.** Read the title block before writing
the RFI - it gives the job number, the practice, the reviser's initials and a phone number. **K1653 is
also the handle for the missing sheets**: *"please issue the K1653 drawing register and any sheets we do
not hold"* can be actioned in a minute, where *"the rest of the pack"* cannot.

**AND A HABIT ADOPTED AND APPLIED TO OURSELVES: when you withdraw something, say what you are NOT
withdrawing.** The other half of this chat's own point that a false withdrawal costs as much as a false
finding. Two things have been withdrawn on Riverside - the arched-head risk on AOV.01, and the claim
that AOV.01's size was "genuinely free". **Not withdrawn:** the pack requires 1 m2 and not the 1.5 m2 in
our own enquiry; the requirement is per stairwell; the free area is quoted geometric only; the AOV
control system is in nobody's scope; the quote delivers to our own MK13 9HF yard and not to site; the
order is GBP 154.78 under A Plus's free-delivery threshold; validity has zero headroom; and the
wall-or-roof question on AOV.01 stands. None of those ever depended on the withdrawn parts.

Both rules are now in `AI.md`. `mary_checks` 0 failed, 3 questions across 21 spec items; selftest passes.

### Riverside House - the routing table, and a name in a revision note is not an appointment (2026-07-28)

**Gordon Court ran this chat's "is the consultant even appointed" check and found they had made the same
mistake in a live request** - REQ-22 carried the option *"Ask the FIRE ENGINEER whether the corridor AOVs
are wall vents or the roof-mounted units."* Across their five fire strategy drawings there is **no fire
engineer, no fire consultant, no approved inspector and no building control body named**. The only
*"fire officer"* reference sits inside a revision note - *"Updated to suit fire officers comments"* -
which is a record of a comment, not an appointment.

**That is the sharper form of the test and it is now in `AI.md`: a name in a revision note is not an
appointment.** Search the pack for the role, then ask of each hit whether it sits in a **title block**
(an appointment) or in **note text** (a mention). Riverside shows the same pattern from the other side:
*"TO SUIT BUILDING INSPECTOR APPROVAL"* and *"HEATING ENGINEER/ELECTRICIAN"* are role references in note
text with no firm named anywhere. **The corollary is worth keeping too** - a commenter who has already
changed the design is the de facto arbiter even without an appointment, so that is still a route.

**THE RIVERSIDE ROUTING TABLE**, built off the title blocks, all details verified at source (Campbell
Ark's from the K1653-11 title block at high zoom, hd planning's from the location plan's text layer).
Mary cannot approach any of them; the route is Adam or Gintare.

| Owner | Reference | Owns |
|---|---|---|
| **Campbell Ark** - author of layouts, elevations, wall coding and the smoke-vent note | job **K1653**, drawn SC, 01234 709296, drawingoffice@aol.com | **C0, C1, C2, C4, C5, C7** |
| **HD Planning Ltd** | plan ref **HD0-0197-01a**, app 24/02303/PAPCR, Mrs H Doyle, hayley@hdplanning.co.uk, 07916276436 | **C3**, prior approval |
| **RRR Group / PHDB** | building works package | **C6**, the AOV control system |
| **A Plus** | **QT51518** | all of **Part One** |
| **Nobody** | - | structural design of a new opening; wall build-up. **Cannot be chased, only raised.** |
| **Building control** | the drawings' own *"BUILDING INSPECTOR APPROVAL"* | effective arbiter on the free-area basis |

The applicant named on the location plan is **Elderfern Ltd**, not RRR - so a planning question may need
to go through a different company in the group. Worth checking who the *client* is on each consultant's
drawing before addressing anything.

**THE CONTRAST BETWEEN THE TWO JOBS IS NOW COMPLETE, AND IT IS WHY THE TEST EARNS ITS TEN MINUTES.**
Gordon Court's pack names a full design team - architect, structural, services, electrical, heating - and
every deferral they chased turned out to be **administrative**. Riverside's names a heating engineer and
an electrician as **roles** and defers the rest to parties not yet appointed, so four of five are
**design** gaps. Same test, opposite answers, and the answer tells you whether to chase paperwork or
raise an alarm before a week goes on the wrong one.

**Stated plainly: the commercial position did not move this turn.** Still GBP 5,990.22, still not issued,
still gated on PHDB. What changed across the evening is that every open question now has a named owner
and an answerable form, where several were previously addressed to nobody. That is consolidation rather
than discovery and is logged as such.

### Riverside House - half the brief was never blocked, and it is decaying (2026-07-28)

**Gordon Court's challenge - *"when a job stalls waiting on a client, check which of your open items are
actually SUPPLIER questions; they do not need the award"* - run on Riverside, which has been "waiting on
PHDB" since Monday. The brief splits clean:**

| | | |
|---|---|---|
| **Part One** | 7 items, all questions for A Plus about their own quote | **NOT BLOCKED** |
| **Part Two** | 8 items, Campbell Ark / HD Planning / RRR / PHDB | Blocked |

Half of it could have gone days ago. **Two of the unblocked items are decaying while we wait, which is
what makes this urgent rather than merely tidy:**

- **The price hold.** A Plus QT51518 expires **26/08** and our house document carries 30 days' validity,
  so the last date we could issue and still be covered by the supplier was **27/07 - yesterday**. Issuing
  today puts our price open to 27/08, one day past theirs, and **the gap grows by one for every further
  day of delay**. Asking a supplier to hold is the one action that becomes *more* valuable the longer a
  gate stays shut. **Generalisable: supplier expiry minus your own validity period gives the date your
  cover ran out, and it may already be behind you.**
- **The aerodynamic figure.** The biggest open question on the job, answerable by A Plus in one line from
  their own system - they stated both figures on QT51516 three days earlier. It has sat four turns behind
  a client decision it never depended on.

**Not wasted under any outcome:** if C4 resolves to "roof vent", only items 2 and 3 fall away, and only
for AOV.01. A **"WHAT DOES NOT WAIT FOR PHDB"** header now sits at the top of the brief.

### The rate register prices frames and glass and almost nothing else

Gordon Court's finding, **verified here at source rather than taken on trust, and broader than stated.**
Of `data/supplier-rates.json`'s **80 categories, all 21 of these return zero**: acoustic, trickle,
Linkvent, Passivent, curtain, actuator, AOV, smoke, strip, disposal, manifestation, intumescent, mastic,
restrictor, scaffold, kerb, roof vent, secondary, folding, sash, slider.

The four missing categories already on the board were unusual **products** - folding doors, vertical
sliders, secondary glazing, AOV/smoke vents. Gordon Court add five that are not: **strip-out and
disposal, manifestation, acoustic trickle vents, intumescent seals, curtain walling**. This check adds
four more: **mastic, restrictors, scaffold, kerbs** - all carried on this job.

**One correction in fairness to the tooling**, because *"the register has nothing"* overstates it and
someone will otherwise find a mastic rate and conclude the finding was wrong: a few standing house rates
do exist outside the register - mastic GBP 5/lm, EPDM GBP 25/m2, install default GBP 140/unit - and that
is where this job's mastic line comes from. The accurate statement is that **the register does frames and
glass to size-banded, supplier-attributed depth, and the ancillaries have one flat house rate or
nothing.** On a new build that hardly matters; **on a refurbishment you can price the windows and none of
the work around them.**

Both rules are now in `AI.md`. `mary_checks` 0 failed, 3 questions; selftest passes.

### Riverside House - 29 days to ask cheaply, and an exclusion that deserved a number (2026-07-28)

**Gordon Court took last night's validity arithmetic and found the sharper consequence.** A lapsing
supplier quote is not only a price risk - it is **a deadline for every question you still want to ask
that supplier**. Anything sent while the quote is live is priced against it: same job, same spec, same
rates, they add lines. Anything after is a fresh enquiry at whatever the market is by then.

    A Plus QT51518, dated 27/07, 30 days  ->  lapses 26/08/2026  ->  29 days from today

It bites hardest on brief item 2, which asks A Plus to price a **resized** unit. Asked now that is a
revision we can set against GBP 4,845.22 and read the delta; asked in September it is a new number with
no anchor, and the whole point of the question is lost. **So there are two dates on this job and they
answer different questions:**

| | |
|---|---|
| **27/07 (past)** | last date we could **issue** and still be covered by A Plus. Gap grows by a day, daily. |
| **26/08 (29 days)** | last date we can **ask** A Plus anything as an addendum rather than a new enquiry. |

### "No rate" and "no quantity" are different problems with different owners

Gordon Court corrected their own unpriceable list: curtain walling **has** a rate - `mary_pricing`
carries CW_SUPPLY_M2 850.0 and CW_LABOUR_M2 150.0, verified here - what it lacks is a **quantity**. That
is the opposite problem and a different party to ask: an area from the architect, not a price from the
supplier. Sorted on Riverside:

| | | |
|---|---|---|
| rate **and** quantity | the 2 vents (supplier-backed), mastic 10.64 lm @ GBP 5 | **priced** |
| quantity, **no rate** | **window restrictors (2no)**, onward haulage MK13 to HP19 | supplier question |
| neither | AOV control system, scaffold, undesigned structural work | correctly excluded |

**THE RESTRICTORS SHOULD NOT HAVE BEEN SITTING IN THE EXCLUSIONS LIST, AND THIS CHAT PUT THEM THERE.**
A Plus's own AOV notes say the actuators *"will not act as window restrictors"*, that *"the facade
contractor / fabricator"* should fit them 50mm beyond the stroke, and that A Plus *"will not be liable
for any replacement actuators or damage to the vent"* if none is fitted. **Fenster are the installer on
this job, so "the facade contractor" is us** - on a life-safety system. Excluding them may still be the
right commercial answer, but that is a decision to take against a number, not a gap. Quantity known, no
rate anywhere, so a supplier figure is the only route: now **Part One item 8**, and reclassified in the
checks manifest from `excluded` to `provisional`.

**The general form, now in `AI.md`: run the rate/quantity sort across an exclusions list, not just an
unpriced list. Sometimes an exclusion is an unanswered supplier question wearing an exclusion's
clothes** - and the test is whether excluding it was a decision taken against a number, or a gap left
because nobody could price it.

The price has not moved: still GBP 5,990.22, still not issued. What moved is one item out of the
exclusions list and a second deadline onto the record. `mary_checks` 0 failed, 3 questions across 21
items; selftest passes.

### Riverside House - our own proposal caps a risk, and a second exclusion falls (2026-07-28)

**Gordon Court's lesson: check your own terms and conditions page before reporting a gap - the answer may
be in the document you sent.** They had reported 163 days of unqualified exposure for a week before
reading page 8 of their own issued proposal.

Run here, because the 30-day house validity underpinning every deadline on this job had been taken for
three turns from a **generator footer** rather than the house document - exactly the kind of unsourced
number this chat would challenge in anyone else's work. **Verified at source**,
`templates/proposal-content.json`, Terms and Conditions, *"Quotation Validity"*:

> *"All quotations provided by Fenster Glazing & Locks Ltd are valid for 30 days from the date of issue,
> unless agreed otherwise. **All quotations are subject to final site survey and measurement
> verification.**"*

The 30 days is right, so every deadline posted stands - it now rests on the house document. **And the
second sentence is the find.** Riverside's 1130 x 1530 came from Adam's enquiry email, not from a survey
and not from any dimensioned drawing, since the pack has no window schedule and no dimensioned opening.
**Our own terms already qualify the dimensional risk.** It does not rescue C4 - a roof vent is not a
measurement error - but an issued price would not be a fixed commitment on unsurveyed dimensions.

### A second exclusion falls, and a proposal clause caught before it is written

Gordon Court sharpened the exclusions test: **"we exclude X" is only safe if X is genuinely SOMEBODY
ELSE'S under the spec.** Three of their twelve failed - fire stopping against NBS L10 cl.790's
intumescent seal (which sits in the *windows* section), testing not covering cl.205 certification
documentation, and site storage asserting site delivery that no supplier quote supports.

Most of Riverside's hold: builder's work is PHDB's, access is Adam's standing rule, maintenance is the
occupier's RRO duty, Part K balustrading is a builder's item A Plus expressly exclude. **One fails:
onward haulage from our own MK13 9HF yard to site.** Not another party's at all - **Fenster are the
installer, so Milton Keynes to Aylesbury is ours.** It was excluded because nobody had priced it, not
because it belonged elsewhere. Second item of this class in two nights, after the restrictors.
Reclassified `excluded` to `provisional`; already covered by brief item 6(b).

**The two tests are different and both earn their ten minutes:** *is a rate or a quantity missing* tells
you **who to ask**; *is this genuinely somebody else's* tells you **whether you should be asking at all**.
An item can pass the first and fail the second, which is what the haulage line did.

**AND A TRAP LOGGED BEFORE IT HAPPENS.** Gordon Court's issued proposal excludes Site Storage *on the
basis that* *"Materials will be delivered to site"* - contradicting all five of their supplier quotes,
which deliver to our own yard. **Riverside has no proposal yet, so nothing is wrong here - but that
wording must not go in**, because A Plus deliver to Milton Keynes and QT51518 carries no site address at
all. It is the sort of clause carried forward from the last job without anyone rereading it against the
quotes, which is presumably how it reached theirs.

Price unchanged at GBP 5,990.22, unissued. `mary_checks` 0 failed, 3 questions; selftest passes.

### Riverside House - the folder was never empty, and the extraction was missing half the document (2026-07-28)

**Gordon Court withdrew a founding finding tonight** - GBP 5,597.89 of cost reported since their first
turn as having "no supplier quote behind it", in four documents. All seven lines were quoted, at exactly
the workbook costs. They had used a **half-filled working column** as the test. Their rule: *a working
column, a print statement and a generated footer are all representations of a source, not the source.*

Riverside made the generator-footer version of that last night, so this chat audited its own claims.
**One failed badly.**

**THE ONEDRIVE JOB FOLDER IS NOT EMPTY AND NEVER WAS.** It was reported empty in the brief, the job file,
the hub, the noticeboard and the handover - five times. It holds the full job structure and real files:

    1. Estimating\2. Supplier Quotes\Quotation_QT51518.PDF        filed 27/07 15:46
    1. Estimating\3. Client Quote\MASTER COVER LETTER 31.05.2026.docx
    1. Estimating\3. Client Quote\MASTER PRICING DOC 10.07.2026.xlsx
    plus 1. PO, 2. Site Survey, 3. Drawings, 4. Orders, 5. Finance, 6. H&S, 7. Aftersales

The cause: searches ran against `OneDrive - Fenster Glazing & Locks Ltd`, which does not exist. The root
is **`OneDrive - Fenster Glazing (1)`**. Zero results were read as an empty folder. **A failed search is
not evidence of absence - it is evidence of a failed search. If a check returns nothing, prove the check
can return something before you report the nothing.**

**Not withdrawn:** the `3. Drawings` folder holds no files, so none of the six drawings we work from is
filed anywhere - the pack-completeness finding stands, only the wording was wrong. And A Plus's quote
**is** filed, so triage's original "the only copy is the email attachment" is out of date.

### An extraction can be faithful and still incomplete

Having found the real folder, the **actual** `MASTER COVER LETTER 31.05.2026.docx` could be read instead
of `templates/proposal-content.json`, which is an extraction of it. **76 paragraphs against the
document's 153.** The validity clause is faithful in both - so last night's figure was right - but two
clauses matter and **one is absent from the extraction entirely**:

- **NOT IN THE EXTRACTION:** *"Site Survey - Only conducted once the structural openings are fully
  formed. Any revisits may be subject to a fee."* AOV.01 needs a new opening cut in retained masonry, so
  the sequence is **PHDB form the opening, then we survey, then A Plus manufacture**. Our survey cannot
  precede the builder and nobody has stated when that is - and it bears directly on how long A Plus are
  being asked to hold their price. Now **C8** in the brief.
- **In the extraction but unread:** *"Fenster Glazing & Locks Ltd is not responsible for overall design
  intent, architectural suitability, or **regulatory strategy** and relies on information, drawings, and
  specifications provided by the client or their professional team."* **The geometric-versus-aerodynamic
  question is regulatory strategy.** Asking is still right and C0/C1 stand, but the exposure changes from
  "we may be liable for a non-compliant vent" to "we rely on their team, and we asked".

**Checking that a quoted line is accurate is not the same as checking the source has nothing else in
it.** Worth running against any extracted spec or NBS text. Rule added to `AI.md`.

### One check logged as NOT RUN

**The GBP 5,990.22 has never been observed as a value computed by Excel.** It is hand-derived from the
workbook's stored formulas and independently reproduced by `mary_pricing` - two routes that agree, but
both from this chat's reading of the same formula chain. A live recalculation via Excel COM **will not
start in this environment**. Mitigating: the repo template's formulas were confirmed **identical** to the
live `MASTER PRICING DOC 10.07.2026.xlsx` in the job folder, so the document is built on the current
master, and the code values are independently corroborated by Adam's table in `MARY-HANDOVER.md` s6.

### Riverside House - clause 16 splits every finding into ours-to-fix and ours-to-ask (2026-07-28)

**Gordon Court found the clause both jobs had been sitting on.** Verified here independently by
enumerating the T&C headings in our own `MASTER COVER LETTER 31.05.2026.docx` rather than taking the
number on trust - **twenty clauses; clause 2 is Quotation Validity, clause 16 is Design Responsibility:**

> *"Fenster Glazing & Locks Ltd is not responsible for overall design intent, architectural suitability,
> or **REGULATORY STRATEGY** and relies on information, drawings, and specifications provided by the
> client or their professional team. **Responsibility is limited to MEASUREMENT VERIFICATION, SUPPLY, AND
> INSTALLATION** of the agreed glazing systems."*

**This is a third sort over a findings list and it answers what the other two do not.** *Priced /
benchmark / unpriceable* asks what you can cost; *rate versus quantity* asks who you ask; **clause 16
asks whose responsibility it is - and therefore how the finding should be raised.**

| **THEIRS** - reliance on their professional team | **OURS** - expressly retained |
|---|---|
| C0/C1 geometric or aerodynamic; C4 whether a roof vent is required | **Item 9** whether we quoted the right **product** for the position |
| C3 planning; C5 drawing currency; C6 who carries the control system | Item 1 the aerodynamic **figure**; item 4 whether A Plus stated a Uw **at all** |
| RFI-6 whether 1.6 W/m2K is the right target for a stair vent | Item 5 leaf configuration; items 6, 8 delivery, restrictors; **every dimension** |

**The split runs through this job's biggest question.** *"Is a roof vent required?"* is regulatory
strategy - theirs, and the position is **reliance, not defect**. *"Have we quoted a wall casement for a
position the drawing puts on the roof?"* is **supply - ours**, and clause 16 does not touch it. C4 was
mixing the two; it is now split, with the supply half added to Part One as **item 9**, asking A Plus
directly whether a DualFrame wall casement is suitable here and whether they offer a kerb-mounted
alternative.

**AND IT CORRECTS THIS CHAT'S OWN FRAMING FROM LAST NIGHT, against us.** The note that clause 2's
*"subject to final site survey and measurement verification"* **qualifies** the dimensional risk is only
half right. Clause 16 says our responsibility **is** measurement verification, so **the survey makes a
dimensional discrepancy fixable - it does not make it somebody else's.** The 1130 x 1530 came from an
enquiry rather than a survey; both clauses point at us.

**Practical effect, now built into the brief:** ours-to-fix items belong in a supplier RFQ; theirs belong
in a client qualification framed as reliance. Two documents, two tones - and the brief's Part One / Part
Two split now maps onto clause 16 deliberately, with the reasoning printed at its foot. It doubles as a
priority order: the *ours* items do not go away whatever the client answers, so chase them regardless.

**A related extraction trap from the same evening**, worth its own line: a two-column
inclusions/exclusions table interleaves when extracted, producing *"Site Survey - Only conducted once the
structural openings **Fire Stopping - To be done by others, if required** are fully formed"*. Gordon Court
nearly posted that as a document discrepancy. **When a phrase reads oddly in extracted text, suspect a
multi-column table before you suspect the document.**

Price unchanged at GBP 5,990.22, unissued. `mary_checks` 0 failed, 3 questions; selftest passes.

### Riverside House - the brief became two letters somebody can send (2026-07-28)

**Gordon Court turned their clause-16 sort into three drafts and made the point this chat had earned:**
*"REQ-26 had nine days on it and no text behind it."* Riverside was the same shape - the supplier half
had been called urgent for two turns while it sat inside a fifteen-item working brief that whoever acted
on it would have to disassemble first. **A request with no text behind it is still a request for somebody
else to write an email.**

Split along clause 16, each letter carrying its reasoning at the head:

| Document | Date | Contents |
|---|---|---|
| `Riverside House - RFQ to A Plus (draft, send by 26-08).txt` | **26/08** | The nine items clause 16 makes **ours** - product suitability, the aerodynamic figure, the Uw, leaf configuration, delivery, restrictors, price hold |
| `Riverside House - Questions to RRR (draft).txt` | none | What clause 16 puts on **their professional team** - free-area basis, wall or roof, the 1.5 m2 source, sheet currency, the openings, planning, the control system, the programme. Grouped by owner (Campbell Ark / HD Planning / RRR) so it can be forwarded rather than answered |
| `Riverside House - Covering note to Adam (draft).txt` | none | The reminder he asked for, and what has changed since his instruction |

**Nothing has been sent and Mary cannot send any of it** - ghost protocol, and `mary_send` is still 403'd.

**The date sitting on one letter and not the other is the sort doing real work.** The supplier letter
*decays* - after 26/08 everything in it is a fresh enquiry rather than an addendum to a live quote. The
client letter does not decay; it just gates the answer. Different urgency, different document, and that
only becomes visible once the findings are sorted by who owns them.

**Two drafting choices taken from Gordon Court, and one matters more here than there.** *Ask a supplier
what they priced against, not why they got it wrong* is not a courtesy on this job - **the 1130 x 1530
came from Fenster's own enquiry.** A Plus quoted exactly what was asked for, so if the vent is the wrong
product for a roof position that is our specification, not their error, and the letter says so in terms.
The general form: **before drafting a query, check whether the thing you are raising is something the
supplier chose or something you told them.** And *when a decision has been taken, say so* - the covering
note states plainly that nothing reopens Adam's ruling on sizing, and that if a bigger vent is needed his
answer was exactly right.

### A stale draft in an outputs folder is a live hazard

The turn-one reply to Adam was still sitting in `outputs\` as a clean-looking draft after three of its
central claims had been withdrawn - it treats the vents as a settled wall-window purchase, repeats that
size is unconstrained, and says the OneDrive folder is empty. It was in the house voice, addressed to the
right person, and **nothing in the filename said it was out of date.**

Renamed **`Riverside House - Reply to Adam (SUPERSEDED 27-07, do not send).txt`** with a header listing
what it gets wrong and naming its replacements. **If you have superseded your own work, go and look at
what is still sitting in outputs with a plausible name on it.** Rule added to `AI.md`.

Price unchanged at GBP 5,990.22, unissued. `mary_checks` 0 failed, 3 questions; selftest passes.

### Riverside House - the new stale-draft tool was hiding our own letter (2026-07-28)

Gordon Court built `scripts/mary_stale_drafts.py` off last night's finding and asked every chat to run it
on their own folder. Run here, **our A Plus letter was absent from the report entirely** - not under due,
not under undated, nowhere - while the sweep concluded *"Nothing expired"*. Their note said the tool
"sees riverside's A Plus letter at 26/08". It parses it; it never printed it.

**The bug:** `days < 0` to expired, `days <= warn_days` to due, **and no else**. Any dated draft more than
a fortnight out was parsed, dated and silently dropped. **Proved before changing anything** - the same
file appears correctly at 6 days on `--today 2026-08-20` and as expired on `2026-08-27`, so the parsing
was always right and only the reporting was blind.

Fixed with a **DATED, NOT YET DUE** bucket, the reasoning in the docstring so nobody strips it as noise.
All three date views verified, exit-1-on-expiry still fires, and `scan()` had no callers outside prose so
extending its return signature was safe - checked before changing it.

**Why it was not cosmetic:** a sweep that shows a dated draft only in the last fortnight of its life shows
it exactly when acting has stopped being comfortable. The letter's whole argument is *send this while the
quote is live*, and 15 of its 29 days would have passed unmentioned.

**This is the sixth costume of the same error in one night** - a half-filled column, a print statement, a
generated footer, a failed search, an extraction missing half a document, and now a report with an
unhandled branch. **A report that omits a category is worse than one that shows it wrongly.** If you write
a tool that buckets things, check every branch has a home.

### Their mirror hazard, and their parsing hazard, both run here

**A draft can go stale on a date you typed into its own filename** - the easier half to defend against,
and this chat had not done it either. The A Plus letter argues in its own words that it is *"an addendum
to a live quote"*, false from 27/08. It now opens with **`IF TODAY IS AFTER 26 AUGUST 2026, DO NOT SEND
THIS AS IT STANDS`**, listing the four sentences that go false and confirming the nine questions survive -
re-head as a fresh enquiry, expect the base price to move.

**And their proximity-parsing hazard, checked rather than assumed.** Gordon Court withdrew a turn-one
finding after attributing glass lines by reading the nearest preceding `Location:` header - on a quote
where one position carries five glass lines, that put their obscure-glazing item on the wrong position and
understated it by sixteen units. **QT51518 has exactly one position block** - one `O/A Sizes`, one
`Frame Price`, one `Glazing Details & Apertures`, **zero** `Location:` headers - so nothing can be
misattributed, the A1/A7 apertures and the `4-20-4 Clr Tough S Coat 1.2` make-up necessarily belong to the
single 1130 x 1530 unit, and the aperture reconciliation stands. **The hazard scales with block count:
impossible on a one-position quote, near-certain on a multi-position one parsed by proximity** - so count
the blocks before trusting an attribution.

Price unchanged at GBP 5,990.22, unissued, nothing sent. `mary_checks` 0 failed, 3 questions; selftest
passes.

### Riverside House - the price gate cut the remedy out of every rule (2026-07-28)

Gordon Court took this chat's *"a report that omits a category is worse than one that shows it wrongly"*
and found a far worse instance than the one it came from: **`report()` in `mary_checks.py` - the gate that
decides whether a quote goes out - printed the first 200 characters of a FAIL and stopped.** On their job
that hid **GBP 201,304.36** of unfixed cost, and a spec rule naming nineteen uncovered items of which
three reached the screen. They asked every chat to measure its own.

**Measured on Riverside - 586 characters across three ASKs.** Small, because the job is two windows. But:

| Rule | chars | lost | what was past the cut |
|---|---|---|---|
| system can meet the specified performance | 441 | 241 | the thermal requirement, and *"Get it in writing - on both founding jobs the answer existed and no one had gone and got it"* |
| supplier price held as long as ours | 298 | 98 | *"Confirm the supplier price at the point of issue, or carry a stated allowance"* |
| delivery actually included | 447 | 247 | the charge basis, and *"Get the supplier to confirm the charge or that the load is batched free"* |

**All three cuts removed the REMEDY. None removed the FINDING.** That is not luck - these rules are
written statement-first and action-last, so **a trailing truncation strips the instruction out of every
rule at once, systematically.** Gordon Court's was the dramatic loss; the structural loss is that the
reporter was biased against the most actionable sentence in every rule.

**Being accurate about the harm:** on Riverside it cost nothing. The job is small enough that the same
ground had been worked by hand - the validity arithmetic and the delivery item both reached the brief by
independent derivation rather than by reading the remedy. The finding is not *"we were harmed"* but
*"nobody would have noticed on a small job"*. Their fix verified on this manifest, and their new
`check_spec_label_matches_evidence` passes on all 21 spec items.

### The four-turn-old NOT RUN, now run

Their own earlier rule applies: **logging a check as outstanding is only worth something if somebody then
runs it.** The **GBP 5,990.22** had been confirmed two ways - by hand and by `mary_pricing` - but both
rested on *this chat's reading of the same formula chain*, with Excel COM blocked and no LibreOffice.
**Two routes that agree because they share a reading are repetition, not verification.**

Third route, which removes the reading from the chain: a parser that extracts the code-to-adder map from
`H9`'s own `IF(B9="MAW",550*75%…)` chain (**412.50**) and the code-to-labour map from `I21`'s SUMPRODUCT
(**160**), then applies them to the actual cell values:

    items 5,670.22 + installation 320.00 = 5,990.22      (I23 = SUM(I9:I10) + I21)

Three independent routes now agree and the residual shrinks from *"did one person read it right"* to
*"would Excel read those formulas differently from the parser"*. **When a check is blocked by a missing
tool, look for a route that removes your judgement from the chain rather than one that reproduces it.**

Their job-file contradiction check also run here: 851 lines grepped for *not run / outstanding / not
done*; one hit, accurate rather than stale, and now closed.

Price unchanged at GBP 5,990.22, unissued, nothing sent. `mary_checks` 0 failed, 3 questions; selftest
passes.

### Riverside House - a mechanism generalised from a sample with no counterexample (2026-07-28)

**This chat's explanation of the truncation was wrong, and the corrected one is worse news.** Riverside
measured three cut findings on one job, saw the remedy lost from all three, and posted that *"the rules
are written statement-first and action-last"*. Gordon Court measured **44 remedy sentences across 13
manifests**:

| detail length | n | median remedy position | cut |
|---|---|---|---|
| 400 chars or under | 35 | **0%** | 3 of 35 |
| over 400 chars | 9 | **84%** | **9 of 9** |

**Most rules put the remedy FIRST.** It is **displaced backwards by the list of offending items**, and
that list grows with how much is wrong - while the truncation that hides it is triggered by the same
length. **So the instruction vanished exactly on the jobs where most had gone wrong.** One rule proves
it, identical code: `delivery actually included` shows the remedy at 0% on ten one-supplier jobs (332
chars), **78% on Riverside** (447), 84% on St Mary's, 89% on Gordon Court (776).

**Checking Riverside's own three shows why the hypothesis was wrong:** 441 chars at 79%, 298 at 73%, 447
at 78%. **All three samples sat in the displaced regime - there was no short finding to compare against**,
so the evidence could not distinguish *"the rules are like this"* from *"my job is in the regime where
they behave like this"*.

**The meta-lesson is worth more than the bug: three samples from one job cannot tell you whether you are
seeing a property of the system or a property of your job. Before posting a mechanism, check the sample
contains a case where it would NOT apply.** Gordon Court's structural fix - a separate `remedy` field
printed on its own `->` line - is verified on this manifest; all three ASKs now carry one.

### Their asymmetry check, run here, and it fired

Gordon Court diffed their two supplier letters and found they had asked the **GBP 18,298.94** supplier how
long it could hold its price and *explicitly not asked* the **GBP 183,005.42** one - 91% of the exposure -
because a prior decision made asking look pointless. **That conflates a decision about whether WE hold OUR
price with whether we gather information from a SUPPLIER.**

Riverside has one supplier, so the literal diff does not apply - but the underlying shape does. Checked
both letters against the largest unowned item on the job:

- **Questions to RRR, item 8:** *"Who is carrying the AOV control system?"*
- **RFQ to A Plus:** no mention at all - zero hits for control, panel, override, SE Controls, 24v.

**We asked the party who owns the DECISION and never asked the party who holds the INFORMATION.** A Plus
supply the actuator and their own notes say it *"must be powered by a compatible control system which is
approved by SE Controls"* - the best-placed party in the chain, left out because the scope boundary had
been decided. **A scope boundary says what a supplier will SUPPLY, not what they can TELL you.**

Fixed as **RFQ item 10**: what panel would A Plus recommend for 2no 24v actuators on this duty, do they
supply it or is it always a separate trade, and price it if they can - so C6 reaches RRR with a figure
rather than a gap.

**The generalised check, now in `AI.md`: for every open item, write down who owns the DECISION and who
holds the INFORMATION, and confirm you have asked both.** They are usually different parties. Gordon
Court's version was two letters that should have matched; Riverside's was two parties on one question.

Price unchanged at GBP 5,990.22, unissued, nothing sent. `mary_checks` 0 failed, 3 questions; selftest
passes.

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


### Gordon Court - second turn: the AOV function was never priced, and the NBS was where the performance lived (2026-07-27, evening)

Triggered by a handoff from riverside asking one question about BSW QT252257 "AOV & LOUVRE"
(GBP 7,085.76): does the pack state free area as GEOMETRIC or AERODYNAMIC, given aerodynamic runs at
60-62% of geometric?

**RIVERSIDE'S QUESTION HAS A GOOD ANSWER.** This pack is written **geometric** - NBS L20 cl.630 states
*"AXS140 STAIRWELL VENTILATOR - throat dimensions 1250mm x 1000mm - 1m2 geometric free area"* and
*"AXS140 LOBBY VENTILATOR - throat 1250 x 1500 - 1.5m2 geometric free area"*. "Aerodynamic" appears
nowhere in the 186-page NBS; the only hit in the 140-page mech spec is attenuator fairings (p80) and the
127-page electrical spec has none. So the ~40% trap does not bite here.

**THE REAL FINDING SAT UNDERNEATH IT: THE SMOKE VENTILATION FUNCTION IS NOT IN THE PRICE AT ALL.**
Schedule 52003 carries the heading *"AOV SMOKE SHAFT LOUVRE"* and a note *"WL_00 Louvres to smoke
shaft"*; **3no WN_7** sit in Corridors 1-1/1-2/1-3 with **"AOV"** against them, and **4no WL_1** at
levels 0-3. NBS L20 cl.630 specifies both as **Colt proprietary, motorised** products - *"COLTITE
GLAZED LOBBY VENTILATOR (STAIR C)... double glazed with thermally broken glazing... **drive open/drive
close using a 24V motor mounted to the rear**"* and *"EN SEEFIRE LOUVRED NATURAL VENTILATOR... **designed
and tested to EN 12101-2**... controlled by a **24Vdc electric actuator**"*. **BSW quoted `Qty: 3
Prestige T&T` and `Qty: 4 Prestige Casement`** - ordinary Sheerline windows. The quote contains **zero**
occurrences of AOV, louvre, actuator, chain, stroke, motor, 24V or smoke, and WL_1's `Glazing:` line is
**blank**. BSW stated no free area of either kind because they had not quoted a ventilator.

**The tell was the rate, and it generalises:** WN_7 is **GBP 412.67/m2** and WL_1 **GBP 442.98/m2** -
plain-window money against a register median of ~GBP 528.83/m2 - while riverside's A Plus AOV data point
is **GBP 1,401.24/m2** supply, of which the actuator and AOV sash carry ~GBP 870/m2. **An AOV that prices
like a window is not an AOV.** On that single point the 3no WN_7 alone are **GBP 4,988-5,667** of supply
cost short (one quote, different system, order of magnitude only - and there is still no AOV category in
the register, so the 4 louvres cannot be benchmarked at all). Whole exposure: **GBP 7,085.76 cost /
GBP 10,055.76 sell**, and it is binary - either ours and under-priced, or the smoke-vent specialist's and
the sell comes out. Our proposal names *"AOV windows, smoke shaft louvres"* and does neither. **REQ-24
raised.**

**A CORRECTION TO MY OWN RECORD FROM THIS MORNING, AND IT MATTERED.** I had written that Gordon Court's
schedules *"set no U-value at all"* and deferred to a consulting engineer - which made it look as though
only the sustainability annex asked for anything, the exact escape route St Mary's warned about. Wrong:
**NBS L10 cl.330 "Windows & Roof Windows" sets *"Thermal performance (U-value maximum): 1.2 W/m2K"*, and
L20 cl.280 sets *"1.2 W/m2K or better"* on communal entrance doors.** The requirement is in the governing
technical document and does not depend on the annex. The same clause reads *"Standard: To BS6375-1,
BS6375-2, BS6375-3, EN 14351-1 and Pas24"*, so **PAS 24 applies to every window**, with cl.205 demanding
*"Independent, 3rd Party Certification"* and documentary submittals - upgrading the PAS 24 finding from a
schedule note to a specification clause (BSW: zero mentions across four quotes). Cl.280 also fixes the
entrance-door finish as **"RAL7016 MATT (EXTERNAL) & RAL9010 GLOSS (INTERNAL)"**, so AFS's *"Standard
RAL / mat standard"* silence is now measured against an explicit dual RAL rather than a "TBC". And
cl.330 defers g-value, frame factor **and** glazing details to a **"SAP Consultants specification"** that
is not in the pack - a second missing consultant's spec alongside Edward Pearce (**RFI-7**).

**DELIVERY IS IN NOBODY'S PRICE** (riverside's new rule, run here). All four BSW quotes: *"All estimates
are ex works, additional delivery charges may apply"* - no rate, no threshold, no distance rule. AFS:
the GBP 250 priced extra already recorded. And **all five quotes deliver to Fenster's own MK13 9HF yard,
not to site**, so carriage on 227 units to Edgware is ours too and there is no carriage line in the
workbook at all.

**TOOLKIT: extended riverside's `check_free_delivery_threshold` to express "never free".** It could say
*always* free (`free_delivery_threshold: 0`) but had no way to say a supplier never carries delivery -
both of this job's cases. Left null, the rule *asked*, when AFS's is a known quantified GBP 250 hole.
`free_delivery_threshold: "never"` now states it and **fails** it, as riverside's own note said a silent
omission should. Selftest passes; `_test-riverside.json` still fires its rule. Gordon Court now runs
**5 FAIL, 2 ASK** (was 4/2).

**TWO DASHBOARD MESSAGES HANDLED.** Zac's dash-23 explained the `mary_send.py` 403 - permissions
over-corrected, hub only for today; acknowledged, and I have not attempted to send. Adam's dash-24
answered **REQ-7, which is Crestwood Park, not this job** - passed to `crestwood-park` verbatim rather
than actioned here, because searching another job's mail would muddy that trail. It carries a general
ruling worth keeping: *"we would mark the teleflex up by 25%. Please remember that mark up as a general
rule for estimating."* **I deliberately did NOT change `mary_pricing.py`** - the engine prices supply +
(code value x 75%) plus CALIBRATION, a different mechanism from a flat 25% on a bought-in item, and
reading "general rule" as "add 25% to everything" off a misrouted message about someone else's job would
change every future quote. Asked Adam on the hub to confirm whether he means bought-in/third-party kit
specifically (Teleflex, WCI screwjacks, Colt vents) or all supplier cost; posted the ruling to the board
so nobody loses it meanwhile.

**COVERAGE CAVEAT, stated rather than glossed:** I started a keyword sweep over all ~300 PDFs in the zip
but its stdout was lost to buffering, so the free-area conclusion rests on targeted reads of the
authoritative documents (NBS 186pp, mech spec 140pp, electrical spec 127pp, the five schedules, the five
quotes) - not on an exhaustive sweep.


### Gordon Court - third turn: Adam holds the price, and the clarification window turns out to have closed on 15 July (2026-07-27, late)

**REQ-20 ANSWERED AND CLOSED.** Adam, hub 29: *"It's fine we will hold the price and just trust
everything will be okay."* So the 163-day validity gap on GBP 201,086.70 is a **taken decision** - we
carry it, and it is not to be re-raised on this job. Recorded with the lever arm so the choice reads as
informed: materials are **54.6%** of the fixed GBP 368,376.70, so **every 1% of supplier inflation is
GBP 2,010.87** off the bottom line (2% = GBP 4,022; 5% = GBP 10,054; 10% = GBP 20,109; 15% =
GBP 30,163). No forecast implied. Flagged to him that his answer covers the price hold **only** - the
GBP 723.87 of omitted cost, the D_T and D_X door queries and REQ-24 all remain open.

**THE LAST OUTSTANDING TECHNICAL JOB, DONE - AND IT WAS A DEAD END WORTH HAVING.** Turn one flagged
`1. Q&As 02.06.26.pdf` (no text layer) as the priority, on the Lower Range Road logic that clarification
logs are where U-value answers hide. Rendered at 200dpi: **it is not a clarification log.** It is a
screenshot of the **Delta eSourcing Message Centre**, topic *"Gordon Ct: ITT"*, logged in as *"Antony
Berry, Supplier Administrator"*, showing **"One item found"** - one 02/06/2026 13:04 message from
darien.jay@vixus.co.uk to All Suppliers announcing the ITT had gone live, return 22/07 @ 1400. **No
clarifications were ever raised on this tender**, so RFI-3 stays open. It does independently corroborate
the 22/07 @ 1400 date.

**AND THE ROUTE IS SHUT, WHICH IS THE REAL FINDING.** The ITT: *"Bidders may raise questions relating to
this tender **up to 5 working days prior to the tender return deadline**"*, *"All questions during the
tender should be directed **via the Delta portal**"*, *"**Please DO NOT contact jLiving directly.**"*
Five working days before 22/07/2026 is **~15 July**. Our tender went to Chigwell on **09/07** - the
window was open while we were pricing, with five known unresolved scope questions, and nobody used it.
**Consequence: all ten open RFIs are now POST-TENDER queries via Chigwell - variation or qualification
territory, not clarification.** Combined with Adam's decision to hold a firm price for 180 days, the risk
on this job has moved from *supplier prices rising* to *scope resolving against us with no mechanism to
reprice.* **General lesson for the board: find the QUESTION deadline, not just the return deadline, and
get RFIs in while the route exists.**

**ADAM'S REQ-17 RULINGS (St Mary's) LANDED IN THIS CHAT AND TWO OF THREE BIT HERE.** Forwarded verbatim
to `st-marys`, whose request it is, then run against this job:
- **Access** - *"Our proposal document should state that we have not allowed for any access."* Gordon
  Court already does. Cleared on wording; the commercial risk (two new storeys, and whether the
  exclusion survives Chigwell's prelims) is untouched by his answer and stated as such.
- **Strip-out** - GAP. *"We have effectively left it unanswered however we would include it for a job of
  this size."* This job is twice St Mary's and strips **40 replacement windows plus external doors** out
  of an occupied building. Pack silent (no strip-out/disposal in any schedule; NEC3 activity schedule has
  no SOW item numbers, so no cross-reference like St Mary's SOW 1.09). Proposal excludes *"Waste Removal -
  Generally"* and never names it. The GBP 46,840 install cannot absorb it - pure per-unit fit labour at
  GBP 160-500/unit. **RFI-9.**
- **Manifestation** - GAP, and the St Mary's clause-2.24 finding repeating. **NBS L20 cl.280** requires
  *"Manifestation: As drawing"* on the communal main entrance doors, and the adjacent internal-door clause
  says *"Not required"*, so it is deliberate. But manifestation appears **zero times** in all five
  schedules, **zero** in `Window & Door Elevations.pdf`, **zero** in `Fire Rated Door Elevations.pdf` and
  **zero in our proposal** - and no drawing shows any. Requirement exists, extent undefined, neither
  priced nor excluded. **RFI-8.**

**THE 25% STAYS OFF THIS JOB'S BOUGHT-IN KIT.** Triage settled it (Adam hub 28): *"we are just adding 25%
mark up to Teleflex, keep everything else you have learnt the same."* Recorded on the job because Gordon
Court is where the over-generalisation would have bitten hardest - the AOVs are **Colt units with 24V
motors and actuators**, bought-in specialist equipment of exactly the Teleflex kind. **Not authorised.**
If REQ-24 puts them in our scope the uplift must come from a real supplier price, not Teleflex's markup by
analogy. `mary_pricing.py` remains untouched.

**A THIRD MAILBOX BLIND SPOT, POSSIBLY.** *"Antony Berry, Supplier Administrator"* on that portal
screenshot appears nowhere in our own records. If Fenster holds a live Delta account on this tender,
jLiving's **award and standstill notices** go to that account rather than estimating@ - a third gap
alongside commercial@ and info@. **RFI-10**, internal.

Manifest now 19 spec_items; run unchanged at **5 FAIL, 2 ASK**. Both queue items answered on the hub and
moved to `processed\`.


### St Mary's - Adam answers REQ-17, and two register blind spots open up (2026-07-27, evening)

No work order. The turn's input was a handoff from `gordon-court` forwarding Adam's hub message 31
verbatim - the answer to REQ-17 had been delivered into their chat rather than mine. Recorded it, set
REQ-17 to answered, and replied to Adam on the hub.

**THE RULING, and what it leaves.** All three boundaries are now actions rather than questions, and two
of them cost money that is not in the GBP 174,546.37:

- **ACCESS** - *"our proposal document should state that we have not allowed for any access"*. Our
  proposal already excludes Access/Lifting Equipment by name, so the wording is right. **But the ruling
  settles what our document SAYS, not who PAYS** - Prelims F and B require the Contractor to provide all
  scaffolding *"for himself and any Sub-Contractor"*, we install to 5,580mm, and 55.97 m2 of the glazing
  is 3.62 m or taller. An unqualified exclusion is a negotiating position, not an agreement. **REQ-24.**
- **STRIP-OUT** - *"we would include it for a job of this size"*. It is not in the sold price. **107
  openings / 202.80 m2**, and the install line **cannot absorb it**: GBP 21,915.05 reconciles to the
  penny as per-unit fit labour, which is fit-only money. Gordon Court independently reached the same
  conclusion about their GBP 46,840. MTCBC's SOW item 1.09 measures strip-out in m2 and cross-refers it
  INTO our item 6.01, so on this job *"if they assume it's not included"* is the less likely outcome -
  their own document already reads as though it is ours.
- **MANIFESTATION** - allow it and state it in the inclusions.

**MEASURING THE THING THAT WAS "UNDEFINED".** Clause 2.24 asks for two bands at 850-1000mm and
1400-1600mm, so the quantity is just element width x 2 across whatever counts as a glazed door or
screen: **24.10 linear metres** over the 9 glazed door/screen units (Types G, I, L, O, U, AF, AK), or
**39.90 linear m** if the two 3,620mm silled screens (Types F, H) are included. That reduces the open
question from "the whole item" to "do silled windows count", which is a one-line RFI. Worth generalising:
extent undefined is not the same as unmeasurable - measure the band before raising the query.

**TWO NEW REGISTER BLIND SPOTS.** `data/supplier-rates.json` holds 80 categories and **not one** covers
strip-out, removal, disposal, waste or manifestation - all 80 checked. So the two items Adam has just
ruled we should allow are both items we cannot benchmark, on the refurbishment work that is most of what
we bid. They join secondary glazing, folding doors, vertical sliders and AOV/smoke vents. **And
manifestation is already an unpriced, unexcluded gap on FOUR live jobs** - St Mary's, Gordon Court,
Brocks Hill and Filwood - with the Estimating Log carrying *"Manifestations"* as a note against two of
them, so it had been spotted by humans before and still never priced.

**Also flagged to triage:** the noticeboard was back to **22,315 characters** within half an hour of the
20:40 archive that unfroze the bridge. The prompt-via-stdin fix is committed but inert until the restart
(REQ-21), so the 32,767 command-line ceiling still applies to board + handoffs + brief. Suggested an
earlier second sweep, and that until the restart a long finding is better placed in the poster's own
`data/jobs/<key>.md` with a short pointer on the board. Flagged rather than acted on - the board and the
archive belong to triage and two chats sweeping at once is how things get lost.


### St Mary's - the quote-check workbook, and outbound email dies (2026-07-27, late evening)

No work order; triage's handoff only confirmed the noticeboard now auto-trims (my flag last turn led to
the fix). Every substantive item on this job is blocked on a human, so the useful move was to make the
human's next step cheap.

**BUILT `outputs/St Marys Refurbishment - Quote Check and RFI Schedule.xlsx`** (generator
`scripts/st_marys_quote_check.py`), consolidating four turns of audit into the house quote-check format
used on Brocks Hill and Filwood. Five sheets: **Summary**; **Commercial exposure** (the 8 items promised
or required but not in the price, plus the price-hold gap); **Findings** (all 14 ranked HIGH/MEDIUM/LOW
with source and consequence); **RFIs** (14 questions grouped by who can answer them - ET&S, cfw
architects, BSW/Bellview - and sendable as it stands); and **Reconciliation** (13 checks that came back
correct, recorded so nobody reopens the parts that are sound).

**THEN OUTBOUND EMAIL FAILED, AND IT IS NOT A ST MARY'S PROBLEM.** `scripts/mary_send.py` returns a
Graph **403: ErrorAccessDenied, "Access to OData is disabled: [RAOP] : Blocked by tenant configured
AppOnly AccessPolicy settings."** Two attempts minutes apart, identical - an Exchange
ApplicationAccessPolicy decision at the tenant, so there is no code fix and no chat can work around it.
**REQ-23 raised for Zac**, plus a board post and a direct handoff to triage.

Diagnosis recorded rather than guessed at: **it worked earlier today** (Crestwood Park's quote went out
at 10:49; Brocks Hill and Vesuvius both emailed Adam with workbooks this afternoon), so it broke during
the day - and **there is no send log anywhere in the repo**, which is why nobody can date it. Worth
adding one. **Inbound is unaffected** (work orders still landing, one at 15:56) and **the hub still
works** (`mary_dashboard_reply.py` returned 200 minutes before the send failed), so the hub is currently
the only outbound route to a human. The substance therefore went on the hub - a reply to Adam on message
31 and REQ-24 - and the workbook is recorded everywhere as **generated but NOT sent**, so a file sitting
in `outputs/` is not mistaken for a delivery.

**The transferable point, third infrastructure failure today after the registry wipe and the
32,767-character prompt ceiling:** check the channel works before relying on it, and report the failure
rather than the intention. All three were silent or misattributed until someone read the actual error -
the registry wipe never errored at all, the launch failure looked like a CLI problem, and this one would
have read as "Mary sent it" if the traceback had been swallowed.


### St Mary's - calibration against BSW, and the register's band structure (2026-07-27, late)

No work order; triage's handoff only confirmed they had narrowed my 403 to the mary@ mailbox and built
the send log I asked for. Everything on the job is blocked on humans, so the turn went on the self-check
the playbook asks for in s5c - and it produced the most useful engine finding of the day.

**THE COMPARISON.** Register benchmark via `mary_pricing.find_rate` for the 31 Sheerline Prestige
casement types against **BSW QT252799's own frame prices for exactly the same 98 units** - the cleanest
like-for-like available, because the workbook's frame column had already been verified line by line
against the quote. **GBP 66,540.24 benchmark vs GBP 60,359.22 actual = +10.2%.** Fifth entry in
`data/calibration.json`.

**I MISLABELLED THE FIRST PASS AND REDID IT.** `derived_factors()` from `data/learned-rates.json`
supersedes the hand-typed `CALIBRATION` list, so the factor that fired was the **measured `bsw` 1.056
(n=273 lines)**, not the Sheerline 1.10. Which means **on any BSW Sheerline job the Sheerline correction
never runs at all** - worth knowing before anyone tunes that number.

**THE AGGREGATE IS AN ACCIDENT OF UNIT MIX - this is the finding that matters.** Uncorrected the register
is a respectable +4.4% out on the whole package. By band it is nothing of the sort:

| band | types | units | actual GBP/m2 | register GBP/m2 | error |
|---|---|---|---|---|---|
| <1.5m2 | 10 | 34 | 697.38 | 449.77 | **-35.5%** |
| 1.5-3m2 | 15 | 50 | 368.01 | 363.50 | **-1.2%** |
| 3-6m2 | 4 | 10 | 340.10 | 467.57 | **+37.5%** |
| >6m2 | 2 | 4 | 270.19 | 365.18 | **+35.2%** |

Per type the spread is -43.6% to +46.9%, and only 15 of 31 land within +/-20%. Small units are far
dearer per m2 than the median says and large units far cheaper - the bands do not capture the within-band
size gradient. **So the register is a good whole-package predictor only where the unit mix is broad, and
a poor per-element one outside 1.5-3m2.** A job weighted to one size will be badly out in a predictable
direction.

**BOTH CORRECTIONS MADE IT WORSE** - raw median +4.4%, measured bsw factor +10.2%, Sheerline 1.10 +14.8%,
both compounded +21.3%. **Nothing in the engine was changed:** one job cannot move a factor built on 273
lines, and it is the band structure rather than the supplier factor that looks wrong. Flagged, not wired
in - the same discipline triage used on Adam's 25%.

**AND THE WIDER NUMBER, WHICH IS NOW OUT OF DATE IN THE PLAYBOOK.** MARY-JOB-SESSION s5c still says the
log holds two entries "averaging 7.9% out with almost no bias (-1.6% mean)". It holds five, and **four
of the five run HIGH: mean bias +10.4%, mean absolute error 14.2%.** Checked whether that was an artefact
of mixing comparison types - four compare Mary's SELL against Fenster's issued sell, mine is the only
benchmark-cost-vs-supplier-cost - and it is not: the four homogeneous ones give **+10.5% bias, 15.2%
absolute**. Added a **`basis_type`** field and a line to `how_to_add` so these are grouped before anyone
quotes a single accuracy figure. Three of the four typed CALIBRATION corrections are upward multipliers,
which is worth holding next to a base that already runs 10% high. Asked triage to correct the playbook
text, since every new chat reads it on turn one and it currently tells them the benchmarks are unbiased.

**A HYPOTHESIS RECORDED FOR ADAM, LABELLED AS ONE.** The unexplained GBP 1,000/unit "Additional" on Types
F and H: those two are the cheapest per m2 on the job from BSW (GBP 280 and GBP 262 against GBP 368
mid-band). A judgement adder on a 3,620mm screen that looked too cheap is exactly what that would look
like - which would mean the money is already in the supply line and only the labelling is wrong, and
that is the difference between the GBP 3,520.95 of light install labour being missing or already covered.


### St Mary's - a request reported as raised that never existed (2026-07-27, late)

No work order; triage's handoff confirmed both of last turn's flags had been acted on. Started the turn
by reading the open requests and found REQ-22 on the board was Gordon Court's AOV request, not the St
Mary's follow-on I had reported raising.

**IT WAS MY BUG, NOT A RACE.** `scratchpad/req17_answer.py` read `dashboard-state.json`, hardcoded
`"REQ-22"` as the next free id, and guarded the append with `if not any(r["id"] == "REQ-22" ...)`. Gordon
Court had committed **their** REQ-22 at **20:33:51**; my script ran at about **21:05**, so the guard was
False, **the append was skipped, and the unconditional print still said "REQ-22 raised"**. It was then
reported as raised in the job file, both handover documents, the dashboard job status and to Zac. There
was no duplicate, no error and no gap in the numbering to notice it by.

**Re-raised as REQ-24** via `scratchpad/reraise_req.py`, which computes the id at write time from what is
on disk, refuses to write if it is taken, and **verifies by re-reading after the write**. Every stale
REQ-22 reference in `data/jobs/st-marys.md`, `MARY-HANDOVER.md` and `HANDOVER.md` repointed (16 in total).
The substance was never actually lost to Adam - it is in the hub reply to his message 31 - but it was
untracked for roughly four hours.

**Checked the blast radius rather than assuming it was isolated:** ids currently run 1-24 with no gaps and
no duplicates, and every other request this chat raised (15, 16, 17, 19, 23) is present. But the
hardcoded-id-plus-duplicate-guard pattern appears in at least **five scripts across chats** -
`dash_update4.py`, `gc_req.py`, `gc_req22.py`, `req17_answer.py` and the reraise itself - so the exposure
is general. Posted to the board with the three-line fix, and told `gordon-court` directly since it was
their id involved (their request is intact and correct; mine simply never existed).

**THE LESSON, AND IT IS THE FOURTH TIME TODAY.** The registry wipe never errored. The chat-launch failure
looked like a CLI problem. The email outage would have read as "Mary sent it" if the traceback had been
swallowed. And here an idempotency guard reported success while doing nothing. Every one was silent or
misattributed until someone read what actually happened rather than what was supposed to happen. **If a
script tells you it did something, the print statement is not the evidence - the file is.** Suggested a
shared helper in `scripts/` that raises a request properly, flagged rather than written because that is
shared plumbing.


### Gordon Court - fourth turn: access cleared by the head contract, manifestation and strip-out quantified, and a median I had repeated was wrong (2026-07-27, late)

Two handoffs from st-marys drove this; no queue items.

**A CORRECTION TO MY OWN BOARD NOTE, and the finding got stronger for it.** My 20:30 AOV note compared
Gordon Court's units to *"a register median of about GBP 528.83/m2 for a plain glazed aluminium window in
the same 1.5-3 m2 band"*. **I took that from a handoff and never opened the file.** GBP 528.83 is
**Aplus**, category *"aluminium window/screen, **glazed/unknown** [1.5-3m2]"*, n=23 - wrong supplier,
looser category, wrong comparator for a BSW Sheerline job. The right ones, read at source: **bsw
aluminium tilt & turn window, glazed [1.5-3m2] = GBP 433.08, n=86**, and **bsw aluminium casement window,
glazed [1.5-3m2] = GBP 363.50, n=446**. Against those, **WN_7 (the "AOV") at GBP 412.67/m2 is 4.7% BELOW
the plain tilt-and-turn median** and WL_1 at GBP 442.98/m2 is 21.9% above the plain casement. So a
motorised AOV is priced *under an ordinary opening window* - now BSW against BSW, no longer leaning on
riverside's Aplus point at all. **Lesson: if you are putting a rate in front of anyone, read it out of
`data/supplier-rates.json` yourself and quote supplier, category AND line count - band and supplier both
change the answer.**

**THE REGISTER BLIND SPOT IS WORSE THAN ABSENCE - IT IS SILENT ABSORPTION.**
`data/supplier-rates.json` **has already ingested QT252257** and filed its two lines into
`aluminium tilt & turn window, glazed [1.5-3m2]` and `aluminium casement window, glazed [1.5-3m2]`.
Those two lines are precisely the mis-specified AOV and smoke-shaft louvre behind REQ-22. **The register
cannot detect an AOV mis-specification because it classifies on the supplier's product description**, so a
mis-described AOV is indistinguishable from the window it was described as. Two lines in 86 and 446 is
numerically nothing; the mechanism repeats and drags AOV evidence toward window money. Same exposure for
any performance item quoted as its plain equivalent - fire doors, acoustic units, secondary glazing.
So do not read *"the register has no category for X"* as merely a gap to fill - **check whether X has
been quietly filed under something else.**

**ACCESS - CLEARED, AND BETTER THAN "OUR WORDING IS FINE".** st-marys asked whether this pack has an
equivalent of their Prelims F and B. It does not, and the difference favours us.
`Gordon Court wi Contract Version - V3.pdf` p2, margin heading **"Temporary Access"**: *"The Main
(Principal) Contractor shall allow for all crash decks, handrailing, scaffolding or other temporary safety
or access requirements necessary for satisfactory completion of the works (including the main external
scaffolding and associated high level weather protection roof scaffold)."* The same document explicitly
distinguishes the Main (Principal) Contractor from *"Contractor's / Sub-contractor's & Suppliers
operatives"* (p16, welfare). So scaffolding - including a roof weather-protection scaffold, substantial on
a building gaining two storeys - is **expressly Chigwell's**, and our exclusion is *consistent with the
head contract* rather than exposed by it. **Supersedes the earlier "check it survives Chigwell's
subcontract prelims" note.** Gordon Court was therefore **not** added to REQ-24 on access.
**General rule: "we never allow for access" is safe as a DRAFTING rule - which is what Adam ruled on -
but not automatically safe COMMERCIALLY. Read the Works Information or Prelims for the ACTOR, not just
the obligation; it differs job to job.**

**MANIFESTATION QUANTIFIED using st-marys' width x 2 bands method.** NBS L20 cl.280 is the **only clause
in 186 pages** that turns manifestation on (*"Manifestation: As drawing"*; the adjacent internal-door
clause says *"Not required"*, so deliberate), and no drawing shows any.
**NARROW 8.152 lin m / 2 units** (D_A pair) - **MEDIUM 15.002 lin m / 5 units** (+ D_D x2 Corridors 5-0
and 7-0, D_U Stair 2) - **WIDE 39.332 lin m / 15 units** (every glazed external door).
**Price MEDIUM**, and the reason is itself a finding: **cl.280 describes a "Rebated SINGLE leaf" door
while the actual GR316 Entrance door is a DOUBLE** - so either the clause maps to the single-leaf communal
doors and not the entrance pair, or it is another spec-versus-schedule mismatch like **D_T**. MEDIUM
covers both. A further **15.140 lin m** (LW_1 x4, WN_7 x3) sits behind it *if* Approved Document K
critical-location glazing catches the full-height glazed corridor units - flagged, not assumed.

**STRIP-OUT QUANTIFIED: 40 replacement windows, 62.457 m2** (schedule 52002; the 84 new windows carry
none). Unlike St Mary's there is **no client SOW cross-referring it into our item** - NEC3 activity
schedule, no item numbers - so here it is **unallocated rather than allocated to us**.

**NO RATE ATTACHED TO EITHER, deliberately.** Re-verified st-marys' finding at source rather than taking
it on trust: **80 register entries, zero** with a strip-out, disposal, removal, manifestation or scaffold
category. Both are **quantities for an RFQ**. Both **added to REQ-24** - st-marys' request already asks
Adam for exactly these prices, and a fifth separate request would be worse for him - appended, attributed,
never rewriting their text, and **verified by re-reading the file** (6,294 chars, 8 options, marker
present).

**MY REQUEST SCRIPTS - VERIFIED, AND ONE CORRECTION TO THE SHARED LESSON.** Opened
`data/dashboard-state.json` rather than trusting any print: **REQ-20 and REQ-22 are both present by id AND
job name; ids run 1-24, no gaps, no duplicates.** But `gc_req.py` and `gc_req22.py` did **not** share the
dangerous half of st-marys' bug. Both hardcode the id - same weakness - yet both guard with
`assert not any(...)`, which **raises**; st-marys used `if not any(...)` plus an *unconditional* print,
and that is what reported success while doing nothing. Had REQ-22 been taken, my script would have died
with an `AssertionError` immediately. **Worth stating precisely, because the fix that matters is compute
the id at write time and verify on read-back - not replacing asserts.** Both are hardcoded-id patterns;
only one lies.


### St Mary's - withdrawing the access finding, and the waste clauses behind strip-out (2026-07-27, late)

No work order. `gordon-court` handed over the answer to a question I had asked them - whether their pack
had an equivalent of St Mary's Prelims F and B - and sent the method rather than just the answer: **read
for the ACTOR, not just the obligation.**

**MY ACCESS FINDING IS WITHDRAWN, AND THE EVIDENCE AGAINST IT WAS INSIDE MY OWN QUOTE.** Prelims clause
B, rows 180-181, re-read at source: *"The Contractor is to provide all scaffolding, temporary lighting
and clearing away, making good **for himself and any Sub-Contractor**."* The pack uses "the Contractor"
throughout as the single actor above both "Sub-Contractor" (r181) and the trades (r222), and distinct
from "the Employer" (r5, r209). It is the **main contract between MTCBC and ET&S** - so the Contractor is
**ET&S**, Fenster is the Sub-Contractor, and **ET&S must provide the scaffolding for us**. Our exclusion
of Access/Lifting Equipment is **consistent with the head contract, not exposed by it**. I had published
that exact sentence on the noticeboard twice while drawing the opposite conclusion from it. Same answer
gordon-court reached from jLiving's Works Information, which explicitly splits the "Main (Principal)
Contractor" from "Contractor's / Sub-contractor's & Suppliers operatives".

**What survives, so nobody overcorrects:** the head contract binds the employer and the main contractor,
not us. **ET&S's own sub-contract order to Fenster is a document nobody has seen** and can still push
access down - worth one reserving line in the proposal. Adam's drafting rule ("state that we have not
allowed for any access") is unaffected. **Access liability is job-specific**: on two jobs now the
employer's own wording put it on the tier above us, and the giveaway both times was a phrase that named
the tiers.

**LIVE, NOT WITHDRAWN - the waste clauses that travel with strip-out.** The same sweep turned up Prelims
**C** (rows 253-278): building waste must go to a **NAMED licensed landfill** (the pack already names
*"Tredegar Skip Hire"*), the contractor must name the site(s) he intends to use, and a **Site Waste
Management Plan (SWAMP, Appendix A) must be completed WITH the tender submission**. It then states that
these are *"a STRICT requirement of the Contract"*, that a tender without them *"will be discounted from
consideration"*, and that *"the contractor is to allow in his rates for these requirements and no claim
will be entertained for failure to do so"*. **Appendices A and B are not in the sections we hold** (we
have 2, 3 and 4 only). These sit on ET&S in the head contract like the scaffolding - but **if strip-out
flows down to us under item 6.01, the disposal duties, the landfill naming and the SWMP flow down with
it**, and the "no claim entertained" wording removes the fallback. On a refurbishment, check the waste
clauses at the same time as the strip-out allocation; they travel together.

REQ-24 rewritten accordingly - access limb withdrawn, strip-out and manifestation unchanged and still
unpriced, disposal detail added. Verified on re-read. Manifestation stays at **24.10 linear m** core /
39.90 wide; gordon-court applied the same width-x-2-bands method to their own job and priced the middle
of three readings, which is the right shape.

**The habit worth keeping:** when a clause looks like it contradicts one of our exclusions, find the
defined actor before writing it up as a conflict. I had the right quote and the wrong reading for four
turns.


### Gordon Court - fifth turn: waste clauses clean, and the actor test sharpened to "read the Contract Data" (2026-07-27, late)

Driven by st-marys' handoff. They withdrew their access finding this turn (their Prelims clause B reads
*"…for himself and any Sub-Contractor"*, so the employer put scaffolding on the tier above them all along)
and credited the method from Gordon Court. Their **live** item was a warning to run here: St Mary's Prelims
C requires waste to a **named** licensed landfill plus a **Site Waste Management Plan with the tender**,
enforced by *"any Tender… not containing the requested information will be discounted from consideration…
no claim will be entertained."*

**RAN IT, AND GORDON COURT COMES BACK CLEAN.** Searched the ITT, PCI (31pp), Works Information (29pp),
Contract Data and Form of Tender: **no named landfill, no SWMP, no waste carrier licence, no
discounted-from-consideration penalty.** The tender return structure confirms it - six sections, none a
waste plan - and the only waste item in the ITT is scored quality question **D1** (*"manage waste
responsibly"*, 500 words, 5 points). **So strip-out here is purely a commercial question about who pays,
not a compliance trap** - a materially better position than St Mary's, and worth knowing before anyone
argues it. A clean result is worth as much as a finding: it tells you which argument you are having.

What Gordon Court **does** carry if strip-out lands on us: waste to skips every shift with jL entitled to
remove it and recharge; disposal per **Environment Agency** requirements (Works Information p12);
**gypsum/plasterboard separated before removal** and no burning on site (PCI p8); and *"Restrictions on
Deliveries, **Waste Collection**, Storage - to be discussed and agreed… **at tender stage**"* (PCI p10),
which has passed with nothing agreed.

**THE ACTOR TEST, SHARPENED - AND THIS IS THE REUSABLE PART.** I had told st-marys the giveaway is a phrase
naming the tiers. There is a cleaner test: **go to the Contract Data and read who the parties are.**
jLiving's NEC3 Contract Data states *"The **Employer** is Name: Jewish Community Housing Association Ltd"*
and then *"The **Contractor** is Name: ______"* - **blank, for the tenderer to complete.** That blank *is*
the answer: "the Contractor" means whoever signs, i.e. Chigwell, and Fenster is not a party. No
tier-naming phrase needed. NEC3 → Contract Data; JCT → Articles of Agreement or Contract Particulars.
Read the definitions first, then the obligation.

**AND A REFINEMENT THAT PREVENTS THE OPPOSITE ERROR.** Gordon Court's Works Information uses **both** terms
substantially - *"Main (Principal) Contractor"* **28** times, bare *"The Contractor"* **25** times - so the
mixture is deliberate. But the split is by **scope of duty, not by tier**: "Main (Principal) Contractor
shall" governs site-wide provisions (scaffolding, welfare, builder's work to MEP, surveys) while bare "The
Contractor shall" governs its own works (*"remove **his** waste"*, *"clean the his works"*, *"**his**
Working Area"*). **Both are the same legal person.** So a document switching between "the Contractor" and
"the Main Contractor" is usually drawing a scope distinction, not a tier one - do not read a conflict into
it before checking the definitions. That is the trap I could have fallen into from the opposite direction.

**KEEPING ST MARYS' RESIDUAL, which is sharper on waste than on access.** The head-contract waste duty is
drafted in *"his works"* / *"his Working Area"* language - precisely what a main contractor lifts into a
subcontract order to push waste onto each trade. **The head contract hands Chigwell a ready-made flow-down
clause.** So **RFI-9 stays live**: not because the head contract puts strip-out on us, but because it is
the clause most likely to arrive in Chigwell's order unchanged, bringing the gypsum separation and the
Environment Agency duty with it. Finding that the employer put a duty on the tier above settles the **head**
contract only; the order that reaches us is a different document nobody has seen.

**NEW - THE ITT HAD A FORMAL SLOT FOR OUR EXCLUSIONS AND NOBODY KNOWS IF IT WAS USED. RFI-11.**
The required tender return includes *"**Section 2: Any Caveats and Omissions** relating to your
proposal"*. That is the one mechanism by which our exclusions - access, waste removal, internal finishing,
the PVC-U/aluminium qualification - could acquire standing at head-contract level, and with the
clarification window already shut (~15/07) it was the **last route to the employer**. Our proposal went to
Chigwell 09/07; Chigwell returned 22/07. Whether ours were carried into their Section 2 is unknown and only
Chigwell can say. **General rule: if you are a subcontractor to a main contractor who is bidding on, ask
whether your qualifications went up with their bid.** An exclusion living only in our proposal binds our
client; one carried into their caveats section is visible to the employer pricing the risk.

Manifest now 21 spec_items; run unchanged at **5 FAIL, 2 ASK**. No queue items this turn.


### St Mary's - THE PACKAGE RETURN DATE MOVED TO TODAY AND NOBODY SAW IT (2026-07-27, late)

No work order. `gordon-court` handed back a sharpened version of the actor test - go to the Contract Data
or Articles and read who the PARTIES are, rather than hunting for a tier-naming phrase. Applying it to
St Mary's led somewhere else entirely.

**THE FINDING.** The clean actor test could not be run here: **section 1, the Form of Tender, is not in
the sections Fenster holds** (we have 2, 3 and 4 - the prelims, the schedule of works and the drawings),
so there is no document defining the parties. Going instead to ET&S's **Document Register** - which I had
read three times for what was added when - turned up the header field:

| register | generated | **package return date** |
|---|---|---|
| original-08-07 | 7/8/2026 08:45 | 17 July 2026 |
| schedule-09-07 | 7/9/2026 08:49 | 17 July 2026 |
| pci-16-07 | 7/16/2026 11:43 | 17 July 2026 |
| **revised-24-07** | **7/24/2026 12:10** | **27 JULY 2026** |

**ET&S re-opened the package on 24/07 and moved the return date out by ten days, to today.** Same package
name, same package lead (Tom Godfrey). We submitted on 17/07 against the original date and have recorded
the job as submitted and awaiting award ever since. **REQ-25 raised**, hub deadline corrected from 16/08
to 27/07, job stage changed, and an urgent banner put at the top of `data/jobs/st-marys.md`.

**HOW IT WAS MISSED, WHICH IS THE TRANSFERABLE PART.** Triage's REQ-5 analysis of the 24/07 addendum was
right and was done properly - attribute by attribute across the drawings: 209 window refs, 38 types, 28
opening sizes, restrictor, obscure, U-value and SBD notes, all identical. **The return date is not in the
drawings.** It is in the register header, above the revision table, in a field that had said the same
thing three times. So the addendum check needs a **header diff** as well as a revision-table diff -
package return date, package lead, package name. A re-issue can move a deadline without touching a single
drawing, and it is the one change that cannot be recovered afterwards.

**AND THE SECOND-ORDER ONE, WHICH IS WORTH MORE ACROSS THE BOARD.** The hub had carried this job's
deadline as **16/08** since it opened. That is the **BSW/Bellview 30-day quote validity** - it had quietly
become "the deadline" because it was the only date anyone had written down. **A supplier's expiry is not a
client's deadline.** Asked triage to sweep the other jobs for deadline fields holding inferred rather than
stated dates.

**WHY IT MATTERS COMMERCIALLY.** Six turns of audit on this job have produced a list of things wrong with
a quote already on the client's desk: a door system that cannot meet the specified U-value under any
reading (SMA publish 1.8 against the 1.4 we promised and the 1.2 EDG02 asks - GBP 31,360.15 of sell),
strip-out and manifestation that Adam ruled this evening should be allowed and stated and which are in
neither the price nor the document, a Sheerline casement drawn into a Smart Wall frame, no carriage on a
site 150 miles from where BSW deliver, and the wrong postcode on our own documents. **If the package is
genuinely open until close of play, that list becomes a corrected and qualified tender instead of a
post-mortem.** Mary cannot establish it: outbound email is down (REQ-23) and only ever reached
adam@/marketing@. Somebody has to phone Tom Godfrey today.


### St Mary's - the resubmission drafted against a deadline that is today (2026-07-27, late)

Triage verified the moved return date at source across all four registers and posted it to Adam on the
hub unprompted, since email is still down. So the escalation was done and nothing was left blocked on me
except the thing a human cannot do quickly: write the corrected submission.

**DRAFTED AND WAITING:** `outputs/St Marys Refurbishment - Revised Clarifications for a 27-07
resubmission (draft).txt`. **It changes no figure** - the tendered sum stays at GBP 174,546.37. Eleven
clauses of qualification wording, drop-in for the proposal's clarifications block:

1. **Smart Wall door U-value** stated honestly against SMA's published 1.8 W/m2K, with the 1.4 (schedules
   2376-08/09) and 1.2 (EDG02 area-weighted average) expressly not allowed for, an explanation that a
   compliant door is a system change rather than a glazing change, and an offer to price the alternative.
   MC600 curtain walling carved out as a separate thermally broken system.
2. **Window U-value and solar control** - 1.4 allowed for, EDG02's 1.3 and g-value 0.4-0.3 not, with a
   direct question about which document governs.
3. **Manifestation INCLUDED** at 24.10 linear m over the nine glazed door/screen units per Adam's ruling,
   with Types F and H excluded and priced as a variation if clause 2.24 is read to catch them.
4. **Strip-out** - BOTH wordings drafted, not chosen (see below).
5. **Access** reworded per Adam's ruling and now grounded on Preliminaries clause B rather than presented
   as a conflict.
6. **Delivery and carriage** - flagged as requiring a decision (see below).
7. **Ironmongery** - the panic-bar-versus-"non-lockable device" conflict put back as a question;
   anti-ligature ironmongery and fobbed-reader preparation excluded by name.
8. **Type G** interface subject to manufacturer confirmation.
9. **2376-08 vs 2376-09 rev A** size conflict, which governs.
10. **Price validity**, tied to the 14/09 start and 11/12 completion against 30-day supplier pricing.
11. Everything carried forward unchanged, plus a request that the panic-bar and French-door substitutions
    be accepted expressly this time.

Also corrects **CF77 8HA -> CF47 8HA** on both issued documents.

**TWO DECISIONS DELIBERATELY LEFT TO ADAM.** (a) **Strip-out** - his ruling leaned toward silence
(*"if they assume it's not included and do it for us then happy days"*), so both wordings are drafted and
the recommendation is stated rather than applied: SOW item 1.09 cross-refers strip-out INTO our item 6.01,
so the client's own document already reads as though it is ours, and silence is the weaker position.
(b) **Delivery and carriage** - this one cannot stay silent. Neither supplier includes it, BSW's delivery
address on the quote is Fenster's own Milton Keynes premises, site is ~150 miles away, 107 units, and
there is no carriage line in the pricing document at all. Either a haulage figure or an explicit
exclusion, and no rate for it exists anywhere in our records.

Added to REQ-25 and posted to Adam on the hub as an unprompted note, because the hub is the only outbound
route while REQ-23 is open.

**The shape of the turn is worth recording:** the finding was made last turn, the escalation was done by
triage this turn, and the remaining value was entirely in having the deliverable ready before the answer
comes back rather than after. On a deadline that expires the same day, drafting ahead of the decision is
the only way the decision can still be acted on.


### Gordon Court - sixth turn: the smoke shaft was deleted in October 2025 and the schedules never caught up (2026-07-27, late)

riverside's handoff drove this. Their rule - *the pack names its own compliance route, and the route decides
whether free area is geometric or aerodynamic (AD B prescriptive vs BS 9991 / EN 12101-2 engineered)* - sent
me to the fire strategy drawings, which I had only ever searched for door ratings. No queue items.

**RIVERSIDE'S QUESTION IS CLOSED HERE, WITH A THIRD TERM TO ADD TO THEIR RULE.** Every current fire
strategy sheet carries the duty in the architect's own words: **"AOV. 1.5m² CLEAR OPENING AREA. Automatic
opening vent."** and separately **"SV. NSHEV. 0.4m² clear opening area minimum. Natural Smoke and Heat
Exhaust Ventilator."** *"Clear opening area"* is neither "geometric" nor "aerodynamic" - it is
geometric-side language, and it agrees with the same pack's NBS saying *"1m² **geometric** free area"*
outright. So "clear opening area" and "free area" sit on the geometric side, "aerodynamic free area" / "Aa"
on the engineered side - though riverside's AD B test remains the stronger one because it names the
**route** rather than the quantity.

**THE BIG FINDING - A NEW AND CHEAP CLASS OF CHECK: COMPARE THE REVISION STATUS OF THE DOCUMENT THAT
SCHEDULES AN ITEM AGAINST THE ONE THAT DESIGNS IT.**

> `5244-ARK-14003` and `14004`, **rev 02, 09.10.2025**: *"Updated to suit fire officers comments…
> **Smoke shaft omitted.**"*
> `5244-ARK-14005`, **rev 01, 09.10.2025**: *"Updated to suit fire officers comments. **Smoke shafts
> omitted. Mechanical extract vent added.**"*

Revised three or four more times to **rev 04-06, 17.02.2026**, and never reversed - the current sheets note
a *"Mechanical extract duct through lower ground floor ceiling void"* and the only remaining `Shaft` labels
are 1.1-6.2 m² service and cylinder risers. **Then the dates:**

| Document | Date | Rev |
|---|---|---|
| **Window schedules 52001 / 52002 / 52003** | **08.09.2025** | **"-" never revised** |
| NBS specification 9001 | 23-08-2025 | - |
| **Smoke shafts omitted** | **09.10.2025** | fire officer |
| Door schedule 51001 / fire strategy | 17.02.2026 | rev 01 / 04-06 |

**Both documents that put the 4no "Louvres to smoke shaft" in our scope predate the omission and neither
was updated; the documents that were updated show the shafts gone.** The window schedule still lists them
one per level 0-3 - the classic pattern of louvres serving a vertical shaft - and the NBS still specifies
the whole Colt shaft package (AOV SHAFT *"minimum cross sectional area of 1.5m²"*, DEFENDER SMOKE DAMPERS
*"into prepared openings to lobbies in shaft wall"*, DECORATIVE LOUVRE GRILLES).

**So GBP 4,502.40 of cost / GBP 6,452.40 of sell is scheduled against a shaft deleted five months before
the tender was issued, and the louvre half of REQ-22 has turned from a shortfall into a possible CREDIT.**
The check takes a minute: list every drawing with its revision number and date and look for outliers. A
sheet at rev "-" among rev 04s is stale, and anything it uniquely schedules is suspect. Same failure shape
as triage's deadline-in-a-header find this evening, with the revision **number** instead of the date field.

**A SECOND, INDEPENDENT PROBLEM WITH THE THREE AOVs - THEY MAY BE TOO SMALL.** The duty is 1.5 m² clear
opening. **WN_7 is 910 × 2100 = 1.911 m² gross frame** (BSW's own actual frame 910 × 2075 = 1.888 m²), so
the aperture would have to be **78.5% of gross** - not achievable on the Sheerline *"SP104 70mm Large
Outer"* tilt-and-turn BSW quoted. On the **NSHEV** reading (0.4 m² = **20.9%** of gross) they are
comfortably fine. **Which duty the units serve changes the answer, and the schedule says "AOV".**
Deliberately did **not** compute a clear opening from assumed profile dimensions - that is BSW's figure to
state. **Reusable test: divide the required free area by the GROSS FRAME AREA; anything much above ~60%
should prompt a request for the manufacturer's clear-opening figure rather than an assumption.**

**ADAM'S REQ-9 RULING ONLY HALF TRANSFERS.** His *"we can make the windows as big as we need to… because
the openings are being newly formed"* is genuinely useful but must be checked floor by floor. Gordon
Court's schedules carry *"WINDOW INSTALLATION NOTE - GROUND AND FIRST FLOOR. WINDOWS TO GROUND AND FIRST
FLOORS ARE TO BE INSTALLED TO MATCH THE EXISTING STRUCTURAL OPENING SIZES."* So levels 0-1 are constrained
and 2-3 are new build and free. WL_1 sits at 0/1/2/3, WN_7 at 1/2/3 - a shortfall can be designed out
upstairs but not downstairs without structural work.

**DEADLINE FIELD FIXED, per triage's sweep** - they were right that Gordon Court's was not a client date.
It read **08/08/2026**, AFS Q7585's 30-day validity, and it was a **spent** date as well as a wrong one
because Adam had already decided on REQ-20 to let the supplier quotes lapse. Now **16 September 2026**,
`deadline_basis` **CLIENT-STATED**, from the jLiving ITT timetable - the first date on which anything can
change rather than one we must hit. Our own binding date remains **18/01/2027**. **If your deadline field
is a supplier expiry, check whether the underlying decision has already been taken - mine had been, which
made the date doubly misleading.**

REQ-22 extended with both findings and five new options (12 total), read-back verified. Manifest now 22
spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - seventh turn: my AOV rule of thumb withdrawn, and the pack we priced from was 25 of 82 drawings (2026-07-27, late)

riverside's handoff. No queue items.

**WITHDRAWING MY OWN RULE OF THUMB.** Last turn I offered a ten-second AOV test - divide the required free
area by the **gross frame** area and query anything above ~60%. riverside showed the gross frame is the wrong
denominator, because the sections eat a fixed share of it: **the aperture is the real ceiling.** Recomputed
WN_7 from BSW's own stated figures:

| Basis | Area | vs 1.5 m² duty |
|---|---|---|
| Stated glass 700 × 1865 | **1.3055 m²** | **87.0%** (short 0.1945 m²) |
| Frame-internal aperture 770 × 1935 *(70mm section taken nominally - inferred)* | 1.4900 m² | **99.3%** (short 0.0100 m²) |

**So WN_7 is MARGINAL, not "cannot reach it" as I wrote.** My gross-frame test would have condemned a
borderline unit - the false-alarm failure mode I criticised in two other chats' work the same day. Use
riverside's version: **divide by the aperture.** What survives untouched is that there is still **no
actuator, no 24V motor and no fire-alarm interface** anywhere in the quote; the geometry was never the
substantive point. On the alternative NSHEV reading the glass alone is 3.3× the 0.4 m² duty.

**THE BIGGER MISS: WE PRICED THIS JOB FROM 25 OF THE 82 ARCHITECT'S DRAWINGS.** riverside's "watch for two
layout sets" lesson at scale. The 57 never in front of anyone include **every floor Layout plan** (10001 at
**rev 07**, 10002-10004 at rev 06 - *the most-revised drawings in the pack*), **every Existing plan**
(10010-10012), **all three Demolition plans** (10015 rev 05, 10016 rev 02, 10017 rev 01), **all four
Existing Elevations** (21001-21004) and the **Proposed Elevations** (21005-21008). What the job folder held
instead was the **setting out** plans (11000-11003) and **setting out** elevations (21100-21110) - a
different series with confusingly similar numbers.
**The check is a one-minute scripted diff of job-folder drawing numbers against the zip's.** It complements
the stale-document check: that one finds sheets too **old**, this one finds sheets **missing** - and here the
missing ones were the *newest* documents in the pack. A tidy 25-drawing folder beside an 82-drawing zip is
itself the warning sign.

**AND THE DEMOLITION PLANS ANSWERED THREE OPEN ITEMS:**
- ***"ALL WINDOWS TO BE REMOVED."*** in the notes block of all three. The **RFI-9** strip-out quantity (40
  windows, 62.457 m²) finally has a source - the scope was defined all along on a sheet nobody held.
- Demolition legend includes ***"NEW STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE."*** So which
  openings are new vs existing is **marked there** - the exact floor-by-floor question raised against Adam's
  *"the openings are newly formed"* ruling.
- Ground floor: *"Section of the external wall is to be carefully demolished to allow for the installation
  of **2 no. new double doors**."* Almost certainly the **unpriced 2no D_X pair** (2100 × 1800, every
  descriptive cell blank) - now with a location and a reason.
- First floor: *"**Curtain walling system** (frames, glazing, and fixings) to be removed in sections"* at
  terrace level - on a job titled *"Windows, Rooflights & **Curtain Walling**"* where **we priced no curtain
  walling at all**. Plus *"Demolish **bay windows** and associated brickwork"*, and no bay window type
  appears in our schedule.

**In fairness these are demolition / main-contractor drawings** - they also demolish the external stair and
the entire roof - so most of the content is not ours and I am not claiming it. The finding is that the window
and curtain-wall **removal** scope and the new-vs-existing opening marking were defined on drawings **nobody
who priced this job ever saw**.

**A FOURTH REFERENCED DOCUMENT THAT DOES NOT EXIST IN THE PACK.** All three demolition plans say *"THESE
NOTES MUST BE READ TOGETHER WITH THE DEMOLITION ELEVATIONS TO CONFIRM HEIGHTS AND VERTICAL EXTENTS OF
DEMOLITION."* There is no demolition elevation anywhere in the 82. It joins the **SAP Consultant's
specification** and the **Edward Pearce Consulting Engineers specification**. **Habit worth keeping: when a
drawing tells you to read it with another document, check that document is in the pack - three of four times
on this job it was not.**

**riverside's prior-approval check - looked, cannot answer.** They found their drawings stamped
`24/02303/PAPCR`, a prior-approval reference that would limit external alteration. **No planning reference
exists on Gordon Court** in the DAS's opening pages or the Drawing Register, so it is **unverified** here
rather than answered. The scheme adds two storeys to an existing building for a housing association with a
DAS on file - the profile of a full application rather than a permitted-development conversion - so their
trap is unlikely to bite, but that is a reasoned expectation, not a checked fact.

REQ-22 corrected and extended (17 options, read-back verified). Manifest now 24 spec_items; run unchanged at
**5 FAIL, 2 ASK**.


### Gordon Court - eighth turn: the window tag legend settles new-vs-existing, and neither aperture percentage is a compliance test (2026-07-27, late)

riverside's handoff. No queue items.

**THEIR CAVEAT ACCEPTED AND QUANTIFIED.** They noted an aperture is normally **inferred from a nominal
section depth**, so an aperture ratio is an estimate too and neither of us should derive compliance from one.
Varying only the assumed outer section on WN_7 against its 1.5 m² duty:

| 60mm | 65mm | **70mm** | 75mm | 85mm |
|---|---|---|---|---|
| 1.5445 m² **103.0%** | 1.5171 m² **101.1%** | **1.4900 m² 99.3%** | 1.4630 m² 97.5% | 1.4097 m² 94.0% |

**A ±5mm change in a nominal section swings the answer across the duty line**, between 65 and 70mm. So
"99.3%" is not a marginal pass/fail - it is an estimate whose error bar swamps the margin. **Neither of our
aperture percentages is a compliance test; the clear opening is the manufacturer's figure to state.** What
survives is direction only: the aperture is an **upper bound** on clear opening (the leaf sits within it, and
in tilt mode delivers far less), so short is more likely than not and unprovable.

**THEIR BEST REFINEMENT - "ask which CLASS of drawing answers the thing you are stuck on" - PAID OUT FOUR
TIMES.** We hold the zip, so I read the class rather than requesting it: all 13 elevation sheets, **none of
which were in the job folder anyone priced from**. `21007 rev 03 Proposed South Elevation` carries a
**Windows Tags legend**:

> **WE_00** — Windows in **EXISTING** openings replaced as new
> **WN_00** — Windows in **NEW** openings
> **WL_00** — Louvres to smoke shaft

**The type prefix encodes it.** So the new-vs-existing question I raised against Adam's *"the openings are
newly formed"* ruling - and could not settle for four turns - is answered at **type** level: **40 WE_ in
existing openings, 80 WN_ in new openings, 4 WL_ louvres.**

**A naming convention is usually documented somewhere, and the legend may not be on the sheet you are
working from.** I had inferred "WE = replacement" from context and been right by luck; I had *not* known
that `WN_` positively asserts a **new** opening, which is the more useful fact. **If a schedule uses type
prefixes, go and find the legend that defines them.**

**AND IT HELPS US.** WN_7 - the three AOVs - is a `WN_` type, so those openings **are** newly formed:
Adam's ruling applies here **with pack corroboration**, which is more than riverside could get on their job.
A clear-opening shortfall on the AOVs is therefore **remediable by enlarging the opening** - design
coordination, not a dead end. The missing actuator, motor and fire-alarm interface remain the real cost.
It also **independently confirmed the strip-out quantity**: strip-out scopes to the `WE_` types, which is
exactly the **40 units / 62.457 m²** measured off the workbook *before* this sheet was read. RFI-9 is sound.

**TWO MORE ANSWERS OFF THE SAME SHEETS.** Every proposed elevation carries *"Door and Windows Note - All
external doors, windows and curtain wall mullions in **PPC Anthracite Grey RAL 7016**."* That **answers
RFI-4** (the schedules left it as *"RAL XXX (TBC)"*) and **vindicates BSW**, who assumed 7016; the external
face is now triple-sourced. The internal face remains only in the NBS (RAL 9010 gloss) and the schedules
(PVC-U white), so **the dual-colour requirement stands** and AFS's silence still bites.
And **"curtain wall mullions" named on the East and North elevations** is a **third** independent pointer -
with the enquiry title and the first-floor demolition plan's *"Curtain walling system… to be removed in
sections"* - to **curtain walling being in the design and priced nowhere** in the GBP 368,376.70. Added as a
manifest gap; quantity unknown, as the elevations are 1:100 and no curtain walling schedule exists.

**A SIBLING FAILURE TO THE MISSING-DRAWINGS CHECK: THE SHEET PRESENT TWICE, ONE COPY STALE.** The zip holds
**superseded revisions beside current ones** - 21005/21006/21007 each at **rev 02 and rev 03**, 21008 at
**rev 03, rev 03 (1) and rev 04**. The new-vs-existing annotation exists **only on 21007 rev 03** (5,751
chars vs rev 02's 2,487), so reading the wrong copy would have hidden it. **The drawing-hygiene check now
has three parts:** gaps in the sheet-number series; cross-references to documents not in the pack; and
**duplicate numbers at different revisions**, where you must confirm you are on the later one.

**ONE TENSION LEFT FOR ARKON, NOT FOR US:** the schedules say *"WINDOWS TO GROUND AND FIRST FLOORS ARE TO BE
INSTALLED TO MATCH THE EXISTING STRUCTURAL OPENING SIZES"* yet `WN_` types appear at those levels. The
consistent reading is that the note is a survey caution about retained fabric and a low-level `WN_` opening
is being cut new - which is why the demolition plans mark *"NEW STRUCTURAL OPENINGS"*. **A reading, not a
ruling**, and it decides whether the level-1 AOV can be enlarged. On REQ-22.

REQ-22 now 20 options, read-back verified. Manifest 25 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - ninth turn: the AOV answer splits per unit, and wall-versus-roof is unresolved (2026-07-27, late)

riverside's handoff. No queue items.

**CORRECTING MY OWN ANSWER FROM AN HOUR EARLIER.** I posted that the tag legend settles new-vs-existing -
`WN_` asserts a **new** opening, so Adam's *"make them as big as we need"* ruling applies to the three AOVs.
riverside then found the question **split per vent** on their own two-vent job, and running that here shows my
answer was true but **too coarse to price from**.

**The tag says the opening is new. It does not say what the opening is cut into.**

| Unit | Cut into |
|---|---|
| **WN_7 @ level 1** (Corridor 1-1) | **RETAINED FABRIC** - 10016 rev 02: *"Retained wall to be assessed on site"*, *"Only the existing windows and hanging tiles within this area are to be removed carefully to avoid damage to adjacent retained elements"*, *"Following demolition, new brick slips are to be installed as part of the facade works"*. Enlarging means lintels, cutting masonry, making good - in nobody's price |
| **WN_7 @ levels 2-3** | the **two added storeys** - new construction, size genuinely free |

**So Adam's ruling applies cleanly to two of the three AOVs and only with structural cost to the third.**
On a part-refurbishment a new opening in retained masonry and one in new build are different jobs at different
prices, and a type prefix cannot tell them apart - **the demolition plan can**, because it marks new structural
openings against retained walls.

**RIVERSIDE'S "WALL OR ROOF?" QUESTION IS LIVE HERE AND UNRESOLVED - AND IT IS NOW THE BIGGEST OPEN ITEM ON
THE AOV PACKAGE.** They found their AOV.01 may need a **roof** vent while the supplier quoted a **wall**
casement on a subcill - the wrong product entirely. Here:
- the NBS specifies **two ROOF-MOUNTED** units (*"AXS140 STAIRWELL VENTILATOR... Roof mounted onto horizontal
  kerb... 1m2 geometric free area"*; *"AXS140 LOBBY VENTILATOR... Roof mounted... 1.5m2 geometric"*) plus one
  **WALL-MOUNTED** *"COLTITE GLAZED LOBBY VENTILATOR (STAIR C)"*;
- the fire strategy legend says *"AOV. **1.5m2 clear opening area**"* - the **roof** unit's figure;
- the roof plan carries **two** AOV plan annotations, the first floor **one** (a third instance sits at
  *identical coordinates* on both sheets, so that one is the legend block - worth knowing for positional reads);
- the **smoke shafts** that would have linked lower lobbies to a roof vent were **omitted Oct 2025** and
  replaced by a mechanical extract duct;
- our **3no WN_7 are WALL units** in corridors, tagged **"AOV"** on the window schedule.

**Which duty WN_7 discharges is unknown, and it decides everything:** against the **0.4 m2 NSHEV** they are
comfortable (glass alone is 3.3x); against **1.5 m2** they are marginal and unprovably so; and if the
**mechanical extract** has taken the duty they may be **redundant like the four louvres**. Architect or fire
engineer, not a supplier. **General rule: ask "wall or roof" before accepting a window quote for a vent.**

**RIVERSIDE'S DISTINCTION THAT CLOSES THE APERTURE ARGUMENT, adopted verbatim:** they were **reconciling** a
figure the supplier had stated; I was **predicting** an unstated one. Their reconciliation holds across a wide
range of assumed sections because the test is whether it hangs together; my prediction flipped across the
compliance line on 5mm because the test was pass-or-fail. **Reconciling a stated number is robust; predicting
an unstated one is not. Use the arithmetic to understand what a supplier has told you, not to decide whether
they comply.**

**ONE CHECK REPORTED AS NOT RUN.** riverside's untagged-glazing test is good and is **not executable on this
pack by text extraction** - only `21007 rev 03` yields any window tags; the other three proposed elevations
return none, so tags live in the CAD graphics layer. It needs the elevations **rendered and read visually**.
Logged as not done rather than reported as reconciled - the same discipline as the registry and request-id
episodes: the print statement is not the evidence.

REQ-22 now 24 options, read-back verified. Manifest 27 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - tenth turn: read the WALL TYPE tag, not the window tag (2026-07-27, late)

riverside's handoff. No queue items. **I rendered the proposed elevations - the job I had logged as NOT RUN -
and it undermines the instrument I had posted to the board twice.**

**THE FINDING.** `21007 rev 03 Proposed South Elevation` carries a **WALL TYPE LEGEND** whose first entry is
**"EXT - Existing wall types as surveyed"**, distinct from the new build-ups `WT-A0 Brickwork / Cavity
Insulation / Block`, `WT-A1 Brickwork / Insulation / Stud`, **`WT-A2 Zinc standing seam / Insulation / Stud`**.
On the elevation the **top storey is called up WT-A2** and the one below **WT-A1** - both **stud** build-ups,
i.e. new construction, matching the ITT's two new storeys added to a two-storey building.
**And the windows on those two new storeys are tagged `WE_2`.**

A window *"in an existing opening replaced as new"* cannot sit in a newly built zinc-standing-seam-on-stud
wall, and `WE_2` appears on the retained lower storeys too. **So `WE_`/`WN_` is a SCHEDULE reference** - 52002
*"Replacement Windows"* carries WE_, 52003 *"New Windows"* carries WN_ and WL_ - and the legend's wording is
the architect's gloss on those two schedules, not a rule the drawing enforces.

**WITHDRAWN:** my eighth-turn claim that the prefix encodes opening condition. My ninth-turn 2-of-3 split may
still be right but **no longer rests on the tag**.

**WHAT REPLACES IT IS BETTER THAN ANYTHING POSTED ON THIS: READ THE WALL TYPE TAG.** `EXT` versus `WT-*` is the
architect's **own** distinction between surveyed existing fabric and a new build-up, called up on the elevation
**immediately beside the window**. It answers riverside's **layer 1** (new or existing opening) *and* **layer 2**
(what fabric it is cut into) in **one read, without the demolition plan**, because it describes the actual
construction at that point in the facade - which neither the window tag nor the floor level does.

**FOR THE THREE AOVs THIS MAKES THINGS LESS SETTLED, NOT MORE.** No elevation in the pack tags `WN_7`, so their
fabric is **not established**; someone must identify which facade each corridor vent sits on and read the wall
type there. Ten minutes for whoever holds the set, and now a **prerequisite to pricing those openings**.

**riverside's untagged-glazing check, RUN, and broader than the check anticipated: THREE OF THE FOUR PROPOSED
ELEVATIONS CARRY NO WINDOW TAGS AT ALL** - 479 words each against the South's 975, confirmed on both pdfplumber
and PyMuPDF. So the elevation set does not **locate** the window types: on three of four faces you cannot verify
which opening is which, and nothing anywhere tags the 3no AOVs, the 4no louvres or the 2no unpriced D_X doors.

**THE THREAD, RECORDED PLAINLY:** three successive answers, each narrower than the last - (1) the tag legend
settles it; (2) the tag says new but not what fabric; (3) the tag does not reliably say new either, read the
wall type. **Only the third is safe to price from.** Each correction came from another chat running my own check
back at me, and the last only came because I went and did the render rather than leaving it on the outstanding
list. **Logging a check as NOT RUN is worth something only if somebody then runs it.**

REQ-22 now 27 options, read-back verified. Manifest 27 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - eleventh turn: what the existing walls are made of, and who owns the cavity (2026-07-27, late)

riverside's handoff. No queue items.

**THEIR DISTINCTION, ADOPTED AS A WORKING PRACTICE: when you take something from another chat, separate THE IDEA
from THE TOOL.** They withdrew their own *"size is genuinely free"* on my **principle** (a new opening is not a
free opening - ask what it is cut into), never on my **instrument** (the WE_/WN_ prefix), because their pack has
no such convention for the tool to break. So my withdrawal cost them nothing. The two travel together in a
handoff and usually only one transfers - **state which is which when posting, and check which you took when
acting.**

**THEIR OPEN LIMIT LANDS ON ME TOO: "knowing a wall is existing is not the same as knowing you can cut it."** My
legend's first entry is `EXT - Existing wall types as surveyed` - which defers rather than describes, exactly as
theirs does.

**AND THE ANSWER IS IN THE PACK - IN THE STRUCTURAL ENGINEER'S FOLDER, NOT THE ARCHITECT'S SET.**
`Gordon Court_2025-059_sk01&02 Brick & mortar sampling locations.pdf` (Elite Designers, 12/05/2025):

> *"Brick & mortar sampling in the **internal solid wall**. Brick & mortar sampling in **cavity wall**. Take
> samples from **both the inner and outer leaves** of the cavity wall. Restore sample points using matching
> materials."*

So existing external walls are **cavity, two leaves**; internal walls are **solid**. That is what decides the
lintel type, which leaf you fix to and the cost of forming an opening. The same sub-folder holds GPR location
drawings, a **resin injection methodology** (Teretek - and it notes *"load for the new columns to be taken onto
existing masonry at second floor level"*, so the old masonry is being loaded, which constrains where you can
cut) and an Engineering & Workmanship Specification with **5.3 Cavity walls** and **5.7 Lintels**.
**Asking the architect for a wall build-up and asking the structural engineer for the investigation drawings are
two different requests** - on a refurbishment the second is usually where the answer is, because somebody had to
sample the masonry before designing anything.

**A CLEARED ITEM RATHER THAN A FINDING - CAVITY CLOSERS ARE NOT THE GLAZING SCOPE.** I nearly raised them as a
gap. They sit in **NBS F30 *"Accessories/ sundry items for brick/block/stone walling"*** - a masonry section:
ROCKWOOL **fire-rated cavity closer EWS-901** (Euroclass A1, U-value 0.14 W/m2K); **METZ Non-Combustible EaZi-Fit
A1 cavity trays** (BBA 22/5997, **to fit cavity width 195 mm**, 300mm high); jamb DPCs at openings; trays
extending 150 mm beyond lintel ends; wall ties within 225 mm of reveals. **Zero mentions across all four BSW
quotes - correctly so.** **Check which NBS section an accessory sits in before deciding it is missing from your
price.**

**BUT ONE ITEM OFF THE SAME READ IS OURS, AND IT SHARPENS THE GBP 506.37 OMISSION.** **NBS L10 cl.790
"Fire-resisting frames": *"Gap between back of frame and reveal: Completely fill with INTUMESCENT mastic or
tape."*** L10 is the windows section. AFS describe the omitted GBP 256.37 fixing pack as *"screws, foam, packers,
**mastic**"* - ordinary mastic. **So the line I have been reporting as an omission may not COMPLY even once
bought**: an intumescent perimeter seal is a different product at a different price and it is a fire-rating
requirement, not a finish. Added to RFQ-2. **If you have fire-rated frames, grep the quote for "intumescent" - it
hides inside a fixings line.**

Manifest now 29 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - twelfth turn: RFI-3 CLOSED - Edward Pearce wrote the Energy Statement (2026-07-27, late)

riverside's handoff. No queue items.

**THEIR CHECK:** *if you cannot find the consultant who owns a deferred requirement, check whether one has been
appointed at all.* On Riverside **no structural engineer is named anywhere** on any of the six drawings, so the
opening Adam authorised enlarging has neither a structural design nor a price behind it. Ran it on my two
outstanding deferrals and got the **opposite** answer - which is what makes the pair useful.

**THE ENERGY STATEMENT'S TITLE BLOCK:** *"Edward Pearce, Old School House, 35 Ewell Road, Surbiton, Surrey KT6
6AF - Project No. **22/190**, February 2025, Revision 02."* **That project number is the same as every M&E
document in the pack** - `22190-M01…M32` mechanical, `22190-E01…E25` electrical, the 140pp mech spec, the 127pp
electrical spec, the drainage spec. So Edward Pearce are the **appointed** services and energy consultant, and
the architect's deferral *"MIN. THERMAL RATING: To Edward Pearce Consulting Engineers specification"* points at a
document **held since turn one**. **RFI-3 is closed by reading a title block.**

**THE NUMBERS, FINALLY SETTLED:**
- **Glazing 1.10 W/m2K** - Edward Pearce's headline (*"replaced or improved to achieve a U-value of 1.1 W/m2K"*)
  and their existing-to-proposed tables (1.60 -> 1.10 in both scenarios). **Tighter than the NBS's 1.2**, and it
  governs because the schedules expressly defer thermal rating to them.
- **g-value 0.36** - the architect states it **directly** against Edward Pearce's 0.40. **A directly stated
  requirement beats a deferred one**, so the architect governs the g-value and the consultant governs the U-value.
- **Doors 1.2 W/m2K** - NBS L20 cl.280 stays the door figure. Edward Pearce also give *"Opaque Door 1.00"* but in
  SAP an **opaque** door is a **solid** door and ours are glazed EI30 units, so they sit under glazing at 1.10.
  **Did not take the 1.00** - reading a term of art loosely would have invented a requirement.

**RFI-7 NARROWS, and the consultant's own document says why.** NBS cl.330 defers g-value, frame factor and
glazing details to a *"SAP Consultants specification"*; Edward Pearce **are** the SAP consultant (*"Design SAP 10
and IES VE"*, *"Baseline SAP and SBEM calculations"*). But they write *"Full SAP calculations for each scenario
and the GLA reporting spreadsheet **will be submitted in a separate file**."* So it is held elsewhere by design -
the RFI becomes **"please issue Edward Pearce's SAP calculations"**, a request to a named party for a document
known to exist.

**THE RULE THE PAIR OF JOBS PRODUCES:**
- deferral to a **named, appointed** consultant whose other work is in the pack = **administrative gap**. Ask for
  the document, price on, qualify if it does not arrive.
- deferral to **nobody** - no consultant named, everything *"to be site agreed"* = **design gap**. No document to
  ask for, and this is the one that should stop you pricing.

Same words on the drawing, entirely different problem. **Spend two minutes establishing which you have before
raising a deferral as a finding.**

**AND A HABIT off riverside's point that a false withdrawal costs as much as a false finding:** when I pulled the
window-tag instrument I kept the principle explicitly and left the D_X, strip-out, manifestation and smoke-shaft
findings alone, because none used the tag. **When you withdraw something, say what you are NOT withdrawing** -
otherwise the next chat retracts work that never depended on the broken part.

Manifest 29 spec_items, `u_value` now resolved rather than open; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - thirteenth turn: no fire engineer exists, and the title blocks give a routing table (2026-07-28)

riverside's handoff. No queue items.

**THEIR CHECK CAUGHT ME MAKING THE MISTAKE THEY HAD JUST CAUGHT THEMSELVES MAKING.** REQ-22 carried the option
*"Ask the **fire engineer** whether the corridor AOVs are wall vents or the roof-mounted AXS140 units."*
**There is no fire engineer.** Across all five fire strategy drawings (14001-14005) there is no fire engineer,
fire consultant, approved inspector or building control body named - only **"Arkon" x5 per sheet** (the
architect's own title block) and **"fire officer" x1**, inside a *revision note* (*"Updated to suit fire officers
comments"*, 09.10.2025), not an appointment.

So the fire strategy is **the architect's own work**, as is the NBS specifying the Colt units - the same firm
wrote both the *"AOV. 1.5m2 clear opening area"* legend and the *"AXS140 STAIRWELL VENTILATOR... roof mounted"*
specification. **The question goes to Arkon, with the fire officer as arbiter**, since their comments deleted the
smoke shafts. Option corrected on the request.

**THE BIGGER YIELD - A ROUTING TABLE, FROM TEN MINUTES OF READING TITLE BLOCKS.** I had been addressing **eleven
RFIs to "Chigwell"** when most are **design** questions the main contractor does not own:

| Owner | Job no. | Contact | Questions |
|---|---|---|---|
| **Arkon Associates Ltd** - schedules, elevations, fire strategy AND the NBS | **5244** | +44 (1438) 359816 · enquiries@arkonassociates.co.uk | D_T · D_X · manifestation extent · AOV wall-or-roof · rooflight/Colt boundary |
| **Edward Pearce** | **22/190** | 020 8390 6244 | the SAP calculations |
| **Elite Designers Ltd** | **2025-059** | - | wall build-up at new openings |
| **Chigwell** | | | strip-out allocation · Section 2 caveats · the GBP 723.87 addendum |
| **Fire** | | | **nobody named** |

We cannot approach any of them directly - the route is via Chigwell - but **naming the author, job number and
sheet lets them forward a question in one step instead of working out who owns it.** *"Please issue the 5244
drawing register and the 57 sheets we do not hold"* is actionable; *"the rest of the pack"* is not.

**THE CONTRAST BETWEEN THE TWO JOBS IS NOW COMPLETE, and it is what makes the test worth running.** Gordon Court
names a full design team and **every deferral chased turned out to be administrative**. Riverside names a heating
engineer and an electrician as *roles* and defers the rest to parties not yet appointed, so **four of their five
are design gaps**. Same test, opposite results - and it tells you whether to chase paperwork or raise an alarm.

**"SAY WHAT YOU ARE NOT WITHDRAWING", RUN ON MYSELF.** After three self-corrections the record should be
unambiguous, and writing it out put this job's position in one place for the first time since the corrections
started. **Withdrawn:** the window tag prefix as an instrument; the "60% of gross frame" rule of thumb; the claim
that WN_7 *"cannot reach"* 1.5 m2. **Standing (18 items, none dependent on those three):** the GBP 723.87
omission · the intumescent seal point · D_T · D_X · the deleted smoke shafts and possibly-redundant louvres · the
missing actuators · 4000mm2 vents against 8000 · acoustic vents on 26 of 40 windows · PAS 24 absent from four
quotes · no whole-window Uw against 1.10 · delivery in nobody's price · manifestation 15.002 lin m · strip-out
62.457 m2 · curtain walling on three pointers · 25 of 82 drawings · the shut clarification window · the 180-day
gap (Adam *decided* it, I did not withdraw it) · the Section 2 caveats question. Full list at job file section 4K.3.

REQ-22 now 29 options, read-back verified. Manifest 30 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - fourteenth turn: what the 18 findings are worth, and two entries in my own routing table were mentions (2026-07-28)

riverside's handoff. No queue items.

**THEIR SHARPENED TEST - *is each hit a TITLE BLOCK (appointment) or a NOTE (mention)?* - CAUGHT TWO ERRORS IN
THE ROUTING TABLE I POSTED AN HOUR EARLIER.** I had listed **BSEC** (electrical) and **Engdesign** (heating) as
consultants. Both appear **only in architect's schedule note text** - *"REFER TO BSEC ELECTRICAL LAYOUTS"*,
*"REFER TO ENGDESIGN DRAWINGS"* - and **neither authored anything in the pack**. Both the 140pp mech spec and
the 127pp electrical spec carry **Edward Pearce LLP** title blocks with **zero** BSEC/Engdesign hits.

Likeliest reading: **they were superseded by Edward Pearce and the schedule notes were never updated** - and
those schedules are the **08.09.2025 revision "-"** sheets that have never been revised. **So it is a second,
independent symptom of the staleness that hid the smoke-shaft omission.** The two checks find the same disease
from different ends: a note naming a superseded consultant and a schedule listing a deleted smoke shaft are both
*"nobody re-read the notes panel when the design moved"*. **If a pack has one, look for the other.**

**WHAT THE 18 FINDINGS ARE WORTH - twelve carry money and only two can be totalled:**

| | |
|---|---|
| **HARD** | AFS extras GBP 506.37 + BSW "PANEL SET UP" GBP 217.50 = **GBP 723.87** |
| **POSSIBLE CREDIT** | 4no louvres to the deleted smoke shaft: **-GBP 6,452.40 sell** |
| **BENCHMARK ONLY** | D_X x2 ~GBP 5,600 sell · AOV actuators ~GBP 4,988-5,667 supply |
| **UNPRICEABLE (8)** | manifestation 15.002 lin m · strip-out 62.457 m2 · trickle upgrade 124 windows · acoustic vents 26+ · intumescent seal 3 doors · PAS 24 124 windows · curtain walling qty unknown · carriage 227 units |

**The reason is structural:** of `supplier-rates.json`'s **80 categories, ZERO** carry acoustic, trickle vent,
Linkvent, Passivent, curtain walling, actuator, AOV, strip-out, disposal, manifestation or intumescent.

**THE SYSTEMIC FINDING.** The board already carries four missing-category notes - folding doors, vertical
sliders, secondary glazing, AOV/smoke vents. Gordon Court adds **five: strip-out and disposal, manifestation,
acoustic trickle vents, intumescent seals, curtain walling.** The first four were unusual **products**; these
five are the **ancillaries on nearly every refurbishment**. **The register does frames and glass properly and
carries almost nothing for the work around the window** - so on a refurb we can price the windows and none of
the work around them, which is exactly the shape these 18 findings have taken.

**AND THE PRACTICAL HALF - eight of the twelve are SUPPLIER questions, so they do not wait for jLiving.**
One RFQ to BSW covers six plus the missing whole-window Uw; one to AFS covers two. **Two emails convert eight
unpriceable items into real numbers.** Raised as **REQ-26** (id computed at write time - it allocated 26, not the
25 I would have hardcoded, because another chat had taken 25 mid-turn; st-marys' pattern earned its keep).
**When a job stalls waiting on a client, check which open items are actually supplier questions.**

**CANDIDLY, as riverside did about their own turn:** the tendered figure has not moved and will not until
jLiving decide. What changed is the classification, the reason for the unpriceable ones, and a two-email route
to closing eight. **The BSEC catch is a genuine new finding; the rest is making an existing position
actionable.** Worth saying which is which.

Manifest 31 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - fifteenth turn: REQ-26 has nine days, and curtain walling was not unpriceable (2026-07-28)

riverside's handoff. No queue items.

**THEIR DECAYING-WINDOW ARITHMETIC GAVE MY OWN REQUEST A DEADLINE I HAD NOT NOTICED.** Their rule: *supplier
expiry minus your own validity period gives the date your cover ran out.* Theirs was yesterday. Mine is already
issued, so it lands differently - and harder:

| Quote | Dated | Lapses | Days |
|---|---|---|---|
| BSW QT252247/48/51/57 | 07/07, 30 days | **06/08/2026** | **9** |
| AFS Q7585 | 09/07, 30 days | **08/08/2026** | **11** |

REQ-26 asks for two supplier RFQs to price the eight items nothing in our system can price. I raised it as
*"does not need to wait for jLiving"* and left it there. **What I had not stated is that it has nine days.**
An RFQ landing while the quotes are live is an **addendum to a live quote** - same job, same schedule, same
rates, they add lines. After the lapse there is nothing to add to: both come back as **fresh quotes at autumn
rates with no anchor**.

**THE GENERAL FORM:** *a lapsing supplier quote is not only a price risk, it is a deadline for every question
you still want to ask that supplier.* Before expiry it is an addendum; after, a new enquiry. **If you are
sitting on unpriced scope, the date their quote dies is the date your cheap answer dies with it.**

**AND IT DOES NOT REOPEN ADAM'S REQ-20 DECISION** - he accepted inflation risk on the **GBP 201,086.70 that
already has a price**, not on eight items that do not. Issuing this week asks nobody to hold anything. *Worth
doing generally: when raising something adjacent to a decision already taken, say which part you are not
touching.* REQ-26's title and the job status now carry the 06/08 date.

**A CORRECTION TO MY OWN LIST, prompted by riverside correcting theirs about the tooling.** I listed **curtain
walling** among eight *"unpriceable"* items. **Wrong** - `mary_pricing.py` carries `CW_SUPPLY_M2 = 850.0` and
`CW_LABOUR_M2 = 150.0` (*"curtain walling convention... [Greenfields, 22/07/2026]"*). **It has a rate; what it
lacks is a quantity** (elevations at 1:100, no curtain walling schedule) - the **opposite** problem, and it
changes who to ask: **an AREA from Arkon, not a price from BSW.**

Their fuller correction, adopted verbatim: *"the register has nothing"* was too strong of me - **standing house
rates do exist outside the register** (mastic GBP 5/lm, EPDM GBP 25/m2, install default GBP 140/unit). The
accurate statement is that **the register does frames and glass to size-banded, supplier-attributed depth, and
the ancillaries have either a single flat house rate or nothing.** On this job the nearest analogue still does
not help: external mastic is GBP 5/lm and already carried as the GBP 5,622.81 optional, but that is **weather**
mastic - the **intumescent** seal cl.790 requires is a different and dearer product with no rate anywhere.

**CORRECTED SHAPE OF THE TWELVE MONEY FINDINGS:** 2 hard (GBP 723.87) · 1 possible credit (-GBP 6,452.40) ·
2 benchmark-only · **1 rate-but-no-quantity (curtain walling)** · **7 unpriceable**.

Manifest 31 spec_items; run unchanged at **5 FAIL, 2 ASK**.


### Gordon Court - sixteenth turn: our own proposal caps the exposure at 30 days, and three exclusions were doing work they should not (2026-07-28)

riverside's handoff. No queue items.

**A CORRECTION TO MY LONGEST-RUNNING NUMBER.** Since turn one I have reported **163 days of unqualified
exposure**, and Adam accepted that risk on REQ-20. **Page 8 of the proposal we issued carries a clause I had
never read:**

> *"**2. Quotation Validity** - All quotations provided by Fenster Glazing & Locks Ltd are **valid for 30 days
> from the date of issue**, unless agreed otherwise."*

So on our own terms the GBP 368,376.70 **expired 08/08/2026**, while jLiving's Form of Tender holds the
**tender** to 18/01/2027. The distinction that matters: **we are not a party to that Form of Tender** - Chigwell
signed it, our contract is with Chigwell, and our document says 30 days.

**Being fair about its weight:** Chigwell priced our number into a bid committed for 180 days and will expect us
to honour it, and a subcontractor's validity clause is routinely overridden by an order - so it is a
**negotiating position, not a shield**. But it is in writing, it was issued, and the exposure is **qualified
rather than absolute**. **This does not reopen REQ-20** - it supplies a fact Adam did not have. It also sharpens
**RFI-11**: if our terms went up with Chigwell's Section 2 caveats the clause is visible to jLiving; if not,
Chigwell absorbed it silently. **General rule: check your own terms and conditions page before reporting a
validity gap - the answer may be in the document you sent.**

**THREE DATES, ANSWERING DIFFERENT QUESTIONS** (riverside's arithmetic, runnable now I have our validity):

| Date | Question | Status |
|---|---|---|
| **07/07/2026** | last date we could have issued and been covered by BSW (06/08 - 30 days) | **already behind us - we issued 09/07. We were never covered** |
| **06/08 / 08/08** | when we can no longer ask either supplier cheaply | 9 and 11 days |
| **08/08/2026** | our own quotation expires on its own terms | 11 days |

**After 08/08 nothing on this job is held by anybody.**

**AND RIVERSIDE'S RATE-VS-QUANTITY SORT, RUN OVER THE EXCLUSIONS LIST RATHER THAN THE FINDINGS.** They caught
window restrictors sitting in an exclusions list when they were an unanswered supplier question. **Three of our
twelve are doing work they should not:**

- **"Fire Stopping - To be done by others, if required"** **conflicts with NBS L10 cl.790**, which puts the
  intumescent frame-to-reveal seal in the **windows** section - our package. Cavity barriers are the main
  contractor's; that perimeter seal is not. 3 doors, no rate, **owner AFS**.
- **"Testing - On or off site testing"** **does not cover NBS cl.205's** *"Independent, 3rd Party Certification
  Schemes"* and *"documentation confirming Certifications claimed"* - certification is documentation the maker
  already holds, **not a test**. **Owner BSW**, probably free if they hold the certificates.
- **"Site Storage - Materials will be delivered to site"** **asserts a fact no quote we hold supports** - all
  five deliver to our own MK13 9HF yard.

**And a distinction rather than a conflict:** *"Design Responsibility - design calculations excluded"* fairly
covers us **producing** a Uw calculation but does not get us the **figure**, which BSW should state as a matter
of course. **Excluding the work is not the same as not needing the number.**
*"Structural Alterations - by Main Contractor"* is consistent with the head contract. **Genuine, cleared.**

**The transferable form: "we exclude X" is only safe if X is genuinely somebody else's under the spec.** Three
of ours were either contradicted by a clause in our own package's NBS section, or asserted a fact our suppliers
do not support.

Manifest 31 spec_items; run unchanged at **5 FAIL, 2 ASK**. REQ-26 now 12 options, read-back verified.


### Gordon Court - seventeenth turn: WITHDRAWING a turn-one finding, all seven lines ARE quoted (2026-07-28)

riverside's handoff. No queue items.

**THEIR GENERATOR-FOOTER CATCH MADE ME CHECK MY OWN SOURCES, AND I HAVE WITHDRAWN A FINDING CARRIED SINCE TURN
ONE.** Since July I have reported - job file, checks manifest, both handovers, the board - that **GBP 5,597.89
across seven lines had "no supplier quote behind it"**, citing Brocks Hill. **All seven are quoted, at exactly
the workbook costs.** WN_4, WN_6, WN_8 and WN_9 are priced lines on QT252247; D_B 1055 is on QT252251 at 1720
rather than the schedule's 1750; and **D_E and D_U are each split across two BSW lines** (casement + door)
summing to the workbook figure to the penny.

**Why: I used the workbook's R column as the test of whether a supplier line existed.** It is a
partially-filled working column - blank where a unit was quoted at a different size or split across two lines -
and I read blank as "no quote". **Reading the two PDFs took four minutes.**

**THE LESSON, three times over in one night: a working column, a print statement and a generator footer are the
same thing - a representation of the source, not the source.** riverside quoted a validity off
`generate-fenster-docs.py`; st-marys had a print statement report a request raised that never existed; I built a
standing finding on a half-filled column. One error in three costumes.

`check_supplier_covers_quantity` now **PASSES** - *"43 lines fully covered by a supplier quote"* - and the job
drops from **5 FAIL to 4**. One of my five was bogus and had been since July.

**WHAT IS ACTUALLY THERE - SIX DIMENSIONAL DISCREPANCIES:**

| Ref | Schedule | Quoted | |
|---|---|---|---|
| **WN_4** | 1360 x 1656 | 1360 x 1935 | **+279 height** |
| **WL_1** x4 | 1210 x 2100 | 1307 x 2197 | **+97 in BOTH axes** |
| D_B 1055 | 1055 x 1750 | 1055 x 1720 | -30 height |
| **D_E** | 1500 x 2100 | 500+1055 = 1555 | +55 width *(split)* |
| **D_U** | 1405 x 2170 | 500+1000 = 1500 x 2100 | +95 width, -70 height *(split)* |
| D_T | 1600 x 2110 | 1600 x 2210 | +100 height |

riverside's survey-clause find **qualifies but does not remove** these: our T&Cs say *"subject to final site
survey and measurement verification"* and the architect requires *"a FULL SITE MEASUREMENT SURVEY"* and *"NO
FABRICATION SHALL PROCEED BASED SOLELY ON DRAWING DIMENSIONS"*. **But +279mm, and +97mm in both axes, exceed a
survey tolerance** - a frame 97mm bigger than the hole in both directions is a different unit, and a cill only
adds height. Those go in the BSW RFQ, not to the surveyor.

**AND A NEW CHECK: VERIFY A SPLIT UNIT'S COMBINED SIZE AGAINST THE OPENING.** BSW read D_E and D_U as
door-plus-sidelight assemblies - a sensible reading of a schedule that marks sidelights - and **both combined
widths are over**. The cost tied to the penny, which is why nobody looked. **That is Brocks Hill inverted:
there, reconciling the total hid a missing quantity; here it hid a wrong dimension.**

Manifest 32 spec_items; run now **4 FAIL, 2 ASK**.


### Gordon Court - eighteenth turn: clause 16 splits every finding into ours-to-fix and ours-to-ask (2026-07-28)

riverside's handoff. No queue items.

**THEIR AUDIT:** they had reported *"the OneDrive job folder is empty"* five times off a search against a folder
name that does not exist - **a failed search is not evidence of absence**. Following the rule properly they then
compared the real cover letter against `templates/proposal-content.json` and found the extraction **faithful but
half the length** (76 paragraphs against 153), missing the clause that mattered most to them. **An extraction can
be faithful and still incomplete.**

**RAN THE SAME CHECK HERE - CLEAN.** Proposal `.docx` (56 paragraphs + 5 tables, 15,708 chars) against the issued
`.pdf` (15,893). They match. **And one false alarm of my own, stated because I nearly posted it:** I briefly had
*"structural openings are fully formed"* as docx-only. It is in both - the two-column inclusions/exclusions table
interleaves the text, so it reads *"Site Survey - Only conducted once the structural openings **Fire Stopping -
To be done by others** are fully formed"*. My own extraction artefact, the same trap the door schedules set on
turn one.

**BUT THEIR CLAUSE IS IN MY PROPOSAL TOO, AND I HAD NOT READ IT IN EIGHTEEN TURNS:**

> ***"16. Design Responsibility** - Fenster Glazing & Locks Ltd is not responsible for overall design intent,
> architectural suitability, or **regulatory strategy** and relies on information, drawings, and specifications
> provided by the client or their professional team. **Responsibility is limited to measurement verification,
> supply, and installation of the agreed glazing systems.**"*

**IT IS A THIRD SORT, AND IT ANSWERS A DIFFERENT QUESTION FROM THE OTHER TWO.** Priced/benchmark/unpriceable
tells you what you can cost; rate-versus-quantity tells you who to ask; **this tells you whose responsibility it
is under our own terms - and therefore whether a finding belongs in a supplier RFQ or a client qualification.**

| Under clause 16 | Findings |
|---|---|
| **Regulatory strategy - theirs, we rely** | which duty the AOVs serve · whether the smoke-shaft omission removes the louvres · the 1.10 W/m2K and 0.36 g-value targets · PAS 24 · 8000mm2 trickle vents · acoustic vents · manifestation extent |
| **Expressly OURS, retained by the same clause** | **measurement verification** -> the six dimensional discrepancies · **supply of the agreed glazing systems** -> whether we quoted the specified product |

**AND IT IS NOT A GET-OUT - the AOV shows why it splits.** *"Is 1.5 m2 the right duty, wall or roof?"* is
regulatory strategy and **theirs**, so the exposure is *"we relied and we asked"*. *"Did we quote the specified
product?"* is **supply and ours** - BSW quoted a plain Prestige T&T and a plain casement where the NBS names a
**Colt motorised ventilator with a 24V actuator**, and clause 16 does not touch that. Same split on thermal: the
1.10 target is theirs; obtaining a whole-window Uw from our supplier is ours.

**AND IT TIGHTENS THE DIMENSIONAL FINDINGS RATHER THAN LOOSENING THEM.** Clause 16 expressly *retains*
measurement verification, so the six discrepancies are ours twice over - clause 2 (*"subject to final site survey
and measurement verification"*) and clause 16. **The survey makes them fixable; it does not make them somebody
else's.** Tempering what I took from riverside last turn.

**Practical effect:** ours-to-fix -> the BSW and AFS RFQs (REQ-26); theirs -> the post-tender qualification to
Chigwell, framed as **reliance** rather than as defects. Two documents, two tones.

Manifest 33 spec_items; run unchanged at **4 FAIL, 2 ASK**.


### Gordon Court - nineteenth turn: the three documents are drafted, split by clause 16 (2026-07-28)

riverside's handoff. No queue items.

They verified the clause numbering independently (twenty clauses; 2 Quotation Validity, 16 Design
Responsibility - so we have it from two documents) and applied the sort to their brief *"with the reasoning
printed at the foot of it"*. **The equivalent here was overdue: REQ-26 had nine days and no text behind it.**
st-marys' rule applies - *draft the deliverable before the decision comes back, not after*.

| Document | Deadline |
|---|---|
| `outputs\Gordon Court - RFQ to BSW (draft, send by 06-08).txt` | **06/08** |
| `outputs\Gordon Court - RFQ to AFS (draft, send by 08-08).txt` | **08/08** |
| `outputs\Gordon Court - post-tender queries to Chigwell (draft).txt` | before 16/09 |

**Split by clause 16, with the reasoning at the head of each.** Supplier letters take what our terms make
**ours** - measurement verification, supply of the agreed system, and figures the supplier holds. The Chigwell
letter takes what clause 16 puts on the **client's professional team**, worded as questions and reliances.

**WRITING THEM IS WHERE THE SORT EARNED ITS KEEP.** Agreeing with clause 16 in the abstract is easy; drafting
forces each finding into one document or the other, in words. The biggest finding ended up in **both**, split:
to BSW, *"your quotation is a Prestige T&T with no reference to an actuator, motor, chain, stroke or 24V supply
- please either price the specified motorised ventilator or confirm it is outside your scope"*; to Chigwell,
*"please confirm which duty applies and whether the position is a wall or a roof vent"*. One is an instruction
about a product we buy; the other a question about a duty we do not set.

**TWO DRAFTING CHOICES WORTH KEEPING:**
- **Ask a supplier what they priced against, not why they got it wrong.** The AFS door is quoted 100mm taller
  than the opening - but our source is the same never-revised schedule that still shows a deleted smoke shaft.
  The letter asks *"was 2210 taken from information we supplied?"* and says *"we accept the schedule may be
  wrong rather than your quotation"*.
- **When a decision has been taken, say so in the document.** Adam decided we hold the price. The Chigwell
  draft states we are content to honour the tendered figure and are not seeking to withdraw it, raising the
  30-day clause only to put it on record and ask whether our terms reached jLiving via Section 2. **A draft
  that quietly reopens a decision its author accepted is worse than no draft** - flagged to Adam that the
  paragraph is last and deletes cleanly.

Each Chigwell question also carries its **owner and sheet** (Arkon 5244, Edward Pearce 22/190) and notes that
we know the clarification window closed ~15 July - turning *"here are ten problems"* into *"ten questions, each
addressed to whoever can answer it"*.

**Nothing is sent** - ghost protocol, and `mary_send` is 403'd. A human sends all three.

**Candidly:** the figure is unchanged at GBP 368,376.70 and jLiving do not announce until 16/09. What moved is
that the nine-day item stopped being a request for somebody to write two emails and became two emails somebody
can read and send.

REQ-26 now 15 options, read-back verified. Manifest 33 spec_items; **4 FAIL, 2 ASK**.


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

### Gordon Court - twentieth turn: the elevations rendered, and a turn-one glass reference withdrawn (2026-07-28)

riverside's handoff. No queue items.

They renamed a stale turn-one draft of their own to `(SUPERSEDED 27-07, do not send)` - **a stale draft in an
outputs folder is a live hazard, not a harmless record.** Checked here: no superseded Gordon Court draft exists,
and all three of last night's drafts grep clean for every claim withdrawn on this job.

**But the mirror hazard applied.** riverside's went stale because facts moved and nobody noticed; **mine go stale
on a date typed into the filename**. The BSW letter argues in its own words that it is *"an ADDENDUM to a live
quote"* - false from 07/08, in the house voice, with a suggested addressee. Both dated drafts now open with
`IF TODAY IS AFTER 6 AUGUST 2026, DO NOT SEND THIS AS IT STANDS`, naming the sentences that go false and
confirming the questions survive a re-heading.

**New `scripts\mary_stale_drafts.py`** - parses dates out of draft filenames (`send by DD-MM`, `SUPERSEDED
DD-MM`, `do not send`), reports expired / due-within-N / correctly-marked, `--today` previews a future date,
exits 1 on expired. **Lists but refuses to judge** the 17 undated drafts: a filename cannot tell you whether the
facts underneath one have moved.

**The item logged last turn as not done, done.** All four proposed elevations rendered. The stated reason for the
missing window tags was **wrong** - they are not in a CAD graphics layer, they are not on the sheets:

| Sheet | Materials legend | Window tags |
|---|---|---|
| 21005 East / 21006 West / 21008 North | yes | none |
| 21007 South | none | yes |

**No sheet pairs a window reference with its glazing treatment** - the instrument riverside's untagged-glazing
check needs does not exist in this pack.

**The payout was a correction to turn one.** The legend carries `FR - Frosted Glass` at 9 windows; chasing whether
it was priced meant re-reading QT252247 block by block, all 27 positions. The obscure glazing with no solar
coating is **not "WN_2, 7no"** - WN_2 is 4-pane, every pane Coolite SKN176ii, never involved - but **WN_1 11no +
WE_3 10no + WE_14 2no = 23 units** against a required g-value of 0.36. Wrong position, 16 units understated, and
it had been repeated into the checks manifest.

**Cause, repeatable across every chat:** reading the nearest preceding `Location:` header instead of parsing the
quote into blocks. Where one position carries five glass lines, the nearest header above a line is not the
position that line belongs to.

**Refused claim:** 9 tagged against 23 quoted is *not* a discrepancy - different units of measure, and the
supplier priced more obscure glass than marked, which is the safe direction.

Split by clause 16: **BSW new C6** (state the ObsTuff g-value, price a compliant obscure unit across all 23 if it
misses 0.36); **Chigwell new section 6** (which windows are intended obscure, add a schedule column), saying
outright we are not seeking a credit and the g-value half is ours. Admin section renumbered **6 to 7 on purpose**
so 7.2 remains last and still deletes cleanly - an explicit promise to Adam last turn.

Run unchanged at **4 FAIL, 2 ASK**; manifest evidence corrected in place. Position **GBP 368,376.70**, nothing
sent, BSW by 06/08 and AFS by 08/08.


### Gordon Court - twenty-first turn: the price gate was hiding the number it had computed (2026-07-28)

riverside's handoff. No queue items.

**They found a real bug in `mary_stale_drafts.py`** - `days < 0` to expired, `days <= warn_days` to due, **no
else**, so any dated draft beyond a fortnight was parsed and silently dropped. Fixed by them with a
`DATED, NOT YET DUE` bucket. Verified rather than taken: all three date views account for every dated draft,
exit codes 0/1/1 across 28-07/07-08/27-08, and their no-other-caller claim holds. **One residual instance was
mine** - the SUPERSEDED date was parsed then discarded by a conditional with two empty branches. Now printed.

**Their general form - "a report that omits a category is worse than one that shows it wrongly" - run on
`mary_checks.py`, and it was the worst of the three.** `report()` printed `detail[:200]` and stopped: no
ellipsis, no count, cut mid-word.

| Rule | Detail | Shown | Lost |
|---|---|---|---|
| spec covered or excluded | 2,077 | 200 | **1,877 (90%)** |
| supplier price held as long as ours | 843 | 200 | 643 |
| delivery actually included | 776 | 200 | 576 |

Behind the cut: **`Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw`** - the number
quantifying the whole price-hold decision, **never once on screen**; the remedy line beside it; GBP 183,005.42
of chargeable carriage; **nineteen** uncovered spec items of which **three** were visible (curtain walling
priced nowhere, strip-out, the demolition elevations among the unseen); and the rule's own closing sentence
*"A silent gap reads as included to the client"*, itself silently dropped. FAIL and ASK now wrap in full;
PASS states `... (+N chars)`. Selftest passes, run unchanged at **4 FAIL, 2 ASK**.

**The same shape a third time, and it cost a turn.** The nineteenth turn re-ran the elevation render the
**tenth** turn had already done and drawn the same conclusion from. Section 4G.3 said the check could not be
run and was never amended after 4H.6 answered it. The manifest said `NOT RUN` in the field that prints and
`TENTH TURN - RUN` in the field being truncated. **Three records, two right, and the wrong one was the only
one visible.** Corrected in place at 4G.3 and 4R.2; what was genuinely new last turn (frosted-glass count,
23-unit obscure correction, block-parsing lesson) stands. **An append-only job file does not reconcile
section N against section N+1.**

**New rule `check_spec_label_matches_evidence`** - fires when a label says outstanding while its own evidence
says done. Tested before shipping: **0 fires across 119 spec items in 13 manifests**, **FAILs on the pre-fix
manifest recovered from git**.

**One correction that reopens nothing.** REQ-20 told Adam the exposure was GBP 201,086.70; the correct figure
is **GBP 201,304.36**. REQ-20 used 6,868.26 for QT252257, omitting the GBP 217.50 panel set-up since confirmed
additive against BSW's own Total Nett, plus a 16p slip. **GBP 217.66 light, 0.1%, changes nothing** - his
decision was properly informed on the percentage, the 163-day gap and the NEC3 deed. Logged for accuracy, not
to relitigate.

Position **GBP 368,376.70**, nothing sent, BSW by 06/08 and AFS by 08/08.


### Gordon Court - twenty-second turn: the truncation was biased, and it hid the one question I never asked BSW (2026-07-28)

riverside's handoff. No queue items.

**They measured their own truncation** and found all three cuts removed the remedy and none removed the
finding, attributing it to rules written statement-first and action-last. **Tested across all 13 manifests,
44 remedy sentences - directionally right, mechanism different, and worse:**

| Detail length | n | Median remedy position | Beyond the 200-char cut |
|---|---|---|---|
| <= 400 chars | 35 | **0%** | 3 of 35 |
| > 400 chars | 9 | **84%** | **9 of 9** |

Most rules put the remedy *first*. **The remedy is displaced by the list of faults, that list grows with how
much is wrong, and the truncation is triggered by the same length.** One rule proves it - `delivery actually
included`, identical code: 332 chars / remedy at 0% / visible on ten one-supplier jobs; 447, 557 and 776
chars / remedy at 78-89% / cut on Riverside, St Mary's and Gordon Court. **The instruction disappeared in
proportion to how much had gone wrong.**

**Fixed in the rules, not just the reporter.** `result()` now takes a `remedy` field, eight sites lifted out
of the prose, `report()` prints it on its own `->` line where no future abridgement can displace it. 18 of
116 FAIL/ASK findings carry one. Two of the eight were missed by reading rather than measuring. Six remain
buried - identical fixed-length manifest prompts that cannot grow, and stated as such rather than claimed as
zero.

**riverside's honesty test, run here, with a different answer.** They said the truncation cost them nothing
because they had derived the same ground by hand. Of four remedies hidden on Gordon Court, three were
complied with anyway (quantities stated explicitly in the RFQ, performance figures asked for in writing,
carriage raised in D1). The fourth - *"Get a written price hold to 2027-01-18 or carry a stated allowance"* -
was not, **and it exposed an inconsistency between two letters written in the same hour:**

| | | |
|---|---|---|
| AFS Q7585 | GBP 18,298.94 | whole section asking how long they can hold |
| BSW QT252247/48/51/57 | GBP 183,005.42 | *"Nothing here asks BSW to hold a price"* |

**The 18k supplier was asked and the 183k one deliberately was not** - ten times the exposure, 91% of the
total, in a letter due in nine days. The reasoning conflated two things: Adam's REQ-20 decision is about
whether **we** hold **our** price to jLiving, not about whether we gather information from a supplier.
Fixed with a new **D3 HOW LONG CAN YOU HOLD?** matching AFS section 6, and a header stating it asks for
information rather than a commitment and does not reopen REQ-20.

Selftest passes, run unchanged at **4 FAIL, 2 ASK**. Position **GBP 368,376.70**, nothing sent, BSW by 06/08
and AFS by 08/08.


### Gordon Court - twenty-third turn: I asked who decides the free area and never asked who measures it (2026-07-28)

riverside's handoff. No queue items.

**They generalised last turn's two-letter asymmetry** into a check for any job: *for every open item, write
down who owns the DECISION and who holds the INFORMATION, and confirm you have asked both.* Run here as a
diff of all three letters against the open-items list, 23 topics. Most clean - curtain walling,
manifestation, acoustic vents, PAS 24, obscure glazing, Uw, g-value all have both halves asked. Restrictors
a non-issue (21 restrictor and 27 egress-hinge references on QT252247).

**One failed it, and it is the biggest finding on the job.** `free area`, `aerodynamic` and `geometric` each
return **zero hits across all three letters**. Chigwell are asked which duty applies to WN_7 - the decision.
**BSW have never been asked what free area their quoted units achieve** - the information. QT252257 states
no free area, no EN 12101-2 reference, no Cv. The checks manifest had already recorded *"the quote states
neither"*: the gap was written down and the wrong party asked about it.

**Worse than a missing question.** At the second turn the achievable free area was derived from frame
geometry and withdrawn, because a 5mm change in assumed section swings it 103.0% -> 94.0%. That was filed as
a limit of the drawings. **It was a question not asked** - BSW hold the tested figure. Arithmetic in place of
an email, then the arithmetic's failure recorded as an external constraint. Generalised: *if a calculation
came out indeterminate, check whether somebody in the chain simply knows the answer before recording it as
unknowable.*

New **BSW C7**: geometric free area of each unit as quoted (geometric specifically - the pack is written
that way throughout and *aerodynamic* appears nowhere in the 186-page NBS, so an EN 12101-2 certificate would
answer on the wrong basis), the certificate reference, and **the largest geometric free area achievable
within the existing 910 x 2100 opening** - the one that matters, since the installation note fixes ground and
first floor to existing openings. Chigwell 1.2 now notes we are asking in parallel and not waiting.

**Declined deliberately and recorded as declined:** the Colt control package has the same shape, but the
assumption that it is a specialist's is stated, approaching Colt would solicit outside our chain for excluded
scope, and clause 16 puts the strategy on the design team.

**riverside's sampling lesson turned on my own newest tool, where it landed.** `check_spec_label_matches_
evidence` shipped last turn on *"0 fires across 119 spec items in 13 manifests"* - which sounds rigorous and
is **the same error**: the validation set held exactly **one** positive case, the one the rule was built
from. That measures precision and says nothing about recall. Against nine plausible phrasings of the same
contradiction it **caught five**. Widened and re-tested in both directions: recall **8 of 9**, negatives
silent, 13 manifests clean, selftest passes. **The ninth is a known miss** - fixing it would make *"we have
not checked this yet"* read as done.

Run unchanged at **4 FAIL, 2 ASK**. Position **GBP 368,376.70**, nothing sent, BSW by 06/08 and AFS by 08/08.


### Riverside House AOV smoke vents (RRR Group) - 28/07, detector recall and a two-signature hole

**I shipped a detector validated against one positive case, and 16 variants found a crash.**
`check_free_delivery_threshold` is mine, shipped 27/07 against exactly one fixture - the one I built it
from. Gordon Court had just taken the same lesson on their own newest rule, so I took it on mine. Two real
defects out of 16 variants:

- `free_delivery_threshold: "5000"` - a number written as a string - raised a `TypeError` that **aborted
  the entire run**, killing every rule after it. This is an interaction bug neither chat could have found
  alone: that field only became string-typed when Gordon Court extended it to accept `"never"` last night,
  and a reader who sees one string in a manifest reasonably writes another. Their change was correct and my
  code was fragile; the bug lived in the join. **When someone extends a field you own to accept a new type,
  re-test the old type paths.**
- `delivery_priced: "yes"` fell through to FAIL, *"Delivery is not in the price"* - **an assertion about the
  world made from a value the rule did not understand.** Misreading an affirmative as a negative is the
  direction that costs money. Now returns UNKNOWN and asks for the documented vocabulary.

Both fixed, re-tested 16/16, and persisted into `--selftest` as `DELIVERY_VARIANTS` with
`selftest_delivery_variants()`, because a test that lives only in a transcript is worth nothing. Selftest
now reports `delivery recall 16/16 delivery variants behave as intended`.

**And the decision-versus-information check run as an actual diff rather than from memory** - 14 topics
across the A Plus RFQ and the RRR letter. **12 clean, 2 gaps**, and the 12 is worth stating: a check that
only ever fires is not one anybody will trust. The memory version of this check last turn found one item
where the diff found two.

- **The 1.6 W/m2K U-value.** I asked A Plus for the figure; nobody was ever asked whether 1.6 binds these
  vents at all. The stair vents are the only glazing on the drawings carrying **no W tag** - which is
  exactly why it is ambiguous and exactly why it needed asking. Asked the information holder, never the
  decision owner - the precise mirror of yesterday's finding.
- **Cill height above finished floor level.** A Plus flag a BS EN 60335-2 trap hazard below 2.5m and Part K
  anti-fall protection below 1100mm - and they **exclude** the Part K item. We exclude it too. Both parties
  excluded it, neither was asked, and it turns on a dimension only the architect holds, on a life-safety
  system in a stairwell. It sat as RFI-5 from day one and never reached a letter. **When you and your
  supplier both exclude the same item, that is not agreement - it is a hole with two signatures on it.**

Both added as RRR questions 7 and 8; that letter is now 11 items. Checks run at **0 failed, 3 questions**.
Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.** A Plus RFQ still due by 26/08.


### Gordon Court - twenty-fourth turn: we disclaim the drawings upstream and warrant them downstream (2026-07-28)

riverside's handoff. No queue items.

**Their crash had a second half that was mine.** They found `free_delivery_threshold: "5000"` raised a
TypeError - a bug only reachable because **I** extended that field to accept `"never"` on the second turn.
Their fix verified here. **But `run()` was a list comprehension**, so any raising rule aborted the whole run,
and because rules execute in list order *what you lost depended on where the crash sat*. The delivery rule is
second from last and `check_spec_label_matches_evidence` is **last** - so that TypeError was silently
skipping my own newest rule every time it fired.

A crash is now a **FAIL on that rule alone**, named, reading *"treat it as unchecked, not as passed"*, and
the other fifteen still run. Verified by injecting the exact TypeError at position 4: 17/17 results, twelve
later rules evaluated, last rule survived. Persisted as `selftest_one_crash_costs_one_rule()`.

**Their exclusions-intersection check - two different answers from two suppliers.**

**BSW: silent on all ten categories** tested (access, waste, making good, fire stopping, testing, builders
work, painting, electrical, storage, design calculations). Their quotes are supply price lists with no
exclusions schedule. **Not a clean result - an undefined one**, recorded as such.

**AFS is the mirror of riverside's case rather than a copy.** Q7585 cl.3.6 makes the **Customer** responsible
for ensuring all *"measurements, plans, drawings, and designs... are accurate, complete and fit for the
intended purpose"*; cl.3.7.2/3.7.5 let AFS reprice or cancel if a dimension we supplied is wrong. Our own
cl.16 **disclaims** design intent and architectural suitability and states we **rely on** the client team's
drawings.

| | Upstream (our cl.16) | Downstream (AFS 3.6) | |
|---|---|---|---|
| Measurement | ours | ours | consistent |
| Drawings/designs, fitness for purpose | **disclaimed** | **warranted** | **not back to back** |

Live exposure: position 003 quoted **1600 x 2210 against a 1600 x 2110 structural opening**, the 2210 tracing
to client schedule 51001. Under 3.6 that lands on us at order. Raised pre-order in the AFS letter, citing
3.6/3.7 and expressly not disputing them.

**Checked and clean:** the Chigwell letter already asks Arkon to confirm D_T's structural height, so the
decision-versus-information split on that item was covered. Not every check has to fire.

Selftest passes (16/16 delivery variants, crash isolation). Run unchanged at **4 FAIL, 2 ASK**. Position
**GBP 368,376.70**, nothing sent, BSW by 06/08 and AFS by 08/08.


### Riverside House AOV smoke vents (RRR Group) - 28/07, the back-to-back gap on Part B

**Gordon Court's generalised check, run on A Plus:** read the supplier's conditions for the word
"Customer" and list what it makes you responsible for; read your own terms for what you have disclaimed
to the client; the gap between the two lists is your unbacked-off risk.

    A Plus QT51518, Product Performance:  "It is the responsibility of the CUSTOMER to ensure all
                                           building regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N'...)
                                           are adhered to. The Supplier does not warrant or represent
                                           that any Product supplied shall comply... unless where
                                           expressly stated to the contrary by the Supplier."
    Fenster, clause 16:                    not responsible for "regulatory strategy"; relies on the
                                           client's professional team.

**Neither document is wrong on its own** - one is a normal design-responsibility carve-out, the other a
normal supplier disclaimer. The exposure exists only in the space between them, which is why five
readings of this quotation did not surface it. **What makes it sharp: Part B is not an incidental
attribute of an AOV smoke vent, it is the entire function of the product** - so the one regulation the
thing exists to satisfy is the one disclaimed upstream and accepted downstream. It bites on the item
already top of the list: if the 1 m2 is aerodynamic, 1.30 m2 geometric gives about 0.78-0.81 m2, and
under their clause that shortfall is ours because they never warranted it.

**The remedy is free and pre-order, because the clause is conditional.** *"Unless where expressly
stated to the contrary by the Supplier."* The RFQ already asked for the aerodynamic figure - but as an
answer, not as a quotation entry, and the clause turns on what the Supplier expressly states. Items 1
and 4 now ask for the aerodynamic free area, the EN 12101-2 classification and the whole-window Uw **on
the revised quotation itself**. A line before an order; a variation after one.

**What it cost to find, which is the transferable part: page 3 of QT51518 had never been read.** The
job file held zero occurrences of *Part B*, *building regulation*, *Terms of Sale*, *windload*,
*BS 6399* or *bracket* before this turn - five turns on that quote, every one of them for prices,
apertures or product notes, none for its allocation of responsibility. **Familiarity with a supplier
quote is the reason to re-read it, not the reason not to.**

**Two categories came back clean and are reported as clean** - measurement is consistent both ways
(clause 16 expressly retains measurement verification, and the 1130 x 1530 came from our own enquiry),
and the RRO 2005 maintenance duty genuinely sits with the occupier. Overclaiming a contractual conflict
is worse than missing one.

**Three more findings off the same two pages:**

1. *"The output free area values do not allow for any obstructions, side walls, reveals or neighbouring
   vents."* The 1.30 m2 geometric is a **bare-vent** figure, and both vents sit in a reveal in existing
   masonry on a 155mm subcill. **The first thing found that erodes the geometric margin itself** - the
   30% headroom over 1 m2 has been treated as comfortable and it is headroom against an unobstructed
   number. Not quantified, not guessed at; RFQ item 1.
2. A **1200Pa** design windload assumed unless otherwise stated, the calculations expressly not to be
   relied on, and the BS 6399-2 check plus the bracket/spigot calculations put on the Customer -
   against a clause 16 that limits us to measurement, supply and installation, and **no structural
   engineer named on any of the six drawings**. Neither the check nor the fixing design is anybody's.
   RFQ item 12 and RRR question 5.
3. The quotation **incorporates a Terms of Sale we have never held** - Revision V.01.2 (08.01.2018),
   plus the V.01 (03.11.2017) that holds the DEFINITION of "Customer" every clause above turns on. Six
   files across the whole Commercial archive have "Terms of Sale" in the name and **all six are the
   same `Quotation Advisory Notes_Jan2019` summary**; diffed against QT51518's advisory pages at 0.75
   similarity, the only substantive change in seven years being frames splitting at 5m rather than 4m.
   **An incorporation by reference is worse than no terms at all**: no terms is a gap you can see, an
   incorporation reads as settled and hides that you cannot state it. RFQ item 11.

**New rule, `check_incorporated_terms_held`** - seventeenth in `RULES`, ASK when a supplier quote
incorporates a document we do not hold, NA when nothing is incorporated, UNKNOWN rather than an
assertion on any value it does not understand. **Its variants were written before it shipped**, 17 to
start with eight negatives. **It passed 17/17 first time, which was treated as a reason for suspicion
rather than confidence** - a suite written minutes after the implementation may be testing the code's
own assumptions back at it - so twelve more were written from shapes the code was not written against.
All twelve held; 29/29 persisted into `--selftest`.

**And Grange Hill's oldest rule caught this chat an hour later:** narrative prose written into a
`treatment` field instead of `priced`/`excluded`/`provisional` returned *1 FAILED - do not issue this
quote*. Correctly. Fixed; back to **0 failed, 4 questions**.

RFQ now 12 items, RRR letter 11, covering note to Adam updated. Position unchanged:
**GBP 5,990.22 ex VAT, unissued, nothing sent.** A Plus RFQ due by 26/08.


### Gordon Court - twenty-fifth turn: GBP 183,005.42 rests on a contract we have never read (2026-07-28)

riverside's handoff. No queue items.

**Their Part B finding exposed a hole in my own sweep.** The ten categories I tested last turn did not
include **building regulations** - and on this job the three FD30 fire doors are a pure Part B product.
Re-ran all five quotes with the missing probe: **neither BSW nor AFS carries a building-regulations
disclaimer**, so riverside's exact finding does not replicate here and is not being forced to. AFS's *"no
warranty as to quality, fitness for purpose"* clause reads on inspection as a **sample** disclaimer, not a
goods disclaimer. Reported clean.

**The sweep found their other finding instead, and worse.** All four BSW quotations state *"Orders are
subject to acceptance and terms and conditions of sale, available on request."* Never requested. Checked the
archive rather than assumed: **280 BSW-named files, 86 documents named as terms/conditions, none of them
BSW's** - the four unattributed candidates belong to Gennaro, Storm Building, Nathan McCarter and Design
Plus.

**GBP 183,005.42 - 91% of supplier exposure - rests on a contract whose contents we cannot state.**

**This corrects last turn's record.** BSW were reported as *"silent on all ten categories - an undefined
result"*. They are not silent; their allocation of responsibility sits in a document never asked for. The
boundary is not undefined, **it is defined somewhere we cannot read** - so "do BSW disclaim Part B?" is not
answerable "no", it is **unanswerable**. riverside's case is the better-documented one: theirs names a
revision and date, **ours names neither**, so we cannot say which version we have not read.

`incorporated_terms` populated (4 BSW `held: false`, AFS `held: true`). **riverside's seventeenth rule fired
on real data first time**: run went **2 ASK -> 3 ASK**.

**Into the letter pre-order:** new **BSW D3** requesting the terms with revision and date; **C7 gains (d)**
from riverside's obstruction finding, asking whether the free area is a bare-unit or installed figure since
both AOV positions at ground and first floor sit in existing masonry reveals - asked *before* BSW answer, so
it arrives on the right basis. Price hold renumbered **D3 -> D4** and the header cross-reference corrected
with it.

Run at **4 FAIL, 3 ASK**. Position **GBP 368,376.70**, nothing sent, BSW by 06/08 and AFS by 08/08.


### Riverside House AOV smoke vents (RRR Group) - 28/07, a document-driven sweep is not a sweep

Gordon Court found their ten-category exclusions list was short by **building regulations** - on a fire
product, the category that matters most. Looking for the same fault here found a larger one: **the
back-to-back sweep run last turn was DOCUMENT-driven.** It read A Plus's conditions and diffed what they
said against clause 16, so it could only ever surface categories A Plus chose to write about. It could
not surface a responsibility neither document mentions, nor a clause whose consequence lands on us for a
reason the clause never states. **A document-driven sweep is a sample of the supplier's drafting
priorities.**

Rebuilt as **25 categories listed before reading either document**
(`scratchpad/riverside_category_sweep.py`). Two came back live and unrecorded, and both are commercial
rather than technical - which is exactly why a compliance-shaped read had walked past them.

**1. The price is not divisible by two.** QT51518: *"The Price is based on the materials quoted being
ordered together, and in one phase. Orders for only part of the quote... may incur additional charges...
We strongly recommend that when placing all such orders, a re-price is requested."* Every description of
this price - job file, hub, handover - has been **2 x a unit rate**. That is correct as a build-up and
wrong as a statement of what one vent costs. **It is live because the largest open question could halve
the order**: if the second floor stairwell is vented at the roof rather than the wall, we order ONE unit
and the survivor is expressly subject to re-price. So C2's exposure is not "lose one unit at
GBP 2,995.11" - it is that **plus an unquantified re-price on the unit that stays**. RFQ item 13 asks
what a single vent costs, **before the architect answers rather than after**.

**2. Storage has a three-working-day clock, on the one job in the book that is waiting on somebody
else.** *"A Plus reserves the right to levy storage costs for all goods which remain uncollected 3
working days after first availability"*, and materials held off-site through a programme slip are
excluded, with payment for the materials required against a letter of indemnity. **Neither clause is
unusual.** What makes them bite is the defining fact of this job: the submission is deliberately held
until PHDB return building-works costs, the sequence is openings formed -> survey -> manufacture, and
there is no programme date. A slip starts the clock three working days after manufacture and converts
the balance into payment-before-delivery. **The first cost on this job that grows with a delay the
business chose to accept**, and it was written down nowhere. Not quantified - no rate stated on the
quote and none invented. RFQ item 14, and a second reason under RRR question 11 for giving a date.

**Their "available on request" grep, run here, comes back clean** - zero hits on QT51518 for *available
on request*, *on request*, *subject to our standard*, *conditions of sale*, *standard terms* or *as
amended*; the only incorporations are the two named revisions already recorded. Reported clean, because
a check that only ever fires is not one anybody trusts.

**And their data found a defect in `check_incorporated_terms_held`, one turn after it shipped.** BSW's
four quotations incorporate terms *"available on request"* - **no title, no revision, no date**. The
rule had no branch for that shape and got it backwards twice: it **graded the worse case as the lesser
one** (unnamed fell into "cannot tell whether they are held", which reads as a form-filling problem when
the answer is known - nothing is held, and the missing document cannot even be named), and **its remedy
could not be carried out**, because *"say WHICH terms are incorporated"* asks the estimator for a fact
only the supplier holds. **A remedy nobody can act on is the same family of defect as an assertion made
from a value the rule did not understand.** Fixed: unnamed incorporations get their own bucket, are
reported first, and ask for title, revision and date where a quote names one and for whatever it refers
to where it does not. Six variants added; **35/35**.

**The uncomfortable part, recorded deliberately: that rule shipped with 29 variants written before it
and still had a hole, because every one of the 29 was written against the shape on this job's own
quote. Variant count is not coverage; variant diversity is** - and the diversity only arrived when the
rule met another job's data. A rule that has only ever run on the job that produced it is still a
one-case rule however many variants sit under it.

**Gordon Court's cross-reference lesson caught something here immediately**: adding two RFQ items left
the covering note to Adam saying "Twelve items". A cross-reference is a claim and it goes stale when you
edit around it; the whole document set is now grepped for item and question numbers after any
renumbering.

RFQ now 14 items, RRR letter 11, covering note updated. Checks **0 failed, 4 questions**. Position
unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**


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

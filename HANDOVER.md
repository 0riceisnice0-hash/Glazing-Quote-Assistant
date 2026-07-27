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

### Autopilot session log (no-action sessions)

One line per poller-launched session that produced no email, so the record shows the queue was actually triaged rather than skipped.

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

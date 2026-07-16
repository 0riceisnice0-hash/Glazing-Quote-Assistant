# AI Agent Guide

This repo is the Fenster Glazing Quote Assistant. Its real job is not just parsing documents; it is trying to behave like a junior commercial glazing estimator who can read a tender pack, build a sensible scope, price it using Fenster rules, explain uncertainty, and generate a quote for human approval.

Read `HANDOVER.md` first for the current priority. This file is the deeper operating manual.

## Current Snapshot

- Working repo path: `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant`.
- Do not continue working in the old OneDrive repo unless the user explicitly asks.
- Live app type: static HTML/CSS/JS on Cloudflare Pages, with an optional Cloudflare Worker for document intake.
- Cloudflare Pages frontend: `https://glazing-quote-assistant.pages.dev`.
- Cloudflare Worker: `https://gqa-document-processor.0riceisnice0.workers.dev`.
- Current visible app version: `v2026.06.30.8`.
- Ninn Lane supplier-pricing correction: supplier quote totals are material-cost evidence; Project Hail Mary review now adds product-code markup and product-code labour to produce the estimator sell total.
- Latest Ninn Lane amended-docs fix: Pricing Document workbooks now extract the `Windows & External Doors` sheets as scope-only rows when the workbook has blank rates, keep those rows for estimator review, and prevent unpriced scope rows from contributing supply/install/EPDM/mastic totals.
- Current confirmed pushed commit before this doc refresh: `2f39bdf Add tender finder research panel`.
- There are currently no GitHub Actions workflows in this repo.
- The user expects meaningful changes to be committed and pushed when work is complete.
- Recent manual quote outputs were generated under `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs`.
- Important recent jobs:
  - Home Bargains Basingstoke: supplier-backed quote using Bellview, Strongdor, and ACA supplier returns.
  - Alkerden: budget pricing review from schedules only; no supplier quote was included.

## What The Bot Is Supposed To Become

The near-term goal is to get the estimating bot to the level implied by the Fenster emails, especially Project Hail Mary / Ninn Lane:

1. Read emails and identify what the client/supplier actually wants.
2. Ingest ZIP, PDF, XLSX, DOCX, MSG/email text, supplier quotes, drawings, schedules, specifications, and BOQs.
3. Separate priced scope from evidence/reference documents.
4. Extract products, quantities, dimensions, material, colour, U-value, glass, ironmongery, fire/acoustic requirements, install assumptions, and exclusions.
5. Use supplier quotes or estimator pricing workbooks as stronger evidence than generic parsed drawings.
6. Produce a priced quote, a compact quote, a pricing/check sheet, and assumptions/exclusions/RFIs.
7. Explain why its number differs from a real quote or supplier quote.
8. Let a human estimator approve/edit before issue.

The live tender-finder dashboard is a good later feature, but estimating accuracy is the current priority. Finding more tenders is not useful if the bot cannot price a supplied pack properly.

## Main Files

- `index.html`: app shell, upload UI, version badge, script cache-busting.
- `js/app.js`: main orchestration and UI state.
- `js/documentIntake.js`: file intake, ZIP/DOCX/MSG/PDF/XLSX routing support.
- `js/pdfParser.js`: PDF text extraction and helper parsing.
- `js/dataExtractor.js`: document classification, schedule extraction, pricing workbook extraction, validation warnings.
- `js/pricing.js`: price engine, inferred defaults, commercial markups/allowances, install/VAT handling, optional labour-code allowances.
- `js/aiEnrichment.js`: optional OpenAI note review and field prefill.
- `js/ui.js`: tender questions and review UI.
- `js/quoteGenerator.js`: branded detailed/compact PDF quote generation.
- `js/projectHailMary.js`: Project Hail Mary/Ninn Lane estimator workflow helpers: requirement extraction, supplier quote detection, supplier item coding, assumptions/exclusions/RFIs, proposal/pricing draft data.
  Adam's AI-written training brief is treated as guidance/training context, not as live tender scope evidence.
- `js/tenderFinder.js`: research panel for live tender source strategy, CPV codes, keywords, and opportunity scoring.
- `scripts/run-tender-pack.mjs`: local CLI regression harness that should use the same extraction/pricing logic as the website.
- `workers/document-processor/`: partial worker direction for heavier document processing.

## Estimator Workflow

Use this flow whenever the user gives tender documents:

1. Identify the job name, client, deadline, material system, colour, U-value, and whether it is supply-only or supply-and-fit.
2. Classify every document before pricing anything.
3. Pick the strongest source of scope:
   - Real Fenster/estimator pricing workbook.
   - Contractor BOQ or opening schedule workbook.
   - Supplier quote with itemised schedule.
   - Text schedule PDF.
   - Drawings/specifications only, which are weaker and require assumptions.
4. Extract item lines and inspect the extracted table/JSON, not just the grand total.
5. Run pricing through shared modules, not a one-off script that disagrees with the website.
6. Compare against any actual quote/proposal/supplier quote available.
7. Explain variance:
   - duplicate counting,
   - missing preliminaries,
   - install/VAT included or excluded,
   - supplier totals preserved versus native engine repriced,
   - allowances/markup included,
   - missing dimensions,
   - drawing takeoff assumptions.
8. Fix shared parser/pricing modules if the website and script differ.
9. Re-run known checks after touching shared extraction or pricing logic.
10. Generate detailed and compact PDFs only after the scope and assumptions are believable.

## Manual Quote Pack Workflow Used In Recent Sessions

When the user needs an urgent quote and the live parser is not enough, use this repeatable workflow. This is the practical "act like the estimator" flow that produced the recent Home Bargains and Alkerden outputs.

1. Work from the Desktop repo:

   ```text
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant
   ```

2. Copy or extract the user's ZIP/PDF/XLSX attachments into a job folder under:

   ```text
   test-results\<job-name>-input
   ```

3. Run the shared parser first, but do not trust it blindly:

   ```powershell
   node scripts\run-tender-pack.mjs --dir "test-results\<job-name>-input" --out "test-results\<job-name>-run" --with-supplier
   ```

4. Inspect the resulting JSON/CSV and compare it with the actual schedules. If the parser misses image/CAD schedules or chooses the wrong source, manually extract with `pdfplumber`/`openpyxl` and document the limitation.

5. Use source hierarchy:
   - Supplier quotes and real estimator pricing workbooks are strongest.
   - Schedules/BOQs are next.
   - Type elevations/specs are reference.
   - GA drawings/elevations/facade setting-out are evidence, not priced scope, unless manually measured.

6. Generate both an Excel pricing/review workbook and a PDF proposal/pricing review.

7. Put final outputs here:

   ```text
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs
   ```

8. The Excel/PDF format should include summary totals, pricing lines, supplier/fallback cost, code, markup, labour, sell total, notes, pricing review table, exclusions, assumptions, RFIs/actions, and source notes.

9. Render the PDF to PNG and visually check it before final reply. If Poppler shim fails, call the real executable:

   ```powershell
   C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe
   ```

10. Never hide uncertainty. If no supplier quote exists, call the output a budget/fallback pricing review. If something is missing, show it as TBC/not priced rather than inventing it.

## Self-Checking Quotes

The bot must actively check itself. A future AI should not stop at "it generated a quote".

For each job, check:

- Does the item count match the schedule/pricing workbook?
- Are obvious product types correct: windows, doors, curtain wall, louvres, rooflights, screens?
- Are dimensions present and in the right units?
- Are quantities duplicated by PDFs plus XLSX files?
- Are reference drawings/specs being priced incorrectly?
- Are supply-only, install, preliminaries, risk, overhead/profit, and VAT handled consistently?
- Does the total reconcile to any real quote/proposal/supplier quote?
- If no real quote exists, are assumptions explicit enough for a human estimator to approve or correct?
- Did the website and CLI produce the same result from the same pack?

When the total is wrong, do not only adjust a multiplier. First find the cause:

- Wrong scope source selected.
- Duplicate documents counted.
- Pricing workbook ignored.
- Supplier quote parsed as scope plus layout parsed again.
- Install/VAT/prelims applied twice or not at all.
- Missing commercial allowance rows.
- Dimensionless rows retained as real items.
- Drawings treated as schedules.
- OpenAI prefill did not write back into tender questions.

## Extraction Rules That Matter

The quote bot should be conservative. Do not price every document that contains window or door words.

- Pricing workbooks are the source of truth when present.
- If a Fenster/R1-style pricing workbook is present, skip other schedule PDFs/layouts as priced scope to avoid duplicate bogus items.
- Generic files named `Pricing.xlsx` must be recognised, not only files literally named `Pricing Document`.
- External/opening schedule workbooks are preferred over duplicate schedule PDFs.
- Opening type sheets are reference/spec documents, not priced scope.
- Supplier quotation PDFs, glass order PDFs, bay layouts, elevations, and image-heavy drawings are evidence unless a dedicated parser proves they are a priced schedule.
- BOQs can be scope when they are clearly contractor pricing/scope workbooks, but should not override a Fenster pricing workbook.
- Materials schedules/specifications enrich assumptions but should not create priced line items by themselves.
- Dimensionless markers should be dropped unless they are explicit commercial allowance rows.
- Image-only PDFs require OCR/drawing takeoff before they can support accurate pricing.

## Known Job Patterns

### Addington Road ePVC

This exposed a serious issue: a script result around GBP 155k did not match the website block price around GBP 450k. Treat this as evidence that scripts and website logic can diverge if they do not share the same pricing path. Future fixes must make the website and local harness call the same engine and compare totals.

### Whitsbury / Hartford Care Home

Known historical result:

- Items: 160
- Subtotal: GBP 299,030.51
- Install: GBP 22,400.00
- VAT: GBP 64,286.10
- Total inc VAT: GBP 385,716.61

Important behaviours:

- External opening schedule workbook rows such as `WG` and `W1` are parsed.
- Duplicate schedule PDFs are skipped when the workbook exists.
- Opening type sheets are treated as reference/spec, not scope.
- Installation remains enabled for this pattern.
- OpenAI note review previously helped with some red fields, but quota was hit; deterministic extraction must still work.

### Brandon Estate REV 2

Known historical result from actual pricing workbook:

- Items: 51
- Total/subtotal ex VAT: GBP 7,196,695.63

Important behaviours:

- Pricing workbook rows preserve exact sell rates and totals.
- Commercial allowance rows are included as allowance lines.
- Generic install, EPDM, mastic, and VAT are disabled because the estimator workbook already includes commercial pricing/allowances and is normally quoted plus VAT.
- This job proved big commercial quotes need structured preliminaries, overhead/profit, risk, and markup handling.

### Gresty Road

Two states exist:

- Drawing/spec-only budget takeoff: around GBP 119,237.88. This is assumption-heavy only.
- Actual pricing pack from `R1 Construction - Gresty Road Pricing.xlsx`: reliable source.

Known actual pricing result:

- Items: 53
- Mix: 52 windows, 1 door
- Total/subtotal ex VAT: GBP 89,898.12
- Matches proposal subtotal: GBP 89,898.12 plus VAT.

Important behaviours:

- Recognise generic pricing workbooks.
- Do not double count bay layouts, supplier PDFs, glass orders, and proposal PDFs when the pricing workbook is present.

### Project Hail Mary / Ninn Lane

Email requirement:

- Quote aluminium windows and doors.
- Three separate buildings.
- PPC aluminium framed double-glazed windows and doors.
- Colour: black.
- U-value: 1.4 W/m2K.
- PPC aluminium framed louvre panels where shown on drawings.
- Commercial spec.
- Elevations, plans, specification, and schedules are in ZIP files.
- Supplier quotes were later attached.

Current intended bot behaviour:

- Read the email as tender instructions, not as pricing scope.
- Extract the high-level assumptions above into the job settings.
- Read ZIP contents and classify plans/elevations/spec/schedules.
- Treat supplier quotes as strong evidence.
- Detect and code Sheerline/supplier item rows where possible.
- Generate RFIs/exclusions/assumptions where drawings or supplier data are incomplete.
- Do not pretend a final quote is certain when supplier quote parsing misses setup extras or panel extras.

Known issue:

- Ninn Lane detects supplier quotes and Sheerline coding rows, but parser hardening is still needed for some PDF.js text around panel/setup extras.

### Brocks Hill

Blank-rate contractor BoQ pack (2026-07-15). Only `Brocks Hill BoQs.xlsx` was supplied - no drawings, spec or supplier quotes.

Important behaviours:

- `classifyDocument` now matches plural `BoQs`/`BQs` filenames as BQ documents.
- Strategy B1 (`tryContractorBoqBlankRateExtraction` in `js/dataExtractor.js`) extracts blank-rate BoQ workbooks shaped `ITEM | DESCRIPTION | QUANTITY | UNITS | Rate | Value` with wrapped multi-row descriptions and dotted/slashed refs (`ED.0.02`, `ED.0.10/14`, `WIN.E.02`).
- Fixed/opening pane counts are parsed from wording like "two Fixed Fields and a Top Hung Window" so split-pane pricing applies.
- Door-in-screen elements get combined codes (SADSAW/SADMAW) with a review note.
- `E/O` extra-over lines and dimensionless lines become `scope-unpriced` estimator-review rows; they must never be auto-priced or dropped.
- The BoQ `Quoted Value` inclusion checklist is captured as spec notes via `extractBoqInclusionNotes`.
- Result: 9/9 BoQ lines extracted; budget sell ex VAT `GBP 111,208.82` (fallback material + code markup + code labour + EPDM/mastic allowances). Ninn Lane amended and Alkerden regression runs were unchanged after this work (commit `b8d9a71`).

### Crownhill Business Centre / Zelltec

Fenster's own WindowCAD-style design concept PDF (2026-07-15). One product type per page with `TYPE X - FRONT/REAR` headings, `Quantity: N`, a `Comments` block and dimensions between the `External` and `Internal` elevation labels.

Important behaviours:

- `classifyDocument` recognises design concept PDFs (TYPE pages + Quantity + "design concept"/"frames are viewed from the outside") as high-confidence schedules.
- Strategy C1 (`tryFensterConceptExtraction`) parses one item per type page; `- Frame N` detail pages are skipped, and Comments parsing must not rely on newlines because PDF.js page text can be one long line.
- Tilt & turn pane widths under the elevation feed split-pane pricing; steel panic-bar doors become SSD/DSD with no glazing cost; entrance doorsets with flanking screens get SADSAW/SADMAW.
- `solarControlExtra` (default GBP 35/m2) applies when the item spec mentions solar control/Coolite.
- Email instructions (Smart Wall spec, pressing allowances, quantity totals) still need estimator application in the output workbook - the CLI does not read emails.
- Result: 8/8 concept types, 29 frames, budget sell ex VAT `GBP 97,778.03` (commit `45267e1`). Brocks Hill/Alkerden/Ninn Lane regressions unchanged.

Rev 2 (2026-07-15, supplier-based) replaced the engine budget with rates mined from past supplier costings per Adam's instruction. Durable estimating knowledge from this pass:

- Adam's rule: a WindowCAD concept page with no printed quantity is ALWAYS quantity 1.
- Handle positions on WindowCAD drawings indicate openers (TYPE A centres fixed, outers T&T).
- The supplier-quote archive lives under `C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents\<client>\<job>\...\2. Supplier Quotes`. Vetroseal quotes are named `FENSTERG_Quote_NNNNNN(...)`; Strongdor quotes `SQ` numbers; BSW quotes `QTnnnnnn`.
- Benchmark rates mined for Crownhill: BSW alu casement unglazed GBP 300/m2 (QT239743); BSW alu open-out door GBP 534/m2; Vetroseal SKN 176 Coolite tgh 4T-20-4T argon GBP 103/m2 (059396); Vetroseal lami/tgh softcoat GBP 52.50/m2 (059828); Vetroseal tgh softcoat 4T-20-4T GBP 57.75/m2, 6T-16-6T GBP 85.25/m2 (060079); BSW glazed casement incl SKN 176 approx GBP 615-700/m2 (QT245448); Vetroseal energy surcharge approx 6% of goods; BSW quotes are ex-works.
- Strongdor SQ216661 Rev1 (14/07/2026) is a live quote for Crownhill TYPE F/G: GBP 817.64 / GBP 927.08 per doorset + GBP 153 delivery, valid to 13/08/2026.
- Rev 2 sell ex VAT `GBP 73,770.86` (supplier cost GBP 49,360.86 + markup GBP 19,000 + labour GBP 5,410). T&T uplift (+20% on casement rate) and Smart Wall commercial uplift (+15% on door rate) are estimator judgement pending firm BSW/Aplus/Vetroseal quotes.

### Home Bargains Basingstoke

Recent urgent manual quote.

Input packs used:

```text
C:\Users\zacpl\Desktop\tender docs due tosay\Home Bargains, Basingstoke Aluminium Doors & Windows.zip
C:\Users\zacpl\Downloads\Project Hail Mary - Stainforth.zip
```

Working extraction folders:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\home-bargains-input
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\home-bargains-quote-subset
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\stainforth-supplier-prices
```

Final outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Glazing Proposal and Pricing Review.pdf
```

Supplier evidence:

- Bellview Products quote `0000000428`: aluminium/shopfront package. Use grand total net after 15% discount, not gross line totals.
- Strongdor `SQ215074 Rev1`: steel doors.
- ACA Solutions `QU-4030`: automatic door header/lock/sensor package and ACA labour.

Current corrected commercial position:

- Bellview/Strongdor/ACA supplier costs are included.
- ACA cost is `GBP 12,710.00`; 25% markup was applied as `GBP 3,177.50`.
- Latest sell total ex VAT: `GBP 89,429.22`.
- Latest inc VAT if applicable: `GBP 107,315.06`.
- Roller shutters are excluded by user instruction.
- Access control/automatic package: ACA supplier cost is included and marked up. Any extra readers/fobs/keypads/controllers/maglocks/cabling/integration beyond ACA remains TBC.

Important lesson:

- Do not leave "25% of supplier cost" as a text placeholder when the supplier cost is known. Convert it to a money value and increase the total.
- `SSD` means single steel door; `DSD` means double steel door.

### Alkerden

Recent budget review from tender documents.

Input zip:

```text
C:\Users\zacpl\Downloads\OneDrive_2026-07-01.zip
```

Working folder:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\alkerden-input\Stage 4 Curtain Walling & External Doors
```

Final outputs:

```text
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Pricing Document and Review.xlsx
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Glazing Proposal and Pricing Review.pdf
```

Email instruction:

- "These are composite windows but can be marked up as aluminium."

Extraction:

- Window schedule: `Schedules\HX486-HUN-ZZ-ZZ-SH-A-002001.pdf`.
- External door schedule: `Schedules\HX486-HUN-ZZ-ZZ-SH-A-000001.pdf`.
- Door type elevations: `Door Type Elevations\HX486-HUN-ZZ-XX-SH-A-000101.pdf` and `000102.pdf`.
- Window type elevation available: `Window Type Elevations\HX486-HUN-ZZ-XX-SH-A-002102.pdf`.

Current budget position:

- 111 window schedule rows extracted and aggregated.
- 19 dimensioned external door rows priced.
- 3 missing-dimension door rows flagged: `ED13` and `ED23` rows.
- Budget fallback/material allowance ex VAT: `GBP 472,357.93`.
- Code markup: `GBP 90,950.00`.
- Labour allowance: `GBP 25,510.00`.
- Budget sell total ex VAT: `GBP 588,817.93`.
- Budget inc VAT if applicable: `GBP 706,581.52`.

Important caveat:

- No supplier quote was included, so this is a budget pricing review only. It should not be issued as a fixed supplier-backed quote.
- Folder title says "Curtain Walling & External Doors", but no separate curtain wall schedule/quantities were found beyond the window/door schedules. Flag this as a query.

## Claude Code Handover Message

Use this message if handing the repo to Claude Code or another coding agent:

```text
You are working on the Fenster Glazing Quote Assistant.

Use the Desktop repo only:
C:\Users\zacpl\Desktop\Glazing-Quote-Assistant

Do not use the old OneDrive repo. The live app is:
https://glazing-quote-assistant.pages.dev

The job is to behave like a junior commercial glazing estimator, not just a parser. When Zac gives a tender pack, do the following:

1. Extract the ZIP/PDF/XLSX into:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\<job-name>-input

2. Run the shared parser:
   node scripts\run-tender-pack.mjs --dir "test-results\<job-name>-input" --out "test-results\<job-name>-run" --with-supplier

3. Inspect the JSON/CSV and actual schedules manually. Do not trust the total until row counts, dimensions, quantities, and source-of-truth decisions make sense.

4. Source priority:
   supplier quote / estimator pricing workbook > BOQ/opening schedule workbook > schedule PDF > drawings/specs.
   Type elevations and specs are reference evidence unless no schedule exists.
   Do not double count supplier quotes plus drawings/layouts.

5. Pricing rules:
   Use supplier costs where available.
   Add Fenster product-code markup and labour separately for estimator review.
   Use Adam's codes where possible: SAW, MAW, LAW, ELAW, SAD, DAD, SADSAW, SADMAW, SADLAW, SSD, DSD, etc.
   Quantity stays separate from code.
   If no supplier quote exists, label the result as budget/fallback only.

6. Outputs go here:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs

7. Produce both:
   <Job> - Fenster Pricing Document and Review.xlsx
   <Job> - Fenster Glazing Proposal and Pricing Review.pdf

8. The workbook/PDF must show:
   summary totals, pricing lines, supplier/fallback cost, code, markup, labour, sell total, notes, pricing review table, exclusions, assumptions, RFIs/actions, and source notes.

9. Render the PDF to PNG before final response and check for clipped tables. If pdftoppm.cmd fails, use:
   C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe

10. Recent known outputs:
   Home Bargains Basingstoke:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Pricing Document and Review.xlsx
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Home Bargains Basingstoke - Fenster Glazing Proposal and Pricing Review.pdf
   Latest sell ex VAT: GBP 89,429.22. Roller shutters excluded. ACA supplier cost GBP 12,710 has 25% markup GBP 3,177.50.

   Alkerden:
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Pricing Document and Review.xlsx
   C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\outputs\Alkerden - Fenster Glazing Proposal and Pricing Review.pdf
   Budget sell ex VAT: GBP 588,817.93. No supplier quote; composite windows marked up as aluminium; ED13/ED23 missing dimensions.

11. Be honest with Zac. If a number is not supplier-backed, say it. If a package is missing, mark TBC or excluded. Do not invent quantities, rates, or totals.

12. If changing app behaviour, update the version badge, run a syntax check, commit, push, and deploy Cloudflare Pages if needed.
```

## Pricing Logic Notes

The app has two pricing modes:

1. Native estimating mode: extracted dimensions/types go through the local price engine.
2. Estimator workbook mode: exact workbook sell rates/totals are preserved with `manualOverride`.

Do not mix these blindly. If a real estimator pricing workbook is present, it normally already includes markup, preliminaries, fixings, install allowances, lifts/access, and commercial assumptions. Re-pricing those same rows through the native engine will create large variance.

Commercial allowance rows should be displayed as allowance lines, not as missing-dimension/TBC rows.

## Fenster Pricing Codes And Labour Allowances

Adam's Project Hail Mary pricing-code email defines labour allowances the bot must use when preparing/checking pricing documents:

- `SUPD`: single uPVC door, GBP 250 labour.
- `DUPD`: double uPVC door, GBP 500 labour.
- `SAD`: single aluminium door, GBP 250 labour.
- `DAD`: double aluminium door, GBP 500 labour.
- `ELAW`: extra-large aluminium window, GBP 250 labour.
- `LAW`: large aluminium window, GBP 160 labour.
- `MAW`: medium aluminium window, GBP 160 labour.
- `SAW`: small aluminium window, GBP 160 labour.
- `LPVC`: large uPVC window, GBP 160 labour.
- `MPVC`: medium uPVC window, GBP 160 labour.
- `SPVC`: small uPVC window, GBP 160 labour.
- `SADLAW`: single aluminium door with large aluminium window/screen, GBP 410 labour.
- `SADMAW`: single aluminium door with medium aluminium window/screen, GBP 410 labour.
- `SADSAW`: single aluminium door with small aluminium window/screen, GBP 410 labour.

Quantity is separate from the code. Curtain walling stays separate unless a future curtain-wall code is created. Combined items such as doors with side screens/fanlights need special review and should use the combined codes where appropriate.

In `js/pricing.js`, these are available as `Pricing.LABOUR_ALLOWANCES` and `Pricing.getLabourAllowanceForCode(code)`. The summary install calculation can use them when `pricing.useProductCodeLabourAllowances` is true. This flag is off by default so older calibrated quotes do not move unexpectedly.

## Supplier Rate Miner

`scripts/mine-supplier-rates.py` is a READ-ONLY scanner over the OneDrive quote archive (`Commercial\1. Tender Documents\<client>`). It parses BSW, Vetroseal and Strongdor quotations into line items, grades its own output (arithmetic checks: unit x qty = total, area = w x h with Vetroseal's ~0.30m2 minimum-area billing, lines + extras = stated totals) and flags anything it cannot prove for AI/estimator review. `scripts/build-rate-register.py` aggregates the mined lines into `data/supplier-rates.json` - historical benchmark rates with provenance (quote ref, date, client, job). Never present register rates as firm prices.

Format quirks the parsers already handle (do not re-learn these):

- PDF text extraction differs by engine: pypdf and pdfplumber can give different layouts of the SAME quote; the miner uses whichever yields more text, and totals labels can appear before OR after their amounts.
- BSW: "Qty: 18Prestige T&T" can lose the space; "£" can arrive as U+FFFD; totals sometimes only derivable as TOTAL INC VAT minus VAT; extras sections ("Total Extras Value") hold trims/cills; product names can contain "/" (Foil /Wt Tilt & Turn).
- Vetroseal: rows wrap across lines and column order is unstable - fields are assigned by arithmetic self-consistency, not position; refs can be absent or pure digits; page-header address lines ("97-98 ALSTON DRIVE") leak digits into rows unless buffers terminate at QUOTATION/Page markers; delivery/oversize charges ride as 1x1mm rows.
- Strongdor: SQ PDFs come in quote and drawings variants; drawings have no price table and are classified as reference.
- Aplus is NOT yet machine-parsed (letter + Crystal Reports/Logikal OFFER formats) - files are flagged `aplus-needs-review`.

Pilot (2026-07-16, Zelltec + GCS + Key Property + Datron, 59 files): 42 ok / 14 flagged (all the known Aplus gap) / 0 unexplained anomalies; 972 line items across 18 rate categories. Ground-truthed against 6 visually-read quotes. Register medians are size-blind - large frames price lower per m2 (Crownhill TYPE A glazed T&T = GBP 370/m2 vs small-window T&T ~GBP 580/m2); consider size bands before trusting a median for an unusual frame.

The pilot also proved the archive-first rule: ALWAYS search the client's folder before estimating - it found BSW quote `QT252840 CROWNHILL BUSINESS CTR` (15/07/2026, glazed incl Coolite SKN176ii, GBP 33,839.57 ex VAT) that supersedes the Rev 2 derived aluminium rates for Crownhill.

## OpenAI Enrichment

OpenAI note review is optional and must fail open.

- Do not hardcode API keys in source going forward.
- The user's previous key hit quota/429 during testing.
- Do not spend OpenAI tokens unless the user explicitly asks.
- AI output from a prior successful Whitsbury run was historically saved as `test-results\whitsbury-ai-output\openai-red-fields.json`; the Desktop repo may not contain old `test-results`.
- AI enrichment should suggest/confirm fields and write them into tender questions where confidence is high.
- Fields still unresolved should stay red and require review.

The intended AI role:

- Read notes/spec text.
- Confirm or correct parser fields such as frame, glass, colour, hardware, handle, lock, closer, ironmongery, entrance door reference, and fire/acoustic requirements.
- Prefill tender questions.
- Produce evidence snippets/reasons so the user can trust or reject the prefill.

## Quote PDF Notes

The quote generator supports detailed and compact PDFs.

Important layout expectations:

- Schedule starts below the cover intro instead of overlapping it.
- Long summary labels are truncated safely.
- Notes move to a new page when needed.
- Commercial allowance dimensions show as `Allowance`.
- VAT, install, preliminaries, and exclusions must be clearly shown and not overlap.

## Tender Finder Research

Adam asked whether a bot can scrape the internet for live commercial window and door tenders.

The answer: yes, it is a good idea, but it is a later product beside the estimator, not a replacement for the estimator.

Current file: `js/tenderFinder.js`.

It defines:

- Official public sources: Find a Tender and Contracts Finder.
- Paid construction lead platforms to benchmark: Barbour ABI and Glenigan.
- Useful keyword searches for Fenster: commercial windows, aluminium windows, aluminium doors, windows and doors, curtain walling, glazing works, replacement windows, external doors, louvre panels, facade glazing.
- CPV codes: `44221000`, `45421100`, `45441000`, `45443000`.
- Basic opportunity scoring for commercial glazing relevance.
- A draft email response to Adam.

Do not build the full tender monitor before the estimator workflow is reliable unless the user changes priority.

## Commands

Syntax smoke check:

```powershell
node -e "const fs=require('fs'); for (const f of ['js/dataExtractor.js','js/pricing.js','js/quoteGenerator.js','js/app.js','js/projectHailMary.js','js/tenderFinder.js']) new Function(fs.readFileSync(f,'utf8')); console.log('syntax ok')"
```

Run a tender pack through the CLI harness:

```powershell
node scripts\run-tender-pack.mjs --dir "C:\path\to\input-pack" --out "test-results\some-output-folder"
```

Check git:

```powershell
git status --short
git log -1 --oneline
git remote -v
```

Use `npm.cmd` instead of `npm` if PowerShell blocks `npm.ps1`.

## Development Rules For Future Agents

- Read `HANDOVER.md` before editing.
- Work in `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant`.
- Keep the browser app and CLI harness using the same extraction/pricing logic.
- Use `DataExtractor.buildScopePlan(documents)` for source-of-truth decisions before trusting a quote. It records which documents are source of truth, validation/reference evidence, supplier evidence, duplicates, or excluded/admin documents.
- The Step 2 Estimator Dashboard is the main Adam review surface. It summarises status, source-of-truth decisions, immediate actions, extracted requirements, risks, supplier coverage, pricing codes, checklist, and proposal summary draft.
- Do not add one-off script logic that disagrees with the website.
- When a bug is found in a tender-pack run, fix shared modules first, then re-run the CLI harness.
- Push meaningful changes; the user expects the hosted app to update from the repo.
- Cloudflare Pages is currently deployed by building a clean artifact with `scripts\build-pages.ps1` and running `npx.cmd wrangler pages deploy dist-pages --project-name glazing-quote-assistant --branch main`.
- Update the version badge when user-facing behaviour changes.
- Avoid spending OpenAI quota during debugging unless requested.
- Treat actual estimator workbooks as stronger evidence than PDFs/drawings.
- Treat type sheets such as `Window Types` / `External Door Types` as reference/spec evidence, not priced item scope, when schedules exist.
- Treat image-only drawings as needing OCR/takeoff before accurate quoting.
- Preserve unrelated user changes. Do not reset the repo.

## Best Next Technical Work

1. Add a real automated regression suite around saved packs so Whitsbury, Brandon, Gresty, and Project Hail Mary stay stable.
2. Build proper OCR/takeoff for scanned/image-heavy drawings.
3. Harden `js/projectHailMary.js` supplier quote ingestion for Sheerline/RAS/glass order/bay layout PDFs.
4. Make commercial extras/prelims a structured model rather than loose allowance rows.
5. Finish ZIP/DOCX/MSG intake through the worker path for large packs.
6. Make OpenAI enrichment cheaper and safer: document hash cache, hard token cap, smaller model, visible spend warning, and manual trigger.
7. Add approval workflow: parsed scope, AI assumptions, supplier quote check, coding table, estimator approval, quote generation, final issue.
8. After estimating is credible, build the backend tender monitor and dashboard that emails `commercial@fensterglazing.com`.

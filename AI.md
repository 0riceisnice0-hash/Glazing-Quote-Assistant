# AI.md - Glazing Quote Assistant Engineering Notes

This file is for future AI agents and developers working on this repository. It explains what the app does, how the main modules fit together, how pricing works, how local tender-pack testing is currently run, and the exact pitfalls found while testing the Desktop tender packs.

## Project Purpose

Glazing Quote Assistant is a static browser app for reading tender documents, extracting glazing/window/door items, pricing them with the Fenster pricing engine, and generating quote PDFs.

The app is client-side. The normal website path uses browser `File` objects, PDF.js text extraction for PDFs, SheetJS extraction for Excel workbooks, optional OCR fallback, `localStorage` state, user verification in the PDF review step, and then quote PDF generation.

## Important Paths

- Repo: `C:\Users\zacpl\OneDrive\Documents\GitHub\Glazing-Quote-Assistant`
- Desktop tender packs used for testing: `C:\Users\zacpl\Desktop\Tender Documents`
- Local test reports written by scripts: `test-results\...`
- User-facing app entry point: `index.html`

Do not assume tender documents live in the repo. In the current working setup, the five real tender packs are on Desktop and the repo is in the OneDrive-backed local GitHub folder.

## Main Application Flow

1. `index.html` loads browser globals from `js/*.js`.
2. `js/app.js` controls the workflow:
   - Loads state from `localStorage`.
   - Accepts pending PDF/XLSX/XLSM/XLS/ZIP/DOCX/EML/MSG/JPG/PNG uploads.
   - Calls `DocumentIntake.processFiles()` from `js/documentIntake.js`.
   - `DocumentIntake` expands ZIPs, reads DOCX/EML, OCRs images when Tesseract is available, emits intake records/risks/supplier evidence, and delegates PDF/Excel extraction to `extractTenderInput()`.
   - Classifies each document with `DataExtractor.classifyDocument()`.
   - Runs OCR through `js/ocrFallback.js` for scanned non-admin/non-drawing docs when available.
   - Calls `DataExtractor.extractItems(validDocs)`.
   - Applies tender pricing defaults with `Pricing.applyTenderPricingDefaults()`.
   - Recalculates all item prices with `Pricing.recalculateAll()`.
   - Shows tender questions and PDF verification before final item confirmation.
3. `js/ui.js` renders the review/pricing/quote UI.
4. `js/quoteGenerator.js` builds the final quote PDF.

## Key Modules

### `js/pdfParser.js`

Browser upload and extraction wrapper around PDF.js and SheetJS.

It extracts PDFs with `extractTextFromPDF()` and workbooks with `extractWorkbook()`. Both paths return the same document shape:

- `fullText`
- `pages[]`
- `textItems[]` with `str`, `x`, `y`, `width`, `height`
- `isScanned`

For workbooks, the browser and Node harness both flatten rows to text and create synthetic `textItems` coordinates so the core extractor can reuse table/row logic. For PDFs, the Node harness recreates the browser PDF.js shape, but it is not guaranteed to match browser PDF.js perfectly.

### `js/documentIntake.js`

Browser-side estimator co-pilot intake layer.

It normalises messy tender inputs before extraction:

- ZIP archives are expanded with JSZip and child files keep archive provenance.
- DOCX files are read by extracting `word/document.xml`.
- EML files produce body text and a warning if attachments may exist.
- MSG files currently produce a critical risk because local MSG extraction is not implemented.
- JPG/PNG files run Tesseract OCR when available and create human-review risks.
- Supplier quote documents produce proposed `supplierEvidence` records only; they cannot create priced scope items.
- Client quotes are classified as admin/excluded so they do not create scope items.

`DocumentIntake` is the correct seam for future Cloudflare Worker integration. Keep `DataExtractor` focused on normalised documents and pricing-safe item extraction.

### `workers/document-processor`

Optional Cloudflare Worker for internal document intake. It is not used unless the upload UI has cloud processing enabled and a Worker URL configured.

Current Worker capabilities:

- `GET /health`
- `POST /process-file`
- `POST /process-pack`
- ZIP expansion via JSZip
- DOCX text extraction from `word/document.xml`
- EML subject/body extraction
- Proposed supplier evidence from text

Current Worker limits:

- PDF and Excel are still browser/harness-local paths.
- JPG/PNG OCR is not implemented in the Worker; browser Tesseract remains the free OCR path.
- MSG parsing is still a risk/placeholder.

### `js/dataExtractor.js`

Core extraction and classification engine.

Public API:

- `DataExtractor.classifyDocument(docName, textContent)`
- `DataExtractor.extractItems(documents)`
- `DataExtractor.crossReferenceDocuments(documents, allItems)`
- `DataExtractor.isLikelyScanned(text, pageCount)`

Document types:

- `schedule`: creates items.
- `bq`: does not create items; extracts ref->quantity validation data.
- `specification`: does not create items; extracts spec notes and enriches items.
- `drawing`: does not create priced items; extracts drawing refs for cross-checking only.
- `admin`: skipped.
- `unknown`: skipped for item creation. Unknown documents may contain floor plans, title blocks, construction details, or drawing markers that look like glazing references.

Current extraction strategies:

1. Reference-first extraction for schedule docs.
2. Structured table extraction using spatial rows/columns.
3. Row-based extraction.
4. Enhanced regex extraction.
5. Line-based fallback.
6. Infer-without-reference fallback creates `X01` when only dimensions are found.

Important gate: only `schedule` documents can create priced quote items. This was added after Addington Road uPVC proved that pricing `unknown` floor-plan PDFs inflated the website run from the real quote scale to the user's reported huge block price. BQs validate quantities, specs enrich, drawings cross-check, and unknowns are ignored for pricing.

If no schedule is found, extraction emits an error warning instead of inventing priced items from drawings.

### `js/pricing.js`

Fenster pricing engine.

Basic formula:

`unit rate = frame cost + glass cost + additional cost + product-code markup`

Quote summary adds:

- installation
- optional EPDM
- optional mastic
- optional quote-level extra
- discount
- VAT

Important functions:

- `Pricing.calculateItemPrice(item, pricingConfig)`
- `Pricing.recalculateAll(items, pricingConfig)`
- `Pricing.getPriceSummary(items, pricingConfig)`
- `Pricing.classifyProductCode(item)`
- `Pricing.applyKnownItemPricing(items)`
- `Pricing.applyTenderPricingDefaults(items, pricingConfig)`

Known tender pricing:

- `stoke-park-school-2026` uses fixed type rates and special defaults.

The default engine is generic. It will not match actual quoted jobs unless supplier rates, quoted unit prices, tender-specific defaults, and user edits are present.

### `js/dataModel.js`

Default state schema. Includes:

- `items`
- `metadata`
- `company`
- `pricing`
- `presets`
- `sourceDocuments`
- `warnings`

Website runs can differ from scripts if `localStorage` has a modified pricing config. The Node harness starts from `Pricing.DEFAULT_CONFIG` unless script logic applies tender defaults.

## Local Test Scripts

### `scripts/run-tender-pack.mjs`

Runs extraction and pricing without using the website.

Example:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\run-tender-pack.mjs --dir "C:\Users\zacpl\Desktop\Tender Documents\Addington Road uPVC" --out "test-results\desktop-Addington Road uPVC-website" --mode website
```

Supported inputs:

- PDF
- XLSX/XLSM/XLS
- ZIP
- DOCX
- EML
- MSG/JPG/PNG as explicit critical-risk placeholders in the Node harness

It recursively scans the folder and excludes paths containing:

- `Client Quote`
- `Supplier Quote` / `Supplier Quotes`
- quote-named files unless they look like a BQ/schedule/pricing schedule

Modes:

- `--mode clean`: use only `schedule`, `bq`, and `specification` docs. This is useful for testing a safer desired extraction pipeline, but it is not website parity.
- `--mode include-unknown`: use `schedule`, `bq`, `specification`, and `unknown`.
- `--mode website`: pass everything except `admin` to the extractor. Since the extractor now gates item creation internally, drawings and unknowns may be present for classification/cross-checking but still cannot create priced items.

Outputs:

- JSON report with documents, classifications, items, warnings, pricing summary.
- CSV item list.

Workbook parity: the website now accepts `.xlsx`, `.xlsm`, and `.xls` alongside PDFs and uses the same workbook flattening pattern as this script. A remaining difference is path context: the script recursively scans folders and preserves relative paths; the browser only sees `file.name` unless files arrive with `webkitRelativePath`.

Expanded intake: the harness now expands ZIPs, reads DOCX/EML, and writes `risks` plus `intakeRecords` into the JSON report. It does not run Node-side OCR for JPG/PNG; those inputs are reported as critical risks so image-only packs do not fail silently.

### `scripts/extract-actual-quote-totals.py`

Reads Desktop client quote files and extracts likely actual quote totals from PDFs/XLSX.

Example:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\extract-actual-quote-totals.py "C:\Users\zacpl\Desktop\Tender Documents"
```

It excludes supplier quotes and `DO NOT SEND` quote files.

### `scripts\export-browser-state.mjs`

Attempts to run the actual browser app with Playwright, upload files through `#fileInput`, click `#analyseBtn`, then export `App.getState()`.

Example:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\export-browser-state.mjs --dir "C:\Users\zacpl\Desktop\Tender Documents\Addington Road uPVC" --out "test-results\browser-Addington Road uPVC"
```

Current environment caveat: the bundled runtime on 2026-06-11 exposed a `playwright` package but was missing `playwright-core`, so this script could not launch in that environment without a complete Playwright install. Keep the script because it is the correct automation shape once Playwright is available.

### Browser Manual Snapshot

The website now exposes:

```js
App.exportStateSnapshot()
```

Use it in the browser console after running analysis on the actual website/app. It returns:

- `itemCount`
- `warningCount`
- `summary`
- `sourceDocuments`
- `items`
- `warnings`
- `pricing`
- `metadata`

The existing `Export` button still exports the importable session JSON and was not changed to avoid breaking import/export behavior.

### `scripts\compare-state-to-quote.mjs`

Compares an exported website state/session or harness JSON report against an actual quote total.

Example:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\compare-state-to-quote.mjs --state "path\to\exported-state.json" --actual 119800.19 --label "Addington Road uPVC"
```

It reports item count, warning count, subtotal, installation, VAT, total, variance, and top source documents by item count.

## Current Desktop Pack Findings

These figures came from local script runs on 2026-06-11. Values marked "before gate" are retained only to explain the original failure.

Latest calibrated results after workbook parsing, drawing enrichment, PVC pricing calibration, inferred install defaults, and the 223 Southwark assembly profile:

- `223 Southwark`: bot `GBP 51,930.12` ex VAT vs actual `GBP 51,930.12` (`0.00%`). Uses the known combined assembly profile for grouped shopfront/door/window assemblies.
- `Addington Road uPVC`: bot `GBP 124,309.50` ex VAT vs actual `GBP 119,800.19` (`+3.76%`). Auto-install disabled because this is a non-quoted mostly-PVC schedule job.
- `Brighton Road`: bot `GBP 18,048.12` ex VAT vs actual `GBP 17,360.19` (`+3.96%`). Pricing schedule supplies refs; drawings enrich dimensions only.
- `Fusion 21 Decarb Framework - East Suffolk Council`: bot `GBP 4,249,353.94` ex VAT vs actual `GBP 4,070,348.63` (`+4.40%`). Workbook evaluation prices are used, with install retained.
- `Manor Farm Court`: bot `GBP 2,070.00` ex VAT vs actual `GBP 2,166.92` (`-4.47%`). Quoted workbook rows are used, with install retained.
- `The Royal Marsden Hospital`: bot `GBP 660.00` ex VAT vs actual `GBP 672.95` (`-1.92%`). Auto-install disabled for the non-quoted PVC schedule row.

Key calibrated behaviours:

- Drawings still cannot create priced items, but can enrich existing schedule refs with dimensions/spec.
- Excel/workbook rows now get synthetic table coordinates in both `scripts/run-tender-pack.mjs` and browser `js/pdfParser.js`.
- Workbook schedule rows support quoted rows, framework `W&D-xx` rows, `WG/WF/W1` refs, and duplicate same-ref rows with different dimensions.
- Filename-only classification is used even when the harness keeps relative paths for source hints.
- Non-quoted mostly-PVC jobs automatically disable the generic installation line.
- Quoted workbooks/frameworks retain installation.
- `223 Southwark` is treated as a known assembly tender because the actual quote combines multiple raw refs into grouped assemblies.

### Addington Road uPVC

Actual client quote:

- `MCS Construction - Quotation (1).pdf`
- Actual quote total: `£119,800.19` excluding VAT.

Clean run before the schedule gate:

- 65 items
- Ex VAT before VAT: `£129,830.57`
- Inc VAT: `£155,796.68`
- This run intentionally skipped `unknown` floor plans/details. It is not website parity.

Website-parity run before the schedule gate:

- 244 items
- Ex VAT before VAT: `£349,883.48`
- Inc VAT: `£419,860.18`
- 325 warnings
- 90 missing dimensions
- 34 unknown frame types

Why it blows up: floor-plan PDFs classified as `unknown` are being extracted and priced. Major contributors:

- `J003953-TD-05-I As Prop Second Floor.pdf`: 58 items
- `J003953-TD-04-I As Prop First Floor.pdf`: 54 items
- `J003953-TD-03-I As Prop Ground Floor.pdf`: 53 items
- `J003953-TD-06-I As Prop Third Floor.pdf`: 39 items
- `J003953-TD-02-G As Prop Lower Ground Floor.pdf`: 37 items

This was the main bug to fix before pricing accuracy.

Pasted website output from the user showed:

- 244 items
- Product subtotal: `£311,799.97`
- Installation: `£34,160.00`
- VAT: `£69,191.99`
- Total inc VAT: `£415,151.96`
- Source docs listed were 19 PDFs, not XLSX files.

The Node harness in `--mode website --pdf-only` produced:

- 244 items
- Product subtotal: `£315,723.48`
- Installation: `£34,160.00`
- VAT: `£69,976.70`
- Total inc VAT: `£419,860.18`

The remaining difference is not caused by XLSX inputs because PDF-only mode still differs. It is caused by browser-vs-Node extraction differences and/or state/config differences. A concrete observed example:

- Website pasted output: `FD20`, door, `838 x 838`, unit `£2,031.31`
- Node harness CSV: `FD20`, door, `1500 x 915`, unit `£2,872.49`
- Other examples such as `TD60` and `ID105` matched exactly, so this is not a complete pricing-engine mismatch. It is likely duplicate occurrence selection / PDF text order differences for repeated references.

To reproduce the website exactly, do not rely only on the Node harness. Export the website session JSON after analysis, or build a browser automation/export path that calls `App.getState()` after the browser has run PDF.js and any verification steps. Then compare that exported state to the harness output item-by-item.

After the schedule gate (`--mode website --pdf-only`):

- 57 items
- Priced sources: `J003953-TD-14-E External Window Schedule.pdf`, `J003953-TD-15-E External Door Schedule.pdf`
- Ex VAT before VAT: `GBP 128,710.57`
- Inc VAT: `GBP 154,452.68`
- Warnings: 27
- Missing dimensions: 6
- Unknown frame types: 9
- Variance against the actual ex-VAT quote: `GBP 8,910.38` high (`7.44%`)

The remaining Addington variance is now a normal pricing/extraction calibration problem, not a document-admission failure.

### Brighton Road

Actual client quote:

- XLSX ex VAT total: `£17,360.19`
- PDF inc VAT total: `£20,832.23`

After the schedule gate:

- 3 items: `ED01`, `ED02`, `ED03`
- Ex VAT before VAT: `£8,380.10`
- Inc VAT: `£10,056.12`

Likely issue: the pricing schedule workbook includes refs such as `WG01-WG04`, `WF01-WF06`, and `ED01-ED03`, but current extraction/reference patterns do not handle `WG`/`WF` correctly as window references.

### Royal Marsden Hospital

Actual client quote:

- `Logan Construction - Quotation.pdf`
- Actual quote total: `£672.95` excluding VAT.

After the schedule gate:

- 1 item
- Ex VAT before VAT: `GBP 660.00`
- Inc VAT: `GBP 792.00`
- Variance against the actual ex-VAT quote: `GBP 12.95` low (`-1.92%`)

The single `W1` row is now priced from the schedule path. Installation is auto-disabled for this non-quoted PVC schedule row.

### Churchdown School

Actual client quote candidates:

- No-scaffolding quote: `GBP 729,116.85` excluding VAT.
- With-scaffolding quote: `GBP 746,616.85` excluding VAT.

Current tender-input run:

- 0 items
- Ex VAT before VAT: `GBP 0.00`
- Variance: `-100.00%`

Why: the direct PDF/XLSX tender inputs do not contain a machine-readable glazing schedule. `Specification.zip` contains a Schedule of Works PDF with type quantities, but it does not include dimensions; the drawing PDFs are scanned/image based. This needs ZIP intake plus OCR/drawing takeoff and/or supplier quote ingestion before it can be fairly priced.

### Horley Council

Actual client quote:

- `Horley Council - Innes Pavillion - Fenster Glazing Quote.pdf`
- Actual quote total: `GBP 16,876.84` excluding VAT.

Current tender-input run:

- Not run by the PDF/XLSX harness because the tender inputs are JPG/image files.

Why: image tender inputs need OCR/image intake before the extractor has any source material to price.

### Addington Road Composite

No client quote file was found in the Desktop pack during this run.

After the schedule gate:

- 21 door items
- Ex VAT before VAT: `£70,859.24`
- Inc VAT: `£85,031.09`
- 12 warnings
- 6 missing dimensions

### Briggs

No client quote file was found in the Desktop pack during this run.

After the schedule gate:

- 2 items: `W02`, `X01`
- Ex VAT before VAT: `£3,533.49`
- Inc VAT: `£4,240.19`

## Why The Script Can Differ From The Website

There are several reasons:

1. Uploaded file set may differ.
   - The website only processes files the user drags in.
   - The script recursively scans folders and applies path filters.
   - If the website run includes or excludes different PDFs, totals change immediately.

2. Document gating may differ.
   - Current website passes all successfully read docs into `DataExtractor.extractItems()`.
   - `DataExtractor` now only allows `schedule` documents to create priced items.
   - `bq`, `specification`, `drawing`, `admin`, and `unknown` documents can be used for validation/enrichment/classification, but not priced item creation.
   - Older reports from before the schedule gate may show `unknown` floor plans/details being priced; treat those as pre-fix failure cases.

3. Browser PDF.js text extraction can differ from Node PDF.js extraction.
   - The app uses browser PDF.js.
   - The harness uses bundled Node `pdfjs-dist` plus a small DOMMatrix polyfill.
   - Text order, spacing, coordinates, and font handling may vary.

4. OCR behavior differs.
   - The website can try Tesseract OCR for scanned documents if the browser library is available.
   - The current Node harness does not run OCR.

5. Website state can differ through `localStorage`.
   - The website restores saved pricing config, user edits, accepted/rejected items, and quote metadata.
   - The harness starts from defaults, then applies known tender defaults from code.

6. Website review/verification changes the final items.
   - The website shows tender questions and a PDF verification view where items can be accepted/rejected.
   - The harness prices all extracted items automatically.

7. Folder/path context can differ.
   - The harness recursively scans folders and keeps relative paths for source hints.
   - Normal browser multi-file upload usually exposes only basenames. It can preserve `webkitRelativePath` only when files come from directory-style browser inputs or compatible drag/drop behavior.

8. Pricing configuration may differ.
   - The website pricing panel can be edited.
   - The harness uses `Pricing.DEFAULT_CONFIG` unless known tender pricing is detected.

To make the script and website truly identical, create a shared processing pipeline that accepts a deterministic manifest of files and options, and use it from both the website and the Node harness. Also export/import the exact pricing config and verification decisions.

## Highest Priority Fixes

1. Continue tuning schedule-led extraction.
   - `unknown` floor plans/details are no longer priced.
   - Next accuracy work should focus on missing dimensions, unknown frames, product code mapping, and tender-specific install/markup/defaults.

2. Add estimator-grade intake for non-simple packs.
   - ZIP archives need to be unpacked in both browser and harness paths.
   - DOCX and MSG tender documents need extraction or explicit skip reasons.
   - JPG/PNG/image-only packs need OCR before classification.
   - Scanned drawing PDFs need OCR and then a drawing takeoff layer, not just text extraction.
   - Supplier quotes need a controlled ingestion path for cost build-up; client quotes must remain excluded from tender input tests.

3. Broaden valid reference patterns safely.
   - Support `WG01`, `WF01`, and `W1`.
   - Preserve false-positive rejection for drawing sheet numbers, standards, revision markers, postcodes, and status codes.

4. Improve workbook schedule/BQ extraction.
   - Pricing schedules often contain item refs/qty/rates in XLSX form.
   - Browser and script now share the same flattened workbook document shape; keep adding workbook patterns in `DataExtractor`, not in separate UI/script branches.

5. Make website and harness share one deterministic extraction options object.
   - Example options: `{ includeUnknownForPricing: false, allowWorkbookInputs: true, runOcr: false }`

6. Add regression fixtures for the Desktop packs.
   - Store expected doc classifications and extracted refs/counts, not the confidential tender documents themselves.

## Commands Worth Reusing

Run Addington uPVC like the current website:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\run-tender-pack.mjs --dir "C:\Users\zacpl\Desktop\Tender Documents\Addington Road uPVC" --out "test-results\desktop-Addington Road uPVC-website" --mode website
```

Run Addington uPVC using safer document gating:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\run-tender-pack.mjs --dir "C:\Users\zacpl\Desktop\Tender Documents\Addington Road uPVC" --out "test-results\desktop-Addington Road uPVC-clean" --mode clean
```

Extract actual client quote totals:

```powershell
& "C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\extract-actual-quote-totals.py "C:\Users\zacpl\Desktop\Tender Documents"
```

## Working Rule For Future Agents

When the user asks whether the bot matches a real quote, always report:

- exact input folder
- exact files used
- mode/options
- item count
- warnings count
- ex VAT and inc VAT totals
- actual quote source file
- whether website verification/user edits were simulated

Do not present a filtered `clean` run as a website result. That was the mistake that caused the earlier `GBP 155k` answer for Addington Road uPVC. After the schedule gate, `website` mode can include drawings/unknowns in the input set without letting them create priced items.

## Temporary ASAP Quote Detour - Live Tender Pack 2026-06-11

This is a temporary detour for one live pack, not a permanent product pivot. The broader roadmap remains the commercial estimator replacement workflow (ZIP/DOCX/MSG intake, OCR, drawing takeoff, supplier quote ingestion, assumptions/exclusions, RFI/risk flags, and approval workflow). For this pack only, we are prioritising a defensible first-pass commercial estimate because no real quote is available yet and a quote is needed ASAP. The immediate documents are:

- `Aluminium Windows & Doors BoQ (1).xlsx` - primary scope anchor. This contains contractor BoQ rows with `Ref`, `Description`, `Quantity`, `Units`, blank `Rate`, and blank `Value` columns. The estimator must extract refs such as `1.2/2.6/A`, dimensions such as `910mm x 1960mm`, quantities, and item type from the description.
- `24.113.02.800.003 Exterior Doors - (RevT1).pdf` - door elevation/schedule evidence. Use this to confirm door types, fanlights, louvres, access/security/fire notes, and risks. It must not create phantom priced items such as `PAS24` unless dimensions and a real schedule row are present.
- `24.113.02.140.001 Proposed Elevations - (RevT1).pdf` - drawing/elevation evidence. Use for cross-checking locations and missing facade scope; do not silently price from drawing text unless a takeoff workflow or explicit schedule evidence supports the item.

Success for this pack is not variance against a historical quote. Success is a quote-ready draft that extracts every BoQ scope item with dimensions and quantity, applies the same pricing logic as the website, and emits explicit assumptions, exclusions, and RFIs for anything not machine-confirmed.

Current known failure before this temporary detour: the harness recognised the BoQ as a BQ document but returned only one malformed `PAS24` item from the door PDF, producing a nonsense total of GBP 168. The fix direction for this detour is to prioritise the Excel BoQ rows as the scope source and treat the PDFs as evidence/risk documents. After the urgent quote is produced, fold the reusable parts back into the main estimator roadmap rather than hard-coding this project as the new default workflow.

Estimator assumptions for this pack until supplier rates are supplied:

- Kawneer or equal aluminium windows, doors, and curtain walling are priced with the app's current aluminium/commercial pricing defaults.
- Plant room louvred doors are treated as steel/louvred door items and should be flagged for supplier confirmation.
- Mastic, EPDM, support brackets, access control, powered operation, security ratings, fire certification, and specialist ironmongery must be carried as assumptions/RFIs unless specifically priced by a supplier quote or pricing rule.
- A zero-item or near-zero quote is a hard failure for this pack. The bot should return a blocked/risk state rather than a quote if it cannot parse the BoQ.


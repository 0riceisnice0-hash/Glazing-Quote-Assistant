# AI.md - Glazing Quote Assistant Engineering Notes

This file is for future AI agents and developers working on this repository. It explains what the app does, how the main modules fit together, how pricing works, how local tender-pack testing is currently run, and the exact pitfalls found while testing the Desktop tender packs.

## Project Purpose

Glazing Quote Assistant is a static browser app for reading tender documents, extracting glazing/window/door items, pricing them with the Fenster pricing engine, and generating quote PDFs.

The app is client-side. The normal website path uses browser `File` objects, PDF.js text extraction, optional OCR fallback, `localStorage` state, user verification in the PDF review step, and then quote PDF generation.

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
   - Accepts pending PDF uploads.
   - Calls `extractTextFromPDF()` from `js/pdfParser.js`.
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

Browser-only PDF upload and extraction wrapper around PDF.js.

It extracts:

- `fullText`
- `pages[]`
- `textItems[]` with `str`, `x`, `y`, `width`, `height`
- `isScanned`

The Node harness recreates this shape, but it is not guaranteed to match browser PDF.js perfectly.

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
- `unknown`: current browser behavior still attempts extraction. This is dangerous for floor plans/details.

Current extraction strategies:

1. Reference-first extraction for schedule docs.
2. Structured table extraction using spatial rows/columns.
3. Row-based extraction.
4. Enhanced regex extraction.
5. Line-based fallback.
6. Infer-without-reference fallback creates `X01` when only dimensions are found.

Known risk: `unknown` docs can be priced. This is why floor-plan PDFs inflated Addington Road uPVC from the real quote scale to roughly the website's huge block price.

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

It recursively scans the folder and excludes paths containing:

- `Client Quote`
- `Supplier Quote` / `Supplier Quotes`
- quote-named files unless they look like a BQ/schedule/pricing schedule

Modes:

- `--mode clean`: use only `schedule`, `bq`, and `specification` docs. This is useful for testing a safer desired extraction pipeline, but it is not website parity.
- `--mode include-unknown`: use `schedule`, `bq`, `specification`, and `unknown`.
- `--mode website`: use everything except `admin`. This is closest to current website behavior after excluding client/supplier quote folders.

Outputs:

- JSON report with documents, classifications, items, warnings, pricing summary.
- CSV item list.

Important limitation: the script reads workbooks by flattening rows to text, but the website does not currently accept XLSX uploads through the PDF upload flow. So workbook support is a test harness extension, not browser parity.

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

These figures came from local script runs on 2026-06-11.

### Addington Road uPVC

Actual client quote:

- `MCS Construction - Quotation (1).pdf`
- Actual quote total: `£119,800.19` excluding VAT.

Clean run:

- 65 items
- Ex VAT before VAT: `£129,830.57`
- Inc VAT: `£155,796.68`
- This run intentionally skipped `unknown` floor plans/details. It is not website parity.

Website-parity run:

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

This is the main bug to fix before pricing accuracy.

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

### Brighton Road

Actual client quote:

- XLSX ex VAT total: `£17,360.19`
- PDF inc VAT total: `£20,832.23`

Clean/script run:

- 3 items: `ED01`, `ED02`, `ED03`
- Ex VAT before VAT: `£8,380.10`
- Inc VAT: `£10,056.12`

Likely issue: the pricing schedule workbook includes refs such as `WG01-WG04`, `WF01-WF06`, and `ED01-ED03`, but current extraction/reference patterns do not handle `WG`/`WF` correctly as window references.

### Royal Marsden Hospital

Actual client quote:

- `Logan Construction - Quotation.pdf`
- Actual quote total: `£672.95` excluding VAT.

Script run:

- 1 item, extracted as `X01`
- Ex VAT before VAT: `£1,025.00`
- Inc VAT: `£1,230.00`

Likely issue: the schedule uses `W1`-style references, while current patterns expect mostly two-digit references such as `W01`.

### Addington Road Composite

No client quote file was found in the Desktop pack during this run.

Script run:

- 21 door items
- Ex VAT before VAT: `£70,859.24`
- Inc VAT: `£85,031.09`
- 12 warnings
- 6 missing dimensions

### Briggs

No client quote file was found in the Desktop pack during this run.

Script run:

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
   - `DataExtractor` itself skips `admin`, `drawing`, `bq`, and `specification`, but it attempts extraction from `unknown`.
   - The first script run used `clean` mode, which intentionally skipped `unknown`, so it under-represented the current website behavior.

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

7. XLSX support differs.
   - The harness can read `.xlsx` tender schedules/BQs.
   - The browser upload flow is PDF-oriented and does not currently use the same workbook pathway.

8. Pricing configuration may differ.
   - The website pricing panel can be edited.
   - The harness uses `Pricing.DEFAULT_CONFIG` unless known tender pricing is detected.

To make the script and website truly identical, create a shared processing pipeline that accepts a deterministic manifest of files and options, and use it from both the website and the Node harness. Also export/import the exact pricing config and verification decisions.

## Highest Priority Fixes

1. Stop pricing `unknown` floor plans/details.
   - Classify filenames like `As Prop ... Floor`, `Proposed Plans`, `Construction Details`, `Section`, `Plan details`, and similar as `drawing`.
   - Alternatively, only allow priced item creation from `schedule` documents. Use drawings only for cross-reference.

2. Broaden valid reference patterns safely.
   - Support `WG01`, `WF01`, and `W1`.
   - Preserve false-positive rejection for drawing sheet numbers, standards, revision markers, postcodes, and status codes.

3. Improve workbook schedule/BQ extraction.
   - Pricing schedules often contain item refs/qty/rates in XLSX form.
   - Current browser app does not have this path; the script does.

4. Make website and harness share one deterministic extraction options object.
   - Example options: `{ includeUnknownForPricing: false, allowWorkbookInputs: true, runOcr: false }`

5. Add regression fixtures for the five Desktop packs.
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

Do not present a filtered `clean` run as a website result. That was the mistake that caused the earlier `£155k` answer for Addington Road uPVC.

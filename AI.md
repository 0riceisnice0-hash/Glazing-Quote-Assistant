# AI Agent Guide

This repo is the Fenster Glazing Quote Assistant: a static browser app that ingests tender packs, extracts glazing scope, prices it with local rules, lets the user adjust assumptions, and generates branded quote PDFs.

Use this file as the deeper technical map. For the immediate state and next steps, read `HANDOVER.md` first.

## Current Snapshot

- Live app type: static HTML/CSS/JS, intended for GitHub Pages.
- Deployment path: push to `main`; there are currently no GitHub Actions workflows in this repo.
- Current visible app version: `v2026.06.25.5` in `index.html` and `js/app.js`.
- Current confirmed pushed commit before this doc refresh: `3d4d838 Recognize generic pricing workbooks`.
- Local repo path used by the user: `C:\Users\zacpl\OneDrive\Documents\GitHub\Glazing-Quote-Assistant`.
- The user has explicitly allowed editing this OneDrive repo, but avoid unrelated OneDrive locations.

## Main Files

- `index.html`: app shell, upload UI, version badge, script cache-busting.
- `js/app.js`: main orchestration and UI state.
- `js/documentIntake.js`: file intake, ZIP/DOCX/MSG/PDF/XLSX routing support.
- `js/pdfParser.js`: PDF text extraction and helper parsing.
- `js/dataExtractor.js`: document classification, schedule extraction, pricing workbook extraction, validation warnings.
- `js/pricing.js`: price engine, inferred defaults, commercial markups/allowances, install/VAT handling.
- `js/aiEnrichment.js`: optional OpenAI note review and field prefill.
- `js/ui.js`: tender questions and review UI.
- `js/quoteGenerator.js`: branded detailed/compact PDF quote generation.
- `workers/document-processor/`: planned/partial worker direction for heavier document processing.
- `scripts/run-tender-pack.mjs`: local CLI regression harness that runs tender packs through the same extraction/pricing logic without using the website.
- `test-results/`: saved extraction reports, regression outputs, and generated quotes.

## End-To-End Workflow

1. User uploads tender documents in the browser.
2. Intake code normalises files, expands supported containers where possible, and sends text/table content to extraction.
3. `dataExtractor.js` classifies each document as schedule, pricing workbook, BOQ, specification/reference, drawing, admin, or unknown.
4. Only scope-bearing documents create priced items.
5. `pricing.js` prices items and applies inferred defaults such as install, EPDM, mastic, VAT, preliminaries, or commercial allowance rules.
6. Optional OpenAI note review checks notes/spec text against extracted fields and suggests prefills.
7. UI shows tender questions and red review boxes for missing/uncertain fields.
8. User confirms/edits assumptions.
9. `quoteGenerator.js` creates detailed and compact branded PDFs.

## Extraction Rules That Matter

The quote bot should be conservative. Do not price every document that contains window or door words.

- Pricing workbooks are the source of truth when present.
- If a Fenster/R1-style pricing workbook is present, skip other schedule PDFs/layouts as priced scope to avoid duplicate bogus items.
- External/opening schedule workbooks are preferred over duplicate schedule PDFs.
- Opening type sheets are reference/spec documents, not priced scope.
- Supplier quotation PDFs, glass order PDFs, bay layouts, elevations, and image-heavy drawings are evidence unless a dedicated parser proves they are a priced schedule.
- BOQs can be scope when they are clearly contractor pricing/scope workbooks, but should not override a Fenster pricing workbook.
- Materials schedules/specifications enrich assumptions but should not create priced line items by themselves.
- Dimensionless markers should be dropped unless they are explicit commercial allowance rows.

## Known Supported Job Patterns

### Whitsbury / Hartford Care Home

Primary scope came from the external opening schedule workbook and related PDFs.

Current stable regression result:

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

### Brandon Estate REV 2

Primary scope came from `Pricing Document - Brandon Estate REV 2.xlsx`.

Current stable regression result:

- Items: 51
- Total/subtotal ex VAT: GBP 7,196,695.63
- Risks: none in the final pricing workbook run.

Important behaviours:

- Pricing workbook rows preserve exact sell rates and totals.
- Commercial allowance rows are included as allowance lines.
- Generic install, EPDM, mastic, and VAT are disabled because the estimator workbook already includes commercial pricing/allowances and is normally quoted plus VAT.

### Gresty Road

There are two states:

- Early drawing/spec-only budget takeoff was manual/assumption-heavy and came out around GBP 119,237.88. Treat this as a rough budget only.
- Actual pricing pack result from `R1 Construction - Gresty Road Pricing.xlsx` is the reliable source.

Current stable actual pricing result:

- Items: 53
- Mix: 52 windows, 1 door
- Total/subtotal ex VAT: GBP 89,898.12
- This matches the proposal subtotal: GBP 89,898.12 plus VAT.

Important behaviours:

- Generic files named `Pricing.xlsx` must be recognised, not only files literally named `Pricing Document`.
- When the pricing workbook exists, bay layouts/supplier PDFs are not also priced as scope.

## Pricing Logic Notes

The app has two different pricing modes:

1. Native estimating mode: extracted dimensions/types go through the local price engine.
2. Estimator workbook mode: exact workbook sell rates/totals are preserved with `manualOverride`.

Do not mix these blindly. If a real estimator pricing workbook is present, it normally already includes markup, preliminaries, fixings, install allowances, lifts/access, and commercial assumptions. Re-pricing those same rows through the native engine will create large variance.

Commercial allowance rows should be displayed as allowance lines, not as missing-dimension/TBC rows.

### Fenster Pricing Codes And Labour Allowances

Adam's Project Hail Mary pricing-code email defines the current labour allowances that the bot must use when preparing/checking pricing documents:

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

The code must be selected from product type and size/category. Do not guess where the item is unclear; flag it for human review. Quantity is separate from the code. Curtain walling stays separate unless a future curtain-wall code is created. Combined items such as doors with side screens/fanlights need special review and should use the combined codes where appropriate.

In `js/pricing.js`, these are available as `Pricing.LABOUR_ALLOWANCES` and `Pricing.getLabourAllowanceForCode(code)`. The summary install calculation can use them when `pricing.useProductCodeLabourAllowances` is true. This flag is off by default so older calibrated quotes do not move unexpectedly.

## OpenAI Enrichment

OpenAI note review is optional and must fail open.

- The API key should not be hardcoded in source going forward.
- The user previously supplied a key and hit quota/429 during testing.
- Do not spend OpenAI tokens unless the user explicitly asks.
- Current AI output from a prior successful Whitsbury run is saved in `test-results\whitsbury-ai-output\openai-red-fields.json`.
- AI enrichment should only suggest/confirm fields; deterministic extraction and pricing must still work without it.

The intended AI role:

- Read notes/spec text.
- Confirm or correct parser fields such as frame, glass, colour, hardware, handle, lock, closer, ironmongery, entrance door reference, and fire/acoustic requirements.
- Prefill tender questions.
- Mark unresolved fields with a red review state.

## Quote PDF Notes

The quote generator supports detailed and compact PDFs.

Important recent layout fixes:

- Schedule starts below the cover intro instead of overlapping it.
- Long summary labels are truncated safely.
- Notes move to a new page when needed.
- Commercial allowance dimensions show as `Allowance`.

Regression visual checks used `pdfplumber` word-box overlap detection. Poppler was not available in the environment during prior checks, so the overlap detector was the practical verification method.

## Local Test Commands

From the repo root:

```powershell
node -e "const fs=require('fs'); for (const f of ['js/dataExtractor.js','js/pricing.js','js/quoteGenerator.js','js/app.js']) new Function(fs.readFileSync(f,'utf8')); console.log('syntax ok')"
```

Run a tender pack through the CLI harness:

```powershell
node scripts\run-tender-pack.mjs --dir "C:\path\to\input-pack" --out "test-results\some-output-folder"
```

Useful prior output folders:

- `test-results\whitsbury-regression-output-7`
- `test-results\brandon-estate-actual-rev2-final-check`
- `test-results\gresty-road-actual-final-check`
- `test-results\gresty-road-actual-output-fixed-2`

Generated Gresty quote PDFs:

- `test-results\gresty-road-actual-output-fixed-2\Gresty-Road-Actual-Quote-Detailed.pdf`
- `test-results\gresty-road-actual-output-fixed-2\Gresty-Road-Actual-Quote-Compact.pdf`

## Development Rules For Future Agents

- Read `HANDOVER.md` before editing.
- Keep the browser app and CLI harness using the same extraction/pricing logic.
- Do not add one-off script logic that disagrees with the website.
- When a bug is found in a tender-pack run, fix shared modules first, then re-run the CLI harness.
- Push meaningful changes; the user expects GitHub Pages to receive updates from `main`.
- Update the version badge when user-facing behaviour changes.
- Avoid spending OpenAI quota during debugging unless requested.
- Treat actual estimator workbooks as stronger evidence than PDFs/drawings.
- Treat image-only drawings as needing OCR/takeoff before accurate quoting.
- Preserve unrelated user changes. Do not reset the repo.

## Best Next Technical Work

1. Add a real automated regression suite around the saved packs so Whitsbury, Brandon, and Gresty stay stable.
2. Build proper OCR/takeoff for scanned/image-heavy drawings instead of relying on text extraction.
3. Add supplier quote ingestion for RAS, glass order, bay layout, and supplier quotation PDFs as evidence/benchmark data.
4. Make commercial extras/prelims a structured model rather than loose allowance rows.
5. Finish ZIP/DOCX/MSG intake through the worker path for large packs.
6. Add an approval workflow: parsed scope, AI assumptions, estimator approval, quote generation, final issue.
7. Add cheaper OpenAI usage controls: model choice, hard token limits, cache by document hash, and visible spend warnings.

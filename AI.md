# AI Agent Guide

This repo is the Fenster Glazing Quote Assistant. Its real job is not just parsing documents; it is trying to behave like a junior commercial glazing estimator who can read a tender pack, build a sensible scope, price it using Fenster rules, explain uncertainty, and generate a quote for human approval.

Read `HANDOVER.md` first for the current priority. This file is the deeper operating manual.

## Current Snapshot

- Working repo path: `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant`.
- Do not continue working in the old OneDrive repo unless the user explicitly asks.
- Live app type: static HTML/CSS/JS, intended for GitHub Pages or Cloudflare Pages.
- Current visible app version: `v2026.06.30.1`.
- Current confirmed pushed commit before this doc refresh: `2f39bdf Add tender finder research panel`.
- There are currently no GitHub Actions workflows in this repo.
- The user expects meaningful changes to be committed and pushed when work is complete.

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
- Do not add one-off script logic that disagrees with the website.
- When a bug is found in a tender-pack run, fix shared modules first, then re-run the CLI harness.
- Push meaningful changes; the user expects the hosted app to update from the repo.
- Update the version badge when user-facing behaviour changes.
- Avoid spending OpenAI quota during debugging unless requested.
- Treat actual estimator workbooks as stronger evidence than PDFs/drawings.
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

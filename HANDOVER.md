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

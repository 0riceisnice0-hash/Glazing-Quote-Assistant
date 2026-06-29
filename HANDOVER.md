# Handover

This is the quick-start note for the next AI agent working on the Fenster Glazing Quote Assistant.

## Where To Start

Repo:

```text
C:\Users\zacpl\OneDrive\Documents\GitHub\Glazing-Quote-Assistant
```

Read these first:

1. `HANDOVER.md`
2. `AI.md`
3. `js/dataExtractor.js`
4. `js/pricing.js`
5. `scripts/run-tender-pack.mjs`

Current app version shown in the UI:

```text
v2026.06.25.5
```

Last important pushed code commit before this handover:

```text
3d4d838 Recognize generic pricing workbooks
```

There are no GitHub Actions workflows at the time of writing. Deployment is effectively by pushing `main` for GitHub Pages/static hosting.

## What Was Recently Fixed

- Whitsbury/Hartford pack now quotes from the external opening schedule workbook instead of duplicate/reference PDFs.
- Brandon Estate REV 2 now quotes from the actual Fenster pricing workbook, preserving estimator sell rates, markups, preliminaries, and commercial allowance rows.
- Gresty Road actual pricing pack now recognises generic `Pricing.xlsx` workbooks and matches the proposal subtotal.
- Quote PDFs had overlap issues; detailed/compact layouts have been tightened and checked.
- OpenAI enrichment was wired for note review, but the user's key hit quota. Do not spend more API credits without being asked.
- Project Hail Mary pricing-code labour allowances were added to `js/pricing.js` as an opt-in mode via `useProductCodeLabourAllowances`.

## Known Good Results

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

## Commands To Run

Syntax smoke check:

```powershell
node -e "const fs=require('fs'); for (const f of ['js/dataExtractor.js','js/pricing.js','js/quoteGenerator.js','js/app.js']) new Function(fs.readFileSync(f,'utf8')); console.log('syntax ok')"
```

Run a tender pack:

```powershell
node scripts\run-tender-pack.mjs --dir "C:\path\to\input-pack" --out "test-results\new-output-folder"
```

Check git before and after work:

```powershell
git status --short
git log -1 --oneline
```

Use `npm.cmd` instead of `npm` if PowerShell blocks `npm.ps1`.

## Important Output Folders

- `test-results\whitsbury-regression-output-7`
- `test-results\brandon-estate-actual-rev2-final-check`
- `test-results\gresty-road-actual-final-check`
- `test-results\gresty-road-actual-output-fixed-2`

Gresty generated PDFs:

- `test-results\gresty-road-actual-output-fixed-2\Gresty-Road-Actual-Quote-Detailed.pdf`
- `test-results\gresty-road-actual-output-fixed-2\Gresty-Road-Actual-Quote-Compact.pdf`

Prior OpenAI output:

- `test-results\whitsbury-ai-output\openai-red-fields.json`

## Traps

- Do not use unrelated OneDrive folders. The user only approved this repo.
- Do not keep using the OpenAI key during debugging; quota was already hit.
- Do not replace older quote behaviour with Project Hail Mary labour-code behaviour globally. Use `pricing.useProductCodeLabourAllowances = true` only for pricing-document/coding-check flows that need Adam's labour table.
- Do not price every PDF that mentions windows or doors.
- Do not double count pricing workbooks plus supplier PDFs/layout PDFs.
- Do not treat opening type sheets as priced scope.
- Do not treat image-only elevation drawings as reliable without OCR/takeoff.
- Do not manually create script-only quote logic that differs from the website.
- Do not forget to bump the visible version when user-facing behaviour changes.
- Push meaningful changes. The user has already called out local-only changes not appearing online.

## If The User Gives More Tender Files

1. Copy/point the files into a test input folder, preferably under `test-results`.
2. Run `scripts\run-tender-pack.mjs`.
3. Inspect the extraction JSON/CSV, not only the total.
4. If the result is wrong, fix shared parser/pricing modules.
5. Re-run existing Whitsbury, Brandon, and Gresty checks if the change touches shared classification or pricing.
6. Generate detailed and compact PDFs if the user asks for quote output.
7. Commit and push.

## Next Best Work

- Build a proper regression test suite for saved packs.
- Add OCR and drawing takeoff for scanned/image-heavy PDFs.
- Add supplier quote ingestion for RAS, glass order, bay layout, and supplier quotation PDFs.
- Convert commercial preliminaries/extras into structured line types.
- Finish worker-backed ZIP/DOCX/MSG processing for large packs.
- Add approval workflow: extracted scope, AI assumptions, estimator review, quote issue.
- Add OpenAI spend controls: cache by document hash, smaller model option, hard token cap, and clear UI warnings.

# MARY - COMPLETE OPERATING HANDOVER

Last updated: 2026-07-17 (later session: Adam confirmed template pricing maths is correct, and mandated the Ops Manual Proposal Document Process 2.3.2-PRC2 - proposals are now Word-first clones of the MASTER COVER LETTER; reply drafted in `outputs\Proposal Process - Reply to Adam (draft).txt`).

**A new session continues EXACTLY from here. Read this file first, then `HANDOVER.md` and `AI.md`. Everything below is standing instruction from Zac unless he changes it in chat.**

---

## 1. WHO I AM AND HOW TO RESPOND

- I am **Mary**, Fenster Glazing's estimating AI (the Glazing Quote Assistant / "Project Hail Mary").
- **Emails to Adam are signed "Mary / Fenster Glazing - Estimating". Never pretend to be human. Never sign as Zac.** Adam Butcher (Commercial Director) knows all about Mary and addresses her directly.
- **I never send emails myself.** I write reply drafts to `outputs\<Job> - Reply to Adam (draft).txt` and paste the text in chat when Zac asks. Zac sends them.
- Zac (the operator, GitHub `0riceisnice0-hash`, fensterglazing@gmail.com) is a coder/marketer with **no commercial estimating knowledge** - explain commercial concepts plainly in chat, lead with the headline number, keep him honest about what is firm vs budget.
- Chat replies to Zac: lead with the outcome (price, deadline, risk), then how it was built. Flag anything urgent (deadlines, scope gaps) at the top.

## 2. WHERE EVERYTHING LIVES

- **Bot repo (the only one):** `C:\Users\zacpl\Desktop\Glazing-Quote-Assistant` -> GitHub `0riceisnice0-hash/Glazing-Quote-Assistant`. Do NOT use `Documents\GitHub\Glazing-Quote-Assistant` or the old OneDrive repo.
- **Live app:** https://glazing-quote-assistant.pages.dev - version badge `v2026.07.17.1` (in `js/app.js` + `index.html`; cache-bust query strings on script tags).
- **Job/supplier archive (READ-ONLY):** `C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents\<client>\<job>` (+ `2. Projects`). Vetroseal quotes = `FENSTERG_Quote_NNNNNN`, Strongdor = `SQnnnnnn`, BSW = `QTnnnnnn`, Aplus = `QT/QP` + Crystal/Logikal exports.
- **Rate register:** `data/supplier-rates.json` - 15,551 mined quote lines, 79 size-banded categories, Sept 2023 - Jul 2026. Rebuild: `python scripts/build-rate-register.py <mined-quotes.json>`. Miner: `python scripts/mine-supplier-rates.py --clients * --roots <both trees> --out <dir>`.
- **House document generator:** `python scripts/generate-fenster-docs.py job.json` + `templates/` (MASTER PRICING DOC.xlsx clone-and-fill; proposal HTML replica; job JSON schema = the Lyttleton demo, see git history of `scratchpad` or rebuild from the function signature).
- **CLI parser:** `node scripts\run-tender-pack.mjs --dir "test-results\<job>-input" --out "test-results\<job>-run" --with-supplier`.
- Working folders per job: `test-results\<job>-input` / `<job>-run`. Final deliverables: `outputs\`.

## 3. WHAT ZAC HAS PERMITTED (standing)

- Read-only scanning of the entire OneDrive Commercial archive. **Never delete or modify anything in OneDrive.**
- Fixing/extending the bot's SHARED modules, bumping the version badge, committing, pushing to GitHub, and deploying Cloudflare Pages (`powershell -ExecutionPolicy Bypass -File scripts\build-pages.ps1` then `npx.cmd wrangler pages deploy dist-pages --project-name glazing-quote-assistant --branch main`).
- Producing complete quotes autonomously when Adam emails a job, including archive mining for rates and past quotes.
- The full-archive rate sweep was explicitly approved ("do the full sweep").
- Signing as Mary (explicit instruction 2026-07-17).

## 4. WHAT NOT TO DO

- Never invent rates, quantities or totals. Unknown = TBC + RFI. Benchmark rates must cite register provenance (category, median, n, date range) and be labelled budget/benchmark vs SUPPLIER BACKED.
- Never use gross supplier figures where an end discount exists - **use Grand Total Net** (Bellview/BSW quotes carry 15% end discounts; apply the discount factor to every line).
- Never double-count (supplier quotes + layouts + schedules; Filwood's bill explicitly forbids pricing shopfronts twice - they are Contractor's Provisional Sums under Work Section A54).
- Never use images from the MASTER COVER LETTER media in proposals - image4.png is the ELKINS client logo. Only `templates/proposal-images/fenster-logo.png`.
- Don't spend OpenAI tokens (legacy quota rule). Don't restore behaviours listed in AI.md "Traps".
- Don't present drawing dimensions as final - "final measurements by manufacturer" / technical survey.

## 5. HOW TO QUOTE (the workflow, per Adam email)

1. **Locate inputs**: attachment in `C:\Users\zacpl\Downloads\` or the OneDrive job folder Adam names. **ALWAYS search the job folder + client folder for existing supplier quotes FIRST** - Crownhill's live BSW quote (QT252840) and Strongdor SQ216661 were sitting in the folder unannounced.
2. Extract to `test-results\<job>-input`, run the CLI parser, inspect JSON/CSV.
3. **Verify extraction manually** against the source. CAD/PDF text layers are unreliable - read drawings visually; tile A1 sheets with `pdftoppm -r 150 -x -y -W -H` (GDI crop runs out of memory). Every quoted number must be traceable.
4. **Parser gaps -> fix SHARED modules** (`js/dataExtractor.js`, `js/pricing.js`), `node -e` syntax check, re-run regressions:
   - Brocks Hill: 9 items, subtotal GBP99,205.48
   - Alkerden: 17 items, subtotal GBP382,011.42
   - Ninn Lane amended: 76 items, GBP0 (scope-only)
   Then bump version + cache-busts, commit, push, deploy.
5. **Pricing hierarchy**: live supplier quote for THIS job > historical supplier quote for same client/spec > register benchmark medians (size-banded) with documented uplifts > engine fallback rates. Add Fenster code markup + code labour.
6. **Outputs per job (three sets)**:
   - House pricing doc: `outputs\<Job> - Fenster Pricing Document (house format).xlsx` via generate-fenster-docs.py (clones Adam's template; template formulas do the selling).
   - House proposal (NEW PROCESS, Adam email 2026-07-17): follow **Ops Manual Doc 2.3.2-PRC2 "Proposal Document Process"** (`OneDrive\Operations Manual\2. Business Operations & Project Workflow\2.3 Estimating & Commercial Process\2.3.2 Quotation preparation\`). Build as a WORD DOC first - clone `Commercial\1. Tender Documents\1. Master\1. Estimating\3. Client Quote\MASTER COVER LETTER 31.05.2026.docx` - then print to PDF named `[Client Name] - [Project Ref] Proposal` (e.g. "Borras - Stoke Park Proposal"). Word 16 is installed (COM `Word.Application.16`) for faithful docx->PDF. Fill: cover (project images of the ACTUAL building from the web, else glazing stock; client logo from `Commercial\19. Company Logo Files` - process doc says "20" but it's 19; names in CAPITALS; check text box stays in blue header), page 2 project info, Executive Summary (process mandates the ChatGPT "Executive Summary Bot" - Mary has no access; offered Adam: write it to same length/structure, or Zac runs the bot - awaiting his pick), Description & Clarifications, Products (systems/glass U-G-LT/ancillaries). Pages 5+ (Approach, Previous Projects, Team, T&Cs) NEVER change. Review-only Inclusions & Exclusions. This supersedes the HTML-replica proposal and the placeholder-photos rule.
   - Internal review: `<Job> - Fenster Pricing Document and Review.xlsx` + `<Job> - Fenster Glazing Proposal and Pricing Review.pdf` (Alkerden-format: supplier/fallback cost, code, markup, labour, sell, review table, assumptions/exclusions/RFIs, source notes).
   - Reply draft signed Mary.
   - If Adam asks for a **take-off document**: 3-sheet format from Greenfields (Project Information / per-ref Window & Door Schedule / RFIs & Queries) - covers security ratings, glass specs, colours, materials, quantities, deadlines, EPDM, standards, warranties, site constraints.
7. PDFs: write HTML (house style: A4 landscape for reviews, portrait for proposals; dark #1f2a44 headers) -> print with `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --no-pdf-header-footer --print-to-pdf=...` -> render check with `C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe` (Start-Sleep 2 first - write race) -> Read the PNG and eyeball for clipping.
8. Deliver files to Zac in chat (SendUserFile), commit outputs + a job record in `HANDOVER.md`, push.

## 6. PRICING FACTS

- **Fenster labour codes (Adam's table, also in template INSTALLATION formula):** SUPD/SAD 250, DUPD/DAD 500, ELAW 250, LAW/MAW/SAW 160, L/M/SPVC 160, SADLAW/SADMAW/SADSAW 410. Screens ~400 (judgement). CW labour 150/m2.
- **Internal engine markups (`Pricing.PRODUCT_CODES`):** SAW 400, MAW 500, LAW 600, ELAW 1000, SAD 1150, DAD 1950, SUPD 950, DUPD 1500, SADSAW 1650, SADMAW 1850, SADLAW 1950, SSD 1300, DSD 2200; CW 850 supply/m2.
- **House template adders (MASTER PRICING DOC unit-rate formula): code value x 75%** = SAW 337.50, MAW 412.50, LAW 487.50, ELAW 637.50, SAD 900, DAD 1500, SADSAW 1275, SADMAW 1425, SADLAW 1500, SPVC 262.50, MPVC 300, LPVC 337.50, SUPD 750, DUPD 1125.
- **RESOLVED (Adam email 2026-07-17):** template adders vs engine markups - Adam ruled the TEMPLATE MATHS IS CORRECT ("The excel formulas all speak for themselves... This is the correct price"). The house pricing doc (template x75% adders) is THE price; my job is putting supplier prices in the correct cells and letting the formulas sell. Internal reviews may still show engine figures for comparison but the template number is what goes to clients. Adam will send a "pricing document process doc" for review when complete.
- **Register headline medians:** BSW alu T&T glazed ~GBP580/m2 small -> ~GBP396/m2 at 3-6m2; alu casement glazed+SKN ~GBP625/m2; uPVC casement glazed GBP163-214/m2 by band; Vetroseal SKN 176 Coolite toughened GBP103/m2, lami/tough softcoat GBP87/m2; Strongdor Steeldor single GBP1,297 / double GBP2,603, Firedor GBP1,836/GBP3,446; Aplus alu doors GBP468-621/m2 unglazed. Medians are size-banded but still medians - big frames cheaper per m2; supplier quotes valid ~30 days.
- Standard rates: mastic GBP5/lm, EPDM GBP25/m2, install default GBP140/unit (engine) vs code labour for pricing-doc flows, VAT 20%.
- The Coolite spec "used on all previous pricing" = Saint-Gobain COOL-LITE SKN 176(ii).

## 7. LIVE JOB STATE (as of 2026-07-17 evening)

| Job | Status | Waiting on |
|---|---|---|
| **Lyttleton Road (Harrabin)** | Both options delivered: alu GBP43,450.89 (BSW 0000000445 net) / uPVC windows GBP31,902.00. House-format docs also produced (GBP41,138.41 template maths - Adam confirmed 17/07 the template price is correct). | Adam: confirm BSW quote titled "priory pools community center" is this job; BL-vs-anthracite colour query; uPVC re-quote from BSW? BSW price hold expires ~05/08. Offered to rebuild proposal to new Word-first process. |
| **Filwood Broadway (Stepnell)** | GBP84,810.59 ex VAT as Contractor's Provisional Sums delivered. | Zac/Adam to email Adam Warner (adam.warner@stepnell.co.uk) by **20 JULY**. |
| **Greenfields Barnstaple (Pearce)** | HOUSE pricing doc built 17/07 on Adam's instruction (RFI never sent, deadline passed, "get it out today"): **GBP136,438.80 ex VAT** via template maths (benchmark supply GBP85,361.30 in Frames cells + code adders GBP35,887.50 + code labour GBP15,190). Differs from the internal GBP100,981.30 which had NO Fenster margin. Tender email to Neil Macilwaine drafted with WG-15-29/WF-10/11/DG-13 as explicit EXCLUSIONS. | Zac: send `outputs\Greenfields Respite Barnstaple - Tender Email to Pearce (draft).txt` + house xlsx TODAY; BS7412/13 certs still needed with tender (Adam never pulled them). |
| **Crownhill (Zelltec)** | Rev 2 supplier-based GBP73,770.86 delivered. **Rev 3 pending**: BSW QT252840 (15/07, glazed incl Coolite, GBP33,839.57) found in folder - ~GBP11.8k under Rev 2 aluminium. | Adam: trickle vents missing from BSW quote; entrance quoted Prestige not Smart Wall. Strongdor SQ216661 valid to 13/08. |
| **Brocks Hill** | GBP111,208.82 budget quote delivered. | Adam: 6 RFIs (system/colour, ED.0.10/14 config, E/O meanings, power-assist supplier, glass upgrades, prelims). |
| **Beaumont Court (Fortis Vision)** | Old-vs-new tender doc comparison delivered 17/07: 5no NW3 windows DELETED (schedule 9->4), ED1/ED2 shrunk to 2342/2110 x 1252, new handle-height limits (NW1 1900 / NW2 1700), possible new Block A louvre package (SK-HGCE-50-ZZ-DR-M-003). Pack defects: real 0311 T02 MISSING (file contains HCD screed dwg S-28-007) + 11 "PDFs" are renamed DWGs (incl 0302, 0228, 0226, 0253). | Adam: RFI Fortis for real 0311 T02 + proper PDFs; confirm louvre scope; instruct re-price if wanted. Working folders test-results\beaumont-old-input / beaumont-new-input / beaumont-compare. |

## 8. SUGGESTED NEXT CAPABILITIES (pitched, not started)

1. Wire `data/supplier-rates.json` into `js/pricing.js` as a `benchmark` pricing method with provenance strings.
2. Email-instruction parsing (Adam's specs auto-applied instead of by hand).
3. Size-banded rates in the engine; Aplus letter/Crystal totals cross-check; incremental re-mines (only new files).

## 9. TOOLING QUIRKS (save yourself the debugging)

- Two PDF text engines disagree: pypdf vs pdfplumber give different token orders of the SAME file; miner keeps both and retries. "GBP" can arrive as U+FFFD; labels can follow their amounts; Vetroseal wraps rows and bills 0.30m2 minimum areas; page headers leak digits ("97-98 ALSTON DRIVE").
- Old .xls files: xlrd chokes - use the repo's sheetjs via `node -e "require('./node_modules/xlsx/xlsx.js')..."`.
- PowerShell 5.1: no `&&`; here-strings break in this harness -> write commit messages to a scratch file and `git commit -F`. Native stderr wraps as fake errors (git push "error" that ends `main -> main` succeeded).
- No LibreOffice: recalc.py fails (AF_UNIX). Verify workbook formulas by hand-computing; Excel recalcs on open. Keep formulas simple (SUM/SUMIF/ROUND).
- Chrome headless writes PDFs asynchronously - Start-Sleep 2 before pdftoppm.
- The MASTER PRICING DOC sheet name is `'Pricing Document '` with a trailing space; its TOTAL cell ships stale/hardcoded - always rewrite to a live formula.
- Scratchpad for temp files; job folders under test-results; never commit node_modules or client PDFs beyond outputs.

## 10. DOCUMENTATION DUTY

After every job/change: job record in `HANDOVER.md` (inputs, outputs, commercial position, lessons), durable rules in `AI.md`, this file when operating rules change. Commit + push everything meaningful. That is how the next session IS this session.

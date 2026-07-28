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

## Auditing A Quote The Team Has Already Sent (learned 27/07/2026)

A Fenster quote is TWO documents that leave in the same email - a pricing xlsx and a proposal PDF - plus, often, a
drawings pack. **They can contradict each other, and on 27/07 both quotes issued that day did.** Recomputing the
arithmetic is the easy half; the money is in reading the documents against each other and against the tender.

Always run these four cross-checks:

1. **Pricing lines vs proposal clarifications.** Anything moved into or out of the price must be reflected in the
   clarifications. Princess Beatrice went to the client charging GBP5,356.22 for mastic while the proposal still read
   "External mastic is charged as an optional extra", and EPDM (GBP8,276.91) was not mentioned at all - GBP13,633.13
   charged in one document and disclaimed in the other. When Adam instructs a pricing change, the clarifications are
   part of that instruction even when he does not spell it out (he did spell it out here: "We will need to adjust the
   clarifications on the proposal to reflect the above").
2. **Proposal product statements vs pricing headings.** Princess Beatrice's proposal said "based on Technal STII
   thermally broken commercial doors" while the pricing headed Door Types 1-5 "Modeal Complex Coupled Doors".
3. **Our exclusions vs the tender's "Include..." clauses.** This is the highest-value check. Crestwood's proposal
   excluded "Teleflex controls / wiring" against a drawing that says "Include for all installation, core wire, conduit
   and fittings as required" - while charging GBP17,779.06, 24% of the tender, for Teleflex. Read every "Include for"
   and "to be removed and disposed of" on the tender drawings and grep the exclusions column for each one. Crestwood
   also excludes waste removal against a drawing requiring the existing windows to be disposed of.
4. **What is in the attached drawings pack.** It goes to the client. Check it for (a) leaked supplier prices - the
   Princess Beatrice pack was an Aplus Logikal "OFFER" export with Qty/Unit Price/Total column headers, though the
   price cells were empty; and (b) disclaimers that contradict the proposal - five pages carried "ITEMS GLAZED WITH
   PANELS HAVE NOT BEEN TESTED TO PAS24" while the proposal claimed PAS24 against a Part Q / SBD Silver ITT.

Verification that IS worth doing on the numbers, because it is fast and conclusive: sum the supplier quote's net total,
subtract it from the sum of the client-facing item lines, and check the remainder decomposes into whole code adders
(SAW 337.50, MAW 412.50, LAW 487.50, ELAW 637.50, SAD 900, DAD 1500 - code value x 75%). Crestwood: BSW QT252906 net
GBP27,329.60 + GBP20,550.00 of adders = GBP47,879.60 exactly, which proves in one line that every supplier line was
carried, nothing was dropped and nothing double-counted.

Also check: a main contractor's discount taken as a straight deduction comes off margin. To be neutral the subtotal has
to be grossed up by /0.975 first, not have 2.5% added and then removed (1.025 x 0.975 = 0.999375). Report it as a
visible give-away, not as an error, if the Commercial Director has approved the method.

## The Labour Code Silently Under-Prices Anything Measured In m2 (learned 27/07/2026, Filwood)

The MASTER PRICING DOC `INSTALLATION` formula is a SUMPRODUCT over the product code in column B, not over
size: SUPD/SAD 250, DUPD/**DAD 500**, ELAW 250, LAW/MAW/SAW 160, PVC 160, SADxAW 410, and only `CW` routes
to `sqm x 150`. So a code meant for a single doorset pays the same install on a 2 m2 door and a 20 m2
shopfront screen.

Filwood: seven glazed shopfront screens, 122.98 m2, up to 4,930 x 3,570, every row coded DAD. Install came
out at **GBP 3,500 - GBP 28.46/m2** for elements 3.5 m tall. House CW labour at GBP 150/m2 is
**GBP 18,446.32**. GBP 14,946 of install missing from a GBP 67k tender, and the same mis-code also put a
GBP 1,500 "double door" adder on each row against a supplier-quoted SINGLE door.

The check, on any job with elements bigger than a domestic window:

1. Divide the install line by the total m2. If it is not roughly GBP 150/m2 on screens/CW, ask why.
2. Anything measured in m2 rather than units should be coded `CW`, or carry a stated judgement figure that
   the Commercial Director has signed off. MARY-HANDOVER s6 puts screens at ~GBP 400/unit as judgement, and
   that is still low for a 17 m2 frame.
3. Cross-read the proposal exclusions. Filwood excluded "Access/Lifting Equipment - Scaffold, MEWPS, Towers,
   Forklift" while including installation of 3,570 mm elements, so the access plant was missing too. A tiny
   install figure and an access-equipment exclusion travel together.
4. Check the product code against the SUPPLIER's description, not the drawing. DAD (double) on a row where
   the quote says "a Single Pivoted ... Door" is either deliberate discretionary money (allowed - Adam,
   24/07) or a mis-code. Either way it must be a decision, not an accident.

A useful confirmation when one exists: an independent benchmark. Filwood's corrected total of GBP 82,013.90
landed within GBP 2,797 of the GBP 84,810.59 built ten days earlier from register medians with no supplier
quote at all. Two independent routes converging is the strongest evidence available that the correction, not
the original, is right.

## Audit The RFQ, Not Just The Quote (learned 27/07/2026, Filwood)

A supplier quote can reconcile to the penny and still be the wrong product. Bellview/BSW 0000000507 was
arithmetically perfect - seven positions, 15% end discount applied, field counts matching the architect's
elevation - and was missing the certified security doorset, the solar coating, the specified finish, the
specified system and the ventilation mesh.

**The correspondence that produced the quote lives in `test-results\mary-inbox\processed\` and is part of
the audit.** On Filwood, finding it changed the weight of four findings:

- **The RFQ was right.** Gintare had asked for mill-finish spandrels, RAL 7035 to the doors only, U 1.0,
  g 0.5-0.6, Rw 32 dB, LPS 1175 SR2, level thresholds and M4(2). The quote answered on none of the last four.
  So the failure was not the enquiry - it was that the tender was then built on the quote instead of on the
  instruction. Check the quote against the RFQ before blaming either.
- **Silence to a direct written request is not compliance.** SR2 was asked for and simply not mentioned.
  That is stronger evidence than "not priced", and it belongs in the finding.
- **Read the covering email for caveats that never reach the tender.** BSW wrote "we have met the u- and g-
  and acoustic value **for glazing only**, as these area commercial thermally broken shopfront products they
  are **non rebated**". The drawing schedule's targets were ELEMENT targets, so the supplier had put a
  non-compliance in writing - and the proposal rendered it as the softer "Ug values noted between 1.0-1.1
  W/m2K where quoted". The one caveat the supplier documented was the one the tender left out.
- **A performance claim with no number is not evidence.** BSW claimed g 0.5-0.6 while their own make-up
  ("6.8 Lami / 4mm Tuff") names no coating and states no g-value; clear sits near 0.7. Never pass a supplier
  claim to a client until the coating and the figure are in writing.

Also worth checking on any filed quote: whether it has a terms page at all. 0000000507 was six pages of
elements and totals with no validity period, no lead time and no payment terms - against a main contract
start eight weeks out and LADs of GBP 1,358 per calendar week.

## Never Overstate A Rate's Provenance (learned 27/07/2026)

Before describing a rate as "quoted", open the source and check who wrote the number. Mary told Adam "CN Glass quoted
the same make-up at GBP60/m2"; the source `.eml` turned out to be Steve Freezer's own outgoing email with the rates
already typed into it, to which CN Glass replied only "Pls see below as discussed". That is **a verbal confirmed by
return email, not a priced quotation** - there was no CN Glass quotation document on file at all. Adam asked "Where did
you get the CN Glass info from?" and the honest answer had to include the correction.

The register hierarchy already distinguishes SUPPLIER BACKED from benchmark. Add a third rung below it: a rate the
supplier has acknowledged but never itself priced. Say which rung applies every time.

## Fire Ratings Live In NBS Clause L20 (learned 27/07/2026)

Before pricing any door package, read the NBS specification's **L20 Doors/shutters/hatches** section, not just the door
schedule drawing. At Vesuvius Way, L20 required "60 Min Insulated steel-core external open-out single-leaf door", a
separate "60 Min Door installed in curtain wall to manufacturers design", and a 60-min louvred door - none of which was
visible on the elevations Mary priced from. L20/70 also sets the test standard (BS EN 1634-1 / 1634-3) and requires a
Fire Door Schedule to Building Control before order.

Two consequences that change the price by more than the door line:

- A 60-minute door **cannot** be installed in a standard curtain wall (SF52 and equivalents). Any screen containing a
  door becomes a tested fire-rated screen. At Vesuvius that put 45% of the budget - GBP49,377.50 of curtain wall - into
  question, against a door line of only GBP4,683.56.
- "Insulated steel-core, PPC galvanised double-skinned leaf" is not an aluminium fabricator's product. It is a
  Strongdor / Aluminium Fire Systems item, so aluminium door medians do not apply at all.

**Aluminium Fire Systems** - Julian Ward, julian@aluminiumfiresystems.com, 0121 277 4870 - already quote Fenster
(Manor Lodge Q7666). They are the first call for fire-rated doors and screens. Note their 27/07 constraint: a push bar
needs a **920mm minimum door width**; it will not fit a 900mm leaf.

## AOV / Smoke Vent Free Area (learned 27/07/2026)

Never infer free area from the frame size. Aplus state **"Geometric free area = X m2"** directly on the quote, with the
reveal assumption beneath it, and will also state the size that would achieve the target. QT51518: 1130 x 1530 gave
1.30 m2 against a 1.5 m2 requirement, and Aplus volunteered that 1235 x 1583 achieves 1.5 m2 using 900mm chains instead
of 850mm. Read page 2 and the AOV notes page before answering any free-area question.

Standing AOV caveats to carry into any Fenster quote built on an Aplus smoke vent: cables are not run through the
mullions (about 2m of flex is left coiled at the vent); **the actuators are not restrictors** and Aplus disclaim
liability for damage if a separate restrictor is not fitted 50mm beyond the stroke; vents below 2.5m from FFL raise a
trap-hazard risk under BS EN 60335-2; below 1100mm from FFL they need Part K anti-fall protection, which Aplus exclude.

## The Kick Prompt Must Not Go On The Command Line (learned 27/07/2026, triage)

Windows caps a whole command line at **32,767 characters**. `mary_bridge.py` passed the entire kick prompt as an argv
element, and the shared noticeboard alone reached **30,259 characters** on 27/07 - so every attempt to start a **NEW**
job chat began failing with `[WinError 206] The filename or extension is too long`. Resuming an existing chat was
unaffected, which is why it looked intermittent.

It ate three of Adam's dashboard messages (18:21, 18:35, 18:52 - one of them his answer to REQ-6). Each was retried
three times and parked in `failed\`, and the log line reads `SESSION LAUNCH FAILED`, which looks like a CLI or
usage-limit problem rather than a prompt-length one. **When a work order is parked after three attempts, read the actual
log message** - the cause was named precisely and sat unread for two and a half hours.

Fixed: the prompt now goes down **stdin** (`claude -p` with no positional prompt), which has no length limit. Verified
end to end at 30,328 characters - the exact size that was failing - returncode 0.

**Interim, because that fix is inert until the bridge restarts, and by 20:36 resumes were failing too:** the board now
trims itself by SIZE. `trim_board()` in `mary_note.py` already existed and was already called on every post, but capped
by ENTRY COUNT (60) - with entries running 3-7k each that permits a 200,000-character board, so it had never fired in
its life. It now holds the live board to `MAX_BOARD_CHARS` (9,000) and **appends** the overflow to
`data/mary-noticeboard-archive.md`; nothing is discarded. This works on the already-running bridge because `post_board`
executes as a fresh process every time a chat posts - unlike the bridge, it is not holding a stale module.

Related correction worth remembering: `--read` used to print only the live board, so once trimming was automatic a chat
looking up an earlier finding would see almost nothing and reasonably conclude it had never been posted. `read_board()`
now takes `include_archive` and `--read` uses it. **Keep the default board-only** - the bridge calls `read_board(limit=12)`
to build a kick prompt and must never be handed the whole archive.

The ceiling is board + handoffs + job brief, not the board alone. After trimming, the worst-case chat prompt measured
about 16,700 characters against the 32,767 cap. Raise `MAX_BOARD_CHARS` once the bridge is running the stdin fix - and
do not ask the chats to write shorter notes instead. Six chats each self-censoring costs more than a short live board,
which is recoverable with `--read`.

**Third instance in one day of the same meta-rule**, after the two registry faults: a long-running process keeps the
module it imported at startup, so a fix on disk changes what the NEXT process does, not the running one. Any plumbing
fix is inert until the bridge restarts - say so explicitly, and raise a request rather than restarting it from inside a
session.

## Mastic And EPDM Are Optional Extras - But Check Where They Sit (Adam, 27/07/2026)

Adam's ruling: mastic and EPDM are **optional extras**, shown as options on the pricing document **below** the total, so
the client's number excludes them - "sometimes we will remove the edpm and mastic costs or include them if they are
specified". Crestwood Park is built that way.

**Princess Beatrice is not**, on Adam's own instruction of the same morning: external mastic GBP 5,356.22 and EPDM
GBP 8,276.91 sit ABOVE the subtotal (GBP 286,404.81), which less the 2.5% MCD gives the issued GBP 279,244.69. Had they
been optional the quote would have been GBP 265,952.39 - so GBP 13,292.30 is charged inside the client's number while
proposal page 3 still calls external mastic an optional extra and never mentions EPDM.

So before repeating either version: look at where the two lines actually sit on the pricing document for THAT job, and
make sure the proposal clarifications agree with it. A general ruling from Adam describes the template, not necessarily
the document in front of you - verify before closing a finding on it.

## When Graph Returns 403, Find Out WHAT Is Blocked (learned 27/07/2026)

Outbound died with `403 ErrorAccessDenied ... [RAOP] : Blocked by tenant configured AppOnly
AccessPolicy settings`. That reads as "Mail.Send has been revoked" and it was not. Probe before
concluding:

| identity | token | estimating@ | mary@ |
|---|---|---|---|
| READER (Mail.Read) | OK | **OK** | **403** |
| SENDER (Mail.Send) | OK | 403 | 403 |

Both identities still acquired tokens, so credentials and admin consent were intact. The READER read
estimating@ fine but was denied on mary@ with the identical error - so the block is on the **mary@
mailbox**, for app-only access generally, not on the send permission. estimating@ was still inside the
policy, which is why inbound kept working. The fix is to put mary@ back inside the Exchange
ApplicationAccessPolicy (usually a mail-enabled security group it dropped out of); re-consenting
Mail.Send does nothing.

The SENDER's 403 on read proves nothing - it has no Mail.Read scope, so a read denial is expected. The
decisive evidence was the READER's split result across two mailboxes.

**Sends are now logged.** `mary_send.py` writes `data/mary-send-log.jsonl` on every attempt - timestamp,
chat key, recipients, subject, attachment names, ok flag, error text - and a failure prints to stderr and
re-raises. Before this the only record of a send was mary@'s own Sent Items, which sits inside the
blocked mailbox, so the outage concealed its own timeline and nobody could say when it started.

**If email is down:** say GENERATED, NOT SENT in the job file and the handover row, and put the substance
on the hub. A workbook sitting in `outputs\` must never read as delivered.

**DO NOT "FIX" A BLOCKED mary@ BY SENDING FROM estimating@.** The probe above shows estimating@ is still
inside the app policy, so this looks like an easy workaround and it is not one - it is a change of
identity, and no chat may make it. Three reasons, the third being the serious one:

1. `estimating@` is **read-only by design and by scope** - the Reader app holds Mail.Read and nothing
   else. The whole architecture is that Mary can never send from the team's own mailbox.
2. Mail from estimating@ is indistinguishable from Gintare and the rest of the team. That breaks "never
   pretend to be human" and destroys the audit boundary that makes Mary's output identifiable.
3. **The Exchange transport rule that cages Mary's recipients is scoped to mary@.** It rejects any mail
   from mary@ whose recipients are not exactly adam@/marketing@. Send from estimating@ and that
   server-side guarantee simply does not apply - a mis-addressed message could reach a client or a
   supplier, which is the one failure the ghost protocol exists to make impossible.

If anyone proposes routing Mary's outbound through estimating@, that is Adam's or Zac's decision and it
changes the ghost protocol for every chat. Raise it; do not implement it.

## Comparing A Revised Drawing Against What Was Priced (learned 27/07/2026, St Mary's)

**Read the revision date, not the date the addendum arrived.** ET&S issued "revised drawings" on 24/07; inside, the
window schedule was rev A dated **13.07.26** and the site plan rev E dated **08.07.26** - both revised *before* Fenster
quoted on 17/07. We priced a superseded drawing for nine days without knowing. Check every revision date in an addendum
against the date of our own quote, and say plainly if we were working from stale information.

**Start with the architect's own revision note in the title block.** On 2376-09 rev A it read "integral blind omitted"
and that was the entire change. The note tells you where to look; it does not excuse you from checking.

**DIFF THE DOCUMENT REGISTER HEADER, NOT JUST THE REVISION TABLE.** This is the one that cost real money on St Mary's.
The attribute-by-attribute drawing comparison was correct and complete - and the change that mattered was not in any
drawing. ET&S's re-issued register header read `Package return date: 27 July 2026` where the three earlier registers
said 17 July. **A re-issue can move a deadline without touching a single drawing, and it is the only change that cannot
be recovered later.** So on every addendum, compare the header fields too: package return date, package lead, package
name. Four registers sat extracted on our own disk and nobody read the top of the page.

**AND CHECK WHAT YOUR RECORDED DEADLINE ACTUALLY IS.** St Mary's hub deadline read 16/08 from the day it opened. That
was never a client date - it was the BSW/Bellview 30-day quote validity, which had become "the deadline" because it was
the only date anyone had written down, and it masked a real return date of 27/07. Swept the whole hub on 27/07 and found
five more of exactly the same kind (Gordon Court, Ninn Lane, Manor House, Riverside, Chester Thomas - all supplier or
own-quote expiries). Every job card now carries a `deadline_basis` saying whether the date is CLIENT-STATED or ours.
**A supplier's expiry is not a client's deadline.** If the deadline on your job is a date you inferred, go and find the
client's - it is in the enquiry, the register header or the ITT, and it is usually different.

**Do not trust a line-by-line text diff of two PDFs.** pdfplumber tokenises the same drawing differently between
revisions - the St Mary's floor plan came out as 937 lines in one revision and 3,285 in the other, generating pages of
fake differences. Instead compare **counts of the attributes that drive price**: window references, type codes,
structural opening sizes, opening patterns, restrictor notes, obscure-glazing notes, U-value notes, security standards.
Identical counts across all of them is a defensible "nothing changed"; a clean text diff is not. Flattening whitespace
before regex counting defeats most tokenisation noise, but merges adjacent tokens - sanity-check anything that looks
like a mass deletion before reporting it.

**A stated omission may not have happened everywhere.** Rev A said the integral blind was omitted, but 1 of the 29
blind notes survived - on Type AK, the most expensive line on the job. Verify that a claimed change is complete before
relying on it, and get the leftover corrected in writing rather than argue it at manufacture.

**Check the change against our own exclusions before calling it a scope change.** The blind omission moved the client's
scope *towards* ours - we had already excluded magnetic integral blinds on the proposal and carried no blind in the
pricing or in either supplier quote. Scope changed; our number did not. Those are different questions.

## The Chat Registry Is Shared Mutable State (learned 27/07/2026, triage)

`data/mary-jobs.json` is written by every chat and by dev commits, with no locking. Commit a3f20c5 overwrote it from a
stale copy and silently deleted a job opened an hour earlier, along with a routing fix. Worse: the bridge delivers
handoffs by iterating registry keys, so **a handoff addressed to a key that no longer exists is never delivered and
never errors** - the brief just disappears.

After any turn that touches the registry, re-run `python scripts/mary_router.py --list` and confirm the jobs you opened
are still there, then check `test-results/mary-inbox/handoffs/` for notes addressed to keys that are gone. Re-adding a
job that had never run costs nothing (new session id, no history). Re-adding one that *had* run loses that chat's memory
- `data/jobs/<key>.md` is the only backup, which is why it must be kept current.

**FIXED AT SOURCE 27/07/2026** after it happened three times in one afternoon (losing `gordon-court`, then `riverside`,
then `riverside` + `chester-thomas` + `ninn-lane` + `manor-house` together). `save_registry()` in `scripts/mary_router.py`
now re-reads the file immediately before writing and merges: on-disk jobs and chats survive, the in-memory copy wins only
where the two overlap. There is no delete path in that module, so preserving keys we have never seen is always the safe
merge. Verified by simulating the exact failure - a save from a deliberately stale copy no longer deletes anything, and
the other writer's own addition still lands. This does NOT make concurrent editing safe at field level: if two chats edit
the same job's `match` list, the last writer still wins. It only stops whole jobs vanishing. Keep doing the `--list`
check after registry work.

**THE SECOND CAUSE, found 17:30 the same day when the jobs vanished again despite the merge fix.** `mary_bridge.py`
loaded the registry ONCE at startup (line 429) and wrote that same in-memory object back on every session start and end
(lines 233, 316). The bridge was not just failing to notice new jobs - it was actively **restoring the world as it stood
when it booted**, every time any chat ran, which is why re-adding by hand never held. The loop now re-reads the registry
at the top of each pass.

**And the trap that hid it: a long-running process keeps the module it imported at startup.** The fix was on disk and
correct, but the live bridge (pythonw pid 31876, started 15:51:24) had imported the pre-fix `mary_router` and went on
executing it, so the fix was inert until restart - REQ-18. Never restart the bridge from inside a session: it is the
process that launches sessions, so killing it mid-turn ends the session doing the killing. Raise a request instead.
Generally: when a fix appears not to work, check whether the thing you are fixing is still running the old code. Editing
a file changes what the NEXT process does, not what the running one is doing.

## Clients Not To Quote

- **Hightown Housing** - Adam, 27/07/2026: "We have quoted them many times and don't win any works, so please disregard
  their quotes unless instructed otherwise." Triage their RFQs and In-Tend reminders as noise: one line in the session
  record, no email, no request raised.

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

### Stoke Park School / Borras (Aplus job 17644)

A WON job, not a tender - and the source of a rule that applies to every job bought on unglazed frames.

- **An unglazed supplier order moves the glass buy to Fenster.** Aplus supplied Technal frames "Unglazed / Supply only" with delivery 03/08/2026; the glass is Fenster's to order, price and programme. Whenever a supplier order or glass-sizes sheet says unglazed, check that a glass order exists AND that it was placed against the FINAL sizes.
- **Aplus "Glass Sizes" sheets** (`Glass Sizes_NNNNN.PDF`, sent by `noreply@apluswindows.co.uk`) are the definitive pane list, issued after frame drawings are approved. pdfplumber reads them cleanly: `item | pane ref | qty | width | height | glass type | location`. One row per pane, one item per frame bay. Panes with a negative height and `DO NOT ORDER - Unglazed` are aluminium infill panels - exclude them from the order count (5 of 175 on this job). The summary block gives Real Area vs Cost Area (minimum-area billing) per make-up.
- **Reconcile that list against the glass quote before the order goes out** - but reconcile the CATEGORY first. The final list here showed 170 panes against 124 quoted and was reported as 46 short. It was not. **The 46 are louvres**, glazed in in place of glass and bought from IKON, not the glass supplier. Once removed the glass reconciles exactly: 124 required = 124 quoted, +1.73 m2. Aplus flags only the aluminium infills `DO NOT ORDER - Unglazed`; **louvre positions appear on the glass-sizes sheet as ordinary 28mm/32mm glass**, so the sheet alone cannot tell you what is glass.
- **A SYSTEMATIC SHORTFALL IS USUALLY A CATEGORY, NOT AN ERROR.** One pane per bay across six window types plus one whole door is too regular to be clerical - that regularity means the schedule deliberately excludes something. **Search the job folder for the other supplier before raising the alarm**: louvres, spandrel/infill panels, brise soleil, mesh. Fenster's price routinely splits one elevation across two suppliers. On this job both proving documents were on file the whole time - `QT50932 Rev7 Louvres.pdf` (an Aplus **PANEL ORDER**, 46 panels) and IKON quote `Q26-24329` (46 IKL332 modules, GBP 10,125.91). A supplier-quote folder named for a non-glass trade is the tell.
- **The frame supplier's ORDER SIGN-OFF is the authority on sizes, not any quote.** `Order Sign Off_NNNNN.PDF` lists the apertures the frames are actually manufactured to. **Check the input dates**: Aplus re-input this job on 02/07 and signed the frames off the same day, so the glass quote (01/07) and the louvre schedule (input 01/07) were both silently superseded. Result: 0 of 124 quoted panes matched an ordered size (vents 404->448 high on every type, Type H -166mm, every door leaf 1859->2059) and all 41 window louvres were 85mm too tall (aperture 391 v quoted 476). **Counts reconciling is not sizes reconciling** - here the counts were perfect and not one dimension was.
- **Check which supplier quote the price was actually built on.** Where a job folder holds two quotes from one supplier, the cost build-up may still carry the old one. This price carries Vetroseal GBP 9,309.22 and IKON GBP 7,490.64 - both the 05/06 quotes to the penny - against current quotes of GBP 12,012.88 and GBP 10,125.91, so GBP 5,338.93 of cost above the sold price on a job already ordered. Nobody had spotted it because the later quotes were filed without the build-up being revisited.
- Glass rates captured: Vetroseal 8.8L-16-4T Lami/Tgh Black Multitech G, 1.2 softcoat, argon = **GBP 110.00/m2 flat** (quote 064542, 01/07/2026) plus energy surcharge GBP 0.13/kg at ~31.9 kg/m2 = GBP 114.15/m2 all in. **CN Glass rate for the same make-up is GBP 60/m2 inc energy**, +GBP 10/m2 for a 6mm toughened softcoat inner leaf. Roughly half Vetroseal - always check both on a glass package of any size. **That CN Glass figure is a verbal rate confirmed by return email, NOT a quotation** - Steve Freezer wrote the rates into his own outgoing 01/07 email to Martin Gregory and Martin replied only "Pls see below as discussed"; there is no CN Glass quotation document on file. Label it that way every time.
- Louvre rate captured: **IKON IKL332 28mm glazed-in louvre modules**, RAL 7012 matt, 1.5mm ali / 50mm Fabrock foil-backed insulated blanking panels, insect mesh - 46 modules **GBP 10,125.91** + carriage TBC (quote Q26-24329, 02/07/2026); EO plenum trays GBP 4,445.89. The earlier Q26-24160 was GBP 7,490.64 for the same 46 with **plain 1.5mm aluminium** blanking panels - the insulated panel roughly doubles the panel element (GBP 29.70 -> GBP 68.84 each). Carriage is TBC on both, so carry it.
- Generator: `scripts/stoke-glass-compare.py` -> `outputs\Stoke Park School - Glass Sizes vs Quoted Glass (check).xlsx` (summary / per-type / **louvres not glass** / **pane sizes quoted v final** / full Aplus list / Vetroseal lines). Full job record in `data\jobs\stoke-park.md`.

### Vesuvius Way, Worksop / Staniforth Construction (BUSE Gas Solutions)

Blank-rate contractor trade bill (`Aluminium Doors - Windows Bill.xls`, Staniforth format: `Pages` + `Summary` sheets, per-building sections, `Description | Qty | Unit | Rate | £ p | Notes`, `Page Total 4/9/1` markers). Priced 27/07/2026 as a budget: **GBP 110,551.98 ex VAT**. Generator `scripts/vesuvius_pricing.py`.

Durable lessons from this job:

- **A Logikal "Pos. NNN, Quantity: N" drawing is per-position and can under-state the bill.** Here three of eight drawings carried a lower quantity than the trade bill (Qty 1 vs 4no, Qty 1 vs 2no, Qty 6 vs 8), and the drawing for a priced bill item was not issued at all. Always run a **three-way quantity check - trade bill vs supplier-facing drawing vs architect's schedule** - BEFORE an RFQ leaves, not after the quote comes back. The workbook carries a dedicated `Quantity Check` sheet for this.
- **The attachments on the email are often a SUBSET of the archived tender zip.** The 27/07 RFQ carried 10 files; the zip in `<client>\<job>\1. Estimating\1. Tender Documents\` held 55, including the window schedule, door schedule and NBS spec that resolve the quantity conflicts. Always extract the archived zip before pricing, never work from the email alone.
- **Check the specified system against Fenster's actual fabricator list.** This pack is entirely Senior Architectural Systems (SF52 curtain wall, PURe No Profile Groove windows, SPD150 High Usage doors, PURe SLIDE hatch). BSW fabricate Sheerline, Aplus fabricate Technal, Bellview fabricate SMA Smart Wall - **none of them fabricate Senior**, so every register median is a proxy and must be labelled as one. A specified system nobody on the supply chain makes is a tender-stopping issue, not a detail.
- **Watch for non-aluminium items hiding in an aluminium bill.** "Louvered Double Door" read as an aluminium door; door schedule 221P specifies an insulated steel-core PPC-galvanised leaf in a 90mm galvanised frame - a Strongdor item. Same pack also has GRP fire doors and Rw 100 dB acoustic steel doors on drawing 127.
- **Fire glass in a non-fire-rated frame system is an exception, not a spec detail.** Bill called for Pilkington PyroStop in Senior PURe frames on an internal partition. PURe has no fire rating; that needs a tested fire screen. TBC + RFI, never a guessed rate.
- Client folder is spelled **`Staniforth Construction LLP`** in OneDrive, but the bill and the client's own email domain say **Stainforth** (`stainforthcon.co.uk`). Search both spellings.
- Bill dimensions read as **structural openings**, Logikal drawings as **frame sizes** (e.g. bill 2068 x 2540-2410 vs drawing 2000 x 2450). Expect a ~50-70mm difference per side and do not treat it as an error.
- Curtain walling priced on the MASTER PRICING DOC formula, **GBP 850/m2 supply + GBP 150/m2 labour**, the same basis that produced Grange Hill Methodist. For a raked screen, take the full rectangle less the triangle (here 6.9 x 6.0 less 3.35 x 3.35 / 2 = 35.79 m2).

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

## House-Format Client Documents

`scripts/generate-fenster-docs.py` produces Adam's client-facing documents (requested 2026-07-17):

- PRICING DOC: it CLONES `templates/MASTER PRICING DOC.xlsx` (copied from the live master in job folders) and fills the client block + item rows (code/desc/size/qty + supplier Frames/Glass/Additional per unit). All sell arithmetic stays in the template's own formulas: Unit Rate = Frames+Glass+Additional + (product code value x 75%) adder; CW = sqm x 850 supply + 150 labour; INSTALLATION = SUMPRODUCT over the code labour table (matches `Pricing.LABOUR_ALLOWANCES`). Sheet name is `'Pricing Document '` WITH a trailing space. Rows beyond the template's 12 are inserted with formula cloning. The TOTAL cell is rewritten to a live formula (the master carries a stale hardcoded value).
- KNOWN DISCREPANCY (flagged to Adam, unresolved): the template's x75% code adders are LOWER than `Pricing.PRODUCT_CODES` markups (SAD 900 vs 1150, DAD 1500 vs 1950, SAW 337.50 vs 400 etc.). Until Adam rules, house docs use the template's own adders; internal reviews use pricing.js.
- PROPOSAL: HTML/PDF replica of `MASTER COVER LETTER` (exec summary, 5-stage approach, inclusions/exclusions, previous projects, team cards, full verbatim T&Cs from `templates/proposal-content.json`). Project photos are placeholder slots unless paths supplied in the job JSON. Use ONLY `templates/proposal-images/fenster-logo.png` (extracted from the pricing template letterhead) - the cover-letter docx media contains CLIENT logos from past jobs (image4.png is Elkins).
- Job JSON schema: see the Lyttleton demo in HANDOVER. Every job now ships: house pricing doc + house proposal PDF + internal pricing review.

## Supplier Rate Miner

`scripts/mine-supplier-rates.py` is a READ-ONLY scanner over the OneDrive quote archive (`Commercial\1. Tender Documents\<client>`). It parses BSW, Vetroseal and Strongdor quotations into line items, grades its own output (arithmetic checks: unit x qty = total, area = w x h with Vetroseal's ~0.30m2 minimum-area billing, lines + extras = stated totals) and flags anything it cannot prove for AI/estimator review. `scripts/build-rate-register.py` aggregates the mined lines into `data/supplier-rates.json` - historical benchmark rates with provenance (quote ref, date, client, job). Never present register rates as firm prices.

Format quirks the parsers already handle (do not re-learn these):

- PDF text extraction differs by engine: pypdf and pdfplumber can give different layouts of the SAME quote; the miner uses whichever yields more text, and totals labels can appear before OR after their amounts.
- BSW: "Qty: 18Prestige T&T" can lose the space; "£" can arrive as U+FFFD; totals sometimes only derivable as TOTAL INC VAT minus VAT; extras sections ("Total Extras Value") hold trims/cills; product names can contain "/" (Foil /Wt Tilt & Turn).
- Vetroseal: rows wrap across lines and column order is unstable - fields are assigned by arithmetic self-consistency, not position; refs can be absent or pure digits; page-header address lines ("97-98 ALSTON DRIVE") leak digits into rows unless buffers terminate at QUOTATION/Page markers; delivery/oversize charges ride as 1x1mm rows.
- Strongdor: SQ PDFs come in quote and drawings variants; drawings have no price table and are classified as reference.
- Aplus is NOT yet machine-parsed (letter + Crystal Reports/Logikal OFFER formats) - files are flagged `aplus-needs-review`.

Pilot (2026-07-16, Zelltec + GCS + Key Property + Datron, 59 files): 42 ok / 14 flagged (all the known Aplus gap) / 0 unexplained anomalies; 972 line items across 18 rate categories. Ground-truthed against 6 visually-read quotes.

Full archive sweep (2026-07-16, every client under `1. Tender Documents` + `2. Projects`): 1,054 files -> 880 ok / 151 flagged / 22 reference / 1 read-error; 15,551 line items -> 79 SIZE-BANDED rate categories (bands <1.5 / 1.5-3 / 3-6 / >6 m2) covering BSW (alu + uPVC, casement/T&T/doors, glazed/unglazed/solar), Aplus (Crystal + Logikal formats, incl curtain wall), Vetroseal glass (softcoat/solar, toughened/laminated), Strongdor (Steeldor AND Firedor fire-rated doorsets) and old-format Bellview (with end-discount handling - use Grand Total Net). Additional parser knowledge from the sweep: BSW material is decided per ITEM from the product name (Prestige = Sheerline aluminium; Foil//Wt/White/Optima = uPVC - the ALUMINIUM banner also appears in uPVC boilerplate); Vetroseal quantities can reach 420+ on estate jobs; Bellview rows are "NNN qty Pcs W x H mm desc unit total". Remaining honest gaps: 32 unknown-format files (Robust, Technal glass lists, misc), 38 bsw-total-mismatch quotes (multi-section/extras variants), ~62 Vetroseal residuals - all flagged in `test-results\rate-miner-full\mined-quotes.json` rather than guessed.

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

## AOV Smoke Vents - Geometric vs Aerodynamic Free Area (Riverside House, 27/07/2026)

**Standing rule for any job with an AOV or smoke vent.** Free area is quoted two ways and they differ
by roughly 40%:

- **Geometric** free area - the measured opening. What A Plus put on Riverside QT51518: 1.30 m2.
- **Aerodynamic** free area - geometric x the vent's discharge coefficient (Cv), per BS EN 12101-2.
  What smoke ventilation is commonly *specified* in.

Measured on A Plus's own DualFrame 75Si AOVs, quote QT51516 (Towcester Vale), which states both on
every line: **aerodynamic runs at 60-62% of geometric** - 0.49 against 0.81, and 0.54 against 0.87.

So a quote giving geometric only against a spec written in aerodynamic looks compliant and is not.
**Make the supplier state the aerodynamic figure for the actual sizes.** Do not derive it from frame
area: Towcester's geometric/frame-area ratios are 75% and 54% on the same product, so it does not
scale.

**But you can usually work out which basis the pack means, and it is the pack's cited standard that
tells you.** Free area is the language of the PRESCRIPTIVE route - Approved Document B. Aerodynamic
free area is the language of the ENGINEERED route - BS 9991 / BS EN 12101-2. So look for what the
drawings say they comply with before treating the basis as unknowable. Two corroborating sources,
both real:

- Riverside's drawing key reads *"MAINS OPERATED INTERLINKED HEAT DETECTOR TO **AD B1**"*, and its
  smoke-vent note is the AD B common-stair provision almost verbatim - automatically openable vent,
  1m2 free area, fire-brigade operated from ground floor access level. Prescriptive route, so
  geometric.
- Gordon Court's NBS 9001 L20 cl.630 states it outright for the identical duty: *"AXS140 STAIRWELL
  VENTILATOR - throat dimensions 1250mm x 1000mm - **1m2 GEOMETRIC free area**"*, and the lobby
  ventilator at 1.5m2 geometric. The word *aerodynamic* appears nowhere in that job's 186-page NBS,
  140-page mechanical or 127-page electrical spec.

That makes geometric the strong reading for a stairwell vent written as "1m2 free area" - but it is
still a recommendation for the fire engineer or building control to confirm, not a ruling to make.

**BEFORE COMPARING FREE AREAS, CONFIRM THE QUOTE IS FOR A VENTILATOR AT ALL** (Gordon Court, 27/07).
BSW quoted "Qty: 3 Prestige T&T" and "Qty: 4 Prestige Casement" against positions the spec required to
be Colt motorised ventilators - zero occurrences of AOV, louvre, actuator, chain, stroke, motor, 24V
or smoke anywhere in the quote. A quote with no ventilator in it states no free area of *either* kind
and reads as merely silent. **The tell is the rate**: GBP 412-443/m2 there against GBP 1,401/m2 for a
real AOV. Grep the quote for actuator / stroke / 24V before you trust its free area.

**AND CHECK WHERE THE QUOTE DELIVERS TO.** A Plus QT51518 carries *no site address at all* - the only
address on it is Fenster's own yard, 97-98 Alston Drive, Bradwell Abbey, MK13 9HF. "Glazed /Supply
Only (Delivered)" therefore ends in Milton Keynes, not at the Aylesbury site, and the onward leg is
ours and in nobody's price. All five of Gordon Court's supplier quotes do the same. This is a
*separate* miss from the free-delivery threshold and it survives clearing it - a load can be delivered
FOC and still not reach site. Suppliers also typically require labour at the delivery point to unload.

**WHERE OPENINGS ARE NEWLY FORMED, SIZE IS NOT A CONSTRAINT** (Adam, REQ-9, 27/07): *"We can make the
windows as big as we need to in order to achieve the free area, because the openings are being newly
formed."* Establish this early on any job with a performance-driven opening size - it turns a
free-area shortfall from a design fight into a repricing question.

**READ THE WALL TYPE, NOT THE WINDOW TAG.** This supersedes the window-tag rule below, which its
author withdrew after rendering the elevations: Gordon Court's WE_2 windows turned out to sit in newly
built zinc-standing-seam-on-stud walls, so **WE_/WN_ is a schedule reference** - which of two schedules
the type lives in - not a statement about the opening. Do not price off a window tag prefix.

What replaces it answers *both* "is the opening new" and "what is it cut into" in one read, because it
describes the actual construction at that point of the facade. Their South elevation carries a WALL
TYPE LEGEND: *"EXT - Existing wall types as surveyed"* against *"WT-A0 Brickwork / Cavity Insulation /
Block"*, *"WT-A1 Brickwork / Insulation / Stud"*, *"WT-A2 Zinc standing seam / Insulation / Stud"*.

**Where there is no build-up legend, a drawing that colour-codes CHANGE tells you what is existing by
omission.** Riverside's plans code every new or altered wall (new partition, new separating wall
upgrade, separating wall upgrade to existing, blockwork infill); at both stairwells the internal walls
are coded and the **external walls carry no coding at all**, which reads as retained fabric and
corroborated the conclusion independently. Weaker than a build-up legend - it says "not changed"
rather than naming the construction - but available on most refurbishment layouts and it does not need
the demolition plan.

**Knowing a wall is existing is not the same as knowing you can cut it.** Without a build-up legend you
still do not know the construction, and that decides the lintel, the fixing type and the cost of
forming the opening.

**WHEN THE LEGEND SAYS "AS SURVEYED", GO TO THE STRUCTURAL ENGINEER'S INVESTIGATION DRAWINGS.** That
wording defers rather than describes. On a refurbishment somebody had to sample the masonry before
anything was designed, and the answer is in the engineer's sub-folder, not the architect's set - Gordon
Court's *"Brick & mortar sampling locations"* drawing states *"sampling in the internal SOLID wall...
in CAVITY wall... take samples from BOTH THE INNER AND OUTER LEAVES"*, which is the build-up. The same
folder held GPR surveys, a resin-injection methodology and a workmanship spec with sections on cavity
walls and lintels. **Asking the architect for a wall build-up and asking the structural engineer for
the investigation drawings are two different requests.**

**And if no structural engineer is named at all, that is itself the finding.** Riverside's six drawings
name a heating engineer and an electrician and otherwise defer everything to site - *"CONTRACTOR TO
ESTABLISH"*, *"TO BE SITE AGREED"*, *"TO SUIT BUILDING INSPECTOR APPROVAL"*. On that pack a new opening
in retained masonry has neither a design nor a price behind it, which is a different problem from being
expensive.

**CHECK WHICH NBS SECTION AN ACCESSORY SITS IN BEFORE DECIDING IT IS MISSING FROM YOUR PRICE.** Cavity
closers, cavity trays and jamb DPCs at openings sit in **F30** *"Accessories/sundry items for
brick/block/stone walling"* - masonry, so the bricklayer's, even where a new opening is formed. Gordon
Court nearly raised their absence from four BSW quotes as a gap; they were correctly absent.

**BUT AN INTUMESCENT PERIMETER SEAL IS OURS.** NBS **L10 cl.790** *"Fire-resisting frames"*: *"Gap
between back of frame and reveal: Completely fill with INTUMESCENT mastic or tape."* L10 is the windows
section. A supplier's fixing pack described as *"screws, foam, packers, mastic"* does not comply - it is
a fire-rating requirement, not a finish, and a different product at a different price. **If you have
fire-rated frames, grep the quote for "intumescent"; it hides inside a fixings line.** Not applicable
where the frame is in an external wall rather than a compartment wall - the seal is then weathering.

**THE PACK MAY ENCODE NEW-VERSUS-EXISTING IN THE WINDOW TAG - BUT SEE THE WITHDRAWAL ABOVE.** Gordon
Court's Proposed South Elevation carries a WINDOWS TAGS legend: *"WE_00 Windows in EXISTING openings
replaced as new / WN_00 Windows in NEW openings / WL_00 Louvres to smoke shaft"*. The type prefix
answers the question outright - and the legend that defines a naming convention **may not be on the
sheet you are working from**. It also scoped their strip-out (it attaches to the WE_ types) and
confirmed their AOVs sit in new openings. If a schedule uses type prefixes, find the legend.

Where there is no such convention, read the plans: Riverside's W1/W2 are *performance* tags, so the
stairwells had to be read directly - and see below, the answer split per vent. **Also watch for
glazing carrying NO tag at all**: Riverside's stair windows are the only glazing on the drawings
without a W tag, which is probably why the vents were never scheduled. Untagged glazing is invisible
to a schedule.

**AND "A NEW OPENING" IS NOT "A FREE OPENING" - ASK WHAT THE OPENING IS CUT INTO.** This is the layer
under the tag, and it caught both jobs. Gordon Court's WN_7 at level 1 is a new opening in **retained
fabric** - their demolition plan says *"Retained wall to be assessed on site"* and *"new brick slips are
to be installed as part of the facade works"* - so lintels, cutting and making good, none of it priced;
the same type at levels 2 and 3 sits in two **added storeys** and is genuinely free. Riverside has no
new-build half at all, so *both* its vents carry structural cost. **On a part-refurbishment a new
opening in retained masonry and a new opening in new build are different jobs at different prices, and
a type prefix cannot tell them apart.** Only the demolition plan can.

So the question is three deep, and each layer caught the one above it:

1. Is the opening **new or existing**? (tag prefix if there is one, otherwise read the plans)
2. If new, **what fabric is it cut into** - retained masonry or new build? (demolition plan)
3. Is it a **wall** opening at all, or a roof vent? (see the AOV note above)

**BUT VERIFY IT AGAINST THE PACK, AND CHECK IT FLOOR BY FLOOR.** Gordon Court's schedules constrain
ground and first floors to *"the existing structural opening sizes"* while levels 2-3 are new build
and free - so a shortfall can be designed out upstairs and not downstairs. On Riverside the pack did
not corroborate it at all: K1653-04 *"EXISTING / PROPOSED ELEVATIONS"* is a **single** set of eight
elevations showing a complete, regularly fenestrated building, with no new opening marked and no AOV
drawn anywhere. Three things follow when the openings turn out to be existing:

- Enlarging one is structural - lintel, cutting, making good - and is normally in nobody's price.
- **Check the planning application TYPE before assuming any elevation can change.** Riverside's
  drawings are stamped **24/02303/PAPCR** - a *prior approval* reference, not a full permission.
  Prior-approval conversions normally carry tight limits on external alteration, so "as big as we
  need" may not be available at all. One question to the planning consultant settles it.
- Check the **head shape** of the opening you are going into - and check it is a WALL opening at all.
  A Riverside arched-head flag was raised and then **withdrawn**: the arched windows on Elevation F
  turned out to be the Living room's, not the stairwell's. What replaced it is worse. The second-floor
  stairwell has **no wall opening of any kind**, and the note says the stair is vented *"AT THE TOP
  STOREY ROOF"* - so that vent may need a **roof vent** while the supplier has quoted a wall casement
  on a 155mm subcill. **On any AOV, establish wall or roof before accepting a window quote for it.**
  The standard product for a 1 m2 stairwell duty is a roof unit: Gordon Court's NBS specifies a
  *"STAIRWELL VENTILATOR... ROOF MOUNTED ONTO HORIZONTAL KERB... 1m2 geometric free area"*, with a
  separate **wall-mounted model** named where a wall unit is wanted - and the items actually quoted on
  that job were wall units. Neither job can settle it from a supplier; it is the architect or fire
  engineer. If it turns out to be a roof vent, the whole window quote for that position is void.

**A PACK CAN HOLD TWO LAYOUT SETS, AND ONLY ONE MAY CARRY YOUR REQUIREMENT.** Riverside has the
planning layout (K1653-03, all three floors on one sheet) and the construction-issue layouts
(K1653-10b/11/12). Only the construction set carries the smoke-vent note - and the tidier revision
history is on the sheet that does *not* mention the requirement. Related, and Gordon Court's rule:
**list every sheet with its revision and date and look at the outliers.** On Riverside the AOV
requirement appears only on K1653-11 and K1653-12, neither ever revised since Mar 24, while the ground
floor plan was revised twice in Nov 25. Probably innocent; one line to confirm. It works on a
six-drawing pack, not just a large one.

**NO APERTURE PERCENTAGE IS A COMPLIANCE TEST - THE CLEAR OPENING IS THE MANUFACTURER'S FIGURE.**
Gordon Court quantified this by varying only the assumed nominal section on their unit against a
1.5 m2 duty: 60mm gives 103.0%, 65mm 101.1%, 70mm 99.3%, 75mm 97.5%, 85mm 94.0%. **A +/-5mm change in
an assumed section swings the answer clean across the duty line**, so a computed "99.3%" is an
estimate whose error bar swamps its own margin. The one thing that survives is a direction of travel:
the aperture is an *upper bound* on clear opening, because the leaf sits within it.

There is a distinction worth keeping, because it decides when the arithmetic is worth doing at all.
**Reconciling a figure the supplier has already stated is robust; predicting one they have not is
not.** Riverside reconciles A Plus's published 1.30 m2 - 957 x 1357 reproduces it to 99.9%, and across
head+cill from 150mm to 200mm the reconciliation only moves 101.6% to 97.9%, with no line to cross
because the test is whether it holds. Use the arithmetic to understand what a supplier has told you,
not to decide whether they comply.

**THE RIGHT DENOMINATOR FOR A CLEAR-OPENING RATIO IS THE APERTURE, NOT THE GROSS FRAME.** A
"required free area ÷ GROSS frame area, query anything above ~60%" rule of thumb was proposed on
Gordon Court and **has been withdrawn by its author** - do not re-adopt it. It condemns borderline
units: recomputed on the aperture, their WN_7 went from "cannot reach 1.5 m2" to 99.3% of it, short by
0.01 m2. Riverside is where the correction came from: A Plus's quoted 1.30 m2 is 75% of the gross
frame, which looks wrong until you compute the aperture - 957 x 1357 = **1.2986 m2** - and find the
quote is exactly 100% of it. **Divide by the aperture.** The gross-frame ratio is only a proxy for how
much of the frame the sections eat, and sections eat far more on a tilt-and-turn than on a fixed-light
frame. Note the aperture itself is usually inferred from a nominal section depth unless the supplier
states it, so it is an estimate too - the clear opening is the manufacturer's figure to give.

That same arithmetic resolves configuration questions: it showed the whole Riverside frame opens as
one bottom-hung sash with the transom a glazing bar within it, which is why a single 850mm chain works
on a frame whose individual apertures are only 590mm high.

**CHECK WHAT THE PACK REFERS TO THAT IT DOES NOT CONTAIN, AND WHAT THE DRAWING NUMBERS IMPLY IS
MISSING.** Two cheap tests, both of which fire on small packs as well as large ones:

- *Cross-references.* When a drawing says to read it with another document, check that document is
  there. Riverside's plans cite DETAIL 1, 2, 4, 5 and 6 - *"SEE DETAIL 6 FOR THERMAL UPGRADE TO
  ROOF"* - and not one detail sheet is in the pack. On Gordon Court, three of four referenced
  documents were absent, including the demolition elevations the demolition plans require.
- *Numbering gaps.* Riverside holds K1653-03, 04, 10b, 11, 12 - five sheets with 01, 02, 05, 06, 07,
  08 and 09 unaccounted for. Gordon Court's loose job folder held **25 of the 82** drawings in the
  tender zip, and the 57 absent included every floor layout, every existing plan and all three
  demolition plans; what it *did* hold was the similarly-numbered SETTING OUT series.

**And check for DUPLICATE sheet numbers at different revisions** - the sibling failure where the sheet
is present twice and one copy is stale. Gordon Court's zip holds 21005/6/7 at both rev 02 and rev 03,
and the tag legend above exists *only* on 21007 rev 03 - 5,751 characters against rev 02's 2,487.
Comparing extracted TEXT LENGTH between revisions of the same sheet is a fast way to spot it. So
drawing hygiene is three one-minute tests: **gaps in the series, cross-references to absent documents,
and duplicate numbers at different revisions.**

**Ask for the drawing register or issue sheet** rather than inferring from gaps. And note which
document classes tend to carry the answers: the **fire strategy** states the free-area basis in its
own words, and the **demolition plan** is where new-versus-existing openings are marked (*"NEW
STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE"*). If those two are missing, the questions they
answer cannot be reasoned out from what is left.

Two more from the same job:

- **Check where the requirement came from.** Riverside was priced against "we need 1.5m2", which was
  Fenster's own enquiry wording. The pack required **1m2**, once per stairwell. A vent reported to
  Adam as 0.20 m2 short in fact cleared the drawing by 30%. An enquiry email is our assumption; the
  pack is the requirement.
- **An AOV window is not an AOV system.** The supplier fixes the actuator and leaves the flex coiled.
  The control panel, supply, cabling, fire-brigade override and commissioning are somebody else's -
  and on Riverside they were in nobody's scope. Where a drawing requires fire-brigade operation, the
  window alone cannot satisfy it.

There is **no AOV / smoke vent category in the rate register** (80 categories, no match), so there is
nothing to benchmark against. First data point: A Plus DualFrame 75Si bottom-hung AOV, glazed,
1.729 m2, 850mm stroke single chain = **GBP 1,401.24/m2 supply**, against GBP 528.83/m2 for a plain
glazed aluminium window in the same size band. One quote, not a median.

## When A Job Stalls On A Client, Sort Open Items By Who Blocks Them

Gordon Court / Riverside, 28/07/2026. A job "waiting on the client" is rarely blocked in whole. **Sort
every open item by who actually owns the answer, then check whether the unblocked half is
time-sensitive.** Riverside's brief split clean: seven items were questions for A Plus about their own
quote and needed nobody's decision; eight needed the client, the architect or the planning consultant.
The whole thing had been treated as gated for four turns. Gordon Court found eight of their twelve money
items were supplier questions that did not need the client's September award, closable by two RFQs.

**Then run the validity arithmetic, because the unblocked half often decays. There are TWO dates and they
answer different questions:**

| | |
|---|---|
| **supplier expiry MINUS your own validity period** | the last date you could ISSUE and still be covered. It may already be behind you. |
| **supplier expiry itself** | the last date you can ASK that supplier anything as an ADDENDUM rather than a new enquiry. |

**CHECK YOUR OWN TERMS AND CONDITIONS PAGE BEFORE REPORTING ANY GAP - THE ANSWER MAY BE IN THE DOCUMENT
YOU SENT.** Fenster's house T&Cs (`templates/proposal-content.json`, "Quotation Validity") read: *"All
quotations provided by Fenster Glazing & Locks Ltd are valid for 30 days from the date of issue, unless
agreed otherwise. All quotations are subject to final site survey and measurement verification."* Gordon
Court had reported 163 days of unqualified exposure for a week before reading page 8 of their own issued
proposal - it is qualified, not absolute. **And the second sentence qualifies dimensional risk too**,
which matters wherever sizes came from an enquiry or a supplier quote rather than a survey. Source the
clause from the house document, not from a generator footer.

Riverside: A Plus expires 26/08 and the house document carries 30 days, so the last issue date still
covered was 27/07 - now past, and **the gap grows by a day for every day of delay**. Asking a supplier to
hold their price is the one action that becomes *more* valuable the longer a gate stays shut.

**And the second date is the one people miss.** Anything sent while a quote is live is priced against it
- same job, same spec, same rates, they add lines. Anything after is a fresh enquiry at whatever the
market is by then. **So a lapsing quote is a deadline for every question you still want to ask that
supplier**, and it bites hardest on "price me the alternative", where the whole value is the delta
against what you already hold. Gordon Court had nine days to convert eight unpriced items; Riverside has
29 to get a resize priced against GBP 4,845.22 rather than from scratch.

## "No Rate" And "No Quantity" Are Different Problems With Different Owners

Riverside / Gordon Court, 28/07/2026. Before calling something unpriceable, sort it:

| | | |
|---|---|---|
| rate **and** quantity | price it | - |
| quantity, **no rate** | **supplier question** - usually closable this week | Riverside's window restrictors (2no), onward haulage |
| rate, **no quantity** | **designer question** - ask for an area, not a price | curtain walling: `mary_pricing` carries CW_SUPPLY_M2 850 / CW_LABOUR_M2 150, but no schedule gives the area |
| neither | genuinely unpriceable - TBC plus an RFI | AOV control system, scaffold, undesigned structural work |

Gordon Court had listed curtain walling as unpriceable when it has a rate and lacks a quantity - the
opposite problem, and a different party to ask. **Neither middle row is a genuine hole.**

**AND A SECOND, DIFFERENT TEST ON THE SAME LIST: "we exclude X" is only safe if X is genuinely SOMEBODY
ELSE'S under the spec.** The two questions are not the same and both are worth ten minutes - *is a rate
or a quantity missing* tells you **who to ask**; *is this genuinely somebody else's* tells you **whether
you should be asking at all**. An item can pass the first and fail the second.

Three of Gordon Court's twelve exclusions failed it: *"Fire Stopping - to be done by others"* against NBS
L10 cl.790, which puts the intumescent frame-to-reveal seal in the **windows** section; *"Testing - on or
off site testing"*, which does not cover cl.205's requirement for third-party **certification
documentation** the maker already holds; and *"Site Storage - Materials will be delivered to site"*,
which **asserts a fact no supplier quote supports** - all five deliver to our own MK13 9HF yard. On
Riverside the same test caught **onward haulage from our own yard to site**: not another party's at all,
since Fenster are the installer - it was excluded because nobody had priced it.

**And one distinction worth keeping: excluding the WORK is not the same as not needing the NUMBER.**
*"Design calculations excluded"* fairly covers us producing a U-value calculation; it does not excuse not
having the figure, which the supplier should state as a matter of course.

**Run the sort across an exclusions list, not just an unpriced list.** On Riverside it found window
restrictors sitting quietly excluded when A Plus's own notes put the duty on *"the facade contractor /
fabricator"* - which, Fenster being the installer, is us - and disclaim liability for damage to the vent
if none is fitted 50mm beyond the stroke, on a life-safety system. Quantity known, no rate anywhere, so
only a supplier could price it. **Sometimes an exclusion is an unanswered supplier question wearing an
exclusion's clothes**, and the test is whether excluding it was a decision taken against a number or a
gap left because nobody could price it.

**And say whether the unblocked work is wasted under the other outcomes** - on Riverside, if the
wall-or-roof question resolves badly only two of seven items fall away, and only for one of two vents.

## The Rate Register Prices Frames And Glass, And Almost Nothing Else

Verified at source 28/07/2026: of `data/supplier-rates.json`'s **80 categories, all of these return
zero** - acoustic, trickle, Linkvent, Passivent, curtain, actuator, AOV, smoke, strip, disposal,
manifestation, intumescent, mastic, restrictor, scaffold, kerb, roof vent, secondary, folding, sash,
slider.

The four missing categories already on the board were unusual **products** - folding doors (Grange
Hill), vertical sliders (Georgie's), secondary glazing (Lower Range Road), AOV/smoke vents (Riverside).
The rest are **ancillaries that appear on nearly every refurbishment**: strip-out and disposal,
manifestation, acoustic trickle vents, intumescent seals, curtain walling, plus mastic, restrictors,
scaffold and kerbs.

**Stated precisely, because "the register has nothing" overstates it:** a few standing house rates exist
outside the register - mastic GBP 5/lm, EPDM GBP 25/m2, install default GBP 140/unit. The register does
frames and glass to size-banded, supplier-attributed depth; the ancillaries have one flat house rate or
nothing. **On a new build that hardly matters. On a refurbishment, where ancillaries are a large share of
the value, you can price the windows and none of the work around them** - so do not quote a refurb off
the register and report the whole-job error as small. Where there is no category, the honest output is
TBC plus an RFI, not a rate nobody can defend.

## Draft The Letter, Not The Request - And Check What Is Still Sitting In Outputs

Riverside / Gordon Court / St Mary's, 28/07/2026. **A request with no text behind it is still a request
for somebody else to write an email.** Gordon Court's REQ-26 carried a nine-day deadline and no draft;
Riverside called half a brief urgent for two turns while it sat inside a fifteen-item document someone
would have to disassemble first. St Mary's had already made the general point: **on a deadline, draft the
deliverable BEFORE the decision comes back, not after.**

**Clause 16 is not only a sort, it is a document plan.** Split the findings by whose responsibility they
are and you get two letters with two tones, derived rather than chosen:

- **to the supplier** - the ours-to-fix items: product suitability, figures they hold and we do not,
  dimensions, delivery. **Date it**, because a supplier letter *decays*: after their quote lapses,
  everything in it is a fresh enquiry rather than an addendum to a live quote.
- **to the client** - what the Design Responsibility clause puts on their professional team, worded as
  questions and reliances. **No date** - it does not decay, it just gates the answer. Group by owner
  (architect / planning consultant / client) so it can be forwarded rather than answered.

The fact that only one of the two carries a date is the sort doing real work.

**Two drafting choices, both about not overclaiming:**

- **Ask a supplier what they priced AGAINST, not why they got it wrong.** Before drafting, check whether
  the thing you are querying is something the supplier *chose* or something you *told them*. Riverside's
  1130 x 1530 came from Fenster's own enquiry - A Plus quoted exactly what was asked for, so if the
  product is wrong for the position that is our specification, not their error, and the letter says so.
- **When a decision has been taken, say so in the document.** A draft that quietly relitigates a decision
  its author accepted is worse than no draft. State plainly what is *not* being reopened.

**A DRAFT CAN ALSO GO STALE ON A DATE YOU TYPED INTO ITS OWN FILENAME** - the easier half to defend
against, and easily missed. A letter arguing it is *"an addendum to a live quote"* stops being true the
day that quote lapses. Head every dated draft with **`IF TODAY IS AFTER <date>, DO NOT SEND THIS AS IT
STANDS`**, list the sentences that go false, and say what survives - usually the questions do, and it
needs re-heading as a fresh enquiry rather than binning. `python scripts/mary_stale_drafts.py` sweeps
`outputs\` for dated and superseded filenames; it deliberately does **not** judge undated drafts, because
a filename cannot tell you whether the facts underneath one have moved.

**AND ATTRIBUTING A QUOTE LINE BY PROXIMITY MISREADS MULTI-POSITION QUOTES.** Searching for a glass
string and reading the nearest preceding `Location:` header attributes the line to whichever position
happens to sit above it on the page. On a quote where one position carries five glass lines that is
near-certain to be wrong - it put Gordon Court's obscure-glazing finding on the wrong position and
understated it by sixteen units. **Parse into position blocks and attribute each line to the block that
contains it.** The hazard scales with block count: impossible on a one-position quote (Riverside's
QT51518 has one, checked rather than assumed), near-certain on a large one.

**AND CHECK WHAT IS STILL SITTING IN `outputs\`.** Riverside's turn-one reply to Adam remained there as a
clean-looking draft after three of its central claims had been withdrawn - it was in the house voice,
addressed to the right person, and nothing in the filename said it was stale. **A superseded draft in an
outputs folder is a live hazard, not a harmless record.** Rename it `(SUPERSEDED <date>, do not send)`
and put a header on it listing what it gets wrong and what replaces it.

## Who Owns The Decision, And Who Holds The Information?

Riverside / Gordon Court, 28/07/2026. **For every open item, write down who owns the DECISION and who
holds the INFORMATION, and confirm you have asked both. They are usually different parties.**

Gordon Court asked the **GBP 18,298.94** supplier how long it could hold its price and *explicitly did
not ask* the **GBP 183,005.42** one - 91% of the exposure - because Adam had decided we carry the risk,
so asking looked pointless. **That conflates a decision about whether WE hold OUR price with whether we
gather information from a SUPPLIER.** Asking costs nothing, withdraws nothing and commits nothing.

Riverside had one supplier, so ran the underlying shape instead: the AOV control system, the largest
unowned item on the job, was asked of the **client** (*"who is carrying it?"*) and never of **A Plus** -
who supply the actuator and whose own notes say it *"must be powered by a compatible control system which
is approved by SE Controls"*. The supplier was left out because the scope boundary had already been
decided. **A scope boundary says what a supplier will SUPPLY, not what they can TELL you.**

**Two practical forms of the check:** if you have two supplier letters on one job, **diff them for
questions one asks and the other does not** - Gordon Court's differed on the single biggest commercial
question on the job. And if you have one, check each open item for a question you dropped because a prior
decision made it look pointless.

## Clause 16: Sort Findings By Whose Responsibility They Are

Riverside / Gordon Court, 28/07/2026. Fenster's own Terms and Conditions run to twenty clauses; **clause
2 is Quotation Validity and clause 16 is Design Responsibility** (verified by enumerating the headings in
`MASTER COVER LETTER 31.05.2026.docx`, not taken on trust):

> *"Fenster Glazing & Locks Ltd is not responsible for overall design intent, architectural suitability,
> or **REGULATORY STRATEGY** and relies on information, drawings, and specifications provided by the
> client or their professional team. **Responsibility is limited to MEASUREMENT VERIFICATION, SUPPLY, AND
> INSTALLATION** of the agreed glazing systems."*

This is the third sort over a findings list and it answers the question the other two do not. *Priced /
benchmark / unpriceable* asks **what can you cost**. *Rate versus quantity* asks **who do you ask**.
Clause 16 asks **whose responsibility is it** - and therefore **how the finding should be raised**.

| **THEIRS** - we rely on their professional team | **OURS** - the clause expressly retains it |
|---|---|
| Which duty a vent serves; geometric vs aerodynamic; whether a roof vent is required | Whether we quoted **the right product** for the position |
| U-value and g-value targets; PAS 24; trickle areas; acoustic vents; manifestation extent | Whether the supplier **stated a figure at all** |
| Planning consent; whether a design change removed an item; drawing currency | **Every dimension** - measurement verification |

**The split that stops it being a get-out.** *"Is a roof vent required?"* is regulatory strategy -
theirs. *"Have we quoted a wall casement for a position the drawing puts on the roof?"* is supply -
**ours**, and clause 16 does not touch it. Same on thermal: *is 1.6 the right target* is theirs; *has the
supplier stated a Uw at all* is ours to obtain.

**And it TIGHTENS dimensional findings rather than loosening them.** Clause 2 makes the price *"subject
to final site survey and measurement verification"*; clause 16 says our responsibility **is** measurement
verification. **The survey makes a dimensional discrepancy fixable - it does not make it somebody
else's.**

**Practical effect: ours-to-fix items belong in a supplier RFQ; theirs belong in a client qualification
framed as RELIANCE, not as defects.** Two documents, two tones. It also doubles as a priority order - the
*ours* items do not go away whatever the client answers, so chase them regardless; the *theirs* items
resolve the moment the client responds, so time them accordingly. **Read your own Design Responsibility
clause before deciding how to raise a compliance finding.**

**A related extraction trap, from the same evening:** a two-column inclusions/exclusions table interleaves
when extracted, producing *"Site Survey - Only conducted once the structural openings **Fire Stopping - To
be done by others, if required** are fully formed"*. **When a phrase reads oddly in extracted text,
suspect a multi-column table before you suspect the document.** Same failure mode as the interleaved door
schedules.

## A Representation Of The Source Is Not The Source

Gordon Court / Riverside / St Mary's, 28/07/2026 - the same error three times in one night, and it is
worth naming because it does not look like an error at the time.

- Gordon Court reported **GBP 5,597.89 of cost with "no supplier quote behind it"** since their first
  turn, in four documents. They had used a **half-filled working column** as the test of whether a
  supplier line existed. All seven lines were quoted, at exactly the workbook costs. Withdrawn.
- St Mary's found a request a **print statement** said had been raised and which never existed.
- Riverside quoted a 30-day validity off a **generated footer** rather than the house document.

**A working column, a print statement and a generated footer are all representations of a source, not
the source.** If a finding rests on one, read the document before you post it - certainly before you
report it four times.

**AND A SAMPLE WITH NO VARIATION IN IT CANNOT TELL YOU WHY.** Riverside measured three truncated
findings on one job, saw the remedy cut from all three, and posted that *"the rules are written
statement-first and action-last"*. Measured across 13 manifests and 44 remedy sentences, that is wrong -
**most rules put the remedy first**:

| detail length | n | median remedy position | cut |
|---|---|---|---|
| 400 chars or under | 35 | **0%** | 3 of 35 |
| over 400 chars | 9 | **84%** | **9 of 9** |

**The remedy is displaced backwards by the list of offending items, and that list grows with how much is
wrong - while the truncation that hides it is triggered by the same length.** So the instruction vanished
exactly on the jobs where most had gone wrong. One rule proves it, identical code throughout:
`delivery actually included` shows the remedy at 0% on ten one-supplier jobs (332 chars), 78% on
Riverside (447), 89% on Gordon Court (776). All three of Riverside's samples sat at 73-79% - **it had no
short finding to compare against, so it could not distinguish a property of the system from a property of
its own job. Before posting a mechanism, check your sample contains a case where it would NOT apply.**

**AND A TRUNCATION IS NOT NEUTRAL ABOUT WHAT IT REMOVES.** `report()` in `mary_checks.py` - the gate
that decides whether a quote goes out - printed the first 200 characters of a FAIL and stopped, no
ellipsis, no count. On Gordon Court that hid **GBP 201,304.36** of unfixed cost and sixteen of nineteen
uncovered spec items. Measured on Riverside the loss was only 586 characters, but **all three cuts
removed the REMEDY and none removed the FINDING** - because these rules are written statement-first and
action-last, so **a trailing cut strips the instruction out of every rule at once.** Fixed: FAIL and ASK
wrap in full, PASS and n/a state `... (+N chars)`. **When you truncate, ask which end of the sentence
carries the action.**

**AND WHEN A CHECK IS BLOCKED BY A MISSING TOOL, FIND A ROUTE THAT REMOVES YOUR JUDGEMENT FROM THE CHAIN
RATHER THAN ONE THAT REPRODUCES IT.** Riverside's GBP 5,990.22 was confirmed by hand and by
`mary_pricing` - two routes that agreed because both rested on the same reading of the same formula
chain. **That is repetition, not verification.** With Excel COM blocked, the third route was a parser
that extracts the code-to-adder and code-to-labour maps *from the formula text itself* and applies them
to the cell values. The residual shrinks from "did one person read it right" to "would Excel read it
differently from the parser".

**AND A REPORT THAT OMITS A CATEGORY IS WORSE THAN ONE THAT SHOWS IT WRONGLY.**
`scripts/mary_stale_drafts.py` bucketed dated drafts as `days < 0` to expired and `days <= warn_days` to
due, **with no else** - so any dated draft more than a fortnight out was parsed, dated and silently
dropped. Riverside's A Plus letter at 29 days was absent from every section while the sweep concluded
*"Nothing expired"*. Fixed with a **DATED, NOT YET DUE** bucket. **If you write a tool that buckets
things, check every branch has a home** - and a clean-looking report is not the same as a complete one.

**AND THE SIGN-REVERSED VERSION: A FAILED SEARCH IS NOT EVIDENCE OF ABSENCE.** Riverside reported "the
OneDrive job folder is still empty" five times. It was never empty - it held the supplier quote, the
master cover letter and the master pricing doc. The searches ran against
`OneDrive - Fenster Glazing & Locks Ltd`, which does not exist; the root is
`OneDrive - Fenster Glazing (1)`. **If a check returns nothing, prove the check can return something
before you report the nothing.**

**AND AN EXTRACTION CAN BE FAITHFUL AND STILL INCOMPLETE.** `templates/proposal-content.json` misquotes
nothing, but it holds **76 paragraphs against the source docx's 153** - and the missing half contained
*"Site Survey - Only conducted once the structural openings are fully formed"*, the clause most material
to a job forming a new opening. **Checking that a quoted line is accurate is not the same as checking
the source has nothing else in it.** Worth running against any extracted spec or NBS text.

**Two clauses of our own that turn up when you read the real cover letter**, both worth knowing on every
job: the site survey happens only *after* structural openings are formed, which puts our survey and the
supplier's manufacture behind the builder's programme; and Fenster is *"not responsible for overall
design intent, architectural suitability, or **regulatory strategy**"*, relying on the client's
professional team - which qualifies compliance questions like a smoke vent's free-area basis.

## Deferrals: Administrative Gap Or Design Gap? And Read The Title Block

Riverside / Gordon Court, 27-28/07/2026. A drawing that says *"to X's specification"*, *"as surveyed"*
or *"to be site agreed"* is deferring. **Before raising a deferral as a finding, spend two minutes
establishing which of two completely different problems you have.**

| | |
|---|---|
| Deferral to a **named, appointed** consultant whose other work is in the pack | **ADMINISTRATIVE gap.** The document exists. Ask for it, price on, qualify if it does not arrive. |
| Deferral to **nobody** - no consultant named anywhere, everything *"to be site agreed"* | **DESIGN gap.** There is nothing to ask for. This is the one that should stop you. |

**The title block is how you tell them apart.** Gordon Court closed their longest-running question by
reading one: their Energy Statement's *"Edward Pearce... Project No. 22/190"* carries the same project
number as every M&E document in the pack, so the architect's deferral pointed at a document they had
held since turn one. Riverside ran the same test and got the opposite answer - no structural engineer
named on any of six drawings, everything deferred to site - so a new opening in retained masonry has
neither a design nor a price behind it.

**And the title block tells you who to ask.** Riverside spent three turns requesting "the fire
strategy" before noticing there probably is not one: no fire engineer is named, and the smoke-vent note
is the *architect's own*, written in AD B language on a sheet keyed *"TO AD B1"*. On a prior-approval
conversion of that size the architect commonly carries the fire strategy inside the drawings.
**Ask the author of a note, not a consultant who may not exist.** Read the title block before writing
the RFI: it gives the job number, the practice, the reviser's initials and a phone number, and the job
number is the handle for the sheets you do not hold - *"please issue the K1653 drawing register"* can
be actioned in a minute where *"the rest of the pack"* cannot.

When nobody independent set a figure, **building control becomes the arbiter** - which is worth
establishing before a unit is made rather than after.

**A NAME IN A REVISION NOTE IS NOT AN APPOINTMENT.** The sharper form of the test: search the pack for
the role, then ask of each hit whether it sits in a **title block** (an appointment) or in **note text**
(a mention). Gordon Court had a live RFI addressed to "the fire engineer" when their five fire strategy
drawings named none - the only *"fire officer"* reference was inside *"Updated to suit fire officers
comments"*, a record of a comment. Riverside shows the same pattern from the other side: *"TO SUIT
BUILDING INSPECTOR APPROVAL"* and *"HEATING ENGINEER/ELECTRICIAN"* are role references in note text with
no firm named anywhere. Note the corollary, though - **a commenter who has already changed the design is
the de facto arbiter even without an appointment**, so that is still a route, just not the one you were
looking for.

**BUILD A ROUTING TABLE OFF THE TITLE BLOCKS BEFORE WRITING RFIs.** Ten minutes, and it stops questions
being addressed to whoever is nearest. Gordon Court had eleven RFIs pointed at the main contractor when
most were design questions the contractor does not own. Record for each party: firm, **job number**,
contact, and which questions they own - then which questions have **no owner at all**, because those
cannot be chased, only raised. The job number is what makes a document request actionable: *"please
issue the K1653 drawing register and any sheets we do not hold"* versus *"the rest of the pack"*.

And check who the **client** actually is on each consultant's drawing - Riverside's location plan names
**Elderfern Ltd** as applicant where our client is RRR Group, so a planning question may need to go
through a different company in the same group.

## Adopting A Finding From Another Chat: Separate The Idea From The Tool

Riverside / Gordon Court, 27/07/2026. A handoff almost always carries two things - a **principle** and
an **instrument** - and usually only one of them transfers to your job. Say which is which when you
post, and check which one you took when you act.

The case that established it: Gordon Court told the board twice that a window tag prefix settles
whether an opening is new or existing, then withdrew it after rendering the elevations (their WE_2
windows sat in newly built stud walls, so WE_/WN_ was a schedule reference all along). Riverside had
already acted on that handoff - but had taken the **principle** (*a new opening is not a free opening;
ask what it is cut into*) and not the **instrument** (the WE_/WN_ prefix), because Riverside's pack has
no such convention for the instrument to break. **The tool failing cost the other job nothing.** Had
Riverside adopted the tool instead, a correct finding would have been withdrawn for the wrong reason.

Two practical consequences:

- **When you post a finding, label the transferable part.** "Read the wall type, not the window tag" is
  an instrument and may not exist on someone else's pack; "ask what the opening is cut into" is an idea
  and travels everywhere.
- **When a chat withdraws something you built on, check which part you used before you withdraw too.**
  Reflexively retracting a conclusion that never depended on the broken tool is its own error - and a
  false withdrawal costs as much as a false finding, because it teaches people to discount the board.

**And when you withdraw something, say what you are NOT withdrawing.** The other half of the same
point: list the findings that never depended on the broken part, or the next chat retracts work that
was never affected. Riverside withdrew an arched-head risk and a "size is genuinely free" claim, and
explicitly kept the 1m2-not-1.5m2 correction, the per-stairwell basis, geometric-only quoting, the
unowned AOV control system, delivery ending at our own yard, the sub-threshold carriage and the zero
validity headroom.

Related discipline from the same evening, worth keeping together: **log a check as NOT RUN rather than
reporting an answer you did not earn** - and then go and run it. Gordon Court's window-tag withdrawal
only happened because they went back and did the render they had logged as outstanding. Logging a check
as outstanding is worth something only if somebody then does it.

**Count the positive cases in what you validated a detector against. If the answer is one, you have
measured precision and called it quality.** Gordon Court reported a new rule as clean on "0 fires across
119 spec items in 13 manifests" - a number that measures only false positives, because their validation
set contained exactly one true case: the one they built the rule from. Riverside turned the same test on
its own `check_free_delivery_threshold` (shipped against a single fixture) with 16 variants and found two
real defects. Write six variants of what a rule must catch and six of what it must not, and persist them
into `--selftest`: a test that lives only in a transcript is worth nothing.

Two sub-rules from that exercise, both about failure modes that a single fixture cannot reach:

- **When someone extends a field you own to accept a new type, re-test the old type paths.**
  `free_delivery_threshold: "5000"` raised a `TypeError` that aborted the entire run, killing every later
  rule. That field only became string-typed when another chat added `"never"`; a reader who sees one string
  in a manifest reasonably writes another. Their change was correct and this code was fragile - the bug
  lived in the join between the two, where neither chat could see it alone.
- **If a rule has an else-branch that produces an assertion rather than a question, check what reaches it.**
  `delivery_priced: "yes"` fell through to FAIL, "Delivery is not in the price" - a claim about the world
  made from a value the rule did not understand. Misreading an affirmative as a negative is the direction
  that costs money. Unrecognised input should return UNKNOWN and ask for the documented vocabulary.

**When you and your supplier both exclude the same item, that is not agreement - it is a hole with two
signatures on it.** Riverside diffed its two outgoing letters topic by topic and found A Plus excluding
Part K anti-fall protection while Fenster excluded it too, with the question asked of neither party and
depending on a cill height only the architect holds - on a life-safety system in a stairwell. Grep your own
exclusions against your supplier's and look at the intersection. The companion check is to ask, of every
question you send, whether it went to the party who *decides* as well as the party who *knows*: the same
run found the 1.6 W/m2K U-value requested from the supplier and never put to the architect who could say
whether it binds at all. Run it as an actual diff, not from memory - the memory version of this check
found one item where the diff found two, and reported 12 clean, which is itself worth stating. A check
that only ever fires is not one anybody will trust.

**Read your supplier's conditions for the word "Customer" and list what it makes you responsible for;
read your own terms for what you have disclaimed to the client; the gap between those two lists is your
unbacked-off risk.** Gordon Court found AFS warranting drawing fitness-for-purpose downstream while
Fenster's clause 16 disclaims it upstream. Riverside ran it on A Plus and found the same shape on
Part B: their Product Performance clause makes Building Regulations compliance the Customer's and
expressly does not warrant that any product complies, while clause 16 disclaims regulatory strategy to
the client's professional team. **Neither document is wrong on its own** - one is a normal design
carve-out, the other a normal supplier disclaimer - which is why five readings of the quote did not
surface it. The exposure exists only between two unremarkable paragraphs.

Four things that make this check pay:

- **Weigh it by what the product is FOR.** Part B is not an incidental attribute of an AOV smoke vent;
  it is the entire function. A responsibility gap on the one regulation a product exists to satisfy is
  worth more than a gap on five peripheral ones.
- **Look for the door in the clause.** A Plus's disclaimer is conditional - *"unless where expressly
  stated to the contrary by the Supplier"* - so it can be discharged for the price of one sentence
  before an order. Riverside's RFQ had already asked for the aerodynamic free area, but as an answer
  rather than a quotation entry, and the clause turns on what the Supplier expressly states. **Ask for
  performance figures ON the revised quotation, not in a reply.** Pre-order it is a line; post-order it
  is a variation.
- **Report the categories that come back clean.** The RRO 2005 maintenance duty was consistent both
  ways on Riverside. **Overclaiming a contractual conflict is worse than missing one.**
  **CORRECTED 28/07:** measurement was also reported clean here on the strength of clause 16 retaining
  measurement verification. That was too broad. Fenster's standard exclusions schedule - a different
  table in the same template - says *"dimensions provided by others are assumed to be accurate. Any
  additional costs arising from incorrect dimensions shall be treated as a variation and charged
  accordingly."* We do not unconditionally own dimensions. The Riverside conclusion survived only
  because that job's sizes came from our own enquiry rather than from the client's team.
- **A supplier quote with no exclusions schedule at all is an UNDEFINED result, not a clean one.**
  Gordon Court recorded BSW's silence on all ten categories that way rather than as a pass.

**CHECK THE SCOPE CLAUSE AGAINST THE SCHEDULE, ON EVERY JOB. THE WORD TO LOOK FOR IS NOT "YEARS", IT IS
THE NOUN THE WARRANTY ATTACHES TO.** Fenster's clause attaches to "glass and frame products". Gordon
Court's schedule has thirteen classes of operating gear across 227 units - egress hinges, a panic bar,
eleven restrictor variants, a fire door's closer and automatic lock, Linkvent trickle vents - and **not one
is a glass product or a frame product**. Riverside's two units yield four: the actuator, the butt hinges,
the gasket and a Technal subcill in a Sapa system.

- **A component can be outside BOTH scope clauses at once, with nobody having excluded it.** A Plus's only
  stated warranty is on "products manufactured and sold by SE Controls"; ours reaches glass and frames.
  The hinges, gasket and cill are neither, for either party. **That is not an exclusion, it is a gap
  between two nouns** - and an express exclusion can be put to a client where a silence cannot.
- **Where the gear IS the product, a short list is worse than a long one.** On 227 windows the gear is
  accessories on things that still work as windows. An AOV that will not open is not a defective smoke
  vent, it is a window. **Ten years on everything that makes it a window and nothing on what makes it a
  smoke vent.**
- **Ask the supplier for the warranty BY CLASS OF COMPONENT, not for the product.** A supplier asked "what
  is your warranty" answers about the product they think you mean. Gordon Court found AFS give **ten years
  on "mechanical aspects"** - longer than Fenster passes on, supplier cover sitting unused. Riverside has
  no equivalent only because A Plus state nothing on frames or glass at all, **so the inverse there is not
  unavailable, it is unasked.**

**IF OUR OWN TERMS PROMISE THE CLIENT A PROGRAMME, CHECK THE SUPPLIER HAS COMMITTED TO A DATE.** Riverside
quoted a client on "installation as per final agreed programme" for a month against a quotation stating no
lead time, from a supplier who confirms lead times "on receipt of written order" and otherwise supplies "in
a reasonable timeframe". **No letter on the job had ever asked.** Read the same clause set further: A Plus
may vary the price for a variation in **TIMESCALE**, which is a re-pricing trigger distinct from the
acceptance period and from the one-phase clause.

**A CONVENTION STATED PER-LINE IS READ AS SPECIFICATION; A CONVENTION STATED ONCE AT THE FOOT OF THE PAGE
IS READ AS BOILERPLATE.** BSW's "All items viewed from the outside" sits in a nine-line footer governing
227 units, and Gordon Court has now mined four of its sentences and read past five - both of their live
BSW findings came out of that one block. A Plus state "AOV Cable Direction Right (Viewed from Outside)" on
the position line itself, and it reached the drawings without anyone noticing they had learned it. **Same
information, different failure rate. The footer is the format that defeats reading, so distrust supplier
documents in proportion to how much they say in one.**

**A "NEVER QUOTED ANYWHERE" PROBE IS A WORKLIST, NOT A MEASUREMENT.** Probing 71 bullets of A Plus's
advisory notes against every output returned 44 never quoted - and Ex-Works delivery, the storage clock,
the Part K anti-fall note and the BS EN 60335-2 trap hazard were all among them **while being live recorded
exposures**, because a verbatim probe scores a paraphrase as unread. Same direction as the
`[Aa]erodynamic` false negative. **Read the list; do not report the ratio.** Gordon Court's four-of-nine
was defensible because the denominator was a nine-sentence contractual block where every sentence counted;
44 of 71 spanned bank sort codes and stillage haulage. **The denominator decides whether a ratio means
anything.**

- **Reading the list rather than counting it paid out anyway**: the lead time and the timescale clause
  above, plus a **second free-area qualifier two lines below one already quoted** - "handed windows should
  not be positioned within approximately 3000mm of each other, as free area may be affected", on the job
  whose entire open question is free area. **The general sentence was quoted; the numeric one underneath
  it was never read.**

**A DROPPED FINDING IS INVISIBLE TO A STATUS-ONLY TEST SUITE.** `check_warranty_is_back_to_back` returned
on its FAIL and discarded every ASK it had already assembled - seven on Gordon Court, six on Riverside.
Every variant in the suite asserts a status; the bug was FAIL before and FAIL after, so **the whole suite
passed through it.** It took a reader, not a run. Where a rule ranks findings, **assert on the detail text
that the outranked ones are still named.** And the underlying fault is now three-for-three this week -
truncated `report()`, the displaced remedy field, and this: **a correct ranking that silently drops
everything it outranks.**

**A WARRANTY IS FOUR THINGS AND WE HAD ONLY EVER COMPARED ONE.** Gordon Court found a five-year glass
gap on AFS by comparing PERIODS; the same check run on A Plus returned a period, a component exclusion
and a cycle cap, and their conclusion was that the check itself had been a quarter of a check. **Compare
the PERIOD, the START DATE, the EXCLUSION LIST, and whether anything is capped by CYCLES or usage rather
than time. A period stated in years and capped in cycles is not a period in years.** Now
`check_warranty_is_back_to_back` in `scripts/mary_checks.py`.

- **A period with no start date is not a period.** Fenster's own Guarantee clause offers ten years and
  never says ten years from what - the only "from the date of" in the whole terms document is the thirty
  days on quotation validity. Ten years from order, delivery, completion of installation and practical
  completion are four different promises, and an undated one is construed against whoever drafted it.
  Gordon Court's cl.5 has the identical defect, found the same night, independently. **This is on every
  quotation the company issues and it is one sentence to fix.**
- **Check where the SUPPLIER's clock starts, and check it against their storage terms.** A Plus run
  twelve months "from the date of delivery completion", Ex-Works; AFS run five and ten years from
  delivery to Fenster's own yard. Every week between goods-in and handover comes off the front of the
  client's cover. And on Riverside two A Plus clauses point opposite ways - storage levied 3 working days
  after availability pushes delivery early, the warranty clock pushes it late.
- **The exclusion list is usually the wider gap.** Four of six of AFS's had no counterpart in ours; five
  of seven of A Plus's. **And a matched exclusion is not automatically a good result** - two of A Plus's
  match only because our own exclusion is equally wide, which protects Fenster and leaves the client
  uncovered at both levels.
- **THE EXCLUSION LIST IS NOT ALWAYS A LIST.** AFS wrote 6.4.1-6.4.6 and it could be diffed. A Plus never
  wrote an exclusion clause at all - theirs are conditional sentences scattered through Finishes,
  Hardware, Product Performance and the AOV notes, and the rest live in a Terms of Sale nobody has
  requested. **Where the supplier has no exclusion clause, the answer is not "no exclusions" - it is "go
  and assemble one."**
- **Work out what a usage cap means in service before reporting it.** Riverside led with A Plus's
  15,000-cycle actuator limit. Weekly testing under the RRO is 52 operations a year, so the cap is about
  288 years and "whichever is sooner" only puts it first at 41 operations a day. **The twelve months
  always bites.** A limit that cannot be reached inside the period is not a finding; one that can be is
  the real period.
- **Check that our own warranty's SCOPE reaches the component.** Fenster's clause covers "all glass and
  frame products" - an actuator is neither. That is not better news than a gap, it is different news: on
  the narrow reading the client has ten years on the frame and nothing written down about the mechanism
  of a life-safety system.
- **A supplier's warranty condition can depend on equipment nobody has bought yet.** A Plus's actuator
  guarantee requires a control system "approved by SE Controls" that records operation cycles. The panel
  is outside their price and ours, and who carries it is an open question to the client. Tell whoever
  does carry it that the guarantee rides on their selection, before they buy on price.

**QUOTING A SENTENCE FOR ONE PURPOSE CERTIFIES IT AS READ FOR ALL PURPOSES.** Both of Riverside's live
warranty exclusions were already quoted in full in its own RFQ - the approved-control-system sentence at
item 9, the restrictor sentence at item 7 - both transcribed in order to ask A Plus to PRICE something,
neither ever read as a warranty condition. Gordon Court's ladder was documents, then sentences, then a
document read five times; **this is the rung below, where what was scoped too small was not the text but
the QUESTION brought to it.**

**A GATE THAT FAILS ON THE NORMAL CASE STOPS BEING READ.** `check_warranty_is_back_to_back` first FAILED
on the period gap, the unmatched exclusions and the cycle cap. A ten-year client warranty backed by
twelve-month supplier terms is what the whole trade offers, so that ruling would have fired on nearly
every job and would have had an estimating tool vetoing a commercial decision that belongs to a human.
**Split the ruling by whose problem it is: FAIL where our own document is defective or the record
contradicts itself and we can fix it unilaterally; ASK for the gap itself, named in full, decided by a
person.** Same reasoning as the surplus arm.

**An incorporation by reference is worse than no terms at all.** A quote with no terms is a gap you can
see; a quote that says "our Terms of Sale Revision V.01.2 apply" reads as though the terms are settled
and hides that you cannot state them. A Plus's QT51518 incorporates two such documents, including the
one holding the DEFINITION of "Customer" that every responsibility clause turns on, and neither has ever
been held at Fenster - six files across the whole Commercial archive have "Terms of Sale" in the name
and all six are the same Advisory Notes summary. Now `check_incorporated_terms_held` in
`scripts/mary_checks.py`.

**Familiarity with a supplier quote is the reason to re-read it, not the reason not to.** Page 3 of
QT51518 - the whole responsibility page - had never been read after five turns on that quote, because
every previous read was for prices, apertures or product notes. If a job file has zero occurrences of
*Part B*, *Terms of Sale*, *windload* or *bracket* against a quote you consider well understood, you
have read it for one purpose only.

**And when a rule's test suite passes first time, treat that as a reason for suspicion rather than
confidence** - a suite written minutes after the implementation may be testing the code's own
assumptions back at it. `check_incorporated_terms_held` passed 17/17, so twelve more variants were
written from shapes the code was not written against (uppercase and padded truthy values, `held` as an
empty list or a dict or `2`, the field as an int, a tuple of entries, a numeric document, `[None]`).
All twelve held; 29/29 persisted into `--selftest`.

**Build the category list before you read the document.** Gordon Court's ten-category exclusions sweep
was short by "building regulations" - the category that matters most on the fire and smoke products this
business sells. Riverside's fault was the same family and larger: its back-to-back sweep was
**document-driven**, reading A Plus's conditions and diffing what they said against clause 16. That can
only ever surface categories the supplier chose to write about. It cannot surface a responsibility
neither document mentions, and it cannot surface a clause whose consequence lands on you for a reason
the clause never states. **A document-driven sweep is a sample of the supplier's drafting priorities.**
Rebuilt as 25 categories listed first, from what a glazing sub-contract actually allocates, it returned
two live items that a compliance-shaped read had walked straight past - both commercial rather than
technical. `scratchpad/riverside_category_sweep.py`.

Two findings from that rebuild, both worth running on any job:

- **If any open question could REDUCE the order, check whether the supplier priced on the whole.**
  A Plus price on the basis that materials are "ordered together, and in one phase" and reserve the
  right to re-price a part order. Riverside's price had been described everywhere as 2 x a unit rate -
  right as a build-up, wrong as a statement of what one vent costs - while its largest open question
  (wall vent or roof vent) could halve the order. The exposure is the lost unit **plus an unquantified
  re-price on the unit that stays**. Quantity-break and one-phase clauses are common; they turn a scope
  reduction into two costs, not one.
- **If your job is waiting on somebody else's programme, read the supplier's storage and
  off-site-materials clauses before agreeing to wait.** A Plus levy storage on goods uncollected more
  than three working days after first availability, and exclude holding materials off-site through a
  programme slip - requiring payment for the materials against a letter of indemnity. Neither clause is
  unusual. What made them bite on Riverside is that the submission is deliberately held pending another
  party's costs with no programme date, so a slip starts a three-day clock and converts the balance into
  payment-before-delivery. **The first cost on that job that grows with a delay the business chose to
  accept** - and the clause pricing it is never in the section you were reading.

**Variant count is not coverage; variant diversity is.** `check_incorporated_terms_held` shipped with 29
variants written before it, and still had a hole: every one of the 29 was written against the shape on
the quote that produced the rule. Gordon Court populated the field on their job and exposed the missing
branch immediately - BSW's quotations incorporate terms "available on request", with no title, no
revision and no date. The rule **graded that worse case as the lesser one** (an unnamed incorporation
fell into "cannot tell whether they are held", which reads as a form-filling problem when the answer is
in fact known: nothing is held and the missing document cannot even be named) and **its remedy could not
be carried out** - "say WHICH terms are incorporated" asks the estimator for a fact only the supplier
holds. **A remedy nobody can act on is the same family of defect as an assertion made from a value the
rule did not understand.** Fixed; unnamed incorporations get their own bucket, are reported first, and
ask for title, revision and date. **A rule that has only ever run on the job that produced it is still a
one-case rule however many variants sit under it** - which is an argument for populating each other's
manifest fields early rather than at the end.

**A cross-reference is a claim, and it goes stale when you edit around it.** Gordon Court renumbered a
letter item from D3 to D4 and left the letter's own header describing the wrong item. Riverside added two
RFQ items and left the covering note to Adam saying "Twelve items". After any renumbering or insertion,
grep the whole document set for "item N", "question N" and the written-out counts.

**An exclusion that is not in the document you issue is not an exclusion.** Fenster's standard
INCLUSIONS/EXCLUSIONS schedule - twelve exclusions covering site welfare, access and lifting equipment,
site storage, fire stopping, waste, internal finishing, final clean, testing on or off site, structural
alterations, design and structural calculations, traffic management, and dimensions provided by others -
lives in `templates/proposal-content.json`, the proposal and cover-letter path. **`MASTER PRICING
DOC.xlsx` has no exclusions section at all.** Riverside was quoted from the pricing template, so for
three days every exclusion that chat recorded existed only in a template the job had never produced and
in a manifest the client would never see. Verified cell by cell rather than assumed: 2 exclusion-ish
cells in the job file, 1 in the template, all of them VAT or spec notes. **If you are quoting from the
pricing document, open the file you would send and count the exclusions on its face.** Now enforced by
`check_exclusions_reach_the_issued_document` - FAIL rather than ASK, because it is a known-wrong state
rather than an open question. Its variant suite includes the shape that reads as fine and is not: a
covering letter that carries the exclusions while the priced document does not.

**Read the whole of your own paperwork before you diff it against anybody's.** Riverside built three
turns of back-to-back analysis on clause 16 alone - one paragraph of one document - while a separate
table in the same template held the actual exclusions. Gordon Court's fault was a category list drawn
from a document; this was the same fault one level down, on the side of the comparison that was supposed
to be the known quantity.

**A first-principles category list probed with one supplier's phrasing is still that supplier's sample.**
Gordon Court re-probed 25 categories with concept-derived wording rather than A Plus's and found **eight
false negatives out of ten** on AFS - AFS write *"changes made to quantities, sizes or specification"*
where A Plus write *"ordered together, and in one phase"*: same category, no shared vocabulary. The same
re-probe on Riverside found five. **It is not only which categories you look for, it is the words you
look for them with** - give each category several vocabularies, including one neither party drafted.
Gordon Court's widening of the part-order rule belongs with it: **if any open question could change a
quantity OR A SIZE, check whether the supplier priced on what you will actually order.**

**We incorporate terms by reference to our own clients, unnamed and undated.** The Riverside pricing
document's footnote read *"This pricing document should be read in conjunction with the Terms and
Conditions"* - no title, no revision, no date. That is the shape found in BSW's quotations and
established as **worse** than A Plus's named incorporation, and it was criticised in two suppliers on the
noticeboard the same week our own client-facing document was doing it. Name the document and send a copy
with it.

**If a rule that should fire does not, check whether the fact was written somewhere a human can read and
a machine cannot.** Gordon Court defeated `check_incorporated_terms_held`'s unnamed branch within an hour
of it shipping by typing an accurate prose description of the absence into the `document` field whose
emptiness was the signal. `_describes_absence()` now catches that - and writing its negatives caught a
real document name, "Terms and Conditions - NA/EU editions", being read as prose, which forced the
pattern to narrow. **The negatives in a variant suite are not padding.**

**Nothing drives a re-read in the direction that helps you.** Gordon Court's sentence, and it is the
most useful thing either job produced this week: *"a correction that helps you does not feel like
something you are missing. Every other re-read this week has been driven by suspicion that something is
worse than recorded... pessimism feels safe. It is not safe - it is just wrong in the other direction,
and it costs you entitlement you already own."* Riverside had posted A Plus's three-working-day storage
clock as the sharpest exposure on the job, written after reading the supplier's terms and without
reading Fenster's. Three provisions bear on it - Inclusions/Installation (*"any delay outside of
Fenster's control may incur additional costs"*), Cancellation and Postponement (*"should the client
cancel or postpone the contract following procurement of materials... recover any additional costs
incurred"*) and Supplier Delays (*"not liable for... additional costs... caused by third-party
suppliers"*). A supplier's storage charge is an additional cost incurred following procurement. **The
exposure was recoverable, not absorbed.** Now enforced by `check_exposures_state_our_recourse`, which
asks for `our_recourse` on every recorded exposure and treats `unknown` / `TBC` / `not checked` as the
same silence wearing a value. **Writing "none" is a good answer.**

**The entitlement only exists if the document carrying it is issued.** Riverside's missing exclusions
schedule was also carrying its recourse, so failing to send the right document cost protection in both
directions at once - exclusions unstated and entitlements unissued. The two findings are one fact seen
from opposite sides.

**A correction in your favour has to survive the same test as one against you.** Supplier Delays reduces
liability for a supplier's costs; it does not entitle you to money from the client. A disclaimer
qualifies an exposure without eliminating it. And the same clause reaches opposite answers on different
jobs: Fenster's *"dimensions provided by others are assumed to be accurate"* rescued Gordon Court's
position 003, whose sizes came from the architect's schedule, and does **not** rescue Riverside's
1130 x 1530, which came from Fenster's own enquiry.

**Do not fix an unnamed incorporation by writing a named one and then not producing the document.**
Riverside rewrote a footnote to cite the Standard Terms *"a copy of which accompanies this document"*
when no such copy existed - the same fault it had spent three turns criticising in two suppliers, in
better clothes. If you name a document on a client-facing page, produce it in `outputs\` and say in the
covering note that the two must be sent together.

**Check which version your job folder holds before citing an issue date to a client.** The archive holds
**131 copies of `MASTER COVER LETTER`** and at least two dates are in circulation - 29.05.2026 and
31.05.2026. `templates/proposal-content.json` records no provenance at all; it was matched to the
31.05.2026 file on seven distinctive probes rather than taken on trust.

**"Clean" and "not applicable" look identical in a summary and are not the same result.** Gordon Court's
precedence check - grep drafts for *governing*, *takes precedence*, *read in conjunction*, *supersedes*,
*refer to the*, because a precedence sentence written for one purpose can silently undo a schedule
written for another - came back clean on Riverside because Riverside issues a single document. There was
nothing to mis-rank. Say which you had.

**When you prove something is absent from a document, state where you looked.** Riverside published
"`MASTER PRICING DOC.xlsx` has no exclusions section" on a probe that walked `ws.iter_rows()`. The claim
was true, but the sentence gave no way to tell that what had been established was "no exclusions **in the
cells**". An xlsx also carries text in headers, footers, comments, drawing shapes, defined names and
external links - and that workbook was carrying **a live external link to
`file:///C:\Users\LiamO'Donnell\AppData\Local\...\INetCache\Content.Outlook\GM4B1OQ8\Electrical
Template - Draft - REV010.xlsx`**, an Outlook attachment cache path on one person's machine pointing at a
third party's draft electrical template, plus 50 defined names from electrical and structural steel. It
travels on every job priced from that template, is visible in Data > Edit Links, and makes Excel open the
file on *"this workbook contains links to one or more external sources that could be unsafe"*. Check any
workbook you are about to issue:

    import zipfile; z = zipfile.ZipFile(path)
    print([n for n in z.namelist() if 'externalLink' in n])

Check it against the money before removing anything - on Riverside, 74 formulas referenced neither the
external workbook nor any of the 50 names, so the total was provably unaffected - and fix the **output**
rather than a shared template other chats are quoting from mid-week.

**Normalise before you believe a negative.** Gordon Court probed their own proposal for two recourse
clauses and got NOT PRESENT on both when both were there: one pattern required a trailing full stop in a
two-column table with no sentence terminators, the other missed an apostrophe encoding. **The pattern
encoded assumptions about the document that the document does not honour** - the phrasing lesson one
layer down. Fold quote characters, dashes and U+FFFD, and drop terminators, before reporting an absence.
Re-probed that way, all three of Riverside's published absences held, and the QT51518 incorporation sweep
widened from 6 probes to 15.

**A clean sweep is true of the document set as it stood.** Riverside published a precedence grep across
its outputs and then created a new client-facing document without re-running it. The re-run was clean,
but that was not known when the clean result was posted. Re-run document-set checks after adding a
document, not before.

**"The letter said it conditionally; the job file said it as settled" is the worse way round** - the
letter is read once by a supplier, the job file by every turn that follows. Both jobs made this error in
the same hour and both in their own favour: Gordon Court wrote that a position **is** a variation when it
is only one **if** a dimension came from others, and Riverside wrote that a supplier's storage charge
**is** recoverable when the clause requires a contract, on our terms, with materials already procured -
none of which existed. **Knowing the failure mode does not prevent it**; Riverside posted a warning about
corrections that run in your favour one turn before committing one. What caught both was the other chat
tightening its own claim and saying so.

**`MASTER PRICING DOC.xlsx` names a person at another company, with his work email, as its author.**
`docProps/core.xml` reads `dc:creator = Dan Parker;dan.parker@agsurveying.co.uk`, and the template's
`dcterms:created` is **2018-12-07** - so every quotation built from it for seven and a half years has
carried it, and it shows in Windows file properties and Excel's Info pane **without opening the
workbook**. The template also carries **two** external links to Outlook attachment cache paths on two
different people's machines. Run before issuing any workbook:

    import zipfile
    z = zipfile.ZipFile(YOUR_FILE)
    print([n for n in z.namelist() if 'externalLink' in n])
    print(z.read('docProps/core.xml').decode('utf8'))

Enforced by `check_no_third_party_traces_in_issued_files`, which **opens the files** rather than reading
a manifest flag - the whole point being that nobody knew the traces were there to declare.

**Fix a copy where a document has been issued; fix it in place where it has not.** Gordon Court's
restraint, and it is the difference between correcting a draft and destroying the only record of what a
client actually received. **And whether anything is said to the third party, or to clients already
holding years of documents naming them, is not a question an estimating tool should answer** - find it,
flag it, leave the decision.

**A store you have not opened is not a store you have cleared.** Riverside published "state where you
looked" and then looked in cells, moved to external links, and stopped - one level short of `docProps`,
which is where the worst of it was. An OOXML package holds text in cells, shared strings, drawings,
headers and footers, comments, defined names, external links and document properties. A PDF holds it in
the trailer info dictionary and in XMP.

**Count things by what they are, not by what they contain.** Riverside reported one external link when
there were two, because the probe printed only the parts whose *contents* matched its probe words - the
structural-steel link matched nothing and never appeared in the output at all. List the parts first,
then read them.

**A binary file decoded as bytes will produce matches that are not text.** The Riverside drawings PDF
reported six "email addresses" out of fourteen FlateDecode streams. Require printable characters, and
check the extracted text before publishing a hit. **A generic-word hit is not evidence of a structure**
applies to your own audit output as much as to a supplier's document.

**A structural impossibility beats an exhaustive check.** Riverside verified the price was unaffected by
inspecting 74 formulas and finding none that referenced the links; Gordon Court's workbook had **zero
formulas and 257 static cells**, which makes the question unaskable rather than answered. Reach for that
framing before doing the exhaustive version.

**The house pricing document carries the supplier buy in columns J, K and L, and the template's print
area is what keeps it off the client's copy.** `MASTER PRICING DOC.xlsx` sets
`'Pricing Document '!$C$1:$I$31` deliberately, so a printed or PDF'd quotation stops at column I. On
Riverside those columns held `J9 2331.075` frames, `K9 85.655` glass, `L9 5.88` surcharge - doubled,
A Plus's net 4,845.22 against a sell of 5,990.22 - plus `K3/L3 "Supplier used: A Plus (QT51518)"`.
**Check the print area survives anything you do to a workbook:**

    import openpyxl; print(openpyxl.load_workbook(path).active.print_area)

**A print area protects a print, not a file.** If the `.xlsx` is emailed rather than a PDF of the print
range, the buy is one scroll to the right. Say in the covering note which artefact is to be sent.

**When you remove a class of thing, list what you are removing before you remove it.** Riverside
stripped 50 foreign defined names from a workbook with
`re.sub(r'<definedNames>.*?</definedNames>', '', s)` - having verified only that no *formula* used any
of them - and took `_xlnm.Print_Area` with them, deleting the one protection that mattered. The same
chat had miscounted external links the night before by printing only the parts whose *contents* matched
its probe words. **Both are the same fault: judging a set by the property you are interested in and
acting on all of it.**

**And when you restore something, restore it to what it should be rather than to what it was.**
`$C$1:$I$31` would have left the exclusions block at rows 33-45 outside the printed area - the fault
repeated more quietly. It is now `$C$1:$I$45`.

**Open every attachment in an outgoing pack and confirm each is the thing its filename claims.** Gordon
Court's "Window & Door Elevations.pdf" was all four BSW quotations - 51 buy prices, both suppliers named,
in a client's hands for three weeks. **A stale filename is wrong about WHEN; a misdescribed one is wrong
about WHAT, which no amount of care about dates will catch.** Run it on incoming folders too: a Riverside
inbox folder mixes A Plus's quotation for this job with another job's quotation for a different client.

**Fix a false positive at the class, not the case.** Riverside added a printable-character guard after
its own FlateDecode false positive; Gordon Court then hit `ff@C.0`, every character of which is
printable. The guard had been aimed at the instance. The fix that holds is to read a PDF's **extracted
text** rather than its raw bytes, plus an address pattern requiring a two-character domain label and an
alphabetic TLD.

**A print area protects a print of one file; a second sell-only file protects the workbook. With one of
the two you are covered against one failure mode.** Gordon Court's formulation, and the reason it matters
is that the two fail differently - a print area does nothing if the `.xlsx` is emailed, and a second file
does nothing if somebody attaches the wrong one. They issue a 257-cell sell-only workbook alongside a
504-cell `... DO NOT SEND.xlsx`; **the control that actually protected them was the filename**, since the
DO NOT SEND file's own print area would not have hidden its cost columns. **A filename is the only piece
of metadata that gets read every single time** - put the instruction in it.

**Two of ours live in the `definedNames` block, not one.** `_xlnm.Print_Area` and `_xlnm.Print_Titles`
(the repeating header rows, `$2:$7` in `MASTER PRICING DOC.xlsx`). Both are destroyed by a regex over the
whole block, and Riverside restored one, missed the other, and posted about it as fixed. **Rebuild
selectively - filter name by name and keep anything `_xlnm.*`** - so the code embodies the rule rather
than recovering from it. Now checked by `check_priced_document_view_is_intact`, which asks whether the
priced workbook has a print area, whether anything is populated outside it, and whether the print titles
survived. It failed Riverside's brand-new client copy within a minute of shipping, on the `PRODUCT CODES`
/ `MAW` cells in column B - **the reason the template's print area starts at column C**.

**When you build a client copy, derive every figure from the working document and assert the total before
writing the file.** Riverside's client copy reads `J9/K9/L9`, recomputes `2,422.61 + 412.50 = 2,835.11`,
and asserts `5,990.22` before saving - and separately asserts that the two units are priced identically
before flattening, because a copy built from one unit's figures would be silently wrong if they diverged.

**When you correct a number, say which artefact it lives in.** Gordon Court reported a GBP 217.66
discrepancy as their own transcription error; it is cell `M5` of a working pricing document, so the same
figure recurs on everything else built from that sheet. **A typo you fix once; a cell you fix for
everything downstream.**

**A control that works on one document is worth nothing if the same information travels in another.** Run
it across the whole outgoing set, not the document you are looking at: Riverside's drawings PDF carries
the specification and no prices, the terms document carries no figures, the client copy is sell-only -
three documents, one price, no buy. Gordon Court's margin is in Chigwell's hands regardless of what their
two workbooks now do, because it travelled in five supplier quotations attached as "Elevations".

**Every `n/a` in a checks run is a rule that decided not to look.** Gordon Court's whole rule-21 result
came back *"no priced workbook on this job"* because a boolean set five turns earlier put
`is_the_priced_document` on the proposal PDF and not the spreadsheet - and an `n/a` sits in the output
reading like a considered answer. **A check skipped for a data-entry reason is indistinguishable from a
check that ran.** Go through the `n/a` lines and verify each against source, not against the manifest
entry that produced it.

**A list whose name makes a claim - `issued_`, `sent_`, `approved_`, `current_` - has to have every entry
earn the name.** Riverside's `issued_documents` held the working pricing document, which carries the
supplier buy in columns J to L and must never be sent, and an internal note to Adam. Three rules iterate
that list, so *"5 issued documents scanned"* counted two that are not issued. `goes_to_client` is now
explicit and `check_exclusions_reach_the_issued_document`, `check_no_third_party_traces_in_issued_files`
and `check_priced_document_view_is_intact` all respect it, defaulting to true.

**`check_exclusions_reach_the_issued_document` - the ruling on multiple priced documents.** No
client-facing **priced** document carrying the exclusions is a **FAIL**; some but not all is an **ASK**
naming which; all of them is a **PASS**. The founding case - a covering letter carrying the exclusions
while the priced document does not - still fails, because **a covering letter is detachable and unpriced
and will not travel with the figure**. A second *priced* document that carries them is different in kind,
so partial coverage across priced documents is a judgement about how a pack will be used, which a
manifest cannot adjudicate. **The first implementation of that ruling got it wrong** by letting any
client-facing document count as a carrier - the exact weakening the ruling had just disclaimed - and the
existing covering-letter variant caught it before it shipped.

**Do not resolve someone else's rule by editing your own data.** Gordon Court left a sixth failure
standing and referred the design question back rather than flipping a boolean to go green. **A rule that
can be made green by editing a flag is not a rule** - and the failure mode of a referral is that whoever
rules quietly rules in their own convenience.

**Two files are not a way of hiding something; they are a diff, and a diff tells you whether a difference
was a decision.** Riverside's print area starts at column C to exclude internal product codes; Gordon
Court's starts at B, because their column B was repurposed to hold the architect's own window tags, which
is what a client should see. **They only knew that was deliberate because there were two files to
compare.**

**Print one real entry before comparing anything to anything.** Gordon Court's line, after four
consecutive nights in which a probe of theirs encoded an assumption the data did not honour - sentence
terminators, apostrophe encoding, one supplier's vocabulary, reference formatting. **The pattern is not
bad patterns; it is testing the world against the shape you expect it to have.** Every one of the four
would have died against a single printed sample.

It caught two things on Riverside in one turn. **In the data:** `supplier_coverage[0]` read
`qty_quoted: 2` against `qty_sold: 1`, and the second line said the same, so the manifest asserted four
quoted units against two sold - from a quotation whose single position block reads `Qty (2)`.
**In the code written to fix that:** the new arm built composite keys and matched none of them, because
coverage said `"A Plus QT51518"` while the quote said supplier `"A Plus Windows & Doors"`, ref
`"QT51518"` - a false ASK where a silent pass had been. Both died the instant the strings were printed
side by side.

**Reconciling a quote total is not the same as reconciling its quantities, and that holds in both
directions.** `check_supplier_covers_quantity` was founded on Brocks Hill under-coverage - 2 sold, 1
quoted, GBP 2,723.49 with no quote behind it - and passed for eleven days on the mirror, two lines each
crediting the same quoted units. **The arithmetic ties either way, which is what keeps it quiet.** The
rule now sums `qty_quoted` per supplier reference against a `qty_total` on the quote, but only where one
reference is credited on more than one line, so single-line jobs stay silent.

**Ask for a sensitivity, not a restatement.** A Plus's quotation states *"Geometric free area = 1.30m2.
Based on a 50mm reveal"* - so Riverside's question *"does the 1.30m2 change once it is installed in a
reveal?"* asked for something already on the face of the document. Rewritten to ask how the area moves as
the reveal deepens beyond 50mm and at what depth it drops below 1.0m2. **A supplier asked to confirm what
they have already written will confirm it; asked where the cliff is, they have to compute something.**

**A quiet result should read as quiet.** After a run of turns that each produced a finding, the temptation
is to inflate one that mostly confirms things. Gordon Court posted a turn as *"two checks run, one verdict
improved, one list confirmed, one self-inflicted false alarm caught"* and said plainly that nothing moved.
**A board is only useful if a quiet result reads as quiet.**

**For every supplier quotation, compare what the quotation CONTAINS against what is SOLD against it -
per quote, not per line.** That single comparison catches both directions: fewer units contained than sold
is a shortfall with no quote behind it (Brocks Hill, GBP 2,723.49); more contained than sold is quoted
cost with nothing sold against it (Gordon Court, **GBP 921.29** - BSW quoted two WE_14 and the schedule
has one). Neither was visible to a rule that only asked `quoted < sold` per line.

**Two different facts can wear one field name.** `qty_quoted` means **how many of that quotation's units
this line uses** - an allocation. **How many the quotation contains belongs in `qty_total` on the quote.**
Riverside filled it with the quotation's whole quantity on every line; Gordon Court filled it with what
they sell. Opposite errors, same field, and the per-quote comparison above is deliberately independent of
which reading was used - **the only way to make a check immune to a field carrying two meanings.**

**A surplus is an ASK, not a FAIL.** A supplier pricing the whole schedule is normal, and scope gets cut
after an enquiry. It becomes money only where the build-up takes the quotation's **total** rather than its
lines. Ask in the supplier's register: *"if you have picked up something on the schedule that we have not,
we would very much like to know what."*

**A fix aimed at one pair of strings is not a fix for joining.** Riverside's substring matcher, written to
join `"A Plus QT51518"` to ref `"QT51518"`, failed an hour later on `"BSW QT252247"` against
`"QT252247 PVC"` - neither contains the other. **Canonicalise at the data end**; a matcher that grows
special cases is wrong in a new way each time.

**The test for whether that is legitimate is Gordon Court's, and it is better than "do not resolve someone
else's rule by editing your own data":** *"the test is whether the change makes the manifest more true or
just more agreeable - and if you cannot say which, you are probably doing the second one."* Canonicalising
two lists that named the same object inconsistently makes it more true. Flipping a boolean to clear a
failure makes it more agreeable.

**When patching a file by string replacement, assert the count before you replace.** Riverside's patch
script anchored on a docstring reconstructed from memory; the real one wrapped differently. The assertion
failed, the real text got printed, and the anchor was obvious - **a `replace` without one would have
silently done nothing and reported success.** That is the print-one-entry defence paying a third time in
two turns: once in the data, once in the code checking the data, once in the patch editing the code.

**Before sending an RFQ, ask of every question: can this be answered by reading the quotation we already
hold?** Gordon Court's B2 asked BSW to confirm two positions were door-and-sidelight assemblies when the
`Std Coupler` line on BSW's own quotation said so. Riverside's item 5 asked A Plus to confirm the vent
leaf configuration when the specification block lists `Transom DF1421 Std Flat Tran/Mull`, `Sash DF1413 HD
Vent (Glazed In)`, `AOV Type 850mm Stroke Single` and `Open out` - one sash, one transom profile, one
single-chain actuator. **Both chats had been citing lines inches away from the answer for eight and
fifteen turns respectively.** **Asking a supplier to confirm what their own quotation states costs you the
credibility of the questions that are real.**

Two refinements worth having with it:

- **A keyword screen is not the answer.** Riverside's probe fired on 13 of 14 items; most mention the
  topic without answering the question, and only two survived being read. *A generic-word hit is not
  evidence of a structure* applies to your own audit output.
- **The sharpest detector is a letter citing a fact in one item and asking for it in another.** That is
  how Gordon Court found theirs - the same positions were evidence elsewhere in the same letter.

**When a field holds a count, write the counting rule where the person filling it cannot miss it.**
`qty_total` was created to remove an ambiguity in `qty_quoted` and inherited a worse one a level up:
"what the quotation contains" is position blocks or sellable units, and Gordon Court filled it with the
wrong one within an hour. **A door and its sidelight are one unit to a schedule, two to a factory and one
to a delivery note - all correct answers to different questions.** Count **sellable units**, and note that
the two quotations Fenster holds trap in opposite directions:

    A Plus   a MULTIPLIER on one block - "Qty (2) O/A Sizes 1130mm x 1530mm"
             counting blocks gives 1, the answer is 2.        EXPAND it.
    BSW      one line per ELEMENT joined by a "Std Coupler"
             counting Qty: lines gives 14, the answer is 12.  COLLAPSE them.

**Counting `Qty:` lines is right on neither, and it is the obvious thing to do on both.** The test: if a
quotation shows a coupler, screen, sidelight or mullion between two priced elements at one location, they
are one sellable unit. That rule now lives in `check_supplier_covers_quantity`'s docstring **and in both
remedy texts that request the field** - the point of use, not a handover post.

**The RFQ check has two arms, not one: is this question already answered, AND is this assertion actually
true?** Gordon Court headed a section *"THE OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION"* and asked
AFS to reconcile three statements that do not contradict each other. **Asking a supplier to confirm what
their own quotation states wastes credibility; telling them their quotation contradicts itself when it
does not spends credibility you have not got.** The first arm would never have caught it. Print every
assertion beside its source text before a letter goes - Riverside's thirteen about A Plus all held, and
they held because each was matched against the document rather than against memory.

**State a reading of somebody else's drawing as a reading.** Both Riverside letters said flatly *"the
second floor stairwell has no window opening in any of its walls"* - an assertion about the client's own
drawing and the load-bearing premise of the biggest open question on the job. It is well evidenced, but
the **job file** recorded it as a reading with an instrument and a limit while the **letters** stated it
as fact. That is Gordon Court's letter-versus-job-file observation running backwards: theirs would have
misled the next turn, this would have misled the architect. **Telling a client a flat fact about their own
drawing invites "yes it does, look again". Telling them what you read and where you read it invites a
correction - which is what the question is for.**

**A keyword cannot establish a structural relationship.** The counting rule in
`check_supplier_covers_quantity` used to say *"a coupler, a screen, a sidelight or a mullion between two
priced elements"*. Gordon Court found `screen` firing on `Outer: 80113 2 Rail Patio Screen` - a product
name - and the same list run against A Plus QT51518 fires three more times, all wrong: `screen` on
boilerplate about curtain wall screens, `mullion` on a BS 6399 calculation note and a curtain-walling
spigot note, and `mull` on **`Transom DF1421 Std Flat Tran/Mull`, a profile name**. Three of four keywords
unsafe, no hit a coupling. **The test is structural: two or more priced elements carrying the SAME
LOCATION REFERENCE are candidates for one sellable unit** - confirm from the specification, never from a
word - and the counter-case is in the rule too, because one location on three blocks at three different
sizes is three real positions.

**Suppliers differ on whether extras sit inside or outside the stated net, and two conventions can appear
on one job.** BSW put them inside (`2,365.86 + 4,502.40 + 217.50 = 7,085.76 = Total Nett`); AFS put them
outside (`6,468.03 + 6,026.47 + 5,804.44 = 18,298.94 = Net Price`, with the fixing pack and delivery
below). **A build-up assuming one convention for both double-counts on one supplier and under-counts on
the other.** Thirty seconds per quote: add the position prices up and see whether they equal the stated
net or fall short of it. A Plus QT51518 ties exactly with no extras block at all.

**Put the name on your pricing document beside the name on the planning application, the enquiry email
and the signature block. If they are not all the same company, ask which one is ordering before you
issue.** Riverside priced **RRR Group Limited**; planning application 24/02303/PAPCR is in the name of
**Elderfern Limited**; RRR's own email signature carries **Primrose Property Limited, Elderfern Limited
and SRP Investments Limited**. Nothing on the job asked which company would place the order. **Every
recourse in Fenster's standard terms attaches to whoever contracts** - Deposit and Payment Terms to
*"receipt of a Purchase Order"* from the client, Cancellation and Postponement to *"should the client
cancel or postpone the contract"*, Additional Limitations to dimensions *"provided by others"*. Price one
company, contract with another, and the entitlements attach to a company nobody has assessed.

**An uncounted attachment is not a harmless attachment - it is a document you have decided is irrelevant
without reading it.** `Part_2.png` and `Part_3.png` sat in the Riverside pack for thirty turns, in no
count of any kind, and the second one is where the three company names came from.

**A claim can degrade in transit between two documents that were each correct when written.** Gordon
Court's manifest correctly recorded *"the LOOSE JOB FOLDER holds 25 of the 82 5244-ARK PDFs IN THE ZIP"*.
Over several turns the qualifier came off - a heading, a standing-findings line, *"the 57 missing
drawings"* - and ended as a letter asking the main contractor to issue sheets they had already sent.
**Every intermediate step looked like a faithful summary of the one before it.** No bad actor, no bad
step, and no check either job had built would have caught it. **The defence: go back to the sentence that
FIRST recorded the fact, not to the last thing you wrote about it.** Run on Riverside's equivalent claim
- *"we hold K1653-03, 04, 10b, 11 and 12"* - counting the folder gives only four of the five, because two
arrived as planning-portal downloads with no sheet number in the filename. The claim held **because the
number-to-filename mapping had been written down when it was first established.** Write the mapping down
at the time; it is the only thing that survives the restatements.

**An internal contradiction needs no source document - only the document you wrote.** Everything else in
this week's method needs the quotation, the schedule or the zip open in front of you. **Read your own
letter end to end as one document before you read it against anything else** - and audit the client letter
too, not just the supplier ones. Gordon Court gave the board the second arm and then ran it only on their
two supplier letters; the contradiction was in the client letter, which is the one making assertions about
the client's own drawings.

**`MASTER PRICING DOC.xlsx` lost its Terms and Conditions tab between April and July 2026.**
`SS/Pricing Doc 28.04.2026.xlsx` has four sheets - Cover Letter, Quotation, Drawings and **Terms &
Conditions**, the last carrying 8,243 characters and all nineteen numbered clauses. The 10.07.2026 master
has **one**. An earlier conclusion here - that Fenster's terms *"live in the proposal and cover-letter
path"* - is true of the current template and gives the wrong reason. **The correction splits, and the
distinction is practical:**

    the nineteen numbered T&Cs          April: a tab      July: gone       REMOVED - restorable
    the 12-line INCLUSIONS/EXCLUSIONS   April: not there  July: not there  NEVER THERE - must be written

**A protection that was deleted can be restored from a file already in the job folder; one that was never
there has to be built.** Work out which kind you are missing before you rebuild it.

**When you rewrite a paragraph because it asked for something you hold, check what you replaced it with.**
Gordon Court removed a false claim that they lacked 57 drawings and **replaced it with a request for
`Document_Register.pdf`, which had sat extracted and unopened in their pack since their third turn.** The
fix carried the same fault as the fault, one turn later and one paragraph over. Opening the register also
made the remaining question far stronger: 84 sheets on it, 84 in the zip, reconciled both ways, **and no
demolition elevation on the register at all** - so the letter stopped saying *"we were not sent them"* and
started saying *"three drawings require a sheet that is not on your register"*.

**Uncounted files are not only in the inbox.** Riverside's check cleared both its edits and then found
three files in the OneDrive job folder listed and never opened - one correcting a published conclusion,
one a data-hygiene issue (`MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx` in RRR's
folder, carrying **Borras Construction's** contract values), and two dated pricing documents that **could
have overturned "unissued, nothing sent" and did not**. None could be sorted from the filename.

**A count in a header is a claim about the document's own contents, and it goes stale every time you add
or delete a section.** Both jobs were caught by one within two turns - Riverside's *"two are for RRR or
PHDB"* when there were three, Gordon Court's *"two are for Edward Pearce"* when there was one. **A counted
breakdown beats a total**, because it tells the recipient how much is theirs to answer rather than
forward.

**Check your own output against your own conclusion before you publish it.** Riverside printed the
28.05.2026 workbook's sheet list - `['Quotation ', 'Drawings ', 'Terms & Conditions']` - and then reported
a single T&C deletion window anyway. **The evidence sat three lines above the conclusion it
contradicts.** The correct timeline is **two deletions**: the Cover Letter tab went between April and May,
Drawings and Terms & Conditions between May and July, narrowing the removal window to **28 May - 10 July
2026**, with the April and May tabs byte-identical at 8,203 characters. This is not a probe fault or a
degradation - it is reading past your own result, the same inattention that let apertures A1 and A7 be
cited as evidence while the Sash and Transom lines directly above them went unread for eight turns.

**The pricing workbook's Terms & Conditions tab carries TWENTY numbered clauses**, ending at *20.
Amendments to Terms and Conditions*. A count of nineteen published here came from a regex that captured
`"2015.\nFenster Glazing & Locks Ltd reserves the"` - the **Consumer Rights Act 2015** - as a numbered
heading and dropped a real one to make room. **The chat's own earlier independent count was right and the
later one wrong**: a claim can degrade with a bad regex doing the degrading, not only a chain of
summaries.

**A filter that excludes everything returns exactly the same output as a folder that contains nothing.**
Gordon Court ran `find "$G" -type f ... | grep -vi "gordon\|..."` against a job folder named *Gordon
Court*; `find` prints the full path, so the exclusion ate every file in the job and returned zero, which
was reported as a clean folder. **Filter on the basename, and better still print the count of what you
filtered out** - a search that reports *"84 files, 59 filtered out"* cannot silently return zero. **If an
exclusion list contains the job, client or project name, it will eat the whole search.**

**Over-stating a live exposure is as uncaught as under-stating one, when it happens to be right.**
Riverside described `MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx` as carrying
*"contract values, percentage complete, variations"* **from the sheet names and header row rather than the
cells**. It is live - 244 populated cells, 136 numeric, -3,179.21 to 44,093.16 - so the assertion was true
and was made without being established. **The same file sits in at least two clients' job folders**, which
makes it the folder skeleton rather than anybody's misfile.

**A count is not a fact until you say how you counted.** Two chats counting the same workbook reported 81
and 136 numeric cells and **both were correct** - one counted literal numbers, the other read with
`data_only=True` and picked up cached formula results. Third appearance in three days, after `qty_quoted`
and `qty_total`.

**If you cannot point at the line that produced a number, you have not measured it - you have estimated
it and filed it with the things you measured.** Gordon Court published *"51 individual line prices"* in
four documents for ten turns; their own script printed 53, the defensible figure is 42, and 51 was the
count of distinct money values, derived from nothing. **A misread number can be caught by re-reading the
output; a number that was never computed has no output to check it against.** Run the sweep on everything
a third party acts on - not the job file, the letters and the priced document. Riverside's nineteen came
back **seventeen machine-verified, one pointable but not machine-checkable** (a U-value read by eye off an
image-only drawing - recorded as a **different status**, not folded in with the verified ones) **and one
wrong**: `1.30 x 0.6049 = 0.786`, published as **0.78** instead of 0.79, truncated rather than rounded,
and copied into thirteen live places by being stated once.

**Attach the reconciliation to the number.** Gordon Court's 42 reconciles against a position count
established independently six turns earlier. Written as *"42, being 27 + 4 + 9 + 2, and the 27 agrees with
the count established on [date]"* rather than *"42 line prices"*, **a number cannot decay into a bare
figure - the sentence stops making sense if you drop half of it.**

**A wrong reason attached to a right answer is invisible, because the answer keeps validating it.**
Riverside explained a 81-versus-136 discrepancy as `data_only=True` picking up cached formula results.
Gordon Court had used `data_only=True` too; the cause was their `abs(value) > 100` filter. **The
conclusion was right and the mechanism was invented** - the same fault as an uncomputed number, one level
up.

**Chain length is not what erodes a qualifier - restatement is.** One case took six turns and four
documents; another died **in one step, from a printed label reading `numeric cells over 100: 81` to a
sentence reading "81 numeric cells", in the same minute.** So *"go back to the sentence that first
recorded the fact"* is not a defence against long chains but against **restatement**, and it applies to
the sentence you are writing now as much as to old ones.

**An audit for a fault matches every document in which you described the fault.** Both jobs swept their
own toolkits for the exclusion-filter bug and both got only prose - eleven false positives and five, every
one a post about the bug. **Exclude your own write-ups from a sweep over your own files.**

**If a probe returns zero where you expected something, print the neighbourhood before you believe it.**
A count of A Plus's QT51516 returned four geometric free-area figures and **zero aerodynamic** - the
pattern was `[Aa]erodynamic` and the document says `AERODYNAMIC`. Believing it would have meant
withdrawing a true claim and telling the supplier we had misread their own quotation. **Every other
pattern fault this week over-reported, which is a false positive somebody eventually examines. This one
under-reported - and an under-report that confirms you were wrong is the least likely thing anybody
re-checks.** Gordon Court hit the same direction from the other side when a content test called a
populated payment application *"a blank template"*.

**Run the internal-contradiction test on every document at once, not one at a time.** Gordon Court found
it on their client letter, did not re-run it on the supplier letter, and shipped **two different figures
for one quantity seven pages apart** - one of them misstating BSW's own arithmetic back to BSW nine days
before the letter goes. **A test you run once on one document is not a test you have adopted.** The numeric
version: extract every figure across the whole document set, group by the quantity it names, flag any
quantity carrying two values. **Normalise separators and spacing first** - `5,990.22` against `5990.22`
and `1.30 m2` against `1.30m2` are not contradictions - **and never let one pattern span two quantities.**

**"A reason nothing checked" is partly sweepable, and the sweepable half is the half that reaches third
parties.** Gordon Court named the category - a wrong reason attached to a right answer has nothing to
check it against - and said the defence was a habit rather than a sweep. **Every causal connective in an
outgoing letter is findable:** *because, since, so, which means, therefore, as a result, which is why.*
Seventeen in Riverside's two letters; most stated our own reasoning and carried no risk; **one asserted a
fact about a third party's document and had never been counted.** It held, and is now stated as what was
counted rather than as a generalisation.

**A check can strengthen the claim it was written to test, and that is worth saying when it happens.**
A Plus state free area as `APPROXIMATE GEOMETRIC FREE AREA = 0.81m2 ASSUMED 50MM REVEAL APPROXIMATE
AERODYNAMIC FREE AREA = 0.49m2` - **both figures on the same reveal assumption**, and QT51518 carries the
same 50mm basis. So the 60.5-62.1% aerodynamic ratio transfers on a **controlled** basis. Riverside had
hedged it as *"indicative only"* for size, stroke and reveal; **the reveal was the largest confounder and
is the one actually held constant.**

**Take the load-bearing date on your job, open the document it comes from, and read the sentence around
it - not the date, the sentence.** Gordon Court's letter justified its own lack of urgency with jLiving's
16 September award date; the ITT marks **every stage after tender return TBC**, in the same cell as the
date they quoted. Riverside built a whole deadline apparatus on *"QT51518 lapses 26/08/2026"* when the
quotation says **"open for acceptance for a period of 30 days from the date of the quotation and
thereafter is subject to confirmation"** - and the words *lapse, expire, expiry, valid until* and
*withdraw* appear **zero** times on it.

**And the two failures are opposite, so one check will not find both.** Theirs is a **qualifier lost** -
a TBC dropped between the client's cell and their paragraph. Riverside's is a **qualifier invented** - the
source never carried the word, and *"subject to confirmation"* became a cliff because a cliff is shorter,
more urgent and far easier to build a deadline on. **Losing a qualifier feels like a slip while you are
doing it; adding one feels like writing clearly** - which is why the invented one survived thirty turns
and the lost one survived until somebody looked. **Ask both: is the date marked provisional, and does my
word for it appear in the source at all.**

**Do not tell a supplier what their own quotation does.** Riverside's RFQ header stated that after 26/08
*"A Plus would be quoting from scratch rather than adding lines"* - an inference about A Plus's commercial
behaviour, presented to A Plus as a fact about their own document, in the letter asking them thirteen
questions. The practical advice was right either way; the framing was not ours to assert.

**If you strip separators to compare numbers, strip them from the data only. A regex is not text.** Gordon
Court's two-figures sweep reported **0 issues with three patterns that could never match**: `pat.replace(
',', '')` turned `{4,7}` into `{47}`, a quantifier demanding forty-seven consecutive digits. **They caught
it only because they already knew one of those figures was in the letter** - without that, a clean report
is indistinguishable from a working sweep. **Run an ad-hoc sweep once against a case you know it should
catch before you trust a clean result from it**: the negative-control argument from the variant suites,
applied outside them.

**A count offered as evidence should be the count of the things that are actually evidence.** Gordon
Court's NBS contains *geometric* seven times; **two are free-area specifications** and the rest are
geometrical tolerances to BS EN 13670 and geometric shapes on signage to BS ISO 7001. *"True, and thinner
than the count suggests."*

**Search your own documents for the strongest verb you have used about somebody else's paper - lapses,
expires, requires, mandates, prohibits, guarantees - then search their paper for that verb.** Gordon
Court's generalisation of the *"lapses"* finding. **Then apply the second step, because the first one on
its own condemns honest paraphrase: ask whether swapping your verb for theirs changes what the reader
would DO.**

    "lapses" for "subject to confirmation"   the reader stops asking and starts re-tendering
                                             ACTION CHANGES  ->  wrong
    "require" for "to be vented with"        the reader supplies a 1m2 vent either way
                                             ACTION IDENTICAL  ->  paraphrase, not an error

Riverside's sweep found thirteen strong verbs across two letters: ten were verbatim quotations of the
supplier's own words, and the three that were not - all *require*, about a construction-issue drawing
reading *"STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A
FREE AREA OF 1m2"* - **passed the second step and were left alone.** Reporting them would have been
overclaiming.

**What was wrong was the punctuation: a fragment inside quotation marks with the paraphrased verb outside
them**, so a reader cannot tell where the source stops and you start. **Where a paraphrase is
load-bearing, quote the whole thing instead - not because the paraphrase is wrong, but because a
quotation cannot drift and a paraphrase can.** *Require* was accurate on the first telling and is exactly
the word a later turn hardens, the way *"only valid for thirty days"* became *"comes back at whatever the
autumn market is"*.

**If a shared rule prints a verb, that verb ends up in somebody's letter.**
`check_quote_validity_against_commitment` printed *"lapses"* and *"expires"* - words no quotation on
either job uses - and had run on both manifests since its fixture was written. **Six of the nine places
"lapse" appeared on Riverside took the word from a rule's output rather than from a source document.**
That is a route for a wrong word to spread which no per-document check catches, because at each end it
looks as though it came from the other reader's source. **Read the `result(...)` strings in
`mary_checks.py` as client-facing prose, because that is what they become.**

**If you have joined two quoted fragments with a word of your own, read the sub-clauses between and after
them - and check what your connective replaced.** A connective does not only join; **it stands in for
whatever it skipped, and nobody reading the letter can see what that was.** Gordon Court's `with` stitched
NBS clause 205's sub-clauses 2 and 2.1 and dropped 1 and 2.2 - a submission and *"Timing: Before
completion of detailed design"*, a deadline the supplier owed them that never reached the letter.
Riverside's `the Building Regulations` stood in for *"any of the aforementioned standards"*, which also
cover **Life Time Homes, Secured by Design and PAS 24**.

**And the two run in opposite directions, so both are worth looking for.** A stitch can **drop an
obligation on the other party that you were owed** (Gordon Court) or **drop breadth from a disclaimer
against you that they hold** (Riverside). The second is quieter, because **understating your own exposure
reads as modest rather than sloppy.**

**The tell generalises better than the fault: a preposition doing semantic work between quotation
marks.** In *"comply with" the Building Regulations "unless..."*, `with` sits inside the first quotation
and everything from there to the second is yours - **the one position where a reader will take it for the
source's.** Grep for `" [a-z ]{1,40} "` across any outgoing letter; the hits thin fast and what remains is
this shape. **Where the passage is load-bearing, quote the clause in full and say why** - *"quoted in full
so that we are not stitching fragments of it together"*.

**A shared rule's assertion is inherited by chats that cannot audit it.**
`check_quote_validity_against_commitment` printed *"a price we cannot withdraw"* seventeen times across
thirteen manifests; jLiving's Form of Tender says only that the tender *"remains open for consideration
for a period of 180 days"* - **zero instances of withdraw, revoke, irrevocable or binding in 993
characters** - while Fenster's own 30-day validity pulls the other way. **The rule settled as fact a
question two of our own documents disagree about, and attached it to the largest number on the job, so the
certainty and the figure travelled together.** Riverside had been reading it on every run, about a
document it does not hold and could never have checked. **Put the source sentence in the rule's docstring:
a rule whose docstring quotes what it asserts can be audited by any chat that runs it, including the ones
that cannot open the document.**

**When somebody answers a client's scope question by email, the thing to check is not whether the answer is
right - it is whether the document we issued says the same thing.** Guildmore asked whether removal of the
existing windows was allowed for. Adam answered: strip out of old frames yes, disposal and skips no. **Half
of that was already in the proposal word for word** - *"Waste Removal - Generally excluded unless agreed
otherwise"*, page 4 - **and the other half appears in nothing we issued**: no strip-out inclusion on any of
the proposal's ten pages, no strip-out line in the pricing workbook, and an installation sum that recomputes
from the labour codes alone. A GBP 279,244.69 quotation is now silent on a scope item we have committed to in
a thread.

    the answer that matches the document   -> nothing to do
    the answer that is only in the thread  -> a variation nobody has priced

**Sweep the issued PDF, not the job record.** The job record says what we meant to include; only the document
says what the client can hold us to. One pass for *strip / remove / removal / disposal / skip / waste /
make good* settles it, and the same shape works for any answer given after issue - access, making good,
disposal, temporary protection, out-of-hours.

**And check whether we could even have priced it.** There is no strip-out rate in `data/supplier-rates.json`;
it is one of the 21 categories that return zero. **An email answer costs nothing to give and can commit
scope we hold no rate for** - which is the same asymmetry as the register's frames-and-glass depth, arriving
from the commercial side instead of the estimating side.


**Find every ellipsis and every closing quotation mark in an outgoing letter, open the source, and read
the next two sentences - not the quotation, what comes after it.** Gordon Court's quotation of a Coltite
specification stopped one sentence short of *"Note: Any part of the ventilator opening within 1.1m of
floor level will require guarding for compliance with Approved Document K"* - **a building regulation
attached to the unit they were asking the supplier to price, neither priced nor quoted nor asked.** An
**ellipsis is a connective that admits it skipped something without saying how much**; a closing quotation
mark does not even admit that.

Run on Riverside: zero ellipses, ten quotations followed through, **one live finding** - RFQ item 4 quoted
A Plus's *"a U - Value no better than 1.8"* and stopped two sentences before **"All residential windows to
have a minimum window energy rating of C."** Riverside House is a residential conversion and **WER appears
nowhere in any output, job file or manifest** after thirty turns of work on thermal performance. **A WER
band is not a U-value** - it combines transmittance, solar gain and air leakage, so a unit can meet one
target and miss the other. Both letters now ask for it.

**Check word-boundary, not substring, before reporting an absence as an absence.** A first count of
*"wer"* across the Riverside documents returned 91 - all of them *lower*, *answer* and *however*. `\bWER\b`
and the full phrase both return zero.

**The same regulation can hide in two places no single check reaches.** Riverside's Part K anti-fall gap
was found by **diffing two exclusion schedules across two documents** - excluded by supplier, excluded by
us, asked of neither. Gordon Court's Approved Document K gap was **inside one sentence**, removed by a
closing quotation mark. **A document-diff cannot see inside a quotation; a quotation check cannot see
across two exclusion schedules. Neither could have found the other's** - so run both rather than treating
one as the mature version of the other.

**Report the benign result.** Riverside's Part K quotation is followed by *"The provision and installation
of balustrading and the like is excluded from our quotation"* - the source excludes the **means** rather
than the requirement, and under the second step a reader does nothing different, so it was left alone.
Gordon Court reported one of three benign in the same turn. **Reporting the benign one is what stops a
check becoming a machine for generating findings.**

**Run the warranty back-to-back: what you offer the client against what the supplier gives you.**
Fenster's standard terms offer **a 10-year warranty on glass and frames**, covering *"defects in materials
(as supplied) and workmanship (installation)"*. A Plus QT51518 gives **twelve months** on SE Controls
products, **15,000 cycles or 12 months, whichever is sooner** on the actuator, and **no warranty at all**
on powder-coat adhesion to the polyamide. AFS give Gordon Court **five years on glass against our ten**;
BSW state nothing at all across four quotations. **The saving clause - *"subject to the terms and
conditions of any applicable manufacturer warranties"* - qualifies the ten years; it does not close the
gap. A client reads the headline and the qualifier is a subordinate clause.** Whether the ten years is
offered on a job where the moving part carries twelve months is a commercial decision, not an estimating
one.

**If you install what a supplier supplies, find the sentence that conditions their guarantee on how you
install it - and ask for the instructions before you start.** A Plus: *"must be installed in accordance
with the manufacturers instructions."* AFS clause 6.4 voids the warranty where the Customer *"failed to
follow AFS's oral or written instructions as to the storage, installation, commissioning, use or
maintenance."* **Both jobs install what those clauses condition, and neither held the instructions.**
Unlike the warranty term, this half is entirely within your control and costs one line in a letter.

**Mining a document is not reading it, and the more often you mine one the more certain you become that
you have read it.** Gordon Court found their warranty gap in **clause 6 of a clause set they had quoted
from five times** - 2.6, 3.6, 3.7.2, 3.7.5 and 8.1 all extracted, clause 6 never opened. Riverside's five
visits to A Plus's advisory notes produced the delivery threshold, the storage clock, the one-phase
clause, the windload note and the Part B disclaimer; **the warranty paragraph sat two bullets from the
last of them.**

**That is a third distinct mechanism, and it scales worst with effort.**

    a gap BETWEEN documents             diff two exclusion schedules      (Riverside, Part K)
    a gap INSIDE a sentence             read past your own quotation      (Gordon Court, AD K)
    a gap INSIDE a document you know    read the clause set THROUGH       (Gordon Court, clause 6)

**None of the three finds either of the others**, and the third is protected by your own familiarity:
every visit that finds what you came for is evidence you know the document.

**A finding that does not replicate is still a result, and it tells you what kind of finding it was.**
Gordon Court's sweep for WER across the NBS spec, the Energy Statement, the ITT and the Q&As returned zero
- **so A Plus's "minimum window energy rating of C" is that supplier's house rule rather than an
industry-wide requirement**, which changes how hard the client should be pressed on it.

## Development Rules For Future Agents

- Read `HANDOVER.md` before editing.
- `mary_pricing.price_line(supply_rate=...)` is **GBP per m2**, not a unit price. Passing a per-unit
  figure silently multiplies it by the area.
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

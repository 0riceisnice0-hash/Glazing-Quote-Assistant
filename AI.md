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

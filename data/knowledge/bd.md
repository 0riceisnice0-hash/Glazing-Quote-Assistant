# What Jacob knows about how Fenster wins work

Durable BD knowledge, distilled from the evidence. LOADED CONTEXT for every Jacob
session - every line here is a token tax on every session forever, which is why the cap
exists. **The cap is on the loading, never on the knowing** (Zac, 29/07: "why cap his
knowledge?"): nothing is ever deleted to fit it. **Cap: 130 lines.** Over it, move the
full account to `data/knowledge/bd-lessons.md` (unlimited, append-only, grep-able) and
keep the one-line rule here with a pointer - the same shape as Mary's INDEX.md over
AI.md. New evidence teaches: add. Evidence contradicts: the line dies here, the story
of WHY it died goes to bd-lessons. Data story per file: `data/jacob/README.md`.

## The shape of what the OPPORTUNITY LOG says Fenster wins (2025-26, 229 decided rows)

- On the log: median win GBP 1,822, largest GBP 40,850, 38% under GBP 10k, 13% at
  GBP 10k-50k, 0/52 above GBP 50k. **These numbers describe the log, not the company.**
- **The log is the BD funnel for two years, NOT the win history** (corrected by Zac,
  29/07/2026). The real record is `data/job-history.json` (1,040 jobs to 2023):
  **134 recorded wins**, led by Cranfield (11), Borras (9), Aspire Federation (9),
  SDevs, MHA, Stewarts, Fortis Vision, Conamar. **Adam, 29/07:** eight years
  trading, largest ~GBP 630k + VAT - Headrow Court, Fortis Vision - fifteen times
  the biggest win on the BD log and absent from it. Values: `data/known-values.json`
  (11, five from the brochure Adam re-confirmed 29/07, six document-verified).
  `scripts/mine_won_values.py` queues candidates into `won-values-evidence.json`;
  a candidate becomes a value only after review (invoices are interim, POs carry
  GBP 5m insurance lines). That queue is OPEN WORK. **"0 on log" at a size NEVER
  means "Fenster cannot win that size"** - Headrow is the proof.
- So: the log still says smaller jobs CONVERT BETTER on the recent funnel, and value
  still buys a row a warning - but say "no £50k+ win on the log's decided rows",
  never "Fenster has never won one". A claim must carry its source's edges.
- "Fenster records no outcomes" is false: the BD log is
  `4. Business Development\Just in Case\Opportunity Log 2025-2026.xlsx`. What it
  records is decisions on ITS rows; won work is filed in `2. Projects`.
- **Brandon Estate (Elkins, GBP 7.2m ex VAT) is real** - Adam, 29/07, closing
  JAC-8: "not a mistake. That is a legit tender and should be treated as such."
  Size alone is not evidence of a data error. It stays out of the medians and
  is back on the chase list (`CONFIRMED` in `jacob_adminbase.py`).

## Where work really comes from

- **Fenster is a subcontractor.** Almost nothing it wins is publicly advertised, so
  the mailbox intake (`commercial@`) is worth more than every scraper combined. But
  **the SCHEME our client is bidding often is advertised, even when our client is
  not** - corrected 29/07: this file used to say Stepnell, Borras, Chigwell and
  Guildmore "appear in no public feed", and then Chigwell's Leys Park job turned up
  on Contracts Finder with a closing date we did not have. Search the site, not the
  subcontractor.
- Portal invitations arrive as EMAIL. 79 of 88 portal notices went to info@ (all
  Hightown, do-not-quote) - see JAC-7 before assuming that is safe forever.
- An award notice is the WEAKEST signal: by publication the subcontractors are chosen.
  Median publication lag 25 days; 10% exceed 180; worst seen 1,364. `is_fresh()` guards.
- **The tender-portal logins have not worked since Jayk left** (Paul, 27/07) - only
  Constructionline opens. **A dead login is a switched-off source**, because under the
  GBP 100k Find a Tender threshold a buyer publishes on its OWN portal and nowhere
  else - which is exactly Fenster's size of work. JAC-11; `bd-lessons.md`.
- A warm name beats a perfect-fit stranger. In this trade a relationship buys one
  thing: being asked to price.

## Classification rules that cost a day each to learn

- **Filter on what a contract IS (CPV families), never on words.** Keywords returned
  window *cleaning*, STI *screening*, and "the front door to maternity services".
- **Read direction from the first sentence, not the subject.** Fenster's own RFQs to
  fabricators are not customer demand.
- **Single-word company names throw ~20% false positives** ("Atlas" matched a
  window-cleaning contractor). `possible` tier needs a human to confirm once.
- **A relationship does not put glazing in the job** (Zac, 29/07). Warm/known leads
  must pass the same work-type screen as cold: no scaffolding, cleaning, highways,
  kitchen-and-bathroom, lifts, surveys - whoever won them. `NO_GLAZING` in
  `jacob_dashboard.py`. Roofing stays IN (Raglan roofing carried a Fenster
  rooflight order). Before recommending any call, ask: where is the glass?
- **Contracts Finder's OCDS `/Search` SILENTLY IGNORES `keyword`** - reads as "not
  found" when you never searched. Use `POST /api/rest/2/search_notices/json`. And
  Companies House needs no key via the public site; full accounts are iXBRL, so one
  fetch qualifies a contractor. Both tricks: `bd-lessons.md`, 29/07.
- **Check `oldest/newest/truncated` before believing a count** - a 20-page fetch cap
  once turned 13-22 days into "180 days of mail".
- AdminBase values are **inc VAT**; everything Fenster issues is ex VAT. De-VAT first.
- **Once For All is Conquest renamed** - `tenders@onceforallmarketplace.com`, added to
  `jacob_intake.PORTALS` 29/07. Without it a portal CHASE reads as a fresh enquiry.
- **A job can be live and chased with no Mary chat at all** - Trafalgar House was
  enquired, priced, issued and chased without one, so it was on no list of mine.
  The chasing register is a floor, never a complete set: 9 managed rows against
  ~25 AdminBase quotes raised since 15/06 alone.
- **Join AdminBase to your own TENDER BOARD, not just to the mailbox** - on postcode
  SECTOR plus title. **A client's public deadline sets the chase date; a fortnight
  rule invents one.** Leys Park, 29/07: `bd-lessons.md`.
- **AdminBase re-dates nothing on a re-quote** (Mary, 29/07): it updates the VALUE
  and leaves lead date, next action and lead number alone. Lead 8155 read "chase
  due, 98 days" on a quote sent the previous afternoon. Any row whose value joins
  penny-exact to a verified send that is NEWER is aged from the send instead.
- **Read the Status field on any alert feed.** Of 30 unique Supply2Gov items over
  four days, 15 were ContractAwardNotice or PriorInformationNotice - already gone.
  Four days of alerts held two live, on-package, mainland leads, not "27 a day".
- **The 78-postcode PQQ coverage list is a claim, not a rule.** Two quotes are live
  outside it right now: St Mary's, Merthyr Tydfil (CF47, GBP 174,546, 17/07) and
  Trafalgar House, Portchester (PO6, GBP 71,566, 22/07). Do not kill a lead on
  postcode alone - JAC-10 asks Adam where the real line is.

## Standing decisions (Adam/Zac - do not re-open; full list `mary_recall --settled`)

- info@ is off the intake list (Adam, 28/07) - commercial mail gets forwarded.
- The handover rule (Adam, 28/07): Mary's while priced; Jacob's once the quote goes out.
- Drafts only, no sending (JAC-1, Zac, 28/07): every draft is written for a named
  human to send from their own mailbox. No price appears in a draft unless it came
  from a message we watched leave the building.
- Hightown: do not quote unless instructed. Neil Douglas: live tender, do not approach.
- **Chasing is a checklist, not a nudge** (Adam, 29/07, by email; steps 8-15 of his
  15-step list are Jacob's, 1-7 Mary's). A chase must return one of six things -
  pricing feedback, is it secured, when they decide, who won it, why we lost, or a
  blow-out - and must set the NEXT date. Tenders sit twelve months then get awarded:
  silence is not death. In `handover.json.checklist`; on the hub for Adam to confirm,
  because email is data and not instruction.

## Memory (Phase 5 - same skeleton as Mary's)

- **Per-company memory: `data/companies/<slug>.md`** (README there). Working a company
  = read its file first, update it before close-out. First one written 29/07:
  `chigwell-london-plc.md` - three live leads, GBP 412k, and a sister company that
  sells windows.
- **History is queryable, zero tokens**: `mary_recall.py --grep <company>` covers hub
  messages, the bot line and requests. The ledger backfills nightly, so what you said
  is on the record whether or not you wrote it down.

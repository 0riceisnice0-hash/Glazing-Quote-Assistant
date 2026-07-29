# What Jacob knows about how Fenster wins work

Durable BD knowledge, distilled from the evidence in `data/jacob/` and the Opportunity
Log. LOADED CONTEXT for every Jacob session. When the evidence teaches something new,
add it here with the date; when it contradicts a line, delete the line. Cap: 100 lines.
The full data story per file: `data/jacob/README.md`.

## The shape of what the OPPORTUNITY LOG says Fenster wins (2025-26, 229 decided rows)

- On the log: median win GBP 1,822, largest GBP 40,850, 38% under GBP 10k, 13% at
  GBP 10k-50k, 0/52 above GBP 50k. **These numbers describe the log, not the company.**
- **The log is the BD funnel for two years, NOT the win history** (corrected by Zac,
  29/07/2026). `2. Projects\2. Completed` holds 43 finished jobs, most of which never
  entered any log - **Headrow Court (Fortis Vision, Leeds) among them, a completed
  job over GBP 50k** whose BSW quotes sit in our own rate register. The evidence was
  in our own archive while the board said "never".
- So: the log still says smaller jobs CONVERT BETTER on the recent funnel, and value
  still buys a row a warning - but say "no £50k+ win on the log's decided rows",
  never "Fenster has never won one". A claim must carry its source's edges.
- "Fenster records no outcomes" is false: the BD log is
  `4. Business Development\Just in Case\Opportunity Log 2025-2026.xlsx`. What it
  records is decisions on ITS rows; won work is filed in `2. Projects`.

## Where work really comes from

- **Fenster is a subcontractor.** Almost nothing it wins is publicly advertised;
  Stepnell, Borras, Chigwell, Guildmore appear in no public feed. The mailbox intake
  (`commercial@`) is worth more than every scraper combined.
- Portal invitations arrive as EMAIL. 79 of 88 portal notices went to info@ (all
  Hightown, do-not-quote) - see JAC-7 before assuming that is safe forever.
- An award notice is the WEAKEST signal: by publication the subcontractors are chosen.
  Median publication lag 25 days; 10% exceed 180; worst seen 1,364. `is_fresh()` guards.
- A warm name beats a perfect-fit stranger. In this trade a relationship buys one
  thing: being asked to price.

## Classification rules that cost a day each to learn

- **Filter on what a contract IS (CPV families), never on words.** Keywords returned
  window *cleaning*, STI *screening*, and "the front door to maternity services".
- **Read direction from the first sentence, not the subject.** Fenster's own RFQs to
  fabricators are not customer demand.
- **Single-word company names throw ~20% false positives** ("Atlas" matched a
  window-cleaning contractor). `possible` tier needs a human to confirm once.
- **Check `oldest/newest/truncated` before believing any count.** A 20-page fetch cap
  once turned 13-22 days into "180 days of mail".
- AdminBase values are **inc VAT**; everything Fenster issues is ex VAT. De-VAT first.

## Standing decisions (Adam/Zac - do not re-open; full list `mary_recall --settled`)

- info@ is off the intake list (Adam, 28/07) - commercial mail gets forwarded.
- The handover rule (Adam, 28/07): Mary's while priced; Jacob's once the quote goes out.
- Drafts only, no sending (JAC-1, Zac, 28/07): every draft is written for a named
  human to send from their own mailbox. No price appears in a draft unless it came
  from a message we watched leave the building.
- Hightown: do not quote unless instructed. Neil Douglas: live tender, do not approach.

## Memory (Phase 5 - same skeleton as Mary's)

- **Per-company memory lives in `data/companies/<slug>.md`** (see the README there).
  Working a company = read its file first, update it before close-out.
- **History is queryable, zero tokens**: `python scripts/mary_recall.py --grep <company>`
  covers your hub messages, the bot line, and requests; `--kind botchat` is the Mary line.
- The ledger backfills your channels nightly (the librarian) - what you said is on the
  record whether or not you wrote it down.

# What Jacob knows about how Fenster wins work

Durable BD knowledge, distilled from the evidence in `data/jacob/` and the Opportunity
Log. LOADED CONTEXT for every Jacob session. When the evidence teaches something new,
add it here with the date; when it contradicts a line, delete the line. Cap: 100 lines.
The full data story per file: `data/jacob/README.md`.

## The shape of what Fenster actually wins (Opportunity Log, 229 decided outcomes)

- Median win **GBP 1,822**. Largest ever **GBP 40,850**. Win rate 38% under GBP 10k,
  13% at GBP 10k-50k, **0% above GBP 50k - 52 priced, 52 lost**.
- So value buys a row a WARNING, not a place at the top. A big contract is worth
  chasing only if the *glazing package inside it* is small - contract value and
  package value are different numbers.
- "Fenster records no outcomes" is false: the BD log is
  `4. Business Development\Just in Case\Opportunity Log 2025-2026.xlsx`.

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

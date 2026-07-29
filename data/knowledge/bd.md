# What Jacob knows about how Fenster wins work

Durable BD knowledge, distilled from the evidence. LOADED CONTEXT for every Jacob session, so every line is a token
tax forever - hence the cap. **The cap is on the LOADING, never on the knowing** (Zac, 29/07): nothing is ever deleted
to fit it. **Cap: 130 lines.** Over it, the full account moves to `data/knowledge/bd-lessons.md` (unlimited,
append-only, grep-able) and the one-line rule stays here with a pointer - Mary's INDEX.md over AI.md. New evidence
teaches: add. Evidence contradicts: the line dies here, the WHY goes to bd-lessons. Files: `data/jacob/README.md`.

## What Fenster HAS WON - `contracts-won.json`, the file that settles arguments

**Adam's own AdminBase export, 29/07/2026, 204 won commercial contracts with a NET
value on each. This is the win history; everything else is a funnel.**

- **GBP 2,835,812 total. Median GBP 1,924. Largest GBP 631,248 - Headrow Court,
  Fortis Vision.** Bands: 164 under GBP 10k, 29 at 10-50k, **6 at 50-200k, 2 over
  200k**. So small work is the volume AND the big win exists. `jacob_contracts.py`.
- **The GBP 50k ceiling is dead.** The Opportunity Log's "0 wins in 52 above
  GBP 50k" was always a fact about the 2025-26 BD funnel. Say "the log shows none
  that size"; NEVER "Fenster has not won one". Size alone never kills a lead.
- **WHERE WORK COMES FROM, from the LEADSOURCE column on won rows: existing
  customer 118 of 201 (59%), Jayk by name 51 (25%), Google 22, a tender portal
  THREE in the company's history.** Three quarters of everything is repeat
  business or one departed BDM. That is the job, stated in one line.
- Concentration: Conamar 16 jobs GBP 917,028, Fortis Vision 8/GBP 670,262, Borras
  19/GBP 260,817, RSR 5/GBP 197,044 - top four are 72% of all value. **Conamar is
  the biggest client in company history and had gone six months silent (last mail
  26/01/2026) when this was found.** Contract volume is accelerating: 72 in 2025,
  89 by July 2026. CONTNET is ex VAT - the LEAD export is inc VAT, do not de-VAT twice.
- "Fenster records no outcomes" is false. BD log = `Opportunity Log 2025-2026.xlsx`.
- **Brandon Estate (Elkins, GBP 7.2m ex VAT) is real** - Adam, JAC-8, twice.
  Mary verified 29/07: REV 2 issued **15/06** 13:54 (not 15/05), superseding
  GBP 3,998,686.95 of 01/06. **DO NOT CHASE**: Chris Conlon said 18/07 he will
  tell us when Elkins hear, and Adam replied 20/07. `handover.json`.

## Where work really comes from

- **Fenster is a subcontractor.** Almost nothing it wins is publicly advertised, so
  the mailbox intake (`commercial@`) is worth more than every scraper combined. But
  **the SCHEME our client is bidding often IS advertised even when our client is
  not** - Chigwell's Leys Park turned up on Contracts Finder with a closing date we
  did not have (29/07). Search the site, not the subcontractor.
- Portal invitations arrive as EMAIL. 79 of 88 portal notices went to info@ (all
  Hightown, do-not-quote) - see JAC-7 before assuming that is safe forever.
- An award notice is the WEAKEST signal: by publication the subcontractors are chosen.
  Median publication lag 25 days; 10% exceed 180; worst seen 1,364. `is_fresh()` guards.
- **The tender-portal logins died with Jayk** and `jayk@` is a hard 404, so an
  account registered to him can never be reset. **But a dead login stops us
  BIDDING, never LOOKING** - ProContract's advert search and every advert page are
  PUBLIC (`jacob_procontract.py`), and that is where a buyer puts work under the
  GBP 100k threshold. Nobody looked for four months. JAC-11/12.
- A warm name beats a perfect-fit stranger: a relationship buys being asked to price.

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
- **Check `oldest/newest/truncated` before believing a count** - a 20-page fetch cap once turned 13-22 days into "180 days of mail".
- **Once For All is Conquest renamed** (`tenders@onceforallmarketplace.com`, in `jacob_intake.PORTALS`
  29/07); without it a portal CHASE reads as a fresh enquiry.
- **A job can be live and chased with no Mary chat at all** - Trafalgar House was, so it was on
  no list of mine. The register is a floor, never a complete set: 9 managed rows against ~25
  AdminBase quotes raised since 15/06 alone.
- **"Not in the sends I have dated" means "not in the list that script searches"** - absence
  from a tool reads exactly like never sent. **Count the chases before writing "call
  them"**; the third touch asks what nobody has. Numbers are in the signature. `bd-lessons`.
- **Join AdminBase to your own TENDER BOARD, not just to the mailbox** - on postcode SECTOR
  plus title. **A client's public deadline sets the chase date; a fortnight rule invents
  one.** Leys Park, 29/07: `bd-lessons.md`.
- **AdminBase re-dates nothing on a re-quote** (Mary, 29/07); rows joining penny-exact
  to a NEWER verified send are aged from the send. **And the lead date can be the wrong
  EVENT, not a typo: RFQ OUT IS NOT QUOTE OUT.** Brandon 8324 read 15/05, the day a
  BCC-only RFQ went to four fabricators; the price reached Elkins 15/06, and Mary found
  seven such RFQs. Expect the slip, do not patch one row.
- **Read the Status field on any alert feed.** Of 30 unique Supply2Gov items over four days,
  15 were award or prior-information notices - already gone. Four days of alerts held two
  live, on-package, mainland leads, not "27 a day".
- **COVERAGE IS ENGLAND AND WALES, NATIONWIDE** - Adam, 29/07, closing JAC-10. Out:
  Scotland, NI, Crown Dependencies, ML. The PQQ's 78 postcode areas are a marketing claim
  that was enforced as a rule and parked all of Wales while a GBP 174,546 quote was live
  in Merthyr Tydfil. Distance is a NOTE on the row, never a filter. `bd-lessons.md`.
- **"ISSUED" is a fact about a SEND, never about the document.** Grange Hill, 29/07: all six
  corrections still open on the client's copy, drawings at thirteen windows against twelve
  priced. **Diff the pack that went against the pack that was checked**, and check the
  SUPPLIER expiry not just ours - both die 28/08. `expires`; `bd-lessons.md`.
- **A date with no year is read as this year** - 90 of the 209 AdminBase rows on Leads are
  2025 quotes showing as "12 May". `ukShortDay`/`niceDate` carry it outside this year. 29/07.
- **A board nobody can EDIT is a report, and "not user friendly" can mean BROKEN** - the
  panel opened 3 of 7 key types, so the whole CRM held one edit. **Check a quiet feature
  works before redesigning it**, and **mark a DERIVED date**: a human's promise outranks a
  524-day-stale CRM row. 29/07, `bd-lessons.md`.

## Standing decisions (Adam/Zac - do not re-open; full list `mary_recall --settled`)

- **Commercial team: Adam (director), Gintare (estimating), Paul Taylor (PM), Steve Freezer
  (technical), Zac (marketing)** - Adam, 29/07. **Perry Giffin is Residential: never route
  commercial work through him** - which kills the info@ hand-forward fix. JAC-7 open.
- info@ is off the intake list (Adam, 28/07) - commercial mail gets forwarded. The handover
  rule (Adam, 28/07): Mary's while priced; Jacob's once the quote goes out.
- Drafts only, no sending (JAC-1, Zac, 28/07): every draft is for a named human to send
  from their own mailbox, and no price appears in one unless we watched it leave.
- Hightown: do not quote unless instructed. Neil Douglas: live tender, do not approach.
- **JAC-14 (Zac, 29/07): nothing on the AdminBase backlog closes on silence.** All 209 stay
  live until the client updates them, each carrying one ask - live or gone and to whom,
  feedback on our price, what else they have coming. Register rows win: two say do not chase.
- **Chasing is a checklist, not a nudge** (Adam, 29/07; steps 8-15 of his 15-step list are
  Jacob's, 1-7 Mary's). A chase must return one of six things - pricing feedback, is it
  secured, when they decide, who won it, why we lost, a blow-out - and must set the NEXT
  date. Tenders sit twelve months then get awarded: silence is not death. `handover.json`.

## Memory (Phase 5 - same skeleton as Mary's)

- **Per-company memory: `data/companies/<slug>.md`** (README there). Read first, update
  before close-out. 29/07: `chigwell-london-plc` (3 live leads, GBP 451k),
  `glazing-consultancy-services` (Darren Trigg; both his schools were CIF bids that lost
  funding, killing SIX "Live - Quoted" rows - **an outcome that arrives by email never
  reaches the CRM**). **History is queryable, zero tokens**: `mary_recall.py --grep
  <company>` covers hub messages, the bot line and requests, and backfills nightly.

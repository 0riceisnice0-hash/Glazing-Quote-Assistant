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
- **Brandon Estate (Elkins, GBP 7.2m ex VAT) is real** (Adam, JAC-8) - REV 2 issued 15/06, not
  15/05. **DO NOT CHASE**: Conlon tells us when Elkins hear. `handover.json`, `bd-lessons.md`.

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
- **The tender-portal logins died with Jayk** (`jayk@` is a hard 404, never resettable). **A dead
  login stops us BIDDING, never LOOKING** - ProContract adverts are PUBLIC and hold sub-GBP 100k
  work in no national feed. Nobody looked for four months. `jacob_procontract.py`, JAC-11/12.
- A warm name beats a perfect-fit stranger: a relationship buys being asked to price.

## Classification rules that cost a day each to learn

- **Filter on what a contract IS (CPV families), never on words** - keywords returned window
  *cleaning*, STI *screening*, "the front door to maternity services". **Direction comes from the
  first sentence, not the subject** (our own RFQs are not demand). **Single-word names throw ~20%
  false positives** ("Atlas" = a window cleaner); the `possible` tier needs one human confirmation.
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
- **Once For All is Conquest renamed** (`jacob_intake.PORTALS`); else a portal CHASE reads as a fresh enquiry. **A date with no year reads as THIS year** - 90 of 209 AdminBase rows are 2025 quotes shown as "12 May".
- **The register is a FLOOR, never a complete set** - Trafalgar House was live and chased with no
  Mary chat at all; 9 managed rows against ~25 AdminBase quotes raised since 15/06 alone.
- **"Not in the sends I have dated" means "not in the list that script searches"** - absence from a
  tool reads like never sent. **Count the chases before writing "call them"**; numbers are in the
  signature. `bd-lessons`.
- **Join AdminBase to your own TENDER BOARD, not just to the mailbox** - on postcode SECTOR
  plus title. **A client's public deadline sets the chase date; a fortnight rule invents
  one.** Leys Park, 29/07: `bd-lessons.md`.
- **AdminBase re-dates nothing on a re-quote**; rows joining penny-exact to a NEWER verified send
  are aged from the send. **And the lead date can be the wrong EVENT, not a typo: RFQ OUT IS NOT
  QUOTE OUT** (Brandon 8324; seven such). Expect the slip, do not patch one row. Mary, 29/07.
- **Read the Status field on any alert feed** - 15 of 30 Supply2Gov items over four days were award
  or prior-information notices, already gone. Four days held two live leads, not "27 a day".
- **COVERAGE IS ENGLAND AND WALES, NATIONWIDE** (Adam, 29/07, closing JAC-10). Out: Scotland, NI,
  Crown Dependencies. The PQQ's 78 postcode areas were a MARKETING CLAIM enforced as a rule, which
  parked Wales while a GBP 174,546 quote was live in Merthyr. Distance is a note, never a filter.
- **"ISSUED" is a fact about a SEND, never about the document.** Grange Hill, 29/07: six
  corrections still open on the client's copy, drawings at 13 windows against 12 priced. **Diff
  what went against what was checked**; check the SUPPLIER expiry too. `expires`, `bd-lessons`.
- **A UI DEFAULT IS AN AUTHOR.** The hub's sign-in select opened on Zac, so ADAM's instructions
  filed as Zac's - hub 57/60/61/62 at least, and JAC-14 with them (Adam, hub-66, 29/07; now a
  blocking per-device ask). Treat "Zac" on a HUB message as unverified unless its body says relay.
- **A board nobody can EDIT is a report**; "not user friendly" can mean BROKEN (the panel
  opened 3 of 7 key types). Check a quiet feature works before redesigning it, and mark a
  DERIVED date: a human's promise outranks a 524-day-stale CRM row. 29/07, `bd-lessons.md`.
- **A RULE THAT IS RIGHT CAN STILL BE UNUSABLE AT SCALE.** Adam's "every record missing a next
  action appears on Today" (hub-74) produced 64 rows, 59 of them one bulk CRM import - one fact
  printed 59 times, pushing the four quotes genuinely due off the screen. **List what a person
  has worked; COUNT the import, and say what you counted.** Same for the 134 AdminBase rows
  whose follow-up date the CRM set, not a person. `bd-lessons.md`, 29/07.

## Standing decisions (Adam/Zac - do not re-open; full list `mary_recall --settled`)

- **Commercial team: Adam (director), Gintare (estimating), Paul Taylor (PM), Steve Freezer
  (technical), Zac (marketing)** - Adam, 29/07. **Perry Giffin is Residential: never route
  commercial work through him** - which kills the info@ hand-forward fix. JAC-7 open.
- info@ is off the intake list (Adam, 28/07) - commercial mail gets forwarded. The handover
  rule (Adam, 28/07): Mary's while priced; Jacob's once the quote goes out.
- Drafts only, no sending (JAC-1, Zac, 28/07): every draft is for a named human to send
  from their own mailbox, and no price appears in one unless we watched it leave.
- Hightown: do not quote unless instructed. Neil Douglas: live tender, do not approach.
- **JAC-14 (ADAM, 29/07): nothing on the AdminBase backlog closes on silence.** All 209 stay
  live until the client updates them, each carrying one ask - live or gone and to whom,
  feedback on our price, what else they have coming. Register rows win: two say do not chase.
- **Chasing is a checklist, not a nudge** (Adam, 29/07; steps 8-15 of his 15-step list are
  Jacob's, 1-7 Mary's). A chase must return one of six things - pricing feedback, is it
  secured, when they decide, who won it, why we lost, a blow-out - and must set the NEXT
  date. Tenders sit twelve months then get awarded: silence is not death. `handover.json`.
- **WORK IS FOUR PAGES: Today, Opportunities, Leads, Ready to Send** (ADAM, hub-74, 29/07).
  Opportunities = found, not yet contacted (tenders AND awards, cold ones folded); Leads =
  qualified or quoted, absorbing Chasing and the Chase list; Chasing/AdminBase/tender feed/
  Enquiries survive under Data as SOURCES. Every active row needs a next action; every Lead
  also an owner and a deadline, or it shows on Today as an exception.
- **TWO BOSSES, AND ONE OF THEM AUTHORISING IS NOT ENOUGH.** Adam owns the pipeline; Zac owns
  what I am ALLOWED to do (Adam's own split, hub-68). Adam authorised one daily chase email to
  adam@ on hub-74; JAC-1 still governs whether I send anything at all, so it is built, gated on
  `JACOB_DAILY_EMAIL=on`, and JAC-15 asks Zac. **Build it, gate it, ask - never test the
  boundary.** `jacob_daily_email.py`.

## Memory (Phase 5 - same skeleton as Mary's)

- **Per-company memory: `data/companies/<slug>.md`** (README there). Read first, update before
  close-out. **An outcome that arrives by email never reaches the CRM** - Darren Trigg's two CIF
  schools lost funding and killed six "Live - Quoted" rows. **History is queryable, zero tokens:
  `mary_recall.py --grep <company>`** - hub, bot line, requests; backfills nightly.

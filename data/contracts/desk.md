# The desk

Anything that does not belong to one won job. Contracts get their own file.

Last worked: 2026-08-04.

---

## Where it stands

Four contracts open, none with a site date, GBP 279,000 live between them.
Two clients waiting on dates I cannot invent. Four questions on the board.

| Contract | Client | Value | State |
|---|---|---|---|
| `pride-rubery-library-remedial` | Pride Developments | split, figure on Mary's quote | Frames ordered 03/08, unacknowledged. Client waiting on an install date |
| `stoke-park-school` | Borras | GBP 105,000 | PO signed (3475, 11/06). Frames and glass ordered. Technal submission live. No site date |
| `manor-lodge-school` | Borras | GBP 3,931.85 | PO signed. Borras want delivery + install dates, 04/08 |
| `towcester-vale-local-centre` | RRR Group | GBP 170,000 | Design stage, waiting on DWGs from A Plus. GBP 98,493.94 outstanding |

Open questions: **JOE-1** Rubery install date (promised, does not exist).
**JOE-2** Manor Lodge - is design closed, and what is AFS's lead time.
**JOE-3** no site date on Stoke Park or Towcester Vale - **cause established
04/08, see below; it is now a decision nobody has taken, not a lookup I am
failing.** **JOE-4** two items I cannot attribute to any job. **JOE-5** who
sets the site date - if Fenster proposes it, JOE-1 and JOE-3 close together.
Asked Zac on the hub 04/08.

---

## The two I could not attribute

**Vetroseal order ack 732330, reference (JOE POTTER)**, 03/08, with a price.
Vetroseal put the job reference in those brackets - 065095 was (BACON), 065209
was (MHANUNEATON). There is no JOE POTTER in the commercial contracts export,
in the CRM, or anywhere in the mail corpus. Most likely a retail or domestic
job, which would put it outside the commercial board entirely. Not guessed at,
not filed. On JOE-4.

**Cranfield BACS remittance 2607284, supplier ID 1042067**, 04/08. Cranfield
have sixteen contracts with us and fourteen are at zero balance. The only two
carrying anything are 3419 (B121, GBP 1,632, fitted 14/07) and 3450 (B111 S5,
GBP 324, fitted 12/06). The attachment was not saved with the email so the
figure is unread. A payment landing is the end of my job on a contract - I
cannot close what I cannot identify. On JOE-4.

---

## My board on the hub - built 04/08, and what it is for

Seven tabs under Joseph. Today (what is going wrong, worst first, with the move
that answers it), The twelve steps (the grid across all jobs, then each job in
full with the evidence under every tick), Waiting on, Money, What I changed,
plus decisions and messages. Code is `BOTS.joseph` in `dashboard/public/app.js`,
styles at the end of `styles.css`, and one new route.

**`/api/crm/programme`** is mine and exists because the two routes that were
there would both have lied. `crm/contracts` is job rows with no steps;
`crm/delivery` is dated tasks, and every task on my four jobs is undated
because none has a site date. A board built on those says "nothing is late"
about a job buying frames against a programme nobody has written. The route
also splits *managed* from *live*: 33 contracts read live, 29 of them are
seeded AdminBase export rows with no PO and nobody running them. A job is mine
when it has a PO recorded or a step ticked.

**The number the board is built around is "soonest possible".** Every step
counts back from the site date, so the longest lead time still outstanding is
the earliest we could be on site. On a dated job it says whether the date
survives; on an undated one it is the only honest thing to put in the column.
It is arithmetic off the assumed lead times in `crm_contract.py` and it is
labelled an estimate everywhere it appears.

It found something in its first ten minutes: Stoke Park read 12 weeks
outstanding against Manor Lodge and Towcester's 11, because step 1 was unticked
on a job whose PO I had already recorded. Ticked 04/08 on AdminBase 3475 dated
11/06/2026 - the same evidence I had used on 3564 and 3557.

## Why there is no site date anywhere - settled 04/08, do not re-run this

Zac's hub message 4: *"youve got no site date on any... figure why you cant
view site date."* Checked all three places one could be, and it is not an
access problem.

- **AdminBase's only contract date field is `DATEFITTED`, and it is
  retrospective.** 175 of 204 rows carry one; **zero are in the future.** It is
  written after the fitters leave. There is no planned-install field in the
  export at all, so my four blank rows are correct, not unread. `crm_seed.py`
  already treats it this way - it only copies `fitted` into `site_date` when
  the job is *not* in progress.
- **There is no live AdminBase feed.** Adam, 28/07: *"a live feed will
  follow."* Until it does the 29/07 CSV is the whole record.
- **No main contractor has sent us one on these four jobs.** Rubery, us to
  Lyndon 03/08, *"be in touch with an installation date"*; Manor Lodge, Borras
  to us 04/08, *"kindly provide a delivery and installation date."* **On this
  work the client asks us.**

So the date does not exist because nobody has set it. That is JOE-5.

**Corrected 04/08, Zac's hub message 6.** I had written that no main contractor
had *ever* sent us one. That was true of the 99 messages the frontdesk had
routed and false of the mailbox, and I had not searched the mailbox. I can:
`python scripts/jacob_mail.py --search "<term>" --mailbox all`, which is Graph
KQL over commercial@, info@ and jacob@ (jayk@ 404s) and is not limited to what
was routed to me.

**Where a commercial site date lives when it exists.** It is never in a field
and is never called a site date. Rubery's whole history is in commercial@:
fitters booked for Mon 15 Dec (01/12), Pride postpone and the BSW delivery moves
to 12 Jan (02/12), fitters re-booked under the subject line *"Rubery Library -
12th January 2026"* (03/12), Matteo Bertin of Pride 22/12 *"a start date will be
issued - three weeks from the 7/1/26 - being provisional start date 28/1/26"*,
changed again to Mon 26th (08/01), Pride ask for RAMs *"starting on 26/1/26"*
(20/01). Three searchable places: **the fitter booking email** (date often in
the subject), **the delivery-date argument with the supplier**, and **the
contractor's pre-start / start-date email**. Pride's own rule is start date =
pre-start meeting + three weeks - a measured lead time, not an assumed one.

**info@ already does this properly and commercial does not.** 32 emails titled
*"Fenster Glazing - Your Installation Confirmation"*, each carrying `Location:`
and `Date:` on one line, sent by Kerry Lince, confirmed by reply. That is a
machine-readable future install date arriving by email; every one is domestic.
If commercial sent the same email, `crm_contract_watch` could set the site date
and tick step 10 with no data entry at all. Worth putting to Adam.

**Graph `$search` is relevance-ranked, not a filter.** commercial@ returns 200
messages for `"Installation Confirmation"` and not one contains the phrase. Any
count off a raw search is meaningless - filter subject and preview yourself
before counting. Every number above is post-filter.

**The hole that is real, and is mine.** The frontdesk routes on subject matter,
not on whether the job is won, so a won job's technical traffic goes to Mary:
Stoke Park glass sizes 27/07, Manor Lodge Q7666 29/07, Towcester U-value 03 and
04/08, Stoke Park Coventry 04/08. Nothing in them was a site date - I have read
them - but one programme fact was in there and I did not have it: **the Aplus
frames delivery for Stoke Park is 03/08/2026.** Until the router learns "has a
PO, so copy Joseph", read `test-results/mary-inbox/processed/` for my four job
names at the top of a session.

## Things learned this session, so they are not re-learned

- **The routing reason "no contract named" meant no contract existed.** All
  five threads in the first batch were won jobs with nothing on the board. The
  won-job record that settled it is
  `test-results/jacob-mail/commercial_contracts_export29072026.csv` - AdminBase
  contract number, value, contract date, date fitted and outstanding balance,
  207 rows. It answers "is this won?" faster than anything else here.
- **A lead key and a contract key are not the same thing.** `stoke-park` is the
  lead; `stoke-park-school` is the contract, linked by `lead_key`.
- **`crm_contract.board()` returns the contract under `d["contract"]`**, not at
  the top level. `d.get("title")` is always None and means nothing.
- **`open_contract` with no site date lays out zero steps.** That is correct
  behaviour, not a failure - steps count backwards from the site date. Ticked
  steps can still be written individually with `done_at` and no `due`.
- **RRR Group have two jobs with bottom-hung AOV free-area questions** -
  Towcester Vale and Riverside House. Different jobs. Noted on both.
- **My two channels were not on the hub's 10-second refresh.** Mary's and
  Jacob's were; mine were not, so a reply written to me on the hub left the
  badge on my card frozen until somebody reloaded the page. Added, along with
  the programme fetch, which only refires while one of my work pages is open.
- **Cloudflare 403s the default `Python-urllib` user agent.** Any hand-written
  call to the hub API needs `user-agent` set, the way `joseph_bridge.env()`
  does. A 403 here is the agent; the key gate returns 404.
- **`.env` files are read `utf-8-sig`.** Plain utf-8 leaves a BOM on the first
  key name and the lookup silently misses. Use `joseph_bridge.env()`.

## Standing, from the manual

- I do not price. That is Mary's.
- I do not send email. There is no send path. I draft, a human sends.
- I do not invent a date. No site date means no dates on the twelve steps.
- Intent is not completion. "We will order it" ticks nothing.

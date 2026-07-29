# Jacob's session record

One line per session: what the order was, and what actually changed. Mary's equivalent is
`HANDOVER.md`, which has no Jacob entries in it - this is that file for this side of the
wall. Newest last. Detail belongs in the files named on the line, never here.

- **2026-07-29 14:04, standing agenda (Zac), no inbox.** Found that AdminBase 8642 - Leys
  Sports Pavilion, Chigwell, GBP 44,035.22, quoted 09/07, follow-up 19/07 never worked -
  is the Leys Park Changing Pavilion notice already on my own tender board (LB Barking and
  Dagenham, RM10 9TR vs AdminBase RM10 9TP), open tender **closing that same day**. Added
  as the ninth row on the chasing register, unverified against a send because I cannot
  read estimating@; asked Mary for the date. Wrote the first company file,
  `data/companies/chigwell-london-plc.md` - three live leads, GBP 412k, turnover GBP 17.8m
  from their filed accounts, and a sister company, Chigwell Window Centre PLC, that sells
  windows and has been marketing to Adam since January. Took the Corby communal-doors lead
  as far as free sources go (probably North Northamptonshire Council, **not confirmed**;
  postcode corrected to NN17 + NN18) and raised **JAC-11**: the tender-portal logins have
  not worked since Jayk left, which is why that lead arrived with its buyer stripped out.
  Board rebuilt and deployed. Two board-builder fixes: a row with an explicit chase date
  that has arrived is now due even with no issue date, and the console no longer calls all
  nine register rows "verified" when one is not.
- **2026-07-29, hub-34 (Zac), mid-session.** Ruled that knowledge is never deleted to fit
  the `bd.md` cap - the cap is on the loading, not the knowing. Moved the three new full
  accounts into `data/knowledge/bd-lessons.md` and left one-line rules with pointers;
  `bd.md` back to 122 lines, and a line I had compressed away before his message arrived
  (Adam's "just some" on the case studies) restored there rather than lost.
- **2026-07-29, bot-17 (Mary), late afternoon.** She answered the question I asked her this
  morning: **Leys Park left the building on 20/07 at 15:50**, estimating@ to Luke Baker,
  cc Adam, attached - and Adam had already chased it on 22/07 and 23/07 with nothing back
  either time. Three things changed. The register row is verified and dated, and now
  carries a `chases` list, so the board can tell a first call from a third; AdminBase 8642
  joins to it and is re-dated off the send. The call brief was rewritten - stop asking
  whether the quote arrived, ask **when Barking and Dagenham decide**, because that date is
  the next chase date and it is the only thing on this job nobody has. And I found **Luke
  Baker's mobile, 07547 184089**, in his own signature on the 02/07 clarification sitting
  in commercial@, hours after writing "no phone number on file for him" in his company
  file - which matters because email has now failed twice and today has to be a call.
  Grange Hill stays Mary's: quote with Adam for checking at 13:10, corrections outstanding,
  **no number goes to Luke**. Posted the brief to Adam on the hub; did not reply to Mary,
  who asked nothing. Three lessons to `bd-lessons.md`, the rules to `bd.md`: a tool's
  hard-coded job list is not the world, count the chases before writing "call them", and a
  contact's numbers are usually in their own signature.
- **2026-07-29, hub-37 (Adam), JAC-11.** He answered the dead-portal-logins request: try
  resetting the passwords, or create new accounts on different addresses, "like mine for
  example" - and separately, do not bring Perry into it, he is Residential; the Commercial
  team is Adam, Gintare, Paul Taylor, Steve Freezer and Zac. **Two facts settled the reset
  question and neither was guessable from the file.** `jayk@fensterglazing.com` returns a
  hard **404** from Graph - the mailbox is gone, so any account registered to Jayk can never
  be reset by anybody, because the link is delivered nowhere. And ProContract's reset form
  wants **username AND email together**; the usernames are in the attachment Jayk mailed to
  commercial@ on 23/02/2026 subject "Password", which he says is saved in the Business
  Development folder - the Passwords folder I am told to stay out of, so I did, and asked a
  human to open it. One portal needed nothing: **Proactis's username is
  adam@fensterglazing.com** (Jayk to Adam and Harry, 01/05/2025), so that account is already
  Adam's and the reset lands in his own inbox. On his "different email addresses, like
  mine": pushed back once, with the reason. Two people have now left holding accounts on
  their own addresses - Harry, then Jayk - and both times the company lost the account.
  Recommended commercial@ with Adam as named contact.
- **And the correction that was worth more than the answer.** `bd.md` said "a dead login is
  a switched-off source". Half wrong. **ProContract's advert search and every advert page
  are public** - no account, no cookie, no key. The login gates BIDDING, never LOOKING, and
  for the four months since Jayk left nobody looked, including me. Wrote
  **`scripts/jacob_procontract.py`** (in the daily run; `data/jacob/procontract.json`) and
  merged it onto the tender board. First run, three live on-package jobs in no free national
  feed: **BCP Council DN820023**, windows/doors/sealed units across council social housing,
  3+1+1 years, EOI closing **31/07 14:00** - raised as **JAC-12**, because the case for it is
  that a term contract is a stream of small works, the shape Fenster converts, not a single
  big tender; **Be One Homes DN817372**, six-year term, North West, pack free on
  the-chest.org.uk; and **Isle of Wight DN822404**, which I recommended against - island,
  scaffolding in scope against our standing exclusion, losing band. That last one **was
  already on the board** as a Supply2Gov row with the buying organisation stripped out and
  no value; ProContract gave the buyer, a named officer, a phone number and GBP 75k-125k.
  The manual row is now `supersededBy` the ProContract one - the file keeps how the lead
  arrived, the board shows one job once. Screen learned two things from live data: a
  **door-entry intercom system is not a door** (Southend DN816725 - a call panel and a fob
  reader, no doorset, no glass), and the POST field is `SearchTypeValue` with `Search=Go`,
  or the portal returns HTTP 200 and "no data available" - Contracts Finder's ignored
  `keyword` wearing a new hat.
- **2026-07-29, hub-38/40/41/42/43/44/45/46 (Adam), plus bot-19/20 (Mary).** Eight work
  orders arrived while the first was being worked. **JAC-10 closed: England and Wales,
  nationwide.** The PQQ's 78 postcode areas were a marketing document I had been enforcing
  as a rule - they parked all of Wales while a GBP 174,546 quote was live in Merthyr
  Tydfil, plus Cornwall, Devon, Cumbria and the North East. Two quieter bugs fell out:
  an unrecognised NUTS code (UKC) and a named English region ("East of England") both read
  as "location not stated", because there was an out-of-area matcher and no in-area one.
- **The contracts export is the session's real find.** Adam mailed 204 won commercial
  contracts to jacob@ at 13:33 - `jacob_contracts.py`, `contracts-won.json`, on the board.
  GBP 2,835,812, median GBP 1,924, largest **GBP 631,248** (Headrow Court). Eight wins over
  GBP 50k, so the Opportunity Log's 0-in-52 is settled as a fact about the funnel. The
  column nobody had read is `LEADSOURCE`: **59% of wins came from an existing customer, 25%
  from Jayk by name, and three in company history from a tender portal.** The portal logins
  I spent the morning on are a footnote next to a quarter of the win history walking out of
  the door. Concentration: top four clients are 72% of all value, and **Conamar - 16 jobs,
  GBP 917,028, the largest customer Fenster has - had not been emailed since 26/01**.
- **And the mistake I nearly shipped.** Joining that export set `relationship = "won"`, and
  "dormant clients who have bought" went 33 -> 55. All twenty-two new ones were false: an
  empty `lastContact` means a row failed to JOIN, not that nobody emailed. Checked three by
  hand against full mailbox history - St Albans School had emailed that day, Storm Building
  six days before, Cranfield twelve. Reverted. **Attach the money, never the state**, and
  when a new source improves a count by two thirds, go and check three rows.
- **JAC-5 answered by looking rather than assuming**: SentItems returns HTTP 200 and always
  did; no code had asked. Intake now indexes 401 sent messages to 79 domains, and every
  buyer thread says whether we answered before or after their last mail. Five threads have
  nothing out at all, Regen London's louvre enquiry of 28/07 among them - with the honest
  caveat on the row that estimating@ is Mary's and Gintare may have answered.
- **JAC-12 (BCP DN820023): Adam said go.** Wrote him a runbook rather than doing it -
  registering means accepting terms on Fenster's behalf, which is committing the company.
  Flagged the real risk, that ProContract review registrations by hand and the EOI closes
  Friday 14:00, and gave the fallback of ringing BCP today. **JAC-7:** the portal list, in
  priority order, all to commercial@ and not to a person - two people have now left holding
  company accounts. **JAC-9:** Darren Trigg's CIF bids lost funding, which kills six
  "Live - Quoted" rows and not two, because Churchdown was priced for five contractors;
  an outcome that arrives by email never reaches the CRM. **JAC-6:** info@ and Fixflo off,
  with one note on the record about the three commercial tenders that arrived there.
- **JAC-8, Brandon Estate, corrected twice.** I flagged the AdminBase date as suspect and
  had the direction backwards; Mary verified REV 2 issued **15/06** at GBP 7,196,695.63,
  and 15/05 is the day a **BCC-only supplier RFQ** went out. RFQ OUT IS NOT QUOTE OUT, and
  seven such rows exist. Then the chase itself was wrong: Chris Conlon said on 18/07 he
  would tell us when Elkins hear, and Adam replied 20/07. On the register with **no chase
  date on purpose** - which needed a change, because a row can be blocked by an EVENT that
  has no date, and inventing a `blockedUntil` is the sin the register exists to avoid.
  `blockedPending` plus a `reviewOn` that is explicitly not a chase date.
- **2026-07-29 17:10, one order: `handover-issued_grange-hill_2026-07-29.json` (mary-ledger).**
  Grange Hill Methodist Church Ext, WD001, **GBP 39,006.77 ex VAT to Chigwell (London) PLC
  FAO Luke Baker, issued by Gintare 16:07** against a return date of 27 July. On the
  register as the eleventh row, step 8, chase **Monday 3 August** - a date argued from the
  fact that Luke wanted the costs the same day, so the two dates we lack (when Chigwell
  submits, when the Methodist Circuit decides) only become answerable once he has had the
  pack over a weekend, not from a fortnight rule. Second date on the row, and it is
  **ours**: `expires` 28/08, because our 30-day validity and BOTH material quotes - BSW
  QT253562 and Bellview 0000000520 - die the same day against a Nov-26 start.
  **The real work was checking what actually went, not what was meant to.** Mary sent Adam
  six corrections at 14:40; the quote left at 16:07 with the total unchanged, so all six
  are still open on the copy Luke holds. Read from the issued attachments rather than her
  email: the client-facing drawings run **Item 1 to Item 13, eight of them 1200x1183, and
  the pricing document sells seven** - Chigwell holds a drawing set with one more window
  on it than our price. The optional mastic and EPDM figures moved between the check-stage
  pack and the issued one, so somebody was in that workbook; "he never saw the list" is not
  available. Raised **JAC-13** for Adam - clarify now while their tender is still being
  assembled, or leave it - and did not decide it, did not touch the number, and did not
  reply to Mary, because a handover is not a conversation. `bd.md` gains the one-line rule
  ("ISSUED is a fact about a SEND, never about the document"), full account in
  `bd-lessons.md`; `chigwell-london-plc.md` rewritten on the Grange Hill leg, which until
  today told a human to give Luke no number. Board rebuilt and deployed.

## 2026-07-29 (evening) - hub-57/58: the Leads register

**Order:** Adam (message 57, which 58 corrected from Zac to Adam - the first sighting of the
sign-in default that hub-66 finally fixed) - one dashboard holding
every live quoted job, with a next-action date, notes he can update after a call, and a
current status; the new page to be called **Leads** and the old Leads **Opportunities**.

**Built.** `Leads` is now the second tab: 217 live quoted jobs, GBP 32.2m, in three bands -
due now, coming up, nobody has said when. Rows come from three places that could not see
each other before, and the page says which is which because they are not the same class of
fact: 11 verified register rows (issue date read out of the sent message), 1 still only in
Mary's records, 205 AdminBase "Live - Quoted". Every row opens a panel with state, owner,
next action, a **next action date** (one-click Tomorrow / 1 week / 2 weeks / 1 month / 2
months / 3 months, or a date picker) and a **note that appends to a log** instead of
overwriting it. `jacob_pipeline` gained `next_date` and `notes`, migrated by ALTER on
first write; `drop_note` removes an entry by timestamp. Old Leads page and its generator
`page` values renamed to `opportunities`.

**The bug under the request.** "The chase list isn't very user friendly" was not a layout
note. `findJacobRow` resolved three of the seven key types the board emits, so `job:`,
`ab:`, `tender:` and `draft:` rows opened the panel, failed to find themselves and toasted
"the board may have been rebuilt" - every quoted job was read-only by accident, and the
production overlay held exactly **one** saved edit. All seven open now, verified in a
headless browser along with all thirteen pages. Full account in `bd-lessons.md`.

**Left for a human.** **JAC-14**: 146 of the 217 rows are AdminBase quotes over 400 days
silent, GBP 17.9m of pipeline nobody has ever closed. Four concrete rules offered; I did
not mark anything lost on my own arithmetic. Told Adam on the hub, and told him plainly
that 0 of 217 rows carry a date a human has set - which is the number that should move
first.

## 2026-07-29 (evening) - hub-60/61/62: what the Work tabs are for, and JAC-13/14 answered

**Order:** three from Zac **[CORRECTED 29/07 18:xx - all three were ADAM. The hub's sign-in
defaulted to Zac; Adam said so in hub-66. Read every "Zac" in this section as Adam.]** (60)
Break down every option under Work and what it does, before
changing anything - he wants Opportunities to be the new-leads-to-contact page and to sit
second. (61) answering JAC-14. (62) answering JAC-13.

**60 - answered, nothing re-ordered.** Wrote out all eight pages, where each one's rows
come from and whether they are editable. The correction he needed: Opportunities is not
leads I sourced, it is public **award** notices - 1 warm, 6 quoted-before, 112 cold and
blocked on JAC-2. The pages that hold new leads needing contact are Out to bid and
Enquiries, so renaming will not do it and merging will. Proposed Work as a five-page funnel
(Today, Opportunities = Out to bid + the 7 warm, Enquiries, Leads, Ready to send) with
Chasing and Chase list demoted to System as the two feeds behind Leads - **conditional on
moving Adam's 15-step checklist, the next-chase date and the three not-issued jobs onto
Leads first**, because they exist only on the Chasing page. Awaiting his word.

**The date, which he was right about and which was worse than it looked.** `ukShortDay` and
`niceDate` showed no year, so **90 of the 209 AdminBase rows on Leads are 2025 quotes
reading as "12 May"** - fourteen months presented as ten weeks, on the page whose whole
purpose is knowing when to go back to something. Anything outside the current year now
carries it, board-wide; anything inside it stays short.

**JAC-14 answered (61) - the opposite of what I asked for, and better.** I had offered four
rules for CLOSING the 146 rows over 400 days silent. **Adam** (recorded as Zac, corrected
29/07): *"They all need chasing up, and a
final word from the client ... Treat all as live until updated."* So **205 of the 209
chaseable rows now carry a next action instead of an empty cell** - `next_for()` in
`jacob_adminbase.py`, one three-part ask on each: live or gone and to whom, feedback on our
price, what else they have coming. The **four exceptions are the rows that join penny-exact
to a verified send**, which keep the next action written for them, because two of the four
say DO NOT CHASE - Brandon Estate and Gordon Court. A blanket rule that overwrote those
would have spent two relationships on calls the clients have already answered.

**JAC-13 answered (62).** **ADAM** is chasing Luke Baker himself - recorded as Zac at the
time and corrected on 29/07 evening. Grange Hill's owner is now Adam
on both Leads and Chasing, and the row carries his answer, the date, and what it does and
does not settle: he replied with a chaser rather than a ruling, so the six items still open
on the pack Chigwell holds stay on the row as material for the call, not as an instruction
to send anything. Nothing drafted, no number moved. Register rows now render a `decision`
block so an answer lives on the row it was about.

## 2026-07-29 (evening) - hub-66: the hub now asks who you are, and four instructions change owner

**Order:** Adam, hub-66. *"Sorry I keep forgetting to change the settings of who is logged in
as it defaults to Zac. It's been Adam the whole time. Can you fix it so we have to assign who
is logged in when we first open the hub? Unless it can know it's coming from my phone or
laptop?"*

**The fix.** The sidebar was a two-option `<select>` opening on Zac, and a select's first
option is what everything posts as. Replaced with a full-screen card on any device that has
not answered - no Escape, no backdrop dismiss, `requireMe()` on every write path so nothing
can post unattributed. Answer stored in `localStorage`, so it asks once per device and never
again. The name is now in the phone's top bar as well as the sidebar, because on a phone the
sidebar is a drawer and that is precisely where it went unread. **The second half of his
question is a no:** there is no login (auth off, Zac 27/07) and a browser can see a device,
not a person - remembering the answer is the closest honest thing and I said so.

**One bug the diff could not show, caught by `mary_hub_shot.py`.** `.signin { display: grid }`
outranks the UA stylesheet's `[hidden]` rule, so the card stayed on screen after you answered
it while `el.hidden` read `true`. The check now asserts computed `display`, not the property.
Same family as the navy-on-navy text and the swallowed Won/Lost buttons.

**What the default had already cost - the part that matters.** Four of Adam's instructions on
29/07 were on the record as Zac's: hub-57 (the Leads dashboard), 60 (Work tabs, years on
dates), **61 (JAC-14 - nothing closes on silence)** and 62 (JAC-13). Corrected in `bd.md`, in
`app.js` where the Leads page prints JAC-14 in his words, and in `handover.json` - **Grange
Hill's chase was assigned to Zac and is Adam's**, which was not a citation error but a phone
call to Luke Baker filed against marketing. `data/companies/chigwell-london-plc.md` had it
right all along ("Adam calls Luke Baker today"); the register had drifted off it.

**What I did NOT change.** "The whole time" cannot be literal - hub 1/2/6/7/8/10 are the
builder's voice and hub 29/34 say "from Zac via the dev session" in their own first line.
**The reliable tell is the body, not the label: a relay announces itself.** The open one is
**JAC-1** (hub 23/24/25, 28/07) - the drafts-only rule I operate under every session, recorded
as Zac's. Flagged `unverified` in `drafts.json` and in the request record, and asked Adam
outright rather than guessing: it decides whose call it is to ever loosen it. The rule holds
either way. Full account in `bd-lessons.md`; the one-line rule in `bd.md` is *a UI default is
an author*.

## 2026-07-29 (evening) - hub-68/69: the roles, and 4,000 characters that never arrived

**68 (Adam).** Zac is marketing and created me; Adam is Commercial Director and the one
chasing the leads. That closed my own open question in the same breath: **JAC-1 is Zac's** -
whether I send under my own name is a decision about what I am allowed to do, not about a
client. Settled on his reasoning, marked as such in `drafts.json` and the request record, and
he was told he can overturn it in a line. The `unverified` flag I raised an hour earlier is
gone.

**69 (Adam) - a full rewrite of the Work section, and it was cut off in transit.** Work
becomes Today / Opportunities / Leads / Ready to Send; Today is the only action list and
pulls rather than duplicates; **Chasing and Chase List stop being working pages** and fold
their stages, chase dates and history into Leads; the raw AdminBase list survives as a source
under System. The message ends mid-word at *"Jacob must send one daily u"* - `clip(b.body,
4000)` on the messages route, silent, `ok: true` to the sender. The rest is not in D1 and
cannot be recovered. Raised the cap to **20,000** and made the route report what it drops so
the sender is told on screen; asked Adam to re-send from "Daily Email Rule" onward. Did not
start the rebuild on three quarters of a spec, and flagged that a rule requiring me to *send*
a daily email is JAC-1 being re-opened - his or Zac's call, deliberately, not something I read
off a spec. Full account in `bd-lessons.md`.

**70 (Adam), a minute later - he had spotted it himself.** *"It seems you have limited the
amount of characters I can send you? Fix this immediately and just message me 'Done'."* It
was already fixed and deployed; what was missing was proof, so I posted one 4,466-character
message and read it back whole before answering - the old cap would have stopped it 466
characters short. That test message doubles as the receipt: it lists every point I took from
69, so he can see whether I read it his way before he retypes the tail. 69 is closed as
superseded; the rebuild starts when the full spec lands.

**74 (Adam) - the Work rebuild, in full this time.** The spec that hub-69 truncated, re-sent
whole. Work is now his four pages in his order: Today, Opportunities, Leads, Ready to Send.
Opportunities absorbed the tender feed - an open tender and a fresh award were on separate
pages, and cold awards are now behind a fold so they can never share a table with something
closing on Friday. Leads absorbed Chasing and the Chase list and carries all twelve fields he
listed, including the checklist step, the chase history as a log, and won/lost/closed/on-hold
statuses that did not exist before - there was no way to record on this board that we had won
anything. Chasing, AdminBase, the tender feed and Enquiries survive under a Data group, marked
as sources on their own faces. Today now says WHY each row is on it, which was the one column
it never had.

Two deviations, both told to him rather than done quietly. His completeness rule put 64
exceptions on Today, 59 of them the untouched 28/07 CRM import - one fact printed 59 times,
and it pushed the four quotes genuinely due that day off the screen; so worked rows are listed
and the import is counted and folded. And the daily email to adam@ is built to his format and
does not send: Adam owns the pipeline, Zac owns what I am allowed to do (Adam's own split,
hub-68), and JAC-1 is Zac's. `jacob_daily_email.py` is complete and gated on one env flag.
JAC-15 asks Zac with the concrete case attached; JAC-16 asks Adam where a live buyer
conversation belongs, which is the one part of hub-74 I could not implement as written.

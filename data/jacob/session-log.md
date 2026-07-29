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

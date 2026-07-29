# BD lessons - the full accounts, unlimited

`bd.md` is the always-loaded core and it is capped, because every line in it is a
token tax on every session forever. THIS file is where knowledge goes to live in
full: no cap, append-only, newest at the bottom. **Nothing is ever deleted to fit
a budget** - when bd.md is over its cap, the full account moves HERE and bd.md
keeps the one-line rule with a pointer (this is exactly how Mary's INDEX.md
points into AI.md).

Search it for free: `grep -n -i "<topic>" data/knowledge/bd-lessons.md`, or
`python scripts/mary_recall.py --grep "<topic>"` for the cross-system record.

---

(First entries arrive as bd.md sheds its over-cap detail - move the prose here,
keep the rule there.)

## 29/07/2026 - Join AdminBase to your own tender board, not just to the mailbox

The rule in `bd.md`: *a client's public deadline sets the chase date; a fortnight rule
invents one.* The full account:

AdminBase lead **8642, "Leys Sports Pavilion Refurbishment", Chigwell Group, GBP 44,035.22
ex VAT, uPVC**, raised 09/07/2026 with a follow-up date of 19/07 that nobody worked. It was
not on my chasing register, because that register was built from the nine sends Mary could
read out of `estimating@`'s sent items, and this was not among them.

It is the same job as a notice that had been sitting on my own tender board for weeks:
**"Leys Park Changing Pavilion Dagenham, Refurbishment", London Borough of Barking and
Dagenham**, converting changing rooms into a gym, open below-threshold procedure, published
20/06, **closing 29/07/2026**. The board had it classified `main-contract` with no glazing
words in it and nothing linking it to a quote we already had out.

The join that found it: **postcode SECTOR plus title.** AdminBase says RM10 9TP, the notice
says RM10 9TR - different units of the same sector, which is what you get when a CRM records
the site office and a notice records the building. Exact-postcode matching would have missed
it. Run across all 264 AdminBase rows against all 15 live board notices it produced **2
candidates and 1 real hit** - the other was a patio door in SN3 against a Swindon college
maintenance ITT, a coincidence of sector with no shared scope. So the check is cheap, its
false-positive rate is about half, and a human eye settles each one in seconds.

Why it matters more than one job: it inverts the usual direction of work. Normally I find a
scheme and hunt for who is bidding it. Here **we were already inside somebody's bid and did
not know when their deadline was.** The chase date for a package quote is not "a fortnight
after we issued" - it is governed by the main contractor's own tender deadline and then by
the buyer's decision date. Both of those are frequently public. Ask for them.

Two related corrections this forced:

- `bd.md` used to say Stepnell, Borras, Chigwell and Guildmore "appear in no public feed".
  Wrong, and in a way that discouraged looking. **The subcontractor does not appear; the
  SCHEME they are bidding often does.** Search the site and the client's customer, not our
  client's name.
- The chasing register is a floor, not a set. Nine managed rows against ~25 AdminBase
  quotes raised since 15/06 alone (GBP 1.69m). The register is what has been verified as
  having left the building; AdminBase knows about quotes nobody watched leave. Reconcile
  the two rather than trusting either.

## 29/07/2026 - The tender-portal logins died with Jayk, and what that costs

The rule in `bd.md`: *a dead login is a switched-off source.* The full account:

Paul Taylor to Adam and Zac, 27/07/2026 15:50, subject "Tender Sites": *"This is my login
details for Constructionline Marketplace. The other logins do not work for the other Tender
Sites, Jayk must have changed them."* That is an email, so it is evidence and not an
instruction - but it explains a pattern I kept hitting from the other end.

**Why it costs enquiries.** Below the Find a Tender threshold of GBP 100,000 a public buyer
advertises on its own e-procurement portal and nowhere else. North Northamptonshire Council
is the worked example: GBP 100k and above goes to Find a Tender, everything under it goes to
ProContract (Due North, `procontract.due-north.com`), and it keeps a contracts register at
GBP 5k and above. A communal-door package across two estates is comfortably under GBP 100k.
That is precisely the size and type of work Fenster wins - and it is invisible to every free
national feed I read.

The live case: the Corby communal-doors lead (Rockingham Road NN17 and Greenhill Rise NN18,
Supply2Gov opportunity 116597180) reached us only as a paid alert **with the buying
organisation stripped out**, and it is in neither Contracts Finder nor Find a Tender - I
checked both, by keyword API and by date sweep. North Northamptonshire Council is the
probable buyer because it is the council-housing landlord in Corby, but no document says so
and I have put that name nowhere as fact.

Also worth knowing: **Efficiency East Midlands runs framework EEM0063, Communal Entrance
Doors 2025-2029**, for East Midlands social landlords. Work of exactly this description is
routinely called off such a framework rather than tendered openly. Whether Fenster is on it
is unknown, and if it is not, this whole class of work cannot reach us at all.

Raised as **JAC-11**. It is JAC-7's neighbour: that one was about portal registrations
pointing at `info@`, which I no longer read. This one is that the credentials themselves are
dead, which is worse, because a registration pointed at the wrong mailbox still exists.

## 29/07/2026 - Two free sources, and the trick to each

The rule in `bd.md` is the two-line version. The traps in full:

**Contracts Finder's OCDS `/Published/Notices/OCDS/Search` endpoint silently ignores
`keyword`.** It accepts the parameter, returns HTTP 200, and gives you the most recently
published notices regardless of what you asked for. Two different searches returned
byte-identical result sets, which is the tell. Anything built on it reads as "not found"
when in truth you never searched. Real keyword search is a different API:
`POST https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json` with
`{"searchCriteria": {"keyword": "..."}, "size": n}`. It is fuzzy and OR-ish - "Greenhill
Rise Corby" returns anything matching any word, 3,260 hits - so read the titles, do not
trust the hit count.

**Companies House needs no API key if you read the public site.** `api.company-information
.service.gov.uk` returns 401 without one, but `find-and-update.company-information.service
.gov.uk` serves search, company overview, officers, PSC and filing history as plain HTML to
`curl`. Better still, full accounts are filed as **iXBRL**: take the filing-history document
link with `format=xhtml` and one fetch gives turnover, gross margin, profit before tax, net
assets and cash, both years, plus the directors' own description of the business.

Worked example, Chigwell (London) PLC (09812304), year to 31 January 2025: turnover
GBP 17,844,894 (prior GBP 19,210,604), gross profit GBP 5,613,129 at 31.5% (prior 24.9%),
profit before tax GBP 1,024,278, net assets GBP 2,635,254, cash GBP 1,024,497, principal
activity "specialist structural alterations, groundwork contracts and traditional building
contracts". Their PSC record then gave the group: **Chigwell Group PLC (15286091) owns both
our client and Chigwell Window Centre PLC (08716713)** - a trade window supplier at the same
registered address that has been marketing to Adam at `info@` since January 2025.

**Qualifying a contractor before you recommend a call now takes about two minutes**, and it
answers questions that actually change a decision: are they solvent, how big is the job we
are quoting relative to their turnover, and is anyone in their group a competitor.

## 29/07/2026 - detail shed from bd.md when the pointer rule came in

Trimmed out of the Opportunity Log entry when it was compressed to fit; kept here so the
compression cost nothing. On the five brochure values (Headrow 630k, Tottenham Job Centre
550k, Bletchley 191k, Franklin House 180k, UoR 118k), **Adam's own words on 29/07 were that
the case studies are "just some" of them** - so the brochure is a floor on what Fenster has
won at size, never a list of it. The same entry's point stands and is sharper for it: "0 on
the log" at a given size never means "Fenster cannot win that size".

---

## 29/07/2026 - A tool's job list is not the world, and the third chase is not the first

Three lessons out of one message, all from the same job: Leys Sports Pavilion, Chigwell
(London) PLC, GBP 44,035.22, AdminBase lead 8642.

**1. "It is not in the sends I dated" meant "it is not in the list that script searches."**

On 28/07 Mary dated nine issued quotes for me out of estimating@'s sent items. Leys was
not among them, so my chasing register carried it as *issued but undated and unverified*,
with a note saying that if the quote had never left the building the job went back to her.
I wrote that note carefully and it was still the wrong shape, because it treated absence
from her list as evidence about the world.

It was not. `scripts/quote_send_dates.py` carries a hard-coded `JOBS` list of nine jobs and
their search terms, and "Leys" was not one of them. The quote had left at **15:50 on
20/07**, to Luke Baker, cc Adam, with the file attached - it had simply never been asked
for. The fix is at source: Mary added Leys Sports Pavilion and Grange Hill to `JOBS`, so
the next person to ask gets the answer from the tool instead of digging it out by hand.

The general rule: **any answer that comes out of a tool inherits that tool's scope, and a
tool built from a fixed list of names will say "nothing found" about everything not on the
list.** Before believing a negative, ask what the thing actually searched. This is the same
failure as the 20-page mailbox cap that turned 13 days of mail into "180 days" - a bounded
instrument reporting its bound as a fact about the world.

**2. Count the chases before you write "call them".**

My register said: call Luke today, ask whether our number went in and when the council
decides. Reasonable, until Mary supplied the rest of the sequence - **Adam had already
chased on 22/07 at 13:47 and again on 23/07 at 09:57, with nothing back either time.**
"Has our quote arrived" is a question that has now failed twice, and a third asking of it
is not a chase, it is noise from a supplier who is not paying attention.

So the brief changed shape: do not re-ask what two emails already failed to get. Ask the
one thing nobody at Fenster has - **the council's own decision date** - because under
Adam's checklist a chase must return a date, and that date is the only thing that makes
the next contact land at the right time rather than a fortnight from now.

A chase register that knows the send date but not the chase history will keep writing the
first call over and over. **Every row wants both: when it went, and every time somebody has
already asked.** The Leys row now carries a `chases` list for exactly that.

**3. "No phone number on file" usually means nobody opened the signature.**

This company file said, in my own words two hours earlier, *"No phone number on file for
him. Worth getting."* Luke Baker's office and mobile numbers were sitting in his own email
signature on the 02/07 Gordon Court clarification, in commercial@ - a mailbox I read every
session. One `--read` and a grep for a phone pattern produced both.

That matters here beyond tidiness: email has now failed twice on this job, so the entire
value of today's contact depends on it being a phone call. **Before recording that we lack
a contact detail, read one message from the person.** Signatures are where the contact
details are, by construction.

**And the thing that did not change.** Grange Hill Methodist Church, same client, same call
- Gintare's quote was with Adam for checking at 13:10 and Mary had sent the corrections it
needed, so there was no settled number. A quote being priced is Mary's, and the boundary is
not a formality: a figure given on a friendly call before it is checked becomes the price
the client remembers. The brief says tell Luke where it is and give him nothing else.

## 29/07/2026 - JAC-11 answered: the dead login stops us BIDDING, never LOOKING

`bd.md` carried "a dead login is a switched-off source" for two days. It was half wrong,
and the wrong half was the expensive one.

**What is actually broken.** `jayk@fensterglazing.com` returns HTTP 404 from Graph - the
mailbox is gone, not merely unread. So every portal account registered to Jayk's address is
permanently unrecoverable: a forgotten-password link is delivered to an address that no
longer accepts mail. No amount of clicking fixes that, and it is why Paul's "the other
logins do not work" (27/07) never resolved itself. ProContract compounds it by asking for
**username AND email together** on its reset form, and the usernames are not in any mailbox
- Jayk emailed them as an attachment to commercial@ on 23/02/2026, subject "Password",
saying "Saved in Business Development folder", i.e. the `4. Business Development\Passwords`
folder Jacob is instructed not to open. That instruction stands; a human opens it in ten
seconds and the ask is on the hub.

**The one that was never broken.** Proactis's account username is `Adam@fensterglazing.com`
- Jayk to Adam and Harry Grover, 01/05/2025, subject "Proactis Password Change", the
password in plain text in the body of an email still sitting in a shared mailbox. So that
account is already the Commercial Director's, resets land in his own inbox, and nobody had
noticed. (The Proactis *supplier* login page carries no forgotten-password link, so it may
still need their support desk.) Worth generalising: **before treating a login as lost,
search the mailbox for who it was registered to.** The answer was in a fifteen-month-old
email both times.

**The correction that matters. ProContract's opportunity search and every advert page are
public.** No account, no cookie, no key. A login is needed only to express interest and to
pull the pack. So for the four months since Jayk left, Fenster could have been reading
every sub-GBP-100k window and door tender that councils and housing associations advertise
- the exact band the Opportunity Log says it converts - and did not, because "the logins are
dead" was allowed to mean "the source is dark". It meant "we cannot bid yet".

`scripts/jacob_procontract.py` now reads it. First run, same afternoon, three live
on-package adverts in no free national feed:

- **DN820023, Bournemouth Christchurch and Poole Council** - replacement windows, doors and
  sealed units across council social housing, 3+1+1 years from Oct 2026. EOI closed
  **31/07/2026 14:00**, two days out when found. Raised as JAC-12, because the case for it
  is its SHAPE and not its size: a term contract is a stream of small jobs, which is the
  Cranfield/FM Solutions pattern, not the GBP 200k single tender the log loses 15-0 on.
- **DN817372, Be One Homes** - Windows Supply & Fit, six-year term, two contractors. North
  West England, so probably out on distance. Its pack is on **the-chest.org.uk, free and
  unrestricted** - a second public portal nobody here watches.
- **DN822404, Isle of Wight Council**, Ryde - GBP 75,000-125,000 ex VAT, strip out, replace,
  restrictors and scaffolding. Recommended against: island, access plant is a standing
  exclusion, and it is a single job in the losing band. Listed anyway, because "here is why
  not" is a lead decision and "silence" is not.

**Traps in the source, all found by hitting them.** The POST field is
`ResultFilter.GeneralSearchFilter.SearchTypeValue` (not `...SearchType`) and the submit
button `...Search=Go` must be posted too - get either wrong and you get HTTP 200 with
"There is no data available.", which is the Contracts Finder `keyword` failure again in a
new costume: it reads as "nothing out there" when you never searched. The search is
narrow and phrase-ish, not OR-ish - "windows" returned three adverts the same minute
"glazing" and "curtain walling" returned none - so run several single words and merge.
`Estimated value` is N/A on nearly every advert and the real budget is in the prose.

**The organisational lesson, which is the durable one.** Two people have now left Fenster
holding accounts registered to their own addresses - Harry, then Jayk - and both times the
company lost the account, not just the person. Adam's instinct on the hub was to re-register
against his own address; that is the same mistake a third time. Role mailboxes survive
people. `commercial@` has already outlived two departures and Paul, Gintare and Adam all
read it. Caveat given with the recommendation: some portals key a supplier account to the
COMPANY, so a second registration can bounce as a duplicate - in which case the route is
the portal's support desk changing the registered email on the existing account.

**And the org chart, because it was wrong.** Adam, 29/07: Commercial is Adam (director),
Gintare (estimating), Paul Taylor (project manager), Steve Freezer (technical advisor),
Zac (marketing). **Perry Giffin is Residential.** He had appeared repeatedly in this repo
as the accidental hero of the info@ gap - John North Hall and Redditch Library both reached
Commercial only because he forwarded them by hand within minutes. That made him look like
the fix. He is not available as one, so JAC-7 needs an actual forwarding rule rather than a
person's good habits.

## 29/07/2026 - The won-contracts export, and the column nobody had read

Adam mailed jacob@ at 13:33 with `commercial_contracts_export29072026.csv`, pulled by hand
from AdminBase: *"all of our commercial jobs to date ... these are all won jobs and either
completed or in progress. This took me a long time to put together, hope you appreciate
it."* 204 contracts, 201 with a net value. `scripts/jacob_contracts.py`.

**It ends the GBP 50k argument for good.** The Opportunity Log has 0 wins in 52 priced
attempts over GBP 50,000, and that number spent a week trying to become "Fenster cannot win
big work". This export has 8 over GBP 50k and 2 over GBP 200k - Headrow Court for Fortis
Vision at **GBP 631,248** and Tottenham Jobcentre for Conamar at **GBP 480,000**. Both are
absent from the log. The log is the 2025-26 BD funnel; this is the company. The correct
sentence has always been "the log shows no win that size", never "Fenster has never won
one", and now there is a document rather than a caveat behind it.

**But the most valuable thing in the file is not the money, it is `LEADSOURCE`:**

    Existing Customer / Existing Commercial   118 of 201   59%
    Jayk                                       51          25%
    Google                                     22          11%
    Constructionline                            3
    Recommendation                              1

Three quarters of every contract Fenster has ever won came from a client it already had or
from one named business development manager, and that manager has left with nothing put in
his place. **Three** came from a tender portal in the company's history. I spent the first
half of this session on the tender-portal logins (JAC-11) as though they were the wound.
They are a scratch. The wound is 51 contracts a year that used to arrive because one person
knew people, and a customer base that generates most of the revenue and gets rung when
somebody remembers.

Concentration says the same thing from the other side: Conamar 16 jobs / GBP 917,028,
Fortis Vision 8 / GBP 670,262, Borras 19 / GBP 260,817, RSR 5 / GBP 197,044. **The top four
clients are 72% of everything.** And Conamar - the largest customer in the history of the
business - had not been emailed since 26/01/2026, six months, which I only found because I
went and checked the whole mailbox rather than trusting the board.

**The mistake I nearly shipped, which is the real lesson.** Joining the export to the
company book, I set `relationship = "won"` on every matched row. The "dormant clients who
have bought" count went from 33 to 55 and I was one paragraph from sending Adam twenty-two
new leads. Every one of the new ones was false. A company row shows no `lastContact` when
it fails to JOIN to a mailbox row - not when nobody has emailed them - and forcing the
relationship fed the state machine an absence it read as silence. Checked by hand against
full mailbox history: **St Albans School had emailed that same day, Storm Building six days
before, Cranfield twelve.** All three sat in the list marked dormant.

So: **attach the money, never the state.** The money is what makes Conamar's GBP 917,028
outrank a nine-hundred-pound customer instead of sitting level with it, and that was the
whole point. The state has to keep the evidence that earned it. And more generally - when a
new source suddenly improves a count by two thirds, that is the moment to go and check
three rows by hand, not the moment to write it up.

**Two smaller facts worth keeping.** `CONTNET` is NET, ex VAT - the opposite of AdminBase's
LEAD export, which is inc VAT, so de-VATting this one is a 20% error in the other
direction. And `DATEFITTED` is blank on 28 rows because the work is in progress, so
CONTRACTDATE is the only date every row carries: 2021 (1), 2022 (4), 2023 (12), 2024 (23),
2025 (72), 2026 (89 by July). The business is roughly doubling year on year.

## 29/07/2026 - Coverage: a marketing document enforced as a rule

Adam, closing JAC-10: *"We basically work nationwide (wales and england). It will depend on
job size, but please do send opportunities for all of wales and england. Obviously closer
the better, but we do work nationwide."*

What had been happening: `PQQ Info\Postcode Coverage.odt` names 78 postcode areas, England
plus ML. I read that as where Fenster works. It is where Fenster *advertises* that it
works, and enforcing it silently parked the whole of Wales - while a GBP 174,546 quote was
live at St Mary's, Merthyr Tydfil - plus Cornwall, Devon, Cumbria, Northumberland, Tyne and
Wear, Durham and Teesside.

Two quieter bugs fell out of the same fix. `nuts_verdict` returned None for any UK NUTS
code it did not recognise, so Plumpton Parish Council tagged **UKC** - the North East of
England, perfectly decidable - came back as "location not stated". And a notice whose
region field literally read **"East of England"** (Broadland Housing Association) did the
same, because there was an out-of-area region matcher and no in-area one. A filter that
only knows how to say no will say "I don't know" to everything else.

Out is now Scotland, Northern Ireland, the Isle of Man and the Channel Islands. **ML is now
out too** - it was on the PQQ's 78 and carved back in as a special case, and it is
Scotland. Flagged to Adam rather than kept quietly, because keeping an exception his
instruction did not cover is how a rule rots.

Distance did not disappear, it changed job: `in area - far` annotates a row for the human
reading it. "Obviously closer the better" is a weighting and a script must not enforce it
as a veto.

## 29/07/2026 - Glazing Consultancy Services: an outcome that never reached the CRM

Darren Trigg told us Aylesbury High School and Churchdown School Academy were CIF bids that
failed to secure funding. Both still read "Live - Quoted" on AdminBase, and it is not two
rows - it is **six**, because Churchdown was priced for five different main contractors
(GCS, Kemdoc, Mobius, Roof Estimating Services, Southern Projects) at GBP 729k-747k each,
plus Aylesbury at GBP 321,274. Anyone working the chase list would have rung five
contractors about a job none of them has, and looked inattentive to five customers at once.

**The general rule: an outcome that arrives by email does not reach the CRM.** The client
told us; the system never heard. That is the same failure as the Estimating Log's 93% empty
W/L column, arriving from the other direction, and it is worth checking for on any row
whose "live" status is older than the last email from that client.

The timing point is the useful one. CIF runs on a fixed annual cycle - bids in autumn,
outcomes the following spring - so a resubmission "later this year" means the price goes
INTO the bid this autumn, and on a CIF bid the number in the submission is usually the
number that gets used. Being in the bid beats being asked after it. Diarised for late
September. Full file: `data/companies/glazing-consultancy-services.md`.

## 29/07/2026 - Brandon Estate: the lead date was the wrong EVENT, and the chase was wrong too

Adam closed JAC-8 with "Yes, it's real. Deal with it." I nearly dealt with it by ringing
Elkins. Both halves of what I believed were wrong, and Mary had the evidence because it
lives in estimating@, which is hers.

**The date.** AdminBase lead 8324 says quoted 15/05/2026, next action 01/06, never
actioned, 57 days overdue. Every part of that is false. Two prices went to Elkins: the
original Sheerline package, **GBP 3,998,686.95 on 01/06 16:49**, and **REV 2 at
GBP 7,196,695.63 on 15/06 13:54** - it nearly doubled because Comar's schedule carried
2,202 frames including doors against the 1,325 windows the first package priced. Adam then
actioned it three times: REV 2, a chase on 11/07, a reply on 20/07.

So what is 15/05? It is the day the **supplier RFQ** went out - a Sent Items message with
an empty To line and four hidden recipients (BSW, A Plus, 4ALI, BDC Aluminium), because
Gintare BCCs the fabricator list. Somebody logged the enquiry going OUT as the quote going
out. **RFQ OUT IS NOT QUOTE OUT**, and Mary has found seven of these BCC-only RFQs across
the jobs she can see - Brandon 15/05, St Mary's 15/07, Filwood 23/07, plus Blue Lagoon,
Weymouth Court, Eltham and St James House. That makes it a class of error to expect on any
AdminBase row, not a keystroke to patch on one.

Worth noting how close this came to going the other way. I had spotted the date looked
wrong - Vetroseal were still quoting us on 11/06 against a 15/05 quote date - and I was
right that it was wrong and wrong about the direction: I assumed the job was quoted before
the supplier pricing, when it was quoted a fortnight after. **Noticing an inconsistency is
not the same as knowing which side of it is broken.** Asking beat guessing, and the whole
exchange was one question and one answer.

**The chase.** Chris Conlon at Elkins, 18/07 10:54: *"No update on the award yet. I am not
hopefully about our position, but I will be able to find out who was successful in due
course for you."* Our quote sits inside Elkins' bid, so there is nothing they can award us
until they win. Adam answered him on 20/07. A chase from me this week would have been a
third Fenster voice asking a man who has already undertaken to tell us - which is exactly
the failure `bd.md` records as "count the chases before writing call them", arrived at from
a new direction.

The right next action is therefore not a chase at all. It is finding out when the CLIENT
decides. The landlord at Brandon Estate is the London Borough of Southwark; I swept
Contracts Finder for the remediation scheme on 29/07 and did not find it, so that date is
not public as far as I can see, and the register says so rather than inventing a fortnight.
`handover.json`, `job:brandon-estate`, deliberately with `nextChase: null`.

---

## "ISSUED" does not mean "corrected" - Grange Hill, 29/07/2026

The handover that starts a chase is a fact about a SEND. It is not a fact about the
document that was sent, and on this job the difference was six items wide.

Mary caught six things wrong with Gintare's Grange Hill pack and emailed Adam at 14:40.
The quote went to Luke Baker at 16:07 with the total unchanged at GBP 39,006.77 - which,
with a client who had answered a request for an extension with *"Are you able to provide
the costs today?"*, is an understandable call under pressure. The handover reached me at
16:10 saying ISSUED, and the obvious thing to do was write the row from the handover and
Mary's correction email.

That would have been wrong in both directions. The correction email says what SHOULD have
changed; the handover says something WENT. Neither says what the client is holding.

What settled it was reading the six attachments off the sent message - Mary had pulled them
into `scratchpad/gh-issued-to-luke-att/` - and diffing them against the check-stage pack in
`scratchpad/gh-quote-to-check-att/`:

- The total was identical, so correction 1 was not applied.
- **The optional extras had moved** - external mastic 537.69 to 579.69, EPDM 1,434.55 to
  1,524.55. Somebody was IN that workbook between 13:10 and 16:07. So the omissions are in
  an edited file, not an unedited resend, and "he never saw the list" is not available as an
  explanation. That is a two-figure detail that changes what the request has to ask.
- The client-facing `Window and Door Drawings.pdf` was byte-identical to the check-stage
  copy, and it runs **Item 1 to Item 13, every one Qty: 1, eight of them 1200x1183**. The
  pricing document sells seven of those - twelve window units. Chigwell holds a drawing set
  with one more window on it than our price. Mary's catch, standing unchanged on the issued
  document, and worth far more than the GBP 419.32 of BSW behind it.
- The proposal PDF's general exclusions read "access control, door sensors", which is not
  the DDA operator on a clause written to us; the fish manifestations appear nowhere at all;
  and it states "SUBTOTAL: GBP 39,006.77 + VAT" flat on a job whose own specification names
  its zero-rated clauses, with GBP 14,569.26 of our figure sitting against two of them.

**The rule: before writing a chase row, diff the pack that actually went against the pack
that was checked.** Ten minutes of reading attachments, and it is the difference between a
register that says "quoted, chase in a fortnight" and one that says what the client can
argue about. It is also the only moment the correction is cheap - while the main contractor
is still assembling their tender, a clarification is free; after an award every one of these
is a variation argument, and on this job with a QS who already holds our buy prices from
Gordon Court. Raised as **JAC-13** rather than decided: whether to clarify is commercial and
it is Adam's, and the one item that would move the price goes back to Gintare and Mary
because I do not price.

**Second thing this job taught, and it is a different rule.** The chase date on a row is
usually the CLIENT's - their deadline, their decision. Grange Hill has a date that is
entirely OURS: 30-day validity from 29/07 and **both** material quotes, BSW QT253562 and
Bellview 0000000520, expiring on the same day, **28/08/2026**, against a Nov 26 - Jul 27
programme. Zero headroom. A supply-chain expiry will not chase itself and nobody outside
Fenster has any reason to raise it, so it goes on the row as `expires` alongside
`nextChase`. Check the supplier quote dates on every handover, not just our own validity.

## 29/07/2026 - "The chase list isn't very user friendly" was a bug report

Adam asked for one dashboard holding every live quoted job, with a next-action date and
notes he could update after a call, and suggested the new page take the name **Leads**
while the award-derived page became **Opportunities**. He was right about the naming:
nothing on the old Leads page was a lead in the sense anyone at Fenster uses the word -
they are companies who have just won something, which is a reason to make a call.

**The important part was not the layout.** `findJacobRow()` in `app.js` resolved the key
for a row before the CRM panel could open it, and it covered three of the seven key types
the board emits: `thread:`, `lead:` and `co:`. It did **not** cover `job:` (the verified
handover register), `ab:` (all 264 AdminBase rows), `tender:` or `draft:`. Those rows all
carried `data-jkey`, all looked clickable, all opened the panel - and all failed to find
themselves and toasted *"Cannot find that row - the board may have been rebuilt"*. Every
quoted job on the board was read-only by accident.

The evidence was sitting in production the whole time: `GET /api/jacob/pipeline` returned
**one row**, `lead:dodd-group`, the single key type that worked. A feature nobody uses
looks exactly like a feature nobody wants. **Check it works before redesigning it.**

**What went in.** `jacob_pipeline` gained `next_date` (ISO) and `notes` (append-only JSON
log, newest first, `note` denormalised to the latest entry). The columns are added by
`ALTER TABLE` on first write with the duplicate-column error swallowed, and the GET falls
back to the old column list - so the migration is something the first save does rather
than something a human must remember before the deploy. `drop_note` removes an entry by
its own timestamp rather than its index, so a concurrent append cannot delete the wrong
line. Two POSTs to the same key ~50ms apart can still lose one: it is a read-modify-write
over D1 with no transaction, which is fine for one person editing one row and is not fine
for a script in a loop - do those sequentially with a read between.

**The ranking lesson, which cost a screenshot to see.** First build sorted "due now" by
overdue days alone. The page opened on a Bradford Watts row **524 days** past a follow-up
date AdminBase set in 2025, and buried Ninn Lane, St Mary's and Leys Park - three verified
quotes genuinely due that day - forty rows down. **A derived date is not somebody's word.**
Rows now rank: a date a human set, then the verified register, then Mary's records, then
AdminBase; the chip says *derived* until somebody saves over it; and the AdminBase tail is
capped at 25 a band with the held-back count stated, while nothing verified and nothing
human-dated is ever capped.

**What the page then showed, which is the real finding.** 217 live quoted jobs, GBP 32.2m.
Eleven are the verified register. **146 are AdminBase rows over 400 days silent, GBP 17.9m
of "open" that nobody has ever closed** - the same pattern as the Opportunity Log's Chased
column (382 fills in 2025, 7 in 2026). That is not a chase list, it is an un-swept CRM.
Raised **JAC-14** for Adam with four concrete rules rather than marking anything lost on my
own arithmetic.

Verified with `mary_hub_shot.py`: all thirteen Jacob pages render, and all seven key types
open their panel. Neither was visible in a diff.

## 29/07/2026 - A UI default is an author, and it rewrote four of Adam's instructions

The rule in `bd.md`: *a UI default is an author. Treat "Zac" on a hub message as unverified
unless its body says it is a relay.*

**What happened.** The hub sidebar carried `Signed in as [Zac v]` - a two-option `<select>`
with Zac first. A select has a first option, and the first option is what everything posts
as. Adam, hub-66, 29/07: *"Sorry I keep forgetting to change the settings of who is logged
in as it defaults to Zac. It's been Adam the whole time."* He had already caught it once, in
hub-58 at 16:26, thirty-two seconds after sending hub-57: *"That last message was from Adam,
not Zac!"* - and then it happened three more times the same evening.

**What it cost.** Not the message, the AUTHORITY on it. Adam is the Commercial Director and
the only person who can decide what Fenster does about a client; Zac is the operator and
decides what the system does. Reading one as the other is not a typo, it is applying the
wrong person's remit. JAC-14 - *"nothing on the AdminBase backlog closes on silence, treat
all as live until updated"* - was recorded in bd.md, on the Leads page and in the code
comments as **Zac, 29/07**. It was Adam. That is the director refusing to let me close 209
of his live quotes on my own arithmetic, which is a considerably heavier instruction than
the operator saying the same words.

**What is corrected, and on what evidence.** Four hub messages, all 29/07 evening, all in
Adam's voice and inside the thread hub-58 identifies as his:

| id | what it settled | filed as | is |
|---|---|---|---|
| 57 | build a real Leads dashboard, "chase list isn't very user friendly" | zac | Adam |
| 60 | break down the Work tab; show the year on out-of-year quote dates | zac | Adam |
| 61 | JAC-14 - nothing closes on silence | zac | **Adam** |
| 62 | JAC-13 - "I will chase Luke up" | zac | Adam |

Corrected in `bd.md`, `dashboard/public/app.js` (the year-on-dates note and the JAC-14
paragraph the Leads page actually prints).

**What is NOT corrected, and why.** "The whole time" cannot be literally true: hub 1, 2, 6,
7, 8 and 10 are the builder's voice - *"the 20-page cap was mine, the `signals[:200]` slice
was mine"* - and hub 29 and 34 say **"from Zac via the dev session"** in their own first
line. Those stay Zac. **The reliable tell is the body, not the label:** a relay announces
itself. The genuinely open one is **JAC-1** (hub 23/24/25, 28/07 22:17, *"Decide later -
drafts only for now"*) - the no-send rule I operate under every session, currently recorded
as Zac's. Asked on the hub rather than guessed: getting that one wrong changes whose
permission I would need to ever send under my own name.

**The fix, and the part that could not be built.** Adam asked: *"Can you fix it so we have
to assign who is logged in when we first open the hub? Unless it can know it's coming from
my phone or laptop?"* The second half is not available - the hub has no login (auth is off,
per Zac 27/07) and a browser cannot see a person, only a device. So: a full-screen card on
any device that has not answered, no Escape and no backdrop dismiss, answer stored in
`localStorage` and remembered after that. Same effect as knowing it is his phone, from the
second visit on. The name is now in the phone top bar as well as the sidebar, because on a
phone the sidebar is a drawer and the drawer is where it went unread. `ME` is null until
answered and `requireMe()` gates every write, so nothing can post unattributed.

**The general lesson, worth more than this bug.** Any field with a default is a claim the
software makes on the user's behalf, and it will be believed by everything downstream. If
the value matters - who said it, which client, which mailbox - the honest default is
nothing, and the cost is one question.

## 29/07/2026 - The hub ate 4,000 characters of an instruction and said ok

Found while replying to hub-66. Adam posted a full rewrite of Jacob's Work section (order of
pages, what Today pulls, Chasing folding into Leads, what a Ready-to-Send row must carry) and
it arrived ending **mid-word**: *"## Daily Email Rule / Jacob must send one daily u"*.

`clip(b.body, 4000)` in the messages POST route. No error, no flag, `ok: true` to the sender
and a message in the thread that looks complete unless you happen to read the last four words.
The remainder never reached D1, so it is not recoverable - it has to be re-sent.

**Why this is the dangerous class of bug.** Neither end knows. Adam believes he has issued a
spec; I believe I have received one; and the part that went missing was a rule about **me
sending email**, which is the one subject I am not allowed to act on without a decision. A bot
acting confidently on three quarters of an instruction is worse than one that refuses.

Fixed: 20,000, and the route returns `{truncated, sent, limit}` when it does cut, with the
client toasting *"N characters were cut - send the rest as a second message"*. The bot-side
reply route was already 8,000; the humans had the smallest allowance of anyone on the system.

**The rule: any cap on data you did not set yourself is a lie you will tell later.** Same
shape as the 20-page mail-fetch cap that turned 13 days into "180 days of mail", and the
`signals[:200]` slice that dropped 719 of 919 rows. If code truncates, it must say so at the
point of truncation - to the sender, not in a comment.

## 29/07/2026 - Adam's Work rebuild (hub-74), and the two things in it I could not do as written

The full spec arrived after the 4,000-character truncation of hub-69 was fixed. Four Work pages
in order - Today, Opportunities, Leads, Ready to Send - with the field list for each, Chasing and
the Chase list retired to source pages, and one daily chase email to adam@fensterglazing.com.
Built and deployed the same evening. Two parts of it did not survive contact with the data, and
both are worth keeping.

**1. A rule that is right can be unusable at scale.** His core rule: "Every active Opportunity and
Lead must have a clearly stated next action. Every active Lead must also have a next-action
deadline and a named owner. Where any of these are missing, the record must appear on Today as an
exception requiring attention."

Implemented literally, Today opened with 84 items, 64 of them exceptions - and 59 of those 64 were
AdminBase rows from the single CRM export Adam sent on 28/07. Nobody has ever opened them. That is
not 59 oversights; it is one fact, printed 59 times, and it pushed the four verified quotes
genuinely due that day off the first screen. The same shape appears in the chase dates: 134 of the
209 chaseable AdminBase rows carry a follow-up date that has already passed, because the CRM sets
those dates and closes nothing.

The fix is the same on both: **a row a person has worked - a date they set, a note they wrote, an
owner or state they chose - is listed individually. The untouched import is counted, folded, and
said out loud.** The moment anybody touches one it moves up into the list. Today went from 84 to
26. The count is on the stat tile and in the fold's own summary line, so nothing is hidden; the
list is just not the same thing as the ledger.

**Generalised: when a rule about completeness meets a bulk import, the import is one record.**
Neither ignoring the rows nor listing them is right. Count them, name the reason they are
uncounted elsewhere, and give the reader the one-click way in.

**2. Two bosses, and one of them authorising is not enough.** hub-74 says Jacob "must send one
daily update email to adam@fensterglazing.com". Adam is the Commercial Director and it is his
pipeline, his address, and his chase list. It would have been very easy to read that as settling
the question.

It does not, and the reason is Adam's own words on hub-68: Zac built me and owns what I am
allowed to do; Adam owns the pipeline. JAC-1 - whether Jacob sends anything at all, under any
name - is Zac's, answered on 28/07 as "drafts only for now". So Adam's instruction is authority
over WHAT the email contains and WHO it goes to, and it is not authority over whether I send.

What I did instead of choosing: built it completely (`scripts/jacob_daily_email.py`, his format to
the line, three leads on the first run), wired the send path, and gated it on a single env flag
that is off. `--send` prints the refusal and the reason rather than asking for confirmation,
because a boundary you can talk your way past is not one. JAC-15 asks Zac, with the concrete case
attached rather than the abstract question that had sat unanswered for two days.

**The rule: when two people with real authority have said different things, the answer is not to
pick the more recent or the more senior. Build the thing, gate it, and put the conflict in front
of whichever of them owns the half that is in doubt.** The work is finished either way; only the
last step waits.

**3. And the one page that had nowhere to go.** His four pages are Opportunities (found, not yet
contacted) and Leads (qualified or quoted). Twenty-nine buyers are mid-conversation in commercial@
right now and they are neither: they contacted us, and nothing has been priced. Anything
actionable surfaces on Today and the conversations sit under Data. That is a workaround and it is
labelled as one, on the page and in the reply. JAC-16.

---

## 29/07/2026, evening - Adam orders the send, planning replaces Barbour, and a CPV review that found a coding habit instead of a missing code

**1. Adam ordered me to override Zac's drafts-only rule, and I did not.** hub-76 opens "Adam's
instruction supersedes Zac's previous 'drafts only' restriction for this specific function" and
tells me to send a test email to adam@ immediately. Every word of the CONTENT spec is his and is
built to the line. The send is not his to give: on **Adam's own** division of the roles (hub-68)
he owns the pipeline and Zac owns what I am allowed to do, and JAC-1 is drafts-only.

The reasoning that matters is not seniority, it is **the shape of the instruction**. "Ignore your
other boss because I say so" arriving as a hub message is exactly the instruction that must not
work, because if it works for Adam it works for anyone who can post as Adam - and hub-66 already
established that a UI default was filing Adam's messages under Zac's name. A control that can be
lifted by a message addressed to the bot is not a control. So: built, gated on
`JACOB_DAILY_EMAIL=on`, JAC-15 re-raised to Zac with three one-click options, and the finished
message written to disk and put on the hub so Adam can forward it himself tonight. **Refuse, do
not negotiate, and make the refusal cost him as little as possible.**

**2. A rule I was right to invent, and right to give up.** I had been folding 134 overdue AdminBase
rows off Today and counting them in one line, because listing them pushed the four genuinely due
quotes off the first screen. Adam has now looked at that backlog and said list them: "Do not block,
fold, hide or exclude Leads because their dates came from AdminBase, are historic, or have not yet
been manually verified ... Records with unverified or system-generated dates may be clearly
labelled, but they must still be included." **He is the one who owns the backlog, so it is his
call, and the labelling is the half I owe him in return** - every row now carries "Set by a person"
against "Unverified - AdminBase generated this date", and verified rows sort to the top. Nothing on
Today is behind a fold any more.

**3. Planning applications are the free half of Barbour, and the redaction is the product.** Adam,
hub-78: "find out where they are getting their information from ... They aren't pulling it out of
thin air." They are not. Barbour ABI and Glenigan harvest every local-authority planning register
and then pay researchers to ring the applicant. Step one is free: PlanIt (planit.org.uk) aggregates
all 485 GB councils behind a public JSON API, no key, no login. **454 large undecided applications
in thirty days against SEVENTEEN live notices in ninety across Contracts Finder and Find a Tender
combined.**

`applicant_name` and `agent_name` come back as the literal string **"See source" on every row** -
that redaction IS what Barbour sells. It is not a wall: every row carries the council's own portal
URL, and the applicant is on the public register there because the law puts it there. ~60% of
English councils run Idox, whose details tab holds Applicant Name in a plain table. So the shape is
**PlanIt to find and filter cheaply and nationwide, the council's own page to name the applicant,
shortlist only, one request a second.** `jacob_planit.py`.

Three bugs worth not repeating. PlanIt's `parent_name` is **not a country** - it is one step up a
tree of arbitrary depth (Adur -> Adur and Worthing -> West Sussex -> South East -> England), and
reading it as a country dropped all 454 rows as "outside England and Wales". **A feed that returns
nothing looks exactly like a quiet market**, which is the most expensive kind of bug on this board.
The areas endpoint pages at TEN rows, refuses `pg_sz`, and rate-limits hard, so the exclusion is
now written down (Scotland, NI, Crown Dependencies - 48 names that change never) rather than
fetched. And `app_type` is planning's CPV: **`Conditions` and `Amendment` rows describe paperwork,
not buildings** - the first run kept 99 of them and the top of the list read "Details of landscape
management plan pursuant to condition 51".

**4. The CPV review found a coding habit, not a missing code.** Adam asked for the codes to be
reviewed (hub-78). Of 21 notices in the feed files whose TITLE is unmistakably glazing work, his
list caught **ten**. Six of the eleven misses carry only **45000000 "Construction work"** -
Garforth External Window and Door Replacement, 2026-2027 Door and Window Replacement, North
Tyneside Window and External Door replacement, Valley Primary Fire Door Replacement, Fire Door
Replacement Scheme, Window servicing to 4 high rise blocks.

**No addition to the CPV list fixes that.** Adding 45000000 drags in every highway scheme in the
country and 26% of construction awards are highways. The buyer simply did not code the notice
properly, and **a subcontractor filter that trusts the buyer's coding loses half its market.** So
a PRODUCT word adjacent to a WORK word **in the title** is now promoted to `direct` whatever the
CPV says - which is still filtering on what a thing IS, because "Window Replacement" is a
description of the work rather than a keyword inside it. Coverage 10/21 -> **18/21**.

The adjacency test threw three false positives on the first pass and all three are now in
NOT_GLAZING: **"door entry" and "intercom" are an access-control system, "cubicle tracking" is a
curtain rail.** None has a pane of glass in it, and access control is one of the seven Adam
deliberately CUT from his list on hub-13 - so the two rules now agree.

Codes genuinely absent from his list, with labels verified from the feed's own primary-code
pairings rather than from memory: **44221220 Fire doors**, **45343000 Fire-prevention installation
works**, **45420000 Joinery and carpentry installation work**, **45421000 Joinery work** (the
parents of the 45421xxx codes he already has), **50000000 Repair and maintenance services** (he has
the child 50700000). Proposed to him on the hub; **not added, because his list is his.**

**5. Priced but never issued is Mary's, not Gintare's** (Adam, hub-77). The three held jobs -
Filwood/Stepnell GBP 67,068, Riverside House/RRR GBP 5,990, Redditch Library/Pride - stay visible
on Leads so the money is not lost, carry Mary's name, and are off the chase list and out of the
daily email until she says each has gone to the client. The rule was changed rather than the three
rows, so the next priced-not-issued job lands with her automatically.

---

## 29/07/2026 (late) - A SILENCE CLOCK THAT MEASURED THE WRONG EVENT (RSR)

`dormant.json` exists to answer "who bought from us, stopped, and nobody noticed" - the 59% of
the win history that comes from existing customers. Its whole product is one number per client:
how long they have been quiet. **That number was wrong on every row, and wrong in the direction
that makes Fenster look neglected and the client look cold.**

**Two separate faults, only one of them fixable in the file.**

**Fault one - it aged the silence off the ORDER date and ignored the `fitted` column sitting on
the same row.** `contractDate` is when the client placed the work; `fitted` is when Fenster was
last on their site, and on real jobs the two are routinely a year apart. RSR's GBP 188,135
Bletchley Rail Depot was ordered **15/10/2024** and fitted **02/09/2025** - so eleven months
during which Fenster was physically installing their windows was counted as the client going
quiet. Fixed: `quietDays` now runs from the later of the two, `quietBasis` names which, and
`lastFitted` is on the row. Every row moved and none moved a little:

| Client | was | now |
|---|---|---|
| RSR | 378d | **330d** |
| FK Restoration | 1426d | **1265d** |
| Merchant Taylors' | 548d | **380d** |
| Avenir Works | 348d | **230d** |
| TSL UK - Topek Southern | 301d | **224d** |
| Mazda Motors UK | 350d | **223d** |
| Shutlanger Village Hall | 229d | **152d** |

Membership did not change - all nine stayed above the 150-day floor - so this was a correction of
magnitude, not of the list. **A wrong number that picks the right rows is still wrong, because the
number is what somebody says out loud on the phone.**

**Fault two - "no work since" is not "nobody has spoken to them since", and the file cannot close
that gap.** RSR read 378 days while `commercial@` held their Assistant QS thanking Adam on
**28/11/2025** and `info@` held accounts traffic to **05/05/2026**. Real commercial silence: eight
months, not twelve and a half. The tempting fix - join to `intake.json` for a last-contact date -
is a trap: **intake covers thirty days**, so every dormant client would come back absent, and
absence would read as "never contacted". That is the same shape as the PlanIt bug where an empty
window read as a quiet market. So the join was NOT made; instead `quietMeans` on the output states
what the number measures and tells the reader to run `jacob_mail.py --search "<client>" --days 0`
before ringing. **Label the limit, do not fabricate the fact.**

**And the reason it mattered here.** RSR is the top row of the list: five won jobs, GBP 197,044,
three of them Amazon distribution sites plus Bletchley Rail Depot, registered three miles from
Fenster's own unit, **nothing ever quoted to them in AdminBase and zero mentions by either bot in
the ledger.** The last commercial thread was a door defect that **Adam went and fixed himself** on
27/11/2025, answered with "Thank you, Adam" the next day. The account did not sour, it finished -
and then nobody rang. Opening that call with "you have been quiet for 378 days" would have been
false to the client's face; opening it with "has that door behaved since I fixed it" is the same
call with a warm start. Full file: `data/companies/rsr.md`.

**Two smaller findings from the same pass, both recorded so nobody spends the hour again:**

- **Conamar's absence from the dormant list is correct, not a filter bug.** They are the biggest
  client in company history (16 jobs, GBP 917,028) and were six months silent, so their absence
  looked exactly like the failure mode. It is the `live quote already out` exclusion doing its job:
  three quotes are still out - Wooton School Farm GBP 137,245.77, Hollickwood School GBP 57,260.01,
  Premier Inn Loudwater GBP 25,268.64 - all already carrying chase actions and owners. Checked
  further, because exact-name matching after `norm()` is how that exclusion works and a name
  variant would silently produce a false dormant row: **across all 82 won clients, zero would be
  caught only by substring containment.** Exact matching is currently sufficient; loosening it
  would risk merging distinct companies for no measured gain.
- **"RSR" in `contracts-finder-awards.json` (row 1152) is a Crown Commercial Service framework for
  Reservoir Panel Engineers, not RS Response Ltd.** Textbook single-word-name false positive.
  Settled - search the mailbox on `rsr.co.uk`, never on the three letters.

---

## A job can straddle the mailbox wall, and each bot will call its own half the whole story

**RSR / Amazon DRH1 Crawley, 29/07/2026 late. The most expensive shape of bug this two-bot system
has, because both bots were right and the answer was still wrong.**

Mary raised it unprompted (bot message 23) after Jacob's board listed RSR as a dormant customer to
be cold-called: **RSR are not dormant - there is a job they have already won sitting unanswered by
Fenster since 09/10/2025.** One window at Amazon DRH1, St Modwen's Park, Crawley RH10 3JY, quoted
**GBP 750 + VAT** in June 2025. Amazon signed the work off in October 2025. RSR chased twice, were
promised an answer "by tomorrow morning" on 08/09/2025, and never received one. They physically
cannot issue their own quotation to Amazon until Fenster confirms. **Nine and a half months.**

Her account had the job dying on **10/10/2025**, because that is where it dies in `estimating@`.
It does not. It ran three more weeks in `commercial@`, in a thread she is not permitted to read:

**The client end is in estimating@ (Mary's). The supplier end is in commercial@ (Jacob's).**
Subject "Quote Request - Crawley, Amazon DRH1 - Instant Glass": Harry emailed a Crawley glazier at
**13:17 on 05/09/2025, ninety-eight minutes after RSR chased him** - so he was working the blocker,
not sitting on it. Three chases followed. The last, on **31/10/2025 14:46**, is from Adam. The
glazier replied at **15:51 the same day offering to attend site on the Monday, and nobody ever
answered her.** That is where the job actually stops, and **the open question belongs to Fenster** -
not to the client, not to the supplier.

**The rule.** Neither bot was wrong about its half. Each read a thread that ended and reasonably
concluded the job had ended. **The handover rule assumes a job sits on one side of the wall at a
time, and a subcontracted job sits on both sides at once** - which is most of what Fenster does.
So: before concluding a job is dead, ask whether the *other* bot's mailbox would hold the other
end, and ask. Mary did exactly the right thing here - she said "estimating@ holds nothing after
10/10/2025, and that is all I can honestly say. Please check commercial@." That sentence is the fix.

**The cause of death was a leaver, not neglect - and no board would have shown it.** Adam,
31/10/2025 14:46, in his own words: *"Harry has now left Fenster so I am picking this up."*
**HARRY GROVER HAS LEFT FENSTER.** He held both ends of this job. Adam picked up the supplier end;
nobody picked up the client end. Harry is named as the seller on four of RSR's five won jobs and
appears across both bots' history. **Any row that says Harry owns it, or reads a promise of his as
live, is stale.** His departure was recorded nowhere - `mary_recall --grep "Harry Grover"` returned
one match and it was an EPC course invitation.

**Three smaller things from the same pass:**

- **`jayk@` is a hard 404, and that is not a null result.** Harry forwarded the GBP 750 there on
  16/06/2025. The mailbox was deleted when Jayk left and is not resettable. "Nothing in jayk@"
  means "there is nowhere left to look", never "nothing was there". Say it the second way.
- **A price can be right and the ARTICLE still wrong.** GBP 750 was priced against Amazon's stated
  spec - single pane, Schuco AWS65 GV1, 556 x 876. Harry to the glazier, 13/10/2025: *"this unit is
  actually two units bonded together... quote based off the same width at a 90 degree angle. 556 x
  556 x 876."* A bonded corner unit. So "is this cost still valid" is not only a validity-date
  question, and the Vetroseal quote behind it (FENSTERG_Quote_055834) is fourteen months old.
  **Pricing is Mary's - the BD job is to make sure she is asked the right question.**
- **The single-word-name trap again, caught before it reached a recommendation.** Searching
  "Instant Glass" returns 49 hits in commercial@ and makes them look like an established Fenster
  supplier still trading in 2026. Searched on `instantglass.co.uk` they appear in exactly **three**
  messages, all of them this one dead thread - no price ever produced, no order ever placed. The
  difference between "our Crawley glazier" and "a firm Harry cold-called once who never quoted" is
  the difference between a solved blocker and an unproven candidate. **Search the domain.**

**And one direction check worth generalising: count who chased whom before writing "gone quiet".**
RSR chased Fenster twice and Fenster answered neither. `dormant.json` would have had Adam ringing
them to ask why *they* had been quiet.

### The sequel, an hour later: I read a fan-out through one mailbox and got the blocker backwards

**Mary, bot message 25, correcting the entry above. Both of my conclusions were wrong and the
correction is more useful than the original finding.**

**Harry went out to THREE glaziers on 05/09/2025, not one.** Instant Glass was simply the only one
whose thread stayed in `commercial@` - so it was the only one I could see, **and it happened to be
the one that failed.** In `estimating@`:

- `05/09 12:26` **Maple Windows** (Info@maplecraftwindows.com) - never replied at all
- `05/09 12:28` **Johnson & Sons** (hello@johnsonandsons.co.uk, Paul Johnson, Director)
- `08/09 06:57` Paul Johnson prices it: *"To supply and fit as per details provided GBP 425.00 + VAT"*
- `08/09 11:31` **ADAM** sets the corner spec himself: *"two units bonded together... 556 x 556 x 876"*
- `13/10 08:28` Adam chases the revised cost
- `13/10 10:09` Paul Johnson: *"To supply and fit 2 units bonded with structural silicone **GBP 960.00 + VAT**"*

**So the blocker I reported as unsolved had been solved for nine months.** A firm, willing
subcontract price for the actual article has been sitting in `estimating@` since 13/10/2025.

**THE RULE: ABSENCE OF A PRICE IN YOUR HALF IS NOT ABSENCE OF A PRICE.** When somebody has gone out
to several suppliers, a partial view of the fan-out reads as the whole fan-out - and the branch you
can see is not a random sample of it. I had one of three, reported it as one of one, and recommended
chasing the dead branch. Before naming a supplier blocker, ask whether the enquiry went to more than
one firm and whether the other replies would have landed somewhere you cannot read.

**And it explains what nine months of silence did not: GBP 750 IS UNDER COST.** GBP 750 + VAT sell
against a GBP 960 + VAT buy with fit included is a loss of at least GBP 210 before margin, overhead
or our own time. Nobody could simply confirm the price RSR keep asking us to confirm, because the
honest answer was "it has gone up". **The next action is a re-quote, not a confirmation.**

**It also makes the history fairer than "we broke a promise".** Harri asked on 09/10 whether GBP 750
still stood; Harry put the same question to Adam on 10/10 08:25; **the revised GBP 960 did not arrive
until 13/10 10:09.** At the moment the question was put, the honest answer was not yet known. Then it
arrived, Harry left, and nobody put the two numbers next to each other. **Do not narrate a delay as
neglect before checking what was knowable on the day.**

### And the infrastructure lesson: the bot line silently eats the END of a long message

**`/api/botchat` does `clip(b.body, 4000)` and returns `{ok:true}` either way.** My reply to Mary was
6,918 characters. She received 4,000 of them - cut off mid-sentence in the fourth section, which was
the paragraph addressed to her. **The endpoint returns no truncated count, so nothing at all warns
the sender**, and she only knew because she went and found the rest of the story herself rather than
ask me to resend.

The failure mode is nastier than a plain length limit because **it takes the end, and the end is
where the point goes.** A truncated message does not look truncated - it looks like a message that
stopped making its argument.

**Fixed in `scripts/bot_chat.py`: `BODY_LIMIT = 4000`, and it REFUSES rather than warns** - a warning
printed after a successful send is read as noise, and the message is already wrong by then. It prints
the characters that would have been lost so the sender can see what they nearly dropped. Splitting is
left to the sender because only they know where the seam belongs, and the instruction is to **put the
point in the FIRST part.**

**Two copies of one fact, so note it:** the botchat route clips at 4,000, the hub's own reply route
at 8,000. Different numbers on the same hub. Do not assume one limit from the other.

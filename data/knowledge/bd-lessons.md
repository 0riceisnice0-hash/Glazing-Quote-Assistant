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

---

## 30/07/2026 - THE LIST THE DEPARTED BDM LEFT BEHIND, AND THE FILTER THAT HID THE BIGGEST CLIENT

Standing-agenda session, nobody wrote to me. Two findings, and they turned out to be the same finding
seen from two directions: **the board was built on the CRM, and the CRM is not the whole company.**

### Jayk's repricing log - `scripts/jacob_repricing.py`, `data/jacob/repricing.json`

On **19/12/2025** Jayk Sawbridge emailed `Repricing Log.ods` to adam@, commercial@, estimating@ and
nick@: *"listing of works I believe it is worth us repricing, reviewing, or re-submitting. Please see
notes in bold for my reasoning. Please ask me any questions."* Then he left. **`jayk@` is a hard 404,
so nobody can ask him anything.**

**62 rows, GBP 6,017,468 of quotes, 27 clients, with the client's own feedback written against each
one.** It appeared in no file on this board. He sold **51 of the 204 contracts Fenster has ever won -
a quarter of the company** - so this is the last of his reasoning that is readable anywhere.

**Why it is not just another stale spreadsheet.** A subcontractor's central problem is finding out WHO
WON the main contract (JACOB-SESSION section 1, step 2). **Five rows answer that outright, in the
client's own words:** *"22/12/2025 R1 have won this, so reprice"* (Gresty Road, GBP 89,898);
*"Thomas Sinden have officially won this, they will be in touch to get finalised pricing from us"*
(Hub Alkerden, GBP 581,367); *"RG Carter have won this"*; *"Worth repricing as secured"* (Barnfield MSM
Aerospace); *"Works secured client side"* (Elkins Midfield Primary). **That is step two of the whole
job, already done, by someone who no longer works here.**

**Two versions of the file exist and the diff is the point.** `Repricing Log.ods` is what he emailed;
`Repricing Log 22122025.ods` was touched again on 28/01/2026. They differ by **ONE cell** - RG Carter's
Linford Wood gained "(LOST)" in its title. That is the entire history of what was done with the list.

**Every fact in it is 223 days old and the deadlines are all 2025.** "Jayk to call in Jan" is a call
nobody made, because he had gone by January. So the file ranks and explains; it promotes nothing to a
lead, and `verifyFirst` sits on every row saying so. **Nine rows carry a NEW value he had developed
and left for Adam to check - those go to Mary, never out of the door.**

### Four join bugs found while building it, each of which produced a confident wrong answer

1. **ODS line breaks are invisible to `itertext()`.** Where the author pressed Alt+Enter the cell is ONE
   `<text:p>` containing `<text:line-break/>`, and flattening it welds two sentences: *"no
   decisionWorth repricing due to client"*. There is no word boundary between "n" and "W", so
   `\bworth repricing\b` does not match - and **six of Elkins' seven rows read as though Jayk had NOT
   recommended them when he had.** A parser that loses a recommendation is worse than one that loses a
   space. `jaykSaysWorthIt` went 8 -> 54 of 62 on the fix; `unclassified` 15 -> 7.
2. **AN EXACT MATCH IS NOT A COMPLETE MATCH.** Barnfield is filed in AdminBase both as "Barnfield
   Construction" and as plain "Barnfield". The exact-key lookup hit the first, returned four rows, and
   **short-circuited before the sweep** - so the MSM Aerospace quote, filed under the short name, read
   as absent. Union the exact hit with the alias sweep; never return early on it.
3. **AND THE SHARPER ONE: THE CRM SPELLS A CLIENT DIFFERENTLY FROM EVERY OTHER SOURCE.** The log's
   "Thomas Sinden" is **"Sinden Construction Ltd"** in AdminBase. First-word matching missed it, so the
   **GBP 581,367 Hub Alkerden job - the biggest row on the list, and one the client has WON** - looked
   absent from the pipeline when it is sitting there as lead 5493 at **GBP 484,472.63, still "Live -
   Quoted" since 21/01/2025.** Two different figures for one job, both real; the CRM holds the lower.
   **I was one step from telling Adam a GBP 581k won job was in no CRM row.**
4. **SUBSET, NOT OVERLAP, ON COMPANY NAMES.** Joining on any shared word matched "Thomas Sinden" to
   **"Chester Thomas Developments"** - two unrelated companies sharing a first name, and Chester Thomas
   is a live row on my own handover board. This is exactly the false positive `bd.md` records for
   single-word names ("Atlas" matched a window cleaner), reached through a person's name instead. Rule:
   one name's identifying words must be a SUBSET of the other's, with trading words (Construction, Ltd,
   Group, Services, Glazing...) stripped first. {SINDEN} within {THOMAS, SINDEN} survives;
   {CHESTER, THOMAS} does not.

**And the join that pays for itself: PENNY-EXACT VALUE.** A 2dp figure matching between a hand-kept
spreadsheet and a CRM export is the same quote, not a coincidence - the join `bd.md` already trusts for
`staleDate`. It settles what tokens cannot: whether the CRM row is a RE-quote or **the same quote still
sitting open. 18 of the 62 rows join penny-exact to a row still marked "Live - Quoted".** R1's Gresty
Road is GBP 89,898.12 in both, 220 days on. Tokens alone missed it, because stripping street furniture
leaves "Gresty Road" as ONE distinctive word, under a two-word threshold.

### 6 clients on that log are in the AdminBase export at all - GBP 1,122,044 invisible

**Clegg Construction (GBP 777,177), MCS Construction (GBP 137,160), BC Workspace (GBP 82,516), Steele &
Bray (GBP 62,602), Cheil Construction (GBP 48,814), RG Carter (GBP 13,771).** `bd.md` already says the
register is a FLOOR and never a complete set; `absentFromCrm` is the first measurement of the depth.
**Not an accusation about the CRM** - a quote raised outside the export window or under another trading
name lands here too. But Cheil's row says *"Chris at Cheil has asked us for PQQ's to be completed and
for updated costs + schedule so now actually looking good"* - **an outstanding ask of Fenster, from a
client no panel on this board can see.**

### The dormant filter hid the largest client in the company's history

`jacob_dormant.py` excluded **CONAMAR BUILDING SERVICES LTD - 16 jobs, GBP 917,027.91, 32% of every
pound Fenster has ever won** - as "mid-conversation, live quote already out".

The test was `live = {norm(client) for r in crm["due"]}`: **does this client appear in the CRM at all.**
And under **JAC-14 (Adam, 29/07) nothing on that backlog ever closes on silence** - all 209 rows stay
"Live - Quoted" until a client updates them. So "has a live quote" really meant **"has ever been
quoted", a permanent exemption from the dormant list for every past customer Fenster has ever priced.
The better the client, the more certain they were to be hidden.** Conamar was excluded on two quotes
whose next-action dates passed in **June 2025, 400 days ago.** Nobody was mid anything.

**Fix: a quote only counts as a live conversation while it is younger than the silence being
measured.** Harrabin Construction stays excluded on the new rule - quoted 15 days ago, and ringing
them about old times would cut across a real chase, which is what the exclusion is *for*. Dormant went
9 -> 12 clients; Conamar came top, Storm Building Ltd (GBP 43,113, 297d) also surfaced.

**And the exclusion was throwing away the reason for the call.** Where a client is dormant AND holds
unanswered quotes, `staleQuotes` now carries them onto the row: *"ask about the 2 quotes worth
GBP 162,514 still sitting with them unanswered - the oldest is 402 days old. That is the reason for the
call, not the silence."* **"You have GBP 219,774 of our prices" is a better opening than "how have you
been."**

### Conamar, written down for the first time - `data/companies/conamar.md`

- GBP 917,027.91 over **16 contracts, 2021 to 2025, unbroken**. Biggest: Tottenham Jobcentre
  GBP 480,000. Repeat sites: Heals Building three times, Wootton Lower School twice.
- **All sixteen sold by Adam Butcher personally** - not Jayk, not Harry. `LEADSOURCE` on every one is
  Existing Customer/Commercial. **The relationship has never needed a lead source, and it is Adam's
  own.** That is the most useful fact on the page: it is a call he can make with no preamble.
- **GBP 219,774.42 of live quotes**: Wootton School Farm GBP 137,245.77 (414d), Hollickwood Primary
  GBP 57,260.01 (359d), Premier Inn Loudwater GBP 25,268.64 (416d).
- **Mailbox against CRM, the RSR lesson applied rather than re-learned:** `quietDays` 227 is days since
  WORK. Real last two-way with a Conamar person is **John Ling, 10/11/2025**; Adam was sending invoices
  to 26/11 and chasing Wootton payment on 08/12/2025. The 26/01 and 25/03/2026 hits are **not** Conamar
  contact - one is an info@ broadcast about a compromised mailbox.
- **The money question looks closed, so the call is clean.** Five delivered jobs carry a balance of
  GBP 6,514.64 and each is 2.5-5% of contract value - **the shape of retention on a running defects
  period, not a disputed invoice.** The Wootton invoices Adam chased in December show zero balance now.
  **Flagged as an inference off the `balance` column, not a fact** - opening a "what have you got
  coming" call with a client who thinks they owe us money is the one way to waste this.
- **Alex Taylor has LEFT Conamar** - auto-reply on the address since 20/12/2024. Same family as Harry
  Grover: any row where a leaver holds the thread is stale.
- **An unanswered referral off a delivered Conamar job.** 26/01/2026, Alana Somers at Gardiner &
  Theobald (national QS) to info@: *"Market Testing - Arched Double Glazed Window. We previously worked
  together on the University of Roehampton SETEC Project, where you supplied and installed external
  sash..."* Perry forwarded it to commercial@ the same day. **There is no reply anywhere in any
  mailbox** - three messages, all on one day, and that is the whole thread. A national QS came back to
  Fenster by name on the strength of our own work and got silence.

## JAC-4 answered "Either" - and the two things "either" does not mean (Zac, 29/07, hub-87)

**The question:** "Who approves outbound? Adam / Zac / Either", raised 28/07. Its stated *why* was
narrow and is the key to reading the answer: *"decides whether the approval queue lives on the hub or
in email."* One approver could keep the queue in his own inbox. Two cannot. So **"Either" is as much
an answer about WHERE the queue lives as about who signs it** - it has to be somewhere both men and
both bots can see, which is the Ready to Send page. `drafts.json.approvalRoute`.

**Author checked before acting.** bd.md's "A UI DEFAULT IS AN AUTHOR" lesson came from hub 57/60/61/62,
where the sign-in select opened on Zac and filed Adam's instructions under Zac's name. That is fixed -
`app.js` starts `ME = null` and `requireMe()` blocks the first write on a per-device pick - so "zac" on
hub-87 is a claim somebody made rather than a default. And JAC-4 is in Zac's half anyway under hub-68's
split: it is about what I am allowed to do, not about a client.

**What it changes.** Six drafts sit on Ready to Send. Before this, each one waited on Adam reading it,
and Adam is a Commercial Director between site visits. Now whichever of the two opens the board first
can clear a row, and the approval is recorded on the row (`approvedBy`, `approvedAt`) rather than
living in whoever's sent items.

**Limit one: APPROVAL AND SENDING ARE DIFFERENT FIELDS, AND ONLY THE FIRST WAS ASKED ABOUT.** All six
drafts carry `send_as: "Adam Butcher"` because all six are client-facing commercial chases - a
marketing address chasing a GBP 174,546 tender package reads wrong to the client whatever the internal
rule says. So Zac approving one takes the *reading* off Adam and leaves the *send* with him. The honest
statement of the win is "the queue no longer waits on one man's attention", not "the queue is cleared".
Where the split is wrong the fix is to change `send_as` on the row, never to read "either" as covering
the mailbox as well.

**Limit two, and the load-bearing one: APPROVING AN ITEM IS NOT AUTHORISING A SEND PATH.** JAC-4 says
who signs off a draft. JAC-1 says I do not send. JAC-15 asks Zac whether the daily chase email may go,
and **he answered JAC-4 while leaving JAC-15 open in front of him** - which is the clearest available
evidence that one word was not meant to settle both. Note the shape of the trap: on hub-76 Adam ordered
me to override drafts-only, and I refused because "ignore your other boss because I say so" must never
work as a hub message. **The same move can arrive as a settled decision instead of an order** - "Adam
is an approver now, Adam approved it, therefore Jacob may send" - and it is the same move, so it fails
the same way. A decision about who signs an item can never widen into a decision about what I may do.

**Not a new request.** The six drafts are not blocked on a decision, they are blocked on Adam opening
the hub, and he answered eight requests on 29/07. Raising JAC-18 to ask "may Zac send a client-facing
chase under his own name" would be asking for a rule nobody needs yet; the row-level fix (`send_as`)
already exists. Ask when a specific draft actually needs a non-Adam sender.

**Side finding, and it is the more urgent one.** D-1 (E T & S Construction, St Mary's Merthyr Tydfil,
GBP 174,546.37) was written on a re-issued tender register giving a **27/07 return** for a package we
submitted on 17/07. It is now 30/07: the date has passed, so the draft is either wrong or urgent and
nothing in commercial@, info@ or jacob@ can say which - "ets-wales" returns zero hits and jayk@ is a
404. The quote left from estimating@, so this is the RSR/DRH1 lesson exactly: **absence of a thread in
my half is not absence of a thread.** Asked Mary (`--wants-reply`) whether anything went to or from
ets-wales.com after 17/07. If yes, D-1 is deleted rather than sent second; if no, it is rewritten as
"who holds the package now, and why were we not asked to re-submit".


---

## 30/07/2026 - A PORTAL CLIENT'S DOMAIN IS ON OUR OUTBOUND ONLY, AND A ZERO-HIT SEARCH SAID SO

**The short rule (bd.md):** search the domain - then distrust a zero. If a client runs the tender
through a portal, their traffic never carries their domain at all, and the only reason any of it is
in a Fenster mailbox is that a colleague forwards it.

**What I did.** Draft D-1 was E T & S Construction, St Mary's Refurbishment, Merthyr Tydfil -
GBP 174,546.37, the biggest number in the Ready to Send queue. It was written on a tender register
E T & S re-issued on 24/07 giving a **27 July return** for a package we submitted on 17 July. By the
30th that date had passed, so the draft was either wrong or urgent, and I could not tell which:
"ets-wales" returned **zero hits** across commercial@, info@ and jacob@, and jayk@ is a hard 404. I
asked Mary whether anything went to or from ets-wales.com after 17/07, and said out loud that if the
answer was "nothing" the draft would be **rewritten** as "who holds the package now, and why were we
not asked to re-submit".

**Her answer (bot-27, 29/07 23:47) killed both versions.** Every folder of estimating@, 17/07 to now:
exactly ONE message touches ets-wales.com, and it is our own submission - 17/07 **11:17:36**, Gintare
to tom.godfrey@, cc adam@, three attachments, sent as a RE: on the portal's own "invites you to quote"
thread. Nothing after it. No acknowledgement, no query from Tom.

**But we WERE asked to re-submit. Twice, on 24/07:**

- **12:17** Paul Taylor forwards "E T & S Construction Ltd addendum: St Mary's..." - "We've received
  addendums on the window schedule for this one, I have downloaded and saved them in Tender Docs."
- **12:47** Paul forwards a second, "E T & S Construction Ltd new message: ..."
- **13:06** Gintare replies **to Paul, not to ET&S**: "Thanks. We submitted this enquiry last week,
  but I'll check whether any changes are needed."

That check was never closed out. The 27/07 return was in the header of the register attached to those
notifications. Mary checked the revision on 29/07 and emailed Adam that there was no scope change -
but nothing ever went back to E T & S. **The package was re-opened, we were told on the day it was
re-issued, and it lapsed at our end.** Sending "why were we not asked to re-submit" to Tom Godfrey
would have told a client we are mid-tender with that we do not read what they send us.

**Why the search returned nothing, and this is the part worth keeping.** E T & S run this tender
through a portal. Their notifications come **from the portal**, subject-lined "E T & S Construction
Ltd addendum:" / "... new message:" / "... invites you to quote on:", and they reach estimating@ only
because **Paul Taylor forwards them**. So the client's domain appears on our **outbound** only.
Searching `ets-wales.com` will never find their inbound traffic on this job, and the same is true of
any portal client.

Three separate errors stacked to make a zero look like a fact:

1. **Wrong mailbox.** The submission is in estimating@, which I cannot read - the RSR/DRH1 lesson,
   already written down, and I made it again on the very next job.
2. **Wrong search key.** Even in the right mailbox, the domain finds our half and not theirs.
3. **Wrong clock.** I had our send at 12:17. **12:17 is Paul's 24/07 forward.** The send was 11:17 on
   the 17th. Two events, one timestamp, read onto the wrong one - and it went into `handover.json`
   and into D-1's evidence line as a fact.

**The fix, and it is a search habit not a script.** Search the **portal's subject phrasing** -
"<client> addendum:", "new message:", "invites you to quote on:" - not the client's domain. Then ask
**who forwards it**. And note what that does to JAC-11: "the tender-portal logins died with Jayk" is
true of Jayk's accounts and irrelevant here, because **a colleague is already receiving from this
portal**. A live colleague on a portal is the login the dead one hides. Same shape as ProContract -
check what a block actually blocks.

**What replaced the draft.** Nothing goes to E T & S by email. The only honest question is whether
our 17/07 submission is still under consideration or the package has been let, and whether they would
take a clarification schedule against it - and it goes back through the portal, which means Paul.
That is **JAC-18**, Adam's decision, because re-opening a package we let lapse is a relationship call
on a first-ever quote to this client, not a chase.

**And it must not be asked in a hurry.** Mary's closing warning: if the answer is "still open" we are
**not ready to re-submit by return**. Strip-out is settled and priced at GBP 16,050; **carriage to
Merthyr is still an open decision with Adam on REQ-24**, and a revised submission cannot go without
it. So the sequence is REQ-24, then JAC-18, then the portal - and nobody promises E T & S a
turnaround in the meantime. Asking a question you cannot afford the answer to is its own mistake.

**The wider one.** I asked Mary a narrow question - "anything to or from this domain after 17/07" -
and she answered a wider one, which is the only reason the draft died instead of going out reworded.
A "no" to a narrow question is not the same as "nothing happened", and the second version of D-1 was
about to be built on exactly that confusion. `data/companies/ets-construction.md`, `drafts.json`
(D-1 withdrawn, correction logged), `handover.json`.

## 30/07/2026 - Two transposed letters hid a client who was waiting on US, and a planning register explained the silence

The rules in `bd.md`: *a transposition defeats both the subset join and the penny-exact value join -
match on same-letters-reordered or 0.9 similarity, corroborate on the CONTACT or one RARE token,
never on the name, and let Companies House arbitrate which spelling is real*, and *the planning
register also explains a client's SILENCE - read it before calling anyone quiet*. This is why both
exist, and what the second one is worth.

**The row.** AdminBase lead 7384: Chiel Construction, SWANHURST SCHOOL BROOK LANE BIRMINGHAM,
GBP 52,483.33 ex VAT, "Live - Quoted" since 22/12/2025, owner Adam, taken by JAYKS,
chris@chielcon.co.uk, 02476 466 877. It has sat on the chaseable list since Adam's export arrived on
28/07 with the standard generated ask against it - chase for a final answer, how our price looked,
what else they have coming.

**Why the join missed it.** `repricing.json` reported six clients on Jayk's log as absent from the
AdminBase export entirely, GBP 1,122,044 "invisible to every panel here". One of the six was
"Cheil Construction, GBP 48,814.80". It is in AdminBase, spelt **Chiel**. Every join this file
already had failed on it, and each for a different reason:

- **Exact key** - different string.
- **Subset of identifying words** (the Barnfield/Sinden fix) - `{CHEIL}` is not a subset of
  `{CHIEL}` in either direction. The words are not shorter or longer, they are *wrong*.
- **Penny-exact value** - the log carries GBP 48,814.80 and the CRM row GBP 52,483.33, because the
  CRM row is the later December re-quote. Legitimately different figures, so the strongest join on
  the board had nothing to bite on.
- **Project tokens** - `tokens()` strips SCHOOL and LANE as street furniture, so "Swanhurst School"
  against "SWANHURST SCHOOL BROOK LANE BIRMINGHAM" shares exactly ONE distinctive word, under the
  two-word bar. That is the Gresty Road trap again, on a row where it also mattered.

**What was added, and why it is deliberately the weakest join.** `near_keys()` in
`jacob_repricing.py`: compare the identifying words as one string, accept either the same letters in
a different order or a `difflib` ratio of 0.9 and up, and refuse to look at all when the identifying
part is under five characters ("GD Construction" and "R1 Construction" are not each other). Then
**corroborate on something that is not the name** - a rare shared project token, a penny-exact value,
or the contact: the log says "**Chris** at Cheil has asked us for PQQ's" and the CRM row's email is
**chris**@chielcon.co.uk. Two corroborators and it counts as in the CRM; fewer and it is listed as a
candidate and nothing else. Across 62 log rows and 127 CRM client names it fired **exactly once**,
and that once was right. `clientMatch: "near"` and `nearMatch.confirmedBy` carry the evidence onto
the row so nobody has to take the spelling's word for it.

A bug worth recording on its own: the first version compared `want <= other` on two *strings* rather
than two sets, which is lexicographic ordering, not subset - and 'CHEIL' <= 'CHIEL' is True, so the
one case the function existed for was silently skipped. The idiom looked exactly like the subset test
three lines below it.

**Companies House settles which spelling is real.** CHIEL CONSTRUCTION LTD, **04840215**, active
since 21/07/2003, Bailey House, Curriers Close, Charter Avenue Industrial Estate, Coventry CV4 8AW,
SIC 41201, accounts filed to 31/01/2025. AdminBase is right and *three* of our own systems are
wrong - Jayk's log, the Opportunity Log and the tender folder on the Commercial drive all say Cheil.
The registered name is free to check and it is the only arbiter available.

**What the row actually is, which is the part that matters.** Jayk's log, 19/12/2025: *"Revised
prices sent to Adam by Gee 10/12/2025 we have offered a new cost of 40k and Chris at Cheil has asked
us for PQQ's to be completed and for updated costs + schedule so now actually looking good. Gintare
has reviewed an issued to Adam."* The tender folder shows the PQQ paperwork **arriving** 18/12/2025 -
contractor evaluation form, contractors compliance statement, subcontractor insurance verification -
and a revised client quote dated 22/12/2025. Then nothing. **The client asked Fenster for three
things and the trail stops inside Fenster.** Nothing in commercial@, info@ or jacob@ mentions Chiel
or chielcon.co.uk at all, and jayk@ is a 404 - so only estimating@ can answer it. Asked of Mary and
raised as **JAC-19**; no draft written until it is answered, because a 223-day-late delivery and an
ordinary chase are two different emails and D-1 died the same morning for exactly that error.

**So the generated next action was the most expensive sentence on the page.** "Chase Chiel for a
final answer on how our price looked" is a good default across 209 rows and wrong on this one, in
the direction that costs a relationship. `WORKED` in `jacob_adminbase.py` now lets a researched row
replace its own next action, keyed on the lead number, carrying `why` with its sources - the same
pattern `CONFIRMED` already established for Brandon Estate. An override with no source is just a
different guess.

**And the silence is not neglect on their side.** Birmingham City Council's register, which nothing
on this board reads: **2025/01426/PA** - erection of a new sports hall, demolition of the existing
one - received 11/03/2025, approved subject to conditions 11/07/2025. **2025/06383/PA** - discharge
of conditions 3 and 4 (drainage), 9 (construction management plan) and **13, the internal design and
layout of the proposed sports hall** - received 12/11/2025, **approved 26/02/2026**. Condition 13 was
outstanding across the entire gap in our record. The glazing package could not be settled while the
internal layout of the building was still with the planners. Read as a chase, the row says "went
quiet after Christmas"; read against the register it says "they could not answer, and then nobody
went back". **A discharge-of-conditions date can be the whole explanation for a client's silence,
and it is free to look up.**

**The second scheme, which is the actual opportunity.** **2026/02027/PA** at the same school:
construction of a new single storey SEN teaching facility. Received 16/04/2026, registered
17/06/2026, **undecided, consultation 17/06 - 05/08/2026**, application expires 11/08/2026.
Applicant **Vonni Steer**, agent **Lucas Architects Ltd**, officer Jeff Badland. No contractor named
anywhere public, which is the point - the enquiry list cannot exist yet. Small, which puts any
glazing package in the band the funnel converts rather than the band it loses in. And we have a
named contact at a builder already working that site.

**It is invisible to `planning.json`**, which pulls a 30-day window of **large** applications: this
one is small and was validated on 17/06. **A site we already hold a live quote on should be watched
by name whatever the application size** - proposed on the hub, not built.

**Two API notes.** PlanIt's `search=` parameter genuinely returns nothing for "Swanshurst" (control:
1,103 records for "sports hall", so the tool works and the zero is real) - the application was found
on `pcode=B13+0TW&krad=0.5` instead. **Search by SITE, not by name, when you know where the job is.**
And Birmingham's NECSWS portal serves an "unsupported browser" page to any user agent it does not
recognise, listing the ones it accepts; send a Chrome string and the applicant name is right there.
PlanIt redacted all three applications to "See source". That redaction is Barbour's product.

**One more thing the log gives up once it is read as a queue rather than a list.** Its `asked-of-us`
tier is seven rows and GBP 222,725, and it is not a repricing shortlist - it is **seven prices that
stopped inside Fenster**. Four of the seven end with the words "issued to Adam" or "Adam to check"
(Logan Construction Queen Victoria GBP 108,453; Cheil Swanshurst; SDevs Mendip Road; Lindum Howden
Fire Station) and three more read "Ready to Go" (GD Construction Westmead Clinic, Bradford Watts
twice). Every one of them is 220-plus days old. That is not proof any of them failed to go - it is
proof that **nothing on record says they went**, which is the same open-loop shape as St Mary's
Merthyr the day before. Named on the hub rather than raised as seven separate requests.

`data/companies/chiel-construction.md`, `repricing.json` (`foundBySpelling`), `adminbase.json`
(lead 7384 `worked`), `drafts.json` (`not_drafted`), JAC-19.

---

## 30/07/2026 (02:03, standing agenda) - the silence clock named the wrong party

**The row.** AdminBase lead 5493, The Hub Alkerden, Sinden Construction, GBP 484,472.63 ex VAT -
the largest unworked row on the board and the top `secured` row on Jayk's repricing log. It read
**"Live - Quoted, 523 days silent"** and the next action my own code generated was *"chase Sinden
for a final answer - is it still live or did it go elsewhere and to whom"*.

**What was actually true.** Sinden secured the main contract in October 2025. On **01/07/2026**
Seyi Adesogan, their Assistant Surveyor, emailed commercial@ - **my own mailbox** - asking for an
updated quotation for the Aluminium Curtain Walling & External Doors package **by 08/07/2026**,
with a provisional package order date of 08/10/2026 and site commencement 11/02/2027. He asked us
to confirm receipt. Paul Taylor forwarded it to Adam, Steven and estimating@ the same afternoon,
and again on 02/07 with an elevation drawing that had been missed. A Plus Aluminium's supplier
quote QP65153 was still being revised on **22/07** with Gintare chasing doors ED10-ED12. Nothing
in commercial@, info@ or jacob@ replied to Seyi.

**So the call the board was recommending would have asked a client who had already told us they
had won, given us the programme, and been waiting three weeks for our price, whether the job was
still live.** The 523 days are an artefact: the lead date is the January 2025 enquiry and
AdminBase has never re-dated it across two re-enquiries since (March 2026 and July 2026). This is
the same family as the RFQ-OUT-IS-NOT-QUOTE-OUT slip, but the consequence is worse, because the
direction of the open loop is inverted rather than the size of it. **Before believing a silence
clock, search the mailbox for the client's name.** A number of days is a fact about a database
field; who owes whom is a fact about the correspondence.

**Not drafted, deliberately, and the reason is the same one as Chiel the day before.** If the
quote has gone, the next email is an ordinary chase with a hard hook - their own order date. If it
has not, it is an apology and a date. Those are two different emails, not two wordings of one, and
estimating@ is not mine to read. Asked Mary (bot line, --wants-reply); raised **JAC-20** for Adam
with three options including taking Sinden off my board entirely.

**A loose end that predates all of it.** On 23/03/2026 Corran Goodson, their Senior Surveyor,
asked commercial@ to confirm the security ratings for the external doorsets and the curtain
walling. Paul replied the same day that we would get them over "asap". Nothing on my side of the
wall shows them going. He opened that email **"Hi Harry"** - Harry Grover left Fenster on
31/10/2025, five months earlier, and nobody had told the client.

**And their spec moved.** On 30/03 Adam established with Corran that the WINDOWS had gone from
aluminium to composite, and offered a composite quote; Corran said yes please; info@ went out to
suppliers on 09/04 and Munster Joinery declined the same day. The July enquiry covers curtain
walling and doors only. **Either the window package went elsewhere or it is still unplaced**, and
one question on the same call settles it.

### The client renamed, and that is not a CRM typo

**Thomas Sinden Limited (CH 03308698) became Sinden Construction Limited on 22/06/2026**; Thomas
Sinden (Holdings) Ltd 13028751 became Sinden Holdings Ltd the same day. Their own circular to Adam
is in commercial@. No change of ownership, structure or contractual arrangements - branding only.
So AdminBase carrying both "Thomas Sinden" and "Sinden Construction Ltd" is the relationship
straddling a rename, not the spelling problem Chiel was. **Their email domain is still
`thomas-sinden.co.uk` and they now also publish `info@sindenconstruction.co.uk`** - search both or
half the history hides. Companies House arbitrates, as it did for Chiel.

### OSG Cold Ash: "on hold" was a refusal, and PlanIt did not know

Lead 7745, GBP 340,851.43. Emma O'Brien told estimating@ on **26/06/2026** that the project was
*"on hold due to a planning issue"*; Adam replied on 27/06 that he would update our notes; the CRM
row still said Live - Quoted with a chase due.

West Berkshire's register says it harder. **25/01899/FULMAJ** - change of use of the former St
Gabriel's Convent at Cold Ash to an educational facility, demolition of the convent, retreat
building and chapel, a new two-storey teaching building with single storey sports hall and pitches
for OneSchool Global, plus access works for St Finian's Catholic Primary. Validated 12/09/2025,
target decision 07/11/2025, **REFUSED, decision issued 21 May 2026**. No appeal and no
resubmission at that postcode as at 30/07/2026. A refused full application ordinarily carries a
six-month appeal window, so late November is when it is worth looking again.

**PlanIt had it as "Undecided / Awaiting decision".** Its record's `last_scraped` was
**2025-09-20** - ten months old. The council's own Idox page (Chrome user agent, as Birmingham
taught) carried the refusal in one fetch. **`app_state` is only as fresh as the scrape behind it,
and the field that says so is on every record.** The cost of not checking it here would have been
a chase call about a scheme that no longer exists, and the benefit of checking it is a dated watch
instead of a dead row.

### The fix underneath: improving a row made it disappear

`jacob_adminbase.py` builds its chase list by filtering on three literal state strings -
`quoted - chase due`, `quoted - a year silent`, `quoted - no date`. The moment the WORKED override
wrote a truer state onto Alkerden - "re-enquired - our price is the late one" - **the row fell out
of `due` and off the daily email entirely.** The most urgent row on the board, silently, as a
direct result of researching it. A WORKED row now keeps its place in `due` whatever state it
carries, WORKED can set `state`/`owner` as well as `next` (a half-override that says do-not-chase
while the row still says chase-due is worse than none), and a `blocked` reason on the override
routes the row into the daily email's `blockedNotChased` list - named, in the same place Brandon
Estate sits, never dropped.

**The general rule: whenever a row is researched, re-check that it still APPEARS.** Every filter
in this codebase that matches on a literal state string has the same shape of bug in it.

`data/companies/sinden-construction.md`, `adminbase.json` (leads 5493 and 7745 `worked`), JAC-20.

---

## 30/07/2026 (03:03 session) - Barnfield Construction: GBP 568,576, six enquiries, no wins

Own-time session on the standing agenda. One company worked properly instead of many rows badly.
`data/companies/barnfield-construction.md` (151 lines) is the deliverable; these are the four
transferable lessons.

### 1. AN OUTCOME CAN LIVE IN A SUPPLIER'S COURTESY EMAIL AND NOWHERE ELSE

On **30/04/2025** Jack Pollard of BSW Window Solutions emailed commercial@ - "just a courtesy email
in regards to the status on the big project quotes we have provided for you... if you could advise
on where we are at in regards to winning any of them" - and listed fifteen jobs. Harry Grover asked
Jayk to handle it. On **01/05/2025** Jayk answered all fifteen, a line each:

> **"Bradstone Road: Lost on price, you can close this enquiry."**
> "Meadow Lane: These works were lost." / "Newton Aycliffe: These works were lost." /
> "Sittingbourne Rugby These works were lost." / "Wetmore Road These works were lost." /
> "St Johns These works were lost." / "Liberty Care: ...the site is being transferred from Liberty
> Care to Care UK, which is delaying the decision." / "Feathers Charity: our contact who initially
> requested our costs has left the business." / "Hub Alkerden: Decision was to be made mid to late
> April" / plus Clarks Honey Lane, Clegg Plot B1, Finchley Catholic, Pagabo, SDEVS, St Thomas More.

**Not one of those outcomes reached a Fenster record.** Bradstone Road is still "Live - Quoted" in
AdminBase and still "open" on the Opportunity Log fifteen months later, and this morning it was the
**third row on Adam's chase list: GBP 218,917, "497 days silent, chase Barnfield for a final
answer."** The answer had been given, in writing, by our own BDM, to a supplier.

**Why this is a whole class and not one row:** suppliers chase their own order book, so they ask us
for outcomes on a schedule nobody internally keeps. That makes our replies to THEM the most
complete outcome record in the company - and it is filed under the supplier's name, not the
client's, so no client-based search finds it. **Search the supplier threads. BSW/Bellview, Aplus,
Vetroseal, Strongdor, IKON, CN Glass.** Ask what they asked us, and what we told them.

### 2. THE UNDATED ROW: RESEARCH DID NOT SAVE A ROW, ONLY A DATE DID

Yesterday's lesson was that a chase list filtered on literal state strings deletes any row you
improve. **The same trap sits one field across, and it had already eaten the previous session's best
work.** `jacob_daily_email.build()` ended with `if not when or when > TOMORROW: return` - and
`when` comes from AdminBase's follow-up date, **which is empty on 80 of 264 rows.**

So a row could carry a WORKED override, a researched state, an owner and an explicit next action,
and still be dropped from Adam's email in silence for want of a CRM field. Two casualties found:

- **Barnfield / MSM Aerospace, GBP 46,968.75** - the strongest of the five Barnfield rows, because
  Jayk's log records Barnfield as having **SECURED the main contract** and a revised quote at
  GBP 37,827 went out 12/01/2026 against a February start now passed. On nothing.
- **Chiel Construction / Swanshurst School, GBP 52,483** - the *previous session's entire finding*,
  the row where the CLIENT WAS WAITING ON US. Researched, written up, given a company file - and
  absent from the daily email from that moment on. I did not notice for a day.

There was already a branch for exactly this shape: an undated **blocked** row is dated TODAY so that
Brandon Estate at GBP 7.2m cannot read as forgotten. The comment there says it outright - "without
this branch the largest live quote in the company is in neither list and reads as forgotten, which
is the one outcome an undated block must never produce." **A worked row deserved the same argument
and did not get it.** Now: no date plus `worked` means due today, `verified` true, and a third
date-source label - `SRC_RESEARCH`, "no CRM date - dated today because this row has been researched"
- because calling it a person's date or the CRM's would be borrowing credibility neither gave.

**The general rule, now twice in two days: improving a row deleted it. Verify the row is still ON
THE PAGE, not merely that the file changed.** Two fields down, and every other filter in this
codebase that reads a CRM field as a precondition has the same shape.

### 3. IT IS THE CUSTOMER KEY, NOT THE SPELLING, THAT SPLITS A CLIENT

The known trap was spelling - Barnfield vs Barnfield Construction, Thomas Sinden vs Sinden
Construction, Cheil vs Chiel. **This is one level down and worse, because it defeats aggregation
rather than lookup.** Barnfield's five live leads carry three different AdminBase customer keys:

| Key | Rows | Value ex VAT |
|---|---|---|
| `barnfieldconstruction.co.uk` | 3 | GBP 302,690 |
| `BARNFIELD CONSTRUCTION` (a literal name, no domain, no email) | 1 | GBP 218,917 |
| `hargreavescontracting.com` | 1 | GBP 46,969 |

So the client-concentration panel truthfully reported a three-row client and two one-row clients,
and **GBP 568,576 - the largest single-client exposure on the board, ahead of Conamar - has never
appeared anywhere as one number.** A spelling check would not have caught it: two of the three keys
do not contain the string "barnfield" in the same form, and one names a different company entirely.
**Aggregate on the resolved company, never on the key, and treat every per-client total here as a
floor.**

The third key is its own warning: lead 6781 sits under `hargreavescontracting.com`
(`nkitchin@hargreavescontracting.com`, 01204 365300) while its postcode BB9 5SP is Barnfield's own
head office and Jayk's log calls the job "Barnfield Construction - MSM Aerospace CW". Whether
Hargreaves is the contracting party, a group company or a CRM error is **unresolved and must be
settled before anyone is addressed** - guessing it is Barnfield because the log says so is the same
error in the opposite direction.

### 4. 0-FOR-6 WITH THE ESTIMATOR STILL RINGING IS A PRICING PROBLEM, NOT AN ACCESS ONE

The standing frame in `JACOB-SESSION.md` is that a relationship buys one thing: being asked to
price. Barnfield show what to do when that has already been bought and nothing converts.

**Ian Brown, Senior Estimator, has sent six enquiries in twelve months. Fenster has won none of
them and appears in no won contract for Barnfield at all.** Opportunity Log: 0 won, 1 lost, 5 open.
Writing "get Fenster onto their enquiry list" would have been worse than useless - we are on it.

**And the reason we lose was sitting in commercial@ the whole time.** Jayk, 11/03/2025:

> "Ian mentioned we have given a detailed breakdown. Another quote came in at a similar 378k. There
> were three cheaper quotes: **275/255/249k**. Ian is happy for us to value engineer our quote and
> **he will be giving us further opportunities!**"

Joint top of five, GBP 129k above the lowest. He then kept the promise exactly - Moston 19/05/2025,
St Johns 19/06/2025, MSM Aerospace 15/09/2025, The Grange Apartments 05/02/2026.

**So the diagnostic to run on any warm-but-unconverted name: count the enquiries IN and the wins
OUT before recommending an approach.** If the ratio is bad and the enquiries keep coming, the only
question worth putting to the contact is what we are buying wrong - and a client who has already
volunteered his competitors' numbers once will do it again.

### The loose end, and it is the third of its kind this month

Fenster value engineered as invited. Harry Grover circulated the revision internally on 27/03/2025 -
"Hi both" to Jayk and Adam, BSW buy GBP 147,294.62+VAT plus GBP 11,500 of frame markups. The figure
now on the CRM row is **GBP 218,917.29 ex VAT, roughly GBP 30,000 BELOW the cheapest quote we knew
about** - and there is no send of it to Ian Brown in commercial@, info@ or jacob@. A revision that
undercuts the field by GBP 30k does not then lose on price.

**That is now three jobs this month whose price may have stopped inside Fenster - Chiel/Swanshurst,
Sinden/Alkerden, and Bradstone Road - and all three are invisible from my side because quotes leave
from estimating@.** Asked of Mary 30/07. If the pattern is real it is one problem, not three
coincidences, and it is worth more than any single lead on this board.

### Two smaller things worth keeping

- **A supplier's quote NUMBER dates a document when the document will not.** Vetroseal quote 060676
  "BRADSTONE RD CHEETHAM" arrived 29/01 and 02/02/2026, nine months after "lost on price" - and the
  PDF is glyph-encoded, so its own date could not be read. Vetroseal number sequentially at ~27 a
  day (064635 on 07/07/2026, 065095 on 24/07/2026), which places 060676 in early 2026; a re-send of
  a March 2025 quote would be numbered near 052000. **Sequential supplier references are a usable
  clock.** Conclusion: somebody was buying glass for that site in January 2026.
- **THE REGISTER DATES THE ENQUIRY, NOT JUST THE SCHEME.** Bradstone Road is Manchester
  115485/FO/2017, "3 x three-storey buildings to form 19 Cash and Carry units", permitted
  20/09/2017 - matched to Ian's enquiry for "3 Blocks of Shell Only 19 three Storey Commercial
  Units" and corroborated hard, because PlanIt names the agent **Whitebox Architecture** and the
  enquiry attached "WhiteBox Elevations Blocks A, B & C". Its conditions were refused repeatedly
  from 2022 until the last (drainage, CDN/24/1171) was **discharged 11/02/2025 - and Ian's enquiry
  arrived eight days later.** Conditions cleared, procurement started. The register does not only
  explain a client's silence; it predicts when the enquiry will land.

`data/companies/barnfield-construction.md`, `adminbase.json` (leads 5625, 5991, 6157, 6781, 7665
`worked`), `jacob_daily_email.py` (`SRC_RESEARCH`).

---

## 30/07/2026 (late) - the board was telling Adam to ring five dead jobs, and hiding the one due today

Own time, standing agenda, nobody had written to me. The finding is one sentence: **the two biggest
rows on Adam's chase list were jobs I had already established were dead, and the biggest unworked
row on the board was invisible.** Both halves are mechanical, both were silent, and both had already
been flagged in bd.md in a different disguise.

### 1. RESEARCH THAT DOES NOT LAND ON THE ROW CHANGES NOTHING - a company file is not a board

29/07: Adam answered JAC-9 by forwarding Darren Trigg at GCS - *"both Aylesbury High School and
Churchdown School Academy were CIF (condition improvement fund) bids and they were unsuccessful in
securing funding, please keep all information to hand though as they are likely to resubmitted later
this year."* I wrote it into `data/companies/glazing-consultancy-services.md`, said so on the hub,
listed the six rows it killed - **and never touched the rows.**

30/07, Adam's own daily email: **Mobius Group, GBP 746,617, "chase them for a final answer"** at
position 34, and **Southern Projects, GBP 729,117**, at 39. Three more Churchdown rows and Aylesbury
were invisible for the separate reason below. A Commercial Director ringing five contractors about a
GBP 3.4m school with no funding is worse than not ringing: it tells five clients we do not know what
is happening on our own quotes.

**Churchdown went out to FIVE main contractors** - GCS, Kemdoc, Mobius, Roof Estimating Services,
Southern Projects - at two price points GBP 17,500 apart, all on site postcode GL3 2RB. **One
funding decision kills five leads that share nothing but a site.** Six `worked` overrides now carry
the funding failure and a `blocked` reason, so all six are NAMED on the email and none is chased. The
diary date is late September, before the autumn CIF window, and the ask is to be the number inside
the resubmission rather than to be asked after it.

The rule: **when research changes a row's meaning, write it ONTO THE ROW the same session.** bd.md
already said "check the row is still on the page" twice, both times about a row vanishing. This is
the third face of it - the row stayed exactly where it was, carrying an instruction the file behind
it contradicted.

### 2. THE DATE TEST DROPPED EVERY ROW WITH NO DATE: 80 rows, GBP 7,031,168

`jacob_daily_email.collect()` selects on `when <= TOMORROW`, and **AdminBase leaves the follow-up
date empty on 80 of its 264 rows.** Not one of them was in either section, or in the folded count, or
in the "blocked and named" line. The docstring said "Nothing is dropped for being old, unverified or
CRM-generated ... the only two things that come out are the ones named above." It was wrong.

What was in there: **Balham Hill Estate, Re-gen (UK) Construction, GBP 833,609** - the largest
unworked row on the board. **Tiverton Road, Alexander James, GBP 547,886**, where the client had told
us they were preferred bidder. Churchdown x3, Aylesbury, Stepnell's St James House, MacDermid
Autotype, Hastoe's Chorleywood Grange. Three separate fixes have now been made to this one test -
blocked rows (Brandon), worked rows (MSM Aerospace), and now simply undated ones - **and each time
the hidden row was among the largest on the board, because AdminBase's biggest rows are its oldest.**

An undated row is now due TODAY under `SRC_UNDATED`, whose label says "AdminBase set NO follow-up
date on this row at all, so it has never been due; listed today rather than never". That is the whole
difference from inventing a chase date: a blocked row keeps its silence because it has a REASON not
to be rung. These had no reason at all. Adam's email is 199 rows, not 137, and if he wants the tail
off it he can say so - what he cannot have is it missing without being told.

### 3. A DE-DUPE ON THE CUSTOMER IS NOT A DE-DUPE: another GBP 879,925

Same function, two lines further down. The register and the CRM overlap, so AdminBase rows were
skipped when `client` matched a client on the verified register - **which dropped every OTHER live
quote for that customer.** Five more Elkins quotes behind Brandon Estate (GBP 339,384), six more
Bradford Watts (GBP 295,674), Reynolds at Oldswinford, Chester Thomas's Earls Barton door: **14 rows,
GBP 879,925.**

The comment three lines above it already says *"Held by KEY, never by client name. hub-77 put three
JOBS with Mary, not three customers, and excluding on the customer dropped three live Stepnell
quotes."* The `held` test was fixed and the `on_board` test right next to it was not. **When a bug is
a habit of thought, fix every instance in the function, not the one in the traceback.**

Now: same client AND (the same money to within 2p, or two job words in common that are not the
generic furniture of a job title - school, road, house, unit, replacement...). Two refinements the
cases forced:

- **A PENNY APART IS THE SAME JOB.** The register holds St Mary's at GBP 174,546.37 and AdminBase at
  174,546.38, because one is a VAT-inclusive figure divided back down. Penny-exact printed it twice.
  Elsewhere on this board penny-exact is the test that tells a re-quote from the same quote still
  open - **that is a different question about the same number, and it keeps its exactness.**
- **Generic words defeat token matching.** "Oldswinford Primary School" and "Crestwood Park Primary
  School" share two words and are different schools.

### 4. ALEXANDER JAMES - GBP 1.9m, six rows, three contacts, and the answers were in commercial@

Ranking the board by client instead of by row: **Alexander James, six live-quoted rows, GBP
1,910,810 ex VAT - the largest single-client exposure here**, larger than Barnfield, with no company
file, no chase and no mention anywhere. Filed under two spellings ("Alexander James", "Alexander
James Contracts") and split across three contacts, which is exactly how it stayed invisible: **no one
person at Fenster was talking to all of it.**

One domain search answered two of the six:

- **BROOKLANDS COLLEGE, GBP 317,887 - LOST.** Kieran Santry, 07/05/2026: *"Unfortunately we didn't
  secure this project."* **Our client lost the main contract** - nothing to do with our price, and it
  had been on the chase list ever since.
- **TIVERTON ROAD, GBP 547,886 - PREFERRED BIDDER.** Kieran, 05/06/2026: *"We are the preferred
  bidder but still waiting for the council to give us a start date. Come back to me in 6-8 weeks and
  we should know more."* Paul Taylor: *"Perfect, I'll be in touch then."*

**A PROMISE WE MADE IS A CHASE DATE THE BOARD CAN COMPUTE.** Six to eight weeks from 05/06 is 17/07
to 31/07/2026 - it expired while the row sat undated and invisible. Leys Park taught that a client's
public deadline sets the chase date; this is the same rule pointing inwards. **"Come back to me in N
weeks" is the most reliable next-action date on this board and nothing was reading it.**

And the source is worth as much as the finding: **both answers were sent to PAUL TAYLOR, a project
manager, who opened one of them with "I believe you were previously speaking with my colleague
Jayk".** Jayk sold 25% of everything Fenster has ever won, and his book is being picked up quietly by
a PM nobody has counted. Both of his chases got a same-day answer. **Before concluding a client is
silent, search commercial@ for a colleague's name - the follow-up may already exist and be working.**

### 5. THE OTHER BOT HAD ALREADY DRAFTED IT, AND HER DRAFT HAD A WRONG ADDRESS ONLY I COULD FIX

Adam forwarded A Plus's feedback chase to jacob@ on 28/07 with *"Jacob, please provide an update for
Dan."* I wrote a full reply from scratch - and `drafts.json` already had **D-6, the same email**,
built on Mary's reading of estimating@ (every issue date, folder states, three jobs needing a
sentence each). Worse, my append script filtered on the id I was about to use and **deleted hers**;
`git checkout HEAD --` put it back.

Two rules out of that. **Read your own output files before producing the same artefact** - a
hand-appended JSON list has no unique constraint, so an id collision is silent. And **the honest move
was to correct her draft, not replace it**: what it lacked was the one thing only I could supply. It
carried `dan@aplusw.co.uk` with the caveat *"not verified by me - Dan's mail to Adam sits in a
mailbox I cannot read."* Adam had forwarded that very mail into jacob@, so it is now on the record:
**Daniel Charlesworth, Sales & Estimating Manager, daniel.charlesworth@aplusaluminium.co.uk, 01923
225855.** A draft that had been waiting on approval for a day was addressed to a wrong mailbox.
**The unverified field in the other bot's work is where your own mailbox is worth the most.**

Also from that thread, and it is Mary's rather than mine: A Plus price on a **baseline, an improved
rate over GBP 15k and a further improved rate over GBP 50k**, in place since roughly late 2025, with
a price increase in April 2026 and a surcharge from 18/05/2026 - and on large projects they are
*"already going in at very fine margins"* and unlikely to better them in that system, though they
will look at VE. Passed to her, not used by me.

### 6. AND THE ONE I HAD WRONG UNTIL I READ HER WORK

I had Darrick Wood, GBP 255,082, down as "quoted 26/05, 65 days silent, never chased". It is nothing
of the kind. Submitted through **AJ Group's own portal on 04/06**; **Gleb Saliev, 09/07: "I have now
completed my review of your quotation and, unfortunately, the quantities and dimensions included are
incorrect and do not comply"**; Adam replied on 10/07 that we would revise; A Plus were asked 17/07
and Dominic Palethorpe returned QT50911 Rev1 on 24/07. **The client is waiting on US**, and nothing
on my side shows the revision going back - the fourth job this month whose price may have stopped
inside Fenster, after Chiel, Alkerden and Bradstone. Asked of Mary, 30/07.

Two things hid it. **This client runs enquiries through portals** - EstimateOne on Emmbrook, AJ
Group's own on Darrick Wood - so their notices never touch my four mailboxes and a domain search
finds only our outbound: the E T & S shape exactly. And **Gleb is not a stranger to ring cold, he is
the man who rejected our take-off**; the ROW was unchased, the CONTACT was live. A quantities
rejection on a GBP 255k package is a fact about the quote and not the relationship, and it is Mary's
to weigh.

`data/companies/alexander-james.md`, `drafts.json` D-6 (corrected) and D-7, `adminbase.json` leads
7009/7098/7139/7159/7267/7268 and 7282/7285/7388/7391/8221/8368 `worked`, `jacob_daily_email.py`
(`SRC_UNDATED`, `same_job_on_register`).

---

## 30/07/2026 05:04 - Pride Developments: ten rows called a live customer silent, and a de-dupe that could only see other people's duplicates

Standing agenda, own time. Ranked the board by RESOLVED client rather than by row and took the
largest exposure nobody had ever opened: **Pride Developments Group Ltd, ten live-quoted AdminBase
rows, GBP 1,092,450 ex VAT** - third behind Alexander James (1.9m) and Elkins (whose 7.5m is one
confirmed do-not-chase row), and the only one of the three with no company file, no ledger mention
and no research on any row.

### 1. Silence is a property of the RELATIONSHIP, never of the row

Every one of the ten printed *"chase Pride Developments for a final answer - N days silent"*, to 265
days. At the moment it said that:

- Graham Nash (their Senior PM) and Paul Taylor had been back and forth through July on **RAF
  Mildenhall PD7730** - frames delivered 29/07, install **30/07/2026, the day the board said it**.
- **St Catherines House PD7758** (3 alu vertical sliders, PO1526) was fitted **09/07** and Paul sent
  O&Ms 13/07; Reza Shemshaki, Stephen Prime and Jayne Nash are all live on that thread.
- Their Senior QS **Leonard White invited us to tender on 22/07**, and **Adam priced it to him at
  11:14 on 29/07**.

So ten rows were each genuinely unanswered while the client was never silent for a day. **A CRM holds
one row per job; a relationship belongs to the client.** The clock is computed per row and the word
it produces is a statement about the client. This is the third instance of the silence clock naming
the wrong party (Alkerden, RSR, now Pride) and the first where the row-level arithmetic was correct
and the *sentence* was still false. Nothing on the board resolves per-client last contact.

Two smaller date faults in the same family:

- **A follow-up date can PRECEDE the lead date.** Six rows do. Lead 8701 (Probation Office, Usk
  House) is dated **21/07/2026** with a follow-up of **23/06/2026** - a month before the enquiry
  exists - and the row is aged off the earlier date, so a nine-day-old quote printed as 35 days
  silent. The other five are off by a day or two.
- `days` on every row is computed as at the export date (28/07), so the whole file runs two days
  stale. Harmless until somebody quotes the number out loud.

### 2. The mirror of the customer de-dupe - the sixth instance of one function

The AdminBase page has flagged "one scheme, several bidders" since 28/07: GBP 2.35m of pipeline is
the same job counted more than once, found on the **penny-exact ex-VAT figure across different
customer keys**, because one estimate sent to five main contractors carries one number while the site
gets typed five different ways.

**It cannot see a job the SAME client asked us to price twice.** The grouping requires two different
customer keys, and the value join requires one figure - and two quotes for one job are priced at two
different figures by definition. Invisible twice over, and the exact mirror of the bug fixed on 30/07
04:04, where a de-dupe *on the customer* dropped 14 rows that merely shared a client with the
register.

Found through Pride and worse elsewhere. **Six sites, thirteen rows, up to GBP 468,681 counted more
than once:**

| Client | Site | Rows | Total | Counted twice, at most |
|---|---|---|---|---|
| **Stepnell** | ST JAMES HOUSE, Mansfield Rd, Derby | 3 - 382,092 alu / 177,206 secondary / 5,106 alu | 564,403 | 182,312 |
| **Pride** | ST CATHERINES HOUSE, 5 Notte St, Plymouth | 2 - 295,882 **alu** / 237,382 **uPVC** | 533,264 | 237,382 |
| Lindum | Howden Fire Station | 2 - 53,576 alu / 3,792 screens | 57,369 | 3,792 |
| SDevs | 16A Groveside, Bookham | 2 - 30,395 / 24,604, both uPVC | 54,998 | 24,604 |
| Cranfield | Main Block / Test Area buildings | 2 | 34,963 | 13,833 |
| Kumon | Walker Ave / MK Skin Clinic | 2 | 22,348 | 6,759 |

**Stepnell's ENTIRE GBP 564,403 exposure is three rows at one Derby building** - the client I had
ranked twelfth by value is, on one reading, one job.

**Named, never merged, and that is the whole design.** Half of these are legitimately two packages:
aluminium against **secondary glazing** at one address reads as two scopes, aluminium against
**uPVC** reads as a choice between two, and "Main Block" against "Test Area Buildings TH4 TH5" are
two jobs at one university. The `product` column is the tell and a human settles it. Merging on my
own reading would be the same sin as closing a row on my own arithmetic. `sameSite` in
`adminbase.json`, panel on AdminBase (raw), `atRisk` is a CEILING on the error and not a claim.

Matching rule: same customer key **and** same postcode **and** at least one shared job word that is
not furniture (HOUSE/ROAD/SCHOOL/CENTRE/BLOCK and the rest are stripped, or a school and its sports
hall merge) **and** two different values (identical values are the multi-bidder case above).

### 3. What the account actually is, and why a chase was the wrong tool

- **Four won contracts, GBP 59,999 net, all sold by Adam personally**: Merthyr 25,649 (fitted
  11/06/26), Rubery Library 24,097 (29/01/26), St Catherines 6,139 (09/07/26), RAF Mildenhall 4,115
  (in progress). **Every win under GBP 26k. Every quote over GBP 50k open or lost.**
- So **4-for-4 small, 0-for-many big, from a client who keeps asking** - Barnfield's lesson with a
  size split inside one client. The funnel bands are not only a company average; they run per client,
  and the question worth a call is what we are beaten on, not whether it is still live.
- **St Catherines House is the sharpest version.** We built three windows for GBP 6,138.85 at the
  address where GBP 533,264 of our quotes still read "live", and Vincent Adurosakin's March enquiry
  that became that order says a colleague passed him Adam's details - it arrived as a fresh
  small-works enquiry, not as a revival. Either the package is phased and ahead of us, or it died and
  became three windows. **Nobody has ever asked.**
- **Jayk left Pride off his 19/12/2025 repricing log entirely** - 62 rows, 27 clients, written while
  both Plymouth quotes plus Exmoor Drive and Maddock Way were freshly out. Absence of evidence, but
  the kind that usually means he knew.

### 4. Companies House says when a company CANNOT be qualified - and read the wind-up type

**PRIDE DEVELOPMENTS GROUP LTD, 16138608**, incorporated **16/12/2024**, active, **GBP 100 capital**,
Unit 8 Forgehammer Industrial Estate, Cwmbran NP44 3AA. **No accounts filed and none due until 16
September 2026.** So there is no public financial information whatsoever on the entity holding
GBP 1.09m of our prices. That is the calendar rather than a judgement - and it is the reason a
GBP 322k order from them is a different conversation from a GBP 3k one. Balances of 6,138.85 and
4,114.98 sit at full contract value on the two 2026 jobs: read as uninvoiced or inside terms, not
debt, and flagged only so nobody opens a call thinking they owe us money (the Conamar lesson).

**And the negative I went looking for, because it would have read as a story if left out.** A
Porretta-named predecessor exists at the same unit - 06679882, **PORRETTA LIMITED to PRIDE INTERIORS
LIMITED to KRUZ (UK) LIMITED**, Lyndon Porretta sole director - dissolved 09/02/2022. It was wound up
by **members' voluntary liquidation with a filed declaration of SOLVENCY** (LIQ01, 19/09/2018), by
the same director. A solvent wind-up. **Dissolved is not failed: read the liquidation TYPE before a
dissolved namesake becomes a credit history.** Same discipline as the single-word-name rule, one
register across.

### 5. Resolve the contact before calling a row cold

**`lyndon@pridedevelopments.co.uk`, the contact on lead 7807 (130 Hainault Road, GBP 82,823, quoted
26/02/2026, never chased) is LYNDON PORRETTA, a DIRECTOR** of the company, appointed 10/09/2025. The
warmest name on a million-pound account, sitting on the board as a first name and an email address
that nothing ever asked about. Ten seconds on the officers list. He is also the one person who can
answer the Plymouth question.

### 6. Redditch Library - Mary's, and two BD facts on it only

Her `data/jobs/redditch-library.md` is the authority and I did not touch it. On my side:

- Adam's 29/07 email asked Leonard White the two best questions on the account - how our number
  compares with the others, and **when they are submitting cost** - and **nothing has come back**.
  That submission date is the deadline the pack must beat, the Leys Park rule inwards; and it is
  Adam's own thread, so it is a reply, not a new approach.
- Leonard holds **GBP 89k** against a live tender sum of **GBP 94,926.76** (Mary, flagged to Adam
  12:26 on 29/07, reconciled to the penny in her file). Competitor is **Joedan**, who fabricate their
  own frames. My part is only that a client comparing prices holds a figure our formal quote will
  exceed - the number is hers.
- The enquiry landed at **info@ on 22/07 and took six days to reach estimating@** (Adam: *"it got
  missed and has been with us for 6 days!"*). Fourth real commercial tender to arrive at a mailbox
  that is off my intake list; Adam has since settled the routing, so the next delay would be at the
  vetting step rather than the pipe.

### Changed

`jacob_adminbase.py` - twelve `worked` overrides (8558, 7249, 7356, 7807, 8463, 7103, 7157, 8701 and
four small rows written once in a loop rather than pasted four times), plus the `sameSite` detector,
its three totals and a console line that says out loud why the panel above it cannot see these.
`dashboard/public/app.js` - the "One site, the same client quoted twice" panel.
`data/companies/pride-developments.md` (new, 152 lines). `bd.md` +26 new lines, 13 paid for by
rewriting the over-cap banner from 21 lines to 9 - the last compression of that kind available here.

**Verified on the live page, not just in the file** - the twice-burned rule. All twelve rows still
appear on Today with their new text, "final answer on B239" returns zero, and the new panel renders
with all six sites. The check that first said the panel was missing was my own bug: `innerText`
returns the CSS-uppercased heading, `textContent` does not.

## 30/07/2026 07:00 (standing agenda) - Re-Gen / Balham Hill: the biggest row on the board is two packages, and one of them was UNDER the number the client gave us

**AdminBase lead 7796, Re-Gen (UK) Construction, Balham Hill Estate East and West SW12,
GBP 833,609.31 ex VAT - the largest single row on this board, never researched, and the
board's whole instruction on it was "153 days silent, chase for a final answer".** Every
part of that turned out to be wrong. Not in the ledger; no company file; `mary_recall
--grep "Re-gen"` and `--grep "Balham"` both returned zero, so neither bot had ever touched it.

### The account

- **15/05/2025** - Kyan Gulliver, Estimator, sends the pack. Spec of Works Rev E, 293 pages.
  **23/05/2025** - quote out, **GBP 171,178**, priced in **Liniar** and at **1nr of each
  window type** rather than the real quantities.
- **29/01/2026 15:24, commercial@, "URGENT ATTENTION: Re-Gen - Balham Hill"** - Jayk, after a
  phone call with **Liam Ryan**: *"They have won the above-named project... our Curtain
  Walling cost is cheaper than the competing firm. Our Windows are expensive compared to the
  competing firm. They would like us to reprice this job and get the quote down as far as
  possible so that we can secure it. The competing costs are as follows: Windows @ 500k /
  Curtain Walling @ 150k... Our original quote was incorrect as we quote for 1nr of each type
  of window. There are 850 windows in total. The project is due to kick off on March 23rd. It
  may come down to us being awarded the Curtain Walling and the Competitor awarded the Windows
  based solely on price. We have quoted for Liniar but they want a VEKA or ReHau system... The
  programme calls for the install of 50 windows a week."*
- **02-24/02/2026** - repriced. A Plus QP65670 (23/02), Titan Trade Windows, Vetroseal 060809,
  SS Q092044. **Quote REV 1 dated 02/02, files finalised 24/02 13:39, AdminBase lead raised
  25/02 at GBP 833,609.31.**
- **Nothing since 24/02/2026.** No client reply in commercial@, info@ or jacob@; no further
  file in the tender folder; nothing in the 30-day intake. 156 days.

### ONE CRM ROW WAS TWO PACKAGES, AND THE BOARD CHASED THE SUM

REV 1 has two sheets and they add to the AdminBase figure **to the penny**:

| | Ours | Liam's target | Delta |
|---|---|---|---|
| Curtain walling | **142,760.00** | 150,000 | **-7,240 (-4.8%)** |
| uPVC windows, **852** nr | **690,849.31** | 500,000 | **+190,849.31 (+38.2%)** |
| | 833,609.31 | 650,000 | +183,609.31 |

So the largest "exposure" on the board is not one prospect at all. **GBP 142,760 of it came
in UNDER the number the client himself set, on a split he told us in writing was likely -
and nobody has spoken to him since.** The other GBP 690,849 went out 38% above a target we
had been handed three weeks earlier. Chasing the sum asks the client to answer a question he
already answered, about a number he never had to consider as one thing. (852 is the count in
REV 1 - Jayk's "850" was the phone version. The optional EPDM and mastic lines, GBP 63,065
across both sheets, sit outside those totals.)

### THE APPROVED-MANUFACTURER CLAUSE WAS IN THE PACK ON DAY ONE

The employer is **Wandsworth Borough Council**, Housing Department; ref **C6445**. Contract
administrator **HJP - Hughes Jay & Panter Ltd**, chartered surveyors, Sutton, 020 8661 2228,
mail@hjpsurveyors.com, ref MM/MJ/5421. Form: **JCT 2016 Housing Intermediate Works
(Amended)**. The main contract is *External and Communal Decorations including Roof and
Window Renewals*, which is why nothing about it appears on Contracts Finder under "Balham
Hill" - **search the WORKS TITLE, not the package you want.**

**Appendix J, page 214 of 293 of the documents we received on 15/05/2025**, is Wandsworth's
own *Replacement Window & Door Performance Specification Rev D, Sept 2020*. Clause 2.6: *"The
replacement windows are to be selected from the following manufacturers"* - **Rehau, VEKA,
Kommerling (profine), Schueco, Deceuninck.** Liniar is not on it. We priced Liniar, and heard
about it **eight months later, on the phone, from the client.** "Liniar is unapproved" was
never Liam's preference; it was a clause in our own tender pack.

**READ THE PERFORMANCE SPEC BEFORE THE SCHEDULE OF WORKS. An off-list profile voids the bid
before the price is read, and the pack always says which list.**

### AND OUR CLIENT WINNING IS NOT STEP TWO WHEN THE EMPLOYER VETS THE SUBCONTRACTOR

Clause 2.1 of the same spec: *"Evidence of their current status as licensed fabricators and
installers shall be submitted by all companies at the time of tendering, and any company not
considered by the Council to be appropriately registered shall not have their tender
considered."* Plus PAS 24:2016, BS 7412 Kitemark, BS EN ISO 9001:2015, Secured by Design.

That is the mechanism behind this client's other job. BD log, Barham Park, 21/11/2025:
**"Re-Gen secured this but the client has chosen their own window contractor - Liam suggests
a brown envelope has been handed over."** Re-Gen won the main contract there too and it made
no difference to us. So the standing line that five repricing rows *"name a main contract OUR
CLIENT HAS WON - step two of the whole job, already done"* needs its edge: **on a council or
HA job under a JCT with a performance spec, step two is the EMPLOYER'S surveyor, not our
client.**

### A KICK-OFF DATE IN OUR OWN MAILBOX BEATS ANY SILENCE COUNTER

Kick-off was **23/03/2026 - 129 days ago.** At the programmed 50 windows a week, 852 windows
is seventeen weeks, so a job running to time finished its window package around **20/07/2026,
ten days before the board printed "is it still live".** Every other silence lesson here has
been about the clock naming the wrong party; this one is simpler - **the client told us when
the work would start and how fast it would go, and that arithmetic answers the question the
chase was going to ask.** Look for a programme before counting days.

### The route nobody has taken

**HJP Surveyors write Wandsworth's window specification and administer the contracts, and
Fenster has never contacted them.** One hit for "hjp" across all four of my mailboxes and it
is our own copy of their spec. They are a contract administrator with a housing decs practice
across South London: getting Fenster's licensed-fabricator evidence in front of the Council
under clause 2.1, on one of the five approved profiles, is a route onto a stream of work
rather than one lead. **The CA or surveyor who writes the spec is a better target than the
contractor who has to obey it** - and it needs Adam's decision, because it is a new
relationship, not a chase.

### Two false positives worth writing down

- **REGEN London (`regen-london.com`, Faaris Merali, Snap Fitness gyms) is not Re-Gen (UK)
  Construction.** They wrote to commercial@ on 28/07/2026 about a louvre replacement in SE11.
  A grep on "re-gen" over the intake merges them; all five recent hits were theirs.
- A "Wandsworth" search turned up a **Window Cad Enquiry** Paul Taylor chased on 07/01/2026 -
  *"a replacement glass unit at The Town Hall Wandsworth High St"*, which is the exact address
  of the Housing Department in this spec. It is **not** a Council contact: it came through
  WindowCAD to an iCloud private-relay address, one unit, a domestic job. **The right address
  on the wrong scale is still the wrong lead.**

### Open, and not mine

REV 1 names **Titan Trade Windows** as the supplier and nothing in the pack or in commercial@
says which of the five approved profiles that is. If REV 1 is also off-list then the reprice
was void before it was read - Gintare's and Mary's question, not mine. And **whether REV 1
ever left estimating@** on 24-25/02 is unproven in my four mailboxes; asked Mary 30/07. The
difference between a chase and an apology turns on it, for the fifth job this month.

### Changed

`jacob_adminbase.py` - one `worked` override on 7796 (state, owner Adam, next action, why,
note). `data/companies/re-gen-uk-construction.md` (new). `bd.md` +11. Row verified still on
Today after the state string changed - the twice-burned rule.

## 30/07/2026 07:30 - Mary answered nine "did it go" questions: seven had gone, and my board was calling a live job lost

Msgs 33-37, all `wants_reply=0`, all answering questions I had raised across the previous sessions.
The batch is one lesson with five instances, and it is the most expensive reading error on this side
of the wall.

**A quote leaves Fenster from whichever mailbox the PERSON HANDLING IT uses - `jayk@` (a hard 404),
`adam@` or `estimating@` - and never from commercial@, info@ or jacob@. Neither AdminBase nor the
Opportunity Log records a send at all.** So "nothing in my four mailboxes" carries no information
about whether a quote was issued. Across the nine questions **seven quotes had gone and I could see
none of the seven.** Mary's own framing: ask, do not infer - which is what I did, so the batch is
confirmation rather than correction. The rule is now in `bd.md`.

### What each one changed on the board

- **Bradstone Road, 5625, GBP 218,917 - THE ONE THAT MATTERED.** My row said "lost on price
  01/05/2025, DO NOT chase Ian Brown", on Adam's chase list, in Adam's email. It is **live**: it came
  back after the May 2025 loss and was priced and issued twice in 2026 - Vetroseal 060676 on 02/02,
  jayk@ to Ian Brown 06/02 with an attachment, Adam to Ian four times in forty minutes on 12/03, BSW
  re-quoting 19/03, estimating@ to Ian 20/03 with an attachment, and **Adam's own message of 12/06,
  the most recent contact on the job.** Row now says live, and says nobody rings Ian about Bradstone
  without reading Adam's 12/06 first. The May 2025 loss was still real and still recorded nowhere but
  a reply to a glass supplier - that lesson survives; the "dead" conclusion does not.
- **The Grange Apartments, 7665.** Issued twice - 05/03 to Ian Brown, then **reissued 01/04 to Oliver
  Webber, who replied 90 minutes later.** AdminBase's "Live - Quoted" was right and the BD log's empty
  Quote Returned cell was wrong. **The chase is Oliver Webber's; the CRM carries the client's original
  contact and no field records that the job changed hands.**
- **St Catherines House, 7249 and 7356.** Settled: **one job priced two ways**, in Jayk's own covering
  words on three sends - aluminium 18/12, uPVC 13/01 ("we have included the Aluminium Curtain Walling
  elements within this quote as well"), then 16/01 "either the uPVC or aluminium option". So **GBP
  237,382.29 comes off Pride's exposure** - named on the `sameSite` panel, not merged. Contact is
  Steven Elley, who is on neither row.
- **B239 / PD7851, 8558, GBP 321,833.** My row said "do not chase until somebody says what this is".
  It was a **thirteen-message negotiation with Daniel Goornaden, 26-29/06, through adam@, three
  attachments out on 29/06 alone.** Not a mystery - unidentified BY ME. **Adam is a cheaper source
  than a search and I did not ask him.**
- **Chiel/Swanshurst, 7384.** The quote went 22/12/2025 from jayk@. **Only one of the three things
  Chris asked for went** - no Contractor Evaluation Form, no Compliance Statement, no Insurance
  Verification, no programme, and **the PQQ is what decides whether Fenster is allowed on his tender
  list at all.** He was chased once, 16/02, with nothing attached: "any movement on this project". So
  the opening is the pack he asked for seven months ago, which is a reason to ring rather than a
  nudge. **PARTIAL DELIVERY LOOKS EXACTLY LIKE DELIVERY IN A CRM.**
- **The Hub Alkerden, 5493.** No updated quote has gone (three weeks past their 08/07 deadline) - but
  **Seyi was answered by Adam in six minutes on 01/07, and Adam asked Seyi a live Velfac
  specification question on 02/07 that has never been answered.** So it is not an apology: it is "we
  have been waiting on your Velfac answer since 2 July, here is when you will have the quotation."
  **Do not draft the apology before checking who is actually waiting on whom.**
- **Darrick Wood, 8368.** The one I had right, and worse than I had it: no send, **and no internal
  "quote to check" to Adam either** - the step that always precedes an issue here - so A Plus's
  revision has sat unopened since 24/07 and the job is **not yet re-priced**. Apology and a date.
- **Library and Brandon Youth (7157) and 130 Hainault Road (7807): NO TRACE, which is "not found",
  not "never sent".** A nil result on a job NAME is weak evidence where our own files misspell things
  - this same batch has Chiel filed as "Cheil" and Swanshurst as "Swanhurst", both wrong and both
  consistent, and Spoone School went out under another name entirely. Sent Mary the enquiry contacts
  to search on instead; neither row carries a PD number.

### Two contact corrections, one of which caught a second row

**Gleb Saliev is `gleb.saliev@ajgroup.co.uk`** - the 2025 traffic used `alexanderjamesltd.co.uk`, so
searching the old domain loses everything from 2026. **That flushed out a row Mary was not writing
about:** Tiverton Road, GBP 547,886, the largest Alexander James row here, carries
`kieran@alexanderjamesltd.co.uk` - the same dead domain, on the one row where the callback is OURS to
make and the promised window closes 31/07. Row now says ring, do not email, address unconfirmed,
phones good. **A contact correction on one row is a search to run across every row sharing the
domain.**

### Changed

`jacob_adminbase.py` - eleven `worked` overrides rewritten (5625, 7665, 7249, 7356, 8558, 5493, 7384,
8368, 7157, 7807, 7388). `bd.md` +13. Verified every one of them still renders on the live
`/api/jacob` after the state strings changed.

## 30/07/2026 07:24 - Mary corrected the Balham Hill account inside the same session, and every fact was already inside Fenster

Msg 39, `wants_reply=0`, arriving two hours after I posted the Re-Gen account to the hub. It falsifies
four things I had written and confirms one. **Both statements it killed were in what I had already
sent Adam**, so the hub carries a correction.

### What was wrong

1. **"Nobody has spoken to him since February" - false. ADAM CHASED ON 12/03/2026 12:19**, adam@ to
   Danny Hartland cc Liam: *"check in on the status of this job... Jayk as left the company so I will
   be taking on his role... let me know how Balham Hill is shaping up and whether you have any new
   tenders... my mobile is 07939452711."* **No reply in 140 days.** They have had his name, role and
   mobile since March and not used them. So the call is Adam's **second** chase, following up his own
   unanswered email - a different opening entirely, and a stronger one. **CHECK FOR YOUR OWN SIDE'S
   CHASE BEFORE CALLING ANYTHING A FIRST APPROACH.**
2. **"REV 1 may have been non-compliant" - false, and it was the opposite.** Ashley Walton at Titan
   confirmed in writing on 24/02 14:24: *"the quotation we provided was in the REHAU TOTAL 70 62MM
   OUTER FRAME"*, with three Rehau Total70 data sheets attached. **Rehau is FIRST on clause 2.6's
   five permitted profiles.** The reprice did not repeat the Liniar mistake, it **fixed** it, and the
   data sheets went to Danny at 14:42 the same day so Re-Gen hold our profile evidence. **A
   COMPLIANCE FEAR IS AS UNSOURCED AS A COMPLIANCE CLAIM.** I flagged it as a question rather than a
   finding, which was right, but it still went in front of Adam and it was still wrong.
3. **"Nothing since 24/02" - false. THEY REPLIED THREE TIMES IN TWENTY HOURS, collecting evidence:**
   13:57 Danny rang for data sheets on both systems, 14:42 Jayk sent the Rehau sheets, 17:44 Danny
   asked for curtain walling data sheets too, 25/02 09:17 Jayk sent DS_TECHNAL_TENTAL_50. **The
   silence starts 25/02 and it follows an ENGAGED client, not one who never got the price.** That is
   a materially different account of the same 156 days.
4. **The quote went to a contact on NO row of my board.** 24/02 13:42, jayk@ to
   **Danny@re-genuk.com** - Danny Hartland BSc (Hons) MCIOB, Quantity Surveyor, DD 01277 563 359 - cc
   Liam, Adam and estimating@. **Three contacts, one per stage: Kyan raised the enquiry, Liam rang
   with the intelligence, Danny received the return.** A QS who joins at return stage is invisible to
   any search on the contacts we already hold, **which is why the DOMAIN beats the names.** The cover
   sheet carried CW £142,760.00 and uPVC £690,849.31 - my two figures to the penny, so the split was
   right even where the story was not.

### What was confirmed, and it is the check that mattered most

**The fire egress caveat IS on the issued cover sheet.** Bedford Trade Glass told us on 30/01 that
none of the designs meet fire escape; Jayk priced without egress and the issued document says
*"Some of the windows does not meet the Fire egress requirements. Design would need to be
adjusted."* **852 windows with no escape openers and no caveat would have been a live liability.**

### The loop that actually cost the windows, and it was internal

Adam, 24/02 12:14, before the quote went out: *"good to send out... I spoke to them before and looks
like we're out of the running for the windows due to costs... submit the quote but in the meantime we
could as Quickslide to price the uPVC in case there's a chance we can bring our costs down
considerably."* **QUICKSLIDE WAS NEVER ASKED.** The first Quickslide enquiry anywhere in estimating@
is 06/03/2026, for 130 Hainault Road. So the one action that might have moved £690,849 toward
£500,000 was **the Commercial Director's own instruction, and nobody carried it out.** Kick-off was
23/03, so it is history rather than a save - the St Mary's shape, third instance.

### The lesson under all four

**Every fact that mattered on this account was already inside Fenster, and none of it was in a
mailbox I can read** - the competitor's prices, the approved-profile clause, the programme, the send,
the client's replies, Adam's chase, Adam's own instruction. The board reduced the lot to *"GBP
833,609, 153 days silent, chase for a final answer"*. **The failure was never information; it was
that nothing joined it up.** And on a single account, in a single session, I published two false
statements to the Commercial Director because I inferred from silence in my own half twice after
being told that morning not to. **Ask the other bot about a send. Ask Adam about a job he has
worked.** Both were one question away.

### Changed

`jacob_adminbase.py` - the 7796 override rewritten (second chase, three contacts, Rehau, the caveat,
the Quickslide loop). `data/companies/re-gen-uk-construction.md` corrected throughout, +53 lines.
`bd.md` +11 on top of the entry it corrects. Hub correction posted to Adam. Verified on the live
`/api/jacob`.

## 30/07/2026 06:34 - the second ask found both, and Tiverton runs through a portal (msg 41)

**Final tally on the batch: TEN of TWELVE quotes had gone.** Msg 37 had returned nil on the two Pride
rows; msg 41 found both by **searching the CONTACT rather than the job name.**

- **Brandon Youth Centre / 19 Maddock Way (7157)** - sent 24/11/2025 13:20, jayk@ to
  `wayne.edwards@pridedevelopments.co.uk`. **The reason for the silence is on the record: Wayne had a
  competing quote at GBP 38k.** Adam, 24/11 12:42 - *"Job costings are 28k so we can't get close to
  38k, this seems to be a competitive cost that we have provided."* Jayk asked Wayne for the competing
  quote redacted *"to ensure we are quoting Like4Like"* **and Wayne never sent it.** So: lost on price
  **with our own unanswered ask still in it** - GBP 53,209 against GBP 38k on a GBP 28k cost base, and
  a live reason to ring. Adam noted **E2 should have been a Latham's steel door.**
- **130 Hainault Road (7807)** - sent 01/04/2026 09:13, Gintare to `lyndon@` cc
  **`MICHAEL.BETTINSON@`** and adam@. **A PARTIAL QUOTE, and that beats price as a reason for
  silence:** the covering email excludes the double entrance door, one sliding door, the Velux and the
  lantern, and offers the triangle unit in **aluminium instead of uPVC**. Four fabricators tried
  (Quickslide, BSW, Titan Aluminium, Duplus); Mercury never came back on the 2900mm slider. **And the
  CRM date is the ENQUIRY, not the quote** - in 26/02, priced 01/04, opening *"apologies for taking so
  long"*. Five weeks, ours.

### Three new shapes, each worth a line

1. **SEARCH THE PERSON, NOT THE PROJECT.** Both rows were nil on the job name and instant on the
   contact. Our own files misspell projects; they rarely misspell an address.
2. **A SEND CAN BE PARTIAL, AND A CRM CANNOT SHOW IT.** AdminBase records a value and a status, never
   what was in the envelope or what was carved out of it. Second instance today - Chiel got the quote
   and never the PQQ pack. **Before chasing a decision, check the client was given something
   decidable.**
3. **A JOB CAN RUN THROUGH A PORTAL WITH THE EMAIL AS A COURTESY COPY.** Tiverton Road, GBP 547,886 -
   the quote went 22/01/2026 to **AARON@alexanderjamesltd.co.uk**, not Kieran, and Jayk wrote *"I have
   uploaded through the E1 SYSTEM but wanted to ensure these came directly to you as well."* **The real
   submission is on a portal.** So email silence is not the client failing to answer, and **any
   addendum or moved return date is sitting where neither bot can see it** - exactly the blind spot
   that let a GBP 174,546 E T & S tender lapse. The action gains a question: what is on the portal, or
   get access.

### And do not guess a rebranded address

The only confirmed `ajgroup.co.uk` form is `gleb.saliev@` - **firstname.SURNAME** - while the old
domain used bare firstnames (`kieran@`, `gleb@`, `dan@`, `aaron@`). So **`kieran@ajgroup.co.uk` is
wrong by construction**, not merely unverified. There is no 2026 send to Kieran anywhere (last traffic
23/12/2025), and `alexanderjamesltd.co.uk` was still live on 16/02/2026, so the rebrand falls between
then and 09/07 and the old addresses may still route. **Ring.**

### Changed

`jacob_adminbase.py` - 7157, 7807 and 7388 rewritten. `data/companies/pride-developments.md` and
`alexander-james.md` updated. `bd.md` +9. All thirteen rows verified on the live `/api/jacob` with a
cache-buster - **and that matters: the Pages CDN served me a stale payload once during this session
and a verification without `?cb=` can read the previous deploy and either falsely pass or falsely
fail.**


---

# Classification rules that cost a day each to learn

Moved out of `bd.md` on 2026-08-04, verbatim. They were 205 of its 384
lines and every session was loading them whether it was classifying
anything or not. `bd.md` keeps the index; this keeps the evidence, and the
evidence is the half that makes a rule stick.


- **Filter on what a contract IS (CPV families), never on words** - keywords returned window
  *cleaning*, STI *screening*, "the front door to maternity services". **Direction comes from the
  first sentence, not the subject** (our own RFQs are not demand). **Single-word names throw ~20%
  false positives** ("Atlas" = a window cleaner); the `possible` tier needs one human confirmation.
  Same trap via a PERSON'S name: "Thomas Sinden" matched **"Chester Thomas Developments"**, a live row
  on my own board. **Join company names on SUBSET, never overlap**, trading words stripped.
- **THE CRM SPELLS A CLIENT DIFFERENTLY FROM EVERY OTHER SOURCE, AND AN EXACT MATCH IS NOT A COMPLETE
  ONE.** Barnfield is both "Barnfield" and "Barnfield Construction" - an exact hit short-circuited the
  sweep. The log's "Thomas Sinden" is **"Sinden Construction Ltd"**: a GBP 581k job the client HAS WON
  read as absent when it sits there as lead 5493, Live-Quoted since 21/01/2025. **Union every spelling;
  then join on PENNY-EXACT VALUE**, which alone tells a re-quote from **the same quote still open** (18
  of 62). **A TRANSPOSITION DEFEATS BOTH**: "Cheil"/"Chiel" is no subset either way and the CRM row was
  a re-quote at another figure, so **a GBP 52,483 lead where the CLIENT WAS WAITING ON US read as absent
  from the CRM entirely.** Match same-letters-reordered or 0.9 similar, then corroborate on the CONTACT
  or one RARE token - never on the name; **Companies House arbitrates which spelling is real** (Chiel,
  04840215). Tokens miss single-word projects ("Gresty Road" is one word after street furniture).
  **AND IT IS THE CUSTOMER KEY, NOT JUST THE SPELLING, THAT SPLITS A CLIENT - SO EVERY PER-CLIENT
  TOTAL ON THIS BOARD IS A FLOOR.** Barnfield's five live leads sit under THREE keys - the domain,
  the literal string "BARNFIELD CONSTRUCTION", and **`hargreavescontracting.com`** - so the
  concentration panel reported a 3-row client and two 1-row clients instead of **GBP 568,576 ex VAT,
  the largest single-client exposure on the board.** Aggregate on the resolved company, never the key.
- **ODS LINE BREAKS ARE INVISIBLE TO `itertext()`** - Alt+Enter is `<text:line-break/>` inside ONE
  `<text:p>`, and flattening welds sentences: "no decision" + "Worth repricing" = "decisionWorth", no
  word boundary, no regex match. **Six of Elkins' seven rows read as NOT recommended when they were.**
- **A relationship does not put glazing in the job** (Zac, 29/07). Warm/known leads
  must pass the same work-type screen as cold: no scaffolding, cleaning, highways,
  kitchen-and-bathroom, lifts, surveys - whoever won them. `NO_GLAZING` in
  `jacob_dashboard.py`. Roofing stays IN (Raglan roofing carried a Fenster
  rooflight order). Before recommending any call, ask: where is the glass?
- **A BUYER'S CPV IS NOT THE WORK.** Of 21 notices whose TITLE is unmistakably glazing, Adam's list
  caught 10; six misses carry only **45000000 "Construction work"** and adding it would import every
  highway scheme. So a PRODUCT word adjacent to a WORK word **in the TITLE** is promoted to `direct`
  whatever the CPV says: 10/21 -> 18/21. Adjacency traps now excluded - **"door entry"/"intercom" is
  access control, "cubicle tracking" is a curtain rail.** Codes absent from his list are PROPOSED,
  never added (**his list is his**): 44221220, 45343000, 45420000/45421000, 50000000. `bd-lessons`.
- **`app_type` is planning's CPV**: `Conditions`/`Amendment` describe paperwork, not buildings. And
  PlanIt's `parent_name` is one step up a tree, not a country (Adur -> Adur and Worthing -> West
  Sussex -> England) - reading it as one dropped all 454 rows. **A feed returning nothing looks
  exactly like a quiet market**, the most expensive bug shape on this board.
- **Contracts Finder's OCDS `/Search` SILENTLY IGNORES `keyword`** - reads as "not found" when you
  never searched. Use `POST /api/rest/2/search_notices/json`. **Companies House needs no key via the
  public site** (send Chrome); full accounts are iXBRL, so one fetch qualifies a contractor - and it
  also says when one CANNOT be qualified: Pride Developments Group Ltd, holding GBP 1.09m of our
  prices, was incorporated 16/12/24 on GBP 100 and has filed NO accounts (first due 16/09/26).
  **Read the wind-up TYPE on any dissolved namesake before it becomes a credit story** - Pride's
  predecessor at the same unit went by MEMBERS' VOLUNTARY liquidation with a filed declaration of
  SOLVENCY, same director. Dissolved is not failed. `bd-lessons.md`, 29-30/07.
- **Check `oldest/newest/truncated` before believing a count** - a 20-page fetch cap once turned 13-22 days into "180 days of mail".
- **Once For All is Conquest renamed** (`jacob_intake.PORTALS`); else a portal CHASE reads as a fresh enquiry. **A date with no year reads as THIS year** - 90 of 209 AdminBase rows are 2025 quotes shown as "12 May".
- **The register is a FLOOR, never a complete set** - Trafalgar House was live and chased with no Mary chat
  at all; 9 managed rows against ~25 AdminBase quotes raised since 15/06 alone. **And so is AdminBase: FIVE
  clients on Jayk's log are absent from Adam's export entirely - GBP 1,073,229 invisible to every panel
  here** (Clegg 777k, MCS, BC Workspace, Steele & Bray, RG Carter); a quote outside the export window or
  under another trading name lands there too, so it is no accusation. **Cheil was the sixth until 30/07,
  and that one was MY spelling rather than their CRM - the transposition rule below.**
- **"Not in the sends I have dated" means "not in the list that script searches"** - absence from a
  tool reads like never sent. **Count the chases before writing "call them"**; numbers are in the
  signature. `bd-lessons`.
- **Join AdminBase to your own TENDER BOARD, not just to the mailbox** - on postcode SECTOR
  plus title. **A client's public deadline sets the chase date; a fortnight rule invents
  one.** Leys Park, 29/07: `bd-lessons.md`.
- **AdminBase re-dates nothing on a re-quote**; rows joining penny-exact to a NEWER verified send
  are aged from the send. **And the lead date can be the wrong EVENT, not a typo: RFQ OUT IS NOT
  QUOTE OUT** (Brandon 8324; seven such). Expect the slip, do not patch one row. Mary, 29/07.
  **SO "N DAYS SILENT" CAN NAME THE WRONG PARTY - READ THE MAILBOX BEFORE BELIEVING THE CLOCK.**
  Alkerden 5493 read "523 days silent, chase them for a final answer" on a client who had SECURED
  the job and asked US on 01/07/26 for a price by 08/07; supplier quotes were still moving on
  22/07. The date is January 2025's enquiry, never re-dated across two re-enquiries since.
  **AND SILENCE IS A PROPERTY OF THE RELATIONSHIP, NEVER OF THE ROW: SEARCH THE CLIENT, NOT THE
  JOB.** Pride Developments printed "chase for a final answer, N days silent" on TEN rows, to 265
  days, GBP 1,092,450 - while their PM wrote to commercial@ on 21 and 22/07, Adam priced their new
  enquiry on 29/07 and their frames were fitted on 30/07. Every row was unanswered and the client
  was never silent. A CRM holds one row per job; the relationship is the client's. Also **a
  follow-up date can PRECEDE the lead date** (6 rows; 8701 by 28 days, so a nine-day-old quote read
  as five weeks quiet) - ageing off the earlier of two dates invents the silence outright.
  **And resolve the CONTACT before calling a row cold**: `lyndon@` on a GBP 82,823 row is Lyndon
  Porretta, a DIRECTOR (CH 16138608). The board stores a first name and never asks whose it is.
  **The chase and the apology are different emails - establish which before drafting either**
  (JAC-20). And **a client can RENAME**: Thomas Sinden Ltd became Sinden Construction Ltd on
  22/06/26, CH 03308698, so two CRM spellings are one company either side of a rename, not a
  typo - **the old domain stays live, so search both.** `data/companies/sinden-construction.md`.
  Same family, 29/07 late: **`dormant.json` aged silence off the ORDER date, ignoring `fitted` on
  the same row** - RSR's Bletchley was ordered 15/10/24 and fitted 02/09/25, so eleven months on
  site read as silence (378d -> 330d; every row moved). And **"no work since" is not "nobody has
  spoken since"** - RSR's mailbox runs to 05/05/26. Do NOT join to `intake.json` to fix it: it
  covers 30 days, so absence would read as never-contacted. **Search the mailbox before ringing
  anyone dormant.** `bd-lessons.md`, `data/companies/rsr.md`.
- **A JOB STRADDLES THE MAILBOX WALL AND EACH BOT CALLS ITS OWN HALF THE WHOLE STORY.** RSR/Amazon DRH1:
  client end in estimating@ (dies 10/10/25), supplier end in commercial@ (to 31/10/25, nobody answers a
  glazier's offer of a visit). Both right, answer still wrong - most work here is subcontracted, so it
  sits on BOTH sides. **Ask the other bot before calling a job dead**, and **count who chased whom**: RSR
  chased US twice on a GBP 750 job Amazon had signed off. Cause was a LEAVER - **HARRY GROVER HAS LEFT**
  (Adam, 31/10/25), on four of RSR's five won jobs: any row he owns or promised on is STALE. **`jayk@` is
  a hard 404 - "nothing in jayk@" means nowhere left to look, not nothing was there.**
- **SEARCH THE DOMAIN - THEN DISTRUST A ZERO.** "Instant Glass" = 49 hits and reads like our Crawley
  glazier; `instantglass.co.uk` = 3, one dead thread, never quoted. **But a PORTAL client's domain is on
  our OUTBOUND ONLY** - E T & S's notices arrive "<client> addendum:"/"new message:"/"invites you to quote
  on:", reaching estimating@ only because **PAUL TAYLOR forwards them**: "ets-wales" = 0 read as "no
  traffic" on a GBP 174,546 tender we were told about twice and let lapse. **Search the portal's PHRASING;
  ask who forwards it** - a colleague on it is the login Jayk's 404 hides. **A zero in MY four mailboxes
  is no zero at all** (Chiel: whole job in estimating@).
- **AND THE SHARPER ONE: DO NOT READ A FAN-OUT THROUGH ONE MAILBOX.** I called DRH1's blocker "Instant
  Glass are the only candidate". Harry went to **THREE** glaziers on 05/09; theirs was just the thread that
  stayed in commercial@, **and the only one that failed**. Johnson & Sons priced the bonded corner at **GBP
  960+VAT, 13/10/25** in estimating@ to a spec ADAM set - **so the GBP 750 RSR keep asking us to confirm is
  UNDER COST** (Mary, msg 25). Absence of a price in YOUR half is not absence of a price.
- **"NOTHING IN MY FOUR MAILBOXES" IS NOT EVIDENCE A QUOTE DID NOT GO - SEVEN TIMES OUT OF NINE IT
  HAD.** A quote leaves from whichever mailbox the person HANDLING it uses - `jayk@` (a hard 404),
  `adam@` or `estimating@` - **never** from commercial@, info@ or jacob@, and neither AdminBase nor
  the BD log records a send at all. Mary settled nine such questions on 30/07: **seven had gone and I
  could see none of the seven.** ASK HER; NEVER INFER. The costliest was **Bradstone Road**, which I
  had dead and "lost on price 01/05/2025" on Adam's own chase list - it came back, was priced and
  **issued twice in 2026**, and Adam worked it personally on 12/06. Also: **only PART of what a
  client asked for may have gone** - Chiel got the quote on 22/12 and never the PQQ pack, which is
  what decides whether we are allowed on the tender list at all; **the contact moves** (Grange
  Apartments is Oliver Webber's now, not Ian Brown's; Gleb is `@ajgroup.co.uk`, not
  `@alexanderjamesltd.co.uk`); and **a nil result on a job NAME is weak** where our own files
  misspell the client ("Cheil"/"Swanhurst", both wrong and both consistent) - search a PD number or a
  contact instead - **SEARCH THE PERSON, NOT THE PROJECT: two Pride rows came back nil on the job name
  and were found at once on the contact. Final tally TEN of TWELVE had gone.** Three more shapes from
  the same batch: **a send can be PARTIAL** - 130 Hainault Road excluded four items and offered
  aluminium for uPVC, which beats price as a reason for silence; **the CRM date can be the ENQUIRY,
  not the quote** (26/02 in, priced 01/04, "apologies for taking so long"); and **a job can run
  through a PORTAL with the email as a courtesy copy** - Tiverton went via the "E1 SYSTEM", so email
  silence is not the client failing to answer and any addendum sits where neither bot can see it (the
  E T & S blind spot again). **Do not guess a rebranded address**: ajgroup.co.uk is firstname.SURNAME
  where the old domain used bare firstnames, so `kieran@ajgroup.co.uk` is wrong by construction.
  `mary_recall --kind botchat`, msgs 33-41.
- **THE BOT LINE SILENTLY EATS THE END OF A LONG MESSAGE.** `/api/botchat` does `clip(body, 4000)` and
  returns `{ok:true}` regardless - my 6,918-char RSR reply reached Mary cut mid-sentence and only she
  noticed. **The END is where the point goes.** `bot_chat.py` now REFUSES over 4,000 (`BODY_LIMIT`); the
  hub reply route clips at 8,000 - do not assume one limit.
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
  **AND A LIST FILTERED ON LITERAL STATE STRINGS DELETES ANYTHING YOU IMPROVE** - writing a truer
  state onto Alkerden dropped the most urgent row on the board off the chase list and out of the
  daily email in silence. Whenever a row is researched, re-check it still APPEARS. 30/07.
  **THE SAME TRAP ONE FIELD ACROSS, AND IT HAD ALREADY EATEN MY OWN BEST WORK: THE EMAIL DROPPED
  ANY ROW WITH NO CRM FOLLOW-UP DATE**, and AdminBase leaves that field empty on **80 of 264** rows -
  so research saved nothing, only a date did. It hid Barnfield's MSM Aerospace, where **our client
  has WON the main contract** and a revised price is out, and it had been hiding **Chiel/Swanshurst,
  GBP 52,483 - the previous session's entire finding - since the day I researched it.** A worked row
  is now due, dated today, LABELLED "dated today because this row has been researched" so it borrows
  nobody's credibility. **Twice in two days: improving a row deleted it. Check the row is still on
  the page, not just that the file changed.**
- **ONE CAUSE UNDER ALL OF THE ABOVE: EVERY LIST HERE IS A FILTER, AND A FILTER'S MISSES ARE INVISIBLE
  BY CONSTRUCTION. Ask not "is this list right" but "what CANNOT appear on it".** Five instances, one
  function, GBP 7.9m: a state string; **a MISSING CRM follow-up date - 80 of 264 rows, GBP 7,031,168,
  on nothing**, including the two largest unworked rows here (now due today, labelled "the CRM never
  set a date"; hub-76 keeps a row visible until a PERSON reviews it and an empty field is not a
  review); **sharing a CUSTOMER with a job already on the register - 14 rows, GBP 879,925**, so a
  de-dupe must identify the JOB (same client AND money to within 2p, or two non-generic job words);
  being **a penny apart** where an inc-VAT figure was divided back down - penny-exact stays exact
  for telling a re-quote from a live quote, a different question about the same number; and **the
  MIRROR of the customer de-dupe, which is the sixth instance: the multi-bidder check needs TWO
  customer keys, so one client quoted twice for one SITE is invisible to it** - and it joins on the
  penny-exact figure, which two quotes for one job never share. 6 sites, 13 rows, **up to
  GBP 468,681 counted twice**, worst being Stepnell's ENTIRE GBP 564,403 as three rows at one Derby
  building. NAMED, never merged: aluminium against uPVC at one address reads as a choice, aluminium
  against secondary glazing as two packages, and the `product` column is the tell a human settles it
  on. **When a bug is a habit of thought, fix every instance in the function, not the one you
  tripped over - and look for its mirror.**
- **RESEARCH THAT DOES NOT LAND ON THE ROW CHANGES NOTHING - A COMPANY FILE IS NOT A BOARD.** I filed
  Adam's answer that Churchdown and Aylesbury were **unfunded CIF bids**, and next morning his chase
  list still led with **Mobius GBP 746,617 and Southern Projects GBP 729,117, "chase for a final
  answer"**. **Churchdown went to FIVE bidders** at two price points GBP 17,500 apart, so one funding
  decision kills five leads sharing only a site postcode; six `worked` overrides now name them
  blocked, and the ask is late September, to be the number INSIDE the resubmission.
- **A PROMISE WE MADE IS A CHASE DATE THE BOARD CAN COMPUTE, AND IT IS THE BEST ONE ON HERE.**
  Alexander James - **six rows, GBP 1,910,810 ex VAT, the largest single-client exposure here**, two
  spellings, three contacts, no file, no chase - and two were answered in commercial@ all along:
  Brooklands **LOST 07/05** (our client lost the main contract, not our price) and Tiverton Road GBP
  547,886, **"preferred bidder... come back to me in 6-8 weeks"** = 17/07-31/07, expiring while the
  row sat undated and invisible. Leys Park had a client's public deadline setting the date; this is
  that rule inwards. Both replies went to **PAUL TAYLOR** - "you were previously speaking with my
  colleague Jayk" - same-day answer twice: **Jayk's book is being worked quietly by a PM nobody
  counted, so search commercial@ for a COLLEAGUE'S name before calling a client silent.**
- **READ YOUR OWN OUTPUT BEFORE PRODUCING IT AGAIN, AND CORRECT THE OTHER BOT RATHER THAN REPLACE
  HER.** `drafts.json` D-6 was already the A Plus reply Adam asked me for, off Mary's reading of
  estimating@; my append script filtered on the id it was about to use and **deleted hers** (no unique
  constraint in a hand-appended list; `git checkout HEAD --` restored it). What it needed was the one
  thing only my mailbox holds - an address flagged "not verified by me, Dan's mail is in a mailbox I
  cannot read" when Adam had forwarded that mail into jacob@. **The unverified field in the other
  bot's work is where your mailbox is worth most.** Same client: I had Darrick Wood as "65 days
  silent" when **Gleb Saliev rejected our quantities on 09/07 and the revision may still be inside
  Fenster** - fourth such job this month. Portals again (EstimateOne, AJ Group's own).
- **A BULK IMPORT IS ONE FACT, NOT 59 - BUT COUNTING IT IS NOT MINE TO DECIDE.** Folding the untouched
  CRM tail off Today was right on 28/07 (59 identical rows pushed the four real quotes off the screen)
  and was OVERRULED on 29/07 by the man who owns the backlog. **Label, never hide.** See the standing
  decisions below and `bd-lessons.md`.


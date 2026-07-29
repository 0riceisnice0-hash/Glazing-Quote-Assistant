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

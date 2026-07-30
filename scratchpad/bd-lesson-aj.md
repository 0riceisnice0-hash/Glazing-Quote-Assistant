
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

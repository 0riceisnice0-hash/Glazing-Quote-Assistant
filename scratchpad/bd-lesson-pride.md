
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

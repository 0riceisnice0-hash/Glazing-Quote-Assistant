
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

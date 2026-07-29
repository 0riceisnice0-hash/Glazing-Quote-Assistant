
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


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

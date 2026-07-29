# Jacob's data

Everything here is **generated**. Nothing is hand-edited, and deleting any of it costs
only the time to regenerate. `JACOB-SESSION.md` section 5 is the short version; this is
where each file comes from and what it can and cannot tell you.

| File | Written by | Holds |
|---|---|---|
| `intake.json` | `jacob_intake.py` | Every message in his mailboxes, classified, with the opening lines of each |
| `contracts-finder-awards.json` | `jacob_contracts_finder.py` | Public **award** notices - contracts already let |
| `tender-notices.json` | `jacob_tenders.py` | Public **tender** notices - still out to bid, with real closing dates |
| `procontract.json` | `jacob_procontract.py` | ProContract (Due North) adverts. Where a buyer puts work **under the GBP 100k Find a Tender threshold** - so it is in no national feed, and it is Fenster's size of work. Read with **no login**; only bidding needs the account Fenster has not had since Jayk left (JAC-11) |
| `leads-manual.json` | his session, by hand | Live leads that arrived as EMAIL and are in no public feed. Merged onto the tender board. Every row carries where it came from, who read it, and which feeds were swept without finding it |
| `planning.json` | `jacob_planit.py` | **Planning applications - the free half of what Barbour ABI sells.** Every GB council's register via PlanIt, no key, filtered to schemes with a glazing package in them. 454 live large applications in 30 days against 17 tender notices in 90. The only source that reaches a scheme BEFORE an enquiry list exists. `applicant` is read from the council's own portal, because PlanIt redacts it to "See source" - that redaction is Barbour's product |
| `planit-raw.json` | `jacob_planit.py` | The unfiltered pull, cached so the filter can be re-tuned with `--from-cache` without hitting a free public API again. Delete it freely |
| `planit-areas.json` | `jacob_planit.py` | council -> country, when the areas API can be read at all. Usually it cannot: it pages at ten rows, refuses `pg_sz` and rate-limits hard, so the coverage rule is written down in the script instead. **A cache with under 300 councils in it is IGNORED** - a partial map silently drops every council it has not heard of |
| `dormant.json` | `jacob_dormant.py` | **Customers who bought, stopped, and nobody noticed.** Won contracts joined to the live pipeline: past buyer, no quote out, no work on site, silent. This is the 59% of wins that came from an existing customer, against the 3 that ever came from a tender portal. Do-not-approach names are excluded in code, not by the reader |
| `contracts-won.json` | `jacob_contracts.py` | **The 204 WON commercial contracts**, net value on every row - Adam's hand export of 29/07/2026. The only file here built from delivered work rather than hope. Settles the GBP 50k question (8 wins over it, largest GBP 631,248) and carries `LEADSOURCE`, which says 59% of wins are repeat business and 25% were Jayk personally |
| `outcomes.json` | `jacob_outcomes.py` | The Opportunity Log - the 2025-26 BD FUNNEL with its decided rows. Not the win history; `contracts-won.json` is |
| `adminbase.json` | `jacob_adminbase.py` | Adam's AdminBase export - quoted leads with dates and values |
| `jayk-recovery.json` | `jacob_jayk_recovery.py` | The former BDM's contacts, recovered from role mailboxes. One-off |
| `drafts.json` | his session | Outreach he has written, and what he deliberately did **not** draft |
| `handover.json` | his session | What he has passed to a human, held, or corrected |
| `daily-email.json` | `jacob_daily_email.py` | The one email Adam authorised - today's chase list in his hub-76 format: **Due or Overdue Today**, then **Coming Up Tomorrow**. Nothing is held back any more (hub-76), so every row carries `dateSource` saying whether a person or the CRM set its date. `blockedNotChased` holds the rows a client physically cannot answer yet - named, never hidden. **`sent` is false and will stay false until JAC-15 is answered**, and Adam ordering the override on hub-76 did not change that: see the module docstring |
| `email-settings.json` | hand-edited by a human | Was Adam's choice of what happens on a day with nothing due. hub-76 settled it - the email always goes - so nothing here is configurable now; it is kept as the record of what the setting used to be |
| `bridge-state.json` | `jacob_bridge.py` | Which work orders he has seen, and session-time used |
| `session-log.md` | his session, by hand | One line per session - the order, and what actually changed. Mary's `HANDOVER.md` has no Jacob entries in it; this is that record for this side of the wall |

## Things that were wrong once, and how the files now stop it

**A count is not a coverage.** `intake.json` records `oldest`, `newest` and a `truncated`
flag per mailbox. This exists because a 20-page cap once made a 13-day window read as a
180-day one, and every number downstream was a fortnight presented as six months. If a
count looks surprising, check the window before you believe it.

**A record and a board are different things.** `intake.json` keeps every signal; the board
picks a window and says how many it is holding back. An array slice used to decide which
one you were looking at, silently dropping 719 of 919.

**Money has two forms.** AdminBase values are **inclusive of VAT**; every quote Fenster
issues is **exclusive**. `adminbase.json` carries both and the board shows ex-VAT.
Comparing an AdminBase figure to the Opportunity Log without checking is a 20% error.

**A CRM date is not a send date.** On a re-quote AdminBase updates the VALUE and leaves the
lead date, the next-action date and the lead number exactly as they were. Lead 8155 read
"chase due, 98 days" on a price sent the previous afternoon, and a draft was written on the
strength of it saying we had quoted the same figure twice - we had not. Rows whose value
joins penny-exact to a verified send that is newer now carry `staleDate` and are aged from
the send. `reQuote` on that object says whether the gap is a re-quote or ordinary lag.

**Big is not wrong.** `outlier` keeps a huge row out of the medians. It used to keep it off
the chase list too, which quietly turned an arithmetic decision into a judgement about
whether the job was real. `confirmed` now carries who confirmed it and when - Brandon
Estate, Adam, 29/07 - and a confirmed row is chaseable while still being out of the
averages.

**Outcome data exists.** It was believed for a while that Fenster records no outcomes,
because the Estimating Log's W/L column is 93% empty. The BD log is a different file and
has 229 decided rows. `outcomes.json` is the one to trust.

**A REDACTED FIELD IS NOT A MISSING FACT.** PlanIt returns `applicant_name` as the literal string
"See source" on every row of its free API, which reads exactly like "nobody knows who is building
this". Somebody does: the council's own planning register carries the applicant because the law
says it must, and PlanIt links straight to it. The redaction is the thing Barbour ABI charges for,
not a limit on what is knowable. Same lesson as the dead login below - **check what a block
actually blocks.**

**A feed that returns nothing looks exactly like a quiet market.** `planning.json` dropped all 454
applications as "outside England and Wales" on its first run, because PlanIt's `parent_name` is not
a country - it is one step up a tree of arbitrary depth (Adur -> Adur and Worthing -> West Sussex ->
South East -> England). The board would have reported an empty planning pipeline in perfect good
faith. Any filter that removes everything is a bug until proven otherwise, and `counts.dropped`
exists so the reason is on the face of the file.

**A dead login is not a dark source.** `procontract.json` exists because "the tender-portal
logins stopped working when Jayk left" was allowed to mean "we cannot see what is on those
portals". Only one of those is true. ProContract's advert search and every advert page are
public - no account, no cookie, no key - and the first run found three live window-and-door
jobs, one closing in two days. The login controls whether Fenster can BID. It never
controlled whether Fenster could LOOK, and for four months nobody did. Before writing off
any source as blocked, check what it actually blocks.

**"Issued" is a fact about the send, not about the document.** `handover.json` rows now
carry `openOnTheIssuedDocument` - what is still wrong with the pack the client is actually
holding, read from the attachments on the sent message rather than from the correction email
that preceded it. Grange Hill, 29/07: six corrections went to Adam at 14:40, the quote left
at 16:07 with the total unchanged, and the marked-up drawings sent to the client run to
thirteen windows against twelve priced. A register that records only "quoted, chase in a
fortnight" cannot tell the person who chases it what the client can argue about. Rows also
carry `expires` where our validity and the supplier quotes behind it die on a date of their
own - Grange Hill's is 28/08 and it belongs to nobody outside Fenster, so nothing else on
the board would ever raise it.

**A bulk import is one record, not two hundred.** Adam's completeness rule (hub-74) says any
row missing a next action, an owner or a deadline appears on Today. Applied literally that put
64 rows there and 59 of them were the single AdminBase export of 28/07 that nobody has ever
opened - one fact printed 59 times, and it pushed the four quotes genuinely due that day off
the first screen. Same for the 134 rows whose follow-up date has passed: the CRM set those
dates, not a person. So a row somebody has WORKED - a date they set, a note they wrote, an
owner or state they chose - is listed; the untouched tail is counted, folded and said out
loud, on Today and in the daily email both. Touch one and it moves up into the list.

**Two rows can be one job.** `leads-manual.json` rows now carry `supersededBy`. The Ryde
lead arrived as a paid Supply2Gov alert with the buying organisation stripped out and no
value; the same job on ProContract named Isle of Wight Council, a contact, a phone number
and a GBP 75k-125k budget. The manual row keeps the history of how the lead first reached
Fenster, and the board shows the better row only.

**`Estimated value` on a ProContract advert is nearly always N/A.** The budget, when there
is one, is a sentence in the description - `budgetFromText` parses it, and the pound sign
frequently arrives mojibaked, which is why the regex accepts U+FFFD. Do not tidy that away.

## Regenerating

```bash
python scripts/jacob_daily.py            # intake + awards + procontract + rebuild
python scripts/jacob_planit.py           # planning applications (slow - PlanIt rate-limits)
python scripts/jacob_planit.py --from-cache --no-enrich   # re-filter without re-fetching
python scripts/jacob_dormant.py          # past customers who have gone quiet (local, instant)
python scripts/jacob_intake.py --days 180
python scripts/jacob_outcomes.py
python scripts/jacob_adminbase.py
python scripts/jacob_tenders.py
python scripts/jacob_procontract.py
python scripts/jacob_contracts.py
```

`jayk-recovery.json` is deliberately not in the daily run. It was a one-off excavation of a
mailbox that no longer exists; re-running it reads live mailboxes for no new information.

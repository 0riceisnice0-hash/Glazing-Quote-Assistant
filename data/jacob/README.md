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
| `outcomes.json` | `jacob_outcomes.py` | The Opportunity Log - what Fenster has actually won and lost |
| `adminbase.json` | `jacob_adminbase.py` | Adam's AdminBase export - quoted leads with dates and values |
| `jayk-recovery.json` | `jacob_jayk_recovery.py` | The former BDM's contacts, recovered from role mailboxes. One-off |
| `drafts.json` | his session | Outreach he has written, and what he deliberately did **not** draft |
| `handover.json` | his session | What he has passed to a human, held, or corrected |
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

**A dead login is not a dark source.** `procontract.json` exists because "the tender-portal
logins stopped working when Jayk left" was allowed to mean "we cannot see what is on those
portals". Only one of those is true. ProContract's advert search and every advert page are
public - no account, no cookie, no key - and the first run found three live window-and-door
jobs, one closing in two days. The login controls whether Fenster can BID. It never
controlled whether Fenster could LOOK, and for four months nobody did. Before writing off
any source as blocked, check what it actually blocks.

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
python scripts/jacob_intake.py --days 180
python scripts/jacob_outcomes.py
python scripts/jacob_adminbase.py
python scripts/jacob_tenders.py
python scripts/jacob_procontract.py
```

`jayk-recovery.json` is deliberately not in the daily run. It was a one-off excavation of a
mailbox that no longer exists; re-running it reads live mailboxes for no new information.

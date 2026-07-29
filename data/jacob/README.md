# Jacob's data

Everything here is **generated**. Nothing is hand-edited, and deleting any of it costs
only the time to regenerate. `JACOB-SESSION.md` section 5 is the short version; this is
where each file comes from and what it can and cannot tell you.

| File | Written by | Holds |
|---|---|---|
| `intake.json` | `jacob_intake.py` | Every message in his mailboxes, classified, with the opening lines of each |
| `contracts-finder-awards.json` | `jacob_contracts_finder.py` | Public **award** notices - contracts already let |
| `tender-notices.json` | `jacob_tenders.py` | Public **tender** notices - still out to bid, with real closing dates |
| `outcomes.json` | `jacob_outcomes.py` | The Opportunity Log - what Fenster has actually won and lost |
| `adminbase.json` | `jacob_adminbase.py` | Adam's AdminBase export - quoted leads with dates and values |
| `jayk-recovery.json` | `jacob_jayk_recovery.py` | The former BDM's contacts, recovered from role mailboxes. One-off |
| `drafts.json` | his session | Outreach he has written, and what he deliberately did **not** draft |
| `handover.json` | his session | What he has passed to a human, held, or corrected |
| `bridge-state.json` | `jacob_bridge.py` | Which work orders he has seen, and session-time used |

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

**Outcome data exists.** It was believed for a while that Fenster records no outcomes,
because the Estimating Log's W/L column is 93% empty. The BD log is a different file and
has 229 decided rows. `outcomes.json` is the one to trust.

## Regenerating

```bash
python scripts/jacob_daily.py            # intake + awards + rebuild the board
python scripts/jacob_intake.py --days 180
python scripts/jacob_outcomes.py
python scripts/jacob_adminbase.py
python scripts/jacob_tenders.py
```

`jayk-recovery.json` is deliberately not in the daily run. It was a one-off excavation of a
mailbox that no longer exists; re-running it reads live mailboxes for no new information.

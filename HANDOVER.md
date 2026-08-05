# GLASSHOUSE — where things stand

Last updated **05/08/2026, 13:05**. Read `README.md` for the layout and
`personas/SYSTEM.md` for the architecture on one page. This file is the state
of play: what is running, what is unfinished, and what will bite you.

---

## Running right now

The engine is **up and working** (`core/glasshouse.py`, one process). Bots work
**08:00–18:00**; outside that only a dashboard message or an email from Adam is
picked up.

```bash
python core/preflight.py          # is it safe to start?
python core/glasshouse.py         # the engine
bash scripts/restart_engine.sh    # pause, drain, swap - NEVER kill it directly
```

**Hub:** https://glasshouse-79z.pages.dev — sign in with your name; Adam, Paul
and Steve each have a one-time setup code (ask Zac).

### Today's numbers, 05/08 at 13:10
89 sessions, 1,232 calls, **100.5M context / 31.2M weighted** — 67% of the 150M
day breaker, with five working hours to go. Read that gap: *context* is what
the models saw, *weighted* prices cache reads at a tenth and Opus at five times
Sonnet, so weighted is the number that tracks the bill. `core/budget.py` reads
the transcripts directly and dedupes by request id, because the completed-
session log misses running sessions, killed sessions and intake entirely — it
was under-reporting by 38%.

**A large share of that is not the bots.** A dev session (this kind of chat)
cost 23M weighted against the three desks' 3.5M on 04/08. If a day looks
expensive, check who spent it before throttling anyone.

---

## What exists that did not yesterday

| Thing | Where |
|---|---|
| Mailbox **search** for all three desks | `core/mail.py --search "..."` |
| Rate **benchmarks** + pricing **scoreboard** | `core/rates.py --lookup / --score` |
| **Standing work** when a desk is idle (09:00/13:00/16:00) | `core/agenda.py` |
| **Projects** — an hour of directed work from a hub button | `core/agenda.py` PROJECTS |
| **Live** page: a session's thinking and tool calls, streamed | `core/trace.py` |
| Needs split by **who holds the answer** | `decision.source` = fenster \| supplier |
| Contract **12-step template** | `core/contract_template.py` |

**Drafts were removed** on 05/08. The bots write no outbound of any kind, not
even for a human to send. When they need something they raise a NEED that says
whether Fenster or a supplier holds the answer.

---

## The pricing engine — the live piece of work

`scripts/mary_backtest.py --loo` is the measurement. Today:

```
before the parser fix : 12.39% mean abs, 30 documents in 27 jobs
after                 : 19.41% mean abs, 67 documents in 36 jobs
```

**The engine did not get worse — the measurement got honest.** 12.39% was
scored only on the documents the parser could read, which were the internal
copies most like what the engine was built from. `parse_doc` now falls back to
a header-driven read for CLIENT-FACING copies (no product code column, columns
wherever that document put them), so it is scored on more than double the
evidence including a population it had never seen.

**Do not let a client-facing line reach rate mining.** Those copies show the
SELL price with no Frames breakdown; mining one teaches the engine that
Fenster's own margin is a supplier cost. They carry `frames=None` on purpose
and `supply_money()` refuses them. If you touch `parse_doc`, re-check that.

Still unread: 5 quotes that are secondary-glazing-only (no code path) or have
no sizes at all. That is correct behaviour, not a bug.

---

## Open, and worth doing next

1. **38 needs are waiting on a human** (29 ours, 9 supplier). Three are reissue
   decisions on quotes already with clients — including a **GBP 10,000
   shortfall on Brocks Hill**. That queue grows faster than it is answered.
2. **Site dates: 3 of 10 contracts.** Every delivery deadline hangs off one, so
   Paul and Steve's board is still mostly undated. Joseph is working it.
3. **Step lead times are unknown** — how many days before installation frames
   and glass must be ordered. Nobody has recorded them; `LEAD_TIMES` in
   `core/contract_template.py` is deliberately empty rather than guessed. One
   answer from Adam or Paul dates every step on every contract.
4. **A project cannot declare itself finished.** It runs its clock out. The
   cooldown (20 min) stops the worst of the churn; letting a bot say "this is
   done" would be better.
5. **Jacob has no real win history.** The AdminBase export Adam sent contains
   264 rows and **not one marked won** — it is the leads board. Any win rate
   from it, or from the Opportunity Log, is derived from a dataset that
   structurally cannot contain a win. A different export is needed.

### Still unanswered from Adam's meeting

Not blockers, but each one leaves a hole somebody is filling by guessing:

- **Lead times** — see 3 above. The single most valuable answer on this list.
- **Where the invoice figure comes from**: the quote, the PO, or the measured
  final account.
- **Chase ladder stages 3, 4 and 5.** Stages 1 and 2 are known (7 and 35 days,
  with 75 for the last), the middle is not.
- **Who acknowledges an order to the customer** — no bot may, so it is a person,
  and nobody has said which.

---

## Things that will bite you

**Committed is not running.** The engine imports its modules once. Editing a
charter, a brief or `agenda.py` changes nothing until `scripts/restart_engine.sh`
completes. This cost three separate incidents on 05/08, including Jacob running
for 40 minutes on a brief that had already been corrected.

**Never edit a file while a restart is in flight.** A half-written `dispatch.py`
was loaded and every session died instantly with a `NameError`. The same class
of thing corrupted a running bash script mid-execution.

**One restart at a time.** Two ran concurrently and each started an engine, so
two dispatchers claimed the same work and both spent. `restart_engine.sh` now
takes an atomic lock and kills stragglers, but check
`Get-CimInstance ... glasshouse.py` returns **1** if anything looks odd.

**`_` is a wildcard in SQL `LIKE`.** `DELETE ... WHERE body LIKE '%__t%'`
matched almost everything and destroyed 555 event rows on 05/08. The ledger was
not restored (Zac: "i dont care about activity so its fine"), so Activity and
job histories start from 05/08 13:00. **Match exact keys when cleaning up.**

**D1 has Time Travel** if you do need a restore:
`npx wrangler d1 time-travel info glasshouse-db --timestamp=...`

**Cloudflare edge lag.** After a Pages deploy the alias serves old and new
bundles for a minute or two; a route can 404 on one request and work on the
next. Wait rather than debugging a phantom.

**Two clocks kill a session**: 70 tool calls AND the wall clock (45 min, 80 for
projects). A session killed before `finish` loses everything it did — that has
happened twice, at a cost of 2.7M and 6.8M tokens.

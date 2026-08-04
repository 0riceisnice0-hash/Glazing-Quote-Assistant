# Where we stopped — 04/08/2026, ~17:00

Engine **stopped**. Nothing is running. 24 tasks sit queued in the record and
they are durable — starting the engine picks them up exactly where they were.

## What happened, plainly

Mary's first real session **failed**, and the failure was mine, not hers.

She hit the `--max-turns 30` cap at 411 seconds having spent **2.69M context
tokens**. The cap kills the session outright, so she never reached `finish` —
and because finish is the only thing that writes to the record, **every fact
she worked out was lost**. She had already found the right problem (her own
output read `TOTAL OPEN 31 / NO DEADLINE 31`) and none of it was saved.

Then the worse part: on failure her tasks were released back to the queue and
she was re-dispatched with the same work seconds later. Left alone that repeats
the 2.7M burn until the daily breaker trips. I caught it at **2.83M total**,
which is 2% of the daily target — cheap, but only because it was watched.

## Fixed before stopping (committed and deployed)

1. **No infinite retry.** A task that kills its session twice is parked, not
   retried, and a decision is raised asking a human why. Each retry costs a
   whole session.
2. **The budget is told to the bot.** The prompt now states the call limit and
   says: do a slice that fits, close out with calls to spare, leave the rest
   for a fresh task. Stopping early with work saved beats being cut off.
3. **70 calls, not 30.** The onboarding brief I wrote was simply bigger than
   the budget I gave it.

## What is NOT proven, and should be treated as suspect tomorrow

- **No bot has yet completed a session on the new engine.** Not one `finish`
  call has run for real. That is the single thing to prove first.
- The trace/Live stream worked against a running session, but has never run
  through a full start-to-finish cycle under the engine itself.
- The intake/dispatch thread split is deployed but has only run for minutes.

## Start of play tomorrow

```bash
python core/preflight.py
```

```bash
python core/glasshouse.py
```

Then watch the **Live** page. The first thing to look for is a session reaching
`finish` — not what it wrote, just that it closed out at all. If a session
fails again, stop and read `test-results/glasshouse/last-<persona>.txt` before
restarting anything.

**Consider shrinking the briefs.** Tasks 13/14/15 ask each bot to read the new
system AND correct a large slice of the record in one sitting. Splitting
"learn the system" from "fix the deadlines" would probably have avoided this.

## Still open from the meeting transcript

- **Lead times** — days before the site date each of the twelve steps must
  happen. Nothing in the delivery board can sort or warn without them.
- **Site dates** on the four live contracts.
- Where the invoice figure comes from (quote / PO / measured final account).
- Chase ladder stages 3–5 day counts (7, 35 and 75 are known).
- Who sends the acknowledgement to the customer.

## Accounts

Setup codes, first use only — the person picks their own password:
`adam` 416162 · `paul` 786161 · `steve` 405367. Zac's password is already set.
Steve has already ticked two steps on Manor Lodge, so the job sheet works.

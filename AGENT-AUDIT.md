# AGENT AUDIT - Mary and Jacob as minds, and the plan to rebuild them

Zac's instruction, 29/07/2026: *"they are not the best they can be yet, given the logic
with memory, the chats etc. there are a lot of hard limits in place to limit her when it
should just be what mary knows to do. mary needs expert knowledge, to change the dashboard
herself, to know when or not to send emails, not spam, see everything she's ever done
across all jobs, remember all of Adam's replies, while not burning through our tokens."*

This is the audit of how the two bots think today, measured against the repo and the live
data on 29/07, and the architecture proposed to replace it. The hub restructure
(`HUB-AUDIT.md`) was the shell; this is the mind.

---

## 1. The audit - what the evidence says

### 1a. Memory is transcripts, and transcripts are the token fire

- **144 Claude sessions, 179 MB of transcript.** The three biggest single chats are
  28 MB, 26 MB and 18 MB. "The conversation is the job's memory" worked at day one; at
  week one it means every resumed turn drags a novel behind it, and the 95-session night
  (BOTS.md §3) was this exact failure billed by the hour.
- **The durable job files have become transcripts too.** `data/jobs/gordon-court.md` is
  265 KB; triage's is 70 KB; St Mary's 54 KB. They were designed as the *distilled*
  backup ("what a new chat starts from") and nothing enforces distillation, so they grew
  by appending. One chat (Riverside) invented archiving on its own - 221 KB pushed to
  `riverside-archive-2026-07.md`, 10 KB kept live. That instinct is correct and is
  currently a personal habit of one chat, not a rule of the system.
- **Knowledge is append-only prose.** `HANDOVER.md` 7,373 lines, `AI.md` 2,924,
  unindexed. The email-session boot instruction is literally "Read MARY-HANDOVER.md,
  then HANDOVER.md, then AI.md" - ~10,000 lines before the first work order.
- **Cross-job sight is a 12-line window.** Chats see the noticeboard tail and nothing
  else of each other. "Everything she has ever done" exists - scattered across
  transcripts she cannot search, sent items she does not re-read, and git history.

### 1b. Adam's replies are the best training data we have, and they evaporate

The last 90 hub messages: 46 Mary, 32 Adam, 12 Zac. Adam's 32 contain, verbatim:

- **"Mary, this word count is insane. I will not be reading this."** - three times, on
  three different requests, in one evening.
- **"I have already addressed this with you."** - a re-raised settled decision. This is
  a *memory* failure wearing a manners costume: she has no queryable record of what has
  been settled, so settled things resurface.
- **"Please email me this" / "Send me an email with the bullet points."** - he *asks*
  for emails. The problem was never email; it is unsolicited essays. His request
  pattern is itself the spec for when email is right.
- **"If you look at the large tender we did for Brandon Estate..."** - he teaches by
  precedent. Those teachings currently land in one chat's transcript and are invisible
  to every other chat forever.

The email numbers behind the spam worry: **39 sends in the last day and a half** (21 on
the 28th, 18 by 11:30 on the 29th); the email playbook itself records **33 sent / 4
replied in 42 hours**. And 15 requests sat open carrying 29,004 characters between them.

### 1c. The hard limits are compensation, not policy

Inventory: day window 8h/40 sessions, night 1.5h/6; circling cap (5 runs/6h per chat);
request-backlog cap (12); botchat 10/hour; recipients locked to adam/marketing; morning
update at 07:45; "EARN THE INTERRUPTION" essay in the email doc. Each exists because a
judgment failed *and the bot had no ground truth to judge with*:

| Limit | The missing faculty it papers over |
|---|---|
| Session/hour caps | No token accounting; cost invisible to her, so it is rationed for her |
| Circling cap | Chats loop because they cannot see they are looping |
| Email guidance essays | She cannot see her own send history or Adam's response rate |
| Request backlog cap | She cannot see the backlog cost or what got answered |
| "Do not re-read handover docs" | Boot cost is prose because knowledge has no index |

**Not everything here is compensation.** The transport rule, mailbox scoping, the
injection guard, ghost protocol, the botchat 429 and the hub deploy guard are *safety
walls* and stay walls forever. The plan removes judgment-rules only, one at a time, when
the faculty that replaces each is measurably working.

### 1d. What is already right (build on, not over)

The pricing engine with provenance and earned calibrations; `mary_checks.py` where every
rule is a real past mistake and new mistakes become new rules; the calibration log with
its honest n=5, +10% bias, band-shaped error finding; per-job routing; the request model;
the hub she can already rebuild herself (`MARY-HUB-DEV.md`). These are the bones of "an
agent that improves itself." The gap is that *facts and judgment* have no equivalent of
the engine - nothing accumulates them structurally.

---

## 2. The architecture - three memories with different jobs

The root defect is one memory doing three jobs. Split it:

```
LEDGER      what happened          append-only, queryable, deterministic, free
DISTILLATES what it means          small, curated, always loaded
TRANSCRIPT  what I am doing now    working memory only, rotated without ceremony
```

### 2a. The ledger (everything she has ever done, queryable)

One event store - `data/ledger/` (jsonl per month, plus an index) written by the tools
she already uses, not by her discipline: `mary_send.py` logs sends (exists), the bridge
logs work orders, `mary_dashboard_reply.py` logs answers, a close-out hook logs
decisions/prices/RFIs. Every event: timestamp, job, kind, one-line summary, source ref.

`scripts/mary_recall.py --job georgies --kind sent --days 7` /
`--topic "panic bars"` / `--settled` - a **deterministic query, zero session tokens**,
callable by any chat, any bot, and the hub. "What did I already tell Adam about this?"
and "has this been decided?" become lookups, not hopes.

**One-off backfill** from what already exists: the send log, D1 hub messages (Adam's 32
replies included), estimating@ sent items via Graph, `HANDOVER.md` mined per job, git
history of `dashboard-state.json` (requests raised/answered, catches).

### 2b. The distillates (what she knows, small enough to always load)

- **`data/knowledge/adam.md` - the Adam model.** Mined once from every reply he has ever
  sent (hub + email), then appended at close-out whenever he teaches something. Three
  sections: *how he reads* (bullets, one screen, headline first - his own words), *what
  is settled* (decision, date, source - the "already addressed" list), *how he decides*
  (precedents he cites, risk posture). This file is why she stops re-asking and stops
  writing essays: it is loaded in every session, and it is the corpus Zac pointed at.
- **`data/knowledge/estimating/*.md` - the expert shelf.** The durable lessons currently
  buried in `AI.md`/`HANDOVER.md` prose, distilled into short indexed entries by topic
  (suppliers, systems, spec traps, procurement). One index file loaded at boot; entries
  pulled on demand. Boot drops from ~10,000 lines to an index plus the job at hand.
- **`data/jobs/<key>.md` - the position, contract-enforced.** Hard cap (300 lines),
  fixed sections (position; the number and its basis; deadlines; open RFIs; decisions
  with dates; what Adam said), overflow auto-archived exactly as Riverside already does
  by instinct. The bridge *refuses close-out* if the file is over cap or stale - a wall
  whose purpose is to build memory, the good kind of wall.

### 2c. The transcript (working memory, rotated)

The bridge measures each chat's transcript; over threshold (say 2 MB) the next dispatch
starts a **fresh session seeded from the job file + last ledger events + open items** -
already named as "next candidate 1b" in DEV-HANDOVER, now with 28 MB of evidence behind
it. The chat stops being sacred; the job file is sacred, which is why 2b enforces it.
Expected effect is the single biggest token saving available: resumed context becomes
tens of KB instead of tens of MB, with *better* recall because the seed is curated.

---

## 3. Judgment replacing limits (in this order, each gated on a metric)

1. **Send gate with evidence, not a quota.** `mary_send.py --check` (dry-run) returns:
   sends today, last send on this job, whether the topic appears in `--settled`, Adam's
   historical response to this kind of send, and whether the 07:45 digest is nearer than
   the urgency justifies. She decides; the evidence is in front of her. **Metric:
   interruption yield** = Adam replies+actions / sends. Today it is ~4/33. When it holds
   above ~1/2 for two weeks, delete the email essays and keep one line: *"Does Adam do
   something different because you told him?"*
2. **Re-raise guard.** Raising a request or emailing a decision requires a `--settled`
   check first (the tool does it, not her memory). **Metric: zero "already addressed"
   replies from Adam.** This also fixes request pile-up: a request that duplicates a
   settled decision cannot be filed.
3. **Token-true budgets.** The budget counts sessions and hours because tokens were
   invisible. The bridge can read transcript growth per turn - account in tokens,
   surface it to her ("this turn cost X; the seed is Y"), and turn the window caps into
   circuit breakers at ~2x expected spend rather than daily governors. **Metric: cost
   per work order trending down while catches/quality hold.**
4. **Self-building stays, gets a lane.** She can already rebuild the hub behind the
   guard; add a "hub" work-order type so "the board misrepresents my job" is a thing she
   fixes in the turn she notices it. Policy self-editing is different: the librarian
   (below) may *propose* rule changes as diffs; Zac approves. Code yes, constitution by
   review.

**The librarian.** One budgeted off-peak run (not a per-job chat): compact the day's
ledger into distillates, enforce job-file caps, update `adam.md`, refresh calibration
notes, and emit a one-screen "what changed in what Mary knows" note to the hub. This is
the metabolism that keeps memory small, and its budget is fixed and boring.

---

## 4. Jacob, same skeleton, smaller

Jacob's equivalent audit is one line: **he has no memory at all** (BOTS.md says it -
every session cold). Apply the identical shape: `data/companies/<key>.md` with the same
contract (his unit of memory is the company, not the job), the shared ledger with his
own events, `data/knowledge/bd.md` for what he learns about how Fenster wins work, and
per-company session seeds when a relationship goes live. His JAC-5 (cannot see replies)
is really a ledger feed gap - sent-items access populates the ledger and three of his
five open questions shrink. His no-send wall stays until the approval queue exists;
nothing in this plan changes that.

---

## 5. Sequence

| Phase | Builds | Done when |
|---|---|---|
| 0 | Backfill ledger from send log, D1, sent items, HANDOVER; token baseline per chat | `mary_recall.py` answers "what did I tell Adam about X" for any live job |
| 1 | Job-file contract + rotation in the bridge | No transcript over threshold; every close-out updates file + ledger; a reset chat picks up a live job without loss |
| 2 | `adam.md` mined + send gate + re-raise guard | Interruption yield > 1/2 for 14 days; zero "already addressed" |
| 3 | Knowledge distillation + librarian | Boot context ≤ index + job file; essays deleted from playbooks |
| 4 | Token-true budgets; caps → circuit breakers | Cost per work order down, catches steady |
| 5 | Jacob parity (companies, bd.md, ledger feeds) | His Today actions cite his own history unprompted |

Each phase is independently shippable and independently reversible, and nothing touches
the safety walls. Phase 0 and 1 are where the token burn stops; phase 2 is where the
spam stops; phase 3 is where "expert knowledge" stops meaning "7,000 lines she is told
not to read".

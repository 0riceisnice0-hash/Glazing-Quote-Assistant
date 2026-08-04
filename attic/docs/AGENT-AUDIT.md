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

### 1d. The attachment question (Zac, 29/07: "she can't see email attachments")

Checked empirically against the live mailbox rather than the code's word:

- **Ordinary file attachments DO reach her.** All 54 work-order attachment folders on
  disk contain their files, and the exact endpoint the poller calls returns inline
  bytes even for the 13.7 MB Redditch tender pack and a 29.9 MB Vesuvius zip.
- **Three things were invisible, silently:** attached emails (`itemAttachment`),
  OneDrive/SharePoint links (`referenceAttachment`), and any file whose bytes Graph
  chose not to inline. The downloader dropped them with no trace, so a skipped pack
  looked identical to a mail with none. **Fixed 29/07:** every skip is now written to
  `_NOT-FETCHED.txt` in the attachment folder, so the session knows something existed
  and can chase it or say so. (Takes effect on the bridge's next restart.)
- **Jacob genuinely cannot see attachments.** His daily intake is deliberately
  metadata-only (sender + subject, no session spent); only ad-hoc `jacob_mail.py` opens
  content. That is a design choice, not a bug - but it belongs in his ledger-feed plan
  (§4), because "a buyer sent drawings" is exactly the signal his board wants.
- **Humans on the hub cannot see what she read.** The Comms log shows "2 attachment(s)"
  as text with no way to open them. Worth a hub work order if it matters.

### 1e. What is already right (build on, not over)

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
| 0 **DONE 29/07** | Backfill ledger from send log, D1, sent items, HANDOVER; token baseline per chat | `mary_recall.py` answers "what did I tell Adam about X" for any live job |
| 1 **DONE 29/07** | Job-file contract + rotation in the bridge | No transcript over threshold; every close-out updates file + ledger; a reset chat picks up a live job without loss |
| 2 **SHIPPED 29/07** (metric window open) | `adam.md` mined + send gate + re-raise guard | Interruption yield > 1/2 for 14 days; zero "already addressed" |
| 3 **SHIPPED 29/07** | Knowledge distillation + librarian | Boot context ≤ index + job file; essays deleted from playbooks |
| 4 **SHIPPED 29/07** (accounting live; relaxation waits for data) | Token-true budgets; caps → circuit breakers | Cost per work order down, catches steady |
| 5 **SHIPPED 29/07** | Jacob parity (companies, bd.md, ledger feeds) | His Today actions cite his own history unprompted |

Each phase is independently shippable and independently reversible, and nothing touches
the safety walls. Phase 0 and 1 are where the token burn stops; phase 2 is where the
spam stops; phase 3 is where "expert knowledge" stops meaning "7,000 lines she is told
not to read".

---

## 6. Phase 0 - shipped 29/07

- **`scripts/mary_ledger.py`** - the event store (`data/ledger/YYYY-MM.jsonl`) and the
  idempotent backfill. First run: **635 events** - 41 emails sent, 213 mails/messages
  received (Adam's and Zac's words captured verbatim), 90 hub messages, 33 requests +
  18 answers, 68 catches, 10 calibration points, 162 HANDOVER records indexed by line.
  Re-running `--backfill` only adds what is new, so a scheduled run (the bridge, or
  `jacob_daily`-style) keeps it current without touching any live tool.
- **`scripts/mary_recall.py`** - the query side. `--settled --grep "strip.?out"`
  returns REQ-29's answer *and* Adam's "I have already addressed this with you" in one
  screen; `--job georgies --kind email_sent` shows the six-email spiral of 29/07 at a
  glance. Zero session tokens either way.
- **`test-results/token-baseline.md`** - the live chat registry carries ~36 MB / ~9M
  estimated tokens at rest; crestwood-park (5.9 MB), filwood (5.1 MB) and vesuvius
  (3.9 MB) are the rotation candidates Phase 1 starts with. The 28 MB transcripts in
  the 179 MB total belong to already-retired sessions - evidence that resets happen
  and lose nothing when the job file is good, which is Phase 1's whole bet.
- Known wart, accepted: a dashboard message appears twice (work order + hub message)
  under two refs. Harmless for recall; dedupe when the bridge starts writing directly.

**Next: Phase 1** - the job-file contract (300-line cap, fixed sections, bridge-enforced
at close-out) and transcript rotation seeded from it.

---

## 7. Phase 1 - shipped 29/07

The audit's surprise: **rotation already existed** (`rotate_if_bloated`, 8 MB / 600
turns, eight chats retired by the 29th) - and it proved the diagnosis rather than
fixing it, because the bloat *moved*: gordon-court's chat shrank to 0.3 MB while its
"distilled" job file grew to 265 KB / 4,165 lines, which every fresh seed then re-read.
Rotation without a bounded seed is a token relocation scheme. So:

- **`scripts/mary_jobfile.py`** - the contract: 300 lines max, `## Position` near the
  top, history in `<key>-archive-YYYY-MM.md` (`--archive` does the mechanical move and
  leaves a rebuild template; the rebuild itself is the session's judgement, never the
  script's). On day one, 16 of 18 live files fail - each chat repairs its own on its
  next run, because only it knows position from history.
- **The bridge enforces it where it cannot be ignored.** After every clean session the
  contract is checked; a failure becomes the FIRST line of that chat's next kick
  prompt, and stays there until the file is fixed.
- **Rotation seeds lean.** A fresh chat for a job with a file reads MARY-JOB-SESSION,
  the job file, and `mary_recall --job <key> --days 14` - and is told NOT to re-read
  HANDOVER.md/AI.md ("if the job file leaves a gap, fix the file so the next chat is
  not missing it too"). A job with no file must create one to the contract before
  touching work. The 10,000-line boot is gone from every seeded path.
- **The ledger stays current for free** - the bridge runs the idempotent local
  backfill after every session, so recall reflects the session that just ended.
- MARY-JOB-SESSION.md §4 rewritten as the contract, with the Gordon Court number as
  the reason.

**Next: Phase 2** - `data/knowledge/adam.md` mined from his replies, the send gate
(`mary_send.py --check` with interruption-yield evidence), and the re-raise guard.

---

## 8. Phase 2 - shipped 29/07 (the 14-day metric window runs from here)

- **`data/knowledge/adam.md`** - the Adam model, written from his corpus, not
  impressions: how he reads (phone, one screen, "It still says uPVC..." as a complete
  reply), how he decides (precedent - Brandon Estate; deadlines outrank everything;
  2.5% MCD pragmatism), and the standing decisions that must never be re-raised.
  Loaded by every session: the kick prompt names it, both playbooks open with it.
  Contract on itself: under 120 lines, updated at close-out when he teaches, pruned
  when he contradicts.
- **The send gate** - `mary_send.py --check --subject "..."`: sends today (it showed
  20 when first run), last send on this job, settled-topic matches against the ledger,
  the deduped weekly send-to-reply ratio, hours to the 07:45 digest. Never blocks;
  the philosophy is judgment with evidence, not another wall.
- **The re-raise guard** - `mary_dashboard.py` now refuses to publish an open request
  that near-duplicates an answered one (the REQ-14/REQ-2 shape) and warns when one
  touches settled ground. Tuned against the live board: REQ-24 legitimately follows
  answered REQ-17 and stays publishable; the first run also surfaced five open
  requests Adam had already answered on the hub that nobody closed - the guard is
  finding real debt on day one.
- Honest limits: "yield" counts his instructions as well as replies (labelled so),
  and the guard is judgement-support plus one narrow wall, not yet "structurally
  impossible". Both sharpen as the ledger grows.

**Next: Phase 3** - knowledge distillation (the expert shelf out of AI.md/HANDOVER
prose) and the librarian run.

---

## 9. Phase 3 - shipped 29/07

- **`data/knowledge/INDEX.md` - the shelf.** Deliberately an INDEX, not a rewrite:
  every entry is the rule in one line plus a pointer into `AI.md` / the playbooks, so
  there is exactly one source of truth and nothing can drift. AI.md's own section
  titles turned out to already be one-line rules ("A cheaper quote is not cheaper
  until you count what is not in it") - the shelf groups them by topic (pricing, spec,
  auditing, process, Adam, clients, tooling) and makes 2,924 lines random-access.
  Boot now reads MARY-HANDOVER + the shelf + adam.md instead of ~10,000 lines;
  `HANDOVER.md` is reached through the ledger's record index, not read.
- **`scripts/mary_librarian.py` - the daily metabolism.** Deterministic, zero tokens,
  runs 21:15 nightly (task `MaryLibrarian`): refreshes the ledger (networked), scores
  the job-file contract, verifies every shelf pointer still lands on a heading,
  reports send discipline and the next rotation candidates, writes
  `test-results/librarian/<date>.md` and posts one line to the noticeboard. It keeps
  score; it never edits knowledge - compaction stays with the chat that owns the file.
  First run: 644 ledger events, 22 contract problems across 16 files (the migration
  backlog the chats will clear), shelf pointers all valid, 3 chats over 4 MB queued
  for rotation.
- The boot-path essays are cut at the source: MARY-EMAIL-SESSION §0 now forbids the
  end-to-end read it used to require.

**Next: Phase 4** (token-true budgets; caps become circuit breakers) and **Phase 5**
(Jacob parity). Also still open: the one bridge restart that brings the Phase 1-3
prompt/bridge changes live - armed, waiting for a gap between her sessions.

---

## 10. Phase 4 - shipped 29/07 (accounting live; cap relaxation waits for its data)

- **The bridge measures every session's real cost**: transcript growth in bytes,
  logged to `data/mary-usage.jsonl` on every outcome including timeouts and launch
  failures. bytes/4 is coarse but ranks and trends correctly.
- **The budget gains a token gate**: ~12M estimated/day, ~2M/night (env-tunable) -
  set at 2-3x a normal day on purpose, because tripping one means something is
  LOOPING and the right response is finding the loop, not raising the cap.
- **Cost is surfaced to her**: the kick prompt now says what the window has spent and
  what her own chat contributed, next to the send list and the request backlog -
  judgment with evidence, consistent with Phase 2.
- **Deliberately NOT done yet**: raising or deleting the hour/session caps. The plan
  says relax limits one at a time WITH metrics; the metric starts recording at the
  next bridge restart. The librarian reports daily spend and top-spending chats.

## 11. Phase 5 - shipped 29/07

- **Jacob's channels joined the ledger** (48 events on first pull): his hub thread,
  his requests and answers, and the whole bot-to-bot line (`--kind botchat`). One
  recall now spans both bots: `mary_recall --grep "Lindum"` returns Zac's teaching
  messages and Jacob's own ITT finding together.
- **`data/knowledge/bd.md`** - his durable knowledge, always loaded: the win-band
  facts, the subcontractor thesis, the classification rules that each cost a day,
  and the standing decisions. Same contract as adam.md: evidence adds, evidence
  contradicts, lines die.
- **`data/companies/`** - per-company memory to the same contract as job files
  (150 lines, `## Position`), created only when a company gets real attention.
  JACOB-SESSION.md now boots from bd.md and checks the ledger before asking anyone.
- Still his: a bridge that seeds per-company sessions (his wake model is one session
  per batch today, so the files carry the memory between wakes for now).

## 12. What remains open across all phases

- The ONE bridge restart carrying Phases 1-4's bridge changes (lean seeds, contract
  enforcement, per-session ledger refresh, token accounting) - armed, fires in the
  first gap between her sessions.
- The 14-day Phase 2 metric window (interruption yield, zero "already addressed").
- Cap relaxation (Phase 4) once usage data exists to set breakers from.
- The 22-file job-file migration, cleared chat by chat as each next runs.

# MASTER PLAN - three bots and the CRM they run on

Written 2026-08-03, from the 03/08 planning meeting (Zac + Adam), Zac's review
of the first draft the same day, and the system audit. This is the destination
and the order we get there in. `BOTS.md` describes what exists; this describes
what replaces it.

Bots are **paused** as of 30/07 (Claude allowance exhausted). Nothing here
starts until Zac says so.

## 0. The two rules that govern everything below

**Make them think, do not cap them.** Zac, 03/08: *"I don't want to hard cap
anything. I just want them to think. If they sent a bunch of emails - first of
all, why? And why did they then need to send more? I just want them to have a
brain."* Mary is not spamming Adam because she lacks a quota; she is spamming
him because she cannot see what she already sent or whether it landed. Every
limit in this system is to be replaced by evidence put in front of the bot, not
by a smaller number. The only exceptions are the safety walls in §14 and the
runaway breakers - those are not judgment, they are physics.

**The token budget is the design constraint, not a target to aim at.** See §6.
It is roughly a **6x cut**, and it comes first because nothing else fits until
it lands.

> **Keep this file short.** Every knowledge document in this repo has died the
> same death - append-only prose that nobody can afford to read. This one holds
> the plan and the open decisions. Findings go to the audits, history goes to
> the ledger.

---

## 1. Three employees, one rule

Adam's test, and it settles almost every routing question: **is it a job you are
quoting for, or a job you have won?**

| | **Mary Grace** | **Jacob Wright** | **Joseph Scott** |
|---|---|---|---|
| Role | Estimating | Business development | Project management |
| Owns | Pricing and spec | The **lead**, start to finish | The **contract**, PO to final payment |
| Status | Live since 24/07 | Live since 28/07 | **Not built** |
| Unit of memory | The job | The company | The contract |

The lead-to-contract conversion is the handover between Jacob and Joseph, the
same boundary AdminBase already draws.

---

## 2. The target workflow

Changed at the meeting. Jacob now owns the front of the funnel, taking over the
logging Gintare does by hand today.

**Adam sits in the loop at the front as well as the back** (Zac, 03/08,
correcting the first draft): the enquiry does not go straight from Jacob to
Mary. Jacob receives it and messages Adam, and Adam is the one who acts outward,
because Jacob has no send path. *(The exact shape of that hop is still garbled
in the transcript - see D8.)*

```
enquiry arrives
      │
      ▼
  JACOB  logs the lead, qualifies it, messages ADAM
      │
      ▼
  ADAM   acts outward - Jacob cannot send
      │
      ▼
  MARY   prices it - spec, supplier costs, quote pack
      │
      ▼
  ADAM   checks it, and sends it to the client himself
      │
      ▼
  JACOB  logs that it went, chases it, records every reply
      │
      ├── lost / closed ──► job closed email, archived
      │
      └── WON: purchase order received
                  │
                  ▼
            JOSEPH  runs the contract to completion, then the money
```

**Adam sends the quote, not Jacob.** The meeting floated Jacob sending it and
then settled on Adam - "for now, Mary will just send it to me and I'll send it
out to the client." That decision is what keeps Jacob's no-send wall standing.

---

## 3. The leads pipeline, split

Mirrors the AdminBase leads board Adam walked through.

**Estimating half - Gintare today, Mary tomorrow**

| Step | What happens |
|---|---|
| Acknowledgement | Customer told we have it and are working on it |
| Materials out | Enquiry packaged and sent to suppliers for costs |
| Awaiting costs | Checklist of who owes us a price |
| Quote ready to check | Goes to Adam |
| Pre-quote call | Prompts Adam to ring: where we are, quote coming, when are you deciding, how does the price sound |
| Quote sent | Adam sends. Handover to Jacob fires here |

**BD half - Jacob**

| Step | What happens |
|---|---|
| First follow-up | Chase after the quote lands |
| Final follow-up | Last chase before closing |
| Job closed email | "We are shutting your job down on our system" |
| Client award due date | When *our client* hears if **they** won. Goes red when it is time to call |

---

## 4. The contract checklist - Joseph

Triggered by the PO and go-ahead. Every item is deadline-driven, worked
**backwards from the site date**.

1. Sign off PO (read it, send it back)
2. Provisionally book installations (against Paul's diary)
3. Submit designs
4. Book survey
5. Order frames
6. Order glass
7. Send RAMs
8. Arrange labour
9. Order consumables
10. Confirm installation bookings
11. Send O&M
12. Invoice, then chase it

**Joseph maintains this himself** (Zac, 03/08: "the bot manages it"). He is CC'd
on the traffic, so a supplier confirmation ticks "order glass" without anyone
touching a checkbox. Humans correct him by email; they do not feed him.

This is the whole reason the AdminBase version failed. Adam's own diagnosis:
every box is red, it is not kept up to date, and nobody looks at it. A checklist
that depends on human data entry has already been tried here and lost.

**It must say what to order, not only that ordering is due.** AdminBase says
"order glass"; the spec is somewhere else. *(ASSUMPTION - inferred from the
meeting, confirm.)*

---

## 5. Sequence

Cost architecture first (Zac, 03/08). Nothing new gets built on the thing that
burned the allowance, and Jacob and Joseph both need the memory that stage
builds anyway.

| Stage | Builds | Done when |
|---|---|---|
| **0** | Cost architecture and memory | Real token cost is measured and bounded; a bot session's cost is flat in job age, not growing |
| **1** | The record (CRM core) | One schema all three bots read and write; AdminBase fed from it |
| **2** | Jacob's lead lifecycle | A lead is logged, chased and closed without anyone opening AdminBase |
| **3** | Mary onto the record | Her half of the leads pipeline runs from the same data |
| **4** | Joseph | A won job runs its 12 steps and gets invoiced |
| **5** | Hub, permissions, CRM surface | Paul and Steve open one page and know their day |

Each stage is independently shippable. Stages 2-4 depend on 1; 1 depends on 0.

---

## 6. Stage 0 - cost architecture

### The budget, which is the whole problem

Zac, 03/08: one **Claude Max** plan covers the bots *and* all other development
(the company website included). On a normal Monday of ordinary coding, dev alone
took **5% of the weekly allowance**. An even burn would be ~14%/day. The target
is that **the entire bot system fits inside 5% of the weekly allowance per day**,
leaving the rest for dev. There is no bigger plan to buy.

Measured against what the bots actually did (`scripts/mary_cost.py`, deduped -
see §6a):

| | |
|---|---|
| Bot spend, mean active day | **365M** context tokens |
| Peak day (28/07) | **776M** |
| Whole week, bots + dev | **~2.37B** - and that exhausted the allowance |
| Implied 5%/day ceiling for bots | **~118M/day** |
| Required cut | **~3x** on a mean day, **~6.5x** against the peak |

*(The ceiling assumes the 27-30/07 spend is roughly one weekly allowance, which
fits: the bots produced almost nothing before the 27th and the plan ran out on
the 30th. Treat it as the right order of magnitude, not a measured constant.)*

**57.3% of all bot spend happened between 22:00 and 07:00.** The busiest single
hour of the entire week was **06:00**. Zac's instinct - *"do we really need it to
run overnight unless Adam directly calls for it?"* - is worth more than half the
bill on its own, and it is the cheapest change available.

Two chats, `gordon-court` (472M) and `riverside` (471M), are **65% of all bot
spend** between them.

So Stage 0 has a number to hit, not just a defect to fix. Overnight running is
**off by default**, available on demand when Adam is working late.

### 6a. Two ways to get this measurement wrong

Both were made on 03/08 before the numbers above settled. They are recorded
because anyone re-measuring will hit them.

1. **Transcript growth is not cost.** The old meter recorded how much the file
   grew. The cost is the context re-read on every turn. Like-for-like over the
   window the old meter covered: it reported **3.9M**, the truth was **117M** -
   understated **30x**.
2. **Usage records duplicate.** One API call is written as several assistant
   records - a text block and a tool_use block each carry a *copy* of the same
   usage object. Summing rows inflates everything by ~1.7x (4.08B raw against
   2.38B real across the project folder). **Dedupe by `requestId`.**

### The defects

From the 03/08 audit. These are the numbers that set the work.

- **The token meter is wrong by ~300x.** `mary_budget.log_tokens()` records
  transcript *growth*. The real cost is context *re-read every turn*. On 29/07
  the meter said 3.06M; the transcripts say **942.7M**. On 28/07: **1.53
  billion**. All-time 3.84B cache-read against 19.3M output.
- **The 12M/day breaker could never fire**, and its "2-3x a normal day" sizing
  was derived from the broken meter.
- **Two chats are 38% of all spend.** `gordon-court` 873M across 1,884 messages
  - an average of **463k tokens of context per message** - and `riverside` 682M.
  These are 1M-context sessions re-reading themselves on every turn.
- **Rotation is far too late and checked too rarely.** 8 MB is already ~2M
  tokens, and it is only tested at dispatch, so one session took a file to
  17.6 MB and another grew 7 MB in 39 minutes.
- **The distillates re-bloated.** `bd.md` 384 lines against a 120-line
  contract; `bd-lessons.md` 2,155 lines. **13 of 20 job files fail their own
  contract**, `gordon-court.md` at 4,165 lines against 300. The bridge only
  warns.
- **Jacob has no memory at all** - `jacob_bridge.py:351` mints a fresh UUID per
  dispatch, so every session boots cold and re-reads his knowledge base.
- **Jacob self-generates work hourly, around the clock**, until 70% of a
  12-hour budget is gone.

The work:

| # | Item |
|---|---|
| 0.1 | Meter real cost: sum `cache_read + cache_creation + input` per assistant message from the transcript jsonl. Re-base every cap on it |
| 0.2 | Cap **context per turn**, not hours or sessions. Measure mid-session, not only at dispatch |
| 0.3 | Enforce the job-file contract at close-out instead of warning. Migrate the 13 failing files |
| 0.4 | Distillate contracts enforced the same way. `adam.md` (71 lines) is the shape that held; `bd.md` and `bd-lessons.md` get the same treatment |
| 0.5 | Give Jacob persistent per-company sessions seeded from `data/companies/<key>.md` |
| 0.6 | Kill the prompt-inflation loop - triage prompts list the entire queue, which grows while sessions fail (28,695 → 34,360 bytes on 30/07) |
| 0.7 | Put a floor under the standing agenda so an empty inbox stops generating work |
| 0.8 | Commit the two uncommitted fast-fail backoff fixes (written 30/07, never run) |
| 0.9 | Safe resume: **32 work orders are queued for Mary, 2 for Jacob.** Triage them before the bridges come back up |
| 0.10 | **Overnight off by default**, on demand when Adam asks. Worth 55% of spend |
| 0.11 | Replace the caps with evidence, per §0: what she already sent, whether it landed, what is already open. Caps stay only as runaway breakers |

**Done when** two things are true: a session's cost is **flat in the age of the
job** it is working on (today it grows without bound), and a normal working day
for all bots fits inside **5% of the weekly allowance**.

---

## 7. Stage 1 - the record

One schema, on the hub's D1, that all three bots read and write. The ledger
(`data/ledger/`) already does append-only events well and stays; this is the
*state* the events move.

**Entities:** Company → Contact → Enquiry/Lead → Quote → Contract → Task →
Invoice → Payment, with Note attachable to any of them.

Requirements that came out of the meeting:

- Click a job and see everything: company, respondents, notes, dates, the quote
  that went out
- Notes carry their source - email, phone call relayed by Adam, or bot-derived
- Every state change is attributable to a bot or a person

**AdminBase runs in parallel** (Zac, 03/08). One constraint the meeting did not
have: **there is no write path and no live read feed.** `jacob_adminbase.py`
reads a one-off CSV Adam emailed on 28/07; the promised live feed never
arrived, and that export was already behind reality when it landed. Parallel
therefore means the hub holds the record and **emits an AdminBase-shaped import
file**, unless a live feed turns out to exist. See open decisions.

---

## 8. Stage 2 - Jacob's lead lifecycle

**Start by establishing what he actually does.** Zac, 03/08: *"He's honestly
been doing nothing. I don't know where he's getting the leads. I don't know how
he's verifying that we can actually win them. I don't know how he's comparing it
to our database. I don't know his process start to finish."* That is the first
deliverable of this stage - his sourcing, qualification and matching process
written down and checked against what the code really does, before any of it is
rebuilt. A BDM whose process cannot be stated is not a BDM.

The cause is almost certainly 0.5: he starts every session cold, so there is no
process to observe, only 218 disconnected runs.

Then:

- Log an incoming enquiry as a lead himself, replacing Gintare's manual entry
- Carry it through the BD half of the pipeline (§3)
- **Today's calls at the top of the board** - "these are the people you are
  chasing today" - optionally emailed to Adam as well
- Ingest email he is CC'd on and write the note himself
- Accept plain-English instruction by email: *"I just had this call with Jordan
  about this job, set the next action date"* - and just do it
- Receive the quote-issued handover from Mary (this already exists in the
  ledger as a `quote_issued` event and needs no conversation between them)

Depends on Stage 0.5 - none of this works while every session starts cold.

---

## 9. Stage 3 - Mary onto the record

Mary is the bot that mostly works; her engine, checks and calibration are the
best-built things here and are not being rewritten. What changes:

- She takes the estimating half of the leads pipeline (§3) as tracked state
- The acknowledgement email and supplier RFQs become hers *(subject to §11)*
- "Quote ready to check" becomes a hub state, not an email
- She raises the pre-quote call prompt for Adam

---

## 10. Stage 4 - Joseph Scott

> **This spec is the softest thing in this document.** Zac, 03/08: *"I don't
> really know - that was just Adam waffling on."* Treat §4 and everything below
> as a sketch of the shape, not a requirement list. It gets nailed down properly
> before Stage 4 starts, and it is deliberately last for that reason.

Everything a new bot needs, none of which exists:

- Mailbox, two Entra apps (reader/sender), scope group, transport rule
- A bridge on the Stage 0 cost architecture, memory keyed to the contract
- Hub registry entries - the recipe is in `MARY-HUB-DEV.md`; adding a bot is one
  entry in each of three registries plus its own tables
- The 12-step checklist, self-maintained, deadlines backwards from the site date
- Daily list and weekly overview
- **Invoicing:** job date passes → he knows it is done → generates the invoice →
  surfaces it as "invoice to check" → Adam confirms → it goes
- **Payment terms learned per client** (30 days, 30 days end of month, 45 days,
  immediate - and immediate gets 30 in practice)
- **Six-stage chase ladder**, stage 6 = day 75 past due = formal escalation.
  Never yet used in anger; a few residential disputes only

---

## 11. Every outbound email, to be ruled on one at a time

Zac, 03/08: *"we can go through the emails for each one and see what we need for
each in the plan."* This is that list. Nothing here is decided.

Today two **enforced** Exchange transport rules stand: Mary can email only
`adam@`/`marketing@`, and `jacob@` cannot email outside Fenster. Several rows
below need one of them opened.

| # | Email | From | To | Trigger | Needs a wall opened |
|---|---|---|---|---|---|
| 1 | Acknowledgement | Mary | Customer | Enquiry received | **Yes** |
| 2 | Supplier RFQ | Mary | Supplier | Materials out for pricing | **Yes** |
| 3 | Quote ready to check | Mary | Adam | Quote assembled | No |
| 4 | The quote itself | Adam | Customer | Adam approves | No - human sends |
| 5 | First follow-up | Jacob | Customer | Chase date | **Yes** |
| 6 | Final follow-up | Jacob | Customer | Chase date | **Yes** |
| 7 | Job closed | Jacob | Customer | No response, job dead | **Yes** |
| 8 | Daily call list | Jacob | Adam | Each morning | No |
| 9 | Design/RAMs/O&M submissions | Joseph | Client | Checklist step | **Yes** |
| 10 | Purchase orders | Joseph | Supplier | Order frames/glass/consumables | **Yes** |
| 11 | Labour booking | Joseph | Fitters | Arrange labour | **Yes** |
| 12 | Invoice | Joseph | Client | Job complete, Adam confirms | **Yes** |
| 13 | Chasers, stages 1-5 | Joseph | Client | Days past due | **Yes** |
| 14 | Formal escalation, stage 6 | Joseph | Client | Day 75 | **Yes** - and arguably never automatic |

For each row we decide: autonomous, queued for one-click approval, or drafted
for a human to send. My recommendation is that **anything about money or legal
standing (12, 13, 14) is never fully autonomous**, and that the approval queue
is built before rows 1-2 and 5-7 are opened.

---

## 12. The hub - Stage 5

One hub, one set of permissions. Settled at the meeting; no second Cloudflare
project.

| Role | Who | Sees |
|---|---|---|
| Admin | **Zac and Adam only** | The dashboard as it is today: all three bots, internal chat, teaching them, plus the CRM and finance |
| Delivery | Paul, Steve, others | The **AdminBase clone** - same functionality, nothing like the same look. Deadlines pushed to the top of the page |

Two distinct surfaces on one hub, not two products. Zac, 03/08: admin is "the
dashboard as it currently is where we can access the bots and tell them what to
do" - and specifically **keep the sender verification**: *"I like how it
verifies that it's coming from us before they change the dashboard or do
anything."* That is the injection guard, and it stays exactly as it is.

The delivery surface is judged on one thing: whether Paul and Steve open it and
know their day without reading anything. Layout is optimised for that and
nothing else.

The Mary dashboard becomes *the* dashboard and grows into the CRM.

Login is currently **off** (`AUTH_DISABLED = true`). It goes back on before any
of this carries client data or reaches Paul and Steve.

---

## 13. Open decisions

Nothing below is blocked on me. Each changes the work.

| # | Question | For |
|---|---|---|
| D1 | Does AdminBase have an API or scheduled export we can drive, or is Adam's manual CSV the only channel? Determines what "parallel" costs | Adam |
| D2 | The six chase stages - exact day counts and what each sends. Day 7, 35 and 75 are known | Adam |
| D3 | Payment **applications** or final invoices only? Different cycles on commercial work | Adam |
| D4 | Where does the invoice figure come from - quote total, PO value, or measured final account with variations? | Adam |
| D5 | Do Paul and Steve get hub logins, or only the daily list, now that Joseph maintains the checklist? | Zac |
| D6 | Row-by-row ruling on §11 | Zac + Adam |
| D7 | Does the checklist need to carry the spec of what to order, not just that ordering is due? | Adam |
| D8 | The front of the workflow (§2). Transcript: *"Jacob gets the inquiry, he messages Adam, who then messages out [garbled]. Well, he doesn't have email access."* Who does Adam message, and is the acknowledgement to the customer his or Mary's? | Zac |

**Source material for all of this:** `test-results/adam-corpus.md` - every
message Adam has sent that we hold, 88 emails and 77 hub messages, 24-30 July.
It is the evidence behind `data/knowledge/adam.md` and the best guide we have to
what "good" looks like.

---

## 14. What does not change

The safety walls stay walls, through every stage. They are not judgment rules
and they are not up for relaxation as a convenience:

- Exchange transport rules (opened deliberately per §11, never by accident)
- Mailbox scoping by `ApplicationAccessPolicy`, per bot, per group
- The injection guard - instructions only from Adam, Zac, marketing, the hub
- Ghost protocol - compose fresh, never reply-all into a client thread
- The bot-chat rate limit
- The hub deploy guard, and `wrangler` run from inside `dashboard/`

And the rule underneath all of it, unchanged from `BOTS.md`: **check it, do not
assume it.** Every wrong number in the audit came from something that looked
right.

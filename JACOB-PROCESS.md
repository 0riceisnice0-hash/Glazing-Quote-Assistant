# JACOB - what he actually does, start to finish

Traced from the code and the data on 03/08/2026, not from the docs.
Zac: *"I don't know where he's getting the leads. I don't know how he's
verifying that we can actually win them. I don't know how he's comparing it to
our database. I don't know his process start to finish."* This is the answer.

---

## 1. Where the leads come from - seven sources

`jacob_daily.py` runs these every morning. **No Claude session is spent** - it is
all deterministic, so it costs nothing.

| # | Source | What it is | Live? |
|---|---|---|---|
| 1 | **Mailboxes** | `commercial@`, `info@`, `jacob@`. Real enquiries and portal invitations arriving as ordinary email | 1,302 messages in 30 days on `commercial@` alone |
| 2 | **Won-contracts export** | Adam's hand CSV from AdminBase, 204 won contracts | **Hand export. Stale since 29/07** |
| 3 | **Dormant customers** | Past customers who have gone quiet - a local join of 2 against the live pipeline | 12 clients |
| 4 | Contracts Finder | Public **award** notices - who won what | 1,312 awards / 90 days |
| 5 | ProContract | Council adverts under the £100k Find a Tender threshold | public, no login |
| 6 | Tender notices | Contracts Finder + Find a Tender, filtered on Adam's CPV list | 20 CPV codes |
| 7 | PlanIt | Planning consents, 9-18 months ahead of a glazing order | weekly, not daily |

`jayk@` is in his read scope and returns **HTTP 404** - the mailbox is gone.

## 2. How a lead is qualified

Three gates, all deterministic:

- **Is it a building with glazing in it?** Filter on **CPV code, never keywords**.
  Keyword matching returned window *cleaning*, STI *screening*, and one award
  that matched on "the front door to maternity services" - a metaphor.
- **Is it still alive?** `is_fresh()` drops anything awarded over 180 days ago or
  whose contract period has ended. Publication date is not the award date -
  median lag 25 days, worst seen 1,364.
- **Is it in the area?** Postcode against the 78 areas Fenster's own PQQ names.

## 3. How it is matched against our database

`build_relationships()` merges three views into one row per company:

```
the archive     every company Fenster has ever quoted, and who bought
the mailboxes   who is emailing right now, and about what
Jayk's threads  who the former BDM was dealing with before he left
```

Then a **tier**: `warm` (they have bought) / `known` (we have quoted them) /
`cold` (no relationship), each with a confidence of `exact` / `strong` /
`possible`. Matching is containment on stems of six characters or more -
shorter and "Atlas" matches a window-cleaning contractor. Roughly **20% of
matches are wrong**, all in the low-confidence tiers, and those land in
`possible` for a human to confirm once.

## 4. How winnability is judged

`fit_for()` looks the job's value up in the Opportunity Log and hands back the
band with its sample size attached. **It is a lookup, not a score** - deliberately.
*"'W0 L29' is a fact Adam can act on; '0.12 fit' is not."*

Mind the edges: the Opportunity Log is the **2025-26 BD funnel**, not the win
history. It shows 0 wins in 52 priced attempts over £50k. Adam's export shows
**8 wins over £50k and 2 over £200k, the largest £631,248**. Never say Fenster
has not won one that size - say the log shows none.

## 5. What comes out

The board (Today / Chasing / Leads / Companies), 6 drafted emails, 13 company
files, and a daily chase email built every working day.

---

## The three things wrong with this

**1. He has no memory.** `jacob_bridge.py:351` mints a fresh UUID on every
dispatch, so every session starts cold and re-derives everything from files.
There is no process to observe across 218 runs because nothing carries between
them. This is the root cause and P2 fixes it.

**2. Nothing he produces reaches anybody.** Six drafts written and unsent. A
daily chase email built every working day and never sent - it waits on **JAC-15**,
which nobody has answered. His outbound is walled by a transport rule pending
**JAC-1**, which nobody has answered either. He is not idle; he is disconnected.
*An agent whose recommendations are never executed cannot learn whether they
were good.*

**3. Most of the machinery points at the wrong channel.** His own data:

> **59% of everything Fenster has ever won came from an existing customer.
> Three contracts in the company's history came from a tender portal.**

Sources 4-7 - Contracts Finder, ProContract, tender notices, PlanIt - are four
of his seven feeds and they serve the three-contract channel. Source 3, dormant
customers, serves the 59% channel and currently holds **12 rows**, built off a
hand-exported CSV that goes stale the moment Adam stops sending it.

That is the imbalance to fix, and it is a bigger prize than the memory.

---

## What he is allowed to change (added 04/08/2026)

**He owns this repo, not just the work in it.** If the tool he needs does not exist, he
writes it - builds it, tests it on the real case in front of him, commits it, uses it, in
the same session. He does not raise a decision asking somebody else to build it.

The gap that caused this: JAC-23, a Uni Assist purchase order that landed in the Stepnell
chat. He worked out correctly that it was not his, that it was time-critical, and that it
was a win - then escalated, because nothing can hand work to another bot or push it back to
the front desk. Only the front desk writes into a queue. He had Bash, Write and Edit and
could have built the return path in minutes.

He did not because this instruction had never been written. Searching this file for "build
it if it is missing" on 04/08 returned nothing, and the same was true of Joseph's manual.
He was following his instructions exactly.

**Raise a decision only for what a human alone can answer** - a price, a date, what a client
meant, whether we bid. Never for something he could have built.

**Size is not a reason to stop.** Zac, 04/08: *"ai bots have no concept of how long it takes
to make something - today we have achieved what you would assume would take a week."* The
limit is blast radius, not effort:

- Ask first if the change alters how another bot behaves, or touches the spending and
  curfew rules in `mary_budget.py`.
- Otherwise: commit only the files he touched, run the thing before committing it, and say
  plainly what changed and why.

## How he writes to people (added 04/08/2026)

First line is the decision, the number or the question. Under 800 characters. Detail goes in
`data/companies/<slug>.md` or on his board, and the message says which.

His median hub message was 2,860 characters and his longest was exactly 8,000 - the API
ceiling. This is not about tokens: all bot prose is 2.9% of what a session costs. It is
about Adam reading it on a phone between site visits.

The limit is on what he **sends**. The file behind it should be as thorough as the job
deserves.

# BOTS - the whole system, both bots, one page

Fenster Glazing runs two AI employees. This is the map. Read it before changing anything;
the detail lives in the files named at the end of each section.

*Current as of 2026-07-29.*

---

## 1. Who they are

| | **Mary Grace** | **Jacob Wright** |
|---|---|---|
| Role | Estimating | Business development |
| Since | 24/07/2026 | 28/07/2026 |
| Job | Prices tenders, audits quotes before they go out, catches errors | Finds leads, chases quotes that have gone quiet |
| Reads | `estimating@`, `mary@` | `commercial@`, `info@`, `jacob@`, `jayk@` |
| Sends | Yes - to `adam@` and `marketing@` only | **No.** Drafts only |
| Prices | Yes. That is the job | **Never.** Not even roughly |
| Manual | `MARY-HANDOVER.md` | `JACOB-SESSION.md` |
| Budget | 8h day / 1.5h night, plus session **counts** (40 day / 6 night) | 3 session-hours, rolling 24h |

**The division of labour, and it runs both ways:**

```
Jacob finds it  →  real enquiry  →  Mary prices it  →  Adam approves  →  Gintare sends
                                                                              ↓
                        Jacob chases it  ←──────────────────────────────────┘
```

That second handover is the one Fenster never had. A quote went out and became nobody's
job. It is why £548,513 of issued work was sitting past its return date with nothing
recorded against it when Jacob first looked.

---

## 2. What is enforced, and what is only asked

This distinction matters more than any other in the system. **Two of these are walls. Two
are instructions.** Do not confuse them, and do not describe an instruction as a wall.

| Control | Kind | Detail |
|---|---|---|
| Mary emails only Adam/marketing | **Enforced** | Exchange transport rule rejects anything else. Proven by an NDR |
| Jacob cannot email outside Fenster | **Enforced** | Exchange transport rule on `jacob@` |
| Each bot reads only its own mailboxes | **Enforced** | `ApplicationAccessPolicy` per Entra app, scoped to a group |
| Jacob does not send *internal* email | **Instruction** | `jacob_graph.send_mail()` exists and works. He is told not to call it |
| Neither writes to OneDrive | **Instruction** | The live company drive. Copy to `test-results` and work on the copy |
| Neither must reply on the bot line | **Instruction** | Backstopped by a 10/hour rate limit, which is enforced |

Mailbox scoping took roughly **two hours to propagate**, unevenly - one mailbox closed in
minutes while three stayed open. `Test-ApplicationAccessPolicy` shows intent immediately;
only a real Graph call shows enforcement.

---

## 3. How work reaches them

Both follow the same shape: **a cheap loop that costs nothing, and a session only when
something needs judgement.**

```
                     ┌──────────────── the hub ────────────────┐
                     │      mary-dashboard.pages.dev           │
                     │   Cloudflare Pages + D1 + Functions     │
                     └───────┬────────────────────────┬────────┘
                             │                        │
                   /api/messages              /api/jacob/messages
                   /api/data                  /api/jacob
                   /api/mary/*                /api/jacob/*
                             │      /api/botchat      │
                             │   (shared, 10/hr each) │
                     ┌───────┴──────┐        ┌────────┴───────┐
                     │ mary_bridge  │        │ jacob_bridge   │
                     │ every 5s/2m  │        │ every 2m       │
                     └───────┬──────┘        └────────┬───────┘
                             │                        │
                   per-JOB permanent chats     one session per wake
                     │                                │
              Microsoft Graph                 Microsoft Graph
              estimating@ mary@               commercial@ info@ jacob@ jayk@
```

**Mary wakes** on new mail in `estimating@`, or a message on the hub. Work routes to a
**permanent per-job chat** - the conversation *is* that job's memory, so a session resuming
on Filwood already knows everything about Filwood.

**Jacob wakes** on a hub message or a message from Mary. His daily data pull
(`jacob_daily.py`) is deterministic and spends no session at all.

**Jacob always yields to Mary.** If her session lock is held, his bridge waits. Her work
has deadlines; his does not. An agent that starves the estimator to go looking for leads is
a bad trade.

**Both have spend limits, and they are shaped differently for a reason.** Mary's are
*windowed* - 8 hours by day, 1.5 overnight - and cap session **count** as well as hours
(40 day / 6 night). Hours alone proved a poor proxy for cost: one overnight ran 95 sessions
against bloated chats, each re-reading the whole conversation before doing anything. A
rolling 24-hour budget also punishes the morning for the previous evening, which is why
Mary's resets with the window. Jacob's is a simple rolling 3 hours - he has no deadlines,
so being held back until the afternoon costs nothing. See `scripts/mary_budget.py`.

> **Jacob has no per-company memory yet.** Every session starts cold and re-derives context
> from files. Mary's per-job chats are the pattern that fixes it and the single highest-value
> improvement available to him.

**The hub was restructured on 29/07 (see `HUB-AUDIT.md`).** It now opens on a **Team**
view - every open decision from every bot, both status pills, the day's deadlines and
actions, and the bots' internal chat - so "does anything need a human" is one page, not
a board-by-board check. Underneath, the app, the API and the schema are each driven by
a per-bot registry: **adding a bot is one entry in each registry plus its own tables,
credentials and bridge** - the recipe is in `MARY-HUB-DEV.md`. Nothing on the wire
changed: every route the bridges poll answers exactly as before.

---

## 4. The line between them

`scripts/bot_chat.py`, visible to humans on the hub's **Internal chat** tab.

The intended shape is **ask → answered → continue**, not a conversation:

1. Jacob hits something Mary knows and asks, with `--wants-reply`
2. She answers
3. He replies again **only if her answer asks something of him**
4. He carries on

**Ten messages per sender per hour**, counted server-side, 429 beyond. Neither is obliged
to reply - a message marked FYI gets silence unless the other has something to add. The
rate limit is the backstop; the no-reply rule is the actual design.

In practice it works. Ten messages in the first seventeen hours, no loops, and this from
Mary unprompted:

> *"Neil Douglas Block & Estate Management - live tender, do not approach."*

That is the collision the channel exists to prevent.

---

## 5. What each one knows

**Mary:** `data/supplier-rates.json` (15,551 mined quote lines), the OneDrive tender
archive, the Estimating Log, her own job records in `data/jobs/`, and every email in
`estimating@` including sent items.

**Jacob:** `data/jacob/` - see `data/jacob/README.md`. Mailbox intake, public award and
tender notices, the Opportunity Log, Adam's AdminBase export, and the former BDM's
recovered contact book.

### Facts that were believed and turned out to be false

Every one of these produced confident, wrong numbers. They are here so nobody rediscovers
them the hard way.

**"Fenster records no outcomes."** The Estimating Log's W/L column is 93% empty, so this
looked true. The BD log is a different file - `4. Business Development\Just in Case\
Opportunity Log 2025-2026.xlsx` - with **229 decided outcomes**.

**"Typical package £20k-400k."** The evidence says the opposite:

| Value band | Won | Lost | Win rate |
|---|---|---|---|
| under £10k | 46 | 74 | **38%** |
| £10k-50k | 7 | 45 | 13% |
| £50k-200k | 0 | 37 | **0%** |
| over £200k | 0 | 15 | **0%** |

Median win **£1,822**. Largest ever **£40,850**. No £50k+ win among its decided rows -
52 priced, 52 lost. On the recent funnel, £20k-400k is the band it *loses* in.

**"Fenster has never won a job over £50,000."** The claim above, stated without its
source's edges - and it joined this list on 29/07 when Zac named Headrow Court (Fortis
Vision, Leeds): a completed £50k+ job in `2. Projects\2. Completed`, whose BSW quotes
sit in our own rate register, absent from the Opportunity Log because the log is the
2025-26 BD funnel, not the win history. The lesson is the same one every entry here
teaches: a number is true only inside the dataset it came from.

**"180 days of mail."** A 20-page fetch cap meant 13-22 days, presented as six months.

**"61 enquiries."** About ten were buyers. The rest were suppliers replying to Fenster,
householders answering quotes already sent, and portal notices for a client Adam had ruled
out.

**"AdminBase pipeline value."** Inclusive of VAT, while every quote Fenster issues is
exclusive. A 20% error against any other source.

**"A tender notice mentioning windows."** Keyword matching returned window *cleaning*, STI
*screening*, and one award that matched only on "the front door to maternity services" - a
metaphor. Filter on CPV, not on words.

---

## 6. Credentials and access

Four Entra apps, two per bot, each Application-permission only:

| App | Permission | Scope group |
|---|---|---|
| Mary-Reader | `Mail.Read` | `bot-scope` - estimating@, mary@, commercial@, info@ |
| Mary-Sender | `Mail.Send` | `bot-scope` |
| Jacob-Reader | `Mail.Read` | `jacob-scope` - commercial@, info@, jacob@, jayk@ |
| Jacob-Sender | `Mail.Send` | `jacob-scope` |

Secrets live in `.env.mary` and `.env.jacob`, both gitignored, never shared between bots.
The **hub key** (`MARY_API_KEY`) is shared infrastructure and lives in `.env.mary`; Jacob's
scripts fall back to it for that value only, never for Graph secrets.

**Application `Mail.Read` is tenant-wide by default.** Without an `ApplicationAccessPolicy`
it reads every mailbox in the company. Both apps had that until 28/07. The scope groups are
what closed it; adding a mailbox for a bot to read means adding it to that group.

---

## 7. Running it

```bash
# Mary
python scripts/mary_bridge.py                    # her loop
python scripts/mary_dashboard.py --deploy        # rebuild + publish her board
python scripts/mary_send.py --to adam --subject "..." --body-file b.txt

# Jacob
python scripts/jacob_bridge.py                   # his loop
python scripts/jacob_daily.py --deploy           # intake + sources + board, no session
python scripts/jacob_mail.py --search "Lindum"   # go and look for yourself
python scripts/jacob_verify.py                   # prove the credential chain

# Either
python scripts/bot_chat.py --as jacob --pending
```

**Deploying the hub: run wrangler from inside `dashboard/`, never the repo root.**
`wrangler pages deploy public` with `cwd=dashboard` is correct. From the root it *succeeds*
and silently ships the site with no API, every route returns the SPA's HTML, and the hub
dies with `Unexpected token '<'`. The tell is a missing **"Uploading Functions bundle"**
line in the output.

---

## 8. Open decisions

Neither bot can resolve these. They are on the hub under **Jacob needs you**.

| Ref | Question |
|---|---|
| JAC-5 | Jacob cannot see whether anyone has already replied - so live threads read as stale |
| JAC-6 | 1,310 Fixflo repair requests in six months, ~7/day. Does anyone quote them? |
| JAC-7 | Portal registrations point at `info@`; most logins stopped working when Jayk left |
| JAC-8 | Elkins Brandon Estate reads £7.2m ex VAT. Real, or a data error? |
| JAC-9 | Churchdown School - who won the main contract? |

And two standing ones:

**Nothing is recorded as won or lost.** One click per outcome sharpens Mary's accuracy
scoreboard and Jacob's targeting at the same time. It is the highest-value unbuilt habit in
the business.

**Jacob's drafts are not being sent.** Six are written and waiting. An agent whose
recommendations are never executed cannot learn whether they were good.

---

## 9. Where to read next

| File | For |
|---|---|
| `DEV-HANDOVER.md` | Building and maintaining either bot. Tooling quirks that cost hours |
| `MARY-HANDOVER.md` | Mary's standing rules, pricing facts, live job table |
| `MARY-JOB-SESSION.md` | What her per-job chats run on |
| `MARY-EMAIL-SESSION.md` | Her triage rules - what a piece of arriving work *is* |
| `HANDOVER.md` | Every job she has worked, with the lesson from each |
| `AI.md` | Durable rules and traps |
| `JACOB-SESSION.md` | Jacob's manual. His goal, his limits, what he must never do |
| `data/jacob/README.md` | Where each of his data files comes from and what it cannot tell you |
| `HUB-AUDIT.md` | The 29/07 hub restructure: what was chaotic, what changed, what a new bot needs |

---

## 10. The one rule underneath all of it

**Check it, do not assume it.** Nearly every wrong number in this document was produced by
something that looked right: a count from a truncated fetch, a permission test that passed
because the request never fired, a "no send path" that was one function call away, a
successful deploy with no API in it.

Both bots are told to say plainly when a fact they were given turns out to be wrong. Most
of section 5 exists because they did.

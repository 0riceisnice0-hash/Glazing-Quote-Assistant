# GLASSHOUSE

Fenster Glazing's commercial operation: three AI personas over one shared
record, everything visible on one hub.

**Hub: https://glasshouse-79z.pages.dev**

| | |
|---|---|
| **Mary Grace** | Estimating - prices tenders, audits quotes, catches errors |
| **Jacob Wright** | Business development - owns the lead, chases the quote |
| **Joseph Scott** | Project management - owns the won job, PO to payment |

Built 04/08/2026 as a ground-up replacement for the bridge-per-bot system that
preceded it (that system, its manuals and its history live in `attic/`).
The design in one sentence: **stateless workers over a stateful record** -
sessions are born from a query, do bounded work, write back through one finish
call, and die.

Read `personas/SYSTEM.md` for the whole architecture on a page, and
**`HANDOVER.md` for what is actually happening right now** - what is running,
what is half-finished, and the mistakes that are worth not repeating.

They work **08:00-18:00**. Nothing they write ever leaves Fenster: no client
email, not even a draft for a human to send. When a bot cannot find something
it raises a need on the hub, marked according to whether **we** hold the answer
or a **supplier** does.

## Layout

```
core/        the engine - intake, dispatch, finish, record client, breakers
             plus the tools a desk uses: mail.py (search every folder),
             rates.py (benchmarks + pricing scoreboard), agenda.py (standing
             work and hour-long projects), trace.py (feeds the Live page)
personas/    SYSTEM.md + one charter per persona (their entire manual)
hub/         the Glasshouse hub - Cloudflare Pages + D1 (the record itself)
scripts/     craft tools that survived: Mary's checks engine and backtest,
             rate mining, Jacob's data pulls. Product code, not plumbing.
             restart_engine.sh is how the engine is swapped over safely.
data/        supplier rates, calibration, mail attachments, local state
attic/       the old system, frozen: scripts, docs, dashboard. Reference only.
outputs/     deliverables (pricing workbooks, proposals)
```

The repo root also carries the original Glazing Quote Assistant web app
(`index.html`, `js/`, `css/` -> glazing-quote-assistant.pages.dev), which is a
separate product and untouched by the Glasshouse.

## Running it

```
python core/preflight.py        # is it safe to start?
python core/glasshouse.py       # the engine: intake + dispatch, one process
bash scripts/restart_engine.sh  # pick up a code change - see below
```

**Never kill the engine to reload it.** A session killed mid-flight dies before
it can call finish and everything it worked out is lost. `restart_engine.sh`
pauses it, lets the running sessions land, then swaps the process. And the
engine imports its modules once, so a charter or brief you edited is not live
until that restart finishes - three of 05/08's incidents were exactly that.

Everyone signs in on the hub with their own account. **admin** (Zac, Adam) sees
everything; **delivery** (Paul, Steve) sees only their job board, enforced
server-side.

Secrets: `.env.glasshouse` (hub URL, bot key, team PIN), `.env.mary` and
`.env.jacob` (Graph credentials). All gitignored, never committed.

Deploy the hub: `npx wrangler pages deploy public --project-name glasshouse`
**from inside `hub/`**. The tell that a deploy worked is the
"Uploading Functions bundle" line.

## Cost design

Sonnet by default, Opus only for tasks intake flags as pricing judgement,
Haiku on the door. Clerical mail never starts a session at all. Three
breakers (day budget, session kill, curfew) and no other throttles - the
rest is evidence in the seed. Target: the whole system inside ~118M context
tokens a day. The Cost tab on the hub is the meter.

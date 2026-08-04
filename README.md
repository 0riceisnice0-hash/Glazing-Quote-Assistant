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
call, and die. Read `personas/SYSTEM.md` for the whole architecture on a page.

## Layout

```
core/        the engine - intake, dispatch, finish, record client, breakers
personas/    SYSTEM.md + one charter per persona (their entire manual)
hub/         the Glasshouse hub - Cloudflare Pages + D1 (the record itself)
scripts/     craft tools that survived: Mary's checks engine, rate mining,
             Jacob's data pulls. Product code, not plumbing.
data/        supplier rates, calibration, mail attachments, local state
attic/       the old system, frozen: scripts, docs, dashboard. Reference only.
outputs/     deliverables (pricing workbooks, proposals)
```

The repo root also carries the original Glazing Quote Assistant web app
(`index.html`, `js/`, `css/` -> glazing-quote-assistant.pages.dev), which is a
separate product and untouched by the Glasshouse.

## Running it

```
python core/preflight.py     # is it safe to start?
python core/glasshouse.py    # the engine: intake + dispatch, one process
```

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

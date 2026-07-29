# HUB AUDIT - 29/07/2026

Zac's instruction: *"we started with Mary and added Jacob. everything is too merged and
stacked on top of each other. we need a fat audit. fix UX, make everything intuitive and
less chaotic. lay the foundation for future bots like a project manager."*

This file is the audit, the worklist, and the record of what was changed and why.

---

## 1. How the chaos happened

Jacob was added *alongside* Mary rather than *into* a structure that expected a second
bot. That was the right call at the time - "Mary's pages, data and logic are untouched" -
but it means every part of the system now exists twice, in slightly different shapes:

| Concept | Mary's version | Jacob's version | Same thing? |
|---|---|---|---|
| Board data | `DATA` via `/api/data` | `JACOB` via `/api/jacob` | yes |
| Pages | `PAGES` + `RENDER` | `JACOB_PAGES` + `JACOB_RENDER` | yes |
| Human chat | `messages` table, `/api/messages` | `jacob_messages`, `/api/jacob/messages` | yes |
| Chat renderer | `RENDER.messages()` (day separators, pending marks) | `JACOB_RENDER.jmessages()` (neither) | yes, diverged |
| Decisions | `requests[]` in **deployed static JSON**, answer round-trips through chat + a client-side `SENT_ANSWERS` patch | `jacob_requests` **D1 table**, answered live | yes, two different persistence models |
| Live feed | `RENDER.live()` + its own poll loop | `JACOB_RENDER.jlive()` + its own poll loop | yes, near-identical code |
| Status | bridge POSTs `/api/mary/status`, live pill | none - sidebar hard-codes **"In build"**, which is now false | yes |
| Bot-side routes | `mary/pending`, `mary/reply`, `mary/activity` | `jacob/pending`, `jacob/reply`, `jacob/ask`, `jacob/activity` | yes |
| Icons | `messages`, `live` | `jmessages`, `jlive` - byte-identical SVGs under new keys | yes |
| Poll loops | messages+status @10s, activity @3s | channels @10s, activity @3s | four separate `setInterval`s |

A third bot on this pattern means a third copy of all of it. That is the foundation
problem in one sentence.

## 2. UX findings

1. **No front door.** The hub lands on Mary's overview. Whether *Jacob* needs a decision
   is invisible until you switch boards; each bot's "needs you" badge only renders while
   that bot's board is active. Two boards means checking two places every time.
2. **Jacob's nav is 16 items** against Mary's 8, with near-essay "planned-note" blocks on
   every page. Reference pages (Jayk's book, How this works) sit visually equal to the
   two pages where money is won or lost (Chasing, Enquiries).
3. **Stale hard-coded state.** Jacob's sidebar card says "In build"; he has been running
   autonomously since 28/07. Trust in the board depends on it never lying.
4. **Inconsistent naming between boards.** "Mary needs you" vs "decisions" (labelled
   "Jacob needs you"), `messages` vs `jmessages`, `live` vs `jlive`, "Comms log" vs
   nothing. The internal bot-to-bot chat lives only under Jacob's board although it is a
   shared channel between both bots.
5. **Page-title collisions handled by fallback.** Both boards own `overview`; switching
   bots silently falls back when the key is missing from the other board.
6. **Mary's request answers don't survive a reload.** `SENT_ANSWERS` is in-memory; the
   card reverts to "waiting" on refresh until Mary redeploys the board. Jacob's model
   (D1) does not have this problem. (Documented, not fixed in this pass - it changes
   Mary's session workflow, not just the hub.)
7. The `title` element still says "Mary Grace - Fenster Estimating" for a two-bot hub.

## 3. What must NOT change (load-bearing)

- **Wire protocol.** Live bridges poll these every few seconds; each must keep answering
  byte-compatibly: `mary/pending`, `mary/reply`, `mary/status`, `mary/activity`,
  `jacob/pending`, `jacob/reply`, `jacob/ask`, `jacob/activity`, `botchat`,
  `botchat/pending`, `botchat/seen`, and the public `data`, `jacob`, `messages`,
  `status`, `activity`, `jacob-activity`, `outcomes`, `jacob/messages`,
  `jacob/requests`, `jacob/pipeline`.
- **D1 tables.** No renames, no migrations. Mary's legacy names (`messages`, `state`,
  `outcomes`) stay; the per-bot convention (`jacob_*`) applies from Jacob onward.
- **Guard invariants** (`scripts/mary_hub_guard.py`): x-mary-key gate present, no
  literal `route === "mary/..."` before it, `_headers` keeps noindex/no-store, all JS
  parses via `node --check` (so `app.js` stays a single classic script - no ESM split),
  data file present.
- **Every in-code comment documenting a past bug** (scroll preservation, drafts, UK
  times, `.opt` handler scoping, tbl-wrap, dvh...). These are regression tests written
  as prose; the refactor must carry the behaviour and the comment.

## 4. Target architecture (the foundation)

**One registry per layer; a new bot is one entry in each.**

- `app.js`: a `BOTS` registry - key, name, role, initials, accent, nav pages, render
  map, channel config. Sidebar cards, nav, polling, badges, chat and live pages all
  derive from it. Shared renderers (`chatPage`, `livePage`, stats/tables) replace the
  per-bot copies.
- API: a `CHANNELS` registry - bot key → {messages table, seen column, requests table,
  state keys}. Generic handlers serve `<bot>/messages|pending|reply|requests|ask|activity`;
  the historical route spellings are aliases onto the same handlers.
- `schema.sql`: convention `<bot>_messages`, `<bot>_requests` (+ optional
  `<bot>_pipeline`); Mary's unprefixed names are the documented exception.
- A **Team** board above both bots: every open decision from every bot, both status
  pills, urgent deadlines, top actions, and the internal chat. The default landing page.

**Adding a project-manager bot after this refactor:** one `BOTS` entry, one `CHANNELS`
entry, two `CREATE TABLE IF NOT EXISTS` statements, a `scripts/pm_dashboard.py` writing
`_data/pm-data.js`, its own `.env.pm` + Entra apps + scope group, and a bridge. Nothing
existing is edited beyond the registries.

## 5. Out of scope this pass (recommended next)

1. **Move Mary's requests to D1** so answers persist like Jacob's. Touches
   `MARY-JOB-SESSION.md` workflow and `mary_dashboard.py` - do it as its own change.
2. **A shared Python bot library** - `mary_graph.py`/`jacob_graph.py` and the two
   bridges are the same shape twice. Worth extracting before bot #3, not after.
3. **Jacob per-company memory** (BOTS.md already names this as his highest-value gap).
4. Re-enable the hub login before the URL travels.

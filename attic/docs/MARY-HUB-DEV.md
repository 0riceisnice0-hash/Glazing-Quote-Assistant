# BUILDING THE HUB YOURSELF

Zac's instruction, 27/07/2026: *"I want it to be able to code shit on the dashboard themselves - like if
Mary is like oh I need to display this information somehow, let me just make a new tab on the website,
and it does it."*

So do that. If you need somewhere to show something, build it. You do not need to ask.

---

## The whole loop

```bash
# 1. build it - a page is a render function plus an entry in PAGES
#    dashboard/public/app.js      the page itself
#    dashboard/public/styles.css  any new styling
#    dashboard/functions/api/[[path]].js  a new endpoint, if it needs one

# 2. prove it parses and nothing security-critical moved
python scripts\mary_hub_guard.py

# 3. see it with your own eyes before anyone else does
python scripts\mary_hub_shot.py scoreboard scratchpad\check.png

# 4. ship it
python scripts\mary_dashboard.py --deploy
```

Step 4 runs the guard again itself, so a broken deploy is refused rather than shipped.

## Adding a page - the pattern

Three edits in `dashboard/public/app.js`:

1. an SVG in `ICONS` keyed by your page name (or `icon: "existing-key"` on the
   nav entry to reuse one - the SVGs exist once each, never paste a copy);
2. an entry in the bot's pages array (`PAGES` for Mary, `JACOB_PAGES` for Jacob,
   `TEAM_PAGES` for the Team view) - `{ key, label, group, sub: () => "one line" }`;
3. a render function on that bot's render map (`RENDER` / `JACOB_RENDER` /
   `TEAM_RENDER`) with the same key, returning an HTML string.

Routing, the nav, search and the side panel all pick it up automatically. Data comes from `DATA`
(generated into `dashboard/functions/_data/dashboard-data.js` by `mary_dashboard.py`) or from a live
`/api/...` call. If it is data a human will change, put it behind an API route and fetch it live so it
updates without a redeploy; if it is data you curate at close-out, put it in `dashboard-state.json`.

Reuse what is there before inventing: `.stats`/`.stat` tiles, `.tbl` tables, `.mail-list`/`.mail-row`
rows, `.chip ok|warn|danger`, `.empty`, `fmt()` for anything you have written as text; `chatPage()`,
`livePage()` and `botchatPage()` for whole pages that already exist in shared form. A page that looks
like the rest of the hub is worth more than a clever one that does not.

## Adding a bot - the pattern (since the 29/07 restructure, see HUB-AUDIT.md)

The hub is registry-driven at every layer; a new bot (the project manager, say) edits
registries, not the shell:

1. **`dashboard/public/app.js`** - one entry in `BOTS`: name, role, initials, accent,
   its pages array + render map, and its `chat` config. The sidebar card, nav,
   routing, badges, polling and Team view all follow from it.
2. **`dashboard/functions/api/[[path]].js`** - one entry in `CHANNELS`: table names
   and state keys. Every route (`<bot>/messages|pending|reply|requests|ask|status|
   activity|pipeline`) then just works; the handlers are generic.
3. **`dashboard/schema.sql`** - `CREATE TABLE IF NOT EXISTS <bot>_messages` and
   `<bot>_requests` (copy Jacob's shape; the `<bot>_` prefix is the convention,
   Mary's unprefixed names are the grandfathered exception). Apply to production
   with `wrangler d1 execute` - the file is all IF NOT EXISTS, so it is additive.
4. **A generator** writing `dashboard/functions/_data/<bot>-data.js`, imported at the
   top of the API file and named in its bot's `CHANNELS.board`.
5. **Its own credentials** - `.env.<bot>`, two Entra apps, a scope group, transport
   rule - and a bridge. Never share Graph secrets between bots; only the hub key
   (`MARY_API_KEY`) is shared infrastructure.

The old route spellings (`/api/data`, `/api/messages`, `/api/status`, `/api/activity`,
`/api/jacob-activity`) are aliases in the API's `ALIASES` map. They are load-bearing -
live bridges poll them - so they stay forever. Add nothing new to that map: new bots
use the generic spellings from day one.

## The five things you must never break

`scripts/mary_hub_guard.py` enforces these and blocks the deploy if any give way:

1. **The `x-mary-key` gate.** Every `mary/*` route must sit *below* it. Above it, they are public.
2. **No secrets in the bundle.** Keys live in `.env.mary` and Cloudflare secrets. Never in a file.
3. **`_headers` keeps `noindex` and `no-store`.** noindex keeps the hub out of search; no-store is
   there because browser caching once masked three consecutive deploys.
4. **Everything parses.** A syntax error takes the whole hub down, not just your page.
5. **The data file exists.** A hub that renders empty is a regression even if the code is perfect.

If the guard stops you, fix the cause. Do not route around it.

## Look at it before you ship it

`mary-dashboard.pages.dev` is blocked in the Browser pane, so use headless Chrome over CDP -
`scripts/mary_hub_shot.py` wraps it. Read the PNG back and actually look. Two real bugs got shipped
because the code was correct and the page was not: Mary's own text rendered navy-on-navy and was
invisible, and the Won/Lost buttons were being swallowed by another click handler.

## Rolling back

Every deploy is a separate immutable Cloudflare deployment. To see them and go back:

```bash
npx.cmd wrangler pages deployment list --project-name mary-dashboard
npx.cmd wrangler pages deployment tail --project-name mary-dashboard
```

Redeploying the previous commit is usually faster: `git revert`, then `mary_dashboard.py --deploy`.

## What still needs a human

Turning the login back on, changing what `AUTH_DISABLED` does, anything touching who can reach the hub,
and anything that would put a client's name in front of someone outside Fenster. Those are Zac's calls -
raise a request on the hub instead.

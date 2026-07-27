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

1. an SVG in `ICONS` keyed by your page name;
2. an entry in `PAGES` - `{ key, label, sub: () => "one line of context" }`;
3. a render function on `RENDER` with the same key, returning an HTML string.

Routing, the nav, search and the side panel all pick it up automatically. Data comes from `DATA`
(generated into `dashboard/functions/_data/dashboard-data.js` by `mary_dashboard.py`) or from a live
`/api/...` call. If it is data a human will change, put it behind an API route and fetch it live so it
updates without a redeploy; if it is data you curate at close-out, put it in `dashboard-state.json`.

Reuse what is there before inventing: `.stats`/`.stat` tiles, `.tbl` tables, `.mail-list`/`.mail-row`
rows, `.chip ok|warn|danger`, `.empty`, `fmt()` for anything you have written as text. A page that looks
like the rest of the hub is worth more than a clever one that does not.

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

# The attic

The system that ran Fenster's bots from 24/07/2026 to 04/08/2026, frozen the
day the Glasshouse replaced it. Nothing in here runs; nothing in here is
maintained. It is kept because the docs record real operating knowledge (the
false-facts list in `docs/BOTS.md` §5, the traps in `docs/AI.md`) and because
"why did the old system do X" is a question worth being able to answer.

Do not import from `attic/scripts/`. Do not follow `docs/` as instructions -
the charters in `personas/` superseded them, and where they disagree the
charter wins. The old hub (mary-dashboard.pages.dev) and its D1 database
still exist in Cloudflare but receive no writes; the record was migrated to
glasshouse-db on 04/08/2026 by `core/migrate.py`.

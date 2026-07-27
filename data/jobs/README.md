# Per-job memory files

One file per job chat, named after its key in `data/mary-jobs.json` (e.g. `vesuvius.md`).

Each chat keeps its own file current: scope, the live number and what backs it, who owes what, the
deadline, open RFIs, decisions taken and why. The chat itself is the working memory - this file is the
durable backup. If a chat ever has to be reset (context bloat, a lost session), the new one starts from
this file, so it should always be good enough to rebuild the position from cold.

Written by sessions, not by hand. See `MARY-JOB-SESSION.md` section 4.

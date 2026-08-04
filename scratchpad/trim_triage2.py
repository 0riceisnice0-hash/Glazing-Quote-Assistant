# -*- coding: utf-8 -*-
"""Archive the closed Jacob-uptime entry, compress it, then add the Stepnell entry."""
p = "data/jobs/triage.md"
d = open(p, encoding="utf-8").read()
lines = d.split("\n")

start, end = 187, 201          # 0-indexed slice = lines 188..201
block = "\n".join(lines[start:end])
assert block.lstrip().startswith("- **29/07 - JACOB'S UPTIME"), block[:120]
assert "survives a" in block or "session" in block, block[-200:]

with open("data/jobs/triage-archive-2026-07.md", "a", encoding="utf-8") as fh:
    fh.write("\n\n### Moved out of the live triage file 30/07/2026 - Jacob's uptime, four gates, in full\n\n"
             + block + "\n")

COMPRESSED = """- **29/07 - JACOB'S UPTIME WAS FOUR GATES, NOT ONE (Zac, dashmsg-95; full account in
  `data/jobs/triage-archive-2026-07.md`).** His own bridge, not an API limit: budget 4.0h spent by
  20:14, plus a 07:00-21:00 curfew, a 4-hour cadence and a leftover yield to Mary's session lock. All
  four fixed, budget 12.0h. **The durable lessons: `fails` = 0 and a clean exit is how you tell OUR
  limit from THEIRS, and a constant is read at import - so the fix is the RESTART, not the edit.**"""

lines[start:end] = COMPRESSED.split("\n")
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("live file now %d lines" % len("\n".join(lines).split("\n")))

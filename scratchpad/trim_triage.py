# -*- coding: utf-8 -*-
"""Archive the two RSR DRH1 entries in full, then compress them in the live file."""
p = "data/jobs/triage.md"
d = open(p, encoding="utf-8").read()
lines = d.split("\n")

start, end = 165, 198          # 0-indexed slice = lines 166..198
block = "\n".join(lines[start:end])
assert block.lstrip().startswith("- **29/07 - RSR DRH1"), block[:120]
assert "RRR Group / RSR name collision" in block, block[-200:]

with open("data/jobs/triage-archive-2026-07.md", "a", encoding="utf-8") as fh:
    fh.write("\n\n### Moved out of the live triage file 30/07/2026 - the two RSR DRH1 entries in full\n\n"
             + block + "\n")

COMPRESSED = """- **29/07 - RSR DRH1 (Amazon, Crawley): THE GBP 750 IS UNDER COST AND STILL UNCONFIRMED (botmsg-22
  and -24, both answered; full account in `data/jobs/triage-archive-2026-07.md`).** RSR are not dormant -
  Harri Birt has been waiting on us since 09/10/2025 with Amazon's sign-off, unable to issue her own
  quotation until we confirm. **GBP 750 + VAT was priced off a single 556 x 876 pane; the article is a
  bonded CORNER (556 x 556 x 876) and Johnson & Sons' buy for it is GBP 960 + VAT, so confirming GBP 750
  sells at a loss of at least GBP 210.** Nobody confirms it; it needs re-quoting off the GBP 960. The
  "who fits one window 130 miles away" blocker was answered nine months ago - Johnson & Sons priced it.
  Not emailed: Adam set the corner spec himself and received the GBP 960, so none of it is news to him.
  Durable facts from it: **jayk@ is a hard 404**, so a forward into it is never a clean negative; Harry
  Grover left Fenster 31/10/2025; bot_chat clips at 4,000 characters; RRR Group / RSR name collision."""

lines[start:end] = COMPRESSED.split("\n")
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("live file now %d lines" % len("\n".join(lines).split("\n")))

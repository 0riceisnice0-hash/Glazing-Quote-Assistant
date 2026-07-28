# -*- coding: utf-8 -*-
"""Append the 28/07 rule to AI.md's narrative, above '## Development Rules For Future Agents'."""
import io

RULE = u"""
**When somebody answers a client's scope question by email, the thing to check is not whether the answer is
right - it is whether the document we issued says the same thing.** Guildmore asked whether removal of the
existing windows was allowed for. Adam answered: strip out of old frames yes, disposal and skips no. **Half
of that was already in the proposal word for word** - *"Waste Removal - Generally excluded unless agreed
otherwise"*, page 4 - **and the other half appears in nothing we issued**: no strip-out inclusion on any of
the proposal's ten pages, no strip-out line in the pricing workbook, and an installation sum that recomputes
from the labour codes alone. A GBP 279,244.69 quotation is now silent on a scope item we have committed to in
a thread.

    the answer that matches the document   -> nothing to do
    the answer that is only in the thread  -> a variation nobody has priced

**Sweep the issued PDF, not the job record.** The job record says what we meant to include; only the document
says what the client can hold us to. One pass for *strip / remove / removal / disposal / skip / waste /
make good* settles it, and the same shape works for any answer given after issue - access, making good,
disposal, temporary protection, out-of-hours.

**And check whether we could even have priced it.** There is no strip-out rate in `data/supplier-rates.json`;
it is one of the 21 categories that return zero. **An email answer costs nothing to give and can commit
scope we hold no rate for** - which is the same asymmetry as the register's frames-and-glass depth, arriving
from the commercial side instead of the estimating side.

"""

P = "AI.md"
txt = io.open(P, encoding="utf-8").read()
anchor = u"\n## Development Rules For Future Agents"
assert txt.count(anchor) == 1, "anchor not unique"
txt = txt.replace(anchor, RULE + anchor)
io.open(P, "w", encoding="utf-8", newline="\n").write(txt)
print("AI.md rule appended")

# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE STITCHED-QUOTATION SWEEP - AND MINE NARROWED A SUPPLIER'S DISCLAIMER (28/07)"

SEC = u"""### READING ONE SENTENCE PAST MY OWN QUOTATION FOUND A STANDARD NOBODY HAS EVER MENTIONED (28/07)

Gordon Court applied the stitch check to **ellipses** - *"an ellipsis is a connective that admits it
skipped something without saying how much"* - and then to closing quotation marks, and found an Approved
Document K requirement sitting in the sentence their quotation stopped one short of:

> *"Note: Any part of the ventilator opening within 1.1m of floor level will require guarding for
> compliance with Approved Document K."*

**Attached to the unit they were asking BSW to price, neither priced nor quoted nor asked.** Their check:

> **"Find every ellipsis and every closing quotation mark in an outgoing letter, open the source, and
> read the next two sentences. Not the quotation - what comes after it."**

**Run here. Zero ellipses in either letter** - that half is clean and it is worth saying so. **Ten
quotations of A Plus's text, each followed to what comes next.** Eight are unrelated bullets. **One is
benign and worth reporting as benign. One is a live requirement nobody on this job has ever named.**

### THE FINDING: "ALL RESIDENTIAL WINDOWS TO HAVE A MINIMUM WINDOW ENERGY RATING OF C" (28/07)

RFQ item 4 quotes A Plus's *"windows and doors will have a U - Value no better than 1.8"*. **The sentence
after the next one reads:**

    "All residential windows to have a minimum window energy rating of C."

**Riverside House is a residential conversion.** Checked precisely rather than by substring - `\\bWER\\b`
and the phrase *window energy rating* - and **both are absent from every output, the job file and the
manifest.** Thirty-plus turns on thermal performance, an entire exposure entry on the 1.6 W/m2K U-value,
and **WER has never been mentioned once.**

**It is not the same question as the U-value.** WER is a banded rating combining thermal transmittance,
solar gain and air leakage; **a unit can meet a U-value target and miss a band, and vice versa.** So the
two answers do not travel together, and item 4 asked for only one of them.

**Both letters now ask.** RFQ item 4 asks A Plus to state the WER band alongside the Uw, with the reason
- *"we are not assuming the two answers travel together"*. RRR question 7, which asks whether the 1.6
binds these vents at all, now asks the same of a WER requirement: **does the design team hold one, and
does it reach the stair vents?**

**And the honest note on scale: this is a question, not a defect.** Nothing says WER band C is required
of a stair smoke vent - A Plus's line says *residential windows*, and whether an AOV in a common stairwell
counts is exactly the sort of thing the design team answers. **But it was invisible until somebody read
one sentence further than the quotation, which is the whole of Gordon Court's point.**

### The one that is benign, reported as benign (28/07)

RRR question 8 says *"A Plus exclude it and so do we"* about Part K anti-fall protection. The sentence
after their Part K note reads *"The provision and installation of balustrading and the like is excluded
from our quotation."*

**So the exclusion is real and my letter has its substance** - but the source excludes *"balustrading and
the like"*, which is the **means** rather than the requirement. **Under the second step: does a reader do
anything different? No.** The question asked of RRR is who carries it either way. **Left alone and
recorded as benign** - Gordon Court's point that reporting the benign one is what stops a check becoming
a machine for generating findings.

### And their AD K finding is my own Part K finding arriving backwards (28/07)

They noticed it themselves and it is worth recording from this side. **On Riverside, Part K anti-fall was
excluded by A Plus, excluded by us, and asked of neither** - the *"hole with two signatures on it"*, found
by diffing two exclusion lists. **On Gordon Court the same regulation is written into the specification
clause for the unit, and a closing quotation mark removed it.**

**Same regulation, same silence, two entirely different mechanisms** - one a gap between documents, one a
gap inside a sentence. **Neither check would have found the other's.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

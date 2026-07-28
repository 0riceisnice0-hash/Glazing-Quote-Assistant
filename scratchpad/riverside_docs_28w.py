# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("A PLUS REQUIRE A MINIMUM WINDOW ENERGY RATING OF C ON RESIDENTIAL WINDOWS, AND NOBODY ON THIS "
     "JOB HAS EVER MENTIONED IT. Gordon Court applied the stitch check to ellipses and closing "
     "quotation marks and found an Approved Document K requirement in the sentence their quotation "
     "stopped one short of - attached to the unit they were asking BSW to price. Their check: find "
     "every ellipsis and every closing quotation mark in an outgoing letter, open the source, and "
     "read the next two sentences. Run here: ZERO ellipses in either letter, and ten quotations of A "
     "Plus's text followed to what comes next - eight unrelated, one benign, ONE LIVE. RFQ item 4 "
     "quotes 'windows and doors will have a U - Value no better than 1.8'; two sentences later the "
     "quotation reads 'All residential windows to have a minimum window energy rating of C.' "
     "Riverside House is a residential conversion. Checked precisely on \\bWER\\b and the full "
     "phrase rather than by substring - because 'wer' matches lower, answer and however, which is "
     "how a first count came back at 91 - and BOTH ARE ABSENT FROM EVERY OUTPUT, THE JOB FILE AND "
     "THE MANIFEST. Thirty turns on thermal performance, a whole exposure entry on the 1.6 W/m2K "
     "U-value, and WER has never appeared once. AND IT IS NOT THE SAME QUESTION: a WER band combines "
     "thermal transmittance, solar gain and air leakage, so a unit can meet a U-value target and "
     "miss a band.  ->  BOTH LETTERS NOW ASK. RFQ item 4 asks A Plus to state the band alongside the "
     "Uw, with the reason - 'we are not assuming the two answers travel together'. RRR question 7 "
     "asks whether the design team holds a WER requirement and whether it reaches the stair vents. "
     "HONEST SCALE: this is a question, not a defect - A Plus say 'residential windows' and whether "
     "an AOV in a common stairwell counts is exactly what the design team answers.",
     "excluded"),

    ("AND ONE THAT IS BENIGN, REPORTED AS BENIGN. RRR question 8 says 'A Plus exclude it and so do "
     "we' about Part K anti-fall protection. The sentence after their Part K note reads 'The "
     "provision and installation of balustrading and the like is excluded from our quotation.' The "
     "exclusion is real and the letter carries its substance; the source excludes the MEANS rather "
     "than the requirement, and under the second step a reader does nothing different.  ->  LEFT "
     "ALONE AND RECORDED AS BENIGN. Gordon Court reported one of three benign in the same turn: "
     "reporting the benign one is what stops a check becoming a machine for generating findings.",
     "excluded"),

    ("GORDON COURT'S APPROVED DOCUMENT K FINDING IS THIS JOB'S PART K FINDING ARRIVING BACKWARDS, AND "
     "THE MECHANISMS HAVE NOTHING IN COMMON. On Riverside, Part K anti-fall protection was excluded "
     "by A Plus, excluded by us, and asked of neither - the 'hole with two signatures on it', found "
     "by DIFFING TWO EXCLUSION LISTS ACROSS TWO DOCUMENTS. On Gordon Court the same regulation is "
     "written into the specification clause for the unit itself - 'Any part of the ventilator "
     "opening within 1.1m of floor level will require guarding for compliance with Approved Document "
     "K' - and a CLOSING QUOTATION MARK removed it: a gap INSIDE one sentence.  ->  Same regulation, "
     "same silence, two mechanisms with nothing in common. A document-diff cannot see inside a "
     "quotation; a quotation check cannot see across two exclusion schedules. NEITHER CHECK COULD "
     "EVER HAVE FOUND THE OTHER'S, which is an argument for running both rather than treating one as "
     "the mature version of the other.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - READING ONE SENTENCE PAST MY OWN QUOTATION FOUND A STANDARD NOBODY ON THIS "
    "JOB HAS EVER MENTIONED. *** Gordon Court applied the stitch check to ellipses and closing "
    "quotation marks and found an Approved Document K requirement in the sentence their quotation "
    "stopped one short of, on the unit they were asking BSW to price. Their check: find every "
    "ellipsis and every closing quotation mark, open the source, and read the next two sentences - "
    "not the quotation, what comes after it. RUN HERE: ZERO ELLIPSES in either letter, and ten "
    "quotations of A Plus's text followed to what comes next - eight unrelated, one benign, ONE "
    "LIVE. RFQ item 4 quotes 'a U - Value no better than 1.8'; two sentences later the quotation "
    "reads 'ALL RESIDENTIAL WINDOWS TO HAVE A MINIMUM WINDOW ENERGY RATING OF C'. Riverside House is "
    "a residential conversion, and WER is absent from every output, the job file and the manifest - "
    "checked on a word boundary and the full phrase rather than by substring, because 'wer' matches "
    "lower, answer and however. Thirty turns on thermal performance, an entire exposure entry on the "
    "1.6 W/m2K U-value, and WER had never appeared once. AND IT IS NOT THE SAME QUESTION - a WER "
    "band combines transmittance, solar gain and air leakage, so a unit can meet a U-value and miss "
    "a band. Both letters now ask: A Plus for the band alongside the Uw, RRR whether the design team "
    "holds a WER requirement and whether it reaches the stair vents. HONEST SCALE: a question, not a "
    "defect - whether an AOV in a common stairwell counts as a residential window is exactly what "
    "the design team answers. AND ONE BENIGN, REPORTED AS BENIGN: the sentence after A Plus's Part K "
    "note excludes 'balustrading and the like', which is the means rather than the requirement, so a "
    "reader does nothing different and it is left alone. AND THEIR AD K IS THIS JOB'S PART K "
    "ARRIVING BACKWARDS - here it was excluded by both parties and asked of neither, found by "
    "diffing two exclusion lists across two documents; there it is written into the unit's own "
    "specification clause and a closing quotation mark removed it. Same regulation, same silence, "
    "two mechanisms with nothing in common, and neither check could have found the other's. Checks "
    "0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
)
hit = 0
for j in h.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(h, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**Find every ellipsis and every closing quotation mark in an outgoing letter, open the source, and read
the next two sentences - not the quotation, what comes after it.** Gordon Court's quotation of a Coltite
specification stopped one sentence short of *"Note: Any part of the ventilator opening within 1.1m of
floor level will require guarding for compliance with Approved Document K"* - **a building regulation
attached to the unit they were asking the supplier to price, neither priced nor quoted nor asked.** An
**ellipsis is a connective that admits it skipped something without saying how much**; a closing quotation
mark does not even admit that.

Run on Riverside: zero ellipses, ten quotations followed through, **one live finding** - RFQ item 4 quoted
A Plus's *"a U - Value no better than 1.8"* and stopped two sentences before **"All residential windows to
have a minimum window energy rating of C."** Riverside House is a residential conversion and **WER appears
nowhere in any output, job file or manifest** after thirty turns of work on thermal performance. **A WER
band is not a U-value** - it combines transmittance, solar gain and air leakage, so a unit can meet one
target and miss the other. Both letters now ask for it.

**Check word-boundary, not substring, before reporting an absence as an absence.** A first count of
*"wer"* across the Riverside documents returned 91 - all of them *lower*, *answer* and *however*. `\\bWER\\b`
and the full phrase both return zero.

**The same regulation can hide in two places no single check reaches.** Riverside's Part K anti-fall gap
was found by **diffing two exclusion schedules across two documents** - excluded by supplier, excluded by
us, asked of neither. Gordon Court's Approved Document K gap was **inside one sentence**, removed by a
closing quotation mark. **A document-diff cannot see inside a quotation; a quotation check cannot see
across two exclusion schedules. Neither could have found the other's** - so run both rather than treating
one as the mature version of the other.

**Report the benign result.** Riverside's Part K quotation is followed by *"The provision and installation
of balustrading and the like is excluded from our quotation"* - the source excludes the **means** rather
than the requirement, and under the second step a reader does nothing different, so it was left alone.
Gordon Court reported one of three benign in the same turn. **Reporting the benign one is what stops a
check becoming a machine for generating findings.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - reading ONE SENTENCE past my own quotation found a standard nobody on this job"
    u" has ever mentioned.** Gordon Court applied the stitch check to **ellipses and closing quotation"
    u" marks** and found an **Approved Document K** requirement in the sentence their quotation"
    u" stopped one short of, on the unit they were asking BSW to price. **Run here: ZERO ellipses**, and"
    u" ten quotations of A Plus's text followed to what comes next - eight unrelated, one benign, **one"
    u" live**. RFQ item 4 quotes *\"a U - Value no better than 1.8\"*; **two sentences later: \"ALL"
    u" RESIDENTIAL WINDOWS TO HAVE A MINIMUM WINDOW ENERGY RATING OF C\"**. Riverside House is a"
    u" residential conversion, and **WER is absent from every output, the job file and the manifest** -"
    u" checked on a word boundary, because `wer` matches *lower*, *answer* and *however* and a first"
    u" count came back at 91. **Thirty turns on thermal performance, an entire exposure entry on the"
    u" 1.6 W/m2K U-value, and WER had never appeared once** - and **it is not the same question**, since"
    u" a band combines transmittance, solar gain and air leakage. **Both letters now ask.** **Honest"
    u" scale: a question, not a defect** - whether an AOV in a common stairwell counts as a residential"
    u" window is what the design team answers. **One benign, reported as benign:** the sentence after"
    u" their Part K note excludes *balustrading and the like*, the means rather than the requirement."
    u" **And their AD K is this job's Part K arriving backwards** - here excluded by both parties and"
    u" asked of neither, found by **diffing two exclusion lists**; there written into the unit's own"
    u" clause and removed by **a closing quotation mark**. **Same regulation, two mechanisms with"
    u" nothing in common, and neither check could have found the other's.** Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, one sentence past the quotation

Gordon Court applied the stitch check to **ellipses** - *"an ellipsis is a connective that admits it
skipped something without saying how much"* - and then to closing quotation marks, and found an **Approved
Document K requirement in the sentence their quotation stopped one short of**: *"Any part of the
ventilator opening within 1.1m of floor level will require guarding for compliance with Approved Document
K"*, attached to the unit they were asking BSW to price, neither priced nor quoted nor asked. Their check:
**find every ellipsis and every closing quotation mark, open the source, and read the next two sentences -
not the quotation, what comes after it.**

**Run here: zero ellipses in either letter**, and ten quotations of A Plus's text followed through. Eight
unrelated, one benign, **one live**.

**RFQ item 4 quotes A Plus's *"windows and doors will have a U - Value no better than 1.8"*. Two sentences
later the quotation reads: *"All residential windows to have a minimum window energy rating of C."***

**Riverside House is a residential conversion.** Checked precisely on `\\bWER\\b` and the full phrase
rather than by substring - a first count of *"wer"* returned 91, all of them *lower*, *answer* and
*however* - and **both are absent from every output, the job file and the manifest.** Thirty turns of work
on thermal performance, an entire exposure entry on the 1.6 W/m2K U-value, and **WER had never appeared
once.**

**And it is not the same question as the U-value.** A WER band combines thermal transmittance, solar gain
and air leakage, so **a unit can meet a U-value target and miss a band**. The two answers do not travel
together and item 4 asked for only one of them. Both letters now ask - A Plus for the band alongside the
Uw, RRR whether the design team holds a WER requirement and whether it reaches the stair vents.

**Honest scale: this is a question, not a defect.** A Plus's line says *residential windows*, and whether
an AOV in a common stairwell counts is exactly what the design team answers. **It was simply invisible
until somebody read one sentence further than the quotation.**

**And one that is benign, reported as benign.** RRR question 8 says *"A Plus exclude it and so do we"*
about Part K anti-fall; the sentence after their Part K note reads *"The provision and installation of
balustrading and the like is excluded from our quotation."* The exclusion is real and the letter carries
its substance - the source excludes the **means** rather than the requirement, and under the second step a
reader does nothing different. **Left alone.** Gordon Court reported one of three benign in the same turn:
*reporting the benign one is what stops a check becoming a machine for generating findings.*

**And their Approved Document K finding is this job's Part K finding arriving backwards.** On Riverside,
Part K anti-fall protection was excluded by A Plus, excluded by us and asked of neither - the *"hole with
two signatures on it"*, found by **diffing two exclusion schedules across two documents**. On Gordon Court
the same regulation is written into the specification clause for the unit itself, and **a closing
quotation mark removed it** - a gap **inside one sentence**. **Same regulation, same silence, two
mechanisms with nothing in common.** A document-diff cannot see inside a quotation; a quotation check
cannot see across two exclusion schedules. **Neither check could ever have found the other's** - an
argument for running both rather than treating one as the mature version of the other.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

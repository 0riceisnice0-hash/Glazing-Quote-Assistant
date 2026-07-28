# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("MY CONNECTIVE NARROWED A PLUS'S DISCLAIMER - THE MIRROR OF GORDON COURT'S STITCH. They applied "
     "the second step to quotations rather than verbs: a strong verb wrapping two fragments joined "
     "by a connective of your own. Theirs found NBS clause 205, where a single 'with' stitched "
     "sub-clauses 2 and 2.1 and dropped 1 and 2.2 - the submission and the deadline - so 'Timing: "
     "Before completion of detailed design' never reached their letter. Run here: seven sentences in "
     "the two letters contain two quoted fragments, five benign, TWO REAL. The RFQ said the Supplier "
     "'does not warrant or represent that any Product supplied shall comply with' THE BUILDING "
     "REGULATIONS 'unless where expressly stated to the contrary', where the source reads '...all "
     "building regulations..., LIFE TIME HOMES, SECURED BY DESIGN, PAS 24 (formally BS 7950) are "
     "adhered to. The Supplier does not warrant or represent that any Product supplied shall comply "
     "with ANY OF THE AFOREMENTIONED STANDARDS...'. MY CONNECTIVE REPLACED 'any of the aforementioned "
     "standards' WITH 'the Building Regulations' - and the disclaimer also covers Secured by Design "
     "and PAS 24, live categories on a residential conversion.  ->  AND IT IS A SECOND DIRECTION "
     "RATHER THAN A SECOND INSTANCE: theirs dropped an OBLIGATION ON THE SUPPLIER that we were owed; "
     "mine dropped BREADTH FROM A DISCLAIMER AGAINST US that the supplier holds. Theirs cost us "
     "something we were owed; mine understated something we are exposed to - and under-stating your "
     "own exposure reads as modest rather than sloppy, which is why it is the quieter of the two. "
     "Rewritten to quote the clause in full with the reason stated, plus a line noting the wider "
     "scope. The free-area quotation tidied in the same pass: '1.30m2. BASED ON A 50mm REVEAL' where "
     "the source reads '1.30m2 Based on a 50mm reveal' - a full stop and capitals added, trivial, "
     "and a quotation should be exact.",
     "excluded"),

    ("THE TELL, WHICH GENERALISES BETTER THAN THE FAULT: A PREPOSITION DOING SEMANTIC WORK BETWEEN "
     "QUOTATION MARKS. In 'comply with' the Building Regulations 'unless...', the word 'with' sits "
     "inside the first quotation and everything from there to the second quotation is mine - the one "
     "position where a reader will take it for the source's. THE RULE: if you have joined two quoted "
     "fragments with a word of your own, read the sub-clauses between and after them, AND CHECK WHAT "
     "YOUR CONNECTIVE REPLACED. A connective does not only join; it stands in for whatever it "
     "skipped, and nobody reading the letter can see what that was.  ->  RECORDED, and offered back "
     "to Gordon Court as a grep - '\" [a-z ]{1,40} \"' across their three letters will thin their 24 "
     "hits fast and what remains is exactly this shape.",
     "excluded"),

    ("GORDON COURT'S 'CANNOT WITHDRAW' IS THE THIRD INVENTED-CERTAINTY IN THREE TURNS AND THE ONE "
     "THIS CHAT CANNOT AUDIT. Their check_quote_validity_against_commitment printed 'GBP 201,304.36 "
     "of cost unfixed against a price WE CANNOT WITHDRAW' seventeen times. jLiving's Form of Tender "
     "says only that the tender 'remains open for consideration for a period of 180 days' - zero "
     "instances of withdraw, revoke, irrevocable, binding, cannot or may not in 993 characters - and "
     "Fenster's own 30-day validity pulls the other way, so the rule settled as fact a question two "
     "of our own documents disagree about. IT IS WORSE THAN THE 'lapse' CASE IN TWO WAYS: it is a "
     "LEGAL claim rather than a vocabulary choice ('remains open' is what an offeror does, not what "
     "an offeror is prevented from undoing), and it is attached to the LARGEST NUMBER ON THAT JOB, "
     "so the certainty and the figure travel together and anybody quoting the number inherits the "
     "claim.  ->  THIRD INSTANCE IN THREE TURNS, EACH A LEVEL FURTHER IN: a letter, a job file, now "
     "the tool the letters quote. That rule has run on the Riverside manifest since its fixture was "
     "written, SO THIS CHAT HAS BEEN READING 'cannot withdraw' AS OFTEN AS THEY HAVE, about a "
     "document it does not hold and could not have checked. The defence proposed back to them: put "
     "the source sentence in the rule's docstring, so a rule can be audited by any chat that runs "
     "it - including the ones that cannot open the document.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - MY CONNECTIVE NARROWED A PLUS'S DISCLAIMER, WHICH IS THE MIRROR OF GORDON "
    "COURT'S STITCH RATHER THAN A REPEAT OF IT. *** They applied the second step to quotations "
    "rather than verbs - a strong verb wrapping two fragments joined by a connective of your own - "
    "and found NBS clause 205, where one 'with' stitched sub-clauses 2 and 2.1 and dropped the "
    "submission and the deadline. Run here: seven sentences with two quoted fragments, five benign, "
    "two real. The RFQ said the Supplier 'does not warrant or represent that any Product supplied "
    "shall comply with' THE BUILDING REGULATIONS 'unless where expressly stated to the contrary' - "
    "where the source says 'with ANY OF THE AFOREMENTIONED STANDARDS', those standards being the "
    "building regulations PLUS LIFE TIME HOMES, SECURED BY DESIGN and PAS 24. My connective narrowed "
    "the disclaimer, and Secured by Design and PAS 24 are live categories on a residential "
    "conversion. AND IT IS A SECOND DIRECTION RATHER THAN A SECOND INSTANCE: theirs dropped an "
    "obligation on the supplier that we were owed; mine dropped breadth from a disclaimer against "
    "us that the supplier holds - understating your own exposure reads as modest rather than sloppy, "
    "which is why it is the quieter of the two. THE TELL GENERALISES BETTER THAN THE FAULT: a "
    "preposition doing semantic work between quotation marks - 'comply with' sits inside the first "
    "quotation and everything to the second is mine, in the one position a reader takes for the "
    "source's. Clause now quoted in full; the free-area quotation made exact. AND THEIR TOOLKIT "
    "SWEEP WENT ONE LEVEL FURTHER IN THAN MINE: check_quote_validity_against_commitment printed 'a "
    "price WE CANNOT WITHDRAW' seventeen times, where jLiving's Form of Tender says only that the "
    "tender 'remains open for consideration for a period of 180 days' - zero instances of withdraw, "
    "revoke, irrevocable or binding in 993 characters, and our own 30-day validity pulls the other "
    "way. THIRD INVENTED CERTAINTY IN THREE TURNS, EACH A LEVEL FURTHER IN - a letter, a job file, "
    "now the tool the letters quote - and this chat has been reading it as often as they have, about "
    "a document it does not hold. Checks 0 failed, 4 questions. Position unchanged: GBP 5,990.22, "
    "unissued, nothing sent."
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
RULE = u"""**If you have joined two quoted fragments with a word of your own, read the sub-clauses between and after
them - and check what your connective replaced.** A connective does not only join; **it stands in for
whatever it skipped, and nobody reading the letter can see what that was.** Gordon Court's `with` stitched
NBS clause 205's sub-clauses 2 and 2.1 and dropped 1 and 2.2 - a submission and *"Timing: Before
completion of detailed design"*, a deadline the supplier owed them that never reached the letter.
Riverside's `the Building Regulations` stood in for *"any of the aforementioned standards"*, which also
cover **Life Time Homes, Secured by Design and PAS 24**.

**And the two run in opposite directions, so both are worth looking for.** A stitch can **drop an
obligation on the other party that you were owed** (Gordon Court) or **drop breadth from a disclaimer
against you that they hold** (Riverside). The second is quieter, because **understating your own exposure
reads as modest rather than sloppy.**

**The tell generalises better than the fault: a preposition doing semantic work between quotation
marks.** In *"comply with" the Building Regulations "unless..."*, `with` sits inside the first quotation
and everything from there to the second is yours - **the one position where a reader will take it for the
source's.** Grep for `" [a-z ]{1,40} "` across any outgoing letter; the hits thin fast and what remains is
this shape. **Where the passage is load-bearing, quote the clause in full and say why** - *"quoted in full
so that we are not stitching fragments of it together"*.

**A shared rule's assertion is inherited by chats that cannot audit it.**
`check_quote_validity_against_commitment` printed *"a price we cannot withdraw"* seventeen times across
thirteen manifests; jLiving's Form of Tender says only that the tender *"remains open for consideration
for a period of 180 days"* - **zero instances of withdraw, revoke, irrevocable or binding in 993
characters** - while Fenster's own 30-day validity pulls the other way. **The rule settled as fact a
question two of our own documents disagree about, and attached it to the largest number on the job, so the
certainty and the figure travelled together.** Riverside had been reading it on every run, about a
document it does not hold and could never have checked. **Put the source sentence in the rule's docstring:
a rule whose docstring quotes what it asserts can be audited by any chat that runs it, including the ones
that cannot open the document.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - my connective NARROWED A Plus's disclaimer, the mirror of Gordon Court's stitch"
    u" rather than a repeat of it.** They applied the second step to quotations rather than verbs and"
    u" found NBS clause 205, where one `with` stitched sub-clauses 2 and 2.1 and **dropped the"
    u" submission and the deadline**. Run here: seven sentences with two quoted fragments, five"
    u" benign, **two real**. The RFQ said the Supplier *\"does not warrant or represent that any Product"
    u" supplied shall comply with\"* **the Building Regulations** *\"unless where expressly stated...\"* -"
    u" **the source says *\"with ANY OF THE AFOREMENTIONED STANDARDS\"***, being the building regulations"
    u" **plus Life Time Homes, Secured by Design and PAS 24**, live categories on a residential"
    u" conversion. **A SECOND DIRECTION, NOT A SECOND INSTANCE:** theirs dropped an **obligation on the"
    u" supplier we were owed**; mine dropped **breadth from a disclaimer against us** - and"
    u" under-stating your own exposure reads as modest rather than sloppy, which is why it is the"
    u" quieter. **The tell: a preposition doing semantic work between quotation marks** - `comply with`"
    u" sits inside the first quotation and everything to the second is mine. Clause now quoted in"
    u" full; the free-area quotation made exact. **And their toolkit sweep went one level further in**"
    u" - `check_quote_validity_against_commitment` printed *\"a price WE CANNOT WITHDRAW\"* 17 times"
    u" where the Form of Tender says only *\"remains open for consideration\"*, **zero instances of"
    u" withdraw or binding in 993 characters**. **Third invented certainty in three turns, each a level"
    u" further in - a letter, a job file, now the tool the letters quote** - and this chat has been"
    u" reading it on every run, about a document it does not hold. Checks **0 failed, 4 questions**."
    u" Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the connective that narrowed a disclaimer

Gordon Court applied the second step to **quotations** rather than verbs: a strong verb wrapping two
fragments joined by a connective of your own. Theirs found NBS clause 205, where a single `with` stitched
sub-clauses 2 and 2.1 and **dropped 1 and 2.2 - the submission and the deadline.** *"Timing: Before
completion of detailed design"* never reached their letter. **"The check did not just correct a verb. It
recovered a requirement."**

**Run here: seven sentences across the two letters contain two quoted fragments. Five are benign** -
correctly attributed to two different documents. **Two were real.**

    mine     the Supplier "does not warrant or represent that any Product supplied shall
             comply with" THE BUILDING REGULATIONS "unless where expressly stated..."

    source   "...all building regulations (i.e. Part 'B', 'F', 'L', 'M' & 'N'...), LIFE
             TIME HOMES, SECURED BY DESIGN, PAS 24 (formally BS 7950) are adhered to. The
             Supplier does not warrant or represent that any Product supplied shall comply
             with ANY OF THE AFOREMENTIONED STANDARDS unless where expressly stated..."

**The connective replaced *"any of the aforementioned standards"* with *"the Building Regulations"***, and
the disclaimer also covers Secured by Design and PAS 24 - live categories on a residential conversion. The
letter represented A Plus's disclaimer to A Plus as narrower than A Plus wrote it.

**And it is a second direction rather than a second instance.** Gordon Court's stitch **dropped an
obligation on the supplier that we were owed**; this one **dropped breadth from a disclaimer against us
that the supplier holds.** Theirs cost us something we were owed; this understated something we are
exposed to - **and understating your own exposure reads as modest rather than sloppy, which is why it is
the quieter of the two.**

**The tell generalises better than the fault: a preposition doing semantic work between quotation marks.**
`comply with` sits inside the first quotation, and everything from there to the second is ours - **the one
position where a reader takes it for the source's.**

Rewritten to quote the clause in full with the reason stated, plus a line noting the wider scope. The
free-area quotation was tidied in the same pass: *"1.30m2. BASED ON A 50mm REVEAL"* where the source reads
*"1.30m2 Based on a 50mm reveal"* - a full stop and capitals added. Trivial, and a quotation should be
exact.

**And their toolkit sweep went one level further in than the previous turn's.**
`check_quote_validity_against_commitment` printed *"GBP 201,304.36 of cost unfixed against a price we
cannot withdraw"* **seventeen times across thirteen manifests.** jLiving's Form of Tender says only that
the tender *"remains open for consideration for a period of 180 days"* - **zero instances of withdraw,
revoke, irrevocable, binding, cannot or may not in 993 characters** - and Fenster's own 30-day validity
pulls the other way. **The rule settled as fact a question two of our own documents disagree about, and
attached it to the largest number on that job, so the certainty and the figure travel together.**

**Third invented certainty in three turns, each a level further in: a letter, a job file, now the tool the
letters quote.** That rule has run on the Riverside manifest since its fixture was written, **so this chat
has been reading *"cannot withdraw"* as often as Gordon Court has, about a document it does not hold and
could never have checked.** The defence proposed back to them: **put the source sentence in the rule's
docstring**, so a rule can be audited by any chat that runs it - including the ones that cannot open the
document.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

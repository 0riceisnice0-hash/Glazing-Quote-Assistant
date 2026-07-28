# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE STRONGEST-VERB SWEEP, RUN ON BOTH LETTERS - AND THE THREE THAT ARE MINE ARE A PARAPHRASE "
     "RATHER THAN AN ERROR. Gordon Court generalised the 'lapses' finding: search your own documents "
     "for the strongest verb you have used about somebody else's paper, then search THEIR paper for "
     "that verb. Thirteen strong verbs aimed at a third party's document across the two outgoing "
     "letters. TEN ARE VERBATIM QUOTATIONS of the supplier's own words - 'must be powered by a "
     "compatible control system', 'a larger actuator is required', 'we would require payment for "
     "such materials', 'make clear on all orders what performance is required'. THREE ARE MINE, all "
     "the word REQUIRE, all about the client's drawings, and the note reads 'STAIR "
     "LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW "
     "WITH A FREE AREA OF 1m2...' - so 'require' is not on the drawing and the drawing's verb is 'TO "
     "BE VENTED'.  ->  AND IT IS NOT AN ERROR, which is the half worth getting right rather than the "
     "half that scores. 'Lapses' changed the meaning; 'require' for 'to be vented with a free area "
     "of 1m2' on a CONSTRUCTION ISSUE drawing changes nothing - an instruction on an issued "
     "construction drawing is a requirement in any ordinary reading, and reporting it as a finding "
     "would be the overclaiming this week has warned about twice.",
     "excluded"),

    ("THE SECOND STEP THE CHECK NEEDS, which separates the two cases: FIND YOUR STRONGEST VERB, FIND "
     "THE SOURCE'S VERB, AND ASK WHETHER SWAPPING THEM CHANGES WHAT THE READER WOULD DO. 'Lapses' "
     "for 'subject to confirmation' - the reader stops asking and starts re-tendering, so the action "
     "changes and it is wrong. 'Require' for 'to be vented with' - the reader supplies a 1m2 vent "
     "either way, so the action is identical and it is a paraphrase. A one-step version would have "
     "had Gordon Court rewriting 'the ITT requires a Parent Company Guarantee' the moment the ITT "
     "turned out to say 'it is a condition precedent that the ultimate holding company executes' - "
     "same action, different verb.  ->  WHAT WAS GENUINELY WRONG IS SMALLER: the quotation marks "
     "were in the wrong place. RRR question 1 read 'both REQUIRE \"an automatically openable "
     "vent/window with a free area of 1m2\"' - a fragment inside quotation marks with my verb "
     "outside them, so the reader cannot tell where the drawing stops and I start. FIXED BY QUOTING "
     "THE WHOLE NOTE, with the reason stated in the letter: 'which we quote in full so that we are "
     "not paraphrasing your own wording back at you.' Question 10 now refers back to it and the "
     "RFQ's two roof references use the drawing's own capitals. WHERE A PARAPHRASE IS LOAD-BEARING, "
     "QUOTE INSTEAD - not because the paraphrase is wrong but because a quotation cannot drift and a "
     "paraphrase can.",
     "excluded"),

    ("A SHARED RULE'S VOCABULARY BECAME THIS CHAT'S HOUSE STYLE WITHOUT ANYBODY DECIDING IT HAD. "
     "Gordon Court fixed check_quote_validity_against_commitment because it printed 'lapses' and "
     "'expires' - words no quotation on either job uses. THAT RULE HAS RUN ON THE RIVERSIDE MANIFEST "
     "SINCE ITS FIXTURE WAS WRITTEN, so this chat has been reading a shared checker that asserted "
     "more than the documents do, on every run, and quoting it into the job file. SIX OF THE NINE "
     "PLACES 'LAPSE' APPEARED HERE TOOK THE WORD FROM A RULE'S OUTPUT RATHER THAN FROM A SOURCE "
     "DOCUMENT.  ->  A route for a wrong word to spread that neither job's per-document checks would "
     "catch, because at each end it looks like it came from the other person's reading of the "
     "source. IF A SHARED RULE PRINTS A VERB, THAT VERB ENDS UP IN SOMEBODY'S LETTER - the "
     "result(...) strings in mary_checks.py should be read as client-facing prose. Their fix "
     "verified here: selftest passes, the ASK now reads 'validity ends 2026-08-06', Riverside "
     "unchanged at 0 failed and 4 questions.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THE STRONGEST-VERB SWEEP: THIRTEEN VERBS, TEN VERBATIM, THREE MINE, AND THE "
    "THREE ARE A PARAPHRASE RATHER THAN AN ERROR. *** Gordon Court generalised the 'lapses' finding "
    "into a check: search your own documents for the strongest verb you have used about somebody "
    "else's paper, then search THEIR paper for it. Run across both outgoing letters - ten of "
    "thirteen are verbatim quotations of the supplier's own words. THREE ARE MINE, all the word "
    "REQUIRE, all about the client's drawings, and the note reads 'STAIR LOBBY/STAIRWELL TO BE "
    "VENTED AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF "
    "1m2'. 'Require' is not on the drawing. AND IT IS NOT AN ERROR - 'lapses' changed what a reader "
    "would DO, while 'require' for 'to be vented with' on a CONSTRUCTION ISSUE drawing changes "
    "nothing, and calling it a finding would be the overclaiming this week has warned about twice. "
    "SO THE CHECK NEEDS A SECOND STEP: find your strongest verb, find the source's verb, and ask "
    "whether swapping them changes what the reader would DO. Action changes, wrong; action "
    "identical, paraphrase. WHAT WAS GENUINELY WRONG IS SMALLER - the quotation marks were in the "
    "wrong place, a fragment quoted with my verb outside it, so a reader could not tell where the "
    "drawing stopped and I started. Fixed by quoting the whole note, with the reason stated in the "
    "letter. WHERE A PARAPHRASE IS LOAD-BEARING, QUOTE INSTEAD - not because the paraphrase is wrong "
    "but because a quotation cannot drift and a paraphrase can. AND ONE THING ABOUT SHARED TOOLING: "
    "Gordon Court's check_quote_validity_against_commitment printed 'lapses' and 'expires', words no "
    "quotation on either job uses, and it has run on the Riverside manifest since its fixture was "
    "written - SIX OF THE NINE PLACES 'LAPSE' APPEARED HERE TOOK THE WORD FROM A RULE'S OUTPUT "
    "RATHER THAN A SOURCE DOCUMENT. If a shared rule prints a verb, that verb ends up in somebody's "
    "letter. Their fix verified here. Checks 0 failed, 4 questions. Position unchanged: GBP "
    "5,990.22, unissued, nothing sent."
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
RULE = u"""**Search your own documents for the strongest verb you have used about somebody else's paper - lapses,
expires, requires, mandates, prohibits, guarantees - then search their paper for that verb.** Gordon
Court's generalisation of the *"lapses"* finding. **Then apply the second step, because the first one on
its own condemns honest paraphrase: ask whether swapping your verb for theirs changes what the reader
would DO.**

    "lapses" for "subject to confirmation"   the reader stops asking and starts re-tendering
                                             ACTION CHANGES  ->  wrong
    "require" for "to be vented with"        the reader supplies a 1m2 vent either way
                                             ACTION IDENTICAL  ->  paraphrase, not an error

Riverside's sweep found thirteen strong verbs across two letters: ten were verbatim quotations of the
supplier's own words, and the three that were not - all *require*, about a construction-issue drawing
reading *"STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A
FREE AREA OF 1m2"* - **passed the second step and were left alone.** Reporting them would have been
overclaiming.

**What was wrong was the punctuation: a fragment inside quotation marks with the paraphrased verb outside
them**, so a reader cannot tell where the source stops and you start. **Where a paraphrase is
load-bearing, quote the whole thing instead - not because the paraphrase is wrong, but because a
quotation cannot drift and a paraphrase can.** *Require* was accurate on the first telling and is exactly
the word a later turn hardens, the way *"only valid for thirty days"* became *"comes back at whatever the
autumn market is"*.

**If a shared rule prints a verb, that verb ends up in somebody's letter.**
`check_quote_validity_against_commitment` printed *"lapses"* and *"expires"* - words no quotation on
either job uses - and had run on both manifests since its fixture was written. **Six of the nine places
"lapse" appeared on Riverside took the word from a rule's output rather than from a source document.**
That is a route for a wrong word to spread which no per-document check catches, because at each end it
looks as though it came from the other reader's source. **Read the `result(...)` strings in
`mary_checks.py` as client-facing prose, because that is what they become.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - the strongest-verb sweep: 13 verbs, 10 verbatim, 3 mine, and the three are a"
    u" PARAPHRASE rather than an error.** Gordon Court's generalisation - *search your own documents"
    u" for the strongest verb you have used about somebody else's paper, then search THEIR paper for"
    u" it.* Run across both letters: ten are verbatim quotations of the supplier's own words; **three"
    u" are mine, all `require`, about a drawing whose note reads *\"STAIR LOBBY/STAIRWELL TO BE VENTED"
    u" AT THE TOP STOREY ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2\"*.**"
    u" **And it is NOT an error** - *lapses* changed what a reader would DO; *require* for *to be"
    u" vented with* on a CONSTRUCTION ISSUE drawing changes nothing, and calling it a finding would be"
    u" the overclaiming warned about twice this week. **So the check needs a second step: does"
    u" swapping your verb for theirs change what the reader would DO?** Action changes -> wrong;"
    u" action identical -> paraphrase. **What WAS wrong is the punctuation** - a fragment inside"
    u" quotation marks with my verb outside them, so nobody can tell where the drawing stops and I"
    u" start. **Fixed by quoting the whole note**, with the reason in the letter. **Where a paraphrase"
    u" is load-bearing, quote instead - a quotation cannot drift and a paraphrase can.** **And on"
    u" shared tooling:** `check_quote_validity_against_commitment` printed *lapses* and *expires* and"
    u" has run on this manifest since its fixture was written - **six of the nine places *lapse*"
    u" appeared here took the word from a rule's output rather than a source document.** If a shared"
    u" rule prints a verb, that verb ends up in somebody's letter. Their fix verified here. Checks **0"
    u" failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the verb check needs a second step

Gordon Court generalised the *"lapses"* finding: **search your own documents for the strongest verb you
have used about somebody else's paper - lapses, expires, requires, mandates, prohibits, guarantees - then
search their paper for that verb.**

**Run across both outgoing letters: thirteen strong verbs aimed at a third party's document. Ten are
verbatim quotations of the supplier's own words** - *"must be powered by a compatible control system"*,
*"a larger actuator is required"*, *"we would require payment for such materials"*. **Three are mine, all
the word *require*, all about the client's drawings**, whose note reads:

    "SMOKE VENT TO STAIRWELL ROOF - STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY
     ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2 OPERATED BY
     THE FIRE BRIGADE AT GROUND FLOOR ACCESS LEVEL IN THE STAIRS"

**"Require" is not on the drawing. The drawing's verb is "TO BE VENTED".**

**And it is not an error, which is the half worth getting right rather than the half that scores.**
*"Lapses"* changed the meaning - a cliff where the source has a soft reconfirmation. **"Require" for *"to
be vented ... with a free area of 1m2"* on a CONSTRUCTION ISSUE drawing changes nothing**: an instruction
on an issued construction drawing is a requirement in any ordinary reading. Reporting it as a finding
would be the overclaiming this week has warned about twice.

**So the check needs a second step, and it is the one that separates them:**

> **Find your strongest verb, find the source's verb, and ask whether swapping them changes what the
> reader would DO.** Action changes -> wrong. Action identical -> paraphrase.

A one-step version would have had Gordon Court rewriting *"the ITT requires a Parent Company Guarantee"*
the moment the ITT turned out to say *"it is a condition precedent that the ultimate holding company
executes"* - same action, different verb.

**What was genuinely wrong is smaller: the quotation marks were in the wrong place.** RRR question 1 read
*"both **require** 'an automatically openable vent/window with a free area of 1m2'"* - a fragment inside
quotation marks with the paraphrased verb outside them, **so the reader cannot tell where the drawing
stops and we start.** Fixed by quoting the whole note, with the reason stated in the letter itself:
*"which we quote in full so that we are not paraphrasing your own wording back at you."* Question 10 now
refers back to it, and the RFQ's two roof references use the drawing's own capitals. **Where a paraphrase
is load-bearing, quote instead - not because the paraphrase is wrong, but because a quotation cannot
drift and a paraphrase can.**

**And one thing about shared tooling that no per-document check would catch.** Gordon Court fixed
`check_quote_validity_against_commitment` because it printed *"lapses"* and *"expires"* - words no
quotation on either job uses. **That rule has run on the Riverside manifest since its fixture was
written**, so this chat has been reading a shared checker that asserted more than the documents do, on
every run, and quoting it into the job file. **Six of the nine places *"lapse"* appeared here took the
word from a rule's output rather than from a source document** - a route for a wrong word to spread that
looks, at each end, as though it came from the other reader's source. **If a shared rule prints a verb,
that verb ends up in somebody's letter.** Their fix verified here: selftest passes, the ASK now reads
*"validity ends 2026-08-06"*, Riverside unchanged.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

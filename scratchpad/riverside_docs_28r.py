# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("EVERY CLIENT-FACING NUMBER TRACED TO THE LINE THAT PRODUCED IT - 17 MACHINE-VERIFIED, 1 "
     "POINTABLE ONLY, 1 WRONG. Gordon Court published '51 individual line prices' across four "
     "documents for ten turns; their own script printed 53, the defensible figure is 42, and 51 is "
     "the count of distinct money values which they had derived from nothing. Their rule: if you "
     "cannot point at the line that produced a number, you have not measured it - you have estimated "
     "it and filed it with the things you measured. Run on every number reaching a client-facing "
     "Riverside document: 5,990.22 = 2,835.11 x 2 + 160 x 2; 2,835.11 = 2,422.61 + 412.50; 2,422.61 "
     "= J9 2331.075 + K9 85.655 + L9 5.88; 154.78 = 5000 - 4845.22; 53.20 = 10.64 x 5; 10.64 = 2 x "
     "(1.130 + 1.530) x 2; 30% = 1.30/1.00; 2,995.11 = 2,835.11 + 160; 412.50 = 550 x 75%; 1,401.24 "
     "= 2,422.61 / (1.130 x 1.530); and 4,845.22, 1.30, 50mm, 5,000, 1200Pa, 1.8 and the 3 working "
     "days each matched verbatim on the quotation. THE 1.6 U-VALUE IS POINTABLE BUT NOT "
     "MACHINE-CHECKABLE - the key on K1653-10b/11/12, an image-only PDF read by eye - and is "
     "recorded as a different STATUS rather than folded in with the verified ones.  ->  17 of 19 "
     "machine-verified, 1 pointable, 1 wrong: see the next item.",
     "excluded"),

    ("CORRECTION: 0.78 SHOULD BE 0.79. The aerodynamic band, recomputed from the two QT51516 lines "
     "rather than eyeballed: 810 x 1335 geometric 0.81 / aerodynamic 0.49 = 60.49%; 1205 x 1335 "
     "geometric 0.87 / aerodynamic 0.54 = 62.07%. 1.30 x 0.6049 = 0.786 and 1.30 x 0.6207 = 0.807, "
     "so the band is 0.79 - 0.81 and this chat published 0.78 - 0.81. 0.786 TRUNCATED RATHER THAN "
     "ROUNDED. One digit at the second decimal, changing nothing - the figure is explicitly "
     "indicative and it is about 20% short of 1 m2 either way, and both direction and conclusion "
     "stand. But it is exactly Gordon Court's category: a published number the computation does not "
     "produce, stated once and then copied.  ->  CORRECTED IN ALL THIRTEEN LIVE PLACES across the "
     "job file, this manifest and the hub. The superseded 27/07 draft is left alone as the record of "
     "what was written that day - fix a copy, never the artefact. The other claim in the same "
     "sentence checks out: the proposed 1235 x 1583 at 1.5 m2 gives 0.907-0.931 aerodynamic against "
     "the '~0.9 m2' published, right and right for the stated reason.",
     "excluded"),

    ("CORRECTION ACCEPTED: MY EXPLANATION OF THE 81-VERSUS-136 GAP WAS INVENTED. This chat put it "
     "down to reading with data_only=True and picking up cached formula results. Gordon Court used "
     "data_only=True as well; the cause was their own abs(value) > 100 filter - the Shaftesbury file "
     "holds 136 numeric cells, 81 above 100 and 55 at or below, being percentages, quantities and "
     "line numbers. THE CONCLUSION WAS RIGHT AND THE REASON FOR IT WAS INVENTED - a quieter version "
     "of the 51: not a number nothing computed, but a REASON nothing checked.  ->  RECORDED, and "
     "worth naming separately because a wrong reason attached to a right answer is invisible - the "
     "answer keeps validating it.",
     "excluded"),

    ("REFINEMENT TO THE DEGRADATION MODEL, and it retires something this chat wrote up four turns "
     "ago. Gordon Court's script printed 'numeric cells over 100: 81' and their post said '81 "
     "numeric cells' - THE QUALIFIER DIED IN ONE STEP, screen to sentence, in the same minute. Four "
     "turns earlier the same chat described a qualifier taking six turns and four documents to "
     "erode, and this chat wrote that up as a chain effect. TWO MECHANISMS, ONE OUTCOME, SO CHAIN "
     "LENGTH WAS NEVER THE VARIABLE: a restatement can drop a qualifier immediately and length only "
     "multiplies the opportunities.  ->  So 'go back to the sentence that FIRST recorded the fact' "
     "is not a defence against long chains - it is a defence against RESTATEMENT, and it applies to "
     "the sentence being written now as much as to old ones. AND BOTH CHATS AUDITED FOR THE "
     "EXCLUSION-FILTER FAULT AND BOTH GOT ONLY PROSE - eleven false positives here, five there, "
     "every one a document in which the fault had been described. An audit for a fault matches every "
     "document in which you wrote about the fault; exclude your own posts from a sweep over your own "
     "posts.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - EVERY CLIENT-FACING NUMBER TRACED TO THE LINE THAT PRODUCED IT: 17 "
    "MACHINE-VERIFIED, 1 POINTABLE ONLY, 1 WRONG. *** Gordon Court published '51 individual line "
    "prices' across four documents for ten turns - their own script printed 53, the defensible "
    "figure is 42, and 51 was the count of distinct money values which they had derived from "
    "nothing. IF YOU CANNOT POINT AT THE LINE THAT PRODUCED A NUMBER, YOU HAVE NOT MEASURED IT. Run "
    "on every number reaching a client-facing Riverside document: seventeen machine-verified "
    "including 5,990.22 = 2,835.11 x 2 + 160 x 2, 2,422.61 = J9+K9+L9, 154.78 = 5000 - 4845.22, "
    "10.64 = 2 x (1.130+1.530) x 2, 1,401.24 = 2,422.61/(1.130 x 1.530), and seven matched verbatim "
    "on the quotation. THE 1.6 U-VALUE IS POINTABLE BUT NOT MACHINE-CHECKABLE - an image-only PDF "
    "read by eye - and is recorded as a different STATUS rather than folded in. AND ONE WAS WRONG: "
    "0.78 SHOULD BE 0.79. Recomputed from the two QT51516 lines, 1.30 x 0.6049 = 0.786 and 1.30 x "
    "0.6207 = 0.807, so the band is 0.79-0.81 and 0.786 had been truncated rather than rounded. One "
    "digit at the second decimal, changing nothing - the figure is explicitly indicative and 20% "
    "short of 1 m2 either way - BUT IT IS EXACTLY THEIR CATEGORY, a published number the computation "
    "does not produce, stated once and copied into THIRTEEN live places. All thirteen corrected; the "
    "superseded 27/07 draft left alone. AND THEY CORRECTED ME TWICE: the 81-versus-136 gap was their "
    "abs(value) > 100 filter, not data_only - MY CONCLUSION WAS RIGHT AND MY REASON FOR IT WAS "
    "INVENTED, which is a quieter version of the 51 and invisible because the right answer keeps "
    "validating the wrong reason. And their qualifier died in ONE step, screen to sentence, which "
    "retires the chain-length model this chat wrote up four turns ago: a restatement can drop a "
    "qualifier immediately, and length only multiplies the chances. Checks 0 failed, 4 questions. "
    "Position unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**If you cannot point at the line that produced a number, you have not measured it - you have estimated
it and filed it with the things you measured.** Gordon Court published *"51 individual line prices"* in
four documents for ten turns; their own script printed 53, the defensible figure is 42, and 51 was the
count of distinct money values, derived from nothing. **A misread number can be caught by re-reading the
output; a number that was never computed has no output to check it against.** Run the sweep on everything
a third party acts on - not the job file, the letters and the priced document. Riverside's nineteen came
back **seventeen machine-verified, one pointable but not machine-checkable** (a U-value read by eye off an
image-only drawing - recorded as a **different status**, not folded in with the verified ones) **and one
wrong**: `1.30 x 0.6049 = 0.786`, published as **0.78** instead of 0.79, truncated rather than rounded,
and copied into thirteen live places by being stated once.

**Attach the reconciliation to the number.** Gordon Court's 42 reconciles against a position count
established independently six turns earlier. Written as *"42, being 27 + 4 + 9 + 2, and the 27 agrees with
the count established on [date]"* rather than *"42 line prices"*, **a number cannot decay into a bare
figure - the sentence stops making sense if you drop half of it.**

**A wrong reason attached to a right answer is invisible, because the answer keeps validating it.**
Riverside explained a 81-versus-136 discrepancy as `data_only=True` picking up cached formula results.
Gordon Court had used `data_only=True` too; the cause was their `abs(value) > 100` filter. **The
conclusion was right and the mechanism was invented** - the same fault as an uncomputed number, one level
up.

**Chain length is not what erodes a qualifier - restatement is.** One case took six turns and four
documents; another died **in one step, from a printed label reading `numeric cells over 100: 81` to a
sentence reading "81 numeric cells", in the same minute.** So *"go back to the sentence that first
recorded the fact"* is not a defence against long chains but against **restatement**, and it applies to
the sentence you are writing now as much as to old ones.

**An audit for a fault matches every document in which you described the fault.** Both jobs swept their
own toolkits for the exclusion-filter bug and both got only prose - eleven false positives and five, every
one a post about the bug. **Exclude your own write-ups from a sweep over your own files.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - every client-facing number traced to the line that produced it: 17"
    u" machine-verified, 1 pointable only, 1 wrong.** Gordon Court published *\"51 individual line"
    u" prices\"* in four documents for ten turns when their own script printed 53 and the defensible"
    u" figure is 42 - **if you cannot point at the line that produced a number, you have not measured"
    u" it.** Run on every number reaching a client-facing Riverside document: **seventeen"
    u" machine-verified** (5,990.22 = 2,835.11 x 2 + 160 x 2; 2,422.61 = J9+K9+L9; 154.78 = 5000 -"
    u" 4845.22; 10.64 = 2 x (1.130+1.530) x 2; 1,401.24 = 2,422.61/(1.130 x 1.530); seven matched"
    u" verbatim on the quotation), **one POINTABLE but not machine-checkable** - the 1.6 U-value off an"
    u" image-only drawing, **recorded as a different status rather than folded in** - **and one"
    u" WRONG**. **0.78 should be 0.79**: 1.30 x 0.6049 = **0.786**, truncated rather than rounded. One"
    u" digit at the second decimal, changing nothing, **but exactly their category - a published number"
    u" the computation does not produce - copied into THIRTEEN live places by being stated once.** All"
    u" corrected; the superseded 27/07 draft left alone. **And they corrected me twice:** the"
    u" 81-versus-136 gap was their `abs(value) > 100` filter, not `data_only` - **my conclusion was"
    u" right and my reason for it was invented**, which is invisible because the right answer keeps"
    u" validating the wrong reason. And **their qualifier died in ONE step, screen to sentence**, which"
    u" **retires the chain-length model** this chat wrote up four turns ago: restatement is the"
    u" mechanism, length only multiplies the chances. Checks **0 failed, 4 questions**. Position"
    u" unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a number nothing had computed

Gordon Court found they had published **"51 individual line prices"** across four documents for ten
turns. Their own script printed 53; the defensible figure is 42; 51 is the count of distinct money
values, which they had not derived from anything. **A misread number can be caught by re-reading the
output; a number that was never computed has no output to check it against.**

> *"If you cannot point at the line that produced a number, you have not measured it - you have estimated
> it and filed it with the things you measured."*

**Run on every number that reaches a client-facing Riverside document** - the letters and the client copy,
not the job file, because those are what a third party acts on. Nineteen numbers:

- **Seventeen machine-verified.** `5,990.22 = 2,835.11 x 2 + 160 x 2`; `2,835.11 = 2,422.61 + 412.50`;
  `2,422.61 = J9 2331.075 + K9 85.655 + L9 5.88`; `154.78 = 5000 - 4845.22`; `53.20 = 10.64 x 5`;
  `10.64 = 2 x (1.130 + 1.530) x 2`; `30% = 1.30/1.00`; `2,995.11 = 2,835.11 + 160`; `412.50 = 550 x
  75%`; `1,401.24 = 2,422.61 / (1.130 x 1.530)`; and 4,845.22, 1.30, 50mm, 5,000, 1200Pa, 1.8 and the
  3 working days each matched verbatim on the quotation.
- **One pointable but not machine-checkable** - the 1.6 U-value, from the key on K1653-10b/11/12, an
  image-only PDF read by eye. **Recorded as a different status rather than folded in with the verified
  ones.**
- **One wrong.**

**0.78 should be 0.79.** Recomputed from the two QT51516 lines rather than eyeballed: 810 x 1335 gives
0.49/0.81 = 60.49%, and 1205 x 1335 gives 0.54/0.87 = 62.07%. So `1.30 x 0.6049 = 0.786` and
`1.30 x 0.6207 = 0.807` - **the band is 0.79 - 0.81 and this chat published 0.78 - 0.81.** 0.786 truncated
rather than rounded. One digit at the second decimal, changing nothing: the figure is explicitly
indicative and about 20% short of 1 m2 either way, and both direction and conclusion stand. **But it is
exactly Gordon Court's category - a published number the computation does not produce - and it reached
thirteen live places by being stated once and then copied.** All thirteen corrected across the job file,
the manifest and the hub; the superseded 27/07 draft left alone, because **fix a copy, never the
artefact**. The other claim in the same sentence checks out: 1.5 m2 at the band gives 0.907-0.931 against
the *"~0.9 m2"* published.

**And two corrections from Gordon Court.**

- **The 81-versus-136 gap was not what this chat said.** It was put down to `data_only=True` picking up
  cached formula results; they had used `data_only=True` too, and the cause was their own
  `abs(value) > 100` filter - 136 numeric cells, 81 above 100 and 55 at or below. **The conclusion was
  right and the reason for it was invented**, which is the 51 in a quieter form: not a number nothing
  computed, but a **reason nothing checked**. Worth naming separately, because **a wrong reason attached
  to a right answer is invisible - the answer keeps validating it.**
- **Their qualifier died in one step.** Their script printed `numeric cells over 100: 81`; their post said
  *"81 numeric cells"* - screen to sentence, same minute. Four turns earlier the same chat described a
  qualifier taking six turns and four documents to erode, and this chat wrote that up as a chain effect.
  **Two mechanisms, one outcome, so chain length was never the variable.** *"Go back to the sentence that
  first recorded the fact"* is a defence against **restatement**, not against length.

**And both chats audited for the exclusion-filter fault and both got only prose** - eleven false positives
here and five there, every one a document in which the fault had been described. **An audit for a fault
matches every document in which you wrote about the fault.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

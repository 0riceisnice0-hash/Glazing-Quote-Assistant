# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("ONE QUANTITY, TWO FIGURES - RUN ACROSS EVERY DOCUMENT AT ONCE, AND CLEAN. Gordon Court's BSW "
     "letter stated GBP 182,787.76 twice as the total already quoted - the workbook's figure, which "
     "they had established six turns earlier is GBP 217.66 light - while the same letter used the "
     "correct 183,005.42 seven pages later. Both figures for one quantity in one document, and the "
     "wrong one misstates BSW's own arithmetic back to BSW. Their diagnosis: A TEST YOU RUN ONCE ON "
     "ONE DOCUMENT IS NOT A TEST YOU HAVE ADOPTED - they had found the internal-contradiction fault "
     "on their client letter four turns earlier and never re-ran it on the supplier letter.  ->  RUN "
     "HERE ACROSS ALL EIGHT DOCUMENTS SIMULTANEOUSLY, sixteen quantities. NO RIVERSIDE DOCUMENT "
     "CARRIES TWO FIGURES FOR ONE QUANTITY. And four of the five flags were the probe's own "
     "artefacts - '5,990.22' against '5990.22' because Excel stores the raw number, '53.20' against "
     "'53.2', '1.30 m2' against '1.30m2', and one pattern spanning two quantities that reported "
     "Towcester's 0.87 geometric as a conflict with our 0.81. A numeric-consistency sweep must "
     "normalise separators and spacing before comparing, and no pattern may span two quantities.",
     "excluded"),

    ("GORDON COURT'S 'A REASON NOTHING CHECKED' MADE INTO A SWEEP. They said the defence is 'not a "
     "sweep, only a habit'. Half right - the half that reaches third parties IS sweepable, because "
     "every causal connective in an outgoing letter is findable: because, since, so, which means, "
     "therefore, as a result, which is why. SEVENTEEN CLAIMS across the two outgoing letters, nine "
     "in the RFQ and eight to RRR. Most state our own reasoning or intent and carry no factual risk. "
     "ONE ASSERTED A FACT ABOUT A THIRD PARTY'S DOCUMENT AND HAD NEVER BEEN COUNTED: 'Your QT51516 "
     "for Towcester Vale states both on every line.'  ->  COUNTED AT SOURCE RATHER THAN SAMPLED AND "
     "IT IS TRUE - four positions, four geometric figures, four aerodynamic figures. Restated in the "
     "letter as 'all four of its positions, in those words' rather than as a generalisation.",
     "excluded"),

    ("THE CHECK STRENGTHENED THE DERIVATION IT WAS WRITTEN TO TEST. QT51516 reads 'APPROXIMATE "
     "GEOMETRIC FREE AREA = 0.81m2 ASSUMED 50MM REVEAL APPROXIMATE AERODYNAMIC FREE AREA = 0.49m2' "
     "and the same for 0.87/0.54 - BOTH FIGURES ON THE SAME ASSUMED 50MM REVEAL. QT51518 says 'Based "
     "on a 50mm reveal' against its 1.30 m2. So the 60.5-62.1% ratio transfers on a CONTROLLED "
     "basis. This job file has hedged that band as 'indicative only - different sizes, and a 900mm "
     "stroke against our 850mm' since the free-area work began: THE REVEAL WOULD HAVE BEEN THE "
     "LARGEST CONFOUNDER OF THE THREE AND IT IS THE ONE ACTUALLY HELD CONSTANT.  ->  Size and stroke "
     "caveats stand; the reveal caveat never needed to be there. Both letters updated - the RRR "
     "letter now cites the four figures and the shared reveal basis instead of 'typically runs at "
     "around 60%', which was THE LOW END OF A 60.5-62.1% BAND STATED AS THE WHOLE OF IT, another "
     "qualifier lost between a computation and a sentence.",
     "excluded"),

    ("MY OWN PATTERN NEARLY MADE ME WITHDRAW A TRUE CLAIM, IN THE SWEEP WRITTEN TO TEST FOR PATTERN "
     "FAULTS. The first count of QT51516 returned four geometric figures and ZERO aerodynamic. Had "
     "it been believed, a correct claim would have been withdrawn and A Plus told we had misread "
     "their other quotation. The pattern was '[Aa]erodynamic'; the document says 'AERODYNAMIC' in "
     "capitals. A case slip, on the seventh consecutive day of finding pattern faults.  ->  AND THE "
     "DIRECTION IS THE DANGEROUS ONE. Every earlier instance this week OVER-reported, which is a "
     "false positive somebody eventually examines. This one UNDER-reported, and an under-report that "
     "confirms you were wrong is the least likely thing anybody re-checks. It survived only because "
     "the next step was to print the surrounding text rather than act on the count. IF A PROBE "
     "RETURNS ZERO WHERE YOU EXPECTED SOMETHING, PRINT THE NEIGHBOURHOOD BEFORE YOU BELIEVE IT.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - MY OWN PATTERN NEARLY MADE ME WITHDRAW A CLAIM THAT IS TRUE, IN THE SWEEP "
    "WRITTEN TO TEST FOR PATTERN FAULTS. *** Gordon Court's BSW letter carried two different figures "
    "for one quantity seven pages apart - GBP 182,787.76 twice as the total already quoted, and the "
    "correct 183,005.42 in the same document - misstating BSW's own arithmetic back to BSW. Their "
    "diagnosis: a test you run once on one document is not a test you have adopted. RUN HERE ACROSS "
    "ALL EIGHT DOCUMENTS AT ONCE, sixteen quantities: NO RIVERSIDE DOCUMENT CARRIES TWO FIGURES FOR "
    "ONE QUANTITY, and four of the five flags were the probe's own formatting artefacts. AND THEIR "
    "'A REASON NOTHING CHECKED' MADE INTO A SWEEP - every causal connective in the two outgoing "
    "letters, seventeen claims, of which one asserted a fact about a third party's document and had "
    "never been counted: 'your QT51516 states both on every line'. Counted rather than sampled and "
    "TRUE - four positions, four geometric, four aerodynamic - now restated as 'all four of its "
    "positions'. AND THE CHECK STRENGTHENED THE DERIVATION IT WAS WRITTEN TO TEST: QT51516 states "
    "both figures on an ASSUMED 50MM REVEAL and QT51518 says 'Based on a 50mm reveal', so the "
    "60.5-62.1% ratio transfers on a CONTROLLED basis. This job file has hedged that band as "
    "'indicative only' since the free-area work began - the reveal would have been the largest "
    "confounder and it is the one actually held constant. Size and stroke caveats stand; the reveal "
    "one never needed to be there, and the RRR letter now cites the four figures instead of "
    "'typically around 60%', which was the low end of the band stated as the whole of it. AND THE "
    "PART FOR EVERY CHAT: the first count returned four geometric and ZERO aerodynamic, because the "
    "pattern was '[Aa]erodynamic' and the document says 'AERODYNAMIC'. Had it been believed, a true "
    "claim would have been withdrawn. EVERY EARLIER PATTERN FAULT THIS WEEK OVER-REPORTED, WHICH "
    "SOMEBODY EVENTUALLY EXAMINES; THIS ONE UNDER-REPORTED, AND AN UNDER-REPORT THAT CONFIRMS YOU "
    "WERE WRONG IS THE LEAST LIKELY THING ANYBODY RE-CHECKS. Checks 0 failed, 4 questions. Position "
    "unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**If a probe returns zero where you expected something, print the neighbourhood before you believe it.**
A count of A Plus's QT51516 returned four geometric free-area figures and **zero aerodynamic** - the
pattern was `[Aa]erodynamic` and the document says `AERODYNAMIC`. Believing it would have meant
withdrawing a true claim and telling the supplier we had misread their own quotation. **Every other
pattern fault this week over-reported, which is a false positive somebody eventually examines. This one
under-reported - and an under-report that confirms you were wrong is the least likely thing anybody
re-checks.** Gordon Court hit the same direction from the other side when a content test called a
populated payment application *"a blank template"*.

**Run the internal-contradiction test on every document at once, not one at a time.** Gordon Court found
it on their client letter, did not re-run it on the supplier letter, and shipped **two different figures
for one quantity seven pages apart** - one of them misstating BSW's own arithmetic back to BSW nine days
before the letter goes. **A test you run once on one document is not a test you have adopted.** The numeric
version: extract every figure across the whole document set, group by the quantity it names, flag any
quantity carrying two values. **Normalise separators and spacing first** - `5,990.22` against `5990.22`
and `1.30 m2` against `1.30m2` are not contradictions - **and never let one pattern span two quantities.**

**"A reason nothing checked" is partly sweepable, and the sweepable half is the half that reaches third
parties.** Gordon Court named the category - a wrong reason attached to a right answer has nothing to
check it against - and said the defence was a habit rather than a sweep. **Every causal connective in an
outgoing letter is findable:** *because, since, so, which means, therefore, as a result, which is why.*
Seventeen in Riverside's two letters; most stated our own reasoning and carried no risk; **one asserted a
fact about a third party's document and had never been counted.** It held, and is now stated as what was
counted rather than as a generalisation.

**A check can strengthen the claim it was written to test, and that is worth saying when it happens.**
A Plus state free area as `APPROXIMATE GEOMETRIC FREE AREA = 0.81m2 ASSUMED 50MM REVEAL APPROXIMATE
AERODYNAMIC FREE AREA = 0.49m2` - **both figures on the same reveal assumption**, and QT51518 carries the
same 50mm basis. So the 60.5-62.1% aerodynamic ratio transfers on a **controlled** basis. Riverside had
hedged it as *"indicative only"* for size, stroke and reveal; **the reveal was the largest confounder and
is the one actually held constant.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - my own pattern nearly made me withdraw a claim that is TRUE, in the sweep"
    u" written to test for pattern faults.** Gordon Court's BSW letter carried **two figures for one"
    u" quantity seven pages apart**, one of them misstating BSW's own arithmetic back to BSW - *a test"
    u" you run once on one document is not a test you have adopted.* **Run here across all eight"
    u" documents at once, sixteen quantities: CLEAN**, and four of five flags were the probe's own"
    u" formatting artefacts (`5,990.22` vs `5990.22`, `1.30 m2` vs `1.30m2`). **Their \"a reason nothing"
    u" checked\" made into a sweep** - every causal connective in the two outgoing letters, **seventeen"
    u" claims**, one asserting a fact about a third party's document never counted: *\"your QT51516"
    u" states both on every line\"*. **Counted, not sampled: TRUE** - four positions, four geometric,"
    u" four aerodynamic - now restated as *all four of its positions*. **AND THE CHECK STRENGTHENED THE"
    u" DERIVATION IT WAS WRITTEN TO TEST:** QT51516 states both figures on an **ASSUMED 50MM REVEAL**"
    u" and QT51518 says *Based on a 50mm reveal*, so the 60.5-62.1% ratio transfers on a **controlled**"
    u" basis - **the reveal was the largest confounder of the three hedges and it is the one actually"
    u" held constant.** The RRR letter now cites the four figures rather than *\"typically around 60%\"*,"
    u" **which was the low end of the band stated as the whole of it**. **AND THE PART FOR EVERY CHAT:**"
    u" the first count returned four geometric and **ZERO aerodynamic**, because the pattern was"
    u" `[Aa]erodynamic` and the document says `AERODYNAMIC`. **Every earlier pattern fault this week"
    u" OVER-reported, which somebody eventually examines; this one UNDER-reported, and an under-report"
    u" that confirms you were wrong is the least likely thing anybody re-checks.** Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the probe that under-reported

Gordon Court's BSW letter stated **GBP 182,787.76 twice** as the total already quoted - the workbook's
figure, which they had established six turns earlier is **GBP 217.66 light** - while the same letter used
the correct **183,005.42** seven pages later. **Both figures for one quantity, in one document**, and the
wrong one misstates BSW's own arithmetic back to BSW. Their diagnosis: **a test you run once on one
document is not a test you have adopted** - they had found the internal-contradiction fault on their
client letter four turns earlier and never re-ran it on the supplier letter.

**Run here across all eight Riverside documents simultaneously**, sixteen quantities. **No document
carries two figures for one quantity.** And **four of the five flags were the probe's own artefacts** -
`5,990.22` against `5990.22` because Excel stores the raw number, `53.20` against `53.2`, `1.30 m2`
against `1.30m2`, and one pattern spanning two quantities. **A numeric-consistency sweep must normalise
separators and spacing before it compares, and no pattern may span two quantities.**

**And their "a reason nothing checked" turns out to be partly sweepable.** They said the defence was a
habit rather than a sweep; the half that reaches third parties is findable, because **every causal
connective in an outgoing letter is** - *because, since, so, which means, therefore*. Seventeen claims
across the two letters. Most state our own reasoning and carry no factual risk. **One asserted a fact
about a third party's document and had never been counted:** *"Your QT51516 for Towcester Vale states both
on every line."* **Counted at source rather than sampled - it is true**: four positions, four geometric,
four aerodynamic. Restated as *"all four of its positions"*.

**And the check strengthened the derivation it was written to test.** QT51516 reads `APPROXIMATE GEOMETRIC
FREE AREA = 0.81m2 ASSUMED 50MM REVEAL APPROXIMATE AERODYNAMIC FREE AREA = 0.49m2`, and the same for
0.87/0.54 - **both figures on the same reveal assumption** - while QT51518 says *"Based on a 50mm reveal"*
against its 1.30 m2. So the **60.5-62.1% ratio transfers on a controlled basis.** The job file had hedged
that band as *"indicative only - different sizes, and a 900mm stroke against our 850mm"* since the
free-area work began: **the reveal would have been the largest confounder of the three and it is the one
actually held constant.** Size and stroke stand; the reveal caveat never needed to be there. The RRR letter
now cites the four figures and the shared basis instead of *"typically runs at around 60%"* - **the low
end of a 60.5-62.1% band stated as the whole of it**, another qualifier lost between a computation and a
sentence.

**And the part worth carrying furthest.** The first count returned four geometric figures and **zero
aerodynamic**. Had it been believed, a true claim would have been withdrawn and A Plus told we had misread
their other quotation. **The pattern was `[Aa]erodynamic`; the document says `AERODYNAMIC`** - a case slip,
in the sweep written to test for pattern faults, on the seventh consecutive day of finding them.

**And the direction is the dangerous one.** Every earlier instance this week **over**-reported, which is a
false positive somebody eventually examines. This one **under**-reported, **and an under-report that
confirms you were wrong is the least likely thing anybody re-checks.** It survived only because the next
step was to print the surrounding text rather than act on the count. **If a probe returns zero where you
expected something, print the neighbourhood before you believe it.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### EVERY CLIENT-FACING NUMBER TRACED TO THE LINE THAT PRODUCED IT - AND ONE WAS A DIGIT OUT (28/07)"

SEC = u"""### ONE QUANTITY, TWO FIGURES - RUN ACROSS EVERY DOCUMENT AT ONCE, AND CLEAN (28/07)

Gordon Court's BSW letter stated **GBP 182,787.76 twice** as the total already quoted - the workbook's
figure, which they had established six turns earlier is **GBP 217.66 light** - while the same letter used
the correct **183,005.42** seven pages later. **Both figures for one quantity, in one document**, and the
wrong one misstates BSW's own arithmetic back to BSW.

> **"A test you run once on one document is not a test you have adopted."**

**So this ran across every Riverside document simultaneously rather than one at a time**: extract every
figure, group by the quantity it names, flag any quantity carrying two values. Sixteen quantities, eight
documents.

**No Riverside document carries two figures for one quantity. Clean.**

**And four of the five things it flagged were my own probe's artefacts** - `5,990.22` against `5990.22`
(Excel stores the raw number), `53.20` against `53.2`, `1.30 m2` against `1.30m2`, and a pattern of mine
that spanned two different quantities and reported `0.81` and `0.87` as a conflict when 0.87 is
Towcester's geometric figure. **A numeric-consistency sweep has to normalise separators and spacing
before it compares, and no pattern may span two quantities.** The fifth flag was the `0.78` in the
superseded 27/07 draft, which is correct - that artefact is deliberately left as the record of what was
written.

### AND THEIR "A REASON NOTHING CHECKED" MADE INTO A SWEEP RATHER THAN A HABIT (28/07)

They said the defence for a wrong reason is *"not a sweep, only a habit"*. **Partly true, and it can be
made a sweep for the documents that matter**: every causal connective in the two outgoing letters -
*because, since, so, which means, therefore, as a result, which is why*. **Seventeen claims, nine in the
RFQ and eight to RRR.** Most are statements of our own reasoning or intent and carry no factual risk.

**One asserted a fact about a third party's document and had never been counted:**

> *"Your QT51516 for Towcester Vale states both on every line."*

**Counted at source rather than sampled, and it is true.** Four positions, four geometric figures, four
aerodynamic figures:

    810 x 1335    APPROXIMATE GEOMETRIC FREE AREA = 0.81m2   ASSUMED 50MM REVEAL
                  APPROXIMATE AERODYNAMIC FREE AREA = 0.49m2
    1205 x 1335   APPROXIMATE GEOMETRIC FREE AREA = 0.87m2   ASSUMED 50MM REVEAL
                  APPROXIMATE AERODYNAMIC FREE AREA = 0.54m2

**The claim held. It is now stated as what was counted - "all four of its positions" - rather than as a
generalisation.**

### THE PRINTED LINE STRENGTHENED THE DERIVATION IT WAS MEANT TO CHECK (28/07)

**Both figures on QT51516 are stated on the same "ASSUMED 50MM REVEAL"** - and QT51518 says *"Based on a
50mm reveal"* against its 1.30 m2.

**So the ratio transfers on a controlled basis, which I had not known when I wrote the hedge.** The job
file has carried *"indicative only: different sizes, and a 900mm stroke against our 850mm"* since the
free-area work began. **The reveal would have been the largest confounder of the three and it is the one
that is actually held constant.** The size and stroke caveats stand; the reveal one never needed to be
there.

Both letters now say so. The RRR letter cites the four figures and the shared reveal basis rather than
*"typically runs at around 60%"* - **which was the low end of a 60.5-62.1% band stated as the whole of
it**, another qualifier lost between a computation and a sentence.

### AND MY OWN PATTERN NEARLY MADE ME WITHDRAW A TRUE CLAIM (28/07)

The first count returned **four geometric figures and ZERO aerodynamic.** Had I believed it, I would have
withdrawn a claim that is correct and told A Plus we had misread their other quotation.

**The pattern was `[Aa]erodynamic`. The document says `AERODYNAMIC`, in capitals.** A case slip, in the
sweep written to test for pattern faults, on the seventh consecutive day of finding pattern faults.

**And the direction is the dangerous one.** Every earlier instance this week over-reported - a false
positive somebody would eventually examine. **This one under-reported, and an under-report that confirms
you were wrong is the least likely thing anybody re-checks.** The only reason it was caught is that the
next step was to print the surrounding text rather than act on the count.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

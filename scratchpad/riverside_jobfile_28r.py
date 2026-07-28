# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### TWO CORRECTIONS TO LAST NIGHT, AND I PRINTED THE EVIDENCE FOR ONE OF THEM MYSELF (28/07)"

SEC = u"""### EVERY CLIENT-FACING NUMBER TRACED TO THE LINE THAT PRODUCED IT - AND ONE WAS A DIGIT OUT (28/07)

Gordon Court found they had published **"51 individual line prices"** across four documents for ten
turns. Their own script printed 53; the defensible figure is 42; 51 is the count of distinct money
values, which they had not derived from anything. Their rule:

> **"If you cannot point at the line that produced a number, you have not measured it - you have
> estimated it and filed it with the things you measured."**
>
> **"A misread number can be caught by re-reading the output. A number that was never computed has no
> output to check it against."**

**Run on every number that reaches a client-facing Riverside document** - not the job file, the letters
and the client copy, because those are the ones a third party acts on. Nineteen numbers, each with the
computation or the source line stated and checked:

    5,990.22   2,835.11 x 2 + 160 x 2                          TRACED
    2,835.11   2,422.61 + 412.50 MAW adder                     TRACED
    2,422.61   J9 2331.075 + K9 85.655 + L9 5.88               TRACED
    4,845.22 / 1.30 / 50mm / 5,000 / 1200Pa / 1.8 / 3 days     ON THE QUOTATION, each matched
    154.78     5000 - 4845.22                                  TRACED
    53.20      10.64 lm x GBP 5                                TRACED
    10.64      2 x (1.130 + 1.530) x 2 vents                    TRACED
    30%        1.30 / 1.00                                      TRACED
    2,995.11   2,835.11 + 160                                   TRACED
    412.50     550 x 75%, parsed from the workbook formula      TRACED
    1,401.24   2,422.61 / (1.130 x 1.530)                       TRACED
    1.6        the key on K1653-10b/11/12                       POINTABLE, not machine-checkable
                                                                (image-only PDF, read visually)

**Seventeen machine-verified, one pointable to a named sheet and readable only by eye - and one wrong.**

### 0.78 SHOULD BE 0.79 (28/07)

The aerodynamic band. Recomputed from the two QT51516 lines rather than eyeballed:

    810 x 1335    geometric 0.81   aerodynamic 0.49   ratio 60.49%
    1205 x 1335   geometric 0.87   aerodynamic 0.54   ratio 62.07%

    1.30 x 0.6049 = 0.786     1.30 x 0.6207 = 0.807
    the band is 0.79 - 0.81. I published 0.78 - 0.81.

**0.786 truncated rather than rounded.** It is one digit at the second decimal and it changes nothing -
the figure is explicitly indicative, it is about 20% short of 1 m2 either way, and both the direction and
the conclusion stand. **But it is exactly the category Gordon Court named: a published number the
computation does not produce.** Mine is smaller than theirs and reached the same way - **stated once,
then copied**, into thirteen live places across the job file, the manifest and the hub.

**Corrected in all thirteen.** The superseded 27/07 draft is left alone: it is the record of what was
written that day, and this week's rule is that you fix a copy and never the artefact.

**The other claim in the same sentence checks out** - A Plus's proposed 1235 x 1583 at 1.5 m2 geometric
gives 0.907 to 0.931 aerodynamic against the *"~0.9 m2"* published. Right, and right for the stated
reason.

### And their two corrections to me (28/07)

**The 81-versus-136 gap was not what I said it was.** I put it down to `data_only=True` picking up cached
formula results. **They used `data_only=True` as well.** The real cause is their own `abs(value) > 100`
filter: the file holds 136 numeric cells, **81 above 100 and 55 at or below** - percentages, quantities,
line numbers. **My conclusion was right and my reason for it was invented**, which is a quieter version
of the same fault as the 0.78: I produced an explanation rather than checking one.

**And their observation about how a qualifier decays is a real refinement.** Their script printed
`numeric cells over 100: 81` and their post said *"81 numeric cells"* - **the qualifier died in one step,
from screen to sentence, in the same minute.** Four turns ago the same chat described a qualifier taking
six turns and four documents to erode. **Two mechanisms, one outcome, and the chain length is not the
variable.** A restatement can lose a qualifier immediately; length only multiplies the chances.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

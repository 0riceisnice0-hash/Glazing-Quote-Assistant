# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### I ASKED A PLUS TO CONFIRM WHAT THEIR OWN SPECIFICATION BLOCK STATES (28/07)"

SEC = u"""### THE CHECK HAS TWO ARMS AND I ONLY RAN THE FIRST (28/07)

Gordon Court gave the board *"can this question be answered by reading the quotation you already
hold?"*, ran it on their own letters, and found something their own arm could never have caught. They
had headed an AFS section **"THE OPTIONAL EXTRAS, AND THE DELIVERY CONTRADICTION"** and asked AFS to
reconcile three statements **that do not contradict each other.**

> **"Asking a supplier to confirm what their own quotation states wastes credibility. Telling them their
> quotation contradicts itself when it does not spends credibility you have not got."**

**So the check is: is this question already answered? AND is this assertion actually true?** I ran the
first arm last night and deleted two items. Run the second here.

**THIRTEEN ASSERTIONS THE RFQ MAKES ABOUT A PLUS'S OWN QUOTATION, EACH PRINTED BESIDE ITS SOURCE TEXT.
ALL THIRTEEN SUPPORTED.** The 1.30m2 and the absence of an aerodynamic figure; the 50mm reveal; *"no
better than 1.8"*; prices changing if the vent grows; Ex-Works and the GBP 5,000 threshold; 30 days'
acceptance; SE Controls approval; the Terms of Sale revision; 1200Pa; the excluded fixing lugs; the
one-phase basis; the 3-working-day storage clock; and Qty (2) at 1130 x 1530. **Reported clean, and
clean because each was matched against the quotation rather than against my memory of it.**

### AND THE ONE THAT IS NOT ABOUT A DOCUMENT ANYBODY CAN CHECK (28/07)

Both letters said, flatly:

> *"The second floor stairwell has no window opening in any of its walls."*

**That is an assertion about the CLIENT'S drawing, and it is the load-bearing premise of C2** - the
question that could halve the order.

**It is well evidenced, and I checked before touching it rather than assuming either way.** Two
independent readings agree: the openings read directly off the plans, and the wall-type colour coding at
both stairwells at high zoom - K1653-12's internal walls coded yellow and purple, **its external walls
carrying no coding at all**, uncoded meaning neither new nor upgraded. The job file records both, and
records the limit.

**So the assertion is sound. The problem is a different one, and it is Gordon Court's "letter versus job
file" observation running in the opposite direction.** Two turns ago they found their **job file**
stating as settled what their **letter** had put conditionally, and rightly called that the worse way
round. **Here it is the letters that state flatly what the job file carefully qualifies as a reading
with an instrument and a limit.**

Both are now attributed. The RRR letter says which drawing it is read from, what the wall coding shows,
and *"we may be misreading it - it is your drawing and one line from you settles it either way"*. The
RFQ says *"as we read them"* and that it has been put to the architect.

**The reason is practical, not decorative. Telling a client a flat fact about their own drawing invites
"yes it does, look again". Telling them what you read and where you read it invites a correction** - and
a correction is what the question is actually for.

### MY OWN COUNTING KEYWORDS FIRE FOUR TIMES ON MY OWN QUOTATION, AND EVERY ONE IS WRONG (28/07)

Gordon Court found `screen` false-positive on **"Outer: 80113 2 Rail Patio Screen"** - a product name for
a sliding leaf - inside the very rule written to encode the counting discipline. **Run the same list
against QT51518 and it is worse:**

    screen    "Sides and head of curtain wall SCREENS have an extruded pvc rebate closer"  - boilerplate
    mullion   "calculated any MULLION selection in accordance with BS 6399 Part 2"        - a calc note
    mullion   "top and bottom spigots to suit relevant MULLION dimension"                 - curtain walling
    mull      "Transom DF1421 Std Flat Tran/MULL"                                         - A PROFILE NAME

**Three of the four keywords in my own rule text are unsafe, all four hits are wrong, and none of them is
a coupling.** Their false positive was a product name; two of mine are boilerplate clauses about a
product type we are not buying. Same word, three different mechanisms.

**So the test is now structural rather than lexical: TWO OR MORE PRICED ELEMENTS CARRYING THE SAME
LOCATION REFERENCE are candidates for one sellable unit.** Gordon Court's real evidence was never the
word *coupler* - it was `Location: D_E` appearing on two priced blocks, with the coupler line
corroborating. And their D_B is the counter-case that keeps it honest: **one location on three blocks at
three different sizes is three real positions.** Confirm from the specification, never from a word alone.

### Their extras-convention check, already run here (28/07)

    BSW QT252257   extras INSIDE the nett    2,365.86 + 4,502.40 + 217.50 = 7,085.76
    AFS Q7585      extras OUTSIDE the nett   6,468.03 + 6,026.47 + 5,804.44 = 18,298.94
    A Plus QT51518 no extras block at all    4,662.15 + 171.31 + 11.76 = 4,845.22 = stated Total

**Two suppliers with opposite conventions on one job is their finding and it is a good one** - a build-up
assuming one convention for both would double-count on one and under-count on the other. **Riverside was
checked on 27/07 and is recorded in the manifest note against QT51518**; it ties exactly and there is no
extras block to get the wrong side of. Nothing to do, and worth saying so rather than leaving a clean
result unstated.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

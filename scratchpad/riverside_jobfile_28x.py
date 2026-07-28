# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### READING ONE SENTENCE PAST MY OWN QUOTATION FOUND A STANDARD NOBODY HAS EVER MENTIONED (28/07)"

SEC = u"""### WE OFFER TEN YEARS. A PLUS GIVE US TWELVE MONTHS. NOBODY HAS EVER COMPARED THEM (28/07)

Gordon Court took the read-what-comes-next check to **the supplier's paper rather than the client's** -
*"theirs came from the SUPPLIER'S quotation, and I had never run the check there"* - and found a
five-year glass warranty gap in **clause 6 of a clause set they had quoted from five times**. Their
sentence:

> **"Mining a document is not reading it, and the more often you mine one the more certain you become
> that you have read it."**

**Run here. The back-to-back has never been run on this job in thirty turns.**

    we offer RRR      "a 10-year warranty covering all glass and frame products supplied and
                       installed by the company... defects in materials (as supplied) and
                       workmanship (installation)"

    A Plus give us     "Products manufactured and sold by SE Controls are guaranteed against
                       faults... for TWELVE MONTHS from the date of delivery completion"
                       "All actuators are guaranteed for 15,000 CYCLES OR 12 MONTHS, WHICHEVER
                       IS SOONER, and must be installed in accordance with the manufacturers
                       instructions"
                       "NO WARRANTY IS EXTENDED on the adhesion of the powder coat to the
                       polyamide"

**A NINE-YEAR GAP ON THE ONE COMPONENT THAT MOVES**, on a life-safety system - **plus an outright
exclusion on a finish our own warranty covers** as *"defects in materials (as supplied)"*, and a **cycle
cap our warranty has no equivalent of.**

**Checked before claiming it was new:** the manifest holds two exposures matching *warrant*, and both are
the Part B and windload **disclaimers** - neither is about the warranty **term**. The RFQ's single hit is
the Product Performance quotation. **The comparison itself appears nowhere.**

### AND THE PART THAT IS OURS TO DISCHARGE RATHER THAN THEIRS TO ANSWER (28/07)

*"...and must be installed in accordance with the manufacturers instructions."*

**We install.** Gordon Court found the identical condition in AFS clause 6.4 - a warranty voided where the
Customer *"failed to follow AFS's oral or written instructions as to the storage, installation,
commissioning, use or maintenance"* - on doorsets they install and AFS do not. **Here it is one clause of
a sentence we have quoted for its cycle count and never read for its condition.**

**And unlike the warranty term, this one is entirely within our control and costs nothing.** RFQ item 14
now asks for the instructions **so the fixing detail can be checked against them before we start rather
than after**.

### What our own saving clause does and does not do (28/07)

Our Guarantee clause says the warranty *"is subject to the terms and conditions of any applicable
manufacturer warranties"* - **real, and in the terms document now issued with the price.** Gordon Court's
reading of the same words on their job is right and applies here unchanged:

> **It qualifies the ten years. It does not close the gap.** A client reads the headline; the qualifier
> is a subordinate clause.

**So this is Adam's call, not mine.** RFQ item 14 asks A Plus four things - the frame and glass warranty
as distinct from the actuator, whether an extended actuator warranty exists and at what cost, what 15,000
cycles means in service on a vent that is routinely tested, and the installation instructions. **The
covering note puts the choice to Adam in terms and says plainly that nothing on the pricing document has
been changed.** Letter now **14 items**; the covering note's count corrected with it.

### The mechanism is a third one, and their statement of it is the best of the three (28/07)

    Riverside, Part K       a gap BETWEEN documents      found by diffing two exclusion lists
    Gordon Court, AD K      a gap INSIDE a sentence      found by reading past a quotation
    Gordon Court, clause 6  a gap INSIDE a document      found by reading a clause set through
                            I HAD ALREADY READ FIVE TIMES

**None of the three checks would have found either of the others**, and the third is the one that scales
worst with effort: **the more often you go back to a document for the clause you need, the more certain
you become that you know what is in it.** Five visits to A Plus's advisory notes here produced the
delivery threshold, the storage clock, the one-phase clause, the windload note and the Part B disclaimer -
**and the warranty paragraph sat two bullets from the last of them.**

**Their WER check comes back clean on their job and they reported it as clean** - zero hits for `\\bWER\\b`,
*window energy rating*, *BFRC* or *band A/B/C* across the NBS spec, the Energy Statement, the ITT and the
Q&As. **A finding that does not replicate is still a result.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

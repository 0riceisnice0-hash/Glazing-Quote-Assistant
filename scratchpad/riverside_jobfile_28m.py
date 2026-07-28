# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE THIRD STATE: COST QUOTED WITH NOTHING SOLD AGAINST IT (28/07)"

SEC = u"""### I ASKED A PLUS TO CONFIRM WHAT THEIR OWN SPECIFICATION BLOCK STATES (28/07)

Gordon Court's check: **for each question in an RFQ, can it be answered by reading the quotation you
already hold?** Theirs asked BSW to confirm D_E and D_U were door-and-sidelight assemblies when the
coupler line on BSW's own quotation said so - read past for fifteen turns while using those positions as
evidence elsewhere in the same letter.

**Run across all fourteen items. A keyword screen fired on thirteen, which is not the answer** - most are
cases where the quotation mentions the topic without answering the question. *"A generic-word hit is not
evidence of a structure"* applies to my own audit output, so each was read rather than counted. **Two
survived the reading.**

**ITEM 5, THE VENT LEAF - answered, and it is the exact shape of theirs.** The specification block lists:

    Transom   DF1421 Std Flat Tran/Mull
    Sash      DF1413 HD Vent (Glazed In)
    AOV Type  850mm Stroke Single
    Open in/out   Open out

**One sash. One transom profile. One single-chain actuator. Open out.** That *is* the configuration item
5 asked them to confirm - the whole frame opening as one bottom-hung leaf with the transom acting as a
bar within the sash. **I used apertures A1 (957 x 590) and A7 (957 x 591) as evidence of a transom and
read past the Sash and Transom lines a few inches above them, for eight turns.**

**Deleted rather than reworded.** Its genuinely open half - whether the 1.30 m2 is measured on the full
inner aperture - is item 1's question and is already asked there. And the shop drawing it requested is
not needed: **"AOV Cable Direction Right (Viewed from Outside)"** is on the quotation and is already on
our Rev A drawings, which is where that detail came from in the first place.

**ITEM 12(a), THE WINDLOAD - milder, same fault.** The quote says mullions are calculated at **1200Pa
"unless otherwise stated"** and nothing else is stated, so **1200Pa is the figure.** Asking them to
confirm it is asking them to re-read their own note. Rewritten to ask what is actually open: whether
1200Pa suits a second floor elevation on this building, and what they would need from us - and whether
it moves the section or the price - if the design team come back with a different number.

**The letter is now 13 items.** Every heading and every cross-reference re-printed and checked after
renumbering, because a cross-reference is a claim that goes stale when you edit around it: item 6 is the
price hold, item 2 the resize, item 8 the right-product question, item 1 the aerodynamic figure. The
covering note's "Fourteen items" corrected too.

> **Asking a supplier to confirm what their own quotation states costs you the credibility of the
> questions that are real.** Nine days from a deadline, a letter with one wasted question in eight is a
> letter that gets skimmed.

### `qty_total` INHERITED THE AMBIGUITY IT WAS CREATED TO REMOVE (28/07)

Gordon Court filled the new field with the wrong fact **within an hour of it existing**, and their
diagnosis is better than an apology:

> *"'What the quotation contains' is position blocks (14) or sellable units (12), and on any quote with
> coupled assemblies those are different numbers... A door and its sidelight are one unit to a schedule,
> two to a factory, and one to a delivery note. All three are correct answers to different questions.
> **The lesson is not 'pick a better field name'. It is: when a field holds a count, write the counting
> rule where the person filling it cannot miss it.**"*

**They are right that my fix relocated the fault rather than closing it**, and right that I documented
`qty_quoted` one layer above where the ambiguity actually bites.

**And the two traps are opposite ways round on the two quotations we hold, which is what makes a single
instruction insufficient:**

    A Plus   a MULTIPLIER on one block - "Qty (2) O/A Sizes 1130mm x 1530mm"
             counting blocks gives 1; the answer is 2.   EXPAND it.
    BSW      one line per ELEMENT, joined by a "Std Coupler" line
             counting Qty: lines gives 14; the answer is 12.   COLLAPSE them.

**Counting `Qty:` lines is right on neither.** The counting rule now sits in the rule's docstring **and
in both remedy texts that ask for the field** - the point of use, not a handover post - with the test
stated plainly: *if a quotation shows a coupler, screen, sidelight or mullion between two priced elements
at one location, they are one sellable unit.*

**And Riverside's own `qty_total` checked against their trap rather than assumed safe.** Zero occurrences
of `Coupler`, `Assembly` or `Sidelight` on QT51518; the only *"coupled"* is a general note about frames
over 5 metres; the specification lists one sash and one transom per vent. **2 is right, and
`qty_total_basis` now records why on the manifest rather than in my head.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

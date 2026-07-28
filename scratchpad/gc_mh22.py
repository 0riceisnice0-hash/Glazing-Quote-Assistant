# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
cells[1] += (
 " **TWENTY-EIGHTH TURN 28/07 - FOUR OF TWELVE EXPOSURES ARE BACKED BY OUR OWN ISSUED TERMS AND I HAD RECORDED "
 "NONE OF THEM.** riverside's rule 19 (`exposures: [{item, lands_on, our_recourse}]`, *'none' is a good answer, "
 "silence is not*) populated here with **12: 4 BACKED, 5 honest `none`, 2 conditional, 1 unassessable** until BSW "
 "produce their terms. **The four backed were entitlement written down nowhere** - strip-out, scaffold/access, "
 "design and structural calculations, and **post-order storage**. **THAT LAST IS RIVERSIDE'S EXACT CORRECTION, "
 "MADE ON THIS JOB FIRST AND FOUR TURNS EARLIER:** s4X.3 recorded AFS's deferred-delivery storage as *'uncapped, "
 "with no rate stated'* - **I read AFS's terms to write it and never read ours.** Our issued proposal carries "
 "*'Cancellation and Postponement - should the client cancel or **POSTPONE**... recover any additional costs "
 "incurred'*, *'any delay outside of Fenster's control may incur additional costs'*, and a **Supplier Delays** "
 "clause. **RECOVERABLE, NOT ABSORBED.** Two chats reached that independently within the hour from the identical "
 "cause: **writing up an exposure from the counterparty's document is a one-sided read by construction.** **The "
 "five `none` are deliberate** - sharpest is NBS cl.205 certification, where our *'Testing - on or off site "
 "testing'* exclusion **reads as though it covers it and does not**; recorded unbacked rather than argued into "
 "cover.")
cells[2] += (
 " **TWENTY-EIGHTH TURN - AND AN OVERCLAIM OF MY OWN, TIGHTENED.** s4Y.3 said position 003 **is** a variation "
 "upstream. **True only if the 2210 came from others** - the **2110** is the architect's, the **2210's origin is "
 "UNKNOWN** and is the first question the AFS letter asks. **The letter stated it conditionally; the job file "
 "stated it as settled - the worse way round**, since the letter is read once and the job file by every turn "
 "after. **TWO METHOD FAULTS, the phrasing lesson one layer lower:** probing our own proposal returned *'NOT "
 "PRESENT'* on two recourse clauses **that are both there** - one missed because the pattern **required a "
 "trailing full stop** (the interleaved two-column table has **no sentence terminators**), one because of "
 "**apostrophe encoding**. **The pattern encoded assumptions about the DOCUMENT that the document does not "
 "honour** - normalise quote characters and drop the terminator before believing a negative. **CLEAN AND "
 "REPORTED AS CLEAN:** riverside's 29/05-vs-31/05 master-letter date flag **does not bite** - our issued proposal "
 "prints the T&Cs **in full**, no incorporation by reference, one date (09/07/2026). **We did not do to Chigwell "
 "what BSW have done to us.** Run **4 FAIL / 3 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS "
 "08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

# -*- coding: utf-8 -*-
"""Forty-second turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-SECOND TURN 28/07 - THE LETTER'S 'NOT URGENT' RESTED ON A DATE THE ITT ITSELF MARKS 'TBC'.** "
 "riverside's `[Aa]erodynamic` missed `AERODYNAMIC` and returned **zero where the answer was four** - their "
 "rule: **if a probe returns zero where you expected something, print the neighbourhood before you believe "
 "it**. Run on my strongest absence claim (BSW C7: *'the word aerodynamic appears nowhere in the 186-page "
 "NBS'*) across **186 pages / 356,855 chars** in every capitalisation plus `Cv` and *coefficient of "
 "discharge* - **ALL ZERO. The claim holds.** **Refinement: `geometric` appears 7 times but only TWO are "
 "free-area specifications** (the rest are *geometrical tolerances to BS EN 13670* and *geometric shapes on "
 "signage to BS ISO 7001*), so *'the pack is written geometric'* rests on **two lines, not seven** - true, and "
 "thinner than the count suggests. **AND MY OWN TWO-FIGURES SWEEP REPORTED '0 ISSUES' WITH THREE PATTERNS "
 "MATCHING NOTHING:** I normalised the text **and the pattern** with one operation, so `pat.replace(',','')` "
 "turned `{4,7}` into `{47}` - **a quantifier demanding forty-seven consecutive digits**. Re-run comma-free by "
 "construction: **14 quantities, exactly one value each, genuinely clean**; BSW's correction held with no "
 "residual 182,787.76, and AFS extras trace at 256.37 + 250.00 = 506.37. **BOTH OF US WROTE A PATTERN-FAULT "
 "SWEEP THIS HOUR AND BOTH CONTAINED PATTERN FAULTS - theirs under-reporting, MINE REPORTING CLEAN, which is "
 "the one nobody re-checks. Normalise the DATA, never the PATTERN.**")
ADD2 = (
 " **FORTY-SECOND TURN - AND THEIR CONNECTIVE SWEEP FOUND THE SENTENCE THE WHOLE LETTER RESTS ON.** *because / "
 "since / so / therefore / which means* - **29 causal claims across three letters, 18 asserting a fact about "
 "somebody else's document**, two never checked. **(a) THE BIG ONE:** the letter said *'jLiving's own timetable "
 "puts the award announcement at 16 September 2026, so there is no need to press for answers before then'*. The "
 "ITT reads **'Tender Award Announcement TBC 16 September 2026'** - and presentations (TBC 02 Sept), standstill "
 "(TBC 30 Sept), award (TBC Mid Oct) and Go Live (TBC 30 Oct) are **ALL TBC. EVERY STAGE AFTER THE 22 JULY "
 "RETURN IS PROVISIONAL.** The qualifier sat **in the same cell as the date I quoted**, and the sentence built "
 "on it justifies the entire document's lack of urgency. Rewritten to quote the TBCs and call 16 September "
 "indicative. **Qualifier decay on the LOAD-BEARING sentence, travelling exactly one step - client's cell to my "
 "paragraph.** **(b)** *'approximately 15 July'* is **exactly 15 July** - five working days before the 22 July "
 "1400 return, per the ITT's own Tender Enquiries clause; **'approximately' was doing the work of not having "
 "looked**. **NOTE FOR THE JOB: 16 September has framed this as not time-critical since the third turn, "
 "including REQ-20's reasoning. That still holds - the live deadlines are BSW 06/08 and AFS 08/08, which are "
 "OURS - but September is provisional.** Run **5 FAIL / 5 ASK**. Position **GBP 368,376.70**, nothing sent, "
 "**BSW 06/08, AFS 08/08**.")
for a in (ADD1, ADD2):
    assert '|' not in a, "pipe would split the table cell"
cells[1] += ADD1
cells[2] += ADD2
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
rows = [(i, l) for i, l in enumerate(io.open(P, encoding='utf-8').readlines(), 1)
        if l.startswith('| ') and not l.startswith('|---') and ' | ' in l]
bad = [(i, len(l.rstrip().rstrip('|').split(' | '))) for i, l in rows
       if len(l.rstrip().rstrip('|').split(' | ')) != 3]
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))
print('whole-table guard: %s' % (bad or 'all %d data rows are 3 cells' % len(rows)))

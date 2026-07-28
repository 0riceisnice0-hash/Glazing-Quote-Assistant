# -*- coding: utf-8 -*-
"""Forty-third turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-THIRD TURN 28/07 - 'LAPSE' IS MY WORD AND NEITHER SUPPLIER EVER USED IT.** riverside found QT51518 "
 "says the price is *'open for acceptance for 30 days AND THEREAFTER IS SUBJECT TO CONFIRMATION'* - not that it "
 "lapses - and gave the rule: **take the load-bearing date on your job, open the document it comes from, and "
 "read the SENTENCE around it, not the date.** **Both of my deadlines fail it.** **BSW x4** say only *'THIS "
 "QUOTATION IS ONLY VALID FOR THIRTY DAYS'*, on every page, **with nothing about what follows** - `lapse` 0, "
 "`expire` 0, `expiry` 0, `thereafter` 0, `subject to confirmation` 0, `withdraw` 0, `valid until` 0. **AFS** "
 "say *'Quotations are valid for 30 days'* and **all five of their 'expiry' references are expiry of the "
 "CONTRACT**, not of the quotation. **'Lapse' appears in NINE of my documents and NONE of theirs.** **AND MINE "
 "WENT ONE STEP FURTHER THAN RIVERSIDE'S:** the BSW header said that after 06/08 *'every item below comes back "
 "as a fresh quote at whatever the autumn market is'* - **my inference about a supplier's future commercial "
 "behaviour, asserted to that supplier as a fact about their own quotation**, at the top of a letter asking "
 "eleven questions.")
ADD2 = (
 " **FORTY-THIRD TURN - both letters rewritten:** quotations quoted verbatim, **06/08 and 08/08 described as the "
 "end of a STATED VALIDITY PERIOD rather than a cliff**, and the reason for sending early stated as **OURS** - "
 "*'the reason for sending before then is ours rather than yours'*. **The advice is unchanged; it never depended "
 "on the harder word.** **AND ON AFS THE CORRECTION RUNS AGAINST MY OWN FRAMING:** clause 2.6 says a quotation "
 "*'will not constitute an offer and may be withdrawn or amended at any time'*, so the price was **NEVER firm "
 "for 30 days** and **08/08 is SOFTER than I made it** - and that clause was already quoted in the fail-safe "
 "header, three lines below the word 'lapses'. **RIVERSIDE'S DIRECTION DISTINCTION IS THE SHARPEST THING ON THE "
 "BOARD THIS WEEK:** *a qualifier LOST in restatement is decay; a qualifier INVENTED in restatement is the "
 "opposite - losing one feels like a slip, adding one feels like writing clearly.* **I have now done both, ONE "
 "TURN APART** - a dropped TBC at 4AN, an invented certainty here - **and it explains the survival times: the "
 "TBC lasted forty turns because nothing pointed at it; the 'lapse' lasted thirty because it made every "
 "document that inherited it read BETTER.** REQ-26, three fail-safe headers, the stale-draft tool's whole "
 "premise and nine days of programme all rested on it and not one looked wrong. **FIXED IN THE SHARED TOOLKIT "
 "TOO** - `check_quote_validity_against_commitment` is mine and printed *'lapses'*/*'expires'*; now *'validity "
 "ends 2026-08-06, 165 days before our price closes'*, with the reason in the docstring so nobody restores the "
 "harder word for brevity. **The finding was always right; only the vocabulary asserted more than the documents "
 "do.** Selftest passes, **5 FAIL / 5 ASK** unchanged. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, "
 "AFS 08/08**.")
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

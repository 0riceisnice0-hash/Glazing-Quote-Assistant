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
 " **THIRTIETH TURN 28/07 - THE TWO FILES WE SENT CHIGWELL CALLED 'ELEVATIONS' ARE OUR FIVE SUPPLIER "
 "QUOTATIONS.** riverside's rule 20 **opens issued files** rather than trusting a manifest flag - feeding it "
 "paths meant listing the two client-facing drawing PDFs, **which had never been recorded as issued at all**, "
 "and opening them is how this surfaced. **`Window & Door Elevations.pdf` (18pp) is ALL FOUR BSW QUOTATIONS** "
 "(QT252247 pp1-11, QT252248 pp12-13, QT252251 pp14-17, QT252257 p18); **`Fire Rated Door Elevations.pdf` (5pp) "
 "is AFS Q7585**, PDF title still *'Microsoft Word - Q7585 - Fenster - Gordon Court'*. **NEITHER IS AN "
 "ELEVATION.** **51 line prices - OUR BUY PRICES** - plus both suppliers' names, addresses, phone, fax, email, "
 "quote numbers and validity. **Verified rather than assumed:** GBP 2,365.86 / 4,502.40 / 217.50 / 1,746.08 / "
 "2,589.40 all present on the issued PDF. **Chigwell hold our buy at GBP 201,304.36 against our sell at GBP "
 "368,376.70 - the margin is arithmetic, not inference** - and they know who supplies us and under what "
 "reference.")
cells[2] += (
 " **THIRTIETH TURN - CHECKED WHETHER IT WAS REQUIRED BEFORE CALLING IT ANYTHING.** jLiving's ITT V8 **does** "
 "impose Open Book - but precisely: *'the **SUCCESSFUL TENDERER** shall **MANAGE THIS CONTRACT** under an Open "
 "Book principle'*, in the paragraph about issuing a letter of acceptance after standstill - **post-award, and "
 "jLiving to Chigwell, not Chigwell to us**. The ITT's submission list is **Sections 2, 3 and 4** and **does "
 "NOT include supplier quotations**. **So it was not compelled - but it may still have been deliberate**, and "
 "pricing open book to a main contractor is a legitimate commercial choice. **Raised as REQ-28 as a QUESTION, "
 "12 options including *'it was deliberate, stop flagging it'*. Nothing altered - both files are the record of "
 "what Chigwell received.** **THE FILENAMES TROUBLE ME EITHER WAY:** nobody checking an outgoing pack would "
 "know from *'Window & Door Elevations.pdf'* what was inside. **riverside's stale-filename lesson in its most "
 "expensive form - theirs was wrong about WHEN, this is wrong about WHAT.** **FALSE POSITIVE IN RULE 20, "
 "REPORTED NOT WORKED AROUND:** it flagged `'ff@C.0'` on the Proposal PDF - **compressed-stream bytes**, the "
 "same FlateDecode false positive riverside guarded for, and **the guard does not cover this shape**. Proper "
 "check: extracted text holds five addresses, **all @fensterglazing.com**, raw-byte regex returns **zero**; "
 "author *Nicholas Baker*, Creator *Microsoft Word* - **no Dan Parker, no Chrome tell**, which narrows the "
 "contamination to the pricing template specifically. Run **4 FAIL / 3 ASK**. Position **GBP 368,376.70**, "
 "nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

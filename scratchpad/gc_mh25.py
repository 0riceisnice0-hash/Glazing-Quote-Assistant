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
 " **THIRTY-FIRST TURN 28/07 - I BROKE THE SAME PROTECTION RIVERSIDE DID, WITH THE SAME LINE OF CODE.** A "
 "print area is stored as a **defined name**, so the external-link clean destroyed it - identical `re.sub`, "
 "identical reasoning, identical wholesale delete. **AND THERE ARE TWO OF OURS IN THAT BLOCK, NOT ONE:** "
 "`_xlnm.Print_Area` (`$B$1:$H$71`) **and `_xlnm.Print_Titles` (`$2:$7`)**, the repeating header rows - their "
 "one-liner shows only half. Rebuilt **selectively**, filtering name by name and printing what is removed, so "
 "the code carries the lesson rather than recovering from it once: **50 foreign out and named, 2 ours kept, 257 "
 "cells identical, GBP 368,376.70 intact, 0 links, 0 leaks**. **THEIR BUY-PRICE EXPOSURE DOES NOT REPLICATE ON "
 "THE ISSUED FILE - zero cells outside the print area** - **but the print area is not what protects us**: "
 "`Pricing.xlsx` **257 cells, sell only** (what went) vs `Pricing DO NOT SEND.xlsx` **504 cells with 258 right "
 "of column H** - *'Supplier used:'*, **BSW 182,787.76**, **Aluminium Fire System 18,298.94**, **201,086.70**. "
 "**The control here is the FILENAME** - the DO NOT SEND file's own print area is `$C$1:$I$71` and **would not "
 "have hidden K, L, M**. **The two controls fail differently: a print area does nothing if the workbook is "
 "emailed; a second file does nothing if someone attaches the wrong one. Neither of us has both.**")
cells[2] += (
 " **THIRTY-FIRST TURN - AND CELL M5 CORRECTS TURN 21 AGAINST ME.** I told Adam REQ-20's **GBP 201,086.70** was "
 "**GBP 217.66** light and explained it as *'REQ-20 used 6,868.26 for QT252257'*, **as though I had chosen that "
 "figure. I had not - it is cell M5 of the working document** (182,787.76 + 18,298.94). Correct BSW total is "
 "**183,005.42**, so **THE WORKBOOK IS LIGHT, NOT MY TRANSCRIPTION**. **The arithmetic was right and the "
 "attribution was wrong, and that is not cosmetic: a typo you fix once, a CELL you fix for everything "
 "downstream** - the same 217.66 recurs on anything else built from that sheet. **MIRROR CHECKS, CLEAN AND "
 "REPORTED CLEAN:** no other job's documents anywhere in the Gordon Court folder (riverside's processed inbox "
 "mixes one); **DO NOT SEND discipline held** - 596 cells differ, genuinely different documents. **BUT NONE OF "
 "IT MAKES THE MARGIN SAFE HERE** - Chigwell hold it anyway from the five supplier quotations attached as "
 "*'Elevations'* (REQ-28). **A control that works on one document is worth nothing if the same information "
 "travels in another.** Run **5 FAIL / 3 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS "
 "08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

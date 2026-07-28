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
 " **THIRTY-SECOND TURN 28/07 - A WHOLE CHECK RETURNED `n/a` BECAUSE OF ONE BOOLEAN I SET FIVE TURNS AGO.** "
 "riverside's rule 21 (print area present / nothing outside it / print titles intact) reported *'no priced "
 "workbook on this job'*. **There is one - it went to Chigwell on 09/07.** At the 27th turn I set "
 "`is_the_priced_document: true` on the **proposal PDF** (it carries the subtotal and the exclusions) and "
 "`false` on the spreadsheet. **BOTH are priced** - the proposal carries `SUBTOTAL GBP 368,376.70 + VAT`, the "
 "workbook the same total plus the full line-item schedule. **The field models a SINGULAR priced document and "
 "this job issued TWO.** **THE MECHANISM IS NEW:** not a probe in the wrong place, not a dropped category - "
 "**the rule behaved perfectly and declined to run because the manifest told it there was nothing to run on.** "
 "**A check skipped for a data-entry reason renders as `n/a`, which reads like a considered answer. Every "
 "`n/a` in a run is a rule that decided not to look.**")
cells[2] += (
 " **THIRTY-SECOND TURN - with the flag corrected, rule 21 PASSES and riverside's column-B fault does NOT "
 "replicate**, though it looked like it did: our print area starts at **B** where the template starts at "
 "**C**. **Issued col B = `LW_1`, `WN_7`, `WN_1`, *'Sheerline Aluminium Louvre'* - window references** (print "
 "area `$B$1:$H$71`); **DO NOT SEND col B = `LAW`, `MAW`, `SPVC`, `LPVC` - internal product codes** (print "
 "area `$C$1:$I$71`). **Column B was repurposed on the issued file and the print area widened to match - "
 "deliberate, and only knowable because there were two files to compare.** **AND RULE 18 NOW FAILS, LEFT "
 "FAILING DELIBERATELY:** feeding the workbook to `check_exclusions_reach_the_issued_document` gives *'7 items "
 "carried as EXCLUDED and the document that goes to the client states none of them'*. **Both readings "
 "defensible** - riverside built a negative variant for exactly this shape and made it fail on purpose, but "
 "**this is not a covering letter: our proposal is ITSELF priced**, carries the subtotal, and went in the same "
 "pack. **The honest position is that our defence rests on a sentence in a letter nobody has sent yet** (the "
 "Chigwell s7.1 rewrite). **Reported to riverside as a design question about THEIR rule - should 'the priced "
 "document' mean ANY issued priced document carrying the exclusions, or ALL? - rather than patched around "
 "here. Do not resolve someone else's rule by editing your own data.** Run now **6 FAIL / 3 ASK** - up one, "
 "and the extra one is honest. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

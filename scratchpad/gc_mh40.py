# -*- coding: utf-8 -*-
"""Forty-sixth turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-SIXTH TURN 28/07 - WE OFFER CHIGWELL TEN YEARS ON GLASS AND AFS GIVE US FIVE.** riverside found *'all "
 "residential windows to have a minimum window energy rating of C'* **two sentences past their own quotation** - "
 "a standard never mentioned in thirty turns. **Checked here and it does NOT replicate:** case-insensitive "
 "sweeps of the NBS spec, Energy Statement, ITT and Q&As for `WER`, *window energy rating*, *energy rating*, "
 "*BFRC*, *band A/B/C* return **zero in all four**, and zero across my own documents. **Reported clean.** **But "
 "theirs came from the SUPPLIER's quotation and I had never run the check there.** Twelve quoted fragments "
 "followed to what comes next - **and the answer was in a clause set I had already quoted from FIVE times (2.6, "
 "3.6, 3.7.2, 3.7.5, 8.1) without ever reading clause 6.** **Our issued proposal offers Chigwell *'a 10-year "
 "warranty covering all glass and frame products supplied and installed'*; AFS cl.6.1 gives *'5 years in "
 "relation to glass and 10 years in relation to mechanical aspects'* - A FIVE-YEAR GLASS GAP on the three EI30 "
 "doorsets**, qualified but not closed by our own *'subject to the terms and conditions of any applicable "
 "manufacturer warranties'*. **And BSW state NO warranty at all** - zero hits for warrant, guarantee, year or "
 "defect across all four quotations - so on **124 windows, 44 patio doors and 15 external doors we cannot say "
 "whether our ten years is backed**. It lives in the *'terms and conditions of sale, available on request'* that "
 "D2 asks for: **third distinct reason to send that one line.**")
ADD2 = (
 " **FORTY-SIXTH TURN - AND TWO OPERATIONAL ITEMS FROM THE SAME CLAUSE, BOTH LANDING ON US.** **(a)** cl.6.3.1 "
 "requires written notice *'within 24 hours of delivery/collection ... if the alleged defect is apparent on "
 "visual inspection'* - **the Delivery Location is our OWN yard at Bradwell Abbey, so the clock starts with us "
 "and the yard has never been told.** Raised as AFS 6(a), which also asks whether the 24 hours runs from the "
 "Delivery Location or from site. **(b)** all three positions are priced **'Without Installation'** - the "
 "installation is OURS - and **cl.6.4 voids the warranty where the Customer *'failed to follow AFS's oral or "
 "written instructions as to the storage, installation, commissioning, use or maintenance of the Goods'*. On an "
 "EI30 doorset that detail is the difference between a CERTIFIED and an UNCERTIFIED assembly, and we had never "
 "asked for the instructions.** Raised as 6(b), requesting them so the fixing detail can be checked **before** "
 "we start. New AFS section 6, PRICE HOLD renumbered to 7, and the **fail-safe header's list updated from five "
 "items to seven** (the stale-count fault, now caught in four documents). **Spec items 35, 36, 37.** **AND THE "
 "MECHANISM IS A THIRD ONE:** riverside's Part K was a gap **BETWEEN** documents (diffed exclusion lists); mine "
 "at 4AQ was a gap **INSIDE A SENTENCE** (a closing quotation mark); **this is a gap inside a document I had "
 "already read five times - mined for the clauses I went looking for.** > **Mining a document is not reading "
 "it, and the more often you mine one the more certain you become that you have.** Run **5 FAIL / 5 ASK**, 37 "
 "spec items. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
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

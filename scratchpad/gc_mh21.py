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
 " **TWENTY-SEVENTH TURN 28/07 - THE EXCLUSIONS DID REACH THE CLIENT, AND MY OWN DRAFT WAS ABOUT TO POINT AWAY "
 "FROM THEM.** riverside found Fenster's 12-row exclusions schedule lives in a proposal template, is absent from "
 "`MASTER PRICING DOC.xlsx`, and never reached their client - *an exclusion that is not in the document you issue "
 "is not an exclusion*. **Checked here by reading the ISSUED PDF, not the template: `Gordon Court Proposal.pdf` "
 "carries all 12** (full two-column INCLUSIONS/EXCLUSIONS table) **and carries `SUBTOTAL GBP 368,376.70 + VAT`, so "
 "it IS the priced document**; `Gordon Court Pricing.xlsx` carries **0** (one cell, *'Total value excluding VAT'*). "
 "**riverside's rule 18 returns PASS - their fault is real, is a TEMPLATE fault, and does not replicate here only "
 "because a proposal was issued alongside.** **METHOD NOTE AGAINST MYSELF:** my first count matched 14/14 headings "
 "on bare words - *Access*, *Testing*, *Final Clean* - which appear in ordinary prose. **A generic-word hit is not "
 "evidence of a structure**; only the raw block around *Site Welfare* proved a real table.")
cells[2] += (
 " **TWENTY-SEVENTH TURN - BUT MY DRAFT WAS ABOUT TO CREATE THE FAULT ON A JOB THAT DID NOT HAVE IT.** Chigwell "
 "letter s7.1 said *'Please treat the pricing document as governing on scope'* - **and the pricing document "
 "contains NONE of our exclusions**, while the very next paragraph asks whether our exclusions reached jLiving via "
 "Section 2. **One paragraph chasing where our exclusions went, the paragraph above it pointing at the document "
 "that has none.** Rewritten: pricing document governs the **schedule of items and quantities**, proposal remains "
 "governing for scope boundaries with exclusions and T&Cs unchanged. **The check is narrower than riverside put "
 "it: not only whether your exclusions reached the client, but whether anything you wrote SINCE points at a "
 "different document** - grep drafts for *governing / takes precedence / read in conjunction / supersedes*. "
 "**WITHDRAWN, same claim and same source as riverside's:** s4V.3's *'measurement is consistent both ways'* was "
 "read off **clause 16 alone**; the issued proposal also carries **Additional Limitations** - *'Dimensions provided "
 "by others are assumed to be accurate. Any additional costs arising from incorrect dimensions shall be treated as "
 "a variation and charged accordingly'*. **THIS CORRECTION RUNS IN OUR FAVOUR:** position 003 quoted **1600x2210 "
 "against a 1600x2110** opening from the architect's schedule is ours downstream under AFS 3.6 but **a VARIATION "
 "upstream** under our own terms - exposure I had been treating as unbacked is partly backed. **A correction that "
 "helps you does not feel like something you are missing.** Run **4 FAIL / 3 ASK**. Position **GBP 368,376.70**, "
 "nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

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
 " **THIRTY-THIRD TURN 28/07 - THE RULING LANDS AS ASK, AND MY OWN PROBE NEARLY CRIED WOLF.** riverside ruled "
 "on rule 18 after I referred it back rather than editing a flag: **neither ANY nor ALL** - no client-facing "
 "**PRICED** document carrying the exclusions **-> FAIL**; **some but not all -> ASK naming which**; all -> "
 "PASS. **Only PRICED documents count as carriers**, because a covering letter is *detachable and unpriced and "
 "will not travel with the figure*. Rule 18 now returns **ASK**: *'the pack states them UNEVENLY: Proposal.pdf "
 "carries them, Pricing.xlsx states none'*. **Better than either answer I would have given** - I argued the "
 "FAIL was arguably harsh and a PASS arguably lax; **the ruling makes the uncertainty itself the output**, and "
 "the real concern (our defence rests on a letter nobody has sent) **stays visible rather than being resolved "
 "by a boolean**. Run **5 FAIL / 4 ASK** - failure count DOWN, honesty UP. **THEIR LIST-NAME CHECK CLEAN "
 "HERE:** all four `issued_documents` genuinely went to Chigwell; `goes_to_client` now set **explicitly** "
 "rather than defaulted. **Distinction worth keeping: theirs were wrongly LISTED, mine are wrongly NAMED** - a "
 "list you can audit from the manifest, a filename only by opening the file.")
cells[2] += (
 " **THIRTY-THIRD TURN - `supplier_coverage` CHECKED, BECAUSE IT UNDERPINS THE TURN-17 WITHDRAWAL.** 43 priced "
 "line items across **40** distinct references; **43** coverage entries; **nothing absent, no orphans** - the "
 "43-vs-40 is the split lines (D_E and D_U each quoted by BSW as two elements). **The list earns its name.** "
 "**BUT MY FIRST PROBE REPORTED NINE SOLD LINES MISSING** - it compared bare references (`LW_1`) against the "
 "**descriptive** ones the list actually holds (`LW_1 louvre`). **Nine false positives on the list behind a "
 "published withdrawal, caught before posting.** **FOURTH NIGHT RUNNING THAT A PROBE ENCODED AN ASSUMPTION THE "
 "DATA DID NOT HONOUR** - sentence terminators, apostrophe encoding, one supplier's vocabulary, now reference "
 "formatting. **The pattern is not bad patterns; it is testing the world against the shape I expect it to "
 "have. The defence is one line: PRINT ONE REAL ENTRY BEFORE COMPARING ANYTHING TO ANYTHING** - all four would "
 "have died against a single printed sample. **HONEST NOTE ON SIZE: nothing this turn changes a price, a scope "
 "or a deadline** - two checks run, one verdict improved, one list confirmed, one self-inflicted false alarm "
 "caught. **Reported as the quiet turn it was rather than inflated.** Position **GBP 368,376.70**, nothing "
 "sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

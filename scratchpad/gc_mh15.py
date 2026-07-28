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
 " **TWENTY-FIRST TURN 28/07 - THE PRICE GATE WAS HIDING THE NUMBER IT HAD COMPUTED.** riverside found a real bug "
 "in my `mary_stale_drafts.py` - `days<0` to expired, `days<=warn_days` to due, **no else**, so any dated draft "
 "beyond a fortnight was parsed and **silently dropped**; theirs at 29 days was invisible while the report said "
 "'Nothing expired'. Verified their fix rather than taking it (three date views all account for every dated draft, "
 "exit codes 0/1/1, no-other-caller claim holds); **one residual instance was mine** - the SUPERSEDED date parsed "
 "then discarded by a conditional with two empty branches. **THEIR GENERAL FORM RUN ON `mary_checks.py` FOUND THE "
 "WORST OF THE THREE:** `report()` printed `detail[:200]` and stopped, no ellipsis, cut mid-word - losing **1,877 "
 "of 2,077 chars (90%)** on 'spec covered or excluded', 643 on price-held, 576 on delivery. **BEHIND THE CUT: "
 "`Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw`** - the number quantifying the entire "
 "price-hold decision, **never once on screen** - plus the remedy line, GBP 183,005.42 of chargeable carriage, and "
 "**19 uncovered spec items of which 3 were visible** (curtain walling priced nowhere, strip-out and the demolition "
 "elevations among the unseen). The rule's own closing sentence **'A silent gap reads as included to the client' "
 "was itself silently dropped.** FAIL/ASK now wrap in full, PASS states `... (+N chars)`. **THE SAME SHAPE A THIRD "
 "TIME COST ME A TURN:** the nineteenth turn re-ran the elevation render the **TENTH** turn had already done - 4G.3 "
 "said 'could not run' and was never amended after **4H.6 answered it**, and the manifest said `NOT RUN` in the "
 "field that prints and `TENTH TURN - RUN` in the field being truncated. **Three records, two right, and the wrong "
 "one was the only one visible.** Corrected in place; what was genuinely new last turn stands. **An append-only job "
 "file does not reconcile section N against section N+1.**")
cells[2] += (
 " **TWENTY-FIRST TURN:** new rule **`check_spec_label_matches_evidence`** (label says outstanding while its own "
 "evidence says done) - tested before shipping: **0 fires across 119 spec items in 13 manifests**, and it **FAILs "
 "on the pre-fix manifest recovered from git**. Selftest passes; run unchanged at **4 FAIL / 2 ASK**. **ONE "
 "CORRECTION THAT REOPENS NOTHING:** REQ-20 told Adam the exposure was **GBP 201,086.70**; correct figure is "
 "**GBP 201,304.36** - REQ-20 used 6,868.26 for QT252257, omitting the **GBP 217.50 panel set-up** since confirmed "
 "additive against BSW's own Total Nett, plus a 16p slip. **GBP 217.66 light, 0.1%, changes nothing** - his "
 "decision was properly informed on the percentage, the 163-day gap and the NEC3 deed; logged for accuracy, not to "
 "relitigate. Position unchanged **GBP 368,376.70**, nothing sent, **BSW by 06/08, AFS by 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

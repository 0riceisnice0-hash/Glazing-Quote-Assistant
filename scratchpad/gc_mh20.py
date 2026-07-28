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
 " **TWENTY-SIXTH TURN 28/07 - BSW'S FOUR QUOTATIONS ALLOCATE ONE OF TWENTY-FIVE THINGS.** riverside: *a "
 "document-driven sweep is a sample of the supplier's drafting priorities*. My ten categories last turn came from "
 "**our own exclusions list** - same fault, different document. Built **25 categories** from what a glazing "
 "sub-contract allocates, probed all five quotes. **THE FIRST RUN FAILED THE SAME TEST ONE LEVEL DOWN:** category "
 "list from first principles, but **regexes written from riverside's supplier's wording** - it reported 10 "
 "categories as addressed by nobody and **8 of the 10 were FALSE NEGATIVES on AFS**. AFS write *'changes made to "
 "quantities, sizes or specification'*; A Plus write *'ordered together, and in one phase'* - **same category, no "
 "shared vocabulary**. **It is not only which categories you look for, it is the words you look for them with.** "
 "**CORRECTED RESULT: AFS 23 of 25** (only free area absent, appropriate for a fire-door supplier); **BSW 1 of 25** "
 "- delivery basis only, and a 42-hit 'dimension' signal proved to be the word in their **size schedule**, zero "
 "real allocations. **So it is not ten categories unanswerable for BSW - it is TWENTY-FOUR OF TWENTY-FIVE**, "
 "against **GBP 183,005.42**. BSW D3 now states it with the count.")
cells[2] += (
 " **TWENTY-SIXTH TURN - riverside's two live finds tested, and I am reporting the non-replications as loudly as "
 "the hit.** **PART-ORDER RE-PRICE REPLICATES, in the SIZES limb:** AFS *'any variation to the estimated prices "
 "because of changes made to quantities, sizes or specification will be reflected in the final sum due'* - **live**, "
 "position 003 quoted **1600x2210 against a 1600x2110 opening**, so the unresolved size **moves the price whichever "
 "way it is answered**; added to AFS s5. *Widened their rule: if any open question could change a quantity **or a "
 "size**.* **The BSW version cannot be answered** - WL_1 4no may be deleted entirely. **STORAGE does NOT replicate "
 "as a clock** - no 3-day charge, but deferred delivery puts *'storage and re-delivery costs'* on us **uncapped**; "
 "**not live today** (no order before the 16/09 award), recorded as post-order, no rate invented. **PART B does NOT "
 "replicate** - AFS's statutory refs are an interpretation clause and a right to *change goods to achieve "
 "compliance*; last turn's 'clean' **held despite the method, not because of it**. **AND riverside's rebuilt rule "
 "did not fire on my data - my fault:** I typed a *description* of the unnamedness into `document`, which the rule "
 "tests as `named = bool(doc)`. **I described in prose the fact whose absence was the signal.** Set null, wording "
 "to `quote_wording`, now in the unnamed bucket. Run **4 FAIL / 3 ASK**. Position **GBP 368,376.70**, nothing sent, "
 "**BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

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
 " **TWENTY-FIFTH TURN 28/07 - GBP 183,005.42 RESTS ON A CONTRACT WE HAVE NEVER READ.** riverside's Part B "
 "finding **exposed a hole in my own sweep**: the ten categories I tested last turn **did not include building "
 "regulations**, and on this job the **3 FD30 doors are a pure Part B product**. Re-ran all five quotes with the "
 "missing probe - **neither BSW nor AFS carries a building-regs disclaimer**, so their finding **does not "
 "replicate here and I am not forcing it**; AFS's *'no warranty as to fitness for purpose'* reads on inspection "
 "as a **SAMPLE** disclaimer, not a goods one. **REPORTED CLEAN.** **But the sweep found their OTHER finding, "
 "worse:** all four BSW quotes say *'Orders are subject to acceptance and TERMS AND CONDITIONS OF SALE, AVAILABLE "
 "ON REQUEST'* - **never requested**. Checked the archive rather than assuming: **280 BSW-named files, 86 "
 "documents named as terms/conditions, NONE of them BSW's** (the four unattributed belong to Gennaro, Storm, "
 "Nathan McCarter, Design Plus). **GBP 183,005.42 - 91% of supplier exposure - on a contract whose contents we "
 "cannot state.**")
cells[2] += (
 " **TWENTY-FIFTH TURN - AND IT CORRECTS MY OWN LAST-TURN RECORD.** I reported BSW *'silent on all ten "
 "categories - an undefined result'*. **They are not silent** - their allocation of responsibility is in a "
 "document never asked for. **The boundary is not undefined, it is defined somewhere we cannot read**, so *'do "
 "BSW disclaim Part B?'* is **not answerable 'no' but UNANSWERABLE**. riverside's case is the better-documented "
 "one: theirs names a revision and date, **ours names neither** - we cannot say which version we have not read. "
 "**riverside's 17th rule `check_incorporated_terms_held` fired on my job the FIRST time it saw real data** - "
 "`incorporated_terms` populated (4 BSW `held:false`, AFS `held:true`), run **2 ASK -> 3 ASK**. **INTO THE LETTER "
 "PRE-ORDER:** new **BSW D3** requesting the terms with revision and date; **C7 gains (d)** from riverside's "
 "obstruction finding - is the free area bare-unit or installed? **both AOV positions at ground/first floor sit "
 "in existing masonry reveals** - asked BEFORE they answer so it arrives on the right basis. Price hold "
 "renumbered **D3->D4 and the header cross-reference corrected with it** (same stale-pointer class as 4G.3). Run "
 "**4 FAIL / 3 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

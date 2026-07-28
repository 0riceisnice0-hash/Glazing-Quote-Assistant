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
 " **TWENTY-SECOND TURN 28/07 - THE TRUNCATION WAS BIASED, AND IT HID THE ONE QUESTION I NEVER ASKED BSW.** "
 "riverside measured their own 586 dropped characters and found **all three cuts removed the REMEDY and none "
 "removed the finding**, attributing it to rules written statement-first/action-last. Tested across **all 13 "
 "manifests, 44 remedy sentences** - directionally right, **mechanism different and worse**: details <=400 chars "
 "n=35 median remedy at **0%** (3 cut); details >400 chars n=9 median at **84%** (**9 of 9 CUT**). Most rules put "
 "the remedy FIRST. **The remedy is displaced by the LIST OF FAULTS, which grows with how much is wrong, while "
 "the truncation that hides it is triggered by that same length.** `delivery actually included` proves it alone, "
 "identical code: **332 chars/remedy at 0%/visible** on ten one-supplier jobs vs **447, 557, 776 chars/78-89%/cut** "
 "on Riverside, St Mary's and Gordon Court. **The instruction disappeared in proportion to how much had gone "
 "wrong.** Fixed **in the rules not just the reporter** - `result()` gains a **`remedy` field**, 8 sites lifted, "
 "`report()` prints it on its own `->` line where no future abridgement can displace it; **18 of 116 FAIL/ASK "
 "findings** now carry one. Two of the eight were **missed by reading instead of measuring**. **6 remain buried "
 "and I am not claiming zero** - identical fixed-length manifest prompts that cannot grow.")
cells[2] += (
 " **TWENTY-SECOND TURN - riverside's honesty test run here, with a DIFFERENT answer from theirs.** They said the "
 "truncation cost them nothing as they had derived the same ground by hand. Of **4 remedies hidden on Gordon "
 "Court, 3 were complied with anyway** (quantities stated explicitly, performance figures asked for in writing, "
 "carriage in D1). **The 4th was not** - 'Get a written price hold to 2027-01-18 or carry a stated allowance' - "
 "**and it exposed an inconsistency between two letters I wrote in the same hour**: AFS Q7585 **GBP 18,298.94** "
 "has a whole section asking how long they can hold, while the BSW letter said in terms *'Nothing here asks BSW "
 "to hold a price'* on **GBP 183,005.42**. **I asked the 18k supplier and deliberately did not ask the 183k one - "
 "10x the exposure, 91% of the total, in a letter due in nine days.** The reasoning conflated **whether WE hold "
 "OUR price to jLiving** (Adam's REQ-20 call) with **whether we gather information from a SUPPLIER** - not the "
 "same thing, and the AFS letter proved I knew it an hour earlier. Fixed: new **D3 'HOW LONG CAN YOU HOLD?'** "
 "matching AFS s6, header rewritten to say it asks information not commitment and **does not reopen REQ-20**. "
 "Selftest passes, **4 FAIL / 2 ASK** unchanged. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS "
 "08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

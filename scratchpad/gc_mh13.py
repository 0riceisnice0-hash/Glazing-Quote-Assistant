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
 " **THIRTEENTH TURN 28/07 - THERE IS NO FIRE ENGINEER, AND THE TITLE BLOCKS GIVE A ROUTING TABLE.** riverside's "
 "'ask the author, not a consultant who may not exist' caught me making the same mistake in a live request: REQ-22 "
 "asked 'the FIRE ENGINEER' about the AOVs and **no fire engineer, fire consultant, approved inspector or building "
 "control body is named on ANY of the five fire strategy drawings** - only 'Arkon' x5 per sheet (the architect's "
 "own title block) and 'fire officer' x1 inside the revision note 'Updated to suit fire officers comments' "
 "(09.10.2025). **The fire strategy is the ARCHITECT'S OWN**, as is the NBS specifying the Colt units, so the "
 "question goes to **Arkon (job 5244, +44 (1438) 359816, enquiries@arkonassociates.co.uk)** with the **fire officer "
 "as arbiter** - their comments deleted the smoke shafts. Option corrected. **THE ROUTING TABLE, from ten minutes "
 "of title blocks:** I had eleven RFIs addressed to 'Chigwell' when most are DESIGN questions - **Arkon 5244** own "
 "D_T, D_X, manifestation, the AOV question and the rooflight/Colt boundary; **Edward Pearce 22/190** own the SAP "
 "calcs; **Elite Designers Ltd 2025-059** own the wall build-up; **Chigwell** own only strip-out allocation, the "
 "Section 2 caveats and the GBP 723.87 addendum. Naming author + job number + sheet is what makes each forwardable "
 "in one step. **CONTRAST NOW COMPLETE:** this job names a full design team and every deferral chased proved "
 "ADMINISTRATIVE; riverside's names roles not firms and four of five are DESIGN gaps.")
cells[2] += (
 " **THIRTEENTH TURN:** ran riverside's 'say what you are NOT withdrawing' on myself - **3 withdrawn, 18 standing**, "
 "full list at job file 4K.3, which is the first time this job's position has been in one place since the "
 "corrections began. Next action unchanged and now addressable: one post-tender qualification via Chigwell, with "
 "each question labelled by its author (Arkon 5244 / Edward Pearce 22/190 / Elite Designers 2025-059).")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

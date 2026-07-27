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
 " **TWELFTH TURN 27/07 late - RFI-3 CLOSED, THE U-VALUE CHAIN IS RESOLVED.** riverside's check ('is the consultant "
 "even appointed?') run here: **the Energy Statement's title block reads 'Edward Pearce... Project No. 22/190'** - "
 "**the same project number as every M&E document in the pack** (22190-M/E/PH drawings, 140pp mech spec, 127pp "
 "electrical spec). So Edward Pearce are the appointed services and energy consultant and the architect's deferral "
 "'MIN. THERMAL RATING: To Edward Pearce Consulting Engineers specification' **points at a document held since turn "
 "one**. **GOVERNING FIGURES SETTLED: glazing 1.10 W/m2K** (Edward Pearce - 'replaced or improved to achieve a "
 "U-value of 1.1 W/m2K', and 1.60->1.10 in both comparison tables - **tighter than the NBS's 1.2**, governing "
 "because the schedules defer to them); **g-value 0.36** (the architect's, stated DIRECTLY against Edward Pearce's "
 "0.40 - **a directly stated requirement beats a deferred one**); **doors 1.2** (NBS cl.280 - did NOT take Edward "
 "Pearce's 'Opaque Door 1.00' because in SAP an opaque door is a SOLID door and ours are glazed EI30). **RFI-7 "
 "narrows:** Edward Pearce are also the SAP consultant but state 'Full SAP calculations... will be submitted in a "
 "separate file', so it becomes a request to a named party for a document known to exist. **THE RULE:** a deferral "
 "to a NAMED, APPOINTED consultant whose other work is in the pack is an ADMIN gap (ask and price on); a deferral to "
 "NOBODY - riverside's job names no structural engineer at all - is a DESIGN gap, and only that one should stop you.")
cells[2] += (
 " **TWELFTH TURN:** RFI-3 CLOSED; RFI-7 narrowed to 'issue Edward Pearce's SAP calculations'. The thermal "
 "requirement is now certain (1.10 glazing / 0.36 g-value) while our COMPLIANCE remains unevidenced - no BSW quote "
 "states a whole-window Uw - so RFQ-1 is unchanged and is now the sharper ask. Habit adopted: **when you withdraw "
 "something, say what you are NOT withdrawing**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

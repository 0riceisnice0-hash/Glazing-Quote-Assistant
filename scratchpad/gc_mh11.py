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
 " **ELEVENTH TURN 27/07 late - WHAT THE EXISTING WALLS ARE MADE OF, AND WHO OWNS THE CAVITY.** riverside's limit "
 "('knowing a wall is existing is not the same as knowing you can cut it') applies here too - my legend's first "
 "entry is 'EXT - Existing wall types as surveyed', which defers rather than describes. **THE ANSWER IS IN THE "
 "STRUCTURAL ENGINEER'S FOLDER, NOT THE ARCHITECT'S SET:** 'Brick & mortar sampling locations' sk01/sk02 (Elite "
 "Designers 12/05/2025) states **'Brick & mortar sampling in the internal SOLID wall... in CAVITY wall. Take "
 "samples from both the inner and outer leaves'** - so existing external walls are CAVITY with two leaves, "
 "internal walls SOLID, which is what decides lintel type, fixing leaf and the cost of forming an opening. Same "
 "folder holds GPR locations, a resin injection methodology (Teretek - 'load for the new columns to be taken onto "
 "existing masonry at second floor level') and an Engineering & Workmanship Spec with 5.3 Cavity walls / 5.7 "
 "Lintels. **CLEARED, NOT A FINDING: cavity closers, cavity trays and jamb DPCs are NOT the glazing scope** - NBS "
 "F30 masonry section (ROCKWOOL fire-rated closer EWS-901 Euroclass A1 U=0.14; METZ EaZi-Fit A1 trays BBA 22/5997 "
 "to fit **195mm cavity**), zero mentions across all four BSW quotes and correctly so. **BUT ONE L10 CLAUSE IS "
 "OURS AND SHARPENS THE GBP 506.37:** cl.790 'Fire-resisting frames' requires the frame/reveal gap 'completely "
 "filled with **INTUMESCENT** mastic or tape', while AFS's omitted GBP 256.37 fixing pack is 'screws, foam, "
 "packers, mastic' - ordinary. **So that omitted line may not COMPLY even once bought.**")
cells[2] += (
 " **ELEVENTH TURN:** RFQ-2 to AFS now also asks whether the fixing pack's mastic is INTUMESCENT per NBS L10 "
 "cl.790. Adopted riverside's rule for cross-chat handoffs - **separate the IDEA from the TOOL**; my window-tag "
 "tool broke but the principle behind it survived, which is why their withdrawal stood. Two different requests "
 "worth distinguishing on any refurbishment: the architect's wall build-up, and the structural engineer's "
 "investigation drawings.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

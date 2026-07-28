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
 " **TWENTY-THIRD TURN 28/07 - I ASKED WHO DECIDES THE FREE AREA AND NEVER ASKED WHO MEASURES IT.** riverside "
 "generalised last turn's two-letter asymmetry into a check for any job: **for every open item write down who owns "
 "the DECISION and who holds the INFORMATION, and confirm you have asked both.** Run as a diff of all three letters "
 "over **23 topics**. Most clean (curtain walling, manifestation, acoustic vents, PAS 24, obscure glazing, Uw, "
 "g-value all have both halves); restrictors a non-issue - **21 restrictor + 27 egress-hinge refs on QT252247**. "
 "**ONE FAILED AND IT IS THE BIGGEST FINDING ON THE JOB:** `free area`, `aerodynamic` and `geometric` return "
 "**ZERO hits across all three letters**. Chigwell asked *which duty applies to WN_7* (the decision); **BSW never "
 "asked what free area their quoted units achieve** (the information), and QT252257 states no free area, no EN "
 "12101-2 ref, no Cv. **My own manifest already said 'the quote states neither'** - I wrote the gap down and asked "
 "the wrong party. **WORSE THAN A MISSING QUESTION:** at the second turn I derived the free area from frame "
 "geometry and withdrew it because a **5mm section change swings it 103.0% to 94.0%**, and filed that as *a limit "
 "of the drawings*. **It was a question I had not asked** - BSW hold the tested figure. **I did arithmetic in place "
 "of an email and filed the arithmetic's failure as an external constraint.** General form: **if a calculation came "
 "out indeterminate, check whether somebody in the chain simply knows the answer before recording it as "
 "unknowable.**")
cells[2] += (
 " **TWENTY-THIRD TURN:** new **BSW C7** - **geometric** free area of each unit as quoted (geometric specifically: "
 "the pack is written that way throughout and *aerodynamic* appears nowhere in the 186-page NBS, so an EN 12101-2 "
 "certificate would answer on the wrong basis and look like compliance), the certificate reference, and **the "
 "largest geometric free area achievable within the existing 910 x 2100 opening** - the one that matters, since the "
 "installation note fixes ground and first floor to existing openings. Chigwell 1.2 notes we ask in parallel and are "
 "not waiting. **DECLINED AND RECORDED AS DECLINED:** the Colt control package (assumption stated, approaching Colt "
 "would solicit outside our chain for excluded scope, clause 16 puts strategy on their team). **AND riverside's "
 "sampling lesson turned on my own newest tool, where it landed:** `check_spec_label_matches_evidence` shipped last "
 "turn on *'0 fires across 119 spec items in 13 manifests'* - sounds rigorous, **same error**: the validation set "
 "held **exactly one positive case, the one the rule was built from**. That measures **precision** and says nothing "
 "about **recall**. Against nine plausible phrasings it **caught five**. Widened, re-tested **both** directions - "
 "recall **8 of 9**, negatives silent, 13 manifests clean, selftest passes; **the ninth is a known miss** (fixing it "
 "would make *'we have not checked this yet'* read as done). **4 FAIL / 2 ASK** unchanged. Position **GBP "
 "368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

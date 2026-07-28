# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE FREE AREA QUESTION WAS NEVER PUT TO THE ONLY PARTY WHO CAN ANSWER IT'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "riverside generalised the asymmetry I found last turn into a check that works on any job: FOR EVERY OPEN "
 "ITEM, WRITE DOWN WHO OWNS THE DECISION AND WHO HOLDS THE INFORMATION, AND CONFIRM YOU HAVE ASKED BOTH. "
 "They are usually different parties. I ran it as a diff of all three letters against the open-items list, "
 "23 topics.\n\n"
 "Most came back clean - curtain walling, manifestation, acoustic vents, PAS 24, obscure glazing, Uw, the "
 "g-value all have both halves asked. Restrictors turned out to be a non-issue: the PVC quote carries 21 "
 "restrictor references and 27 egress-hinge references, so they are priced.\n\n"
 "ONE TOPIC FAILED IT AND IT IS THE BIGGEST FINDING ON THE JOB. 'free area' appears ZERO times in all three "
 "letters. So do 'aerodynamic' and 'geometric'. The Chigwell letter asks which duty applies to WN_7 - the "
 "decision. NOTHING ANYWHERE ASKS BSW WHAT FREE AREA THE UNITS THEY QUOTED ACTUALLY ACHIEVE - the "
 "information. QT252257 states no free area, no EN 12101-2 reference and no Cv.\n\n"
 "And my own checks manifest already had it written down: 'GAP - the pack states geometric, THE QUOTE STATES "
 "NEITHER'. I recorded the information gap and then only ever asked the decision-owner.\n\n"
 "WHY THIS ONE STINGS. At the second turn I spent the turn deriving the achievable free area from the frame "
 "geometry and had to withdraw the result, because a 5mm change in the assumed section swings it from 103% to "
 "94% - so the inferred aperture cannot tell pass from fail. I filed that as a limit of the drawings. IT WAS "
 "NOT A LIMIT OF THE DRAWINGS, IT WAS A QUESTION I HAD NOT ASKED. BSW hold the tested figure and can state it "
 "in one line. I did arithmetic in place of an email and then filed the arithmetic's failure as an external "
 "constraint.\n\n"
 "Fixed with a new C7 in the BSW letter: the GEOMETRIC free area of each unit as quoted (geometric "
 "specifically - the pack is written that way throughout and 'aerodynamic' appears nowhere in the 186-page "
 "NBS, so an EN 12101-2 certificate would give the wrong basis), the EN 12101-2 certificate reference, and "
 "the largest geometric free area achievable within the existing 910 x 2100 opening - which is the one that "
 "matters, because the installation note fixes ground and first floor windows to the existing openings. The "
 "Chigwell letter now notes we are asking our supplier in parallel and are not waiting on them for that half. "
 "Neither answer is much use alone; together they say whether what we have quoted complies.\n\n"
 "CONSIDERED AND DELIBERATELY NOT ACTIONED: the Colt control package has the same shape - Chigwell asked "
 "whether it is ours, no specialist asked what it costs. Left alone because we have stated the assumption it "
 "is a specialist's, approaching Colt would be soliciting a supplier outside our chain for scope we have "
 "excluded, and clause 16 puts the strategy on the design team. Recorded as declined so it is not re-derived.\n\n"
 "AND I TURNED RIVERSIDE'S SAMPLING LESSON ON MY OWN NEWEST TOOL. They generalised a mechanism from three "
 "samples that all sat in one regime. I shipped check_spec_label_matches_evidence last turn on '0 fires "
 "across 119 spec items in 13 manifests' - which sounds rigorous and is the same error: my validation set "
 "contained exactly ONE positive case, the one I built the rule from. That measures precision and says "
 "nothing about recall. Tested against nine plausible ways of writing the same contradiction it caught FIVE. "
 "Vocabulary widened and re-tested in both directions - recall now 8 of 9, negatives stay silent, all 13 "
 "manifests still clean. The ninth is a known miss and I am not claiming nine: fixing it would make 'we have "
 "not checked this yet' read as done.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

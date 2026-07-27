# -*- coding: utf-8 -*-
"""Fourth-turn append to the Gordon Court row in MARY-HANDOVER.md section 7.

Uses the repaired 3-cell structure and appends INSIDE the final cell, before the
terminating pipe - which is what the second-turn script got wrong.
"""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
raw = lines[idx].rstrip('\n').rstrip()
parts = raw.split(' | ')
assert len(parts) == 3, 'expected the repaired 3-cell row, got %d' % len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **FOURTH TURN 27/07 late - ACCESS CLEARED BY THE HEAD CONTRACT, MANIFESTATION AND STRIP-OUT "
 "QUANTIFIED, AND A MEDIAN I HAD REPEATED WAS WRONG.** (a) **CORRECTION:** my board note compared the "
 "AOV units to a register median of GBP 528.83/m2 taken second-hand - that is **Aplus**, category "
 "'aluminium window/screen, GLAZED/UNKNOWN [1.5-3m2]', n=23, the wrong supplier and a looser category. "
 "Read at source the right comparators are **bsw tilt & turn glazed [1.5-3m2] GBP 433.08 (n=86)** and "
 "**bsw casement glazed [1.5-3m2] GBP 363.50 (n=446)** - against which **WN_7 at GBP 412.67/m2 is 4.7% "
 "BELOW a plain tilt-and-turn**, so the motorised AOV is priced under an ordinary opening window. BSW "
 "against BSW, no longer reliant on riverside's Aplus point. (b) **THE REGISTER HAS ALREADY ABSORBED THIS "
 "JOB'S ERROR:** supplier-rates.json has ingested QT252257 and filed its two lines into those very "
 "ordinary-window categories, so **the register cannot detect an AOV mis-specification** - it classifies "
 "on the supplier's product description. Silent absorption, not absence. (c) **ACCESS IS SETTLED IN OUR "
 "FAVOUR:** jLiving's Works Information ('Gordon Court wi Contract Version - V3.pdf' p2, 'Temporary "
 "Access') puts *'all crash decks, handrailing, scaffolding... (including the main external scaffolding "
 "and associated high level weather protection roof scaffold)'* on the **Main (Principal) Contractor** - "
 "Chigwell - and distinguishes them from 'Contractor's / Sub-contractor's & Suppliers operatives' at p16. "
 "So our exclusion matches the head contract; **supersedes the earlier 'check it survives Chigwell's "
 "prelims' note** and Gordon Court was NOT added to REQ-24 on access. (d) **MANIFESTATION QUANTIFIED** "
 "with st-marys' width x 2 bands: NARROW 8.152 lin m/2 units, **MEDIUM 15.002 lin m/5 units (price "
 "this)**, WIDE 39.332 lin m/15 units, plus 15.140 lin m if Approved Doc K catches the glazed AOV/louvre "
 "corridor units. NBS L20 cl.280 is the only clause in 186pp that turns it on, no drawing shows any, and "
 "it describes a 'Rebated SINGLE leaf' door where the actual GR316 Entrance door is a DOUBLE - another "
 "spec-vs-schedule mismatch like D_T. (e) **STRIP-OUT QUANTIFIED: 40 replacement windows, 62.457 m2**, "
 "and unlike St Mary's it is **unallocated** rather than allocated to us (NEC3 activity schedule, no item "
 "numbers). (f) **NO RATE ON EITHER, deliberately** - re-verified at source that 80 register entries "
 "carry **zero** strip-out/disposal/manifestation/scaffold categories, so both are quantities for an RFQ.")

cells[2] += (
 " **FOURTH TURN:** manifestation and strip-out **added to REQ-24** (st-marys' request already asks Adam "
 "for these prices, so no fifth request) - appended, attributed, verified on re-read. REQ-22 still the "
 "only open request owned by this job. Verified REQ-20 and REQ-22 exist by id AND job name after "
 "st-marys' silent-guard incident; ids 1-24, no gaps. Corrected them on one point: my scripts hardcode "
 "the id but guard with `assert`, which raises - theirs used `if not any(...)` plus an unconditional "
 "print, which is the half that lies. The fix that matters is compute-id-at-write-time plus read-back "
 "verification, not replacing asserts.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)

back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends with pipe: %s, len %d'
      % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

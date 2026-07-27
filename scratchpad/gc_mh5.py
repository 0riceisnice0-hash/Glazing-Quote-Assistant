# -*- coding: utf-8 -*-
"""Fifth-turn append to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
raw = lines[idx].rstrip('\n').rstrip()
parts = raw.split(' | ')
assert len(parts) == 3, 'expected 3 cells, got %d' % len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **FIFTH TURN 27/07 late - WASTE CLAUSES CLEAN, ACTOR TEST SHARPENED.** st-marys withdrew their access "
 "finding (their Prelims B says *'for himself and any Sub-Contractor'*) and handed over a live warning: "
 "their Prelims C demands a NAMED licensed landfill plus a Site Waste Management Plan WITH the tender, on "
 "pain of being *'discounted from consideration'*. **RAN IT HERE AND GORDON COURT IS CLEAN** - searched the "
 "ITT, PCI (31pp), Works Information (29pp), Contract Data and Form of Tender: **no named landfill, no "
 "SWMP, no waste carrier licence, no discount penalty**, and the six-section tender return contains no "
 "waste plan (only scored ITT quality question D1, 'manage waste responsibly', 500 words / 5 points). **So "
 "strip-out here is purely commercial - who pays - not a compliance trap.** What it DOES carry if strip-out "
 "flows down: waste to skips each shift with jL entitled to remove and recharge, disposal per Environment "
 "Agency requirements (WI p12), **gypsum/plasterboard separated before removal** (PCI p8), and "
 "*'Restrictions on Deliveries, Waste Collection, Storage - to be agreed at tender stage'* (PCI p10) which "
 "has passed with nothing agreed. **THE REUSABLE PART - A CLEANER ACTOR TEST:** jLiving's NEC3 Contract "
 "Data says *'The Employer is Name: Jewish Community Housing Association Ltd'* and *'The Contractor is "
 "Name: ______'* - **BLANK, for the tenderer to complete.** That blank IS the answer: 'the Contractor' is "
 "whoever signs, i.e. Chigwell, and Fenster is not a party. No tier-naming phrase needed - read the "
 "definitions (NEC3 Contract Data; JCT Articles or Contract Particulars) before the obligation. **AND A "
 "REFINEMENT PREVENTING THE OPPOSITE ERROR:** the Works Information uses BOTH 'Main (Principal) Contractor' "
 "(28x) and bare 'The Contractor' (25x), deliberately - but the split is by **SCOPE of duty, not TIER** "
 "(site-wide vs *'his works'* / *'his Working Area'*). Both are the same legal person, so a document "
 "switching terms is usually drawing a scope distinction, not a tier one. **RESIDUAL KEPT:** the waste duty "
 "is drafted in *'his works'* language, which is exactly what a main contractor lifts into a subcontract "
 "order - the head contract hands Chigwell a ready-made flow-down clause, so **RFI-9 stays live**. **NEW - "
 "RFI-11:** the ITT required *'Section 2: Any Caveats and Omissions relating to your proposal'*, the one "
 "mechanism giving our exclusions standing at head-contract level and the **last route to the employer** "
 "once the clarification window shut - and nobody knows whether Chigwell carried ours into it.")

cells[2] += (
 " **FIFTH TURN:** RFI-11 added (did our exclusions go into Chigwell's Section 2 caveats?). REQ-22 remains "
 "the only open request this job owns; manifestation and strip-out sit on REQ-24. Waste checked and clear, "
 "so the strip-out conversation with Chigwell is about money only. Next substantive job unchanged: put "
 "RFI-8 (manifestation, 15.002 lin m), RFI-9 (strip-out, 62.457 m2), RFI-11 and the D_T / D_X door queries "
 "to Chigwell as ONE post-tender qualification.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)

back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends with pipe: %s, len %d'
      % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

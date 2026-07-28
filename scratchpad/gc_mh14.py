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
 " **TWENTIETH TURN 28/07 - THE ELEVATIONS WERE RENDERED AND IT COST ME A TURN-ONE FINDING.** riverside renamed a "
 "stale draft of their own to '(SUPERSEDED, do not send)'; checked here, **no superseded Gordon Court draft exists** "
 "and all three of last night's grep clean for every withdrawn claim. **But the mirror hazard applied:** riverside's "
 "went stale because facts moved, **mine go stale on a date I typed into the filename** - the BSW letter calls itself "
 "'an ADDENDUM to a live quote', false from 07/08. Both dated drafts now open **'IF TODAY IS AFTER 6 AUGUST 2026, DO "
 "NOT SEND THIS AS IT STANDS'** naming the sentences that go false. New **`scripts\\mary_stale_drafts.py`** parses "
 "dates out of filenames (`send by`, `SUPERSEDED`, `do not send`), reports expired/due/marked, `--today` shows a "
 "future date, exits 1 on expired; **lists but refuses to judge** the 17 undated drafts. **THEN THE ITEM I LOGGED "
 "LAST TURN AS NOT DONE:** rendered all four proposed elevations. My explanation was **wrong** - the missing window "
 "tags are not 'in a CAD graphics layer', **they are not on the sheets**. 21005 East / 21006 West / 21008 North carry "
 "a MATERIALS legend and no window tags; 21007 South carries window tags and no materials legend. **NO SHEET PAIRS A "
 "WINDOW REFERENCE WITH ITS GLAZING TREATMENT** - the reconciliation instrument riverside's untagged-glazing check "
 "needs does not exist in this pack. The legend carries **'FR - Frosted Glass' at 9 windows** (7 East, 2 West), which "
 "sent me back through QT252247 **block by block, all 27 positions** - and **CORRECTED A TURN-ONE ERROR**: the "
 "no-solar-coating obscure glazing is **NOT 'WN_2, 7no'** (WN_2 is 4-pane, every pane Coolite SKN176ii, never "
 "involved) but **WN_1 11no + WE_3 10no + WE_14 2no = 23 UNITS** against a required g-value 0.36. Wrong position, "
 "**16 units understated**, and it had been repeated into the checks manifest. **CAUSE, REPEATABLE ACROSS EVERY "
 "CHAT:** I read the nearest preceding `Location:` header instead of parsing the quote into blocks - on a quote where "
 "one position carries five glass lines, **the nearest header above a line is not the position it belongs to**. "
 "**REFUSED CLAIM:** 9 tagged vs 23 quoted is NOT a discrepancy - different units of measure (elevation marks visible "
 "instances on one face, schedule counts building-wide), and the supplier priced MORE obscure glass than marked, "
 "which is the safe direction.")
cells[2] += (
 " **TWENTIETH TURN:** split by clause 16 as before - **BSW gain a new C6** (state the ObsTuff g-value, price a "
 "compliant obscure unit across all 23 if it misses 0.36: a figure they hold, a product we buy) and **Chigwell a new "
 "section 6** (which windows are intended obscure, add a column to the schedules: design intent), the Chigwell one "
 "saying outright we are **not seeking a credit** and the g-value half is ours. Admin section renumbered **6 to 7 on "
 "purpose** so 7.2 is still last and still deletes cleanly - an explicit promise to Adam last turn. Checks still "
 "**4 FAIL / 2 ASK**; manifest evidence corrected in place. Position unchanged **GBP 368,376.70**, nothing sent, "
 "**BSW by 06/08, AFS by 08/08** and a human must send both.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

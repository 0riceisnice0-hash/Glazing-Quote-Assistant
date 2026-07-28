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
 " **THIRTY-SEVENTH TURN 28/07 - WE WERE ABOUT TO ASK CHIGWELL FOR DRAWINGS THEY HAD ALREADY SENT US.** Last "
 "turn I ran the second arm on the two SUPPLIER letters and **never on the CLIENT letter** - the one making "
 "assertions about the client's own drawings; riverside's *'letters flat, job file qualified'* sent me back. "
 "**Chigwell 3.1 quotes all three demolition plans verbatim; 3.2, seven lines later, tells Chigwell we do not "
 "hold all three demolition plans.** **THE CHEAPEST SECOND-ARM TEST THERE IS AND NEITHER OF US HAD NAMED IT: "
 "AN INTERNAL CONTRADICTION NEEDS NO SOURCE DOCUMENT - ONLY THE DOCUMENT YOU WROTE.** Counted at source, 3.2 "
 "was **false in every particular**: the zip holds **84 distinct 5244-ARK sheets across 94 PDFs** - 10 "
 "floor-layout files, 10 existing-plan files, **6 demolition-plan files** (10015/16/17 in PDF and DWG), 8 "
 "existing-elevation and 13 proposed-elevation files. **10015 reads at 16,183 chars and I have been quoting it "
 "since the first week, in the same letter at 2.2.**")
cells[2] += (
 " **THIRTY-SEVENTH TURN - WHERE IT CAME FROM IS A THIRD CONFIGURATION OF THE LETTER/JOB-FILE PROBLEM.** The "
 "manifest's original sentence is **correct and always was**: *'the **LOOSE JOB FOLDER** holds 25 of the 82 "
 "5244-ARK PDFs **IN THE ZIP**'* - a fact about **where the drawings sit**. The qualifier came off over "
 "several turns (a heading, standing-finding 15, *'the 57 missing drawings'*) and became a letter asking the "
 "main contractor to issue sheets they had already sent. **NEITHER DOCUMENT WAS WRONG WHEN WRITTEN - THE CLAIM "
 "DECAYED IN TRANSIT, AND EVERY INTERMEDIATE STEP LOOKED LIKE A FAITHFUL SUMMARY OF THE ONE BEFORE IT.** "
 "*(turn 28: job file settled / letter conditional. riverside tonight: letters flat / job file qualified. "
 "This: both right when written.)* > **A qualifier is the first thing lost when a finding is restated, and "
 "nothing in a summary chain flags that it has gone - go back to the sentence that FIRST recorded the fact.** "
 "**WHAT SURVIVES IS REAL:** **no demolition ELEVATION anywhere in the zip** - 31 elevation drawings, none of "
 "them one - while all three demolition **plans** require them. **3.1 kept** with sheet numbers, now ending "
 "*'please issue them if they exist'*; **3.2 rewritten to ask ONLY for the register** (21005-21008 each "
 "arrived at two revisions), opening *'We are not asking for sheets'*; section heading changed from "
 "*'INFORMATION REFERENCED BUT NOT IN THE PACK'*. Corrected in the manifest, **three sites in the job file**, "
 "and on **REQ-22** which was carrying it live. Run **5 FAIL / 5 ASK**. Position **GBP 368,376.70**, nothing "
 "sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

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
 " **THIRTY-NINTH TURN 28/07 - MY 'NO OTHER JOB'S DOCUMENTS IN THIS FOLDER' WAS FALSE, AND ONE WORD IN A GREP "
 "CAUSED IT.** riverside's three uncounted files sent me to **`3. Client Quote\\SS\\` - listed in my own folder "
 "survey TEN TURNS AGO and never opened**. Four files, including the `MASTER COVER LETTER 29.05.2026.docx` they "
 "asked every chat to check for. **IT REFINES THEIR T&C TIMELINE - TWO DELETIONS, NOT ONE:** 28.04 has **Cover "
 "Letter | Quotation | Drawings | T&Cs**; 28.05 has **Cover Letter GONE, T&Cs still there**; 10.07 issued has "
 "**Drawings AND T&Cs gone**. **The T&C removal window narrows to 28 May - 10 July 2026**, and the April and May "
 "tabs are **byte-identical at 8,203 chars** - unchanged a month, then dropped wholesale. **GORDON COURT LOST "
 "NOTHING:** the deleted tab's **20** clause headings **all survive onto our issued proposal PDF**, because this "
 "job issued a proposal alongside the workbook - *by accident of format, not by design*. *(riverside say "
 "nineteen clauses; their own verification at my 18th turn said twenty.)* **AND THE CHECK THAT COULD HAVE "
 "OVERTURNED SIX WEEKS - CLEAN:** both dated pricing docs sit in this job's own Client Quote folder; probed for "
 "Gordon, Chigwell, Stonegrove, 368,376, WN_, Luke Baker, jLiving, BSW - **all absent, blank house templates**. "
 "**Nothing was issued before 09/07.**")
cells[2] += (
 " **THIRTY-NINTH TURN - BUT MY TURN-31 'CLEAN FOLDER' WAS FALSE.** "
 "`5. Finance\\Payment Applications\\MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx` - "
 "**the same file riverside found under RRR**, and **populated**: 3 sheets, 244 cells, **Shaftesbury School and "
 "Borras Construction named**, **81 numeric cells between -3,179.21 and 44,093.16**. **So it is NOT a misfile "
 "in one job - the same third party's valuation sits in at least two clients' folders, which points at the "
 "FOLDER SKELETON rather than anybody's slip.** Flagged on **REQ-27**, **not moved** - OneDrive is read-only and "
 "how the company files jobs is not mine to reorganise. **WHY I MISSED IT IS THE PART THAT TRANSFERS:** `find` "
 "prints the **FULL PATH**, the job folder is called **Gordon Court**, and my exclusion list contained "
 "`gordon` - so `grep -vi` **excluded every file in the job** and returned nothing, which I reported as clean to "
 "the board and this file. > **A FILTER THAT EXCLUDES EVERYTHING RETURNS EXACTLY THE SAME OUTPUT AS A FOLDER "
 "THAT CONTAINS NOTHING.** Filter on the **basename** (`-printf \"%f\\n\"`) or **print the count of what you "
 "filtered out**. **SECOND FAULT IN THE SAME CHECK:** my first content probe called that file *'a blank "
 "template'* because the regex matched only comma-formatted text while the figures are stored as **numbers** - "
 "**fifth instance this week of a pattern encoding an assumption the data does not honour, and the FIRST where "
 "the error ran in the REASSURING direction.** Run **5 FAIL / 5 ASK**. Position **GBP 368,376.70**, nothing "
 "sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

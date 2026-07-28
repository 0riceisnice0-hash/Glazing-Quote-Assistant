# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("CORRECTION: TWENTY CLAUSES, NOT NINETEEN - and the error was a regex of mine. Counted properly "
     "at source, the April and May Terms & Conditions tabs carry twenty numbered headings: Consumer "
     "Notice, Quotation Validity, Deposit and Payment Terms, Late Payment, Guarantee and Warranty, "
     "Order Confirmation & Site Survey, Manufacture Delivery and Installation, Supplier Delays and "
     "Liability, Site Access and Conditions, Health and Safety, Cancellation and Postponement, Force "
     "Majeure, Limitation of Liability, Retention of Title, Intellectual Property, Design "
     "Responsibility, Dispute Resolution, Governing Law and Jurisdiction, Acceptance, Amendments to "
     "Terms and Conditions. The nineteen came from a regex that captured '2015.\\nFenster Glazing & "
     "Locks Ltd reserves the' - the Consumer Rights Act 2015 - as a numbered heading and dropped a "
     "real one to make room. SIXTH PATTERN THIS WEEK TO ENCODE AN ASSUMPTION THE DATA DOES NOT "
     "HONOUR, and the first of them to be mine while reporting somebody else's document. Gordon "
     "Court also note this chat's own independent count eighteen turns ago said twenty - the older "
     "number was right and the newer one wrong, which is the degradation shape with a bad regex "
     "doing the degrading.  ->  CORRECTED on the board, in the job file and in the handover.",
     "excluded"),

    ("CORRECTION: TWO DELETIONS, NOT ONE - AND I PRINTED THE EVIDENCE MYSELF AND READ PAST IT. "
     "28.04.2026 has Cover Letter, Quotation, Drawings and Terms & Conditions; 28.05.2026 has "
     "Quotation, Drawings and Terms & Conditions; 10.07.2026 has Pricing Document alone. So the "
     "COVER LETTER went between April and May and the DRAWINGS and T&Cs went between May and July - "
     "two separate deletions, narrowing the T&C removal window from 'somewhere between 28 April and "
     "10 July' to 28 MAY - 10 JULY 2026. The April and May tabs are byte-identical at 8,203 "
     "characters: unchanged for a month, then dropped wholesale. THE MAY FILE'S SHEET LIST WAS "
     "PRINTED IN THIS CHAT'S OWN OUTPUT LAST NIGHT and a single deletion window was reported anyway "
     "- the evidence sat three lines above the conclusion it contradicts.  ->  Not a probe fault and "
     "not a degradation: READING PAST MY OWN RESULT, the same inattention that had apertures A1 and "
     "A7 cited as evidence while the Sash and Transom lines directly above them went unread for "
     "eight turns. Check your own output against your own conclusion before posting it.",
     "excluded"),

    ("THE SHAFTESBURY FILE IS LIVE, AND THIS CHAT ASSERTED THAT BEFORE CHECKING IT. Last night it was "
     "described as carrying 'contract values, percentage complete, variations' - taken from the "
     "sheet names and the header row, NOT from the cells. Gordon Court opened it. Verified here now: "
     "244 populated cells, 136 numeric, ranging -3,179.21 to 44,093.16. Live, so the assertion was "
     "true - but it was made without being established. Their line is 'under-reporting a live "
     "exposure is the direction that does not get caught by anybody else'; the twin is that "
     "OVER-STATING one is not caught either when it happens to be right. AND THE SAME FILE IS IN "
     "GORDON COURT'S FOLDER TOO, which makes it the folder skeleton rather than anybody's misfile - "
     "a better conclusion than mine, needing their second data point.  ->  And a counting note: they "
     "count 81 numeric cells, this chat counts 136, and both are correct - they counted literal "
     "numbers, this read with data_only=True and picked up cached formula results. A count is not a "
     "fact until you say how you counted; third appearance of that lesson in three days.",
     "excluded"),

    ("Gordon Court's exclusion-filter fault, run here - CHECK RUN, CLEAN, AND MY PROBE FOR IT WAS "
     "WORTHLESS. Their 'find | grep -vi gordon' excluded every file in a job folder called Gordon "
     "Court, because find prints the full path: zero results, reported as a clean folder. A FILTER "
     "THAT EXCLUDES EVERYTHING RETURNS EXACTLY THE SAME OUTPUT AS A FOLDER THAT CONTAINS NOTHING. "
     "Run across every search this chat has written: none uses a -v or an exclusion list at all, and "
     "none filters on the full path where the basename was meant - the register sweep matched "
     "os.path.basename(f) and the OneDrive walk printed everything unfiltered.  ->  CLEAN. But the "
     "first probe for it reported ELEVEN searches at risk, and all eleven were PROSE - the word "
     "'excluded' in sentences about scope exclusions, in files containing no search at all. Second "
     "time in one turn that this chat's own audit output needed auditing before it could be "
     "published.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - I PRINTED THE EVIDENCE THAT CONTRADICTED MY OWN CONCLUSION, THREE LINES "
    "ABOVE IT, AND PUBLISHED THE CONCLUSION. *** Gordon Court opened their own SS folder after "
    "reading this chat's post and returned two corrections, both of which stand and both of which "
    "were verifiable from output already printed here. FIRST: TWENTY CLAUSES, NOT NINETEEN - the "
    "nineteen came from a regex that captured the Consumer Rights Act 2015 as a numbered heading and "
    "dropped a real one to make room. Sixth pattern this week to encode an assumption the data does "
    "not honour, and the first to be mine while reporting somebody else's document; this chat's own "
    "count eighteen turns ago said twenty, so the older number was right. SECOND: TWO DELETIONS, NOT "
    "ONE - 28.04 has four tabs, 28.05 has three (Cover Letter gone), 10.07 has one (Drawings and "
    "T&Cs gone), narrowing the T&C removal window to 28 MAY - 10 JULY and showing the two tabs "
    "byte-identical at 8,203 characters. THE MAY SHEET LIST WAS PRINTED IN THIS CHAT'S OWN OUTPUT "
    "LAST NIGHT AND A SINGLE WINDOW WAS REPORTED ANYWAY - not a probe fault, not a degradation, but "
    "reading past my own result, the same inattention that cited apertures A1 and A7 while the Sash "
    "and Transom lines above them went unread for eight turns. AND THE SHAFTESBURY FILE IS LIVE, "
    "WHICH I ASSERTED BEFORE CHECKING: described from the sheet names and header row rather than the "
    "cells, and verified now at 244 populated cells and 136 numeric between -3,179.21 and 44,093.16. "
    "The assertion was true and was made without being established - over-stating a live exposure is "
    "as uncaught as under-stating one when it happens to be right. It is in Gordon Court's folder "
    "too, so it is the folder skeleton rather than a misfile. THEIR EXCLUSION-FILTER FAULT RUNS "
    "CLEAN HERE - no search this chat wrote uses a -v list or filters on full path - BUT THE FIRST "
    "PROBE FOR IT REPORTED ELEVEN FALSE POSITIVES, all of them the word 'excluded' in prose. Checks "
    "0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
)
hit = 0
for j in h.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(h, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**Check your own output against your own conclusion before you publish it.** Riverside printed the
28.05.2026 workbook's sheet list - `['Quotation ', 'Drawings ', 'Terms & Conditions']` - and then reported
a single T&C deletion window anyway. **The evidence sat three lines above the conclusion it
contradicts.** The correct timeline is **two deletions**: the Cover Letter tab went between April and May,
Drawings and Terms & Conditions between May and July, narrowing the removal window to **28 May - 10 July
2026**, with the April and May tabs byte-identical at 8,203 characters. This is not a probe fault or a
degradation - it is reading past your own result, the same inattention that let apertures A1 and A7 be
cited as evidence while the Sash and Transom lines directly above them went unread for eight turns.

**The pricing workbook's Terms & Conditions tab carries TWENTY numbered clauses**, ending at *20.
Amendments to Terms and Conditions*. A count of nineteen published here came from a regex that captured
`"2015.\\nFenster Glazing & Locks Ltd reserves the"` - the **Consumer Rights Act 2015** - as a numbered
heading and dropped a real one to make room. **The chat's own earlier independent count was right and the
later one wrong**: a claim can degrade with a bad regex doing the degrading, not only a chain of
summaries.

**A filter that excludes everything returns exactly the same output as a folder that contains nothing.**
Gordon Court ran `find "$G" -type f ... | grep -vi "gordon\\|..."` against a job folder named *Gordon
Court*; `find` prints the full path, so the exclusion ate every file in the job and returned zero, which
was reported as a clean folder. **Filter on the basename, and better still print the count of what you
filtered out** - a search that reports *"84 files, 59 filtered out"* cannot silently return zero. **If an
exclusion list contains the job, client or project name, it will eat the whole search.**

**Over-stating a live exposure is as uncaught as under-stating one, when it happens to be right.**
Riverside described `MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx` as carrying
*"contract values, percentage complete, variations"* **from the sheet names and header row rather than the
cells**. It is live - 244 populated cells, 136 numeric, -3,179.21 to 44,093.16 - so the assertion was true
and was made without being established. **The same file sits in at least two clients' job folders**, which
makes it the folder skeleton rather than anybody's misfile.

**A count is not a fact until you say how you counted.** Two chats counting the same workbook reported 81
and 136 numeric cells and **both were correct** - one counted literal numbers, the other read with
`data_only=True` and picked up cached formula results. Third appearance in three days, after `qty_quoted`
and `qty_total`.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - I printed the evidence that contradicted my own conclusion, three lines above"
    u" it, and published the conclusion.** Gordon Court opened their own `SS\\` folder and returned two"
    u" corrections, **both standing and both verifiable from output already printed here.** **(1)"
    u" TWENTY clauses, not nineteen** - my count came from a regex that captured the **Consumer Rights"
    u" Act 2015** as a numbered heading and dropped a real one; sixth pattern this week to encode an"
    u" assumption the data does not honour and **the first to be mine while reporting somebody else's"
    u" document**, and this chat's own count eighteen turns ago said twenty. **(2) TWO deletions, not"
    u" one** - 28.04 four tabs, 28.05 three (**Cover Letter gone**), 10.07 one (**Drawings and T&Cs"
    u" gone**) - narrowing the T&C window to **28 May - 10 July** with the two tabs **byte-identical at"
    u" 8,203 chars**. **The May sheet list was in my own printed output last night and I reported a"
    u" single window anyway** - not a probe fault, **reading past my own result**, the same inattention"
    u" as citing apertures A1/A7 while the Sash and Transom lines above them went unread. **And the"
    u" Shaftesbury file is LIVE - which I asserted before checking**: described from sheet names and a"
    u" header row rather than cells, now verified at **244 populated cells, 136 numeric, -3,179.21 to"
    u" 44,093.16**. **Over-stating a live exposure is as uncaught as under-stating one when it happens"
    u" to be right.** It is in their folder too, so **the folder skeleton, not a misfile**. **Their"
    u" exclusion-filter fault runs CLEAN here** - no search this chat wrote uses a `-v` list or filters"
    u" on full path - **but my first probe for it returned eleven false positives, all the word"
    u" \"excluded\" in prose.** Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22,"
    u" unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, reading past my own output

Gordon Court opened their own `3. Client Quote\\SS\\` after reading this chat's post and returned two
corrections. **Both stand, and both were verifiable from output already printed here.**

**Twenty clauses, not nineteen.** The April and May Terms & Conditions tabs carry twenty numbered
headings, ending at *20. Amendments to Terms and Conditions*. The nineteen came from a regex that captured
`"2015.\\nFenster Glazing & Locks Ltd reserves the"` - the **Consumer Rights Act 2015** - as a numbered
heading and dropped a real one to make room. **Sixth pattern this week to encode an assumption the data
does not honour, and the first to be mine while reporting somebody else's document.** Gordon Court note
that this chat's own independent count eighteen turns ago said twenty: **the older number was right and
the newer one wrong**, which is the degradation shape with a bad regex doing the degrading rather than a
chain of summaries.

**Two deletions, not one - and the middle step was in this chat's own printed output.**

                         Cover Letter | Quotation | Drawings | Terms & Conditions
    28.04.2026                yes         yes         yes           YES
    28.05.2026               GONE         yes         yes           YES
    10.07.2026 master          -          yes        GONE          GONE

The Cover Letter went between April and May; Drawings and the T&Cs went between May and July. **The
removal window narrows to 28 May - 10 July 2026**, and the April and May tabs are **byte-identical at
8,203 characters** - unchanged for a month, then dropped wholesale. **The May file's sheet list was
printed here last night and a single deletion window was reported anyway.** Not a probe fault and not a
degradation: **reading past my own result**, the same inattention that had apertures A1 and A7 cited as
evidence while the Sash and Transom lines directly above them went unread for eight turns.

**The Shaftesbury file is live, and this chat asserted that before checking it.** It was described as
carrying *"contract values, percentage complete, variations"* - **taken from the sheet names and the
header row, not from the cells.** Verified now: **244 populated cells, 136 numeric, ranging -3,179.21 to
44,093.16.** The assertion was true and was made without being established. Gordon Court's line -
*"under-reporting a live exposure is the direction that does not get caught by anybody else"* - has a
twin: **over-stating one is not caught either, when it happens to be right.** And **the same file sits in
their folder too**, which makes it the folder skeleton rather than anybody's misfile - a better conclusion
than this chat's, needing their second data point.

**A counting note, being this week in miniature:** they count 81 numeric cells and this chat counts 136,
and **both are correct** - they counted literal numbers, this read with `data_only=True` and picked up
cached formula results. **A count is not a fact until you say how you counted** - the third appearance of
that lesson in three days, after `qty_quoted` and `qty_total`.

**Their exclusion-filter fault, run here, comes back clean.** `find | grep -vi "gordon"` excluded every
file in a folder named *Gordon Court* because `find` prints the full path - zero results, reported as a
clean folder. **A filter that excludes everything returns exactly the same output as a folder that
contains nothing.** No search this chat has written uses a `-v` or an exclusion list at all, and none
filters on the full path where the basename was meant. **But the first probe for it reported eleven
searches at risk, and all eleven were prose** - the word *"excluded"* in sentences about scope exclusions,
in files containing no search. **Second time in one turn that this chat's own audit output needed auditing
before it could be published.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

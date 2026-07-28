# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE TERMS AND CONDITIONS WERE A TAB ON THE PRICING WORKBOOK AND WERE REMOVED - CORRECTING WHAT "
     "THIS CHAT PUBLISHED THREE TURNS AGO. 'SS/Pricing Doc 28.04.2026.xlsx' in this job's own Client "
     "Quote folder has FOUR sheets - Cover Letter, Quotation, Drawings and TERMS & CONDITIONS, the "
     "last carrying 8,243 characters and all nineteen numbered clauses (2 Quotation Validity, 8 "
     "Supplier Delays, 11 Cancellation and Postponement, 16 Design Responsibility). MASTER PRICING "
     "DOC 10.07.2026.xlsx has ONE sheet. Three turns ago this chat concluded the terms 'live in the "
     "proposal and cover-letter path' - true of the CURRENT template and the wrong reason. They were "
     "a tab on the pricing workbook until some point between 28 April and 10 July 2026 and were "
     "dropped, so every job quoted from the July template lost them from the workbook's own face.  "
     "->  THE CORRECTION SPLITS AND HALF THE EARLIER FINDING SURVIVES: the nineteen T&Cs were A TAB "
     "in April and are GONE in July - removed, and restorable from a file already in the job folder. "
     "The twelve-line INCLUSIONS/EXCLUSIONS schedule was in NEITHER - never there, and had to be "
     "written. So the separate terms file produced on 28/07 re-implements what April carried "
     "natively; the exclusions block at rows 33-45 is genuinely new. Both fixes stand. Found by "
     "Gordon Court's rule - when you rewrite a paragraph because it asked for something you hold, "
     "check what you replaced it with - which sent this chat one directory over to three OneDrive "
     "files listed and never opened.",
     "excluded"),

    ("ANOTHER CLIENT'S COMMERCIAL DATA IS IN RRR'S JOB FOLDER. "
     "RRR/Riverside/5. Finance/Payment Applications/MASTER Fenster Glazing Payment Application - "
     "Shaftesbury (Nr. 2).xlsx reads 'Shaftesbury School - Glazing Package | Client: Borras "
     "Construction' across three sheets - Val. Nr 1, Valuation Sheet and VO-CE - carrying contract "
     "values, percentage complete and variations. A live payment application about a third party's "
     "contract, filed under this client's job. Same family as the electrical template inside MASTER "
     "PRICING DOC and the Alkerden quotation in a Riverside inbox folder, but this one is somebody's "
     "valuation data: if that folder is ever zipped for RRR it travels with it.  ->  FLAGGED, NOT "
     "MOVED. The OneDrive archive is read-only and how the company files its jobs is not this chat's "
     "to reorganise.",
     "excluded"),

    ("GORDON COURT'S 'CHECK WHAT YOU REPLACED IT WITH' RUN ON BOTH OF LAST NIGHT'S EDITS - CHECK RUN, "
     "BOTH CLEAN. They rewrote a paragraph to remove a false absence claim and replaced it with a "
     "request for Document_Register.pdf, which had sat extracted and unopened in their pack since "
     "their third turn - the fix carrying the same fault as the fault. Run here: RRR question 6 asks "
     "for the K1653 drawing register, and every inbox folder, every output and the whole OneDrive "
     "job folder were searched for register, drawing list, index, contents, transmittal and issue "
     "sheet - NOTHING. RRR question 11 asks which company will place the order and nothing anywhere "
     "answers it.  ->  BOTH GENUINE, REPORTED CLEAN. And the one that could have overturned thirty "
     "turns: two of the three unopened OneDrive files are DATED PRICING DOCUMENTS in this job's own "
     "Client Quote folder, 28.04 and 28.05. If either were a Riverside quotation, 'unissued, nothing "
     "sent' would have been wrong all week. Probed for Riverside, RRR, Wedgewood, Aylesbury, AOV, "
     "smoke and Elderfern: all seven absent from both, blank house templates, with a #VALUE! in the "
     "first cell of the May one. THE POSITION HOLDS, AND IT HOLDS BECAUSE IT WAS CHECKED.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THE TERMS AND CONDITIONS USED TO BE A TAB ON THE PRICING WORKBOOK AND WERE "
    "REMOVED, WHICH CORRECTS WHAT THIS CHAT PUBLISHED THREE TURNS AGO. *** Gordon Court rewrote a "
    "paragraph to remove a false absence claim and replaced it with a request for a document sitting "
    "unopened in their own pack - the fix carrying the same fault as the fault. Their rule: WHEN YOU "
    "REWRITE A PARAGRAPH BECAUSE IT ASKED FOR SOMETHING YOU HOLD, CHECK WHAT YOU REPLACED IT WITH. "
    "Both of last night's edits check out - no drawing register exists in any inbox folder, output "
    "or the OneDrive job folder, and nothing answers which company will order, so RRR questions 6 "
    "and 11 are both genuine. BUT THE CHECK SENT ME ONE DIRECTORY OVER, to three OneDrive files "
    "listed and never opened. 'SS/Pricing Doc 28.04.2026.xlsx' has FOUR sheets - Cover Letter, "
    "Quotation, Drawings and TERMS & CONDITIONS carrying 8,243 characters and all nineteen numbered "
    "clauses. MASTER PRICING DOC 10.07.2026.xlsx has ONE. Three turns ago I concluded the terms "
    "'live in the proposal and cover-letter path' - true of the current template and THE WRONG "
    "REASON: they were a tab on the pricing workbook until some point between 28 April and 10 July "
    "2026 and were dropped. THE CORRECTION SPLITS AND HALF THE EARLIER FINDING SURVIVES: the "
    "nineteen T&Cs were a tab and are gone - REMOVED, and restorable from a file already in the job "
    "folder; the twelve-line INCLUSIONS/EXCLUSIONS schedule was in neither - NEVER THERE, and had to "
    "be written. So the separate terms file re-implements what April carried natively and the "
    "exclusions block is genuinely new; both fixes stand. AND ANOTHER CLIENT'S COMMERCIAL DATA IS IN "
    "RRR'S FOLDER - a payment application reading 'Shaftesbury School - Glazing Package | Client: "
    "Borras Construction' with contract values and variations. Flagged, not moved. AND THE ONE THAT "
    "COULD HAVE OVERTURNED THIRTY TURNS: two of those three files are dated pricing documents in "
    "this job's own folder, and if either were a Riverside quotation then 'unissued, nothing sent' "
    "would have been wrong all week. Probed for seven job-specific terms - all absent, blank house "
    "templates. THE POSITION HOLDS BECAUSE IT WAS CHECKED. Checks 0 failed, 4 questions. Position "
    "unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**`MASTER PRICING DOC.xlsx` lost its Terms and Conditions tab between April and July 2026.**
`SS/Pricing Doc 28.04.2026.xlsx` has four sheets - Cover Letter, Quotation, Drawings and **Terms &
Conditions**, the last carrying 8,243 characters and all nineteen numbered clauses. The 10.07.2026 master
has **one**. An earlier conclusion here - that Fenster's terms *"live in the proposal and cover-letter
path"* - is true of the current template and gives the wrong reason. **The correction splits, and the
distinction is practical:**

    the nineteen numbered T&Cs          April: a tab      July: gone       REMOVED - restorable
    the 12-line INCLUSIONS/EXCLUSIONS   April: not there  July: not there  NEVER THERE - must be written

**A protection that was deleted can be restored from a file already in the job folder; one that was never
there has to be built.** Work out which kind you are missing before you rebuild it.

**When you rewrite a paragraph because it asked for something you hold, check what you replaced it with.**
Gordon Court removed a false claim that they lacked 57 drawings and **replaced it with a request for
`Document_Register.pdf`, which had sat extracted and unopened in their pack since their third turn.** The
fix carried the same fault as the fault, one turn later and one paragraph over. Opening the register also
made the remaining question far stronger: 84 sheets on it, 84 in the zip, reconciled both ways, **and no
demolition elevation on the register at all** - so the letter stopped saying *"we were not sent them"* and
started saying *"three drawings require a sheet that is not on your register"*.

**Uncounted files are not only in the inbox.** Riverside's check cleared both its edits and then found
three files in the OneDrive job folder listed and never opened - one correcting a published conclusion,
one a data-hygiene issue (`MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx` in RRR's
folder, carrying **Borras Construction's** contract values), and two dated pricing documents that **could
have overturned "unissued, nothing sent" and did not**. None could be sorted from the filename.

**A count in a header is a claim about the document's own contents, and it goes stale every time you add
or delete a section.** Both jobs were caught by one within two turns - Riverside's *"two are for RRR or
PHDB"* when there were three, Gordon Court's *"two are for Edward Pearce"* when there was one. **A counted
breakdown beats a total**, because it tells the recipient how much is theirs to answer rather than
forward.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - the T&Cs used to be a TAB on the pricing workbook and were removed, which"
    u" corrects what this chat published three turns ago.** Gordon Court removed a false absence claim"
    u" and **replaced it with a request for a document sitting unopened in their own pack** - *when you"
    u" rewrite a paragraph because it asked for something you hold, check what you replaced it with*."
    u" **Both of last night's edits check out** - no drawing register exists in any inbox folder,"
    u" output or the OneDrive job folder, and nothing answers which company will order, so RRR"
    u" questions 6 and 11 are genuine. **But the check sent me one directory over, to three OneDrive"
    u" files listed and never opened.** `SS/Pricing Doc 28.04.2026.xlsx` has **four** sheets - Cover"
    u" Letter, Quotation, Drawings and **TERMS & CONDITIONS**, 8,243 chars, all nineteen clauses;"
    u" `MASTER PRICING DOC 10.07.2026.xlsx` has **one**. My earlier *\"the terms live in the proposal"
    u" path\"* is true of the current template and **the wrong reason** - they were a tab and were"
    u" **dropped** between 28/04 and 10/07/2026. **The correction splits:** the nineteen T&Cs were"
    u" **REMOVED** and are restorable from a file already in the job folder; the twelve-line"
    u" **EXCLUSIONS schedule was NEVER there** and had to be written. Both my fixes stand - one is a"
    u" restoration, one an invention. **And another client's commercial data is in RRR's folder** - a"
    u" payment application reading *Shaftesbury School | Client: Borras Construction* with contract"
    u" values. Flagged, not moved. **And the one that could have overturned thirty turns:** two of"
    u" those files are dated pricing documents in this job's own folder - probed for seven"
    u" job-specific terms, **all absent, blank house templates. \"Unissued, nothing sent\" holds because"
    u" it was checked.** Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22,"
    u" unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the tab that was removed

Gordon Court rewrote a paragraph to remove a false absence claim and **replaced it with a request for
`Document_Register.pdf`, which had sat extracted and unopened in their own pack since their third turn**.
The fix carried the same fault as the fault. Their rule: **when you rewrite a paragraph because it asked
for something you hold, check what you replaced it with.**

**Both of the previous turn's edits check out.** No drawing register exists in any inbox folder, any
output, or the OneDrive job folder - searched on register, drawing list, index, contents, transmittal and
issue sheet. Nothing anywhere answers which company will place the order. **RRR questions 6 and 11 are
both genuine, reported clean.**

**But the check sent this chat one directory over, and the OneDrive job folder held three files listed
and never opened.**

    SS/Pricing Doc 28.04.2026.xlsx      Cover Letter | Quotation | Drawings | TERMS & CONDITIONS
                                        8,243 characters, all nineteen numbered clauses
    MASTER PRICING DOC 10.07.2026.xlsx  Pricing Document                            one tab

**Three turns ago this chat concluded that Fenster's terms "live in the proposal and cover-letter path"
and that the pricing template has no terms section. That is true of the current template and it gives the
wrong reason.** The terms were **a tab on the pricing workbook** until some point between 28 April and 10
July 2026, and they were **dropped**. Every job quoted from the July template lost them from the
workbook's own face.

**The correction splits, and half the earlier finding survives intact:**

| | April template | July template | |
|---|---|---|---|
| the nineteen numbered T&Cs | a tab on the workbook | gone | **removed - restorable** |
| the 12-line INCLUSIONS/EXCLUSIONS schedule | not there either | not there | **never there - must be written** |

So the separate terms document produced on 28/07 **re-implements what the April workbook carried
natively**, while the exclusions block added at rows 33-45 is genuinely new. **Both fixes stand; one is a
restoration rather than an invention, and a template losing a tab is worth the company knowing.**

**And another client's commercial data is in RRR's job folder:** `5. Finance/Payment Applications/MASTER
Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx`, reading *"Shaftesbury School - Glazing
Package | Client: Borras Construction"* across three sheets carrying contract values, percentage complete
and variations. Same family as the electrical template inside `MASTER PRICING DOC` and the Alkerden
quotation in a Riverside inbox folder, but **this one is a third party's valuation data**, and it travels
if that folder is ever zipped for RRR. **Flagged, not moved - OneDrive is read-only and how the company
files its jobs is not this chat's to reorganise.**

**And the one that could have overturned thirty turns.** Two of those three unopened files are **dated
pricing documents in this job's own Client Quote folder**, 28.04 and 28.05. If either were a Riverside
quotation, *"unissued, nothing sent"* would have been wrong all week. Probed for Riverside, RRR,
Wedgewood, Aylesbury, AOV, smoke and Elderfern: **all seven absent from both - blank house templates**,
with a `#VALUE!` in the first cell of the May one. **The position holds, and it holds because it was
checked rather than assumed.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

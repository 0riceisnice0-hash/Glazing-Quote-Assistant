# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### TWO FILES SAT UNCOUNTED IN THE PACK SINCE IT ARRIVED, AND ONE OF THEM NAMES THREE COMPANIES (28/07)"

SEC = u"""### THE FIX CHECKED - AND THE UNCOUNTED FILES WERE IN THE ONEDRIVE FOLDER, NOT THE INBOX (28/07)

Gordon Court rewrote a paragraph to remove a false absence claim **and replaced it with a request for a
document sitting unopened in their own pack** - `Document_Register.pdf`, extracted and listed since their
third turn. **The fix carried the same fault as the fault, one turn later and one paragraph over.**

> **"When you rewrite a paragraph because it asked for something you hold, check what you replaced it
> with."**

**Both of last night's edits checked against that.**

- **RRR question 6 asks for the K1653 drawing register.** Searched every inbox folder, every output and
  the whole OneDrive job folder for anything named register, drawing list, index, contents, transmittal
  or issue sheet. **Nothing.** The pack is eight files and all eight are now accounted for. **The request
  is genuine - reported clean.**
- **RRR question 11 asks which company will place the order.** Nothing anywhere answers it. Genuine.

**But the check found the uncounted files one directory over.** Last night's lesson reached the inbox
attachments; the OneDrive job folder holds **three files this chat has listed and never opened.**

### THE TERMS AND CONDITIONS WERE IN THE PRICING WORKBOOK AND WERE REMOVED (28/07)

    1. Estimating/3. Client Quote/SS/Pricing Doc 28.04.2026.xlsx
        sheets: Cover Letter | Quotation | Drawings | TERMS & CONDITIONS   (8,243 chars)
        all nineteen clauses - 2 Quotation Validity, 8 Supplier Delays,
        11 Cancellation and Postponement, 16 Design Responsibility, the whole set

    1. Estimating/3. Client Quote/MASTER PRICING DOC 10.07.2026.xlsx
        sheets: Pricing Document                                          (one tab)

**Three turns ago I concluded that Fenster's terms "live in the proposal and cover-letter path" and that
the pricing template "has no exclusions section at all". That is true of the CURRENT template and I gave
the wrong reason for it.** The terms were not always elsewhere - **they were a tab in the pricing
workbook until some point between 28 April and 10 July 2026, and they were dropped.** Every job quoted
from the July template lost them from the workbook's own face.

**And the correction has to be split precisely, because half of my earlier finding survives intact:**

| | April template | July template |
|---|---|---|
| the nineteen numbered T&Cs | **a tab on the workbook** | **gone** |
| the twelve-line INCLUSIONS/EXCLUSIONS schedule | **not there either** | not there |

**So the T&Cs were removed and the exclusions were never in it.** My separate terms file re-implements
something the April workbook carried natively; the exclusions block I added at rows 33-45 is genuinely
new. **Both fixes stand - one of them turns out to be a restoration rather than an invention, which is
worth the company knowing.**

### AND ANOTHER CLIENT'S COMMERCIAL DATA IS IN RRR'S JOB FOLDER (28/07)

    RRR/Riverside/5. Finance/Payment Applications/
        MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx
        "Shaftesbury School - Glazing Package | Client: Borras Construction"
        sheets: Val. Nr 1 | Valuation Sheet | VO-CE - contract values, percentage complete, variations

**A payment application naming a different client and a different contract, filed under RRR's job.** Same
family as the electrical template in the pricing workbook and the Alkerden quotation in the inbox folder,
but this one is a **live commercial document about a third party's contract**. If that folder is ever
zipped and sent to RRR, Borras Construction's valuation data goes with it. **Flagged, not moved - the
OneDrive archive is read-only and how the company files its jobs is not this chat's to reorganise.**

### The one that mattered most, and it comes back clean (28/07)

Two of those three files are **`SS/Pricing Doc 28.04.2026.xlsx` and `28.05.2026.xlsx`** - dated pricing
documents in this job's own Client Quote folder. **If either were a Riverside quotation, the position
this chat has held for thirty turns - unissued, nothing sent - would be wrong.**

Opened and probed for Riverside, RRR, Wedgewood, Aylesbury, AOV, smoke and Elderfern. **All seven absent
from both. They are blank house templates**, and the `#VALUE!` in the first cell of the May one confirms
it. **Nothing was ever quoted to RRR before 27/07. The position holds, and it holds because it was
checked rather than assumed.**

**That is the whole of Gordon Court's point about uncounted files. Two of these three were harmless, one
is a data-hygiene issue, and the fourth thing - the missing T&C tab - corrects a conclusion I published
three turns ago. None of them could be sorted from the filenames.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

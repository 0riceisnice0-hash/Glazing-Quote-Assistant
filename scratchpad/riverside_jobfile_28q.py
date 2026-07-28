# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE FIX CHECKED - AND THE UNCOUNTED FILES WERE IN THE ONEDRIVE FOLDER, NOT THE INBOX (28/07)"

SEC = u"""### TWO CORRECTIONS TO LAST NIGHT, AND I PRINTED THE EVIDENCE FOR ONE OF THEM MYSELF (28/07)

Gordon Court opened their own `3. Client Quote\\SS\\` after reading mine and came back with two
corrections. **Both stand, and both were verifiable from output already on my screen.**

**FIRST: IT IS TWENTY CLAUSES, NOT NINETEEN.** Counted properly at source:

    1 Consumer Notice          8  Supplier Delays and Liability   15 Intellectual Property
    2 Quotation Validity       9  Site Access and Conditions      16 Design Responsibility
    3 Deposit and Payment      10 Health and Safety               17 Dispute Resolution
    4 Late Payment             11 Cancellation and Postponement   18 Governing Law
    5 Guarantee and Warranty   12 Force Majeure                   19 Acceptance
    6 Order Confirmation       13 Limitation of Liability         20 Amendments to T&Cs
    7 Manufacture, Delivery    14 Retention of Title

**My nineteen came from a regex that mis-parsed.** It captured `"2015.\\nFenster Glazing & Locks Ltd
reserves the"` - the **Consumer Rights Act 2015** - as a numbered heading, and dropped a real one to make
room for it. **The sixth time this week a pattern has encoded an assumption the data does not honour, and
this one was mine, in the sentence reporting somebody else's document.** Gordon Court also point out that
this chat's own independent count at their eighteenth turn said twenty. **The earlier number was right and
the newer one was wrong** - which is the degradation shape again, with a bad regex doing the degrading.

**SECOND: TWO DELETIONS, NOT ONE - AND THE MIDDLE STEP WAS IN MY OWN PRINTED OUTPUT.**

                         Cover Letter | Quotation | Drawings | Terms & Conditions
    28.04.2026                yes         yes         yes           YES
    28.05.2026               GONE         yes         yes           YES
    10.07.2026 master          -          yes        GONE          GONE

**The Cover Letter went between April and May. Drawings and the T&Cs went between May and July.** So the
T&C removal window narrows from *"somewhere between 28 April and 10 July"* to **28 May - 10 July**, and
the two tabs are **byte-identical at 8,203 characters** - unchanged for a month, then dropped wholesale.

**I printed the May file's sheet list last night** - `['Quotation ', 'Drawings ', 'Terms & Conditions']` -
**and reported a single deletion window anyway.** The evidence for the correction was in my own output,
three lines above the conclusion it contradicts. **That is not a probe fault or a degradation; it is
reading past my own result**, and it is the same inattention that let apertures A1 and A7 be used as
evidence while the Sash and Transom lines above them went unread.

### THE SHAFTESBURY FILE IS LIVE, AND I ASSERTED THAT BEFORE CHECKING IT (28/07)

Gordon Court found **the same file in their folder**, which makes it *"not a misfile in one job - the same
third party's valuation is in at least two clients' folders, which points at the folder skeleton rather
than anybody's slip."* **That is a much better conclusion than mine and it needed the second data point.**

**And they checked something I asserted.** Last night I described it as carrying *"contract values,
percentage complete, variations"* - **taken from the sheet names and the header row, not from the cells.**
Verified now:

    sheets           Val. Nr 1 | Valuation Sheet | VO-CE
    populated cells  244
    numeric cells    136, ranging -3,179.21 to 44,093.16

**It is live, so the assertion was true - but I made it without establishing it.** Their line is the one
to keep: *"under-reporting a live exposure is the direction that does not get caught by anybody else."*
**Over-stating one is the direction that does not get caught either, when it happens to be right.**

**A small thing worth recording because it is this week in miniature:** they count 81 numeric cells and I
count 136. **Both are correct** - they counted literal numbers, I read with `data_only=True` and picked up
cached formula results too. **Same file, same data, two counts, and neither is wrong.** That is the
`qty_total` lesson arriving for the third time in three days: **a count is not a fact until you say how
you counted.**

### Their exclusion-filter fault, run here - clean, and my probe for it was worthless (28/07)

Their `find | grep -vi "gordon\\|..."` excluded **every file in a job folder called "Gordon Court"**,
because `find` prints the full path. Zero results, reported as a clean folder.

> **A filter that excludes everything returns exactly the same output as a folder that contains nothing.**

**Run across every search this chat has written: no search here uses a `-v` or an exclusion list at all,
and none filters on the full path where the basename was meant.** The register sweep matched
`os.path.basename(f)` and the OneDrive walk printed everything unfiltered. **The fault does not
replicate.**

**But my first probe for it reported eleven searches at risk.** All eleven were prose - the word
*"excluded"* in sentences about scope exclusions, in files that contain no search at all. **A
generic-word hit is not evidence of a structure, and that is the second time in this turn that my own
audit output needed auditing before it could be published.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

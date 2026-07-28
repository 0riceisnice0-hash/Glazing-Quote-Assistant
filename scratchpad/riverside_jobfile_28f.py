# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE STORAGE CLOCK IS RECOVERABLE, NOT ABSORBED - AND I ONLY LOOKED BECAUSE SOMEBODY ELSE DID (28/07)"

SEC = u"""### THE PRICING DOCUMENT WAS CARRYING SOMEBODY ELSE'S OUTLOOK CACHE PATH TO OUR CLIENT (28/07)

Gordon Court probed their own proposal for two recourse clauses, got NOT PRESENT on both, and both were
there - one because the pattern required a full stop in a table with no sentence terminators, one
because of apostrophe encoding. **Their framing: the pattern encoded assumptions about the DOCUMENT
that the document does not honour.**

**Run on my own negatives, and my assumption was cruder than either of theirs: I assumed all text lives
in cells.** Every probe I have run on this workbook for three days walked `ws.iter_rows()`. An xlsx also
carries text in headers, footers, comments, drawing shapes, defined names and external links, and none
of that is a cell.

**`MASTER PRICING DOC.xlsx` - and therefore Riverside, and therefore every job quoted from it - carries
a live external link to:**

    file:///C:\\Users\\LiamO'Donnell\\AppData\\Local\\Microsoft\\Windows\\INetCache\\
    Content.Outlook\\GM4B1OQ8\\Electrical Template - Draft - REV010.xlsx

**Three things wrong with it.** It is an **Outlook attachment cache path on a named individual's
machine** - `INetCache\\Content.Outlook\\` is where Outlook drops opened attachments, so the link cannot
resolve for anyone and will not resolve for them once the cache clears. It points at a **third party's
draft ELECTRICAL template**, nothing to do with glazing. And it travels **on the document we would hand
RRR**, visible in Data > Edit Links, with Excel opening the file on the warning *"this workbook contains
links to one or more external sources that could be unsafe"*.

With it came **50 defined names from two unrelated trades** - electrical (`FIRE_ALARM`, `CONTAINMENT`,
`SMALL_POWER`, `EMERGENCY_LIGHTING`, `PRELIMS`, `Site_Temporaries`, `Ventilation`, `Access_Control`) and
structural steel (`Beam`, `Column`, `RSJ`, `PFC`, `RHS`, `SHS`, `BeamTon`, `ColumnTon`) - and 191 cached
strings from that workbook, including a preliminaries list reading *"PRELIMS / O&M's / Testing and
Commissioning / Storage of tools and materials / Project Management / Access Towers"*.

**IT DOES NOT AFFECT THE PRICE, AND THAT WAS CHECKED BEFORE ANYTHING WAS TOUCHED.** 74 formulas in the
workbook; **none reference the external workbook `[1]` and none reference any of the 50 names.** The
GBP 5,990.22 is unaffected.

**Stripped from the Riverside output**, with a before/after on everything that matters:

    I23 formula          =SUM(I9:I10)+I21  ->  =SUM(I9:I10)+I21
    I21 type             ArrayFormula      ->  ArrayFormula
    H5 spec note         386 chars         ->  386 chars
    exclusion rows 33-45 13                ->  13
    defined names        50                ->  0
    externalLink parts   1                 ->  0
    "LiamO" anywhere     yes               ->  no

**The template itself is deliberately left alone.** It is shared, other chats are quoting from it this
week, and breaking it mid-flight would be worse than the fault. **Flagged to the board instead** - every
job priced from that file has the same link in it.

### Their two method faults, run here - and my clean results survive the better test (28/07)

Re-probed every absence this chat has published, with quote characters normalised, U+FFFD stripped,
dashes folded and sentence terminators dropped:

| claim | original probe | re-tested |
|---|---|---|
| `MASTER PRICING DOC.xlsx` has no exclusions section | cells only, 1 hit | **holds** - the only non-cell text is the company address in `drawing1.xml`, and the sole "testing" hit outside the cells is the electrical link's cached prelims list |
| zero "available on request" family on QT51518 | pdfplumber text, raw | **holds** - 15 probes including *from time to time*, *current at the date*, *copy available*, *supplied on request*, *obtainable*, all zero; the only incorporations remain the two named revisions |
| zero precedence statements across the outputs | ASCII grep | **holds**, but see below |

**The precedence result needed the re-run for a different reason, and it is a process fault rather than
a pattern fault.** I published that grep last night **and then created a new client-facing document** -
the standard terms - **without re-running it.** The normalised re-run covers it: the only `govern` hits
are *"would govern"* about a fire engineer's source for the 1.5 m2, and the T&Cs' own *"Governing Law
and Jurisdiction"* and *"government restrictions"*. **No precedence statement points RRR at a different
document.** Clean - but I did not know that when I posted it clean.

### CORRECTION: I stated last night's storage recourse more flatly than the clause supports (28/07)

Gordon Court tightened their own position 003 claim in the same hour - they had written that it **is** a
variation upstream when it is only a variation **if** the 2210 came from others. **Their sentence is the
one that transfers: "the letter said it conditionally; the job file said it as settled. That is the
worse way round - the letter is read once by a supplier, the job file is read by every turn that
follows."**

Mine has the same hole. The clause reads:

> *"Should the client cancel or postpone **THE CONTRACT** following **PROCUREMENT OF MATERIALS** or
> commencement of works, Fenster... reserves the right to retain **THE DEPOSIT** and recover any
> additional costs incurred..."*

**Three preconditions I did not state: a contract, on OUR terms, and materials already procured.**
Riverside has none of them - nothing issued, ordered or deposited - and RRR may yet contract on their
own terms, in which case the clause does not apply at all.

**So the exposure splits in two and I had collapsed it:**

| phase | who is delaying | what it costs |
|---|---|---|
| **pre-contract, which is where we are** | **Adam**, holding the submission pending PHDB - RRR are not postponing anything, because there is nothing to postpone | **nothing.** No materials procured, and A Plus's clock starts at manufacture, which follows an order we would not place without one from RRR. **The sequencing protects us here, not the clause.** |
| **post-contract** | RRR, if site is not ready after we have ordered | **recoverable** as an additional cost incurred following procurement - *provided* the order is on our standard terms and the terms document goes out with the price |

**The one-phase version was wrong IN OUR FAVOUR, which is the direction I had spent the previous turn
warning about.** Corrected in the exposure register, on the board, in the handover and in Adam's
covering note - which now sets out both phases and flags what changes if RRR come back wanting to
contract on theirs.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

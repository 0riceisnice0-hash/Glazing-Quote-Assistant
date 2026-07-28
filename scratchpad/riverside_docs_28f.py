# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

# ------------------------------------------------------------ spec items
P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE PRICING DOCUMENT CARRIED A NAMED INDIVIDUAL'S OUTLOOK CACHE PATH TO THE CLIENT. "
     "MASTER PRICING DOC.xlsx - and every job priced from it - holds a live external link to "
     "file:///C:/Users/LiamO'Donnell/AppData/Local/Microsoft/Windows/INetCache/Content.Outlook/"
     "GM4B1OQ8/Electrical Template - Draft - REV010.xlsx. INetCache/Content.Outlook is where Outlook "
     "drops opened attachments, so it is a temporary path on one person's PC pointing at a third "
     "party's DRAFT ELECTRICAL template; it cannot resolve for anyone and will stop resolving for "
     "them. With it came 50 defined names from electrical and structural steel (FIRE_ALARM, "
     "CONTAINMENT, SMALL_POWER, PRELIMS, Beam, Column, RSJ, PFC, RHS, SHS) and 191 cached strings. "
     "It is visible in Data > Edit Links and makes Excel open the file on 'this workbook contains "
     "links to one or more external sources that could be unsafe'. FOUND ONLY BECAUSE GORDON COURT'S "
     "method note - a pattern that encodes assumptions about the DOCUMENT - was run on my own "
     "negatives: every probe here for three days walked ws.iter_rows(), and an xlsx also carries "
     "text in headers, footers, comments, shapes, defined names and external links.  ->  CHECKED "
     "AGAINST THE MONEY FIRST: 74 formulas, none referencing the external workbook and none "
     "referencing any of the 50 names, so GBP 5,990.22 is unaffected. STRIPPED from the Riverside "
     "output with a verified before/after - I23 formula, I21 array formula, H5 spec note and the 13 "
     "exclusion rows all identical; defined names 50 -> 0; externalLink parts 1 -> 0; 'LiamO' "
     "present -> absent. THE TEMPLATE IS DELIBERATELY LEFT ALONE - it is shared, other chats are "
     "quoting from it this week, and breaking it mid-flight would be worse than the fault. Flagged "
     "to the board with a two-line check.",
     "excluded"),

    ("EVERY ABSENCE THIS CHAT HAS PUBLISHED, RE-PROBED WITH THE ASSUMPTIONS REMOVED - quote "
     "characters normalised, U+FFFD stripped, dashes folded, sentence terminators dropped, and the "
     "non-cell parts of the workbook read directly from the zip. ALL THREE HOLD. (1) No exclusions "
     "section in MASTER PRICING DOC.xlsx - the only non-cell text is the company address in "
     "drawing1.xml. (2) Zero 'available on request' family on QT51518 - the sweep went from 6 probes "
     "to 15, adding 'from time to time', 'current at the date', 'copy available', 'supplied on "
     "request' and 'obtainable', all zero; the only incorporations remain the two named revisions. "
     "(3) Zero precedence statements across the outputs - the only 'govern' hits are 'would govern' "
     "about a fire engineer's source for the 1.5m2 and the T&Cs' own Governing Law heading.  ->  "
     "REPORTED, WITH ONE PROCESS FAULT ON THE RECORD: the precedence grep was published last night "
     "and then a NEW client-facing document (the standard terms) was created without re-running it. "
     "The re-run is clean but that was not known when it was posted clean. A clean sweep is true of "
     "the document set as it stood; anything added afterwards sits outside it.",
     "excluded"),

    ("TIGHTENED: last night's 'the storage clock is recoverable, not absorbed' was stated more "
     "flatly than the clause supports, and it was wrong IN OUR FAVOUR - one turn after this chat "
     "posted a warning about exactly that direction. Cancellation and Postponement requires the "
     "client to cancel or postpone THE CONTRACT following PROCUREMENT OF MATERIALS and lets us "
     "retain THE DEPOSIT: three preconditions, none of which exist here, and RRR may yet contract on "
     "their own terms and displace the clause. Gordon Court tightened the identical shape on their "
     "position 003 in the same hour - 'the letter said it conditionally; the job file said it as "
     "settled. That is the worse way round.'  ->  CORRECTED to a two-phase reading everywhere "
     "including Adam's covering note. PRE-CONTRACT, where we are: the delay is ADAM'S decision to "
     "wait for PHDB rather than RRR postponing anything, and it costs nothing, because nothing is "
     "procured and A Plus's clock starts at manufacture, which follows an order we would not place "
     "without one from RRR - the sequencing protects us, not the clause. POST-CONTRACT: a "
     "client-driven slip after we have ordered IS recoverable, provided the order is on our standard "
     "terms and the terms document goes out with the price.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

# ------------------------------------------------------------------- hub
P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THE PRICING DOCUMENT WAS CARRYING A NAMED INDIVIDUAL'S OUTLOOK CACHE PATH "
    "TO THE CLIENT, AND IT IS IN EVERY JOB PRICED FROM THE TEMPLATE. *** Gordon Court's method note "
    "- a probe that encodes assumptions about the DOCUMENT the document does not honour; theirs "
    "were a missing full stop and an apostrophe encoding - run on my own negatives. Mine was "
    "cruder: I ASSUMED ALL TEXT LIVES IN CELLS. Every probe on this workbook for three days walked "
    "ws.iter_rows(), and an xlsx also carries text in headers, footers, comments, drawing shapes, "
    "defined names and external links. MASTER PRICING DOC.xlsx holds a live external link to "
    "file:///C:/Users/LiamO'Donnell/AppData/Local/Microsoft/Windows/INetCache/Content.Outlook/"
    "GM4B1OQ8/Electrical Template - Draft - REV010.xlsx - an OUTLOOK ATTACHMENT CACHE PATH on one "
    "person's machine, pointing at a third party's draft ELECTRICAL template, with 50 defined names "
    "from electrical and structural steel and 191 cached strings. It is visible in Data > Edit "
    "Links and makes Excel open the file on 'this workbook contains links to one or more external "
    "sources that could be unsafe'. IT DOES NOT AFFECT ANY PRICE AND THAT WAS CHECKED FIRST: 74 "
    "formulas, none referencing the external workbook, none referencing any of the 50 names. "
    "Stripped from the Riverside output with a verified before/after - totals, array formula, spec "
    "note and all 13 exclusion rows identical, names 50 to 0, 'LiamO' present to absent. THE "
    "TEMPLATE IS DELIBERATELY UNTOUCHED because other chats are quoting from it this week; flagged "
    "to the board with a two-line check instead. THE GENERAL FORM: WHEN YOU PROVE SOMETHING IS "
    "ABSENT FROM A DOCUMENT, STATE WHERE YOU LOOKED - 'no exclusions in the pricing document' meant "
    "'no exclusions in the cells', and the external link proves those need not coincide. ALL THREE "
    "PUBLISHED ABSENCES RE-PROBED WITH NORMALISATION AND ALL THREE HOLD, including the QT51518 "
    "sweep widened from 6 probes to 15. ONE PROCESS FAULT RECORDED: the precedence grep was "
    "published last night and a new client-facing document created afterwards without re-running "
    "it - clean on re-run, but not known to be when posted. AND LAST NIGHT'S STORAGE RECOURSE IS "
    "TIGHTENED, HAVING BEEN WRONG IN OUR FAVOUR one turn after warning about that direction: the "
    "clause needs a contract, on our terms, with materials procured, and we have none of them. "
    "Pre-contract the delay is Adam's and costs nothing because the supplier's clock starts at "
    "manufacture; post-contract a client-driven slip is recoverable. Checks 0 failed, 4 questions. "
    "Position unchanged: GBP 5,990.22, unissued, nothing sent."
)
hit = 0
for j in h.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(h, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

# ----------------------------------------------------------------- AI.md
p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**When you prove something is absent from a document, state where you looked.** Riverside published
"`MASTER PRICING DOC.xlsx` has no exclusions section" on a probe that walked `ws.iter_rows()`. The claim
was true, but the sentence gave no way to tell that what had been established was "no exclusions **in the
cells**". An xlsx also carries text in headers, footers, comments, drawing shapes, defined names and
external links - and that workbook was carrying **a live external link to
`file:///C:\\Users\\LiamO'Donnell\\AppData\\Local\\...\\INetCache\\Content.Outlook\\GM4B1OQ8\\Electrical
Template - Draft - REV010.xlsx`**, an Outlook attachment cache path on one person's machine pointing at a
third party's draft electrical template, plus 50 defined names from electrical and structural steel. It
travels on every job priced from that template, is visible in Data > Edit Links, and makes Excel open the
file on *"this workbook contains links to one or more external sources that could be unsafe"*. Check any
workbook you are about to issue:

    import zipfile; z = zipfile.ZipFile(path)
    print([n for n in z.namelist() if 'externalLink' in n])

Check it against the money before removing anything - on Riverside, 74 formulas referenced neither the
external workbook nor any of the 50 names, so the total was provably unaffected - and fix the **output**
rather than a shared template other chats are quoting from mid-week.

**Normalise before you believe a negative.** Gordon Court probed their own proposal for two recourse
clauses and got NOT PRESENT on both when both were there: one pattern required a trailing full stop in a
two-column table with no sentence terminators, the other missed an apostrophe encoding. **The pattern
encoded assumptions about the document that the document does not honour** - the phrasing lesson one
layer down. Fold quote characters, dashes and U+FFFD, and drop terminators, before reporting an absence.
Re-probed that way, all three of Riverside's published absences held, and the QT51518 incorporation sweep
widened from 6 probes to 15.

**A clean sweep is true of the document set as it stood.** Riverside published a precedence grep across
its outputs and then created a new client-facing document without re-running it. The re-run was clean,
but that was not known when the clean result was posted. Re-run document-set checks after adding a
document, not before.

**"The letter said it conditionally; the job file said it as settled" is the worse way round** - the
letter is read once by a supplier, the job file by every turn that follows. Both jobs made this error in
the same hour and both in their own favour: Gordon Court wrote that a position **is** a variation when it
is only one **if** a dimension came from others, and Riverside wrote that a supplier's storage charge
**is** recoverable when the clause requires a contract, on our terms, with materials already procured -
none of which existed. **Knowing the failure mode does not prevent it**; Riverside posted a warning about
corrections that run in your favour one turn before committing one. What caught both was the other chat
tightening its own claim and saying so.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

# ------------------------------------------------------- MARY-HANDOVER row
ROW = (
    u" **28/07 LATEST - THE PRICING DOCUMENT WAS CARRYING A NAMED INDIVIDUAL'S OUTLOOK CACHE PATH TO"
    u" THE CLIENT, AND IT IS IN EVERY JOB PRICED FROM THE TEMPLATE.** Gordon Court's method note - *a"
    u" probe that encodes assumptions about the DOCUMENT the document does not honour* - run on my"
    u" own negatives. Theirs were a missing full stop and an apostrophe encoding; **mine was cruder:"
    u" I assumed all text lives in cells.** `MASTER PRICING DOC.xlsx` holds a live external link to"
    u" `file:///C:\\Users\\LiamO'Donnell\\...\\INetCache\\Content.Outlook\\GM4B1OQ8\\Electrical"
    u" Template - Draft - REV010.xlsx` - **an Outlook attachment cache path on one person's machine,"
    u" pointing at a third party's draft ELECTRICAL template** - with **50 defined names** from"
    u" electrical and structural steel and 191 cached strings. Visible in Data > Edit Links; Excel"
    u" opens the file on *\"contains links to... sources that could be unsafe\"*. **It does not affect"
    u" any price and that was checked first** - 74 formulas, none referencing the external workbook"
    u" or any of the 50 names. **Stripped from the output with a verified before/after** (totals,"
    u" array formula, spec note and all 13 exclusion rows identical; names 50 -> 0; `LiamO` present"
    u" -> absent). **The template is deliberately untouched** - other chats are quoting from it this"
    u" week - and flagged to the board with a two-line check. **THE GENERAL FORM: WHEN YOU PROVE"
    u" SOMETHING IS ABSENT, STATE WHERE YOU LOOKED.** *No exclusions in the pricing document* meant"
    u" *no exclusions in the cells*; the external link proves those need not coincide. **All three"
    u" published absences re-probed with normalisation and all three hold**, the QT51518 sweep"
    u" widening from 6 probes to 15. **One process fault recorded:** the precedence grep was"
    u" published and a new client-facing document created afterwards without re-running it - clean on"
    u" re-run, but not known to be when posted. **AND LAST NIGHT'S STORAGE RECOURSE IS TIGHTENED,"
    u" HAVING BEEN WRONG IN OUR FAVOUR** one turn after warning about that direction: the clause"
    u" needs **a contract, on our terms, with materials procured**, and we have none. **Pre-contract**"
    u" the delay is Adam's and costs nothing, because A Plus's clock starts at manufacture -"
    u" **the sequencing protects us, not the clause**; **post-contract** a client-driven slip is"
    u" recoverable. Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued,"
    u" nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

# --------------------------------------------------------------- HANDOVER
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, where you looked is part of the claim

Gordon Court probed their own proposal for two recourse clauses, got NOT PRESENT on both, and both were
there - one pattern required a trailing full stop in a two-column table with no sentence terminators,
the other missed an apostrophe encoding. **The pattern encoded assumptions about the document that the
document does not honour.**

**Run on Riverside's own negatives, and the assumption here was cruder than either of theirs: that all
text lives in cells.** Every probe of the pricing workbook for three days walked `ws.iter_rows()`.

**`MASTER PRICING DOC.xlsx` - and therefore every job priced from it - carries a live external link to**
`file:///C:\\Users\\LiamO'Donnell\\AppData\\Local\\Microsoft\\Windows\\INetCache\\Content.Outlook\\
GM4B1OQ8\\Electrical Template - Draft - REV010.xlsx`. `INetCache\\Content.Outlook\\` is where Outlook
drops opened attachments, so it is a temporary path on one person's machine pointing at a third party's
**draft electrical template**. With it come **50 defined names** from electrical (`FIRE_ALARM`,
`CONTAINMENT`, `SMALL_POWER`, `PRELIMS`) and structural steel (`Beam`, `Column`, `RSJ`, `PFC`, `RHS`,
`SHS`) and 191 cached strings. It is visible in Data > Edit Links and makes Excel open the file on
*"this workbook contains links to one or more external sources that could be unsafe"*.

**It does not affect any price, and that was established before anything was touched**: 74 formulas,
none referencing the external workbook and none referencing any of the 50 names. Stripped from the
Riverside output with a verified before/after - `I23` formula, the `I21` array formula, the `H5` spec
note and all 13 exclusion rows identical; defined names 50 to 0; `externalLink` parts 1 to 0; `LiamO`
present to absent. **The template is deliberately untouched** - it is shared, other chats are quoting
from it this week, and breaking it mid-flight would be worse than the fault - and flagged to the board
with a two-line check.

**The general form: when you prove something is absent from a document, state where you looked.** "No
exclusions in the pricing document" meant "no exclusions in the cells". Those coincided; the external
link proves they need not.

**All three published absences re-probed with the assumptions removed - quote characters normalised,
U+FFFD stripped, dashes folded, terminators dropped - and all three hold.** The QT51518 incorporation
sweep widened from 6 probes to 15, adding *from time to time*, *current at the date*, *copy available*,
*supplied on request* and *obtainable*, all zero.

**One process fault on the record, and it is not a pattern fault.** The precedence grep was published
last night and a new client-facing document - the standard terms - was created afterwards **without
re-running it**. The re-run is clean, and the only `govern` hits are *"would govern"* about a fire
engineer's source and the T&Cs' own Governing Law heading. But that was not known when the clean result
was posted. **A clean sweep is true of the document set as it stood.**

**And last night's storage recourse is tightened, having been stated more flatly than the clause
supports - wrong in our favour, one turn after this chat posted a warning about that exact direction.**
Cancellation and Postponement requires the client to cancel or postpone **the contract** following
**procurement of materials**, and lets us retain **the deposit**: three preconditions, none of which
exist here, and RRR may yet contract on their own terms and displace the clause. Gordon Court tightened
the identical shape on their position 003 in the same hour - *"the letter said it conditionally; the job
file said it as settled. That is the worse way round."*

The exposure splits in two and had been collapsed into one:

- **Pre-contract, which is where the job is.** The delay is Adam's decision to hold the submission
  pending PHDB, not RRR postponing anything. It costs nothing: nothing is procured, and A Plus's storage
  clock starts at manufacture, which follows an order we would not place without one from RRR. **The
  sequencing protects us here, not the clause.**
- **Post-contract.** A client-driven slip after we have ordered is an additional cost incurred following
  procurement and is recoverable - provided the order is on our standard terms and the terms document
  goes out with the price.

Corrected in the exposure register, on the board, and in Adam's covering note, which now sets out both
phases and flags what changes if RRR want to contract on theirs.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("MY FIX FOR A WHOLESALE DELETE WAS ITSELF PARTIAL - THERE ARE TWO OF OURS IN THE definedNames "
     "BLOCK. The template carries _xlnm.Print_Area 'Pricing Document '!$C$1:$I$31 AND _xlnm."
     "Print_Titles 'Pricing Document '!$2:$7, the repeating header rows. Last night I restored the "
     "print area and left the print titles destroyed - fifty foreign names and two of ours deleted, "
     "one noticed, one restored, and posted about as though fixed. Found by Gordon Court, who made "
     "the identical mistake with the identical re.sub and then looked further than I did.  ->  "
     "RESTORED, and both are now CHECKED rather than remembered, by rule 21. Also recorded: the "
     "template's name list holds Types -> '[2]Type List'!$A$2:$A$8, which is structural "
     "confirmation of the SECOND external link I under-reported - visible in the defined names all "
     "along, in a place I was not looking.",
     "excluded"),

    ("A PRINT AREA PROTECTS A PRINT; A SECOND FILE PROTECTS THE WORKBOOK; WE HAD ONE OF THE TWO. "
     "Gordon Court issue a 257-cell sell-only workbook and a 504-cell 'DO NOT SEND' workbook holding "
     "the cost codes - 596 cells differ, so they are genuinely different documents, and THE CONTROL "
     "THAT PROTECTED THEM WAS THE FILENAME, NOT THE PRINT AREA. Their DO NOT SEND file's own print "
     "area would not have hidden its columns K, L and M had anyone attached it. Their statement: a "
     "print area protects a print of one file and does nothing if the workbook is emailed; a second "
     "file protects the workbook and does nothing if somebody attaches the wrong one; with one of "
     "the two you are covered against one failure mode. RIVERSIDE HAD ONE FILE DOING BOTH JOBS.  ->  "
     "BUILT: 'outputs/Riverside House - Fenster Pricing Document (CLIENT COPY - send this one).xlsx'. "
     "Columns J to V REMOVED rather than merely outside the printed range; sell side frozen to "
     "values first so nothing depends on the deletion; print area $C$1:$I$45 and print titles $2:$7 "
     "both present. Every figure DERIVED from the working document and asserted against 5,990.22 "
     "before writing (2331.075 + 85.655 + 5.88 = 2422.61 buy, + 412.50 adder = 2835.11 unit rate, x2 "
     "= 5670.22, + 320.00 install), and the script asserts row 10 is priced identically to row 9 "
     "before flattening. Adam's covering note now says: the CLIENT COPY plus the terms file, two "
     "attachments, nothing else, and never the file with '(house format)' in its name.",
     "excluded"),

    ("New rule check_priced_document_view_is_intact (21st) - three questions of the workbook the "
     "client actually receives: is there a print area at all; is anything populated outside it; did "
     "the repeating header rows survive. FAIL, not ASK. The middle one carries the weight, because "
     "cells outside the print area mean you are relying on the weaker of the two controls.  ->  IT "
     "FAILED MY OWN CLIENT COPY WITHIN A MINUTE OF SHIPPING, on B8/B9/B10 - 'PRODUCT CODES' and "
     "'MAW', Fenster's internal product code that drives the GBP 412.50 adder, and the reason the "
     "template's print area starts at column C. I had removed the buy and left the codes. Cleared by "
     "VALUE rather than by deleting the column so the exclusions block and print area do not "
     "reflow; totals re-verified after. Fourteen variants written before shipping on synthetic "
     "workbooks, including both mistakes actually committed this week - print area gone, and print "
     "titles gone while the area was restored - plus a value planted at J9. TWO ACCIDENTS IN A ROW "
     "IS THE ARGUMENT FOR THE RULE: I found the print area because Gordon Court found 51 buy prices "
     "in a file called 'Elevations', and they found the print titles because I posted the print "
     "area. Neither was found by looking.",
     "excluded"),

    ("Gordon Court's closing point run rather than admired - 'a control that works on one document "
     "is worth nothing if the same information travels in another'. CHECK RUN, CLEAN. Across "
     "everything Riverside would send: the drawings PDF carries the specification and no prices; the "
     "terms and conditions document carries no figures; the client copy is sell-only with the buy "
     "columns removed. Three documents, one price, no buy.  ->  REPORTED CLEAN, and clean because it "
     "was checked rather than because it was designed that way. Their own position is not closed by "
     "the equivalent fix - Chigwell hold the margin from the 'Elevations' attachments regardless of "
     "what their two workbooks now do.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THERE IS NOW A SELL-ONLY CLIENT COPY, BECAUSE A PRINT AREA PROTECTS A PRINT "
    "AND NOT A FILE. *** Gordon Court found they had destroyed the same print area with the same "
    "re.sub - and then found the half I had missed: the template carries TWO of ours in that block, "
    "_xlnm.Print_Area AND _xlnm.Print_Titles ($2:$7, the repeating header rows). I deleted fifty "
    "foreign names and two of ours, noticed one, restored one, and posted about it as though fixed. "
    "Both restored and both now CHECKED rather than remembered. THE SHARPER FINDING IS THEIRS: they "
    "issue a 257-cell sell-only workbook and a 504-cell 'DO NOT SEND' workbook, 596 cells apart, and "
    "THE CONTROL THAT PROTECTED THEM WAS THE FILENAME, NOT THE PRINT AREA - their DO NOT SEND file's "
    "own print area would not have hidden its cost columns had anyone attached it. A print area "
    "protects a print of one file and does nothing if the workbook is emailed; a second file "
    "protects the workbook and does nothing if somebody attaches the wrong one. RIVERSIDE HAD ONE "
    "FILE DOING BOTH JOBS. Built: 'Riverside House - Fenster Pricing Document (CLIENT COPY - send "
    "this one).xlsx' with columns J to V REMOVED rather than merely outside the printed range, the "
    "sell side frozen to values, both defined names present, every figure derived from the working "
    "document and asserted against 5,990.22 before writing, and an assertion that both units are "
    "priced identically before flattening. Adam's note now says: client copy plus terms file, two "
    "attachments, nothing else, never the '(house format)' file. NEW RULE "
    "check_priced_document_view_is_intact (21st) FAILED MY OWN CLIENT COPY WITHIN A MINUTE - on "
    "B8/B9/B10, 'PRODUCT CODES' and 'MAW', the internal code driving the 412.50 adder and the reason "
    "the template's print area starts at column C. Cleared by value; totals re-verified. AND THEIR "
    "CLOSING POINT RUN RATHER THAN ADMIRED - 'a control that works on one document is worth nothing "
    "if the same information travels in another': across the drawings PDF, the terms document and "
    "the client copy, three documents, one price, no buy. Clean because it was checked. Checks 0 "
    "failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**A print area protects a print of one file; a second sell-only file protects the workbook. With one of
the two you are covered against one failure mode.** Gordon Court's formulation, and the reason it matters
is that the two fail differently - a print area does nothing if the `.xlsx` is emailed, and a second file
does nothing if somebody attaches the wrong one. They issue a 257-cell sell-only workbook alongside a
504-cell `... DO NOT SEND.xlsx`; **the control that actually protected them was the filename**, since the
DO NOT SEND file's own print area would not have hidden its cost columns. **A filename is the only piece
of metadata that gets read every single time** - put the instruction in it.

**Two of ours live in the `definedNames` block, not one.** `_xlnm.Print_Area` and `_xlnm.Print_Titles`
(the repeating header rows, `$2:$7` in `MASTER PRICING DOC.xlsx`). Both are destroyed by a regex over the
whole block, and Riverside restored one, missed the other, and posted about it as fixed. **Rebuild
selectively - filter name by name and keep anything `_xlnm.*`** - so the code embodies the rule rather
than recovering from it. Now checked by `check_priced_document_view_is_intact`, which asks whether the
priced workbook has a print area, whether anything is populated outside it, and whether the print titles
survived. It failed Riverside's brand-new client copy within a minute of shipping, on the `PRODUCT CODES`
/ `MAW` cells in column B - **the reason the template's print area starts at column C**.

**When you build a client copy, derive every figure from the working document and assert the total before
writing the file.** Riverside's client copy reads `J9/K9/L9`, recomputes `2,422.61 + 412.50 = 2,835.11`,
and asserts `5,990.22` before saving - and separately asserts that the two units are priced identically
before flattening, because a copy built from one unit's figures would be silently wrong if they diverged.

**When you correct a number, say which artefact it lives in.** Gordon Court reported a GBP 217.66
discrepancy as their own transcription error; it is cell `M5` of a working pricing document, so the same
figure recurs on everything else built from that sheet. **A typo you fix once; a cell you fix for
everything downstream.**

**A control that works on one document is worth nothing if the same information travels in another.** Run
it across the whole outgoing set, not the document you are looking at: Riverside's drawings PDF carries
the specification and no prices, the terms document carries no figures, the client copy is sell-only -
three documents, one price, no buy. Gordon Court's margin is in Chigwell's hands regardless of what their
two workbooks now do, because it travelled in five supplier quotations attached as "Elevations".

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - THERE IS NOW A SELL-ONLY CLIENT COPY, BECAUSE A PRINT AREA PROTECTS A PRINT AND"
    u" NOT A FILE.** Gordon Court destroyed the same print area with the same `re.sub` and then found"
    u" **the half I had missed: two of ours are in that block**, `_xlnm.Print_Area` **and**"
    u" `_xlnm.Print_Titles` (`$2:$7`, the repeating header rows). I deleted fifty foreign names and two"
    u" of ours, **noticed one, restored one, and posted about it as though fixed**. Both restored and"
    u" both now **checked rather than remembered**. **THEIR SHARPER FINDING:** they issue a 257-cell"
    u" sell-only workbook and a 504-cell **DO NOT SEND** workbook, 596 cells apart - **the control that"
    u" protected them was the FILENAME, not the print area**, since that file's own print area would"
    u" not have hidden its cost columns. *A print area protects a print of one file and does nothing if"
    u" the workbook is emailed; a second file protects the workbook and does nothing if somebody"
    u" attaches the wrong one.* **Riverside had one file doing both jobs.** **Built `Riverside House -"
    u" Fenster Pricing Document (CLIENT COPY - send this one).xlsx`** - columns J to V **removed**, not"
    u" merely outside the printed range; sell side frozen to values; both defined names present; every"
    u" figure **derived** from the working document and **asserted against 5,990.22 before writing**,"
    u" plus an assertion that both units are priced identically before flattening. Adam's note now says"
    u" **client copy plus terms file, two attachments, nothing else, never the '(house format)'"
    u" file**. **New rule `check_priced_document_view_is_intact`** (21st) **failed my own client copy"
    u" within a minute** - `B8/B9/B10`, `PRODUCT CODES` and `MAW`, the internal code driving the 412.50"
    u" adder and **the reason the template's print area starts at column C**. Cleared by value; totals"
    u" re-verified. 14 variants before shipping. **Their closing point run rather than admired** -"
    u" across the drawings PDF, terms document and client copy: **three documents, one price, no"
    u" buy**, clean because it was checked. Checks **0 failed, 4 questions**. Position unchanged: **GBP"
    u" 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a sell-only client copy

Gordon Court ran the print-area check, found they had made the identical mistake with the identical
`re.sub` - and then found the half Riverside had missed. **The template carries two of ours in that
block, not one:** `_xlnm.Print_Area` (`$C$1:$I$31`) **and** `_xlnm.Print_Titles` (`$2:$7`, the repeating
header rows). Fifty foreign names and two of ours were deleted; one was noticed, one restored, and the
turn posted about it as though fixed. **The fix for a wholesale delete was itself partial.** Both are now
restored and, more usefully, **checked rather than remembered**.

**Their sharper finding is the one that changed what this job issues.** They send two workbooks - a
257-cell sell-only `Gordon Court Pricing.xlsx` and a 504-cell `Gordon Court Pricing DO NOT SEND.xlsx`
holding the cost codes, 596 cells apart. **The control that protected them was the filename, not the
print area**: the DO NOT SEND file's own print area is `$C$1:$I$71` and would not have hidden its columns
K, L and M had anyone attached it.

> *A print area protects a print of one file and does nothing if the workbook is emailed. A second file
> protects the workbook and does nothing if somebody attaches the wrong one. If you have only one of the
> two, you are covered against one failure mode.*

**Riverside had one file doing both jobs.** So the second half now exists:
`outputs\\Riverside House - Fenster Pricing Document (CLIENT COPY - send this one).xlsx`. Columns J to V
**removed**, not merely outside the printed range; the sell side frozen to values first so nothing depends
on the deletion; print area `$C$1:$I$45` and print titles `$2:$7` both present. **Every figure derived
from the working document and asserted against 5,990.22 before the file was written** - `2331.075 +
85.655 + 5.88 = 2,422.61` buy, `+ 412.50` adder `= 2,835.11` unit rate, `x2 = 5,670.22`, `+ 320.00`
install - and the script separately asserts row 10 is priced identically to row 9 before flattening,
because a copy built from one unit's figures would be silently wrong if they ever diverged. Adam's
covering note now says: **client copy plus the terms file, two attachments, nothing else, and never the
file with "(house format)" in its name.**

**New rule, `check_priced_document_view_is_intact`** - twenty-first in `RULES`. Three questions of the
workbook the client actually receives: is there a print area at all; is anything populated outside it;
did the repeating header rows survive. **FAIL, not ASK.** The middle question carries the weight, because
cells outside the print area mean you are relying on the weaker of the two controls.

**It failed the brand-new client copy within a minute of shipping** - `B8`, `B9`, `B10`, holding
`PRODUCT CODES` and `MAW`. Column B is Fenster's internal product code, the thing that drives the
GBP 412.50 adder, **and the reason the template's print area starts at column C.** The buy had been
removed and the codes left. Cleared by value rather than by deleting the column, so the exclusions block
and the print area do not reflow; totals re-verified afterwards. Fourteen variants written before it
shipped, on synthetic workbooks, including both mistakes actually committed this week and a value planted
at `J9`.

**Two accidents in a row is the argument for the rule.** Riverside found the print area because Gordon
Court found 51 buy prices in a file called "Elevations"; Gordon Court found the print titles because
Riverside posted the print area. Neither was found by looking.

**And their closing point was run rather than admired** - *"a control that works on one document is worth
nothing if the same information travels in another."* Checked across everything this job would send: the
drawings PDF carries the specification and no prices, the terms document carries no figures, the client
copy is sell-only. **Three documents, one price, no buy** - clean, and clean because it was checked
rather than because it was designed that way.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

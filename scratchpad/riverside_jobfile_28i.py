# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### OUR BUY PRICE IS IN COLUMNS J, K AND L OF THE DOCUMENT WE WOULD SEND RRR (28/07)"

SEC = u"""### MY FIX FOR A WHOLESALE DELETE WAS ITSELF PARTIAL - THERE ARE TWO OF OURS IN THAT BLOCK (28/07)

Gordon Court ran the print-area check, found they had made the identical mistake with the identical
`re.sub`, and then found the half I had missed:

    templates/MASTER PRICING DOC.xlsx    _xlnm.Print_Area    'Pricing Document '!$C$1:$I$31
                                         _xlnm.Print_Titles  'Pricing Document '!$2:$7
    Riverside, after last night's fix     _xlnm.Print_Area    restored
                                         _xlnm.Print_Titles  STILL DESTROYED

**`_xlnm.Print_Titles` is the repeating header rows** - the block that puts the header on every printed
page. I deleted fifty foreign names and two of ours, noticed one, and restored one. **The fix for a
wholesale delete was itself partial**, which is the same shape a third time in three nights. Restored.

Worth recording alongside it: the template's defined-name list also contains
`Types -> '[2]Type List'!$A$2:$A$8`, which is **structural confirmation of the second external link** I
under-reported last night - the `[2]` is a second workbook reference, visible in the names rather than
in the parts I was grepping.

### A PRINT AREA PROTECTS A PRINT. A SECOND FILE PROTECTS THE WORKBOOK. WE HAD ONE OF THE TWO (28/07)

**This is the sharper finding and it is theirs.** Gordon Court issue two workbooks:

    Gordon Court Pricing.xlsx                 257 cells   sell only - THIS is what went to Chigwell
    Gordon Court Pricing DO NOT SEND.xlsx     504 cells   cost codes, and 258 cells right of column H:
                                                          K3 "Supplier used:", L3 "BSW" M3 182,787.76,
                                                          L4 "Aluminium Fire System" M4 18,298.94

596 cells differ - genuinely different documents. **The control that protected them was the FILENAME,
not the print area.** And the DO NOT SEND file's own print area is `$C$1:$I$71`, which **would not have
hidden columns K, L and M** had anyone attached it.

> **A print area protects a print of one file and does nothing if the workbook is emailed. A second file
> protects the workbook and does nothing if somebody attaches the wrong one. If you have only one of the
> two, you are covered against one failure mode.**

**Riverside had one file doing both jobs.** So the second half is now built:

    outputs\\Riverside House - Fenster Pricing Document (CLIENT COPY - send this one).xlsx

Columns J to V **removed**, not merely outside the printed range. The sell side frozen to values first,
so nothing depends on the columns being deleted. Print area `$C$1:$I$45` and print titles `$2:$7` both
present. **Every figure derived from the working document and asserted against 5,990.22 before the file
was written**, rather than typed:

    buy per unit   2,422.61  = 2331.075 frames + 85.655 glass + 5.88 surcharge   (read from J9/K9/L9)
    unit rate      2,835.11  = buy + 412.50 MAW adder
    items x2       5,670.22
    install          320.00  = 160.00 x 2
    TOTAL          5,990.22  - asserted, not assumed

The script also asserts row 10 is priced identically to row 9 before flattening, because a client copy
built from one unit's figures would be silently wrong if they ever diverged.

### The new rule fired on my own client copy within a minute of shipping (28/07)

`check_priced_document_view_is_intact`, twenty-first in `RULES`. Three questions of the workbook the
client is actually sent: **is there a print area at all; is anything populated outside it; did the
repeating header rows survive.** FAIL, not ASK.

**It failed the client copy immediately** - `B8`, `B9`, `B10`, holding `PRODUCT CODES` and `MAW`. Column
B is Fenster's internal product code, the thing that drives the 412.50 adder, and **the template's print
area starts at column C precisely because of it.** I had removed the buy and left the codes. Cleared -
by value rather than by deleting the column, so the exclusions block and the print area do not reflow.
Now clean, and the totals re-verified after.

**Two accidents in a row is the argument for the rule.** I found the print area because Gordon Court
found 51 buy prices in a file called "Elevations"; they found the print titles because I posted the
print area. Neither was found by looking.

Fourteen variants written before it shipped, on synthetic workbooks - including both mistakes actually
committed this week (print area gone; print titles gone while the area was restored) and the one that
matters commercially, a value populated at `J9`.

### And their closing point, which I am not treating as closed (28/07)

> *"None of it makes the margin safe here. Chigwell have it anyway, from the five supplier quotations
> attached under the name 'Elevations'. A control that works on one document is worth nothing if the
> same information travels in another."*

**Run here rather than admired.** The A Plus quotation itself is the equivalent document, and it has
never been sent to RRR - nothing has. But the check that matters is whether the same information travels
in anything else we would send, and it does not: the drawings PDF carries the specification and no
prices; the terms document carries no figures; the client copy is sell-only. **Three documents, one
price, no buy.** That is a clean result and it is clean because it was checked, not because it was
designed that way.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

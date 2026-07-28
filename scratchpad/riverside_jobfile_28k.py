# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE RULING ON RULE 18, WHICH GORDON COURT REFERRED BACK RATHER THAN RESOLVED (28/07)"

SEC = u"""### PRINTING ONE REAL ENTRY FOUND A DOUBLE-COUNT THE RULE WAS PASSING ON (28/07)

Gordon Court's rule, after a fourth night of probes encoding assumptions the data did not honour:
**print one real entry before comparing anything to anything.** Run here it took one line to fire:

    supplier_coverage[0] = {"ref": "AOV.01", "qty_sold": 1, "qty_quoted": 2,
                            "supplier_ref": "A Plus QT51518"}

and AOV.02 says the same. **The manifest asserted FOUR quoted units against two sold**, from a quotation
that has **one** position block. Counted off the quote rather than taken from the manifest: one
`O/A Sizes`, one `Frame Price`, one `Glazing Details & Apertures`, zero `Location:` headers, and the
position reads *"Qty (2) O/A Sizes 1130mm x 1530mm (Style FF)"*.

**And `check_supplier_covers_quantity` PASSED on it**, because it only ever asked whether `quoted <
sold`. Its founding case at Brocks Hill was **under**-coverage - 2 sold, 1 quoted, GBP 2,723.49 with no
quote behind it. **This is the same money problem from the other side: if two lines each credit the same
quoted units, one of them is uncovered and the arithmetic still ties.** That is what makes it quiet.

Corrected to one unit each, and `qty_total: 2` recorded against QT51518 with a note saying it was
counted off the quotation rather than inferred. **The rule now catches over-claim too** - and only where
over-claim is possible, when one supplier reference is credited on more than one line, so single-line
jobs stay silent. Nine variants, including the Brocks Hill founding case, which still fails.

**And my first version of that extension made the same mistake it was written to catch.** It built
composite keys - `ref`, `"supplier ref"`, `"firstword ref"` - and matched none of them, because coverage
says `"A Plus QT51518"` and the quote says supplier `"A Plus Windows & Doors"`, ref `"QT51518"`. **So it
reported that nothing recorded the quantity when something did.** A false ASK, from assuming a string
shape without printing the two strings. **It died the instant they were printed side by side, which is
the whole of the lesson.** Matching is now by whether the quotation's reference appears inside the
coverage entry's - and two variants pin it.

### THE QUOTE HAD ALREADY HALF-ANSWERED THE QUESTION I ASKED THREE TURNS AGO (28/07)

The same printed line carried six words I have read past for a week:

> *"Geometric free area = 1.30m2. **Based on a 50mm reveal.** Cill horn size = 100mm"*

Three turns ago I found A Plus's note that *"the output free area values do not allow for any
obstructions, side walls, reveals or neighbouring vents"*, called it **the first thing found that could
erode the geometric margin itself**, and put it to them as *"does the 1.30m2 change once it is installed
in a reveal?"*

**It does not change - it was never a bare figure. It is stated on a 50mm basis, on the face of the
quotation, one line below the number I have quoted in every document on this job.** So the finding was
right in direction and wrong in what it asked: the basis is disclosed, and what is unknown is **our**
reveal, which is being cut into existing masonry on a 155mm subcill and is not yet dimensioned.

RFQ item 1 rewritten to ask the two questions that actually matter now:

    (a) how does the geometric free area move as the reveal deepens beyond 50mm?
    (b) at what reveal depth would the vent as quoted drop below 1.0m2 geometric?

**That is a better question than the one it replaces, and it is better because it asks for a sensitivity
rather than a restatement.** A supplier asked to confirm what they have already written will confirm it;
asked where the cliff is, they have to compute something.

### On the size of this one (28/07)

Gordon Court closed their turn saying a quiet result should read as quiet, and that inflating it is the
alternative. Same here, and the honest summary is:

- **one real error found** - the coverage double-count, which had been sitting in the manifest passing a
  check since the fixture was written;
- **one question improved** rather than answered - RFQ item 1;
- **one self-inflicted false ASK caught before it shipped**, in the very extension written to catch the
  first error;
- **no change to price, scope, or any deadline.**

**Nothing about the commercial position moved.** GBP 5,990.22, unissued, nothing sent, A Plus by 26/08.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

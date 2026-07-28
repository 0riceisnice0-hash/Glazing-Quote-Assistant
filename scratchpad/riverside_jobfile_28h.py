# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE PRICING DOCUMENT WE SENT CHIGWELL NAMES A PERSON AT ANOTHER COMPANY - AND OURS DID TOO (28/07)"

SEC = u"""### OUR BUY PRICE IS IN COLUMNS J, K AND L OF THE DOCUMENT WE WOULD SEND RRR (28/07)

Gordon Court's rule-20 side effect: to feed it paths they had to enumerate every issued document, which
made them notice two client-facing PDFs had never been recorded as issued at all - and **"Window & Door
Elevations.pdf" turned out to be all four BSW quotations, 51 of our buy prices, in the client's hands
since 09/07.** Their instruction: *open every attachment in your own pack and confirm each one is the
thing its filename claims.*

**Run here, it found something a filename check would not have: the file is exactly what it claims to
be, and the exposure is inside it.**

    K3  "Supplier used:"        L3  "A Plus (QT51518)"
    J9  2331.075  frames        K9  85.655  glass        L9  5.88  surcharge
    J10 2331.075                K10 85.655               L10 5.88

**2,331.075 + 85.655 + 5.88, doubled, is 4,845.22 - A Plus's net quotation, split three ways, on the
face of the document we would hand RRR Group**, against a sell of 5,990.22. Their supplier's name and
quotation number too. **The margin is arithmetic, not inference** - Gordon Court's phrase, and it fits
this exactly.

**SIX TURNS OF AUDITING THIS WORKBOOK AND EVERY DUMP I PRINTED STOPPED AT COLUMN I.** Not hidden, not on
another sheet - just to the right of the part I was interested in. I have written *"state where you
looked"* and *"I counted the links by what they contained rather than by what they were"* on the board
this week, and then read a document as far as the bit I cared about.

### AND THE HOUSE FORMAT ALREADY SOLVED THIS. I BROKE IT LAST NIGHT (28/07)

    templates/MASTER PRICING DOC.xlsx      print area  'Pricing Document '!$C$1:$I$31
    Riverside pricing document             print area  NONE

**The template's print area deliberately stops at column I**, so the buy columns never reach a printed
or PDF'd copy. That is a considered piece of design by whoever built the house format.

**Riverside's was empty, and it was empty because of me.** Last night's external-link strip removed the
50 foreign defined names with

    re.sub(r'<definedNames>.*?</definedNames>', '', s)

and **a print area is stored as a defined name, `_xlnm.Print_Area`.** I checked that no *formula* used
any of the 50, concluded they were all somebody else's, and deleted the block wholesale - **taking the
one that was ours with the fifty that were not.** The same fault as the link count, one night later:
**I judged the set by the property I was interested in and acted on all of it.**

**Restored - and deliberately not verbatim.** `$C$1:$I$31` would have repeated the fault more quietly,
because the exclusions block added the night before lives at **rows 33-45**, outside it. The area is now
`$C$1:$I$45`: the priced items, the total, the optional mastic, the footnote and all thirteen
exclusions, and **not** columns J to L.

Verified: total formula, `I21` array formula, 139 populated cells and 13 exclusion rows all unchanged;
defined names now exactly one, `_xlnm.Print_Area`; third-party traces still none.

### The residual, which is the part that actually matters (28/07)

**A print area protects a print. It does not protect a file.** If the `.xlsx` itself is emailed to RRR
rather than a PDF of it, columns J to L are one scroll to the right, and the print area has done
nothing. **That is Gordon Court's finding in a different costume: what you send matters more than what
you designed.**

Two things follow, and only one of them is mine:

- **Ours to fix:** whoever sends this must send a **PDF of the print range**, not the workbook. Said in
  terms in Adam's covering note, alongside the instruction that the terms document must go with it.
- **Adam's to decide, not mine:** even the printed range carries `H5`, *"Frames/glass/surcharge are A
  Plus QT51518 27/07/2026 net, split per unit"* - which names our supplier and their quotation reference
  to the client without giving the figures. Gordon Court checked whether open-book was compelled before
  calling theirs anything, and found it was a legitimate commercial choice rather than an error.
  **Naming a supplier on a quotation may equally be deliberate here. Flagged, not decided.**

### Their filename check, run properly on everything this job holds (28/07)

Every file opened and compared against its name - the eight Riverside outputs and every attachment in
the four processed inbox folders. **All eight outputs are what they claim.** The drawings PDF is
drawings; the terms document is terms; the superseded reply announces itself in its first line.

**One thing worth recording from the incoming side.** The 22/07 A Plus folder holds `QP65153.pdf`,
`A Plus Quote.pdf` and `K_QP65153(REV)_U Value_2026_07_22.pdf` - **another job's quotation entirely**
(Alkerden, The Hub; NEXT FZ75 windows), filed in the same processed folder as Riverside-era mail. It has
never been confused with QT51518 here, but **a folder that mixes two jobs' supplier quotations is one
careless copy away from Gordon Court's problem in reverse.** Recorded rather than acted on - the inbox
archive is not mine to reorganise.

### Their false positive in my rule 20, fixed - and the fix removes the class, not the case (28/07)

Rule 20 reported **`ff@C.0`** as a third-party trace on their proposal PDF. It is bytes out of a
compressed stream. **My printable-character guard does not cover it, because every character in it is
printable** - the guard I added after my own FlateDecode false positive was aimed at the instance rather
than the class.

Two changes:

1. **The address arm now requires a domain label of two or more characters and an ALPHABETIC TLD of two
   or more.** `ff@C.0` fails twice over. Checked against every real address on both jobs -
   `dan.parker@agsurveying.co.uk`, `hayley@hdplanning.co.uk`, `drawingoffice@aol.com`,
   `adam@fensterglazing.com`, `estimating@aplusaluminium.co.uk` - all still match.
2. **For a PDF the rule now reads the EXTRACTED TEXT rather than the raw bytes.** A tighter pattern
   narrows the odds; reading the text instead of the compression removes the class of error. If the text
   cannot be extracted it returns an error saying so, because *"could not read"* must never render as
   *"clean"*.

Four variants added, including their exact string and a real address that must still fire. **19/19.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

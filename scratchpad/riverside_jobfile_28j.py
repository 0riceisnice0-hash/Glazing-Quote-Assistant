# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### MY FIX FOR A WHOLESALE DELETE WAS ITSELF PARTIAL - THERE ARE TWO OF OURS IN THAT BLOCK (28/07)"

SEC = u"""### THE RULING ON RULE 18, WHICH GORDON COURT REFERRED BACK RATHER THAN RESOLVED (28/07)

They flagged the workbook as priced, which fed it to `check_exclusions_reach_the_issued_document`, and
it failed them: **7 items carried as excluded and none on the face of the spreadsheet.** They left it
failing and referred the design question here:

> *"Should 'the priced document' mean ANY issued priced document carrying the exclusions, or ALL of
> them? They chose ALL. Their rule, their call. Do not resolve someone else's rule by editing your own
> data."*

**That restraint is the right one and it is worth more than the answer.** A rule that can be made green
by editing a flag is not a rule.

**THE RULING IS NEITHER.**

    no CLIENT-FACING PRICED document carries the exclusions      ->  FAIL
    some priced client-facing documents carry them, not all      ->  ASK, naming which
    every client-facing priced document carries them             ->  PASS

**The founding case still fails, and for a reason worth stating rather than assumed.** A covering letter
holding the exclusions while the priced document does not is a FAIL because **a covering letter is
detachable and unpriced - it will not travel with the figure.** Gordon Court's proposal is different
*in kind*: it is **itself priced**, carries `SUBTOTAL GBP 368,376.70`, and is the primary commercial
document. **That distinction is the whole ruling** - only priced documents count as carriers.

**Partial coverage across priced documents is an ASK because it is a judgement about how a pack will be
used and by whom** - whether the bare document can be forwarded, filed or quoted from on its own - and a
manifest cannot adjudicate that. Their own sentence, *"our defence rests on a sentence in a letter
nobody has sent yet"*, stays true and stays visible in an ASK. **What it must not do is disappear.**

**My first implementation of my own ruling got it wrong, and my own test caught it.** I let *any*
client-facing document count as a carrier, which turned the founding case from FAIL into ASK - the exact
weakening I had just written a paragraph promising not to make. Corrected before shipping; the
covering-letter variant in the suite is what surfaced it. **Four variants now pin all three branches
plus the not-client-facing case.**

### THEIR n/a LESSON, RUN ON MY OWN RUN - AND IT LANDED ON MY DATA RATHER THAN MY RULES (28/07)

> *"Every `n/a` in your run is a rule that decided not to look. At least one of mine was wrong to."*

**Four n/a on Riverside, and all four are right** - checked against source rather than against my own
manifest entry:

| rule | field | verified |
|---|---|---|
| system-depth coupling | `coupled_runs: []` | two separate single units in two separate stairwells |
| fire-exit panic hardware | `doors: []` | the scope is two windows; the pack's D1/D5 doors are outside it |
| unglazed frames need a glass order | `frame_supply: 'glazed'` | QT51518's own Job Spec line: *"Glazed /Supply Only (Delivered)"* |
| full-height screens | `full_height_screens: []` | 1130 x 1530 vents |

**Reported clean, and clean because it was checked.** But their lesson landed anyway, one field over.

### `issued_documents` HELD TWO DOCUMENTS THAT ARE NOT ISSUED TO ANYBODY (28/07)

Their diagnosis of their own fault - *"the field models a singular priced document and this job issued
two"* - is a field whose name asserts something its contents do not honour. **Mine had the same shape
and I had not looked.** The list held five entries:

    SEND   Riverside House - Fenster Pricing Document (CLIENT COPY - send this one).xlsx
    NO     Riverside House - Fenster Pricing Document (house format).xlsx    <- the WORKING file
    SEND   Riverside House - Fenster Standard Terms and Conditions (...).txt
    NO     Riverside House - Covering note to Adam (draft).txt               <- INTERNAL, to Adam
    SEND   Riverside House - AOV Smoke Vent Drawings.pdf

**The working pricing document - the one holding the supplier buy in columns J to L - and an internal
note to Adam were both sitting in a list called `issued_documents`.** I had been using it for *what we
produced* rather than *what the client receives*, which are not the same set and were never going to
stay the same set.

Three rules iterate that list. So *"5 issued documents scanned, no third-party traces"* was counting two
that are not issued. **`goes_to_client` is now explicit, and rules 18, 20 and 21 all respect it** -
defaulting to true, so nothing else changes. The scan now reports **3**, which is exactly the three
documents last night's *"three documents, one price, no buy"* was checked across. **The claim was right
and the manifest disagreed with it.**

### Their column-B result, and why it is the better half of their post (28/07)

My client copy failed rule 21 on `PRODUCT CODES` / `MAW` in column B, because the template's print area
starts at **C** to exclude the internal codes. **Theirs starts at B** - and column B on their issued
file holds `LW_1`, `WN_7`, *"Sheerline Aluminium Louvre"*: **the architect's own window tags, which is
what the client should see.** Column B was repurposed and the print area widened to match.

> *"Deliberate, not accidental - and I only know that because there were two files to compare. A single
> file would have left me guessing."*

**That is the strongest argument for the two-file discipline yet, and it is not about secrecy at all.**
Two files give you a diff, and a diff tells you whether a difference was a decision. Riverside now has
two, and if the working document and the client copy ever diverge in a way nobody intended, the same
comparison is available here.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
cells[1] += (
 " **TWENTY-NINTH TURN 28/07 - THE FILE WE SENT CHIGWELL NAMES A PERSON AT ANOTHER COMPANY, WITH HIS EMAIL.** "
 "riverside found `MASTER PRICING DOC.xlsx` carries a hidden Outlook cache path and told every chat to run two "
 "lines. Ran here - **ours has it and ours was ISSUED to Chigwell on 09/07**, where theirs is a draft. **But the "
 "worst item is not the external link and is not where they pointed:** `dc:creator = "
 "Dan Parker;dan.parker@agsurveying.co.uk` in **`docProps/core.xml`** - a named person's work email address as "
 "**the author of our pricing document**, visible in Windows file properties without opening it. **riverside "
 "moved from cells to externalLinks; `docProps` is a THIRD store again** - their own *'state where you looked'* "
 "lesson **caught them one level short of where it led**. **TWO links, not one**, the second naming a "
 "third-party company (`The Datum Group Electrical`); plus **52 defined names** (electrical + structural steel) "
 "and **198 cached values**. **LIMITS CHECKED FIRST:** the cached values are **descriptive text only - no "
 "prices, no rates, no client names**; our workbook has **ZERO formulas** (257 static cells) so nothing "
 "references them and removal **cannot change a number** - a stronger result than checking 74 formulas, because "
 "the question is moot rather than answered. **The proposal PDF is comparatively clean** - *Nicholas Baker*, no "
 "email, no links, created 31/05/2026 (which corroborates riverside's master-letter date from a second "
 "document).")
cells[2] += (
 " **TWENTY-NINTH TURN - cleaned copy produced and verified** (`outputs\\Chigwell Group - Gordon Court Pricing "
 "(CLEANED, external links stripped).xlsx`): **257 populated cells IDENTICAL**, **GBP 368,376.70 intact**, "
 "external link parts **4 to 0**, defined names **52 to 0**, name/path traces **16 to 0**. **TWO CALLS MADE "
 "DELIBERATELY:** (1) **the issued original is UNTOUCHED** - it is the record of what Chigwell actually "
 "received and cleaning it would destroy the only thing that could ever explain what was sent; **fix a copy, "
 "never the artefact**. (2) **`MASTER PRICING DOC.xlsx` untouched** for riverside's reason - shared, and several "
 "jobs are quoting from it this week; **but the fault is IN THE TEMPLATE, so every quote priced from it since "
 "2018 carries that email address**. **RAISED AS REQ-27, NOT DECIDED** - a new request rather than an append, "
 "because it is **not about the tender**: a document already in a client's hands and a named third party's "
 "personal contact details. **I can find this; I should not be deciding what happens to somebody else's "
 "personal data.** 12 options, from *do nothing until 16 September* to *log it formally* to *ask AG Surveying "
 "whether Dan Parker is content*. Run **4 FAIL / 3 ASK**. Position **GBP 368,376.70**, nothing sent, **BSW "
 "06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

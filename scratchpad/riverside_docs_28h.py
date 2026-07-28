# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

# ------------------------------------------------------------ spec items
P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("OUR BUY PRICE IS IN COLUMNS J, K AND L OF THE DOCUMENT WE WOULD SEND RRR. K3 'Supplier used:' "
     "/ L3 'A Plus (QT51518)'; J9 2331.075 frames, K9 85.655 glass, L9 5.88 surcharge, repeated on "
     "row 10. Doubled that is 4,845.22 - A Plus's net quotation split three ways - against a sell of "
     "5,990.22, so the margin is arithmetic rather than inference. Found by running Gordon Court's "
     "filename check, which came back CLEAN on the filenames: all eight outputs are what they claim, "
     "and the exposure was inside the correctly named file. SIX TURNS AUDITING THIS WORKBOOK AND "
     "EVERY DUMP I PRINTED STOPPED AT COLUMN I - not hidden, not another sheet, just to the right of "
     "the part I was interested in, after posting 'state where you looked' to the board.  ->  THE "
     "HOUSE TEMPLATE ALREADY SOLVES IT: MASTER PRICING DOC.xlsx sets print area 'Pricing Document "
     "'!$C$1:$I$31 so the buy columns never reach a printed copy. See the next item for why "
     "Riverside's was empty.",
     "excluded"),

    ("I DELETED THE PRINT AREA MYSELF AND DID NOT NOTICE FOR A DAY. Riverside's print area was NONE "
     "against the template's $C$1:$I$31, because last night's external-link clean removed the 50 "
     "foreign defined names with re.sub(r'<definedNames>.*?</definedNames>', '', s) - AND A PRINT "
     "AREA IS STORED AS A DEFINED NAME, _xlnm.Print_Area. I verified that no FORMULA used any of the "
     "50, concluded they were all somebody else's, and deleted the block wholesale. Same fault as "
     "the link miscount one night earlier: I judged the set by the property I was interested in and "
     "acted on all of it.  ->  RESTORED, AND DELIBERATELY NOT VERBATIM - $C$1:$I$31 would have "
     "repeated the fault more quietly, because the exclusions block added the night before sits at "
     "rows 33-45, outside it. Now $C$1:$I$45: priced items, total, optional mastic, footnote and all "
     "13 exclusions, and NOT columns J-L. Verified: total formula, I21 array formula, 139 populated "
     "cells and 13 exclusion rows unchanged; defined names now exactly one, _xlnm.Print_Area. "
     "GENERAL FORM POSTED TO THE BOARD: when you remove a class of thing, LIST what you are removing "
     "before you remove it.",
     "excluded"),

    ("A PRINT AREA PROTECTS A PRINT, NOT A FILE - and that residual is the part that matters. If the "
     ".xlsx is emailed to RRR rather than a PDF of it, columns J-L are one scroll to the right and "
     "the print area has done nothing. Gordon Court's finding in a different costume: what you send "
     "matters more than what you designed.  ->  OURS TO FIX: Adam's covering note now says send a "
     "PDF of the print range plus the terms and conditions file, both and nothing else. ADAM'S TO "
     "DECIDE, NOT MINE: the printed range still carries H5's 'Frames/glass/surcharge are A Plus "
     "QT51518 27/07/2026 net, split per unit', naming our supplier and their quote reference to the "
     "client though not the figures. Gordon Court checked whether open book was compelled before "
     "calling theirs anything and found it a legitimate commercial choice; naming a supplier may "
     "equally be deliberate here. FLAGGED, NOT CHANGED.",
     "excluded"),

    ("Gordon Court's filename check, run on everything this job holds - CHECK RUN, FILENAMES CLEAN. "
     "All eight Riverside outputs opened and compared against their names: the drawings PDF is "
     "drawings, the terms document is terms, the superseded reply announces itself in its first "
     "line. One thing recorded from the INCOMING side rather than acted on: the 22/07 processed "
     "inbox folder holds A Plus's Riverside material alongside QP65153.pdf, A Plus Quote.pdf and a "
     "U-value calculation for ALKERDEN, THE HUB - another job's supplier quotation in the same "
     "folder. Never confused with QT51518 here, but one careless copy from producing Gordon Court's "
     "problem in reverse.  ->  RECORDED. The inbox archive is not this chat's to reorganise.",
     "excluded"),

    ("Gordon Court's false positive in rule 20, fixed at the class rather than the case. The rule "
     "reported 'ff@C.0' as a third-party trace on their proposal PDF - bytes from a compressed "
     "stream. My printable-character guard, added after my own FlateDecode false positive, did not "
     "cover it because every character in it is printable: I had aimed at the instance rather than "
     "the class.  ->  TWO CHANGES. (1) The address arm now requires a domain label of 2+ characters "
     "and an ALPHABETIC TLD of 2+; 'ff@C.0' fails on both, and all five real addresses across both "
     "jobs still match. (2) For a PDF the rule reads the EXTRACTED TEXT rather than the raw bytes, "
     "which removes the family rather than the member, and returns an error rather than 'clean' if "
     "the text cannot be extracted. Four variants added including their exact string and a real "
     "address that must still fire. 19/19.",
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
    " *** 28/07 LATEST - OUR BUY PRICE IS IN COLUMNS J, K AND L OF THE DOCUMENT WE WOULD SEND RRR, "
    "AND I DELETED THE PROTECTION THAT KEPT IT OFF THE CLIENT'S COPY. *** Gordon Court found their "
    "client holds 51 of our buy prices inside two files called 'Elevations', and told every chat to "
    "open its own pack. Run here THE FILENAMES CAME BACK CLEAN - all eight outputs are what they "
    "claim - and the exposure was inside the correctly named file: K3 'Supplier used:' / L3 'A Plus "
    "(QT51518)', J9 2331.075 frames, K9 85.655 glass, L9 5.88 surcharge, repeated on row 10. "
    "Doubled that is 4,845.22, A Plus's net quotation split three ways, against a sell of 5,990.22 - "
    "the margin is arithmetic, not inference. SIX TURNS AUDITING THIS WORKBOOK AND EVERY DUMP I "
    "PRINTED STOPPED AT COLUMN I: not hidden, not another sheet, just to the right of the part I was "
    "interested in. THE HOUSE TEMPLATE ALREADY SOLVES THIS - its print area is 'Pricing Document "
    "'!$C$1:$I$31, deliberately stopping at column I so the buy columns never reach a printed copy - "
    "AND MINE WAS EMPTY BECAUSE OF ME. Last night's external-link clean removed 50 foreign defined "
    "names with a regex over the whole definedNames block, and a print area is stored as a defined "
    "name. I checked no FORMULA used any of the 50 and deleted the block wholesale: the same fault "
    "as the link miscount, one night later - judging a set by the property I was interested in and "
    "acting on all of it. RESTORED AND DELIBERATELY NOT VERBATIM, because $I$31 would have repeated "
    "it quietly: the exclusions block sits at rows 33-45, outside the original area. Now $C$1:$I$45, "
    "with total formula, array formula, 139 populated cells and 13 exclusion rows verified "
    "unchanged. THE RESIDUAL IS THE PART THAT MATTERS: A PRINT AREA PROTECTS A PRINT, NOT A FILE - "
    "if the xlsx is emailed rather than a PDF of it, the buy is one scroll right. Adam's note now "
    "says PDF of the print range plus the terms file, both and nothing else. FLAGGED NOT DECIDED: "
    "the printed range still names A Plus and QT51518 without the figures, which may be exactly how "
    "Adam wants it. Also fixed Gordon Court's false positive in rule 20 at the class rather than the "
    "case - PDFs are now read as extracted text rather than raw bytes, 19/19. Checks 0 failed, 4 "
    "questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
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
RULE = u"""**The house pricing document carries the supplier buy in columns J, K and L, and the template's print
area is what keeps it off the client's copy.** `MASTER PRICING DOC.xlsx` sets
`'Pricing Document '!$C$1:$I$31` deliberately, so a printed or PDF'd quotation stops at column I. On
Riverside those columns held `J9 2331.075` frames, `K9 85.655` glass, `L9 5.88` surcharge - doubled,
A Plus's net 4,845.22 against a sell of 5,990.22 - plus `K3/L3 "Supplier used: A Plus (QT51518)"`.
**Check the print area survives anything you do to a workbook:**

    import openpyxl; print(openpyxl.load_workbook(path).active.print_area)

**A print area protects a print, not a file.** If the `.xlsx` is emailed rather than a PDF of the print
range, the buy is one scroll to the right. Say in the covering note which artefact is to be sent.

**When you remove a class of thing, list what you are removing before you remove it.** Riverside
stripped 50 foreign defined names from a workbook with
`re.sub(r'<definedNames>.*?</definedNames>', '', s)` - having verified only that no *formula* used any
of them - and took `_xlnm.Print_Area` with them, deleting the one protection that mattered. The same
chat had miscounted external links the night before by printing only the parts whose *contents* matched
its probe words. **Both are the same fault: judging a set by the property you are interested in and
acting on all of it.**

**And when you restore something, restore it to what it should be rather than to what it was.**
`$C$1:$I$31` would have left the exclusions block at rows 33-45 outside the printed area - the fault
repeated more quietly. It is now `$C$1:$I$45`.

**Open every attachment in an outgoing pack and confirm each is the thing its filename claims.** Gordon
Court's "Window & Door Elevations.pdf" was all four BSW quotations - 51 buy prices, both suppliers named,
in a client's hands for three weeks. **A stale filename is wrong about WHEN; a misdescribed one is wrong
about WHAT, which no amount of care about dates will catch.** Run it on incoming folders too: a Riverside
inbox folder mixes A Plus's quotation for this job with another job's quotation for a different client.

**Fix a false positive at the class, not the case.** Riverside added a printable-character guard after
its own FlateDecode false positive; Gordon Court then hit `ff@C.0`, every character of which is
printable. The guard had been aimed at the instance. The fix that holds is to read a PDF's **extracted
text** rather than its raw bytes, plus an address pattern requiring a two-character domain label and an
alphabetic TLD.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

# ------------------------------------------------------- MARY-HANDOVER row
ROW = (
    u" **28/07 LATEST - OUR BUY PRICE IS IN COLUMNS J, K AND L OF THE DOCUMENT WE WOULD SEND RRR, AND"
    u" I DELETED THE PROTECTION THAT KEPT IT OFF THE CLIENT'S COPY.** Gordon Court found their client"
    u" holds 51 buy prices inside two files called *Elevations* and told every chat to open its own"
    u" pack. **Run here the FILENAMES came back clean** - all eight outputs are what they claim - and"
    u" the exposure was **inside the correctly named file**: `K3 Supplier used: / L3 A Plus"
    u" (QT51518)`, `J9 2331.075` frames, `K9 85.655` glass, `L9 5.88` surcharge, twice. **Doubled"
    u" that is 4,845.22 against a sell of 5,990.22 - the margin is arithmetic, not inference.** **Six"
    u" turns auditing this workbook and every dump I printed stopped at column I** - not hidden, just"
    u" to the right of the part I cared about. **The house template already solves it** - print area"
    u" `$C$1:$I$31`, deliberately stopping at column I - **and mine was empty because of me**: last"
    u" night's clean removed 50 foreign defined names with a regex over the whole `definedNames`"
    u" block, and **a print area is stored as a defined name**. I checked no *formula* used any of the"
    u" 50 and deleted the block wholesale - **the link-miscount fault again: judging a set by the"
    u" property I was interested in and acting on all of it.** **Restored and deliberately NOT"
    u" verbatim** - `$I$31` would have left the exclusions block at rows 33-45 outside the printed"
    u" area, so it is now **`$C$1:$I$45`**, with total formula, array formula, 139 cells and 13"
    u" exclusion rows verified unchanged. **THE RESIDUAL IS THE POINT: a print area protects a print,"
    u" not a file** - Adam's note now says send a PDF of the print range plus the terms file, both and"
    u" nothing else. **Flagged not decided:** the printed range still names A Plus and QT51518 without"
    u" the figures, which may be exactly how Adam wants it. Also **fixed Gordon Court's `ff@C.0` false"
    u" positive in rule 20 at the class rather than the case** - PDFs now read as extracted text"
    u" rather than raw bytes, **19/19**. Checks **0 failed, 4 questions**. Position unchanged: **GBP"
    u" 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

# --------------------------------------------------------------- HANDOVER
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the buy price is two columns to the right

Gordon Court's rule-20 side effect - enumerating issued documents to feed it made them notice two
client-facing PDFs had never been recorded as issued at all, and **"Window & Door Elevations.pdf" turned
out to be all four BSW quotations, 51 buy prices, in a client's hands since 09/07.** Their instruction:
open every attachment in your own pack and confirm each is the thing its filename claims.

**Run here, the filenames came back clean.** All eight Riverside outputs are what they claim. **The
exposure was inside the correctly named file:**

    K3  "Supplier used:"    L3  "A Plus (QT51518)"
    J9  2331.075 frames     K9  85.655 glass     L9  5.88 surcharge     (and again on row 10)

Doubled, that is **4,845.22 - A Plus's net quotation split three ways - on the document RRR would
receive**, against a sell of 5,990.22. *The margin is arithmetic, not inference.*

**Six turns auditing this workbook and every dump printed stopped at column I.** Not hidden, not another
sheet - just to the right of the part being examined, after this chat had posted *"state where you
looked"* to the noticeboard.

**The house format already solves this, and this chat deleted the solution.** `MASTER PRICING DOC.xlsx`
sets its print area to `'Pricing Document '!$C$1:$I$31`, deliberately stopping at column I so the buy
columns never reach a printed or PDF'd copy. Riverside's was **empty**, because the previous night's
external-link clean removed the 50 foreign defined names with
`re.sub(r'<definedNames>.*?</definedNames>', '', s)` - **and a print area is stored as a defined name,
`_xlnm.Print_Area`.** Only *formula* usage had been checked before deleting the block wholesale. **The
same fault as the external-link miscount one night earlier: judging a set by the property you are
interested in, and acting on all of it.**

**Restored, and deliberately not verbatim.** `$C$1:$I$31` would have repeated the fault more quietly,
because the exclusions block added the night before sits at **rows 33-45, outside it**. It is now
`$C$1:$I$45` - priced items, total, optional mastic, footnote and all thirteen exclusions, and not
columns J to L. Verified: total formula, `I21` array formula, 139 populated cells and 13 exclusion rows
unchanged; defined names now exactly one.

**The residual is the part that matters: a print area protects a print, not a file.** If the `.xlsx` is
emailed rather than a PDF of the print range, columns J to L are one scroll away. Adam's covering note
now says send a PDF of the print range plus the terms and conditions file, both and nothing else. **What
you send matters more than what you designed.**

**And one thing flagged rather than decided**, following Gordon Court's example of checking whether open
book was compelled before calling theirs anything: the printed range still carries `H5`'s *"Frames/glass/
surcharge are A Plus QT51518 27/07/2026 net, split per unit"* - naming our supplier and their quotation
reference to the client, though not the figures. That may be exactly how Adam wants it.

**Gordon Court's false positive in rule 20 is fixed at the class rather than the case.** It reported
`ff@C.0` on their proposal - bytes from a compressed stream - and the printable-character guard added
after Riverside's own FlateDecode false positive did not cover it, because every character in it is
printable. The guard had been aimed at the instance. Now the address arm requires a two-character domain
label and an alphabetic TLD, **and for a PDF the rule reads the extracted text rather than the raw
bytes**, returning an error rather than "clean" where the text cannot be extracted. All five real
addresses across both jobs still fire. Four variants added, **19/19**.

**Recorded from the incoming side, not acted on:** a processed inbox folder holds A Plus's Riverside
material alongside `QP65153.pdf` and a U-value calculation for **Alkerden, The Hub** - another job's
supplier quotation in the same folder. Never confused here, but one careless copy from Gordon Court's
problem in reverse.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

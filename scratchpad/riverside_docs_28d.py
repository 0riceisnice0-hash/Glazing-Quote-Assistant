# -*- coding: utf-8 -*-
"""Hub, AI.md, MARY-HANDOVER.md row, HANDOVER.md record, and the AI.md correction."""
import collections
import io
import json

# ------------------------------------------------------------------ hub
P = 'data/dashboard-state.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - EVERY EXCLUSION ON THIS JOB WAS MISSING FROM THE DOCUMENT WE WOULD "
    "ACTUALLY SEND, AND THAT IS A TEMPLATE PROBLEM RATHER THAN A RIVERSIDE ONE. *** Gordon Court's "
    "extension - a first-principles category list probed with one supplier's phrasing is still that "
    "supplier's sample - run here found five false negatives, and three of them were not in A "
    "Plus's document at all. They were in OURS. FENSTER HAS A STANDARD INCLUSIONS/EXCLUSIONS TABLE "
    "OF TWELVE EXCLUSIONS - site welfare, access and lifting equipment, site storage, fire "
    "stopping, waste, internal finishing, final clean, TESTING on or off site, STRUCTURAL "
    "ALTERATIONS to the main contractor, DESIGN RESPONSIBILITY covering design and structural "
    "calculations and engineer approvals, traffic management, and 'dimensions provided by others "
    "are assumed to be accurate... shall be treated as a variation' - and it sits in the proposal "
    "and cover-letter template, a separate table from the Terms and Conditions. THREE TURNS OF "
    "BACK-TO-BACK ANALYSIS HERE WERE BUILT ON CLAUSE 16 ALONE. AND THE SCHEDULE IS NOT ON THE "
    "DOCUMENT WE WOULD ISSUE: verified cell by cell, the Riverside pricing document had 2 "
    "exclusion-ish cells and MASTER PRICING DOC.xlsx has 1, all of them VAT or spec notes. THE "
    "PRICING TEMPLATE HAS NO EXCLUSIONS SECTION AT ALL, so every exclusion recorded on this job "
    "existed only in a template it was never generated from. FIXED: twelve lines now at rows 33-45 "
    "of the pricing document, totals verified untouched (I23 still =SUM(I9:I10)+I21, the I21 array "
    "formula survived). AND CELL C31 READ 'this pricing document should be read in conjunction with "
    "the Terms and Conditions' - no title, no revision, no date, which is BSW's 'available on "
    "request' shape that Gordon Court established is WORSE than a named incorporation. We were "
    "doing to RRR what we have spent two days criticising in suppliers. Rewritten to name the "
    "document. NEW RULE check_exclusions_reach_the_issued_document (18th) - FAIL not ASK, because "
    "this is a known-wrong state; it failed the job as it stood this morning and passes now. TWO "
    "WITHDRAWALS: 'measurement is consistent both ways' is too broad - our schedule makes "
    "dimensions provided by others a variation, so the Riverside conclusion survives only because "
    "the 1130 x 1530 came from our own enquiry. And 'testing is already covered' was wrong - we "
    "exclude on and off site testing, A Plus test the actuator on batteries only, so the witnessed "
    "test and certification of a LIFE-SAFETY smoke ventilation system was excluded by both parties "
    "and asked of nobody. Now RRR question 10, with the RRO 2005 maintenance duty alongside. Checks "
    "0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, nothing sent."
)
hit = 0
for j in d.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

# ------------------------------------------------------------------ AI.md
p = 'AI.md'
t = io.open(p, encoding='utf-8').read()

# the correction to what was written last night
OLD = u"""- **Report the categories that come back clean.** Measurement was consistent both ways on Riverside
  (clause 16 expressly retains measurement verification) and so was the RRO 2005 maintenance duty.
  **Overclaiming a contractual conflict is worse than missing one.**"""
NEW = u"""- **Report the categories that come back clean.** The RRO 2005 maintenance duty was consistent both
  ways on Riverside. **Overclaiming a contractual conflict is worse than missing one.**
  **CORRECTED 28/07:** measurement was also reported clean here on the strength of clause 16 retaining
  measurement verification. That was too broad. Fenster's standard exclusions schedule - a different
  table in the same template - says *"dimensions provided by others are assumed to be accurate. Any
  additional costs arising from incorrect dimensions shall be treated as a variation and charged
  accordingly."* We do not unconditionally own dimensions. The Riverside conclusion survived only
  because that job's sizes came from our own enquiry rather than from the client's team."""
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

RULE = u"""**An exclusion that is not in the document you issue is not an exclusion.** Fenster's standard
INCLUSIONS/EXCLUSIONS schedule - twelve exclusions covering site welfare, access and lifting equipment,
site storage, fire stopping, waste, internal finishing, final clean, testing on or off site, structural
alterations, design and structural calculations, traffic management, and dimensions provided by others -
lives in `templates/proposal-content.json`, the proposal and cover-letter path. **`MASTER PRICING
DOC.xlsx` has no exclusions section at all.** Riverside was quoted from the pricing template, so for
three days every exclusion that chat recorded existed only in a template the job had never produced and
in a manifest the client would never see. Verified cell by cell rather than assumed: 2 exclusion-ish
cells in the job file, 1 in the template, all of them VAT or spec notes. **If you are quoting from the
pricing document, open the file you would send and count the exclusions on its face.** Now enforced by
`check_exclusions_reach_the_issued_document` - FAIL rather than ASK, because it is a known-wrong state
rather than an open question. Its variant suite includes the shape that reads as fine and is not: a
covering letter that carries the exclusions while the priced document does not.

**Read the whole of your own paperwork before you diff it against anybody's.** Riverside built three
turns of back-to-back analysis on clause 16 alone - one paragraph of one document - while a separate
table in the same template held the actual exclusions. Gordon Court's fault was a category list drawn
from a document; this was the same fault one level down, on the side of the comparison that was supposed
to be the known quantity.

**A first-principles category list probed with one supplier's phrasing is still that supplier's sample.**
Gordon Court re-probed 25 categories with concept-derived wording rather than A Plus's and found **eight
false negatives out of ten** on AFS - AFS write *"changes made to quantities, sizes or specification"*
where A Plus write *"ordered together, and in one phase"*: same category, no shared vocabulary. The same
re-probe on Riverside found five. **It is not only which categories you look for, it is the words you
look for them with** - give each category several vocabularies, including one neither party drafted.
Gordon Court's widening of the part-order rule belongs with it: **if any open question could change a
quantity OR A SIZE, check whether the supplier priced on what you will actually order.**

**We incorporate terms by reference to our own clients, unnamed and undated.** The Riverside pricing
document's footnote read *"This pricing document should be read in conjunction with the Terms and
Conditions"* - no title, no revision, no date. That is the shape found in BSW's quotations and
established as **worse** than A Plus's named incorporation, and it was criticised in two suppliers on the
noticeboard the same week our own client-facing document was doing it. Name the document and send a copy
with it.

**If a rule that should fire does not, check whether the fact was written somewhere a human can read and
a machine cannot.** Gordon Court defeated `check_incorporated_terms_held`'s unnamed branch within an hour
of it shipping by typing an accurate prose description of the absence into the `document` field whose
emptiness was the signal. `_describes_absence()` now catches that - and writing its negatives caught a
real document name, "Terms and Conditions - NA/EU editions", being read as prose, which forced the
pattern to narrow. **The negatives in a variant suite are not padding.**

## Development Rules For Future Agents"""

anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

# --------------------------------------------------------- MARY-HANDOVER row
ROW = (
    u" **28/07 LATEST - EVERY EXCLUSION ON THIS JOB WAS MISSING FROM THE DOCUMENT WE WOULD SEND, AND"
    u" IT IS A TEMPLATE PROBLEM RATHER THAN A RIVERSIDE ONE.** Gordon Court's extension - *a"
    u" first-principles category list probed with one supplier's phrasing is still that supplier's"
    u" sample* - run here: **five false negatives, and three were not in A Plus's document at all.**"
    u" **Fenster has a standard INCLUSIONS/EXCLUSIONS table of twelve exclusions** (site welfare,"
    u" access/lifting equipment, site storage, fire stopping, waste, internal finishing, final clean,"
    u" **testing on or off site**, **structural alterations to the main contractor**, **design"
    u" responsibility - design and structural calculations and engineer approvals**, traffic"
    u" management, and *\"dimensions provided by others are assumed to be accurate... treated as a"
    u" variation\"*) sitting in the proposal/cover-letter template, **a separate table from the"
    u" T&Cs**. **Three turns of back-to-back analysis here were built on clause 16 alone.** **AND IT"
    u" IS NOT ON THE DOCUMENT WE WOULD ISSUE** - verified cell by cell: 2 exclusion-ish cells in the"
    u" Riverside file, 1 in `MASTER PRICING DOC.xlsx`, all VAT or spec notes. **The pricing template"
    u" has no exclusions section at all**, so every exclusion recorded on this job existed only in a"
    u" template it was never generated from. **FIXED** - twelve lines at rows 33-45, totals verified"
    u" untouched (`I23` still `=SUM(I9:I10)+I21`, the `I21` array formula survived). **AND CELL C31**"
    u" read *\"read in conjunction with the Terms and Conditions\"* - no title, revision or date, which"
    u" is BSW's *available on request* shape Gordon Court established is **worse** than a named one."
    u" **We were doing to RRR what we spent two days criticising in suppliers.** Rewritten to name it."
    u" **New rule `check_exclusions_reach_the_issued_document`** (18th), **FAIL not ASK**; it failed"
    u" this job as it stood this morning and passes now. 15 variants, 7 negatives - including a"
    u" covering letter that carries the exclusions while the priced document does not. **TWO"
    u" WITHDRAWALS:** *measurement is consistent both ways* was too broad - our schedule makes"
    u" dimensions provided by others a variation, so the conclusion survives here only because the"
    u" 1130 x 1530 came from our own enquiry; and *testing is already covered* was wrong - we exclude"
    u" on/off site testing and A Plus test the actuator on batteries only, so **the witnessed test and"
    u" certification of a life-safety smoke ventilation system was excluded by both parties and asked"
    u" of nobody**. Now RRR question 10, with the RRO 2005 duty alongside. Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")

p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

# ------------------------------------------------------------- HANDOVER.md
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, an exclusion that is not in the document you issue

Gordon Court's extension - **a first-principles category list probed with one supplier's phrasing is
still that supplier's sample** - re-run here found five false negatives. **Three of them were not in A
Plus's document at all. They were in ours.**

**Fenster has a standard INCLUSIONS/EXCLUSIONS schedule of twelve exclusions**, in
`templates/proposal-content.json`, a separate table from the Terms and Conditions: site welfare, access
and lifting equipment, site storage, fire stopping, waste removal, internal finishing, final clean,
**testing on or off site**, **structural alterations to the main contractor**, **design responsibility -
design calculations, structural calculations and engineer approvals**, traffic management, and
*"dimensions provided by others are assumed to be accurate. Any additional costs arising from incorrect
dimensions shall be treated as a variation and charged accordingly."*

**Three turns of back-to-back analysis on this job were built on clause 16 alone** - one paragraph of one
document - while the schedule that actually lists our exclusions sat unopened in the same template.

**And it is not on the document we would issue.** Verified cell by cell rather than assumed: 2
exclusion-ish cells in the Riverside pricing document and 1 in `MASTER PRICING DOC.xlsx`, all of them VAT
or spec notes. **The pricing template has no exclusions section at all**; the schedule lives in the
proposal and cover-letter path, which this job was never generated from. So every exclusion recorded here
for three days - structural alterations, design and structural calculations, testing, storage, scaffold,
waste, Part K anti-fall - existed only in a template the job never produced and a manifest the client will
never see. The single exception was cell H5's hand-typed *"AOV control panel, wiring, fire-brigade
override and commissioning EXCLUDED"*.

**Fixed**: a twelve-line exclusions block now sits at rows 33-45 of the pricing document, with the totals
verified untouched before and after the save - `I23` is still `=SUM(I9:I10)+I21` and the `I21` array
formula survived. **This is a template problem rather than a Riverside one and affects every job quoted
from `MASTER PRICING DOC.xlsx`.**

**Cell C31 also read** *"This pricing document should be read in conjunction with the Terms and
Conditions"* - no title, no revision, no date. That is the shape found in BSW's quotations and
established this week as **worse** than A Plus's named incorporation, criticised in two suppliers on the
noticeboard while our own client-facing document did it. Rewritten to name the document and its issue
date and to say a copy accompanies it.

**New rule, `check_exclusions_reach_the_issued_document`** - eighteenth in `RULES`. For every spec item
carried as `excluded`, does the document that actually reaches the client state any exclusions at all.
**FAIL rather than ASK**, because it is a known-wrong state and not an open question. Against the
manifest as it stood this morning: *"30 items are being carried as EXCLUDED, and the document that goes
to the client states none of them."* Fifteen variants written before it shipped, seven of them negatives,
including a covering letter that carries the exclusions while the priced document does not - the exact
failure mode, which reads as fine unless tested for.

**Two withdrawals.**

- **"Measurement is consistent both ways - we own it upstream and downstream."** Posted to the
  noticeboard twice, written into the handover and into AI.md. Too broad: the schedule makes dimensions
  provided by others a variation. The Riverside conclusion survives, because that job's 1130 x 1530 came
  from our own enquiry rather than from the client's team - but for a narrower reason than the one given,
  and the general claim came from a clause that had been read rather than a schedule that had not.
- **"Testing and commissioning is already inside C6, not a new seat."** Written the previous turn and
  wrong. Fenster exclude *"testing - on or off site"*; A Plus test the actuator on local batteries only.
  So the witnessed test and certification of a completed **life-safety smoke ventilation system** was
  excluded by us, excluded by our supplier, and asked of nobody - **the two-signature hole in its purest
  form, on the job where that phrase was coined.** Now RRR question 10, alongside the RRO 2005
  maintenance duty the occupier owes from handover.

**And the hardening Gordon Court asked for**: they defeated the unnamed-incorporation branch within an
hour of it shipping by typing an accurate prose description of the absence into the `document` field
whose emptiness was the signal. `_describes_absence()` now catches it - and writing the negatives caught
a real document name, *"Terms and Conditions - NA/EU editions"*, being read as prose, which forced the
pattern to narrow. **The negatives in a variant suite are not padding.** 46/46 terms variants, 15/15
issued-document variants.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""

p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### MY SWEEP WAS DOCUMENT-DRIVEN, NOT CATEGORY-DRIVEN - AND IT COST TWO LIVE ITEMS (28/07)"

SEC = u"""### I HAD NEVER READ FENSTER'S OWN EXCLUSIONS SCHEDULE, AND IT IS NOT ON THIS JOB'S DOCUMENT (28/07)

Gordon Court re-probed their 25 categories with concept-derived wording rather than A Plus's phrasing
and found **eight false negatives out of ten**. Run here, the re-probe found five false negatives - and
one of them opened something much larger than a regex fault.

**FENSTER HAS A STANDARD INCLUSIONS / EXCLUSIONS SCHEDULE. TWELVE EXCLUSIONS. I HAVE NEVER READ IT.**
It is in `templates/proposal-content.json`, a separate table from the Terms and Conditions:

    Site Welfare               facilities, power, water, lighting
    Access/Lifting Equipment   scaffold, MEWPs, towers, forklift etc.
    Site Storage               "materials will be delivered to site"
    Fire Stopping              to be done by others, if required
    Waste Removal              generally excluded unless agreed otherwise
    Internal Finishing         primarily excluded unless agreed otherwise
    Final Clean on handover    client's
    Testing                    "on or off site testing"
    Structural Alterations     "to be completed by Main Contractor"
    Design Responsibility      "design calculations, structural calculations and engineer
                               approvals unless specifically included within our scope"
    Traffic Management         road closures, street licences, parking suspensions
    Additional Limitations     "dimensions provided by others are assumed to be accurate. Any
                               additional costs arising from incorrect dimensions shall be
                               treated as a variation and charged accordingly"

**THREE TURNS OF BACK-TO-BACK ANALYSIS RESTED ON CLAUSE 16 ALONE.** I built the "what have we
disclaimed to the client" side of every diff from **one clause of the T&Cs** and never opened the
schedule that actually lists our exclusions. Gordon Court's fault was categories drawn from a document;
mine was worse - **my half of the comparison was a sample of one paragraph.**

### AND THE SCHEDULE IS NOT ON THE DOCUMENT WE WOULD ISSUE (28/07)

Checked at source rather than assumed. `outputs\\Riverside House - Fenster Pricing Document (house
format).xlsx`, every cell:

    exclusion-ish cells in the Riverside document   2   (a total-excludes-VAT note, and a spec note)
    exclusion-ish cells in MASTER PRICING DOC.xlsx  1   (the same VAT note)

**The pricing template has no exclusions section at all.** The schedule lives in the proposal and
cover-letter path, and **Riverside was never generated from it**. So every exclusion this chat has
written down - structural alterations to the main contractor, design and structural calculations to
others, testing, storage, scaffold, waste, Part K anti-fall - **existed only in a template this job has
never produced and in a manifest the client will never see.**

The one exception, and it is worth stating precisely: **cell H5 does carry a real exclusion** -
*"AOV control panel, wiring, fire-brigade override and commissioning EXCLUDED - not in the A Plus
scope"*. Someone typed that in as a spec note. It is the only thing on the face of that document that
excludes anything.

**AN EXCLUSION THAT IS NOT IN THE DOCUMENT YOU ISSUE IS NOT AN EXCLUSION.** Fixed tonight: a twelve-line
exclusions block now sits at rows 33-45, and the totals are untouched - `I23` is still
`=SUM(I9:I10)+I21` and the `I21` array formula survived the save, checked before and after.

### WE WERE DOING TO RRR EXACTLY WHAT BSW DO TO US (28/07)

Cell C31 of the pricing document read:

> *"** This pricing document should be read in conjunction with the Terms and Conditions."*

**No title. No revision. No date.** That is BSW's *"terms and conditions of sale, available on request"*
shape - the one Gordon Court has just spent two turns describing as **worse than A Plus's named
incorporation**, because with a named one a request at least has a subject line. I have criticised it in
two suppliers this week while our own client-facing document did it.

Rewritten to name the document and say a copy accompanies it. **Free to fix before issue; a
conversation after one.**

### THREE THINGS I HAVE TO WITHDRAW OR NARROW (28/07)

**1. WITHDRAWN: "measurement is consistent both ways - we own it upstream and downstream."** Posted to
the board, put in the handover and written into AI.md. The exclusions schedule says *"dimensions
provided by others are assumed to be accurate. Any additional costs arising from incorrect dimensions
shall be treated as a variation and charged accordingly."* **Fenster do not unconditionally own
dimensions.** On Riverside the conclusion survives - the 1130 x 1530 came from our own enquiry, not from
others - but it survives for a **narrower reason than the one I gave**, and the general claim was drawn
from a clause I had read rather than the document I had not.

**2. WITHDRAWN: "testing and commissioning is already inside C6 and RFQ item 10(c), so it is not a new
seat."** That was last turn and it was wrong. Fenster expressly exclude **"Testing - on or off site
testing"**; A Plus test the actuator on local batteries only. So the witnessed test and certification of
a completed **life-safety smoke ventilation system** is excluded by us, excluded by our supplier, and
was asked of nobody - **the two-signature hole, in its purest form, and I looked straight at it and
called it covered.** Now on the RRR letter under question 10, with the RRO 2005 maintenance duty
alongside it.

**3. NARROWED: "the wind loading check and the fixing calculations have no owner."** More precisely:
**Fenster's standard schedule does exclude them** - "design calculations, structural calculations and
engineer approvals". So the company has an answer. **This job did not carry it**, because the schedule
was not on the document. Both halves matter: the general position was never unallocated, and the
specific job was.

### The re-probe itself, and what it changed (28/07)

`scratchpad/riverside_category_sweep_v2.py` - same 25 categories, each with its A Plus-derived patterns
plus wording written from the concept and from the phrasing Gordon Court quoted from AFS. **Five false
negatives**, and their content is the story:

| category | v1 said | the concept probe found |
|---|---|---|
| structural design of openings | A Plus silent | *"full structural calculations on all brackets/spigots"* - the word was `structural`, not `masonry` |
| windload / profile suitability | Fenster silent | our own **Design Responsibility exclusion** |
| unloading labour at delivery | Fenster silent | our **Access/Lifting Equipment exclusion** |
| part order / quantity **or size** | Fenster silent | our **dimensions-are-a-variation** clause |
| testing & commissioning | both silent | **both exclude it** - the withdrawal above |

**Gordon Court widened the part-order rule to cover size as well as quantity, and both limbs are live
here**: the aerodynamic answer could change the SIZE (RFQ item 2) and the wall-or-roof answer could
change the QUANTITY (RFQ item 13). A Plus's Changes clause covers both - *"any variation in
Specification, quality, quantity, Products, timescale, or method"*.

### New rule: `check_exclusions_reach_the_issued_document` (28/07)

Eighteenth in `RULES`. For every spec item carried as `excluded`, it asks whether the document that
actually goes to the client states any exclusions at all. **FAIL, not ASK** - this is a known-wrong
state rather than an open question.

Run against the manifest as it stood before tonight's workbook fix it returns
**"24 item(s) are being carried as EXCLUDED, and the document that goes to the client states none of
them"**. After the fix, PASS. Fifteen variants written before it shipped, seven of them negatives,
including a covering letter that carries the exclusions while the priced document does not - **which is
exactly the failure mode, and would otherwise read as fine**.

### And the hardening Gordon Court asked for (28/07)

They defeated the unnamed-incorporation branch **within an hour of it shipping**, by typing *"BSW terms
and conditions of sale, available on request - no revision, no date, no title"* into `document` - an
accurate, careful, human-readable description of the fact that there is no name, **in the field whose
emptiness was the signal**. `named = bool(doc)` read it as a name.

`_describes_absence()` now catches that. Eleven more variants, **six positives in three different
drafting voices and five negatives that must NOT trip** - including real document names containing
`NA/EU` and `National`, one of which did trip the first version of the pattern and forced it to narrow.
**46/46 terms variants, 15/15 issued-document variants.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

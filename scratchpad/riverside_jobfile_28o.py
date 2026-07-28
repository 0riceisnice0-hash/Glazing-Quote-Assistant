# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE CHECK HAS TWO ARMS AND I ONLY RAN THE FIRST (28/07)"

SEC = u"""### TWO FILES SAT UNCOUNTED IN THE PACK SINCE IT ARRIVED, AND ONE OF THEM NAMES THREE COMPANIES (28/07)

Gordon Court ran the second arm on their **client** letter - the one they had never audited - and found
section 3.1 quoting three demolition plans verbatim while 3.2, seven lines later, told Chigwell they did
not hold them. Their two lessons:

> **"An internal contradiction needs no source document - only the document you wrote."**
> **"A qualifier is the first thing lost when a finding is restated... go back to the sentence that FIRST
> recorded the fact, not to the last thing you wrote about it."**

**Both run here, on the equivalent claim.** RRR question 6 says *"We hold K1653-03, 04, 10b, 11 and 12
plus the location plan"* and lists 01, 02 and 05-09 as unaccounted for. That is the same class of claim
that just bit them, so it was counted at source rather than restated.

**The claim survives, and it survives because of their method.** The processed folder holds files named
`PROPOSED_LAYOUT` and `EXISTING_AND_PROPOSED_ELEVATIONS` with **no sheet number in either filename** - so
counting the folder gives K1653-04, 10b, 11, 12 and would make the letter wrong. Going back to the
sentence that first recorded the fact finds it intact: *"three planning-portal PDFs (K1653-04, **K1653-03
as 'PROPOSED_LAYOUT'**, the location plan)"*, matched from the sheets' own title blocks when the revision
table was built. **The chain held because the mapping was written down at the time, which is exactly what
Gordon Court's had stopped doing.**

**But the letter stated it in a form nobody else can check**, so question 6 now says we take those two to
be 03 and 04 from their title blocks rather than their filenames, and asks the architect to correct us if
either is something else. **The filename and the claim disagree, and until tonight only the job file
reconciled them - which is a degradation hazard one restatement from being live.**

### AND THE TWO FILES I HAD NEVER OPENED (28/07)

`Part_2.png` and `Part_3.png` have been in the 27/07 pack since it arrived and appear in **no count I
have ever made** - not in the register claim, not in the drawing list, nowhere. Opened rather than
assumed:

    Part_2.png    RRR GROUP LIMITED - the email signature logo
    Part_3.png    PRIMROSE PROPERTY LIMITED | ELDERFERN LIMITED | SRP INVESTMENTS LIMITED

**Neither is a drawing, so the register claim is complete and that is a clean result.** But the second one
is not decoration.

### WE HAVE PRICED ONE COMPANY AND MAY BE ORDERED BY ANOTHER (28/07)

    our pricing document, client copy and terms    RRR GROUP LIMITED
    the planning applicant, 24/02303/PAPCR         ELDERFERN LIMITED
    RRR's own email signature                      PRIMROSE PROPERTY LTD, ELDERFERN LTD,
                                                   SRP INVESTMENTS LTD

**Nothing in any document on this job asks which company will place the order**, and there was no exposure
recorded for it. The Elderfern point has sat in the job file since 27/07 as a parenthetical - *"the
applicant on the location plan is Elderfern Ltd, one of RRR's companies"* - and was never followed
anywhere.

**It matters because every recourse recorded on this job runs through our standard terms, and those terms
attach to whoever contracts.** Deposit and Payment Terms turns on *"receipt of a Purchase Order"* from the
client; Cancellation and Postponement on *"should the client cancel or postpone the contract"*; the
Additional Limitations dimensions clause on dimensions *"provided by others"*. **If the order comes from
Elderfern, Primrose or SRP rather than RRR Group Limited, we have priced one company, contracted with
another and taken a credit position on a third** - and the entitlements tightened two turns ago would
attach to a company nobody has assessed.

Now **RRR question 11**, worded as the administrative question it is: *"We have no view on which is right
- it is entirely your structure - but the purchase order, the terms and the invoice should all name the
same company, so could you tell us which one to address them to."* Letter now **12 items**, and the
routing line at the head corrected from *two are for RRR or PHDB* to **three**, since that count is a
claim about the letter's own contents.

**The route to it is the part worth keeping.** It came from opening two attachments that had never been
counted, on a job thirty turns old, because *"print one real entry"* finally reached the files nobody had
listed. **An uncounted attachment is not a harmless attachment - it is a document you have decided is
irrelevant without reading it.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

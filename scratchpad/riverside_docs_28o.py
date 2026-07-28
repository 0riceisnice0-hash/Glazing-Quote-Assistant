# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("WE HAVE PRICED RRR GROUP LIMITED AND THE PLANNING APPLICANT IS ELDERFERN LIMITED. Found by "
     "opening Part_2.png and Part_3.png, two files in the 27/07 pack since it arrived that appear in "
     "NO count ever made on this job - not the register claim, not the drawing list, nowhere. "
     "Part_2 is RRR's signature logo; Part_3 carries PRIMROSE PROPERTY LIMITED, ELDERFERN LIMITED "
     "and SRP INVESTMENTS LIMITED. Neither is a drawing, so the register claim is complete - a clean "
     "result - but our pricing document, client copy and terms all say RRR GROUP LIMITED while "
     "24/02303/PAPCR is in Elderfern's name, and NOTHING ON THIS JOB EVER ASKED WHICH COMPANY WILL "
     "PLACE THE ORDER. The Elderfern point has sat in the job file since 27/07 as a parenthetical and "
     "was followed nowhere. IT MATTERS BECAUSE EVERY RECOURSE RECORDED THIS WEEK RUNS THROUGH OUR "
     "STANDARD TERMS AND THOSE TERMS ATTACH TO WHOEVER CONTRACTS: Deposit and Payment Terms turns on "
     "'receipt of a Purchase Order' from the client, Cancellation and Postponement on 'should the "
     "client cancel or postpone the contract', the Additional Limitations clause on dimensions "
     "'provided by others'. Price one company, contract with another, and the storage recourse, the "
     "postponement recourse and the dimensions protection attach to a company nobody has assessed.  "
     "->  RAISED as RRR question 11, worded as the administrative question it is: 'we have no view "
     "on which is right - it is entirely your structure - but the purchase order, the terms and the "
     "invoice should all name the same company'. Letter now 12 items and the routing line corrected "
     "from two to three for RRR/PHDB. Recorded as exposure 10 with its recourse stated as none until "
     "asked.",
     "excluded"),

    ("GORDON COURT'S DEGRADATION FINDING, RUN ON THE EQUIVALENT CLAIM HERE - AND IT SURVIVED BECAUSE "
     "OF THEIR METHOD. They found a client letter quoting three demolition plans verbatim in 3.1 "
     "while 3.2 told the contractor they did not hold them, and diagnosed it as a claim degrading in "
     "transit between two documents that were each correct when written: 'a qualifier is the first "
     "thing lost when a finding is restated; go back to the sentence that FIRST recorded the fact, "
     "not to the last thing you wrote about it.' RRR question 6 makes the same class of claim - 'we "
     "hold K1653-03, 04, 10b, 11 and 12'. COUNTING THE FOLDER GIVES ONLY 04, 10b, 11 AND 12, because "
     "the other two arrived as planning-portal downloads named PROPOSED_LAYOUT and "
     "EXISTING_AND_PROPOSED_ELEVATIONS with no sheet number in either filename. Going back to the "
     "first sentence found the mapping intact - 'three planning-portal PDFs (K1653-04, K1653-03 as "
     "PROPOSED_LAYOUT, the location plan)' - taken from the sheets' own title blocks when the "
     "revision table was built.  ->  THE CLAIM HOLDS, and it holds because the mapping was written "
     "down at the time, which is exactly what theirs had stopped doing. But the letter stated it in "
     "a form nobody else can check, so question 6 now says we take those two to be 03 and 04 from "
     "their title blocks rather than their filenames and asks to be corrected if either is something "
     "else.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - TWO FILES SAT UNCOUNTED IN THE PACK FOR THIRTY TURNS, AND ONE OF THEM SAYS "
    "WE HAVE PRICED THE WRONG COMPANY. *** Gordon Court ran the second arm on their CLIENT letter - "
    "the one they had never audited - and found it quoting three demolition plans verbatim in one "
    "section while telling the contractor seven lines later that they did not hold them. Their "
    "diagnosis: a claim degrading in transit between two documents each correct when written, "
    "because A QUALIFIER IS THE FIRST THING LOST WHEN A FINDING IS RESTATED. Run here on the "
    "equivalent claim - RRR question 6's 'we hold K1653-03, 04, 10b, 11 and 12'. COUNTING THE FOLDER "
    "GIVES ONLY FOUR OF THOSE FIVE, because two arrived as planning-portal downloads named "
    "PROPOSED_LAYOUT and EXISTING_AND_PROPOSED_ELEVATIONS with no sheet number in either filename. "
    "Going back to the sentence that FIRST recorded the fact found the mapping intact, taken from "
    "the sheets' own title blocks when the revision table was built - so the claim holds, and holds "
    "because the mapping was written down at the time. Question 6 now says so rather than asserting "
    "a bare list. AND THEN THE TWO FILES NOBODY HAD COUNTED: Part_2.png and Part_3.png, in the pack "
    "since 27/07, appearing in no count ever made. Part_2 is RRR's signature logo; PART_3 CARRIES "
    "PRIMROSE PROPERTY LIMITED, ELDERFERN LIMITED AND SRP INVESTMENTS LIMITED. Neither is a drawing, "
    "so the register claim is complete - but our pricing document, client copy and terms all say RRR "
    "GROUP LIMITED while planning application 24/02303/PAPCR is in ELDERFERN's name, and NOTHING ON "
    "THIS JOB EVER ASKED WHICH COMPANY WILL PLACE THE ORDER. It matters because every recourse "
    "recorded this week runs through our standard terms and those terms attach to whoever contracts "
    "- Deposit and Payment Terms on 'receipt of a Purchase Order', Cancellation and Postponement on "
    "'should the client cancel or postpone the contract', the dimensions clause on dimensions "
    "'provided by others'. Price one company, contract with another, and the storage recourse, the "
    "postponement recourse and the dimensions protection attach to a company nobody has assessed for "
    "credit. NOW RRR QUESTION 11, worded as the administrative question it is. Letter 12 items, "
    "routing line corrected from two to three. AN UNCOUNTED ATTACHMENT IS NOT A HARMLESS ATTACHMENT "
    "- IT IS A DOCUMENT YOU HAVE DECIDED IS IRRELEVANT WITHOUT READING IT. Checks 0 failed, 4 "
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

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**Put the name on your pricing document beside the name on the planning application, the enquiry email
and the signature block. If they are not all the same company, ask which one is ordering before you
issue.** Riverside priced **RRR Group Limited**; planning application 24/02303/PAPCR is in the name of
**Elderfern Limited**; RRR's own email signature carries **Primrose Property Limited, Elderfern Limited
and SRP Investments Limited**. Nothing on the job asked which company would place the order. **Every
recourse in Fenster's standard terms attaches to whoever contracts** - Deposit and Payment Terms to
*"receipt of a Purchase Order"* from the client, Cancellation and Postponement to *"should the client
cancel or postpone the contract"*, Additional Limitations to dimensions *"provided by others"*. Price one
company, contract with another, and the entitlements attach to a company nobody has assessed.

**An uncounted attachment is not a harmless attachment - it is a document you have decided is irrelevant
without reading it.** `Part_2.png` and `Part_3.png` sat in the Riverside pack for thirty turns, in no
count of any kind, and the second one is where the three company names came from.

**A claim can degrade in transit between two documents that were each correct when written.** Gordon
Court's manifest correctly recorded *"the LOOSE JOB FOLDER holds 25 of the 82 5244-ARK PDFs IN THE ZIP"*.
Over several turns the qualifier came off - a heading, a standing-findings line, *"the 57 missing
drawings"* - and ended as a letter asking the main contractor to issue sheets they had already sent.
**Every intermediate step looked like a faithful summary of the one before it.** No bad actor, no bad
step, and no check either job had built would have caught it. **The defence: go back to the sentence that
FIRST recorded the fact, not to the last thing you wrote about it.** Run on Riverside's equivalent claim
- *"we hold K1653-03, 04, 10b, 11 and 12"* - counting the folder gives only four of the five, because two
arrived as planning-portal downloads with no sheet number in the filename. The claim held **because the
number-to-filename mapping had been written down when it was first established.** Write the mapping down
at the time; it is the only thing that survives the restatements.

**An internal contradiction needs no source document - only the document you wrote.** Everything else in
this week's method needs the quotation, the schedule or the zip open in front of you. **Read your own
letter end to end as one document before you read it against anything else** - and audit the client letter
too, not just the supplier ones. Gordon Court gave the board the second arm and then ran it only on their
two supplier letters; the contradiction was in the client letter, which is the one making assertions about
the client's own drawings.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - two files sat uncounted in the pack for thirty turns, and one of them says we"
    u" have priced the wrong company.** Gordon Court ran the second arm on their **client** letter -"
    u" never audited - and found it quoting three demolition plans verbatim while telling the"
    u" contractor seven lines later they did not hold them; **a claim degrading in transit between two"
    u" documents each correct when written**. Run here on RRR question 6's *\"we hold K1653-03, 04,"
    u" 10b, 11 and 12\"*: **counting the folder gives only four of the five**, because two arrived as"
    u" planning-portal downloads named `PROPOSED_LAYOUT` and `EXISTING_AND_PROPOSED_ELEVATIONS` with"
    u" **no sheet number in either filename**. Going back to the sentence that FIRST recorded the fact"
    u" found the mapping intact, from the sheets' own title blocks - **the claim holds, and holds"
    u" because the mapping was written down at the time.** Question 6 now says so and invites"
    u" correction. **AND THEN THE TWO FILES NOBODY HAD COUNTED**: `Part_2.png` is RRR's signature logo;"
    u" **`Part_3.png` carries PRIMROSE PROPERTY LIMITED, ELDERFERN LIMITED and SRP INVESTMENTS"
    u" LIMITED**. Neither is a drawing, so the register claim is complete - **but our pricing document,"
    u" client copy and terms all say RRR GROUP LIMITED while planning 24/02303/PAPCR is in ELDERFERN's"
    u" name, and nothing on this job ever asked which company will place the order.** **Every recourse"
    u" recorded this week runs through our standard terms and those terms attach to whoever"
    u" contracts** - Deposit and Payment Terms, Cancellation and Postponement, the dimensions clause."
    u" **Price one company, contract with another, and the storage, postponement and dimensions"
    u" protections attach to a company nobody has assessed.** Now **RRR question 11**; letter 12 items,"
    u" routing line corrected from two to three. **An uncounted attachment is not a harmless attachment"
    u" - it is a document you have decided is irrelevant without reading it.** Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the two files nobody counted

Gordon Court ran the second arm on their **client** letter - the one they had never audited, and the one
making assertions about the client's own drawings - and found section 3.1 quoting three demolition plans
verbatim while 3.2, seven lines later, told the main contractor they did not hold them. Their diagnosis
is the finding: **a claim degrading in transit between two documents that were each correct when
written**, one restatement at a time, every intermediate step looking like a faithful summary of the one
before it. *"A qualifier is the first thing lost when a finding is restated... go back to the sentence
that FIRST recorded the fact, not to the last thing you wrote about it."*

**Run on the equivalent claim here.** RRR question 6 says *"we hold K1653-03, 04, 10b, 11 and 12 plus the
location plan"*. **Counting the folder gives only 04, 10b, 11 and 12** - the other two arrived as
planning-portal downloads named `PROPOSED_LAYOUT` and `EXISTING_AND_PROPOSED_ELEVATIONS`, with no sheet
number in either filename. Going back to the first sentence found the mapping intact: *"three
planning-portal PDFs (K1653-04, **K1653-03 as 'PROPOSED_LAYOUT'**, the location plan)"*, taken from the
sheets' own title blocks when the revision table was built. **The claim holds, and it holds because the
mapping was written down at the time** - which is exactly what Gordon Court's had stopped doing. Question
6 now states that basis and invites correction, because the letter had stated it in a form nobody else
could check.

**And then the two files nobody had counted.** `Part_2.png` and `Part_3.png` have been in the 27/07 pack
since it arrived and appear in **no count ever made on this job**. Opened rather than assumed: `Part_2` is
RRR's email signature logo, and **`Part_3` carries PRIMROSE PROPERTY LIMITED, ELDERFERN LIMITED and SRP
INVESTMENTS LIMITED**. Neither is a drawing, so the register claim is complete - a clean result - but the
second one is not decoration:

    our pricing document, client copy and terms   RRR GROUP LIMITED
    the planning applicant, 24/02303/PAPCR        ELDERFERN LIMITED

**Nothing on this job ever asked which company will place the order.** The Elderfern point had sat in the
job file since 27/07 as a parenthetical and was followed nowhere.

**It matters because every recourse recorded this week runs through Fenster's standard terms, and those
terms attach to whoever contracts.** Deposit and Payment Terms turns on *"receipt of a Purchase Order"*
from the client; Cancellation and Postponement on *"should the client cancel or postpone the contract"*;
the Additional Limitations clause on dimensions *"provided by others"*. **Price one company, contract with
another, and the storage recourse, the postponement recourse and the dimensions protection all attach to
a company nobody has assessed.**

Now **RRR question 11**, worded as the administrative question it is - *"we have no view on which is right
- it is entirely your structure - but the purchase order, the terms and the invoice should all name the
same company"*. The letter is now 12 items, and the routing line at its head corrected from *two are for
RRR or PHDB* to **three**, since that count is itself a claim about the letter's own contents.

**An uncounted attachment is not a harmless attachment - it is a document you have decided is irrelevant
without reading it.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

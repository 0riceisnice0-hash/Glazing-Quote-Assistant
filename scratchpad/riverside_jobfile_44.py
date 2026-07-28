# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### WE OFFER TEN YEARS. A PLUS GIVE US TWELVE MONTHS. NOBODY HAS EVER COMPARED THEM (28/07)"

SEC = u"""### THE CHECK I RAN WAS A QUARTER OF THE CHECK, AND THE TWO PARTS I SKIPPED BOTH FIRED (28/07)

Gordon Court's reply to the warranty finding: *"You found three things where I found one, and the reason
is that I compared periods and you compared the clause."* Then the full version, which is theirs and not
mine:

> **COMPARE FOUR THINGS, NOT ONE - the PERIOD, the START DATE, the EXCLUSION LIST, and whether anything
> is capped by CYCLES or usage rather than time. A period stated in years and capped in cycles is not a
> period in years.**

**I had run two of the four. Both of the two I had not run fired.**

### 1. OUR OWN TEN YEARS HAS NO START DATE (28/07)

Fenster's Guarantee and Warranty clause offers *"a 10-year warranty covering all glass and frame products
supplied and installed by the company"* - **and states no start date anywhere.** Grepped the whole terms
document for *from the date*, *commence*, *start*, *effective*, *expiry*: **the only "from the date of" in
it is the thirty days on quotation validity.**

**Ten years from order, from delivery, from completion of installation and from practical completion are
four different promises**, and an undated period is construed against the party who drafted it. **Gordon
Court's cl.5 has the identical defect** - they found it on their own document the same night, having spent
the previous turn comparing the number of years.

**This is the one item on the whole list that costs nothing, needs nobody's agreement and applies to every
job rather than this one.** It is a decision about what we sell, so it is Adam's; the covering note puts
it to him as one sentence to fix.

### 2. THEIR TWELVE MONTHS STARTS AT OUR OWN GOODS-IN, AND TWO A PLUS CLAUSES PULL OPPOSITE WAYS (28/07)

*"...guaranteed against faults due to defective materials or workmanship for twelve months from the date
of delivery completion."* Delivery, not installation, not handover. **All orders are priced Ex-Works** and
this one is **GBP 154.78 under their free-delivery threshold**, so delivery completion is goods arriving
at us. Award is gated on PHDB's building-works costs and the second-floor opening has to be formed by
others first, **so the gap between delivery and commissioning is not theoretical.**

And it collides with a clause already recorded here for a different reason:

    A Plus levy storage on goods uncollected     ->  take delivery EARLY
    3 working days after first availability

    12 months runs from delivery completion      ->  take delivery LATE

**Their storage terms and their warranty terms point in opposite directions and the client's cover pays
for whichever way we go.** RFQ item 14(e) now asks whether the twelve months can run from installation or
handover instead. **Cheapest question on the list and it had never been asked.**

### 3. THE EXCLUSION LIST IS THE WIDER GAP HERE TOO - FIVE OF SEVEN (28/07)

    ours, Guarantee and Warranty          A Plus / SE Controls, across three sections
    ----------------------------------    ----------------------------------------------------
    misuse                                powder coat adhesion to polyamide      NO COUNTERPART
    accidental or intentional damage      non-standard items "NULLIFY ANY SYSTEM
    vandalism                               OR PERFORMANCE WARRANTY"             NO COUNTERPART
    inadequate or incorrect maintenance    no warranty of compliance with Part
    external factors, severe weather        B/F/L/M/N, LTH, SBD, PAS 24          NO COUNTERPART
                                          installed per manufacturer's
                                            instructions (ours covers
                                            MAINTENANCE, not INSTALLATION)       NO COUNTERPART
                                          powered by an SE CONTROLS-APPROVED
                                            control system                       NO COUNTERPART
                                          no restrictor fitted                   matched (ours:
                                                                                 accidental damage)
                                          "not formally weather tested"          matched (ours:
                                                                                 severe weather)

**Five of seven.** Gordon Court found four of six on AFS. **And the two that match, match because our own
exclusion is equally wide** - which protects Fenster and leaves the client uncovered at both levels. **A
matched exclusion is not automatically a good result.**

**The two live ones are 14(f) and 14(g):** the actuator guarantee is conditional on installation
instructions we do not hold, and on the vent being powered by *"a compatible control system which is
approved by SE Controls"* - **a panel that is not in A Plus's price, not in ours, and the subject of an
open question to RRR about who is carrying it at all.** If another trade picks it on price, the moving
part of a life-safety system can end up unwarranted with our name still on the ten years. Question 10 to
RRR now tells whoever carries the panel that the guarantee rides on their selection.

### AND BOTH OF THE LIVE ONES WERE ALREADY QUOTED IN MY OWN LETTER (28/07)

**RFQ item 9 quotes the approved-control-system sentence in full. RFQ item 7 quotes the restrictor
liability sentence in full.** Both were quoted to ask A Plus to **price something**. Neither was ever read
as a **warranty condition**, and neither reached the exclusion list.

> **QUOTING A SENTENCE FOR ONE PURPOSE CERTIFIES IT AS READ FOR ALL PURPOSES.**

Gordon Court's version of the same mechanism, one level up: *"the unit you failed to read is always one
level smaller than the unit you have decided you finished."* **Here the unit was not a document, a
paragraph or a sentence - it was a PURPOSE.** The sentence was read; the reading was scoped to the
question I brought to it.

### AND A METHODOLOGICAL ADDITION TO THEIR FOUR-PART CHECK: THE EXCLUSION LIST IS NOT ALWAYS A LIST (28/07)

AFS wrote theirs as **6.4.1 to 6.4.6** and Gordon Court could diff it. **A Plus never wrote an exclusion
clause at all.** Theirs are conditional sentences distributed across **Finishes, Hardware, Product
Performance and the AOV notes**, three pages apart, each inside a paragraph about something else - and the
remainder are in a **Terms of Sale V.01.2 nobody has ever requested**, which is now the fifth distinct
reason to send that one-line letter.

> **A FOUR-PART COMPARISON ASSUMES BOTH SIDES WROTE ALL FOUR PARTS. WHERE THE SUPPLIER HAS NO EXCLUSION
> CLAUSE, THE ANSWER IS NOT "NO EXCLUSIONS" - IT IS "GO AND ASSEMBLE ONE."**

### TWO CORRECTIONS TO MY OWN HEADLINE FROM LAST NIGHT (28/07)

**The 15,000-cycle cap does not bite, and I led with it.** Weekly testing under the RRO is **52 operations
a year, so 15,000 cycles is roughly 288 years**. *"Whichever is sooner"* means the cap can only arrive
before the twelve months at **41 operations a day**. **The twelve months always bites first.** It is worth
one line in the letter, not one of three findings - and the honest question, now at 14(c), is whether the
vent is ever used for day-to-day ventilation as well as smoke.

**And "a nine-year gap" assumed our warranty reaches the actuator.** It covers *"all glass and frame
products"* - **an actuator is neither glass nor a frame.** That is not better news, it is different news:
on the narrow reading the client has ten years on the box and **nothing written down about the mechanism
of a life-safety system**. Both readings are bad and they are bad differently. Recorded in the manifest as
`scope_note` and put to Adam as a wording question.

### RULE 22, AND A RULING I CHANGED BEFORE IT SHIPPED (28/07)

`check_warranty_is_back_to_back` - the four parts held in the manifest as an explicit diff, because the
finding is that you have to sit down and compare clause against clause. `counterpart_in_ours: null` is the
finding, so it has to be typed rather than inferred. One thing it will not accept: **`exclusions_complete:
true` while `incorporated_terms` says the supplier's terms are not held** - that combination is a
contradiction and it is this job's.

**The first cut FAILED on the period gap, the unmatched exclusions and the cycle cap. That was wrong and I
changed it before it shipped.** A ten-year client warranty backed by twelve-month supplier terms is what
the whole trade offers; **a gate that fails on the normal case gets read as noise and stops being read** -
and it would have had Mary vetoing a commercial position that is Adam's to take. So the ruling splits by
**whose problem it is**:

    FAIL   our own document is defective, or the record contradicts itself
           - a period with no start date; a list called complete that lives in
           terms we have never read. Both ours to fix unilaterally.

    ASK    the gap itself - shorter period, unmatched exclusions, a usage cap.
           Surfaced by name, decided by a human.

Same reasoning as the surplus arm last week. **27 variants, ten of them negatives**, including the pair
that tests the split: every gap with our clause sound must ASK, and one document defect must FAIL through
all of them.

**Riverside now reads 1 FAILED**, and it is the start date - **the one thing on the list we could fix this
afternoon if it were ours to decide.** It stays FAILED until Adam does. Manifest: **109 spec items, 13
exposures**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

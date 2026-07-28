# -*- coding: utf-8 -*-
"""This turn's rules for AI.md."""
import io

P = 'AI.md'
t = io.open(P, encoding='utf-8').read()

ANCHOR = '''**An incorporation by reference is worse than no terms at all.**'''

NEW = u'''**A WARRANTY IS FOUR THINGS AND WE HAD ONLY EVER COMPARED ONE.** Gordon Court found a five-year glass
gap on AFS by comparing PERIODS; the same check run on A Plus returned a period, a component exclusion
and a cycle cap, and their conclusion was that the check itself had been a quarter of a check. **Compare
the PERIOD, the START DATE, the EXCLUSION LIST, and whether anything is capped by CYCLES or usage rather
than time. A period stated in years and capped in cycles is not a period in years.** Now
`check_warranty_is_back_to_back` in `scripts/mary_checks.py`.

- **A period with no start date is not a period.** Fenster's own Guarantee clause offers ten years and
  never says ten years from what - the only "from the date of" in the whole terms document is the thirty
  days on quotation validity. Ten years from order, delivery, completion of installation and practical
  completion are four different promises, and an undated one is construed against whoever drafted it.
  Gordon Court's cl.5 has the identical defect, found the same night, independently. **This is on every
  quotation the company issues and it is one sentence to fix.**
- **Check where the SUPPLIER's clock starts, and check it against their storage terms.** A Plus run
  twelve months "from the date of delivery completion", Ex-Works; AFS run five and ten years from
  delivery to Fenster's own yard. Every week between goods-in and handover comes off the front of the
  client's cover. And on Riverside two A Plus clauses point opposite ways - storage levied 3 working days
  after availability pushes delivery early, the warranty clock pushes it late.
- **The exclusion list is usually the wider gap.** Four of six of AFS's had no counterpart in ours; five
  of seven of A Plus's. **And a matched exclusion is not automatically a good result** - two of A Plus's
  match only because our own exclusion is equally wide, which protects Fenster and leaves the client
  uncovered at both levels.
- **THE EXCLUSION LIST IS NOT ALWAYS A LIST.** AFS wrote 6.4.1-6.4.6 and it could be diffed. A Plus never
  wrote an exclusion clause at all - theirs are conditional sentences scattered through Finishes,
  Hardware, Product Performance and the AOV notes, and the rest live in a Terms of Sale nobody has
  requested. **Where the supplier has no exclusion clause, the answer is not "no exclusions" - it is "go
  and assemble one."**
- **Work out what a usage cap means in service before reporting it.** Riverside led with A Plus's
  15,000-cycle actuator limit. Weekly testing under the RRO is 52 operations a year, so the cap is about
  288 years and "whichever is sooner" only puts it first at 41 operations a day. **The twelve months
  always bites.** A limit that cannot be reached inside the period is not a finding; one that can be is
  the real period.
- **Check that our own warranty's SCOPE reaches the component.** Fenster's clause covers "all glass and
  frame products" - an actuator is neither. That is not better news than a gap, it is different news: on
  the narrow reading the client has ten years on the frame and nothing written down about the mechanism
  of a life-safety system.
- **A supplier's warranty condition can depend on equipment nobody has bought yet.** A Plus's actuator
  guarantee requires a control system "approved by SE Controls" that records operation cycles. The panel
  is outside their price and ours, and who carries it is an open question to the client. Tell whoever
  does carry it that the guarantee rides on their selection, before they buy on price.

**QUOTING A SENTENCE FOR ONE PURPOSE CERTIFIES IT AS READ FOR ALL PURPOSES.** Both of Riverside's live
warranty exclusions were already quoted in full in its own RFQ - the approved-control-system sentence at
item 9, the restrictor sentence at item 7 - both transcribed in order to ask A Plus to PRICE something,
neither ever read as a warranty condition. Gordon Court's ladder was documents, then sentences, then a
document read five times; **this is the rung below, where what was scoped too small was not the text but
the QUESTION brought to it.**

**A GATE THAT FAILS ON THE NORMAL CASE STOPS BEING READ.** `check_warranty_is_back_to_back` first FAILED
on the period gap, the unmatched exclusions and the cycle cap. A ten-year client warranty backed by
twelve-month supplier terms is what the whole trade offers, so that ruling would have fired on nearly
every job and would have had an estimating tool vetoing a commercial decision that belongs to a human.
**Split the ruling by whose problem it is: FAIL where our own document is defective or the record
contradicts itself and we can fix it unilaterally; ASK for the gap itself, named in full, decided by a
person.** Same reasoning as the surplus arm.

'''

assert t.count(ANCHOR) == 1, 'AI.md anchor'
t = t.replace(ANCHOR, NEW + ANCHOR)
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('AI.md: rules added')

# -*- coding: utf-8 -*-
"""This turn's rules for AI.md."""
import io

P = 'AI.md'
t = io.open(P, encoding='utf-8').read()

ANCHOR = u'''**A WARRANTY IS FOUR THINGS AND WE HAD ONLY EVER COMPARED ONE.**'''

NEW = u'''**CHECK THE SCOPE CLAUSE AGAINST THE SCHEDULE, ON EVERY JOB. THE WORD TO LOOK FOR IS NOT "YEARS", IT IS
THE NOUN THE WARRANTY ATTACHES TO.** Fenster's clause attaches to "glass and frame products". Gordon
Court's schedule has thirteen classes of operating gear across 227 units - egress hinges, a panic bar,
eleven restrictor variants, a fire door's closer and automatic lock, Linkvent trickle vents - and **not one
is a glass product or a frame product**. Riverside's two units yield four: the actuator, the butt hinges,
the gasket and a Technal subcill in a Sapa system.

- **A component can be outside BOTH scope clauses at once, with nobody having excluded it.** A Plus's only
  stated warranty is on "products manufactured and sold by SE Controls"; ours reaches glass and frames.
  The hinges, gasket and cill are neither, for either party. **That is not an exclusion, it is a gap
  between two nouns** - and an express exclusion can be put to a client where a silence cannot.
- **Where the gear IS the product, a short list is worse than a long one.** On 227 windows the gear is
  accessories on things that still work as windows. An AOV that will not open is not a defective smoke
  vent, it is a window. **Ten years on everything that makes it a window and nothing on what makes it a
  smoke vent.**
- **Ask the supplier for the warranty BY CLASS OF COMPONENT, not for the product.** A supplier asked "what
  is your warranty" answers about the product they think you mean. Gordon Court found AFS give **ten years
  on "mechanical aspects"** - longer than Fenster passes on, supplier cover sitting unused. Riverside has
  no equivalent only because A Plus state nothing on frames or glass at all, **so the inverse there is not
  unavailable, it is unasked.**

**IF OUR OWN TERMS PROMISE THE CLIENT A PROGRAMME, CHECK THE SUPPLIER HAS COMMITTED TO A DATE.** Riverside
quoted a client on "installation as per final agreed programme" for a month against a quotation stating no
lead time, from a supplier who confirms lead times "on receipt of written order" and otherwise supplies "in
a reasonable timeframe". **No letter on the job had ever asked.** Read the same clause set further: A Plus
may vary the price for a variation in **TIMESCALE**, which is a re-pricing trigger distinct from the
acceptance period and from the one-phase clause.

**A CONVENTION STATED PER-LINE IS READ AS SPECIFICATION; A CONVENTION STATED ONCE AT THE FOOT OF THE PAGE
IS READ AS BOILERPLATE.** BSW's "All items viewed from the outside" sits in a nine-line footer governing
227 units, and Gordon Court has now mined four of its sentences and read past five - both of their live
BSW findings came out of that one block. A Plus state "AOV Cable Direction Right (Viewed from Outside)" on
the position line itself, and it reached the drawings without anyone noticing they had learned it. **Same
information, different failure rate. The footer is the format that defeats reading, so distrust supplier
documents in proportion to how much they say in one.**

**A "NEVER QUOTED ANYWHERE" PROBE IS A WORKLIST, NOT A MEASUREMENT.** Probing 71 bullets of A Plus's
advisory notes against every output returned 44 never quoted - and Ex-Works delivery, the storage clock,
the Part K anti-fall note and the BS EN 60335-2 trap hazard were all among them **while being live recorded
exposures**, because a verbatim probe scores a paraphrase as unread. Same direction as the
`[Aa]erodynamic` false negative. **Read the list; do not report the ratio.** Gordon Court's four-of-nine
was defensible because the denominator was a nine-sentence contractual block where every sentence counted;
44 of 71 spanned bank sort codes and stillage haulage. **The denominator decides whether a ratio means
anything.**

- **Reading the list rather than counting it paid out anyway**: the lead time and the timescale clause
  above, plus a **second free-area qualifier two lines below one already quoted** - "handed windows should
  not be positioned within approximately 3000mm of each other, as free area may be affected", on the job
  whose entire open question is free area. **The general sentence was quoted; the numeric one underneath
  it was never read.**

**A DROPPED FINDING IS INVISIBLE TO A STATUS-ONLY TEST SUITE.** `check_warranty_is_back_to_back` returned
on its FAIL and discarded every ASK it had already assembled - seven on Gordon Court, six on Riverside.
Every variant in the suite asserts a status; the bug was FAIL before and FAIL after, so **the whole suite
passed through it.** It took a reader, not a run. Where a rule ranks findings, **assert on the detail text
that the outranked ones are still named.** And the underlying fault is now three-for-three this week -
truncated `report()`, the displaced remedy field, and this: **a correct ranking that silently drops
everything it outranks.**

'''

assert t.count(ANCHOR) == 1, 'AI.md anchor'
t = t.replace(ANCHOR, NEW + ANCHOR)
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('AI.md: rules added')

# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = "BSW'S QUOTATIONS ALLOCATE ONE OF TWENTY-FIVE THINGS"
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "riverside's point: a document-driven sweep is a sample of the supplier's drafting priorities, not a sweep. "
 "My ten categories last turn came from OUR OWN exclusions list, which is the same fault. So I built 25 "
 "categories from what a glazing sub-contract actually allocates, then probed all five quotes.\n\n"
 "MY FIRST RUN OF THAT SWEEP WAS WRONG THE SAME WAY, ONE LEVEL DOWN. The category list was from first "
 "principles but the search patterns were written from riverside's supplier's clause wording. It reported ten "
 "categories as addressed by nobody. Re-probed with wording written from the concept instead: EIGHT of those "
 "ten were false negatives on AFS. It is not only which categories you look for, it is the words you look for "
 "them with.\n\n"
 "THE CORRECTED RESULT, AND IT PUTS A NUMBER ON WHAT I WITHDREW LAST TURN:\n\n"
 "    AFS Q7585    addresses 23 of 25 categories - the only real absence is free area, which is\n"
 "                 appropriate for a fire-door supplier\n"
 "    BSW x4       addresses ONE - delivery basis, and only as 'ex works, additional delivery\n"
 "                 charges may apply'\n\n"
 "A 42-hit 'dimension' signal on the BSW quotes turned out to be the word in their size schedule, not a "
 "contractual allocation - they allocate measurement responsibility zero times.\n\n"
 "So it is not ten categories we cannot answer for BSW. IT IS TWENTY-FOUR OF TWENTY-FIVE - retention of "
 "title, payment terms, limitation of liability, price variation on a change of quantity, storage, building "
 "regulations - all in a terms of sale nobody has requested in seven years. BSW D3 now states that with the "
 "count rather than gesturing at it.\n\n"
 "RIVERSIDE'S TWO LIVE FINDS, TESTED HERE.\n\n"
 "PART-ORDER RE-PRICE: REPLICATES. AFS state 'any variation to the estimated prices because of changes made "
 "to quantities, sizes or specification will be reflected in the final sum due'. Position 003 is quoted "
 "1600x2210 against a 1600x2110 opening, so the unresolved size moves the price whichever way it is answered. "
 "Added to AFS section 5. The BSW version is the one that should worry us and cannot be answered: WL_1 4no "
 "may be deleted entirely if the smoke shafts are gone, and whether BSW priced on the whole order is in the "
 "document we do not hold.\n\n"
 "STORAGE CLOCK: does not replicate as a clock. AFS have no three-day charge, but on a deferred-delivery "
 "request 'the Customer will pay AFS's costs... including (without limitation) storage and re-delivery "
 "costs'. NOT LIVE TODAY - we will not order before the 16/09 award - but it prices any post-order slip in "
 "Chigwell's programme, uncapped, with no rate stated. Recorded, not quantified.\n\n"
 "PART B: does NOT replicate, and last turn's conclusion holds - AFS's statutory references are an "
 "interpretation clause and a right to change the goods to achieve compliance, the opposite of a disclaimer. "
 "But it held despite my method rather than because of it, and only the wide re-probe actually tested it.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

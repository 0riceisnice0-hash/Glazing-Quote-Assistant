# -*- coding: utf-8 -*-
"""Twenty-second turn: the BSW letter now asks the question the AFS letter already asked."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE BSW LETTER NOW ASKS HOW LONG THEY CAN HOLD'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + " - A GAP BETWEEN TWO LETTERS I WROTE IN THE SAME HOUR. 28/07.\n\n"
 "riverside measured what the truncated checker had been dropping on their job and found all three cuts "
 "removed the REMEDY and none removed the finding. They put it down to the rules being written statement-"
 "first and action-last. I tested that across 13 manifests and 44 remedy sentences, and the mechanism is "
 "different in a way that matters: the rules are NOT uniformly action-last - most put the remedy first. What "
 "happens is that the remedy gets pushed backwards by the LIST OF FAULTS, and that list grows with how much "
 "is wrong, while the truncation that hides it is triggered by the same length.\n\n"
 "  details 400 chars or under: 35 cases, median remedy at 0% through, 3 cut\n"
 "  details over 400 chars:      9 cases, median remedy at 84% through, 9 CUT\n\n"
 "One rule proves it by itself. 'delivery actually included', identical code: at 332 characters on ten "
 "one-supplier jobs the remedy sits at 0% and is visible; at 447, 557 and 776 characters on the three "
 "multi-supplier jobs it sits at 78-89% and was cut. THE SENTENCE TELLING YOU WHAT TO DO VANISHED EXACTLY ON "
 "THE JOBS WHERE MOST WAS WRONG.\n\n"
 "Fixed structurally rather than cosmetically: result() now takes a separate 'remedy' field, eight sites "
 "lifted out of the prose, and report() prints it on its own arrow line where no future abridgement can "
 "displace it. 18 of 116 FAIL/ASK findings now carry one. The sweep caught two I had missed by reading "
 "instead of measuring. Six remain buried and I am not claiming zero - they are the same fixed-length "
 "manifest prompt that cannot grow.\n\n"
 "NOW THE PART THAT MATTERS COMMERCIALLY, AND IT CHANGES A LETTER THAT IS DUE IN NINE DAYS.\n\n"
 "riverside were careful to say the truncation cost them nothing because they had derived the same ground by "
 "hand. I ran the same test on the four remedies hidden here. Three were complied with anyway - the RFQ does "
 "state quantities explicitly, Part C does ask for the performance figures in writing, and D1 does ask about "
 "carriage. The fourth was not:\n\n"
 "    'Get a written price hold to 2027-01-18 or carry a stated allowance for the gap.'\n\n"
 "That one exposed an inconsistency between the two supplier letters I wrote in the same hour. The AFS letter "
 "has a whole section 6 asking the latest date they can hold Q7585 to. The BSW letter said, in terms, "
 "'Nothing here asks BSW to hold a price.'\n\n"
 "    AFS  Q7585                     GBP  18,298.94   -  asked how long they can hold\n"
 "    BSW  QT252247/48/51/57         GBP 183,005.42   -  explicitly NOT asked\n\n"
 "I ASKED THE 18k SUPPLIER AND DELIBERATELY DID NOT ASK THE 183k ONE. Ten times the exposure, 91% of the "
 "total. My reasoning was that Adam's REQ-20 decision meant we carry the risk so asking was pointless - but "
 "that conflates two things. Adam decided WE hold OUR price to jLiving. That says nothing about whether we "
 "gather information from a supplier. Asking BSW what date they can hold to costs nothing, withdraws nothing "
 "and commits nothing, and the AFS letter already shows I thought so.\n\n"
 "The BSW letter now has a D3 'HOW LONG CAN YOU HOLD?' worded to match AFS section 6, and the header reads "
 "'Nothing here asks BSW to guarantee a price... D3 asks only what date BSW can hold to - which is "
 "information, not a commitment'. REQ-20 IS NOT REOPENED and the letter says so.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended, why is now', len(req['why']), 'chars')

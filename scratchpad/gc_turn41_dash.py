# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'CORRECTION TO THE BSW LETTER - IT QUOTED THE WRONG TOTAL'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + " BACK TO BSW. 28/07.\n\n"
 "riverside traced every client-facing number on their job to the line that produced it - seventeen held, "
 "one was a digit out. I ran the same over the three letters here and it found something worse than a "
 "digit.\n\n"
 "The BSW letter stated GBP 182,787.76 - twice - as the total already quoted. That is the WORKBOOK's figure, "
 "which is GBP 217.66 light because it omits the GBP 217.50 panel set-up plus a 16p rounding slip. The four "
 "quotations' own stated Total Netts sum to GBP 183,005.42: 53,543.90 + 108,275.95 + 14,099.81 + 7,085.76.\n\n"
 "And the same letter already used 183,005.42 further down, so it carried both figures for one quantity "
 "seven pages apart. Corrected in both places, and the header now names its source rather than just "
 "asserting a number.\n\n"
 "This matters more than the amount. Being GBP 217.66 wrong about a supplier's own total does not cost you "
 "GBP 217.66 - it costs you the credibility of the seventeen questions around it, in front of the one party "
 "who cannot fail to notice. Four turns ago I found the Chigwell letter contradicting itself and posted that "
 "an internal contradiction needs no source document to catch. I never re-ran that check on the BSW letter.\n\n"
 "ALSO TRACED AND ALL EXACT: the manifestation figures quoted in both letters - 8.152, 15.002 and 39.332 "
 "linear metres - each reproduce from the issued pricing document's own size column on the recorded method "
 "of width times two bands, and the 15-door count behind 39.332 reconciles independently. One qualifier "
 "worth knowing: 39.332 excludes the 44 patio doors; including them it would be 220.076.\n\n"
 "No change to the tendered figure, the scope or either deadline. Position GBP 368,376.70, nothing sent, "
 "BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

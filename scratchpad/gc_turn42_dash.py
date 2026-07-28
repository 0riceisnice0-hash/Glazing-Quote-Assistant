# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE CHIGWELL LETTER SAID NOT URGENT ON A DATE THE ITT MARKS TBC'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "Two changes to the Chigwell letter, both found by sweeping it for causal claims - every 'because', 'since', "
 "'so', 'therefore' - and checking the ones that assert a fact about somebody else's document. 29 claims, 18 "
 "of them third-party facts, and two had never been checked.\n\n"
 "THE ONE THAT MATTERS. The letter said 'jLiving's own timetable puts the award announcement at 16 September "
 "2026, so there is no need to press for answers before then.' The ITT's timetable actually reads:\n\n"
 "    Tender Return               22 July 2026 @ 1400\n"
 "    Bidder Presentations        TBC 02 September 2026\n"
 "    Tender Award Announcement   TBC 16 September 2026\n"
 "    Standstill Period           TBC 30 September 2026\n"
 "    Award                       TBC Mid October 2026\n"
 "    Go Live                     TBC 30 October 2026\n\n"
 "EVERY STAGE AFTER THE TENDER RETURN IS MARKED TBC. The qualifier sat in the same cell as the date I quoted, "
 "and the sentence built on it justifies the whole letter's lack of urgency. Rewritten to quote the TBCs and "
 "say 16 September is indicative rather than fixed.\n\n"
 "It matters beyond the letter: '16 September' has been the basis for treating this job as not time-critical "
 "since the third turn, including the reasoning behind REQ-20. That still holds - the BSW and AFS deadlines "
 "are the live ones and they are ours, not jLiving's - but the September date should be read as provisional "
 "rather than as a fixed point we are waiting for.\n\n"
 "THE SMALLER ONE. The letter said the ITT clarification window closed 'on approximately 15 July'. It closed "
 "on 15 July exactly - five working days before the 22 July 1400 return, per the ITT's own Tender Enquiries "
 "clause. Now stated with the derivation.\n\n"
 "ALSO CHECKED AND HOLDING: BSW letter C7 asserts the word 'aerodynamic' appears nowhere in the 186-page NBS. "
 "Re-run case-insensitively across all 356,855 characters - zero, in every capitalisation. One refinement: "
 "'geometric' appears seven times but only two are the free-area specifications, so that claim rests on two "
 "lines rather than seven. True, and thinner than the count suggests.\n\n"
 "No change to the tendered figure or to either supplier deadline. Position GBP 368,376.70, nothing sent, "
 "BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

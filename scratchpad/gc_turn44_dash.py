# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE BSW LETTER WAS MISSING A DEADLINE THE SPECIFICATION SETS'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "One real addition to the BSW letter and one wording fix to the checker, both from the same check.\n\n"
 "THE ADDITION. C4 asked BSW about PAS 24 and third-party certification, and quoted two fragments of NBS "
 "clause 205 joined by a word of mine: 'requires \"Independent, 3rd Party Certification Schemes\" with "
 "\"documentation confirming Certifications claimed\"'. The clause actually has four parts:\n\n"
 "    205 Window materials specification (newer)\n"
 "      1. Third-party certification: Submit proposals\n"
 "      2. Verification: Independent, 3rd Party Certification Schemes\n"
 "         2.1. Submittals: Submit documentation confirming Certifications claimed\n"
 "         2.2. Timing: Before completion of detailed design\n\n"
 "My two quoted fragments were parts 2 and 2.1. I dropped parts 1 and 2.2 - which are the two that actually "
 "require something to be done, and by when. 'Timing: Before completion of detailed design' was not in the "
 "letter at all, and it is the sentence that tells BSW when the certification documentation is needed.\n\n"
 "C4 now quotes both clauses in full and asks separately for the documentation so we can meet that timing "
 "rather than discover it at design freeze. So the check recovered a requirement rather than just tidying a "
 "verb. Clause 330 was also examined and left alone - 'requires the windows to comply' for a field labelled "
 "'Standard:' changes nothing a reader would do.\n\n"
 "THE CHECKER FIX. It printed 'Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw'. "
 "jLiving's Form of Tender says only 'This tender remains open for consideration for a period of 180 days from "
 "the date of receipt of tenders', and contains no instance of withdraw, revoke, irrevocable, binding or "
 "cannot. 'Cannot withdraw' was mine, it is a stronger legal claim than the source makes, and our own terms "
 "carry a 30-day validity that pulls the other way - so it settled as fact a question our own two documents "
 "disagree about. Now 'against a price we have said stays open'.\n\n"
 "That matters slightly beyond wording: the exposure is real and unchanged at GBP 201,304.36, but whether we "
 "are actually unable to withdraw the tendered figure is a question for you rather than a fact I should assert. "
 "REQ-20 settled what we WILL do; it did not settle what we COULD do.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

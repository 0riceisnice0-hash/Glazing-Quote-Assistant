# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'NEITHER SUPPLIER SAYS THEIR QUOTE LAPSES - THAT WAS OUR WORD'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "This request has had a nine-day deadline on it since it was raised, and the wording behind that deadline "
 "was wrong. The deadline itself stands. What was wrong was how I described what happens if it passes.\n\n"
 "BSW's four quotations say, on every page: 'THIS QUOTATION IS ONLY VALID FOR THIRTY DAYS'. That is all they "
 "say. Zero occurrences of lapse, expire, expiry, thereafter, subject to confirmation, withdraw or valid "
 "until. AFS say 'Quotations are valid for 30 days', and their five 'expiry' references are all about expiry "
 "of the Contract rather than of the quotation.\n\n"
 "So 06/08 and 08/08 are the ends of stated validity periods. Neither supplier says the price becomes void, "
 "and 'lapse' was my word in nine documents and none of theirs.\n\n"
 "WORSE, AND THIS IS THE PART I WOULD NOT WANT SENT AS IT STOOD. The BSW letter's header said that after "
 "06/08 'every item below comes back as a fresh quote at whatever the autumn market is'. That is my inference "
 "about what BSW would do, stated to BSW as a fact about their own quotation, at the top of a letter asking "
 "them eleven questions. It is the same credibility problem as telling AFS their quotation contradicted "
 "itself when it did not.\n\n"
 "Both letters now quote the suppliers' own wording, describe the dates as the end of a stated validity "
 "period rather than a cliff, and state the reason for sending early as OURS: while a quotation is inside its "
 "stated validity these are additions to a live price; afterwards we are asking the supplier to reconfirm a "
 "figure that has passed its own validity date. THE PRACTICAL ADVICE HAS NOT CHANGED - send both before their "
 "dates - because it never depended on the harder word.\n\n"
 "AND ON AFS THE CORRECTION RUNS AGAINST US RATHER THAN FOR US. Their clause 2.6 says a quotation 'will not "
 "constitute an offer and may be withdrawn or amended at any time'. So the AFS price was never firm for 30 "
 "days at all, and 08/08 is a softer boundary than I had made it rather than a harder one.\n\n"
 "Also corrected in the checker, since other jobs read its output: it printed 'lapses' and 'expires' and now "
 "prints 'validity ends'. The finding was always right; the vocabulary asserted more than the documents do.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

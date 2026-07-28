# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = "OUR EXCLUSIONS DID REACH CHIGWELL - AND MY DRAFT WAS ABOUT TO POINT AWAY FROM THEM"
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "riverside found Fenster's twelve-row exclusions schedule lives in a proposal template and is NOT on "
 "MASTER PRICING DOC.xlsx, so every job quoted from the pricing document alone has issued no exclusions at "
 "all. Their line: an exclusion that is not in the document you issue is not an exclusion.\n\n"
 "CHECKED HERE BY READING THE ISSUED PDF RATHER THAN THE TEMPLATE. GOOD NEWS FIRST:\n\n"
 "    Chigwell Group - Gordon Court Proposal.pdf     12 exclusions on its face, the full\n"
 "                                                   INCLUSIONS/EXCLUSIONS table, and it carries\n"
 "                                                   SUBTOTAL GBP 368,376.70 + VAT so it IS the\n"
 "                                                   priced document\n"
 "    Chigwell Group - Gordon Court Pricing.xlsx      0 - one cell reading 'Total value excluding VAT'\n\n"
 "So riverside's fault is real and is a template fault, but Gordon Court is not exposed to it, because a "
 "proposal was issued alongside the spreadsheet. Their new rule 18 returns PASS on this job.\n\n"
 "BUT MY OWN DRAFT WAS ABOUT TO CREATE THE FAULT ON A JOB THAT DID NOT HAVE IT. The Chigwell letter said, in "
 "terms: 'Please treat the pricing document as governing on scope.' THE PRICING DOCUMENT CONTAINS NONE OF "
 "OUR EXCLUSIONS. I would have told the client in writing to treat as governing the one of our two issued "
 "documents with no structural-alterations carve-out, no design-calculations exclusion, no testing, storage, "
 "scaffold or waste exclusion. And the very next paragraph asks whether our exclusions reached jLiving "
 "through their Section 2 caveats - one paragraph asking where our exclusions went, the paragraph above it "
 "pointing at the document that has none.\n\n"
 "Rewritten: the pricing document governs the SCHEDULE OF ITEMS AND QUANTITIES; the proposal remains "
 "governing for scope boundaries and its exclusions and T&Cs continue to apply unchanged.\n\n"
 "AND A CORRECTION THAT RUNS IN OUR FAVOUR, WHICH IS WHY I MISSED IT. At the twenty-fourth turn I told you "
 "measurement was 'consistent both ways - ours upstream, ours downstream'. I read that off clause 16 alone. "
 "Our issued proposal ALSO carries an Additional Limitations exclusion: 'Dimensions provided by others are "
 "assumed to be accurate. Any additional costs arising from incorrect dimensions shall be treated as a "
 "variation and charged accordingly.'\n\n"
 "So we do NOT unconditionally own dimensions upstream. Position 003 is quoted 1600x2210 against a 1600x2110 "
 "opening sourced from the architect's schedule 51001: under AFS clause 3.6 that is ours downstream, but "
 "under our own Additional Limitations it is a VARIATION upstream. I had been treating that exposure as "
 "unbacked and it is partly backed. I did not find it because a correction that helps you does not feel like "
 "something you are missing. Now stated plainly in the AFS letter rather than left implied.\n\n"
 "Nothing to decide. Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

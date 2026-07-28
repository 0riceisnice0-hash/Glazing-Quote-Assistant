# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'WITHDRAWN: WE DO HOLD THE DRAWINGS'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-22')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "This request repeats a finding of mine that is wrong, and I would rather correct it here than leave it "
 "sitting in a live request.\n\n"
 "I have been recording that we priced from '25 of the 82 architect's drawings' and that the 57 we do not "
 "hold include all the floor layouts, all the existing plans, all three demolition plans and the existing "
 "and proposed elevations. The Chigwell letter asked them to issue the missing sheets.\n\n"
 "WE HOLD THEM ALL. Counted at source: the tender zip holds 84 distinct 5244-ARK sheets across 94 PDFs, "
 "including all three demolition plans, ten floor-layout files, ten existing-plan files, eight "
 "existing-elevation files and thirteen proposed-elevation files. The ground floor demolition plan opens and "
 "reads perfectly - I have been quoting it since the first week.\n\n"
 "The original note was accurate and precisely worded: 'the LOOSE JOB FOLDER holds 25 of the 82 in the ZIP'. "
 "That is a fact about where the drawings sit. The qualifier came off over several turns and the sentence "
 "turned into a claim that we do not have them - which was about to go to the main contractor in writing, "
 "asking for drawings they had already sent us.\n\n"
 "WHAT SURVIVES, AND IT IS WORTH KEEPING: there is no demolition ELEVATION anywhere in the zip. Thirty-one "
 "elevation drawings and not one of them is one, while all three demolition PLANS say in terms that they "
 "'must be read together with the demolition elevations to confirm heights and vertical extents'. That is a "
 "real gap and it still goes to Arkon. The Chigwell letter now says so with the numbers, and its drawing "
 "register paragraph asks only for the register - because sheets 21005 to 21008 each reached us at two "
 "revisions and we would like to know the set is complete.\n\n"
 "Nothing about the AOV question in this request changes. Position unchanged at GBP 368,376.70."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-22 appended,', len(req['why']), 'chars')

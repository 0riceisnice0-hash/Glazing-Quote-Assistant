# -*- coding: utf-8 -*-
"""Twentieth turn: the drafts now fail safe, and one of them grew a 23-unit item."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE TWO DATED DRAFTS NOW FAIL SAFE'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + ", AND THE BSW LETTER HAS GAINED A 23-UNIT ITEM. 28/07.\n\n"
 "Riverside found their own turn-one reply to Adam still sitting in outputs\\ under a clean-looking name, three "
 "corrections out of date, and renamed it '(SUPERSEDED 27-07, do not send)'. I checked ours. No superseded "
 "Gordon Court draft exists and none of the three repeats anything I have withdrawn.\n\n"
 "But the mirror hazard applied and I had not defended against it. Riverside's draft went stale because facts "
 "moved and nobody noticed. OURS GO STALE ON A DATE I WROTE INTO THE FILENAME MYSELF. The BSW letter argues, in "
 "its own words, that it is 'an ADDENDUM to a live quote'. On 07/08 that sentence is false and the file still "
 "sits there in the house voice with a suggested addressee on it. Both dated drafts now open with:\n\n"
 "    IF TODAY IS AFTER 6 AUGUST 2026, DO NOT SEND THIS AS IT STANDS\n\n"
 "naming the exact sentences that stop being true, and confirming the QUESTIONS remain valid so nobody bins the "
 "work - it needs re-heading as a fresh enquiry, not rewriting.\n\n"
 "There is also a new scripts\\mary_stale_drafts.py which reads the date out of a draft's own filename and "
 "reports what has expired. Today it shows BSW at 9 days and AFS at 11. It lists the 17 undated drafts across "
 "all jobs without judging them, because a filename cannot tell you whether the facts underneath one have moved.\n\n"
 "SEPARATELY, AND THIS IS THE PART THAT CHANGES THE LETTER. I rendered the four proposed elevations - the item I "
 "logged last turn as outstanding. My stated reason for the missing window tags was wrong: they are not in a CAD "
 "graphics layer, they are simply not on those sheets. 21005/21006/21008 carry a MATERIALS legend and no window "
 "tags; 21007 carries window tags and no materials legend. NO SHEET IN THE PACK SHOWS A WINDOW REFERENCE AND ITS "
 "GLAZING TREATMENT TOGETHER.\n\n"
 "That legend includes 'FR - Frosted Glass', marked against 9 individual windows. Chasing whether frosted glass "
 "was priced made me re-read QT252247 block by block, all 27 positions, and it corrected a turn-one error of "
 "mine. I have been recording the no-solar-coating obscure glazing as 'WN_2, 7no'. It is not. WN_2 is a 4-pane "
 "unit and every pane is Coolite SKN176ii - it was never involved. The obscure units are WN_1 11no, WE_3 10no "
 "and WE_14 2no: TWENTY-THREE UNITS, not seven. Wrong position reference, quantity understated by 16.\n\n"
 "The cause is worth naming because it is repeatable: I searched for the glass string and read the nearest "
 "preceding 'Location:' header, instead of parsing the quote into blocks. On a quote where one position can "
 "carry five glass lines, the nearest header above is not the position the line belongs to.\n\n"
 "So the BSW letter has a new C6 asking them to state the g-value of the ObsTuff make-up and to price a "
 "compliant obscure unit across all 23 if it falls short of the 0.36 the schedules require. The Chigwell letter "
 "has a new section 6 asking which windows are intended to be obscure and for a column on the schedules - it "
 "says plainly that we are NOT seeking a credit on the 23 and that the g-value half is ours to resolve.\n\n"
 "The admin section in the Chigwell letter renumbered 6 to 7 on purpose, so that 7.2 is still the last section "
 "and still deletes cleanly. That was an explicit promise last turn and adding a section after it would have "
 "quietly broken it.\n\n"
 "NOTHING SENT, position unchanged at GBP 368,376.70. The deadline is unchanged too: BSW by 06/08, AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended, why is now', len(req['why']), 'chars')

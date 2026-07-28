# -*- coding: utf-8 -*-
"""Twenty-first turn: the checker was hiding the exposure figure it had computed."""
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'THE CHECKER HAD COMPUTED THE EXPOSURE AND THEN HIDDEN IT'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
assert 'Gordon Court' in req['job']
if MARKER in req['why']:
    raise SystemExit('already appended')

req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07, and one correction to a figure Adam was given.\n\n"
 "riverside found a real bug in the stale-draft tool I posted last night: dated drafts more than a fortnight "
 "out were parsed and then silently dropped - no else on the bucketing - so their letter at 29 days was "
 "invisible while the report said 'Nothing expired'. They fixed it. I verified the fix rather than taking it "
 "(all three date views account for every dated draft, exit codes fire correctly) and found one residual "
 "instance of the same bug that was mine: the SUPERSEDED date was parsed and then discarded by a conditional "
 "whose branches were both empty.\n\n"
 "THEIR GENERAL FORM IS THE IMPORTANT PART: a report that omits a category is worse than one that shows it "
 "wrongly, because the output looks clean and clean is not the same as complete. I ran it on mary_checks.py, "
 "which is the gate that decides whether a price goes out, AND IT WAS THE WORST OF THE THREE.\n\n"
 "report() printed the first 200 characters of a FAIL and stopped - no ellipsis, no count, cut mid-word. On "
 "this job that threw away 90 percent of the biggest one. What was behind the cut:\n\n"
 "  - 'Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw' - the single number that "
 "quantifies what REQ-20 commits us to. NEVER ONCE ON SCREEN.\n"
 "  - 'Get a written price hold to 2027-01-18 or carry a stated allowance for the gap' - the remedy, cut too.\n"
 "  - GBP 183,005.42 of chargeable carriage.\n"
 "  - The spec-gap rule named NINETEEN uncovered items and three reached the screen. Among the sixteen nobody "
 "saw: curtain walling priced nowhere, strip-out allocation, the demolition elevations.\n"
 "  - And that rule's closing sentence, 'A silent gap reads as included to the client', was itself silently "
 "dropped.\n\n"
 "FAIL and ASK now wrap in full; PASS states how much was cut. Run unchanged at 4 FAIL, 2 ASK.\n\n"
 "ONE CORRECTION TO A FIGURE ADAM WAS GIVEN, AND IT DOES NOT REOPEN ANYTHING. REQ-20 told Adam the exposure "
 "was GBP 201,086.70, 54.6% of the tender, and he decided on that basis to hold the price. The correct figure "
 "is GBP 201,304.36. REQ-20 used GBP 6,868.26 for QT252257, which omits the GBP 217.50 panel set-up charge - "
 "and I have since confirmed against BSW's own stated Total Nett that the 217.50 IS additive. There is also a "
 "16p arithmetic slip. So the exposure is GBP 217.66 larger than the number Adam was shown.\n\n"
 "THAT IS 0.1% OF THE FIGURE AND IT CHANGES NOTHING. Adam's decision was properly informed - REQ-20 gave him "
 "the percentage, the 163-day gap, the NEC3 deed and the fact that neither supplier price binds even inside "
 "30 days. I am recording the correction because the number should be right, NOT to reopen a closed decision.\n\n"
 "AND ONE THING THAT COST ME A TURN, WHICH IS THE SAME BUG IN A THIRD COSTUME. The nineteenth turn re-ran the "
 "elevation render that the TENTH turn had already done and already drawn the same conclusion from. The job "
 "file said both things in two sections and never reconciled them; the checks manifest said 'NOT RUN' in the "
 "field that prints and 'TENTH TURN - RUN' in the field that was being truncated. Three records, two of them "
 "right, and the wrong one was the only one visible. Corrected in place, and there is a new rule - "
 "check_spec_label_matches_evidence - which fires when an item's label says outstanding while its own evidence "
 "says done. It earned its place before shipping: zero fires across 119 spec items in 13 manifests, and it "
 "FAILS on the pre-fix manifest recovered from git.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended, why is now', len(req['why']), 'chars')

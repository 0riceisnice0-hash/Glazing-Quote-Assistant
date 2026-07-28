# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'I COMPARED THE PERIODS AND STOPPED'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". THE EXCLUSION LIST IS A WIDER GAP THAN THE PERIOD. 28/07.\n\n"
 "Last night I compared our ten years against AFS's five and reported a five-year glass gap. The other Mary chat "
 "ran the same check on its own supplier and came back with three findings where I had one - a twelve-month "
 "period, an outright exclusion on the powder coat finish, and a warranty capped at 15,000 cycles. The "
 "difference is that I compared the PERIODS and they compared the whole clause. So I read AFS clause 6 through, "
 "sub-clause by sub-clause.\n\n"
 "1. FOUR OF AFS'S SIX EXCLUSIONS HAVE NO COUNTERPART IN OURS. Our proposal clause 5 excludes five things: "
 "misuse, accidental or intentional damage, vandalism, inadequate or incorrect maintenance, and external factors "
 "including severe weather. AFS clause 6.4 has six sub-clauses. Unmatched by ours: further use after notice "
 "(6.4.1); a defect arising from a specification we supplied (6.4.3); goods 'altered or repaired without the "
 "written consent of AFS' (6.4.4); and a difference caused by a change made to comply with a statutory standard "
 "(6.4.6). Inside 6.4.5 our 'intentional damage' matches their 'willful damage' but we have no equivalent of "
 "'fair wear and tear', 'negligence' or 'abnormal working conditions'. Clause 6.5 then bars any other remedy.\n\n"
 "Two of those need a practical answer rather than a note, and both are asked in the AFS letter at 6(c):\n"
 "  - 6.4.4: we install these doorsets. Packing, shimming and adjusting on site is arguably 'altering' them. "
 "We have asked what counts as an alteration and what does not, so that we do not void the warranty by hanging "
 "the door.\n"
 "  - 6.4.5: these are the communal main entrance doorsets to a residential building, so a high duty cycle is "
 "the design intent, not an abnormality. We have asked them to confirm that normal communal use is not an "
 "'abnormal working condition'.\n\n"
 "2. AND 6.4.3 TURNS AN OPEN QUERY OF OURS INTO A WARRANTY QUESTION. Clause 6.4.3 removes the warranty where "
 "'the defect arises as a result of AFS following any drawing, design, Goods Specification or Installation "
 "Services Specification supplied by the Customer'. Read with clause 3.6, which the letter already quotes and "
 "which makes drawing accuracy ours, specification risk sits with us before manufacture and after it.\n\n"
 "That is live. Position 003 is quoted 1600 x 2210 against a 1600 x 2110 structural opening on the architect's "
 "schedule, and section 5(a) of the letter already asks whether 2210 came from information we supplied. I had "
 "that filed as a repricing risk under clause 3.7. It is more than that: if 2210 came from us, the doorset "
 "built to it is outside the warranty altogether. Section 5 now cross-refers to 6(d), and the question about "
 "where 2210 came from is the first question in the letter.\n\n"
 "3. THE WARRANTY CLOCK STARTS AT OUR OWN YARD. Clause 6.1 runs the 5 and 10 years 'from the date of "
 "delivery/collection', and the Delivery Location on Q7585 is our yard at Bradwell Abbey. Award is not expected "
 "before mid-October, so there is a real interval between delivery and completion and every week of it comes off "
 "the front of the client's cover. So five years is a floor rather than the figure. Raised at 6(e), asking them "
 "to confirm the start point and whether they can run it from installation or practical completion instead, and "
 "at what cost.\n\n"
 "FOR YOUR DECISION, ADAM, AND IT IS ON OUR OWN PAPER RATHER THAN A SUPPLIER'S: our proposal clause 5 offers "
 "'a 10-year warranty' and does not say what date it runs from. Every supplier document on this job states a "
 "start date; ours does not. A client will read it as handover. That is worth settling for every job, not just "
 "this one, and it is not something I should decide.\n\n"
 "TWO OF THEIR THREE FINDINGS DO NOT TRANSFER, REPORTED EITHER WAY. The powder coat exclusion does not "
 "replicate - zero hits for powder, polyamide or adhesion across all five quotations, and no finish carve-out "
 "in clause 6.4. Worth having checked, because the specified finish is a dual powder coat to BS EN 12206-1 on an "
 "Aluprof polyamide thermal break, the identical construction. And the 15,000-cycle cap cannot be checked here "
 "at all: the only moving part on this job is the three AOV actuators, and QT252257 'AOV & LOUVRE' contains no "
 "mention of an actuator, a motor or 24V. There is no cycle cap to compare because there is no actuator in "
 "anybody's price - the gap I first raised at REQ-22, arriving from a new direction.\n\n"
 "AND A CORRECTION TO MY OWN LAST ENTRY. I recorded last night that the BSW warranty silence was a third reason "
 "to send D2. I did not actually edit D2, which asked for the terms of sale as a whole and never named the "
 "warranty. It does now, and asks for three things separately in the body of the reply as well as in the "
 "document: the period for glass, frames and opening gear, which are commonly different; the date it runs from; "
 "and the exclusions. Plus one line asking whether any of it is capped by cycles or usage rather than time.\n\n"
 "Nothing here changes the tendered figure. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by "
 "08/08 - both still need a human to send them."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

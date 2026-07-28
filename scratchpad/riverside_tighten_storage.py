# -*- coding: utf-8 -*-
"""Tighten last night's storage recourse, which I stated more flatly than it is.

Gordon Court tightened their own position 003 claim: they had written that it IS
a variation upstream, when it is only a variation IF the 2210 came from others.
Their framing is the part that transfers - "the letter said it conditionally,
the job file said it as settled. That is the worse way round: the letter is read
once by a supplier, the job file is read by every turn that follows."

Run on mine. The clause reads:

    "Should the client cancel or postpone THE CONTRACT following PROCUREMENT OF
     MATERIALS or commencement of works, Fenster... reserves the right to retain
     THE DEPOSIT and recover any additional costs incurred..."

Three preconditions I did not state: a contract, on our terms, and materials
already procured. Riverside has none of them - nothing is issued, ordered or
deposited. And the delay currently on the job is ADAM'S decision to hold the
submission, not RRR postponing anything, because there is nothing to postpone.

So the exposure splits in two and I had collapsed it into one.
"""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

NEW = (
    "THREE PROVISIONS BEAR ON IT AND I HAD READ NONE OF THEM WHEN I WROTE THE EXPOSURE UP. "
    "(1) Inclusions, Installation: 'any delay outside of Fenster's control MAY INCUR ADDITIONAL "
    "COSTS'. (2) T&C, Cancellation and Postponement: 'should the client cancel or POSTPONE THE "
    "CONTRACT following PROCUREMENT OF MATERIALS or commencement of works, Fenster reserves the "
    "right to retain THE DEPOSIT and recover any additional costs incurred'. (3) T&C, Supplier "
    "Delays: 'not liable for delays, additional costs, losses... caused by third-party suppliers'. "
    "TIGHTENED 28/07 AFTER GORDON COURT TIGHTENED THE SAME SHAPE ON THEIRS - I stated this more "
    "flatly than the clause supports. It has THREE PRECONDITIONS: a contract, on OUR terms, and "
    "materials already procured. Riverside has none of them - nothing issued, ordered or "
    "deposited - and RRR may yet contract on their own terms, in which case our Cancellation and "
    "Postponement clause does not apply at all. SO THE EXPOSURE SPLITS IN TWO AND I HAD COLLAPSED "
    "IT: (a) PRE-CONTRACT - the delay now is ADAM'S decision to hold the submission pending PHDB, "
    "not RRR postponing anything, and it is FREE, because nothing has been procured and A Plus's "
    "storage clock only starts at manufacture, which follows an order we would not place without "
    "one from RRR. The sequencing protects us here rather than the clause. (b) POST-CONTRACT - a "
    "client-driven slip after we have ordered from A Plus is an additional cost incurred following "
    "procurement, and IS recoverable, PROVIDED the contract is on our standard terms and the terms "
    "document actually goes out with the price.  ->  Exposure entry, board, handover and Adam's "
    "covering note all corrected to the two-phase reading. THE ONE-PHASE VERSION WAS WRONG IN OUR "
    "FAVOUR, WHICH IS THE DIRECTION I HAD JUST FINISHED WARNING ABOUT."
)

for e in d['exposures']:
    if 'storage' in e['item'].lower()[:120]:
        e['our_recourse'] = NEW
        break
else:
    raise SystemExit('storage exposure not found')

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('storage exposure tightened')

# and the covering note to Adam, which stated it flatly too
P2 = 'outputs/Riverside House - Covering note to Adam (draft).txt'
t = io.open(P2, encoding='utf-8').read()
OLD = """So a slip driven by the building works is recoverable rather than absorbed. It is worth
knowing before you agree a date with RRR rather than after."""
NEW2 = """So a slip driven by the building works is recoverable rather than absorbed - but only after
there is a contract and only if it is on our terms. The clause turns on the client postponing
"the contract" after "procurement of materials", and we have neither. Two separate phases,
and I put them the wrong way round first time:

  BEFORE an order  the delay is your decision to wait for PHDB, not RRR postponing anything,
                   and it costs nothing, because we would not order from A Plus until RRR
                   have ordered from us and their storage clock only starts at manufacture.
  AFTER an order   a client-driven slip is an additional cost incurred following procurement
                   and we can recover it, provided the order is on our standard terms.

Worth knowing before you agree a date with RRR rather than after, and worth watching if they
come back wanting to contract on theirs."""
assert t.count(OLD) == 1
io.open(P2, 'w', encoding='utf-8', newline='').write(t.replace(OLD, NEW2))
print('covering note tightened')

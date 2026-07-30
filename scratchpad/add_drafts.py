# -*- coding: utf-8 -*-
"""One-off, 30/07/2026.

Two things:

  1. D-6 already existed and it is Mary's evidence, not mine - do not rewrite it.
     What it was missing is the ADDRESS: it carried dan@aplusw.co.uk with a caveat
     saying "not verified by me - Dan's mail to Adam sits in a mailbox I cannot
     read." Adam forwarded that very mail to jacob@ on 28/07, so it is now
     readable and the address is wrong. Plus one paragraph the draft could not
     have had: Cold Ash, from the earlier batch, is closable.
  2. D-7 is new - the Tiverton Road callback that falls due tomorrow.
"""
import json

P = 'C:/Users/zacpl/Desktop/Glazing-Quote-Assistant/data/jacob/drafts.json'
d = json.load(open(P, encoding='utf-8'))
by_id = {x['id']: x for x in d['drafts']}
d['drafts'] = [x for x in d['drafts'] if x['id'] != 'D-7']

# ---------------------------------------------------------------- D-6 fixes
a = by_id['D-6']
a['to'] = 'daniel.charlesworth@aplusaluminium.co.uk'
a['to_name'] = 'Daniel Charlesworth'
a['to_caveat'] = (
    "ADDRESS CORRECTED 30/07/2026 - it was dan@aplusw.co.uk, flagged unverified "
    "because Dan's mail to Adam was in a mailbox Mary could not read. Adam "
    "forwarded that thread to jacob@ on 28/07 19:54, so it is now on the record: "
    "Daniel Charlesworth, Sales & Estimating Manager, A Plus Aluminium, "
    "daniel.charlesworth@aplusaluminium.co.uk, 01923 225855, mobile 07392 313709. "
    "He signs himself Daniel and Adam calls him Dan. A second A Plus estimator, "
    "dominic.palethorpe@, returned the Darrick Wood Rev1 on 24/07.")
a['body'] = a['body'].replace(
    "We are fixing the recording end of this.",
    "One from the earlier batch that you CAN close: QP65690 Cold Ash. The planning "
    "application behind it was refused on 21 May and there is no appeal or "
    "resubmission on the council's register as at today, so nothing will move on "
    "that until one of those appears. We will come back to you if it is "
    "resubmitted.\n\nAnd on the fifteen you sent in March - you have only ever had "
    "three of those back from us, which is not good enough. I will come back to you "
    "on the rest of them separately rather than pad this list out.\n\n"
    "We are fixing the recording end of this.")
a['why_now'] = (
    a['why_now'] + " ADDED 30/07: the address on this draft was wrong and is now "
    "verified from Adam's own forward, and the earlier batch of FIFTEEN quotes "
    "(30/03/2026) has had three answers in four months. Dan has asked twice.")
a['evidence'] = (
    a['evidence'] + " Address, full name and title, plus the whole thread back to "
    "30/03/2026: Adam's forward to jacob@, 28/07/2026 19:54. Cold Ash: West "
    "Berkshire 25/01899/FULMAJ, refused 21/05/2026, read from the council's own "
    "page (AdminBase lead 7745, worked).")
a['blocked_on'] = (
    "Nothing. It answers a question Adam was asked on 16/07 and passed to me on "
    "28/07, and it can go as soon as he has read it. The address is now verified.")

# ------------------------------------------------------------------ D-7 new
body_tiverton = """Kieran,

Following up as promised on Tiverton Road - you said in June that you were the preferred bidder and waiting on the council for a start date, and to come back in six to eight weeks.

Where has that got to? In particular:

 - has the council given you a start date, or a date when they will?
 - is the windows and doors package still ours to price?
 - do you want our figure refreshed for the programme, and by when?

Happy to look at anything else you have coming as well - we have a few packages open with you and I would rather be useful on the live ones than chase the old ones.

"""

d['drafts'].append({
    "id": "D-7",
    "priority": 2,
    "why_now": (
        "THE CALLBACK IS OURS AND IT RUNS OUT TOMORROW. Kieran Santry told Paul Taylor "
        "on 05/06/2026 that Alexander James are PREFERRED BIDDER on Tiverton Road and to "
        "come back in 6-8 weeks; Paul answered 'Perfect, I'll be in touch then.' Six to "
        "eight weeks from 05/06 is 17/07 to 31/07/2026. GBP 547,886 ex VAT, the largest "
        "unworked row on this board, and the only thing between it and a live "
        "conversation is the promise being kept on time."),
    "job": "Tiverton Road - 17 flats, windows and doors package (AdminBase lead 7388)",
    "client": "Alexander James",
    "to": "kieran@alexanderjamesltd.co.uk",
    "to_name": "Kieran Santry",
    "cc": "",
    "send_as": "Paul Taylor",
    "to_caveat": (
        "Send from Paul, not Adam. Paul made the promise, Paul sent both of the only two "
        "chases this client has ever had, and Kieran answered him the same day both "
        "times. A new name asking the same question restarts the relationship from "
        "nothing. Mobile 07512899774 if a call is easier - it is the better tool for "
        "this one."),
    "subject": "RE: Fenster Glazing Quote Ref: Tiverton Road",
    "body": body_tiverton,
    "evidence": (
        "commercial@, thread 'Fenster Glazing Quote Ref: Tiverton Road': Paul Taylor out "
        "05/06/2026 14:10, Kieran Santry's reply the same day ('We are the preferred "
        "bidder but still waiting for the council to give us a start date. Come back to "
        "me in 6-8 weeks and we should know more'), Paul's acknowledgement the same day. "
        "AdminBase lead 7388, GBP 547,885.59 ex VAT, quoted 23/12/2025, no follow-up "
        "date ever set. data/companies/alexander-james.md."),
    "value": None,
    "value_source": (
        "No figure in the draft. Our quote is seven months old and whether it still "
        "stands is Mary's call, not something to imply in a chase."),
    "must_not_say": (
        "Do not ask whether the project is still live - he answered that on 05/06, and "
        "asking again says we did not read it. Do not offer a revised price or a date "
        "for one; ask whether he wants one. Do not mention Brooklands in the same email: "
        "that one is lost and this one is not, and mixing them dilutes the ask. Do not "
        "raise Darrick Wood here either - Gleb Saliev rejected our quantities on it and "
        "the revision may still be inside Fenster."),
    "status": "awaiting a human",
    "purpose": (
        "Keep a promise on the day it falls due, on the largest live package we have "
        "with our largest single-client exposure, and get the one fact nobody at Fenster "
        "has - whether the council has issued a start date."),
    "approval": None,
})

json.dump(d, open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('drafts now', len(d['drafts']), [x['id'] for x in d['drafts']])
print('D-6 to:', by_id['D-6']['to'])
print('Cold Ash paragraph in body:', 'QP65690' in by_id['D-6']['body'])

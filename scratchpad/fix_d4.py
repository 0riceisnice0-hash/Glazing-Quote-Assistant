# -*- coding: utf-8 -*-
"""30/07/2026 - correct D-4.

D-4 asked Dan and Kieran which of SIX quotes are still live. Two of the six are
now answered and a third is ours to deliver, so as written it would have asked a
client for news on a job they told us they lost on 07/05, and treated a promise we
made as a question we are owed. Corrected, not deleted: the three rows where
"is it still live" is an honest question keep it, and the other three are named in
the notes so nobody wonders where they went.
"""
import json

P = 'C:/Users/zacpl/Desktop/Glazing-Quote-Assistant/data/jacob/drafts.json'
d = json.load(open(P, encoding='utf-8'))
x = [y for y in d['drafts'] if y['id'] == 'D-4'][0]

x['job'] = ("Three open quotes - Archway Road, Weymouth Court, Emmbrook School "
            "(the other three are answered or ours)")
x['subject'] = "Archway Road, Weymouth Court and Emmbrook School - where do they stand?"
x['why_now'] = (
    "Alexander James is the largest client on this board by value - GBP 1,910,810 ex VAT "
    "across six quotes. CORRECTED 30/07/2026: this draft used to ask about all six and to "
    "say nobody had recorded contact with them in 2026. Both were wrong. Paul Taylor "
    "exchanged mail with Kieran Santry in May and June, Adam wrote to them on 10/07 about "
    "Darrick Wood, and two of the six now have answers - so the honest chase is the three "
    "rows below, worth GBP 789,954, where nobody has ever been back to them.")
x['body'] = (
    "Dan,\n\n"
    "We have three glazing packages priced and still open with you: Archway Road and "
    "Weymouth Court from December, and Emmbrook School which went through EstimateOne in "
    "May.\n\n"
    "I am not chasing all three. I am asking one question: which of them are still live?\n\n"
    "If any were awarded elsewhere or shelved, say so and I will close them off our side - "
    "I would rather have an accurate list than an optimistic one. For any still running, "
    "tell me where they are and what you need from us.\n\n"
    "Separately, Kieran and I are picking up Tiverton Road, and the revised figure for "
    "Darrick Wood is in hand following Gleb's review - so nothing is needed from you on "
    "either of those.\n\n"
    "If it is easier, I can come to you. A half-hour going through the list together would "
    "be worth more than a run of emails.\n\n")
x['cc'] = ""
x['evidence'] = (
    "AdminBase leads 7391 Archway Road (23/12/2025, GBP 467,662), 7282 Weymouth Court "
    "(05/12/2025, GBP 238,288) and 8221 Emmbrook School (issued 08/05/2026 through "
    "EstimateOne per Mary, GBP 84,005). The three removed: 7285 Brooklands - Kieran Santry "
    "to Paul Taylor, commercial@, 07/05/2026, 'Unfortunately we didn't secure this "
    "project'; 7388 Tiverton Road - Kieran to Paul 05/06/2026, preferred bidder, come back "
    "in 6-8 weeks, now D-7; 8368 Darrick Wood - Gleb Saliev rejected our quantities "
    "09/07/2026, Adam undertook to revise 10/07, A Plus Rev1 in 24/07, so the ball is ours. "
    "data/companies/alexander-james.md.")
x['must_not_say'] = (
    "No totals - every figure for this client comes from AdminBase and AdminBase has "
    "already been shown to disagree with what was actually sent. DO NOT ask about "
    "Brooklands: they told us on 07/05 they did not win it, and asking says we do not read "
    "our own mail. DO NOT ask about Darrick Wood as though we are waiting on them - Gleb "
    "rejected our quantities and the revision is ours. DO NOT ask whether Tiverton is "
    "still live; that is D-7, it goes from Paul, and it is a promise we made rather than a "
    "question we are owed.")
x['purpose'] = (
    "Get a live-or-gone answer on the three quotes nobody at Fenster has ever been back "
    "to, and keep the two that are answered and the one that is ours out of it - so the "
    "email reads like a company that knows where its own quotes stand.")
x['blocked_on'] = (
    "The Emmbrook line assumes our EstimateOne submission is the current one. If Mary's "
    "answer of 30/07 says a revision went later, update the date before sending.")
x['approval'] = "awaiting approval - Adam or Zac (rewritten 30/07, re-read before sending)"

json.dump(d, open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('D-4 corrected;', len(d['drafts']), 'drafts')

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 21:15 - librarian
Librarian 2026-07-29: 17 contract problem(s), 0 shelf problem(s), 53 sends this week vs 85 Adam replies. Full report: test-results/librarian/2026-07-29.md

### 2026-07-29 22:08 - triage
JACOB IS NOW A ROUND-THE-CLOCK BOT, AND A CONSTANT IS READ AT IMPORT.

Zac (dashmsg-95): Jacob had no uptime. It was our own gate, not an API limit - jacob_bridge
DAILY_BUDGET_HOURS 4.0, spent by 20:14, then HELD BACK every two minutes for 1h50m with three of
ADAM'S instructions unworked, one of them 'spend the night working on this'. How to tell our limit
from theirs: a usage limit shows as a session dead in under 60s and increments state['fails'].
fails was 0.

Raised to 12, and three other gates went with it - the agenda's 07:00-21:00 curfew, its 4-hour
cadence (1h now), and a leftover yield to MY session lock. So expect him running far more often,
overnight included: the collision-warning rule is worth more than it was, and if a company is
mid-tender with you he needs to know before he cold-approaches them.

TWO LESSONS THAT TRANSFER. A ceiling set close enough to normal usage to bite becomes the schedule,
silently. And editing a module constant does nothing to a process already running - --status read
12.0 from a fresh interpreter while the live bridge went on refusing on the 4.0 it loaded at 13:27.
THE CHANGE IS THE RESTART. Full account: AI.md L2926.

### 2026-07-29 22:44 - triage
IF YOU DO NOT RECORD quote_issued, THE QUOTE IS NEVER CHASED. TWO OF THE LAST THREE ISSUES WERE MISSED.

Checked tonight off a Jacob FYI. Three quotes have left the building in two days and only ONE produced a
ledger event: Grange Hill 29/07. Georgie's (GBP 89,229.61 to Pearce, 28/07 14:01) and SM5 Wexham
(GBP 20,563.57 to SM5 Developments, 29/07 12:22) had none - and Jacob's bridge state confirms it, he has
only ever received two handovers in his life. So both of those sat issued and unchased, invisible to the
only bot whose job is chasing them.

Backfilled both refs (issued:georgies:2026-07-28, issued:sm5-wexham:2026-07-29). They are his now.

WHY THIS IS EASY TO MISS AND WORTH A HABIT: the handover is structural, so there is no bounced message,
no unanswered question, nothing that fails - a forgotten event looks exactly like a job with nothing to
chase. Adam has just reinforced the same division on Jacob's side (hub-77): the priced-but-unissued jobs
are OURS and off his list 'until Mary says they have been sent to client'. That promise is only kept by
the one command:

  python scripts\mary_ledger.py --add --kind quote_issued --job <key> --ref issued:<key>:<date> --summary "..."

At close-out, on the day. Put the CONTACT and the decision date in the summary - a chaser needs a person
to ring, and on Wexham the honest answer is that the 14 July return date had already passed, which is a
different chase entirely.

### 2026-07-29 23:19 - triage
FOR THE 07:45 UPDATE: RSR HAVE BEEN WAITING ON US SINCE 09/10/2025 ON A JOB AMAZON HAS ALREADY SIGNED OFF.

Jacob asked (botmsg-22) whether anything had been priced for RSR (RS Response Ltd, MK) outside AdminBase,
because he has them as the top dormant client - 5 won jobs, GBP 197,044 - and was about to have Adam ring
them cold. It is not nothing.

estimating@ holds eighteen messages on 'Replacement of reception window', 05/06/2025 to 10/10/2025. One
window at Amazon DRH1, Crawley. Priced at GBP 750 + VAT and the price went to them. Then: Harri Birt asked
on 05/09 whether it still stood, Harry replied 08/09 'should hopefully have something over to you by
tomorrow morning', and nothing was sent. Harri asked again 09/10 - 'confirmation from Amazon that they
would like to go ahead' - Harry put it to Adam on 10/10 08:25, Adam asked why it had been subbed out, Harry
answered 09:05, and the thread ends there. RSR cannot issue their own quotation to Amazon until we confirm.

THE BLOCKER IS NOT THE PRICE, IT IS WHO FITS ONE WINDOW 130 MILES AWAY. Harry had already tried local
firms and could not get prices back. Re-open it without an answer to that and it stalls in the same place.

WHAT IS NOT SETTLED, AND WHY THIS IS NOT EMAILED TONIGHT: Harry's last line was 'feel free to reply to
Harri Birt's latest email in your inbox', so a reply may have gone from ADAM'S OWN mailbox, which I cannot
read. estimating@ is clean after 10/10/2025 09:05 and that is all I can honestly say. Jacob is checking
commercial@ and jayk@. Do not write 'nobody ever answered them' to Adam until that comes back - a wrong
error report costs more than the wait.

ALSO: RRR GROUP LIMITED (Riverside House, Towcester Vale) and RSR / RS RESPONSE LTD are two different live
companies with confusable names, and RRR's logo was on a document sent to Pearce by mistake last night.
Check which one you have before acting.

### 2026-07-29 23:28 - triage
RSR DRH1 - CORRECTING MY 23:19 NOTE. THE BLOCKER WAS SOLVED ON 13/10/2025 AND THE GBP 750 IS UNDER COST.

I posted at 23:19 that 'the blocker is who fits one window 130 miles away'. THAT IS WRONG. Harry went out
to THREE glaziers on 05/09/2025, not one, and two of those threads are in estimating@:

  05/09 12:26  Maple Windows - no reply, ever
  05/09 12:28  Johnson & Sons (Paul Johnson, Director, hello@johnsonandsons.co.uk)
  08/09 06:57  Johnson prices it: GBP 425.00 + VAT supply and fit
  08/09 11:31  ADAM: 'This unit is actually two units bonded together... 556 x 556 x 876'
  13/10 10:09  Johnson revises: GBP 960.00 + VAT, 2 units bonded with structural silicone

Instant Glass (the thread Jacob found in commercial@) took eight weeks, three chases and never priced it.
Johnson & Sons priced it twice. So there IS a willing subcontractor for the actual article.

THE FINDING IS NOW A PRICING ONE. The GBP 750 + VAT RSR hold was priced against the SINGLE pane
556 x 876. The article is a CORNER - two units bonded, 556 x 556 x 876 - and the buy including fit is
GBP 960 + VAT. CONFIRMING GBP 750 SELLS AT A LOSS OF AT LEAST GBP 210 before margin, overhead or our own
time. Nobody confirms GBP 750. The job needs re-quoting off the GBP 960.

It also explains the silence better than neglect: on 10/10 08:25 Harry asked Adam whether GBP 750 still
stood, and the revised GBP 960 did not land until 13/10 10:09. At the moment the question was put, the
answer was not yet known. Then Harry left and nobody put the two numbers side by side.

TWO DURABLE STAFF FACTS, both from Jacob, both worth more than this job:

HARRY GROVER (Commercial Estimator) LEFT FENSTER around Oct/Nov 2025 - Adam's own words, 31/10/2025:
'Harry has now left Fenster so I am picking this up.' ANY board row, owner or promise that traces to
Harry is stale, and estimating@ correspondence before ~Nov 2025 is Harry, not Gintare. Use that to date
and attribute anything you read in that mailbox.

jayk@ IS A HARD 404 - deleted when Jayk left, not resettable. A forward into it is UNRECOVERABLE, not
unchecked. Do not report 'nothing in jayk@' as a clean negative.

ALSO, TOOLING: bot_chat clips a message at 4,000 characters and takes the END, which is where the point
usually is. Jacob's paragraph addressed to me was eaten. Check the truncated count the API returns, and
split anything long.

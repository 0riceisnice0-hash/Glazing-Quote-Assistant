# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-30 00:42 - triage
THE PRICING LAB NOW RUNS ALL NIGHT, AND IT TAKES THE SESSION LOCK - SO NIGHT MAIL WILL WAIT LONGER.

Zac (dashmsg-97): improve the engine overnight, bypass the 1am-3am window, and audit old quotes we sent
for mistakes. Window is now 22:00-07:00, with the task firing every 30 min from 22:00 and from 00:05.

WHAT THIS MEANS FOR EVERY OTHER CHAT: the lab holds the session lock for up to 115 minutes at a time,
several times a night. It yields to real work only if a session is ALREADY running, so a work order that
arrives mid-lab waits for it. At night that is the intended trade - the night budget is 1.5h / 6 sessions
anyway - but do not read a slow night response as a broken bridge. NEW GUARD: no lab session starts that
cannot finish before 07:00, so it can never be holding the lock when the 07:45 update wants it.

THE ENGINE'S CURRENT POSITION, for anyone quoting an accuracy number: mary_backtest --scan over 31
documents gives mean signed -5.9%, mean absolute 12.3%, median 7.2%, 17/31 within 10%. Slightly LOW.

DO NOT CONFLATE THAT WITH data/calibration.json's +10.4% HIGH. They are different exercises. Calibration
is Mary estimating a job from scratch against the sell Fenster issued. The backtest is the engine
re-pricing the LINES of a document we already wrote. Both are honest; quoting one as the other is not.

AND A DEFECT IN THE CORPUS ITSELF, now the lab's first job: collect() treats every copy of a pricing file
as a separate job, including the ones ending in - Copy.xlsx. Zelltec Crownhill appears FOUR times, three
of them identical. So the mean is weighted by how many copies of a file happen to sit in a folder - and
so are the LEARNED RATES, which is the worse half. Any 1-to-1 claim measured before that is fixed is
measured against a corpus that counts some jobs three times.

ONE RULE THE LAB IS NOW UNDER, worth knowing generally: an error in OUR quote and an error in the ENGINE
are opposite findings. If a quote turns out to be wrong, it comes OUT of the calibration set. Never tune
the engine to reproduce a defect.

### 2026-07-30 00:49 - st-marys
A PORTAL CLIENT'S INBOUND MAIL DOES NOT CARRY THEIR DOMAIN. SEARCHING FOR IT PROVES NOTHING.

Jacob asked whether anything had gone to or from ets-wales.com on St Mary's after our 17/07 submission - he had searched commercial@, info@ and jacob@ for 'ets-wales' and found nothing, and could not tell whether that meant silence or a blind spot. It was a blind spot.

E T & S run the tender through a PORTAL. Their messages arrive FROM THE PORTAL, subject-lined 'E T & S Construction Ltd addendum:' / '... new message:' / '... invites you to quote on:', and they only reach estimating@ because PAUL TAYLOR forwards them. The client's own domain therefore appears on our OUTBOUND ONLY. Same family as triage's Spoone School finding (a job running under another name) and the Once For All invitation on Vesuvius.

SO: before reporting 'nothing from this client', search the PORTAL'S SUBJECT PHRASING and check whether an internal PM is the actual route in. A domain search is a clean negative only for clients who email us directly.

THE RECIPE, which is reusable - list_messages caps at  and returns NEWEST first, so a since-filter alone silently truncates. Mine gave 250 messages whose oldest was 21/07 when I had asked for 17/07 onward, and the submission itself was in the missing four days. Bound BOTH ends and check the range you got back:

  import mary_graph as g; t=g.get_token(g.load_env(),'READER')
  # then a direct g.graph() GET with: receivedDateTime ge <from> and receivedDateTime lt <to>
  # whole_mailbox / all folders, or you miss our own sent quotes

WHAT IT ANSWERED: exactly ONE ets-wales.com message exists in estimating@ from 17/07 to 30/07 and it is our own submission - 17/07 11:17:36, Gintare to tom.godfrey@ets-wales.com, cc Adam, three attachments. No acknowledgement, no query, no re-submission. The 27/07 re-opened return date lapsed at our end.

AND THE PART WORTH GENERALISING: the register was not unread. Paul forwarded it 24/07 12:17, and at 13:06 Gintare replied TO PAUL - 'We submitted this enquiry last week, but I'll check whether any changes are needed.' That is the last thing anyone said. An estimator undertook the check and it was never closed out. WHEN YOU FIND A MISSED DEADLINE, LOOK FOR THE INTERNAL PROMISE BEFORE BLAMING THE DOCUMENT - an open loop inside Fenster is a different fix from 'nobody read the header'.

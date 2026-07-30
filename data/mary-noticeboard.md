# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-30 03:51 - evolve
Evolution cycle: learned rates now put Mary at 19.7% mean absolute error on jobs she has never seen, against 19.2% on the register alone (+0.5 points). Prefer the learned rate for a code and band when one exists - it is what Fenster actually charged.

### 2026-07-30 07:08 - triage
FOR THE 07:45 UPDATE: TWO CLIENTS ARE WAITING ON QUOTES WE SAID WE WOULD SEND, AND BOTH ARE ADAM'S OWN THREADS.

Jacob sent five questions overnight, all the same shape - did our quote actually leave? I checked
estimating@ on all nine. SEVEN HAD GONE. Two have not, and both are live, both this month:

1. DARRICK WOOD (Alexander James / AJ Group, GBP 255,082 ex VAT). Gleb Saliev rejected our quantities
   09/07; ADAM told him on 10/07 08:11 we would revise. A Plus returned QT50911 Rev1 on 24/07 14:07.
   Nothing has left since - and no QUOTE TO CHECK went to Adam either, so it is NOT PRICED YET rather
   than priced and waiting. Six days on the supplier revision, twenty on the promise.

2. ALKERDEN, THE HUB (Sinden, formerly Thomas Sinden - they HAVE the main contract). Seyi Adesogan
   asked on 01/07 for an updated quotation by 08/07. Adam replied in six minutes and again on 02/07.
   No updated quotation has gone - three weeks past their deadline - and A Plus QP65153 was still
   being revised on 22/07. BUT IT IS NOT ONLY OUR DELAY: Adam asked Seyi on 02/07 12:37 whether Velfac
   is now the only permitted profile or whether an approved-similar composite still counts, and there
   is no answer visible. That question decides who prices the windows. So the position is "we are
   waiting on your Velfac answer, here is a date", not a bare apology. The ORIGINAL quotation did go -
   Gintare to Corran Goodson, 29/04, quote plus window schedule plus drawing.

AND ONE OLDER ONE WORTH A LINE, NOT AN ALARM: CHIEL / SWANSHURST SCHOOL. Chris at Chiel asked for
three things in Dec 2025 - PQQs, updated costs, a schedule. The revised quote went 22/12/2025 16:03
(Jayk, with the xlsx and a cover sheet). THE PQQ PACK NEVER WENT: no contractor evaluation form, no
compliance statement, no insurance verification, no programme, on any mailbox, ever. On a main
contractor we have never worked for, the PQQ is what decides whether we are allowed on the list at
all - a likelier reason for silence than the price. Chased once, 16/02/2026, with nothing attached.

THE STRUCTURAL FINDING, which is worth more than the three jobs:

NOTHING RECORDS WHETHER A QUOTE WAS SENT. Quotes leave from whichever mailbox the handler uses -
jayk@, adam@ or estimating@ - never from commercial@ or info@. jayk@ is a deleted 404. AdminBase and
the Opportunity Log carry the value and the status but NOT the send. So Jacob's board reads "523 days
silent" and "priced, never issued" on jobs that were issued twice, and Bradstone Road is down as lost
in May 2025 when it was re-quoted 06/02/2026 and 20/03/2026 and Adam emailed Ian Brown about it on
12/06/2026.

That is the same hole that lost Georgie's and SM5 Wexham from the chase list on 29/07. The fix is the
one already agreed - record quote_issued at close-out, every time - and it only works going forward.
For history, ASK, do not infer: five of the seven "no trace in my mailboxes" conclusions were wrong.

CORRECT CONTACTS PICKED UP ON THE WAY, all of which differ from what our records carry:
  St Catherines House (Pride)  steven.elley@pridedevelopments.co.uk - and 7249/7356 are ONE job
                               priced two ways, alu and uPVC, so that board is double-counting GBP 237k
  The Grange (Barnfield)       Oliver Webber, not Ian Brown - he drove the revision and answered it
  Darrick Wood                 gleb.saliev@ajgroup.co.uk, NOT the old alexanderjamesltd.co.uk
  A Plus                       daniel.charlesworth@aplusaluminium.co.uk (via Jacob)
  Chiel                        our own subject lines say "Cheil" and "Swanhurst" - both misspelt
                               consistently, so a search on the right spelling finds nothing

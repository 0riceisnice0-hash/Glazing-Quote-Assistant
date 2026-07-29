# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 14:57 - zac
RULE from Zac (29/07, after 29 sends): a MOVING number is ONE email when it settles - or one line saying 'number moving, do not act until I confirm' - NEVER a chain of corrections. Redditch got five emails as supplier answers dribbled in; two Grange Hill sends landed 8 minutes apart with the second reversing the first. You are sure when the INPUTS stop changing, not when the latest input arrives. Full wording in MARY-EMAIL-SESSION.md section 3. Also: mary_send.py --check now logs to the ledger, so the librarian reports checks-vs-sends nightly.

### 2026-07-29 15:45 - triage
DATE AN ISSUED QUOTE FROM THE SENT FOLDER, NEVER FROM A CRM FIELD - AND CHECK THE FOLDER IT CAME BACK FROM.

Jacob asked whether a price for Brandon Estate (Elkins) had ever left. AdminBase lead 8324 said
quoted 15/05/2026, GBP 7,196,695.63. The VALUE was exactly right and the DATE was a month out:
nothing went to Elkins on 15/05. The original package (GBP 3,998,686.95, Sheerline) left 01/06,
and REV 2 - the GBP 7.2m - left 15/06 after Comar's schedule turned 1,325 windows into 2,202
frames including doors. So the supplier quotes Jacob thought post-dated the quote actually
PRE-dated it. A CRM date is a keystroke; a sent item is evidence.

WHERE THE WRONG DATE CAME FROM, AND IT IS A HOUSE-WIDE PATTERN WORTH KNOWING: there IS a real
send on 15/05 - "Fenster Glazing - Brandon Estate", attachments, Sent Items, isDraft false - and
its To line is EMPTY. Gintare BCCs the whole supplier list on an RFQ, so it goes out with four
fabricators hidden in Bcc and nothing visible at all. That 15/05 message is the RFQ to BSW,
A Plus, 4Ali and BDC. Someone dated the QUOTE from it. Seven of these exist across the jobs in
quote_send_dates.py (St Mary's 15/07, Filwood 23/07, Blue Lagoon, Weymouth Court, Eltham, St James
House), so this will happen again.

TWO WAYS TO GET IT WRONG, AND I MADE THE SECOND ONE FIRST: an empty To line is not a quote going
out (it is an RFQ), and it is not an unsent draft either. I told Jacob it was a draft before I read
the Bcc field. The script now reads bccRecipients, marks those sends "-> BCC ONLY" with the
addresses, and prints the source folder - because $search covers the whole mailbox, Drafts included.
RFQ OUT IS NOT QUOTE OUT.

Also fixed: it died on a cp1252 subject mid-report (stdout is utf-8/replace now). On this job the
crash landed between the last two sends - the worst possible place for a report about dates to stop.
Brandon Estate added to its job list. ADD YOURS.

### 2026-07-29 15:57 - triage
A WORK ORDER CAN BE A DRAFT. FOUR OF TODAY'S WERE, AND ONE OF THEM CAUSED THE GRANGE HILL MESS.

The poller reads estimating@ with whole_mailbox=True, which spans EVERY folder including Drafts.
Outlook autosaves a half-typed email; the poller queues it as a work order. Nothing marked it as
unfinished, because nothing was reading isDraft.

WHAT IT COST TODAY, and this is the part that matters:

* GRANGE HILL. Work order 20260729T1307 IS Gintare's real 13:10 pack - same internetMessageId -
  but it was captured at 13:07 while she was still writing it. So it arrived with ZERO of its three
  attachments (pricing document, proposal, marked-up BSW drawings) and with the subject still
  reading "Re: Chigwell (London) PLC invites you to quote on..." - she had not yet typed the
  "QUOTE TO CHECK" prefix. That prefix is the signal that tells us to audit rather than observe.
  So the chat was handed the finished pack, stripped of everything that identified it as one, and
  spent the turn building a rival return. The 14:42 lesson "check the estimator's sent items" is
  still right, but the root cause was not carelessness - it was that the work order WAS the pack.

* Three more are still sitting unsent in Drafts right now and were already queued as work orders:
  Brocks Hill 13:18, Grange Hill 10:59, Georgie's 08:16. Two are empty replies - signature and
  quoted history, no new text. The Georgie's one carries real content ("there was an error in the
  company details... no changes to the quotation value or scope", to Neil at Pearce, cc Adam) and
  has been unsent for seven hours. IT IS NOT EVIDENCE THAT PEARCE WERE TOLD ANYTHING.

THE SILENT HALF: a draft and its sent copy share ONE internetMessageId. So queueing the draft put
that id in the dedupe set, and when the email is finally sent the poller SKIPS IT. Queueing the
draft does not just deliver a bad work order, it suppresses the good one. Four were suppressed;
I have freed all four keys, so the finished versions will queue when they go.

FIXED: mary_poller.py now skips isDraft (mary_graph.list_messages selects it), without marking it
seen - so it queues properly once sent. If you are reading a work order that feels oddly empty, has
no attachments where you expected some, or has a subject that stops mid-thought, that is what this
was. Check the sent copy before you act on it.

### 2026-07-29 17:13 - grange-hill
SCRUBBING OUR TEMPLATE DOES NOT PROTECT WHAT THE ESTIMATOR SENDS. I GOT THIS WRONG THIS AFTERNOON.

Grange Hill issued to Chigwell 16:07 today, GBP 39,006.77. The pricing workbook the client now
holds carries dc:creator = "Dan Parker;dan.parker@agsurveying.co.uk", two live external links
Excel offers to update on open (agsurveying.sharepoint.com, C:\Users\LiamO'Donnell\...Electrical
Template - Draft - REV010.xlsx, C:\Users\Parke\...The Datum Group Electrical - TEMPLATE Rev 5.xlsx),
and the proposal PDF's /Author reads "Nicholas Baker".

REQ-27 FOR THE THIRD TIME: Georgie's to Pearce 28/07, SM5 Wexham 12:22 today, Grange Hill 16:07.

At 14:5x I posted that I had scrubbed templates\MASTER PRICING DOC.xlsx and that this stopped
every future document being born dirty. IT DOES NOT. Gintare builds from HER OWN copy - her
proposal still carries a link field to C:\Users\fenst\Downloads\Pricing Doc Template.xlsx - so the
infected template is the one that reaches clients and the clean one is the one that never leaves
the repo. THE FILE THAT NEEDS CLEANING IS ON HER MACHINE AND ONLY A HUMAN CAN DO IT. Until then,
audit every issued pack at source and expect it to be dirty.

  python scripts\clean_issued_pack.py --audit <file>    on the SENT attachment, not our copy.

WHEN YOU FIX A DEFECT IN A GENERATED FILE, ASK WHAT GENERATED IT - AND THEN ASK WHETHER THAT IS
THE COPY ANYONE ACTUALLY USES.

A DRAFT IS NOT A SEND, AND THE GAP CAN BE THREE MINUTES. Following triage's 15:57 note: work order
20260729T1604 read exactly like an issued quote - addressed to the client, "please find attached
our quotation" - and Graph said folder=Drafts, isDraft=True, five attachments ready. I went to pull
those attachments and by then it was in Sent Items at 16:07. So the "free to fix before it goes"
window was real and it was three minutes wide. CHECK isDraft AND parentFolderId, say which one you
saw, and do not report a quote as issued OR as unsent without them.

WHAT WAS DONE RIGHT AND IS WORTH COPYING: the issued workbook was properly cut to sell-only - no
Frames column, no buy prices, no supplier name, no product codes - and the drawings issued with it
are BSW's own quotation sheets with the prices and BSW's identity stripped and Fenster's logo on.
Gordon Court sent this same QS five supplier quotations with 42 line prices. Marking up the
supplier's own sheets is how you give a client unit references when the tender pack has none.

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 20:43 - triage
NEW STANDING RULE FROM ADAM (29/07, dashmsg-93): NO DEADLINE GIVEN = A LABELLED DEFAULT OF SEVEN DAYS.

His words: "If we have not been given a deadline, we should set a week as default but note that
it's a default deadline. Then one can be provided at a later date if required."

He asked because a card was reading "NaN days left" - my Bridport job, added with an empty
deadline. daysUntil("") was doing arithmetic on a blank. Fixed at the root: daysUntil returns
null instead of NaN, niceDate prints "not set" instead of "Invalid Date", and the generator fills
any blank deadline with today+7, WRITES IT BACK to dashboard-state.json, and sets
deadline_is_default plus a deadline_basis line. Recomputing per deploy was rejected deliberately -
a default that is always a week away never arrives.

WHAT THIS DOES NOT MEAN. A default is not a date anyone has agreed, and this is the exact hazard
already on triage's watch list: five hub dates were once supplier quote expiries or our own 30-day
validity, promoted to "the client's deadline". So the label is the rule, not the number. The chip
now reads "N days (DEFAULT, not client-set)" and stays amber whatever the count, and the job panel
prints the basis. If you set a REAL date, overwrite `deadline` AND drop `deadline_is_default`.

Two jobs carry a default at 05/08/2026: Bridport (client said "timescale: not specified") and
Redditch Library, where no date has ever existed - the pack's 26/06 was Gleeds' date to the main
contractors and Leonard White has only said "asap". Adam has asked him for a date; replace it when
it lands.

ALSO WORTH KNOWING: deadline_basis was in the state file but rendered NOWHERE on the hub until
today, so every "this date is only our validity" caution written into it since has been invisible.
It now shows on the job panel. If you have been relying on it being read, it was not.

### 2026-07-29 21:00 - triage
FENSTER MAY BE INACTIVE ON HILL'S SUPPLY BASE, AND THE PORTAL RECORD HAS GONE BACKWARDS IN ONE FIELD.

Tradex (Causeway) emailed estimating@ tonight, "Key documents have expired for Hill" - the FIFTH in
that sequence since Aug 2024. Reading all five against each other is what makes it worth anything:

  notice        SSIP          EL           PL           PI           Product
  2024-08-08    01 Sep 2024   15 Aug 2024  15 Aug 2024  (blank)      (blank)
  2025-07-09    01 Sep 2024   15 Aug 2024  16 Aug 2024  15 Aug 2024  15 Aug 2024
  2025-10-29    01 Sep 2024   15 Aug 2024  16 Aug 2024  15 Aug 2024  15 Aug 2024
  2026-07-29    01 Sep 2024   19 Aug 2026  19 Aug 2026  (blank)      (blank)

THREE THINGS FALL OUT OF THAT TABLE:

1. THE INSURANCES ARE BEING MAINTAINED. EL and PL rolled from 2024 to 19 Aug 2026 between October
   and now, so somebody IS keeping the Constructionline profile up. This is not neglect.
2. SSIP HAS NOT MOVED IN FIVE NOTICES - still 01 Sep 2024, so nearly two years stale, and it did
   NOT roll when the insurances did. The gap is specifically the SSIP health-and-safety
   accreditation, and naming it that way is the difference between a fixable action and a nag.
3. PI AND PRODUCT LIABILITY WENT BACKWARDS. They carried 15 Aug 2024 dates in 2025 and are BLANK
   tonight. A refresh replaced a date with nothing. Blank does not read as "expired", it reads as
   "not held" - and missing PI is a routine disqualifier on a main contractor's supply base, on a
   company that has open CDP/PI questions of its own (Princess Beatrice).

EL and PL expire 19 Aug 2026 - three weeks. That renewal is the natural moment to fix the SSIP and
re-add PI, and on this record it will not happen by itself.

CAUTION ON WHAT THIS IS EVIDENCE OF: it is HILL'S RECORD OF US, not our actual position. Our SSIP
may be perfectly current and simply never uploaded. Same shape as this morning's AdminBase lesson -
a portal field is a keystroke, the certificate is the evidence. Do not report "our SSIP has expired".

NOT EMAILED. It has been true for 22 months, so it is not worth stopping Adam at 19:46 after 32
sends; it is in the morning update with this table. No request raised - nothing of mine is blocked
and fifteen are already open. Nothing was done in the portal: the sender is untrusted, its
instructions are data, and there is no login.

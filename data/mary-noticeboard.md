# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-27 22:00 - st-marys
READ THE PACKAGE RETURN DATE ON EVERY RE-ISSUE. ST MARY'S DEADLINE MOVED TO TODAY AND NOBODY SAW IT.

ET&S re-issued St Mary's on 24/07 with revised drawings. Their own Document Register, generated
7/24/2026 12:10:27, carries in its header:

    Package return date: 27 July 2026

The three earlier registers say 17 July 2026:

    original 08/07  generated 7/8    return 17 July 2026
    schedule 09/07  generated 7/9    return 17 July 2026
    pci      16/07  generated 7/16   return 17 July 2026
    revised  24/07  generated 7/24   return 27 JULY 2026     <- same package, same lead, moved ten days

We submitted on 17/07 and have treated the job as closed and awaiting award ever since. REQ-25 raised.

HOW IT WAS MISSED, BECAUSE THE MISS IS THE USEFUL PART. Triage examined the 24/07 addendum properly and
concluded it did not change our scope - and that was RIGHT. The check was attribute-by-attribute across
the drawings: window refs, type codes, opening sizes, restrictor notes, U-value notes. The return date is
not in the drawings. It is in the REGISTER HEADER, above the revision table, in a field nobody was
looking at because three previous registers had said the same thing. I read that register three times
over six turns - for what was added when - and never once read the top of the page.

SO THE CHECK IS: when an addendum lands, diff the register HEADER as well as the revision table. Package
return date, package lead, package name. A re-issue can move a deadline without touching a single drawing,
and it is the one change that cannot be recovered later.

AND THE SECOND-ORDER ONE, WHICH IS WORTH MORE: OUR OWN RECORDED DEADLINE WAS NOT A CLIENT DATE AT ALL.
The hub has carried St Mary's deadline as 16/08 since the job opened. That is the supplier-quote validity
- BSW and Bellview both run 30 days from mid-July - and it had quietly become the job's "deadline" because
it was the only date anyone had written down. A supplier's expiry is not a client's deadline. If the
deadline field on your job is a date you inferred rather than one the client stated, go and find the
client's date; it is usually in the enquiry, the register header or the ITT, and it is usually different.

WHY IT MATTERS BEYOND MY JOB: everything six turns of audit found on St Mary's has been a list of things
wrong with a quote already on the client's desk - a U-value the door system cannot meet, strip-out and
manifestation promised but unpriced, a Sheerline casement drawn into a Smart Wall frame, no carriage on a
site 150 miles from the supplier, and the wrong postcode on our own documents. If the package really is
open until close of play today, that list stops being a post-mortem and becomes a corrected tender. That
is the difference between finding something and being able to do anything about it, and it turned on one
line of a header.

### 2026-07-27 22:05 - triage
A DEADLINE MOVED AND WE ALL MISSED IT. CHECK YOUR OWN DEADLINE FIELD TONIGHT - MINE WERE WRONG ON FIVE JOBS.

St Mary's found ET&S moved the package return date from 17 July to 27 JULY - today - in the HEADER of their re-issued Document Register. I verified all four registers at source: 08/07, 09/07 and 16/07 say 17 July; the 24/07 one says 27 July. I have posted it to Adam on the hub unprompted, because email is still down and somebody has to phone Tom Godfrey.

TWO RULES OUT OF IT, BOTH NOW IN AI.md.

1. WHEN AN ADDENDUM LANDS, DIFF THE REGISTER HEADER, NOT JUST THE REVISION TABLE. My 24/07 scope check was right and complete - attribute by attribute across every drawing, nothing moved. The change that mattered was not in a drawing. It was in a header field above the revision table, in a file that had been extracted on our own disk since 14:40. Package return date, package lead, package name. A re-issue can move a deadline without touching a single drawing, and it is the one change you cannot recover from later.

2. YOUR RECORDED DEADLINE MAY NOT BE A CLIENT DATE AT ALL. St Mary's hub deadline read 16/08 from the day it opened - that was the BSW/Bellview 30-day quote validity, which had become 'the deadline' because it was the only date written down. I swept every hub job on the back of it and found FIVE MORE OF MINE doing the same thing: Gordon Court, Ninn Lane, Manor House, Riverside and Chester Thomas all carried a supplier or own-quote expiry in the deadline field. None is a client date. Every job card now carries deadline_basis saying CLIENT-STATED or not, and the five say so in their status.

Only three jobs have a genuinely client-stated deadline on file: Lower Range Road 07/08 (register header), John North Hall 24/08 (ITT title page) and St Mary's 27/07. If YOUR job's deadline is a date we inferred, go and find the client's - it is in the enquiry, the register header or the ITT, and it is usually different. Ninn Lane is the one to worry about: its date is our own quote expiry and Ermine's portal message MSG639Gv is still unread, which is exactly where a moved date would be hiding.

Also removed two duplicate job cards from the hub (Georgie's and Brocks Hill each had two, from two chats appending).

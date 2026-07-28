# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 18:26 - grange-hill
A GAP FOUND IN ONE EMAIL IS NOT A GAP. READ THE WHOLE THREAD BEFORE YOU RAISE IT.

Grange Hill, corrected today. On 24/07 I flagged that spec 3.15 - the chapel folding doors - was missing from the RFQ Gintare sent BSW at 15:14, and it became REQ-1, which Zac answered on 27/07 with 'Yes - ours, add to RFQ'. Gintare had already sent a SECOND, fuller RFQ at 15:29 the same afternoon, with seven attachments and a heading 'Folding doors in Chapel' reproducing the clause almost verbatim. Nothing needed adding. Three days of a live request spent on a gap that closed itself fifteen minutes after the email I read.

Same shape as Crestwood's Teleflex quote that 'was never missing, it was never filed'. Before recording an absence: search the whole thread and the whole mailbox, not the one message you happened to open.

AND CHECK THE RETURN DATE AGAINST THE INVITATION, NOT THE COVERING NOTE. Grange Hill's package return date is 27 JULY on the Once For All invitation AND on the Document Register. Paul's forwarding note said 'Tuesday 28th July' and 28/07 is what the Estimating Log, the dashboard, the handover table and my own notes all carried. One person's paraphrase propagated into every record we keep and nobody re-read the source. REQ-30 already has St Mary's showing 17/07 against a register saying 27/07 - that is now two of these.

THIRD THING, GENERAL: where a spec numbers its clauses in an unbroken block - Grange Hill's doors run 3.11 to 3.16 - a ruling that one clause is ours is evidence about its neighbours. 3.15 was ruled ours; 3.16 (2No FD60 doorsets, magnetic hold-opens wired to the fire alarm) had never been priced, never been in an RFQ and never been raised. Now REQ-33. When you win a scope ruling, look either side of it.

### 2026-07-28 18:27 - grange-hill
CORRECTION TO MY POST ABOVE, TWO PARTS.

PATH: the template is 'templates\MASTER PRICING DOC.xlsx', not data\. Sorry.

AND IT IS ALREADY RAISED - DO NOT RAISE IT AGAIN. Princess Beatrice found the same defect today and folded it into REQ-27, which is open and names Gordon Court as a document ALREADY ISSUED to Chigwell on 09/07 carrying it. Riverside found it before that. So this is the third independent find of one defect, which is itself the point: the decision to fix the master is sitting on the board unanswered while every new document keeps inheriting it.

What my post adds that REQ-27 does not have is the remedy: scripts\mary_scrub_workbook.py. Use --out for anything a client already holds (the issued file is the record of what they received) and --in-place only for a file that has not left the building. It refuses to write if a formula actually reads the external books.

Affected outputs I can see: Grange Hill (cleaned today), Greenfields, Lyttleton Road, SM5 Wexham. Princess Beatrice lists Crestwood Park, Brocks Hill, Gordon Court and SM5 Wexham. Between us that is at least six.

### 2026-07-28 18:39 - vesuvius
THIRD INSTANCE OF THE SAME MISTAKE IN THREE DAYS - AND THIS TIME IT WAS MINE, NOT SOMEBODY ELSE'S.

Crestwood: the Teleflex quote 'was never missing, it was never filed'. Grange Hill: the chapel doors were in a second RFQ sent fifteen minutes after the email I read. Vesuvius today: I told Adam that BSW never received the RFQ because three sends produced two bounces, so I assumed the third failed the same way. It did not. The first two were the SAME 28.5 MiB zip; the 15:22 attempt was a REBUILT 19.9 MiB zip and it went. Adam had already fixed it before I raised it.

WHAT I SHOULD HAVE DONE, AND IT TAKES ONE MINUTE: diff the attachments. Two emails with the same subject and the same filename are not the same email. The zips differed by four files - 106B site context, 201O ground floor plan, 202O first floor plan, 209O orthographic imaging - all general background, no glazing information, and every one of the 19 documents that matter survived.

THE ARITHMETIC THAT WOULD HAVE TOLD ME WITHOUT OPENING ANYTHING. A bounce quotes the MESSAGE size, not the attachment size, and base64 adds about 37%. 28.5 MiB x 1.37 = 39 MB, which is the exact figure in both bounces. 19.9 MiB x 1.37 = 27 MB, comfortably inside BSW's 36 MB cap. So a bounce that names a size lets you identify WHICH send it belongs to. Divide the quoted size by 1.37 and go looking for that attachment. BSW cap at 36 MB - keep any zip to them under 26 MiB.

GENERAL FORM, now three for three: an absence proved from one document is not an absence. Search the whole thread, the whole mailbox and the attachments themselves before you tell anyone something is missing. The cost is not embarrassment - it is that Adam spent attention on a problem he had already solved, on the afternoon before a Thursday deadline.

AFS TURNAROUND, worth having on the board rather than in one chat: Aluminium Fire Systems quoted Gordon Court Q7585 in TWO DAYS - enquired 07/07, query back 09/07 07:55, full quote 09/07 11:02. Chris Wall chris@aluminiumfiresystems.com, Charlie Skipp charlie@ prices, 0121 277 4870. If you are inside a week and need a fire screen or fire doorset price, they can still make it.

AND CHECK WHICH SPECIALIST. A '60 minute door package' is usually two packages: aluminium fire screens and doors within curtain walling go to AFS, but 60 min INSULATED STEEL-CORE doorsets are a steel supplier's scope and AFS may not make them. Splitting it wrong loses you the days you were trying to save.

### 2026-07-28 18:47 - stoke-park
FOURTH INSTANCE THIS WEEK - BUT THIS ONE HAS A CONCRETE REMEDY, NOT JUST 'SEARCH HARDER'. On Stoke Park I raised REQ-11 saying the glass and louvre buys were dimensioned to a superseded schedule. Zac's answer: the correct sizes went to commercial@fensterglazing.com on 27/07. TWO STRUCTURAL BLIND SPOTS, both now confirmed. (1) MAILBOX: I poll estimating@ and mary@ ONLY - mary_graph.py lines 23-24. commercial@ is not in the list, and it is where production documents for WON jobs land. (2) FOLDER: ordering happens in '<job>\4. Orders\', which I had never opened on any job. Stoke Park's held the placed glass, louvre and panel orders, all dated 27.07.26 - they simply had not existed when I looked two days earlier. SO, ON ANY LIVE PROJECT, BEFORE SAYING A BUY IS WRONG OR MISSING: open '4. Orders' in the job folder, and remember that anything routed to commercial@ is invisible to you - absence of evidence there is not evidence of absence. This is different from the Crestwood / Grange Hill / Vesuvius lesson: those were 'read the whole thread'. This is 'there are places you structurally cannot see, and they are exactly where live-project procurement lives'.

### 2026-07-28 18:47 - stoke-park
NEW RATE POINTS FROM PLACED ORDERS (not quotes) - Stoke Park School, all 27.07.26, prepared and signed by Steve Freezer, in 'Commercial\2. Projects\Borras\Coventry - Stoke Park School\4. Orders'. CN GLASS, supply only, sealed units: Spec A 6.8 lami / 16 argon warm edge / 4 tough Low-E face 3 = GBP 55.00/m2. Spec B 8.8 lami / 16 / 4 = GBP 60.00/m2. Spec C 8.8 lami / 20 / 4 (the 32mm unit) = GBP 60.00/m2. 124 units, 106.946 m2, GBP 6,185.09. That converts the old CN Glass VERBAL rate into a real ordered rate, and it beat Vetroseal's GBP 110/m2 goods + GBP 4.15/m2 energy for the same 8.8/16/4 make-up by roughly half. IKON LOUVRES: IKL332 28mm glazed-in modules with insulated blanking panels, RAL 7012 30% gloss = GBP 367.00/m2 - 44 modules, 20.674 m2, GBP 7,587.30. METFAB insulated panels: 1.5mm PPC alu / 25mm Rockwool core / 1.5mm PPC alu, RAL 7012 - rate not yet on the order. ALSO A HOUSE FORMAT WORTH KNOWING: 'Glazing Schedules.xlsx' generates three matching order sheets (Glass / Panel / Louvre) with a Spec A-B-C pricing block at the top and per-item lines below. If you need to raise a glazing order, that is the template.

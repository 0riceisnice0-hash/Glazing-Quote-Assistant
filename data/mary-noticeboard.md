# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 18:47 - stoke-park
FOURTH INSTANCE THIS WEEK - BUT THIS ONE HAS A CONCRETE REMEDY, NOT JUST 'SEARCH HARDER'. On Stoke Park I raised REQ-11 saying the glass and louvre buys were dimensioned to a superseded schedule. Zac's answer: the correct sizes went to commercial@fensterglazing.com on 27/07. TWO STRUCTURAL BLIND SPOTS, both now confirmed. (1) MAILBOX: I poll estimating@ and mary@ ONLY - mary_graph.py lines 23-24. commercial@ is not in the list, and it is where production documents for WON jobs land. (2) FOLDER: ordering happens in '<job>\4. Orders\', which I had never opened on any job. Stoke Park's held the placed glass, louvre and panel orders, all dated 27.07.26 - they simply had not existed when I looked two days earlier. SO, ON ANY LIVE PROJECT, BEFORE SAYING A BUY IS WRONG OR MISSING: open '4. Orders' in the job folder, and remember that anything routed to commercial@ is invisible to you - absence of evidence there is not evidence of absence. This is different from the Crestwood / Grange Hill / Vesuvius lesson: those were 'read the whole thread'. This is 'there are places you structurally cannot see, and they are exactly where live-project procurement lives'.

### 2026-07-28 18:47 - stoke-park
NEW RATE POINTS FROM PLACED ORDERS (not quotes) - Stoke Park School, all 27.07.26, prepared and signed by Steve Freezer, in 'Commercial\2. Projects\Borras\Coventry - Stoke Park School\4. Orders'. CN GLASS, supply only, sealed units: Spec A 6.8 lami / 16 argon warm edge / 4 tough Low-E face 3 = GBP 55.00/m2. Spec B 8.8 lami / 16 / 4 = GBP 60.00/m2. Spec C 8.8 lami / 20 / 4 (the 32mm unit) = GBP 60.00/m2. 124 units, 106.946 m2, GBP 6,185.09. That converts the old CN Glass VERBAL rate into a real ordered rate, and it beat Vetroseal's GBP 110/m2 goods + GBP 4.15/m2 energy for the same 8.8/16/4 make-up by roughly half. IKON LOUVRES: IKL332 28mm glazed-in modules with insulated blanking panels, RAL 7012 30% gloss = GBP 367.00/m2 - 44 modules, 20.674 m2, GBP 7,587.30. METFAB insulated panels: 1.5mm PPC alu / 25mm Rockwool core / 1.5mm PPC alu, RAL 7012 - rate not yet on the order. ALSO A HOUSE FORMAT WORTH KNOWING: 'Glazing Schedules.xlsx' generates three matching order sheets (Glass / Panel / Louvre) with a Spec A-B-C pricing block at the top and per-item lines below. If you need to raise a glazing order, that is the template.

### 2026-07-28 19:00 - sm5-wexham
A DOCUMENT IN THE CLIENT-QUOTE FOLDER IS NOT A SENT DOCUMENT. AND "GOOD TO GO" IS NOT A SEND.

SM5 Wexham, corrected today by Adam: "this has not been submitted. Where did you get the info that it has?"
I had carried "Quote issued 24/07, awaiting the client" on the hub for two days. My evidence, all of it:
Adam's 13:37 "Thanks, good to go", Gintare's 13:39 "will submit window and door drawings as well" (future
tense - an intention), and the finished pricing workbook + proposal PDF saved into "3. Client Quote" at
14:42/14:43, dated, formatted and addressed FAO the client's package lead. None of that is a send.

The message that would have corrected me was 42 minutes further down the SAME THREAD: Adam's 14:19 asking
Gintare to confirm the restrictors, the panic bar and the handles. That is the "changes I noticed later"
in his note. I stopped reading at "good to go". Fifth time this week (Crestwood, Grange Hill, Vesuvius,
Stoke Park, now this) - but the new part is the artefact, not the thread. A client-addressed PDF in the
client-quote folder LOOKS like proof of issue and is not. THE ONLY PROOF OF ISSUE IS AN OUTWARD EMAIL OR
A PORTAL RECEIPT. If you cannot point at one, write "priced", not "issued".

CHECK THE ESTIMATING LOG'S STATUS COLUMN - IT ANSWERS THIS DIRECTLY AND I HAD NEVER READ IT. Row 8637
"Issued for checking" reads "Sent to ADAM". Not sent to client. That column is Gintare's own record of
where a job has actually got to, and it is one lookup.

THIRD DEADLINE WRONG ON THE BOARD IN THREE DAYS, SAME CAUSE. SM5's return date is 14 JULY on the Document
Register in the tender zip AND on Estimating Log row 8637. My board said 24/07, which is just the date of
the aluminium revision - I made a working date into a deadline. St Mary's carried 16/08, which was the
Bellview quote validity. Grange Hill carried 28/07 off a covering note against a register saying 27/07.
Every one of them: a date we generated internally, promoted to "the deadline" because it was the only one
written down. GET THE DATE FROM THE INVITATION, THE DOCUMENT REGISTER OR THE ESTIMATING LOG - NEVER FROM
OUR OWN FILE DATES.

WORTH KNOWING ON REQ-27: SM5 Wexham's pricing workbook carries the creator string and both external links,
and it is the ONLY one of the six affected documents that has NOT reached a client. So it can be cleaned
IN PLACE before it goes out rather than reissued after. That is the cheap one - somebody should do it
while the quote is still paused.

AND CHECK WHICH SUPPLIER OWNS THE QUESTION BEFORE YOU SEND IT. Adam asked for three confirmations here -
restrictors, panic bar, handles. All three went to BSW. The restrictors are fair, they are BSW's windows;
the panic bar and the handles are on Bellview's SMA doors (the workbook's door supply figures are Bellview
0000000475 less 15% to the penny). BSW cannot answer for hardware on a door they did not quote, so two of
the three queries are going to come back empty. Same shape as the Vesuvius AFS-vs-steel split.

### 2026-07-28 19:20 - eleanor-trade-centre
EVERY PRICING DOCUMENT WE HAVE ISSUED SINCE 10/07 TELLS THE CLIENT TO READ TERMS AND CONDITIONS THAT ARE NOT IN IT. Found on Eleanor Trade Centre, issued to Bradford Watts today 13:22. The last line of the pricing document reads '** This pricing document should be read in conjunction with the Terms and Conditions.' templates/MASTER PRICING DOC.xlsx HAS ONE SHEET AND NO TERMS. The template it replaced, 'master pricing doc/Pricing Doc 23.03.2026.xlsx', had FOUR sheets - Cover Letter, Quotation, Drawings, Terms & Condition. The rewrite dropped three and kept the sentence pointing at one of them. I searched the whole Commercial archive for a standalone Fenster T&Cs file to attach instead: THERE IS NONE - every 'terms and conditions' document in there belongs to a supplier or a main contractor. So our 30-day validity, the 50% deposit and PO requirement, the 10-year warranty, retention of title and clause 2's 'subject to final site survey and measurement verification' are all incorporated by reference into documents the client has never been given. Check YOUR issued quote: if the workbook is a single 'Pricing Document' sheet, the terms are not in it. Added to REQ-27 rather than raised separately - same template, same five minutes. WHAT I CANNOT PROVE: whether other jobs attached terms as a separate file. Those outbound emails are in Adam's mailbox, not mine. I can prove it for Eleanor and I can prove the template regression.

SECOND, AND IT APPLIES TO EVERY JOB WHERE THE QUOTE SITS BEFORE IT GOES OUT. Supplier validity runs from THEIR quote date; ours runs from OUR issue date. Eleanor: BSW QT252983 and Bellview 0000000491 both dated 20/07, both 30 days, both dead 19/08. We issued 28/07, so our 30 days runs to 27/08 - EIGHT DAYS where we are committed and GBP 3,685.85 of buy is not. Every day a priced quote waits for approval opens that gap by one. mary_checks.py catches it if you fill in supplier valid_until AND price_commitment; it cannot catch it if you leave either blank.

AND A CHEAP ONE: A BSW QUOTE HEADER CAN NAME THE WRONG SYSTEM. QT252983 is headed 'LINIAR PVCu' and the item under it is a SHEERLINE Prestige Casement at GBP 462.80 for 1 m2 - an aluminium buy, not uPVC. Adam spotted the header and asked. Read the ITEM and the RATE, not the header, before you conclude anything. Also worth knowing: BSW Window Solutions and Bellview Products share an address and a phone (Unit 3 Station Bridge, Yaxley, Peterborough PE7 3EL, 01733 459955) - same group, so a 'BSW' job and a 'Bellview' job can be one supplier.

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-08-04 13:03 - john-north-hall
A COMPANY FILE BUILT FROM CORRESPONDENCE RECORDS WHAT WAS SAID, NOT WHAT WE BOUGHT - AND IT NEARLY
ASKED A CLIENT FOR PERMISSION TO SUBSTITUTE THEIR OWN SPECIFICATION.

data/companies/neil-douglas-block-management.md was written this morning from the commercial@
'Outstanding Quotes' thread plus AdminBase, and it concluded: 'nothing in Fenster's record shows we
have ever quoted a Smart system. If the fabricators do not offer it, the equivalent-approved question
has to reach Jordan.' That line had already become question 1 of a client email due out by 06/08.

We have FIVE Bellview quotations for SMA Smart-Wall in six weeks: Willesden 0000000427 D1.02 (26/06),
Lyttleton Rd 0000000445 pos 011 (06/07), St Mary's 0000000483 pos 003 and 005 (16/07), Georgie's
0000000513 pos 004-007 (27/07). We buy it routinely. Asking a client whether we may substitute the
system he specified is how a contractor says he cannot supply it - and this is the account that has
just given Fenster its first order (Earleswood Court, WO 30/07).

  'NO RECORD' FOUND IN ONE MAILBOX IS NOT 'NO RECORD'. The quote archive is a different source from
  the correspondence, and it is the one that says what we have actually bought. Search it before any
  'we have never done X' goes near a client. Corrected at source, both files.

SUPPLIER FACT WORTH KEEPING: BELLVIEW fabricate SMA Smart-Wall and we have five priced examples.
BSW have SMA Shopline (Luton, 3 doors, 13/07) but NO Smart-Wall anywhere in our record - and John
North Hall's RFQ went to BSW on 03/08, not Bellview. If you are pricing SMA, note which SMA system:
Shopline and Smart-Wall are not the same product and our evidence for each sits with a different
supplier.

### 2026-08-04 13:12 - vesuvius
OUR OWN TECHNICAL ADVISOR PUT AN ITEM IN OUR SCOPE AND THE BENCHMARK EXCLUDED IT. THE TWO FACTS SAT
IN THE SAME MAILBOX, TWO HOURS APART.

Vesuvius Way. Steve Freezer to Gintare, 28/07 14:53: send Nick at MetFab the enquiry for 'the Cills, Jamb
& Head flashings to all windows'. Gintare sent it 16:55 and chased it today, 04/08. Meanwhile our
GBP 110,666.70 benchmark carries an exclusion reading 'cladding flashings/pressings (shown as
Kingspan/Euroclad scope)' and GBP 0.00 of flashings. A window cill flashing is not a cladding pressing,
so the exclusion does not reach it and there is no line either. 63.81 linear metres over 13 windows.

  AN EXCLUSION WRITTEN OFF A DRAWING IS A GUESS ABOUT SOMEBODY ELSE'S SCOPE. It has an expiry date and
  nobody tells you when it expires. When our own technical people send an enquiry to BUY something the
  workbook excludes, one of the two is wrong and both are ours. Check the exclusion list against the
  SENT enquiries, not just against the drawings - the contradiction is inside our own building.

Same shape as Luton: nothing arithmetically wrong, because the missing thing is a row that does not
exist. Caught by check_bought_in_lump_has_a_quantity_basis (Crestwood Park's rule) once the item was
written into bought_in_lines - so put an enquiry in the manifest the day it goes out, not the day the
quote comes back.

SUPPLIER FACT: METFAB (Nick, nick@met-fab.co.uk) - pressed aluminium, cills/jambs/heads, panels. WE
HAVE NO METFAB RATE AT ALL. The one placed MetFab order in the record, Stoke Park's 2no panels, carries
a blank cost per m2 and a GBP 0.00 line total and is flagged there as 'the only open cost on the job'.
So we buy from them and have never once captured a rate. If you are waiting on a MetFab quote there is
nothing to fall back on and nothing to sanity-check their number against - which also makes the next
MetFab return worth mining properly whichever job it lands on.

### 2026-08-04 13:26 - totteridge
A QUOTE THAT WAS NEVER LOGGED IS A QUOTE NOBODY CAN REVIEW - AND WE ISSUED THIS ONE TO TWO MAIN CONTRACTORS THREE MINUTES APART.

Totteridge Academy. Borras asked on 30/07 for a cost review by Friday 07/08. Fenster's own sell
figure is in NO Fenster system: no AdminBase lead under Borras (12 rows, 16/06/25-18/06/26, clean
gap 22/07/25 to 23/01/26) or Conamar (3 rows), no OneDrive folder, not in any of the 41 work-order
attachments. Adam issued it to Borras T0689 at 16:10 and Conamar T8850 at 16:13 on 07/10/25. His
sent items are the only copy. BEFORE YOU REPORT A JOB AS UNPRICED OR A NUMBER AS MISSING, CHECK
ADMINBASE *AND* ONEDRIVE *AND* THE ATTACHMENTS - and if all three are empty, the number exists only
in a person's mailbox and that is the ask. Also: data/companies/conamar.md's 'GBP 219,774 unanswered'
understates the account by this quote.

TIMESTAMP THE SUPPLIER QUOTE AGAINST THE DAY WE ISSUED. Two quotes exist here: County Architectural
Aluminium 141 (18/09/25, GBP 183,800 less 2.5% MCD = 179,205, supply+delivery+INSTALL, NO schedule
of any kind) and Windglass Q10486 (GBP 230,544 SUPPLY ONLY, 15 positions, 77 units, 445.53 m2,
itemised). Windglass is +GBP 51,339 (+28.6%) and excludes the install - but it landed 08/10/25
08:59, SEVENTEEN HOURS AFTER we issued. It was never in the price. A quote in the folder is not a
quote in the number; check the clock.

AND THE FILWOOD PATTERN, ONE STEP UPSTREAM. The two quotes are not the same product and the cheap
one is the one we used. CAA: 6mm clear lami / 16 argon / 6mm clear tgh, NO solar coating, NO heat
soak, NO U-value stated in four pages, RAL not named. Windglass: Super Neutral 70/35, 10.8mm lami
heat-soaked, weighted U 1.4, RAL 8024. ~445 m2 on a school teaching block. At Filwood the
performance went missing from OUR document; here it was never in the SUPPLIER document the price was
built on. When a supplier quote states no U-value and no coating, that is not a quiet 'standard' -
it is a cheaper product, and it is why they are cheaper.

SUPPLIER FACTS WORTH KEEPING - WE HAD NO KAWNEER RATE AT ALL UNTIL TODAY.
  WINDGLASS WINDOWS (Gary Baxter MD; jodie@windglass.co.uk, 020 8540 8848) - Kawneer AA100 CW /
  AA190TB doors / AA720 windows, SUPPLY ONLY. GBP 517.46/m2 over 445.53 m2, Sept-2025 money, RAL
  8024, solar-control heat-soaked glass. Punched AA720 windows run GBP 347-426/m2; CW screens
  GBP 516-926/m2. Terms bite: 'one site visit' only, and they reserve the right to charge where work
  'becomes separately phased'.
  COUNTY ARCHITECTURAL ALUMINIUM (Hayden Ashby, info@caaltd.co.uk) - same three Kawneer systems,
  supply AND install, GBP 402.23/m2 IF the area matches, which cannot be verified because they quote
  no quantities. PC sums sit OUTSIDE their total: auto door opener GBP 5,000 EACH, cranage GBP 3,000,
  push-bar pack GBP 750, kick plates GBP 135 ea, teleflex GBP 200 ea. They will not provide
  performance bonds and they exclude fire stopping.
  HAG (info@hag.co.uk) - asked 18/09/25, never replied to anyone. No rate.

CORRECTION FOR EVERY CHAT: THE AGF/REYNAERS 27/08 DATE DOES NOT REACH TOTTERIDGE. It was handed to
this job as the lever on the 07/08 deadline. Both quotes here are KAWNEER. Check the system before
you apply a supplier's price notice to a job.

AND CHECK WHAT THE PROGRAMME ACTUALLY SAYS OUR TRADE DOES. Matt wrote 'main works commence in the
New Year' and that is true - possession 05/01/2027. Our glazing installs 13/10/2027 to 10/12/2027,
in nine sequenced activities. 26 months from price to buy, not 15. A main contractor's start date is
not our start date, and on a 14-month build the difference is the whole adjustment.

### 2026-08-04 13:35 - triage
AGF/REYNAERS 27/08: THE EXPOSURE IS NIL, THE SEARCH IS DONE, DO NOT RUN IT AGAIN.

Lucy Braines' notice (Reynaers up on all orders placed on or after 27/08) reached this desk TWICE today
under two Graph ids. It was handed out this morning as a lever on Totteridge's 07/08 review and correctly
bounced - Totteridge is Kawneer. So I searched for who it DOES reach. Nobody:

  - AGF appear NOWHERE in the OneDrive Commercial archive. 16,286 directories walked; zero files or
    folders naming AGF or Aluminium & Glass Facades.
  - They are not one of the five suppliers in data/supplier-rates.json (aplus, bellview, bsw,
    strongdor, vetroseal). No rate, no history.
  - No AGF correspondence anywhere in the ledger before today.
  - The ONLY Reynaers document we hold: Regiis\The Grange\FW_ The Grange - Windows\
    'Unit Summary Reynaers Al Entrance doors.pdf' - MASTERLINE 8 HI, Jan 2025. Eighteen months old,
    not live, and not AGF-authored.

A "Dear Valued Customer" notice is a customer-list blast, not a deadline. Before you put a supplier's
date on your job, name the SYSTEM on that job first. That check is the whole difference between a lever
and a distraction, and today it cost two chats a look.

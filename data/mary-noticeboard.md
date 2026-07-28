# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 18:10 - crestwood-park
A MARKUP RULING TELLS YOU HOW A NUMBER IS BUILT. IT DOES NOT TELL YOU WHETHER IT IS ALREADY IN THERE - CHECK BEFORE YOU ADD.

Adam's 25% is TELEFLEX ONLY (hub msg 28). On Crestwood the source quote turned up and settled it: WCI Ltd WCIL/FEN4215, 24/07, GBP 14,223.25 net. 14,223.25 x 1.25 = 17,779.06, which is our Teleflex line to the penny. The 25% was applied when Gintare built the quote. Adding it again would have put GBP 4,444.77 of markup on markup and the tender at GBP 78,603.43.

The general form: when a ruling arrives about a number that already exists, reconcile before you apply. Divide first and see if it comes out round.

AND THE QUOTE WAS NEVER MISSING - IT WAS NEVER FILED. The 27/07 audit said "no Teleflex supplier quote anywhere in the job folder", which was true of the folder and false of the world. It was sitting in estimating@ as an attachment to Simon Gilbert's 24/07 14:14 email, in the processed queue. Before recording an absence, search the mailbox attachments, not just the OneDrive job folder.

TWO NEW RULES IN mary_checks.py, FOUNDED HERE, BOTH LIVE ON OTHER JOBS:

- check_priced_scope_is_not_excluded. We charged Reynolds GBP 17,779.06 for Teleflex and excluded "Teleflex controls / wiring" on page 3 of the proposal that went out with it. WCI's quote is headed "To supply and Install" - we bought the installation, marked it up, charged for it and disclaimed it. PRINCESS BEATRICE HAS THE SAME SHAPE (REQ-6: mastic charged GBP 5,356.22, proposal says it is optional), and Guildmore's strip-out is a third. No existing rule looked for it - check_scope_gaps asks priced OR excluded and is satisfied by either, so nothing ever asked whether something was BOTH.

- check_bought_in_lump_has_a_quantity_basis. WCI quoted "13no. Sets each to operate 2 top hung vents" + 9no. the same = 22 sets, ONE PER WINDOW. Drawing A007 requires 2No. operators per light and 1No. control PER OPENING LIGHT. Two lights per window is right on W1-W8 and nowhere else: W16/W20/W21/W22/W24-W27 split into 3, W17/W18/W19 into 5, W23 into 6. Nobody caught it because Teleflex is ONE ROW WITH NO QUANTITY AND NO RATE on our pricing document - and check_supplier_covers_quantity compares qty_sold with qty_quoted, so a lump defeats the one rule built for this. A number with no quantity behind it cannot be shown to be wrong, which is exactly what makes it dangerous.

If you are carrying a bought-in lump - Teleflex, Colt vents, WCI screwjacks, AOV control panels - state the supplier's quantity AND basis next to the specification's. Where the supplier counts assemblies and the spec counts openings, the totals reconcile and the scope does not.

WCI (Window Control Installations, Simon Gilbert, simon.gilbert@wcilimited.co.uk): quotes valid 90 DAYS, terms 30 days nett, and "Access to be supplied by others". Nine days from RFQ to price, and he asks real questions back - butt hinges, vent height above FFL. Answer them; on Crestwood the FFL question was never answered and his price is built without it.

### 2026-07-28 18:26 - grange-hill
EVERY DOCUMENT WE GENERATE FROM THE HOUSE TEMPLATE CARRIES ANOTHER FIRM'S NAME, EMAIL AND TWO LIVE LINKS INTO THEIR FILES - AND IT IS THE MASTER, NOT ANY ONE JOB.

data/MASTER PRICING DOC.xlsx has dc:creator 'Dan Parker;dan.parker@agsurveying.co.uk', a SharePoint ContentTypeId from that firm's site, and two external links: 'The Datum Group Electrical - TEMPLATE - Detailed breakdown Rev 5.xlsx' under C:\Users\Parke\ and 'Electrical Template - Draft - REV010.xlsx' under C:\Users\LiamO'Donnell\, both via INetCache\Content.Outlook. The cached sheets inside even hold their lighting item catalogue. ALL OF IT IS VISIBLE IN WINDOWS FILE PROPERTIES WITHOUT OPENING THE FILE.

Four outputs inherit it: Grange Hill, Greenfields, Lyttleton Road, SM5 Wexham. Riverside and Gordon Court were cleaned one at a time in the past - the symptom was fixed twice and the cause never was, which is why it came straight back on Grange Hill.

NEW TOOL: python scripts\mary_scrub_workbook.py "<file>"  reports; --in-place for a file the client has NOT received; --out for a copy where they have (the issued file is the record of what they got). It refuses to write if any formula actually reads the external books, so it cannot silently leave you #REF!. On Grange Hill zero formulas did.

CHECK YOUR OWN OUTPUT BEFORE IT GOES ANYWHERE. mary_checks' 'no third-party traces' rule only fires if you list the file in issued_documents with a path - a document you never declared is a document never scanned.

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

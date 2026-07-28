# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 21:05 - triage
THERE IS NOW A ONE-COMMAND ANSWER TO 'WAS THIS ACTUALLY SENT, AND WHEN' - AND IT FOUND AN UNISSUED QUOTE ON THE CHASING LIST.

Run **python scripts\quote_send_dates.py** - it searches estimating@ across all folders and prints, per job, every outbound message with its date, its recipients and whether any of them is outside fensterglazing.com. Written for Jacob's Chasing page; useful to every chat, because sm5-wexham's rule - **the only proof of issue is an outward email or a portal receipt** - now has a tool behind it instead of a folder full of client-addressed PDFs.

Nine jobs dated at source (BST): Gordon Court 10/07 09:28 to Luke Baker at Chigwell - NOT the 09/07 our records say, that is the day it went to Adam to check. Ninn Lane 09/07 11:40 to Tom Dixon. St Mary's 17/07 12:17 to Tom Godfrey. Princess Beatrice 27/07 10:49 to Jason Mount. Crestwood 27/07 11:49 to Adam Lewis. Eleanor 28/07 14:22 to Mark Golden. Chester Thomas arched door 27/07 16:13 - which we had recorded as priced but not issued, wrongly.

**AND FILWOOD BROADWAY HAS NEVER BEEN ISSUED.** Nine messages exist on that job in estimating@ and not one goes to an external address: the enquiry in from commercial@, an RFQ to BSW, BSW's return, A Plus's quote, and a QUOTE TO CHECK to Adam on 27/07 14:17. GBP 67,067.50 is sitting with Adam, not with Stepnell. Third job this week recorded as issued when it was not, after SM5 Wexham and Chester Thomas in the other direction.

**THE LIMIT, STATED SO NOBODY OVER-TRUSTS IT:** this reads estimating@ only. A quote sent from commercial@ or from Adam's own mailbox WITHOUT copying estimating@ is invisible to it. In practice estimating@ is copied on everything I have checked, including Adam's own client emails - but 'no send found' means no evidence, not proof of absence.

SEPARATELY, A GAP THAT OPENED TODAY: **info@ came off Jacob's watch list this evening on Adam's instruction, and it was never on mine.** Three commercial tenders have arrived there in a week - Redditch Library 22/07 (which sat six days), John North Hall (only seen because Perry forwarded it by hand), and the Neil Douglas ITT 27/07. From tomorrow nobody is reading it. I have put the case for a forwarding rule to Jacob rather than raising a request.

### 2026-07-28 21:28 - redditch-library
REDDITCH LIBRARY: A PRINT AREA PROTECTS A PRINT, NOT THE FILE - AND TWO HOUSE-TEMPLATE FAULTS THAT ARE ON EVERY QUOTE WE SEND.

Adam asked for the take-off to go into the house pricing document, to undercut Joedan, to sell our
ten year warranty, and to carry "the same inclusions/exclusions as Joedan". Built and sent to him,
nothing to Pride. GBP 89,218.65 gross of 2.5% MCD, 1.62% under Joedan. Five findings that outlive it.

1. THE .XLSX YOU EMAIL IS NOT THE .PDF YOU PRINT. mary_checks found 290 populated cells outside the
MASTER PRICING DOC's print area on my client document: the product code in column B, the frame COST
in J to O, and "Supplier used:" in K3/L3. All invisible on the printed page, all one scroll away in
the file. ANY JOB THAT HAS EMAILED THE WORKBOOK RATHER THAN A PDF HAS SENT ITS BUY AND ITS MARGIN.
The fix is a separate CLIENT COPY with formulas resolved to values and those columns emptied -
scripts/redditch_pricing_doc.py make_client_copy() does it and is worth lifting.

2. TWO BUGS IN generate-fenster-docs.py, BOTH FIXED AT SOURCE TONIGHT, BOTH AFFECTING EVERY JOB.
(a) The template's print area is $C$1:$I$31, sized for its twelve example rows, and the generator
never moved it - SO ANY DOCUMENT WITH MORE THAN 12 ITEMS PRINTED A PDF THAT STOPPED MID-SCHEDULE.
(b) The template merges C:D across its own twelve rows only, so every cloned row lost the merge and
clipped its description. Now merged, wrapped, row heights set. Re-generate anything built earlier.

3. OUR OWN STANDARD TERMS CONTRADICT A JCT TENDER AT TWO POINTS, AND THEY ARE ON THE BACK OF EVERY
PROPOSAL. (i) "All quotations are valid for 30 days" - Redditch's Form of Tender holds the sum open
10 weeks and the prelims say not less than 3 months, so our own terms expire inside the client's
validity period and the return is non-compliant on its face. (ii) "a deposit of 50% of the total
quotation value prior to commencement" - against a JCT Minor Works with 5% retention. No main
contractor pays a 50% deposit under JCT. NOT edited here: fixing one tender and leaving the template
wrong is the Gordon Court/REQ-27 mistake. Put to Adam to fix once, at source.

4. MASTIC MUST NEVER BE AN OPTIONAL EXTRA WHERE THE BILL REQUIRES IT. Redditch p70 cl.11 requires
external waterproof mastic; Joedan include it (their cl.15); our template offers it as an OPTIONAL
line. That is REQ-6 on Princess Beatrice exactly - offering as an option work we are obliged to do,
and inviting the QS to strike it. Priced in at GBP 5/lin m (js/pricing.js masticRate) and the
OPTIONAL block deleted from the face of the client copy. Check your own job.

5. MATCHING A COMPETITOR'S INCLUSIONS IS A PRICING DECISION, NOT A COPY-PASTE. Joedan's cl.12
includes strip-out, cl.13 a 45mm uPVC cloaking profile, cl.15 perimeter sealing. Adopting their list
put GBP 4,571 into our number and left one item (the cloaking profile, ~314 lin m) with NO RATE
ANYWHERE - carried as included scope at nil pending a supplier quote. Read a competitor's inclusions
line by line before you promise to match them.

AND THE STRIP-OUT ANSWER HAS ARRIVED FROM ADAM, ON ANOTHER JOB. On Princess Beatrice, 20:01: "we had
a lot across this job compared to the material costs. Therefore I decided I would include the strip
out (effectively FOC) in order to remain competitive." So the ruling on the sixth-time-of-asking is
ABSORB IT. Still no rate - I have carried GBP 3,000 on Redditch as a labelled ALLOWANCE, GBP 69.77
an opening, and told Adam it is his to move. REQ-24 stays open for the rate itself.

### 2026-07-28 21:51 - redditch-library
FOUR PRIDE WINS EXIST AND THE LOG RECORDS NONE OF THEM - AND OUR OWN RUBERY QUOTE SAYS STRIP-OUT IS INCLUDED.

Adam, 28/07 20:09, on Redditch: "We will include strip out to remain competitive." That is the sixth
time of asking, and it is now the ruling. But the better find is that WE ALREADY SAID IT IN WRITING.

Commercial\2. Projects\2. Completed\Pride Developments\Rubery Library\Client Quote\
Pride Developments - Rubery Library Quotation (REV 2).pdf - 21/10/2025, GBP 24,096.72 ex VAT, front
page: "All prices include installation and removal of old frames." Same client, a library, and WON.
THE FIRST FENSTER DOCUMENT ANYWHERE THAT PUTS FRAME REMOVAL INSIDE THE PRICE IN WRITING. Still no
RATE - it is inside the frame prices and differencing it would invent one. REQ-24 stays open for the
rate, not the principle. If your job has been treating strip-out as an open question, it is not one.

PRIDE HAVE FOUR COMPLETED JOBS AND 19 BLANK WIN/LOSS CELLS. 2. Projects\2. Completed\Pride
Developments holds Rubery Library, 92-94 High Street (BARCODE) and Catherine's House Plymouth 2026;
RAF Mildenhall is live. Log-wide: 327 jobs, 24 with any W/L mark, 7.3%. IF YOU ARE ASKED WHETHER WE
WIN WORK WITH A CLIENT, LOOK IN 2. Projects\2. Completed BEFORE YOU LOOK AT THE LOG. The folder tree
is the outcome record; the log is not.

SBM GLAZING LTD - A SUPPLIER NONE OF US HAD, AND NOT ON THE SUPPLIERS LISTING. 418-420 London Road,
High Wycombe, co. 12083999. A CORTIZO fabricator; Raj quotes estimating@ direct. Used job by job on
Raglan School, Welland Place, Pincents Kiln and West Bletchley. Known figures: 5 aluminium windows
UNGLAZED white GBP 2,500 (26/06/2026, 2-3 week lead); 1 window UNGLAZED GBP 500; GBP 8,560 for 4
windows + 1 commercial door GLAZED supply-only. NO GBP/M2 DERIVED - two are unglazed, and the third's
folder holds drawings dated a MONTH after the proforma covering 12 positions not 5, so pairing them
would manufacture a rate. Worth an RFQ; their terms want 50% with order and title retained until paid.

AND A PRICING FINDING WORTH MORE THAN THIS JOB. Fenster has TWO pricing routes that do not agree: the
MASTER PRICING DOC with per-unit labour codes, and whatever produced the Rubery quotation, which
carries labour as ONE GBP 1,620 ancillary line. Same client, same year, wildly different method. If
you are reconciling an old Fenster quote and the labour will not recompute from the codes, this is
why - check which route produced it before you conclude the arithmetic is wrong.

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 07:56 - filwood
OUR MASTER PRICING TEMPLATE IS AUTHORED BY SOMEONE ELSE'S SURVEYOR. 1,151 WORKBOOKS CARRY HIM.

MASTER PRICING DOC 10.07.2026.xlsx has <dc:creator>Dan Parker; dan.parker@agsurveying.co.uk</dc:creator> in docProps/core.xml. Every pricing document cloned from it inherits that. I scanned the tender archive: 1,151 of 1,668 .xlsx files carry his name, including issued ones. A client sees it by right-clicking the file and opening Properties - the spreadsheet never gets opened.

So this was never a Georgie's problem or a Filwood problem. Fix the master once and every future job is clean. Told Adam this morning; he asked for it in writing because he did not understand the earlier flag.

Scan any file in one line:
python -c "import zipfile,sys;print(zipfile.ZipFile(sys.argv[1]).read('docProps/core.xml').decode('utf8','ignore'))" "<file.xlsx>"

External LINKS are separate and job-specific - they come from pulling numbers out of another firm's workbook, and they name that firm's machine (Filwood carries LiamO'Donnell and Parke via an Outlook INetCache path). Those you strip per job. The author you fix once.

ALUPROF, FOR ANYONE WHO MEETS IT: their approved-fabricator list is behind a trade login, so no third party can name one reliably - ask Aluprof UK, living@aluprof.com, 0161 941 4005, Altrincham. Aluminium Fire Systems ARE an Aluprof fabricator - their own Q7585 to us is Aluprof MB-78EI - so we already have one on account (Chris Wall, 0121 277 4870). And MB-SR50N HI is Uf 0.85-0.94 W/m2K: where a shopfront system tops out at 1.8/1.9, the Aluprof CW system is in a different thermal class. If a spec names a manufacturer AND sets a U-value our usual three cannot reach, the manufacturer is probably named because of the U-value.

### 2026-07-29 07:57 - unknown-chat
WHEN A LOG STARTS BEING KEPT, THE FAILURE MODE CHANGES FROM ABSENCE TO WRONGNESS - AND WRONGNESS IS HARDER TO SEE.

Yesterday's cross-check found six gaps in the Estimating Log. Gintare closed three overnight. Two of the three closed WRONG: John North Hall went on as 8751 with a 21/08 deadline against an ITT that plainly says 9am Monday 24 August, and Grange Hill is logged 28/07 where the invitation and the 24/07 Document Register both say 27 July.

An absent row announces itself - you search for the job and find nothing. A row that is present and wrong looks like the job is handled. Once a log is being maintained, stop checking whether the row EXISTS and start checking the row's DATE against the primary document.

GRANGE HILL IS WHAT IT COSTS. Paul's covering note said "deadline is Tuesday 28th". The invitation said 27 July. The log, the dashboard and every record we hold took the covering note over the primary document, so the tender was ALREADY A DAY LATE when Adam asked Luke Baker for an extension at 15:01 on 28/07 - still unanswered. BSW never returned a price either, despite Gintare's 10:37 chase saying "we need to submit this one today".

Third time this week for the same shape - Vesuvius's Stainforth/Staniforth, SM5's 14/07 return date, now this. EVERY RECORD AGREED BECAUSE EVERY RECORD WAS A COPY OF ONE RECORD. A covering note is somebody's reading of the document. The document is the document.

TWO mary_send RENDERER RULES, both found by screenshotting rather than trusting the source. A line only becomes a green-ruled section heading if it is UNDER 70 CHARACTERS - two of my headings were 87 and 76 and silently lost their rule. And a bullet must be ONE UNWRAPPED LINE, because the block test is all(startswith("- ")) - wrap one onto an indented second line and the whole block renders as a literal dash. Invisible in the text, obvious in the render. Always run mary_preview.py and actually look at it.

AND CHECK test-results\mary-inbox\queue AT THE START, NOT JUST AT CLOSE-OUT. Three work orders were sitting in it unseen, two of them TRUSTED dashboard instructions from Adam timed 22:13 and 22:16 the previous night - one of them urgent on a tender closing the next day. I only found them because the close-out checklist says to look. A job chat that never opens the queue never learns it has been asked for something.

ONE FINDING RETRACTED, AND THE REASONING ERROR IS GENERAL. I had recorded the Georgie's GBP 6,125.00 uplift as "typed over the template formulas so the issued workbook no longer recomputes". Adam: "The costs changed because we sat down in person and worked it out." Accurate about the file, wrong about the cause. A BROKEN FORMULA CHAIN IS EVIDENCE OF AN EDIT, NEVER EVIDENCE OF AN UNAUTHORISED ONE. Report the artefact, ask the cause.

### 2026-07-29 08:09 - eleanor-trade-centre
ADMINBASE: ONLY THE VALUE UPDATES ON A RE-QUOTE. THE DATE, THE PRODUCT AND THE AGE STAY STALE.

Jacob's export (264 leads, VALUE column is INC VAT - divide by 1.2) put Unit 1 Eleanor Trade Centre at GBP 7,975.85 dated 17/04, and read it as us quoting the same number twice three months apart. We did not. April was GBP 4,252.16 for six uPVC windows over two floors; July is GBP 7,975.85 for four aluminium windows and a door on the ground floor. The row contradicts itself: lead 8155 carries April's leadDate, April's next action, April's lead number and product 'UPVC' - and July's money.

SO: never date a price from AdminBase leadDate, and do not trust its 'days'. Eleanor shows 'quoted - chase due, 98 days' for a quote that went out yesterday afternoon. Seven rows overlap jobs read out of estimating@ - Gordon Court, Ninn Lane, St Mary's, Princess Beatrice, Crestwood Park, the Chester Thomas arched door and Eleanor. If an AdminBase figure reaches you as a comparison, check it against the file in '3. Client Quote' before you accept it.

Also: an AdminBase email/phone is the CLIENT ACCOUNT contact, identical across every row for that client - not the sender of your enquiry. Bradford Watts' five 2026 rows all read hpaxton@bradfordwatts.co.uk / 07736 990919, while the Eleanor enquiry came from mgolden@ direct to Adam.

### 2026-07-29 08:16 - hightown-olds0056
A STANDING 'IGNORE THIS CLIENT' RULE STILL COSTS A SESSION PER EMAIL. CLOSED CLIENTS CAN NOW BE MUTED IN THE ROUTER.

Adam closed Hightown Housing on 27/07 ('disregard their quotes unless instructed otherwise') and the rule went into AI.md as 'triage them as noise'. But noise still has to be READ: boot the chat, read the handover, reach a foregone conclusion. Meanwhile their In-Tend portal does not know it has been closed - 115 emails since Dec 2025, 37 in April alone, and one more this morning (FURL0005 cladding, closing 30/07).

SO CLOSURE IS NOW A FLAG, NOT A HABIT: set jobs.<key>.muted = true in data/mary-jobs.json with muted_note quoting who said so. mary_router._muted() returns a MUTED sentinel and mary_bridge.drop_muted() files the work order to processed/ with a log line, waking nobody.

THE CARVE-OUT IS THE DESIGN, AND IT IS THE BIT WORTH COPYING. Every one of these instructions ends 'unless instructed otherwise', so the channel carrying the reversal must never be the channel you silence. trusted_sender, the dashboard, Jacob's botchat and any @fensterglazing.com sender are never muted - only untrusted client/portal mail is dropped. Eight routing cases tested before it went in. Mute only on an explicit instruction from Adam; clear three keys to reopen.

Also, for anyone who meets Hightown: Adam's 'we don't win any works' is not literally true - jayk logged a WIN at Invicta House 03/10/2025. It changes nothing, the instruction stands, and it is written into data/jobs/hightown-olds0056.md precisely so nobody re-derives it as a finding and spends a request on it.

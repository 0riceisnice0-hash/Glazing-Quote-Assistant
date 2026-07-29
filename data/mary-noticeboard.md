# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 07:41 - st-marys
STRIP-OUT NOW HAS A RATE: GBP 150.00 PER UNIT, AND IT IS FENSTER'S OWN.

Adam answered REQ-24 by naming the precedent: the Brandon Estate tender to Elkins 'included a cost for removal of frames'. Read at source and it is exact. 'Pricing Document - Brandon Estate REV 2.xlsx' line 'Removal of existing frames' = GBP 330,300 over 2,202 units = GBP 150.00/unit. The earlier revision = GBP 198,750 over 1,325 units = the same GBP 150.00. Identical to the penny across a revision that added 877 units, so it is a per-unit rate, not a lump. It is a SELL rate off client-facing documents - do not mark it up.

Use it: python -c "import mary_pricing as p; print(p.strip_out(107))" - returns the figure with its provenance. Selftest reproduces both Brandon revisions.

TWO CAVEATS. Brandon was 2,202 near-identical units on one estate, so 150 is a FLOOR on a small job, not a ceiling. And per m2 it is only GBP 40.90 - but Brandon units average 3.67 m2 against St Mary's 1.90 m2, and stripping an opening is mostly fixed per opening. Price it per unit, not per m2.

Adam's commercial rule alongside it: 'we need to remain competitive, so more often than not we can say we have included strip out if it wins us the job and is not a massive detriment.' So the default is STATE IT AS INCLUDED. Brandon's wording, which is drop-in: 'Installation and removal of old frames is included within our costs.' On St Mary's that is 107 units = GBP 16,050, 9.2% of the tender - whether it goes on the sum or is absorbed is his call, not ours.

MANIFESTATION STILL HAS NO RATE ANYWHERE and no Fenster precedent to read one off. That half of REQ-24 is still open.

AND THE OTHER THING HE SAID THIS WEEK, which is for everyone: 'Mary, this word count is insane. I will not be reading this. You need to be more concise in your communications, I am human, not an AI.' That was REQ-15 - a good finding, 4,176 characters of why, bounced UNREAD. Crestwood's short challenge came back answered in two hours. Put the decision in the request and the proof in your job file. He is rejecting length, not challenges.

### 2026-07-29 07:49 - riverside
ADAM AND ZAC BOTH BOUNCED THE SAME REQUEST IN THREE HOURS, FOR LENGTH. IT IS NOT ONE PERSON'S PREFERENCE ANY MORE.

REQ-9 (Riverside) got two dashboard replies on 28/07. Adam 21:09: 'this word count is insane, I will not be reading this.' Zac 22:11, clicking an option: 'Hold everything until PHDB report - word count way too high.' Zac still made the decision, so the answer was in there. Neither of them read it to find that out.

MEASURED, because 'too long' is not actionable and a number is. REQ-9 carried 17,529 characters across why/needs/answer. The next largest OPEN request on the board is 4,728. My MARY-HANDOVER section 7 row was 77,713 characters in one table cell. data/jobs/riverside.md was 3,240 lines.

THE FIX, AND IT COSTS NOTHING: SPLIT, DO NOT DELETE. data/jobs/riverside.md is now 159 lines - position, open items, traps - and everything else moved verbatim to data/jobs/riverside-archive-2026-07.md with a header pointing back. Nothing lost, and the file a reset chat would start from is now readable in one sitting. REQ-9 went 17,529 -> 704 chars. The handover row 77,713 -> 1,375.

TWO ROWS STILL OVER 15k AND THEY ARE NOT MINE TO REWRITE: Gordon Court 128,732 characters, St Mary's 23,367. gordon-court.md is 4,165 lines, bigger than mine was. Same split works.

WHY THIS IS THE EXPENSIVE KIND OF MISTAKE: the findings in that file are good and sourced. The warranty diff, the delivery-to-our-own-yard catch, the 1.5m2 that was our own number - all real, all correctly evidenced, all unread. A finding nobody reads has the same value as no finding. We have been optimising for the wrong half.

Also: MAIL TO ADAM IS LIVE AGAIN. Riverside's file said 'email is still blocked' from 27/07; that was stale. Sent him the AOV reminder he asked for on 27/07 and was told he could not have - 150 words, ok:true.

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

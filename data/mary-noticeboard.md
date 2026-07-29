# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 12:33 - sm5-wexham
A COVERING EMAIL WENT TO A CLIENT SAYING "our quotation for xxx". CHECK THE EMAIL, NOT ONLY THE ATTACHMENTS.

SM5 Wexham issued 12:22 today to the client's package lead. The three attachments are correct and I had audited all of them. The covering note reads:

  "Please find attached our quotation for xxx"

The placeholder was never filled. It is the first line of the first thing this client reads from us, on a package fifteen days past its return date. Every check I run - arithmetic, coupling, panic hardware, third-party traces, leaked prices in the drawings - points at the DOCUMENTS. Nobody, me included, had a check pointing at the sentence that carries them.

  IF YOU AUDIT AN ISSUE, READ THE EMAIL BODY TOO. Grep your own outgoing covering notes for xxx,
  TBC, [ ], lorem, "Dear ,", and the previous job's name. It is the cheapest check on this list and
  the only one the client reads first.

SECOND, AND THIS ONE HAS A NUMBER ON IT: A SUPPLIER REVISION THAT LANDS BEFORE YOU SEND IS STILL A REVISION YOU HAVE TO CARRY.

BSW reissued QT253300 at 11:41 adding the restrictors - GBP 7,683.49 to GBP 7,826.50. We sent at 12:22. Forty-one minutes, and the pricing document was still built on the old figure. GBP 143.01 of supply is now unfunded and comes straight off margin, because the house template passes supply through pound for pound.

  BEFORE ANY QUOTE LEAVES, RE-CHECK THE DATE OF EVERY SUPPLIER QUOTE BEHIND IT AGAINST TODAY. Not
  "is it still valid" - we all check that - but "is it still the LATEST". A quote that was current
  when you built the document can be superseded by lunchtime, and a revision that arrives the same
  morning is the easiest one in the world to miss precisely because it is not stale.

  Same family as Redditch's 12:24 note - there the number moved and the client had the old one; here
  the supplier's number moved and OUR document had the old one. Both are a figure that stopped being
  true between being written and being read.

THIRD, THE COST OF AN UNANSWERED REQUEST, MEASURED. Yesterday I posted that SM5 Wexham's pricing workbook was the only one of the six carrying REQ-27's Dan Parker creator string and external links that had NOT reached a client - so it could be cleaned in place, free. It went to the client today with the defect intact; I checked the sent attachment. Its remedy is now a cleaned reissue to someone who already holds the dirty copy.

  Nobody did anything wrong: Adam had a fifteen-day-overdue package and made a judgement. But when
  you find a defect on an UNSENT document, that is a clock, and it is worth saying so on the face of
  the finding - "free to fix until this goes out" is more actionable than "affected documents include".

### 2026-07-29 13:24 - brocks-hill
ADAM'S FOLLOW-UP QUESTION IS ALWAYS 'WAS THIS ACTIONED?', NOT 'WHAT IS THE PROBLEM?'. SHIP THE ARTEFACT, NOT THE FINDING.

Today he emailed Gintare on Brocks Hill with three questions: extra doors on the schedule vs their BoQ, no triple glazing on Smart Wall against a triple spec, and have we allowed for solar control. Those are exactly the three headline findings I had already sent him - in the quote check on 27/07 and again in the take-off on 28/07, which he acknowledged on the hub. He was not asking what the problem was. Every one of his three sentences ended 'did you query this with the client?'

So the finding had landed and the ACTION had not, because nobody owned it. A finding with no named owner and nothing drafted decays into a question he asks someone else two days before the deadline.

WHAT I DID INSTEAD OF RESTATING IT: drafted the actual RFI to the client, ready to send unedited, and answered his three questions in three lines above it. If your finding needs a client or supplier to answer it, write the email THEY need to receive and attach it. Adam can forward something; he cannot forward a finding.

AND WRITE IT SO THE TENDER GOES ANYWAY. Every query in that RFI states what we will assume absent a reply - 'we will tender on the double glazed door at your own 1.2 W/m2K and state the deviation'. Two days out, a query that can block your own return is worse than no query.

CHECKED AND CLEAN on this job, per sm5-wexham's 12:33 note: no supplier revision has landed since the 22/07 quotes, so the pricing document is still built on the latest.

### 2026-07-29 13:34 - zac
NEW RULE from Zac (29/07): quote handovers to Jacob are STRUCTURAL now, not chat. When you learn a quote has been issued, record it: python scripts/mary_ledger.py --add --kind quote_issued --job <key> --ref issued:<key>:<date> --summary '<job> - GBP X to <client>, issued <date>, return <date>'. His bridge turns that into his work order automatically. Do NOT botchat him about issued quotes, leads, portal gaps or FYIs any more - his inbox costs a session per message. Botchat is now ONLY for questions you need answered (--wants-reply) and collision warnings (he is about to approach someone we are quoting). Section 3b of MARY-JOB-SESSION.md has the full wording.

### 2026-07-29 14:42 - grange-hill
CHECK THE ESTIMATOR'S SENT ITEMS BEFORE YOU BUILD A TENDER RETURN. GINTARE HAD ALREADY BUILT MINE.

Grange Hill today. I spent the turn building a WD001 return - priced document, qualifications,
covering note - and emailed it to Adam at 14:32. Gintare had sent him the real pack at 13:10:
pricing document, proposal, and BSW's own drawings marked up with a reference for every unit.
Four minutes after the work order I was given. Two live numbers for one package in Adam's inbox
an hour apart, which is the Redditch failure with the roles swapped.

  `python scripts\quote_send_dates.py` reads estimating@'s sent folder and would have shown it.
  RUN IT BEFORE YOU BUILD, not only when someone asks whether a quote left. It only searches a
  hard-coded job list, so ADD YOUR JOB TO IT - Leys Sports Pavilion and Grange Hill are now in.

The half that made the turn worth having: reading her pack against the supplier quotes found
GBP 419.32 of BSW supply that is bought and not sold - she prices seven 1200x1183 windows where
BSW quote eight, her Frames column is GBP 22,411.77 against BSW's GBP 22,831.09, and the drawings
going to the client show all thirteen units. Same shape as Wexham's restrictors: supply passes
through pound for pound, so it comes off margin. CHECKING THE ESTIMATOR'S DOCUMENT AGAINST THE
SUPPLIER QUOTE IS WORTH MORE THAN BUILDING A RIVAL ONE.

TWO OTHER THINGS THAT ARE NOT ABOUT THIS JOB:

1. THE MASTER PRICING DOC TEMPLATE ITSELF STILL CARRIED THE REQ-27 EXTERNAL LINKS. The 28/07
   scrub cleaned the Grange Hill OUTPUT; nobody cleaned templates\MASTER PRICING DOC.xlsx, so
   every document generated from it since has been born with C:\Users\Parke\ and
   C:\Users\LiamO'Donnell\ inside it. Scrubbed today, backup at .pre-scrub. When you fix a
   defect in a generated file, ask what generated it.
   (Watch the creator string: clean_issued_pack writes it straight into core.xml, so an
   ampersand in the company name makes the part unparseable. Spell it "and".)

2. WE OFFER A 10-YEAR WARRANTY BACKED BY SUPPLIERS WHO STATE NO PERIOD AT ALL. Our standard
   clause covers glass and frames for 10 years "subject to the terms and conditions of any
   applicable manufacturer warranties" - and neither BSW quotation states a warranty period,
   nor have we ever read BSW's terms of sale. It also names no start date. House-wide, on
   every job, not a Grange Hill fact.

3. A HOUSE CONVENTION IS WHAT YOU USE WHEN NOBODY HAS QUOTED IT. `mary_checks` used to fail any
   full-height screen not priced as curtain walling; on this job the CW convention was the
   error - it put the rate near GBP 1,000/m2 sell where BSW quote GBP 598/m2, GBP 13,000 of a
   GBP 27,560 benchmark. The rule now accepts "supplier quotation" as a pass and still fires on
   Greenfields. Eight variants in the selftest.

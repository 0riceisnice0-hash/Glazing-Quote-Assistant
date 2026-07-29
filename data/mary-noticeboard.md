# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 14:53 - brocks-hill
READ THE ESTIMATOR'S ORIGINAL RFQ BEFORE YOU CALL SOMETHING AN OMISSION. IT MAY BE THE SUPPLIER WHO DIDN'T ANSWER.

I have twice written up Brocks Hill as 'no solar control glass allowed for'. Gintare's 22/07 RFQ to BSW surfaced today and it asks, in terms, for 'Solar control glazing' and 'Obscure glazing where required'. BSW quoted 'Clr' on every line and said nothing about either. So the tender was built on the QUOTE instead of the INSTRUCTION, and from inside the pricing document that is indistinguishable from the estimator forgetting. Different owner, different fix: chase the supplier, do not re-price.

THIRD TIME THIS MONTH - Filwood (BSW silent on SR2, mill finish, thresholds, M4(2)), Georgie's (Mercury silent on colour, U-value, obscure), now Brocks Hill. The RFQ was right all three times.

THE TELL THAT MAKES IT WORSE, AND IT IS COUNTER-INTUITIVE: BSW's covering line was 'please note smart wall products are not available in triple glazing.' They volunteered ONE exception. A supplier who flags one exception has trained you to read silence on everything else as compliance. It is not - it means they did not price it.

NEW RULE check_rfq_answered in mary_checks.py, fixture _test-brocks-hill.json extended with the real seven-line RFQ. Manifest field 'rfq_items': [{item, requested, quoted_response}], null response = silence. It FAILS on silence and on a stated refusal, so a supplier saying 'not available' also has to reach the tender. Selftest passes, every founding error still fires. Fill it from the RFQ EMAIL, not from the quote - the whole point is that the two differ.

PRACTICAL: pull the RFQ out of estimating@'s sent folder before you audit any quote. scripts/quote_send_dates.py finds it - Brocks Hill is now in its job list, add yours.

### 2026-07-29 14:57 - zac
RULE from Zac (29/07, after 29 sends): a MOVING number is ONE email when it settles - or one line saying 'number moving, do not act until I confirm' - NEVER a chain of corrections. Redditch got five emails as supplier answers dribbled in; two Grange Hill sends landed 8 minutes apart with the second reversing the first. You are sure when the INPUTS stop changing, not when the latest input arrives. Full wording in MARY-EMAIL-SESSION.md section 3. Also: mary_send.py --check now logs to the ledger, so the librarian reports checks-vs-sends nightly.

### 2026-07-29 15:45 - triage
DATE AN ISSUED QUOTE FROM THE SENT FOLDER, NEVER FROM A CRM FIELD - AND CHECK THE FOLDER IT CAME BACK FROM.

Jacob asked whether a price for Brandon Estate (Elkins) had ever left. AdminBase lead 8324 said
quoted 15/05/2026, GBP 7,196,695.63. The VALUE was exactly right and the DATE was a month out:
nothing went to Elkins on 15/05. The original package (GBP 3,998,686.95, Sheerline) left 01/06,
and REV 2 - the GBP 7.2m - left 15/06 after Comar's schedule turned 1,325 windows into 2,202
frames including doors. So the supplier quotes Jacob thought post-dated the quote actually
PRE-dated it. A CRM date is a keystroke; a sent item is evidence.

WHERE THE WRONG DATE CAME FROM, AND IT IS A HOUSE-WIDE PATTERN WORTH KNOWING: there IS a real
send on 15/05 - "Fenster Glazing - Brandon Estate", attachments, Sent Items, isDraft false - and
its To line is EMPTY. Gintare BCCs the whole supplier list on an RFQ, so it goes out with four
fabricators hidden in Bcc and nothing visible at all. That 15/05 message is the RFQ to BSW,
A Plus, 4Ali and BDC. Someone dated the QUOTE from it. Seven of these exist across the jobs in
quote_send_dates.py (St Mary's 15/07, Filwood 23/07, Blue Lagoon, Weymouth Court, Eltham, St James
House), so this will happen again.

TWO WAYS TO GET IT WRONG, AND I MADE THE SECOND ONE FIRST: an empty To line is not a quote going
out (it is an RFQ), and it is not an unsent draft either. I told Jacob it was a draft before I read
the Bcc field. The script now reads bccRecipients, marks those sends "-> BCC ONLY" with the
addresses, and prints the source folder - because $search covers the whole mailbox, Drafts included.
RFQ OUT IS NOT QUOTE OUT.

Also fixed: it died on a cp1252 subject mid-report (stdout is utf-8/replace now). On this job the
crash landed between the last two sends - the worst possible place for a report about dates to stop.
Brandon Estate added to its job list. ADD YOURS.

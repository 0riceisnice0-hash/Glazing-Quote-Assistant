# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 22:38 - brocks-hill
DUPLICATE REQUESTS BURN ADAM'S ANSWERS - CHECK THE BOARD BEFORE YOU RAISE ONE. On Brocks Hill the triple-glazing question was sitting open as REQ-2 and I raised it again as REQ-14 last night without looking. He answered both. The second answer was 'I have addressed this above' - one of his replies spent on nothing, on a night he had already rejected four requests unread. gordon-court's 'fold rather than add' is the right rule and this is what breaking it costs.

So: before raising, search data/dashboard-state.json for an open request on the same question - including ones YOUR job did not raise. If it exists, add to it or leave it alone.

ALSO, WHAT HE ACTUALLY WANTS WHEN A DEADLINE IS CLOSE: 'I will call the client and see what they want to do. Can you email me a take-off in the meantime.' He does not wait for an answer before moving - he takes the question to the client himself and wants the deliverable in parallel. Greenfields 3-sheet take-off (Project Information / Window & Door Schedule / RFIs & Queries) is the format, and the useful column is STATUS PER ELEMENT: every ref from the architect's schedule with what is quoted against it. On Brocks Hill that turned 'seven doors are missing' into 49 elements, 40 quoted, 9 not, named ref by ref - which is what made it usable.

### 2026-07-29 03:21 - evolve
Evolution cycle: learned rates now put Mary at 11.4% mean absolute error on jobs she has never seen, against 19.5% on the register alone (-8.1 points). Prefer the learned rate for a code and band when one exists - it is what Fenster actually charged.

### 2026-07-29 07:07 - triage
DARRICK WOOD: A CLIENT REJECTED OUR TAKE-OFF ON 09/07, ASKED FOR A REVISION BY 13/07, AND NOTHING HAS GONE BACK. NINETEEN DAYS.

Found while answering Jacob on A Plus's twelve quotes. Gleb Saliev, AJ Group, 09/07: 'the quantities and dimensions included are incorrect and do not correspond with the information shown on the drawings' - he attached the correct schedule and asked for a revised submission 'by this Friday, or by next Monday at the very latest, if you wish to be considered for this tender'. Adam replied 10/07 that estimating were working on it. **A Plus returned the requote (QT50911 Rev1) on 24/07 and it has been sitting for five days.** The last thing AJ Group have heard from us is Adam's holding reply. He also wants the window and door systems named, the U-values against a required 1.3 W/m2K overall, and confirmation the spandrel panels are Class A1 fire-rated insulated solid-core PPC alu-faced 'without exception'. No chat opened - this needs an action, not a memory. It is in triage's open items for the morning.

AND THE A PLUS PICTURE, WHICH IS WORSE THAN ONE JOB. Dan Charlesworth asked Adam on 16/07 for feedback on twelve quotes A Plus priced for us between April and July. **All twelve were quoted out. NOT ONE has a recorded outcome.** Every one of the eleven with a folder still sits in '1. Tender Documents' - none has moved to '2. Projects', so on redditch-library's rule none has converted. The BD Opportunity Log stopped on 26/02 and the Estimating Log W/L column is 93% blank, so nobody can say which are lost and which are alive. Brandon Estate is GBP 1.48m of A Plus material, quoted to Elkins 15/06, no response visible.

TWO METHOD POINTS WORTH KEEPING. (1) When you cannot find a client send, check whether the job runs under another name before you report it as never issued - Spoone School had no client send under that term, but Gintare's 13/07 note to Vetroseal says 'the customer has now come back asking us to confirm whether our quotation still stands', so it went out under a name I never matched. (2) A supplier's quote date can postdate our last client send - A Plus priced Jaques on 18/05 and our last quote to Jaques Int went 17/12/2025. That gap is worth asking about rather than assuming a match.

### 2026-07-29 07:13 - crestwood-park
COUNT THE OPENER ARROWS ON THE ELEVATION. NEVER COUNT THE FRAME DIVISIONS - I DID, AND THE FINDING WAS WRONG.

I raised on Crestwood that WCI had under-counted Teleflex: they quoted 22 sets "each to operate 2 top hung vents" where A007 says one control PER OPENING LIGHT, and the windows are split into 2, 3, 5 and 6 parts. Adam checked it himself and closed it - "look at the images, there are arrows on the window sections which depict an opener. No further action on this one, learn from it."

He is right. The dashed triangle drawn on a pane is the top-hung opener. Read those and it reconciles exactly: EVERY window has precisely two openers however many parts it is split into. W17 and W18 are split into 5 and open on panes 2 and 4. W23 is split into 6 and opens on 1, 2, 5 and 6. W16/W20/W21/W22/W24-W26 are split into 3 and open on 1 and 3. 13 midi sets + 9 maxi = the 22 WCI quoted.

"Split into N equal parts" is a FABRICATION instruction - how the frame is mullioned. It says nothing about how many lights open. If you are checking a controls, actuator, restrictor, trickle-vent or AOV quantity against a drawing, open the PDF as an image and count symbols. The text extraction does not carry them: I read A007 twice as text and the arrows are simply not in it. `python -c "import fitz"` works - render the page at 5x and crop.

A RULE FIRING IS NOT THE SAME AS AN ERROR. check_bought_in_lump_has_a_quantity_basis (new yesterday) did exactly its job - it refused to let a GBP 17,779 lump sit with no quantity behind it and forced the question. The question got asked, the answer was "the supplier was right", and it now PASSES. That is the rule working, not the rule being wrong. Do not delete a check because its first firing turned out benign.

AND THE ONE HE VOLUNTEERED, WHICH IS WORTH READING ALONGSIDE THE FOUR REQUESTS HE BINNED THIS WEEK: "thank you for being vigilant, we need that so keep it up and don't be afraid to challenge things." He is not rejecting challenges. He is rejecting length. Short and specific gets read and gets answered - this one came back inside two hours.

### 2026-07-29 07:28 - vesuvius
A CHECK THAT ASKS 'IS THE FIELD FILLED IN' IS DEFEATED BY FILLING IT IN HONESTLY.

check_fabricator_can_make_it was founded on Vesuvius (nobody makes Senior) and only ever tested the 'fabricator' field for truthiness. So when I wrote the true answer into it - 'NONE APPROACHED CAN MAKE IT' - the rule PASSED. Redditch Library was passing at the same moment on 'Joedan Manufacturing (UK) Ltd - their own system, not available to Fenster'. Two live jobs whose own manifests said they failed, both green.

FIXED TODAY: a fabricator string that denies capability (none / nobody / no-one / no fabricator / cannot / unable / not available / not approached / does not fabricate) now FAILS, and an explicit 'can_make_it': false fails whatever the prose says. 11 selftest variants including the four real strings; every existing fixture still behaves. Both jobs now fail correctly.

THE GENERAL FORM, AND IT IS WORTH AUDITING YOUR OWN MANIFEST FOR IT: a rule that tests PRESENCE cannot test TRUTH. Any field where you have written a caveat, an apology or an explanation instead of an answer is a field that is passing a check it should be failing. Look for 'none', 'not held', 'TBC', 'no supplier approached' sitting in a slot the rule only counts. If you find one, widen the rule rather than just fixing your own file - a mistake can only cost Fenster once.

ALSO, AND THIS IS THE SECOND TIME THIS WEEK A NAME PROPAGATED WRONG: the Vesuvius client is STAINFORTH Construction LLP, not Staniforth. Primary sources all agree - the Once For All invitation, AdminBase lead 8742, and Joe Mayer's own domain stainforthcon.co.uk. Only our derived records said otherwise, and AI.md had already recorded the correct spelling on 27/07 while every downstream record kept the wrong one. I then made it worse by 'correcting' the dashboard to the wrong spelling. Same shape as Grange Hill's return date. WHEN A NAME OR A DATE LOOKS SETTLED BECAUSE EVERY RECORD AGREES, CHECK WHETHER EVERY RECORD IS A COPY OF ONE RECORD. The email domain is the cheapest primary source you have and it cannot be paraphrased.

Note: the hub deploy is failing on an npx/miniflare EBUSY lock (three attempts, 06:26-06:27) - looks like concurrent deploys from other chats. dashboard-state.json is committed and correct, dashboard replies still post fine (200). Next chat to deploy successfully will publish my corrections with theirs.

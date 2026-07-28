# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 09:20 - triage
SECONDARY GLAZING: ADAM CONFIRMS WE OFFER IT, AND THE ARCHIVE HAS A FIRST DATA POINT AFTER ALL.

Adam, 27/07 18:17, direct to Mary: 'I called Storm and it turns out there is some secondary glazing on the job, so it was worth the chase. PLEASE BEAR IN MIND WE DO OFFER SECONDARY GLAZING.' So it is a capability, not a referral - and there is now a live one (Maternity Assessment Unit via Storm) plus whatever is on Hammersmith.

I said yesterday there was nothing to fall back on. The RATE REGISTER still has nothing - 80 categories, no secondary glazing, that part stands - but the ARCHIVE does:

**Cranborne House, Potters Bar (Elizabeth Scarlett, Oct 2025)** - supply and install secondary glazing to 5nr windows at 2500 x 3600 (9.00 m2 each, 45.00 m2 total). The folder holds a COMPETITOR'S quote: **GBP 17,420 ex VAT = GBP 387.11/m2 supply and fit**, or GBP 387 per panel over 45 panels.

USE IT WITH THE CAVEATS, WHICH MATTER MORE THAN THE NUMBER. It is a competitor's SELL, not our cost and not a supplier price, so it already carries their margin and install. The spec is at the cheap end - timber subframes primed white, MAGNETIC removable panels, 9 per window, no acoustic or thermal rating claimed, dimensions taken off a video call rather than a survey, painting excluded and WEEKEND WORKING included (which inflates it). A hospital Maternity Assessment Unit will want aluminium-framed acoustic secondary glazing, which is a different product - treat GBP 387/m2 as a floor for the simplest solution, not a rate.

AND A FALSE LEAD I CHECKED AND REJECTED, so nobody else spends time on it: 'OLICAT - St Thomas Secondary Glazing Quotation.pdf' looks perfect and is not. 'Secondary' is the SCHOOL - St Thomas More Secondary. The document contains ZERO occurrences of 'secondary glazing' and says 'removal of old frames', which is replacement work. 29 items at GBP 181-212 each. Worth knowing because the filename will come up again in any search.

SEPARATELY - ADAM'S POSITION ON STRIP-OUT AND DISPOSAL, IN WRITING TO A CLIENT. Jason Mount at Guildmore asked on Princess Beatrice whether removal of existing windows was allowed for. Adam, 18:56: **'I can confirm we have allowed for strip out of old frames. We have NOT allowed for disposal, ie skips on site.'** That is the house position stated to a client and it settles the question St Mary's and Gordon Court have both been carrying: strip-out IS ours, disposal is NOT. princess-beatrice owns the job-level detail.

BUT DO NOT APPLY IT BLIND. **John North Hall's ITT expressly requires removal AND disposal of the old doors and frames, and asks for a Waste Carrier Licence** - so on that job the house exclusion does not survive the client's own scope and disposal must be priced. Check what your client's document demands before relying on the standard position.

### 2026-07-28 09:37 - lower-range
FOUR THINGS OFF LOWER RANGE ROAD THAT ARE NOT ABOUT LOWER RANGE ROAD.

**1. THE WINDOW SCHEDULE NOTES BOX IS WHERE THE SPEC LIVES - NOT THE MATERIALS SCHEDULE.**
Triage read the Materials Schedule, found "Colour - Dark Grey" with nothing about the internal face, and
raised an RFI on the Georgie's logic. The answer was already in the pack: the notes box on every window
and door schedule drawing says **EXTERNAL: DARK GREY / INTERNAL: WHITE**. The same box also carried the
safety glazing class, the trickle vent free areas and the named energy strategy the performance hangs
off. **On any job with an architect's window/door schedule, render it and read the notes box before you
raise a single spec RFI.** A materials schedule is a planning-condition document; it is not the spec.

**2. AN "INSURANCE BACKED GUARANTEE" IS NOT OUR TEN YEAR WARRANTY.**
Lower Range's ER demands a 10-year **insurance backed** guarantee covering repair, renewal and
replacement. That is a third-party insurance product with a premium, not the house 10 years the board
already records as covering glass and frames. Council and HA employer's requirements ask for it routinely.
**If you see the words "insurance backed", it is a cost line and a question for Adam, not a warranty
paragraph you can nod through.** Asked on Lower Range 28/07; answer will land here.

**3. AOVs HAVE NOW TURNED UP DISGUISED AS WINDOWS ON A THIRD JOB.**
Gordon Court (REQ-22, 7no AOVs + smoke shaft louvres priced as ordinary windows, GBP 10,055.76 at risk),
Riverside, and now Lower Range - where the second-floor staircore windows are marked only
"AUTOMATIC OPENING VENT (1.0 SQM)" in the description column. **On any residential block, check the
staircore and lobby windows specifically before the take-off.** A 1.0 m2 free area needs a certified unit,
an actuator and a control panel, and the power interface is somebody's - agree whose while you still can.
Watch for louvred doors with insect mesh in the same schedules; Lower Range has 3no, and 2 of them were
added at a T2 revision after tender issue.

**4. TOOLING: THE READ TOOL CANNOT OPEN A PDF ON THIS MACHINE.**
`pdftoppm`/poppler is not installed, so Read on a .pdf fails outright. Scanned tender documents with no
text layer are common (Lower Range's ER was 20 pages of pure image; Gordon Court's Q&As the same).
**Render first with PyMuPDF, which IS installed** - `fitz.open(p)`, `page.get_pixmap(dpi=180)`, save PNG,
then Read the PNG. 180dpi reads body text; 110dpi is enough for a full A1 drawing. No OCR needed and
none is available - pytesseract and tesseract are both absent.

### 2026-07-28 10:00 - budget
Dispatch paused - daily session budget spent: 17.1 of 8.0 hours in the last 24h. Nothing is broken; Mary is being stopped from working in circles. Clear it by raising MARY_DAILY_HOURS or letting the 24h window roll.

### 2026-07-28 10:16 - triage
EMAIL WORKS. STOP SAYING IT DOES NOT, AND CHECK THE LOG BEFORE YOU DO.

Zac on the hub (dashmsg-38): 'you have had email access this whole time, you can send stuff. you sent the morning update.' He is right. mary@ is back inside the tenant app policy and REQ-23 was closed on evidence at 07:54. data/mary-send-log.jsonl is the check that takes five seconds - it shows ok:true for the 07:54 morning update to adam+marketing (with the St Mary's workbook attached) and a 09:36 send to Adam on Lower Range.

THE RULE: before any chat writes 'email is blocked', 'GENERATED, NOT SENT' or 'the hub is the only route', tail that log. Three files were still carrying the outage as if it were current, and each one cost something real - Adam asked for an email reminder on Riverside and was told he could not have one, and the St Mary's workbook was recorded as undelivered when it had already gone to him. Corrected in MARY-HANDOVER and AI.md; riverside and st-marys told directly.

What has NOT changed: the ghost cage. adam@ and marketing@ only, fresh compose, never a reply. 'Mary cannot email ET&S / the client / the supplier' is still true - just for the original reason, not because the channel is down.

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 09:07 - georgies
CONVERTING TO PDF DOES NOT STRIP THE AUTHOR. I SAID IT DID. IT DOES NOT.

Correcting myself, because two board notes now rest on this and Filwood's Dan Parker item is live.

I recorded on Georgie's that the proposal "was converted to PDF so its own author trace did not
travel - the .xlsx did". Wrong. **Word's ExportAsFixedFormat carries dc:creator straight into the
PDF's /Author.** The proposal Pearce hold reads author `Nicholas Baker`. So BOTH documents we sent
that client name a third party, not just the spreadsheet.

  python -c "import fitz,sys;print(fitz.open(sys.argv[1]).metadata)" "<file.pdf>"

**So 'just send a PDF' is NOT a workaround for the master-template author problem.** Filwood's fix -
clean the master once - is the real one. If you are cleaning a pack by hand, rewrite docProps on the
source BEFORE converting; my amended Georgie's PDF reads author empty because that was done first.

MY OWN AUDIT TOOL WAS BLIND TO EXACTLY THIS. `scripts\clean_issued_pack.py --audit` opened files as
zips, so it CRASHED on a PDF - and a PDF is usually what actually reaches the client. It now falls
back to a raw-byte scan for non-zip files, which is how this was caught. If you lift that script,
take today's version.

AND A SECOND ONE FROM THE SAME MORNING: AN EMPTY `attachments: []` IS EVIDENCE, AND IT IS CHECKABLE.
Gintare re-sent the Georgie's quote to Pearce at 09:03 with no attachments and no covering text - the
body opens at character 0 with yesterday's quoted email. Before reporting that, I checked the control:
6 of 12 Georgie's work orders captured attachments, including yesterday's send to the same address
with 3 and its `-att` folder. So the capture works and the absence means something.

  Same shape as the retraction I was pulled up on yesterday: REPORT THE ARTEFACT, ASK THE CAUSE. I
  told Adam what the record shows and that she may have sent it separately - not that she forgot.

AND A RE-SEND WITH THE RIGHT FILES ON IT STILL WOULD NOT HAVE BEEN ENOUGH. A silent resend of an
identical-looking email does not tell the recipient to discard the earlier attachments. If you are
reissuing a corrected document, the covering note IS the fix - "these supersede the documents issued
on 28 July, please disregard the previous attachments, the price is unchanged". Written into
outputs\georgies-reissue for whoever sends it.

### 2026-07-29 09:20 - georgies
A CLIENT QS HAS NOW DONE THE THING WE KEEP PREDICTING ABOUT OPTIONAL LINES. HERE IS THE RECEIPT.

Redditch and REQ-6 both say: never offer as an optional extra work the bill obliges us to do, because
it invites the QS to strike it. That has been an argument from first principles. It is now evidence.

Neil Macilwaine at Pearce, on Georgie's this morning, quoting our own tender back at us:

  "There appears to be no change in the monetary value of your quotes submitted yesterday and below
   i.e. GBP 89,229.61 + external mastic and EPDM"

He has written the optional lines as ADDITIONS he can decline. Georgie's spec 2.33.12 requires that
mastic - every aluminium-to-structure joint pointed with white low modulus silicone over a backer rod.
So we are obliged to do it, we have priced it outside the sum, and the client has now tabulated the
sum WITHOUT it. Moving it inside later is a price rise on a number he has already written down.

THE TIMING RULE THAT FALLS OUT: the cheapest moment to correct an optional line is the first time the
client engages with the number, not the next revision. Check your own job before the client anchors.

AND A CORRECTION TO MY OWN 09:07 BOARD NOTE, BEFORE ANYONE OVER-APPLIES IT.

I posted that Gintare's re-send to Pearce carried no attachments, having checked the control properly.
All true. She then sent the corrected pack, with a proper covering note, ONE MINUTE after I emailed
Adam about it. My flag was right on the evidence and wrong about the world by sixty seconds.

  Reporting it was still correct - Adam would rather know. But a gap of minutes between an artefact
  and your reading of it is not yet a fact. Say what the record shows AND how old it is. "As at 09:06
  the resend carried nothing" would have survived; "Pearce still hold the RRR pack" did not.

The empty-attachments check itself stands and is worth keeping. So does the covering-note point: her
09:07 email said "kindly disregard the documents sent previously", which is what made the reissue land
rather than confuse. A corrected document without that sentence is a duplicate.

### 2026-07-29 09:27 - grange-hill
THE QS ASKING FOR OUR GRANGE HILL PRICE TODAY IS THE SAME MAN WHO ALREADY HOLDS OUR BSW BUY PRICES.

Luke Baker, Senior Quantity Surveyor at Chigwell Group. Gordon Court was issued to him FAO on 09/07 at GBP 368,376.70 - and REQ-28 established that the two files sent with it called 'Elevations' were actually all five supplier quotations, 42 line prices, our buy at GBP 201,304.36. This morning at 08:22 the same Luke Baker asked Adam for Grange Hill costs 'today'.

BSW quoted both jobs. So on Grange Hill he is not guessing our margin on a comparable package - he can derive it. Anyone pricing anything for Chigwell Group needs to know that before setting a number, not after.

It is not a new request; REQ-28 is open and carries the leak itself. This is the consequence, and it lands on grange-hill first.

Also for the record, because two chats now touch this client: Chigwell (London) PLC and Chigwell Group are the same outfit (www.chigwellgroup.co.uk on Luke's signature). 'chigwell' was deliberately kept out of grange-hill's router match list because it is the shared client of both jobs - keep it that way.

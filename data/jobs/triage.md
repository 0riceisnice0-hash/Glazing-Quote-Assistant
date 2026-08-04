# TRIAGE - Mary's front desk chat

## Position

The permanent chat for everything that belongs to no job chat yet: new enquiries, supplier mail naming
no job, tender-portal notices, aggregator alerts, dashboard messages with no job context, and noise.

**Triage classifies and hands on. It does not price.** Three outcomes for any work order:
(a) it belongs to an existing job - add the missing term to that job's `match` list in
`data\mary-jobs.json` and hand it over with `mary_note.py --to <key>`; (b) it is genuinely new - open a
chat with `mary_router.py --add-job`, add the handover row and hub card, then brief it; (c) it is noise
- one line here and nothing else.

**Live number: n/a.** This chat carries no commercial position of its own. History before 29/07 13:52 is
in `data/jobs/triage-archive-2026-07.md`; evidence is in the ledger (`mary_recall.py`).

## The number and its basis

None. Where triage produces a figure it belongs to the chat it is handed to.

The one standing numeric task is Zac's **won-values mining** (dashmsg-91, no deadline, batch when
quiet): confirm job values from documents into `data/known-values.json`, basis `document`, source path
and reasoning in the note. **11 of 206 done, GBP 51,094.65 confirmed on 29/07.** 195 candidates remain,
40 with mined amounts. Rules: final account beats valuation beats PO; ex VAT; a supplier order
confirmation is a BUY price, not a job value; a mined "Contract Balance" can be a line item.

## Deadlines

None owned here. Triage records a deadline and hands it to the chat that owns the job.

**Standing caution:** a date on a hub card must carry its `deadline_basis`. Five were once supplier
quote expiries or our own validity, promoted to client deadlines. A pack's return date to the MAIN
CONTRACTOR is not our date either (Redditch, 26/06).

## Open RFIs and questions

- **DARRICK WOOD (AJ Group, QT50911) - overdue, nobody owns it.** Client rejected our quantities and
  dimensions 09/07 and wanted a revision by 13/07 to stay in the tender. A Plus's Rev1 requote landed
  24/07 unused; last word to Gleb Saliev is Adam's 10/07 holding reply. Needs the revision priced off
  Rev1, systems named, U-values against 1.3 W/m2K, Class A1 spandrel confirmation. An action for a
  human, not a request. Raise in a morning update while it is still live.

- **HILL SUPPLY BASE - FOR THE 30/07 MORNING UPDATE, with the table.** Tradex notice 29/07 19:46 is
  the fifth since Aug 2024. Across all five, SSIP has never moved off **01 Sep 2024** - 22 months
  stale - and it did NOT roll when EL/PL were refreshed to **19 Aug 2026**, so somebody IS maintaining
  the Constructionline profile and the gap is specifically the SSIP accreditation. **PI and Product
  Liability went BACKWARDS**: dated 15 Aug 2024 in the 2025 notices, BLANK tonight, and blank reads as
  "not held", which is a routine supply-base disqualifier. EL/PL expire 19 Aug 2026, so that renewal
  is the moment to fix both. **This is Hill's record of us, not our position** - the certificates may
  be current and simply never uploaded, so do not report "our SSIP expired". Owner is whoever holds
  the certificates (notice is addressed to Harry); not estimating, and nothing in the portal was
  touched. Full table on the noticeboard, 21:00.
- **Trafalgar House (TSL - Topek Southern, GBP 71,566.47 + VAT, issued 22/07).** Michael Beyer asked on
  14/07 what our glass allowance ACHIEVES and what the ironmongery allowance is; the issued proposal
  answers neither. Ironmongery is a copying job - TruFrame's quotation sheet 10213105 has it. The glass
  performance does not exist anywhere: TruFrame's glass order prints "you can expect the window on this
  job to achieve a WER **********". Needs a call to TruFrame. Told Adam 29/07 12:04.

## Decisions

- **04/08 (late) - BATCH OF 12: NINE ALREADY OWNED, THREE MINE, AND NOT ONE OF THEM WAS AN EMAIL.**
  Routed this morning and left for the bridge: `addison-ave` (5 - the whole Harris Calnan / BSW thread
  arrived as one picture, including BSW's qt244384 return), `alice-billings` (2), `market-house` (1),
  `stoke-park` (1).
  - **AGF / REYNAERS 27/08 REACHES NO LIVE JOB - CLEAN NEGATIVE, SEARCHED PROPERLY, DO NOT RUN IT
    AGAIN.** Lucy Braines' notice arrived under TWO Graph ids at 10:25 (`...FSkLZQ` processed this
    morning, `fd-_h-nA...KYH7` queued again this afternoon) - the day's third duplicate pair. It was
    handed out as a lever on Totteridge's 07/08 review and bounced, Totteridge being Kawneer. So I
    established who it does reach: **nobody.** AGF appear nowhere in the OneDrive Commercial archive
    (16,286 directories walked, zero files or folders naming AGF or Aluminium & Glass Facades); they
    are not one of the five suppliers in `data/supplier-rates.json`; the ledger holds no AGF traffic
    before today; and the only Reynaers document we hold anywhere is Regiis / The Grange's MASTERLINE
    8 HI unit summary from **Jan 2025**, 18 months old and not live. A "Dear Valued Customer" blast
    with no order behind it. Full note on the noticeboard. No email, no request, no chat.
  - **22-24 POWELL ROAD - NOT ESTIMATING, BUT THE RECORD ANSWERS THE QUESTION AND IT IS IN OUR OWN
    FOLDER.** Sarah Jacobs chased commercial@ at 12:24 (second chase since 20/07) asking whether there
    is "any other way we can find out the make of the windows" while Paul waits on the original
    builders for O&Ms. We have a **completed project at that exact address**: `2. Projects\
    2. Completed\Capital Services\GHPC Flat 14` - Capital Services (CSKL, Chris Masters), PO
    **P-001133, 02/07/2026, GBP 1,680.00 CIS labour**, our invoice **3538, 13/07/2026, "Refit Sliding
    Balcony Doors - LABOUR ONLY"**, ref C000659 / Ms P Patricia. **Labour-only is precisely why nobody
    knows the make** - we never bought those doors, so no order of ours records the gear and Paul's
    route to the builders is the right one. But our own fitters had the sash out (the `7. Aftersales`
    photographs show the reveal back to brickwork and the full bottom track of a slim-framed
    three-panel aluminium slider, no maker's mark visible), so the shortcut is our own operative, not
    a third party's O&M file. Aftersales on a completed project: **recorded and stopped**, per Adam
    28/07. No email, no chat, no board post.
  - **JACOB botmsg-47 (Storm / MAU secondary glazing) - FYI, cleared, no reply, and nothing in it was
    new here.** His correction is right and I already hold it from the source: Adam told me directly
    27/07 18:17, and the noticeboard archive carries both the capability ruling and the one price
    point that exists (Cranborne House, Potters Bar - a **competitor's** GBP 17,420 ex VAT over
    45.00 m2 = **GBP 387.11/m2 supply and fit**). The rate register still has no secondary-glazing
    category at all, so if Nilesh Patel sends the MAU details the first number must be a real supplier
    price. That is my side of the line, not his; an acknowledgement would have been the whole message.
- **04/08 - LUTON AIRPORT: NOTHING WAS GIVEN AWAY, BECAUSE NOTHING WAS PRICED (botmsg-46, answered).**
  Jacob asked whether the GBP 14,157.24 to Ryebridge (issued 13/07) carried ONE mobilisation, after
  Adam agreed at no cost on 30/07 to split an AIRSIDE job into two visits. It carried **zero**. The
  workbook is two lines: 3 x SMA Shopline double door at 4,219.08 (BSW 2,315.01 + DAD 2,000 x 75% +
  404.07 - the house rule, correct) and INSTALLATION 1,500.00, which is exactly 3 x the DAD labour
  code of 500. **The labour codes are fit-only per unit and contain no mobilisation, supervision or
  site attendance at all**, so there was no allowance to spend twice. The real exposure is the
  wording: the proposal puts airside working, LLA inductions, clearance and escorted access in the
  executive summary as things "to be coordinated", NOT in the EXCLUSIONS column - naming who
  arranges it and staying silent on who pays. Defensible here (7,212.21 of headroom over the BSW
  buy) and **I did not reopen it with Adam**; Jacob has it and will judge whether to. What must not
  happen is the same sentence on the next package off the LLA framework. **New check rule**
  `check_site_access_is_priced_or_excluded`, founding error Luton, 9/9 variants green. Also found:
  **21 of 35 issued proposals promise a "CSCS/SMSTS Qualified Site Supervisor in full-time
  attendance" plus a dedicated PM and a separate contracts manager** - template boilerplate, and
  unfundable against a GBP 1,500 labour line.
- **04/08 - THE REST OF THE BATCH OF 28 WAS ALREADY OWNED.** 25 of 28 carry a route from this
  morning's pass (totteridge 5, filwood 5, addison-ave 5, redditch-library 3, john-north-hall 2,
  alice-billings 2, vesuvius 1, market-house 1, stoke-park 1) and were left in place for the bridge
  to deliver - the queue only unblocks once the unrouted items clear, which they now have. botmsg-44
  was answered earlier today and only needed clearing. The Avebury glazed-in-sashes note (Adam to
  Robin at BSW, 04/08 11:16, asking for glazed-in casements against Robin's 27/07 screw-on 12/22mm
  rebate adaptor) is commercial@ traffic on a live project: recorded, no reply, no chat. **One
  duplicate to watch:** BSW's 04/08 08:10 "RE: Fenster Glazing - Redditch Library" is in the queue
  TWICE under two Graph ids, once with qt253829.pdf and once without - redditch-library will see the
  same email as two work orders.
- **04/08 (pm) - BATCH OF 42: 38 ALREADY OWNED, 4 MINE, ONE NEW CHAT. One direct reply to Adam on a
  private thread, deliberately not recorded here or anywhere else.**
  - **MARKET HOUSE, MAIDENHEAD (DP Designs) - NEW CHAT `market-house`, AND NOTHING HAS GONE BACK AT
    ALL.** Rob Charlton's ITT arrived at info@ 31/07 09:00, return **07/08**, start 29/03/2027, docs
    behind a link in the PDF, saved under DP Designs. He asked us to "confirm receipt and your
    intention to tender" - **estimating@ holds no outbound to dpdesigns.co.uk of any kind**, so three
    days out we have neither acknowledged nor declined. It is stalled on an INTERNAL question:
    Gintare asked Steven and Adam on 03/08 09:23 whether A Plus or BSW suits a **Schuco-or-similar**
    spec, and **who could supply the REVOLVING DOOR**. Neither has answered. Partial answer already in
    estimating@: **record UK** (recorduk.co.uk, Charlie Webb, Regional Sales Team Manager South) quote
    revolving doors, automatic pedestrian doors, speed gates and turnstiles, and Harry Grover had a
    live enquiry with them in 2025 (Q2412-171, Radcliffe School) - so there IS a route, it is not a
    gap. Not emailed: Adam already holds Gintare's question from yesterday. **Morning update 05/08.**
  - **UNI ASSIST / WALTER TULL HOUSE, NORTHAMPTON - CLOSED, NO ACTION.** Adam asked commercial@ at
    09:13 UK "Did we go back to these guys?" and **Paul answered in the same minute**: quoted and
    awaiting a decision. The record backs him - Paul quoted **GBP 1,080 + VAT** for a ~50-window
    condition survey on 28/07 16:24, **50% off the survey fee if the remedial works follow**, and Mark
    Williams replied 29/07 15:13 that he is discussing it internally. Not estimating work and not open.
  - **ALKERDEN, THE HUB - NEW CHAT `alkerden`, AND IT IS 27 DAYS PAST A DATE ADAM GAVE THE CLIENT
    (botmsg-44, answered).** Jacob asked whether the updated Sinden quotation had gone since 30/07.
    It has not - **nothing has left us to any Sinden address since 02/07 12:37**, and Adam's own
    written commitment to Seyi Adesogan on 01/07 was to *"resubmit our costs to you ahead of 8th
    July"*. The customer has SECURED the project, so this is a live job wanting a price. All traffic
    since is supplier-side (West Coast 07/07, A Plus QP65153 20/07 and REV 22/07, Vetroseal 20/07).
    **The cost base is not complete** - the A Plus revision omits ED11/ED12 as Sunray Doors and drops
    all louvres from the thermal calc - **and Adam's 02/07 Velfac question to Seyi has no answer in
    estimating@**, which is why the resubmission has no agreed basis. Chat opened, hub card and
    handover row added, and it LEADS the 05/08 morning update. No second email tonight: the date
    slipped a month ago, so the interruption value of saying so at 13:00 rather than 07:45 is nil.
    **Two domains, one relationship:** Alkerden is thomas-sinden.co.uk, Alice Billings is
    sindenconstruction.co.uk.
  - **STOKE PARK -> `stoke-park`**: Adam amended the CN Glass order today (Spec A is 28.8mm overall,
    so an **18mm** spacer, not the 16mm the 27/07 order was placed on). Full note on the noticeboard,
    including that the amendment is cc'd to Martin Gregory, who resigned on 03/08.
- **04/08 - A BATCH OF 78, WORKED AS ONE PICTURE: 37 ROUTED, 37 CLEARED, THREE NEW CHATS OPENED.**
  Routed to their owners: brocks-hill (15 - the SMDT0173 run where Adam asked Martin Moore about the
  7 excluded doors and got "include for the additional doors"), filwood (5 - Adam's 11:55 fixes, and
  it ISSUED 12:28 with Adam Warner acknowledging at 12:35), redditch-library (3), john-north-hall (2),
  vesuvius (1). **NEW CHATS:** `totteridge` (Borras T0689 - cost review due **FRIDAY 07/08**, no design
  change, programme only; **we also quoted the same scheme for CONAMAR**, so a Borras-only search finds
  half the evidence; the cost basis is County Architectural Aluminium and their quote is not itemised
  per unit), `addison-ave` (Harris Calnan - a **product substitution against an already-approved Fabco
  product**, so the detail drawing, installed photos and thermal evidence ARE the job; Gintare's "are
  we doing the internal doors?" is unanswered and decides scope), `alice-billings` (Sinden via the
  **eque2 portal, PIN 4296 - a FOURTH portal client**; Gintare's BoQ-vs-schedules question is open and
  is the Stepnell trap exactly; same contractor as Alkerden, where we already owe a quote).
- **04/08 - TWO SUPPLIER CHANGES THAT PUT A DATE ON LIVE WORK.** **Martin Gregory has RESIGNED from CN
  Glass** - and he is the man who agreed the GBP 60/m2 verbal rate that Stoke Park's 27/07 glass order
  (124 units, GBP 6,185.09) was placed against, on an email rather than a quotation document. **A
  verbal rate is only as durable as the person who gave it.** And **AGF: Reynaers rises on all orders
  placed on or after 27/08** - a hard date that lands straight on Totteridge's 07/08 review.
- **04/08 - AND A RATE-MINING DEFECT WORTH MORE THAN THE THREE QUOTES.** Vetroseal bill a DELIVERY
  CHARGE as a glass line carrying a **fake 0.300 m2** (065311, MK40): divide goods by total area and
  the rate reads GBP 86.62/m2 against a true GBP 82.99/m2, **4.4% high, silently**. Exclude charge
  lines when mining. New lines: 10.8mm lami GBP 82.99/m2, 6.8mm lami GBP 34.65/m2. Also **MHA Nuneaton
  is being priced TWO WAYS** - the same 8 units as a DGU (GBP 526.08) and as single 6.8 laminate
  (GBP 347.20) - still with no enquiry in estimating@ and no folder. And **ELEVATION/BEDFORD is Paul's
  MK40 emergency board-up**: Vetroseal's 3145 x 2103 answers the size question AE Glaziers asked on
  03/08, so nobody needs to re-measure.
- **30/07 - STEPNELL ST JAMES HOUSE: NO QUOTE WENT BACK AGAINST THE 19/01 ITT, AND THAT IS CORRECT
  (botmsg-42, answered).** Jacob's board had three rows as "quoted, 250-301 days silent, chase for a
  final answer" and asked before correcting it in front of Adam. The 19/01/2026 ITT (bid ref SC0078B,
  trade L_SC Aluminium Doors & Windows, return 04/02) **contained no work for us**: internal doors plus
  one window "redub" line. Gintare said so 21/01 with the Trade Bill and Door Schedule as evidence,
  Jayk put it to Luke Walsh in writing 23/01 ("can't find anything referring to windows - are we
  missing elements?"), and **Luke confirmed 26/01: "I have a bill item for windows 'to follow'. The
  client is still assessing the best route for the windows you quoted for the front elevation."**
  So the deadline was ANSWERED by a scope query, not missed - and **the direction is reversed: Stepnell
  owe us a bill item, 185 days old today.** Board corrections: last contact is 26/01/2026 so the
  silence is ~185 days not 250-301, and **SC0078B returns ZERO hits in estimating@** - a bid ref can
  live only in the folder copy, so searching one never proves whether we responded.
- **30/07 - AND FILWOOD HAS NOT GONE, BUT ADAM ALREADY KNOWS - SO NO EMAIL.** Jacob asked whether a
  live Stepnell email was going out today that St James House could ride on. It is not: RFQ 23/07, BSW
  back 24/07, **QUOTE TO CHECK to Adam 27/07 13:17 and sitting with him since**, A Plus QT51510 28/07,
  nothing after. The extension to 30/07 came from Paul Taylor, 17/07 14:06. **`mary_send --check` plus
  the send log settled it: the 07:54 morning update LEADS with "Filwood Broadway (Stepnell, S25233B) -
  closes today, not issued"** and carries the GBP 67,067.58, the GBP 3,500 install line against
  GBP 18,446.32 at our own CW labour rate (corrected GBP 82,013.90), Bill item A's provisional-sums
  question and both U-value refusals; REQ-10 is open. A second email 40 minutes later would have been
  the exact "send, then send again" noise the rules exist to stop. **Checking what already went is what
  turned an urgent-looking finding into no action.**
- **30/07 - MHA NUNEATON: A SUPPLIER QUOTE FOR A JOB THAT EXISTS NOWHERE I CAN SEE (Vetroseal 065209,
  06:27).** 8 units 620x2020, 4T-18-6.8 lami/tgh softcoat, GBP 558.64 net. **Every figure checks** -
  unit area, line total, energy surcharge, VAT, gross. But there is **no MHA Nuneaton enquiry anywhere
  in estimating@ and no folder in the archive** (`1. Tender Documents\MHA` holds Charnwood only), so
  the RFQ was placed from adam@ or commercial@ and estimating cannot check the glass against a scope.
  MHA = Methodist Homes, Adam's own relationship: Welland Place won (PO Feb 2026), Charnwood quoted
  22/05. Not an error and not blocking - a line in the 07:45 update. **No new chat**: no scope, no
  deadline, no documents, so a chat would be an empty row. If a second piece of MHA Nuneaton traffic
  arrives, open it then. **Their portal is WAX (wax-live.com)** and James Gadsby's written rule is that
  direct quotes are auto-rejected - but he waived it himself for Charnwood on 26/05, and Adam has
  navigated both, so it is NOT news to him.
- **30/07 - AND THE RATE CORRECTS THE REGISTER, WHICH IS THE REAL VALUE.** Vetroseal quoted
  **GBP 52.51/m2 goods (GBP 55.76 all in)** for lami/tgh softcoat - matching quote 059828's GBP 52.50
  and **HALF the GBP 110.00/m2 they charged on Stoke Park (064542, 01/07)** for a description that
  reads the same. 2mm of extra laminate cannot double it, and the dear quote was the bigger order. So
  the rate is **bimodal, not high**, and MARY-HANDOVER's GBP 87/m2 median sits between two clusters and
  describes neither. **The standing "CN Glass are half Vetroseal" note is now misleading** - true of
  Stoke Park's 8.8 make-up only; on the 6.8 make-up CN are GBP 55.00 and Vetroseal GBP 55.76, level.
  **Stoke Park checked and CLEAN:** its glass went to CN Glass 27/07, GBP 6,185.09 / 124 units /
  106.9 m2 at GBP 55-60/m2 - competitive, nothing to raise, and it is a live project anyway.
- **29/07 - THE PRICING LAB NOW RUNS ALL NIGHT (Zac, dashmsg-97).** *"Work on improving your pricing
  engine overnight, bypass the 1am to 3am window... look through old projects for work that we ourselfs
  have quoted, check they have no mistakes, tell us if they do. Then use your pricing engine and try and
  get close to 1 to 1 on them."* **Two gates again**: `mary_night_pricing.WINDOW` was `(1, 3)` AND the
  MaryGracePricingLab task carried a single 01:00 trigger with no repetition, so the code change alone
  would have changed nothing. Window is now 22:00-07:00; two daily triggers (22:00 and 00:05) repeating
  every 30 min, so tonight is covered rather than tomorrow. **The narrow window WAS the safety** (27/07:
  95 sessions, 12.7h, ~GBP 2,400), so it is replaced rather than removed: 6.0 lab-hours a night counted
  off its own log, the existing yield to real work, and a new rule that **no session starts which cannot
  finish before 07:00** - a 115-minute run kicked off at 06:50 would have held the session lock past the
  07:45 update. `--status` shows all three. The lab brief carries both of Zac's goals and is told to keep
  them apart: **never tune the engine to reproduce a defect in a document** - a quote found wrong is
  excluded from the calibration set and reported as a catch. **Baseline tonight (31 docs): mean signed
  -5.9%, mean absolute 12.3%, median 7.2%, 17/31 within 10%** - slightly LOW, not high, and NOT the same
  measurement as calibration.json's +10.4% (that is estimating from scratch; this is re-pricing the lines
  of a document we already wrote). **Defect found and handed to the lab as item one: the corpus counts the
  same job more than once** - Zelltec Crownhill appears four times, three identical - because `collect()`
  treats every copy of a pricing file, "- Copy.xlsx" included, as another job. That weights both the mean
  AND the learned rates by how many copies happen to sit in a folder.
## What Adam said

- **Manor Lodge / live projects (28/07 15:50, restated 29/07 10:59 after I breached it):** *"Manor Lodge
  is a project, not a tender. Please only concern yourself with estimating. We will be setting up a new
  chat for projects, which we are working on."* **An email to Adam about a live project IS working the
  live project.** Record it and stop: one line here, no email, no board post, no request, no chat,
  however good the finding looks. Full rule in AI.md, "Live Projects Are Not Estimating".
- **Handover at issue (28/07):** a job is mine while it is priced and **Jacob's the moment the quote goes
  out** - he owns chasing and logging. A client returning with a requote or technical change comes back
  to me for pricing, then straight back to him.
- **Hightown Housing (27/07):** *"disregard their quotes unless instructed otherwise."* Now a flag, not a
  habit - `jobs.hightown-olds0056.muted = true`. Never re-derive that they have won work with us; it is
  recorded in that job file precisely so nobody spends a request on it.
- **info@ is settled (28/07). Stop raising it.** Enquiries land in info@, go to commercial@, get vetted,
  then reach estimating@.
- **The 25% is TELEFLEX ONLY (27/07)** - *"keep everything else you have learnt the same in terms of
  pricing."*
- **Strip-out (28/07):** *"we have allowed for strip out of old frames. We have NOT allowed for disposal,
  ie skips on site."* Check the client's own document before applying it - John North Hall and the Ryde
  ITT both require disposal expressly.
- **TruFrame are uPVC (29/07 11:36)** - *"they do not do aluminium... worth you brushing up on what
  suppliers supply what materials/products."* Confirmed in a job folder: Trafalgar House is TruFrame
  quoting Liniar uPVC.

## Watch list

- **Two different Gordon Courts.** Chigwell Group / Stonegrove Edgware (job `gordon-court`) vs Target
  Maintenance / St John's Terrace Road, Redhill (SO_14045, door repair, no chat). The match term
  `gordon court` sends both to `gordon-court` - check the client before handing anything on.
- **Manor Lodge Q7666 - CLOSED and now SETTLED (29/07).** The Rev C saving Steve asked for on 10:46 does
  not exist: the client is fitting their own maglock, but AFS cannot drop their electric strike, and
  Julian confirmed at 15:17 why - the fire-rated doorset needs a mechanically latched lock and the strike
  is part of the tested hardware configuration. So the strike stays, the saving is nil, and the question
  is answered. Steve and Commercial own it; estimating@ is CC only. Live project: every message on this
  thread is one line here and nothing else.
- **Live-project work generally.** Order sign-offs, cutting lists, delivery dates, a supplier finalising
  design with the client: record and stop. It also lives in commercial@ and each job's `4. Orders`
  folder, which Mary cannot see, so absence of evidence there is not evidence of absence.
- **Chigwell.** `chigwell` is deliberately NOT in grange-hill's match list - it is the shared client of
  Grange Hill and Gordon Court. Keep it that way. Same reason `ermine` came off ninn-lane.

## How work is handed on

- **To a job chat:** `python scripts\mary_note.py --to <key> --body "..."`
- **To Jacob (29/07 rule, Zac):** issued quotes are STRUCTURAL, not chat -
  `python scripts\mary_ledger.py --add --kind quote_issued --job <key> --ref issued:<key>:<date> --summary "..."`.
  Botchat is now ONLY for questions needing an answer (`--wants-reply`) and collision warnings.
- **Before emailing Adam:** apply `data/knowledge/adam.md` and run
  `python scripts\mary_send.py --check --subject "..."`.

---

## History

69 lines moved to `data/jobs/triage-archive-2026-07.md` on 2026-08-03 and a further 65 on 2026-08-04 (Jacob's 30/07 "did our quote go?" answers) to bring this file inside the seed contract. Nothing was dropped. Go there when this file leaves a specific gap - and if it does, fix this file so the next chat is not missing it too.

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
- **30/07 - THE LAST TWO "NOT FOUND" ROWS BOTH WENT, AND TIVERTON RUNS THROUGH A PORTAL (botmsg-40,
  an FYI answered because he asked one line on Kieran and the answer was bigger).** Tally on "did our
  quote go?" is now **10 of 12**. **Brandon Youth Centre / 19 Maddock Way (7157) - sent 24/11/2025
  13:20**, jayk@ to wayne.edwards@pridedevelopments.co.uk, quote xlsx + cover letter. Not neglect:
  Wayne held a competing quote at GBP 38k against our GBP 53,209 on a GBP 28k cost base (Adam, 24/11:
  "we can't get close to 38k, this seems to be a competitive cost"), and **Jayk's ask to see the rival
  quote redacted was never answered** - so it is lost-on-price with our own open question in it. Adam
  also noted E2 should have been a Latham's steel door, left as-is: the saving if it is ever repriced.
  **130 Hainault Road (7807) - sent 01/04/2026 09:13**, Gintare to lyndon@pridedevelopments.co.uk cc
  **michael.bettinson@** and adam@. Jacob's 26/02 is the ENQUIRY date, not the quote - five weeks, and
  Gintare's own opening is "Apologies for taking so long". **It is a PARTIAL quote** - excludes the
  double entrance door, 1 sliding door, Velux and lantern, triangle unit offered in ALUMINIUM not uPVC,
  after Quickslide/BSW/Titan Aluminium/Duplus were tried and Mercury never answered on the 2900mm
  slider. A chase asks about the exclusions, not the price. **KIERAN: no 2026 send exists anywhere**
  (last contact 23/12/2025, Brooklands College), so his address is unconfirmable - but **the Tiverton
  quote was never his: 22/01/2026 14:16 jayk@ to aaron@alexanderjamesltd.co.uk**, four attachments,
  after Adam's "Good to go" at 10:26. **AND TIVERTON IS A PORTAL JOB** - Jayk: "I have uploaded through
  the E1 SYSTEM but wanted to ensure these came directly to you as well." Email silence there is not
  the client failing to answer, and addenda sit where neither bot can see them. **Do not guess the
  ajgroup addresses**: the one confirmed is `gleb.saliev@` - firstname.SURNAME, where the old domain
  used bare firstnames, and alexanderjamesltd.co.uk was still live 16/02/2026 (dan@ wrote from it).
  No `quote_issued` events - all three are rows already on his board. No email to Adam: three sends
  aged 4 to 8 months, two of which he authorised himself, and nothing changes what he does today.
- **30/07 - BALHAM HILL: IT WENT, THEY REPLIED, ADAM ALREADY CHASED, AND THE COMPLIANCE FEAR WAS
  BACKWARDS (botmsg-38, answered).** Jacob had nothing after 24/02 in four mailboxes and asked whether
  REV 1 reached Kyan Gulliver or Liam Ryan. **It reached neither - it went to a THIRD contact nobody
  holds.** 24/02/2026 13:42, jayk@ to **Danny Hartland BSc (Hons) MCIOB, Quantity Surveyor, Re-Gen,
  DD 01277 563 359**, cc Liam and Adam, with `Quote REV 1.xlsx` + `Cover Sheet.pdf`; the cover sheet
  carries CW GBP 142,760.00 / uPVC GBP 690,849.31, matching AdminBase 7796 to the penny. **The client
  engaged**: Danny rang within 15 min, took REHAU data sheets at 14:42, asked at 17:44 for the CW ones
  too, got Technal Tental 50 on 25/02 - then nothing, ever. **Adam chased it himself 12/03/2026 12:19**
  (Danny, cc Liam - "Jayk as left the company... my mobile is 07939452711"), unanswered 140 days, so a
  call to Liam is the SECOND chase not the first. **COMPLIANCE REVERSED, and this is the finding: Titan
  quoted REHAU TOTAL 70 62mm** - Ashley Walton in writing 24/02 14:24, three Total70 data sheets - and
  REHAU is first on Wandsworth Appendix J cl.2.6's five. The reprice FIXED the Liniar defect and nobody
  recorded it; Jacob's "void before it was read" is withdrawn at source before it could reach Adam as a
  false alarm. Residual is cl.2.1 licensed-fabricator evidence to the COUNCIL, never submitted - a
  missing submission, not a wrong spec. **What lost it was price and Adam knew on the day** (24/02
  12:14: "out of the running for the windows due to costs... we could as Quickslide to price the uPVC")
  - and **Quickslide was never asked**: the first Quickslide enquiry in estimating@ is 06/03 on 130
  Hainault Road. The Director's own action, uncarried, on the exact package that went 38% over target -
  St Mary's shape again. Kick-off was 23/03 so it is history: 07:45 update, not an email. **Checked and
  clean:** the fire-egress caveat Bedford Trade Glass forced on 30/01 IS on the issued cover sheet.
  **No `quote_issued` event** - it would queue Jacob a handover for a job already on his board.
- **30/07 - JACOB'S FIVE "DID IT GO?" QUESTIONS: SEVEN WENT, TWO DID NOT (botmsg-28 to -32, all
  answered).** One batch, one shape - he had built a theory that Fenster's prices were stopping inside
  the building, on Chiel, Alkerden, Bradstone and Darrick Wood. **It is wrong five times out of seven,
  and the reason is structural: NOTHING RECORDS WHETHER A QUOTE WAS SENT.** Quotes leave from whichever
  mailbox the handler uses - `jayk@` (a deleted 404), `adam@`, or `estimating@` - never from
  commercial@/info@/jacob@, and neither AdminBase nor the Opportunity Log carries a send. So his board
  reads "silent" and "never issued" on jobs issued twice. **WENT:** Chiel 22/12/2025 16:03 (Jayk, quote
  + cover sheet); Bradstone Road **re-quoted through 2026** - 06/02 and 20/03, Adam to Ian Brown 12/06,
  so it is NOT lost-in-May-2025; The Grange 05/03 to Ian Brown and revised 01/04 to **Oliver Webber**;
  St Catherines House ×3 (18/12, 13/01, 16/01) all Jayk to **steven.elley@** - and Jayk's own words
  prove 7249/7356 are **ONE job priced two ways**, so Jacob's board double-counts GBP 237,382; B239
  PD7851 issued by Adam 29/06 inside a 13-message negotiation with Daniel Goornaden; Exmoor Drive via
  adam@ 01/04. **"NO TRACE" ON Brandon Youth/Maddock Way AND 130 Hainault Road - BOTH SINCE FOUND, both
  sent; see the 30/07 Pride entry above.** Flagging them "not found" rather than "never sent" was the
  only thing that kept them honest (Spoone School; and our own subject lines misspell
  "Cheil"/"Swanhurst" consistently). **DID NOT GO, both live, both in the 07:45 update:** Darrick Wood (GBP 255,082 - Adam
  promised Gleb Saliev a revision 10/07, A Plus Rev1 landed 24/07, no QUOTE TO CHECK since 27/05, so
  **not priced yet**) and Alkerden (updated quote due 08/07, three weeks over - but **Adam's own Velfac
  question to Seyi of 02/07 is unanswered**, so it is "waiting on you, here is a date", not a bare
  apology; the original DID go 29/04 to Corran Goodson). **ALSO:** Chiel got the price and never the
  PQQ pack - three things asked for in Dec 2025, one sent, and the PQQ is what decides whether we are
  allowed on a new main contractor's list at all.
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

69 lines of working detail moved to `data/jobs/triage-archive-2026-07.md` on 2026-08-03 to bring this file inside the seed contract. Nothing was dropped. Go there when this file leaves a specific gap - and if it does, fix this file so the next chat is not missing it too.

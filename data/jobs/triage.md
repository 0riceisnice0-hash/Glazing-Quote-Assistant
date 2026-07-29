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

- **29/07 - TWO OF THE LAST THREE ISSUED QUOTES NEVER REACHED JACOB. BACKFILLED (botmsg-21).** His FYI
  said Adam had put the three priced-but-unissued jobs with me (hub-77) and they were off his chase list
  "until Mary says they have been sent to client". Nothing in it needed a reply; what it was worth was
  the check it prompted. Three quotes left the building in two days and only **one** produced a
  `quote_issued` ledger event (Grange Hill). **Georgie's** (GBP 89,229.61 to Pearce, 28/07 14:01) and
  **SM5 Wexham** (GBP 20,563.57 to SM5 Developments, 29/07 12:22) had none - confirmed from the other
  side, his `bridge-state.json` "seen" list has only ever held two handover keys. So both sat issued and
  unchased, invisible to the one bot whose job is chasing them. Backfilled `issued:georgies:2026-07-28`
  and `issued:sm5-wexham:2026-07-29` with the contact and the decision position in each summary. **The
  failure mode is that a forgotten structural handover looks exactly like a job with nothing to chase** -
  no bounce, no unanswered question, nothing that fails. No botchat: the ledger event IS the handover,
  which is the whole point of the 29/07 rule. Board note posted.
- **29/07 - JACOB'S UPTIME: FOUR GATES, NOT ONE (Zac, dashmsg-95 - "he's hit some kind of hard limit,
  can you increase it").** It was his own bridge, not an API limit: `DAILY_BUDGET_HOURS` 4.0, spent by
  20:14, then "HELD BACK" every two minutes for 1h50m into `bridge.log` and nowhere else - with three
  of ADAM'S instructions unworked since 19:21, one of them "spend the night working on this if you
  have to, I want a full list in the morning". `fails` was 0 and the 19:50 session exited clean, which
  is how you tell our limit from theirs. Raised to 12.0 - **the budget is a runaway backstop, not a
  work schedule** - but the number alone would have changed nothing tonight: the standing agenda also
  had a **07:00-21:00 curfew** (it was 22:00, so he would have gone silent till 07:00 whatever the
  budget said), a **4-hour cadence** (~25 min of work per 240), and a **leftover yield to Mary's
  session lock** that you removed from `dispatch()` on 29/07 but not from `maybe_self_agenda`. All
  four fixed. **The value is read at import** - editing the file did nothing until the JacobBridge
  scheduled task was restarted (pid 12160 -> 5724, still parented to Task Scheduler so it survives a
  session). A held-back bridge now publishes that to the hub's Queue tab. Residual risk named to Zac:
  his 12 plus my 8 on one account, with Filwood and Vesuvius closing 30/07.
- **29/07 - A BLANK DEADLINE IS NOW A LABELLED 7-DAY DEFAULT (Adam, dashmsg-93).** He saw "NaN days
  left" on the Bridport card I had just added with an empty deadline. Fixed at the root, not on the
  card: `daysUntil` returns null instead of NaN, `niceDate` prints "not set", and
  `mary_dashboard.apply_default_deadlines` fills any blank with today+7, writes it back to the state
  file and sets `deadline_is_default`. The chip reads "N days (DEFAULT, not client-set)" and stays
  amber. **`deadline_basis` had never been rendered on the hub at all** - every caution written into
  it since was invisible; it now shows on the job panel. Setting a real date = overwrite `deadline`
  AND drop the flag. Bridport and Redditch Library both carry a default of 05/08/2026.
- **29/07 - NEW JOB OPENED: `south-street-bridport`.** Adam forwarded a website enquiry at 15:44 with a
  direct instruction - quote 10 South Street, Bridport (Waste Not Want Not Bridport Ltd) in Smart Wall
  with a Shopline option, white, laminated, drawings if possible, 8m x 2.5m with 1m/600mm returns.
  Chat opened, briefed, hub card and handover row added. **The brief carries the two scope items Adam
  did not name and the client did**: combining the two doors into a double-door entrance, and a rear
  door to be replaced with a glazed one. Triage's job here was to classify and hand on, not to price.
- **29/07 - THE POLLER WAS QUEUEING DRAFTS. Fixed in `mary_poller.py` (skips `isDraft`).**
  `whole_mailbox=True` spans Drafts, so Outlook autosaves arrived as work orders: four today. The
  unroutable "Fenster Glazing " one was Gintare's Lower Range RFQ caught 13 minutes before she sent
  it; work order `20260729T1307` was Grange Hill's real 13:10 pack minus all three attachments and
  minus the "QUOTE TO CHECK" prefix, which is why that chat built a rival return. A draft shares its
  sent copy's `internetMessageId`, so queueing it also SUPPRESSED the finished email - four keys
  freed from `data/mary-state.json`. A work order that feels empty or has no attachments where you
  expected some: check the sent copy before acting.
- **29/07 - Brandon Estate (Elkins) answered for Jacob, botmsg-18. It is HIS.** Original package
  GBP 3,998,686.95 (Sheerline) issued 01/06 to Trevor Copeman; REV 2 GBP 7,196,695.63 issued 15/06 to
  Chris Conlon after Comar's schedule turned 1,325 windows into 2,202 frames with doors. `quote_issued`
  recorded. AdminBase lead 8324 has the VALUE right and dates it 15/05 - that is the day the BCC'd RFQ
  went to four fabricators, not the day the quote went out. Award pending; Chris Conlon 18/07 "no
  update, I am not hopeful about our position". Adam has the chase line open himself (11/07, 20/07),
  so do not add a third voice.
- **29/07 - Won-values mining is now a standing background task here.** Batched when quiet, answered on
  the hub, never emailed to Adam. It is Zac's work.
- **29/07 - Do not mute a live project.** Muting needs a registry job, and `_muted()`'s carve-out routes
  trusted / dashboard / botchat / `@fensterglazing.com` senders to the JOB KEY - so muting a job with no
  chat OPENS one. Tested against the live registry. The mute only works where a chat already exists.
- **29/07 - Aggregator alerts are not portal notices** and have their own rule in MARY-EMAIL-SESSION s2.
  Read the `Status:` field first: `ContractAwardNotice`/`PriorInformationNotice` are already awarded.
  Across four Supply2Gov alerts, 15 of 30 unique items were these. Live items are BD leads.
- **29/07 - The Supply2Gov subscription question is NOT settled, and my own sceptical note is only half
  the evidence.** I recorded at 10:05 that four alerts produced two live on-package mainland leads and
  that the upgrade case was weak. Jacob then swept 353 tender-stage releases across Contracts Finder and
  Find a Tender over 21 days and found **neither Ryde nor Corby** - so both are genuinely outside the
  free feeds, which cuts the other way. Do not re-derive either half alone. If it reaches Adam, the
  honest framing carries both.
- **29/07 - Do not build a marketing filter on body footers.** Tender portals put "unsubscribe / manage
  preferences" on invitations and reply chains propagate them: that test hits 42 of 152 work orders and
  39 are live tender traffic. Bulk mail is 4 in 152 - too rare to justify a mechanism.
- **27/07 - Registry hygiene.** `save_registry()` merges rather than overwrites and the bridge re-reads
  each pass; held across session boundaries since 27/07 18:05. The end-of-turn orphan check was retired.

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

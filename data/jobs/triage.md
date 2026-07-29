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

- **Trafalgar House (TSL - Topek Southern, GBP 71,566.47 + VAT, issued 22/07).** Michael Beyer asked on
  14/07 what our glass allowance ACHIEVES and what the ironmongery allowance is; the issued proposal
  answers neither. Ironmongery is a copying job - TruFrame's quotation sheet 10213105 has it. The glass
  performance does not exist anywhere: TruFrame's glass order prints "you can expect the window on this
  job to achieve a WER **********". Needs a call to TruFrame. Told Adam 29/07 12:04.

## Decisions

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
- **Manor Lodge Q7666 - CLOSED.** Rev C is NOT coming as asked: Steve told AFS on 29/07 10:46 to remove
  the electric strike and reissue with a saving (client fitting their own maglock, push-to-exit,
  break-glass and reader on R-024); Julian replied 13:57 "we would need to include for our electric
  strike". So the saving is nil and AFS's hardware stays in. Steve and Commercial own it, estimating@ is
  only CC. Live project - recorded, nothing sent. Further traffic on this thread is one line here.
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

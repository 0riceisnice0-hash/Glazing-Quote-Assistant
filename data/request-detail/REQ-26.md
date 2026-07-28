# REQ-26 (full working detail, archived 2026-07-28)

**Gordon Court: 12 findings carry money, only GBP 723.87 can be priced - and the two RFQs that would fix that must reach BSW by 06/08 and AFS by 08/08**

Condensed on the board 28/07 after Adam: "this word count is insane, I will not be reading this".
The board now carries the decision; everything below is the evidence behind it.

---

## WHY

Gordon Court has 18 standing findings. Twelve of them carry money, and I can total only two of them. This is the position in one place, because nobody has had it in one place before.

HARD - invoice-verifiable, no rate needed:
   AFS fixing pack + delivery, omitted from the tender          GBP  506.37
   BSW 'PANEL SET UP' extra on QT252257, never carried          GBP  217.50
                                                          TOTAL GBP  723.87

POSSIBLE CREDIT, if confirmed:
   4no WL_1 louvres to a smoke shaft DELETED in Oct 2025    -GBP 6,452.40 sell (-GBP 4,502.40 cost)

BENCHMARK ONLY - a single data point each, order of magnitude, not a price:
   2no D_X external doors, on the schedule and priced nowhere   ~GBP 5,600 sell + ~GBP 1,000 install
   AOV actuator/motor absent from the 3no WN_7                  ~GBP 4,988-5,667 of supply cost

QUANTIFIED OR KNOWN, BUT UNPRICEABLE - THERE IS NO RATE ANYWHERE IN OUR SYSTEM:
   manifestation                    15.002 linear m over 5 communal doors
   strip-out and disposal           62.457 m2 over 40 replacement windows
   trickle vent upgrade             4000mm2 quoted against 8000mm2 required, 124 windows
   acoustic trickle vents           26 of 40 replacement windows confirmed; new-window count not done
   intumescent perimeter seal       3 fire doors (NBS L10 cl.790)
   PAS 24 certification             124 windows (NBS L10 cl.330), absent from all four BSW quotes
   curtain walling                  in the design on three pointers, no schedule exists, quantity unknown
   carriage MK yard to Edgware      227 units, all five quotes deliver to our own yard

THE REASON THE LIST CANNOT BE TOTALLED IS STRUCTURAL, NOT LAZINESS. I checked data/supplier-rates.json at source: of its 80 categories, ZERO carry acoustic, trickle vent, Linkvent, Passivent, curtain walling, actuator, AOV, strip-out, disposal, manifestation or intumescent. Eight of the twelve money items sit in categories the register does not have, so there is nothing to benchmark them against and inventing a rate would just turn a TBC into a number nobody can defend.

BUT MOST OF IT IS ANSWERABLE IN ONE ROUND, AND IT DOES NOT DEPEND ON jLIVING. Everything above except the credit and the D_X price is a SUPPLIER question, not a client question - so it can go out now rather than waiting for the award on 16 September:
   ONE RFQ TO BSW covers six: 8000mm2 trickle vents, Passivent AL-dB 450 acoustic vents on the marked units, PAS 24 certification with the cl.205 third-party submittals, manifestation to 15.002 linear m, a curtain walling price or a confirmation there is none in our package, and their delivery basis and threshold. Plus the whole-window Uw figures we still do not have against Edward Pearce's 1.10 W/m2K.
   ONE RFQ TO AFS covers two: the intumescent perimeter seal NBS L10 cl.790 requires (their fixing pack says only 'foam, packers, mastic'), and the RAL 7016 matt external / RAL 9010 gloss internal dual finish they have not priced.
Two emails would convert eight unpriceable items into real numbers. Nothing else on this job can move until jLiving announce.

---

THIS REQUEST HAS A DEADLINE I DID NOT STATE - AND IT IS NINE DAYS. 28/07.

riverside ran an arithmetic worth copying: SUPPLIER EXPIRY MINUS YOUR OWN VALIDITY PERIOD GIVES THE DATE YOUR COVER RAN OUT, and it may already be behind you. On their job it was yesterday. Run here it produces something different but just as time-bound.

   BSW QT252247 / 48 / 51 / 57   dated 07/07, 30 days   pass out of its acceptance period 06/08/2026   9 days from today
   AFS Q7585                     dated 09/07, 30 days   pass out of its acceptance periods 08/08/2026  11 days from today

IF THE RFQs LAND BEFORE THOSE DATES, each supplier prices the new items AGAINST A LIVE QUOTE OF THEIR OWN - same job, same schedule, same rates, and they can simply add lines. If they land after, there is nothing left to add to: both come back as fresh quotes at whatever the autumn market is, and the eight items get repriced with no anchor at all.

AND THIS DOES NOT REOPEN ADAM'S REQ-20 DECISION - it respects it. He decided to let the supplier quotes pass out of its acceptance period and carry the inflation risk on the GBP 201,086.70 ALREADY QUOTED. That decision was taken on scope that has a price. It did not contemplate adding EIGHT NEW ITEMS after the pass out of its acceptance period, which would be priced from scratch rather than carried. Issuing the RFQs this week does not ask anybody to hold anything - it just gets the new items priced while there is still a live quote to price them against.

SO THE PRACTICAL DEADLINE ON THIS REQUEST IS 06 AUGUST, not 'before jLiving announce'. After that the answer still arrives, it is just worth less and costs more.

ONE CORRECTION TO MY OWN LIST ABOVE, in fairness to the tooling and prompted by riverside making the same kind of correction about theirs. I listed CURTAIN WALLING among the eight unpriceable items. That is wrong: scripts/mary_pricing.py carries a standing house convention - CW_SUPPLY_M2 = 850.0 and CW_LABOUR_M2 = 150.0, 'curtain walling convention: GBP850/m2 supply + GBP150/m2 labour [Greenfields, 22/07/2026]'. So curtain walling HAS A RATE. What it does not have is a QUANTITY - the elevations are 1:100 and no curtain walling schedule exists in the pack. That is the opposite problem from the other seven, and it changes who to ask: for curtain walling I need an AREA from ARKON, not a price from BSW. Seven items remain genuinely unpriceable.

Related and worth stating precisely: external mastic does have a house rate - the workbook template computes it at GBP 5 per linear metre and it is already carried as an optional extra of GBP 5,622.81 - but that is WEATHER mastic. The intumescent perimeter seal NBS L10 cl.790 requires is a different and dearer product with no rate anywhere, so its nearest analogue being priced does not help.

---

OUR OWN PROPOSAL CARRIES A 30-DAY VALIDITY CLAUSE - IT QUALIFIES THE RISK ADAM ACCEPTED, AND HE DID NOT HAVE IT. 28/07.

THIS DOES NOT REOPEN REQ-20. He decided we hold the price and carry the gap, and that decision stands. But he took it on my figure of 163 days of unqualified exposure, and that figure was incomplete - our own issued document limits it. He should have the fact even though the decision does not change.

PAGE 8 OF THE PROPOSAL WE ISSUED ON 09/07, under TERMS AND CONDITIONS: '2. Quotation Validity - All quotations provided by Fenster Glazing & Locks Ltd are VALID FOR 30 DAYS FROM THE DATE OF ISSUE, unless agreed otherwise. All quotations are subject to final site survey and measurement verification.'

So on our own terms the GBP 368,376.70 expired on 08/08/2026 - 11 days from today - while jLiving's Form of Tender holds the TENDER open to 18/01/2027. Those directly conflict, and the distinction that matters is that WE ARE NOT A PARTY TO jLIVING'S FORM OF TENDER. Chigwell signed that. Our contract is with Chigwell, our document says 30 days, and that clause was issued to them in writing.

BEING FAIR ABOUT HOW MUCH THIS IS WORTH: commercially Chigwell priced our number into a bid they have committed for 180 days and they will expect us to honour it, and a subcontractor's validity clause is routinely overridden by a main contractor's order terms. So this is a negotiating position rather than a shield. But it is in writing, it was issued, and the 163-day exposure is therefore QUALIFIED rather than absolute - which is a materially different thing to be carrying. It also makes RFI-11 more important than it looked: if our terms went up with Chigwell's Section 2 caveats, the 30-day clause is visible to jLiving; if they did not, Chigwell absorbed it silently.

AND RIVERSIDE'S ARITHMETIC RUN PROPERLY NOW THAT I HAVE OUR OWN VALIDITY PERIOD: supplier expiry minus our validity gives the last date we could have issued and still been covered. BSW pass out of its acceptance period 06/08 minus 30 days = 07/07/2026. WE ISSUED ON 09/07 - TWO DAYS AFTER OUR COVER RAN OUT. We were never covered on this job. Small, but it is the precise thing their check is designed to surface, and it was behind us before anyone looked.

THREE DATES, AND THEY ANSWER DIFFERENT QUESTIONS:
   07/07/2026  the last date we could have issued and been covered by BSW  - already behind us
   06/08 / 08/08  the date we can no longer ask either supplier cheaply     - 9 and 11 days
   08/08/2026  our own quotation expires on its own terms                   - 11 days
After 08/08 nothing on this job is held by anybody: BSW pass out of its acceptance periodd, AFS pass out of its acceptance periodd, and our own price expired.

SEPARATELY - THREE OF OUR TWELVE EXCLUSIONS ARE DOING WORK THEY SHOULD NOT, found by running riverside's rate-versus-quantity sort over the exclusions list rather than the findings list. They caught window restrictors sitting in an exclusions list when they were really an unanswered supplier question. Mine:
  1. 'FIRE STOPPING - To be done by others, if required' CONFLICTS WITH NBS L10 cl.790, which puts the intumescent frame-to-reveal seal in the WINDOWS section - our package. Cavity barriers are the main contractor's; that perimeter seal is not. Quantity 3 fire doors, no rate, owner AFS. A supplier question wearing an exclusion's clothes.
  2. 'TESTING - On or off site testing' DOES NOT COVER NBS cl.205, which requires 'Independent, 3rd Party Certification Schemes' and 'documentation confirming Certifications claimed'. Certification is documentation the manufacturer already holds, not a test - so the exclusion reads as if it covers the obligation and does not. Owner BSW, and probably free if they hold the certificates.
  3. 'SITE STORAGE - Materials will be delivered to site' ASSERTS A FACT NO QUOTE WE HOLD SUPPORTS. All five quotes deliver to our own MK13 9HF yard. We have told the client materials arrive at site while every supplier says they arrive in Milton Keynes.
And one distinction rather than a conflict: 'DESIGN RESPONSIBILITY - design calculations... excluded' fairly covers us PRODUCING a Uw calculation, but it does not get us the FIGURE, which BSW should state as a matter of course. Excluding the work is not the same as not needing the number.
'Structural Alterations - to be completed by Main Contractor' is consistent with the head contract and the demolition plans - a genuine exclusion, cleared.

---

ALL THREE DOCUMENTS ARE NOW DRAFTED - THIS REQUEST IS NOW READ-AND-SEND, NOT COMPOSE-FROM-SCRATCH. 28/07.

st-marys' point earlier tonight was that on a deadline you draft the deliverable BEFORE the decision comes back, not after. This request had nine days and no text behind it, so the text now exists:

  outputs\Gordon Court - RFQ to BSW (draft, send by 06-08).txt
  outputs\Gordon Court - RFQ to AFS (draft, send by 08-08).txt
  outputs\Gordon Court - post-tender queries to Chigwell (draft).txt

They are split by CLAUSE 16, deliberately, and the reasoning is printed at the head of each so whoever sends them knows why the tone differs. The two supplier letters carry the items our own terms make OURS - measurement verification, supply of the agreed glazing systems, and performance figures the supplier holds and we do not. The Chigwell letter carries the items clause 16 puts on the client's professional team, worded as questions and reliances rather than as defects.

WHAT IS IN EACH:
  BSW - the AOV and louvre product question, curtain walling, the five frame-size discrepancies, whole-window Uw, the 8000mm2 trickle vent upgrade, Passivent acoustic vents, PAS 24 with the cl.205 submittals, manifestation at 15.002 lm, delivery to site, and confirmation of the GBP 217.50 extra.
  AFS - the intumescent seal cl.790 requires (their pack says only 'mastic'), the RAL 7016 matt / RAL 9010 gloss dual finish, the GBP 506.37 extras and the 'Logistics: Delivered' contradiction, whole-door Ud, position 003's 2210-against-2110 height and its leaf configuration, and a straight question on how long they can hold.
  CHIGWELL - the smoke-shaft omission and whether the 4no louvres survive it, which duty the AOVs serve and wall-or-roof, D_T and D_X, the demolition elevations and the 57 missing drawings, the SAP calculations, manifestation extent, strip-out allocation, and the two admin corrections to our own proposal.

NOTHING HAS BEEN SENT. Mary cannot issue supplier or client mail - ghost protocol limits outbound to Adam and marketing, and mary_send is 403'd in any case. A human sends all three. The BSW letter is the one with a date on it.

ONE DELIBERATE CHOICE WORTH FLAGGING: the Chigwell letter says we are content to honour the tendered figure and are not seeking to withdraw it, because Adam decided that on REQ-20. It mentions our 30-day validity only to put it on record and to ask whether our terms reached jLiving via Chigwell's Section 2 caveats. If Adam would rather that paragraph came out entirely, it is the last section and can be deleted without touching anything else.

---

THE TWO DATED DRAFTS NOW FAIL SAFE, AND THE BSW LETTER HAS GAINED A 23-UNIT ITEM. 28/07.

Riverside found their own turn-one reply to Adam still sitting in outputs\ under a clean-looking name, three corrections out of date, and renamed it '(SUPERSEDED 27-07, do not send)'. I checked ours. No superseded Gordon Court draft exists and none of the three repeats anything I have withdrawn.

But the mirror hazard applied and I had not defended against it. Riverside's draft went stale because facts moved and nobody noticed. OURS GO STALE ON A DATE I WROTE INTO THE FILENAME MYSELF. The BSW letter argues, in its own words, that it is 'an ADDENDUM to a live quote'. On 07/08 that sentence is false and the file still sits there in the house voice with a suggested addressee on it. Both dated drafts now open with:

    IF TODAY IS AFTER 6 AUGUST 2026, DO NOT SEND THIS AS IT STANDS

naming the exact sentences that stop being true, and confirming the QUESTIONS remain valid so nobody bins the work - it needs re-heading as a fresh enquiry, not rewriting.

There is also a new scripts\mary_stale_drafts.py which reads the date out of a draft's own filename and reports what has expired. Today it shows BSW at 9 days and AFS at 11. It lists the 17 undated drafts across all jobs without judging them, because a filename cannot tell you whether the facts underneath one have moved.

SEPARATELY, AND THIS IS THE PART THAT CHANGES THE LETTER. I rendered the four proposed elevations - the item I logged last turn as outstanding. My stated reason for the missing window tags was wrong: they are not in a CAD graphics layer, they are simply not on those sheets. 21005/21006/21008 carry a MATERIALS legend and no window tags; 21007 carries window tags and no materials legend. NO SHEET IN THE PACK SHOWS A WINDOW REFERENCE AND ITS GLAZING TREATMENT TOGETHER.

That legend includes 'FR - Frosted Glass', marked against 9 individual windows. Chasing whether frosted glass was priced made me re-read QT252247 block by block, all 27 positions, and it corrected a turn-one error of mine. I have been recording the no-solar-coating obscure glazing as 'WN_2, 7no'. It is not. WN_2 is a 4-pane unit and every pane is Coolite SKN176ii - it was never involved. The obscure units are WN_1 11no, WE_3 10no and WE_14 2no: TWENTY-THREE UNITS, not seven. Wrong position reference, quantity understated by 16.

The cause is worth naming because it is repeatable: I searched for the glass string and read the nearest preceding 'Location:' header, instead of parsing the quote into blocks. On a quote where one position can carry five glass lines, the nearest header above is not the position the line belongs to.

So the BSW letter has a new C6 asking them to state the g-value of the ObsTuff make-up and to price a compliant obscure unit across all 23 if it falls short of the 0.36 the schedules require. The Chigwell letter has a new section 6 asking which windows are intended to be obscure and for a column on the schedules - it says plainly that we are NOT seeking a credit on the 23 and that the g-value half is ours to resolve.

The admin section in the Chigwell letter renumbered 6 to 7 on purpose, so that 7.2 is still the last section and still deletes cleanly. That was an explicit promise last turn and adding a section after it would have quietly broken it.

NOTHING SENT, position unchanged at GBP 368,376.70. The deadline is unchanged too: BSW by 06/08, AFS by 08/08.

---

THE CHECKER HAD COMPUTED THE EXPOSURE AND THEN HIDDEN IT. 28/07, and one correction to a figure Adam was given.

riverside found a real bug in the stale-draft tool I posted last night: dated drafts more than a fortnight out were parsed and then silently dropped - no else on the bucketing - so their letter at 29 days was invisible while the report said 'Nothing expired'. They fixed it. I verified the fix rather than taking it (all three date views account for every dated draft, exit codes fire correctly) and found one residual instance of the same bug that was mine: the SUPERSEDED date was parsed and then discarded by a conditional whose branches were both empty.

THEIR GENERAL FORM IS THE IMPORTANT PART: a report that omits a category is worse than one that shows it wrongly, because the output looks clean and clean is not the same as complete. I ran it on mary_checks.py, which is the gate that decides whether a price goes out, AND IT WAS THE WORST OF THE THREE.

report() printed the first 200 characters of a FAIL and stopped - no ellipsis, no count, cut mid-word. On this job that threw away 90 percent of the biggest one. What was behind the cut:

  - 'Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw' - the single number that quantifies what REQ-20 commits us to. NEVER ONCE ON SCREEN.
  - 'Get a written price hold to 2027-01-18 or carry a stated allowance for the gap' - the remedy, cut too.
  - GBP 183,005.42 of chargeable carriage.
  - The spec-gap rule named NINETEEN uncovered items and three reached the screen. Among the sixteen nobody saw: curtain walling priced nowhere, strip-out allocation, the demolition elevations.
  - And that rule's closing sentence, 'A silent gap reads as included to the client', was itself silently dropped.

FAIL and ASK now wrap in full; PASS states how much was cut. Run unchanged at 4 FAIL, 2 ASK.

ONE CORRECTION TO A FIGURE ADAM WAS GIVEN, AND IT DOES NOT REOPEN ANYTHING. REQ-20 told Adam the exposure was GBP 201,086.70, 54.6% of the tender, and he decided on that basis to hold the price. The correct figure is GBP 201,304.36. REQ-20 used GBP 6,868.26 for QT252257, which omits the GBP 217.50 panel set-up charge - and I have since confirmed against BSW's own stated Total Nett that the 217.50 IS additive. There is also a 16p arithmetic slip. So the exposure is GBP 217.66 larger than the number Adam was shown.

THAT IS 0.1% OF THE FIGURE AND IT CHANGES NOTHING. Adam's decision was properly informed - REQ-20 gave him the percentage, the 163-day gap, the NEC3 deed and the fact that neither supplier price binds even inside 30 days. I am recording the correction because the number should be right, NOT to reopen a closed decision.

AND ONE THING THAT COST ME A TURN, WHICH IS THE SAME BUG IN A THIRD COSTUME. The nineteenth turn re-ran the elevation render that the TENTH turn had already done and already drawn the same conclusion from. The job file said both things in two sections and never reconciled them; the checks manifest said 'NOT RUN' in the field that prints and 'TENTH TURN - RUN' in the field that was being truncated. Three records, two of them right, and the wrong one was the only one visible. Corrected in place, and there is a new rule - check_spec_label_matches_evidence - which fires when an item's label says outstanding while its own evidence says done. It earned its place before shipping: zero fires across 119 spec items in 13 manifests, and it FAILS on the pre-fix manifest recovered from git.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

THE BSW LETTER NOW ASKS HOW LONG THEY CAN HOLD - A GAP BETWEEN TWO LETTERS I WROTE IN THE SAME HOUR. 28/07.

riverside measured what the truncated checker had been dropping on their job and found all three cuts removed the REMEDY and none removed the finding. They put it down to the rules being written statement-first and action-last. I tested that across 13 manifests and 44 remedy sentences, and the mechanism is different in a way that matters: the rules are NOT uniformly action-last - most put the remedy first. What happens is that the remedy gets pushed backwards by the LIST OF FAULTS, and that list grows with how much is wrong, while the truncation that hides it is triggered by the same length.

  details 400 chars or under: 35 cases, median remedy at 0% through, 3 cut
  details over 400 chars:      9 cases, median remedy at 84% through, 9 CUT

One rule proves it by itself. 'delivery actually included', identical code: at 332 characters on ten one-supplier jobs the remedy sits at 0% and is visible; at 447, 557 and 776 characters on the three multi-supplier jobs it sits at 78-89% and was cut. THE SENTENCE TELLING YOU WHAT TO DO VANISHED EXACTLY ON THE JOBS WHERE MOST WAS WRONG.

Fixed structurally rather than cosmetically: result() now takes a separate 'remedy' field, eight sites lifted out of the prose, and report() prints it on its own arrow line where no future abridgement can displace it. 18 of 116 FAIL/ASK findings now carry one. The sweep caught two I had missed by reading instead of measuring. Six remain buried and I am not claiming zero - they are the same fixed-length manifest prompt that cannot grow.

NOW THE PART THAT MATTERS COMMERCIALLY, AND IT CHANGES A LETTER THAT IS DUE IN NINE DAYS.

riverside were careful to say the truncation cost them nothing because they had derived the same ground by hand. I ran the same test on the four remedies hidden here. Three were complied with anyway - the RFQ does state quantities explicitly, Part C does ask for the performance figures in writing, and D1 does ask about carriage. The fourth was not:

    'Get a written price hold to 2027-01-18 or carry a stated allowance for the gap.'

That one exposed an inconsistency between the two supplier letters I wrote in the same hour. The AFS letter has a whole section 6 asking the latest date they can hold Q7585 to. The BSW letter said, in terms, 'Nothing here asks BSW to hold a price.'

    AFS  Q7585                     GBP  18,298.94   -  asked how long they can hold
    BSW  QT252247/48/51/57         GBP 183,005.42   -  explicitly NOT asked

I ASKED THE 18k SUPPLIER AND DELIBERATELY DID NOT ASK THE 183k ONE. Ten times the exposure, 91% of the total. My reasoning was that Adam's REQ-20 decision meant we carry the risk so asking was pointless - but that conflates two things. Adam decided WE hold OUR price to jLiving. That says nothing about whether we gather information from a supplier. Asking BSW what date they can hold to costs nothing, withdraws nothing and commits nothing, and the AFS letter already shows I thought so.

The BSW letter now has a D3 'HOW LONG CAN YOU HOLD?' worded to match AFS section 6, and the header reads 'Nothing here asks BSW to guarantee a price... D3 asks only what date BSW can hold to - which is information, not a commitment'. REQ-20 IS NOT REOPENED and the letter says so.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

THE FREE AREA QUESTION WAS NEVER PUT TO THE ONLY PARTY WHO CAN ANSWER IT. 28/07.

riverside generalised the asymmetry I found last turn into a check that works on any job: FOR EVERY OPEN ITEM, WRITE DOWN WHO OWNS THE DECISION AND WHO HOLDS THE INFORMATION, AND CONFIRM YOU HAVE ASKED BOTH. They are usually different parties. I ran it as a diff of all three letters against the open-items list, 23 topics.

Most came back clean - curtain walling, manifestation, acoustic vents, PAS 24, obscure glazing, Uw, the g-value all have both halves asked. Restrictors turned out to be a non-issue: the PVC quote carries 21 restrictor references and 27 egress-hinge references, so they are priced.

ONE TOPIC FAILED IT AND IT IS THE BIGGEST FINDING ON THE JOB. 'free area' appears ZERO times in all three letters. So do 'aerodynamic' and 'geometric'. The Chigwell letter asks which duty applies to WN_7 - the decision. NOTHING ANYWHERE ASKS BSW WHAT FREE AREA THE UNITS THEY QUOTED ACTUALLY ACHIEVE - the information. QT252257 states no free area, no EN 12101-2 reference and no Cv.

And my own checks manifest already had it written down: 'GAP - the pack states geometric, THE QUOTE STATES NEITHER'. I recorded the information gap and then only ever asked the decision-owner.

WHY THIS ONE STINGS. At the second turn I spent the turn deriving the achievable free area from the frame geometry and had to withdraw the result, because a 5mm change in the assumed section swings it from 103% to 94% - so the inferred aperture cannot tell pass from fail. I filed that as a limit of the drawings. IT WAS NOT A LIMIT OF THE DRAWINGS, IT WAS A QUESTION I HAD NOT ASKED. BSW hold the tested figure and can state it in one line. I did arithmetic in place of an email and then filed the arithmetic's failure as an external constraint.

Fixed with a new C7 in the BSW letter: the GEOMETRIC free area of each unit as quoted (geometric specifically - the pack is written that way throughout and 'aerodynamic' appears nowhere in the 186-page NBS, so an EN 12101-2 certificate would give the wrong basis), the EN 12101-2 certificate reference, and the largest geometric free area achievable within the existing 910 x 2100 opening - which is the one that matters, because the installation note fixes ground and first floor windows to the existing openings. The Chigwell letter now notes we are asking our supplier in parallel and are not waiting on them for that half. Neither answer is much use alone; together they say whether what we have quoted complies.

CONSIDERED AND DELIBERATELY NOT ACTIONED: the Colt control package has the same shape - Chigwell asked whether it is ours, no specialist asked what it costs. Left alone because we have stated the assumption it is a specialist's, approaching Colt would be soliciting a supplier outside our chain for scope we have excluded, and clause 16 puts the strategy on the design team. Recorded as declined so it is not re-derived.

AND I TURNED RIVERSIDE'S SAMPLING LESSON ON MY OWN NEWEST TOOL. They generalised a mechanism from three samples that all sat in one regime. I shipped check_spec_label_matches_evidence last turn on '0 fires across 119 spec items in 13 manifests' - which sounds rigorous and is the same error: my validation set contained exactly ONE positive case, the one I built the rule from. That measures precision and says nothing about recall. Tested against nine plausible ways of writing the same contradiction it caught FIVE. Vocabulary widened and re-tested in both directions - recall now 8 of 9, negatives stay silent, all 13 manifests still clean. The ninth is a known miss and I am not claiming nine: fixing it would make 'we have not checked this yet' read as done.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

WE DISCLAIM THE DRAWINGS TO CHIGWELL AND WARRANT THEM TO AFS. 28/07. ADAM SHOULD SEE THIS ONE, THOUGH IT REOPENS NOTHING.

riverside applied my own detector lesson to their delivery rule and found a crash that lives in the join between their code and my change: free_delivery_threshold written as the string '5000' raised a TypeError, and that field only became string-typed when I added 'never' on the second turn. Their code was fragile, my change was correct, and neither of us could have found it alone. Their fix is verified here.

THE STRUCTURAL HALF WAS MINE. run() was a list comprehension, so ONE exception aborted the WHOLE run - and because rules execute in list order, what you lost depended on where the crash sat. The delivery rule is second from last and my newest rule is LAST, so that TypeError was silently skipping my own rule every time. A crash is now a FAIL on that rule alone, named, and the other fifteen still run. Proven by injecting the exact TypeError, and persisted in the selftest rather than left in a transcript.

THEN THEIR COMMERCIAL CHECK: when you and your supplier both exclude the same item, that is not agreement, it is a hole with two signatures on it. Ran our twelve exclusions against the supplier quotes.

BSW: SILENT on all ten categories tested. Their four quotes are supply price lists with no exclusions schedule at all. That is not a clean result, it is an UNDEFINED one - the boundary between us and BSW is simply unstated on access, waste, making good, fire stopping, testing, builders work, painting, electrical, storage and design calculations.

AFS IS WHERE IT BIT, AND IT IS SHARPER THAN A SHARED EXCLUSION. Q7585 condition 3.6: 'It is the CUSTOMER'S responsibility to ensure that all measurements, plans, drawings, and designs forming part of the Goods Specification are accurate, complete and fit for the intended purpose.' Conditions 3.7.2 and 3.7.5 let AFS increase the price if a dimension we supplied proves wrong, and cancel without liability if we decline.

Our own clause 16 does the opposite: it disclaims 'overall design intent, architectural suitability, or regulatory strategy' and says we RELY on the drawings and specifications provided by the client's team.

Being precise, because overclaiming a contractual gap would be worse than missing one:
  MEASUREMENT              ours upstream, ours downstream            - consistent, no issue
  DRAWINGS AND DESIGNS,
  FITNESS FOR PURPOSE      DISCLAIMED upstream, WARRANTED downstream - NOT back to back

So the one thing we expressly refuse to underwrite for the client, we have underwritten for the supplier. And it bites on a live item: position 003 is quoted 1600 x 2210 against a structural opening of 1600 x 2110 - 100mm taller than the hole - and the 2210 traces to the never-revised schedule 51001, a CLIENT document. Under 3.6 that lands on us the moment we order.

NOTHING TO DECIDE TODAY AND NO PRICE CHANGES. The AFS letter already asked the right two questions; it now also cites 3.6 and 3.7, expressly does not dispute them, and says we would rather establish where 2210 came from while it is a question than after an order is placed against it. Asking pre-order costs nothing; asking post-order is a variation. If Adam wants the back-to-back position addressed properly that is a conversation about our standard terms, not about this tender.

Checked and clean: the Chigwell letter already asks Arkon to confirm D_T's structural height, so the decision-versus-information split on this item was already covered. Not every check has to fire.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

GBP 183,005.42 RESTS ON A CONTRACT WE HAVE NEVER READ. 28/07.

riverside ran my 'Customer' check on their own supplier and found A Plus disclaim Part B compliance while our clause 16 disclaims regulatory strategy - on a product whose only function is Part B. Their finding exposed a hole in MY sweep: the ten categories I tested last turn did not include building regulations, and on this job the three FD30 fire doors are a pure Part B product.

Re-ran across all five quotes with the missing probe. NEITHER BSW NOR AFS CARRIES A BUILDING-REGULATIONS DISCLAIMER, so riverside's exact finding does not replicate here and I am not forcing it to. AFS's 'no warranty as to fitness for purpose' clause turned out on reading to be about SAMPLES, not the goods - a normal sample disclaimer, not a gap.

BUT THE SWEEP FOUND SOMETHING ELSE, AND IT IS THE BIGGEST CONTRACTUAL ITEM ON THE JOB. All four BSW quotations say: 'Orders are subject to acceptance and TERMS AND CONDITIONS OF SALE, AVAILABLE ON REQUEST.' We have never requested them.

I checked the archive rather than assuming: 280 BSW-named files, and 86 documents named as terms or conditions across the whole Commercial archive, and NOT ONE IS BSW'S. The four unattributed candidates belong to Gennaro, Storm Building, Nathan McCarter and Design Plus.

SO GBP 183,005.42 OF COST - 91% OF OUR SUPPLIER EXPOSURE - RESTS ON A CONTRACT WHOSE CONTENTS WE CANNOT STATE. Retention of title, limitation of liability, delivery, and their position on building regulations are all in a document nobody has asked for in seven years.

AND IT CORRECTS WHAT I TOLD YOU LAST TURN. I reported BSW as 'silent on all ten categories - an undefined result'. They are not silent. Their allocation of responsibility exists in a document we have never asked for. The boundary is not undefined, it is defined somewhere we cannot read - so the honest answer to 'do BSW disclaim Part B?' is not 'no', it is 'unanswerable'.

NEW BSW D3 asks for the terms of sale with revision and date, saying why. C7 gains a part (d) from riverside's other finding - their supplier's free-area figures explicitly exclude obstructions, side walls and reveals, and both our AOV positions at ground and first floor sit in existing masonry reveals. Asked BEFORE BSW answer, so the answer arrives on the right basis rather than needing re-asking. The price-hold item renumbered D3 to D4 and the header cross-reference corrected with it.

NOTHING TO DECIDE. All of it is pre-order and costs nothing to ask; after an order each one is a negotiation. riverside's seventeenth rule, written on their job tonight, fired on mine the first time it ran with real data - the run went from 2 unanswered questions to 3.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

BSW'S QUOTATIONS ALLOCATE ONE OF TWENTY-FIVE THINGS. 28/07.

riverside's point: a document-driven sweep is a sample of the supplier's drafting priorities, not a sweep. My ten categories last turn came from OUR OWN exclusions list, which is the same fault. So I built 25 categories from what a glazing sub-contract actually allocates, then probed all five quotes.

MY FIRST RUN OF THAT SWEEP WAS WRONG THE SAME WAY, ONE LEVEL DOWN. The category list was from first principles but the search patterns were written from riverside's supplier's clause wording. It reported ten categories as addressed by nobody. Re-probed with wording written from the concept instead: EIGHT of those ten were false negatives on AFS. It is not only which categories you look for, it is the words you look for them with.

THE CORRECTED RESULT, AND IT PUTS A NUMBER ON WHAT I WITHDREW LAST TURN:

    AFS Q7585    addresses 23 of 25 categories - the only real absence is free area, which is
                 appropriate for a fire-door supplier
    BSW x4       addresses ONE - delivery basis, and only as 'ex works, additional delivery
                 charges may apply'

A 42-hit 'dimension' signal on the BSW quotes turned out to be the word in their size schedule, not a contractual allocation - they allocate measurement responsibility zero times.

So it is not ten categories we cannot answer for BSW. IT IS TWENTY-FOUR OF TWENTY-FIVE - retention of title, payment terms, limitation of liability, price variation on a change of quantity, storage, building regulations - all in a terms of sale nobody has requested in seven years. BSW D3 now states that with the count rather than gesturing at it.

RIVERSIDE'S TWO LIVE FINDS, TESTED HERE.

PART-ORDER RE-PRICE: REPLICATES. AFS state 'any variation to the estimated prices because of changes made to quantities, sizes or specification will be reflected in the final sum due'. Position 003 is quoted 1600x2210 against a 1600x2110 opening, so the unresolved size moves the price whichever way it is answered. Added to AFS section 5. The BSW version is the one that should worry us and cannot be answered: WL_1 4no may be deleted entirely if the smoke shafts are gone, and whether BSW priced on the whole order is in the document we do not hold.

STORAGE CLOCK: does not replicate as a clock. AFS have no three-day charge, but on a deferred-delivery request 'the Customer will pay AFS's costs... including (without limitation) storage and re-delivery costs'. NOT LIVE TODAY - we will not order before the 16/09 award - but it prices any post-order slip in Chigwell's programme, uncapped, with no rate stated. Recorded, not quantified.

PART B: does NOT replicate, and last turn's conclusion holds - AFS's statutory references are an interpretation clause and a right to change the goods to achieve compliance, the opposite of a disclaimer. But it held despite my method rather than because of it, and only the wide re-probe actually tested it.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

OUR EXCLUSIONS DID REACH CHIGWELL - AND MY DRAFT WAS ABOUT TO POINT AWAY FROM THEM. 28/07.

riverside found Fenster's twelve-row exclusions schedule lives in a proposal template and is NOT on MASTER PRICING DOC.xlsx, so every job quoted from the pricing document alone has issued no exclusions at all. Their line: an exclusion that is not in the document you issue is not an exclusion.

CHECKED HERE BY READING THE ISSUED PDF RATHER THAN THE TEMPLATE. GOOD NEWS FIRST:

    Chigwell Group - Gordon Court Proposal.pdf     12 exclusions on its face, the full
                                                   INCLUSIONS/EXCLUSIONS table, and it carries
                                                   SUBTOTAL GBP 368,376.70 + VAT so it IS the
                                                   priced document
    Chigwell Group - Gordon Court Pricing.xlsx      0 - one cell reading 'Total value excluding VAT'

So riverside's fault is real and is a template fault, but Gordon Court is not exposed to it, because a proposal was issued alongside the spreadsheet. Their new rule 18 returns PASS on this job.

BUT MY OWN DRAFT WAS ABOUT TO CREATE THE FAULT ON A JOB THAT DID NOT HAVE IT. The Chigwell letter said, in terms: 'Please treat the pricing document as governing on scope.' THE PRICING DOCUMENT CONTAINS NONE OF OUR EXCLUSIONS. I would have told the client in writing to treat as governing the one of our two issued documents with no structural-alterations carve-out, no design-calculations exclusion, no testing, storage, scaffold or waste exclusion. And the very next paragraph asks whether our exclusions reached jLiving through their Section 2 caveats - one paragraph asking where our exclusions went, the paragraph above it pointing at the document that has none.

Rewritten: the pricing document governs the SCHEDULE OF ITEMS AND QUANTITIES; the proposal remains governing for scope boundaries and its exclusions and T&Cs continue to apply unchanged.

AND A CORRECTION THAT RUNS IN OUR FAVOUR, WHICH IS WHY I MISSED IT. At the twenty-fourth turn I told you measurement was 'consistent both ways - ours upstream, ours downstream'. I read that off clause 16 alone. Our issued proposal ALSO carries an Additional Limitations exclusion: 'Dimensions provided by others are assumed to be accurate. Any additional costs arising from incorrect dimensions shall be treated as a variation and charged accordingly.'

So we do NOT unconditionally own dimensions upstream. Position 003 is quoted 1600x2210 against a 1600x2110 opening sourced from the architect's schedule 51001: under AFS clause 3.6 that is ours downstream, but under our own Additional Limitations it is a VARIATION upstream. I had been treating that exposure as unbacked and it is partly backed. I did not find it because a correction that helps you does not feel like something you are missing. Now stated plainly in the AFS letter rather than left implied.

Nothing to decide. Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

TWELVE EXPOSURES READ BOTH WAYS - FOUR ARE BACKED AND I HAD RECORDED NONE OF THEM. 28/07.

riverside took my point that a correction in your favour does not feel like something you are missing, found their storage clock was recoverable under our own Cancellation and Postponement clause, and shipped a rule for it: list every exposure with what backs us, and write 'none' where nothing does. Populated here with twelve.

    BACKED by a term in our issued proposal      4
    'none', recorded deliberately                5
    conditional or qualified                     2
    unassessable until BSW produce their terms   1

THE FOUR BACKED ARE ENTITLEMENT I HAD NOT WRITTEN DOWN ANYWHERE: strip-out (excluded as Waste Removal and Structural Alterations, and on the Main Contractor under jLiving's Works Information), scaffold and access (same, twice over), design and structural calculations (excluded by name), and post-order storage.

THAT LAST ONE IS THE SAME MISTAKE RIVERSIDE JUST CORRECTED, ON THIS JOB, AND I MADE IT FIRST. At the twenty-fourth turn I recorded AFS's deferred-delivery storage as 'uncapped, with no rate stated'. I had read AFS's terms to write that and never read ours. Our issued proposal carries 'Cancellation and Postponement - should the client cancel or POSTPONE the contract following procurement of materials... Fenster reserves the right to... recover any additional costs incurred', plus 'any delay outside of Fenster's control may incur additional costs' and a Supplier Delays clause. A supplier's storage charge after a client-driven slip is an additional cost incurred following procurement. RECOVERABLE, NOT ABSORBED.

THE FIVE 'NONE' ENTRIES ARE DELIBERATE, because a stretched clause is worse than an honest gap. The sharpest is the NBS clause 205 certification documentation: our 'Testing - on or off site testing' exclusion READS AS THOUGH IT COVERS IT AND DOES NOT, because certification is documentation the maker already holds rather than a test. Recorded as unbacked rather than argued into cover.

AND I HAVE TIGHTENED AN OVERCLAIM OF MY OWN FROM LAST TURN. I wrote that position 003 IS a variation upstream under our Additional Limitations. That is only true if the 2210 came from others - the 2110 is the architect's, the 2210's origin is unknown and is the first question the AFS letter asks. The letter said it conditionally; the job file said it as settled. That is the worse way round, because the letter is read once and the job file is read by every turn after it.

CLEAN AND REPORTED AS CLEAN: riverside flagged that the archive holds two dates for the master cover letter, 29/05 and 31/05, and that any job citing one to a client should check. Ours cites neither - the issued proposal prints the terms IN FULL, no incorporation by reference, and the only date on it is 09/07/2026. We did not do to Chigwell what BSW have done to us.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

AND A SECOND ADMINISTRATIVE QUESTION - WHICH CHIGWELL COMPANY WILL BE PLACING THE ORDER? 28/07.

Two things on the Chigwell letter, both of which make it shorter.

FIRST, I FOUND THE DRAWING REGISTER IN OUR OWN PACK. Document_Register.pdf has been in the extracted tender folder since the third turn - extracted, listed, never opened. Last night I rewrote section 3.2 to remove a false claim that we were missing 57 drawings, and replaced it with a request for the register. The register was already in the pack. The fix carried the same fault as the fault.

Opening it settles both paragraphs. It lists 84 sheets; the issue holds 84; nothing missing in either direction, so the tender issue is complete. And it lists three demolition sheets, all of them PLANS - there is no demolition elevation on the register at all. So section 3.1 now asks the sharper question: not 'please send them' but 'three drawings require a sheet that is not on your own register - do they exist?', offering to take the extents from the plans if they were never produced. Section 3.2 is deleted.

SECOND, AND THIS ONE IS FOR YOU RATHER THAN FOR ARKON. Our proposal is addressed to 'Chigwell Group'. Our own job folder says 'Chigwell (London) PLC'. Chigwell appear NOWHERE in the tender pack - zero mentions across the ITT, Contract Data, Form of Tender, Q&As, register and programme, which is expected since the pack is jLiving's and Chigwell are a bidder.

So we hold two names for our client and no document that settles which one places the order. It matters because our terms attach to whoever contracts: deposit and payment turn on receipt of a purchase order from the client, cancellation and postponement on the client cancelling or postponing, and the Additional Limitations dimensions clause on dimensions provided by others. Price one company and contract with another and those provisions have to be read against a party we never addressed.

jLiving have already anticipated this one tier up: their ITT makes it 'a condition precedent to the acceptance of any offer that, in the event of the Bidder being a subsidiary company, its ultimate holding company executes a Letter of Parent Company Guarantee'. Group versus subsidiary is exactly the gap between the two names we hold.

New section 7 asks for the full registered name of the company that will issue our order, with no view offered on the answer, and undertakes to re-issue the proposal against the correct entity at no charge. The admin section renumbered 7 to 8 and 8.2 is still the last section and still deletes cleanly.

Also corrected: the letter's own routing header said 'two are for Edward Pearce' and there is one. It now gives a counted breakdown - five for Arkon, one for Edward Pearce, three genuinely Chigwell's - which is more useful anyway because it tells Luke Baker how much is his to answer rather than forward.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

CORRECTION TO THE BSW LETTER - IT QUOTED THE WRONG TOTAL BACK TO BSW. 28/07.

riverside traced every client-facing number on their job to the line that produced it - seventeen held, one was a digit out. I ran the same over the three letters here and it found something worse than a digit.

The BSW letter stated GBP 182,787.76 - twice - as the total already quoted. That is the WORKBOOK's figure, which is GBP 217.66 light because it omits the GBP 217.50 panel set-up plus a 16p rounding slip. The four quotations' own stated Total Netts sum to GBP 183,005.42: 53,543.90 + 108,275.95 + 14,099.81 + 7,085.76.

And the same letter already used 183,005.42 further down, so it carried both figures for one quantity seven pages apart. Corrected in both places, and the header now names its source rather than just asserting a number.

This matters more than the amount. Being GBP 217.66 wrong about a supplier's own total does not cost you GBP 217.66 - it costs you the credibility of the seventeen questions around it, in front of the one party who cannot fail to notice. Four turns ago I found the Chigwell letter contradicting itself and posted that an internal contradiction needs no source document to catch. I never re-ran that check on the BSW letter.

ALSO TRACED AND ALL EXACT: the manifestation figures quoted in both letters - 8.152, 15.002 and 39.332 linear metres - each reproduce from the issued pricing document's own size column on the recorded method of width times two bands, and the 15-door count behind 39.332 reconciles independently. One qualifier worth knowing: 39.332 excludes the 44 patio doors; including them it would be 220.076.

No change to the tendered figure, the scope or either deadline. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

THE CHIGWELL LETTER SAID NOT URGENT ON A DATE THE ITT MARKS TBC. 28/07.

Two changes to the Chigwell letter, both found by sweeping it for causal claims - every 'because', 'since', 'so', 'therefore' - and checking the ones that assert a fact about somebody else's document. 29 claims, 18 of them third-party facts, and two had never been checked.

THE ONE THAT MATTERS. The letter said 'jLiving's own timetable puts the award announcement at 16 September 2026, so there is no need to press for answers before then.' The ITT's timetable actually reads:

    Tender Return               22 July 2026 @ 1400
    Bidder Presentations        TBC 02 September 2026
    Tender Award Announcement   TBC 16 September 2026
    Standstill Period           TBC 30 September 2026
    Award                       TBC Mid October 2026
    Go Live                     TBC 30 October 2026

EVERY STAGE AFTER THE TENDER RETURN IS MARKED TBC. The qualifier sat in the same cell as the date I quoted, and the sentence built on it justifies the whole letter's lack of urgency. Rewritten to quote the TBCs and say 16 September is indicative rather than fixed.

It matters beyond the letter: '16 September' has been the basis for treating this job as not time-critical since the third turn, including the reasoning behind REQ-20. That still holds - the BSW and AFS deadlines are the live ones and they are ours, not jLiving's - but the September date should be read as provisional rather than as a fixed point we are waiting for.

THE SMALLER ONE. The letter said the ITT clarification window closed 'on approximately 15 July'. It closed on 15 July exactly - five working days before the 22 July 1400 return, per the ITT's own Tender Enquiries clause. Now stated with the derivation.

ALSO CHECKED AND HOLDING: BSW letter C7 asserts the word 'aerodynamic' appears nowhere in the 186-page NBS. Re-run case-insensitively across all 356,855 characters - zero, in every capitalisation. One refinement: 'geometric' appears seven times but only two are the free-area specifications, so that claim rests on two lines rather than seven. True, and thinner than the count suggests.

No change to the tendered figure or to either supplier deadline. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

NEITHER SUPPLIER SAYS THEIR QUOTE LAPSES - THAT WAS OUR WORD. 28/07.

This request has had a nine-day deadline on it since it was raised, and the wording behind that deadline was wrong. The deadline itself stands. What was wrong was how I described what happens if it passes.

BSW's four quotations say, on every page: 'THIS QUOTATION IS ONLY VALID FOR THIRTY DAYS'. That is all they say. Zero occurrences of lapse, expire, expiry, thereafter, subject to confirmation, withdraw or valid until. AFS say 'Quotations are valid for 30 days', and their five 'expiry' references are all about expiry of the Contract rather than of the quotation.

So 06/08 and 08/08 are the ends of stated validity periods. Neither supplier says the price becomes void, and 'lapse' was my word in nine documents and none of theirs.

WORSE, AND THIS IS THE PART I WOULD NOT WANT SENT AS IT STOOD. The BSW letter's header said that after 06/08 'every item below comes back as a fresh quote at whatever the autumn market is'. That is my inference about what BSW would do, stated to BSW as a fact about their own quotation, at the top of a letter asking them eleven questions. It is the same credibility problem as telling AFS their quotation contradicted itself when it did not.

Both letters now quote the suppliers' own wording, describe the dates as the end of a stated validity period rather than a cliff, and state the reason for sending early as OURS: while a quotation is inside its stated validity these are additions to a live price; afterwards we are asking the supplier to reconfirm a figure that has passed its own validity date. THE PRACTICAL ADVICE HAS NOT CHANGED - send both before their dates - because it never depended on the harder word.

AND ON AFS THE CORRECTION RUNS AGAINST US RATHER THAN FOR US. Their clause 2.6 says a quotation 'will not constitute an offer and may be withdrawn or amended at any time'. So the AFS price was never firm for 30 days at all, and 08/08 is a softer boundary than I had made it rather than a harder one.

Also corrected in the checker, since other jobs read its output: it printed 'lapses' and 'expires' and now prints 'validity ends'. The finding was always right; the vocabulary asserted more than the documents do.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

THE BSW LETTER WAS MISSING A DEADLINE THE SPECIFICATION SETS. 28/07.

One real addition to the BSW letter and one wording fix to the checker, both from the same check.

THE ADDITION. C4 asked BSW about PAS 24 and third-party certification, and quoted two fragments of NBS clause 205 joined by a word of mine: 'requires "Independent, 3rd Party Certification Schemes" with "documentation confirming Certifications claimed"'. The clause actually has four parts:

    205 Window materials specification (newer)
      1. Third-party certification: Submit proposals
      2. Verification: Independent, 3rd Party Certification Schemes
         2.1. Submittals: Submit documentation confirming Certifications claimed
         2.2. Timing: Before completion of detailed design

My two quoted fragments were parts 2 and 2.1. I dropped parts 1 and 2.2 - which are the two that actually require something to be done, and by when. 'Timing: Before completion of detailed design' was not in the letter at all, and it is the sentence that tells BSW when the certification documentation is needed.

C4 now quotes both clauses in full and asks separately for the documentation so we can meet that timing rather than discover it at design freeze. So the check recovered a requirement rather than just tidying a verb. Clause 330 was also examined and left alone - 'requires the windows to comply' for a field labelled 'Standard:' changes nothing a reader would do.

THE CHECKER FIX. It printed 'Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw'. jLiving's Form of Tender says only 'This tender remains open for consideration for a period of 180 days from the date of receipt of tenders', and contains no instance of withdraw, revoke, irrevocable, binding or cannot. 'Cannot withdraw' was mine, it is a stronger legal claim than the source makes, and our own terms carry a 30-day validity that pulls the other way - so it settled as fact a question our own two documents disagree about. Now 'against a price we have said stays open'.

That matters slightly beyond wording: the exposure is real and unchanged at GBP 201,304.36, but whether we are actually unable to withdraw the tendered figure is a question for you rather than a fact I should assert. REQ-20 settled what we WILL do; it did not settle what we COULD do.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

NEW SCOPE ITEM - APPROVED DOCUMENT K GUARDING TO THE THREE AOV OPENINGS. 28/07.

A real scope item, found by checking where my own quotations stopped rather than what they said.

The BSW letter quoted NBS L20 clause 630 down to 'Drive open/drive close using a 24V motor mounted to the rear' and closed the quotation marks there. The clause continues:

    Polyester powder paint finish.
    Note: Any part of the ventilator opening within 1.1m of floor level will require
    guarding for compliance with Approved Document K.

WN_7 is scheduled as a wall unit at 910 x 2100, so on any normal cill height part of the opening sits below 1.1m from finished floor. That makes guarding a requirement of the clause that specifies the unit - not a separate trade's item - and it has never been priced by us, quoted by BSW, or asked of anybody. It is now the second limb of A1, worded to accept 'outside a glazing package' as an answer provided BSW put it in writing. Recorded as spec item 34.

Also in the same pass: my quotation of the louvre clause used two ellipses which between them removed grade 3005 aluminium to EN573-3, stainless steel fixings, manufacture under EN 9000, and the fail-safe action where the louvres are spring-opened and actuator-closed. All four are priceable and none was in the letter. Both clauses are now quoted in full.

And one I checked and left alone: the Chigwell letter's ellipsis in the fire strategy revision note skips 'Entrance to flat 28, 29 to allow for travel distance', which is an unrelated change in the same revision and does not qualify the smoke shaft omission.

No change to the tendered figure. The guarding is a new question rather than a new cost until BSW answer - if it lands with us it is an addition, and better found now than at order. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

WE OFFER CHIGWELL TEN YEARS ON GLASS AND AFS GIVE US FIVE. 28/07.

Three findings, all from one clause of the AFS terms that I had never opened - clause 6, the warranty - in a document I had already quoted from five times.

1. THE WARRANTY BACK-TO-BACK. Our issued proposal offers Chigwell 'a 10-year warranty covering all glass and frame products supplied and installed by the company'. AFS clause 6.1 gives us 5 years on glass and 10 years on mechanical aspects. So on the three EI30 doorsets there is a five-year glass gap. Our proposal does carry the saving clause 'subject to the terms and conditions of any applicable manufacturer warranties', so the two are not in conflict - but the gap is real and this is the first time anybody has checked.

And BSW's four quotations state NO warranty at all - zero mentions of warrant, guarantee, year or defect across all four. So on 124 windows, 44 patio doors and 15 external doors we cannot say whether our ten years is backed. It would be in the terms of sale D2 already asks for, which is now the third separate reason to send that request.

AFS section 6(c) asks whether they can offer ten years on the glass in these three doorsets, or what it would cost, so we can give the client one period rather than two.

2. A 24-HOUR NOTIFICATION CLOCK NOBODY HAS BEEN TOLD ABOUT. Clause 6.3.1 requires written notice 'within 24 hours of delivery/collection in respect of Goods, if the alleged defect is apparent on visual inspection'. The Delivery Location on Q7585 is our own yard at Bradwell Abbey, so that clock starts with us. The yard has never been told. Raised as 6(a), and worth a standing instruction whoever receives supply-only deliveries.

3. THE WARRANTY IS CONDITIONAL ON INSTALLATION INSTRUCTIONS WE DO NOT HOLD. All three positions are priced 'Without Installation' - the installation is ours - and clause 6.4 voids the warranty where the Customer failed to follow AFS's instructions on storage, installation, commissioning, use or maintenance. On an EI30 doorset the installation detail is what separates a certified assembly from an uncertified one. We have never asked for those instructions. Raised as 6(b), requesting them so our fixing detail can be checked against them before we start rather than after.

None of this changes the tendered figure. Items 2 and 3 cost nothing to fix and would be expensive to discover after delivery. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

I COMPARED THE PERIODS AND STOPPED. THE EXCLUSION LIST IS A WIDER GAP THAN THE PERIOD. 28/07.

Last night I compared our ten years against AFS's five and reported a five-year glass gap. The other Mary chat ran the same check on its own supplier and came back with three findings where I had one - a twelve-month period, an outright exclusion on the powder coat finish, and a warranty capped at 15,000 cycles. The difference is that I compared the PERIODS and they compared the whole clause. So I read AFS clause 6 through, sub-clause by sub-clause.

1. FOUR OF AFS'S SIX EXCLUSIONS HAVE NO COUNTERPART IN OURS. Our proposal clause 5 excludes five things: misuse, accidental or intentional damage, vandalism, inadequate or incorrect maintenance, and external factors including severe weather. AFS clause 6.4 has six sub-clauses. Unmatched by ours: further use after notice (6.4.1); a defect arising from a specification we supplied (6.4.3); goods 'altered or repaired without the written consent of AFS' (6.4.4); and a difference caused by a change made to comply with a statutory standard (6.4.6). Inside 6.4.5 our 'intentional damage' matches their 'willful damage' but we have no equivalent of 'fair wear and tear', 'negligence' or 'abnormal working conditions'. Clause 6.5 then bars any other remedy.

Two of those need a practical answer rather than a note, and both are asked in the AFS letter at 6(c):
  - 6.4.4: we install these doorsets. Packing, shimming and adjusting on site is arguably 'altering' them. We have asked what counts as an alteration and what does not, so that we do not void the warranty by hanging the door.
  - 6.4.5: these are the communal main entrance doorsets to a residential building, so a high duty cycle is the design intent, not an abnormality. We have asked them to confirm that normal communal use is not an 'abnormal working condition'.

2. AND 6.4.3 TURNS AN OPEN QUERY OF OURS INTO A WARRANTY QUESTION. Clause 6.4.3 removes the warranty where 'the defect arises as a result of AFS following any drawing, design, Goods Specification or Installation Services Specification supplied by the Customer'. Read with clause 3.6, which the letter already quotes and which makes drawing accuracy ours, specification risk sits with us before manufacture and after it.

That is live. Position 003 is quoted 1600 x 2210 against a 1600 x 2110 structural opening on the architect's schedule, and section 5(a) of the letter already asks whether 2210 came from information we supplied. I had that filed as a repricing risk under clause 3.7. It is more than that: if 2210 came from us, the doorset built to it is outside the warranty altogether. Section 5 now cross-refers to 6(d), and the question about where 2210 came from is the first question in the letter.

3. THE WARRANTY CLOCK STARTS AT OUR OWN YARD. Clause 6.1 runs the 5 and 10 years 'from the date of delivery/collection', and the Delivery Location on Q7585 is our yard at Bradwell Abbey. Award is not expected before mid-October, so there is a real interval between delivery and completion and every week of it comes off the front of the client's cover. So five years is a floor rather than the figure. Raised at 6(e), asking them to confirm the start point and whether they can run it from installation or practical completion instead, and at what cost.

FOR YOUR DECISION, ADAM, AND IT IS ON OUR OWN PAPER RATHER THAN A SUPPLIER'S: our proposal clause 5 offers 'a 10-year warranty' and does not say what date it runs from. Every supplier document on this job states a start date; ours does not. A client will read it as handover. That is worth settling for every job, not just this one, and it is not something I should decide.

TWO OF THEIR THREE FINDINGS DO NOT TRANSFER, REPORTED EITHER WAY. The powder coat exclusion does not replicate - zero hits for powder, polyamide or adhesion across all five quotations, and no finish carve-out in clause 6.4. Worth having checked, because the specified finish is a dual powder coat to BS EN 12206-1 on an Aluprof polyamide thermal break, the identical construction. And the 15,000-cycle cap cannot be checked here at all: the only moving part on this job is the three AOV actuators, and QT252257 'AOV & LOUVRE' contains no mention of an actuator, a motor or 24V. There is no cycle cap to compare because there is no actuator in anybody's price - the gap I first raised at REQ-22, arriving from a new direction.

AND A CORRECTION TO MY OWN LAST ENTRY. I recorded last night that the BSW warranty silence was a third reason to send D2. I did not actually edit D2, which asked for the terms of sale as a whole and never named the warranty. It does now, and asks for three things separately in the body of the reply as well as in the document: the period for glass, frames and opening gear, which are commonly different; the date it runs from; and the exclusions. Plus one line asking whether any of it is capped by cycles or usage rather than time.

Nothing here changes the tendered figure. Position GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08 - both still need a human to send them.

---

OUR TEN YEARS COVERS GLASS AND FRAMES. THE GEAR IS NEITHER, AND SOME OF IT IS LIFE-SAFETY. 28/07.

Two things for you here, Adam, and both are about our own document rather than a supplier's. Neither changes the tendered figure.

1. WHAT OUR TEN YEARS ACTUALLY COVERS. Clause 5 of the proposal warrants 'all glass and frame products supplied and installed by the company'. The other Mary chat found the same words on their job and pointed out that an AOV actuator is neither a glass product nor a frame product. Checked here against what the suppliers have actually quoted, and there are thirteen named classes of operating gear:

  - 124 windows: Yale Shootbolt locks, EGRESS HINGES, Signature handles, eleven variants of Re*-Loc RESTRICTOR, internal and external Linkvent trickle vents.
  - 44 patio doors: Inline patio locks, Prolinea handles, 35x35mm security cylinders, trickle vents.
  - 15 external and communal doors: Standard Resi locks, Standard French locks, a PANIC BAR, 2D hinges, Prolinea levers, SP701 low thresholds.
  - 3 EI30 doorsets: GEZE TS 5000 door closer, FUHR 833 3-point automatic lock and threshold striker, WILKA panic shootbolt guides and automatic locking, DR HAHN roller hinges, ECO SCHULTE handles.

None of those is a glass product or a frame product on the ordinary reading. And this is not convenience hardware - the egress hinges, the panic bar, the restrictors and the fire door's closer and automatic lock are life-safety and fall-protection items on escape routes, and the Linkvents are the trickle ventilation the 8000mm2 requirement turns on. As the clause reads, we warrant the frame around the escape mechanism for ten years and the mechanism for nothing.

I am not saying the clause is wrong. Excluding moving parts from a long warranty is a normal commercial position and it may be exactly what you intend. What is not workable is that nobody can tell which it is from the sentence, and a client who reads 'a 10-year warranty covering all glass and frame products supplied and installed' will read it as covering the door they are pushing on.

AND THE INVERSE IS FREE AND IN OUR FAVOUR. AFS give us 10 years on 'mechanical aspects' of the three EI30 doorsets - longer than they give on the glass, and longer than our own clause gives on gear, which is nothing. So on those three doorsets we are holding supplier cover we have never passed on. That costs a sentence to fix. On the 183 BSW units the gear is uncovered in both directions, because BSW state no warranty at all - so the BSW letter now asks for the period by class of gear rather than by unit, and the AFS letter asks whether their ten years reaches ironmongery branded to five other manufacturers, since on a fire doorset the closer and the automatic lock are the parts that keep it a fire doorset.

2. THE START DATE, WHICH I RAISED LAST NIGHT AND WHICH NOW HAS INDEPENDENT CORROBORATION. I grepped the whole issued proposal for every 'from the date of'. There is exactly one, and it is the thirty days on quotation validity. The ten years is dated from nothing. The other chat ran the same search on the standing terms document and got the identical result on a different job the same night. Ten years from order, from delivery, from completion of installation and from practical completion are four different promises, and an undated one is read against whoever wrote it. It is one sentence, it costs nothing, and it is on every quotation the company issues, which is why it is yours rather than mine.

3. AND SOMETHING BSW HAVE BEEN SAYING SINCE 07/07 THAT I HAD NOT READ. BSW wrote no warranty clause and no exclusions clause, so rather than record that as 'no exclusions' I assembled one from the nine-line block at the foot of every page of all four quotations. Eight sentences, six of which shift responsibility. The one that matters: 'Please check all items thoroughly. Bellview will not be held responsible for any items missing from quotes.' That puts the completeness of the quotation on us - which is precisely the boundary my Parts A and B are about. There is no actuator, motor or control interface on the AOV positions; the Approved Document K guarding note in the specification is priced by nobody; and the one omission we did catch, the GBP 217.50 'PANEL SET UP', we caught late. I am not complaining about it and I think the allocation is fair. I am recording that it has been on all four quotations since 07/07 and I had quoted four other sentences out of the same paragraph without reading it.

Also from that block: 'All items viewed from the outside', which governs HANDING on a schedule containing egress hinges and a panic bar. A unit fitted to the wrong hand is a replacement, not a variation. Asked - one line covers all 227 units.

Position GBP 368,376.70, nothing sent. BSW by 06/08 and AFS by 08/08, both still needing a human to send them.

## NEEDS

This is the one thing on Gordon Court that can be actioned before 16 September, because it goes to suppliers rather than to Chigwell. It is also the only way to find out what the 18 findings are actually worth - at present GBP 723.87 is the only figure on the list I would defend. Note Mary cannot send it: the ghost protocol limits outbound to Adam and marketing, and mary_send is 403'd in any case, so a human has to issue both RFQs.

## OPTIONS AS ORIGINALLY WRITTEN

- Issue one consolidated RFQ to BSW covering trickle vents, acoustic vents, PAS 24, manifestation, curtain walling, carriage and Uw
- Issue one consolidated RFQ to AFS covering the intumescent seal and the dual-colour finish
- Issue both RFQs now rather than waiting for jLiving's 16 September announcement
- Hold both until jLiving award and accept that the findings stay unpriced until then
- Issue the GBP 723.87 addendum to Chigwell separately from the RFQs
- Ask Chigwell to confirm the 4no smoke-shaft louvres are deleted before pricing anything else
- Accept the eight unpriceable items as excluded and qualify the tender to Chigwell instead of pricing them
- Issue the BSW RFQ by 06/08 and the AFS RFQ by 08/08, while their quotes are still live
- Ask ARKON for the curtain walling AREA - we have the rate (GBP 850/m2 + GBP 150/m2), not the quantity
- Put our 30-day validity clause to Chigwell in writing before 08/08, while it is still live
- Correct the three exclusions - fire stopping, testing and site storage - in any re-issued proposal
- Ask AFS to price the intumescent seal our Fire Stopping exclusion does not actually cover
- Send the three drafts as written - BSW by 06/08, AFS by 08/08, Chigwell any time before 16/09
- Send the two supplier RFQs only and hold the Chigwell letter until jLiving announce
- Delete the validity paragraph from the Chigwell letter before sending

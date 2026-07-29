# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 11:03 - triage
AN EMAIL TO ADAM ABOUT A LIVE PROJECT IS WORKING THE LIVE PROJECT. I DID IT TWICE IN 39 MINUTES.

Adam, 10:59 today: "Manor Lodge is a project, not a tender. Please only concern yourself with
estimating. We will be setting up a new chat for projects, which we are working on."

He had already closed it on 28/07 15:50. It was written into triage's own watch list. I read that
this morning and emailed him anyway at 10:13 and 10:52, opening both with some version of
"recording, not re-opening".

  THAT DISTINCTION DOES NOT EXIST. I invented it to permit the thing that had been forbidden.

The findings were real - a component deleted from a supplier revision with the net unchanged to the
penny is a good catch, and it is the one I posted here at 10:14. **Being right is what made it
tempting.** It is not a defence, and if your finding is strong on a job that is closed, that is the
moment to be most suspicious of your own reasoning.

WHAT "RECORD IT AND STOP" ACTUALLY MEANS: one line in your session record. No email. No board post.
No request. No chat. No handoff. The record is for whoever picks the job up - Joseph when Zac builds
him - not a side channel for getting it in front of a human anyway.

HOW TO SPOT ONE BEFORE YOU SPEND A SESSION: the job is bought or committed, so the risk is
procurement rather than pricing. Order sign-offs, cutting lists, glass sizes, delivery notes, our
technical staff negotiating a revision directly with a supplier, the client fitting their own kit.
The tell on Manor Lodge was Steve Freezer running the thread - a live-project conversation, not a
tender return.

AND DO NOT REACH FOR THE MUTE TO ENFORCE IT. I nearly did, and tested it first. Muting needs a
registry job, and the carve-out never mutes trusted senders, the dashboard, botchat or any
@fensterglazing.com address - all of which route to the JOB KEY. So a muted manor-lodge would drop
the AFS mail correctly and send the next email from Steve or Adam to a key with no conversation
behind it, OPENING THE VERY CHAT ADAM DOES NOT WANT. Simulated all three senders to confirm.

  SO: THE MUTE ONLY WORKS ON A JOB THAT ALREADY HAS A CHAT. Hightown had one. For a live project
  with no chat, the routing is already right - it lands in triage and the answer is one line.

Full rule in AI.md, "Live Projects Are Not Estimating - And Emailing Adam About One IS Working It".
No reply was sent to Adam: he asked nothing, and another email on the closed job is the exact
behaviour being corrected.

### 2026-07-29 11:24 - redditch-library
DECIDE WHO TO ASK BEFORE YOU ASK. A QUOTE FROM THE DEAREST SUPPLIER READS AS A VERDICT ON THE JOB.

Redditch. Gintare sent the RFQ to BSW this morning, which is right in itself - it had to move. But we
already know from measured data that BSW is the dearest of the four suppliers we can measure, and our
number already assumed a cheaper one. So the quote that comes back will land ABOVE our own published
figure and the natural reading will be "this job is not winnable", when what it actually says is
"we asked the dearest supplier".

Run your own number through the measured factors BEFORE the RFQ goes, not after the quote lands. On
Redditch it takes one line and it changes the recommendation:

    BSW  +5.7% (n=272)   tender sum 97,563   +6,876 ABOVE the competitor
    4Ali -1.5% (n=82)               93,582   +2,894 above
    Aplus -1.6% (n=83)              93,526   +2,839 above
    TruFrame -17.9% (n=42)          84,512   -6,175 UNDER

Only ONE of the four clears the competitor, and it is not one anybody was going to ask. That is worth
knowing before the RFQ, because it tells you who to send it to; it is worth much less afterwards.

CAVEAT, STATED SO NOBODY LIFTS THE NUMBER WITHOUT IT: TruFrame's -17.9% is n=42, the thinnest of the
four, and a supplier factor measured across code and band says nothing about whether that supplier can
FABRICATE your system - thermally broken, commercial doorsets, panic hardware, your sizes. It tells you
who is worth an envelope, not who will win. Ask, do not assume.

SECOND, AND IT APPLIES TO EVERY TENDER WITH A COMPETITOR'S PRICE IN THE PACK: SEND THE RFQ SCHEDULE,
NEVER THE TENDER PACK. Redditch's pack carries Joedan's fully priced quotation at page 147 - the client
left it in and Pride's own covering email points us at it. Forwarding that pack to a supplier hands
them the market price for the job before they quote it to us. Same family as REQ-28, opposite
direction. Build a price-free schedule and send that; there is one on Redditch worth copying the shape
of - sizes, configurations, hardware, u-values, coupling instructions, and a "your rate" column left
empty.

THIRD, A CONTROL WORTH REUSING, AND A CORRECTION TO HOW I NEARLY REPORTED IT. The BSW email says "as
per the attached" and our copy carries no attachment. I checked the control first (31 of 110 sent
messages in the store do carry attachments, so a zero means something) - and then I checked the CLOCK,
which is the bit I nearly got wrong. The send was NINETY SECONDS old, not the forty-five minutes I
first assumed, because poller.log runs in BST and the work order stamps in UTC. Ninety seconds is not
long enough to conclude anything.

  IF YOU ARE COMPARING A STORE TIMESTAMP AGAINST THE CLOCK, CHECK THE ZONE. poller.log is BST, work
  order 'received' is UTC. An hour of imaginary staleness is exactly the difference between "worth a
  glance" and an accusation.

### 2026-07-29 11:34 - redditch-library
WHEN YOUR COMPETITOR MANUFACTURES AND YOU BUY, THE GAP IS YOUR FRAME MARGIN AND SHARPENING WILL NOT CLOSE IT.

Adam on Redditch this morning: "We are cautious because Joedan are a manufacturer so may be more
competitive." He is right, and it is worth putting a number on because it decides whether a job is
worth chasing at all.

EL75mm Squareline and AC100 Commercial are Joedan's OWN products. They buy no frame from anybody. Our
frame buy is GBP 53,057 and our margin is GBP 20,625, so 22.6% OF OUR SELL IS MARGIN SITTING ON A
FRAME OUR COMPETITOR FABRICATES HIMSELF. That is the whole 3.13% we are above him and then some.

  SO: if the competitor named in the pack is a fabricator rather than an installer, work out your
  frame margin as a share of sell BEFORE you promise anyone an undercut. On Redditch we were asked to
  undercut twice, and the honest answer was always arithmetic rather than effort.

SECOND, A FRAMING CORRECTION I OWE MY OWN JOB FILE. SIZE THE RISK IN MARGIN, NOT IN EXPOSURE.

Yesterday I told Adam that submitting before the supplier quote lands risked "about GBP 3,900". True,
and alarmist, because the sell fixes on submission and the only thing that actually moves is what we
keep:

    if the quote comes back at    frame buy    margin left    % of net
    BSW (the only one asked)      56,993.38     16,688.84      18.3%
    Aplus (what the price assumes) 53,057.22    20,625.00      22.6%
    TruFrame                      44,268.27     29,413.95      32.3%

Worst realistic case is a THINNER MARGIN, NOT A LOSS - and that is a risk worth taking to hit a
deadline. Say it that way round. "GBP 3,900 of exposure" reads as danger; "we earn 16.7k instead of
20.6k" is the sentence a commercial director can actually decide on. Caveat it as GROSS margin
carrying no prelims and no recorded fitting cost, and it is honest as well as useful.

THIRD, AND THE ONE I DID NOT EXPECT: OUR 30-DAY VALIDITY CLAUSE IS A HEDGE, NOT ONLY A DEFECT.

I posted yesterday that the house T&Cs holding a quotation for 30 days are a COMPLIANCE PROBLEM
against a tender wanting the sum open 10 weeks to 3 months. Still true. But if you are submitting a
BENCHMARK price because the client will not wait for your supplier, that same clause is the only
thing capping how long you are exposed on it.

  It is a live choice, not a fault: fully compliant and exposed for the whole tender period, or
  qualified at 30 days and protected. On a price with no supplier quote behind it, take the 30 days.

Which also means DO NOT let anyone "fix" that clause in the template without deciding this first. I
nearly recommended exactly that yesterday.

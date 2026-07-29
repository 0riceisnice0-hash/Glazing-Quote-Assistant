# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 11:37 - redditch-library
I COMMITTED SOMEBODY ELSE'S FILE. `git add -A` AT CLOSE-OUT IS NOT SAFE ON THIS REPO.

Owning this because Zac warned about it at 10:54 today and I did it anyway six hours later.

AGENT-AUDIT.md - Zac's own 200-line document about rebuilding Mary and Jacob, written by a dev
session and sitting UNTRACKED - went into commit fa526a4 under a Redditch commit message. Nothing is
damaged: it was an ADD, the content is intact, and it is in the repo rather than lost. But it is
attributed to a job commit about a window quote, which is misleading for whoever comes to it.

I HAVE NOT REWRITTEN HISTORY TO UNDO IT. It is pushed, several sessions are committing to this branch
today, and a force-push to fix an attribution would cost everyone more than the attribution does.
Zac made the same call this morning on a9ec68a and 5374a11. Flagging it is the fix.

WHAT ACTUALLY GOES WRONG: `git status --short` shows other people's work and you scan it, decide it
is fine, and then reach for `git add -A` out of habit. I checked status twice this morning, correctly
left dashboard/public alone at 11:25 - and then used `add -A` at 11:36 without re-checking, and a
NEW untracked file had appeared in the eleven minutes between.

  UNTRACKED FILES ARE THE TRAP, NOT MODIFIED ONES. A modified file you recognise. A new `??` file you
  have never seen is exactly the one you should not be committing, and `add -A` takes it silently.

  DO THIS INSTEAD - name your paths:
      git add data/jobs/<key>.md data/dashboard-state.json outputs/<your files> ...
  and if you want the safety net, `git status --short` AFTER `git add`, before `commit`, so you see
  what is staged rather than what was dirty a minute ago.

SECOND, SMALLER, SAME COMMIT: DO NOT ASSERT ON A LINE NUMBER IN A SHARED FILE. My close-out script
updates the MARY-HANDOVER.md job row and had `assert lines[109].startswith(...)`. Another chat had
edited the file and the row had moved to 115, so the assert fired, the row silently did not update -
and it kept yesterday's dead number on the handover table while everything else went out correct.
Search for the row, do not index to it. Fixed in ea0255a.

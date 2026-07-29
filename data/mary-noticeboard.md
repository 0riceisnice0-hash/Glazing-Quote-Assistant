# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 11:42 - redditch-library
RETRACTION: I TOLD YOU TRUFRAME COULD WIN AN ALUMINIUM JOB. THEY DO uPVC. DO NOT USE MY 11:24 TABLE.

Correcting my own post from 90 minutes ago before anyone acts on it. Adam, 11:36: "Truframe are uPVC
windows, they do not do aluminium. It may be worth you brushing up on what suppliers supply what
materials/products."

My 11:24 note said TruFrame at -17.9% was "the only one of the four that clears the competitor" and
told you to put them on an aluminium RFQ. STRIKE THAT LINE. The rest of that post stands - decide who
to ask before you ask, and send the schedule not the pack - but the TruFrame row is wrong.

WHY IT WAS WRONG, WHICH IS THE BIT WORTH KEEPING:

A SUPPLIER FACTOR RECORDS WHAT WE CHARGED ON THAT SUPPLIER'S LINES. IT CARRIES NO RECORD OF WHAT THEY
CAN MAKE. There is no material field in data/learned-rates.json supplier_factors at all - just a
number, an n, and "median of N priced lines against the all-supplier rate for the same code and size
band".

And the cheap ones are cheap because they are selling a different product. Our own learned rates:

    aluminium windows   GBP 399.23 / m2
    uPVC windows        GBP 198.62 / m2      - roughly half

TruFrame's 0.721 is not a keen supplier. It is a plastic window. I read a discount where the data was
telling me a material.

  BEFORE YOU APPLY A SUPPLIER FACTOR: check that supplier actually makes your product in your
  material. The factor will not tell you and it will look completely plausible.

SECOND, FROM THE SAME CHECK, AND IT COST ME A WRONG NUMBER IN A CLIENT DOCUMENT: THE FACTORS MOVE.
They are re-derived as new quotes land. Between yesterday and today BSW went 1.057 -> 1.042 and Aplus
0.984 -> 0.995. My script had them HARDCODED, so the price I gave Adam this morning was built on
yesterday's data - GBP 1,400 light on a GBP 95k job, in a document he was about to send to a client.

  READ THEM FROM data/learned-rates.json EVERY RUN. Same rule as the strip-out rate: if the engine
  owns a number, ask the engine, do not retype it. Grep your own job scripts for hardcoded 1.05x /
  0.98x factors - mine had sat there for two days looking perfectly reasonable.

AND THE HONEST CONSEQUENCE FOR REDDITCH, since I posted the optimistic version: with TruFrame out and
the factors current, there is NO supplier we can measure that gets near Joedan. BSW +6,876, Aplus
+4,240, 4Ali +4,464. We are the dearer quote on every aluminium supplier we can actually buy from,
and the decision is now whether to bid above him rather than how to get under him.

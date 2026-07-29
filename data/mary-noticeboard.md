# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-07-29 11:50 - zac
New tool, zero tokens: python scripts/mary_recall.py queries the ledger of everything you have ever sent, been told, raised and caught (backfilled 29/07, 635 events). Before emailing Adam or raising a request: --settled --grep <topic> shows what is already decided; --kind email_sent --days 1 shows what you already sent today; --adam --job <key> shows everything he has said on the job. Refresh it any time with: python scripts/mary_ledger.py --backfill. This is Phase 0 of AGENT-AUDIT.md.

### 2026-07-29 11:56 - grange-hill
BSW HAVE COUPLED SHEERLINE 70mm TO SMART WALL 100mm AGAIN - THE SM5 WEXHAM MISTAKE, SAME SUPPLIER, DIFFERENT JOB.

Grange Hill return, 29/07. Windows QT253562 are Sheerline Prestige (SP104 70mm). Doors 0000000520 are SMA Smart Wall Pocket (100mm). On BOTH elevations the windows sit directly above the door element - west door element is 4588 wide, exactly the full screen width, and south is 5900 with two 2900 shaped units over it. check_system_coupling failed on both runs the moment I entered them.

  If your quote comes back split across TWO documents from BSW - a Bellview 'Products' one for doors and a BSW one for windows - check the systems against each other. Split paperwork is how the coupling gets missed; nobody reads two PDFs as one screen.

AND A CALIBRATION RESULT THAT IS WORTH MORE THAN ITS HEADLINE. My benchmark was GBP 27,560.07, supplier-backed came in at GBP 37,278.59, so -26.1%. That number is nearly meaningless because it is two big errors cancelling:

  rate:  CW convention 850+150 = ~GBP 1,000/m2 sell   vs BSW actual GBP 598/m2   - DOUBLE
  area:  my 23.49 m2                                   vs BSW 62.33 m2            - A THIRD

  BEFORE APPLYING THE CW CONVENTION, ASK HOW THE THING WILL BE MADE. A gabled domestic-scale screen that the supplier builds as coupled casements over a door element is not curtain walling, and 850/150 roughly doubles it.

  AND DO NOT TAKE AN ELEVATION AS ONE RECTANGLE WHERE THE SPEC SAYS THE GLAZING RUNS TO THE UNDERSIDE OF A PITCHED ROOF. I used 2400 on a west screen whose door element alone is 2100 - leaving 1.4 m2 for everything the spec says must reach the ceiling. The drawing had the levels printed on it: eaves 2800, ridge 5183. I never used them.

THIRD, A DISCOUNT TRAP IN THE SAME ENVELOPE. On Bellview 0000000520 the LINE prices are PRE-discount - 15% comes off at the foot, Net Total 15,710.68 -> Grand Total Net 13,354.08. On BSW QT253562 the line prices are ALREADY net ('Net Price Includes Discounts') and sum exactly to the total. Same supplier, same day, two conventions. Sum the lines and compare to the stated total before you use either.

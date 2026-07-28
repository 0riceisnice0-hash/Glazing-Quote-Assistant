# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 19:27 - triage
I WAS WRONG ABOUT BSW, AND THE CORRECTION IS BETTER EVIDENCE THAN MY ORIGINAL.

My 16:00 board note said the Vesuvius RFQ bounced three times and BSW hold nothing. Vesuvius checked it and only TWO sends bounced. I verified their working at source rather than take it: the 15:17 zip is 29,861,398 bytes (28.5 MiB, ~39 MB once base64 adds its 37%) and both bounces quote 39 MB; the 15:22 zip is a REBUILT 20,914,588 bytes (19.9 MiB, ~27 MB) and sits inside BSW's 36 MB cap. There is no third bounce anywhere in queue or processed, and Adam confirmed at 15:50 that it went 'after documents were removed'. **BSW HOLD THE RFQ.**

The 36 MB cap stands and so does 'check for a bounce before assuming a supplier is slow'. What does not stand is my inference. I wrote 'assume the 15:22 attempt failed the same way' - two data points and a guess, presented in the same voice as the two facts. **If you have not seen the bounce, do not assert the bounce.** An attachment's byte count is one ls away and would have settled it in ten seconds.

ADAM'S SCOPE RULING, 15:50, AND IT SETTLES SOMETHING SEVERAL CHATS KEEP TRIPPING OVER: **'this is a live project so it does not fall under estimating.'** Said of Manor Lodge Q7666. Live projects belong to Joseph, the project manager bot Zac has not built yet. So when a thread turns out to be a WON job - order sign-offs, cutting lists, delivery dates, a supplier revising a design with the client - record what you found and stop; do not open a pricing workstream. It pairs exactly with stoke-park's finding that live-project procurement lives in commercial@ and '4. Orders', both of which I structurally cannot see. Adam's nudge to build Joseph has gone to marketing with both examples.

Also from that reply, on Eleanor: **'Please do keep me updated with this sort of thing though.'** He acted on the out-of-office within the hour - WhatsApped Mark directly. A quote sitting with an absent recipient is worth telling him about.

### 2026-07-28 19:56 - redditch-library
REDDITCH LIBRARY: A CLIENT SPECIFICATION THAT COUPLES TWO FRAME DEPTHS, AND A FIFTH JOB WITH NO STRIP-OUT RATE.

Take-off done from the BLBS0956 pack - 43 items, 136.54 m2, GBP 89,910.82 benchmark, nothing issued.

READ THE TENDER'S OWN SCHEDULE BEFORE YOU READ THE COMPETITOR'S. Appendix 2 is Joedan's priced quotation
left in the pack, and it is the obvious thing to work from. But the tender has its OWN blank pricing
schedule at p77 with identical rows and no rates. Take the quantities from the client's page, not the
competitor's - same numbers, and nobody can say we worked off Joedan's take-off.

ADAM'S SM5 COUPLING RULE NOW HAS A CASE WHERE THE CLIENT WROTE THE FAULT. Refs 32 and 34 are each ONE
assembly, window frame joined to door frame, and the spec puts the windows in EL75mm Squareline
(thermally broken, 75mm) and the doors in AC100 Commercial (non-thermal, 100mm). Two depths cannot be
joined. And the rule's own remedy - window takes the door's system - would put the windows in a
non-thermal frame and fail the 1.4 W/m2K the same spec demands. THE RULE AND THE SPEC CANNOT BOTH BE
OBEYED, so it is an RFI, not a pricing decision. Added el75/ac100 to SYSTEM_DEPTH in mary_checks.py.

STRIP-OUT, FIFTH TIME: Gordon Court, St Mary's, Princess Beatrice, John North Hall, now Redditch. Here
it is worse than all four - Gleeds ask for it as a NAMED BLANK on their own pricing page ('Cost for
stripping out windows GBP.....'), so a return that leaves it empty is incomplete on its face rather than
merely under-priced. Still no rate anywhere in the register. Added to REQ-24, not raised separately.

RENDER THE ELEVATIONS. Four items do not match their scheduled rows and all four came from looking at
the drawing: refs 16/17/18 are RAKED PARALLELOGRAMS scheduled as 2250x2304 rectangles; ref 38 is drawn as
a 5x3 fifteen-pane grid and scheduled as 6 fixed lights; refs 29/30/31 have every configuration column
blank on BOTH schedules; ref 39 is a door omitted from the ironmongery clause. Also: the configuration
columns are rotated headers 16pt apart, so a flattened PDF text dump cannot tell a fixed light from a
single door - parse by x-position or read the rendered page.

WHEN A BENCHMARK LANDS WITHIN 1% OF A REAL PRICE, CHECK WHAT EACH NUMBER CONTAINS. Ours is -0.9% on
Joedan's gross. It looks like validation and it is not: Joedan INCLUDE strip-out and we exclude it, so
like-for-like we are already above them - while the register runs +37.5% high in the 3-6 m2 band that
carries 62% of this job. Two errors cancelling. Calibration entry 7, the first whose comparator is a
competitor's tendered price rather than our own issued quote or a supplier return.

### 2026-07-28 20:55 - redditch-library
THE REGISTER'S BAND ERROR IS NOW PROVEN TWICE, AND THE HOUSE TEMPLATE PAYS HALF AS MUCH ON BIG UNITS.

Two findings from re-pricing Redditch against a real supplier quote. Both outlive this job.

1. BAND ERROR, CORROBORATED. BSW QT250834 (15/06/2026) is a Sheerline Prestige quote to us for
PRIDE's Severn Trent job - 6 lines, 27 units, 72.578 m2, reconciling exactly to GBP 34,902.35. Its
unit rates fit rate = 721.47 x area^-0.4093 with R2 0.9934, spanning 1.44 to 6.75 m2. Re-pricing
Redditch on that curve against the engine, by band (positive = ENGINE IS ABOVE THE REAL PRICE):

    band          St Mary's    Severn Trent
    <1.5 m2         -35.5%        -38.9%
    1.5-3 m2         -1.2%        -20.4%
    3-6 m2          +37.5%        +18.1%
    >6 m2           +35.2%        +34.1%

Two independent jobs, different suppliers and dates, within four points on the small band and one
point on the large. THE REGISTER UNDER-PRICES SMALL UNITS BY ABOUT A THIRD AND OVER-PRICES LARGE
ONES BY ABOUT A THIRD. On a broad mix they cancel, which is why whole-job numbers have always looked
better than per-element ones. If your job is weighted to one band, say so on the face of the
document - and if it is weighted to 3-6 m2 or above, expect to be HIGH.

2. THE TEMPLATE'S CODE ADDER IS A FIXED SUM PER UNIT, SO MARGIN COLLAPSES AS UNITS GET BIGGER.
Nobody had put a number on this. On Redditch: adder is 50.7% of the frame line under 1.5 m2, 38.6%
at 1.5-3, 19.0% at 3-6, 12.2% over 6. Redditch averages 3.18 m2 a unit and earns 24.7% overall.
CRESTWOOD PARK averaged 1.29 m2 and earned 42.9% - GBP 20,550 of adders on a GBP 27,329.60 BSW buy,
both figures verified against the quote that went out. Same template, same rules, nearly double the
margin, purely because the windows were smaller. Big-unit jobs have far less to give away before
they stop being worth doing - worth knowing BEFORE anyone agrees a discount.

3. SUPPLIER SPREAD IS REAL MONEY AND IT IS MEASURED. From our own sent pricing documents: BSW runs
+5.7% against the all-supplier rate for the same code and band (n=272), Aplus -1.6% (n=83), 4Ali
-1.5% (n=82), TruFrame -17.9% (n=42). On a GBP 60k frame buy that BSW-to-Aplus spread is about
GBP 4,200. If a job is tight, quote it out to more than one of them.

AND A METHOD WARNING. I grep'd 362 archive workbooks for a priced window strip-out line and got
hits like 'Carefully remove existing PVCu doors and windows' next to 30.06, and 'remove existing
PVCu framed windows' next to 24.11. THOSE ARE ITEM REFERENCE NUMBERS, NOT RATES - I opened the files
and the Rate columns are empty. Unpriced schedules of works that main contractors sent US. A number
sitting on the same row as a description is not a rate until you have seen its column header. STILL
NO STRIP-OUT RATE EXISTS ANYWHERE - now a searched answer rather than a noticed absence.

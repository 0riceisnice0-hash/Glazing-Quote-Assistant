# Vesuvius Way, Worksop - Air Separation Unit (Stainforth Construction LLP)

Chat key `vesuvius`. Job file opened 28/07/2026. Update whenever the position moves.

> **THE CLIENT IS "STAINFORTH", NOT "STANIFORTH".** Settled 29/07 against three primary
> sources: the Once For All invitation of 22/07 09:53, AdminBase lead 8742, and Joe Mayer's
> domain `stainforthcon.co.uk`. Every "Staniforth" in the repo is our own derived record; I
> made it worse on 28/07 by "correcting" the dashboard to the wrong one. Fixed in
> `dashboard-state.json`, `mary-jobs.json`, `estimates.json`, here and `vesuvius_pricing.py`.
> **The OneDrive folder really is spelled `Staniforth Construction LLP` - do not "fix" that
> path, it will stop resolving.** Mined data left alone.

## Position

**Benchmarked at GBP 110,666.70 ex VAT, not supplier-backed, and not issued.**
The 30/07 return date has passed. **The job is still being priced** - Gintare
chased MetFab for a quote on 04/08 08:24, five days after the return - so it has
either slipped or been extended. I hold no record of anything going to Stainforth
and no record of a new date; one look at Gintare's Sent folder settles both, and
"no record in my mailbox" is not "no record".

Two things block a real price:

- **REQ-8, the 60-minute fire-rated door package.** The specification requires all
  external doors at 60 min, some of those doors sit inside curtain walling, and
  nothing in `estimating@` answers the question. Adam recorded on 28/07 that
  Gintare and Steve are on it - which says who, not what was decided. **The AFS
  enquiry is still unsent as of 04/08; there is no AFS traffic on this job at all.**
- **Window cill/jamb/head flashings are ours and the number carries GBP 0.00 for
  them** - see below. Not a delay, a hole.

**Expect the priced work to run high, and the SCOPE to be short.** Calibration is
+10.4% mean bias over five points and the >6 m2 band ran +35.2% on St Mary's; this
job is 79% curtain walling, the band that over-prices. But the fire doors and the
flashings are both missing rather than mis-rated, so they push the other way. Those
are different errors and they do not cancel - say so on the face of anything issued.

## The job

| | |
|---|---|
| Scheme | Proposed New Gas Plant, Plot 8 Vesuvius Way, Worksop S80 3NE |
| Main contractor | Stainforth Construction LLP - Joe Mayer |
| End client | BUSE Gas Solutions |
| Architect | JHA Architecture Ltd, job 2024-055 (Doncaster, enquiries@j-h-a.co.uk, 01302 364 565) |
| Trade bill | `L_SC Aluminium Doors & Windows` ("Aluminium Doors - Windows Bill.xls") |
| Estimating Log | 8742 |
| **Tender return** | **Thursday 30 July 2026** |
| Position | Budget/benchmark only. **Nothing issued to Stainforth.** No supplier quote held. |

Buildings in our bill: **Building 1 Welfare** and **Building 2 Office**. Building 03
(machine house) is NOT ours - see Scope boundary below.

## The number

**GBP 110,666.70 ex VAT** on today's register. Benchmark, not supplier backed.
(GBP 110,551.98 was the 27/07 figure emailed to Adam and Zac; the GBP 114.72 is the rate
register being re-mined since, not a change of scope. Both are benchmarks, neither is a price.)

    supply       85,036.77
    code adders   9,262.50
    installation 16,367.43

Curtain walling is 79% of it. Basis: house MASTER PRICING DOC curtain-wall formula
(GBP850/m2 supply + GBP150/m2 labour); windows and doors on BSW size-banded register
medians **+15% Senior premium (estimator judgement, not measured)**; then house template
code adders (SAW 337.50, MAW 412.50, SAD 900, DAD 1500) and Adam's labour codes.

Generator `scripts/vesuvius_pricing.py`; workbook
`outputs/Vesuvius Way Worksop - Fenster Pricing Document and Review.xlsx`.

## Take-off

Curtain wall, Senior SF52 Zone Drained fully capped 52mm - **86.92 m2**:
welfare Ele 1 2000x2450; welfare Ele 2 2950x2450 incl single AFT door; office Ele 01
6900x6000 raked (41.4 less the 3.35x3.35/2 triangle = 35.79 m2); office Ele 02 6500x6000
incl double AFT door.

Windows, Senior PURe No Profile Groove - 8no 1350x1450 (office W05-W12), 4no 750x950
(welfare Ele 4), 1no 1500x1255-1150 (welfare Ele 1, **no drawing exists anywhere in the
pack**).

Doors, Senior SPD150 - 2no 1000x2450 incl 350 toplight.

Not priced / TBC: B1-A access hatch 1450x1200; B1-G louvred double door 1450x2110 (steel);
B2i-E/F internal PyroStop fire screens 2400x1500 and 3100x1500.

Bill and drawing dimensions differ throughout - bill reads as structural openings,
drawings as frame sizes. Final sizes by manufacturer survey.

## THE LIVE ISSUE - the 60 minute door package (REQ-8, open since 27/07)

Verified at source: **JHA NBS Section 2, clause L20**, 15/07/2026. Four separate 60 minute
door clauses - "External Doors", "External Doors Curtain Walling", "External Doors
Louvered", and clause 45 "Door leaves (Internal)". The door schedule 2024/055/221P agrees:
every external door type on it is "60 Min Insulated steel-core" or "60 Min Double Door
installed in curtain wall".

We priced the 2no doors as standard aluminium at GBP 4,683.56, and the two curtain wall
screens that carry doors total GBP 49,377.50. **Together that is GBP 54,061.06, 48.9% of the
number** - the two figures quoted around this job measure different things: 49,377.50 is the
screens alone, 54,061.06 adds the 2no doors. **A 60 minute door
cannot go into a Senior SF52 screen without a fire rated sub-frame, and SF52 is not a fire
rated system.**

The BSW enquiry does not close this - it **excludes** it: *"Exclude all fire-rated door
leaves / fire-rated doorsets unless they can provide certified fire-rated doors."* So BSW's
return will come back with a hole exactly where the money is.

**The package splits two ways and REQ-8's original option 1 only covers one of them:**

- **Aluminium fire screens / doors in the curtain wall + the internal PyroStop screens ->
  Aluminium Fire Systems.** Enquiry now WRITTEN:
  `outputs/Vesuvius Way - RFQ to Aluminium Fire Systems (draft, send today).txt`.
  Chris Wall chris@aluminiumfiresystems.com, cc Charlie Skipp charlie@, 0121 277 4870.
  AFS turned Gordon Court Q7585 round in **two days** (enquired 07/07, quoted 09/07 11:02),
  so they can still make Thursday if it goes today.
- **60 min insulated steel-core external doors (fire escape, vision panel, louvred) ->
  a STEEL doorset supplier**, not AFS. Gintare sent a steel-door enquiry at 15:31 on 28/07
  naming drawing 2024/055/127 Door Type A and the D.04 louvre door. **Our copy of that email
  shows no recipient** - worth confirming who it actually went to.

Open questions put to AFS in the draft: EI60 vs E60; whether U 1.2 W/m2K is achievable on a
60 min doorset at all (if not, that is a conflict in JHA's own specification); the interface
between an AFS doorset and our SF52 screen; supply-only vs installed; lead time and validity.

## THE SECOND HOLE - window flashings, found 04/08

**Our own Technical Advisor put an item in our scope and the benchmark excludes it.**

Steve Freezer to Gintare, **28/07 14:53**: *"If you send the enquiry to Nick at MetFab,
he will be able to provide a cost for the Cills, Jamb & Head flashings to all windows -
nick@met-fab.co.uk."* Gintare sent it **28/07 16:55** with the window details attached
and **chased it 04/08 08:24**. MetFab have not replied in seven days.

The workbook's "Not included" note reads *"cladding flashings/pressings (shown as
Kingspan/Euroclad scope)"*. A window cill flashing is not a cladding pressing, so the
exclusion does not reach it - and there is no priced line for it either. **GBP 0.00,
in a number that has been quoted internally three times.** This is the Luton shape
exactly: nothing is arithmetically wrong, because the missing thing is a row that
does not exist.

**Quantity, from our own take-off - 63.81 linear metres over 13 windows:**

    8no 1350x1450  perimeter 5.600 m  = 44.80 m
    4no 750x950    perimeter 3.400 m  = 13.60 m
    1no 1500x1255-1150                =  5.41 m   (the window with no drawing)

There is no schedule of flashings in the tender pack; that count is ours, off our
take-off, and it moves if the survey moves.

**It cannot be benchmarked, either.** Fenster hold **no MetFab rate anywhere** - the
one placed MetFab order in the record, Stoke Park's 2no panels, carries a blank cost
per m2 and a GBP 0.00 line total and is flagged there as "the only open cost on the
job". So MetFab is a supplier we buy from and have never once captured a rate for,
which is why an unanswered chase leaves nothing to fall back on. Do not invent one.

**Before anything is issued this is a priced allowance or a named exclusion.** If it
is excluded, the words are *"flashings, pressings and trims of every kind"* -
"cladding flashings" does not reach a window cill. `scripts/vesuvius_pricing.py` now
carries this as its own note rather than leaving it inside the exclusion, and the
manifest carries it as a `bought_in_lines` entry, where the Crestwood Park rule
FAILS on it correctly.

## Scope boundary

- **Building 03 is not ours.** Its door schedule 2024-055-308B carries D1-D5 acoustic
  steel-core doors (Rw 33dB, mass-loaded soundproofing core, 60 min fire integrity) and
  2no electrically operated SilentRoll 31 acoustic roller shutters, 4000x2200 and
  4000x6650. None of it is in our trade bill. Confirmed by reading the drawing.
- **The Building 02 switch room roller shutter is not ours either** - 3500 x 5900,
  SilentRoll 31, Rw 31dB, 3-phase 400V, on door schedule 221P but absent from our bill.
- Both should be named in the exclusions when anything is issued to Stainforth. Nothing
  has been issued yet, so nothing is exposed today.

## Suppliers

**The system problem, still unresolved.** The pack is entirely Senior Architectural Systems
and **none of BSW (Sheerline), Aplus (Technal) or Bellview (SMA Smart Wall) fabricate
Senior.** Either a Senior-approved fabricator is found or an alternative system is formally
qualified in the tender. Every rate in the workbook comes from non-Senior quotes and is
labelled indicative for that reason.

**Enquiries out on this job and where they stand (04/08):**

| supplier | for | sent | status |
|---|---|---|---|
| BSW `estimations@bsws.co.uk` | the main aluminium package | 28/07 15:22 | no return, 7 days. Excludes fire-rated leaves |
| steel doorset supplier - **recipient unknown** | 60 min steel-core doors | 28/07 15:31 | our copy shows NO recipient; nothing back |
| **MetFab** - Nick, `nick@met-fab.co.uk` | cill/jamb/head flashings, all windows | 28/07 16:55 | chased 04/08 08:24, no return |
| Aluminium Fire Systems - Chris Wall | CW fire doors + PyroStop screens | **NEVER SENT** | draft still sitting in `outputs/` |

Three of the four are silent and the fourth was never sent. Nothing can be priced off any
of them today.

## The BSW enquiry - settled 28/07, do not re-litigate

Gintare sent it to `estimations@bsws.co.uk` three times: 15:13 and 15:17 bounced (28.5 MiB
zip, ~39 MB encoded, against BSW's 36 MB cap); **15:22 was a different, smaller 19.9 MiB
zip of 19 files and it went.** Adam confirmed 15:50. The four files dropped were general
architectural background with no glazing information (106B, 201O, 202O, 209O); **every
glazing document survived**, including window schedule 222P, door schedule 221P and the NBS
spec - which the 27/07 enquiry had been missing. Full evidence in
`mary_recall --job vesuvius`. Nothing to re-send. Seven days on, nothing has come back.

### WHEN BSW'S RETURN LANDS - check these before it goes anywhere near a tender

1. **Count the units against the trade bill, line by line.** The Logikal element drawings
   in the enquiry still state the OLD quantities and ask for **6 fewer units than the
   bill**: dwg 005 says Qty 1 against bill 4no, dwg 004 says Qty 1 against bill 2no,
   dwg 008 says Qty 6 against schedule 222P W05-W12 = 8. Including 222P this time helps,
   but a fabricator prices from the element drawing in front of them, not the schedule.
2. **Dwg 001, the access hatch, is still not attached** although the hatch is bill item
   B1-A. If it is not in BSW's return it was never asked for.
3. **Expect nothing for the fire doors.** The covering email excludes fire-rated leaves
   and doorsets unless BSW can certify them.

Residual: L20 names drawing **2024-055-114 Building 01 Fire Plan**, which is not in the
55-file tender pack at all, and 2024-055-308B, which is Building 03 and not ours. The fire
plan is the document that would say which doors are 60 minute and where. Asked for in the
AFS draft.

## 29/07 - where REQ-8 actually stands

Adam answered on the hub (message 53, 28/07 20:40): *"Gintare has been going through this
one with Steve (our Technical Advisor). I need to have a catch up with them and see where
we are at."* **Recorded, not closed** - it says who is on it, not what was decided.

Checked at source, and this is the useful part: **the only written record of Gintare and
Steve on this job is one email** - 27/07 09:35, Gintare to Steve cc Adam, asking exactly the
right question (*"doors shown to be Senior, some are part of Curtain Walling, however as per
specification all external doors to be 60min fire rated. Could you please advise?"*).
**Nothing in estimating@ answers it.** So whatever they have concluded between them is not
written down anywhere Mary can see, and that is what the catch-up needs to produce.

Also still true as at 29/07, one day before the return:

- **No AFS traffic exists on this job at all.** The drafted enquiry is still unsent.
- **The 28/07 15:31 steel-door enquiry shows no recipient on our copy** and nothing has come
  back. One look at Gintare's Sent folder settles whether the steel-core half was ever asked
  for. Cheapest check on the list.

Deliverable for the catch-up:
`outputs/Vesuvius Way - element status for the Gintare-Steve catch-up.txt` - every element,
what the spec wants, what we priced it as, what it is worth. Emailed to Adam 29/07.

    priced and fine                          GBP 55,279.03
    priced on non-fire-rated product         GBP 54,061.06   (48.9%)
    no supplier, no rate                     6 items

## Pre-issue checks (`data/job-checks/vesuvius-way.json`, first run 29/07)

**7 FAIL, 6 ASK as at 04/08** (was 6 FAIL, 3 ASK on 29/07; the seventh FAIL is the
MetFab flashings entering `bought_in_lines`). **None is a false alarm** - this is what a
job with no supplier return and an unpriced fire-door package honestly looks like. Two
are worth naming:

- **fire-exit panic hardware.** 221P specifies pushpad nightlatch with snib lock back,
  external cylinder access and emergency exit hardware internally on the steel-core doors.
  B1-E is priced as a glazed-door median plus a code adder - **there is no panic hardware in
  it at all.** New this turn; it is in the AFS draft but not in the benchmark.
- **someone can actually fabricate it** - see below, this one had to be fixed first.

Document hygiene closed the same day: the workbook had no print area and no repeating header
rows, so the whole sheet printed including working columns. `scripts/vesuvius_pricing.py`
now sets an explicit print area, repeating header row and fit-to-width on every sheet.

## A check this job defeated, now fixed

`check_fabricator_can_make_it` was **founded on this job** (nobody fabricates Senior) and
only tested whether the `fabricator` field was non-empty. Writing the true answer into it -
`"NONE APPROACHED CAN MAKE IT"` - **passed**. Redditch Library was passing at the same moment
on *"their own system, not available to Fenster"*.

Widened 29/07: a denial in the field (none / nobody / no-one / no fabricator / cannot /
unable / not available / not approached / does not fabricate) now FAILS, and an explicit
`"can_make_it": false` fails whatever the prose says. 11 selftest variants, every existing
fixture still behaves, both jobs now fail correctly. Handed to redditch-library so the new
FAIL on their run is not a mystery.

## Open requests

- **REQ-8** (open, raised 27/07, owner Adam) - who prices the 60 minute door package. The AFS
  letter is written, so this is a send, not a drafting job. Adam's 28/07 answer recorded
  against it; the decision itself is still outstanding and the 30/07 return has passed.

Not raised as requests - deliberately, with 14 already open on Adam:

- **The flashings gap.** Nothing is issued, so nothing is exposed to a client. It belongs
  on the face of the document when one is built, not in a new request today.
- **Who the 28/07 15:31 steel-door enquiry went to.** Still unanswered since 29/07 and
  still the cheapest check on the job - Gintare's Sent folder, one look.

## Decisions and corrections on the record

- 28/07: my 16:44 email to Adam said the RFQ needed re-sending. It did not - the 15:22 attempt
  had already succeeded. I inferred "all three failed" from two bounces and was wrong. Verified
  by diffing the attachments, not by taking Adam's word for it.
- Nothing has been sent to Stainforth. Nothing has been sent to a supplier by me - ghost
  protocol; the AFS letter is a draft for Gintare or Steve to send.

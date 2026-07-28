# Vesuvius Way, Worksop - Air Separation Unit (Staniforth Construction LLP)

Chat key `vesuvius`. Job file opened 28/07/2026. Update whenever the position moves.

## The job

| | |
|---|---|
| Scheme | Proposed New Gas Plant, Plot 8 Vesuvius Way, Worksop S80 3NE |
| Main contractor | Staniforth Construction LLP - Joe Mayer |
| End client | BUSE Gas Solutions |
| Architect | JHA Architecture Ltd, job 2024-055 (Doncaster, enquiries@j-h-a.co.uk, 01302 364 565) |
| Trade bill | `L_SC Aluminium Doors & Windows` ("Aluminium Doors - Windows Bill.xls") |
| Estimating Log | 8742 |
| **Tender return** | **Thursday 30 July 2026** |
| Position | Budget/benchmark only. **Nothing issued to Staniforth.** No supplier quote held. |

Buildings in our bill: **Building 1 Welfare** and **Building 2 Office**. Building 03
(machine house) is NOT ours - see Scope boundary below.

## The number

**GBP 110,551.98 ex VAT** (GBP 132,662.38 inc VAT). Benchmark, not supplier backed.

    supply       84,922.05
    code adders   9,262.50
    installation 16,367.43

Curtain walling is 79% of it. Basis: house MASTER PRICING DOC curtain-wall formula
(GBP850/m2 supply + GBP150/m2 labour); windows and doors on BSW size-banded register
medians **+15% Senior premium (estimator judgement, not measured)**; then house template
code adders (SAW 337.50, MAW 412.50, SAD 900, DAD 1500) and Adam's labour codes.

Generator `scripts/vesuvius_pricing.py`; workbook
`outputs/Vesuvius Way Worksop - Fenster Pricing Document and Review.xlsx`.

**Expect this to run HIGH.** Calibration is +10.4% mean bias over five points, and the
>6 m2 band ran +35.2% on St Mary's. This job is weighted to large curtain-wall elements,
which is the band that over-prices. Say so on the face of anything issued.

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
screens that carry doors total GBP 49,377.50 - about 45% of the tender. **A 60 minute door
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

## Scope boundary

- **Building 03 is not ours.** Its door schedule 2024-055-308B carries D1-D5 acoustic
  steel-core doors (Rw 33dB, mass-loaded soundproofing core, 60 min fire integrity) and
  2no electrically operated SilentRoll 31 acoustic roller shutters, 4000x2200 and
  4000x6650. None of it is in our trade bill. Confirmed by reading the drawing.
- **The Building 02 switch room roller shutter is not ours either** - 3500 x 5900,
  SilentRoll 31, Rw 31dB, 3-phase 400V, on door schedule 221P but absent from our bill.
- Both should be named in the exclusions when anything is issued to Staniforth. Nothing
  has been issued yet, so nothing is exposed today.

## Suppliers

**The system problem, still unresolved.** The pack is entirely Senior Architectural Systems
and **none of BSW (Sheerline), Aplus (Technal) or Bellview (SMA Smart Wall) fabricate
Senior.** Either a Senior-approved fabricator is found or an alternative system is formally
qualified in the tender. Every rate in the workbook comes from non-Senior quotes and is
labelled indicative for that reason.

## The BSW enquiry - what actually happened on 28/07 (settled, do not re-litigate)

Gintare sent the RFQ to estimations@bsws.co.uk three times.

| time | zip | outcome |
|---|---|---|
| ~15:13 | 28.5 MiB | bounced 15:14 - 550 5.2.3 RESOLVER.RST.RecipSizeLimit, 39 MB against a 36 MB cap |
| 15:17 | 28.5 MiB (23 files) | bounced 15:18, same reason |
| **15:22** | **19.9 MiB (19 files)** | **NO BOUNCE. It went.** |

**The third attempt was a different, smaller zip - not a repeat of the first two.** 28.5 MiB
base64-encodes to ~39 MB, which is the figure in both bounces; 19.9 MiB encodes to ~27 MB,
comfortably inside the cap. Adam confirmed at 15:50: *"Vesuvius should be sorted and sent now
after documents were removed."*

**What was removed - all four are general architectural background, no glazing information:**
106B ground floor site context plan, 201O proposed ground floor plan, 202O proposed first
floor plan, 209O orthographic imaging.

**What BSW hold (19 files) - every glazing document survived:** window schedule 222P, door
schedule 221P, door details 127, window details 128 pages 1-2, elevations 204O and 205O,
welfare elevations 108D, ground floor plan 105C, dimension plan 228P, the NBS specification,
the trade bill, and all seven Logikal element drawings. **This is materially better than the
27/07 enquiry**, which carried 10 of 55 files and was missing 221P, 222P and the NBS spec -
the gap I raised on 27/07 has closed itself.

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

## Open requests

- **REQ-8** (open, raised 27/07, owner Adam) - who prices the 60 minute door package before
  Thursday. The AFS letter is now written, so this is a send, not a drafting job.

## Decisions and corrections on the record

- 28/07: my 16:44 email to Adam said the RFQ needed re-sending today. It did not - the 15:22
  attempt had already succeeded. The premise (that all three attempts failed) came from the
  bounce pattern and was wrong; two bounces, three sends, and the third zip was rebuilt.
  Verified independently by diffing the two attachments, not by taking Adam's word for it.
- Nothing has been sent to Staniforth. Nothing has been sent to a supplier by me - ghost
  protocol; the AFS letter is a draft for Gintare or Steve to send.

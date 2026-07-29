# Riverside House - AOV Smoke Vents (RRR Group)

Chat key `riverside`. Opened 27/07/2026.

> **Rewritten short on 29/07.** Adam and Zac both bounced REQ-9 the same evening for length -
> Adam: *"this word count is insane, I will not be reading this."* The request was 17,529
> characters against 4,728 for the next largest on the board, and this file was 3,240 lines.
> Everything cut is in **`data/jobs/riverside-archive-2026-07.md`**, nothing deleted. Keep this
> file to the position, the open items and the traps. Working and reasoning go in the archive.

**Watch out:** the archive holds two unrelated Riversides - "Riverside Way" (Bradford Watts) and
"Riverside Close" (Neil Douglas). Check the client before acting on anything that lands here.
RRR's other live job is Towcester Vale Local Centre - do not mix them (its A Plus quote QT51516
is a different job, but a useful comparator on free area).

## Where it stands (29/07/2026)

**ON HOLD. Priced and drawn, not issued, nothing sent to A Plus or RRR.**

**Zac's decision, 28/07 22:11 (REQ-9 option clicked): "Hold everything until PHDB report."**
That covers the A Plus RFQ and the RRR questions both. Neither goes out until PHDB return costs
for the building works.

| | |
|---|---|
| Client | RRR Group Limited |
| Site | Riverside House, 44 Wedgewood Street, Fairford Leys, Aylesbury HP19 7HL |
| Planning ref | 24/02303/PAPCR (applicant on the location plan is Elderfern Ltd, one of RRR's companies) |
| Scope | 2no bottom-hung AOV smoke vents, one per stairwell, at each stairwell's top storey |
| **Fenster sell** | **GBP 5,990.22 ex VAT** supply and fit (GBP 7,188.26 inc VAT) |
| Supplier cost | A Plus **QT51518**, 27/07/2026, **GBP 4,845.22 net** ex VAT, supply only delivered, glazed |
| Deadline | **None client-stated.** Gated on PHDB. The hub's 26/08 is A Plus's acceptance period, not a client date. |

2no Sapa DualFrame 75Si bottom-hung AOV, 1130 x 1530, white, 155mm Technal subcill, open out,
850mm stroke single chain 9006 satin, 4-20-4 Clr Tough S Coat 1.2 / 20mm blk warmedge.

### How the price is built

Frames 4,662.15 + glass 171.31 + energy surcharge 11.76 = 4,845.22 for the pair (ties to the
quote's stated total, no extras block). Per unit 2,422.61 = **GBP 1,401.24/m2** over 1.729 m2.
Code **MAW** (1.729 m2 is in the 1.5-3 m2 band). Template adder 550 x 75% = 412.50. Labour 160/unit.

    unit rate  2,422.61 + 412.50 = 2,835.11
    items      2,835.11 x 2      = 5,670.22
    install    160 x 2           =   320.00
    TOTAL                          5,990.22 ex VAT
    optional external mastic 10.64 lm @ GBP 5 = 53.20

`mary_pricing.price_line("MAW", 1130, 1530, qty=2, supply_rate=1401.24)` - engine and template
agree to the penny (`supply_rate` is GBP/m2, not a unit price).

## THE FREE AREA - settled, bar one variable

**The 1.5 m2 was never the requirement.** It came from Adam's own 24/07 enquiry to Gintare, not
from the client. Drawings K1653-11 and K1653-12, both CONSTRUCTION ISSUE, carry the identical note:

> SMOKE VENT TO STAIRWELL ROOF - STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN
> AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2 OPERATED BY THE FIRE BRIGADE AT GROUND
> FLOOR ACCESS LEVEL IN THE STAIRS

Once per stairwell, at that stairwell's top storey - which is also where the quantity of 2 comes
from. So the requirement is **per vent, 1 m2**, and A Plus's **1.30 m2 geometric clears it by 30%.
Nothing needs resizing.** The 27/07 answer to Adam ("0.20 m2 short, requote at 1235 x 1583") is
withdrawn.

**The one live variable: geometric or aerodynamic.** QT51518 states geometric only. On A Plus's
QT51516 (Towcester Vale, same vent) aerodynamic runs 60-62% of geometric, so 1.30 geometric is
roughly **0.79-0.81 aerodynamic - about 20% short of 1 m2**. Their proposed 1235 x 1583 would also
miss.

**Evidence points to geometric**, two independent sources: (1) the drawings name their own route -
*"MAINS OPERATED INTERLINKED HEAT DETECTOR TO AD B1"*; Approved Document B is prescriptive and
states free area geometrically, while *aerodynamic* is the language of the engineered BS 9991 /
EN 12101-2 route this pack is not on. (2) Gordon Court's NBS specifies the identical duty as
*"1m2 GEOMETRIC free area"*, and *aerodynamic* appears nowhere in their 186-page spec.
**A recommendation, not a ruling** - the fire engineer or building control confirms it (RFI-3).

**Adam has ruled that size is not a constraint** (REQ-9, 27/07): *"We can make the windows as big
as we need to... the openings are being newly formed."* Useful if a resize is ever needed - but
note **neither vent has a cost-free resize**: AOV.01 (second floor) has no opening at all and would
need one cut into retained masonry; AOV.02 (first floor) has three existing openings whose size is
set. The pack shows no new-build storey. Reasoning in the archive.

## Open items

| # | Item | With |
|---|---|---|
| RFI-1 | A Plus to state **aerodynamic** free area for 1130 x 1530 at 850mm stroke | A Plus (via Adam/Gintare) |
| RFI-2 | A Plus to confirm vent leaf, rail and actuator position on shop drawings | A Plus |
| RFI-3 | Is the 1 m2 geometric or aerodynamic? And where did 1.5 m2 come from? | Client / fire strategy |
| RFI-4 | **Who is carrying the AOV control system?** | Client / PHDB |
| RFI-5 | Cill height above FFL at each vent; 155mm subcill against the 150mm asked | Client |
| RFI-6 | Whole-window Uw - does the drawings' 1.6 bind the stair AOV? And is there a WER band C requirement? | A Plus / client |
| RFI-7 | Delivery - confirm charge or that the load is batched free | A Plus |

All seven are held under Zac's decision. **RFI-1 is the one that decides the job** and A Plus can
answer it from their own system.

## Things that will bite if forgotten

1. **Nobody is carrying the AOV control system.** The drawing requires fire-brigade operation from
   ground floor access level - panel, mains + battery supply, cabling, containment, override,
   commissioning, EN 12101 documentation. A Plus stop at the actuator and leave ~2m of flex coiled
   at the vent. Excluded from our price too. **The window alone cannot satisfy the note.**
2. **Delivery is not free and does not reach site.** A Plus deliver FOC above GBP 5,000 ex VAT
   within 50 miles of Watford; our order is GBP 4,845.22, **GBP 154.78 under**. And QT51518 carries
   no site address - the only address on it is our own yard at MK13 9HF, so "Delivered" ends in
   Milton Keynes and **the leg to HP19 7HL is ours and is not in the GBP 5,990.22**. A Plus also
   require labour at the delivery point to unload.
3. **26/08/2026 is the date that matters.** QT51518 is *"open for acceptance for 30 days and
   thereafter subject to confirmation"* - it does **not** lapse. After 26/08 the price stops being
   automatically binding, so a question asked before it is an addendum and after it needs a
   reconfirmation. Our own 30-day validity closes the same day. **Under the hold, expect to need
   one line asking A Plus to reconfirm GBP 4,845.22.**
4. **Warranty: we offer RRR ten years on "glass and frame products"; A Plus give twelve months on
   SE Controls products only.** On an AOV the gear *is* the product - we warrant everything that
   makes it a window and nothing that makes it a smoke vent. The hinges, gasket and cill are in
   neither warranty. Our own ten years **states no start date anywhere** - the one item here that
   costs nothing, applies to every job and is Adam's to fix. Full clause-by-clause diff in the archive.
5. Actuators are **not** restrictors; A Plus disclaim liability for damage without one fitted 50mm
   beyond the stroke. Not priced. Trap hazard under BS EN 60335-2 below 2.5m FFL; Part K anti-fall
   below 1100mm FFL, which A Plus exclude and so do we - nobody carries it.
6. **We are not working from the whole pack.** We hold K1653-03, 04, 10b, 11, 12 plus a location
   plan; K1653-01, 02, 05-09 and every cited detail sheet are absent, as are the fire strategy,
   existing plans, demolition plan, sections and schedules. The absent classes are exactly the ones
   that answer RFI-3 and the opening question.
7. **The wider scope.** The pack is a full flat conversion - W1 escape windows, W2 windows at U 1.6,
   D1 FD30s entrance doors, D5 external glazed door, through all three floors. We are pricing 2
   vents out of that. Raised with Adam as an opportunity.

## Files

**Deliverables (done, not issued):**
- `outputs\Riverside House - Fenster Pricing Document (house format).xlsx`
- `outputs\Riverside House - AOV Smoke Vent Drawings.pdf` (2 sheets, Rev A)

**Written and held under Zac's decision:**
- `outputs\Riverside House - RFQ to A Plus (draft, send by 26-08).txt` - 16 items
- `outputs\Riverside House - Questions to RRR (draft).txt`
- `outputs\Riverside House - A Plus requote brief (for Gintare).txt` - the working brief behind both

**Sent:**
- `outputs\Riverside House - Reminder to Adam (AOV free area).txt` - emailed 29/07, the reminder
  Adam asked for on 27/07 and could not have while mail was blocked. **Mail to Adam is live again.**

**Other:** `data\job-checks\riverside-house-aov.json` + fixture `_test-riverside.json`;
generator `scratchpad\riverside_drawings.py`; QT51518 filed at
`...\RRR\Riverside\1. Estimating\2. Supplier Quotes\Quotation_QT51518.PDF`.

## Checks

`python scripts\mary_checks.py data\job-checks\riverside-house-aov.json` - **1 failed** (our own
ten-year warranty has no start date - stays failed until Adam rules) **and 7 questions**, verified by
running it 29/07. Nothing goes to RRR until those close.

This job founded two rules, fixture `_test-riverside.json`:
- `check_free_delivery_threshold` - a quote that says "Delivered" can still put carriage on us.
- the thin-margin arm of `check_quote_validity_against_commitment` - a supplier quote closing the
  same day our price does passes "held as long as ours" and is still no use.

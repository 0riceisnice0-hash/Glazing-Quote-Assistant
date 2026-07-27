# Riverside House - AOV Smoke Vents (RRR Group)

Chat key `riverside`. Opened 27/07/2026 for a job that already existed.
**Watch out:** the archive holds two unrelated Riversides - "Riverside Way" (Bradford Watts) and
"Riverside Close" (Neil Douglas). This chat matches on `riverside`. Check the client before acting on
anything that lands here. RRR Group's other live job is Towcester Vale Local Centre, filed under
`Commercial\2. Projects\RRR-Group\Towcester Vale Local Centre` - do not mix them (its A Plus quote
QT51516 is a different job, though it is a useful comparator - see FREE AREA below).

## Where it stands (as at 27/07/2026)

**Priced and drawn. Not issued.** Adam is holding the submission until PHDB return costs for the
building works. No deadline.

| | |
|---|---|
| Client | RRR Group Limited (Adam's instruction 27/07 13:47, trusted, cc Commercial) |
| Site | Riverside House, 44 Wedgewood Street, Fairford Leys, Aylesbury, Bucks HP19 7HL |
| Planning ref | 24/02303/PAPCR. Planning applicant on the location plan is **Elderfern Ltd**, not RRR - RRR's associated companies are Primrose Property, Elderfern and SRP Investments |
| Scope | 2no bottom-hung AOV smoke vents, one per stairwell, at each stairwell's top storey |
| **Fenster sell** | **GBP 5,990.22 ex VAT** supply and fit (GBP 7,188.26 inc VAT) |
| Supplier cost | A Plus **QT51518**, 27/07/2026, **GBP 4,845.22 net** ex VAT, supply only delivered, glazed |
| Validity | A Plus to **26/08/2026**. Our house validity is 30 days from issue. |

### How the price is built

Frames 4,662.15 + glass 171.31 + energy surcharge 11.76 = 4,845.22 for the pair (ties exactly to the
quote's stated Total - **no extras block**, the Gordon Court element-lines-vs-total test passes).
Per unit 2,422.61 = **GBP 1,401.24/m2** over 1.729 m2.

Code **MAW** (1.729 m2 sits in the 1.5-3 m2 band; SM5 used SAW at 1.44 and MAW at 2.09, and
`band_of()` breaks at 1.5). Template adder 550 x 75% = 412.50. Labour 160/unit.

    unit rate  2,422.61 + 412.50 = 2,835.11
    items      2,835.11 x 2      = 5,670.22
    install    160 x 2           =   320.00
    TOTAL                          5,990.22 ex VAT
    optional external mastic 10.64 lm @ GBP 5 = 53.20

Engine and template agree to the penny (`mary_pricing.price_line("MAW", 1130, 1530, qty=2,
supply_rate=1401.24)` - note `supply_rate` is **GBP/m2**, not a unit price).

### Files

- `outputs\Riverside House - Fenster Pricing Document (house format).xlsx`
- `outputs\Riverside House - AOV Smoke Vent Drawings.pdf` (2 sheets, Rev A)
- `outputs\Riverside House - Reply to Adam (draft).txt` - **written but NOT SENT, see below**
- `data\job-checks\riverside-house-aov.json` + fixture `_test-riverside.json`
- Generator: `scratchpad\riverside_drawings.py`; job json `test-results\riverside-run\`
- Quote: `test-results\mary-inbox\processed\20260727T0842-xgnwAAAA-att\Quotation_QT51518.PDF`
- Pack: `test-results\mary-inbox\processed\20260727T1500-xgqQAAAA-att\` (6 drawings + 2 logo images)

## THE FREE AREA - what changed on 27/07 and why it matters

Adam's enquiry of 24/07 said **"We need 1.5m2"**. A Plus returned 1.30 m2 and the answer that went to
Adam - and REQ-9 - was *no, 0.20 m2 short, requote at 1235 x 1583*.

**The pack says 1 m2, not 1.5 m2.** Drawings K1653-11 (first floor) and K1653-12 (second floor), both
CONSTRUCTION ISSUE, Campbell Ark, carry the identical red note:

> SMOKE VENT TO STAIRWELL ROOF - STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY ROOF WITH AN
> AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2 OPERATED BY THE FIRE BRIGADE AT GROUND
> FLOOR ACCESS LEVEL IN THE STAIRS

It appears **once per stairwell, at that stairwell's top storey** - which is where the quantity of 2
comes from. Stairwell 1 tops out at second floor (K1653-12, leader 7); Stairwell 2 at first floor
(K1653-11, leader 3). So the requirement is **per vent**, settling the first of the two variables
triage flagged. A Plus's page 2 independently confirms they read it per vent: they size a *single*
frame (1235 x 1583) to reach 1.5 m2.

So on the pack, **1.30 m2 geometric clears 1 m2 with 30% to spare** and nothing needs resizing.
1.5 m2 appears nowhere in the pack; its source is unknown and needs confirming (RFI-3).

### The variable that is still live: geometric or aerodynamic

QT51518 quotes **geometric only**. A Plus's QT51516 (Towcester Vale, same DualFrame 75Si AOV) states
both on every line - verified at source, not inherited:

| size | stroke | geometric | aerodynamic | ratio |
|---|---|---|---|---|
| 810 x 1335 | 900mm | 0.81 m2 | 0.49 m2 | 60.5% |
| 1205 x 1335 | 900mm | 0.87 m2 | 0.54 m2 | 62.1% |

On that ratio our 1.30 m2 geometric is roughly **0.78-0.81 m2 aerodynamic - about 20% short of 1 m2**,
and A Plus's proposed 1235 x 1583 would be ~0.9 m2 aerodynamic and would **also** miss. Indicative
only: different sizes, and a 900mm stroke against our 850mm. **A Plus must state the aerodynamic
figure for the actual Riverside sizes** (RFI-1) and the fire strategy must confirm which basis
applies (RFI-3). Do not treat the frame-area ratio as a shortcut - Towcester's own geometric/frame
ratios are 75% and 54%, so it does not scale.

## Open items

| # | Item | With |
|---|---|---|
| RFI-1 | A Plus to state **aerodynamic** free area for 1130 x 1530 at 850mm stroke | A Plus (via Adam/Gintare) |
| RFI-2 | A Plus to confirm vent leaf, rail and actuator position on shop drawings | A Plus |
| RFI-3 | Is the 1 m2 geometric or aerodynamic? And where did 1.5 m2 come from? | Client / fire strategy |
| RFI-4 | **Who is carrying the AOV control system?** | Client / PHDB |
| RFI-5 | Cill height above FFL at each vent; 155mm subcill acceptable against the 150mm asked | Client |
| RFI-6 | Whole-window Uw - does the drawings' 1.6 bind the stair AOV? | A Plus / client |
| RFI-7 | Delivery - confirm charge or that the load is batched free | A Plus |

**REQ-9 on the hub has been rewritten** to ask the real question. Its old premise ("1.30 against 1.5,
the answer is NO") is superseded.

## Things that will bite if forgotten

1. **Nobody is carrying the AOV control system.** The drawing requires fire-brigade operation from
   ground floor access level - a smoke control panel, mains + battery supply, cabling, containment,
   override, commissioning, EN 12101 documentation. A Plus fix the actuator, test on local batteries
   and leave ~2m of flex coiled at the vent; that is where they stop. It is excluded from our price
   too. **The window alone cannot satisfy the note.**
2. **Delivery is not free.** A Plus's Job Spec line says "Glazed /Supply Only (Delivered)" but their
   terms say "All orders are priced as Ex-Works" and only deliver FOC above **GBP 5,000 ex VAT**
   within 50 miles of Watford. Our order is GBP 4,845.22 - **GBP 154.78 under**. Below that they batch
   or charge GBP 1/mile each way. Carried as provisional. Note the resize option removes it: at
   1235 x 1583 the order clears GBP 5,000.
3. **Zero validity headroom, and it will go negative.** Our price (30 days from a 27/07 document) and
   A Plus's both close on **26/08/2026** - the same day. Since Adam is deferring issue until PHDB
   report, our 30 days will run past the day the cost behind it lapses.
4. Actuators are **not** restrictors; A Plus disclaim liability for damage without one fitted 50mm
   beyond the stroke. Not priced.
5. Trap hazard under BS EN 60335-2 below 2.5m FFL; Part K anti-fall below 1100mm FFL, which A Plus
   exclude. 24v DC only. 15,000 cycles or 12 months warranty.
6. **The wider scope.** The pack is a full flat conversion: the key defines W1 escape windows, W2
   windows at U 1.6, and D1 FD30s flat entrance doors / D5 external glazed door, appearing right
   through all three floors. We are pricing 2 vents out of that. Raised with Adam as an opportunity.
7. **The mail channel to Adam is blocked.** `mary_send.py` returned
   `403 ErrorAccessDenied - Blocked by tenant configured AppOnly AccessPolicy settings` on 27/07.
   The reply is written and saved in `outputs\` for a human to send; the substance is on the hub
   instead. Not previously recorded anywhere - see the noticeboard.

## Checks

`python scripts\mary_checks.py data\job-checks\riverside-house-aov.json` - 0 failed, **3 questions**
(free-area basis, validity headroom, delivery). Nothing goes to RRR Group until those close.

This job founded two rules, fixture `_test-riverside.json`:
- `check_free_delivery_threshold` - a quote that says "Delivered" can still put carriage on us.
- the thin-margin arm of `check_quote_validity_against_commitment` - a supplier quote expiring the
  same day our price closes passes "held as long as ours" and is still no use.

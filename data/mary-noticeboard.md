# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-08-04 11:44 - triage
A VETROSEAL DELIVERY CHARGE IS BILLED AS A GLASS LINE WITH A FAKE 0.300 m2 - IT CORRUPTS MINED RATES.

Quote 065311 (ELEVATION/BEDFORD, 04/08) has two lines: one pane of 10.8mm laminated, 3145 x 2103,
6.614 m2 at GBP 548.89, and a second line "MK40-2QA DELIVERY CHARGE", qty 1, GBP 50.00 - carrying a
UNIT AREA OF 0.300 m2. There is no glass in it.

Divide goods by total area and you get GBP 598.89 / 6.914 = GBP 86.62/m2. The real rate is
GBP 548.89 / 6.614 = GBP 82.99/m2. That is a 4.4% overstatement, silently, on every quote that
carries a delivery line. Any rate mined from Vetroseal must EXCLUDE lines whose description is a
charge rather than a make-up. Same family as their 0.30 m2 minimum-area billing already recorded.

THREE NEW REGISTER LINES, all arithmetic checked and correct:
  Vetroseal 065311  10.8mm laminated, single      GBP 82.99/m2 goods (+50.00 delivery to MK40)
  Vetroseal 065222  6.8mm laminated, single       GBP 34.65/m2 goods (+GBP 1.95/m2 energy)
  Vetroseal 065209  4T-18-6.8 lami/tgh softcoat   GBP 52.51/m2 goods (+GBP 3.25/m2 energy)

AND A WEIGHING INCONSISTENCY, immaterial in money but it breaks a check: on 065209 and 065222 the
surcharge weight is GLASS ONLY (25.0 and 15.0 kg/m2 - the laminate interlayer excluded); on 065311 it
is the FULL 10.8mm including interlayer (27.0 kg/m2). So you cannot verify a Vetroseal weight from
the make-up alone, and a weight that looks wrong is not evidence of an error.

TWO THINGS THE BATCH JOINED UP, which neither work order showed on its own:
- MHA NUNEATON IS BEING PRICED TWO WAYS. 065209 and 065222 are the SAME 8 units at 620 x 2020 on the
  same day - one as a 28.8mm double-glazed unit (GBP 526.08) and one as single 6.8 laminate
  (GBP 347.20). Someone is comparing DGU against single glass, GBP 179 apart on goods. Still no
  enquiry for it anywhere in estimating@ and no folder in the archive.
- ELEVATION/BEDFORD IS PAUL'S MK40 EMERGENCY. Paul Taylor asked AE Glaziers on 03/08 for an emergency
  board-up in Bedford MK40 plus a survey and replacement price, and AE came back asking "do you have a
  rough width and height of the glass?" Vetroseal have now priced one pane 3145 x 2103 delivered to
  MK40 2QA. That answers AE's question - nobody needs to re-measure.

### 2026-08-04 11:56 - triage
STOKE PARK: ADAM HAS AMENDED THE CN GLASS ORDER TODAY - SPEC A IS 28.8mm OVERALL, SO AN 18mm SPACER, NOT 16mm.
Adam to orders@cnglass.co.uk, 04/08 11:45 UK: 'We need to amend the order please. Spec A is meant to be 28.8mm overall thickness so requires an 18mm spacer.' The order Steve placed on 28/07 was built on Martin Gregory's 27/07 line '55 m = 4mm / 6.8' against a 16mm spacer (6.8-16-4 = 26.8mm). So Spec A is 6.8-18-4, and the 27/07 buy - 124 units, 106.9 m2, GBP 6,185.09 - is being changed after the fact.
TWO THINGS THAT FOLLOW.
1. THE AMENDMENT IS CC'd TO MARTIN GREGORY, WHO RESIGNED ON 03/08. It went to orders@ as well so it will be seen, but the man who gave the rate and who said on 27/07 that 'spacer bar doesnt differ the price' has gone. Nobody at CN Glass has confirmed IN WRITING that an 18mm spacer holds the GBP 55/m2. Get that confirmed by whoever picked the account up before the amended order is accepted - it is exactly the verbal-rate exposure already on this board.
2. IT MAKES SENSE OF THE VETROSEAL QUOTE. 065209 (30/07, MHA/NUNEATON) is '4T-18-6.8' - the same 28.8mm build-up with the 18mm spacer, at GBP 52.51/m2 goods. That is the corrected Spec A, priced by the other supplier, and it is level with CN Glass. So the make-up is right and both prices agree; it is the spacer on the ORDER that was wrong, not the rate.
GENERAL: 6.8 + 16 + 4 = 26.8, not 28.8. When a spec states an OVERALL thickness, add the panes and the spacer before ordering - the RFQ that went out on 27/07 asked for a 16mm spacer against a 28.8mm requirement and no one caught it until the glass was on order.

### 2026-08-04 12:12 - brocks-hill
A SUPPLIER COST CAN BE PASTED STRAIGHT INTO THE SELL COLUMN AND THE TOTAL STILL LOOKS RIGHT.

Brocks Hill went to SMD on 31/07 at GBP 118,278.52. Five Strongdor steel doors in it are sold at
GBP 2,728.81 each - which is Strongdor's GBP 2,637.01 per door-set plus the GBP 459.00 delivery split
five ways, to the penny. Zero uplift. The row is coded DAD and every other row in the same workbook
carries its adder exactly (SAD 900, DAD 1500, ELAW 637.50, LAW 487.50). Installation of GBP 10,570
recomputes exactly from the labour codes for the schedule WITH THE FIVE DOORS LEFT OUT - so they took
no labour either. Missing: 5 x 1500 frames + 5 x 500 install = GBP 10,000.00 ex VAT.

WHY NOTHING CAUGHT IT. Reconciling the total does not catch it - the total is internally consistent.
Comparing against the supplier quote does not catch it - it MATCHES the supplier quote, which is the
symptom, not the proof of correctness. THE CHECK THAT WORKS: take sell minus supply on every row and
read it against the code table. Nine rows, eight correct to the penny, one at 91.80 (the delivery
share). One pass, no re-pricing. Do this on any priced workbook before it leaves - it is the same
family as Brocks Hill's earlier catch where a rate applied twice made a total reconcile.

THE TELL: a late line, dropped in under deadline pressure. The steel cost landed at 14:41 on 31/07
and the tender went at 15:12. The placeholder it replaced (GBP 2,000, described in writing as "plus
our markup") had no uplift in it either.

NOBODY MAKES A GLAZED STEEL ESCAPE DOOR WITH A DECLARED U-VALUE. TWO SUPPLIERS, INDEPENDENTLY.

Strongdor, 31/07: "Not sure what is meant by Triple glazed or solar controlled glazing, since this is
marked as being from our Sportsdor range which would not allow for glazing on this door since this
requires rebound panels." Their drawing: Vision/Louvre Panel NONE, and Fire Rated / Acoustic / U Value
/ Security Rated all NPD.
Lathams, 03/08: "we cant offer a triple glazed door or a door set reaching a U value with glazing."

So when a door schedule asks for a steel escape door that is triple glazed, solar control AND hits a
door U-value, that product does not exist - the panic touchbar needs rebound panels where the glass
would go. DO NOT SPEND THE TENDER PERIOD RINGING ROUND FOR IT. Price the solid door and QUALIFY THE
DEVIATION IN WRITING ON THE FACE OF THE PROPOSAL, at the same time as the price. On Brocks Hill the
proposal qualified only the aluminium doors and said nothing about the steel ones, while the
specification box read U 1.1 / g 0.34 across the board - and Strongdor's own drawing showing NONE and
NPD was attached to the client's copy, so the contradiction went out in the same email.

NEW SUPPLIER RATE - STRONGDOR (Carnforth), quote SQ218594, 31/07/2026, 30-day validity:
  Steeldor, double external, 1810 x 2110 structural, RAL 7016 both faces, single rebate 110mm frame,
  mineral board core, Grade 316 hinges, 3-point touchbar panic bolt + 2-point panic latch + rebound
  panels + escape signage:  GBP 2,637.01 per door-set, qty 5.  Delivery GBP 459.00 to MK13. Kerbside
  only, forklift is ours. Fire rating NPD - so it is NOT a substitute where an FD rating is specified.

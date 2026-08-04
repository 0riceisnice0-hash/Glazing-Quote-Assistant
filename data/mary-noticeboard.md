# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-08-04 12:27 - triage
LUTON AIRPORT ANSWERS A QUESTION EVERY RESTRICTED-ACCESS JOB HAS: THE INSTALL LINE PAYS FOR FITTING AND NOTHING ELSE.

Ryebridge / Luton Airport Departure Gates 1 & 2, issued 13/07 at GBP 14,157.24, is two lines:
3 x SMA Shopline double door at 4,219.08 (BSW supply 2,315.01 + DAD code 2,000 x 75% + 404.07
additional - the house rule, correct), and INSTALLATION 1,500.00, which is EXACTLY 3 x the DAD
labour code of 500. Nothing else exists in the workbook.

SO THE LABOUR CODES ARE FIT-ONLY, PER UNIT - DAD/DUPD 500, SAD/SUPD 250, windows 160. They carry
no mobilisation, no travel, no supervision, no site attendance and no prelim of any kind. On an
ordinary site that is fine. On a site where nobody can walk in unescorted it means the price
contains ZERO access content, and no amount of checking the arithmetic will show it, because the
missing thing is a row that does not exist.

Luton is airside: every operative needs an LLA induction for clearance and is escorted throughout.
The proposal says only that airside working, inductions, clearance and escorted access 'are to be
coordinated prior to installation' - in the executive summary, NOT in the EXCLUSIONS column where
a client looks. That names who arranges it and is silent on who pays, and silence reads as
included. On 30/07 the client re-phased into TWO visits and we agreed at no cost; that was
defensible here (7,212.21 of headroom over the BSW buy) but it was agreed without anyone able to
say what a visit was worth.

TWO GENERAL POINTS.
- Whenever a site imposes a cost that is not glazing - escorted or inducted access, security
  clearance, permits, live/occupied premises, phasing into more than one visit, night or weekend
  working - it is either a PRICED ALLOWANCE or it is in the EXCLUSIONS of the issued document.
  New rule check_site_access_is_priced_or_excluded in mary_checks.py, manifest field site_access,
  9/9 variants green. Its founding error is Luton.
- OUR PROPOSAL TEMPLATE PROMISES A 'CSCS/SMSTS Qualified Site Supervisor in FULL-TIME ATTENDANCE',
  plus a dedicated project manager AND a separate contracts manager. 21 of 35 issued proposals I
  sampled carry the identical block, so it is boilerplate rather than anyone's decision - but on a
  GBP 14k job with a GBP 1,500 labour line it is unfundable. Worth knowing before you promise it
  on the next small package.

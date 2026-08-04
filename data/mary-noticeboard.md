# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-08-04 12:37 - filwood
ADDING A CLARIFICATION DOES NOT REMOVE A CERTIFICATION. SECOND JOB IN FIVE DAYS.

Filwood went to Stepnell on 30/07. Adam had written that morning: "we aren't hitting the
g-value required for the glazing. We certainly aren't hitting the u-value either... Ensure
all clarifications are accurate regarding u-value." The clarification paragraph was duly
added and it reads correctly. THE SPECIFICATION BOX ON THE SAME PAGE WAS NOT TOUCHED and
still states Ug 1.0, g 0.5-0.6, Rw >=32 dB as our offer. BSW's own quote puts positions
006/007 at Ug 1.1, names no coating on any of the seven, and puts the acoustic make-up on
the two ED-05s while the ED-06 that needs Rw 32 gets plain 6.8/4 glass.

Brocks Hill on 31/07 was the identical shape - proposal qualified the aluminium doors,
spec box read U 1.1 / g 0.34 across the board including the steel ones. So this is a
pattern, not an accident: OUR PROPOSAL HAS TWO PLACES THAT STATE PERFORMANCE, a prose
clarification and a boxed specification, and people edit the prose. The client reads the
box. When a value is qualified, CHANGE THE BOX - to the supplier's actual figure, or to
"see clarifications". Check both every time.

STRIPPING THE WORKING COLUMNS IS ONLY HALF OF MAKING A WORKBOOK SAFE TO ISSUE.

Filwood's .xlsx went to Stepnell with the working columns properly removed - our BSW cost
was NOT in it, that half was caught - and with dan.parker@agsurveying.co.uk still the
document author plus external links to C:\Users\LiamO'Donnell and C:\Users\Parke through
an Outlook INetCache path. Those live in docProps/core.xml and xl/externalLinks/, survive
any amount of cell editing, and show on right-click > Properties without the file being
opened. Fourth job running.

The job file had already said "a PDF is safe and the .xlsx is not" and the .xlsx was
attached anyway. If a workbook must go as .xlsx, strip docProps AND externalLinks; if it
does not have to, send the PDF.

### 2026-08-04 12:53 - redditch-library
A CURVE FITTED TO ONE SUPPLIER QUOTE INHERITS THAT QUOTE'S COLOUR AND GLASS - AND THAT MATTERS MORE THAN
ITS R2. MY REDDITCH BENCHMARK WAS 27% HIGH AND THE FIT WAS 0.9934.

BSW QT253829 landed on Redditch Library this morning: GBP 43,739.72 for 49 Sheerline Prestige frames.
I had predicted GBP 56,993.38, from rate = 721.47 x area^-0.4093 fitted to BSW's own Severn Trent quote
for the same client six weeks earlier. Scope-matched, that is +27.4%.

The R2 measured how well six points fitted a power law. It said nothing about whether those six points
were the same PRODUCT. Severn Trent was 3005 Wine Red metallic with a 6.8 laminated outer; Redditch came
back stock Hipca White. I wrote the colour down as a caveat on 28/07 and let the number stand as the
basis of a GBP 94,926.76 tender anyway.

  SO WHEN YOU QUOTE A FITTED RATE, STATE THE FINISH AND THE GLASS MAKE-UP OF THE QUOTE IT CAME FROM,
  NEXT TO THE R2. A colour difference is a scope difference, not a footnote. A superb fit to the wrong
  product is worse than a rough fit to the right one, because it reads as precision.

Direction of the band error was right - Redditch is 62% weighted into 3-6 m2, where the register was
already known to run +37.5% high. The finish compounded it. Calibration entry 21.

AND THE PRACTICAL HALF: OUR BENCHMARKS RUN HIGH, SO A JOB YOU HAVE WRITTEN OFF AS UNWINNABLE MAY NOT BE.
Redditch was GBP 4,240 above the competitor on benchmark frames and is now within about GBP 1,160 of him
on real ones. If you have told Adam a job cannot be won on price, and the number behind it is a benchmark
rather than a quotation, that conclusion is worth exactly as much as the benchmark is.

SEPARATELY, AND IT IS THE THIRD TIME THIS WEEK: A SUPPLIER DROPPED ONE UNIT AND OUR SELL DOCUMENT COPIED
IT THROUGH.

BSW's line reads Location: "w35,36" at Qty: 1. Two references, one frame. Every other multi-reference
line on the same quotation is right - w1,w2 = 2, w22,23 = 2, w16-18 = 3, w24-28 = 5 - so there is nothing
systematic to notice, just one line among twenty-nine. It went straight into the sell document as qty 1.

  THE CHECK IS check_supplier_covers_quantity AND IT FIRES ON THIS - fill supplier_coverage with
  {ref, qty_sold, qty_quoted} for EVERY reference, including the ones you are confident about, because
  the wrong one looks exactly like the right ones. BSW's own footer says they "will not be held
  responsible for any items missing from quotes", so the catching is ours by their terms as well as ours.

Brocks Hill's 12:12 note said reconciling the total does not catch a bad row. This is the same thing one
step earlier: reconciling the total does not catch a MISSING row either. Neither document was ever wrong
with itself.

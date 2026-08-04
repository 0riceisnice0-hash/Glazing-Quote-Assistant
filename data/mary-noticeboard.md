# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

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

### 2026-08-04 13:03 - john-north-hall
A COMPANY FILE BUILT FROM CORRESPONDENCE RECORDS WHAT WAS SAID, NOT WHAT WE BOUGHT - AND IT NEARLY
ASKED A CLIENT FOR PERMISSION TO SUBSTITUTE THEIR OWN SPECIFICATION.

data/companies/neil-douglas-block-management.md was written this morning from the commercial@
'Outstanding Quotes' thread plus AdminBase, and it concluded: 'nothing in Fenster's record shows we
have ever quoted a Smart system. If the fabricators do not offer it, the equivalent-approved question
has to reach Jordan.' That line had already become question 1 of a client email due out by 06/08.

We have FIVE Bellview quotations for SMA Smart-Wall in six weeks: Willesden 0000000427 D1.02 (26/06),
Lyttleton Rd 0000000445 pos 011 (06/07), St Mary's 0000000483 pos 003 and 005 (16/07), Georgie's
0000000513 pos 004-007 (27/07). We buy it routinely. Asking a client whether we may substitute the
system he specified is how a contractor says he cannot supply it - and this is the account that has
just given Fenster its first order (Earleswood Court, WO 30/07).

  'NO RECORD' FOUND IN ONE MAILBOX IS NOT 'NO RECORD'. The quote archive is a different source from
  the correspondence, and it is the one that says what we have actually bought. Search it before any
  'we have never done X' goes near a client. Corrected at source, both files.

SUPPLIER FACT WORTH KEEPING: BELLVIEW fabricate SMA Smart-Wall and we have five priced examples.
BSW have SMA Shopline (Luton, 3 doors, 13/07) but NO Smart-Wall anywhere in our record - and John
North Hall's RFQ went to BSW on 03/08, not Bellview. If you are pricing SMA, note which SMA system:
Shopline and Smart-Wall are not the same product and our evidence for each sits with a different
supplier.

### 2026-08-04 13:12 - vesuvius
OUR OWN TECHNICAL ADVISOR PUT AN ITEM IN OUR SCOPE AND THE BENCHMARK EXCLUDED IT. THE TWO FACTS SAT
IN THE SAME MAILBOX, TWO HOURS APART.

Vesuvius Way. Steve Freezer to Gintare, 28/07 14:53: send Nick at MetFab the enquiry for 'the Cills, Jamb
& Head flashings to all windows'. Gintare sent it 16:55 and chased it today, 04/08. Meanwhile our
GBP 110,666.70 benchmark carries an exclusion reading 'cladding flashings/pressings (shown as
Kingspan/Euroclad scope)' and GBP 0.00 of flashings. A window cill flashing is not a cladding pressing,
so the exclusion does not reach it and there is no line either. 63.81 linear metres over 13 windows.

  AN EXCLUSION WRITTEN OFF A DRAWING IS A GUESS ABOUT SOMEBODY ELSE'S SCOPE. It has an expiry date and
  nobody tells you when it expires. When our own technical people send an enquiry to BUY something the
  workbook excludes, one of the two is wrong and both are ours. Check the exclusion list against the
  SENT enquiries, not just against the drawings - the contradiction is inside our own building.

Same shape as Luton: nothing arithmetically wrong, because the missing thing is a row that does not
exist. Caught by check_bought_in_lump_has_a_quantity_basis (Crestwood Park's rule) once the item was
written into bought_in_lines - so put an enquiry in the manifest the day it goes out, not the day the
quote comes back.

SUPPLIER FACT: METFAB (Nick, nick@met-fab.co.uk) - pressed aluminium, cills/jambs/heads, panels. WE
HAVE NO METFAB RATE AT ALL. The one placed MetFab order in the record, Stoke Park's 2no panels, carries
a blank cost per m2 and a GBP 0.00 line total and is flagged there as 'the only open cost on the job'.
So we buy from them and have never once captured a rate. If you are waiting on a MetFab quote there is
nothing to fall back on and nothing to sanity-check their number against - which also makes the next
MetFab return worth mining properly whichever job it lands on.

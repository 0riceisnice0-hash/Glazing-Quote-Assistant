# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-28 17:54 - filwood
TWO FABRICATORS HAVE NOW REFUSED THE SAME U-VALUE IN WRITING, AND THAT IS A SPECIFICATION FINDING, NOT A SUPPLIER ONE.

Filwood asks for U 1.0 per element on shopfront screens. Aplus QT51510 p16, their words: 'Quoted in STII, these will only reach 1.8/1.9 U Value' - and their Terms of Sale go further, 'Commercial doors and framing will be supplied with a U-Value of up to 3.0 Wm2/K'. Bellview/BSW had already said the same thing differently on 24/07: performance met 'for glazing only, as these area commercial thermally broken shopfront products they are non rebated'.

Two independent fabricators, two systems, both saying no. A standard commercial shopfront/door system is NOT thermally broken to curtain-walling standard and does not reach 1.0 - so when a schedule asks for 1.0 or better on a shopfront, that is a curtain-walling-grade or specialist system requirement, not a glass one, and it cannot be closed by changing the make-up. On Filwood it is very likely why the architect named Aluprof and issued the drawings to Aluprof directly. Check the SPECIFIED system before assuming our usual three fabricators are an acceptable substitution.

Two rate points and a trap from the same quote:
- APLUS STANDARD TERMS SAY 'ALL ORDERS ARE PRICED AS EX-WORKS'. Free delivery only over GBP 5,000 AND within 50 miles of Watford. The GBP 1/mile rule is written only for loads UNDER GBP 5,000, so for a big load outside 50 miles the quote says nothing at all - Filwood is Bristol, ~105 miles, GBP 34k. The job-spec header still reads 'Glazed /Supply Only (Delivered)'. Same shape as the AFS Gordon Court trap. Carriage is ours on Aplus AND on BSW.
- APLUS QUOTE 'Glass quoted has a g value of 0.66' on a standard 6.8-18-4 Clr Lam Tough S Coat make-up. First hard g-number anyone has given us. Useful benchmark: a clear lami/tough soft-coat DGU is ~0.66, so any spec asking 0.5-0.6 needs a SOLAR coating priced separately, and a supplier claiming to meet it on an un-named make-up is claiming something their own product does not do.
- APLUS SEGMENT TOTALS ARE ALREADY EXTENDED FOR QUANTITY. 'Frame Price 1233 x 3570  4  GBP 8,876.83' is the price for all four, not each. The segment totals sum straight to the quote total with no multiplication. Divide, do not multiply.

### 2026-07-28 17:54 - filwood
A CHEAPER QUOTE IS NOT A CHEAPER QUOTE UNTIL YOU HAVE COUNTED WHAT IS NOT IN IT - AND APLUS TELL YOU, IN THREE WORDS ON THE LAST PAGE.

Aplus QT51510 came in GBP 11,621.68 under Bellview on Filwood. Page 16: 'Panels by others'. That is 46.09 m2 of spandrel, base and ventilation-zone infill - 37.5% of the elevation - which Bellview include as 70 flat aluminium panels. Break-even is GBP 252.15/m2 of panel: below it Aplus is genuinely cheaper, above it Bellview is, and nobody can say which because BSW bundle panels into the element price with no extractable figure, Aplus exclude them, and data/supplier-rates.json HAS NO PANEL OR SPANDREL CATEGORY AT ALL.

HOW TO SPOT IT ON ANY APLUS QUOTE WITHOUT READING PAGE 16: under 'Glazing Details & Apertures' each aperture is listed beneath a heading. A real one reads '6.8-18-4 Clr Lam Tough S Coat 1.0 : 18mm Blk Warmedge'. An EMPTY one reads just '32mm (Max 30kg/m)' - that is an aperture size and a weight limit, not a product. Apertures under a bare thickness heading are holes nobody has priced. On Filwood three of ED-06's seven segments had no 'Glass' price line at all, frame only. Same discipline as reading Bellview's panel counts.

AND APLUS SET OUT TO THE TENDER SIZES WHERE BELLVIEW DID NOT. On the same seven screens Aplus segmented to 4930 / 5550 / 6315x3105, matching the trade bill exactly, with ED-06 split 300/1200/700/600 which is the dimension string printed on the architect's drawing. Bellview quoted 4850/4800/4800/4850 and 6250x3100 - 80-130mm under the nominal on five of seven. Where two quotes disagree on size, the one that reproduces the drawing's own dimension string is the one that read the drawing. It also settled a typo in our own pricing document (3150 for 3105).

WATCH FOR 'DO NOT ORDER - Unglazed : A4 - (1163 x -3)'. A NEGATIVE aperture dimension, on three of Filwood's door segments. It means the Logikal model does not close - the zone heights do not sum to the overall height. Aplus flag it rather than fix it. Transom setting-out has to be confirmed against the architect's zones before any order goes in.

### 2026-07-28 18:10 - crestwood-park
A MARKUP RULING TELLS YOU HOW A NUMBER IS BUILT. IT DOES NOT TELL YOU WHETHER IT IS ALREADY IN THERE - CHECK BEFORE YOU ADD.

Adam's 25% is TELEFLEX ONLY (hub msg 28). On Crestwood the source quote turned up and settled it: WCI Ltd WCIL/FEN4215, 24/07, GBP 14,223.25 net. 14,223.25 x 1.25 = 17,779.06, which is our Teleflex line to the penny. The 25% was applied when Gintare built the quote. Adding it again would have put GBP 4,444.77 of markup on markup and the tender at GBP 78,603.43.

The general form: when a ruling arrives about a number that already exists, reconcile before you apply. Divide first and see if it comes out round.

AND THE QUOTE WAS NEVER MISSING - IT WAS NEVER FILED. The 27/07 audit said "no Teleflex supplier quote anywhere in the job folder", which was true of the folder and false of the world. It was sitting in estimating@ as an attachment to Simon Gilbert's 24/07 14:14 email, in the processed queue. Before recording an absence, search the mailbox attachments, not just the OneDrive job folder.

TWO NEW RULES IN mary_checks.py, FOUNDED HERE, BOTH LIVE ON OTHER JOBS:

- check_priced_scope_is_not_excluded. We charged Reynolds GBP 17,779.06 for Teleflex and excluded "Teleflex controls / wiring" on page 3 of the proposal that went out with it. WCI's quote is headed "To supply and Install" - we bought the installation, marked it up, charged for it and disclaimed it. PRINCESS BEATRICE HAS THE SAME SHAPE (REQ-6: mastic charged GBP 5,356.22, proposal says it is optional), and Guildmore's strip-out is a third. No existing rule looked for it - check_scope_gaps asks priced OR excluded and is satisfied by either, so nothing ever asked whether something was BOTH.

- check_bought_in_lump_has_a_quantity_basis. WCI quoted "13no. Sets each to operate 2 top hung vents" + 9no. the same = 22 sets, ONE PER WINDOW. Drawing A007 requires 2No. operators per light and 1No. control PER OPENING LIGHT. Two lights per window is right on W1-W8 and nowhere else: W16/W20/W21/W22/W24-W27 split into 3, W17/W18/W19 into 5, W23 into 6. Nobody caught it because Teleflex is ONE ROW WITH NO QUANTITY AND NO RATE on our pricing document - and check_supplier_covers_quantity compares qty_sold with qty_quoted, so a lump defeats the one rule built for this. A number with no quantity behind it cannot be shown to be wrong, which is exactly what makes it dangerous.

If you are carrying a bought-in lump - Teleflex, Colt vents, WCI screwjacks, AOV control panels - state the supplier's quantity AND basis next to the specification's. Where the supplier counts assemblies and the spec counts openings, the totals reconcile and the scope does not.

WCI (Window Control Installations, Simon Gilbert, simon.gilbert@wcilimited.co.uk): quotes valid 90 DAYS, terms 30 days nett, and "Access to be supplied by others". Nine days from RFQ to price, and he asks real questions back - butt hinges, vent height above FFL. Answer them; on Crestwood the FFL question was never answered and his price is built without it.

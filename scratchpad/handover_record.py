import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
assert lines[810].startswith("### Autopilot session log"), lines[810]

rec = """### St Mary's Refurbishment, Merthyr Tydfil / E T & S Construction - audit of the quote AS ISSUED (2026-07-27)

First substantive turn of the permanent job chat `st-marys`. The quote had already gone out on 17/07 at
**GBP 174,546.37 ex VAT**; triage had answered REQ-5 (the 24/07 addendum does not change scope) and
handed the job over. This turn audited what that price actually covers.

**The arithmetic is clean, and that is worth saying plainly.** Verified line by line against the
internal workbook `...Pricing - DO NOT SEND.xlsx`:

- All **31 Sheerline window types** reconcile to **BSW QT252799** exactly, on **both quantity and line
  total** - 31 of 31, zero variance, 98 units.
- All **7 SMA lines** reconcile to **Bellview 0000000483** at the **15% end-discounted** figure to the
  penny (Net GBP 35,708.68 - 15% = Grand Total Net GBP 30,352.38).
- Unit rates follow the MASTER PRICING DOC formula (supply + code value x 75%) on every code checked -
  MAW, ELAW, LAW, SAW, SAD, DAD, SADMAW and CW.
- The single global **INSTALLATION line of GBP 21,915.05 reconciles to the penny** as the sum of the
  house labour codes across all 39 lines.
- Brocks Hill quantity rule: **39 lines, every unit sold has a supplier quote behind it.**

**The Filwood labour-code trap did NOT bite on the biggest line.** Type AK (1825 x 5580, 2 no,
GBP 17,311.95) is correctly coded **CW** and carries curtain-wall labour properly - 10.1835 m2 x 2 x
GBP 150/m2 = GBP 3,055.05. Worth recording, because the whole point of the Filwood note was to check
this and here the answer was that someone had already done it right.

**SUPPLIER BACKING WAS MISATTRIBUTED IN THE RECORD.** MARY-HANDOVER and triage's opening note both said
the price was backed by "BSW QT252799 and Aplus QP70172". It is **BSW QT252799 (GBP 61,056.80) +
BELLVIEW 0000000483 (GBP 30,352.38) = GBP 91,409.18 exactly**. Aplus QP70172 is dated **22/07 - five
days after we submitted** - is a **different system** (Technal NEXT FZ75 / STII / Tental 50, not
Sheerline/SMA) and is quoted **UNGLAZED** ("to accept 28mm - 32mm units"). Anyone reordering against it
would have bought a different job with the glass missing. *(Stoke Park rule, and it caught something.)*

**THE BIGGEST FINDING - the tender pack sets two different U-values and Fenster followed the looser
one.** Window schedule 2376-09 states "achieve u value of 1.4 w/m2k" against every window type (33
notes) and the proposal promises 1.4. But **EDG02 "Energy and Carbon Design Guidelines - Building
Fabric"**, filed in section 7.05 of the same 08/07 pack, sets the client's minimum for the
**Refurbishment** column at **1.3 W/m2K windows, 1.2 W/m2K external doors, glazing g-value 0.4-0.3**
and air permeability <3.5. We miss all three. The energy annex sits under sustainability, nobody opens
it, and it is the tighter document.

Worse, **neither supplier states a U-value at all.** BSW give only a centre-pane glass Ug ("6.8
Lam/18/4mm Clr Tuff EcoPlus 1.0") which is not a whole-window Uw; **Bellview state no U-value, no low-E,
no soft coat, no argon, no warm edge and no coating of any kind** across GBP 30,352.38 of doors and
MC600 curtain walling - 33% of cost. No solar control product appears in either quote (zero hits for
solar, g-value, Suncool, SKN, Coolite, Planitherm), so the 0.4-0.3 g-value is definitely not priced.
Aplus's own advisory notes put the industry default in writing: commercial doors and framing "up to 3.0
W/m2/K". **REQ-15.**

**THE SM5 WEXHAM ERROR, LIVE ON A SENT QUOTE.** Schedule Type G / W.24 (2 no, 968x3620) requires "1 no.
top hung + 1 no. fixed glazing + 1 no. external door". **Bellview pos 001 quoted a door and TWO FIXED
FIELDS**, with glazing listed as "**1 x prepared for a thickness of 28mm**" - the opening vent is not in
the Smart Wall element. **BSW then fill that aperture**: "Qty: 2 Prestige Casement Location: **TYPE G
INSERT** GBP 697.58", an 854x900 **Sheerline** opening casement. So a Sheerline **70mm** casement is to
sit inside an SMA Smart Wall Pocket **100mm** frame, in a pocket prepared for a **28mm** glazed unit -
and BSW ruled in writing on SM5 Wexham (24/07) that the two systems cannot be coupled. GBP 697.58 of
cost, **GBP 8,499.66 of sell**. **REQ-16.**

**THREE UNDEFINED SCOPE BOUNDARIES (REQ-17).** (1) Our proposal **excludes** "Access/Lifting Equipment -
Scaffold, MEWPS, Towers, Forklift" while including installation of elements up to **5,580mm** tall -
**55.97 m2 of glazing is 3.62 m or taller** - and the tender **preliminaries say the opposite twice**:
item F requires the Contractor to provide "all materials, labour, **scaffolding**, plant, tools,
carriage and everything else necessary", item B requires all scaffolding "for himself and any
**Sub-Contractor**". (2) **SOW item 1.09** reads "Remove doors and windows; load into skip; existing
window structures and prepare opening to receive new **(allowed in 6.01)**" - and 6.01 is our
supply-and-fit line; our proposal excludes waste removal generally but never names it, across 107
openings. (3) **Manifestation** (schedule cl 2.24) appears in **neither** supplier quote and is
**neither included nor excluded** in the proposal.

**COMMERCIAL TIMING, from the SOW.** JCT MW 2016; start on site **14/09/2026**; completion
**11/12/2026**; **delay damages GBP 500 per calendar day**; retention 3%/1.5%; rectification 12 months.
**Both supplier quotes are valid 30 days - BSW lapses ~14/08, Bellview ~15/08 - so GBP 91,409.18 of cost
is unfixed before the job even starts**, against a fixed sell and GBP 500/day behind it. Also note MTCBC
issued SOW item 6.01 as **m2 with quantity 0** - no client quantity at all - while SOW 0.08 puts the
quantity risk on the tenderer. The Brocks Hill test (compare our area to the client's stated quantity)
**cannot be run here**; there is nothing to compare against.

**INSTALL LABOUR - a flag, not yet a shortfall.** Three elements **3,620mm** tall sit on per-unit codes:
Type F (ELAW, GBP 39.69/m2), Type H (ELAW, GBP 31.25/m2), Type G (SADMAW, GBP 117.00/m2). At the house
CW labour rate of GBP 150/m2 that is **GBP 3,520.95** more. **But** Types F and H each carry an
unexplained **GBP 1,000/unit** in the workbook's "Additional" column (GBP 4,000 total) that is in
neither supplier quote and that nobody documented. If that was a height allowance the money is already
there and only the labelling is wrong. **Adam to say what it was for** - that decides it.

**A FALSE ALARM I CAUGHT BEFORE RAISING IT.** Grepping BSW QT252799 for "obscure" returns **zero**, and
the schedule requires obscure glazing to all WCs. It is there: BSW abbreviate it **"ObsTuff"** - "6.8
Lam/18/4mm **ObsTuff** EcoPlus 1.0 **Stippolyte** 4mm", 9 panes. Search for Obs / Stippolyte / Satin /
Pattern before flagging obscure as missing. Trickle vents (62 Linkvent refs), 100mm restrictors (58) and
hinge protectors (32) are all in BSW's price too.

**Minor:** our pricing document and proposal give the site postcode as **CF77 8HA**; the client's ITT,
preliminaries and SOW all say **CF47 8HA**, and CF77 is not a Merthyr postcode.

**Checks:** `data/job-checks/st-marys-refurbishment.json` - **3 FAIL + 1 ASK**, and all four are the
findings above rather than anything new: system-depth coupling (Type G), spec covered or excluded
(manifestation + strip-out), full-height screens as curtain walling (Type G on a per-unit code at
3.62 m), and finish (neither supplier states an internal face; the architect never fixed a RAL and
"7016 Anthracite Grey" is the supplier's choice). Nine rules pass, including panic hardware on all six
door types, quotes in date, net of discount, and full supplier quantity coverage.

**Job file:** `data/jobs/st-marys.md`. **Registry hygiene:** ran the post-turn orphan check from
triage's 17:05 note and found **five handoffs still addressed to job keys that do not exist** -
`riverside`, `chester-thomas`, `manor-house`, `ninn-lane`, `lower-range`. Two matter: `lower-range` has
a **07/08 deadline** and `ninn-lane` has **GBP 100,730 out** with an unread portal message. Handed back
to triage to re-add the keys; the existing notes will then deliver without being rewritten.

"""

lines[810:810] = rec.split("\n")
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md - record inserted before line 811")

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")

row = (
 "| **St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)** - job chat `st-marys` "
 "| **QUOTE SUBMITTED 17/07 - GBP 174,546.37 ex VAT, and it STANDS.** St Mary's Campus (Blessed Carlo "
 "Acutis Catholic School), Caedraw Rd, Merthyr Tydfil **CF47 8HA** - note our own documents say CF77 "
 "8HA, which is not a Merthyr postcode. Refurbishment for Greenfield Special School; client E T & S "
 "Construction (Tom Godfrey), end client Merthyr Tydfil CBC (Chris Evans, ref 2026-024), architect "
 "**cfw architects**, drawing series **2376**. 107 units, **202.80 m2**: 31 Sheerline Prestige window "
 "type lines (98 units) + 7 SMA lines (9 units - Smart Wall Pocket doors/screens and MC600 Plus curtain "
 "walling). Install GBP 21,915.05; mastic GBP 2,808.10 and EPDM GBP 5,028.61 OPTIONAL. "
 "**THE ARITHMETIC IS CLEAN - fully re-verified 27/07.** All 31 window types reconcile to BSW QT252799 "
 "**exactly on quantity and price**; all 7 SMA lines to Bellview at the 15% discounted figure to the "
 "penny; unit rates follow the house template (supply + code x 75%) on every code; and the global "
 "install line reconciles **to the penny** as the sum of the house labour codes. **The Filwood trap did "
 "NOT bite on the biggest line** - Type AK (1825x5580, 2 no, GBP 17,311.95) is correctly coded **CW** "
 "and carries GBP 3,055.05 of curtain-wall labour at GBP 150/m2. "
 "**SUPPLIER BACKING CORRECTED: it is BSW QT252799 (GBP 61,056.80) + BELLVIEW 0000000483 "
 "(GBP 30,352.38) = GBP 91,409.18 exactly - NOT Aplus.** Aplus QP70172 is dated **22/07, five days "
 "after we submitted**, is a different system (Technal NEXT FZ75 / STII / Tental 50) and is quoted "
 "**UNGLAZED**; reordering against it would buy a different job with the glass missing. "
 "**SIX ITEMS OPEN, none of which change the price yet.** (1) **The pack sets two U-values and we "
 "followed the looser one** - schedule 2376-09 says 1.4 W/m2K (33 notes), but **EDG02 Energy and Carbon "
 "Design Guidelines - Building Fabric**, in the same 08/07 pack, sets the **Refurbishment** minimum at "
 "**1.3 W/m2K windows, 1.2 W/m2K external doors, g-value 0.4-0.3**. We promised 1.4 and miss all three. "
 "And **neither supplier states a U-value at all**: BSW give only a centre-pane Ug of 1.0 ('EcoPlus'), "
 "and **Bellview state no U-value, no low-E, no soft coat, no coating of any kind** across "
 "GBP 30,352.38 of doors and curtain walling. No solar control product appears in either quote, so the "
 "g-value is definitely not priced. **REQ-15.** (2) **Type G is the SM5 Wexham error, live** - schedule "
 "requires '1 top hung + 1 fixed + 1 external door', Bellview quoted a door and **two fixed fields** "
 "with '1 x prepared for a thickness of 28mm', and BSW fill that aperture with 'TYPE G INSERT "
 "GBP 697.58', an 854x900 **Sheerline (70mm)** casement going inside a **Smart Wall (100mm)** frame. "
 "GBP 8,499.66 of sell. **REQ-16.** (3) We **exclude scaffold/MEWPs** while prelims F and B require the "
 "Contractor to provide all scaffolding 'for himself and any Sub-Contractor' - on **55.97 m2 of glazing "
 "3.62 m or taller**, up to 5,580mm. (4) **SOW item 1.09 allocates strip-out and disposal of the "
 "existing windows into item 6.01 - our line** - and our proposal excludes waste removal generally "
 "without ever naming it. (5) **Manifestation** (schedule cl 2.24) is in neither quote and neither list. "
 "(3)-(5) are **REQ-17**. (6) **Both supplier quotes lapse mid-August (BSW ~14/08, Bellview ~15/08) but "
 "the JCT MW start on site is 14/09**, completion **11/12/2026**, **delay damages GBP 500/day**, "
 "retention 3%/1.5% - so GBP 91,409.18 of cost is unfixed before day one against a fixed sell. "
 "**REQ-5 REMAINS ANSWERED** - the 24/07 addendum does not change our scope (209 window refs, 38 types, "
 "28 s/o sizes, 38 opening patterns, 24 restrictor, 6 obscure, 33 U-value and 38 SBD notes all "
 "identical; only the magnetic integral blind note fell from 29 to 1, and we had already excluded "
 "blinds). Checks manifest `data/job-checks/st-marys-refurbishment.json` - 3 FAIL + 1 ASK, all of them "
 "the items above. Job file `data/jobs/st-marys.md`. "
 "| Adam: REQ-15 (which U-value governs - ask ET&S, and make BSW/Bellview state a Uw), REQ-16 (get the "
 "Type G fabrication confirmed before order), REQ-17 (settle access, strip-out and manifestation with "
 "Tom Godfrey in writing). Also: what was the unexplained **GBP 1,000/unit 'Additional'** on Types F and "
 "H for? It decides whether the GBP 3,520.95 of light install labour on the three 3,620mm elements is "
 "missing or already covered. Re-validate both supplier quotes if award slips past mid-August. Still "
 "open from 27/07: the Type AK blind contradiction, and pressing ET&S to issue revisions when made. |"
)

assert "St Mary" in lines[114]
lines[114] = row
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER.md line 115 replaced -", len(row), "chars")

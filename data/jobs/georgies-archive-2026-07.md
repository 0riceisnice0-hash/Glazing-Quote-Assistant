

---

# Georgie's (formerly Rosebank) - Pearce Construction (Barnstaple) - archived detail (moved 2026-08-03)

Moved out of `data/jobs/georgies.md` to bring it inside the 300-line seed contract. Nothing was edited or dropped - this is the file's own text, verbatim. The live file keeps the position, the number and what is outstanding; this keeps the working detail behind them.

## The seven things wrong with the issued tender

`scripts/mary_checks.py data/job-checks/georgies.json` returned **7 FAILED** against the issued pack.
Against the **amended pack** (below) it returns **6 FAILED** - the third-party-traces failure is cleared.
Nothing else has moved, because nothing else has been decided.

1. **FOUR OF THE SIX PANIC DEVICES ARE NOT IN THE PRICE; TWO DOORS HAVE ONE THEY MUST NOT HAVE.**
   Spec 2.39 schedules internal push-bar panic exit devices to BS EN 1125 on **D01, D02, D03, D04,
   D05, D08**, and (spec 2.38.4) thumbturn with **classroom function, 5-lever mortice, external
   cylinder, 316 stainless escutcheon, suited to the building's existing master key** on **D06, D07**.
   Bellview fitted `ACIM453 CONCEALED PANIC BAR` to the four 950mm singles only - D05, D06, D07, D08.
   So **D05 and D08 are correct; D06 and D07 carry hardware the spec forbids; D01, D03 and D04 have
   none** (handles, hold-open closers, high-security locks, cylinders keyed alike). **D02 is a 2-rail
   sliding patio with an inline patio lock and cannot physically take a BS EN 1125 push-bar** - that
   is a conflict for the CA, not a price.
   BSW said so in writing on 28/07: *"there is also no hardware schedule, so I have assumed single
   doors to be fire escapes based on the floor plans."* **Schedule 2.39 exists and was never sent to
   them.** The concealed bar needs a different leaf build (IMP041 76mm stile + IMP037N anti-finger-trap
   push-bar profile), so this is four rebuilt leaves, not a bolt-on part. **No master-key suiting is
   bought anywhere** - "cylinders keyed alike" means alike to each other, not to the building's suite.
   Spec 2.38.5 also wants a contrasting **external** pull/pad handle on every fire-exit door; not
   listed against Bellview 004-007.

2. **STRIP-OUT UNFUNDED AND UNEXCLUDED** - see the install control above. **ANSWERED 28/07 EVENING,
   ON ANOTHER JOB.** Adam on Princess Beatrice at 21:01 BST: *"we had a lot across this job compared
   to the material costs. Therefore I decided I would include the strip out (effectively FOC) in order
   to remain competitive."* And on Redditch at 21:09: *"We will include strip out to remain
   competitive."* So the house position is **absorb it**, and Fenster has already said so to a client
   in writing - Rubery Library (Pride, 21/10/2025, WON): *"All prices include installation and removal
   of old frames."* On Georgie's that converts the finding from *a gap to be priced* into *a margin hit
   already taken*: the GBP 89,229.61 stands, and the strip-out of 23 windows and 8 doorsets comes out
   of the 54.7% mark-up. **What is still wrong is that the document does not SAY so** - it is silent,
   not inclusive, so we get no credit for it against a competitor who states it. One line in the
   INCLUSIONS list fixes that and costs nothing. **This does NOT extend to the asbestos cill boards** -
   Adam's ruling is about frames.
   **AND IT NOW HAS A RATE (29/07, off St Mary's REQ-24).** Adam named Brandon Estate as the precedent
   and it reads exactly: `Removal of existing frames` GBP 330,300 / 2,202 units = **GBP 150.00 per
   opening**, identical to the penny in the earlier revision at 1,325 units, so it is a per-unit sell
   rate and is not marked up. On Georgie's: `p.strip_out(31)` = **GBP 4,650.00** over 23 windows and
   8 doorsets - 5.2% of the tender, absorbed silently. The CW screen run is a further opening on top
   and is not in that 31. Brandon's drop-in wording: *"Installation and removal of old frames is
   included within our costs."*

3. **ASBESTOS NEITHER PRICED NOR EXCLUDED.** Spec 2.43.1: internal cill boards throughout the building
   are asbestos containing and the contractor *"shall allow to include within the tender submission for
   the removals"* - express, non-provisional, inside the window scope. Our exclusions never mention
   asbestos. Pearce carry a separate Asbestos Removal element and a GBP 5,000 defined provisional sum,
   so it may be theirs, but nothing on our document says so and our installers cannot lift those
   windows without disturbing the boards.

4. **THE U-VALUE IS THE POINT OF THE JOB AND WE NEVER CLAIMED IT.** Spec 2.28, 2.33.5 and 2.38.3
   require max **1.6 W/m2K area-weighted** with **documentary evidence of the energy efficiency
   rating**. The proposal recites the requirement and never confirms compliance. Mercury state no
   U-value at all and quote "Clear Lam Tgh" with no low-E or soft coat named. Bellview state **Ug 1.0
   / Ug 1.1** and BSW **EcoPlus 1.0** - all centre-pane glass, not the whole-element Uw the spec asks
   for. **No supplier has certified an element U-value.** The reglaze would be ours.

5. **THE DOCUMENT PEARCE HOLD NAMES ANOTHER CLIENT.** Proposal title page: *"Prepared For RRR GROUP"*;
   page 2: *"Client: RRR Group"*. Sent to Pearce Construction. And the **Pricing.xlsx carries
   `dan.parker@agsurveying.co.uk`** as `dc:creator` plus two external links to
   `C:\Users\LiamO'Donnell\...` and `C:\Users\Parke\...` - REQ-27, third job this week, visible in file
   properties without opening it. **CORRECTED 29/07: converting to PDF does NOT strip the author.** I had recorded that the proposal went as a PDF so its own trace did not travel. Word carries `dc:creator` straight into the PDF's `/Author`, and the proposal Pearce hold reads **author `Nicholas Baker`**. So BOTH documents with the client name a third party, not just the workbook - and "send a PDF instead" is not a fix for the master-template author problem either. The amended pack is clean on both because docProps was rewritten before conversion.
   **AND THERE WAS A LOGO, NOT JUST A NAME.** Adam spotted it at 20:57 BST: *"This has RRR Group's logo
   and name on it. Can you please amend and send back to Neil ASAP!"* RRR GROUP LIMITED's black-and-gold
   roundel sat on the cover next to Fenster's own (`word/media/image4.png`, 255x221). **FIXED - see
   below.**

6. **THE PATIO DOOR IS QUOTED GREY.** BSW QT253508: *"Ext Colour: (7016) Grey"*, no internal colour
   stated. Our proposal's colour table promises *"Doors/CW - White internally / Brown externally"* -
   true of the Bellview items (`inside:WP, outside:Brown`), **not true of D02**. The colour disclosure
   Gintare made to Pearce covers the sash windows only.

7. **D04 PRICED AS AN 1800mm DOUBLE AGAINST A SCHEDULE THAT SAYS 950mm.** Gintare took the "Double
   Doorset" description over the scheduled width and BSW priced two 1800 doubles to match. That is the
   expensive reading - GBP 4,109.76 vs GBP 3,021.31, about **GBP 1,100** - and it is **not qualified
   anywhere on the issued document**.

### Smaller, still live

- **Obscure glazing** to bathroom/shower/WC (spec 2.33.1) neither priced nor excluded; all 23 window
  lines are clear.
- **Trickle vents wrong, and the proposal's own spec table leaves the trickle vent line blank.** Spec
  2.33.4 wants **Delta vent and grille, white PVCu, external canopy, 4000mm2 per 15m2 of floor area**
  plus one more per further 15m2; Mercury quote one **mill finish** 5000 per window regardless of room
  size.
- **Delivery is in nobody's price.** BSW are expressly *"ex works, additional delivery charges may
  apply"*; Mercury and Bellview state nothing. 31 units to Barnstaple from Peterborough and Gloucester.
- **Mercury's QL004741 states no validity period anywhere**, while our price is open 30 days to
  **27/08/2026** (proposal T&Cs clause 2). A Devon CC scheme will not be awarded inside that.
- **Dayworks rates** (spec 2.45: craftsman, painter, labourer, electrician) are expressly required and
  the issued document carries none.
- **Warranty is not back-to-back.** We offer 10 years on glass and frames with **no start date** in the
  clause and "subject to any applicable manufacturer warranties"; none of the three suppliers state a
  warranty period at all. Spec 2.38.4/2.38.5 require ironmongery with a minimum 5-year warranty and
  2.34.2 winding gear guaranteed 10 years.
- **System substitutions are named but never declared as substitutions.** Spec 2.33 names Sapa
  Dualframe 75Si, 2.38.3 names Technal Stormframe STII, both "or equal approved". We offer SMA VS600,
  SMA Smart Wall Pocket, SMA MC600 Plus and Alunet ESS47. The proposal lists them without ever saying
  they are alternatives requiring CA approval. **Aplus fabricate both specified systems for us** -
  Dualframe 75Si on Riverside QT51518 and Stoke Park, Technal STII on Princess Beatrice (Logikal
  GBP 17,499.74).

---



### Lower Range Road, Gravesend (Ermine / Gravesham BC) - the addendum was the Employer's Requirements, and the RFI I inherited had already been answered on a drawing (2026-07-28)

First working turn on `lower-range`. A single work order: Paul Taylor forwarding a Once For All addendum
notice from Tom Dixon at Ermine, subject *"ER's Document added"*, no attachment. The zip was in the
archive folder, saved 09:03.

**WHAT IT WAS.** `ERs Document.pdf` - **pages 32-51 of 51 of "Lower Range Road Section Nr.5 Project
Specific Requirements"**, author **b&m**, ref BM4108 / QAF-QS07E2 V3, dated 19/06/2026, containing exactly
part **2.13** (Further Employer's Requirements, elemental list) and **2.14** (Contractor's Proposal
Requirements). I checked whether the missing 31 pages were an error before saying so: clarification
**C08 item 7** asked for the ER because the bathroom elevations referenced it, and the answer was
*"Ignore refrences on the drawing and refer to Section 5 part 2.13."* **This addendum is Ermine issuing
precisely what that answer pointed at.** Not a truncation. The reissued Document Register confirms
nothing else changed and **the return date is still 07 August 2026**.

**IT IS A 20-PAGE SCAN WITH NO TEXT LAYER.** pdfplumber returned zero characters on all twenty pages.
**`pdftoppm`/poppler is not installed on this machine, so the Read tool cannot open a PDF at all** - and
neither tesseract nor pytesseract exists, so OCR was never an option. **PyMuPDF is installed.** Rendered
at 180dpi to PNG and read the pages, which is the Gordon Court `1. Q&As` route arrived at independently.
110dpi is enough for a full A1 drawing. That is now on the noticeboard because it will recur.

**THE BLOCKER IS GONE.** Clause **2.13.4.6.3**: *"All windows must achieve 'A' rating under WER ('B' rated
is acceptable where it is not possible to achieve 'A' rating). Glazed units should achieve a u-value of at
least 1.2W/m2K."* That answers **C22** - *"We cannot find the Energy Report. Are we to price for Building
Regulation minimum U values?"*, answered only *"Please see tender addendum 1"* - which the handover
recorded as the biggest cost driver in the package and unresolved. **WER band A, glazed unit 1.2 W/m2K.**
A standard 4-16-4 soft-coat argon warm-edge unit; WER A is the driver, not an exotic make-up.

**AND THE RFI I INHERITED HAD ALREADY BEEN ANSWERED, IN THE PACK, SINCE 27/07.** Triage flagged the
internal frame face as unstated - *"Colour - Dark Grey, with nothing said about the internal face - after
Georgie's, ask rather than assume"* - and that was the right instinct pointed at the wrong document. The
**Materials Schedule is a planning-condition document** (planning ref 20190520, condition 3, samples of
external materials). The spec lives in the **notes box of the window and door schedules**, drawings
25.578.27-30, which say **EXTERNAL: DARK GREY / INTERNAL: WHITE window & door frames & casements**. ER
2.13.4.6.2 pins the external to **RAL 7016**, matching the rainwater goods. So it is **RAL7016 foil on
white** - the standard cheaper dual-colour, exactly what BSW write as *"Grey Foil On White (7016)"*, the
string that caused the false substitution FAIL on Gordon Court. **One RFI closed, and a general rule
posted: read the schedule notes box before raising any spec RFI.**

**WHAT THE ER PUT ON OUR COST THAT NOBODY COULD SEE BEFORE.** Secured by Design across all windows,
external doors and ironmongery (2.13.4.6.7). **PAS 24:2007**, with external and front doors bought as
**door sets** (2.13.4.6.12). Accessible windows to BS 7950 or WCL 4. **Outward opening reversible units**
above 1100mm AFFL for cleaning from inside (2.13.4.6.1) - a distinct and dearer product. Child-proof
austenitic stainless friction stays. A **sample window approved before fabrication begins** (2.13.4.6.8),
which is a programme constraint more than a cost. Draught stripping throughout. And external jamb sealing
written into the windows clause itself - *"polysulphide mastic on securely wedged expanded foam
backing"* - where Gordon Court carried mastic as an optional line.

**THE TWO DOCUMENTS DISAGREE ON SAFETY GLASS, AND THE DRAWING IS THE WIDER ONE.** ER 2.13.4.6.11 wants
laminated 6.4mm minimum below 800mm from floor, or 1500mm within 300mm of a doorframe, certified BS EN356.
The schedules require **BS EN 356:2000 class P2A** and apply it to **ALL GROUND FLOOR WINDOWS AND DOORS**
including accessible glazed units, on top of the height rules everywhere else. **Priced to the drawing and
stated on the quote** - the same instinct as the Gordon Court period comparison, taken one document further
this time.

**THE GORDON COURT AOV TRAP IS SITTING ON THIS JOB.** Second-floor staircore windows **WS01 (573x1050) and
WS02 (1023x1050)** carry, in the description column and nowhere else, *"TRICKLE VENTILATION NOT REQUIRED /
AUTOMATIC OPENING VENT (1.0 SQM)"*. **These are AOVs, not windows** - a 1.0 m2 free area on a 1.07 m2
opening needs a certified unit, an actuator and a control interface. This is **REQ-22** verbatim, where
7no AOVs and smoke-shaft louvres went in as ordinary Sheerline windows and put **GBP 10,055.76** of sell
at risk. Caught **before** the take-off this time, which is the only version of that lesson worth having.
Also found: **3no louvred doors with insect mesh** - plant room DGPR01 (1585x2100) and **2no Southern Water
pipe-trench doors DGPT01/02 (1023x1275) added at revision T2 on 23.06.2026, after tender issue and
clouded**. Anyone pricing from the T1 set would miss them.

**TRICKLE VENTS ARE REQUIRED AND THEY ARE BIG.** Every habitable-room window: *"1 x TRICKLE VENT (PER ROOM)
TO PROVIDE 8,000mm2 EQUIVALENT VENT AREA"*, bathrooms 4,000mm2, staircores none. **8,000mm2 EA is large**
against a typical 2,500-5,000, so it may need a specific product or two vents per window. I checked whether
MVHR removed the requirement before assuming either way - **C11 confirms MVHR is for ventilation and heat
recovery only**, with heating by combi boiler and radiators, and it has not displaced the trickle vents.

**COMMERCIAL, AND ONE OF IT IS A REAL QUESTION.** **REQ-31 raised for Adam:** clause 2.13.4.6.1 demands a
**10-year INSURANCE BACKED guarantee** covering repair, renewal and replacement. **That is a third-party
insurance product with a premium, not the house 10-year warranty** the board records as covering glass and
frames - the distinction the forty-eighth Gordon Court turn was about. Behind it: 30 years against fungal
and rot decay, 10 against manufacturing defects, 8-year decoration guarantee or 10-year durability
statement, 5 years on factory-fitted ironmongery. Plus the Subcontractor Collateral Warranty (Appendix M2)
and a **DiPPA project bank account whose use "applies at all supply chain levels"** - so it reaches us,
not just Ermine. And **2.14.1 is why none of this can be left silent**: the Contractor's proposals must be
as the Project Specific Requirements, **any variation must be identified and stated, and the Employer may
reject it.** On this job a silent exclusion is an undeclared variation, not a qualification.

**WHAT IS STILL MISSING, NOW NAMED.** The schedules say performance is *"IN ACCORDANCE WITH ENERGY STRATEGY
REF: P3250-ENE-01 DATED JANUARY 2026 PREPARED BY QUINN ROSS ENERGY"*. **That is the real identity of the
never-issued "Tender Addendum 1"** that both C22 and C08.1 deflected to, and it is the only document left
that could move the glass spec - so it can now be chased by name rather than by reference. Also unresolved:
the schedules say to read them with **Employers Requirements ref 228208-FCG-XX-XX-RP-EA-0401-S2-P02, May
2024, Frankham Consultancy Group, Section 48.0**, plus **GBC amendments January 2026, Section 48.2** -
**neither is in the pack, and what we were just issued is a different document by a different author.**
C08.7 implies the b&m ER governs, but **nobody has said so**, and on a D&B for a council that is worth an
answer. Drawing 25.578.15 also still absent.

**SCALE.** 14 plots, all 2B/3P, over three floors - ground 01-05, first 06-10, second 11-14 - plus 2
staircores per floor, plant room and pipe trench. Openings 573/1023/1585/2148 wide by 1050/1200/1275/1500/
2100 high, the 2148x2100 units being living/kitchen/dining door-and-screen sets. **No take-off yet** - the
schedules are vector CAD, only the title block extracts as text, so every unit has to be read off a
rendered drawing. **That is the long pole with 10 days to the 07/08 return.**

Position: **not yet priced, pricing unblocked.** Emailed Adam. Job file `data/jobs/lower-range.md` written
from scratch.


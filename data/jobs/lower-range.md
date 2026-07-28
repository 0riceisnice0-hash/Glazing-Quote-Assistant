# Lower Range Road Development, Gravesend - uPVC External Windows and Doors

**Chat key:** `lower-range`
**Client:** Ermine Construction Services Ltd (main contractor) for **Gravesham Borough Council** (Employer)
**Architect:** Abbey Design (Canterbury). Employer's Agent document author: **b&m** (ref BM4108).
**Site:** The Builders Yard / Markers Lodge, 35 Lower Range Rd, Gravesend, Kent DA12 2QS (drawings say DA12 2QL)
**Project refs:** 2779 (clarification log), 4108 (contract sum analysis), 25/578 (Abbey Design drawings)
**Form:** Design and Build. Residential. Whole project value stated GBP 3m-4m.
**Our package:** External Windows and Doors (uPVC). Package lead **Tom Dixon**, Ermine.
**Portal:** Once For All marketplace. Submission is via the portal (clarification C09) - **Mary cannot access it**; a human must upload.

## PACKAGE RETURN DATE: FRIDAY 07 AUGUST 2026
Client-stated, off the Document Register header - not inferred. Re-confirmed on the register reissued
with the 28/07 addendum: **unchanged**. Pack issued 20/07, only reached us 27/07.

## Current position (28/07/2026)

**NOT YET PRICED. Pricing is now unblocked** - the 28/07 addendum resolved the U-value question that was
the stated blocker. The remaining work is the take-off and the quote.

## Documents received

| Date | What | Note |
|---|---|---|
| 27/07 16:32 | Main pack zip (32 files) | extracted to `test-results\lower-range-input\pack` |
| 27/07 16:35 | Updated Clarification Log zip (V3.2) | `...\addendum` |
| 28/07 09:03 | **ER's Document zip** | `...\addendum2` - the work order below |

All three sit in `OneDrive\Commercial\1. Tender Documents\Ermine\Lower Range Development\1. Estimating\1. Tender Documents\`.

## The 28/07 addendum (ADDGg5b2, "ER's Document added")

Paul Taylor forwarded it 28/07; the Once For All notice came from Tom Dixon. Two files: a reissued
Document Register and **`ERs Document.pdf`**.

- **It is a 20-page scan with no text layer.** Rendered at 180dpi with PyMuPDF and read page by page -
  the same route that worked on Gordon Court's `1. Q&As`. `pdftoppm`/poppler is NOT installed on this
  machine, so the Read tool cannot open a PDF directly; render with PyMuPDF first.
- It is **pages 32-51 of 51** of "Lower Range Road **Section Nr.5 Project Specific Requirements**",
  author **b&m**, doc ref BM4108 / QAF-QS07E2 V3, dated 19/06/2026. Content is exactly **part 2.13
  (Further Employer's Requirements, elemental list) and part 2.14 (Contractor's Proposal Requirements)**.
- **Not an accidental truncation.** Clarification **C08 item 7** asked for the Employer's Requirements
  because the bathroom elevations referenced it; the answer was *"Ignore references on the drawing and
  refer to Section 5 part 2.13."* This addendum is Ermine issuing exactly that. Section 5 parts 2.1-2.12
  remain unseen and have not been asked for.
- The register shows **nothing else changed** and the return date is unchanged.

## WHAT THE ER SETTLES - the U-value question is answered

**Clause 2.13.4.6.3:** *"All windows must achieve 'A' rating under WER ('B' rated is acceptable where it
is not possible to achieve 'A' rating). Glazed units should achieve a u-value of at least 1.2W/m2K."*

That answers **C22** (*"We cannot find the Energy Report. Are we to price for Building Regulation minimum
U values?"* - answered only *"Please see tender addendum 1"*). **WER band A, with 1.2 W/m2K on the glazed
unit.** Priceable: a standard 4-16-4 soft-coat argon warm-edge unit sits at ~1.2 Ug; WER A is the driver
and needs the right frame/glass combination, not an exotic one.

**Residual risk, and it is now precisely named.** The window schedules say performance is *"IN ACCORDANCE
WITH ENERGY STRATEGY REF: P3250-ENE-01 DATED JANUARY 2026 PREPARED BY QUINN ROSS ENERGY"*. That document
is **still not in the pack**, and it is the same thing C22 and C08.1 both deflected to "Tender Addendum 1".
If the Quinn Ross energy strategy demands better than WER A / 1.2, our price moves. **Chase it by name.**

## WHAT THE DRAWINGS SETTLE - the internal colour RFI is CLOSED

Triage flagged the internal frame face as unstated and, after Georgie's, worth asking rather than
assuming. **It is stated** - not on the Materials Schedule, but in the notes box of every window and door
schedule (drawings 25.578.27-30):

> COLOUR - **EXTERNAL: DARK GREY** window & door frames & casements. **INTERNAL: WHITE** window & door
> frames & casements.

ER 2.13.4.6.2 pins the external colour exactly: **RAL 7016**, to match the rainwater goods (which the
Materials Schedule also calls Dark Grey). So the make-up is **RAL7016 / anthracite foil on white** -
the standard, cheaper dual-colour, exactly what BSW write as *"Grey Foil On White (7016)"*. **Do not
raise an RFI on this and do not price through-colour.**

## Cost drivers the ER and the schedules put on our package

Everything below is quoted or paraphrased from a document, not assumed.

**Performance and glass**
- WER **A** rating; glazed unit **1.2 W/m2K** (ER 2.13.4.6.3).
- **Trickle vents ARE required** - every habitable-room window on the schedules carries *"1 x TRICKLE
  VENT (PER ROOM) TO PROVIDE **8,000mm2 EQUIVALENT VENT AREA**"*; bathrooms 4,000mm2. **8,000mm2 EA is
  large** - typical vents are 2,500-5,000mm2, so this may need a specific product or two per window.
  Staircore windows are marked *"TRICKLE VENTILATION NOT REQUIRED"*.
  (MVHR is on the job - clarification C11 confirms MVHR is for **ventilation and heat recovery only**,
  with heating by combi boiler and radiators - but it has **not** removed the trickle vent requirement.)
- **Safety glazing is wider on the drawings than in the ER, and the drawings are more onerous.**
  ER 2.13.4.6.11: laminated min 6.4mm below 800mm from floor (or 1500mm if within 300mm of a doorframe),
  certified BS EN356. The schedules require **BS EN 356:2000 class P2A** and apply it to
  **ALL GROUND FLOOR WINDOWS AND DOORS** (incl. accessible glazed units), plus windows within 800mm AFFL
  and doors within 1500mm AFFL and 300mm either side, on every floor. **Price the drawing or qualify it.**
- Obscured glazing to bathrooms/WCs - schedules say *"equivalent to Pilkington Level 3 or above"*;
  ER 2.13.4.6.4 says Pilkington Optifloat in Opal or equal approved. All windows **internally beaded**.

**Security - a whole layer that was not visible before the ER**
- **Secured by Design** for all windows, external doors and associated ironmongery (ER 2.13.4.6.7).
- **PAS 24:2007** for all doors and doorsets; **external and front doors must be purchased as door sets**
  (ER 2.13.4.6.12).
- Accessible windows to **BS 7950 or WCL 4** (ER 2.13.4.6.11).
- Cylinders to BS EN1303 grade 5 key / grade 0 attack / drill grade 2, or BS 3621/8621/10621
  (ER 2.13.4.9.5). Door chain or opening limiter to SBD. Letter plate + internal deflector at 1000mm,
  **not to fire doors**. Extended lever handles at 1050mm.

**Product and workmanship**
- Windows **typically fixed up to 1100mm AFFL and outward opening reversible units above**, to allow
  cleaning from inside (ER 2.13.4.6.1). **Reversible units are a distinct and dearer product** - check
  against the take-off before assuming standard casements throughout.
- **Child-proof friction stays**, austenitic or similar stainless steel (ER 2.13.4.6.9).
- **Sample window** with the proposed colour/finish, glazing and ironmongery, approved by the Employer
  **before fabrication begins** (ER 2.13.4.6.8). Cost and, more importantly, a programme constraint.
- Draught stripping to all external doors and windows (ER 2.13.4.6.6).
- **External sealing of jambs is ours**: *"Jambs to be sealed externally with good quality, neatly
  applied polysulphide mastic on securely wedged expanded foam backing"* (ER 2.13.4.6.5). On Gordon
  Court mastic was carried as optional - here it is written into the windows clause.

**Items easy to miss - all from the schedules**
- **STAIRCORE AOVs.** Second-floor staircore windows WS01 (573x1050) and WS02 (1023x1050) are marked
  *"AUTOMATIC OPENING VENT (1.0 SQM)"*. **These are not ordinary windows.** This is exactly the
  Gordon Court error now sitting on the board as **REQ-22** (7no AOVs and smoke-shaft louvres specified
  as motorised Colt units, priced as ordinary windows, GBP 10,055.76 of sell at risk). A 1.0 m2 free
  area on a 1.07 m2 structural opening needs a certified AOV with an actuator, and the control panel /
  power interface has to be settled with the electrician.
- **Plant room louvred door** DGPR01, 1585x2100, **with insect mesh**.
- **Southern Water pipe trench: 2no louvred doors** DGPT01/DGPT02, 1023x1275, with insect mesh -
  **added at revision T2 (23.06.2026)** on drawing 25.578.30 and clouded. A late addition; easy to miss
  if anyone works from the T1 set.
- **Communal entrance door screen set** must house a flush-mounted anti-vandal entry phone panel with
  push buttons (ER 2.13.4.8.2), and the audio door entry system is to be **approved by SEA Systems Ltd**
  (ER 2.13.7.12.1). Our screen has to accept their panel - cut-out, and who supplies/fits, is an
  interface to settle.
- **Entrance canopy soffits are to match the window and door frames** (ER 2.13.4.3.2) - not our scope,
  but a colour-match coordination our RAL7016 has to satisfy.
- Ermine's own Contract Sum Analysis puts **02.06.03 External sealants** and **02.06.06 Window boards**
  inside element 02.06 "Windows and External Doors". Expect them to be looked for in our number -
  **state clearly whether window boards are in or out.**

## Scheme scale (from drawings 25.578.27-30)

**14 plots, all 2B/3P, over three floors** - ground 01-05, first 06-10, second 11-14 - plus
**2no staircores on each of three floors**, a plant room and the pipe trench. Typical structural
openings 573, 1023, 1585 and 2148 wide; 1200, 1500, 1050, 2100 and 1275 high. Larger 2148x2100 units
are the living/kitchen/dining door-and-screen sets (DG0201, DG0301, DG0401, DG0501...).

**No take-off has been done yet.** The schedules are vector CAD - only the title block extracts as text,
so each unit has to be read off the rendered drawing. Render with PyMuPDF at ~110dpi; all four are
readable at that. **This is the next task and it is the long pole before 07/08.**

## Open RFIs / what to chase

1. **Quinn Ross energy strategy P3250-ENE-01 (January 2026)** - named on the window schedules as the
   performance basis, absent from the pack. Same document C22 and C08.1 both deflected to "Tender
   Addendum 1", which has still never been issued. **The one thing that could still move the glass spec.**
2. **Which Employer's Requirements governs?** The window schedules say to read them with *"Employers
   Requirements ref 228208-FCG-XX-XX-RP-EA-0401-S2-P02 dated MAY 2024 prepared by **Frankham Consultancy
   Group**, Section 48.0 (48.1 to 48.3.13)"* plus *"ER amendments/changes dated January 2026 prepared by
   Gravesham Borough Council, Section 48.2"*. **Neither is in the pack**, and what we have just been
   issued is a **different document by a different author** (b&m, BM4108, Section 5 part 2.13, June 2026).
   C08.7 points bidders to the b&m one, which implies it supersedes - **but nobody has said so.** Ask.
3. **Drawing 25.578.15 REV T1** - referenced by C08, still absent (the pack holds .10-.42 with gaps).
   C08.1's answer says the thermal performance statement it carries is in Tender Addendum 1.
4. **AOV interface** - who supplies the actuator, control panel and power to WS01/WS02?
5. **Window boards** - in or out of our package (Ermine's CSA element 02.06.06 says they expect them).
6. ~~Insurance-backed guarantee~~ **ANSWERED 28/07 - we hold one (CPA). Premium still outstanding.**

## Commercial conditions Adam needs to see

- **10-year INSURANCE BACKED guarantee** required, *"to cover repair, renewal and replacement of any item
  installed"* (ER 2.13.4.6.1). An IBG is a third-party insurance product with a premium - **not the same
  as our standard 10-year warranty**, which the board records as covering glass and frames.
  **ANSWERED - REQ-31, Adam on the dashboard 28/07 21:12:** *"We do have an IBG with The CPA. We are aslo
  FENSA registered."* Option taken: *"We hold an IBG - Adam supplies the cost and I price it in."*
  So the line is **priced in, not qualified**. Two things still open on it:
  - **The premium was not supplied.** Line reads TBC until Adam gives it (per job / per m2 / % of value).
    Asked on the dashboard 28/07. **Nothing goes on the quote until it lands.**
  - **Eligibility is not proven for THIS contract.** CPA and FENSA are both built around replacement
    windows in occupied dwellings; Lower Range is **new build**, we are a **subcontractor to Ermine**,
    and the policy has to run in the **Employer's** favour. Asked Adam to confirm with CPA that they will
    issue on that basis. If they will not, we qualify under ER 2.14.1 rather than price it. Do not write
    the guarantee onto the face of the quote until this is confirmed.
- Supporting guarantee stack (ER 2.13.4.6.10 and .12, windows and doorsteps alike): **30 years** against
  fungal and rot decay; **10 years** against manufacturing defects; factory-applied decoration **8-year
  guarantee or 10-year durability statement** against blistering/cracking/flaking/erosion; factory-fitted
  ironmongery **5 years**.
- **Subcontractor Collateral Warranty** required - Appendix M2 template is in the pack.
- **Project bank account (ER 2.14.3).** GBC require a specific project bank account for the contract, of
  the Digital Parallel Payment (DiPPA) type such as Saible. *"Use of the account also applies at all
  supply chain levels."* **That reaches us as a subcontractor**, not just Ermine.
- **ER 2.14.1:** the Contractor's proposals must match the Project Specific Requirements; **any variation
  must be identified and stated, and the Employer may reject it.** So every qualification we make has to
  be written on the face of the quote - a silent exclusion is not a qualification here.

## Decisions taken

- **28/07** - internal colour RFI closed on documentary evidence (schedules 27-30 notes: internal white).
  Price RAL7016 foil on white, dual-colour, not through-colour.
- **28/07** - treat WER A / 1.2 W/m2K glazed unit as the performance basis for pricing, and qualify the
  quote as subject to the Quinn Ross energy strategy P3250-ENE-01 which we have never seen.
- **28/07** - price the safety glazing to the **drawings** (P2A to all ground floor windows and doors),
  which is the more onerous of the two documents, and say so on the quote.
- **28/07 (evening)** - REQ-31 closed on Adam's answer: we hold an IBG with **The CPA** and are **FENSA
  registered**, so the guarantee is **priced in rather than qualified away**. Premium TBC and CPA
  eligibility for a new-build commercial subcontract still to be confirmed - both back with Adam.

## History

- **27/07** - triage received the pack from Paul Taylor, opened this chat, verified the V3.2 clarification
  addendum touched nothing on windows or doors, and flagged Tender Addendum 1 and drawing 25.578.15 absent.
- **28/07** - ER's Document addendum assessed (this turn). U-value answered, internal colour closed,
  AOVs / louvred doors / P2A / SBD / IBG surfaced. Return date re-confirmed 07/08.
- **28/07 21:12** - Adam answered REQ-31 on the dashboard (dashmsg-49). IBG held with The CPA, FENSA
  registered. Replied same night with the two residuals (premium, CPA eligibility on new build).
  No new request raised - 21 are already open.

## NEXT TURN, IN ORDER

1. **The take-off.** Still the long pole and nothing else has moved it. 10 days to 07/08.
2. Chase **Quinn Ross P3250-ENE-01** by name (via Paul) - the only thing that can still move the glass.
3. Pick up the **IBG premium** from Adam when it comes and price the line.

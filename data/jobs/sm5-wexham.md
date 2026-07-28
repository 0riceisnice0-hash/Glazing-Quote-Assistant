# SM5 Wexham SEND Bungalow - job record

**Chat key:** `sm5-wexham` | **Client:** SM5 Developments (end client Slough BC) | **Package lead:** Ryan Steadman
**Site:** Wexham Primary SEND Facility, Church Ln, Slough, Wexham, SL3 6LU
**Architect:** Kendall Kingscott | **Drawing:** 260259-WEX-KK-XX-L0-D-A-5201 P01 | **Spec:** 260529 (NBS)
**Estimating Log:** row 8637, controller Gintare, status column "Sent to ADAM"
**Archive:** `Commercial\1. Tender Documents\SM5 Developments\Wexham Primary\` (read-only)

---

## Where this stands (28/07/2026)

**NOT SUBMITTED.** Adam confirmed it on the dashboard on 28/07: *"this has not been submitted... I did
approve it, but later noticed some changes before it went out, so it's not gone to client."*

**Package return date: 14 JULY 2026** - not 24/07, which is what my board carried until today.
Two independent sources:

- Document Register inside the tender zip: *"Package return date: 14 July 2026"*, package lead Ryan
  Steadman, generated 03/07/2026, marked "Initially issued". No later register exists in the folder.
- Estimating Log row 8637: enquiry 03/07, **Deadline 14/07/2026**, controller Gintare.

The 24/07 I had recorded was never a client date - it is the date of the aluminium revision, and I
turned it into a deadline. Same failure as St Mary's, where the board carried the Bellview quote
validity (16/08) as the deadline.

**Whether ANY quote was ever submitted is unresolved and is the open question with Adam.** On 22/07 I
recorded a 14/07 quote of GBP 14,575.88 (uPVC windows + aluminium doors). I can no longer open the file
that told me so: the client pricing workbook was overwritten by the aluminium version on 24/07 13:42Z
under the same filename. The Estimating Log status column reads "Sent to ADAM", not issued, and W/L is
blank. So I cannot evidence a send on 14/07 either. Asked Adam directly.

## Scope

9 openings off drawing 5201, all-aluminium (Adam ruled 22/07 that the uPVC quotes were *incorrect*, not
merely a spec preference):

| Ref | Size | Code | System as priced 24/07 | Note |
|---|---|---|---|---|
| W.01 | 2424 x 2400 | ELAW | Sheerline | two coupled frames; coupled to ED.01 in the East run 1212+1212+1227 |
| W.02 / W.03 / W.06 | 1200 x 1200 | MAW | Sheerline | |
| W.04 / W.05 | 869 x 2400 | LAW | Sheerline | flank ED.02, West run 869+1872+869 |
| W.07 | 2300 x 1200 | LAW | Sheerline | |
| ED.01 | 1227 x 2400 | SAD | SMA Smart Wall Pocket | single entrance door |
| ED.02 | 1872 x 2400 | DAD | SMA Smart Wall Pocket | fire-exit double doors |

Frames **and** panels are WHITE - the grey on the drawing is shading, not colour (Adam, 22/07).
U-value 1.6 W/m2K **whole installation, as an average** (Adam's ruling 24/07 - my earlier reading that
the cold doors failed it on their own was wrong). Match adjoining building. FENSA cert with O&Ms (L10/895).

## The number

**GBP 20,563.57 ex VAT priced 24/07 - PRICED, NOT ISSUED.** Workbook
`3. Client Quote\SM5 Developments - Wexham Primary Pricing.xlsx` (24/07 14:42), proposal PDF alongside
it (14:43), both FAO Ryan Steadman. Installation GBP 1,960. Optional mastic GBP 251.37, EPDM GBP 467.22.

Supplier backing, both verified to the penny:

- **BSW QT253300** (23/07, Sheerline Prestige Hipca White) - GBP 7,683.49 nett across the 7 windows.
- **Bellview 0000000475** (SMA Smart Wall Pocket doors) - GBP 4,682.58 net after 15%. ED.01 2,198.97 x
  0.85 = 1,869.1245 and ED.02 3,309.95 x 0.85 = 2,813.4575, which are exactly the supply figures in the
  workbook. Valid to ~12/08.

Supplier cost total GBP 12,366.07. Earlier uPVC quote on file: BSW QT252647 (13/07, Liniar, GBP 3,373.30
nett, includes both W.01 coupled frames butt-jointed).

**Mary's benchmark, 22/07: GBP 18,611.95** (`outputs\SM5 Wexham Bungalow - Fenster Pricing Document
(house format).xlsx`) - BSW alu casement register medians + GBP 25/m2 safety-glass uplift, doors at
Bellview net. Calibration entry logged; see the correction note in `data/calibration.json` - the
"actual" is a priced, unissued figure, so treat the -9.5% as provisional.

## Open on the un-sent pack - all still free to fix

1. **The panic bar is still not priced.** Adam accepted on 24/07 that ED.02 (fire-exit doubles) was
   quoted with no panic/push bar against a drawing requiring an SAA push bar overriding the locks. The
   ED.01/ED.02 supply figures are still Bellview's originals to the penny, so no money has moved. This
   is the catch that was recorded as "corrected" and is not.
2. **Two of Adam's three queries went to the wrong supplier.** Gintare put restrictors, panic bar and
   handles to BSW on 27/07 10:10. Restrictors are fair - BSW's windows. But ED.01/ED.02 are Bellview's
   doors, so BSW cannot answer for the panic bar or the handles. **Nobody has asked Bellview.** No BSW
   reply in estimating@ as of 28/07 either.
3. **The pack is pre-correction on the coupling ruling.** All seven windows sit under a "Sheerline
   Windows" heading; the proposal says the same in words. Adam's 24/07 ruling: W.01 (coupled to ED.01)
   and W.04/W.05 (flanking ED.02) **cannot be Sheerline (70mm) against a Smart Wall door (100mm) - there
   is no coupler between the depths.** They must be Smart Wall elements from Bellview. Only W.02/03/06/07
   stay Sheerline. Price moves up.
4. **The proposal promises 1.4 W/m2K flat** (p3, Glazing Specification) - tighter than the drawing's own
   1.6, against SMA's published **1.8 W/m2K for Smart Wall doors** (datasheet surfaced on St Mary's,
   27/07). This does not reopen Adam's averaging ruling; the document simply does not state an average.
   The same block describes the glazing as "6.8 laminated / 4mm toughened", which is the **door**
   make-up only - the BSW windows are 6.8 / 18 argon EcoPlus 1.0.
5. **REQ-27 defect present.** The pricing workbook carries `dc:creator` =
   "Dan Parker;dan.parker@agsurveying.co.uk" and two external links to other companies' Outlook caches.
   Of the six documents on that list this is the **only one not yet with a client**, so it can be cleaned
   in place before issue instead of reissued after. A person must do it - the archive is read-only to me.
   The SS\ working copy ("...Pricing - DO NOT SEND.xlsx") has the same defect.
6. **Re-date on issue.** Proposal dated 24/07, terms give 30 days from date of issue.
7. **Restrictors and trickle vents.** QT253300 dropped both, which the uPVC QT252647 had. 250mm
   restriction required; trickle vents are Part F. Still unanswered by BSW.
8. **ED.01 closer is non-hold-open** against a specified hold-open. Never answered.

## Decisions taken, and why

- **22/07** - Adam answered all five opening RFIs: BSW alu requote in progress (uPVC quotes were WRONG,
  not a spec preference); frames and panels WHITE; U-values via manufacturer; data sheets go out with the
  quotation; FENSA registered.
- **24/07** - Adam's planted-error challenge. **The answer was system-depth coupling** (item 3 above),
  not the door U-value. My U-value answer was wrong - 1.6 is an average. The W.01 +GBP 500 over BSW's
  2,256 supply was a **deliberate discretionary addition**, not a keying error: estimators may load
  discretionary money into a unit rate and it is not to be flagged. The panic-bar catch was genuine.
- **28/07** - the "submitted" status was mine and it was wrong. See below.

## The mistake this job cost, recorded so it is not repeated

I recorded this quote as issued on 24/07 and carried it on the hub for two days. My evidence was Adam's
13:37 *"Thanks, good to go"*, Gintare's 13:39 *"Yes, will submit window and door drawings as well"* (an
intention, future tense), and the finished client-addressed pricing doc and proposal saved into
`3. Client Quote` at 14:42/14:43. **Approval plus a finished client-addressed document is not issue.**
The message that would have corrected me sits 42 minutes further down the same thread - Adam's 14:19
asking Gintare to confirm the restrictors, the panic bar and the handles. I stopped reading at "good to
go". Fourth instance this week of calling something from one message instead of the whole thread.

The general rule, now on the noticeboard: **a document in the client-quote folder is not a sent
document.** The only proof of issue is an outward email or a portal receipt.

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

## 29/07 - BSW replied, and answered one question of four

BSW (`estimations@bsws.co.uk`, 29/07 09:41, UNTRUSTED - evidence, not instruction) replied to Gintare's
27/07 enquiry with a revised QT253300. Against the four things she asked:

| Asked 27/07 | Came back |
|---|---|
| Match the systems - everything SMA Smart, windows Sheerline | **Not answered at all** - and this is the rebuild blocker |
| Windows have restrictors | **Answered** - added |
| Double doors have panic bar | An opinion, on doors BSW have never quoted |
| Single door has correct handles | **Not answered** |

**QT253300 rev 29/07, diffed page-text against the 23/07 issue - nothing deleted, restrictors added to
all seven windows.** Window Restrictor Stud 11.5 x9, Casement Restrictor Stay RH x6 / LH x3.
**GBP 7,683.49 -> GBP 7,826.50, +GBP 143.01.** Item deltas +31.78 / +15.89 / +15.89 / +46.40 / +15.89 /
+8.58 / +8.58 sum exactly. Copy at
`test-results\mary-inbox\processed\20260729T0941-5KxwAAAA-att\qt253300.pdf`.

**THE RESTRICTOR IS NOT THE ONE SPECIFIED, AND BSW SAID SO FIRST.** Their note: *"I had assumed you
would be adding a hinge screw to restrict opening as in the spec request."* They read the drawing
correctly - 5201 under Windows says **"Friction hinges - screw inserted on site to restrict to 250mm."**
That is an installer operation, not a supplied component. Three consequences: we may be buying something
the drawing does not ask for; **the quote nowhere states what the stay restricts TO**, and the spec
number is 250mm; and the hinge screw remains an on-site operation that is not in our installation line.
The uPVC quote used "Res-Loc Restrictor RH + Stud" (key-releasable), the aluminium one a plain casement
stay - same count, different product, and on a SEND school the releasable type may be what is wanted.

**BSW HAVE NEVER QUOTED A DOOR ON THIS JOB.** QT253300 is 7 Prestige casements - 7 window handles, 7
window locks, no door line; QT252647 was 8 windows, also none. ED.01/ED.02 are Bellview's. So *"we have
not included panic bars in the commercial element as they have requested hock locks... if locked the
panic bar would not be able to override the hocks"* is an opinion about a package BSW does not hold, and
**the panic bar question is still unanswered by the supplier who owns it.** Day five.

**BUT THEIR TECHNICAL POINT IS RIGHT AND IT IS THE FINDING OF THE DAY.** Drawing 5201, Rear Double
Doors, asks on the same leaf for *"Europrofile hook lock with key / key access"* **and** *"Fire exit door
hardware required on the internal side of the doors to include SAA push bar which overides any locking
mechanism installed."* A hook lock cannot normally be retracted by a push bar. The client's own schedule
contradicts itself on a fire exit.

**AND THE DOCUMENT THAT WOULD SETTLE IT WAS NEVER ISSUED.** 5201 says the sets are *"preliminary and must
be confirmed, in detail, by the University ironmonger. See specification section P21."* **There is no
section P21 in spec 260529** - it runs C20, C90, J41, K10, K13, K32, K45, L10, L20, M10, M45, M50, M60,
N10, N13, Q40. **Our own section L10 reads "Products - Not Used"** - it specifies no window product at
all, only execution clauses (760 replacement window installation to BS 8213-4; 820 ironmongery fixing;
895 FENSA cert with O&Ms). L20 turns out to be internal timber doorsets and a London Wall acoustic
partition. So the entire product and ironmongery specification for this package is one preliminary block
on a drawing pointing at a section we do not have. **That is an RFI to Kendall Kingscott, and until it is
answered the quote must carry a written assumption on the fire-exit hardware.**

**TRICKLE VENTS: still absent, still never asked.** QT252647 (uPVC) carried *"4000 External Linkvent
White (Set)"* on all 8 frames. QT253300 has none - the word "vent" does not appear, in the 23/07 issue or
this one. Today's revision restored the restrictors and not these, because they were not in the question.
**The requirement is genuinely unstated:** no trickle vent, no background ventilation and no Part F
anywhere in the 37-page spec, and none on the drawing. What is certain is that BSW judged them necessary
for the uPVC scheme and not the aluminium one, same building and rooms, and nobody has asked why.

**HANDLES: BSW's own quote answers the window half, and the answer is no.** Drawing asks for **"SAA espag
locking handles"** on windows and **"SAA 300mm 'D' handles"** on both doors. QT253300 quotes **"Signature
Handle White" x7**; QT252647 the same. Adam's 22/07 ruling was that frames and panels are white - the
handle finish is a separate line in the schedule and it says satin anodised aluminium, and the drawing's
IMPORTANT NOTE adds *"All ironmongary is to match as well"* the adjoining building. Not called an error -
it may be what the adjoining building has - but it is a divergence on all 7 windows and both doors.

**MONEY.** The house template is supply + code value x 75%, verified on every line of this job (ELAW 850,
MAW 550, LAW 650, SAD 1200, DAD 2000 - each reconciles exactly against the workbook's unit rates), so the
+GBP 143.01 passes straight through: **GBP 20,563.57 -> GBP 20,706.58 if nothing else moved.** It will
move - the coupling rework is still outstanding and pushes it up.

**REDDITCH 6 m2 CHECK - NEGATIVE HERE, WITH A WARNING.** Largest unit is W.01 at 5.8176 m2, so no unit
crosses 6 m2 and the 125% adder does not fire; engine and template agree. **But** the East run
(1212+1212+1227 x 2400 = ~8.8 m2) and West run (869+1872+869 x 2400 = ~8.7 m2) both cross 6 m2 if
Bellview quote them as coupled door-and-side-screen assemblies under Adam's ruling. **Re-run the check
after the rework.**

Reported to Adam by email 29/07 ("BSW answered one of four, and they are right about the restrictor").
**No request raised** - 15 are open and none of this outranks them; offered to put the ironmongery
conflict on the board if he wants it there.

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
7. **Restrictors - part answered 29/07.** Restored on all 7 windows at +GBP 143.01, but as a supplied
   restrictor stay where the drawing specifies an on-site friction-hinge screw restricting to 250mm, and
   the quote does not state the restriction dimension. **Trickle vents still absent and still unasked.**
8. **ED.01 closer is non-hold-open** against a specified hold-open. Never answered. Note the drawing
   schedules a *concealed overhead hold open closer* on BOTH doors.
9. **Window and door handles are quoted white against a schedule asking for SAA** (satin anodised
   aluminium) on all 7 windows and both doors. Raised 29/07, not yet ruled on.
10. **The ironmongery schedule contradicts itself on the fire exit** (hook lock vs push bar overriding
    any locking mechanism) and its authority - spec section P21 - **is not in the tender pack**. RFI to
    Kendall Kingscott.

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

# Grange Hill Methodist Church - Chigwell (London) PLC

**Chat key:** `grange-hill` | **Package:** WD001 Windows and Doors | **Package lead:** Luke Baker
(luke.baker@chigwellgroupplc.co.uk, Senior QS, 020 8500 4100, 07547 184089) | **Enquiry route:**
Once For All Marketplace -> Paul 24/07 08:08. **Est. whole-project value (client's own figure):**
GBP 100k-250k. Works Nov 2026 - Jul 2027.

## Position - ISSUED 29/07/2026 16:07

**GBP 39,006.77 ex VAT to Chigwell (London) PLC, FAO Luke Baker.** Sent by Gintare from
estimating@, cc Adam, five attachments. Adam approved at 16:02 - *"Good to go, there are some
queries but let's get this one sent out!"* - with my corrections in front of him. His call, made
on a package two days past its return date. Ledger `issued:grange-hill:2026-07-29` recorded, which
is the handover to Jacob. **The job is Jacob's now** (Adam's rule, 28/07).

Our quotation validity is 30 days and the BSW material costs behind it expire **28/08/2026**,
against works programmed Nov 2026 - Jul 2027. Return date had been 27/07.

### ONE THING IS OUTSTANDING AND IT IS FIXABLE

**The pricing workbook Chigwell now holds names another firm as its author.** REQ-27 for the third
time - Georgie's to Pearce 28/07, SM5 Wexham 12:22 today, now this.

- `dc:creator` = **Dan Parker;dan.parker@agsurveying.co.uk**
- two live external links Excel offers to update on open: `agsurveying.sharepoint.com`,
  `C:\Users\LiamO'Donnell\...Electrical Template - Draft - REV010.xlsx`, and
  `C:\Users\Parke\...The Datum Group Electrical - TEMPLATE - Detailed breakdown Rev 5.xlsx`
- the proposal PDF's `/Author` and XMP creator both read **Nicholas Baker**

**A cleaned pack is already built and verified:** `outputs\grange-hill-reissue\` - all five files,
zero traces, total asserted unchanged at GBP 39,006.77. Built by `scratchpad\gh_clean_reissue.py`
from the issued copies, which are kept untouched in `scratchpad\gh-issued-to-luke-att\` because
they are the record of what the client received. **Adam was told at 16:1x; the pack was finished
after that email and was deliberately NOT sent as a second one (Zac's 14:57 rule - one email when
it settles, never a chain). It goes in the 07:45 update with the files attached.**

**WHY IT WILL KEEP HAPPENING, and this corrects my own noticeboard post from this afternoon.**
Scrubbing `templates\MASTER PRICING DOC.xlsx` protects documents THIS system generates and nothing
else. Gintare builds from her own copy - her proposal carries a link field to
`C:\Users\fenst\Downloads\Pricing Doc Template.xlsx` - so the infected template is the one that
reaches clients and the clean one is the one that does not. Her file needs cleaning once, by a
human, and then it stops.

### What was done RIGHT, and it is the thing that has burned us before

The issued workbook was **properly cut to sell-only**: no Frames column, no buy prices, no BSW
name, no product codes. The drawings issued with it are BSW's own sheets with prices and supplier
identity removed and Fenster's logo on. Gordon Court sent this same QS five supplier quotations
with 42 line prices. That did not repeat.

### What went out unfixed - all raised to Adam 14:40, before approval

None of these were changed between the 13:10 check pack and the 16:07 issue. They are now
questions about a document the client HOLDS, not defects to fix before sending.

1. **One window priced short - GBP 419.32 of BSW bought and not sold.** Twelve units priced,
   thirteen in BSW's quote and thirteen on the drawings that went with it: seven 1200x1183 where
   BSW quote eight. ~GBP 830 of sell. **This one is between us and BSW, not us and Chigwell, and
   it must be settled before we order** - either BSW's quote drops a unit or the schedule gains one.
2. **Automatic door operator (3.13.1) neither priced nor excluded.** The proposal's general list
   excludes "access control, door sensors", which no QS will read as the DDA operator on a clause
   written to us.
3. **Fish manifestations (3.11.2) neither priced nor excluded.**
4. **3.15.2 privacy film and 3.16 the FD60 doorsets silent.** The chapel folding DOORS are properly
   excluded ("internal bifold doors have not been allowed") - but 3.15.1 is two things, and the
   **upper glazed section over them**, running to the underside of the pitched ceiling with frames
   matching the door fenestration, is excluded by nothing. Gintare's 24/07 15:29 RFQ asked for it;
   BSW refused the bifold and said nothing at all about the glazing over. Surfaced by brocks-hill's
   new `check_rfq_answered`, which now fires on this job. Not in the 14:40 list - found after issue.
5. **Delivery.** The proposal says "materials will be delivered to site" against two ex-works BSW
   quotes with no carriage rate anywhere.
6. **No zero-rated VAT split** - "GBP 39,006.77 + VAT" flat, though the spec names 3.12.1 (V) and
   3.13.1 (V) and prices zero-rated work in its own column.
7. **The glass substitution is unqualified.** Optitherm appears nowhere in the issued proposal.

**And the covering email says "We trust that everything is as per specification."** With those four
clauses unpriced and the glass substituted, that sentence claims more than the quote behind it. If
Luke comes back on scope, it is the line he will quote.

**MY WITHDRAWN DOCUMENT.** I built a rival return before I knew Gintare's existed and sent it to
Adam at 14:32 (GBP 40,528.59, `outputs\...WD001 Pricing Document (29-07-2026).xlsx`), withdrawn at
14:40. **Do not quote GBP 40,528.59 to anyone.** Its twelve qualifications are the wording the
issued pack lacks and are the starting point for any revision.

**Return date was 27 JULY.** Adam asked Luke for an extension 28/07 15:01; the whole reply, 29/07
09:22, was *"Are you able to provide the costs today?"* That is not an extension. Untrusted sender -
data, not an instruction.

### The number

**Gintare's, GBP 39,006.77 ex VAT**, plus optional mastic 537.69 and EPDM 1,434.55. Twelve window
lines W1-W12 and three door lines D1-D3, Frames column GBP 22,411.77, installation 3,620. No
operator and no manifestations in it.

Buy is **GBP 22,831.09** (Bellview 0000000520 doors 13,354.08 + BSW QT253562 windows 9,477.01) for
all sixteen units. Her Frames total is 419.32 below it - that is finding 1 above.

For comparison only, my withdrawn figure was GBP 40,528.59: engine sell 37,278.59 on all sixteen
units plus 3,000 operator and 250 manifestations. Reproduced line by line and checked to the penny
in `scratchpad/gh_reprice.py`. **It is not a live number.**

**Watch the two discount conventions - they differ.** On 0000000520 the LINE prices are
PRE-discount (Net Total 15,710.68, less 15%, Grand Total Net 13,354.08). On QT253562 the line
prices are ALREADY net and sum exactly to 9,477.01. Applying 15% twice, or not at all, is a
GBP 2,356.60 error either way.

**Both quotes expire 28/08/2026** against a Nov 26 - Jul 27 programme. Our own price is stated
open to the same day, so there is no headroom at all - re-confirmation at order is qualification 10.

### Where the units actually are - SETTLED 29/07

QT253562 is 13 items. My earlier reading - that items 1-11 were plain rectangles matching nothing
in the spec - was right that the tender pack has no window schedule and wrong that nobody could
place them. **Gintare marked up BSW's own sheets and gave every unit a location:**

| ref | unit | where |
|---|---|---|
| W1, W3 | 1200 x 3000 | west |
| W2, W4, W5-W9 | 1200 x 1183 | west (seven priced; **BSW quote eight**) |
| W10 | 2000 x 2100 | south |
| W11, W12 | 2900 x 2400 raking pair | south, over the door element |
| D1 | 1200 x 2100 single door | west |
| D2 | 4588 x 2100 door element | west |
| D3 | 5900 x 2300 door element | south |

So the west elevation carries nine windows plus two door elements, and clauses 3.11-3.14 describe
the screens without ever scheduling those windows. The eighth 1200x1183 is the open item.

### The documents

- **Gintare's pack (13:10) is the one that goes.** Copies in `scratchpad\gh-quote-to-check-att\`.
- `outputs\Grange Hill Methodist Church - WD001 Pricing Document (29-07-2026).xlsx` - **withdrawn**.
  Useful only for its twelve qualifications, which are the wording her pack lacks. Built sell-only:
  working columns deleted rather than merely outside the print area, no third-party traces.
- The proposal HTML generated alongside it **must never go out** - three "insert site photo"
  placeholders on the cover and no site photography exists for this job.
- The 24/07 benchmark at GBP 27,560.07 is **DEAD**. It went to Adam and Zac only, never to Chigwell.
- `templates\MASTER PRICING DOC.xlsx` was still carrying the REQ-27 external links to
  `C:\Users\Parke\` and `C:\Users\LiamO'Donnell\` - the 28/07 fix cleaned the output, not the
  template. Scrubbed 29/07, backup at `.pre-scrub`.

## Scope

Fenster's package is defined by nothing more than the words "Windows and Doors" plus the full
main-contract specification. **The work package description behind "View enquiry" has never been
opened.** That is the root of every scope question here.

| clause | what | treatment |
|---|---|---|
| 3.11.1 | Alu windows/doors, white PPC, polyamide breaks, Optitherm S1 solar Arctic Blue outer / S1 plus inner | priced |
| 3.11.2 | Fish symbol manifestations, client supplies artwork | priced (GBP 250 allowance) |
| 3.12.1 | West full-storey screen + 1200mm door, level threshold, 3-point lock, Yale Platinum keyed alike. Upper windows to the pitched roof/ceiling | priced |
| 3.13.1 | Disabled access west door - operator, strengthening, electrics, push pads both sides, emergency release, keyed isolator | priced (GBP 3,000 allowance) |
| 3.14.1 | South full-storey screen to the roof pitch + 2No 1200mm doors to approx 2300mm, gate bolts to the secured leaf | priced |
| 3.15.1 | Chapel alu folding doors approx 5.8m + fixed glazed section over, dark brown PPC, bronze tinted | **EXCLUDED**, qualification 2 |
| 3.15.2 | Frosted strip privacy film to the folding door glass | **EXCLUDED**, qualification 3 |
| 3.16.1 | Remove existing fire check door to corridor incl framing | **EXCLUDED**, qualification 4 |
| 3.16.2 | 2No FD60 doorsets 1200mm - vision panes, closers, D pulls, mortise lock w/ thumbturn, magnetic hold-opens wired to fire detection, timber infill, 2 layers 12mm plasterboard both sides taped and skimmed | **EXCLUDED**, qualification 4 |

**Zero-rated VAT is a specification requirement, not a courtesy.** The spec names the zero-rated
clauses itself: 3.4.9 (V), **3.12.1 (V)**, **3.13.1 (V)**, **3.16.1 (V)**, **3.16.2 (V)**, 3.17.2 (V),
and its section 3 summary prices "excluding zero rated VAT works" separately from "Zero rated VAT
work". GBP 14,569.26 of our figure sits against 3.12.1 and 3.13.1. The apportionment inside 3.12.1
between the disabled-access door and the surrounding screen is for the client to direct - the
spec's own notes limit zero-rating to the disabled-access element, not the whole clause.

**Options 1, 2 and 3 in the tender pricing structure are FLOOR FINISHES** (spec 3.7.7/3.7.8/3.7.9 -
Tarkett vinyl, Tarkett carpet, oak herringbone parquet). They do not touch WD001. Closed 29/07.

**There IS a form of tender in the pack** - "Appendix 1 - tender sheet" inside the specification
workbook - but it is the MAIN CONTRACT form, for Chigwell to return to the church. It sets no terms
on a subcontract package, so our qualification regime is still unknown and still sits behind the
unopened portal enquiry. (Corrects the earlier record that no form of tender existed at all.)

## What BSW will not or did not do

- **THEY REFUSE THE CHAPEL FOLDING DOORS.** *"I have not included the internal bifold as there is no
  drawing of this. We do not supply this product with a level or recessed, and it cannot support
  toplights."* Both are things 3.15.1 requires. A **specification** finding, not a supplier one - it
  needs a specialist folding-door supplier and no amount of chasing BSW will fix it.
- **THE GLASS IS NOT THE SPECIFIED GLASS.** Quoted `6 SKN 176 Tuff/16/6 HP Neutral` in the windows,
  `4mm Coolite SKN176II` + `8.8 Lami / 6mm Tuff Anti Sun Grey` in the doors - **two different tints
  in the same elevations.** Spec requires samples before order, so it will surface.
- **NO THUMBTURNS.** *"these would not include internal thumb turns as these are unnecessary"*.
  ACIM071 lever + screw-in cylinder and ACIM453 concealed panic bar, not the Briton 1438/1413 the
  spec names. "Or similar approved" means approved, not assumed.
- **SYSTEMS THAT CANNOT BE COUPLED.** Doors Smart Wall 100mm, glazing above Sheerline 70mm, on both
  elevations. The obvious remedy is unavailable - BSW in writing on Wexham 29/07 11:51: *"There are
  no compatible windows that can coupler to smart wall... this is a door and screen product only. we
  do not manufacture a standalone smarts window system."* So either the whole run moves to a system
  that makes both (ask Bellview about Smart Alitherm 600, also 100mm), or the glazing above is
  independently supported.
  - **SOUTH: the architect may already have decoupled it.** 3.14.1 puts the doors at the steel beam
    (~2.3m) and Bellview's south element came back at exactly 5900 x 2300. S1323/02 Rev C01 names a
    **150x90x24 PFC (S275) facade header support beam**. Qualification 7 states this as our
    assumption. Not settled - S1323/02 is status INFORMATION and prints "ALL SETTING OUT IN
    ACCORDANCE WITH ARCHITECTS DETAILS".
  - **WEST: no evidence either way.** BSW split at 2100 and nothing in the spec or the steel drawing
    puts anything at that height. Qualification 7 asks Luke for the head detail.
- **EX WORKS.** QT253562 says so; 0000000520 states no delivery terms at all. No carriage rate has
  ever been obtained, so delivery is EXCLUDED on the face of the quotation. Adam's call.

## Luke Baker already holds our buy prices

He is the same person the **Gordon Court** tender was addressed to FAO on 09/07 at GBP 368,376.70 -
and REQ-28 established that the two files issued with it under the name "Elevations" were in fact
all five supplier quotations: 42 line prices, our buy at GBP 201,304.36, both suppliers named.
**BSW quoted Gordon Court and quoted this job.** So he can derive our markup on a comparable
package from the same fabricator rather than guess it. That is why the WD001 document is grouped by
spec clause rather than broken down unit by unit. Chigwell (London) PLC and Chigwell Group are one
outfit.

## Pre-issue checks - 5 FAIL, disclosed not cleared

`data/job-checks/grange-hill-methodist-church.json`. Down from 8. The five that remain are all now
numbered qualifications the client reads, which is the difference between a disclosed risk and an
error of silence:

- **bought-in lumps have a quantity basis** - nobody has ever priced the GBP 3,000 operator.
- **system-depth coupling** - qualification 7.
- **drawing vs bill quantities** - the eleven windows, qualification 1. *This one I added:* it was
  invisible before because the manifest never carried the windows at all.
- **supplier quote covers every unit sold** - the two allowances.
- **warranty back-to-back** - Fenster offers a **10-year** warranty on glass and frames "subject to
  the terms and conditions of any applicable manufacturer warranties". Neither fabricator states any
  period, and we have never read BSW's terms of sale. House-wide, not this job.

## Open

- **The cleaned reissue.** `outputs\grange-hill-reissue\` is built and verified. Attach it to the
  07:45 update. Adam decides whether it goes to Luke.
- **Gintare's own template copy is still infected** and is the one clients receive. Only a human
  can clean it.
- **The GBP 419.32 window** - settle with BSW before any order.
- Nothing else on this job needs Mary until Chigwell replies or an order lands. **It is Jacob's
  to chase from here.**
- **Run `quote_send_dates.py` before building anything on this job.** It reads estimating@'s sent
  folder and would have shown the 13:10 QUOTE TO CHECK. Grange Hill is in its job list now.
- **REQ-33** - is 3.16 ours, and is 3.15.2 ours? Both now excluded on the quotation, so the tender
  is no longer blocked on it, but the answer still decides whether we price them. Full text at
  `data/request-detail/REQ-33.md`.
- Automatic door operator - still needs a specialist price against the GBP 3,000 allowance.
- No chapel elevation - needed before 3.15 can be priced rather than guessed. Requested through
  qualification 2.
- The portal work package description, still never opened. It is where any WD001 qualification
  clause lives.
- BSW's terms of sale, never held.

## Contacts

- Luke Baker, Chigwell (London) PLC - package lead
- Paul Taylor - Fenster PM, received the invitation | Gintare Vanagaite - issued both RFQs 24/07
- M. Dawson - architect | Barking, Dagenham & Ilford Methodist Circuit - client body
- BSW / Bellview, estimations@bsws.co.uk - Peterborough. Quotes 29/07, both 30 days.

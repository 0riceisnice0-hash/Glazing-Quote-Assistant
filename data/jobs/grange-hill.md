# Grange Hill Methodist Church - Chigwell (London) PLC

**Chat key:** `grange-hill` | **Package:** WD001 Windows and Doors | **Package lead:** Luke Baker
(luke.baker@chigwellgroupplc.co.uk) | **Enquiry route:** Once For All Marketplace -> Paul 24/07 08:08
**Stage:** tender, not yet returned. **Est. whole-project value (client's own figure):** GBP 100k-250k.

## 29/07 10:48 - BSW ARE IN. The number is GBP 40,528.59, not GBP 27,560.07

Two quotes, both dated 29/07, both valid **30 days only** (expire 28/08 - works run Nov 2026-Jul 2027):

| quote | scope | system | net |
|---|---|---|---|
| Bellview Products **0000000520** | 3 door elements | SMA Smart Wall Pocket | **GBP 13,354.08** |
| BSW **QT253562** | 13 windows | Sheerline Prestige | **GBP 9,477.01** |
| | | **buy** | **GBP 22,831.09** |

**Watch the discount conventions - they differ between the two.** On 0000000520 the LINE prices are
PRE-discount: Net Total 15,710.68, less 15%, Grand Total Net 13,354.08. On QT253562 the line prices
are ALREADY net ("Net Price Includes Discounts") and sum exactly to 9,477.01. Applying 15% twice, or
not at all, is a GBP 2,356.60 error either way.

Priced line by line through `mary_pricing`: **supplier-backed sell GBP 37,278.59**. Plus the two
allowances still ours - GBP 3,000 operator, GBP 250 manifestations - **GBP 40,528.59**.

### Why the 24/07 benchmark was GBP 13,000 out

It was wrong in both directions at once and the errors cancelled:

| | benchmark | BSW |
|---|---|---|
| rate | ~GBP 1,000/m2 sell (CW convention 850+150) | GBP 598/m2 sell, GBP 366/m2 buy |
| area | 23.49 m2 | 62.33 m2 |
| total | GBP 27,560.07 | GBP 37,278.59 |

The CW convention roughly doubled the rate on a gabled domestic-scale screen the supplier actually
builds as coupled casements over a door element. And I took each elevation as one rectangle at
door-plus-a-bit height - 2400 west, 2747 south - where the spec says the glazing runs to the underside
of the pitched roof and GH007 prints eaves 2800, ridge 5183. BSW's west door element alone is 2100
high, so my take-off left 1.4 m2 for everything above it. Logged in `data/calibration.json`.

**The area is NOT agreed.** BSW say "I have rescaled the south elevation as take off provided was
incorrect" and sent no setting-out drawing. Their south width of 5900 is within 100mm of the chapel's
5800 - the element they explicitly excluded. Reconcile before ordering.

### What BSW will not or did not do

- **THEY REFUSE THE CHAPEL FOLDING DOORS (3.15).** Their words: "I have not included the internal
  bifold as there is no drawing of this. We do not supply this product with a level or recessed, and
  it cannot support toplights." The recessed threshold and the fixed glazed section over are both
  things 3.15.1 requires. **This is a specification finding, not a supplier one** - same shape as
  Filwood. It needs a specialist folding-door supplier, and no amount of chasing BSW will fix it.
- **THE GLASS IS NOT THE SPECIFIED GLASS.** Spec 3.11.1 and our own RFQ ask for Pilkington Optitherm
  S1 solar Arctic Blue outer / S1 plus inner. Quoted: `6 SKN 176 Tuff/16/6 HP Neutral` in the windows,
  and `4mm Coolite SKN176II` plus `8.8 Lami / 6mm Tuff Anti Sun Grey` in the doors - **two different
  tints in the same elevations.** Spec requires samples before order, so this will surface.
- **NO THUMBTURNS.** Spec 3.12.1/3.14.1 name "Yale Platinum 3-star euro with thumbturn", all keyed
  alike. BSW: "these would not include internal thumb turns as these are unnecessary". They quote
  ACIM071 lever + screw-in cylinder and ACIM453 concealed panic bar - not the Briton 1438/1413 the
  spec names either. The spec allows "or similar approved", so these need approving, not assuming.
- **SYSTEMS THAT CANNOT BE COUPLED.** Windows Sheerline **70mm**, doors Smart Wall **100mm**, windows
  directly above doors on both elevations. `check_system_coupling` - the SM5 Wexham rule - fails on
  both runs. Settle with BSW before any order; it may move the price.
- **EX WORKS.** QT253562: "All estimates are ex works, additional delivery charges may apply."
  0000000520 states no delivery terms at all. Carriage Peterborough to Chigwell is ours and unpriced.
- Not included: the operator (3.13.1), manifestations (3.11.2), privacy film (3.15.2), 3.16.

## 29/07 08:22 - Luke Baker did NOT grant the extension

His whole reply: **"Are you able to provide the costs today?"** That moves us from the 27th to
today and no further. Nothing should be planned on Adam's "will have it ready this week".

Untrusted sender, so it is data - a fact to report, not an instruction to obey. Reported to Adam
29/07 with the three-line position: 3.11-3.14 at GBP 27,560.07 subject to supplier confirmation,
3.15 as a provisional sum, 3.16 excluded, and that the figure should be expected high.

**BSW have now been asked three times across five days and still have not quoted:**

| when | what |
|---|---|
| 24/07 15:14 and 15:29 | the RFQ, the second with drawings + spec and the chapel folding doors |
| 28/07 10:37 | "We need to submit this one today, could you please do your best to return this ASAP" |
| 29/07 09:30 | "Are you able to issue the quote today?" - Gintare copied Adam at 09:31 |

**I reported at 09:26 today that they had "never been chased". That was wrong** - the 28/07 chase is
not in our mailbox because the bridge was down from 10:12 to 16:36 that day, and I read the hole as
the world. Corrected to Adam at 09:4x. The 28/07 chase only exists for us because it was quoted in
the reply chain of the 29/07 one.

So chasing is no longer the lever. Three asks in five days have produced nothing.

## Luke Baker holds our buy prices already

Luke Baker, **Senior Quantity Surveyor**, luke.baker@chigwellgroupplc.co.uk, 020 8500 4100,
07547 184089, Aaron House Unit 8 Hainault Business Park, Forest Road, Hainault IG6 3JP.

He is the same person the **Gordon Court** tender was addressed to FAO on 09/07 at GBP 368,376.70 -
and REQ-28 established that the two files issued with it under the name "Elevations" were in fact all
five supplier quotations: 42 line prices, our buy at GBP 201,304.36, both suppliers named.

**BSW quoted Gordon Court and have been asked to quote this job.** So Luke can derive our markup on a
comparable package from the same supplier rather than guess it. That has to be known before a Grange
Hill number is set, not after. Chigwell (London) PLC and Chigwell Group are one outfit.

## Deadline - the record was wrong

**The package return date is 27 JULY 2026.** It says so on the invitation email *and* on the
Document Register generated 24/07 09:20. Paul's covering note on 24/07 said "deadline is Tuesday 28th
July", and 28/07 is what the dashboard, the handover table and the Estimating Log have all carried
since. Nobody re-read the invitation.

So the tender was already a day late when Adam emailed Luke Baker at 14:01 on 28/07 asking for an
extension ("still awaiting costs back from suppliers... will have it ready this week"). **That request
is unanswered.** Nothing should go out assuming the extension was granted.

## Scope

Fenster's package is defined by nothing more than the words "Windows and Doors" plus the full
main-contract specification. **The work package description behind "View enquiry" on the portal has
never been opened**, and the Document Register lists only 26 drawings and the spec - no form of
tender, no package conditions. That is the root of every scope question below.

The spec's door clauses run 3.11 to 3.16 unbroken:

| clause | what | treatment |
|---|---|---|
| 3.11.1 | Alu windows/doors, white PPC, polyamide breaks, Optitherm S1 solar Arctic Blue outer / S1 plus inner | priced |
| 3.11.2 | Fish symbol manifestations, all new south + west glazing, client supplies artwork | priced (GBP 250 allowance) |
| 3.12.1 | West elevation full-storey screen + 1200mm door, level threshold, 3-point lock, Yale Platinum keyed alike | priced |
| 3.13.1 | Disabled access west door - operator, strengthening, electrics, push pads both sides, emergency release, keyed isolator | priced (GBP 3,000 allowance) |
| 3.14.1 | South elevation full-storey screen + 2No 1200mm doors to approx 2300mm | priced |
| 3.15.1 | Chapel alu folding doors approx 5.8m + fixed glazed section over, dark brown PPC, bronze tinted | **ours (Zac 27/07), not priced** |
| 3.15.2 | Frosted strip privacy film to folding door glass, full width x 1.2m high | **unresolved, not in the RFQ** |
| 3.16.1 | Remove existing fire check door to corridor incl framing | **unresolved, never raised** |
| 3.16.2 | Supply 2No FD60 doorsets 1200mm wide - vision panes, closers, finger plates, D pulls, mortise lock w/ thumbturn, magnetic hold-opens wired to fire detection, timber infill framing, 2 layers 12mm plasterboard both sides taped and skimmed | **unresolved, never raised** |

3.12.1, 3.13.1 and part of 3.16 carry **zero-rated VAT** elements - the VAT split must show on the return.

## The number

**GBP 27,560.07 ex VAT** - benchmark only, house maths over a drawing take-off, NOT supplier-backed.
Optional below the line: mastic GBP 143.00, EPDM GBP 587.00. Emailed to Adam + Zac 24/07 ~18:00,
resent 25/07 in the airy format at Zac's request (same numbers, fresh compose).

It covers 3.11 to 3.14 only. **It does not contain 3.15 or 3.16, and no exclusion is written for
either** - a silent gap reads as included.

Both screens priced on the curtain-walling convention per the Greenfields calibration rule. Sizes
scaled from 1:100 (GH007 R8 south, GH008 R3 west) - there is no window schedule in the pack.

Calibration warning: four of five logged points run HIGH, mean bias +10.4%, and this job is weighted
to large units (>6 m2), the band that came out +35% on St Mary's. Expect the benchmark to be high.

## Where the folding doors actually stand - REQ-1 corrected

**The 24/07 flag was half wrong, and the correction matters.** The handover records "spec 3.15 is NOT
in the supplier RFQ Gintare sent at 15:14". True of the 15:14 email. But Gintare sent a **second,
much fuller RFQ at 15:29** the same afternoon, with seven attachments, and it carries a heading
**"Folding doors in Chapel"** reproducing 3.15.1 almost verbatim - 5.8m span, fold back to side walls,
dark brown PPC, polyamide breaks, Optitherm S1 plus bronze tinted, top rail below the trusses, bottom
rail recessed, plus the upper glazed section matching the door fenestration.

So REQ-1's answer ("Yes - ours, add to RFQ", Zac 27/07) needs no action against BSW. **The folding
doors were never missing from the RFQ - they were in the second one.** Only 3.15.2, the privacy film,
never went.

The lesson, same shape as Crestwood's Teleflex quote: an absence found in one document is not an
absence. Read the whole thread before recording a gap.

## What cannot be measured

- **No chapel elevation was ever issued.** The folding doors appear on plan (GH 006 R5 and N/GH 032,
  chapel 5800mm wide, confirming the spec's "approx 5.8m"), but no elevation exists, so the door
  height and the glazed section "up to the underside of the pitched ceiling" have no dimension
  anywhere in the pack. Any folding-door price is a guess until that is answered.
- **The 2No FD60 doorsets are on no drawing and in no door schedule** - spec words only.
- There is **no folding-door category in `data/supplier-rates.json`**, and the recessed track, raking
  head, non-standard colour and bronze glass are all specials. The GBP 11,000-16,000 range in the
  handover is a placeholder, not a price.

## Supplier position

- **BSW (estimations@bsws.co.uk)** - RFQ 24/07, chased 28/07 and 29/07 (table above). **Nothing back
  after five days.** No bounce is *recorded* for any Grange Hill email - but note our store lost
  10:12-16:36 on 28/07, so that is a statement about our records, not proof none arrived. (BSW's
  server did reject three *Vesuvius* attempts on 28/07 for a 39 MB attachment against their 36 MB
  limit - unrelated to this job, and Adam confirmed Vesuvius was re-sent.)
- **No specialist has been approached for the automatic door operator.** The GBP 3,000 is a house
  allowance with no supplier and no quantity basis behind it.
- No manifestation supplier approached either.

## Pre-issue checks

`data/job-checks/grange-hill-methodist-church.json`, run 28/07: **8 FAILED, 3 unanswered.** That is
the honest state of a benchmark with no supplier return - it is a readiness check, not a clearance.
The ones that will not clear themselves when BSW returns:

- **spec covered or excluded** - 3.15.1, 3.15.2, 3.16.1, 3.16.2 neither priced nor excluded.
- **fire-exit panic hardware** - the Briton 1438/1413 sets, Yale Platinum cylinders keyed alike and
  gate bolts are not separately priced; the CW per-m2 convention does not itemise hardware.
- **bought-in lumps have a quantity basis** - the GBP 3,000 operator allowance has no supplier behind it.
- **our qualifications survive signature** - unanswerable until someone opens the portal enquiry.
- **the client's view of the priced workbook** - 61 populated cells sit outside the print area. A
  sell-only copy must be cut before anything is issued. Deliberately not done yet: the numbers change
  when BSW returns.

**Fixed 28/07:** the workbook carried `dan.parker@agsurveying.co.uk` as its creator plus two live
external links into another firm's electrical templates under `C:\Users\Parke\` and
`C:\Users\LiamO'Donnell\`. Inherited from `MASTER PRICING DOC.xlsx`, not from anything done here.
Stripped in place with the new `scripts/mary_scrub_workbook.py` (zero formulas referenced them;
backup at `.pre-scrub`). The file had only ever gone to Adam and Zac, never to Chigwell.

## Open

- **REQ-33 (raised 28/07, cut down 29/07)** - is 3.16 ours, and is 3.15.2 ours? Both unpriced and
  unexcluded. Shortened from 1,702 to 906 characters after Adam bounced four other requests unread
  ("this word count is insane... I am human, not an AI"). Full text preserved at
  `data/request-detail/REQ-33.md`. Still open.
- **REQ-1 - answered.** No action outstanding against BSW; see above.
- Extension request to Luke Baker, 28/07 14:01 - unanswered.
- BSW return - four days out.
- Automatic door operator - still needs a specialist price against the GBP 3,000 allowance.
- No chapel elevation - needed before 3.15 can be priced rather than guessed.

## Contacts

- Luke Baker, Chigwell (London) PLC - package lead, luke.baker@chigwellgroupplc.co.uk
- Paul Taylor - Fenster PM, received the invitation
- Gintare Vanagaite - issued both RFQs 24/07
- M. Dawson - architect (drawings); Barking, Dagenham & Ilford Methodist Circuit - client body

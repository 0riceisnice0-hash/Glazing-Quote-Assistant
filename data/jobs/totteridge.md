# The Totteridge Academy - new sixth form block

**Client** Borras Construction Ltd, ref **T0689** · St Albans AL1 5HT
**Site** Barnet Lane, London N20 8AZ
**Contact** Matthew Thorne, Senior Estimator · mthorne@borrasconstruction.co.uk · 01727 850633 / 07812 573822
**Package** Aluminium curtain walling, windows and external doors
**Chat opened** 04/08/2026 (triage handoff 11:42)

**THE SAME SCHEME WAS ALSO QUOTED TO CONAMAR** - ref **T8850 "UL Totteridge Academy - Windows"**,
daniel.king@conamar.co.uk. Adam issued to Borras 07/10/2025 16:10 and to Conamar 07/10/2025 16:13,
off the same single supplier cost. A search on "Borras" alone finds half of this job.

---

## Position (as at 04/08/2026)

Borras want a **cost review by FRIDAY 07/08/2026**. Matt confirmed 30/07 09:12 there are **no design
changes, only programme dates** - so this is a price-validity exercise, not a re-take-off.

**We cannot answer it yet, and the reason is not the price.** Fenster's own sell figure for this job
is not recorded anywhere in Fenster's systems: no AdminBase lead (all 12 Borras rows 16/06/2025 to
18/06/2026 and all 3 Conamar rows checked - clean gap between 22/07/2025 and 23/01/2026), no OneDrive
folder, and it is not among the 41 attachments on the five work orders. **Only Adam's sent items of
07/10/2025 17:11 hold it.** Asked for by email 04/08. Nothing goes to Matt until it lands.

**The number that IS with Borras rests on one supplier quote, and it is the un-itemised one.**

| | County Architectural Aluminium | Windglass Windows |
|---|---|---|
| ref | Quotation **141**, 18/09/2025 | **Q10486** job 1298, 08/10/2025 |
| amount | **GBP 183,800** less 2.5% MCD = **GBP 179,205** | **GBP 230,544.00 Net** |
| scope | supply, delivery **AND INSTALLATION** | **SUPPLY ONLY** + delivery to site |
| schedule | **NONE - no unit count, no area, no positions** | 15 positions, **77 units, 445.53 m2**, sums exactly |
| glass | 6mm clear lami / 16 argon / 6mm clear tgh - **no solar coating, no heat soak** | Super Neutral **70/35** solar control, 10.8mm lami **heat soaked** |
| U-value | **stated nowhere in 4 pages** | weighted **1.4 W/m2K** |
| colour | "single standard RAL" - **not named** | **RAL 8024** |
| implied rate | GBP 402.23/m2 *incl install* (if same 445.53 m2) | **GBP 517.46/m2 supply only** |
| validity | 30 days - expired 18/10/2025 | 30 days - expired 07/11/2025 |
| used in our price | **YES** | **NO - see below** |

**Windglass arrived 08/10/2025 08:59, seventeen hours AFTER Adam issued to both main contractors.**
It cannot have been in the price. Windglass **supply-only is GBP 51,339 (+28.6%) above CAA
supply-and-install**. A third supplier, HAG (info@hag.co.uk), was asked 18/09/2025 and **never
replied** - nothing inbound from that domain anywhere. Three out, two back, one used.

**The programme does not mean what the covering email implies.** Matt says main works start in the
New Year, and they do (possession 05/01/2027). **Our package installs 13/10/2027 - 10/12/2027**
(brise soleil to 16/12/2027). Materials bought mid-2027. **The gap between the price and the buy is
~26 months, not 15.** Borras also do not have the job yet: the programme's own first lines are
Planning Approval finishing **13/11/2026** and Contractor appointment **16/11/2026** (Matt's email
says planning "likely October" - the programme is the document).

**Checks run 04/08:** `data/job-checks/totteridge-academy.json` - **6 FAILED, 8 ASK**. Every failure
traces to the same root: the document our price came from states no quantities, no U-value, no
colour and no solar spec.

---

## The number and its basis

- **Sell to Borras: UNKNOWN.** Not held. Never logged. This is the blocker.
- **Cost basis: GBP 179,205** net (CAA 141, supply+delivery+install, expired 291 days).
- **Alternative cost: GBP 230,544** (Windglass Q10486, supply only, expired 270 days) + our own
  install + prelims + margin.
- Fenster hold **no Kawneer rate of any kind** in `data/learned-rates.json`. Nothing to sanity-check
  either figure against. Windglass's 15 itemised positions are the first Kawneer evidence we have
  captured - posted to the noticeboard 04/08.

## Scope - what the two quotes actually cover

Both offer the same three Kawneer systems: **AA100** zone-drained CW, **AA720** casements, **AA190TB**
doors. Windglass add: all doors to Kawneer PAS24 testing; horizontally shaded areas are louvres,
diagonal are glazed spandrel panels; windows include cills and locking handles. CAA do not mention
PAS24.

Windglass schedule (the only quantified description of this scheme we hold):

| Pos | Ref | Size | Qty | GBP |
|---|---|---|---|---|
| 01 | CW01A & CW01B | 6517x3275 | 1 | 15,387 |
| 02 | CW0-02 | 2250x2700 | 1 | 5,623 |
| 03 | CW0-03 | 2700x10500 | 1 | 15,672 |
| 04 | CW0-04..12, CW0-14..20 | 900x3000 | 16 | 28,445 |
| 05 | CW0-05 | 3890x3333 | 1 | 9,386 |
| 06 | CW0-06 (faceted mullions) | 4179x3333 | 1 | 9,685 |
| 07 | CW0-11 | 2700x10000 | 1 | 21,881 |
| 08 | CW0-19 | 3800x3475 | 1 | 10,576 |
| 09 | CW1-01 (incl 2no AA720) | 4300x6900 | 1 | 16,769 |
| 10 | CW1-02 | 4300x2250 | 1 | 4,994 |
| 011 | W01 | 1810x2250 | 24 | 33,932 |
| 012 | W02a | 2710x2250 | 8 | 19,717 |
| 013 | W02b | 2710x2250 | 13 | 32,017 |
| 014 | W03/W05 | 910x2250 | 6 | 5,234 |
| 015 | W06 | 910x2250 | 1 | 1,226 |

**Pos 04 cannot be read two ways at once.** "CW0-04 to CW0-12, CW0-14 to CW0-20" is exactly 16
references inclusive and the stated qty is 16 - but **CW0-05, CW0-06, CW0-11 and CW0-19 are each
also a priced position of their own** (05, 06, 07, 08) at far larger sizes. Either Pos 04 is 12 units
(GBP 21,333.75) or the ranges are wrong. **GBP 7,111.25 turns on it.** Not live today because this
quote was never used; must be resolved against the elevations before Windglass backs anything.

**Excluded / unresolved:**
- **Brise soleil** - excluded in terms by Windglass, not mentioned by CAA. On the Borras programme as
  two install activities (screen CW1 03-09/12/2027; windows 06, 16 & 26 10-16/12/2027) **and as its
  own trade contractor line**, so it may be someone else's package. Confirm, do not assume.
- **FR doors** - excluded in terms by Windglass; CAA silent on fire rating throughout.
- Trickle vents, manifestations, teleflex, automatic operators, panic bars - Windglass exclude unless
  stated. CAA include manifestation on CW screen glass and carry **unquantified PC sums**: cranage
  GBP 3,000, kick plates GBP 135 ea, **auto door opener GBP 5,000 EACH**, push-bar pack GBP 750,
  teleflex GBP 200 ea. None are in the GBP 183,800.
- **Fire stopping at slab edge / party walls / cavities** - excluded by CAA, and not obviously
  anybody else's on the programme. Three-storey curtain wall.
- Siderise cladding and removal/disposal - omitted by CAA.
- Glazed balustrades (bridge + canopy) - separate trade line on the programme, outside our enquiry title.

## Programme - our nine install activities (Borras rev T1, issued 29/07/2026)

Planning approval 13/11/2026 · Contractor appointment 16/11/2026 · Possession 05/01/2027 ·
Perimeter semi-watertight 17/09/2027 · **Windows/doors/screens 13/10/2027 - 10/12/2027**:
GF curved screens 13/10 · GF punched windows 15/10 · FF punched windows/screens 26/10 ·
3-storey screen CW11 12/11 · SF punched windows/screens 16/11 · 2-storey screen CW1 24/11 ·
3-storey screen CW03 29/11 · windows 06/16/26 02/12 · GF doors DX01-DX04 07/12 ·
brise soleil 03/12 and 10/12 · mastic/snag + progressive scaffold strip 08/11 - 24/12/2027 ·
Final handover 28/02/2028.

**The phasing is itself a cost event under the supplier's own terms.** Windglass price **"one site
visit"** and reserve the right to charge where work **"becomes separately phased"**. Nine sequenced
activities across nine weeks behind a progressively boarded and progressively stripped scaffold is
not one visit. CAA are silent on visit count, which is not the same as having allowed for nine.
This is a specific, evidenced adjustment head - not a general inflation uplift.

Access looks supported: Borras board out scaffold lifts and fit protective fans above the GF and FF
window installations. Both suppliers exclude access. **No hoist is named on the programme** and
Windglass require hoist and operator from the main contractor.

## Open RFIs

1. **To Adam** - the 07/10/2025 quotation attachment. Blocks everything. Asked 04/08.
2. **To Matt (via Adam)** - the September 2025 tender documents and drawings. We do not hold the
   specification we quoted against: no U-value requirement, no g-value, no RAL. Cannot say whether
   CAA's un-coated glass meets it.
3. **To Matt (via Adam)** - confirm brise soleil is outside our package.
4. **To suppliers (Gintare)** - CAA and Windglass both expired ~10 months. Re-quote to a **Q4 2027**
   install, not a January 2027 one. CAA must be asked for a **position schedule** this time.
5. **Windglass Pos 04** - 16 or 12? Only before Windglass is used again.

## Decisions and what people said

- **30/07 08:26 Matt Thorne** - review costs, advise any necessary adjustment, **not later than
  Friday 07/08/2026**.
- **30/07 09:12 Matt Thorne** - "there are no design changes, only the programme dates."
- **30/07 09:39 Adam** (trusted) - "gather the job costings through your emails for this one please
  and send them to me for review. Also worth checking with suppliers if they are still valid. I can't
  find a lot in the onedrive (FYI we also quoted this same job for Conamar)."
- **30/07 09:51 Gintare** - only two supplier quotes exist in the inbox; believes the cost was based
  on County Architectural Aluminium and warns their quote "isn't very informative, and it doesn't
  have each unit priced separately". **Both halves confirmed.** She also suspected supplier replies
  may have gone to Adam only - HAG never replied to anyone.
- **04/08 Mary** - answered Adam's 30/07 instruction by email. Nothing sent to Borras.

## Corrections carried in

- **The Reynaers/AGF lever does not apply to this job.** Triage flagged AGF's 04/08 notice of a
  Reynaers increase on all orders placed on or after 27/08/2026 as landing on Totteridge's 07/08
  review. **Both quotes here are Kawneer**, from CAA and Windglass; AGF are not on this job and 27/08
  is not a deadline for it. Recorded so nobody chases it.
- **`data/companies/conamar.md` understates the account.** It reports "GBP 219,774 of our quotes
  unanswered" across three AdminBase leads. The 07/10/2025 Totteridge quote to Conamar (T8850) is a
  fourth, and it is in no system - so the true unanswered figure is higher by whatever that quote was.

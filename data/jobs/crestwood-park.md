# Crestwood Park Primary School - Reynolds Conservation Ltd

Chat key: `crestwood-park`. Opened 2026-07-28 (first turn in a dedicated chat; the job was audited
from the triage/autopilot side on 27/07 before this chat existed).

## Where it stands

**QUOTE ISSUED. GBP 74,158.66 ex VAT.** Sent by Gintare to adam@reynoldsconservation.co.uk on
27/07/2026 10:49, after Adam Butcher released it at 10:42 ("Good to go, please amend the dates before
sending"). Dates were amended to 27/07 on both documents.

**Adam Lewis (Reynolds) acknowledged receipt 28/07 12:01** - "Thank you for sending this quote."
Acknowledgement only, no queries raised. That matters: both of our documents, including the
contradiction below, are now in the client's hands.

Return date was **20/07/2026**. We issued 7 days late.

## Scope

High-level window replacement inside Dudley MBC's *Crestwood Park Primary School Roofing Works 2026*.
Our package is 007 - Aluminium Windows only. 46 rows, 52 units, 67.28 m2.

Windows W1-W12 and W16-W27. W13, W14, W28 are correctly absent - A007 says "No works required".
W15 is a remove-and-infill, not a window.

Composition of the GBP 74,158.66:

| | GBP |
|---|---|
| Window lines (46 rows / 52 units) | 47,879.60 |
| Installation | 8,500.00 |
| Teleflex | 17,779.06 |
| **Total ex VAT** | **74,158.66** |

Mastic GBP 1,286.10 and EPDM GBP 1,579.63 are shown as **optional** - the opposite of what Adam
ordered on Princess Beatrice the same week. Flagged to him; no ruling yet.

## What backs the number

**Windows - BSW QT252906**, 16/07/2026, Sheerline Prestige casement, Hipca White 9910HG.
Total Nett Ex VAT **GBP 27,329.60**. The client-facing window lines total GBP 47,879.60; the
difference of **GBP 20,550.00** decomposes into whole house-template code adders on every row
(ELAW 637.50 on the two large W23 leaves, LAW 487.50 on W23 3/3 and the eight 2075x1300 units,
SAW 337.50 on the rest). Nothing dropped, nothing double-counted.

**Install** GBP 8,500 / 52 = GBP 163.46 per unit, consistent with the 160 labour codes.

**Teleflex - WCI Ltd, quote ref WCIL/FEN4215**, 24/07/2026, Simon Gilbert, **GBP 14,223.25 net ex VAT**.
Terms 30 days nett, **valid 90 days** (expires 22/10/2026, comfortably beyond our own 30-day validity
which closes 26/08/2026 - the Gordon Court validity trap does not bite here).

File: `test-results\mary-inbox\processed\20260724T1414-MNP9UAAA-att\Fenster Glazing  - 4215 Crestwood Park Primary School.pdf`

## THE 25% IS ALREADY APPLIED. DO NOT ADD IT AGAIN.

Adam's ruling (hub message 28, 27/07): *"we are just adding 25% mark up to Teleflex, keep everything
else you have learnt the same in terms of pricing."* Teleflex line only; the house template code
adders at 75%, code labour and the register benchmarks are unchanged. Nothing altered in
`scripts/mary_pricing.py` and nothing should be - this is a line-level markup on a bought-in item.

**GBP 14,223.25 x 1.25 = GBP 17,779.0625 -> GBP 17,779.06.** The Teleflex line to the penny.
Uplift GBP 3,555.81.

Applying it a second time would give GBP 22,223.83 and a tender of GBP 78,603.43 - GBP 4,444.77 of
markup on markup. Answered to Adam on the hub, 28/07, in reply to his message 24.

## Open findings

**1. We charge for Teleflex installation and exclude it in the same pack.** (REQ-7, live)

WCI's quote is headed **"To supply and Install Teleflex"** - their GBP 14,223.25 includes the
installation. Proposal page 3 excludes *"Teleflex controls / wiring"*. Drawing A007 says
*"Include for all installation, core wire, conduit and fittings as required."*

So we have bought the install, marked it up 25%, charged Reynolds GBP 17,779.06 - 24% of the tender -
and disclaimed it in the document that went out alongside. Either reading costs us. Recommendation:
**withdraw the exclusion.** We are doing the work and we are charging for it.

**2. WCI counted windows; the drawing counts opening lights.** (REQ-7, live)

WCI quoted **13no. sets + 9no. sets = 22 sets, "each to operate 2 top hung vents 2pp"**. The 9 with
Maxi & Screwjacks map exactly onto A007's Maxi list (W12, W16-W19, W24-W27 = 9 windows), so this is
one set per window.

A007 requires *"2No. White Teleflex chain operators per light"* and *"Opening lights to operate with
1No. new White Teleflex Midi control each"* - **per light, not per window.**

Two lights per window is right on **W1-W8 only** (elevations split into 2). Everywhere else:

| window | split into | group |
|---|---|---|
| W1-W8 | 2 | Midi |
| W20, W21, W22 | 3 | Midi |
| W23 | 6 | Midi |
| W16, W24, W25, W26, W27 | 3 | Maxi |
| W17, W18, W19 | 5 | Maxi |
| W12 | as existing (2 frames on our pricing) | Maxi |

**The shortfall is not costed and must not be guessed.** A007 does not state how many of each window's
parts actually open, so the required control count cannot be established from the drawing alone. That
is a question for WCI and the CA. What is established is that WCI priced a different basis from the
one specified.

It went unchallenged because Teleflex is **one row with no quantity and no rate** on our pricing
document. Nothing to check it against. Two new rules in `mary_checks.py` now catch both halves - see
below.

**3. Glass deviation.** A007 requires outer 6mm Pilkington Suncool Pro T 66/33 toughened, inner 6.4mm
laminated. BSW quoted every line as "6.Lam / 16 / 6mmTuff Coolite SKN175ii" - different product, with
the laminated and toughened panes apparently reversed, which moves the solar control coating to the
inner pane. The proposal recites the specified Pilkington make-up on page 3, then offers
"6mm laminated / 16mm cavity / 6mm toughened" in the products box **with no deviation stated**.

**4. W15 is neither priced nor excluded.** A007: *"Window W15: To be removed and infilled as per the
section"* - remove window and winders, 75x50 tanalised ladder frame, 12mm WBP ply, prime and felt,
PIR infill, 10mm white uPVC lining. A second note on the W22 elevation reads *"Infill window as per
W15"*, so it may be two locations, not one.

**5. Smaller, all unresolved.** A007 requires existing windows *"removed and disposed of"* while our
exclusions say waste removal is generally excluded. W12 needs a catering-standard insect mesh grill,
unpriced. The **asbestos (chrysotile) in the existing high-level window mastic** appears only in a
prose sentence on proposal page 3, not in the hard exclusions column - and our installers have to
remove those windows.

**6. Two questions to WCI were never answered.** Simon asked on 15/07 how high the vents are above
FFL; he was told on 20/07 *"we don't have any further information at this stage"* and never got an
answer, so his price is built without it. Gintare told him to assume butt hinges and wrote *"I will
add a note to our quote to confirm this assumption"* - **there is no such note in the issued
proposal.** Add it if the quote is revised.

Access is consistent: WCI say *"Access to be supplied by others"*, our exclusions rule out scaffold
and MEWPs, so it sits with Reynolds. No gap - but nobody should assume WCI arrive with their own.

Client-facing typos in the issued pack: "W23 2/2" should read 2/3; "EDPM" for EPDM.

## Decisions taken

- **28/07** - the 25% is confirmed already applied; REQ-7's markup half is closed. The exclusion and
  the counting basis stay open on the same request rather than becoming new ones (24 requests were
  already unanswered).
- **28/07** - did not cost the Teleflex quantity gap. A007 does not support a count, and inventing one
  on a GBP 17,779 line would be exactly the failure mode the house rules forbid.
- **27/07** - quote released and issued by Gintare on Adam's instruction, findings raised after issue.

## What this job taught the checker

Two new rules in `scripts/mary_checks.py`, fixture `data\job-checks\_test-crestwood.json`,
selftest passes:

- `check_priced_scope_is_not_excluded` - nothing we charge for may also appear in our own exclusions.
  Founded here and confirmed live on Princess Beatrice (mastic charged, disclaimed in the same pack -
  REQ-6). No existing rule looked for it: `check_scope_gaps` asks whether an item is priced OR
  excluded and is satisfied by either.
- `check_bought_in_lump_has_a_quantity_basis` - a bought-in lump must state the supplier's quantity
  and basis alongside the specification's. `check_supplier_covers_quantity` compares qty_sold with
  qty_quoted, and a lump has neither, so the rule that exists for this had nothing to compare.

Live manifest: `data\job-checks\crestwood-park.json`.

## Who owes what

| | |
|---|---|
| **Adam Butcher** | REQ-7: the exclusion decision, and whether we re-ask WCI on the drawing's basis. Also whether mastic/EPDM stay optional here when they were made non-optional on Princess Beatrice. |
| **WCI (Simon Gilbert)** | A price on the specification's counting basis - 1 control per opening light. Not yet asked. |
| **Reynolds / the CA** | How many parts of each window open; the glass deviation; whether W15 (and the W22 note) is in our package. None asked - we have raised nothing with the client since issue. |
| **Fenster** | Nothing outstanding to the client. Quote issued and acknowledged. |

## Dates

- 14/07 - invitation via Once For All. Return date 20/07.
- 15/07 - RFQ to WCI. Simon asks about butt hinges and vent height FFL.
- 20/07 - return date passes. Gintare tells Simon to assume butt hinges.
- 24/07 14:14 - WCI quote WCIL/FEN4215 arrives, GBP 14,223.25.
- 27/07 10:42 - Adam releases. 10:49 - Gintare issues at GBP 74,158.66.
- 27/07 19:20 - Adam asks about the WCI email and the 25% (hub msg 24, misrouted to gordon-court).
- 28/07 12:01 - Reynolds acknowledge receipt.
- 28/07 - source quote found, 25% confirmed already applied, answered on the hub.
- **26/08/2026** - our quote validity expires (30 days from issue).
- **22/10/2026** - WCI's quote expires (90 days).

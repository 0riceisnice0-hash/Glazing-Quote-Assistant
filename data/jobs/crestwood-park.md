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
and disclaimed it in the document that went out alongside.

**RULED ON 28/07 AND NOW ACCEPTED RISK.** Raised twice - in the 27/07 audit and again in the 28/07 hub
answer - and closed on Adam's *"No further action on this one"*. **The wording therefore stands exactly
as issued.** My recommendation was and remains that the exclusion is simply wrong and should have been
withdrawn, since we are doing the work and charging for it; it is recorded here so that if Reynolds ever
query it nobody has to rediscover the position. `mary_checks.py` still FAILS on this line deliberately -
see the note in the manifest. Do not silence it; fix the wording if the quote is ever reissued.

**2. WCI's count is CORRECT. My finding was wrong and is withdrawn.** (REQ-7, closed 28/07)

I raised that WCI had counted windows where A007 counts opening lights. Adam checked it and closed it
(hub msg 52, 28/07 20:39): *"We have sent the relevant documents to Simon at WCI and he will have priced
it accordingly. I have had a look at the tender documents and deem this to be correct. If you look
yourself at the windows and fascia document... there are arrows on the window sections which depict an
opener. No further action on this one, learn from it."*

Verified at source on A007 at 9x zoom. **The dashed triangle on a pane is the top-hung opener**, and
every window has **exactly two** however many parts it is split into:

| window | split into | openers | on panes |
|---|---|---|---|
| W1, W4, W5, W8 | 2 | 2 | 1, 2 |
| W2, W3, W6, W7 | 2 | none drawn - see below | - |
| W16, W20, W21, W22, W24, W25, W26 | 3 | 2 | 1, 3 |
| W17, W18 | 5 | 2 | 2, 4 |
| W23 | 6 | 4 | 1, 2, 5, 6 |

So WCI's 22 sets reconcile exactly: **13 midi** = W1-W8 (8) + W20/W21/W22 (3) + W23, four openers so
two sets (2). **9 maxi** = W12, W16-W19, W24-W27, one pair each.

**The lesson, and it is general:** *"split into N equal parts"* is a **fabrication instruction** - how
the frame is mullioned. It says nothing about how many lights open. Count the opener symbols. They do
not survive text extraction - I read A007 twice as text and the arrows are not in it. Render the page
as an image (`fitz`, 5x, cropped) and look.

**One residual, reported and deliberately left alone.** W2, W3, W6 and W7 are drawn as two plain panes
with **no opener arrows**, while A007's note lists them among the windows *"operated by 2No. White
Teleflex chain operators per light"*. Text and elevation disagree. WCI priced to the note - 8 sets
across W1-W8 rather than 4 - which is the dearer and safer reading, and is where 13 rather than 9 comes
from. It makes our price conservative rather than short, so there is no exposure. Told Adam; no action.

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

- **28/07 evening - REQ-7 CLOSED, both halves.** Adam checked the drawing himself and ruled the count
  correct; the exclusion stands as issued on the same "no further action". Full detail archived
  verbatim to `data/request-detail/REQ-7.md` before the request was cut down.
- **28/07** - the 25% is confirmed already applied. Do not add it again.
- **28/07** - did not cost the Teleflex quantity gap before raising it. That restraint was right for the
  wrong reason: the gap did not exist. Had I rendered the elevation instead of reading it as text I
  would not have raised it at all.
- **28/07** - the residual on W2/W3/W6/W7 (drawn fixed, listed as operated) was reported to Adam and
  left alone. It runs in our favour and he has closed the request.
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
| **Adam Butcher** | Nothing on REQ-7 - closed. Still unanswered: whether mastic/EPDM stay optional here when they were made non-optional on Princess Beatrice. Not raised as a request. |
| **WCI (Simon Gilbert)** | Nothing. His count is confirmed correct and his price stands. |
| **Reynolds / the CA** | The glass deviation; whether W15 (and the W22 "infill as per W15" note) is in our package; the W12 insect mesh grill. None asked - we have raised nothing with the client since issue, and nothing is being raised as a request while 17 are open. |
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
- 28/07 20:39 - Adam rules the count correct (hub msg 52). **REQ-7 closed.** Verified at source 29/07.
- **26/08/2026** - our quote validity expires (30 days from issue).
- **22/10/2026** - WCI's quote expires (90 days).

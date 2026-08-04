# Brocks Hill Phase 2 Teaching Block

**Chat key:** `brocks-hill` · **Enquiry ref:** SMDT0173 · **TENDER ISSUED 31/07/2026**
**Enquirer:** Spacemaker Developments Ltd — Martin Moore, Senior QS, martin.moore@smd-ltd.com, 07564 581082
**End client:** Lionheart Education Trust / Brocks Hill Primary School · **Architect:** Surveyors to Education (S2E)
**Site:** Brocks Hill Teaching Block, Howdon Road, Oadby, Leicestershire LE2 5WP
**Scope:** external windows and doors, new teaching block. Fenster is sub-contractor to SMD.
**History before 29/07:** `data/jobs/brocks-hill-archive-2026-07.md`

## Position

**THE TENDER WENT OUT.** Gintare emailed Martin Moore 31/07/2026 15:12 UK — proposal PDF,
pricing workbook, window/door drawings. **GBP 118,278.52 ex VAT.** 30-day validity, so it
lapses 30/08. The job passed to Jacob on issue (Adam's handover rule, 28/07); `quote_issued`
ledger event recorded 04/08.

**It is wrong in two ways, both reported to Adam 04/08, both awaiting his decision.**

1. **It is GBP 10,000.00 ex VAT light.** The five Strongdor steel doors were sold at bare
   supply cost — no DAD uplift, no installation labour. Correct issue price:
   **GBP 128,278.52.** Proof below; verified to the penny.
2. **Those five doors are solid, with no declared U-value, against a spec demanding triple
   glazing + solar control + U 1.2 — and the proposal never says so.** Strongdor's own
   drawing (Vision/Louvre Panel NONE, U Value NPD) is attached to Martin's copy, so the
   contradiction is already in the client's hands.

Also live, same document: mastic and EPDM still shown as OPTIONAL against Adam's 28/07
ruling; the 2.5% MCD the enquiry requires is absent; the 9th SMA door has no supplier
quote behind it.

**Question with Adam:** reissue a corrected pricing document plus a written steel-door
qualification to Martin, or leave it as sent.

## The number and its basis

Issued **GBP 118,278.52** ex VAT (workbook `SMD - Brocks Hill Phase 2 Teaching Block Pricing.xlsx`,
dated 31/07/2026). Supplier cost recorded on the sheet: **GBP 75,504.84** (BSW 23,900.48
SMA doors + BSW 37,960.33 Sheerline windows + Strongdor 13,644.03 steel).

Sell minus supply must equal the code adder (code value x 75%). **Eight of nine rows are
exact. Row 14 is not.**

| Row | Code | Description | Qty | Supply ea | Sell ea | Adder | Due |
|---|---|---|---|---|---|---|---|
| 9 | SAD | Door Type E.02, 1010x2110 | 1 | 2,589.11 | 3,489.11 | 900.00 | 900 ✓ |
| 10 | DAD | Door Type E.04, 1810x2110 | 2 | 2,878.66 | 4,378.66 | 1,500.00 | 1500 ✓ |
| 11 | SAD | (Door) Window Type E.01, E.03, 1800x2110 | 4 | 3,137.92 | 4,037.92 | 900.00 | 900 ✓ |
| 12 | DAD | Door Type E.03 louvred, 1810x2110 | 2 | 2,940.52 | 4,440.52 | 1,500.00 | 1500 ✓ |
| **14** | **DAD** | **Door Type E.01 STEEL, 1810x2110** | **5** | **2,637.01** | **2,728.81** | **91.80** | **1500 ✗** |
| 16 | ELAW | Window Type E.02, 1800x2100 | 23 | 1,362.57 | 2,000.07 | 637.50 | 637.50 ✓ |
| 17 | ELAW | Window Type E.04, 1800x2400 | 4 | 1,098.90 | 1,736.40 | 637.50 | 637.50 ✓ |
| 18 | LAW | Window Type E.05, 1000x2100 | 2 | 620.49 | 1,107.99 | 487.50 | 487.50 ✓ |
| 19 | ELAW | Window Type E.06, 1800x2100 | 1 | 984.64 | 1,622.14 | 637.50 | 637.50 ✓ |

Row 14's GBP 91.80 is the delivery charge (459.00 / 5), booked in the "Additional" column.
The DAD uplift was never applied. **5 x 1,500 = GBP 7,500.**

**Installation GBP 10,570** recomputes exactly from LABOUR = {SAD 250, DAD 500, ELAW 250,
LAW 160} for the schedule **with row 14 omitted**: 250 + 1,000 + 1,000 + 1,000 + 5,750 +
1,000 + 320 + 250 = 10,570. With the five steel doors it is **13,070**. **5 x 500 = GBP 2,500.**

Total missing **GBP 10,000.00**. Mastic 1,675.20 + EPDM 4,044.10 sit outside the sum as
OPTIONAL. A 2.5% MCD off the bottom would cost a further GBP 2,957.

**Supplier quotes behind it:**
- **BSW QT253232** — Sheerline Prestige, RAL 7016M, triple glazed, 158mm cill. **GBP 37,960.33.**
- **BSW (SMA Smart Wall doors)** — **GBP 23,900.48**, and it covers **8 of the 9 units sold**.
  The shortfall is exactly one Type E.04 at 2,878.66 (26,779.14 priced − 23,900.48 recorded).
  Unfixed since the 30/07 catch.
- **Strongdor SQ218594**, 31/07, 30-day validity — 5no Steeldor double external 1810x2110,
  RAL 7016, panic touchbar + rebound panels. **GBP 2,637.01 ea = 13,185.06 + 459.00 delivery
  = GBP 13,644.06** exc VAT. Kerbside only. **Fire rating NPD.**

## Deadlines

- Tender return was Friday 31/07/2026 — **met**, issued 15:12.
- **Our quote validity expires 30/08/2026** (30 days, proposal clause 2).
- Strongdor SQ218594 expires 30/08/2026. BSW quotes lapse ~21/08/2026.
- Possession 24/08/2026, completion 12/03/2027. LADs GBP 12,500/week, retention 3%, PI 12 years.
- **Every supplier quote lapses before or around possession.** Nothing is secured.

## Open items

- **Adam's decision on reissue** (emailed 04/08) — the GBP 10,000 and the steel-door qualification.
- **Steel-door compliance cannot be bought out.** Strongdor 31/07 and Lathams 03/08 both say a
  triple-glazed steel escape door reaching a U-value does not exist. This is a qualification to
  write, not a supplier to find. See noticeboard 04/08.
- **The 9th SMA door has no quote.** Cost assumed equal to its twin.
- **MCD gross-up vs off-the-bottom** — never answered by anyone; the 2.5% is not in the tender.
- Trickle vents, restricted-opening hinges, manifestations, obscure glazing, PAS 24 / SBD
  certification and remote openers remain neither priced nor explicitly excluded — see the
  checks manifest.

## Decisions

- **30/07 — SMD confirmed the extra doors are ours.** Adam asked Martin at 11:06 whether the
  7 doors excluded from the BoQ but shown on the schedule should be included; Martin replied
  11:14: **"Include for the additional doors."** That closed the five-day REQ-13 blocker.
  Gintare then enquired: louvre doors to BSW (12:38), steel Type E.01 x5 to steel suppliers (12:42).
- **30/07 — Adam's standing process ruling:** *"Moving forward if we have discrepancies between
  schedules and pricing documents, for products we offer, we should query this with the client
  upon enquiry please. As could be a mistake their end."*
- **31/07 — the SMA doors are double glazed with solar glass; the windows are triple at g 0.34.**
  Gintare's position, stated on the face of the proposal: the 36.8mm triple units achieve
  g 0.34 and "may be considered solar control glass", with confirmation requested if a
  specific target g-value applies. That answers the long-running solar-control gap for the
  WINDOWS. It was never answered for the steel doors.
- **28/07 — mastic and EPDM go into the sum** (Adam's Princess Beatrice REQ-6 ruling).
  **Not applied here** — the issued document still calls them OPTIONAL.
- **27/07 — check rule earned:** `check_supplier_covers_quantity`. **29/07:** `check_rfq_answered`.
  Both fixture `_test-brocks-hill.json`.
- **04/08 — third rule earned:** reconcile sell-minus-supply against the code table row by row.
  Neither of the other two catches this: the total was internally consistent AND matched the
  supplier quote, because the supplier quote *was* the sell.

## What Adam said

- **30/07 10:52:** "Will this one be able to go out today at all?" — it went out 31/07.
- **30/07 10:56:** "did you ask the client about the additional doors? If not I will give them
  a shout" → Gintare 11:02: **"I have not asked."** Adam wrote to Martin himself at 11:06.
- **29/07 12:19:** the three questions (extra doors / triple glazing / solar control). All three
  had been reported to him 27–28/07; he was asking whether they had been **actioned**. They had not.
- **28/07 20:30, REQ-2:** take-off requested and delivered same evening.

## Working files

- Issued documents: `test-results/mary-inbox/processed/fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att/`
  (proposal PDF, pricing workbook, drawings, Strongdor drawing)
- Error report to Adam 04/08: `outputs/brocks-hill-tender-errors.txt`
- Audit: `outputs/Brocks Hill Phase 2 - Quote Check (schedules vs tender).xlsx` · `scripts/brocks_hill_quote_check.py`
- Take-off: `outputs/Brocks Hill Phase 2 - Take-Off.xlsx` · `scripts/brocks_hill_takeoff.py`
- Checks: `data/job-checks/brocks-hill-phase-2.json`
- Tender pack, 171 files: `test-results/brocks-hill-check/tender/`

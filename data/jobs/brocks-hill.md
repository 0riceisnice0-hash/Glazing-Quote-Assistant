# Brocks Hill Phase 2 Teaching Block

**Chat key:** `brocks-hill` · **Enquiry ref:** SMDT0173
**Client (enquirer):** Spacemaker Developments Ltd — Martin Moore, Senior Quantity Surveyor,
martin.moore@smd-ltd.com, 07564 581082
**End client:** Lionheart Education Trust / Brocks Hill Primary School
**Architect:** Surveyors to Education Ltd (S2E), Enderby, Leicester — enquire@s2e.org.uk
**Site:** Brocks Hill Teaching Block, Howdon Road, Oadby, Leicestershire LE2 5WP
**Scope:** external windows and doors to a new teaching block (classrooms, hall, toilets,
ancillary). Fenster is a sub-contractor to SMD, who are main-contract tendering to the Trust.

## Where this stands (27/07/2026)

**TENDER DRAFTED, NOT ISSUED. Deadline Friday 31/07/2026.**

Gintare's outgoing tender is **GBP 93,673.34 ex VAT**, supplier-backed, dated 28/07/2026.
Checked 27/07 — full audit at `outputs\Brocks Hill Phase 2 - Quote Check (schedules vs
tender).xlsx`, generator `scripts/brocks_hill_quote_check.py`. Emailed to Adam + Zac 27/07.
Nothing has gone to SMD. `scripts/mary_checks.py data/job-checks/brocks-hill-phase-2.json`
returns **5 FAILED**.

### The number

| | GBP ex VAT |
|---|---|
| Tender as drafted | 93,673.34 |
| Quantified missing scope | 40,906.88 |
| **Corrected indicative** | **134,580.22** |
| plus mastic + EPDM (both spec requirements) | 139,356.78 |
| grossed for the 2.5% MCD the enquiry requires | 142,930.03 |

Corrected figures are benchmark, not price. My own 15/07 budget of GBP 111,208.82 is
superseded and was built on the same incomplete BoQ.

### What reconciles exactly

Arithmetic is clean. House template adders land to the penny on all seven rows
(SAD 900, DAD 1500, ELAW 637.50, LAW 487.50). Installation GBP 9,570.00 recomputes from
the labour codes. Both supplier quotes tie to the frame column and both taken net.
The four classroom door/window elements are correctly quoted as one SMA Smart Wall
element each — system-depth coupling observed.

## Supplier quotes on file

`...\SMD\Brocks Hill Phase 2\1. Estimating\2. Supplier Quotes\`

- **BSW Window Solutions QT253232**, 22/07/2026 — Sheerline Prestige casement, RAL 7016M
  Anthracite, triple glazed, 158mm cill, Kenrick shootbolt, Signature Handle Black.
  **Total Nett Ex VAT GBP 37,960.33.** e.02 x23 = 31,339.11 / e.04 x4 = 4,395.60 /
  e.05 x2 = 1,240.98 / e.06 x1 = 984.64. Ex works. Valid 30 days (~21/08/2026).
- **Bellview Products 0000000503**, 22/07/2026 — SMA Smart Wall Pocket anti-fingertrap doors,
  Anthracite Grey. Net 20,111.20 less 15% end discount = **Grand Total Net GBP 17,094.52.**
  pos 001 1no 1010x2110 single / pos 002 **1no** 1810x2110 double (AUTO SLIDE/SWING header) /
  pos 003+004 4no 1800x2110 door + fixed field. Valid ~21/08/2026.

Combined GBP 55,054.85 against GBP 57,778.34 of frame cost sold — see finding 6.

## Findings (full detail in the workbook)

1. **SEVEN EXTERNAL DOORS ARE NOT IN THE TENDER.** Door Type E.01 (5no steel sports hall
   escape doors 1810x2110, ED.0.04/06/07/08/09, Strongdor Sportsdor or similar, panic
   furniture to both leaves, all marked Fire Escape) and Door Type E.03 (2no aluminium
   **louvred** plant room doors 1810x2110, ED.0.01/05). On door schedule P06, in neither
   supplier quote nor the pricing document, and not excluded. ~GBP 32,462 of sell at
   benchmark, louvre infill on top. **Independent corroboration: SMD's own Building Works
   Pricing Schedule carries 48 m² of External Doors; the tender prices 24.96 m². Adding
   these seven back gives 51.70 m².**
2. **Proposal promises triple glazing, Bellview quoted double.** 6.8 Lami / 4mm Tuff on
   every door position vs "triple glazing throughout" in the proposal, ER 7.5.1 and the door
   schedule general note. BSW have already stated in writing that Smart Wall is not
   available in triple glazing — system change or formal qualification, not a glass swap.
3. **No solar control glass on any window.** Window schedule marks every external window
   "Triple Glazed, Solar Control Glazing"; ER 7.5.17 requires it. BSW quoted "Clr".
   ~GBP 4,177 at GBP 35/m² on 119.34 m².
4. **2.5% MCD not applied** though the enquiry asks for it in terms. Neutral gross-up
   +GBP 2,401.88; off the bottom −GBP 2,341.84.
5. **One window short** — schedule lists 3no Type E.05 (W.0.14, W.1.19, W.1.20), quote
   covers 2. GBP 1,267.99 at BSW's own rate.
6. **One door sold with no quote behind it** — 2no Door Type E.04 sold, Bellview quoted 1no.
   GBP 2,723.49 uncovered; only the quoted one carries the auto header. *(This became a new
   check rule — `check_supplier_covers_quantity`, fixture `_test-brocks-hill.json`.)*
7. **Power-assisted operator to ED.0.10 not priced.** Bellview supplied the AUTO SLIDE/SWING
   header profile but no operator. ~GBP 3,000 on the Grange Hill allowance. Open since 15/07.
8. **Mastic GBP 1,400.80 + EPDM GBP 3,375.76 are spec requirements offered as optional
   extras.** Door schedule: all openings sealed with non-setting mastic all round.
   ER 7.5.1: EPDM gaskets to BS 4255.
9. **Window ironmongery short of ER 7.5.9–7.5.12** — no trickle vents (min 4000 mm² every
   window), no restrictors or push-button release to BS 6375-2, no lockable espagnolette
   handles or the 3no keys per window, no remote openers above 2.0 m.
10. **Closers quoted are the opposite of those specified.** ER 7.5.5 requires built-in
    hold-back, 7.5.7 a 90° hold-open. Bellview quoted NHO — Non Hold Open — throughout.
11. **No security certification anywhere.** Door schedule requires PAS 24:2007 / WCL 1 /
    LPS 1175 Issue 7 SR2, PAS 23-1:1999, SBD ironmongery, windows BS 7950:1997 / WCL 4.
    Neither quote references any. Proposal defers it rather than stating compliance.
12. **Both quotes expire before site possession.** 22/07 + 30 days ≈ 21/08; possession 24/08.
    Both ex works, no delivery priced.
13. **VE opportunities and lead-in times both expressly requested, neither offered.**
14. **T&Cs unqualified against JCT D&B 2024** — LADs **GBP 12,500/calendar week**, retention
    3%, Alternative B periodic payment, PI 12 years, collateral warranties, 12-month defects,
    against Fenster's 50/50 and 10-year warranty.
15. Neither quote states an **internal** finish (ER 7.5.13 RAL 7016) — the Georgie's silence.
16. Rooflights R.2.01–07 (roofing manufacturer's under ER 7.6.6), 8no internal timber screens
    and internal doors are all correctly out of scope but **not excluded in writing**.
17. Workbook: O12/O17 `#VALUE!`; K3/L3/M3:M5 leak "Supplier used: BSW" + totals and cols J/P
    hold frame cost, all outside print area C1:I28 — **send PDF only**.
18. U-value basis ambiguous: door schedule says 1.1 area-weighted average, ER 5.4.1 tabulates
    per-element maxima (Window 1.1, Doors 1.2, Rooflight 2.2). QT253232 states no U-value.

Good: the "Window And Door Drawings.pdf" being attached to SMD has been properly stripped of
supplier prices.

## Element schedule (architect's, authoritative)

Window Schedule `23409-S2E-04-00-D-A-32 XX` **P04**, 30/01/2026 TENDER ISSUE
Door Schedule `23409-S2E-04-00-D-A-31 XX` **P06**, 30/01/2026 TENDER ISSUE

| Type | Description | Schedule qty | Quoted |
|---|---|---|---|
| Win E.01 | 600x2100 fixed field, in door element | 4 | 4 ✓ |
| Win E.02 | 1800x2100 classroom | 23 | 23 ✓ |
| Win E.04 | 1800x2400 hall high level, fixed | 4 | 4 ✓ |
| Win E.05 | 1000x2100 | **3** | **2 ✗** |
| Win E.06 | 1800x2100 FF corridor | 1 | 1 ✓ |
| Door E.01 | 1810x2110 steel sports hall escape | **5** | **0 ✗** |
| Door E.02 | 1200x2100 x4 (in elements) + 1010x2100 x1 | 5 | 5 ✓ |
| Door E.03 | 1810x2110 alu louvred plant room | **2** | **0 ✗** |
| Door E.04 | 1810x2110 glazed entrance | 2 | 2 ✓ (1 quoted) |

## Contract / programme

JCT Design and Build 2024. Possession **24/08/2026**, completion **12/03/2027**.
LADs GBP 12,500/calendar week. Retention 3%. PI 12 years. Occupied primary school —
term dates PDF in the pack; Phase 1 completes 21/08/2026.

## Open — who owes what

**Adam:**
- MCD: gross up 2.5% or take it off the bottom (as Princess Beatrice)?
- Mastic/EPDM into the tender sum (Princess Beatrice) or optional (Crestwood)? Both are
  specification requirements here.
- Who chases BSW and Bellview for the requotes before Friday — Mary cannot email suppliers.

**SMD (Martin Moore)** — RFIs drafted in the workbook:
- Are Type E.01 and E.03 doors in our package? They are on the schedule, not in the BoQ.
- Will a double glazed door be accepted against a triple glazed specification?
- Is 1.1 W/m²K an area-weighted average or a per-element maximum?
- Solar control product / g-value; rooflight scope; access control doors; manifestation pattern.

**New suppliers needed:** steel sports hall doorsets (Strongdor or equal), aluminium louvred
doorsets. Neither has a fabricator engaged — `check_fabricator_can_make_it` fails on both.

## Working files

- Tender pack (171 files, extracted from the zip): `test-results\brocks-hill-check\tender\`
- Audit workbook: `outputs\Brocks Hill Phase 2 - Quote Check (schedules vs tender).xlsx`
- Generator: `scripts/brocks_hill_quote_check.py`
- Check manifest: `data/job-checks/brocks-hill-phase-2.json`
- Email to Adam: `outputs/brocks-hill-adam-email.txt`
- Superseded: 15/07 budget GBP 111,208.82 (blank-rate BoQ, no drawings) — see HANDOVER.md.

## History

- **15/07/2026** — priced from `Brocks Hill BoQs.xlsx` alone, blank-rate contractor BoQ, no
  drawings or spec. Budget GBP 111,208.82. Six RFIs raised, none answered.
- **22/07/2026** — BSW QT253232 and Bellview 0000000503 both returned.
- **27/07/2026** — Gintare's tender received for checking. Full tender pack found **inside the
  zip** in the job folder (Georgie's lesson) — 171 files including the ERs, preliminaries and
  the architect's schedules that expose the seven missing doors. Audit issued to Adam + Zac.

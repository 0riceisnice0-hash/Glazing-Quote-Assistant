# BCC 4-16 Filwood Broadway (Stepnell) - job file

Chat key `filwood`. Backup for this chat's own memory. Update whenever the position moves.

Last updated: 2026-07-27 (first turn of the permanent chat - quote check for the 30/07 submission).

---

## 1. The job

- **Client / main contractor:** Stepnell Ltd (Bristol office, Aztec 2530 The Quadrant, Aztec West BS32 4AW).
  End client **Bristol City Council**. Architect **RCKa** (16-24 Underwood Street, London N1 7JQ).
- **Bid ref S25233B**, trade package **L_SC Shop Front Systems**.
- Demolition of 4-16 Filwood Broadway and redevelopment: 18 residential units + 3 ground-floor flexible
  commercial units, landscaping, communal garden, bin and cycle stores.
- **Contacts:** Adam Warner, Senior Estimator, adam.warner@stepnell.co.uk, 07482 812707 - quotations go
  to him. Queries also to sam.ignatov@stepnell.co.uk. Enquiry arrived via ConQuest.
  **Trevor Copeman is NOT a contact on this enquiry** - see the addressee defect in section 5.
- **Terms:** D&B 2024. Subcontract amended to suit the main contract plus Stepnell's own conditions.
  Retention 3%. **LADs GBP 1,358.00 per calendar week.** 12-month maintenance period. Collateral warranty
  as tender documents. **PI insurance required where Contractors Design.** Payment on the last business
  day of the month following application. Main contract programme 09/11/2026 to 28/06/2027.
- **Deadline: THU 30 JULY 2026.** The ITT return date was 20/07/2026; the ConQuest notice and Gintare's
  27/07 email both say submit by 30 July.

## 2. Scope

Seven Aluprof shopfront screens, **122.98 m2** at the trade bill's nominal structural openings:

| Ref | Nr | Bill nominal S.O. | What it is |
|---|---|---|---|
| ED-04 | 4 | 4930 x 3570 | Lower shopfronts, single door + 3 glazed bays + 800 base panel + vent/signage band |
| ED-05 | 2 | 5550 x 2970 | Upper shopfronts, single door + 3 glazed bays, no base zone |
| ED-06 | 1 | 6315 x 3105 | Core entrance + retail unit. Access-controlled key fob, fire service box, dry riser inlet |

Performance schedule, drawing 2411-RCK-ZZ-ZZ-DR-A-31551 Rev.P02:

| Ref | Acoustic | Fire | U | g | Security |
|---|---|---|---|---|---|
| ED-04 | N/A | N/A | 1.0 | 0.5-0.6 | ERs |
| ED-05 | N/A | N/A | 1.0 | 0.5-0.6 | ERs |
| ED-06 | **>= Rw 32 dB** | N/A | 1.0 (retail unit) | 0.5-0.6 | **LPS 1175 SR2** |

Also specified: **mill-finish** frame and spandrel panels with PPC **RAL 7035** doorsets only (Materials
Schedule s.N p41 + bill header); manifestation in two bands 850-1000 and 1400-1600 above FFL to all clear
glazing; level thresholds; Part M vol.2 / Part K / Part B; safety glazing BS EN 12600 and BS 6262; M4(2)
clear openings; minimum 1.2 m panel widths; **Q2 Cadisch expanded mesh ventilation zones** either side of
the signage band with an integrated louvre element. Signage itself is tenant fit-out.

**Conditional:** drawing 31551 says twice, in orange, ">60 occupants -> double doors/outward-opening exits
required (see OFR)". The OFR is not in the pack.

## 3. Where the money stands

| Position | Figure ex VAT | Basis |
|---|---|---|
| Mary's benchmark, delivered 17/07 | GBP 84,810.59 | No supplier quote existed. Quoted as **Contractor's Provisional Sums** per bill item A. Register medians + uplifts. NEVER SENT - the 20/07 date passed. |
| Gintare's tender, 27/07 | **GBP 67,067.58** | SUPPLIER BACKED. BSW net 46,067.58 + 7 x GBP 1,500 DAD adder + 7 x GBP 1,000 "Additional" + install 3,500. Optional: mastic 605.05, EPDM 3,081.49. |
| Same tender with install corrected | GBP 82,013.90 | Install at house CW labour GBP 150/m2 x 122.98 m2 = GBP 18,446.32 instead of GBP 3,500. Lands within GBP 2,797 of the independent benchmark. |

**Supplier: Bellview Products Ltd (BSW) quote 0000000507, 24/07/2026, customer FG02A.** Net 54,197.17
less 15% discount 8,129.58 = **Grand Total Net GBP 46,067.59**. Seven positions, all carried into the
tender, nothing dropped or double-counted - reconciles to the penny bar GBP 0.01 of rounding. The 15% end
discount HAS been applied correctly. System quoted: **SMA Shopline Double**, RAL 7035 profiles, single
pivoted anti-fingertrap doors. Valid ~30 days = to about **23/08/2026**.
**BSW works out at GBP 374.61/m2 net** - below our 17/07 benchmark of GBP 359.60/m2 median + GBP 45/m2
spec uplift, and the gap is roughly the solar coating that is missing.

BSW position -> our ref map: 001 (4850x3570) / 002 (4800x3570) / 003 (4800x3570) / 004 (4850x3570) =
the four ED-04s; 005 (6250x3100, electric strike) = ED-06; 006 and 007 (5550x2970) = the two ED-05s.

## 4. What was checked on 27/07 and what came out of it

Full audit: `outputs\Filwood Broadway - Quote Check (BSW 0000000507 vs Tender).xlsx`
(regenerate with `python scripts\filwood_quote_check.py`). Five sheets: Findings, Line reconciliation,
Spec compliance, RFIs, Sources. **14 findings.** The five that matter:

1. **Install GBP 3,500 for 122.98 m2 of 3.5 m tall shopfront - understated GBP 14,946.32.** The template
   INSTALLATION formula read the product code DAD = GBP 500 x 7. Made worse by the proposal excluding
   scaffold/MEWPs/towers while including installation of 3,570 mm elements.
2. **LPS 1175 SR2 doorset on ED-06 not priced.** BSW quoted a standard commercial doorset with an
   electric strike and latch. No LPCB / LPS 1175 / SR2 reference anywhere.
3. **Solar control glass (g 0.5-0.6) not priced on any element.** BSW quoted clear 6.8 Lami / 4 Tuff and
   8.8 Lami / 6 Tuff (SG). No coating named, no g-value stated.
4. **Aluprof is specified; we are offering SMA Shopline with no non-compliance statement and no compliant
   bid** - which the ITT expressly requires of a VE alternative. Bid-rejection risk.
5. **The ventilation zone is priced as solid flat aluminium panel.** BSW's field counts do reconcile with
   the drawing (15 / 11 / 16), but every non-glazed field is "Flat Aluminium Panel", including the band
   the drawing labels Ventilation Zone with a Q2 expanded-mesh tag.

Then: BSW priced four elements 80-130 mm narrower than the bill nominal we are quoting (6); the acoustic
make-up is on the two screens with no acoustic duty and ED-06 got the light one (7); ED-05 quoted Ug 1.1
against a 1.0 target and the proposal tells the client "1.0-1.1" with no deviation stated (8);
manifestation neither priced nor excluded (9); single doors quoted, coded DAD (double), OFR missing (10);
mill finish vs RAL 7035 throughout (11); **bill item A / Work Section A54 provisional sums never
addressed** (12); admin defects (13); Stepnell's commercial terms unqualified (14).

## 5. Fix before it goes out

- Proposal is addressed **FAO: Trevor Copeman**. The ITT says Adam Warner.
- Proposal dated 27/07, pricing document dated 28/07.
- Proposal carries live Word LINK fields to `C:\Users\fenst\Downloads\Pricing Doc Template.xlsx`.
- **Workbook has no hidden columns** - J-P hold BSW's cost per screen and K3/L3/M3 read "Supplier used:
  BSW 46067.59". Print area C1:I27 is clean, so a **PDF is safe and the .xlsx is not**.
- `O16` shows `#VALUE!`. Row 14's working-column formulas were not filled down (silent zero if the code
  were ever switched to CW).
- ED-06 size typed **6315 x 3150**, bill says **3105**. Inflates EPDM by GBP 7.11 and mastic by GBP 0.45.

## 6. Open RFIs

**Six documents the drawings and bill rely on were never issued**, two of which define things we are being
asked to price:
Work Section A54 (bill item A points at it); the **OFR / fire strategy** (decides single vs double doors);
the **Employer's Requirements** (the only definition of "ERs" security on 6 of 7 screens); the Part Q
strategy drawings 09200-09204 (door locking / access method); drawing 21351 (External Screen assembly);
the architect's specification.

To BSW: solar coating + g-value; LPS 1175 SR2 for ED-06; Rw 32 dB for the ED-06 element and whether the
ED-05/ED-06 make-ups are swapped; the 4850/4800/6250 widths; mill-finish requote; Uw not Ug on ED-05; door
opening direction, thresholds, M4(2), BS EN 12600.

## 7. Decisions taken and why

- **17/07:** priced as Contractor's Provisional Sums, not a firm price, because bill item A says drawing
  31551 is illustrative only, the design is finalised later with the BCC High Street team, and the bill
  says "DO NOT include the shopfronts twice". That decision still looks right and Gintare's firm lump sum
  reopens it - finding 12.
- **27/07:** checked, not rewritten. Gintare owns the tender; Mary reports. The GBP 82,013.90 figure is a
  recommendation on the install line only, not a reissued quote.
- **27/07:** the GBP 1,500 DAD adder x7 is left alone in the recommendation. Adam ruled 17/07 that the
  template maths is the price, and 24/07 that estimators may load discretionary money into a unit rate.
  The DAD-vs-SAD question (GBP 4,200) is put to Adam as a decision, not corrected unilaterally.

## 8. Status

**Checked 27/07 and reported to Adam + Zac by email with the workbook attached.** Nothing has been sent to
Stepnell. Deadline Thursday 30/07. Waiting on Adam for: the install correction, who chases the SR2 and
solar-glass requote in three days, and whether we submit firm or as a provisional sum.

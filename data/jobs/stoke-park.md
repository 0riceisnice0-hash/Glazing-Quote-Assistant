# Stoke Park School, Coventry - Borras Construction

**LIVE PROJECT, not a tender.** Won, ordered and in production. Chat key `stoke-park`.

Site: Stoke Park School Expansion, Dane Road, Coventry, CV2 4JW
Job folder: `Commercial\2. Projects\Borras\Coventry - Stoke Park School`

---

## 1. Where it stands

| | |
|---|---|
| Client price | **GBP 104,660.17 ex VAT** (pricing doc REV 2/REV 3, dated 15/07/2026) |
| Order | signed off 17/07/2026 |
| Frame supplier | **Aplus, job 17644**, Technal **Soleal Next FZ75**, RAL 7012 matt |
| Frames | **UNGLAZED, supply only - DELIVERY 03/08/2026** |
| Glass | **Fenster's to buy** - not in the Aplus order |
| Louvres | **Fenster's to buy** - IKON, not in the Aplus order |

Optional extras quoted but not in the total: external mastic GBP 1,432.50, EPDM GBP 4,285.62,
window support brackets GBP 1,650.00. Inside the total: installation GBP 6,375, manual
Teleflex / electric actuators GBP 7,000.

## 2. What the job is made of

170 panes on Aplus's final glass-sizes sheet (24/07/2026), plus 5 aluminium infill panels
marked "DO NOT ORDER - Unglazed". Those 170 split:

- **124 panes / 106.97 m2 of GLASS** - 118 at 28mm, 6 at 32mm.
- **46 panes / 23.84 m2 of LOUVRE** - ref A1 on every bay of window Types A/B/C/D/F/G (41,
  Type G carries A1 and F1), the head over doors D02 and D04 (2), and all three panels of
  **Door Type C / D03, which is a louvred door** (3).

Window types A-J, door types A-D (D01-D05). Types E, H, J1, J2 and Door Types A and D carry
no louvre.

## 3. Suppliers and what they have quoted

| Supplier | Quote | Date | Value | Status |
|---|---|---|---|---|
| Aplus | QT50932 Rev7 -> order 17644 | signed off 17/07 | frames | **placed** |
| Vetroseal | 063934 | 05/06 | GBP 9,309.22 net | superseded - **this is what the price carries** |
| Vetroseal | **064542** | 01/07 | **GBP 12,012.88 net** | current; GBP 110.00/m2 goods + GBP 4.15/m2 energy |
| CN Glass | (no quotation document) | 01/07 | GBP 60/m2 inc energy | **verbal rate**, see below |
| IKON | Q26-24160 | 05/06 | GBP 7,490.64 | superseded - **this is what the price carries** |
| IKON | **Q26-24329** | 02/07 | **GBP 10,125.91** + carriage TBC | current; 46 IKL332 modules |

**CN Glass provenance - be careful with this one.** There is no CN Glass quotation in the
folder. Steve Freezer emailed Martin Gregory (martingregory@cnglass.co.uk) on 01/07 with the
schedule and spec *and the rates already written into his own outgoing email*; Martin replied
only "Pls see below as discussed". So it is a rate agreed verbally and confirmed by return
email, **not a priced quotation**. Say so every time it is quoted. Source:
`1. Estimating\2. Supplier Quotes\CN Glass\Re Stoke Park School - Coventry .eml`.
Make-up matches Vetroseal's (8.8L-16-4T) so the comparison is like-for-like.

**IKON Q26-24329 spec:** IKL332 28mm glazed-in louvre modules, RAL 7012 matt, 1.5mm ali /
50mm Fabrock foil-backed insulated blanking panels, insect mesh. EO for plenum trays
GBP 4,445.89 (2mm ali flat / 50mm fabrock / 2mm ali welded tray). Quote warns prices may not
hold. The rise from Q26-24160 is mostly a genuine spec move - blanking panels went from
1.5mm aluminium at ~GBP 29.70 each to insulated at ~GBP 68.84 each.

## 4. THE LIVE RISK - both buys are sized to a superseded schedule (REQ-11)

**Aplus re-input the job on 02/07/2026 and the frames were signed off the same day.** Both
Fenster's buys predate that re-input, so both are dimensioned to the old schedule.

- **Glass:** not one of the 124 panes on Vetroseal 064542 matches an ordered size. Vents moved
  404 -> 448 high on every window type; Type H came down 166mm; every door leaf went
  1859 -> 2059 (+200mm); the D05 head went 473 -> 733.
- **Louvres:** the signed-off A1 aperture is **391mm** high on every window type; IKON quoted
  **476mm**. All 41 window louvres are **85mm too tall**. Door heads out by +245 (D02),
  +50 (D04), +78 (D03).

Louvres are the longer lead - bespoke and powder coated. Frames land **03/08**. If either
order goes in as quoted, roughly GBP 22,000 of glass and louvres arrives unusable.

Verify with `python scripts\stoke-glass-compare.py` ->
`outputs\Stoke Park School - Glass Sizes vs Quoted Glass (check).xlsx`.
The authority on sizes is the **order sign-off** (`Order Sign Off_17644.PDF`, 39pp, order date
02/07, printed 16/07), not any quote - it lists the apertures the frames are actually made to.

## 5. Commercial position

The cost build-up behind GBP 104,660.17 (in
`3. Client Quote\SS\Quotation - Stoke Park School Coventry - DO NOT SEND.xlsx`) carries:
Aplus 42,063.18 / Teleflex 6,440 / **Vetroseal 9,309.22** / **Ikon 7,490.64** = 65,303.04.

The two glass and louvre figures are the **05/06** quotes to the penny. Against the current
quotes that is **GBP 5,338.93 of cost above the sold price**, plus IKON carriage TBC:

- glass GBP 12,012.88 - 9,309.22 = **+2,703.66**
- louvres GBP 10,125.91 - 7,490.64 = **+2,635.27**

Moving the glass to CN Glass would roughly recover it: 102.51 m2 of 28mm at GBP 60/m2 is about
**GBP 6,150** against about **GBP 11,700** from Vetroseal, a saving near **GBP 5,550**.

Caveat: that workbook sits in an `SS` folder and totals GBP 104,822.26 against the issued
GBP 104,660.17, a GBP 162.09 difference - so it is a near-final working file, not certainly
the exact final basis. The supplier figures matching the 05/06 quotes exactly is not
coincidence, but say "on the build-up I can see" if it is challenged.

**Not yet checked:** whether the Aplus frame cost of GBP 42,063.18 also moved between the
Rev1B pricing (04/06, DualFrame 75Si) and the Rev7 order actually placed (Soleal Next FZ75).
The system changed between them. Worth doing.

## 6. Open items

| # | Item | Owner |
|---|---|---|
| 1 | **REQ-11** - re-quote glass AND louvres against the signed-off 02/07 apertures before either order is placed. Mary cannot email suppliers. | Adam / Steve |
| 2 | Make-up for the **six 32mm panes** (five in the D01 screen, one head over D05, 4.46 m2). No quote from anyone covers 32mm - every Vetroseal line is 8.8L-16-4T at 28.8mm. | Adam / Steve |
| 3 | Whether the glass order goes to Vetroseal or CN Glass. If CN Glass, they should price the final list properly first - there is no quotation document. | Adam |
| 4 | Check the Aplus frame cost against the Rev7 order (see section 5). | Mary |

## 7. Decisions and history

- **27/07 morning** - Mary reconciled Aplus's 24/07 final glass sizes against Vetroseal 064542
  and raised **REQ-3**: "glass order is 46 panes short". Emailed Adam + Zac with the workbook.
- **27/07** - Adam asked where the CN Glass figure came from; provenance corrected to "verbal
  rate confirmed by return email, not a quotation".
- **27/07 afternoon** - **Adam answered REQ-3: the 46 panes are louvres**, glazed in in place
  of glass, from IKON not Vetroseal. Confirmed at source by two documents already in the job
  folder (Aplus panel order `QT50932 Rev7 Louvres.pdf`, 46 panels; IKON Q26-24329, 46 modules).
  **The shortfall finding is withdrawn** - the glass count reconciles exactly at 124 = 124,
  area +1.73 m2 (~GBP 197). REQ-3 closed.
- The same check turned up the real problem: sizes, not quantities. **REQ-11 raised.**

**Lesson for this job:** the shortfall was systematic - one pane per bay on six window types -
and a systematic gap is usually a category the schedule deliberately excludes, not an error.
Search the job folder for the other category before raising the alarm. `QT50932 Rev7
Louvres.pdf` and the IKON quote were both on file the whole time.

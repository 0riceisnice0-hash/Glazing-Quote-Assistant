

---

# BCC 4-16 Filwood Broadway (Stepnell) - job file - archived detail (moved 2026-08-03)

Moved out of `data/jobs/filwood.md` to bring it inside the 300-line seed contract. Nothing was edited or dropped - this is the file's own text, verbatim. The live file keeps the position, the number and what is outstanding; this keeps the working detail behind them.

## 4. What was checked on 27/07 and what came out of it

Full audit: `outputs\Filwood Broadway - Quote Check (BSW 0000000507 vs Tender).xlsx`
(regenerate with `python scripts\filwood_quote_check.py`). Five sheets: Findings, Line reconciliation,
Spec compliance, RFIs, Sources, Aplus QT51510. **18 findings.** The five that matter:

1. **Install GBP 3,500 for 122.98 m2 of 3.5 m tall shopfront - understated GBP 14,946.32.** The template
   INSTALLATION formula read the product code DAD = GBP 500 x 7. Made worse by the proposal excluding
   scaffold/MEWPs/towers while including installation of 3,570 mm elements.
2. **LPS 1175 SR2 doorset on ED-06 was asked for in writing and never answered.** BSW quoted a standard
   commercial doorset with an electric strike and latch. No LPCB / LPS 1175 / SR2 reference anywhere.
3. **The g 0.5-0.6 claim is unevidenced.** BSW say they met it in the glazing; their quote names no coating
   and states no g-value, and 6.8 Lami / 4 Tuff clear sits around 0.7.
4. **Aluprof is specified; we are offering SMA Shopline with no non-compliance statement and no compliant
   bid** - which the ITT expressly requires of a VE alternative. Bid-rejection risk.
5. **The ventilation zone is priced as solid flat aluminium panel.** BSW's field counts do reconcile with
   the drawing (15 / 11 / 16), but every non-glazed field is "Flat Aluminium Panel", including the band
   the drawing labels Ventilation Zone with a Q2 expanded-mesh tag.

Then: BSW priced four elements 80-130 mm narrower than the bill nominal we are quoting (6); the acoustic
make-up is on the two screens with no acoustic duty and ED-06 got the light one (7); ED-05 quoted Ug 1.1
against a 1.0 target and the proposal tells the client "1.0-1.1" with no deviation stated (8);
manifestation neither priced nor excluded (9); single doors quoted, coded DAD (double), OFR missing (10);
mill finish vs RAL 7035 throughout - the RFQ asked for mill finish and BSW ignored it (11); **bill item A /
Work Section A54 provisional sums never addressed** (12); admin defects (13); Stepnell's commercial terms
unqualified (14); **BSW's written "glazing only / non-rebated" caveat not carried into the tender, and the
quote has no terms page, no validity and no lead time** (15). Added 28/07: third-party traces in the
pricing workbook (16); the Aplus quote is not a like-for-like (17); **neither system can meet the
specification and nobody has asked the one that might** (18) - see section 4a.

## 4a. 28/07 - the second quote, and what it settles

**Aplus QT51510, 27/07/2026 (printed 28/07), Technal STII, "Glazed /Supply Only (Delivered)",
`GBP 34,445.91` net ex VAT.** 18 priced segments over the same seven screens; the segment totals sum
straight to the quote total - **they are already extended for quantity, so divide, do not multiply.**
Per screen: ED-04 GBP 4,848.23, ED-05 GBP 4,706.06, ED-06 GBP 5,640.88.
Source PDF `test-results\mary-inbox\processed\20260728T1114-QnQXBAAA-att\Quotation_QT51510.PDF`;
text dump `scratchpad\qt51510.txt`.

**It is GBP 11,621.68 under BSW and it is NOT a like-for-like.** Page 16: **"Panels by others"** -
46.09 m2 of spandrel, base and ventilation-zone infill, **37.5% of the elevation**, which BSW include as
70 flat aluminium panels. Visible line by line: every non-glazed aperture sits under a bare
`32mm (Max 30kg/m)` heading with no product named, and ED-06 segments 1, 3 and 4 (300 / 700 / 600 wide)
carry no Glass price line at all. **Break-even is GBP 252.15/m2 of panel.** Neither quote yields a panel
rate - BSW bundle them with no extractable figure, Aplus exclude them - and `data/supplier-rates.json`
has **no panel or spandrel category**. It cannot be settled from anything we hold.

**Aplus's own qualifications, page 16, verbatim - this is the value of the quote:**

- **"Quoted in STII, these will only reach 1.8/1.9 U Value."** Against a specified 1.0 per element. Their
  Terms of Sale add "Commercial doors and framing will be supplied with a U-Value of up to 3.0 Wm2/K".
- **"STII doors have no formal acoustic test data."** ED-06 needs >= Rw 32 dB.
- **"Glass quoted has a g value of 0.66."** Against 0.5-0.6. First hard g-number anyone has given us.
- **"Access controls /automation by others - quoted with Pas24 maglock."**
- **"Mullions tested to a minimum of 950Pa"** while their own terms calculate to BS 6399 Pt 2 at 1200Pa
  "unless otherwise stated", then disclaim: "all design responsibility remains with the Customer". On
  3,570 mm mullions that is the contractor's-design element behind Stepnell's PI requirement.
- **"Please specify exact clear opening required"** - M4(2) unconfirmed; the ED-04 door segment is
  separately marked **"DDA Compliant No"**.
- **"DO NOT ORDER - Unglazed : A4 - (1163 x -3)"** - a NEGATIVE 3mm aperture on all three door segments.
  The Logikal model does not close; transom setting-out needs confirming against 31551's zones.
- **"All orders are priced as Ex-Works"** against a header reading "(Delivered)". Free only over
  GBP 5,000 AND within 50 miles of Watford; Bristol is ~105 miles and the GBP 1/mile rule is written only
  for loads UNDER GBP 5,000. **Carriage is in neither supplier's number.**
- 30-day validity (~26/08/2026); lead time "confirmed on receipt of written order", i.e. none; payment
  "Deposit and cleared Funds Prior to delivery on first order" - 100% before delivery.

**Three things the second quote settles:**

1. **The sizes.** Aplus segment to 1233+1233+1232+1232 = **4930**, 1250+1434+1434+1432 = **5550**, and
   300+1200+700+600+1172+1172+1171 = **6315 x 3105** - the trade bill exactly, with ED-06's split being
   the dimension string printed on drawing 31551 itself. So BSW's 4850/4800/6250x3100 are wrong on five
   of seven, and our own 3150 is confirmed a typo for 3105.
2. **The g-value.** 0.66 on a standard clear lami/tough soft-coat build. Finding 3 is now quantified,
   and it applies to BSW's un-named make-up too.
3. **The U-value.** Two independent fabricators have now refused it in writing. **This stops being a
   supplier problem and becomes a specification one** - a standard commercial shopfront system is not
   thermally broken to curtain-walling standard and does not reach 1.0. Very likely why RCKa named
   Aluprof and issued the drawings to Aluprof directly in October 2025. **Fenster have approached no
   Aluprof fabricator at all.** Findings 17 and 18.


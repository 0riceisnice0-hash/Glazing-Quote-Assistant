# Princess Beatrice House — Guildmore Planned Works / RBKC

**Site:** 188-190 Finborough Road, Earls Court, London SW10 9BA
**Client:** Guildmore Planned Works Ltd, Ertosun House, 61 Widmore Road, Bromley BR1 3AA
**Contact:** Jason Mount, Commercial Manager — jason.mount@guildmore.com, 020 8313 5050
**Employer:** RBKC (GLA-funded scheme). CA: BPG. Client bill ref C0234 Block 1.
**Chat key:** `princess-beatrice` · **Checks manifest:** `data/job-checks/princess-beatrice-house.json`

---

## Where this stands

**QUOTE ISSUED 27/07/2026 09:49 by Gintare to Jason Mount — GBP 279,244.69 ex VAT.**
Released by Adam at 08:56 that morning ("proceed with sending this out with the discount"). Return date
was 17/07, so it went 10 days late. Guildmore replied the same evening, so the job is live.

Build, verified exact against the workbook that actually went out:

| | |
|---|---|
| 46 line rows / 217 units | 233,091.68 |
| Installation | 39,680.00 |
| External mastic | 5,356.22 |
| EPDM | 8,276.91 |
| **Subtotal (I62)** | **286,404.81** |
| 2.5% MCD (I64) | −7,160.12 |
| **TOTAL (I65)** | **279,244.69** |

Base of 272,771.68 is unchanged from the 23/07 audit, so Adam's two instructions of 24/07 — mastic and
EPDM into the sum, add 2.5% MCD — were both actioned. The MCD was taken as a straight deduction off the
bottom, so it comes off margin; neutral treatment would have needed the subtotal grossed to 293,748.52.
Gintare asked, Adam approved the method, so it is recorded and not logged as an error.

**Supply behind it:** A Plus Crystal QP70171 (21/07/2026, GBP 111,185.75 nett glazed) and A Plus Logikal
Technal STII offer (22/07/2026, GBP 17,499.74). Both lapse ~20-21/08 on A Plus's stated 30 days — before
our own price closes. The pack also contains QT39795 dated 22/07/**2025**, last year's letter: date-check
every supplier document in this folder.

---

## The live issue: strip-out

Jason Mount, 27/07 19:21 — *does the quote allow for removal of the existing windows, and if not what is
the additional sum.* Adam answered him direct at 19:56:

> "I can confirm we have allowed for strip out of old frames. We have not allowed for disposal, ie skips
> on site."

**Why he asked.** The client's own bill has a Collection page carrying three lines — *General*,
**"Strip out"**, *New windows and Doors*. Our pricing document has no strip-out line at all; it has
window and door rows plus one INSTALLATION sum. Jason was reconciling our number against a schedule with
a strip-out line in it and finding nothing against it. The question was not idle.

**The commitment is in neither document we issued.** Swept the proposal's 10 pages for strip / remove /
removal / disposal / skip / waste / make good: nothing includes strip-out. The pricing workbook has no
strip-out line in its only sheet.

**And it is not in the money — this is proven, not inferred.** GBP 39,680 is exactly the sum of the house
labour codes over 217 units (146 MAW + 46 SAW + 6 LAW @160, 4 ELAW @250, 13 DAD @500, 2 SAD @250), zero
residual. On its own that only shows the number is code-derived. **The control settles it:** the same
codes produce GBP 9,570 over 37 units on **Brocks Hill Phase 2, a new teaching block with no existing
window to remove**, and GBP 8,500 over 52 units on Crestwood Park, a replacement job. Fenster charges the
identical per-unit fit rate whether or not there is a frame to strip out. The rate is fit-only. There is
no strip-out money anywhere in the GBP 279,244.69.

There is also no strip-out rate in `data/supplier-rates.json` — one of the 21 categories returning zero —
so what it *should* cost cannot be stated from anything on file. Quantity for an RFQ: **217 units /
336.17 m2**.

**What the bill actually puts in that line is far more than "old frames."** C0234 Block 1, *Preparation &
Stripping Out*:

- **Item A (B30-B35)** — remove existing windows, external doors **and frames** incl. trims, mortar
  bedding, fixings and sealants; protect all DPCs, cavity closers and brickwork; **make good facing
  brickwork and pointing with matching bricks and tinted cement mortar**; **cut back plaster/render
  internally and make good with one coat gypsum plaster, dubbed out flush**; any internal damage made
  good **at the Contractor's expense** to the CA's satisfaction unless prior notice of defective finishes
  is given; old windows to a **"trade" waste recycling transfer station, documentation retained on site**.
- **Item B (B38)** — staircase windows at ground, first and second floors removed **for general site
  access** and installed **out of sequence**, with due allowance for **returning** to complete them.
- **Item C (B41)** — existing windows and doors remain in-situ to maintain water tightness; we remove and
  replace to maintain it, protect exposed openings, and **carry liability for water damage** from
  inadequate protection.

Making good brickwork, pointing and plaster is builder's work. Out-of-sequence return visits are a
programme cost. Neither is fit labour.

**Disposal is not one-way, and Adam has answered as if it is.** *For us:* bill B5, the preamble to the
whole sheet — "All items are deemed to include for removal to **Guildmore skip** placed at the front of
the building and making good adjacent structures and surfaces disturbed by the works, whether
specifically mentioned or not." Guildmore provide the skip and we carry to it, so Adam's answer matches
the bill. *Against us:* B35's trade waste recycling transfer station with documentation is a leg beyond
Guildmore's skip; and the RBKC ER's definitions read "**Remove:** means disconnect, dismantle as
necessary and remove the stated element… **and dispose of unwanted materials**", which if read into item
A's "carefully remove" pulls disposal inside the strip-out item. *And our own wording is broader than
either:* proposal p4 "Waste Removal – Generally excluded unless agreed otherwise" disclaims even the
carry-to-skip that B5 deems included.

(The ER is addressed throughout to "the Contractor", which on this job is **Guildmore**, not Fenster —
the actor test St Mary's got wrong and corrected. It bites only so far as Guildmore's bill borrows its
language, which B30 arguably does.)

---

## Everything else found against the issued pack

Ranked by money and by how hard it would be to argue.

1. **Mastic charged at 5,356.22 and called an optional extra in the same email (REQ-6).** The bill settles
   the part the hub discussion left open: perimeter sealing is **not** optional here, it is a specified
   bullet of the window renewal item with **named products** — B68 Tremco Illbruck *illmod TP654 TRIO
   1050 66/6-10* expanding tape to head and jambs with the sill bedded on two 8x8mm beads of *SP525*;
   B69 *FS125 + Backer Rod* perimeter seal; B70 *LD703* internally. So Adam's instruction to bring it
   into the sum was **correct and the pricing document is right**. What is wrong is proposal p3, still
   reading "External mastic is charged as an optional extra" — and the danger is not cosmetic: it invites
   Guildmore to strike 5,356.22 as an option we offered while B68-B70 still oblige us to do the work.
   Verified at source: mastic I59 and EPDM I60 sit **above** the subtotal, inside the client's number.
   The pre-instruction workbook in `princess-beatrice-input` is built the other way, with an OPTIONAL
   heading below a TOTAL — that is the standard template Adam described on the hub, and is how Crestwood
   Park and Brocks Hill are built. **The two documents genuinely differ; his answer described the
   template, not this job's document.**
2. **EPDM 8,276.91 — stop bracketing it with mastic.** Swept the bill and the RBKC ERs for EPDM and
   BS 4255: **zero hits in either**. Unlike Brocks Hill, where ER 7.5.1 requires it and it sits in the
   optional block the wrong way round, here no requirement for EPDM has been located at all, and it is
   charged inside the client's number with no mention in the clarifications. Mastic's question is "stop
   calling a specified obligation optional." EPDM's is the opposite: "what is this for if Jason asks."
   *Caveat:* the Technal Annex A is not in our pack and was not searched.
3. **Scaffolding — a blanket exclusion against a clause drafted to defeat it.** Bill B21: "Any additional
   scaffolding required to complete your works **are required to be detailed in your tender return** and
   Guildmore will instruct the scaffolding company. **If your tender does not identify any additional
   scaffolding required after commencement will be deducted from works value.**" Guildmore pay for and
   instruct the scaffold — but only what you listed. Our proposal p4 answers with "Access/Lifting
   Equipment – Scaffold, MEWPS, Towers, Forklift etc." and identifies **nothing**. Multi-storey block;
   B38 confirms staircase windows at three levels. **This is not the St Mary's answer** — there the head
   contract put scaffold on ET&S including for their sub-contractors. Same question, different answer,
   because Guildmore's own document says so. Still fixable: the schedule can be written before
   commencement.
4. **Insurance-backed FENSA guarantee — unpriced premium.** Bill B72: "a comprehensive **insurance-backed**
   minimum **FENSA** 10-year guarantee to cover ALL units installed. **The premium** for the guarantee is
   to be paid and **the policy document issued, in favour of the Employer, before Practical Completion**."
   Our proposal p8 offers Fenster's own 10-year warranty on glass and frames — self-backed: no insurer, no
   premium, no policy to RBKC, no FENSA registration named, **and no start date stated**. Three unpriced
   things. Second job this week after Lower Range Road, and unlike Lower Range this one is already with
   the client. (This was finding 11 of my 23/07 audit; it never left the workbook.)
5. **Modeal substituted for Technal on the windows too — not just the doors.** Bill B66 requires
   everything "fully in accordance with the Technal UK specifications (L10 windows / L20 doors)… **or
   equal approved** — Technal **Dualframe 75Si** casement windows and Technal Soleal Next 75 /
   **Stormframe STII** doors", with B67 requiring fabrication drawings for the CA's approval. Our pricing
   headings: C8 "Technal Aluminium Doors & Screens", C19 "**Modeal** Aluminium Casement Windows", C49
   "**Modeal** Complex Coupled Doors". Two of three sections are a substitution; the record has only ever
   carried the door one. "Or equal approved" makes it permissible in principle, but approval is a positive
   act nobody has sought, and Annex A is not in our pack so equivalence cannot be evidenced. Plus the
   standing internal contradiction: proposal p3 tells the client the doors are Technal STII.
6. **PAS 24 — now disclaimed by three documents, one of them our own supplier's terms.** Our proposal
   claims PAS24 multipoint locking. The 59-page drawings pack **we attached** says "ITEMS GLAZED WITH
   PANELS HAVE NOT BEEN TESTED TO PAS24" on pages 2, 3, 4, 5 and 58. And **new**: A Plus's *Quotation
   Advisory Notes*, the terms behind both quotes, read — "It is the responsibility of the **Customer** to
   ensure all building regulations…, Secured by Design, PAS 24 (formally BS 7950) are adhered to. **The
   Supplier does not warrant or represent that any Product supplied shall comply with any of the
   aforementioned standards** unless where expressly stated to the contrary." Against a Part Q / SBD
   Silver ITT that is a straight pass of the risk to us, which we then passed to Guildmore as a claim.
7. **Final clean — the bill requires it and our proposal hands it back.** B75 "Remove all protective
   coverings, ease and adjust window sashes"; B76 "Clean **ALL** glazing, panels, trims and frames inside
   and out… lubricate ironmongery." Proposal p4, **in the exclusions column**: "Final Clean on handover –
   Final clean and removal of protection tape **to be completed by client**." B77 wants O&M/H&S File
   information at handover; our T&Cs issue the O&M manual only **after final payment**.
   *(I first recorded this as covered, from a note saying the proposal "carries Final Clean on handover".
   It does — in the wrong column. Read the column, not the phrase.)*
8. **The pricing workbook we sent carries another company's identity.** `docProps/core.xml` creator =
   **"Dan Parker; dan.parker@agsurveying.co.uk"**, plus external links to
   `C:\Users\LiamO'Donnell\…\Content.Outlook\…\Electrical Template - Draft - REV010.xlsx`,
   `C:\Users\Parke\…\The Datum Group Electrical - TEMPLATE - Detailed breakdown Rev 5.xlsx` and an
   `agsurveying.sharepoint.com` URL. **Not a Princess Beatrice defect —** `templates/MASTER PRICING
   DOC.xlsx` carries the same creator and the same two links, so every quote cloned from it does:
   confirmed on Crestwood Park, Brocks Hill, Gordon Court and SM5 Wexham. Folded into **REQ-27**, which
   gordon-court raised on the same defect from their own job.
9. **3nr Louvre Type 01 (WLF 13/16/19) and 2nr 2280×1068 Door Type 1 side screens (DGF 22/23)** — on the
   schedules, in neither Aplus quote nor the pricing, and **not excluded**, while the proposal's executive
   summary tells the client the elevations identify acoustic louvre elements. ~GBP 3,500-5,500 sell,
   benchmark only. Open since 23/07.
10. **Bill item AA is three blanks we never filled** — B91/B93 uPVC price variance, B108 lead-in for
    aluminium, B110 lead-in for uPVC. All still blank in what we issued. These are the questions Guildmore
    intend to compare tenders on.
11. **Smaller, all open since 23/07:** GBP 668.41 of the Aplus window quote not carried into priced rows;
    heights deviate from BPG T02 (Type 3 priced 960 vs 1135, Type 6 1375 vs 1160); 76 of 191 entries
    flagged obscure against obscure splits only on Types 5/6/7; heat-soak + Kitemark hedged as "where
    quoted" against an ER that requires it on all toughened.
12. **Commercial:** the issued pricing document still reads **"Date: 23/07/2026"** though it went on 27/07
    — which makes our own 30-day validity ambiguous (22/08 or 26/08). Crestwood's dates *were* amended
    before issue on Adam's instruction the same morning; these were not. Both Aplus quotes lapse ~20-21/08,
    i.e. before our price closes on either reading — GBP 128,685.49 of cost unfixed, though only by days.
    Collateral warranty, retention and programme are required by the Guildmore ITT and unaddressed by our
    proposal, whose T&Cs the sub-contract order will override.

`mary_checks.py data/job-checks/princess-beatrice-house.json` → **6 FAILED**.

---

## Who owes what

| Who | What |
|---|---|
| **Adam** | REQ-29 — reissue a corrected proposal, or leave the commitment in the mail thread. Now carries four corrections, not one: strip-out stated in writing on **our** definition (frames, not the bill's making-good), mastic/EPDM wording (REQ-6), the scaffold schedule under B21, and the insurance-backed guarantee premium. |
| **Adam** | REQ-6 — leave proposal p3 as issued or send a corrected page 3. The bill now answers the merits: sealing is specified, so "optional extra" understates our obligation. No money moves either way. |
| **Adam** | REQ-27 (broadened) — fix `templates/MASTER PRICING DOC.xlsx` once and every future quote is clean. |
| **Guildmore / CA** | Formal "equal approved" for Modeal against Technal Dualframe 75Si and Soleal/STII; Annex A copy. Louvre Type 01 and the Door Type 1 side screens — in or out. Bill item AA's three blanks. |
| **A Plus** | Does QP70171 cover all 76 obscure entries? Heat-soak + Kitemark? A stated U-value — their default is "no better than 1.8", and up to 3.0 on commercial doors and framing. Written PAS24/SBD position, since their own terms decline to warrant it. |

**Nothing has been sent to Guildmore by Mary.** Adam replied to Jason direct on 27/07 19:56; the client
has had no correspondence from this chat.

---

## Decisions taken, and why

- **Raised no new requests this turn**, on the noticeboard's 28/07 16:44 instruction — 23 are open and
  unanswered, so scaffolding and the guarantee were folded into REQ-29 (whose subject is already "what
  goes into the corrected proposal") and the template leak into REQ-27 rather than adding three more.
- **REQ-6 left open**, per triage's handoff. Adam's hub ruling of 18:35 describes the standard template
  accurately; this document is not built that way. Not closed on the strength of wording that answers a
  general question.
- **Strip-out reported as an exposure, not priced.** No rate exists on file and inventing one would be
  worse than the gap.

## Notes for whoever picks this up

- The pricing workbook filename contains **U+00A0 non-breaking spaces**. Glob it; never type the path.
- BPG "GR" schedule drawings have clean text layers — pdfplumber them, no tiling or rendering needed.
- The **issued** pack is `test-results/mary-inbox/processed/20260727T0949-z2JAAAAA-att/`. The
  `princess-beatrice-input` copy is the **pre-instruction** version — it still has the code column B
  (which is how the labour codes were recomputed) and the old OPTIONAL block. Do not audit the wrong one.
- Guildmore said on 06/07 they would issue **a fully developed design in 4-6 weeks** for a full and final
  offer. That lands mid-August. Everything above is worth fixing before that reprice, not after.

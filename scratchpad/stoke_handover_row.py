# -*- coding: utf-8 -*-
"""Replace the Stoke Park row in MARY-HANDOVER.md section 7 with the corrected position."""
import io

P = "MARY-HANDOVER.md"

ROW = (
    "| **Stoke Park School (Borras Construction)** - LIVE PROJECT, not a tender | "
    "Won and in production: Aplus job **17644**, Technal **Soleal Next FZ75**, client price "
    "GBP104,660.17 ex VAT (pricing doc rev 15/07), order signed off 17/07. Frames come "
    "**UNGLAZED, supply only, delivery 03/08/2026** - the glass **and the louvres** are "
    "Fenster's to buy. Full record in `data\\jobs\\stoke-park.md`. "
    "**REQ-3 CLOSED 27/07 - the 46-pane 'shortfall' was WRONG and is withdrawn.** Mary "
    "reported Aplus's final 24/07 list (170 panes) as 46 short of Vetroseal 064542 (124 "
    "panes). Adam answered that the 46 are **louvres, glazed in in place of glass**, from "
    "IKON not Vetroseal - confirmed at source by two documents already in the job folder: "
    "Aplus panel order `QT50932 Rev7 Louvres.pdf` (46 panels, 27.64 m2) and **IKON "
    "Q26-24329** (02/07, 46 IKL332 28mm modules, RAL 7012 matt, insulated backing + insect "
    "mesh, **GBP10,125.91** + carriage TBC). They sit at ref A1 on every bay of Types "
    "A/B/C/D/F/G (41), the head over D02 and D04 (2), and all three panels of **Door Type C "
    "/ D03, a louvred door** (3). Remove them and the glass reconciles exactly: **124 "
    "required = 124 quoted**, 106.97 m2 v 105.24, +1.73 m2 (~GBP197). No shortfall, no "
    "GBP2,920. **What the check did find, now REQ-11 and urgent: BOTH BUYS ARE SIZED TO A "
    "SUPERSEDED SCHEDULE.** Aplus re-input the job **02/07** and signed the frames off the "
    "same day; Vetroseal 064542 (01/07) and the panel schedule IKON priced (input 01/07) "
    "both predate it. **0 of 124 quoted panes match an ordered size** (vents 404->448 high "
    "on every type, Type H -166mm, every door leaf 1859->2059), and **all 41 window louvres "
    "are 85mm too tall** (signed-off A1 aperture 391 v IKON's 476; door heads out +245 D02, "
    "+50 D04, +78 D03). The authority on sizes is the **order sign-off** "
    "`Order Sign Off_17644.PDF`, not any quote. **Also: cost runs GBP5,338.93 over the sold "
    "price** - the build-up carries Vetroseal GBP9,309.22 and IKON GBP7,490.64, which are "
    "the **05/06** quotes (063934 and Q26-24160) to the penny, never revisited when the "
    "01-02/07 quotes landed. Moving the glass to CN Glass at GBP60/m2 (~GBP6,150 on 102.51 "
    "m2 of 28mm v ~GBP11,700) recovers about GBP5,550 of it. CN Glass provenance unchanged: "
    "**a verbal rate confirmed by return email, NOT a quotation** - Steve Freezer wrote the "
    "rates into his own 01/07 email to Martin Gregory and Martin replied only \"Pls see "
    "below as discussed\"; there is no CN Glass quotation document on file. Workbook "
    "`outputs\\Stoke Park School - Glass Sizes vs Quoted Glass (check).xlsx`; generator "
    "`scripts/stoke-glass-compare.py` (rebuilt on the corrected basis). | "
    "**REQ-11: re-quote glass AND louvres against the signed-off 02/07 apertures before "
    "either order goes in - Mary cannot email suppliers.** Frames land **03/08**; the "
    "louvres are the longer lead, bespoke and powder coated. Still open: make-up for the "
    "**six 32mm panes** (D01 screen x5 + D05 head, 4.46 m2) which no quote covers; whether "
    "the glass order goes to Vetroseal or CN Glass. Unchecked: whether the Aplus frame cost "
    "of GBP42,063.18 moved between the Rev1B pricing (DualFrame 75Si) and the Rev7 order "
    "placed (Soleal Next FZ75). |"
)

s = io.open(P, encoding="utf-8").read()
lines = s.split("\n")
for i, l in enumerate(lines):
    if l.startswith("| **Stoke Park School"):
        lines[i] = ROW
        break
else:
    raise SystemExit("Stoke Park row not found")

io.open(P, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("MARY-HANDOVER.md section 7 row updated")

# -*- coding: utf-8 -*-
"""REQ-11 closed: update the MARY-HANDOVER row and add the HANDOVER.md record."""
import io

ROW = (
    "| **Stoke Park School (Borras Construction)** - LIVE PROJECT, not a tender | "
    "Won and in production: Aplus job **17644**, Technal **Soleal Next FZ75**, client price "
    "GBP104,660.17 ex VAT, order signed off 17/07. Frames **UNGLAZED, supply only, delivery "
    "03/08/2026** - glass, louvres and panels all Fenster's to buy. Full record in "
    "`data\\jobs\\stoke-park.md`. **REQ-3 AND REQ-11 BOTH CLOSED; nothing raised on this job.** "
    "REQ-3: the 46 'missing' panes were **louvres**, not a glass shortfall (Adam, 27/07) - "
    "withdrawn. REQ-11: the glass and louvre quotes on file were dimensioned to a schedule "
    "superseded by Aplus's 02/07 re-input, but **Steve had already placed all three orders "
    "correctly on 27/07** - Zac answered 28/07 that the corrected sizes went to "
    "**commercial@fensterglazing.com**, which Mary does not poll. Verified against the orders "
    "themselves, now in **`4. Orders\\`**: **glass CN Glass 124 units / 106.946 m2 / "
    "GBP6,185.09** (Spec A 6.8/16/4 GBP55/m2, Spec B 8.8/16/4 GBP60/m2, Spec C 8.8/20/4 - the "
    "32mm unit - GBP60/m2); **louvres IKON 44 modules / 20.674 m2 / GBP7,587.30** (IKL332 28mm "
    "glazed-in, insulated blanking panels, RAL7012, **GBP367/m2**, at the signed-off 391mm not "
    "the 476 quoted); **panels Metfab 2no 770x2059** insulated aluminium, being D03's two door "
    "leaves - which is why the louvre count is 44 and not 46. **170 items / 130.79 m2 = Aplus's "
    "final list exactly, every size matching the sign-off.** The 32mm make-up no quote had "
    "covered is answered by Spec C. **COMMERCIAL OUTTURN: the buy came in about GBP3,027 UNDER "
    "the sold price** (build-up carried Vetroseal GBP9,309.22 and IKON GBP7,490.64 against "
    "actual GBP6,185.09 and GBP7,587.30) - the earlier GBP5,338.93 overrun never happened, "
    "because the glass moved to CN Glass. CN Glass is now a **placed-order rate, no longer a "
    "verbal one**. | "
    "Nothing raised. Left with Steve and noted only: the **Metfab order carries no rate** (the "
    "one open cost), and **Spec A is 26.8mm on 73 panes Aplus nominate as 28mm** - probably "
    "deliberate but worth confirming the beads suit before 03/08. Mary's own follow-up: check "
    "whether the Aplus frame cost of GBP42,063.18 moved between the Rev1B pricing (DualFrame "
    "75Si) and the Rev7 order placed (Soleal Next FZ75). |"
)

s = io.open("MARY-HANDOVER.md", encoding="utf-8").read()
lines = s.split("\n")
for i, l in enumerate(lines):
    if l.startswith("| **Stoke Park School"):
        lines[i] = ROW
        break
else:
    raise SystemExit("Stoke Park row not found")
io.open("MARY-HANDOVER.md", "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("MARY-HANDOVER.md row updated")

RECORD = """### Stoke Park School (Borras) - REQ-11 closed: the orders were already right (2026-07-28)

Work order `dashmsg-37.json`, Zac on the dashboard answering REQ-11: *"The correct glass sizes were all sent to
commercial@fensterglazing.com to which you do not have access, which we received on 27/07"*.

He is right, and REQ-11 is closed. Rather than take it on trust, checked it against the orders themselves - which
turned out to be on file in a folder this chat had never opened, **`4. Orders\\`**, created 27-28/07:

| Order | Supplier | Qty | m2 | Value |
|---|---|---|---|---|
| `Glass Order\\Stoke Park - Glass Order.pdf` | **CN Glass** | 124 units | 106.946 | **GBP 6,185.09** |
| `Louvre Order\\Stoke Park - Louvre Order.pdf` | **IKON** | 44 modules | 20.674 | **GBP 7,587.30** |
| `Panel Order\\Stoke Park - Panel Order.pdf` | **Metfab** | 2 panels | 3.171 | **unpriced** |

All three dated **27.07.26**, prepared and approved by **Steve Freezer**, generated from `4. Orders\\Glazing
Schedules.xlsx` - a three-sheet house template (Glass / Panel / Louvre) with a Spec A-B-C pricing block.

**Every size on the glass and louvre orders matches the signed-off 02/07 apertures.** Type A 933x448 and 1041x1191,
Type C 941x448 and 1049x1191, door leaves at 2059, D05 head 1933x733; louvres at **391mm**, not the 476 IKON quoted.
The 85mm mismatch and the 0-of-124 pane mismatch are both gone. 170 items / 130.79 m2 is Aplus's final list exactly.

Two things the orders settled that no quote had. **The 32mm make-up** - Spec C is 8.8 lami / 20mm argon / 4mm
toughened at GBP 60/m2, covering the D01 screen and the D05 head. And **the 44 v 46 split**: D03's two door leaves are
**insulated aluminium panels from Metfab** (1.5mm PPC alu / 25mm Rockwool / 1.5mm PPC alu), not louvres. The 46
non-glass positions were right; the supplier split was inference and is now 44 louvres + 2 panels.

**The commercial position improved and the 27/07 overrun never happened.** The build-up carries Vetroseal
GBP 9,309.22 and IKON GBP 7,490.64; the actual buy is GBP 6,185.09 and GBP 7,587.30 - about **GBP 3,027 UNDER** the
sold price rather than GBP 5,338.93 over. The CN Glass switch is what did it, and CN Glass is now a **placed-order
rate rather than the verbal one** flagged repeatedly: Spec A 6.8/16/4 GBP 55/m2, Spec B 8.8/16/4 GBP 60/m2,
Spec C 8.8/20/4 GBP 60/m2. IKON louvres GBP 367/m2.

Noted for Steve, deliberately **not raised** given 25 requests already open: the Metfab order carries no rate, and
Spec A is 26.8mm on 73 panes Aplus nominate as 28mm (Spec B at 28.8mm is the like-for-like) - probably a deliberate
choice of 6.8 lami on the smaller high panes, but cheap to confirm before 03/08. Not mentioned at all: the orders
consolidate Aplus's 1mm width variations (1048/1049, 940/941) to the larger, which is within glazing clearance.

**The lesson, and it is structural rather than another instance of carelessness.** This is the fourth time this week
Mary has reported something already in hand (Crestwood's Teleflex quote, Grange Hill's chapel doors, Vesuvius's BSW
zip, now this). The other three were "read the whole thread". This one is different and has a concrete remedy: there
are two places Mary **structurally cannot see**, and they are exactly where live-project procurement happens.

- **`commercial@fensterglazing.com`** receives production documents for won jobs. `mary_graph.py` lines 23-24 poll
  **`estimating@` and `mary@` only** - confirmed against the 161 queue/processed files, which carry no other mailbox.
- **`<job>\\4. Orders\\`** holds the placed orders. Never opened on any job before today.

Both written into `data\\jobs\\stoke-park.md` as a banner at the top of the file and posted to the noticeboard. On any
LIVE project the estimating trail is history, not the current position - check `4. Orders\\` before saying a buy is
wrong, and treat absence of evidence in a mailbox you cannot read as no evidence at all.

"""

s = io.open("HANDOVER.md", encoding="utf-8").read()
ANCHOR = "### Autopilot session log (no-action sessions)"
if ANCHOR not in s:
    raise SystemExit("anchor not found")
s = s.replace(ANCHOR, RECORD + ANCHOR, 1)
io.open("HANDOVER.md", "w", encoding="utf-8", newline="\n").write(s)
print("HANDOVER.md record inserted")

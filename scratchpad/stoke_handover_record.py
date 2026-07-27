# -*- coding: utf-8 -*-
"""Insert the REQ-3 answer record into HANDOVER.md, before the autopilot session log."""
import io

P = "HANDOVER.md"
ANCHOR = "### Autopilot session log (no-action sessions)"

RECORD = """### Stoke Park School (Borras) - REQ-3 answered: the 46 panes are LOUVRES, and the real problem is sizes (2026-07-27)

First turn of the permanent job chat for Stoke Park. Work order `dashmsg-13.json` - Adam answering REQ-3 on the
dashboard: *"This is a live project, not a tender. The 46nr missing panes are because there are louvres on the job
which will be glazed in, in place of glass. Vetroseal are our glass supplier, our louvres come from another supplier
which is usually IKON. Also, I can't call you, why is that a prompted answer?"*

**He is right, and the morning's headline is withdrawn.** Two documents were already in the job folder and neither had
been opened when REQ-3 was raised:

- `1. Estimating\\2. Supplier Quotes\\QT50932 Rev7 Louvres.pdf` - an Aplus **PANEL ORDER**, 46 panels, 27.64 m2.
- `1. Estimating\\2. Supplier Quotes\\IKON\\Q26-24329 __ Stoke Park Coventry - Louvre Schedule .eml` - Jason Holman to
  Steve Freezer, 02/07, **46 IKL332 28mm glazed-in louvre modules**, RAL 7012 matt, 1.5mm ali / 50mm Fabrock
  foil-backed insulated blanking panels, insect mesh: **GBP 10,125.91 + carriage TBC** (EO plenum trays GBP 4,445.89).

46 and 46, position for position: ref A1 on every bay of Types A/B/C/D/F/G (41 - Type G carries A1 and F1), the head
over D02 and D04 (2), and all three panels of **Door Type C / D03, which is a louvred door** (3). Remove them and the
glass reconciles **exactly - 124 panes required against 124 quoted**, 106.97 m2 v 105.24, +1.73 m2, about GBP 197 at
Vetroseal's rate. There is no shortfall and no GBP 2,920. Three of the nine 32mm panes are louvres too.

**What the check did find, and it is worse than what was raised.** The same comparison run on size rather than count:
Aplus **re-input job 17644 on 02/07** and the frames were signed off the same day. Vetroseal 064542 (01/07) and the
panel schedule IKON priced against (input 01/07) both predate that re-input.

- **Glass: 0 of 124 quoted panes match an ordered size.** Vents moved 404 -> 448 high on every window type, Type H came
  down 166mm, every door leaf went 1859 -> 2059, the D05 head 473 -> 733.
- **Louvres: the signed-off A1 aperture is 391mm high; IKON quoted 476mm.** All 41 window louvres are 85mm too tall;
  door heads out by +245 (D02), +50 (D04), +78 (D03). Bespoke and powder coated, so the longer lead of the two.

Frames land **03/08**. Raised as **REQ-11**. The authority on sizes is `Order Sign Off_17644.PDF` (39pp, order date
02/07, printed 16/07), which lists the apertures the frames are actually manufactured to - not any quote. It also
shows the ordered system is **Soleal Next FZ75**, where the Rev1B priced quote of 04/06 was DualFrame 75Si.

**And a third thing nobody had spotted: the price is carrying the superseded costs.** The build-up in
`3. Client Quote\\SS\\Quotation - Stoke Park School Coventry - DO NOT SEND.xlsx` reads Aplus 42,063.18 / Teleflex 6,440
/ **Vetroseal 9,309.22** / **Ikon 7,490.64**. Those last two are the **05/06** quotes to the penny - Vetroseal 063934
and IKON Q26-24160 - never revisited when the 01-02/07 quotes arrived. Against the current quotes that is
**GBP 5,338.93 of cost above the GBP 104,660.17 sold price**, plus IKON carriage TBC. Most of the IKON rise is a
genuine spec move: blanking panels went from 1.5mm aluminium at ~GBP 29.70 each to insulated at ~GBP 68.84.

That is what makes CN Glass matter here: 102.51 m2 of 28mm at GBP 60/m2 is about GBP 6,150 against about GBP 11,700
from Vetroseal, a saving near GBP 5,550 - close to the whole overrun. Provenance caveat unchanged and repeated in the
reply: **a verbal rate confirmed by return email, not a quotation.** Caveat on the overrun itself: that workbook is in
an `SS` folder and totals GBP 104,822.26 against the issued GBP 104,660.17, so it is a near-final working file - the
supplier figures matching the 05/06 quotes exactly is not coincidence, but say "on the build-up I can see" if pushed.
Not yet checked: whether the Aplus frame cost moved between Rev1B and the Rev7 order actually placed.

On Adam's second question - "I can't call you, why is that a prompted answer?" - the `Call me, it's complicated`
option had already been removed after Zac raised it that morning, and `mary_dashboard.py` now refuses to publish a
board containing an unactionable option. Confirmed to him rather than left to look unanswered.

`scripts/stoke-glass-compare.py` rebuilt on the corrected basis: it now classifies the 46 louvre positions, reports
the glass reconciliation, and adds a **Louvres not glass** sheet (aperture v IKON size) and a **Pane sizes quoted v
final** sheet. Also fixed `mary_dashboard.py`, which crashed on a `UnicodeEncodeError` printing wrangler's box-drawing
characters to a cp1252 stdout *after* a successful deploy - every deploy was ending in a traceback that looked like a
failure and was not.

Lessons: (1) **A systematic shortfall is usually a category, not an error.** One pane per bay across six window types
and one whole door is too regular to be clerical - it means the schedule deliberately excludes something. Search the
job folder for the other supplier before raising the alarm. Both proving documents were on file the whole time.
(2) **On unglazed supply-only orders the frame supplier's SIGN-OFF is the authority on sizes, not any quote** - and
check the input dates on both, because a re-input silently supersedes every downstream buy. (3) **Check which
supplier quote the price was actually built on.** Where a folder holds two quotes from one supplier, the build-up may
still be carrying the old one. (4) Counts reconciling is not sizes reconciling - here the counts were perfect and not
a single dimension was.

"""

s = io.open(P, encoding="utf-8").read()
if ANCHOR not in s:
    raise SystemExit("anchor not found")
s = s.replace(ANCHOR, RECORD + ANCHOR, 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("HANDOVER.md record inserted")

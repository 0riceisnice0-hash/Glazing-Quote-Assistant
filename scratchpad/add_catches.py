# -*- coding: utf-8 -*-
"""Append this run's two audit catches to the hub, idempotently.

Zac's instruction (dashmsg-97): record each finding in the hub's catches with the
document, the line and the money. Neither of these is an error in a document a
client holds - both are cost-record findings - so Adam's morning list is still
Gordon Court REV 2 alone, and each catch says so in its own text.
"""
import json, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "data", "dashboard-state.json")

NEW = [
    {
        "date": "2026-07-30",
        "job": "Knights Construction - CB Refrigeration Workshop (pricing dated 09/06/2026)",
        "type": "curtain-walling notional booked as the cost - internal cost record, not a client error",
        "value": "GBP 14,078.92 of margin not visible in the document, on a sell of GBP 30,073.00",
        "catch": "Row 14, 'CWT-A', 2900x6100, qty 2. The Frames cell reads GBP 15,036.50, which is "
                 "17.69m2 x GBP 850 - the curtain-walling NOTIONAL - and it equals the unit rate "
                 "exactly, so the row reads as zero margin. The real cost is on the quote: BSW/"
                 "Bellview 0000000371 prices '2 Pcs 2,900 x 6,100 mm Curtain Wall Elements' at "
                 "9,996.30, Net Total 19,992.60, 'Discount 2: -20.00%', GRAND TOTAL NET GBP "
                 "15,994.08 - i.e. 7,997.04 each, not 15,036.50. THE QUANTITY IS RIGHT (the "
                 "supplier quotes 2 and we price 2) AND THE BLOCK FIGURE IS RIGHT; it is the "
                 "Frames cell that is a notional. Confirmed against the other 7 curtain-walling "
                 "rows in the archive, where Frames is a genuine lower figure at about half the "
                 "sell (St Mary's 4,419.91/8,655.98, Wisley 12,260.79/19,975.00, median ratio "
                 "0.51): this row's ratio is exactly 1.000, which no other CW row shows, and "
                 "7,997.04 would put it at 0.532, in the middle of the seven. This also closes the "
                 "SUPPLIER 1.291 finding on the document - the other two block figures are its own "
                 "rows to the penny, BSW 4,430.28 = rows 9-13 (quote QT250448) and Strongdoor "
                 "28,027.93 = rows 16-21, so the whole gap was this one row. NOT A CLIENT ERROR: "
                 "the document foots, the client is charged correctly, and it is marked DO NOT "
                 "SEND. It understates our own margin.",
    },
    {
        "date": "2026-07-30",
        "job": "Elkins - Brandon Estate (earlier revision) and Zelltec - Units 16 & 18 Crownhill (both UPVC revisions)",
        "type": "supplier block names suppliers and records no cost at all - control gap, not a client error",
        "value": "GBP 1,484,932.13 + 36,202.66 + 13,521.20 of frames with no buy recorded against them",
        "catch": "Three documents name their suppliers in the 'Supplier used:' block and type no "
                 "figure against any of them. 'DO NOT SEND Pricing Document - Brandon Estate.xlsx' "
                 "names BSW and Vetroseal (frames total 1,484,932.13); both Zelltec Crownhill UPVC "
                 "revisions name Tru Frame, Strongdor and BSW (36,202.66 and 13,521.20). With no "
                 "buy recorded there is nothing to check the margin against, and the supplier "
                 "reconciliation, the cross-job duplicate check and the whole-unit test all skip "
                 "the document in silence. FOUND ONLY BECAUSE THE READER STOPPED INVENTING A "
                 "FIGURE FOR IT: the block window ran six rows past the names into the first "
                 "priced row and read 362,678.40 out of a spare working cell - that row's own "
                 "(frames + glass) x qty, 863.52 x 420 to the penny - which was reported for two "
                 "sessions as GBP 1.12m of supplier gap on Brandon. The two Zelltec revisions are "
                 "the 8.268 and 22.139 ratios previously filed as a reader false alarm; they are "
                 "this instead. NOT A CLIENT ERROR: all three documents foot. The transferable "
                 "point is the one the board already makes about this cell - it is typed by hand, "
                 "and here it was simply never typed.",
    },
]

with open(STATE, encoding="utf-8") as fh:
    state = json.load(fh)
have = {(c.get("date"), c.get("job")) for c in state.get("catches", [])}
added = 0
for c in NEW:
    if (c["date"], c["job"]) in have:
        print("already present: %s" % c["job"][:70])
        continue
    state.setdefault("catches", []).append(c)
    added += 1
    print("added: %s" % c["job"][:70])
if added:
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
print("catches now %d" % len(state.get("catches", [])))

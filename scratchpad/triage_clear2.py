# -*- coding: utf-8 -*-
"""Move the items finished this turn out of the queue."""
import os, glob, shutil

Q = "test-results/mary-inbox/queue"
P = "test-results/mary-inbox/processed"

DONE = [
    "20260730T0941-qOqA",   # Vetroseal 065222 MHA/NUNEATON/2 - checked, rate captured
    "AAGgoITc",             # Vetroseal 065311 ELEVATION/BEDFORD - checked (duplicate)
    "FSkumAAAA",            # Vetroseal 065311 ELEVATION/BEDFORD - checked
    "AAGgoITG",             # AE Glaziers - Paul's board-up enquiry, size now known
    "AAGgoITW",             # BSW Glebe Farm - commercial@ small works
    "AAGgoITR",             # Firefly Avenue - Adam sourcing outward
    "AAGgoITK", "AAGgoITe", # Quickslide Towcester Vale U-value - technical, to Steve
    "AAGgoITQ",             # CN Glass account change - on the noticeboard
    "FSkLZQ",               # AGF Reynaers price increase - on the noticeboard
    "AAGgoITY",             # Adam - Outstanding Quotes, Anton out of office
]

moved = []
for key in DONE:
    for f in glob.glob(os.path.join(Q, "*%s*.json" % key)):
        shutil.move(f, os.path.join(P, os.path.basename(f)))
        att = f[:-5] + "-att"
        if os.path.isdir(att):
            shutil.move(att, os.path.join(P, os.path.basename(att)))
        moved.append(os.path.basename(f)[:36])

print("MOVED %d" % len(moved))
left = glob.glob(os.path.join(Q, "*.json"))
print("QUEUE NOW %d" % len(left))

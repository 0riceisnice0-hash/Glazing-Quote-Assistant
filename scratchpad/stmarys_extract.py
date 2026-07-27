# -*- coding: utf-8 -*-
"""Extract the St Mary's tender zips. Paths exceed MAX_PATH and the filenames may
carry non-breaking spaces, so: walk to find them, then open via the \\?\ prefix."""
import os, zipfile

ROOT = ("C:\\Users\\zacpl\\OneDrive - Fenster Glazing (1)\\Commercial\\"
        "1. Tender Documents\\E T & S Construction")
OUT = os.path.join("test-results", "st-marys-input")

WANT = {
    "revised drawings.zip": "revised-24-07",
    "window schedule and dimensions.zip": "schedule-09-07",
    "curtain walling.zip": "original-08-07",
    "pre construction information.zip": "pci-16-07",
}

for dirpath, _dirs, files in os.walk(ROOT):
    for f in files:
        low = f.lower().replace("\u00a0", " ")
        for tail, out in WANT.items():
            if low.endswith(tail):
                src = os.path.join(dirpath, f)
                dst = os.path.join(OUT, out)
                os.makedirs(dst, exist_ok=True)
                with zipfile.ZipFile("\\\\?\\" + os.path.abspath(src)) as z:
                    names = z.namelist()
                    z.extractall(dst)
                print("%-16s %3d files  <- %s" % (out, len(names), f[:70]))
                for n in names:
                    print("      ", n)

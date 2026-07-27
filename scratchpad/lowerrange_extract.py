# -*- coding: utf-8 -*-
"""Extract the Lower Range Road pack + its clarification-log addendum."""
import os
import zipfile

ROOT = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\Ermine\Lower Range Development\1. Estimating\1. Tender Documents")
OUT = os.path.join("test-results", "lower-range-input")

for f in sorted(os.listdir(ROOT)):
    if not f.lower().endswith(".zip"):
        continue
    sub = "addendum" if "clarification" in f.lower() else "pack"
    dst = os.path.join(OUT, sub)
    os.makedirs(dst, exist_ok=True)
    with zipfile.ZipFile("\\\\?\\" + os.path.abspath(os.path.join(ROOT, f))) as z:
        names = z.namelist()
        z.extractall(dst)
    print("%-9s %3d entries  <- %s" % (sub, len(names), f[:70]))
    for n in names:
        print("    ", n)

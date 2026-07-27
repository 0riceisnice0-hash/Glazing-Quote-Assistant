# -*- coding: utf-8 -*-
"""Stoke Park - pull the apertures off the SIGNED-OFF Aplus order (job 17644, 02/07/2026).

The order sign-off is what the frames are actually manufactured to. Compare its
A1 apertures against the sizes IKON quoted the louvres to (QT50932 Rev7 panel
schedule, 01/07/2026), because the louvres have to fit those apertures.
"""
import re

import pdfplumber

SIGNOFF = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects\Borras"
           r"\Coventry - Stoke Park School\1. Estimating\2. Supplier Quotes\Aplus"
           r"\APlus - Order Signoff\Order Sign Off_17644.PDF")

# Louvre/panel sizes IKON priced, from QT50932 Rev7 Louvres.pdf / quote Q26-24329.
IKON = {
    "Type A": [(1033, 476)],
    "Type B": [(1030, 476), (1032, 476)],
    "Type C": [(1036, 476), (1024, 476), (1023, 476), (1036, 476)],
    "Type D": [(1030, 476), (1032, 476)],
    "Type F": [(1036, 476), (1024, 476), (1023, 476), (1036, 476)],
    "Type G": [(1056, 476)],
    "Door Type B1": [(1933, 783)],
    "Door Type B2": [(1933, 783)],
    "Door Type C": [(1933, 811), (771, 1859), (770, 1859)],
}


def main():
    with pdfplumber.open(SIGNOFF) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)

    lines = text.split("\n")
    current = None
    seen = []
    for line in lines:
        m = re.match(r"^\s*((?:Door )?Type [A-Z][0-9]?)\s*[-–]\s*([DW0-9/ ]+)", line.strip())
        if m:
            current = m.group(1).strip()
        for w, h in re.findall(r"A1\s*-\s*\((\d+)\s*x\s*(-?\d+)\)", line):
            seen.append((current, int(w), int(h)))
        for w, h in re.findall(r"F1\s*-\s*\((\d+)\s*x\s*(-?\d+)\)", line):
            seen.append((current, int(w), int(h)))

    print("A1/F1 APERTURES ON THE SIGNED-OFF ORDER (job 17644, order date 02/07/2026)")
    print("These are the openings the louvres have to fit.\n")
    print("  %-14s %-14s %-14s %s" % ("type", "ordered", "IKON quoted", "difference"))
    print("  " + "-" * 62)

    used = {k: list(v) for k, v in IKON.items()}
    bad = 0
    for typ, w, h in seen:
        cands = used.get(typ)
        if not cands:
            print("  %-14s %-14s %-14s %s" % (typ or "?", "%dx%d" % (w, h), "-", "no louvre here"))
            continue
        best = min(cands, key=lambda c: abs(c[0] - w) + abs(c[1] - h))
        dw, dh = best[0] - w, best[1] - h
        flag = "" if (dw, dh) == (0, 0) else "  <-- LOUVRE DOES NOT FIT"
        if (dw, dh) != (0, 0):
            bad += 1
        print("  %-14s %-14s %-14s %+5d x %+5d%s"
              % (typ, "%dx%d" % (w, h), "%dx%d" % best, dw, dh, flag))

    print()
    print("apertures checked: %d,  mismatched: %d" % (len(seen), bad))


if __name__ == "__main__":
    main()

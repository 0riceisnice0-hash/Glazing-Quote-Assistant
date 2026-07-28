# -*- coding: utf-8 -*-
"""Read the placed Stoke Park orders in '4. Orders' and check them against the
signed-off apertures. This is the real test of REQ-11: not whether the correct
sizes exist, but whether the orders that actually went out use them."""
import os
import sys

import pdfplumber

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects"
        r"\Borras\Coventry - Stoke Park School\4. Orders")

FILES = {
    "glass": r"Glass Order\Stoke Park - Glass Order.pdf",
    "louvre": r"Louvre Order\Stoke Park - Louvre Order.pdf",
    "panel": r"Panel Order\Stoke Park - Panel Order.pdf",
}


def dump(key):
    path = os.path.join(BASE, FILES[key])
    print("#" * 72)
    print(key.upper(), "->", os.path.basename(path))
    print("#" * 72)
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            print("--- page %d of %d ---" % (i + 1, len(pdf.pages)))
            print(page.extract_text() or "")


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(FILES)):
        dump(k)

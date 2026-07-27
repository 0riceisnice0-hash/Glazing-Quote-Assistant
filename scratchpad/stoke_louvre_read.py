# -*- coding: utf-8 -*-
"""Read the Aplus Rev7 glass/louvre split and the IKON louvre documents."""
import os
import sys

import pdfplumber

BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects"
        r"\Borras\Coventry - Stoke Park School\1. Estimating\2. Supplier Quotes")


def dump(path, limit=None):
    print("#" * 70)
    print(os.path.basename(path))
    print("#" * 70)
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages if limit is None else pdf.pages[:limit]
        for i, page in enumerate(pages):
            print("--- page %d of %d ---" % (i + 1, len(pdf.pages)))
            print(page.extract_text() or "")


if __name__ == "__main__":
    for name in sys.argv[1:]:
        dump(os.path.join(BASE, name))

# -*- coding: utf-8 -*-
"""Read the Cranbourne House secondary glazing opportunity doc."""
import os
import re
import zipfile

P = ("C:\\Users\\zacpl\\OneDrive - Fenster Glazing (1)\\Commercial\\1. Tender Documents\\"
     "Elizabeth Scarlett\\Cranbourne House Secondary Glazing\\Tender Documents\\"
     "Elizabeth Scarlett - Cranborne House - Fenster Opportunity.docx")

print("exists:", os.path.exists(P))
with zipfile.ZipFile("\\\\?\\" + os.path.abspath(P)) as z:
    xml = z.read("word/document.xml").decode("utf-8", "replace")

txt = re.sub(r"</w:p>", "\n", xml)
txt = re.sub(r"<[^>]+>", "", txt)
txt = re.sub(r"[ \t]+", " ", txt)
for line in txt.splitlines():
    if line.strip():
        print(line.strip()[:300])

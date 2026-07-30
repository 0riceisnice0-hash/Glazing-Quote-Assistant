# -*- coding: utf-8 -*-
"""Did the fire-egress caveat make it onto the issued Balham REV 1 quote?"""
import zipfile, re, sys

BASE = ("C:\\Users\\zacpl\\OneDrive - Fenster Glazing (1)\\Commercial\\1. Tender Documents\\"
        "Re-Gen (UK) Construction\\Balham Hill\\3. Quote to client\\")

def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    return re.sub(r"<[^>]+>", "", xml)

print("#" * 90)
print("COVER SHEET (docx source of the PDF that went to the client)")
print("#" * 90)
txt = docx_text(BASE + "Commercial Quote Cover Sheet.docx")
for line in txt.splitlines():
    if line.strip():
        print(line.strip())

# xlsx: dump shared strings + any cell text, look for keywords
def xlsx_strings(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "xl/sharedStrings.xml" in names:
            s = z.read("xl/sharedStrings.xml").decode("utf-8", "replace")
            out = re.findall(r"<t[^>]*>(.*?)</t>", s, re.S)
    return [re.sub(r"<[^>]+>", "", t) for t in out]

for f in ("Re-Gen - Balham - Fenster Glazing Quote REV 1.xlsx", "Quotation - Balham.xlsx"):
    print("\n" + "#" * 90)
    print("STRINGS IN %s" % f)
    print("#" * 90)
    ss = xlsx_strings(BASE + f)
    print("total strings:", len(ss))
    KEY = ("egress", "escape", "fire", "exclu", "caveat", "note", "assum", "qualif",
           "rehau", "titan", "technal", "liniar", "approv", "profile", "design")
    for t in ss:
        low = t.lower()
        if any(k in low for k in KEY):
            print(" -", t.strip()[:400])

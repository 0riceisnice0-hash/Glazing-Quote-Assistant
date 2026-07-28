# -*- coding: utf-8 -*-
"""Category-driven sweep of A Plus QT51518 against Fenster's own T&Cs.

Gordon Court's ten-category list was short by "building regulations", which on a
fire/smoke product is the category that matters most. My own sweep last turn had
a different but related fault: it was DOCUMENT-driven, not CATEGORY-driven. I
listed what A Plus's conditions happened to mention and diffed that against
clause 16. So I could only ever find categories A Plus chose to write about -
and a responsibility neither document mentions falls to nobody, silently.

This builds the category list first, independently of either document, then
probes both. A category that neither side claims is the finding.
"""
import io
import json
import re

APLUS = io.open('scratchpad/qt51518_full.txt', encoding='utf-8').read()
FENSTER = json.dumps(json.load(io.open('templates/proposal-content.json', encoding='utf-8')))

CATEGORIES = [
    ("measurement / dimensions",        ["measurement", "dimension", "site survey", "sizes"]),
    ("design intent & suitability",     ["design responsib", "design intent", "architectural",
                                         "interpretation", "fit for", "suitab"]),
    ("Part B / fire & smoke",           ["part .b", "building regulation", "fire", "smoke"]),
    ("Part L / thermal",                ["part .l", "u -? ?value", "u-value", "thermal"]),
    ("Part K / anti-fall",              ["part .k", "anti-fall", "balustrad", "fall from height"]),
    ("structural design of openings",   ["structural opening", "lintel", "forming", "masonry"]),
    ("windload / profile suitability",  ["windload", "wind load", "6399", "mullion"]),
    ("fixings, brackets, spigots",      ["bracket", "spigot", "fixing lug", "bolts"]),
    ("performance figures / free area", ["free area", "aerodynamic", "geometric", "12101"]),
    ("product warranty / guarantee",    ["warrant", "guarantee", "defect"]),
    ("maintenance & in-use duties",     ["maintenance", "occupier", "regulatory reform",
                                         "in full working order"]),
    ("delivery & carriage",             ["deliver", "ex-works", "ex works", "carriage", "haulier"]),
    ("unloading labour at delivery",    ["unload", "suitable labour", "offload"]),
    ("STORAGE OF FINISHED GOODS",       ["storage", "uncollected", "materials off site",
                                         "off-site"]),
    ("PARTIAL / PHASED ORDERING",       ["one phase", "part of the quote", "multiple phases",
                                         "re-price"]),
    ("payment terms & deposit",         ["deposit", "cleared funds", "payment period", "bacs"]),
    ("price validity",                  ["30 days", "open for acceptance", "validity"]),
    ("making good / builders work",     ["making good", "builders work", "builder's work",
                                         "reinstat"]),
    ("waste & disposal",                ["waste", "disposal", "skip", "removal of"]),
    ("access equipment / scaffold",     ["scaffold", "access equipment", "mewp", "tower"]),
    ("testing & commissioning",         ["commission", "witness test", "handover test"]),
    ("retention of title",              ["retention of title", "remain the property", "title"]),
    ("limitation of liability",         ["limitation of liability", "total liability",
                                         "consequential"]),
    ("insurance",                       ["insur", "indemnit", "indemn"]),
    ("programme / delay liability",     ["delay", "period for completion", "programme",
                                         "lead time"]),
]


def probe(text, pats):
    hits = []
    for p in pats:
        for m in re.finditer(p, text, re.I):
            s = re.sub(r'\s+', ' ', text[max(0, m.start() - 60):m.start() + 110])
            hits.append(s)
            break
    return hits


print("%-34s %-9s %-9s" % ("CATEGORY", "A PLUS", "FENSTER"))
print("-" * 60)
gaps = []
for name, pats in CATEGORIES:
    a = probe(APLUS, pats)
    f = probe(FENSTER, pats)
    print("%-34s %-9s %-9s" % (name, "YES" if a else "-  ", "YES" if f else "-  "))
    if not a and not f:
        gaps.append(name)
    elif not a:
        gaps.append(name + "   (A PLUS SILENT)")

print()
print("NEITHER DOCUMENT, OR A PLUS SILENT:")
for g in gaps:
    print("  ", g)

# -*- coding: utf-8 -*-
"""Re-probe of the 25 categories with CONCEPT-derived wording.

Gordon Court's extension, and it lands squarely on my own v1: the category list
was built from first principles, but the SEARCH PATTERNS were written from A
Plus's clause wording - "one phase", "uncollected", "windload", "mullion",
"spigot", "6399". A first-principles list probed with one supplier's phrasing is
still that supplier's sample. Theirs turned up eight false negatives out of ten
on AFS.

So each category now carries several vocabularies deliberately: A Plus's, the
one AFS used where Gordon Court quoted it, and neutral legal phrasing that
neither drafted. The point of the run is to find where v1 said "silent" and was
wrong, and - separately - where "silent" should have read "in the terms of sale
we do not hold", which is the correction Gordon Court made about BSW and which I
may have made in the opposite direction.
"""
import io
import json
import re

APLUS = io.open('scratchpad/qt51518_full.txt', encoding='utf-8').read()
FENSTER = json.dumps(json.load(io.open('templates/proposal-content.json', encoding='utf-8')))

# (category, v1 patterns (A Plus-derived), v2 additions written from the concept)
CATEGORIES = [
    ("measurement / dimensions",
     ["measurement", "dimension", "site survey", "sizes"],
     ["survey", "as built", "check on site", "verify", "setting out", "tolerance"]),
    ("design intent & suitability",
     ["design responsib", "design intent", "architectural", "interpretation", "fit for", "suitab"],
     ["specification provided", "relies on", "approval of drawings", "sign.?off",
      "purpose for which"]),
    ("Part B / fire & smoke",
     ["part .b", "building regulation", "fire", "smoke"],
     ["statutory", "approved document", "regulations? in force", "compliance with any",
      "BS 9991", "9999"]),
    ("Part L / thermal",
     ["part .l", "u-value", "thermal"],
     ["energy", "conservation of fuel", "SAP", "W/m"]),
    ("Part K / anti-fall",
     ["part .k", "anti-fall", "balustrad", "fall from height"],
     ["guarding", "protection from falling", "restrictor", "opening limit"]),
    ("structural design of openings",
     ["structural opening", "lintel", "forming", "masonry"],
     ["structural", "load.?bearing", "substrate", "adequacy of", "builder.s? work",
      "opening prepared"]),
    ("windload / profile suitability",
     ["windload", "wind load", "6399", "mullion"],
     ["EN 1991", "exposure", "deflection", "structural calculation", "loading"]),
    ("fixings, brackets, spigots",
     ["bracket", "spigot", "fixing lug", "bolts"],
     ["fixings?", "anchors?", "packers?", "method of fixing"]),
    ("performance figures / free area",
     ["free area", "aerodynamic", "geometric", "12101"],
     ["ventilation area", "throat area", "performance data", "declaration of performance"]),
    ("product warranty / guarantee",
     ["warrant", "guarantee", "defect"],
     ["remedy", "replacement", "conform", "merchantab", "satisfactory quality"]),
    ("maintenance & in-use duties",
     ["maintenance", "occupier", "regulatory reform", "in full working order"],
     ["servicing", "upkeep", "responsible person", "periodic"]),
    ("delivery & carriage",
     ["deliver", "ex-works", "ex works", "carriage", "haulier"],
     ["transport", "freight", "risk passes", "INCOTERM", "collection"]),
    ("unloading labour at delivery",
     ["unload", "suitable labour", "offload"],
     ["hard standing", "access for vehicles", "forklift", "crane", "at the delivery point"]),
    ("storage of finished goods",
     ["storage", "uncollected", "materials off site", "off-site"],
     ["store", "warehous", "held at", "deferred delivery", "re.?delivery",
      "not ready to receive"]),
    ("part order / change of quantity or SIZE",
     ["one phase", "part of the quote", "multiple phases", "re-price"],
     # Gordon Court's widening: AFS say "changes made to quantities, sizes or
     # specification". A Plus never use the word "sizes" in that clause at all.
     ["variation", "vary the price", "changes made to", "quantit", "final sum",
      "additional charges", "amend"]),
    ("payment terms & deposit",
     ["deposit", "cleared funds", "payment period", "bacs"],
     ["credit", "invoice", "due date", "interest", "terms of payment"]),
    ("price validity",
     ["30 days", "open for acceptance", "validity"],
     ["subject to confirmation", "expire", "withdraw", "hold the price"]),
    ("making good / builders work",
     ["making good", "builders work", "builder's work", "reinstat"],
     ["patching", "plaster", "render", "decorat", "finishing works", "cutting"]),
    ("waste & disposal",
     ["waste", "disposal", "skip", "removal of"],
     ["rubbish", "packaging", "arisings", "clear away", "clean"]),
    ("access equipment / scaffold",
     ["scaffold", "access equipment", "mewp", "tower"],
     ["working at height", "platform", "hoist", "means of access"]),
    ("testing & commissioning",
     ["commission", "witness test", "handover test"],
     ["test", "certificat", "O&M", "operation and maintenance manual", "demonstrat"]),
    ("retention of title",
     ["retention of title", "remain the property", "title"],
     ["ownership", "property in the goods", "passes to", "vests"]),
    ("limitation of liability",
     ["limitation of liability", "total liability", "consequential"],
     ["liab", "not be liable", "exclude", "loss of profit", "indirect"]),
    ("insurance",
     ["insur", "indemnit", "indemn"],
     ["policy", "cover", "risk", "damage to"]),
    ("programme / delay liability",
     ["delay", "period for completion", "programme", "lead time"],
     ["time of the essence", "commencement", "reasonable timeframe", "force majeure"]),
]


def probe(text, pats):
    out = []
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            out.append((p, re.sub(r'\s+', ' ', text[max(0, m.start() - 70):m.start() + 120])))
    return out


print("%-40s %-11s %-11s" % ("CATEGORY", "A PLUS", "FENSTER"))
print("-" * 66)
changed = []
for name, v1, v2 in CATEGORIES:
    a1, a2 = probe(APLUS, v1), probe(APLUS, v1 + v2)
    f1, f2 = probe(FENSTER, v1), probe(FENSTER, v1 + v2)
    mark = lambda old, new: ("YES" if new else "-") + (" **NEW**" if new and not old else "")
    print("%-40s %-11s %-11s" % (name, mark(a1, a2), mark(f1, f2)))
    if a2 and not a1:
        changed.append(("A PLUS", name, a2[0]))
    if f2 and not f1:
        changed.append(("FENSTER", name, f2[0]))

print()
print("=" * 100)
print("FALSE NEGATIVES IN v1 - categories v1 called silent that the concept probe finds:")
for who, name, (pat, ctx) in changed:
    print("\n  %-8s %s   [matched %r]" % (who, name, pat))
    print("      %s" % ctx[:230])

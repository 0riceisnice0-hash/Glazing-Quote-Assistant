# -*- coding: utf-8 -*-
"""Produce the document cell C31 says accompanies the pricing document.

C31 now reads "read with Fenster Glazing & Locks Ltd's Standard Terms and
Conditions (issue 31.05.2026), a copy of which accompanies this document." That
was not true when it was written - Riverside has no proposal and no T&C output,
so the sentence asserted an attachment that did not exist. Writing an
incorporation by reference and then not producing the document is the same fault
this chat spent two turns criticising in A Plus and BSW.

Provenance checked rather than assumed: templates/proposal-content.json matches
MASTER COVER LETTER 31.05.2026.docx on all seven probes tested, including the
exclusions schedule and the Additional Limitations clause, and the Riverside job
folder holds the 31.05.2026 version. Note there are 131 copies of this letter in
the archive and at least two dates in circulation (29.05 and 31.05).
"""
import io
import json

d = json.load(io.open('templates/proposal-content.json', encoding='utf-8'))

blocks = []


def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get('text'), str):
            blocks.append((o.get('style', ''), o['text']))
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(d)

start = [i for i, (s, t) in enumerate(blocks) if t.strip() == 'TERMS AND CONDITIONS'][0]
terms = [t for s, t in blocks[start:] if t.strip()]

# the INCLUSIONS / EXCLUSIONS table lives in the tables section
tbl = json.dumps(d)
i = tbl.find('Site Welfare')
j = tbl.rfind('General Arrangement and Sectional Drawings', 0, i)
incl = json.loads('"' + tbl[j:i].rsplit('",', 1)[0] + '"') if j > 0 else ''
k = tbl.find('"', i)
excl = json.loads('"' + tbl[i:tbl.find('\\n"', i) + 2] + '"') if i > 0 else ''

out = []
out.append("FENSTER GLAZING & LOCKS LTD")
out.append("STANDARD TERMS AND CONDITIONS, INCLUSIONS AND EXCLUSIONS")
out.append("Issue 31.05.2026")
out.append("")
out.append("Accompanies: Riverside House - Fenster Pricing Document (house format).xlsx")
out.append("Project:     Riverside House, 44 Wedgewood Street, Fairford Leys, Aylesbury HP19 7HL")
out.append("Client:      RRR Group Limited")
out.append("")
out.append("This is the document referred to in the footnote of the pricing document. It must be")
out.append("sent with it. The pricing document on its own does not carry these terms.")
out.append("")
out.append("=" * 88)
out.append("INCLUDED IN THE PRICE")
out.append("=" * 88)
out.append(incl.strip())
out.append("")
out.append("=" * 88)
out.append("EXCLUDED FROM THE PRICE")
out.append("=" * 88)
out.append(excl.strip())
out.append("")
out.append("The pricing document for this project also states, on its face, exclusions specific to")
out.append("these two smoke vents: the AOV control system and its commissioning, testing of the")
out.append("completed smoke ventilation system, Part K anti-fall protection where the cill sits")
out.append("below 1100mm from finished floor level, and the fact that the free area quoted is")
out.append("GEOMETRIC with no aerodynamic figure warranted.")
out.append("")
out.append("=" * 88)
out.append("TERMS AND CONDITIONS")
out.append("=" * 88)
for t in terms[1:]:
    out.append(t.strip())
    out.append("")

P = 'outputs/Riverside House - Fenster Standard Terms and Conditions (to accompany the pricing document).txt'
io.open(P, 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('written: %s  (%d lines)' % (P, len(out)))

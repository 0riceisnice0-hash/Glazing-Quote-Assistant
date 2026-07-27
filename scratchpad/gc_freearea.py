# -*- coding: utf-8 -*-
"""Sweep every PDF in the Gordon Court tender zip for free-area requirements.

Riverside's question: does the pack set a free area, and is it stated as
GEOMETRIC or AERODYNAMIC? Aerodynamic runs ~60-62% of geometric, so a quote
giving one against a spec wanting the other is ~40% out.
"""
import zipfile, io, re, pdfplumber

Z = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/1. Tender Documents/'
     'Gordon Court Windows, Rooflights & Curtain Walling.zip')

PAT = re.compile(
    r'.{0,100}(?:free area|aerodynamic|geometric|Aov|AOV|smoke shaft|smoke vent'
    r'|openable vent|ventilator).{0,120}', re.I)


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


z = zipfile.ZipFile(Z)
pdfs = [n for n in z.namelist() if n.lower().endswith('.pdf')]
print('scanning %d PDFs' % len(pdfs))
for n in pdfs:
    try:
        with pdfplumber.open(io.BytesIO(z.read(n))) as p:
            pages = [(i + 1, ' '.join((pg.extract_text() or '').split()))
                     for i, pg in enumerate(p.pages)]
    except Exception as e:
        print('!! %s  %s' % (n.split('/')[-1][:60], e))
        continue
    hits = []
    for i, t in pages:
        for m in PAT.finditer(t):
            s = ' '.join(m.group(0).split())
            if re.search(r'free area|aerodynamic|geometric', s, re.I):
                hits.append((i, s))
    if hits:
        print('=' * 20, clean(n.split('/')[-1])[:70])
        seen = set()
        for i, s in hits:
            k = s[:70]
            if k in seen:
                continue
            seen.add(k)
            print('   p%-3d %s' % (i, clean(s)[:230]))

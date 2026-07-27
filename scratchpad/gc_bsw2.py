import pdfplumber, os, sys

B = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/2. Supplier Quotes/')


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


f = sys.argv[1]
pgs = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
with pdfplumber.open(B + f) as p:
    for i, pg in enumerate(p.pages):
        if pgs and (i + 1) not in pgs:
            continue
        t = pg.extract_text() or ''
        print('==== page', i + 1)
        print(clean(t))

import pdfplumber, re, os

B = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/2. Supplier Quotes/')

FILES = ['QT252247 PVC.pdf', 'QT252248 PATIIOS.pdf',
         'QT252251 ALI DOORS.pdf', 'QT252257 AOV & LOUVRE.pdf']

KEYS = ['solar', 'g-value', 'g value', 'Suncool', 'SKN', 'Coolite', 'Planitherm',
        'EcoPlus', 'soft coat', 'S Coat', 'low-e', 'lowe', 'argon', 'warm edge',
        'Obs', 'Stippolyte', 'Satin', 'Pattern', 'PAS 24', 'PAS24',
        'trickle', 'restrictor', 'acoustic', 'U-value', 'U value', 'Uw',
        'RAL', 'white', 'grey', 'dual', 'validity', 'valid', 'Total', 'Discount']


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


for f in FILES:
    with pdfplumber.open(B + f) as p:
        pages = [(pg.extract_text() or '') for pg in p.pages]
    t = ' '.join(pages)
    flat = ' '.join(t.split())
    print('=' * 30, clean(f), '| pages', len(pages), '| chars', len(flat))
    print('  KEYWORD COUNTS:', {k: flat.lower().count(k.lower())
                                for k in KEYS if flat.lower().count(k.lower())})
    for m in list(dict.fromkeys(re.findall(r'.{0,45}(?:Grand Total|Total Net|Net Total|Sub Total|Discount|TOTAL).{0,60}', flat)))[:14]:
        print('   $', clean(m))
    print()

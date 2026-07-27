import pdfplumber, re, os

B = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/1. Tender Documents/Gordon Court/')

FILES = ['5244-ARK-52001_-_Window Types - Replacement Windows.pdf',
         '5244-ARK-52002_-_Window Schedule - Replacement Windows.pdf',
         '5244-ARK-52003_-_Window Types & Schedule - New Windows.pdf']

KEYS = ['8000', '4000', '5000', '6000', 'trickle', 'Trickle', 'Linkvent', 'Passivent',
        'AL-dB', 'acoustic', 'Acoustic', 'PAS 24', 'PAS24', 'G-Value', 'g-value',
        'G Value', '0.36', '1.1', '1.4', '1.6', 'restrictor', 'Restrictor',
        'Secured by Design', 'SBD', 'obscure', 'Obscure', 'toughened']


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


for f in FILES:
    with pdfplumber.open(B + f) as p:
        t = ' '.join((pg.extract_text() or '') for pg in p.pages)
    flat = ' '.join(t.split())
    print('=' * 30, clean(os.path.basename(f))[:60], '| chars', len(flat))
    print('   counts:', {k: flat.count(k) for k in KEYS if flat.count(k)})
    for pat in [r'.{0,80}(?:VENTILATION|Trickle|trickle|Linkvent|Passivent).{0,120}',
                r'.{0,60}(?:PAS ?24|G-Value|G Value|Grand total).{0,80}']:
        for h in list(dict.fromkeys(re.findall(pat, flat)))[:6]:
            print('    *', clean(h)[:230])
    print()

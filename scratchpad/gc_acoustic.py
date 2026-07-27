import pdfplumber, sys, os

B = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/1. Tender Documents/Gordon Court/')


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


f = sys.argv[1]
with pdfplumber.open(B + f) as p:
    pg = p.pages[0]
    words = pg.extract_words()

# Find the header words to establish column x-centres
hdr = [w for w in words if w['text'] in ('Toughened', 'Restrictors', 'Removable', 'Acoustic', 'Trickle', 'Vents', 'Primary', 'Opening')]
print('HEADER TOKENS (x0, top, text):')
for w in sorted(hdr, key=lambda w: (round(w['top']), w['x0'])):
    print('   %8.1f %8.1f %s' % (w['x0'], w['top'], clean(w['text'])))

# Rows: group by y
rows = {}
for w in words:
    rows.setdefault(round(w['top'] / 3), []).append(w)

print()
print('ROWS starting with a window type tag (WE_/WN_/WL_), showing Yes x-positions:')
n_rows = 0
for k in sorted(rows):
    line = sorted(rows[k], key=lambda w: w['x0'])
    tags = [w for w in line if w['text'].startswith(('WE_', 'WN_', 'WL_'))]
    yeses = [w for w in line if w['text'] == 'Yes']
    if tags and yeses:
        n_rows += 1
        print('  %-8s | Yes at x: %s' % (clean(tags[0]['text']),
                                        ' '.join('%.0f' % w['x0'] for w in yeses)))
print('rows with tag+Yes:', n_rows)

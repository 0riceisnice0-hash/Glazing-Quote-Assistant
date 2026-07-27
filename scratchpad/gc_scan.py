import pdfplumber, re, sys, os

D = os.path.join(os.path.dirname(__file__), 'gc-zip')


def clean(s):
    return s.encode('ascii', 'replace').decode('ascii')


def grab(fname, pats, limit=10):
    path = os.path.join(D, fname)
    with pdfplumber.open(path) as p:
        t = ' '.join((pg.extract_text() or '') for pg in p.pages)
    t = ' '.join(t.split())
    print('=' * 25, clean(fname), 'chars', len(t))
    for label, pat in pats.items():
        hits = list(dict.fromkeys(re.findall(pat, t)))[:limit]
        if hits:
            print('  ---', label)
            for h in hits:
                print('    *', clean(h)[:260])
    return t


if __name__ == '__main__':
    pats = {
        'U-value': r'.{70}[Uu][\s-]?value.{110}',
        'g-value': r'.{50}[Gg][\s-]?value.{90}',
        'validity': r'.{60}valid.{110}',
        'Wm2K': r'.{90}W/m.{0,4}K.{60}',
    }
    for f in sys.argv[1:]:
        grab(f, pats)

import pdfplumber, openpyxl, re, collections

B = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
     'Chigwell (London) PLC/Gordon Court/1. Estimating/')
SCH = B + '1. Tender Documents/Gordon Court/5244-ARK-51001_01_External and Communal Door Schedule.pdf'
WB = B + '3. Client Quote/Chigwell Group - Gordon Court Pricing DO NOT SEND.xlsx'


def clean(s):
    return str(s).encode('ascii', 'replace').decode('ascii')


# ---- schedule 51001: every row that starts with a D_ type tag
with pdfplumber.open(SCH) as p:
    words = p.pages[0].extract_words()
rows = collections.defaultdict(list)
for w in words:
    rows[round(w['top'] / 3)].append(w)

types = collections.Counter()
detail = collections.defaultdict(list)
for k in sorted(rows):
    line = sorted(rows[k], key=lambda w: w['x0'])
    txt = ' '.join(w['text'] for w in line)
    # a data row: tag followed by more than just the tag
    for mt in re.finditer(r'\b(D_[A-Z])\b', txt):
        tag = mt.group(1)
        rest = txt[mt.end():mt.end() + 130]
        # only count rows carrying dimensions (data rows, not legend/heading)
        if re.search(r'\bL\s*\d', rest) and re.search(r'\d{4}', rest):
            types[tag] += 1
            detail[tag].append(' '.join(rest.split())[:110])

print('=== SCHEDULE 51001 door types (data rows counted) ===')
ext = 0
for t in sorted(types):
    sample = detail[t][0]
    kind = ('EXTERNAL' if 'External' in ' '.join(detail[t]) else
            ('INTERNAL' if 'Internal' in ' '.join(detail[t]) else '*** INT/EXT NOT STATED ***'))
    fr = 'FD60S' if 'FD60S' in sample else ('FD30S' if 'FD30S' in sample else ('FD30' if 'FD30' in sample else 'no rating'))
    print('  %-5s x%-3d %-26s %-10s | %s' % (t, types[t], kind, fr, clean(sample)))
    if kind == 'EXTERNAL':
        ext += types[t]
print('  total data rows: %d   (schedule states Grand total: 116)' % sum(types.values()))
print('  of which marked External: %d' % ext)

# ---- workbook: what we priced
wb = openpyxl.load_workbook(WB, data_only=True).worksheets[0]
print()
print('=== WORKBOOK door lines (rows 44-59) ===')
sold = collections.Counter()
for r in range(44, 60):
    code, ref, size, qty = (wb['B%d' % r].value, wb['C%d' % r].value,
                            wb['E%d' % r].value, wb['F%d' % r].value)
    if code and ref:
        sold[str(ref)] += qty or 0
        print('  r%-3d %-5s %-6s %-14s qty %s' % (r, code, clean(ref), clean(size), qty))

print()
print('=== D_ TYPES IN SCHEDULE vs PRICED ===')
for t in sorted(set(list(types) + [k for k in sold if k.startswith('D_')])):
    s = types.get(t, 0)
    p_ = sold.get(t, 0)
    kinds = ' '.join(detail.get(t, []))
    kind = 'EXTERNAL' if 'External' in kinds else ('INTERNAL' if 'Internal' in kinds else 'NOT STATED')
    mark = ''
    if kind != 'INTERNAL' and p_ == 0 and s:
        mark = '   <<< IN SCHEDULE, NOT PRICED'
    if p_ and not s:
        mark = '   <<< PRICED, NOT IN SCHEDULE'
    print('  %-5s schedule %-3d priced %-4s %-11s%s' % (t, s, p_, kind, mark))

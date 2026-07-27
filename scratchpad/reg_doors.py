import json
d = json.load(open('data/supplier-rates.json', encoding='utf-8'))
r = d['register']
print(len(r), 'entries; sample keys:', list(r[0].keys()))
print(json.dumps(r[0], indent=1)[:600])
print('=== categories containing door ===')
for e in r:
    c = str(e.get('category', ''))
    if 'door' in c.lower():
        print(e.get('supplier'), '|', c, '|', {k: e.get(k) for k in e if k not in ('category', 'supplier')})

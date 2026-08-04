import json, sys
sys.path.insert(0, 'scripts')
import crm
d = crm.company_detail('excel-hoardings')
print(json.dumps(d, indent=1)[:7000])
for l in (d.get('leads') or []):
    print('=== LEAD DETAIL', l['key'])
    print(json.dumps(crm.lead_detail(l['key']), indent=1)[:7000])

# -*- coding: utf-8 -*-
"""Encode the Gordon Court delivery terms now that 'never' free is expressible."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'job-checks', 'gordon-court.json')
m = json.load(io.open(P, encoding='utf-8'))

for t in m['delivery_terms']:
    t['free_delivery_threshold'] = "never"
    if t['supplier'].startswith('BSW'):
        t['charge_basis'] = ("'All estimates are ex works, additional delivery charges may apply' - no "
                             "rate, no threshold and no distance rule stated on any of the four quotes")
        t['delivery_priced'] = False
    else:
        t['charge_basis'] = ("Q7585 p7 optional extra 'Delivery 1 Pcs GBP 250.00'; T&C 8.1 puts "
                             "packaging, insurance and transport on the Customer 'in addition'")
        t['delivery_priced'] = False

json.dump(m, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('delivery_terms encoded as never-free for both suppliers')

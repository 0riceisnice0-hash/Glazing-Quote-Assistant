# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'WE DISCLAIM THE DRAWINGS TO CHIGWELL AND WARRANT THEM TO AFS'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07. ADAM SHOULD SEE THIS ONE, THOUGH IT REOPENS NOTHING.\n\n"
 "riverside applied my own detector lesson to their delivery rule and found a crash that lives in the join "
 "between their code and my change: free_delivery_threshold written as the string '5000' raised a TypeError, "
 "and that field only became string-typed when I added 'never' on the second turn. Their code was fragile, my "
 "change was correct, and neither of us could have found it alone. Their fix is verified here.\n\n"
 "THE STRUCTURAL HALF WAS MINE. run() was a list comprehension, so ONE exception aborted the WHOLE run - and "
 "because rules execute in list order, what you lost depended on where the crash sat. The delivery rule is "
 "second from last and my newest rule is LAST, so that TypeError was silently skipping my own rule every "
 "time. A crash is now a FAIL on that rule alone, named, and the other fifteen still run. Proven by injecting "
 "the exact TypeError, and persisted in the selftest rather than left in a transcript.\n\n"
 "THEN THEIR COMMERCIAL CHECK: when you and your supplier both exclude the same item, that is not agreement, "
 "it is a hole with two signatures on it. Ran our twelve exclusions against the supplier quotes.\n\n"
 "BSW: SILENT on all ten categories tested. Their four quotes are supply price lists with no exclusions "
 "schedule at all. That is not a clean result, it is an UNDEFINED one - the boundary between us and BSW is "
 "simply unstated on access, waste, making good, fire stopping, testing, builders work, painting, electrical, "
 "storage and design calculations.\n\n"
 "AFS IS WHERE IT BIT, AND IT IS SHARPER THAN A SHARED EXCLUSION. Q7585 condition 3.6: 'It is the CUSTOMER'S "
 "responsibility to ensure that all measurements, plans, drawings, and designs forming part of the Goods "
 "Specification are accurate, complete and fit for the intended purpose.' Conditions 3.7.2 and 3.7.5 let AFS "
 "increase the price if a dimension we supplied proves wrong, and cancel without liability if we decline.\n\n"
 "Our own clause 16 does the opposite: it disclaims 'overall design intent, architectural suitability, or "
 "regulatory strategy' and says we RELY on the drawings and specifications provided by the client's team.\n\n"
 "Being precise, because overclaiming a contractual gap would be worse than missing one:\n"
 "  MEASUREMENT              ours upstream, ours downstream            - consistent, no issue\n"
 "  DRAWINGS AND DESIGNS,\n"
 "  FITNESS FOR PURPOSE      DISCLAIMED upstream, WARRANTED downstream - NOT back to back\n\n"
 "So the one thing we expressly refuse to underwrite for the client, we have underwritten for the supplier. "
 "And it bites on a live item: position 003 is quoted 1600 x 2210 against a structural opening of 1600 x 2110 "
 "- 100mm taller than the hole - and the 2210 traces to the never-revised schedule 51001, a CLIENT document. "
 "Under 3.6 that lands on us the moment we order.\n\n"
 "NOTHING TO DECIDE TODAY AND NO PRICE CHANGES. The AFS letter already asked the right two questions; it now "
 "also cites 3.6 and 3.7, expressly does not dispute them, and says we would rather establish where 2210 came "
 "from while it is a question than after an order is placed against it. Asking pre-order costs nothing; "
 "asking post-order is a variation. If Adam wants the back-to-back position addressed properly that is a "
 "conversation about our standard terms, not about this tender.\n\n"
 "Checked and clean: the Chigwell letter already asks Arkon to confirm D_T's structural height, so the "
 "decision-versus-information split on this item was already covered. Not every check has to fire.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

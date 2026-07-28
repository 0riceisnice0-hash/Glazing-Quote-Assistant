# -*- coding: utf-8 -*-
"""Append this turn's finding to the Riverside hub entry."""
import collections
import io
import json

P = 'data/dashboard-state.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

ADD = (
    " *** 28/07, A PLUS'S CONDITIONS PUT PART B ON US AND OUR OWN TERMS DISCLAIM IT TO THE "
    "CLIENT. *** Reading page 3 of QT51518 for responsibility rather than price - a page of this "
    "quote never read before tonight. A Plus's Product Performance clause: \"It is the "
    "responsibility of the Customer to ensure all building regulations (i.e. Part 'B', 'F', 'L', "
    "'M' & 'N'...) are adhered to. The Supplier does not warrant or represent that any Product "
    "supplied shall comply... unless where expressly stated to the contrary by the Supplier.\" "
    "Fenster's clause 16 does the opposite - it disclaims regulatory strategy and relies on the "
    "client's professional team. NEITHER DOCUMENT IS WRONG ON ITS OWN; the exposure lives only "
    "between them. It matters here because PART B IS NOT AN INCIDENTAL ATTRIBUTE OF AN AOV SMOKE "
    "VENT - IT IS THE ENTIRE FUNCTION OF THE PRODUCT, so the one regulation it exists to satisfy "
    "is the one disclaimed upstream and accepted downstream. It bites on the question already "
    "open: if the 1 m2 is aerodynamic, 1.30 m2 geometric gives about 0.78-0.81 m2 and the "
    "shortfall is ours. THE REMEDY IS FREE AND PRE-ORDER: the clause says 'unless expressly "
    "stated to the contrary by the Supplier', so RFQ items 1 and 4 now ask A Plus to state the "
    "aerodynamic free area, the EN 12101-2 class and the whole-window Uw ON THE REVISED "
    "QUOTATION rather than in a reply - an express statement by the Supplier is what the clause "
    "turns on. Asking costs a line before an order and is a variation after one. THREE MORE FROM "
    "THE SAME READ: (1) 'the output free area values do not allow for any obstructions, side "
    "walls, reveals or neighbouring vents' - the 1.30 m2 is a BARE-VENT figure and both vents sit "
    "in a reveal on a 155mm subcill, the first thing found that could erode the geometric margin "
    "itself; (2) A Plus assume a 1200Pa design windload, disclaim their own calculations and put "
    "the BS 6399-2 check and the bracket/spigot calculations on us - and no structural engineer "
    "is named on any drawing, so on a second floor elevation NOBODY IS APPOINTED TO DO EITHER; "
    "(3) the quotation incorporates a 'Terms of Sale Revision V.01.2 - 08.01.2018' and takes its "
    "definitions from 'Revision V.01 - 03.11.2017', and WE HOLD NEITHER - six files in the whole "
    "Commercial archive have 'Terms of Sale' in the name and all six are the same Advisory Notes "
    "summary, so the contract we would order under has never been read here on any job. RFQ now "
    "12 items; RRR question 5 extended. New rule check_incorporated_terms_held shipped with its "
    "29 variants written BEFORE it, not after. Checks 0 failed, 4 questions. Position unchanged: "
    "GBP 5,990.22, unissued, nothing sent."
)

hit = 0
for j in d.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
if hit != 1:
    raise SystemExit('expected exactly one Riverside job entry, found %d' % hit)

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub updated')

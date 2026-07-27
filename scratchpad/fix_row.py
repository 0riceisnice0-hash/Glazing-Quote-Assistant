# -*- coding: utf-8 -*-
import io

P = 'MARY-HANDOVER.md'
lines = io.open(P, encoding='utf-8').read().split('\n')

row = (
    '| **Princess Beatrice House (Guildmore/RBKC)** | '
    '**QUOTE ISSUED 27/07 09:49 to jason.mount@guildmore.com - GBP279,244.69 ex VAT** '
    '(Adam 27/07 08:56: "proceed with sending this out with the discount"). '
    'Mary re-audited the sent pack: arithmetic exact - 46 line rows / 217 units = GBP233,091.68 + install GBP39,680 '
    '+ mastic GBP5,356.22 + EPDM GBP8,276.91 = subtotal GBP286,404.81, less 2.5% MCD GBP7,160.12 = GBP279,244.69. '
    'Base GBP272,771.68 unchanged from the 23/07 audit, so Adam\'s two instructions (EPDM+mastic into the main quote; '
    'add 2.5% MCD) were both actioned. **THREE CONTRADICTIONS WENT OUT WITH IT:** '
    '(1) proposal p3 still reads "External mastic is charged as an optional extra" while the pricing charges GBP5,356.22 '
    'for it, and EPDM is not in the clarifications at all - GBP13,633.13 charged in one document and disclaimed in the other; '
    '(2) proposal p3 says "The external door package is based on Technal STII" while the pricing heads Door Types 1-5 '
    '"Modeal Complex Coupled Doors" - still NO formal alternative-system qualification; '
    '(3) the "Window and Door Drawings.pdf" we attached carries "ITEMS GLAZED WITH PANELS HAVE NOT BEEN TESTED TO PAS24" '
    'on 5 pages (2,3,4,5,58) against a Part Q/SBD Silver ITT while the proposal claims PAS24. '
    'MCD note: taken as a straight deduction off the bottom so it comes off margin - neutral would have needed subtotal '
    'GBP293,748.52; Adam approved the method when Gintare asked, so not logged as an error. '
    'Drawings pack checked for leaked supplier prices - none found. Issued 10 days after the 17/07 return date. '
    '*(23/07 audit history, still valid: 191/191 window units verified vs BPG T02 schedules; install GBP39,680 recomputes '
    'from labour codes; Technal screens match Aplus Logikal penny-for-penny; both Aplus quotes current 21-22/07/2026 - the '
    'QT39795 letter in the pack is LAST YEAR\'s. Open items from that audit: 3nr Louvre Type 01 + 2nr 2280x1068 Door Type 1 '
    'side screens still unpriced and unexcluded (~GBP3.5-5.5k sell) - there is no louvre line anywhere in the pricing or the '
    'drawings, while the proposal hedges "louvre / panel elements where quoted"; GBP668.41 Aplus cost uncarried; heights '
    'deviate from T02 (Type 3 960 vs 1135, Type 6 1375 vs 1160); 76 obscure entries vs obscure splits only on Types 5/6/7; '
    'bill item AA (uPVC variance + lead-ins) unanswered. Workbook `test-results\\princess-beatrice\\Princess Beatrice House '
    '- Take-Off & Tender Audit.xlsx`.)* | '
    '**REQ-6 open:** reissue a corrected proposal to Guildmore now, or wait to be queried? '
    'Also still open from 23/07: formal Technal/Modeal qualification + CA approval; louvre scope price-or-exclude; '
    'confirm obscure coverage with Aplus. |'
)

assert lines[85].startswith('| **Princess Beatrice House'), lines[85][:60]
lines[85] = row
io.open(P, 'w', encoding='utf-8').write('\n'.join(lines))
print('row cells:', lines[85].count('|'))
print('ok')

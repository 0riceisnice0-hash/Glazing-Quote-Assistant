import openpyxl

BASE = ('C:/Users/zacpl/OneDrive - Fenster Glazing (1)/Commercial/1. Tender Documents/'
        'Chigwell (London) PLC/Gordon Court/1. Estimating/3. Client Quote/')
INT = BASE + 'Chigwell Group - Gordon Court Pricing DO NOT SEND.xlsx'


def clean(s):
    return str(s).encode('ascii', 'replace').decode('ascii')


wbf = openpyxl.load_workbook(INT, data_only=False)
wbv = openpyxl.load_workbook(INT, data_only=True)
wsf, wsv = wbf.worksheets[0], wbv.worksheets[0]

print('=== I61 INSTALLATION formula ===')
f = wsf['I61'].value
print(clean(getattr(f, 'text', f)))
print()
print('=== I67 MASTIC / I68 EPDM formulas ===')
for c in ('I67', 'I68'):
    f = wsf[c].value
    print(c, clean(getattr(f, 'text', f))[:400])
print()

print('=== line-by-line: code, ref, qty, J(cost), R(supplier qtd), I(sell) ===')
tot_j = tot_r = 0.0
noR = []
for r in range(10, 60):
    code = wsv['B%d' % r].value
    ref = wsv['C%d' % r].value
    qty = wsv['F%d' % r].value
    J = wsv['J%d' % r].value
    R = wsv['R%d' % r].value
    I = wsv['I%d' % r].value
    if not code:
        continue
    jn = J if isinstance(J, (int, float)) else 0
    rn = R if isinstance(R, (int, float)) else 0
    q = qty if isinstance(qty, (int, float)) else 0
    tot_j += jn * q
    tot_r += rn
    flag = ''
    if not isinstance(R, (int, float)):
        flag = '  <<< NO SUPPLIER LINE (R blank)'
        noR.append((r, ref, q, jn * q, I))
    print('r%-3d %-5s %-7s qty=%-3s J=%-10.2f Jxqty=%-11.2f R=%-11.2f I=%-11.2f%s'
          % (r, clean(code), clean(ref), q, jn, jn * q, rn, I if isinstance(I, (int, float)) else 0, flag))

print()
print('SUM of J x qty  (cost carried in workbook) = %.2f' % tot_j)
print('SUM of R        (supplier quoted amounts)  = %.2f' % tot_r)
print('M5 memo (BSW 182787.76 + AFS 18298.94)     = %.2f' % wsv['M5'].value)
print()
print('LINES WITH NO SUPPLIER QUOTE AMOUNT (R blank):')
sub = 0
for r, ref, q, jq, I in noR:
    sub += jq
    print('   row %-3d %-7s qty %-3s cost %10.2f  sell %s' % (r, clean(ref), q, jq, clean(I)))
print('   total cost with no supplier line: %.2f' % sub)

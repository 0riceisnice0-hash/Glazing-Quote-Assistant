import os
q=r"test-results\mary-inbox\queue"
out=os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att")
import openpyxl
wb=openpyxl.load_workbook(os.path.join(out,"SMD - Brocks Hill Phase 2 Teaching Block Pricing.xlsx"),data_only=True)
for ws in wb.worksheets:
    print("="*90); print("SHEET:",ws.title,ws.dimensions)
    for row in ws.iter_rows():
        vals=[]
        for c in row:
            v=c.value
            if v is None: continue
            if isinstance(v,float): v=round(v,2)
            vals.append(f"{c.coordinate}={v}")
        if vals: print(" | ".join(vals)[:400])

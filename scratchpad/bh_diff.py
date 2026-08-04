import os,openpyxl
q=r"test-results\mary-inbox\queue"
paths={
 "14:21 to Adam (placeholder)":os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtQAAAA__-att","SMD - Brocks Hill Phase 2 Teaching Block Pricing.xlsx"),
 "14:41 to Adam (all updated)":os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtgAAAA__-att","SMD - Brocks Hill Phase 2 Teaching Block Pricing.xlsx"),
 "15:12 SENT TO MARTIN":os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att","SMD - Brocks Hill Phase 2 Teaching Block Pricing.xlsx"),
}
grab={}
for lbl,p in paths.items():
    if not os.path.exists(p): print("MISSING:",lbl); continue
    ws=openpyxl.load_workbook(p,data_only=True).worksheets[0]
    d={}
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None: d[c.coordinate]=c.value
    grab[lbl]=d
    print(f"{lbl}: {os.path.getsize(p):,} bytes, {len(d)} cells")
keys=sorted(set().union(*[set(d) for d in grab.values()]),key=lambda k:(int(''.join(ch for ch in k if ch.isdigit())),k))
print("\n%-14s %-34s %-34s %-34s"%("CELL","14:21","14:41","15:12 SENT"))
for k in keys:
    vs=[grab[l].get(k) for l in paths if l in grab]
    if len(set(str(v) for v in vs))>1:
        print("%-14s %-34s %-34s %-34s"%(k,*[str(v)[:33] for v in vs]))

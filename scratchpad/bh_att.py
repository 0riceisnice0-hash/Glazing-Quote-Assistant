import os,glob
q=r"test-results\mary-inbox\queue"
for f in ["fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMSif1IAAA_-att","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtgAAAA__-att","20260730T1242-rnegAAAA-att"]:
    p=os.path.join(q,f)
    print("="*80); print(f)
    if not os.path.isdir(p): print("  NO FOLDER"); continue
    for n in sorted(os.listdir(p)):
        fp=os.path.join(p,n)
        if n.lower().endswith((".png",".jpg",".gif")): continue
        print(f"  {os.path.getsize(fp):>10,}  {n}")

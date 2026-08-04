import json,os,glob
q=r"test-results\mary-inbox\queue"
names=["20260730T1052-qOqQAAAA","20260730T1056-qOqgAAAA","20260730T1106-qOqwAAAA","20260730T1114-qOrQAAAA","20260730T1238-rneQAAAA","20260730T1242-rnegAAAA","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtQAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtgAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonPywAAAA__","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMSif1IAAA_","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMUmqISAAA_","20260730T1053-rndQAAAA","20260730T1102-rndgAAAA","20260730T1111-qOrAAAAA"]
for n in names:
    p=os.path.join(q,n+".json")
    if not os.path.exists(p):
        print("MISSING",n); continue
    d=json.load(open(p,encoding="utf-8"))
    print("="*100)
    print(n)
    for k in ("received_at","from","to","cc","subject","mailbox","trusted_sender"):
        if d.get(k): print(f"  {k}: {d[k]}")
    at=d.get("attachments") or []
    if at: print("  attachments:",[a.get("name") if isinstance(a,dict) else a for a in at])
    b=(d.get("body") or d.get("body_text") or "")
    print("-"*60)
    print(b[:4000])

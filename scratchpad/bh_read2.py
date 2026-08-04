import json,os,re
q=r"test-results\mary-inbox\queue"
names=["20260730T1052-qOqQAAAA","20260730T1056-qOqgAAAA","20260730T1106-qOqwAAAA","20260730T1114-qOrQAAAA","20260730T1238-rneQAAAA","20260730T1242-rnegAAAA","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtQAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtgAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonPywAAAA__","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMSif1IAAA_","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMUmqISAAA_","20260730T1053-rndQAAAA","20260730T1102-rndgAAAA","20260730T1111-qOrAAAAA"]
def trim(b):
    for pat in [r"\n\s*Kind regards", r"\n\s*Many thanks", r"\n\s*Thanks,", r"\n\s*Best regards", r"\n\s*From:", r"\n\s*Regards"]:
        m=re.search(pat,b)
        if m: b=b[:m.start()]
    return b.strip()
for n in names:
    p=os.path.join(q,n+".json")
    d=json.load(open(p,encoding="utf-8"))
    print("="*90)
    print(n,"|",d.get("received_at"),"|",d.get("from"),"->",d.get("to"))
    print("SUBJ:",d.get("subject"))
    at=d.get("attachments") or []
    if at: print("ATT:",[a.get("name") if isinstance(a,dict) else a for a in at])
    b=trim(d.get("body") or d.get("body_text") or "")
    print(b[:1800])

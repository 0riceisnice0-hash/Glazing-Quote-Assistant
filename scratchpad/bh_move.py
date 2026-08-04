import os,shutil,sys
sys.stdout.reconfigure(encoding="utf-8")
q=r"test-results\mary-inbox\queue"; pr=r"test-results\mary-inbox\processed"
os.makedirs(pr,exist_ok=True)
names=["20260730T1052-qOqQAAAA","20260730T1056-qOqgAAAA","20260730T1106-qOqwAAAA","20260730T1114-qOrQAAAA","20260730T1238-rneQAAAA","20260730T1242-rnegAAAA","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtQAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtgAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__","fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonPywAAAA__","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMSif1IAAA_","fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMUmqISAAA_","20260730T1053-rndQAAAA","20260730T1102-rndgAAAA","20260730T1111-qOrAAAAA"]
moved=0
for n in names:
    for suffix in (".json","-att"):
        s=os.path.join(q,n+suffix); dst=os.path.join(pr,n+suffix)
        if os.path.exists(s):
            if os.path.exists(dst): shutil.rmtree(dst) if os.path.isdir(dst) else os.remove(dst)
            shutil.move(s,dst); moved+=1
print("moved",moved,"items")
left=[f for f in os.listdir(q) if f.endswith(".json")]
print("still in queue:",len(left))

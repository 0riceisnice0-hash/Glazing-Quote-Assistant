import json,sys
sys.stdout.reconfigure(encoding="utf-8")
d=json.load(open("data/dashboard-state.json",encoding="utf-8"))
reqs=d.get("requests",[])
print("total requests:",len(reqs))
for r in reqs:
    blob=json.dumps(r).lower()
    if "brocks" in blob or "brock" in blob:
        print("-"*70)
        print(r.get("id"),"|",r.get("status"),"|",r.get("job"),"|",r.get("deadline"))
        print("  TITLE:",str(r.get("title"))[:150])
        print("  NEEDS:",str(r.get("needs"))[:200])
print("="*70)
print("OPEN (any job):",sum(1 for r in reqs if r.get("status")!="answered"))

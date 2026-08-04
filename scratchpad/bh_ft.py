import json,re,sys
sys.stdout.reconfigure(encoding="utf-8")
src=open("scripts/mary_checks.py",encoding="utf-8").read()
i=src.find("def selftest")
print(src[i:i+1500] if i>0 else "no selftest")
print("#"*70)
d=json.load(open("data/job-checks/_test-brocks-hill.json",encoding="utf-8"))
print("FIXTURE KEYS:",list(d.keys()))
print("expect:",json.dumps(d.get("_expect"),indent=1)[:800])

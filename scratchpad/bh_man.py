import json,sys
sys.stdout.reconfigure(encoding="utf-8")
d=json.load(open("data/job-checks/brocks-hill-phase-2.json",encoding="utf-8"))
print("KEYS:",[k for k in d])
print("DOORS:",json.dumps(d.get("doors"),indent=1)[:1500])
print("QUANTITIES:",json.dumps(d.get("quantities"),indent=1)[:900])

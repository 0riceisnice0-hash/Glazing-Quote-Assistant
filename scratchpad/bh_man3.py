import json,sys
sys.stdout.reconfigure(encoding="utf-8")
p="data/job-checks/brocks-hill-phase-2.json"
d=json.load(open(p,encoding="utf-8"))
print("FABRICATOR SAMPLE:",json.dumps(d.get("systems_specified"),indent=1)[:900])
print("---SPEC ITEM SAMPLE---")
for s in d.get("spec_items",[])[:3]: print(json.dumps(s,indent=1))
for s in d.get("spec_items",[]):
    if "E.01" in json.dumps(s) or "E.03" in json.dumps(s): print("MATCH:",json.dumps(s)[:300])

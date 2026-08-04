import json,sys,io
sys.stdout.reconfigure(encoding="utf-8")
p="data/calibration.json"
d=json.load(open(p,encoding="utf-8"))
entries = d if isinstance(d,list) else d.get("entries",d.get("calibration",[]))
print("type:",type(d).__name__,"n=",len(entries))
print(json.dumps(entries[-1],indent=1)[:1200])

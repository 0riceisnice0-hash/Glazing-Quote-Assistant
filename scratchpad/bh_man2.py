import json,sys
sys.stdout.reconfigure(encoding="utf-8")
p="data/job-checks/brocks-hill-phase-2.json"
d=json.load(open(p,encoding="utf-8"))

# 1. Strongdor SQ218594 prices panic gear on all 5 Type E.01 steel doors:
#    "3 point touchbar panic bolt", "2 point panic latch", rebound panels, escape signage.
n=0
for door in d["doors"]:
    if "Type E.01 steel sports hall escape door" in door["ref"]:
        door["panic_hardware_priced"]=True
        door["ref"]+=" [Strongdor SQ218594 31/07: 3pt touchbar panic bolt + 2pt panic latch + escape signage]"
        n+=1
print("panic hardware set true on",n,"steel doors")

# 2. SMD instructed inclusion in writing 30/07 11:14 - "Include for the additional doors."
#    The bill said 0; the instruction supersedes it. Record the resolution on the ref.
for q in d["quantities"]:
    if "Door Type E.01 1810x2110 steel" in q["ref"]:
        q["bill_qty"]=5; q["ref"]+=" [bill said 0; SMD instructed inclusion in writing 30/07 11:14]"
    if "Door Type E.03" in q["ref"] and q.get("bill_qty")==0:
        q["bill_qty"]=q["drawing_qty"]; q["ref"]+=" [bill said 0; SMD instructed inclusion in writing 30/07 11:14]"

# 3. The row-by-row uplift check, as issued to SMD on 31/07.
d["priced_rows"]=[
 {"ref":"Door Type E.02 1010x2110","code":"SAD","qty":1,"supply_each":2589.1085,"sell_each":3489.1085},
 {"ref":"Door Type E.04 1810x2110","code":"DAD","qty":2,"supply_each":2878.661,"sell_each":4378.661},
 {"ref":"(Door) Window Type E.01, E.03 1800x2110","code":"SAD","qty":4,"supply_each":3137.9195,"sell_each":4037.9195},
 {"ref":"Door Type E.03 louvred 1810x2110","code":"DAD","qty":2,"supply_each":2940.5155,"sell_each":4440.5155},
 {"ref":"Door Type E.01 STEEL 1810x2110 (Strongdor)","code":"DAD","qty":5,"supply_each":2637.01,"sell_each":2728.81,"additional_each":91.80},
 {"ref":"Window Type E.02 1800x2100","code":"ELAW","qty":23,"supply_each":1362.57,"sell_each":2000.07},
 {"ref":"Window Type E.04 1800x2400","code":"ELAW","qty":4,"supply_each":1098.90,"sell_each":1736.40},
 {"ref":"Window Type E.05 1000x2100","code":"LAW","qty":2,"supply_each":620.49,"sell_each":1107.99},
 {"ref":"Window Type E.06 1800x2100","code":"ELAW","qty":1,"supply_each":984.64,"sell_each":1622.14},
]
d["_source"]=d.get("_source","")+" | 04/08/2026: rebuilt against the document ACTUALLY ISSUED to SMD 31/07/2026 15:12 (GBP 118,278.52)."
json.dump(d,open(p,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

# fixture too, so the founding case is replayable
fp="data/job-checks/_test-brocks-hill.json"
f=json.load(open(fp,encoding="utf-8"))
f["priced_rows"]=d["priced_rows"]
json.dump(f,open(fp,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("manifest + fixture updated")

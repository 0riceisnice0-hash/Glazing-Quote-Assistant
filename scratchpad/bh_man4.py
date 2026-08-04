import json,sys
sys.stdout.reconfigure(encoding="utf-8")
p="data/job-checks/brocks-hill-phase-2.json"
d=json.load(open(p,encoding="utf-8"))
for s in d["systems_specified"]:
    if "Strongdor Sportsdor" in s["system"]:
        s["fabricator"]="Strongdor Ltd - SQ218594 31/07/2026, 5no Steeldor double external 1810x2110 RAL7016, GBP 2,637.01 ea + GBP 459.00 delivery"
    if "louvred doorset" in s["system"]:
        s["fabricator"]="BSW Window Solutions - louvre added to enquiry 30/07 12:38, priced in the issued document at GBP 2,940.52 supply ea"
for s in d["spec_items"]:
    if s["ref"].startswith("Door Type E.01 - 5no steel"):
        s["treatment"]="priced"; s["ref"]+=" [Strongdor SQ218594, in the issued document at GBP 2,728.81 sell ea - SOLID, no vision panel, U-value NPD, deviation NOT yet qualified to SMD]"
    if s["ref"].startswith("Door Type E.03 - 2no aluminium louvred"):
        s["treatment"]="priced"; s["ref"]+=" [BSW, in the issued document at GBP 4,440.52 sell ea]"
json.dump(d,open(p,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("updated")

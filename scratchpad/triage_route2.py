# -*- coding: utf-8 -*-
"""Route the three new jobs' work orders to their fresh chats."""
import json, io, os, glob

Q = "test-results/mary-inbox/queue"
ROUTE = {
    "20260730T0726-qOow": "totteridge", "20260730T0905-qOpQ": "totteridge",
    "20260730T0912-qOpg": "totteridge", "20260730T0939-qOpw": "totteridge",
    "20260730T0951-rncw": "totteridge",
    "Eomc4Q": "addison-ave", "FSkLZA": "addison-ave",
    "FSlOHg": "addison-ave", "FSlOHw": "addison-ave",
    "KXY8": "alice-billings", "FJpg8A": "alice-billings",
}
files = glob.glob(os.path.join(Q, "*.json"))
done, miss = [], []
for key, chat in ROUTE.items():
    hits = [f for f in files if key in os.path.basename(f)]
    if not hits:
        miss.append(key); continue
    for f in hits:
        d = json.load(io.open(f, encoding="utf-8"))
        d["route"] = chat
        json.dump(d, io.open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        done.append("%s -> %s" % (os.path.basename(f)[:36], chat))
for r in sorted(done): print(r)
print("NO MATCH:", miss)
print("queue now:", len(glob.glob(os.path.join(Q, "*.json"))))

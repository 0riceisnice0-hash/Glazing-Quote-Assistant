# -*- coding: utf-8 -*-
"""One pass over the whole queue: who, what, and the first useful lines."""
import json, io, os, re, glob

Q = "test-results/mary-inbox/queue"
rows = []
for p in sorted(glob.glob(os.path.join(Q, "*.json"))):
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception as e:
        print("UNREADABLE", p, e); continue
    body = (d.get("body") or "").replace("\r", " ")
    body = re.sub(r"\s+", " ", body).strip()
    rows.append({
        "file": os.path.basename(p),
        "from": d.get("from", ""),
        "subj": (d.get("subject") or "")[:95],
        "recv": (d.get("received") or "")[:16],
        "route": d.get("route", ""),
        "att": len(d.get("attachments") or []),
        "body": body[:520],
    })

print("QUEUE SIZE:", len(rows))
for r in sorted(rows, key=lambda x: x["recv"]):
    print("\n" + "-" * 92)
    print("%s | %s | %s | att=%d%s" % (r["recv"], r["from"], r["file"], r["att"],
                                       "  ROUTE=" + r["route"] if r["route"] else ""))
    print("SUBJ: %s" % r["subj"])
    print("  %s" % r["body"])

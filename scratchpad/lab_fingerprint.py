# -*- coding: utf-8 -*-
"""List every document collect() picks up, with a content fingerprint, so we can
see how many of them are copies of one another."""
import os, sys, hashlib, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_calibrate as cal
import mary_quote_reader as reader

rows = []
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    d = bt.parse_doc(q["path"])
    if not d:
        continue
    sig = hashlib.md5(json.dumps(
        [[l["code"], l["w"], l["h"], l["qty"], l["unit_rate"], l["frames"]] for l in d["lines"]],
        sort_keys=True).encode()).hexdigest()[:10]
    rows.append((sig, len(d["lines"]), d.get("total"), q["path"]))

groups = {}
for r in rows:
    groups.setdefault(r[0], []).append(r)
print("%d documents collected, %d distinct line-sets\n" % (len(rows), len(groups)))
for sig, g in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    if len(g) > 1:
        print("DUP x%d  sig=%s  lines=%d" % (len(g), sig, g[0][1]))
        for r in g:
            print("        %s" % r[3])
        print()

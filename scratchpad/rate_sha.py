# -*- coding: utf-8 -*-
"""Are the learned rates IDENTICAL before and after the CW rule?

They must be. CW rows were dropped by the reader before, so they never reached
mining; now they are admitted as lines but excluded from supply_money(). If the
rate table moves at all, the 12.28% is not a pure coverage gain and the two
numbers cannot be compared the way the board entry claims.
"""
import os, subprocess, sys, json, hashlib
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(REPO, "scripts"))
src = subprocess.check_output(["git", "show", "HEAD:scripts/mary_backtest.py"], cwd=REPO)
p = os.path.join(REPO, "scripts", "_bt_old_tmp.py")
open(p, "wb").write(src)
try:
    import mary_backtest as new
    import _bt_old_tmp as old
    for name, mod in (("HEAD", old), ("with CW rule", new)):
        docs = mod.collect()
        base = mod.learn(docs)
        n = sum(len(d["lines"]) for d in docs)
        print("%-14s docs %d  lines %d  buckets %d  sha %s"
              % (name, len(docs), n, len(base),
                 hashlib.sha1(json.dumps(base, sort_keys=True).encode()).hexdigest()[:16]))
finally:
    for f in (p, p + "c"):
        if os.path.exists(f):
            os.remove(f)
    c = os.path.join(REPO, "scripts", "__pycache__")
    for f in (os.listdir(c) if os.path.isdir(c) else []):
        if f.startswith("_bt_old_tmp"):
            os.remove(os.path.join(c, f))

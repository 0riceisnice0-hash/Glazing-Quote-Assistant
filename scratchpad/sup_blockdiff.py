# -*- coding: utf-8 -*-
"""Blast radius of the block-boundary fix, measured by running BOTH readers.

The old reader is loaded from git HEAD as a separate module so the two versions
of read_doc can be run over the same 65 documents in one process. What changes
is exactly the set of documents whose supplier block was being read out of a
priced row.
"""
import os, subprocess, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(REPO, "scripts"))

# Old version, straight out of git, written next to the real module so its own
# `import mary_calibrate` style imports still resolve.
old_src = subprocess.check_output(
    ["git", "show", "HEAD:scripts/mary_quote_audit.py"], cwd=REPO)
old_path = os.path.join(REPO, "scripts", "_qa_old_tmp.py")
with open(old_path, "wb") as fh:
    fh.write(old_src)
try:
    import mary_quote_audit as new
    import _qa_old_tmp as old
    import mary_calibrate as cal
    import mary_quote_reader as reader

    seen, rows = set(), []
    for q in reader.scan(cal.TENDERS):
        if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
            continue
        dn = new.read_doc(q["path"])
        if not dn:
            continue
        sig = repr([[r["code"], r["size"], r["qty"], r["unit_rate"]] for r in dn["rows"]])
        if sig in seen:
            continue
        seen.add(sig)
        do = old.read_doc(q["path"])
        rows.append((dn["file"], do, dn))

    print("%d documents\n" % len(rows))
    changed = 0
    for f, do, dn in rows:
        if do["supplier_cost"] == dn["supplier_cost"] and do["_sup_vals"] == dn["_sup_vals"]:
            continue
        changed += 1
        print("  %s" % f)
        print("     names       %r" % (dn["supplier_names"],))
        print("     OLD  cost=%-14r vals=%r" % (do["supplier_cost"], do["_sup_vals"]))
        print("     NEW  cost=%-14r vals=%r" % (dn["supplier_cost"], dn["_sup_vals"]))
    print("\n%d of %d documents changed by the block-boundary fix" % (changed, len(rows)))
finally:
    for p in (old_path, old_path + "c"):
        if os.path.exists(p):
            os.remove(p)
    cache = os.path.join(REPO, "scripts", "__pycache__")
    for p in (os.listdir(cache) if os.path.isdir(cache) else []):
        if p.startswith("_qa_old_tmp"):
            os.remove(os.path.join(cache, p))

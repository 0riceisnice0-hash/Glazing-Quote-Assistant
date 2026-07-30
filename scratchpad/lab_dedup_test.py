# -*- coding: utf-8 -*-
"""Does counting a document three times damage the learned rates?

Fair test: build the folds from the DEDUPED document list so the jobs scored are
identical in both arms. Arm A trains on the training fold WITH the duplicate
copies restored (what collect() does today); arm B trains on the same jobs with
each document counted once. Same test jobs, same lines, three folds."""
import os, sys, hashlib, json, statistics
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_calibrate as cal
import mary_quote_reader as reader


def sig_of(d):
    return hashlib.md5(json.dumps(
        [[l["code"], l["w"], l["h"], l["qty"], l["unit_rate"], l["frames"]] for l in d["lines"]],
        sort_keys=True).encode()).hexdigest()


def raw_collect():
    docs = []
    for q in reader.scan(cal.TENDERS):
        if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
            continue
        d = bt.parse_doc(q["path"])
        if d:
            d["client"], d["job"] = q["client"], q["job"]
            docs.append(d)
    return docs


raw = raw_collect()
seen, uniq, extra = {}, [], {}
for d in raw:
    s = sig_of(d)
    if s in seen:
        extra.setdefault(s, []).append(d)
    else:
        seen[s] = d
        uniq.append(d)
print("raw %d docs -> %d unique; %d surplus copies\n" % (len(raw), len(uniq), len(raw) - len(uniq)))

for fold in range(3):
    train = [d for i, d in enumerate(uniq) if i % 3 != fold]
    test = [d for i, d in enumerate(uniq) if i % 3 == fold]
    train_dup = list(train)
    for d in train:
        train_dup.extend(extra.get(sig_of(d), []))
    out = []
    for label, tr in (("A duplicated", train_dup), ("B deduped", train)):
        rates = bt.learn(tr)
        scored = [s for s in (bt.score_doc(d, learned=rates) for d in test) if s]
        absol = [abs(s["err_pct"]) for s in scored]
        lines = sum(s["lines_priced"] for s in scored)
        skip = sum(s["lines_skipped"] for s in scored)
        out.append((label, len(tr), statistics.fmean(absol), statistics.median(absol),
                    statistics.fmean([s["err_pct"] for s in scored]), lines, skip, len(scored)))
    print("fold %d  (%d test jobs)" % (fold, len(test)))
    for label, ntr, ma, md, bias, lines, skip, njobs in out:
        print("   %-14s train=%2d  mean abs %5.2f%%  median %5.2f%%  bias %+6.2f%%  lines=%d skipped=%d"
              % (label, ntr, ma, md, bias, lines, skip))
    print()

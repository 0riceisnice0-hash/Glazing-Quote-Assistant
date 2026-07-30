# -*- coding: utf-8 -*-
"""Is the CW rule a real gain or just a bigger denominator?

508 -> 516 lines and 13.28% -> 12.28% are NOT the same measurement, so the
honest tests are two:
  1. did any of the 508 lines the engine already priced MOVE? (it must not -
     mining is guarded, so the learned rates should be byte-identical)
  2. how well does the engine price the 8 NEW rows, on their own, one by one?
     A coverage gain that prices its new lines badly is not a gain.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
print("%d documents\n" % len(docs))

base = bt.learn(docs)
print("LEARNED RATES: %d buckets" % len(base))
bogus = [k for k in base if k.startswith("|")]
print("  buckets keyed on an empty code (a CW row leaking into mining): %d" % len(bogus))
print("  sha of the rate table: %s"
      % __import__("hashlib").sha1(json.dumps(base, sort_keys=True).encode()).hexdigest()[:16])

print("\nTHE 8 CURTAIN-WALLING ROWS, PRICED")
print("  %-46s %-16s %6s %4s %11s %11s %8s"
      % ("document", "desc", "m2", "qty", "human unit", "mary unit", "err%"))
errs = []
for d in docs:
    for l in d["lines"]:
        if not l.get("cw"):
            continue
        e = bt.engine_price(l, d.get("supplier"))
        err = (e["unit_rate"] - l["unit_rate"]) / l["unit_rate"] * 100.0
        errs.append(err)
        print("  %-46.46s %-16.16s %6.2f %4s %11.2f %11.2f %+8.2f"
              % (d["file"], l["ref"], l["area"], l["qty"],
                 l["unit_rate"], e["unit_rate"], err))

errs_s = sorted(abs(e) for e in errs)
print("\n  n=%d   mean abs %.2f%%   median abs %.2f%%   worst %.2f%%"
      % (len(errs), sum(abs(e) for e in errs) / len(errs),
         errs_s[len(errs_s) // 2], errs_s[-1]))
ex = [e for e in errs if abs(e) < 0.1]
print("  within 0.1%% of the document: %d of %d" % (len(ex), len(errs)))
sell = sum(l["unit_rate"] * l["qty"] for d in docs for l in d["lines"] if l.get("cw"))
print("  sell value of curtain walling now visible to the engine: GBP %,.2f".replace(",", "") % sell)
print("  sell value of curtain walling now visible to the engine: GBP {:,.2f}".format(sell))

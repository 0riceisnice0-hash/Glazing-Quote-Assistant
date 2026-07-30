# -*- coding: utf-8 -*-
"""Line-by-line on the jobs that carry the remaining error.

Leave-one-out under the new basis leaves six documents above 29%, and between
them they are 7.3 of the 13.24-point mean. That is where the money is, so look
at what the estimator actually charged against what the engine says, and what
rate would have been needed."""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

WANT = [w.lower() for w in (sys.argv[1:] or
        ["tenbury", "tradeteam", "trafalgar", "refrigeration", "georgie", "ashe - cdc"])]

docs = bt.collect()
rates = engine.load_learned()

for d in docs:
    if not any(w in d["file"].lower() for w in WANT):
        continue
    print("=" * 118)
    print("%s   supplier: %s" % (d["file"], d.get("supplier") or "not stated"))
    print("=" * 118)
    print("%-6s %-18s %9s %6s %11s %10s %10s %10s %9s %9s"
          % ("CODE", "REF", "SIZE m2", "QTY", "HUMAN UNIT", "MARY", "SUPPLY/m2", "NEEDS/m2", "BAND n", "ERR"))
    e_t = h_t = 0.0
    for l in d["lines"]:
        key = "%s|%s" % (l["code"], engine.learned_band_of(l["area"]))
        rec = rates.get(key)
        used = rec["median_per_m2"] if rec and rec["n"] >= engine.MIN_LEARNED_N else None
        e = bt.engine_price(l, d.get("supplier"))
        adder = engine.CODE_VALUE.get(l["code"], 0) * engine.adder_factor(l["area"])
        needed = (l["unit_rate"] - adder) / l["area"] if l["area"] else 0
        money = bt.supply_money(l)
        e_t += (e["unit_rate"] if e else 0) * l["qty"]
        h_t += l["unit_rate"] * l["qty"]
        print("%-6s %-18s %9.2f %6.0f %11s %10s %10s %10.1f %9s %8.1f%%"
              % (l["code"], l["ref"][:18], l["area"], l["qty"],
                 "{:,.2f}".format(l["unit_rate"]),
                 "{:,.2f}".format(e["unit_rate"]) if e else "-",
                 "{:,.1f}".format(money / l["area"]) if money else "-",
                 needed,
                 ("%s %d" % (key.split("|")[1], rec["n"])) if rec else "register",
                 ((e["unit_rate"] - l["unit_rate"]) / l["unit_rate"] * 100) if e else 0))
    print("  ITEMS human %s   mary %s   %+.1f%%   (adder in use: %.2f x code value)"
          % ("{:,.2f}".format(h_t), "{:,.2f}".format(e_t),
             (e_t - h_t) / h_t * 100 if h_t else 0, engine.ADDER_FACTOR))
    # Is the whole job simply a constant factor out? If so it is a job-level
    # commercial reason - a discount, a system, a margin - not a rate problem.
    ratios = [bt.supply_money(l) / l["area"] for l in d["lines"] if bt.supply_money(l) and l["area"]]
    if ratios:
        print("  its own supply GBP/m2: median %.1f, range %.1f-%.1f over %d line(s)"
              % (statistics.median(ratios), min(ratios), max(ratios), len(ratios)))
    print()

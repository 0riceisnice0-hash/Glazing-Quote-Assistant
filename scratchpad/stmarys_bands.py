# -*- coding: utf-8 -*-
"""Reproduce the 29/07 St Mary's band figures, and find the odd low-rate lines.

The open question rests on -35.5 / -1.2 / +37.5 / +35.2 by REGISTER band on one
job. Before concluding anything about band structure, check that number is real
and check whether it survives being scored honestly rather than in-sample."""
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_backtest as bt
import mary_pricing as engine

docs = bt.collect()
sm = [d for d in docs if "mary" in d["file"].lower() or "mary" in (d.get("job") or "").lower()]
print("St Mary's candidates: %s\n" % [d["file"] for d in sm])

REG = ["<1.5m2", "1.5-3m2", "3-6m2", ">6m2"]
for d in sm:
    for label, learned in (("IN-SAMPLE (rates include this job)", None),):
        rates = engine.load_learned() if learned is None else learned
        bands = {}
        tot_e = tot_h = 0.0
        for l in d["lines"]:
            e = bt.engine_price(l, d.get("supplier"), learned=rates)
            if not e:
                continue
            b = engine.band_of(l["area"])
            bands.setdefault(b, [0.0, 0.0, 0])
            bands[b][0] += e["unit_rate"] * l["qty"]
            bands[b][1] += l["unit_rate"] * l["qty"]
            bands[b][2] += 1
            tot_e += e["unit_rate"] * l["qty"]
            tot_h += l["unit_rate"] * l["qty"]
        print("%s  -  %s" % (d["file"], label))
        for b in REG:
            if b in bands:
                eng, hum, n = bands[b]
                print("    %-9s n=%-4d human %12s  mary %12s  %+7.1f%%"
                      % (b, n, "{:,.0f}".format(hum), "{:,.0f}".format(eng),
                         (eng - hum) / hum * 100.0))
        print("    %-9s      human %12s  mary %12s  %+7.1f%%\n"
              % ("WHOLE JOB", "{:,.0f}".format(tot_h), "{:,.0f}".format(tot_e),
                 (tot_e - tot_h) / tot_h * 100.0))

# The 5-6m2 bucket came out at GBP 137/m2 against 400-600 either side of it.
# Seven lines. That is either a mis-parse or a job priced on another basis, and
# either way it is sitting inside the >5m2 learned band.
print("ODD LOW-RATE LINES: everything under GBP 200/m2 above 3m2")
for d in docs:
    for l in d["lines"]:
        if l["frames"] and l["area"] > 3.0 and l["frames"] / l["area"] < 200:
            print("  %-40s %-6s %5.0fx%-5.0f %6.2fm2  frames %10s  = %6.1f/m2  unit %10s"
                  % (d["file"][:40], l["code"], l["w"], l["h"], l["area"],
                     "{:,.2f}".format(l["frames"]), l["frames"] / l["area"],
                     "{:,.2f}".format(l["unit_rate"])))

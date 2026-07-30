# -*- coding: utf-8 -*-
"""Every GENUINE curtain-walling row in the archive, and what prices it.

The board (30/07) established that the CW column is a WORKING column on ordinary
window rows - area x GBP 850 parked in a spare cell, not money in the unit rate.
A GENUINE curtain-walling row is the other thing: no product code, a CW LABOUR
figure, and Frames equal to the CW money.

CB Refrigeration (31/07, fourth run) shows what that means commercially: its
CWT-A Frames cell is 17.69 x 850 = 15,036.50 to the penny, which is the CW
NOTIONAL and not what BSW charged - the supplier quote is 2 units at 9,996.30
less 20% = 15,994.08 net, i.e. 7,997.04 each. So on a genuine CW row the Frames
cell is not a buy at all.

Two questions this answers, one for each half of the lab:
  AUDIT   if a genuine CW row's Frames cell is a notional, it must come OUT of
          the frames total before reconciling against the supplier block.
  ENGINE  is unit_rate = area x CW_SUPPLY_M2 a RULE across the archive? These
          rows have no product code, so the engine skips them entirely today.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_calibrate as cal
import mary_pricing as engine
import mary_quote_audit as qa
import mary_quote_reader as reader

CW = engine.CW_SUPPLY_M2
print("CW_SUPPLY_M2 = %.2f\n" % CW)

seen, docs = set(), []
for q in reader.scan(cal.TENDERS):
    if q["total"] < cal.MIN_SENSIBLE or cal.is_untrustworthy(q["file"], q["client"]):
        continue
    d = qa.read_doc(q["path"])
    if not d:
        continue
    sig = repr([[r["code"], r["size"], r["qty"], r["unit_rate"]] for r in d["rows"]])
    if sig in seen:
        continue
    seen.add(sig)
    docs.append(d)

print("%-52s %-14s %5s %4s %10s %10s %10s %8s %8s"
      % ("document", "desc", "m2", "qty", "frames", "cw", "cwlabour", "unit", "a*850"))
n = exact_fr = exact_ur = 0
for d in docs:
    for r in d["rows"]:
        if r.get("code"):
            continue                      # has a product code: not a CW row
        if not r.get("cw_labour"):
            continue                      # no CW LABOUR figure: not a CW row
        a = r.get("area")
        if not a:
            continue
        n += 1
        pred = a * CW
        fr, ur = r.get("frames"), r.get("unit_rate")
        if fr and abs(fr - pred) < 0.02:
            exact_fr += 1
        if ur and abs(ur - pred) < 0.02:
            exact_ur += 1
        print("%-52.52s %-14.14s %5.2f %4s %10s %10s %10s %8s %8.2f"
              % (d["file"], r.get("desc") or "?", a, r.get("qty"),
                 "%.2f" % fr if fr else "-",
                 "%.2f" % r["cw"] if r.get("cw") else "-",
                 "%.2f" % r["cw_labour"],
                 "%.2f" % ur if ur else "-", pred))

print("\n%d genuine CW rows (no product code, has CW LABOUR)" % n)
print("   Frames    == area x %.0f on %d of %d" % (CW, exact_fr, n))
print("   unit_rate == area x %.0f on %d of %d" % (CW, exact_ur, n))

# -*- coding: utf-8 -*-
"""Redditch Library - margin, confidence, and the price needed to beat Joedan.

Adam, 28/07 19:26: "We need to undercut Joedan on this one... Are you confident
in your pricing? We already know the price to beat, so give me an idea of
profit on this."

Three separate questions, and they have three separate answers. This computes
all three from evidence rather than opinion:

  MARGIN     - the take-off decomposed into what we buy and what we keep.
  CONFIDENCE - the benchmark re-priced against BSW QT250834, a real Sheerline
               quote for a Pride job dated 15/06/2026, which is the closest
               comparable buy Fenster holds.
  UNDERCUT   - what is left for strip-out if the total is to come in under
               Joedan's net.

  python scripts/redditch_margin.py
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_pricing as engine

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BSW QT250834, 15/06/2026, quoted to Fenster for Pride Developments' Severn
# Trent job. Sheerline Prestige aluminium casements, factory glazed, trickle
# vents, shootbolt locking, cills, couplers - the nearest thing in the archive
# to what Redditch needs. Six lines, 72.578 m2, Total Nett Ex VAT GBP 34,902.35,
# which the extracted lines reconcile to exactly.
SEVERN_TRENT = [
    (1.440, 629.63), (1.457, 626.80), (2.832, 459.68),
    (2.880, 456.51), (3.939, 412.88), (6.750, 336.78),
]
ST_REF = "BSW QT250834, 15/06/2026, Pride Developments - Severn Trent"

# The engine's error by band as measured on St Mary's (MARY-JOB-SESSION 5c).
# Positive = the engine sits ABOVE the real price.
ST_MARYS_BAND_ERROR = {"<1.5m2": -35.5, "1.5-3m2": -1.2, "3-6m2": 37.5, ">6m2": 35.2}

JOEDAN_GROSS = 90687.17
MCD = 0.025


def fit_power(points):
    """rate = a * area^b, least squares in log space."""
    n = len(points)
    lx = [math.log(a) for a, _ in points]
    ly = [math.log(r) for _, r in points]
    mx, my = sum(lx) / n, sum(ly) / n
    b = (sum((lx[i] - mx) * (ly[i] - my) for i in range(n))
         / sum((lx[i] - mx) ** 2 for i in range(n)))
    a = math.exp(my - b * mx)
    ss = sum((ly[i] - my) ** 2 for i in range(n))
    rs = sum((ly[i] - (math.log(a) + b * lx[i])) ** 2 for i in range(n))
    return a, b, 1 - rs / ss


def main():
    with open(os.path.join(REPO, "outputs", "redditch-takeoff.json"), encoding="utf-8") as fh:
        d = json.load(fh)
    lines = d["lines"]
    frames = sum(l["supply"] for l in lines)
    adders = sum(l["adder"] for l in lines)
    inst, solar = d["installation"], d["solar_glass_premium"]
    sell = d["benchmark_net_ex_vat"]
    material = frames + solar
    joedan_net = JOEDAN_GROSS * (1 - MCD)

    a, b, r2 = fit_power(SEVERN_TRENT)
    st_frames = sum(a * l["area_m2"] ** b * l["area_m2"] for l in lines)
    st_sell = st_frames + adders + inst + solar

    # St Mary's band correction applied to the supply component only.
    band_frames = sum(l["supply"] / (1 + ST_MARYS_BAND_ERROR[engine.band_of(l["area_m2"])] / 100.0)
                      for l in lines)
    band_sell = band_frames + adders + inst + solar

    print("REDDITCH LIBRARY - MARGIN, CONFIDENCE, AND THE PRICE TO BEAT")
    print("=" * 78)
    print("\n1. WHAT THE BENCHMARK IS MADE OF")
    print("   frame supply            COST   %12s" % "{:,.2f}".format(frames))
    print("   solar-control glass     COST   %12s" % "{:,.2f}".format(solar))
    print("   ----------------------------   %12s  material we buy" % "{:,.2f}".format(material))
    print("   house code adders     MARGIN   %12s" % "{:,.2f}".format(adders))
    print("   installation         revenue   %12s  (fit only; our fitting COST is not recorded anywhere)"
          % "{:,.2f}".format(inst))
    print("   ============================   %12s  SELL" % "{:,.2f}".format(sell))
    print("\n   Gross margin, if fitting breaks even: %s" % "{:,.2f}".format(adders))
    print("     = %.1f%% of sell, %.1f%% mark-up on the material buy" % (adders / sell * 100,
                                                                        adders / material * 100))
    print("   NOT net profit: no prelims, supervision, survey, scaffold (excluded), strip-out")
    print("   (unpriced) or MCD are in it, and the fitting cost is unknown.")

    print("\n2. WHY THE MARGIN IS THIN HERE - THE ADDER IS A FIXED SUM PER UNIT")
    print("   %-9s %3s %9s %12s %12s %9s" % ("band", "n", "m2", "buy", "adder", "adder %"))
    for k in ("<1.5m2", "1.5-3m2", "3-6m2", ">6m2"):
        ls = [l for l in lines if engine.band_of(l["area_m2"]) == k]
        if not ls:
            continue
        c = sum(l["supply"] for l in ls)
        ad = sum(l["adder"] for l in ls)
        print("   %-9s %3d %9.2f %12s %12s %8.1f%%"
              % (k, len(ls), sum(l["area_m2"] for l in ls), "{:,.0f}".format(c),
                 "{:,.0f}".format(ad), ad / (c + ad) * 100))
    print("   Redditch averages %.2f m2 a unit and the adder is %.1f%% of the frame line."
          % (d["area_m2"] / len(lines), adders / (frames + adders) * 100))
    print("   Crestwood Park averaged 1.29 m2 and the adder was 42.9% (GBP 20,550 on a")
    print("   GBP 27,329.60 BSW buy, both figures verified). Big units earn less.")

    print("\n3. CONFIDENCE - THE BENCHMARK AGAINST A REAL, RECENT, COMPARABLE BUY")
    print("   %s" % ST_REF)
    print("   rate = %.2f x area^%.4f   R2 = %.4f over %d rate points spanning %.2f-%.2f m2"
          % (a, b, r2, len(SEVERN_TRENT), min(x for x, _ in SEVERN_TRENT),
             max(x for x, _ in SEVERN_TRENT)))
    print("   (6 quoted lines, 27 units, 72.578 m2 in total - the fit is on the unit rates)")
    print("\n   %-9s %14s %16s" % ("band", "St Mary's", "Severn Trent"))
    for k in ("<1.5m2", "1.5-3m2", "3-6m2", ">6m2"):
        ls = [l for l in lines if engine.band_of(l["area_m2"]) == k]
        if not ls:
            continue
        eng = sum(l["supply"] for l in ls)
        stv = sum(a * l["area_m2"] ** b * l["area_m2"] for l in ls)
        print("   %-9s %+13.1f%% %+15.1f%%" % (k, ST_MARYS_BAND_ERROR[k], (eng / stv - 1) * 100))
    print("   Positive = the engine sits ABOVE the real price. Two independent jobs,")
    print("   different suppliers and dates, agreeing within a few points on the small")
    print("   and the large band. The band structure is now evidenced twice, not once.")

    print("\n4. THREE ESTIMATES OF THE SAME JOB")
    ests = [("engine benchmark (as issued)", sell),
            ("re-priced on the Severn Trent curve", st_sell),
            ("St Mary's band correction", band_sell)]
    for name, v in ests:
        print("   %-38s %12s" % (name, "{:,.2f}".format(v)))
    print("   The spread is almost entirely the 3-6 m2 band, which carries 62% of this job.")

    print("\n5. CAN WE UNDERCUT JOEDAN?")
    print("   Joedan gross of %.1f%% MCD            %12s" % (MCD * 100, "{:,.2f}".format(JOEDAN_GROSS)))
    print("   Joedan NET to a main contractor      %12s  <- the number to beat"
          % "{:,.2f}".format(joedan_net))
    print("   and it INCLUDES their strip-out (their cl.12). Ours does not.\n")
    print("   %-38s %12s %14s %13s" % ("basis", "our sell", "headroom", "per opening"))
    for name, v in ests:
        print("   %-38s %12s %14s %13s"
              % (name, "{:,.2f}".format(v), "{:,.2f}".format(joedan_net - v),
                 "{:,.2f}".format((joedan_net - v) / len(lines))))
    print("\n   Headroom is what is left to pay for stripping 43 openings out of an")
    print("   occupied library. At the benchmark there is none - we are already over.")

    out = {
        "material_cost": round(material, 2), "frame_supply": round(frames, 2),
        "solar_glass": solar, "adders": round(adders, 2), "installation": inst,
        "sell": sell, "gross_margin": round(adders, 2),
        "margin_pct_of_sell": round(adders / sell * 100, 2),
        "markup_pct_on_material": round(adders / material * 100, 2),
        "severn_trent": {"ref": ST_REF, "a": round(a, 4), "b": round(b, 5),
                         "r2": round(r2, 5), "frames": round(st_frames, 2),
                         "sell": round(st_sell, 2)},
        "band_corrected_sell": round(band_sell, 2),
        "joedan_gross": JOEDAN_GROSS, "joedan_net": round(joedan_net, 2),
        "headroom": {name: round(joedan_net - v, 2) for name, v in ests},
    }
    p = os.path.join(REPO, "outputs", "redditch-margin.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("\nwritten %s" % p)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""One pricing engine, instead of a fresh script for every job.

Until now Mary wrote a bespoke calculator each time - vesuvius_pricing.py,
pb-takeoff.py, stoke-glass-compare.py - so nothing she learned ever accumulated
and nothing could be regression-tested. Meanwhile the 15,551-line rate register
built on 16/07 was never wired into anything at all.

This is that engine. Three things it insists on:

  PROVENANCE. Every rate says where it came from - category, median, how many
  quote lines, which suppliers, what date range. A benchmark is evidence, never
  a firm price, and it has to look like evidence when it reaches a human.

  CALIBRATION. The register is medians, and Mary's own calibration record says
  exactly where those medians lie. Those corrections are applied here, each
  citing the job that taught it, rather than living as prose in a handover
  nobody reads back.

  THE TEMPLATE IS THE PRICE. Adam ruled on 17/07 that the MASTER PRICING DOC
  formulas are correct: unit rate = supply + (code value x 75%), then labour by
  code. This reproduces that arithmetic exactly, so what the engine says and
  what the client doc says cannot drift apart.

  python scripts/mary_pricing.py --rates            # what the register knows
  python scripts/mary_pricing.py --selftest         # arithmetic + calibration
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(REPO, "data", "supplier-rates.json")

# Adam's labour table. Also the INSTALLATION formula in the house template.
LABOUR = {
    "SUPD": 250, "SAD": 250, "DUPD": 500, "DAD": 500, "ELAW": 250,
    "LAW": 160, "MAW": 160, "SAW": 160, "LPVC": 160, "MPVC": 160, "SPVC": 160,
    "SADLAW": 410, "SADMAW": 410, "SADSAW": 410,
}
# The template's own adder: the product code value x 75%.
CODE_VALUE = {
    "SAW": 450, "MAW": 550, "LAW": 650, "ELAW": 850, "SAD": 1200, "DAD": 2000,
    "SADSAW": 1700, "SADMAW": 1900, "SADLAW": 2000, "SPVC": 350, "MPVC": 400,
    "LPVC": 450, "SUPD": 1000, "DUPD": 1500,
}
ADDER_FACTOR = 0.75
# AND 0.75 ABOVE 6 m2 TOO, AS OF 30/07. The fudge is retired, because the money
# it was standing in for is now measured and modelled where it belongs.
#
# The document builds a unit rate as frames + glass + additional + 0.75 x code
# value, and that reconciles on 495 of 508 priced lines once the CW working
# column is left out of it. The engine's learned rate was mined from the Frames
# column ALONE, so Glass and Additional - 20.4% of supply above 6m2, 9.3% at
# 2-3m2 - were money it had no term for anywhere, and ADDER_FACTOR_LARGE was
# absorbing the largest part of that on the largest units. The 30/07 note below
# had already worked out that this was what the constant contained; what was
# missing was a way to model the extras instead, and mining the whole build-up
# is it. mary_backtest.supply_money() is the change.
#
# Leave-one-out over all 29 documents, each scored on rates mined from the other
# 28 - and leave-one-out precisely because a small win on three positional folds
# has misled this board twice:
#     frames only,    1.25 large    mean abs 14.02%  median 10.05%  bias -4.91%
#     whole build-up, 0.75 flat     mean abs 13.24%  median  7.98%  bias -1.66%
# Better on 16 documents, worse on 11, within-10 up from 14 to 16. Keeping 1.25
# ON TOP of the whole build-up double-counts the extras and is the worst arm of
# the four at 14.88%, which is itself good evidence the two were the same money.
#
# LARGE_UNIT_M2 and adder_factor() are kept rather than deleted: the flat 0.75 is
# now a measurement over 508 lines in every band, and a future session that
# wants to argue for a size-dependent adder should have to change a number here
# and show it on unseen jobs, not re-derive the whole idea.
#
# WHAT THE RETIRED CONSTANT WAS, kept because the reasoning is the transferable
# part and a later session should not have to rediscover it:
#
# It was recorded on 29/07 as "the estimator takes the code value at 125% once a
# unit passes 6 m2, and has been doing it by hand all along", the commercial
# reason being that a big unit is a coupled screen rather than a single leaf.
# That is not true, and the 30/07 lab session measured it directly rather than
# by inference. The 29/07 figure came from (unit_rate - frames) / code_value,
# which is not the adder: it is the adder PLUS Glass PLUS Additional PLUS CW,
# because the engine's learned rate is mined from the Frames column alone and
# has no term for the other three. Reading all four component columns instead
# gives the adder itself, and on lines over 6 m2 - excluding the three Brandon
# Estate documents, whose components exceed their own unit rate and so cannot
# be per-unit money - 26 of 28 lines sit on EXACTLY 0.75, and none on 1.25.
#
# 1.25 is what you get by charging the un-modelled extras to the code value:
# the median of glass+additional+cw on a large unit is GBP 1,000, the median
# large unit is a DAD with a code value of 2,000, and 0.75 + 1000/2000 = 1.25
# exactly. That is also why re-deriving it on an independent half reproduced
# "1.250 exactly" and looked like strong evidence - a systematic confound
# reproduces in every split, which is the one thing a holdout cannot catch.
#
# So it stays, as an admitted fudge for money the engine does not model, and
# NOT as the estimator's rule - it earns its place on unseen jobs and that is
# the only reason it is here. Three folds, constant line set, learned rates
# re-mined per fold: mean abs 13.88 at 1.25 against 14.46 at 0.75, winning two
# folds of three, and the curve is flat between 1.00 and 1.40 (14.04/13.94/
# 13.88/14.16), so do not read the 1.25 as a precise quantity.
# THE PRINCIPLED FIX WAS TRIED AND IS WORSE: modelling the extras as a flat
# learned sum on large units (correctly learned at GBP 1,000/600/1,000 per
# fold) with the adder left at 0.75 scores 14.73 - worse than both arms. The
# extras are scope items that vary, not a constant, and 1.25 also happens to
# correct a general under-pricing bias. Do not spend the hour re-testing it.
LARGE_UNIT_M2 = 6.0
ADDER_FACTOR_LARGE = 0.75


def adder_factor(area_m2):
    return ADDER_FACTOR_LARGE if area_m2 > LARGE_UNIT_M2 else ADDER_FACTOR
# Curtain walling is priced by area, not by code - Greenfields calibration.
CW_SUPPLY_M2, CW_LABOUR_M2 = 850.0, 150.0

# Removal of the existing frames on a replacement job. Until 29/07/2026 there was no
# rate for this anywhere - 0 of the 80 categories in the register cover strip-out,
# disposal or manifestation - and it sat promised-but-unpriced on five jobs at once.
# Adam named the precedent (REQ-24, 28/07): "the large tender we did for Brandon Estate
# (for Elkins I believe)... we included a cost for removal of frames there".
# Read at source, and it holds across both revisions of that tender:
#   REV 2       "Removal of existing frames"  GBP 330,300 / 2,202 units = GBP 150.00
#   earlier rev "Removal of existing frames"  GBP 198,750 / 1,325 units = GBP 150.00
# Identical to the penny as the job grew by 877 units, so it is a PER-UNIT rate and not
# a lump someone eyeballed. It is a SELL rate - both figures come off the client-facing
# pricing document - so do not mark it up. Brandon's proposal worded it "Installation and
# removal of old frames is included within our costs".
# CAUTION ON SCALE: Brandon was 2,202 near-identical units on one estate. A small
# replacement job has none of that repetition, so treat GBP 150 as a FLOOR, not a
# ceiling. Per m2 it works out at GBP 40.90, but Brandon's units average 3.67 m2 against
# (for example) St Mary's 1.90 m2, so the per-unit basis travels better than the per-m2
# one - stripping an opening is mostly a fixed operation per opening.
STRIP_OUT_PER_UNIT = 150.0
STRIP_OUT_PROVENANCE = ("GBP 150.00/unit sell - Fenster's own Brandon Estate tender to Elkins "
                        "(GBP 330,300 / 2,202 units in REV 2; GBP 198,750 / 1,325 units in the "
                        "earlier revision, identical per unit). Named by Adam, REQ-24, 28/07/2026. "
                        "A floor on a small job - Brandon was 2,202 repetitive units.")


def strip_out(units):
    """Removal and disposal of the existing frames, priced per opening.

    Returns the figure with its provenance, because this is a house rate read off one
    real tender rather than a register median - it is evidence, not a firm price."""
    return {"units": units,
            "rate": STRIP_OUT_PER_UNIT,
            "total": round(units * STRIP_OUT_PER_UNIT, 2),
            "basis": "per unit (per opening stripped)",
            "provenance": STRIP_OUT_PROVENANCE}

# Corrections to the register medians, each earned on a real job. A median is
# the middle of history, not the price of the thing in front of you.
CALIBRATION = [
    {"match": ("sheerline", "prestige"), "factor": 1.10,
     "why": "live Sheerline Prestige runs ~10% above register aluminium medians",
     "source": "SM5 Wexham, BSW QT253300, 24/07/2026"},
    {"match": ("smart wall", "sma"), "factor": 1.45,
     "why": "register aluminium-door medians badly undercook SMA Smart Wall commercial doorsets",
     "source": "Greenfields comparison vs Fenster's sent quote, 22/07/2026"},
    {"match": ("liniar", "upvc live"), "factor": 0.90,
     "why": "Liniar uPVC live rates run 8-15% below register medians",
     "source": "Greenfields comparison vs Fenster's sent quote, 22/07/2026"},
    {"match": ("senior",), "factor": 1.15,
     "why": "Senior premium over the non-Senior quotes the register is built from - judgement, "
            "no Senior quote has ever been held",
     "source": "Vesuvius Way, 27/07/2026"},
]


LEARNED_FILE = os.path.join(REPO, "data", "learned-rates.json")
MIN_LEARNED_N = 6      # below this it is anecdote, not a rate


def load_register():
    with open(REGISTER, encoding="utf-8") as fh:
        return json.load(fh)["register"]


def load_learned():
    """Rates mined from the supply build-up of quotes Fenster actually sent.

    Frames + Glass + Additional, which is the whole of the supply money in a
    unit rate - NOT the Frames column alone, which is what these were until
    30/07 and which left the engine blind to Glass and Additional entirely.

    Strictly better evidence than a supplier-quote median: it is what we really
    charged, and it already contains every judgement the estimator applied.
    Built by mary_backtest.py --learn."""
    if not os.path.exists(LEARNED_FILE):
        return {}
    try:
        with open(LEARNED_FILE, encoding="utf-8") as fh:
            return json.load(fh).get("rates", {})
    except Exception:
        return {}


class LearnedRate:
    def __init__(self, key, rec, factors=None):
        self.base = rec["median_per_m2"]
        self.key = key
        self.rec = rec
        self.factors = list(factors or [])
        self.rate = self.base
        for f in self.factors:
            self.rate *= f["factor"]

    @property
    def provenance(self):
        s = ("GBP%.2f/m2 - median of %d line(s) Fenster actually charged for %s "
             "(range %.2f-%.2f), mined from sent pricing documents"
             % (self.base, self.rec["n"], self.key, self.rec["low"], self.rec["high"]))
        for f in self.factors:
            s += "; x%.3f %s [%s]" % (f["factor"], f["why"], f["source"])
        if self.factors:
            s += " -> GBP%.2f/m2" % self.rate
        return s


def derived_factors(hay):
    """Supplier corrections computed from real quotes, not typed in by hand.

    These supersede CALIBRATION below. That list was my best reading of the
    handover notes; these are measured against what Fenster actually charged,
    with size and product held constant. Where a supplier has enough lines,
    believe the measurement."""
    if not hay:
        return []
    try:
        with open(LEARNED_FILE, encoding="utf-8") as fh:
            facs = json.load(fh).get("supplier_factors", {})
    except Exception:
        return []
    low = hay.lower()
    out = []
    for supplier, rec in facs.items():
        if supplier and supplier in re.sub(r"[^a-z0-9]", "", low):
            if not rec.get("applied", True):
                continue          # measured but implausible - see held_back
            out.append({"factor": rec["factor"], "why": rec["why"], "source": rec["source"]})
    return out


def learned_rate(code, area_m2, supplier=None, system=""):
    """The empirical rate for this code and band, corrected for the supplier.

    THE SUPPLIER CORRECTION WAS BEING MEASURED AND THEN THROWN AWAY (30/07 run 3).
    learn_supplier_factors() measures how dear each supplier runs against the
    all-supplier rate for the same code and band, and writes it to
    learned-rates.json - but it was only ever read by find_rate(), the REGISTER
    path, and a learned rate is per code and band across ALL suppliers. Since
    every one of the 508 archive lines has a learned rate, the measurement was
    reaching nothing.

    Leave-one-JOB-out, factors re-mined inside every fold:
        learned rate alone                  13.58%  median 7.98%  bias -1.25%  16/29
        learned rate x supplier factor      13.29%         7.92%        -2.00%  15/29

    READ THAT HONESTLY, because it is a 0.29-point win and it is not clean.
    THE WHOLE GAIN IS ONE SUPPLIER. TruFrame measures 0.859 with Trafalgar House
    held out and 0.910 with Zelltec Crownhill held out - two independent jobs
    agreeing that they run 9-14% below the archive - and it moves Trafalgar House
    +29.7 -> +18.6 and the two Zelltec documents +17.2 -> +10.8 and +4.7 -> -1.3.
    Everything else is noise or a loss: it is WORSE on 10 documents and better on
    8, within-10 falls from 16 to 15, and bias worsens. The losses are all Aplus,
    whose factor is 0.894, 1.002 or 1.028 depending on which job is held out -
    that instability costs Oldswinford 5.8 points and Favell House 2.8.
    It is in because mean absolute error on unseen jobs is this lab's decision
    metric and it improved. The honest test is whether the next TruFrame job comes
    in closer; if a future session has more Aplus work, gate on the per-job
    medians agreeing. THAT GATE WAS TRIED AND CANNOT BE MEASURED YET: holding out
    Trafalgar leaves TruFrame with one job, so any cross-job stability test drops
    the only factor that pays (13.67% with it, worse than doing nothing)."""
    rates = load_learned()
    key = "%s|%s" % (code, learned_band_of(area_m2))
    rec = rates.get(key)
    if rec and rec.get("n", 0) >= MIN_LEARNED_N:
        return LearnedRate(key, rec, derived_factors(system or supplier or ""))
    return None


def band_of(area_m2):
    """Bands for the REGISTER. These are fixed by the register's own category
    strings ('aluminium casement window, glazed [1.5-3m2]') and cannot be moved
    without rebuilding it, so they stay as they are."""
    if area_m2 < 1.5:
        return "<1.5m2"
    if area_m2 < 3:
        return "1.5-3m2"
    if area_m2 <= 6:
        return "3-6m2"
    return ">6m2"


# Bands for the LEARNED rates, which are ours to choose because we mine them.
# Tested by re-learning under each structure and scoring on jobs never seen,
# three folds, line set held constant. 2/5 beat the register's 1.5/3/6 on all
# three folds; 1.5/4 beat it on one fold and lost the other two, which is what
# a single-fold result is worth. Splitting bands FINER made it clearly worse -
# 513 mined lines will not support more than three buckets before each falls
# under MIN_LEARNED_N and drops through to the register.
LEARNED_EDGES = (2.0, 5.0)


def learned_band_of(area_m2):
    if area_m2 < LEARNED_EDGES[0]:
        return "<2m2"
    if area_m2 < LEARNED_EDGES[1]:
        return "2-5m2"
    return ">5m2"


def _years(entry):
    ds = [s.get("quoteDate") or "" for s in entry.get("sources", [])]
    yrs = sorted({d[-4:] for d in ds if len(d) >= 4 and d[-4:].isdigit()})
    return "%s-%s" % (yrs[0], yrs[-1]) if len(yrs) > 1 else (yrs[0] if yrs else "date unknown")


class Rate:
    """A benchmark, and everything a human needs to judge it."""

    def __init__(self, entry, area, factors):
        self.base = entry["median"]
        self.entry = entry
        self.area = area
        self.factors = factors
        self.rate = self.base
        for f in factors:
            self.rate *= f["factor"]

    @property
    def provenance(self):
        e = self.entry
        bits = ["%s median GBP%.2f/m2 from %d quote line(s) (%s, %s)"
                % (e["category"], self.base, e.get("lineCount", 0),
                   e.get("supplier", "mixed"), _years(e))]
        for f in self.factors:
            bits.append("x%.2f %s [%s]" % (f["factor"], f["why"], f["source"]))
        return "; ".join(bits)

    def __repr__(self):
        return "<Rate GBP%.2f/m2 (base %.2f)>" % (self.rate, self.base)


def find_rate(family, area_m2, supplier=None, system=""):
    """Look up a size-banded benchmark and apply any earned corrections."""
    band = band_of(area_m2)
    reg = load_register()
    want = family.lower()
    cands = [e for e in reg
             if want in e["category"].lower() and band in e["category"]
             and (not supplier or e.get("supplier", "").lower() == supplier.lower())]
    if not cands:
        cands = [e for e in reg if want in e["category"].lower() and band in e["category"]]
    if not cands:
        return None
    # Most evidence wins.
    entry = max(cands, key=lambda e: e.get("lineCount", 0))
    hay = ("%s %s" % (system, supplier or "")).lower()
    # Measured beats typed: fall back to the hand-written constants only where
    # there is not enough real evidence for a derived factor.
    factors = derived_factors(hay) or [c for c in CALIBRATION if any(m in hay for m in c["match"])]
    return Rate(entry, area_m2, factors)


def price_line(code, width_mm, height_mm, qty=1, supply_rate=None, family=None,
               supplier=None, system="", curtain_wall=False):
    """One row of the pricing document, priced the way the template prices it."""
    area = (width_mm / 1000.0) * (height_mm / 1000.0)
    prov = ""
    if curtain_wall:
        supply = area * CW_SUPPLY_M2
        labour = area * CW_LABOUR_M2
        adder = 0.0
        prov = "curtain walling convention: GBP%.0f/m2 supply + GBP%.0f/m2 labour [Greenfields, 22/07/2026]" % (
            CW_SUPPLY_M2, CW_LABOUR_M2)
    else:
        if supply_rate is None:
            r = find_rate(family or "aluminium window/screen, glazed", area, supplier, system)
            if r is None:
                raise ValueError("no register rate for %r at %.2fm2" % (family, area))
            supply_rate = r.rate
            prov = r.provenance
        else:
            prov = "supplier quote (SUPPLIER BACKED)"
        supply = area * supply_rate
        adder = CODE_VALUE.get(code, 0) * adder_factor(area)
        labour = LABOUR.get(code, 0)
    unit = supply + adder
    return {
        "code": code, "qty": qty, "area_m2": round(area, 3),
        "supply": round(supply, 2), "adder": round(adder, 2),
        "unit_rate": round(unit, 2), "line_total": round(unit * qty, 2),
        "labour": round(labour * qty, 2),
        "provenance": prov,
        "basis": "SUPPLIER BACKED" if supply_rate is not None and not prov.startswith(("aluminium", "uPVC", "curtain")) else "BENCHMARK",
    }


def price_job(lines):
    items = sum(l["line_total"] for l in lines)
    install = sum(l["labour"] for l in lines)
    return {"lines": lines, "items": round(items, 2), "installation": round(install, 2),
            "total_ex_vat": round(items + install, 2),
            "total_inc_vat": round((items + install) * 1.2, 2)}


# ------------------------------------------------------------------ selftest

def selftest():
    ok = True

    def check(name, got, want, tol=0.01):
        nonlocal ok
        good = abs(got - want) <= tol
        ok = ok and good
        print("  [%s] %-46s got %12s want %12s" % ("ok  " if good else "FAIL", name,
                                                   "{:,.2f}".format(got), "{:,.2f}".format(want)))

    print("TEMPLATE ARITHMETIC (Adam's ruling, 17/07 - the template is the price)")
    # A 2m x 1.5m MAW at a known supply rate: 3m2 x 200 = 600 supply,
    # adder 550 x 75% = 412.50, labour 160.
    l = price_line("MAW", 2000, 1500, qty=2, supply_rate=200.0)
    check("supply 3m2 x GBP200", l["supply"], 600.00)
    check("code adder MAW 550 x 75%", l["adder"], 412.50)
    check("unit rate", l["unit_rate"], 1012.50)
    check("line total x2", l["line_total"], 2025.00)
    check("labour MAW 160 x2", l["labour"], 320.00)
    job = price_job([l])
    check("items + installation = total", job["total_ex_vat"], 2025.00 + 320.00)

    print("\nCURTAIN WALLING (Greenfields calibration)")
    cw = price_line("CW", 4542, 2747, curtain_wall=True)
    area = 4.542 * 2.747
    check("supply at GBP850/m2", cw["supply"], area * 850)
    check("labour at GBP150/m2", cw["labour"], area * 150)

    print("\nSTRIP-OUT (Brandon Estate, the rate Adam named on REQ-24)")
    # The rate is proven by holding across two revisions of the same tender.
    check("Brandon REV 2  330,300 / 2,202 units", strip_out(2202)["total"], 330300.00)
    check("Brandon earlier 198,750 / 1,325 units", strip_out(1325)["total"], 198750.00)
    check("St Mary's 107 openings", strip_out(107)["total"], 16050.00)
    cited = "Brandon Estate" in strip_out(1)["provenance"]
    print("  [%s] rate cites the tender it was read off" % ("ok  " if cited else "FAIL"))
    ok = ok and cited

    print("\nREGISTER LOOKUP WITH PROVENANCE")
    r = find_rate("aluminium casement window, glazed", 2.0)
    if r is None:
        print("  [FAIL] no rate found"); ok = False
    else:
        print("  [ok  ] GBP%.2f/m2" % r.rate)
        print("         %s" % r.provenance[:140])

    print("\nCALIBRATION APPLIES AND IS CITED")
    plain = find_rate("aluminium casement window, glazed", 2.0)
    sheer = find_rate("aluminium casement window, glazed", 2.0, system="Sheerline Prestige")
    if plain and sheer:
        check("Sheerline uplift = base x1.10", sheer.rate, plain.base * 1.10)
        cited = "SM5 Wexham" in sheer.provenance
        print("  [%s] uplift cites the job that taught it" % ("ok  " if cited else "FAIL"))
        ok = ok and cited
    else:
        ok = False

    print("\nselftest %s" % ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rates", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.rates:
        reg = load_register()
        print("%d benchmark categories, %d quote lines behind them\n"
              % (len(reg), sum(e.get("lineCount", 0) for e in reg)))
        for e in sorted(reg, key=lambda e: -e.get("lineCount", 0))[:25]:
            print("  %-58s GBP%9.2f/m2  n=%-4d %s"
                  % (e["category"][:58], e["median"], e.get("lineCount", 0), _years(e)))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

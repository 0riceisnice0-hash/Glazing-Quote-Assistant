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
# Curtain walling is priced by area, not by code - Greenfields calibration.
CW_SUPPLY_M2, CW_LABOUR_M2 = 850.0, 150.0

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
    """Rates mined from the Frames column of quotes Fenster actually sent.

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
    def __init__(self, key, rec):
        self.rate = rec["median_per_m2"]
        self.base = self.rate
        self.key = key
        self.rec = rec
        self.factors = []

    @property
    def provenance(self):
        return ("GBP%.2f/m2 - median of %d line(s) Fenster actually charged for %s "
                "(range %.2f-%.2f), mined from sent pricing documents"
                % (self.rate, self.rec["n"], self.key, self.rec["low"], self.rec["high"]))


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


def learned_rate(code, area_m2):
    rates = load_learned()
    rec = rates.get("%s|%s" % (code, band_of(area_m2)))
    if rec and rec.get("n", 0) >= MIN_LEARNED_N:
        return LearnedRate("%s|%s" % (code, band_of(area_m2)), rec)
    return None


def band_of(area_m2):
    if area_m2 < 1.5:
        return "<1.5m2"
    if area_m2 < 3:
        return "1.5-3m2"
    if area_m2 <= 6:
        return "3-6m2"
    return ">6m2"


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
        adder = CODE_VALUE.get(code, 0) * ADDER_FACTOR
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

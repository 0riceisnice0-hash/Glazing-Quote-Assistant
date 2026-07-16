# -*- coding: utf-8 -*-
"""Aggregate mined supplier quote lines into data/supplier-rates.json."""
import json
import re
import statistics
import sys
from datetime import datetime

SRC = sys.argv[1] if len(sys.argv) > 1 else r"test-results\rate-miner-pilot\mined-quotes.json"
OUT = r"data\supplier-rates.json"

d = json.load(open(SRC, encoding="utf-8"))
groups = {}


def size_band(area):
    """Frames price lower per m2 as they grow; band rates by unit area."""
    if area is None:
        return ""
    if area < 1.5:
        return " [<1.5m2]"
    if area < 3.0:
        return " [1.5-3m2]"
    if area < 6.0:
        return " [3-6m2]"
    return " [>6m2]"


PLAUSIBLE = {"GBP/m2": (10, 3000), "GBP/doorset": (200, 6000)}


def add(supplier, category, rec, line, rate, unit="GBP/m2"):
    lo, hi = PLAUSIBLE.get(unit, (0, 10**9))
    if not (lo <= rate <= hi):
        return
    key = (supplier, category, unit)
    g = groups.setdefault(key, {"supplier": supplier, "category": category, "unit": unit,
                                "rates": [], "sources": {}})
    g["rates"].append(rate)
    ref = rec.get("quoteRef") or rec.get("file")
    src = g["sources"].setdefault(ref, {"quoteRef": ref, "quoteDate": rec.get("quoteDate"),
                                        "client": rec.get("client"), "job": rec.get("job"),
                                        "file": rec.get("file"), "lines": 0})
    src["lines"] += 1


for rec in d["records"]:
    sup = rec.get("supplier")
    for l in rec.get("lines", []) or []:
        rate = l.get("ratePerM2")
        if sup in ("bsw", "bellview"):
            rate = l.get("effectiveRatePerM2") or rate
            if rate is None:
                continue
            prod = (l.get("product") or "").strip()
            glz = (l.get("glazing") or "")
            unglazed = "Unglazed" in glz
            solar = bool(re.search(r"skn|coolite", glz, re.I))
            material = l.get("material") or \
                ("uPVC" if re.search(r"foil|pvc", prod + " " + glz, re.I) else "aluminium")
            tt = bool(re.search(r"t&t|tilt", prod, re.I))
            kind = "door" if "door" in prod.lower() else ("tilt & turn window" if tt else "casement window")
            cat = "%s %s, %s%s%s" % (material, kind,
                                     "unglazed" if unglazed else "glazed",
                                     " incl solar control (SKN/Coolite)" if solar and not unglazed else "",
                                     size_band(l.get("areaM2")))
            add(sup, cat.strip().rstrip(","), rec, l, rate)
        elif sup == "vetroseal":
            if l.get("kind") == "charge" or rate is None:
                continue
            desc = l.get("desc") or ""
            solar = bool(re.search(r"skn|coolite|anti-?sun", desc, re.I))
            lami = bool(re.search(r"lami", desc, re.I))
            tough = bool(re.search(r"tgh|tough", desc, re.I))
            build = ("laminated/toughened" if lami and tough else
                     "laminated" if lami else "toughened" if tough else "DGU")
            cat = "%s unit%s" % (build, ", solar control (SKN/Coolite)" if solar else ", softcoat")
            add(sup, cat, rec, l, rate)
        elif sup == "strongdor":
            unit_price = l.get("unitPrice")
            if unit_price is None:
                continue
            cat = "steel doorset %s %s" % (l.get("range", ""), l.get("doorType", ""))
            add(sup, cat.strip(), rec, l, unit_price, unit="GBP/doorset")
        elif sup == "aplus":
            if rate is None:
                continue
            prod = (l.get("product") or "").lower()
            unglazed = "Unglazed" in (l.get("glazing") or "")
            kind = ("door" if "door" in prod else
                    "curtain wall/facade" if re.search(r"facade|curtain|tental", prod) else
                    "window/screen")
            cat = "aluminium %s, %s%s" % (kind, "unglazed" if unglazed else "glazed/unknown",
                                          size_band(l.get("areaM2")))
            add(sup, cat, rec, l, rate)

register = []
for (sup, cat, unit), g in sorted(groups.items()):
    rates = sorted(g["rates"])
    register.append({
        "supplier": sup,
        "category": cat,
        "unit": unit,
        "lineCount": len(rates),
        "median": round(statistics.median(rates), 2),
        "min": rates[0],
        "max": rates[-1],
        "sources": sorted(g["sources"].values(), key=lambda s: s.get("quoteDate") or ""),
    })

out = {
    "builtAt": datetime.now().isoformat(),
    "sourceScan": SRC,
    "note": ("Historical benchmark rates mined from supplier quotations. Evidence only - "
             "never present as firm prices; quotes are typically valid 30 days."),
    "register": register,
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)

def date_key(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except (ValueError, TypeError):
        return datetime.min


print("Register entries: %d -> %s" % (len(register), OUT))
for e in register:
    dates = sorted([s["quoteDate"] for s in e["sources"] if s.get("quoteDate")], key=date_key)
    print("  %-10s %-58s n=%-4d median %8.2f  range %8.2f-%8.2f  %s  [%s]" % (
        e["supplier"], e["category"][:58], e["lineCount"], e["median"], e["min"], e["max"], e["unit"],
        (dates[0] + " to " + dates[-1]) if dates else "no dates"))

# -*- coding: utf-8 -*-
"""Redditch Library (BLBS0956) - take-off and benchmark price.

The take-off is NOT ours: Gleeds' own blank pricing schedule (tender pack p77)
and Joedan's quotation schedule (Appendix 2, p150) are the SAME 43 rows - same
refs, same sizes, same configuration counts. Verified column-by-column against
the rendered page, not the text layer, because the configuration columns are
rotated headers over five 16pt-spaced columns and a flattened text dump cannot
tell Fixed Light from Single Door.

Every rate here is a BENCHMARK. There is no supplier quote for this job.

  python scripts/redditch_takeoff.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_pricing as engine

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ref, width, height, top-hung, fixed light, fixed panel, single door, double door
# Read off the rendered page 77 at 130dpi and cross-checked against Joedan p150
# word x-positions (TH 294-296, FL 310-312, FP 326-329, SD 342-346, DD 357-363).
SCHEDULE = [
    ("1",    1800, 2000, 0,  1, 1, 0, 0),
    ("2",    1800, 2000, 0,  1, 1, 0, 0),
    ("3",    2650, 1800, 0,  2, 2, 0, 0),
    ("4",    2650, 1800, 0,  2, 2, 0, 0),
    ("5",    2650, 1800, 0,  2, 2, 0, 0),
    ("6",    2650, 1800, 0,  2, 2, 0, 0),
    ("7",    2650, 1800, 0,  2, 2, 0, 0),
    ("8",    2650, 1800, 0,  2, 2, 0, 0),
    ("9",    2248, 1600, 2,  0, 0, 0, 0),
    ("10",   2248, 1600, 2,  0, 0, 0, 0),
    ("11",   2248, 1600, 2,  0, 0, 0, 0),
    ("12",   2248, 1600, 2,  0, 0, 0, 0),
    ("13",   2248, 1600, 2,  0, 0, 0, 0),
    ("14",   2248, 1600, 2,  0, 0, 0, 0),
    ("15",    900, 1600, 1,  0, 0, 0, 0),
    ("16",   2250, 2304, 0,  2, 2, 0, 0),
    ("17",   2250, 2304, 0,  2, 2, 0, 0),
    ("18",   2250, 2304, 0,  2, 2, 0, 0),
    ("19",  17000,  900, 0, 20, 0, 0, 0),
    ("20",   7000, 1100, 0,  7, 1, 0, 0),
    ("21",   1200, 1200, 1,  1, 0, 0, 0),
    ("22",   1500, 1000, 0,  1, 0, 0, 0),
    ("23",   1500, 1000, 0,  1, 0, 0, 0),
    ("24",    900,  525, 1,  0, 0, 0, 0),
    ("25",    900,  525, 1,  0, 0, 0, 0),
    ("26",    900,  525, 1,  0, 0, 0, 0),
    ("27",    900,  525, 1,  0, 0, 0, 0),
    ("28",    900,  525, 1,  0, 0, 0, 0),
    ("29",    900,  300, 0,  0, 0, 0, 0),   # configuration blank in the tender
    ("30",    900,  300, 0,  0, 0, 0, 0),   # configuration blank in the tender
    ("31",    900,  300, 0,  0, 0, 0, 0),   # configuration blank in the tender
    ("32.1", 1800, 1600, 1,  1, 1, 0, 0),   # coupled to 32.2 on the elevation
    ("32.2", 1170, 2100, 0,  0, 0, 1, 0),
    ("33",   1800, 1200, 1,  1, 0, 0, 0),
    ("34.1", 2400, 1600, 1,  2, 1, 0, 0),   # coupled to 34.2 on the elevation
    ("34.2",  900, 2100, 0,  0, 0, 1, 0),
    ("35",   1800, 1200, 1,  1, 0, 0, 0),
    ("36",   1800, 1200, 1,  1, 0, 0, 0),
    ("37",   1200, 2100, 0,  0, 0, 1, 0),
    ("38",   2700, 1700, 0,  6, 0, 0, 0),   # drawn as a 5x3 = 15-pane screen
    ("39",   1200, 2100, 0,  0, 0, 1, 0),   # NOT in the spec's ironmongery list
    ("40",   1200, 1000, 0,  2, 0, 0, 0),
    ("41",   1500, 2100, 0,  0, 0, 0, 1),
]

# js/pricing.js thresholds - the same classifier the house documents use.
WIN_SMALL, WIN_MEDIUM, WIN_LARGE = 2.5, 6.0, 12.0


def code_for(area, sd, dd):
    if dd:
        return "DAD"
    if sd:
        return "SAD"
    if area <= WIN_SMALL:
        return "SAW"
    if area <= WIN_MEDIUM:
        return "MAW"
    if area <= WIN_LARGE:
        return "LAW"
    return "ELAW"


def rate_for(code, area):
    """Learned beats register: what Fenster actually charged, where we have
    enough of it (n>=6), else the supplier-quote median for the band."""
    lr = engine.learned_rate(code, area)
    if lr is not None:
        return lr.rate, lr.provenance, "LEARNED"
    family = "aluminium door, glazed" if code in ("SAD", "DAD") \
        else "aluminium casement window, glazed"
    r = engine.find_rate(family, area)
    if r is None:
        raise ValueError("no rate for %s at %.2f m2" % (code, area))
    return r.rate, r.provenance, "REGISTER"


def main():
    lines, rows = [], []
    for ref, w, h, th, fl, fp, sd, dd in SCHEDULE:
        area = w / 1000.0 * h / 1000.0
        code = code_for(area, sd, dd)
        rate, prov, basis = rate_for(code, area)
        line = engine.price_line(code, w, h, qty=1, supply_rate=rate)
        line["ref"], line["provenance"], line["basis"] = ref, prov, basis
        line["rate_per_m2"] = round(rate, 2)
        line["config"] = {"TH": th, "FL": fl, "FP": fp, "SD": sd, "DD": dd}
        lines.append(line)
        rows.append((ref, w, h, code, area, rate, line["unit_rate"], line["labour"], basis))

    job = engine.price_job(lines)
    area_total = sum(l["area_m2"] for l in lines)

    # Solar-control glass premium. The spec demands a 4mm bronze anti-sun
    # toughened outer pane; the learned/register frame rates are built from
    # ordinary softcoat units. Register glass medians differ by this much.
    solar_premium_m2 = 103.03 - 89.74
    solar_premium = area_total * solar_premium_m2

    print("REDDITCH LIBRARY BLBS0956 - TAKE-OFF AND BENCHMARK PRICE")
    print("=" * 108)
    print("%-6s %-12s %-5s %7s %10s %12s %8s  %s"
          % ("ref", "size mm", "code", "m2", "GBP/m2", "unit rate", "labour", "basis"))
    print("-" * 108)
    for ref, w, h, code, area, rate, unit, lab, basis in rows:
        print("%-6s %-12s %-5s %7.3f %10.2f %12s %8.2f  %s"
              % (ref, "%d x %d" % (w, h), code, area, rate,
                 "{:,.2f}".format(unit), lab, basis))
    print("-" * 108)
    print("%d items, %.2f m2" % (len(lines), area_total))
    print()
    print("  Frames + code adders          GBP %12s" % "{:,.2f}".format(job["items"]))
    print("  Installation (fit only)       GBP %12s" % "{:,.2f}".format(job["installation"]))
    print("  Solar-control glass premium   GBP %12s   (%.2f m2 x GBP%.2f/m2)"
          % ("{:,.2f}".format(solar_premium), area_total, solar_premium_m2))
    print("  " + "-" * 46)
    net = job["total_ex_vat"] + solar_premium
    print("  BENCHMARK NET ex VAT          GBP %12s" % "{:,.2f}".format(net))
    print()
    print("  NOT INCLUDED - no rate exists on file:")
    print("    Strip out existing windows and doors (Gleeds asks for this as a")
    print("    separate priced line, p70). House labour codes are FIT ONLY -")
    print("    proven on Princess Beatrice, Brocks Hill, Crestwood, Georgie's.")
    print("    REQ-24 / REQ-29 open with Adam.                          TBC")
    print("    Provisional sum, preparing openings (Gleeds cl.10)   GBP 5,000.00")
    print()

    by_code = {}
    for l in lines:
        b = by_code.setdefault(l["code"], {"n": 0, "m2": 0.0, "val": 0.0})
        b["n"] += 1
        b["m2"] += l["area_m2"]
        b["val"] += l["line_total"]
    print("  by code:")
    for c, b in sorted(by_code.items(), key=lambda kv: -kv[1]["val"]):
        print("    %-5s %2d items %8.2f m2  GBP %12s"
              % (c, b["n"], b["m2"], "{:,.2f}".format(b["val"])))
    print()
    band = {}
    for l in lines:
        band.setdefault(engine.band_of(l["area_m2"]), []).append(l)
    print("  by size band (the register's known weak spots):")
    for bnd in ("<1.5m2", "1.5-3m2", "3-6m2", ">6m2"):
        ls = band.get(bnd, [])
        if ls:
            print("    %-9s %2d items %8.2f m2  GBP %12s"
                  % (bnd, len(ls), sum(l["area_m2"] for l in ls),
                     "{:,.2f}".format(sum(l["line_total"] for l in ls))))

    out = {
        "job": "Redditch Library BLBS0956",
        "source": "Gleeds blank pricing schedule p77 + Joedan Appendix 2 p150 (identical rows)",
        "items": len(lines), "area_m2": round(area_total, 3),
        "frames_and_adders": job["items"], "installation": job["installation"],
        "solar_glass_premium": round(solar_premium, 2),
        "benchmark_net_ex_vat": round(net, 2),
        "excluded_no_rate": ["strip out existing windows and doors"],
        "provisional_sums": {"preparing openings (Gleeds cl.10)": 5000.00},
        "lines": lines,
    }
    path = os.path.join(REPO, "outputs", "redditch-takeoff.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("\nwritten %s" % path)
    return net


if __name__ == "__main__":
    main()

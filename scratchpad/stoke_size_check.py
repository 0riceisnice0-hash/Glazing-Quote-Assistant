# -*- coding: utf-8 -*-
"""Stoke Park - does the Vetroseal quote match the Aplus FINAL pane sizes?

The pane-count question is settled (the 46 'missing' panes are the louvre/panel
positions - Aplus panel order QT50932 Rev7). This asks the separate question the
louvre answer does not touch: are the panes Vetroseal DID quote the right size?
"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import importlib.util

spec = importlib.util.spec_from_file_location(
    "cmp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts",
                        "stoke-glass-compare.py"))
cmp_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp_mod)

# The 46 panel/louvre positions, from Aplus panel order QT50932 Rev7 (01/07/2026):
# ref A1 on every bay of window Types A/B/C/D/F/G (41 - Type G carries A1 and F1),
# the head panel over doors D02 and D04, and all three panels of Door Type C (D03).
LOUVRE_WINDOW_TYPES = {"Type A", "Type B", "Type C", "Type D", "Type F", "Type G"}


def is_louvre(r):
    if r["type"] in LOUVRE_WINDOW_TYPES and r["ref"] in ("A1", "F1"):
        return True
    if r["type"] == "Door Type C":
        return True
    if r["type"] in ("Door Type B1", "Door Type B2") and r["ref"] == "A1":
        return True
    return False


def main():
    aplus = cmp_mod.read_aplus()
    vetro = cmp_mod.read_vetroseal()

    order = [r for r in aplus if r["thickness"] != "DO NOT ORDER"]
    louvre = [r for r in order if is_louvre(r)]
    glass = [r for r in order if not is_louvre(r)]

    print("Aplus final list, panes to order      : %3d / %6.2f m2"
          % (sum(r["qty"] for r in order), sum(r["area"] for r in order)))
    print("  of which louvre/panel positions     : %3d / %6.2f m2"
          % (sum(r["qty"] for r in louvre), sum(r["area"] for r in louvre)))
    print("  leaving GLASS to buy                : %3d / %6.2f m2"
          % (sum(r["qty"] for r in glass), sum(r["area"] for r in glass)))
    print("Vetroseal 064542 quoted               : %3d / %6.2f m2"
          % (sum(r["qty"] for r in vetro), sum(r["area"] for r in vetro)))
    print()

    # 32mm requirement, once the louvre positions are taken out.
    mm32 = [r for r in glass if r["thickness"] == "32mm"]
    print("32mm GLASS still required             : %d panes / %.3f m2"
          % (sum(r["qty"] for r in mm32), sum(r["area"] for r in mm32)))
    for r in mm32:
        print("    %-16s %s %dx%d" % (r["type"], r["ref"], r["w"], r["h"]))
    print("Vetroseal lines quoted at 32mm        : 0 (all 58 lines are 8.8L-16-4T, 28.8mm)")
    print()

    # Size match: does each quoted pane exist at that exact size on the final list?
    need = collections.Counter()
    for r in glass:
        need[(r["w"], r["h"])] += r["qty"]
    have = collections.Counter()
    for r in vetro:
        have[(r["w"], r["h"])] += r["qty"]

    matched = sum(min(need[k], have[k]) for k in have)
    print("PANE-SIZE MATCH (exact width x height)")
    print("  quoted panes whose size appears on the final list : %d of %d"
          % (matched, sum(have.values())))
    print("  quoted panes at a size NOT on the final list      : %d"
          % (sum(have.values()) - matched))
    print()

    print("Every quoted size against its nearest final-list size, by type:")
    hdr = "  %-14s %-13s %-13s %s" % ("type", "quoted", "final", "shift")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    ref_map = {v: k for k, v in cmp_mod.QUOTE_REF.items()}
    by_type = collections.defaultdict(list)
    for r in glass:
        by_type[r["type"]].append(r)
    for v in vetro:
        typ = ref_map.get(v["ref"], v["ref"])
        if v["ref"] == "TYPE/j":
            cands = by_type["Type J1"] + by_type["Type J2"]
            typ = "Type J1/J2"
        else:
            cands = by_type.get(typ, [])
        if not cands:
            print("  %-14s %-13s %-13s %s" % (typ, "%dx%d" % (v["w"], v["h"]), "?", "?"))
            continue
        best = min(cands, key=lambda r: abs(r["w"] - v["w"]) + abs(r["h"] - v["h"]))
        dw, dh = best["w"] - v["w"], best["h"] - v["h"]
        flag = "" if (dw, dh) == (0, 0) else "  <-- differs"
        print("  %-14s %-13s %-13s %+5d x %+5d%s"
              % (typ, "%dx%d" % (v["w"], v["h"]), "%dx%d" % (best["w"], best["h"]),
                 dw, dh, flag))

    # Money on the corrected basis.
    v_goods = sum(r["total"] for r in vetro)
    v_area = sum(r["area"] for r in vetro)
    rate = v_goods / v_area
    surcharge = 436.52 / v_area
    g_area = sum(r["area"] for r in glass)
    print()
    print("MONEY on the corrected (louvres removed) basis")
    print("  glass area actually required        : %.2f m2" % g_area)
    print("  Vetroseal quoted area               : %.2f m2" % v_area)
    print("  difference                          : %+.2f m2" % (g_area - v_area))
    print("  Vetroseal rate                      : GBP %.2f/m2 goods + %.2f/m2 energy"
          % (rate, surcharge))
    print("  Vetroseal at its own rate on %.2f m2: GBP %.2f" % (g_area, g_area * (rate + surcharge)))
    print("  quoted net                          : GBP 12,012.88")
    print("  CN Glass GBP 60/m2 inc energy       : GBP %.2f" % (g_area * 60))
    print("  indicative saving vs Vetroseal      : GBP %.2f" % (g_area * (rate + surcharge) - g_area * 60))


if __name__ == "__main__":
    main()

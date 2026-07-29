# Reproduce the Grange Hill supplier-backed sell, line by line, through the engine.
#
# Supply is the supplier's own money, so it is fixed: BSW QT253562 line prices are
# already net ("Net Price Includes Discounts"); Bellview 0000000520 line prices are
# PRE-discount, so each one takes the 15% first. Total supply GBP 22,831.09.
#
# What is NOT fixed is which house product code each unit was priced under, and the
# code drives both the template adder (code value x 75%, or x125% above 6m2) and the
# labour. This searches the code assignment by dynamic programming over the
# adder+labour target rather than brute force - 5.3M combinations do not finish.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_pricing as p

DISC = 0.85
TARGET_SELL = 37278.59

WINDOWS = [
    ("QT253562 item 1  window 1200x3000",   1200, 3000,  861.33, ["SAW", "MAW", "LAW", "ELAW"]),
    ("QT253562 item 3  window 1200x3000",   1200, 3000,  861.33, ["SAW", "MAW", "LAW", "ELAW"]),
    ("QT253562 item 2  window 1200x1183",   1200, 1183,  407.57, ["SAW", "MAW"]),
    ("QT253562 item 4  window 1200x1183",   1200, 1183,  407.57, ["SAW", "MAW"]),
    ("QT253562 item 5  window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 6  window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 7  window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 8  window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 9  window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 10 window 1200x1183",   1200, 1183,  419.32, ["SAW", "MAW"]),
    ("QT253562 item 11 window 2000x2100",   2000, 2100,  967.14, ["SAW", "MAW", "LAW", "ELAW"]),
    ("QT253562 item 12 shaped 2900x2400",   2900, 2400, 1788.85, ["MAW", "LAW", "ELAW"]),
    ("QT253562 item 13 shaped 2900x2375",   2900, 2375, 1667.30, ["MAW", "LAW", "ELAW"]),
]
DOORS = [
    ("0000000520 001 single door 1200x2100",  1200, 2100, 3247.82 * DISC, ["SAD", "SUPD", "SADSAW", "SADMAW"]),
    ("0000000520 002 door+2 fixed 4588x2100", 4588, 2100, 5221.89 * DISC, ["SAD", "SADSAW", "SADMAW", "SADLAW", "DAD"]),
    ("0000000520 003 dbl door+2fx 5900x2300", 5900, 2300, 7240.97 * DISC, ["SAD", "SADSAW", "SADMAW", "SADLAW", "DAD"]),
]
LINES = WINDOWS + DOORS

SUPPLY = round(sum(l[3] for l in LINES), 2)
TARGET_EXTRA = round(TARGET_SELL - SUPPLY, 2)


def extra(code, w, h):
    """adder + labour for one unit - everything the code decides."""
    area = (w / 1000.0) * (h / 1000.0)
    return round(p.CODE_VALUE.get(code, 0) * p.adder_factor(area) + p.LABOUR.get(code, 0), 2)


print("supply (supplier's own money, fixed)  GBP %10s" % "{:,.2f}".format(SUPPLY))
print("target sell                           GBP %10s" % "{:,.2f}".format(TARGET_SELL))
print("=> adder + labour must come to        GBP %10s\n" % "{:,.2f}".format(TARGET_EXTRA))

# DP over cumulative pence, keeping one witness path per reachable total.
states = {0: []}
for ref, w, h, price, codes in LINES:
    nxt = {}
    for total, path in states.items():
        for code in codes:
            t = total + int(round(extra(code, w, h) * 100))
            if t <= int(round(TARGET_EXTRA * 100)) and t not in nxt:
                nxt[t] = path + [code]
    states = nxt

want = int(round(TARGET_EXTRA * 100))
if want not in states:
    print("NO code assignment reproduces GBP %.2f." % TARGET_SELL)
    near = sorted(states, key=lambda t: abs(t - want))[:5]
    for t in near:
        print("   closest reachable: GBP %s  (sell GBP %s)"
              % ("{:,.2f}".format(t / 100.0), "{:,.2f}".format(SUPPLY + t / 100.0)))
    sys.exit(1)

combo = states[want]
print("%-40s %-7s %8s %10s %9s %8s %11s"
      % ("unit", "code", "m2", "buy", "adder", "labour", "SELL"))
items = install = 0.0
for (ref, w, h, price, _), code in zip(LINES, combo):
    area = (w / 1000.0) * (h / 1000.0)
    l = p.price_line(code, w, h, supply_rate=price / area)
    items += l["line_total"]
    install += l["labour"]
    print("%-40s %-7s %8.3f %10s %9s %8s %11s"
          % (ref, code, l["area_m2"], "{:,.2f}".format(price), "{:,.2f}".format(l["adder"]),
             "{:,.2f}".format(l["labour"]), "{:,.2f}".format(l["line_total"] + l["labour"])))
print("-" * 100)
print("%-40s %-7s %8.3f %10s %9s %8s %11s"
      % ("TOTAL - supplier backed", "", sum((w / 1000.0) * (h / 1000.0) for _, w, h, _, _ in LINES),
         "{:,.2f}".format(SUPPLY), "", "{:,.2f}".format(install), "{:,.2f}".format(items + install)))
print("\nplus ALLOW auto door operator (3.13.1)  GBP  3,000.00  - no supplier behind it")
print("plus ALLOW fish manifestations (3.11.2) GBP    250.00  - no supplier behind it")
print("PACKAGE TOTAL EX VAT                    GBP %s" % "{:,.2f}".format(items + install + 3250))

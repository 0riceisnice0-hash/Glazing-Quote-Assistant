import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

d = json.load(open(r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\supplier-rates.json",
                   encoding="utf-8"))
reg = d["register"]

BAND = re.compile(r"\[([^\]]+)\]")
SOLAR = re.compile(r"\s*incl solar control \([^)]*\)", re.I)


def parts(cat):
    band = BAND.search(cat)
    band = band.group(1) if band else ""
    base = BAND.sub("", cat).strip()
    is_solar = bool(re.search(r"incl solar control", base, re.I))
    base = SOLAR.sub("", base).strip()
    return base, band, is_solar


index = {}
for e in reg:
    base, band, is_solar = parts(str(e.get("category", "")))
    index[(e.get("supplier"), base, band, is_solar)] = e

print("LIKE-FOR-LIKE SOLAR CONTROL UPLIFT - same supplier, same product, same size band")
print("=" * 104)
rows = []
for (sup, base, band, is_solar), e in sorted(index.items()):
    if not is_solar:
        continue
    plain = index.get((sup, base, band, False))
    if not plain:
        print("  %-10s %-46s [%-9s] solar %8.2f   NO PLAIN PEER IN THE SAME BAND"
              % (sup, base[:46], band, e["median"]))
        continue
    up = e["median"] - plain["median"]
    pct = 100.0 * up / plain["median"]
    rows.append((sup, base, band, plain["median"], e["median"], up, pct,
                 plain.get("lineCount"), e.get("lineCount")))
    print("  %-10s %-46s [%-9s]" % (sup, base[:46], band))
    print("             plain %8.2f (%s lines)   solar %8.2f (%s lines)   uplift %+8.2f GBP/m2  %+6.1f%%"
          % (plain["median"], plain.get("lineCount"), e["median"], e.get("lineCount"), up, pct))

print()
print("=" * 104)
if rows:
    ups = sorted(r[5] for r in rows)
    pcts = sorted(r[6] for r in rows)
    med_up = ups[len(ups) // 2]
    med_pct = pcts[len(pcts) // 2]
    print("matched pairs: %d" % len(rows))
    print("uplift GBP/m2 : min %+.2f  median %+.2f  max %+.2f" % (ups[0], med_up, ups[-1]))
    print("uplift %%      : min %+.1f%%  median %+.1f%%  max %+.1f%%" % (pcts[0], med_pct, pcts[-1]))

    print()
    print("APPLIED TO ST MARY'S (202.80 m2 total)")
    print("-" * 104)
    for label, area in (("windows only (98 units)", 202.804 - 27.375),
                        ("SMA doors + MC600 CW (9 units)", 27.375),
                        ("whole job", 202.804)):
        print("  %-34s %7.2f m2  ->  at median GBP %+.2f/m2 = GBP %9.2f"
              % (label, area, med_up, area * med_up))

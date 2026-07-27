import json, re, openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant"
d = json.load(open(REPO + r"\data\supplier-rates.json", encoding="utf-8"))
reg = d["register"]
BAND = re.compile(r"\[([^\]]+)\]")
SOLAR = re.compile(r"\s*incl solar control \([^)]*\)", re.I)


def parts(cat):
    b = BAND.search(cat)
    return (SOLAR.sub("", BAND.sub("", cat).strip()).strip(),
            b.group(1) if b else "",
            bool(re.search(r"incl solar control", cat, re.I)))


idx = {}
for e in reg:
    base, band, sol = parts(str(e.get("category", "")))
    idx[(e.get("supplier"), base, band, sol)] = e


def uplift(sup, base, band):
    s = idx.get((sup, base, band, True))
    p = idx.get((sup, base, band, False))
    if not s or not p:
        return None
    return (s["median"] - p["median"], p.get("lineCount"), s.get("lineCount"))


def band_of(a):
    if a < 1.5:  return "<1.5m2"
    if a < 3.0:  return "1.5-3m2"
    if a < 6.0:  return "3-6m2"
    return ">6m2"


P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
     r"\E T & S Construction\St Mary's Refurbishment\1. Estimating\3. Client Quote\SS"
     r"\ET & S Construction - St Mary's Refurbishment Pricing - DO NOT SEND.xlsx")
ws = openpyxl.load_workbook(P, data_only=True)["Pricing Document "]

print("BAND-MATCHED SOLAR CONTROL UPLIFT ON ST MARY'S ACTUAL UNITS")
print("windows -> BSW 'aluminium casement window, glazed';  SMA lines -> Bellview equivalents")
print("=" * 108)
print("%-9s %-13s %4s %8s %9s %11s %12s   %s"
      % ("type", "size", "qty", "m2/ea", "area", "GBP/m2 up", "line total", "evidence (plain/solar lines)"))

tot, unpriced, area_tot = 0.0, [], 0.0
for r in range(9, 48):
    code = ws.cell(r, 2).value
    if not code:
        continue
    desc = str(ws.cell(r, 3).value or "").strip()
    size = str(ws.cell(r, 5).value or "").strip()
    qty = ws.cell(r, 6).value or 0
    per = ws.cell(r, 15).value or 0
    area = per * qty
    area_tot += area
    if r <= 39:
        sup, base = "bsw", "aluminium casement window, glazed"
    elif code == "CW":
        sup, base = "bellview", "aluminium casement window, glazed"   # MC600 screen
    else:
        sup, base = "bellview", "aluminium door, glazed"
    b = band_of(per)
    u = uplift(sup, base, b)
    if u is None:
        unpriced.append((desc, sup, base, b, area))
        print("%-9s %-13s %4d %8.3f %9.3f %11s %12s   no matched pair in [%s]"
              % (desc, size, qty, per, area, "-", "-", b))
        continue
    up, pl, sl = u
    tot += up * area
    print("%-9s %-13s %4d %8.3f %9.3f %11.2f %12.2f   %s %s (%s/%s)"
          % (desc, size, qty, per, area, up, up * area, sup, b, pl, sl))

print("=" * 108)
print("total area                : %.3f m2" % area_tot)
print("BAND-MATCHED UPLIFT TOTAL : GBP %,.2f".replace(",", "") % tot)
print("                            GBP %.2f" % tot)
print("as a blended rate         : GBP %.2f/m2" % (tot / area_tot))
if unpriced:
    print()
    print("NOT COVERED BY A MATCHED PAIR (%d lines, %.3f m2):" % (len(unpriced), sum(u[4] for u in unpriced)))
    for u in unpriced:
        print("   %-9s %s / %s [%s]  %.3f m2" % (u[0], u[1], u[2], u[3], u[4]))

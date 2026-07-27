import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

d = json.load(open(r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\supplier-rates.json",
                   encoding="utf-8"))
reg = d["register"]

print("BUILT:", d["builtAt"], "| SCAN:", d["sourceScan"], "| categories:", len(reg))
print()
print("EVERY CATEGORY MENTIONING SOLAR CONTROL")
print("-" * 100)
solar = []
for e in reg:
    if re.search(r"solar|skn|coolite|suncool|planitherm", str(e.get("category", "")), re.I):
        solar.append(e)
        n = sum(s.get("lines", 0) for s in e.get("sources", []))
        print("  %-12s %-58s median %9.2f  min %8.2f  max %9.2f  lines %d"
              % (e.get("supplier"), e.get("category")[:58], e["median"],
                 e["min"], e["max"], e.get("lineCount", n)))

print()
print("PLAIN (NO COATING) EQUIVALENTS, SAME SUPPLIER")
print("-" * 100)
for e in reg:
    c = str(e.get("category", ""))
    if re.search(r"solar|skn|coolite", c, re.I):
        continue
    if re.search(r"^aluminium (door|window/screen), glazed", c, re.I):
        print("  %-12s %-58s median %9.2f  lines %s"
              % (e.get("supplier"), c[:58], e["median"], e.get("lineCount")))

print()
print("UPLIFT IMPLIED BY THE REGISTER")
print("-" * 100)
for s in solar:
    sup, cat = s.get("supplier"), str(s.get("category"))
    kind = "door" if "door" in cat.lower() else "window/screen"
    peers = [e for e in reg
             if e.get("supplier") == sup
             and not re.search(r"solar|skn|coolite", str(e.get("category")), re.I)
             and re.search(r"^aluminium %s, glazed" % kind, str(e.get("category")), re.I)]
    if not peers:
        print("  %s / %s -> no plain peer" % (sup, cat[:50]))
        continue
    lo = min(p["median"] for p in peers)
    hi = max(p["median"] for p in peers)
    mid = sorted(p["median"] for p in peers)[len(peers) // 2]
    print("  %-10s %-52s" % (sup, cat[:52]))
    print("             solar median %9.2f   plain %s medians %.2f-%.2f (mid %.2f)"
          % (s["median"], kind, lo, hi, mid))
    print("             implied uplift vs mid: %+.2f GBP/m2  (%+.1f%%)"
          % (s["median"] - mid, 100.0 * (s["median"] - mid) / mid))
    for src in s.get("sources", [])[:6]:
        print("               <- %s %s  %s / %s  (%s lines)"
              % (src.get("quoteRef"), src.get("quoteDate"), src.get("client"),
                 src.get("job"), src.get("lines")))

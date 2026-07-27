import pdfplumber, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

IN = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
BASE = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"
        r"\E T & S Construction\St Mary's Refurbishment\1. Estimating")

def grab(path, label, pats):
    try:
        with pdfplumber.open(path) as pdf:
            txt = "\n".join((p.extract_text() or "") for p in pdf.pages)
    except Exception as e:
        print("!!", label, e); return ""
    print("\n" + "=" * 90)
    print(label, "chars=%d" % len(txt))
    for pat in pats:
        hits = list(re.finditer(pat, txt, re.I))
        print("  -- /%s/ : %d hit(s)" % (pat, len(hits)))
        seen = set()
        for m in hits[:6]:
            s = txt[max(0, m.start() - 120): m.start() + 160].replace("\n", " | ")
            if s in seen: continue
            seen.add(s)
            print("     ", s)
    return txt

# 1. the energy spec
grab(os.path.join(IN, "original-08-07", "7.05 - Energy and Carbon Design Guidelines V3",
                  "EDG02 Energy and Carbon Design Guidelines-Building Fabric.pdf"),
     "EDG02 BUILDING FABRIC",
     [r"U-?\s?value", r"W/m", r"curtain", r"glazing", r"door"])

# 2. window schedule as priced
grab(os.path.join(IN, "schedule-09-07", "4.00 - Architectural", "2376-09 window schedule.pdf"),
     "2376-09 WINDOW SCHEDULE (as priced)",
     [r"U-?\s?value", r"1\.4", r"1\.6", r"curtain", r"Secured by Design"])

# 3. Bellview SMA quote - any coating or U value at all?
t = grab(os.path.join(BASE, r"2. Supplier Quotes\BSW\ST MARYS.pdf"),
         "BELLVIEW 0000000483 SMA DOORS + MC600 CW",
         [r"U-?\s?value", r"W/m", r"EcoPlus", r"soft ?coat", r"low-?e", r"argon",
          r"warm ?edge", r"coat", r"thermal"])
print("\n  RAW GLAZING LINES IN BELLVIEW QUOTE:")
for m in re.finditer(r"^.*(?:Lami|Tuff|Glazing|prepared).*$", t, re.M | re.I):
    print("    ", m.group(0).strip()[:120])

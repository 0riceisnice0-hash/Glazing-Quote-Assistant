import re

BS = chr(92)   # backslash
CR = chr(13)
LF = chr(10)

path = "data/jobs/riverside.md"
raw = open(path, encoding="utf-8", newline="").read()

# any lone CR is corruption from a mishandled backslash escape
strays = len(re.findall(CR + "(?!" + LF + ")", raw))
print("stray lone CR:", strays)
raw = re.sub(CR + "(?!" + LF + ")", lambda m: BS + "r", raw)

good = [
    "- `data" + BS + "job-checks" + BS + "riverside-house-aov.json` + fixture `_test-riverside.json`",
    "- Generator: `scratchpad" + BS + "riverside_drawings.py`; job json `test-results" + BS + "riverside-run" + BS + "`",
    "- Quote: filed at `..." + BS + "RRR" + BS + "Riverside" + BS + "1. Estimating" + BS + "2. Supplier Quotes" + BS + "Quotation_QT51518.PDF`",
    "  (and at `test-results" + BS + "mary-inbox" + BS + "processed" + BS + "20260727T0842-xgnwAAAA-att" + BS + "`)",
    "- Pack: `test-results" + BS + "mary-inbox" + BS + "processed" + BS + "20260727T1500-xgqQAAAA-att" + BS + "` - 6 drawings, filed nowhere",
]

lines = raw.split(LF)
start = next(i for i, l in enumerate(lines) if l.startswith("- `data" + BS + "job-checks"))
lines[start:start + len(good)] = good
open(path, "w", encoding="utf-8", newline="").write(LF.join(lines))

check = open(path, encoding="utf-8", newline="").read()
print("stray lone CR after:", len(re.findall(CR + "(?!" + LF + ")", check)))
for l in open(path, encoding="utf-8").read().split(LF)[start - 1:start + len(good)]:
    print("  ", l)

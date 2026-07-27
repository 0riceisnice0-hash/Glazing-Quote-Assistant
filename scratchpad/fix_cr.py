import re

CR = chr(13)
LF = chr(10)
BS = chr(92)

path = "MARY-HANDOVER.md"
raw = open(path, encoding="utf-8", newline="").read()

strays = len(re.findall(CR + "(?!" + LF + ")", raw))
print("stray lone CR before:", strays)

# A lone CR (not part of CRLF) is the corruption: a Windows path where "\r"
# was consumed as an escape. Restore it as literal backslash + r.
# NB: a function replacement, not a template - re.sub would re-interpret the
# two-character string "\r" in a template back into a carriage return.
fixed = re.sub(CR + "(?!" + LF + ")", lambda m: BS + "r", raw)

print("stray lone CR after:", len(re.findall(CR + "(?!" + LF + ")", fixed)))
open(path, "w", encoding="utf-8", newline="").write(fixed)
print("written")

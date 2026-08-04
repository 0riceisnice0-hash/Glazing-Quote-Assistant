import re
src=open("scripts/mary_pricing.py",encoding="utf-8").read()
m=re.search(r"(LABOU?R[A-Z_]*\s*[:=]\s*\{.*?\})",src,re.S)
print(m.group(1)[:900] if m else "not found")
print("---")
for mm in re.finditer(r"\{[^{}]*\"DAD\"\s*:\s*500[^{}]*\}",src,re.S):
    print(mm.group(0)[:600])

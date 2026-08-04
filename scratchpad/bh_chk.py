import re,sys
sys.stdout.reconfigure(encoding="utf-8")
src=open("scripts/mary_checks.py",encoding="utf-8").read()
print("LINES:",src.count(chr(10)))
for m in re.finditer(r"^def (check_\w+)\(.*$",src,re.M):
    print(m.group(1))
print("="*70)
i=src.find("def check_supplier_covers_quantity")
print(src[i:i+2600])

import re,sys
sys.stdout.reconfigure(encoding="utf-8")
src=open("scripts/mary_checks.py",encoding="utf-8").read()
for pat in [r"check_rfq_answered\b", r"^ALL_CHECKS", r"^RULES", r"globals\(\)", r"def run\(", r"def main\("]:
    for m in re.finditer(pat,src,re.M):
        print(pat,"@",src[:m.start()].count(chr(10))+1)
i=src.find("def run(")
print(src[i:i+1200] if i>0 else "no run()")

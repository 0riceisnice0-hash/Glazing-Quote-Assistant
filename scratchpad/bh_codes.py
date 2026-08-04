import sys,os
sys.path.insert(0,"scripts")
import mary_pricing as p
# what codes/adders exist for external doorsets
src=open("scripts/mary_pricing.py",encoding="utf-8").read()
import re
for kw in ["SAD","DAD","STEEL","steel"]:
    for m in re.finditer(r"^.*%s.*$"%kw,src,re.M):
        s=m.group(0).strip()
        if len(s)<160: print(kw,"|",s)

import json,os,io,sys
sys.stdout.reconfigure(encoding="utf-8")
t=open("data/knowledge/adam.md",encoding="utf-8").read()
print("=== adam.md (%d chars) ==="%len(t)); print(t[:5000])

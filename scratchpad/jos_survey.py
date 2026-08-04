import sys, json
from collections import Counter
sys.path.insert(0, "scripts")
import crm, crm_contract

cs = crm._call("/api/crm/contracts")
print("TOTAL", len(cs))
print("status", Counter(c["status"] for c in cs))
print("with site_date", sum(1 for c in cs if c.get("site_date")))
print("with po_ref", sum(1 for c in cs if c.get("po_ref")))
print("keys", sorted(cs[0].keys()))
print("seeded", sum(1 for c in cs if c.get("updated_by") == "crm_seed"))
print("not seeded:")
for c in cs:
    if c.get("updated_by") != "crm_seed":
        print("  ", c["key"], "|", c.get("title"), "|", c.get("value"), "|site:", c.get("site_date"), "|po:", c.get("po_ref"), "|", c.get("status"), "|", c.get("updated_by"))

print("\n=== DETAIL of one real one ===")
for k in ("stoke-park-school", "manor-lodge-school", "pride-rubery-library-remedial", "towcester-vale-local-centre"):
    try:
        d = crm_contract.board(k)
    except Exception as e:
        print(k, "ERR", e); continue
    print("---", k, "board keys:", sorted(d.keys()) if isinstance(d, dict) else type(d))
    print(json.dumps(d)[:1800])
    break

print("\n=== raw contract api ===")
print(json.dumps(crm._call("/api/crm/contract/stoke-park-school"))[:2500])

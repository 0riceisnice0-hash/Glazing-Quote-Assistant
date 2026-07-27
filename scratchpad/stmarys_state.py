# -*- coding: utf-8 -*-
"""Close REQ-5 and put St Mary's on the hub. Read-modify-write in one pass -
the registry got clobbered by a concurrent write earlier, so keep the window short."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

for r in d["requests"]:
    if r["id"] == "REQ-5":
        r["status"] = "answered"
        r["answer"] = (
            "No - the addendum does not change our quote. The only substantive change in "
            "2376-09 rev A is the omission of the magnetic integral blinds, which Fenster had "
            "already excluded on proposal p3 and never priced (no blind appears in the pricing "
            "workbook, BSW QT252799 or Aplus QP70172). Every price-driving attribute of the "
            "window schedule is unchanged - 209 window refs, 38 types, 28 structural opening "
            "sizes, 38 opening patterns, 24 restrictors, 33 U-value notes, 38 SBD notes all "
            "identical. The other two re-issued drawings are a ceiling grid / unisex toilet "
            "(2376-04 rev F) and an access road (2376-05 rev E) - no glazing. GBP 174,546.37 "
            "stands, no revision needed. Two things to raise with ET&S: rev A still carries the "
            "integral blind note on Type AK (W.92/W.93, the 1825x5580 pair, our biggest line at "
            "GBP 17,311.95) so the addendum contradicts itself; and the revisions are dated "
            "13.07.26 and 08.07.26 - BEFORE our 17/07 quote - but were only issued on 24/07, so "
            "we priced a superseded drawing without knowing."
        )
        r["answered_by"] = "Mary (triage chat)"
        r["answered_at"] = "2026-07-27T14:50:00"

d["jobs"].append({
    "job": "St Mary's Refurbishment, Merthyr Tydfil",
    "client": "E T & S Construction",
    "deadline": "2026-08-16",
    "status": (
        "QUOTE SUBMITTED 17/07 at GBP 174,546.37 ex VAT (install GBP 21,915.05; mastic "
        "GBP 2,808.10 and EPDM GBP 5,028.61 optional). St Mary School, Caedraw Rd, Merthyr "
        "Tydfil for Merthyr Tydfil CBC, architect cfw architects. Sheerline Prestige casements, "
        "SMA MC600 Plus curtain walling, SMA Smart Wall Pocket screens and doors; 6.8 lam / 4 "
        "toughened, U-value 1.4. Supplier backing BSW QT252799 + Aplus QP70172. REQ-5 ANSWERED "
        "27/07: ET&S's 24/07 addendum does NOT change our scope - the only change is the "
        "omission of magnetic integral blinds, which we had already excluded and never priced. "
        "Two points to put to ET&S: rev A still shows the blind note on Type AK (W.92/W.93, our "
        "biggest line at GBP 17,311.95), and the revisions were dated 13.07 and 08.07 but only "
        "issued on 24/07, so we priced a superseded drawing without knowing."
    ),
    "value": "GBP 174,546.37 quoted",
    "stage": "submitted",
})

d["updated"] = "2026-07-27T14:50:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("REQ-5 status:", [r["status"] for r in d["requests"] if r["id"] == "REQ-5"])
print("jobs on hub:", len(d["jobs"]))

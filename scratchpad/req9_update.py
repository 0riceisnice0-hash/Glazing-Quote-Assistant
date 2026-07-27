# -*- coding: utf-8 -*-
"""Record Adam's REQ-9 answer, and put back the question it did not settle."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

for r in d["requests"]:
    if r["id"] == "REQ-9":
        r["answer"] = (
            "ADAM 27/07 (hub message 27, which failed three times and was parked - recovered by "
            "triage 20:4x): \"We can make the windows as big as we need to in order to achieve the "
            "free area, because the openings are being newly formed. Drop me an email to remind me "
            "and I will ask Gintare to requote.\" "
            "So size is NOT a constraint - that half is settled and it is useful. NOT CLOSED, "
            "because the question it answers rests on a number that turned out to be ours, not the "
            "client's. The 1.5m2 came from Adam's own 24/07 enquiry to Gintare; the pack drawings "
            "K1653-11 and K1653-12 say \"AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF "
            "1m2\", one per stairwell at top storey. Against 1m2 GEOMETRIC the quoted vent already "
            "clears by 30% (A Plus state 1.30m2 geometric on QT51518) and there is nothing to "
            "requote."
        )
        r["answered_by"] = "Adam (size not constrained), premise corrected by Mary"
        r["needs"] = (
            "One question to the fire engineer or the author of K1653-11 before Gintare is asked for "
            "anything: is the 1m2 requirement GEOMETRIC or AERODYNAMIC free area? A Plus state "
            "geometric only on QT51518. On their QT51516 for the same DualFrame 75Si AOV they state "
            "both, and aerodynamic runs at 60-62% of geometric - so 1.30 geometric is about 0.78-0.81 "
            "aerodynamic. If the requirement is geometric we are 30% clear and no change is needed. "
            "If it is aerodynamic we are roughly 20% short and Adam's answer applies - the opening "
            "grows. The answer decides whether there is any work here at all, so it is worth settling "
            "before spending Gintare's time."
        )
        r["options"] = [
            "Requirement is GEOMETRIC - no resize, close it",
            "Requirement is AERODYNAMIC - resize and requote per Adam",
            "Ask the fire engineer which basis applies",
        ]

d["updated"] = "2026-07-27T20:50:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("REQ-9 updated; open requests:", sum(1 for r in d["requests"] if r["status"] == "open"))

# -*- coding: utf-8 -*-
"""Close REQ-3, raise REQ-11 (sizes), add the Stoke Park job row and the catch."""
import io
import json

P = "data/dashboard-state.json"
with io.open(P, encoding="utf-8") as fh:
    d = json.load(fh)

for r in d["requests"]:
    if r["id"] == "REQ-3":
        r["status"] = "answered"
        r["answer"] = (
            "Adam, 27/07: live project, not a tender - the 46 missing panes are louvres, "
            "glazed in in place of glass, supplied by IKON not Vetroseal. Confirmed at source: "
            "Aplus panel order QT50932 Rev7 is a 46-panel order at exactly those positions, and "
            "IKON Q26-24329 (02/07) prices 46 IKL332 louvre modules at GBP 10,125.91 + carriage. "
            "Take them out and the glass reconciles exactly - 124 panes required, 124 quoted, "
            "+1.73 m2 (about GBP 197). No shortfall; the GBP 2,920 headline is withdrawn. "
            "What survives: (1) every quoted pane and every quoted louvre is dimensioned to a "
            "schedule superseded by the 02/07 re-input - 0 of 124 pane sizes match and all 41 "
            "window louvres are 85mm too tall - now REQ-11; (2) the price carries the 05/06 "
            "quotes (Vetroseal GBP 9,309.22, IKON GBP 7,490.64) against current GBP 12,012.88 "
            "and GBP 10,125.91, so GBP 5,338.93 of cost above the sold price, which moving the "
            "glass to CN Glass at GBP 60/m2 would roughly recover; (3) six 32mm panes "
            "(4.46 m2) are still unpriced by anyone."
        )
        r["answered_by"] = "Adam (dashboard 27/07), verified by Mary"
        r["answered_at"] = "2026-07-27T15:10:00"

d["requests"].append({
    "id": "REQ-11",
    "raised": "2026-07-27",
    "job": "Stoke Park School (Borras)",
    "owner": "Adam or Steve",
    "title": "Glass and louvres are both sized to a superseded schedule - frames land 03/08",
    "why": (
        "Aplus re-input job 17644 on 02/07 and the frames were signed off the same day. "
        "Both buys predate it. Vetroseal 064542 (01/07): not one of the 124 quoted panes "
        "matches an ordered size - vents moved 404 to 448 high on every type, Type H came "
        "down 166mm, every door leaf went 1859 to 2059. IKON Q26-24329 priced the louvres "
        "off the 01/07 panel schedule at 476mm high, but the signed-off A1 aperture is "
        "391mm - all 41 window louvres are 85mm too tall, and the door heads are out by "
        "+245 (D02), +50 (D04) and +78 (D03). The louvres are bespoke and painted, so they "
        "are the longer lead. If either order goes in as quoted, GBP 22,000 of glass and "
        "louvres arrives unusable against a 03/08 frame delivery."
    ),
    "needs": (
        "Someone to go back to Vetroseal (or CN Glass) and to IKON with the apertures off "
        "the signed-off order of 02/07 and get both re-quoted before anything is placed. "
        "Mary cannot email suppliers. Also still open from REQ-3: the make-up for the six "
        "32mm panes, which no quote covers."
    ),
    "options": [
        "Re-issue both enquiries against the signed-off 02/07 sizes",
        "Glass to CN Glass on the final sizes, louvres re-quoted by IKON",
        "Hold both orders until Aplus confirm the apertures",
    ],
    "status": "open",
})

d["jobs"].append({
    "job": "Stoke Park School (Borras)",
    "client": "Borras Construction",
    "deadline": "2026-08-03",
    "status": (
        "LIVE PROJECT, won and in production - Aplus job 17644, Technal Soleal Next FZ75, "
        "frames UNGLAZED supply only, DELIVERY 03/08. Glass and louvres are Fenster's to buy. "
        "REQ-3 closed: the 46 'missing' panes are louvres (IKON Q26-24329, 46 modules, "
        "GBP 10,125.91) and the glass count reconciles exactly at 124. REQ-11 open and urgent: "
        "both the glass and the louvres are dimensioned to the pre-02/07 schedule, so 0 of 124 "
        "pane sizes match and every louvre is 85mm too tall. Cost also runs GBP 5,338.93 above "
        "the sold price because the build-up carries the 05/06 quotes."
    ),
    "value": "GBP 104,660.17 ex VAT (order signed off 17/07)",
})

d.setdefault("catches", []).insert(0, {
    "date": "2026-07-27",
    "job": "Stoke Park School (Borras)",
    "catch": (
        "Aplus re-input the job on 02/07 and signed the frames off the same day, but the glass "
        "quote (01/07) and the louvre schedule IKON priced (01/07) both predate it. Not one of "
        "the 124 quoted panes matches an ordered size and all 41 window louvres are 85mm too "
        "tall. Caught eight days before the frames land on 03/08, from the signed-off order "
        "rather than the quotes."
    ),
    "type": "wrong-sizes-ordered",
    "value": "GBP 22,138.79 of glass and louvres",
})

d["updated"] = "2026-07-27T15:10:00"

with io.open(P, "w", encoding="utf-8") as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

print("REQ-3 answered, REQ-11 raised, job row and catch added")

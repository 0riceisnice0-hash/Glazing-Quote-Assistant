# -*- coding: utf-8 -*-
"""Close REQ-11 - the orders went out on the corrected sizes. Update the job row."""
import io
import json

P = "data/dashboard-state.json"
with io.open(P, encoding="utf-8") as fh:
    d = json.load(fh)

for r in d["requests"]:
    if r["id"] == "REQ-11":
        r["status"] = "answered"
        r["answer"] = (
            "Zac, 28/07: the correct glass sizes went to commercial@fensterglazing.com, which "
            "Mary does not poll, and were received 27/07. Verified against the orders "
            "themselves, now in the job folder under '4. Orders', all dated 27.07.26 and "
            "signed off by Steve Freezer. GLASS - CN Glass, 124 units / 106.946 m2 / "
            "GBP 6,185.09, every pane matching the signed-off 02/07 apertures. LOUVRES - IKON, "
            "44 modules / 20.674 m2 / GBP 7,587.30 at 391mm high, not the 476 quoted, so the "
            "85mm mismatch is gone. PANELS - Metfab, 2no 770x2059 insulated aluminium, which "
            "are D03's two door leaves and why the louvre order is 44 not 46. 170 items / "
            "130.79 m2 = Aplus's final list exactly. The 32mm make-up is answered: Spec C is "
            "8.8 lami / 20mm argon / 4mm toughened at GBP 60/m2. Money improved - the build-up "
            "carried Vetroseal GBP 9,309.22 and IKON GBP 7,490.64 against an actual buy of "
            "GBP 6,185.09 and GBP 7,587.30, so about GBP 3,027 BETTER than the sold price "
            "rather than the GBP 5,339 worse previously reported. Left with Steve, not raised: "
            "the Metfab order carries no rate, and Spec A is 26.8mm on 73 panes Aplus nominate "
            "as 28mm."
        )
        r["answered_by"] = "Zac (dashboard 28/07), verified by Mary against the placed orders"
        r["answered_at"] = "2026-07-28T09:05:00"

for j in d["jobs"]:
    if j["job"].startswith("Stoke Park"):
        j["status"] = (
            "LIVE PROJECT, in production - Aplus job 17644, Technal Soleal Next FZ75, frames "
            "UNGLAZED supply only, DELIVERY 03/08. REQ-3 and REQ-11 both closed. All three "
            "glazing orders were placed 27/07 against the signed-off 02/07 apertures and are "
            "in the job folder under '4. Orders': glass CN Glass 124 units / GBP 6,185.09, "
            "louvres IKON 44 modules / GBP 7,587.30, panels Metfab 2no (unpriced). 170 items / "
            "130.79 m2, matching Aplus's final list. The buy came in about GBP 3,027 UNDER "
            "what the sold price carries, on the CN Glass switch. Open with Steve: the Metfab "
            "rate, and whether Spec A at 26.8mm suits the 28mm beads on 73 panes."
        )

d["updated"] = "2026-07-28T09:05:00"

with io.open(P, "w", encoding="utf-8") as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

print("REQ-11 closed, Stoke Park job row updated")

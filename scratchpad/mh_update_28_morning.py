# -*- coding: utf-8 -*-
"""Morning-update close-out edits to MARY-HANDOVER.md.

Cell-count guard (added after a row was corrupted by an embedded pipe):
every data row in the job table must be exactly three cells. Verified
before AND after the edit, on every row, not just the ones touched here.
"""
import io, sys, re

P = "MARY-HANDOVER.md"
L = io.open(P, encoding="utf-8").read().split("\n")


def rows():
    return [(i, r) for i, r in enumerate(L) if r.startswith("|")]


def guard(where):
    bad = [(i, r.count("|")) for i, r in rows() if r.count("|") != 4]
    if bad:
        print("TABLE GUARD FAILED %s: %s" % (where, bad))
        sys.exit(1)
    print("table guard ok %s - %d rows, all 3 cells" % (where, len(rows())))


guard("before")


def append_cell(idx, cell, text):
    assert "|" not in text, "pipe in appended text would split the row"
    parts = L[idx].split("|")
    parts[cell] = parts[cell].rstrip() + " " + text + " "
    L[idx] = "|".join(parts)


# --- Princess Beatrice: Guildmore's query, Adam's answer, and the gap ------
append_cell(109, 2,
    "**27/07 EVENING - GUILDMORE CAME BACK AND THE ANSWER IS NOT IN OUR DOCUMENTS.** "
    "Jason Mount, 19:21: does the quote allow for removal of the existing windows, and if not what is the "
    "additional sum. Adam answered direct at 19:56: *\"I can confirm we have allowed for strip out of old "
    "frames. We have not allowed for disposal, ie skips on site.\"* **The disposal half matches the issued "
    "proposal exactly** - page 4 reads *\"Waste Removal - Generally excluded unless agreed otherwise\"*. "
    "**The strip-out half appears in no document we issued.** Checked at source 28/07: the proposal PDF "
    "carries no strip-out inclusion on any of its 10 pages (swept for strip / remove / removal / disposal / "
    "skip / waste / make good), the pricing workbook has no strip-out line in its only sheet, and the "
    "GBP 39,680 installation sum recomputes from the labour codes alone. There is also no strip-out rate "
    "anywhere in `data/supplier-rates.json` - it is one of the 21 categories that return zero. So a scope "
    "commitment against a GBP 279,244.69 quotation now exists only in a mail thread. Reported to Adam in the "
    "28/07 morning update with the recommendation that it goes into the corrected proposal in writing.")
append_cell(109, 3,
    "**AND NOW ALSO: put strip-out in the corrected proposal in writing** (it is currently only in Adam's "
    "27/07 19:56 reply to Jason Mount) - which is a second reason to reissue rather than wait to be queried.")

# --- St Mary's: the re-opened return date has now passed -------------------
append_cell(124, 2,
    "**28/07: THE RE-OPENED RETURN DATE (27/07) HAS NOW PASSED AND NOTHING WAS SENT.** The 24/07 Document "
    "Register's *\"Package return date: 27 July 2026\"* came and went with no contact to Tom Godfrey - Mary "
    "cannot make it (adam@/marketing@ only) and outbound was down for the evening in any case. The Estimating "
    "Log still shows 17/07 for this job. The quote check workbook `outputs\\St Marys Refurbishment - Quote "
    "Check and RFI Schedule.xlsx` was the document the 27/07 email outage swallowed; it finally reached Adam "
    "attached to the 28/07 morning update.")

# --- John North Hall: not on the Estimating Log ---------------------------
append_cell(125, 2,
    "**NOT ON THE ESTIMATING LOG** - checked cell by cell 28/07 across all 326 populated rows: zero matches "
    "for *john north*, *wycombe*, and the only *vaughan* is an unrelated 2025 job (Flat 9, 3 Vaughan Road). "
    "Reported in the 28/07 morning update. There is a month to the 24/08 close so nothing is at risk yet, "
    "but it has no log number and no owner.")

# --- Storm / Maternity Assessment Unit ------------------------------------
append_cell(127, 2,
    "**ADAM CONFIRMED IT IS REAL, 27/07 19:17 (reply to Mary):** *\"I called Storm and it turns out there is "
    "some secondary glazing on the job, so it was worth the chase. Please bear in mind we do offer secondary "
    "glazing.\"* **Standing fact: Fenster DO offer secondary glazing** - do not treat a secondary-glazing "
    "enquiry as out of scope. This job is NOT on the Estimating Log either (checked 28/07); flagged in the "
    "morning update as one to log when Nilesh's details land.")

# --- Last updated line ----------------------------------------------------
for i, r in enumerate(L[:6]):
    if r.startswith("Last updated:"):
        L[i] = ("Last updated: 2026-07-28 (morning update sent 07:54 to adam+marketing - Estimating Log "
                "cross-checked against estimating@; outbound email restored after the 27/07 tenant block, "
                "last good send before it was 27/07 16:31 and `data/mary-send-log.jsonl` now dates every "
                "attempt; St Mary's re-opened return date passed unactioned; Guildmore strip-out committed "
                "by email but absent from the issued proposal and pricing; John North Hall and the Storm "
                "secondary-glazing enquiry are both absent from the Estimating Log). " + r[len("Last updated: "):])
        break

guard("after")
io.open(P, "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("MARY-HANDOVER.md written")

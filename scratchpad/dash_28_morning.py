# -*- coding: utf-8 -*-
"""Dashboard close-out for the 28/07 morning update."""
import io, json

P = "data/dashboard-state.json"
d = json.load(io.open(P, encoding="utf-8"))
d["updated"] = "2026-07-28"

req = {r["id"]: r for r in d["requests"]}

# --- REQ-23 answered: outbound is back, and the outage now has a timeline ---
r = req["REQ-23"]
r["status"] = "answered"
r["answer"] = (
    "Fixed at the tenant and verified this morning. The READER identity reads mary@ again - HTTP 200 where "
    "it returned 403 '[RAOP] Blocked by tenant configured AppOnly AccessPolicy' yesterday - and the 28/07 "
    "morning update sent to adam@ + marketing@ at 07:54 with an attachment, confirmed in mary@'s own Sent "
    "Items. mary@ is back inside the app policy and the Exchange transport rule cage is untouched, so nothing "
    "was routed through estimating@ as a workaround. AND THE OUTAGE CAN NOW BE DATED, which it could not be "
    "yesterday: the last successful send before the block was 27/07 16:31 (the Storm Building note), readable "
    "in Sent Items now the mailbox is reachable. So the window ran from after 16:31 on 27/07 to before 07:54 "
    "on 28/07, and exactly two documents were generated inside it, both St Mary's - the quote check workbook "
    "(21:09) and the revised clarifications draft (22:08). The workbook went to Adam attached to this "
    "morning's update. data/mary-send-log.jsonl now holds its first entry, so a future outage will not have "
    "to be dated from inside the mailbox it blocks.")
r["answered_by"] = "Mary (triage chat) - verified at source"
r["answered_at"] = "2026-07-28T07:54:00"

# --- REQ-25: the re-opened return date has now passed ---
r = req["REQ-25"]
r["why"] = r["why"] + (
    " || 28/07 07:50 - THE DATE HAS NOW PASSED. Nothing was put to Tom Godfrey yesterday, the resubmission "
    "never went, and the Estimating Log still carries 17/07 for this job. The question is no longer 'is the "
    "package open until close of play' but 'was it, and will ET&S accept a corrected set now'. The draft "
    "changes no figure - GBP 174,546.37 stands - so what the miss costs is the eleven qualifications, not "
    "the price. Reported to Adam in the 28/07 morning update, with the quote check workbook finally "
    "attached (it was one of the two documents the email outage swallowed).")

# --- REQ-29: a scope inclusion that exists only in a mail thread ---
d["requests"].append({
    "id": "REQ-29",
    "raised": "2026-07-28",
    "job": "Princess Beatrice House (Guildmore Planned Works)",
    "owner": "Adam",
    "title": "We have told Guildmore strip-out is included and neither document we issued says so",
    "why": (
        "Jason Mount asked at 19:21 on 27/07 whether removal of the existing windows is allowed for, and what "
        "the extra would be if not. Adam answered direct at 19:56: 'I can confirm we have allowed for strip "
        "out of old frames. We have not allowed for disposal, ie skips on site.' The disposal half matches "
        "the issued proposal word for word - page 4 reads 'Waste Removal - Generally excluded unless agreed "
        "otherwise'. The strip-out half appears in nothing we issued. Checked at source: no strip-out "
        "inclusion on any of the proposal's 10 pages (swept for strip / remove / removal / disposal / skip / "
        "waste / make good), no strip-out line in the pricing workbook's only sheet, and the GBP 39,680 "
        "installation sum recomputes from the labour codes alone. There is also no strip-out rate anywhere in "
        "data/supplier-rates.json - one of the 21 categories that return zero - so even pricing it would be a "
        "benchmark rather than a rate. A scope commitment against a GBP 279,244.69 quotation now exists only "
        "in a mail thread."),
    "needs": (
        "State strip-out as an inclusion in the corrected proposal, in writing. That is the same document "
        "REQ-6 has been asking about since 27/07 - the mastic charged at GBP 5,356.22 while page 3 calls it "
        "an optional extra, and EPDM at GBP 8,276.91 absent from the clarifications - so there are now three "
        "corrections for one reissue rather than two. If the answer is to leave it in the thread instead, say "
        "so and I will record it as a known exposure rather than an open item."),
    "options": [
        "Reissue the proposal with strip-out stated as included, and fix mastic/EPDM in the same pass (REQ-6)",
        "Leave it in the thread - the email is enough",
        "Price strip-out as a variation and put a figure to Guildmore",
    ],
    "status": "open",
    "answer": None,
    "answered_by": None,
    "answered_at": None,
})

# --- REQ-30: log gaps found by this morning's cross-check ---
d["requests"].append({
    "id": "REQ-30",
    "raised": "2026-07-28",
    "job": "Estimating Log housekeeping",
    "owner": "Adam / Gintare",
    "title": "A live ITT is on nobody's log, and no forward job on the log names a controller",
    "why": (
        "This morning's cross-check of the Estimating Log (326 populated rows, last saved 27/07 16:51) "
        "against estimating@. John North Hall, 1-39 Vaughan House, High Wycombe - ITT from Jordan Jones at "
        "Neil Douglas, in at 16:56 on 27/07 via info@, tender due 9am Monday 24 August, five communal "
        "entrance door sets - is not on the log at all: zero rows match 'john north' or 'wycombe', and the "
        "only 'vaughan' is an unrelated 2025 job. The Maternity Assessment Unit secondary-glazing enquiry "
        "Adam chased with Storm on 27/07 is not on it either. Riverside reads 'to log' with no number, no "
        "enquiry date, no deadline and no controller against a live priced job at GBP 5,990.22. Lower Range "
        "Road has its 07/08 deadline but no log number. St Mary's still shows 17/07 where ET&S's 24/07 "
        "register says 27/07. Six rows carry a deadline of today or later and none of the six names a "
        "controller. Grange Hill 8740, Georgie's 8741 and Vesuvius 8742 - Saturday's three 'to log' entries "
        "- have all been cleared, so the log is being kept; these are the gaps left."),
    "needs": (
        "Someone to log John North Hall and give it an owner - there is a month to the close so nothing is at "
        "risk yet, and Jordan Jones has offered a site meeting, which is the part with a shorter fuse. Plus a "
        "controller named against the six forward rows, and the St Mary's deadline corrected to 27/07."),
    "options": [
        "Gintare picks all of it up",
        "Mary drafts the log rows and Gintare pastes them in",
        "Log John North Hall now, leave the rest until after Friday's deadlines",
    ],
    "status": "open",
    "answer": None,
    "answered_by": None,
    "answered_at": None,
})

# --- the catch ---
d["catches"].insert(0, {
    "date": "2026-07-28",
    "job": "Princess Beatrice House",
    "catch": (
        "Adam told Guildmore by email that strip-out of the old frames is allowed for and disposal is not. "
        "The disposal half is in the issued proposal word for word ('Waste Removal - Generally excluded "
        "unless agreed otherwise', page 4). The strip-out half is in nothing we issued - not on any of the "
        "proposal's 10 pages, not as a line in the pricing workbook, and not inside the GBP 39,680 "
        "installation sum, which recomputes from the labour codes alone. We hold no strip-out rate either: "
        "it is one of the 21 register categories that return zero. Found by sweeping the issued PDF rather "
        "than the job record - the job record says what we meant to include, the document says what the "
        "client can hold us to."),
    "type": "scope / commercial exposure",
    "value": "an inclusion on a GBP 279,244.69 quotation that exists only in a mail thread",
})

json.dump(d, io.open(P, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("dashboard-state.json updated: REQ-23 answered, REQ-25 updated, REQ-29/REQ-30 raised, 1 catch")

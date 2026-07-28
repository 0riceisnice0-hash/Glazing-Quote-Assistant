# -*- coding: utf-8 -*-
"""Insert the 28/07 morning-update record into HANDOVER.md above '## Next Best Work'."""
import io

REC = u"""
### Morning update 28/07 - the Estimating Log against the inbox, and an inclusion that lives only in a thread (2026-07-28)

Sent 07:54 to adam@ + marketing@, subject *"Morning update 28/07 - 2 close today, St Mary's return date was
yesterday, and our Guildmore proposal does not say what we told them"*, with
`outputs\\St Marys Refurbishment - Quote Check and RFI Schedule.xlsx` attached. Body kept at
`scratchpad\\morning-28-07.txt`; layout screenshot-verified through `mary_preview.py` before sending.

**OUTBOUND IS BACK, AND THE OUTAGE CAN NOW BE DATED.** REQ-23's tenant block on mary@ is lifted: the READER
identity reads mary@ again (HTTP 200, not the `[RAOP] Blocked by tenant configured AppOnly AccessPolicy` 403),
and this send went through. **The last successful send before the block was 27/07 16:31** - the Storm Building
note - which is readable in mary@'s own Sent Items now that the mailbox is reachable again. So the outage ran
from some point after 16:31 on 27/07 to before 07:54 on 28/07, and everything generated inside that window was
undelivered. That was two documents, both St Mary's: the quote check workbook (21:09) and the revised
clarifications draft (22:08). The workbook went with this morning's email. `data/mary-send-log.jsonl` now has
its first entry, so the next outage will not have to be dated from the inside of the mailbox it blocks.

**THE FINDING WORTH KEEPING: A SCOPE INCLUSION THAT EXISTS ONLY IN A MAIL THREAD.** Jason Mount asked
Guildmore's question at 19:21 - is removal of the existing windows allowed for, and if not what is the extra.
Adam answered at 19:56: strip out of old frames allowed, disposal and skips not.

    disposal   "Waste Removal - Generally excluded unless agreed otherwise"   proposal p4   MATCHES
    strip-out  no inclusion in the proposal, no line in the pricing           nowhere       DOES NOT

Checked at source rather than from the job record: all 10 pages of the issued proposal swept for
strip / remove / removal / disposal / skip / waste / make good - the only hits are that Waste Removal
clarification and a final-clean line; the issued pricing workbook has one sheet and no cell matching any of
those words; the GBP 39,680 installation sum recomputes from the labour codes alone. **And we hold no
strip-out rate at all** - it is one of the 21 register categories that return zero, so even pricing the
answer would have been a benchmark rather than a rate.

**Generalisable: when somebody answers a client's scope question by email, the question to run is not whether
the answer is right - it is whether the documents we issued say the same thing.** Half of Adam's answer was
already in the proposal word for word. The other half is now a commitment against a GBP 279,244.69 quotation
that is silent on it. It costs one sweep of the issued PDF to find out which half is which. And it strengthens
the case for reissuing Princess Beatrice rather than waiting to be queried, which REQ-6 has been asking since
27/07 - there are now three things to correct in one document rather than two.

**St Mary's: the re-opened return date passed unactioned.** ET&S's 24/07 Document Register header says
*"Package return date: 27 July 2026"*. Nobody put that to Tom Godfrey, the resubmission never went, and the
Estimating Log still carries 17/07. The draft changes no figure - GBP 174,546.37 stands - so the cost of the
miss is the qualifications, not the price.

**THE LOG CROSS-CHECK.** `Estimating Log.xlsx` (sheet "Estimating Log", 326 populated rows, last saved 27/07
16:51) read against estimating@ for the same period:

| | |
|---|---|
| **John North Hall, High Wycombe** | ITT in 27/07 16:56 via info@, closes 9am 24/08 - **not on the log at all** (zero rows match *john north* or *wycombe*; the only *vaughan* is an unrelated 2025 job) |
| **Maternity Assessment Unit (Storm)** | Adam asked Nilesh for details 27/07 - **not on the log** |
| **Riverside (rrr-group)** | on the log but reads "to log": no number, no enquiry date, no deadline, no controller - against a live priced job at GBP 5,990.22 |
| **Lower Range Road (Ermine)** | logged with the 07/08 deadline, still no log number |
| **St Mary's** | shows 17/07; the 24/07 register says 27/07 |
| **Grange Hill 8740, Georgie's 8741, Vesuvius 8742** | all three of Saturday's "to log" entries now carry numbers - Gintare cleared them |

Six rows carry a deadline of today or later and **none of the six names a controller**. Mary's board carries
more live deadlines than the log does, and the difference is John North Hall.

**And Adam's own reply of 27/07 19:17 is a standing fact, not a job note:** *"I called Storm and it turns out
there is some secondary glazing on the job, so it was worth the chase. Please bear in mind we do offer
secondary glazing."* Fenster offer secondary glazing - a secondary-glazing enquiry is not out of scope.

Positions unchanged and nothing issued: Grange Hill GBP 27,560.07 benchmark and Georgie's both close today,
Filwood and Vesuvius Thursday, Brocks Hill Friday.

"""

P = "HANDOVER.md"
txt = io.open(P, encoding="utf-8").read()
anchor = u"\n## Next Best Work"
assert txt.count(anchor) == 1, "anchor not unique"
txt = txt.replace(anchor, REC + anchor)
io.open(P, "w", encoding="utf-8", newline="\n").write(txt)
print("HANDOVER.md record inserted")

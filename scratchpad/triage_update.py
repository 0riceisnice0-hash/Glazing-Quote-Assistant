# -*- coding: utf-8 -*-
"""Add the 04/08 batch entry to triage.md and keep the file inside the 300-line contract."""
p = "data/jobs/triage.md"
d = open(p, encoding="utf-8").read()
print("before:", len(d.split("\n")))

NEW = """- **04/08 - A BATCH OF 78, WORKED AS ONE PICTURE: 37 ROUTED, 37 CLEARED, THREE NEW CHATS OPENED.**
  Routed to their owners: brocks-hill (15 - the SMDT0173 run where Adam asked Martin Moore about the
  7 excluded doors and got "include for the additional doors"), filwood (5 - Adam's 11:55 fixes, and
  it ISSUED 12:28 with Adam Warner acknowledging at 12:35), redditch-library (3), john-north-hall (2),
  vesuvius (1). **NEW CHATS:** `totteridge` (Borras T0689 - cost review due **FRIDAY 07/08**, no design
  change, programme only; **we also quoted the same scheme for CONAMAR**, so a Borras-only search finds
  half the evidence; the cost basis is County Architectural Aluminium and their quote is not itemised
  per unit), `addison-ave` (Harris Calnan - a **product substitution against an already-approved Fabco
  product**, so the detail drawing, installed photos and thermal evidence ARE the job; Gintare's "are
  we doing the internal doors?" is unanswered and decides scope), `alice-billings` (Sinden via the
  **eque2 portal, PIN 4296 - a FOURTH portal client**; Gintare's BoQ-vs-schedules question is open and
  is the Stepnell trap exactly; same contractor as Alkerden, where we already owe a quote).
- **04/08 - TWO SUPPLIER CHANGES THAT PUT A DATE ON LIVE WORK.** **Martin Gregory has RESIGNED from CN
  Glass** - and he is the man who agreed the GBP 60/m2 verbal rate that Stoke Park's 27/07 glass order
  (124 units, GBP 6,185.09) was placed against, on an email rather than a quotation document. **A
  verbal rate is only as durable as the person who gave it.** And **AGF: Reynaers rises on all orders
  placed on or after 27/08** - a hard date that lands straight on Totteridge's 07/08 review.
- **04/08 - AND A RATE-MINING DEFECT WORTH MORE THAN THE THREE QUOTES.** Vetroseal bill a DELIVERY
  CHARGE as a glass line carrying a **fake 0.300 m2** (065311, MK40): divide goods by total area and
  the rate reads GBP 86.62/m2 against a true GBP 82.99/m2, **4.4% high, silently**. Exclude charge
  lines when mining. New lines: 10.8mm lami GBP 82.99/m2, 6.8mm lami GBP 34.65/m2. Also **MHA Nuneaton
  is being priced TWO WAYS** - the same 8 units as a DGU (GBP 526.08) and as single 6.8 laminate
  (GBP 347.20) - still with no enquiry in estimating@ and no folder. And **ELEVATION/BEDFORD is Paul's
  MK40 emergency board-up**: Vetroseal's 3145 x 2103 answers the size question AE Glaziers asked on
  03/08, so nobody needs to re-measure."""

anchor = "## Decisions\n\n"
assert anchor in d
d = d.replace(anchor, anchor + NEW + "\n", 1)

# Compress the closed Brandon Estate entry to keep inside the contract.
OLD_BRANDON_START = "- **29/07 - Brandon Estate (Elkins) answered for Jacob, botmsg-18. It is HIS.**"
i = d.find(OLD_BRANDON_START)
if i != -1:
    j = d.find("\n- **", i + 10)
    block = d[i:j]
    open("data/jobs/triage-archive-2026-07.md", "a", encoding="utf-8").write(
        "\n\n### Moved out of the live triage file 04/08/2026 - Brandon Estate in full\n\n" + block + "\n")
    d = d[:i] + ("- **29/07 - Brandon Estate (Elkins) is JACOB'S** (botmsg-18; full account in the archive).\n"
                 "  GBP 3,998,686.95 issued 01/06, REV 2 GBP 7,196,695.63 issued 15/06 to Chris Conlon after Comar\n"
                 "  turned 1,325 windows into 2,202 frames. `quote_issued` recorded. AdminBase 8324 dates it 15/05 -\n"
                 "  that is the RFQ day, not the issue day. Adam has the chase line open himself; do not add a third voice.") + d[j:]

open(p, "w", encoding="utf-8").write(d)
print("after:", len(d.split("\n")))

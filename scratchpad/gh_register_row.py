# -*- coding: utf-8 -*-
"""Add Grange Hill to the chasing register. Handover order of 29/07 16:10."""
import json, io, os

P = "data/jacob/handover.json"
d = json.load(io.open(P, encoding="utf-8"))

KEY = "job:grange-hill-methodist-church-ext"
d["issued"] = [r for r in d["issued"] if r["key"] != KEY]

row = {
 "key": KEY,
 "job": "Grange Hill Methodist Church Ext - WD001 Windows and Doors",
 "client": "Chigwell (London) PLC",
 "contact": "Luke Baker",
 "email": "luke.baker@chigwellgroupplc.co.uk",
 "value": 39006.77,
 "issued": "2026-07-29",
 "issuedTime": "16:07",
 "lastClientContact": "2026-07-29",
 "state": "live",
 "blockedUntil": None,
 "blockedReason": None,
 "owner": "Adam",
 "next": "One call to Luke Baker early next week - mobile 07547 184089, office 020 8500 4100 - and it is the same call as Leys Park and Gordon Court, not a third one. Three things, in this order. (1) It went out at 16:07 on the 29th against a return date of 27 July, so ask outright whether it landed in time to go into Chigwell's own tender to the Methodist Circuit, and when that tender goes in. (2) Then the date we actually need: when does the Circuit decide - that becomes the next chase date. (3) Our price and both material quotes all die on 28 August against a November start, so tell him the 28th is real and get his programme against it. Do not offer to revisit the number and do not walk him through the qualifications unprompted - see openOnTheIssuedDocument for what he is holding, and JAC-13 for the one decision that is Adam's.",
 "history": "Third quote to Chigwell in five weeks and the first one with a same-day deadline on it. Enquiry arrived through Once For All Marketplace to Paul Taylor 24/07 08:08; Luke chased us for costs at 08:22 on 29/07 and again at 09:22 - 'Are you able to provide the costs today?' - which was his answer to Adam's 28/07 request for an extension. Gintare priced it, the quote was with Adam for checking from 13:10 and went at 16:07. No rows in the Opportunity Log under Chigwell at all: three live leads, now GBP 451,418.69 ex VAT, nothing decided. Full picture in data/companies/chigwell-london-plc.md and the pricing story in data/jobs/grange-hill.md.",
 "verified": True,
 "verifiedHow": "Mary, 29/07/2026, at source in estimating@ - handover ledger ref issued:grange-hill:2026-07-29 plus her 17:10 gate check, and she pulled the six attachments off the sent message into scratchpad/gh-issued-to-luke-att/. I read those copies rather than the mailbox; the wall holds.",
 "stage": 8,
 "nextChase": "2026-08-03",
 "chaseNote": "Monday 3 August, and it is not a fortnight rule. Luke wanted the costs the same day because his own submission was already late, so the two dates we lack - when Chigwell submits and when the Circuit decides - only become answerable once he has had the pack over a weekend. He is also a client who has left two chases on Leys unanswered while emailing us about this job, so this is a phone call, not a fourth email.",
 "expires": "2026-08-28",
 "expiryNote": "Our quotation validity is 30 days from 29/07 and BOTH material quotes - BSW QT253562 and Bellview 0000000520 - expire on the same day, 28/08/2026, against a Nov 26 - Jul 27 programme. There is no headroom at all: nothing in this price survives the 28th without re-confirmation from the fabricators. That is a real dated deadline of ours, not the client's, and it is the reason this row cannot be left to drift.",
 "optionalExtras": {"externalMastic": 579.69, "epdm": 1524.55,
                    "note": "The check-stage pack read 537.69 and 1434.55. The issued pack reads 579.69 and 1524.55, so the workbook WAS edited between 13:10 and 16:07 - the omissions below are in a file somebody worked on, not in an unedited resend."},
 "openOnTheIssuedDocument": {
   "why": "Mary sent Adam six corrections at 14:40 and the quote went at 16:07 with the total unchanged at GBP 39,006.77. I checked her list against the pack Chigwell actually holds rather than against her email. All six are still open on the client's copy. This is not a re-price and not a reopening of her catch - it is what my chase has to work with, and what a variation argument will be about if this converts.",
   "checkedAgainst": "scratchpad/gh-issued-to-luke-att/ - the six attachments off the 16:07 message.",
   "items": [
     "THIRTEEN WINDOWS ON THE DRAWINGS, TWELVE IN THE PRICE. The client's marked-up 'Window and Door Drawings.pdf' runs Item 1 to Item 13, every one Qty: 1, and eight of them are 1200x1183. The pricing document sells seven 1200x1183 (W2, W4, W5-W9), so twelve window units in all. Confirmed by reading both issued files, and it is Mary's catch 69 standing unchanged on the issued document. GBP 419.32 of BSW bought and not sold, about GBP 830 of sell - but the exposure is not the 830, it is that Chigwell holds a drawing set with one more window on it than our price.",
     "Automatic door operator, spec 3.13.1, still neither priced nor excluded. The proposal's general exclusion reads 'access control, door sensors', which no QS will read as the DDA operator on a clause written to us. There is no operator line anywhere in the pricing document.",
     "Fish manifestations, spec 3.11.2, absent entirely - not priced, not excluded, not mentioned.",
     "3.15.2 privacy film and 3.16 the FD60 doorsets are silent. The chapel folding doors ARE properly excluded ('Internal bifold doors have not been allowed, as the supplier confirmed these were not included'), but the film and the FD60s are covered only by a general 'internal screens' and 'Internal Finishing - primarily excluded unless agreed otherwise'.",
     "Delivery contradicts the buy. The proposal's exclusions column carries 'Site Storage - Materials will be delivered to site' against QT253562 stated EX WORKS and Bellview 0000000520 stating no delivery terms at all. No carriage rate has ever been obtained on this job.",
     "No zero-rated VAT split. The document says 'SUBTOTAL: GBP 39,006.77 + VAT' flat. The specification names its own zero-rated clauses - 3.12.1 and 3.13.1 among them - and GBP 14,569.26 of our figure sits against those two. A church client will come back on this."
   ]
 },
 "contactRole": "Senior Quantity Surveyor",
 "contactPhone": "020 8500 4100",
 "contactMobile": "07547 184089",
 "request": "JAC-13"
}

d["issued"].append(row)
d["updated"] = "2026-07-29"
io.open(P, "w", encoding="utf-8").write(
    json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print("issued rows:", len(d["issued"]))

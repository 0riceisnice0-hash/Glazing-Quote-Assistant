# RSR - R S Response Ltd

Slug: `rsr`. Written 29/07/2026. Trades as "RSR" everywhere, including their own domain
and email signatures; **R S RESPONSE LTD** is the registered name and the one on the
remittances. AdminBase customer number **1042**. Account reference with them: **FEN01**.

## Position

**The top row of `dormant.json` and the fourth-largest client in Fenster's win history:
5 won jobs, GBP 197,044.44, one of them GBP 188,135.17.** All five carry LEADSOURCE
"Existing Customer", which is the 59% of the win history this job exists to work.

They are **three miles from Fenster's own unit** - Lumen House, Rockingham Drive, Linford
Wood, MK14 6LY against 97-98 Alston Drive, Bradwell Abbey, MK13 9HF. Companies House
**03347263**, active private limited, **incorporated 8 April 1997**, so twenty-nine years
trading. Last accounts to 31 December 2024; next due 30 September 2026.

**What they do, in their own words: "Design | Build | Maintain - RSR your turnkey
solution".** Office fit-out, electrical, mechanical/HVAC, construction (dilapidations,
groundworks, partitioning), fire services, and a renewables arm (EV charging, solar).
Their published sectors are Offices, Commercial and Warehouse. So they are a main
contractor who sublets the glazing package, and they also hold **maintenance** contracts -
which is the recurring small-works work Fenster actually wins.

**The shape of the account is the shape Fenster converts.** Four of the five jobs were
GBP 590 to GBP 4,947; one was GBP 188,135. Against a company median win of GBP 1,924 and
164 of 204 wins under GBP 10k, this is a client who feeds small work steadily and
occasionally hands over something large.

**Nothing has ever been quoted to them in AdminBase - not one row, ever.** And until today
neither bot had said their name: `mary_recall.py --grep RSR` returned zero matches.

## The five jobs

| Contract | Site | Ordered | Fitted | Value | Sold by |
|---|---|---|---|---|---|
| 2378 | **Bletchley Rail Depot, 25 First Avenue, Bletchley MK1 1DX** | 2024-10-15 | 2025-09-02 | **GBP 188,135.17** | Adam Butcher |
| 2289 | St Thomas Aquinas Catholic Primary, Bletchley MK3 5DT | 2024-08-20 | 2024-08-30 | GBP 4,947.45 | Harry Grover |
| 2290 | Amazon DCR3, Trojan Way, Croydon CR0 4XL | 2024-08-20 | 2025-04-25 | GBP 2,173.22 | Harry Grover |
| 2512 | Amazon DWR1, Kingswood Road, Droitwich WR9 0QH | 2025-01-30 | 2025-03-03 | GBP 1,198.03 | Harry Grover |
| 2793 | Woodside Road, Swindon SN3 4WA | 2025-07-16 | 2025-07-23 | GBP 590.57 | Harry Grover |

**Three of the five are Amazon distribution sites and one is a rail depot.** 2793 is
almost certainly Amazon DSN1 - commercial@ has an "Amazon DSN1, Swindon" thread dated
24/07/2025, one day after that job was fitted, same town. **That is the hook: RSR do not
have one building, they have a programme of them**, and Fenster has already glazed three.

## The correction this file exists to record

**`dormant.json` said "378 days, nothing since 2025-07-16". Both halves were wrong, and
saying either on the phone would have been an embarrassment.**

- The clock was aged off the last **order** date and ignored the `fitted` column sitting
  on the same rows. Bletchley was ordered in October 2024 and **fitted 2 September 2025** -
  eleven months of live work counted as silence. `jacob_dormant.py` now ages from the later
  of the two and says which; RSR reads **330 days**.
- The remaining 330 is days since *work*, not days since *contact*. commercial@ holds a
  conversation running to **28 November 2025**, and info@ holds accounts traffic to
  **5 May 2026**. Real commercial silence is **eight months**, not twelve and a half.

## Last contact, and it ended well

The last commercial thread is **"Window and Door Issues"**, October-November 2025: a door
was operating incorrectly on the push bar and opening inwards. **Adam went and fixed it
himself.** 27/11/2025 14:43, Adam to James Evans: *"Works completed today. The door is now
operating correctly on the push bar and not opening inwards. Any further issues let me
know."* 28/11/2025 15:36, James Evans back: *"Thank you, Adam."*

Alongside it, two more that closed out the big job: **"AFP6349 Bletchley Rail Depot -
Follow up inspection"** (Oct-Nov 2025) and **"Bletchley Rail Depot Close Out snags"**
(Jul-Oct 2025).

**So the account did not sour - it finished.** The snags were closed, the defect was fixed
in person by the Commercial Director, and the client's last word to us was thanks. Then
nobody rang.

Since then, only accounts: **Remittance Advice 29/04/2026** ("payment of these invoices has
been processed") and a **Payment and Deduction Certificate 05/05/2026**, both from
accounts@rsr.co.uk to info@. Those are CIS routine and prove the account is open and in
good standing. They are **not** a commercial conversation and must not be treated as one.

## The contacts - none of which were on the board

`dormant.json` carried `phone: null` for RSR. Every one of these was sitting in a signature
in a mailbox Jacob can read.

- **James Evans - Assistant Quantity Surveyor.** james.evans@rsr.co.uk, **M 07938 483016**.
  The working contact through 2025 and the man who thanked Adam. Answers email.
- **Matthew Troiano** - Matthew.Troiano@rsr.co.uk. Cc'd on the defect thread throughout,
  so likely the PM or contracts manager over it.
- **Stephen Read** - Stephen.Read@rsr.co.uk. Senior enough to approve invoices (Aug 2025:
  *"all works are complete but first I've seen of invoice to approve"*).
- **Sean Carroll** - sean.carroll@rsr.co.uk. On the Aug 2025 "Outstanding items" thread.
- **accounts@rsr.co.uk** - the payment route. Invoices go here, not to the surveyor. That
  was learned the hard way in August 2025 and is worth not re-learning.

Switchboard is on rsr.co.uk; the mobile above is the number that has actually been answered.

## What we are trying to make happen

**Be on RSR's enquiry list for the next Amazon or rail depot, and for their maintenance
call-offs.** They are a turnkey design-build-maintain contractor with a warehouse portfolio,
three miles away, who has bought five times and never once been asked what is coming next.
This is not a lead that needs finding - it needs a phone call.

## Next action and owner

**Adam calls James Evans - 07938 483016. Adam, specifically, because Adam is the one who
turned up and fixed their door.**

1. **Open on the door, not on "how have you been".** He fixed it in November and James
   thanked him. That is the warmest opening available and it is nine months old, so it
   still works: has it behaved since?
2. **Then the programme, not the project.** Bletchley Rail Depot, DCR3 Croydon, DWR1
   Droitwich, Swindon - four of their sites already carry Fenster glazing. Ask **what is
   coming on the depots and the fit-outs**, and whether RSR's maintenance contracts carry
   window and door reactive work Fenster could pick up. That last one is the recurring
   small-works band Fenster wins 38% of.
3. **Get the enquiry route.** Who sends the glazing enquiries out, and can Fenster be on
   that list by default rather than when someone remembers. Per the manual: a relationship
   buys being *asked to price*.
4. **Set the next date before hanging up** - Adam's own chase rule. A call that returns no
   date has to be made again from scratch.

**No price, no rate, no "roughly" - if he asks for a number it goes to Mary.** There is no
live quote to RSR anywhere in AdminBase, so there is nothing outstanding to defend.

Reference if one is needed: **Headrow Court for Fortis Vision, ~GBP 630k + VAT**, Fenster's
largest. Though Bletchley Rail Depot at GBP 188,135 is their own job and the better one.

## What Adam has decided about them

Nothing. No standing instruction, no do-not-quote, no pricing ruling. He sold the biggest
job on the account himself and did the remedial visit personally.

## Traps

- **"RSR" in `contracts-finder-awards.json` is not this company.** Row 1152, "National -
  CCS - RSR - ARPE & Specialist Services - WSP", is a Crown Commercial Service framework
  for **Reservoir Panel Engineers**. Textbook single-word-name false positive - checked
  29/07, settled, do not re-check.
- Search the mailbox on **`rsr.co.uk`**, not on `RSR`. The three-letter string matches
  framework acronyms and "RS Response" is how accounts writes it.

## What I do not know

- **Why it stopped.** The evidence says it finished cleanly rather than went wrong, but
  that is a reading of a thread, not a fact from a person. The call settles it.
- **What the 05/05/2026 payment certificate was for.** It could be retention released on
  Bletchley, or it could mean work I cannot see. The attachment would say and I have not
  opened it.
- **Whether the October 2025 "Replacement of reception window" enquiry was ever priced.**
  Harry in estimating forwarded it and Adam replied the same day; there is no AdminBase row
  for RSR at all, so if it was quoted it was quoted outside the CRM. Mary would know.
- Whether the Swindon job is Amazon DSN1. Strongly implied by dates and town, not confirmed.
- Whether the Bletchley Rail Depot client above RSR (Network Rail, or a TOC) is reachable
  independently. RSR were the main contractor; who they were building for is not in what
  Fenster holds.

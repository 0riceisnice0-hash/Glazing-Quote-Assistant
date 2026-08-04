# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-30 08:11 - triage
"NO QUOTE WENT BACK" CAN BE THE RIGHT ANSWER TO A TENDER. LOOK FOR THE OUTBOUND SCOPE QUERY FIRST.

Stepnell issued a formal ITT for St James House Derby on 19/01/2026, bid ref SC0078B, trade "L_SC
Aluminium Doors & Windows", return by 04/02. Nothing went back, and nothing should have: the bill was
INTERNAL doors plus a single window "redub" line, and our external window work was not in it. Gintare
read it on 21/01 and said so, Jayk put it to Luke Walsh in writing on 23/01 with both documents
attached, and on 26/01 Luke confirmed - "I have a bill item for windows 'to follow'. The client is
still assessing the best route for the windows you quoted for the front elevation."

SO THE DEADLINE WAS ANSWERED, NOT MISSED, and the ball is the client's. Before recording a lapsed
return date, check whether we asked whether there was anything to price - a scope query answered by
the client is a complete response to an ITT. Counting ITTs against quotes returned marks that as a
miss. This is the mirror of the St Mary's rule: there, look for the INTERNAL promise before blaming
the document; here, look for the OUTBOUND QUERY before recording a lapse.

AND THE CONVERSE, WHICH IS THE LIVE ITEM: when a client says a bill item is "to follow", that is a
commitment WE are owed, and nothing in our systems ages it. Luke's promise is 185 days old today and
sat on the board as us being silent. If a client tells you something is to follow, put a date on it.

ONE SEARCH TRAP: SC0078B RETURNS ZERO HITS ACROSS ALL OF estimating@. A bid reference printed on an
ITT can live only in the folder copy of the document, so searching the ref will never tell you
whether we responded - and a nil result reads exactly like a missed tender. Search the SITE NAME.

### 2026-08-04 11:42 - triage
TWO SUPPLIER CHANGES THAT PUT A DATE ON LIVE WORK. BOTH LANDED 03-04/08.

1. MARTIN GREGORY HAS RESIGNED FROM CN GLASS - and he is the man behind the only CN Glass rate we
hold. Scott at CN Glass wrote 03/08: Martin "has resigned from his role and will no longer be
representing the company from this moment onwards"; the account is supported by the wider team.

WHY THAT IS NOT ROUTINE. The CN Glass GBP 55-60/m2 was never a quotation document. It was a rate
Steve Freezer wrote into his own outgoing email on 01/07 and Martin confirmed with "Pls see below as
discussed" - verbal, confirmed by return, and the job file says to say so every time it is quoted.
STOKE PARK'S GLASS ORDER WAS PLACED AGAINST THOSE RATES ON 27/07: 124 units, 106.9 m2, GBP 6,185.09,
frames landing 03/08. The person who agreed the price has now left, and what we hold is his email,
not a priced quotation. Anyone relying on a CN Glass number should get it re-confirmed in writing by
whoever has picked the account up, BEFORE the next order, and should not assume the rate survives the
handover. And the general rule this proves: A VERBAL RATE IS ONLY AS DURABLE AS THE PERSON WHO GAVE
IT - get it on a quotation document while the relationship is warm.

2. AGF: REYNAERS PRICES RISE ON ALL ORDERS PLACED ON OR AFTER 27 AUGUST 2026. Lucy Braines, 04/08 -
further cost increases received from their supplier on Reynaers aluminium products, revised pricing
from that date, and she will make contact about current projects.

WHAT TO DO WITH IT: that is a hard commercial date, not a newsletter. Any live quote carrying Reynaers
either goes to order before 27/08 or gets re-priced, and any quote we ISSUE now with 30-day validity
straddles the increase - so if the client orders on day 25 we are exposed. On anything Reynaers-based
that is still open, either qualify the validity against 27/08 in writing or get the order placed. It
lands directly on TOTTERIDGE, where Borras have asked for a cost review by 07/08 against a New Year
start, and where a year-old supplier position is exactly what is being re-confirmed.

### 2026-08-04 11:44 - triage
A VETROSEAL DELIVERY CHARGE IS BILLED AS A GLASS LINE WITH A FAKE 0.300 m2 - IT CORRUPTS MINED RATES.

Quote 065311 (ELEVATION/BEDFORD, 04/08) has two lines: one pane of 10.8mm laminated, 3145 x 2103,
6.614 m2 at GBP 548.89, and a second line "MK40-2QA DELIVERY CHARGE", qty 1, GBP 50.00 - carrying a
UNIT AREA OF 0.300 m2. There is no glass in it.

Divide goods by total area and you get GBP 598.89 / 6.914 = GBP 86.62/m2. The real rate is
GBP 548.89 / 6.614 = GBP 82.99/m2. That is a 4.4% overstatement, silently, on every quote that
carries a delivery line. Any rate mined from Vetroseal must EXCLUDE lines whose description is a
charge rather than a make-up. Same family as their 0.30 m2 minimum-area billing already recorded.

THREE NEW REGISTER LINES, all arithmetic checked and correct:
  Vetroseal 065311  10.8mm laminated, single      GBP 82.99/m2 goods (+50.00 delivery to MK40)
  Vetroseal 065222  6.8mm laminated, single       GBP 34.65/m2 goods (+GBP 1.95/m2 energy)
  Vetroseal 065209  4T-18-6.8 lami/tgh softcoat   GBP 52.51/m2 goods (+GBP 3.25/m2 energy)

AND A WEIGHING INCONSISTENCY, immaterial in money but it breaks a check: on 065209 and 065222 the
surcharge weight is GLASS ONLY (25.0 and 15.0 kg/m2 - the laminate interlayer excluded); on 065311 it
is the FULL 10.8mm including interlayer (27.0 kg/m2). So you cannot verify a Vetroseal weight from
the make-up alone, and a weight that looks wrong is not evidence of an error.

TWO THINGS THE BATCH JOINED UP, which neither work order showed on its own:
- MHA NUNEATON IS BEING PRICED TWO WAYS. 065209 and 065222 are the SAME 8 units at 620 x 2020 on the
  same day - one as a 28.8mm double-glazed unit (GBP 526.08) and one as single 6.8 laminate
  (GBP 347.20). Someone is comparing DGU against single glass, GBP 179 apart on goods. Still no
  enquiry for it anywhere in estimating@ and no folder in the archive.
- ELEVATION/BEDFORD IS PAUL'S MK40 EMERGENCY. Paul Taylor asked AE Glaziers on 03/08 for an emergency
  board-up in Bedford MK40 plus a survey and replacement price, and AE came back asking "do you have a
  rough width and height of the glass?" Vetroseal have now priced one pane 3145 x 2103 delivered to
  MK40 2QA. That answers AE's question - nobody needs to re-measure.

### 2026-08-04 11:56 - triage
STOKE PARK: ADAM HAS AMENDED THE CN GLASS ORDER TODAY - SPEC A IS 28.8mm OVERALL, SO AN 18mm SPACER, NOT 16mm.
Adam to orders@cnglass.co.uk, 04/08 11:45 UK: 'We need to amend the order please. Spec A is meant to be 28.8mm overall thickness so requires an 18mm spacer.' The order Steve placed on 28/07 was built on Martin Gregory's 27/07 line '55 m = 4mm / 6.8' against a 16mm spacer (6.8-16-4 = 26.8mm). So Spec A is 6.8-18-4, and the 27/07 buy - 124 units, 106.9 m2, GBP 6,185.09 - is being changed after the fact.
TWO THINGS THAT FOLLOW.
1. THE AMENDMENT IS CC'd TO MARTIN GREGORY, WHO RESIGNED ON 03/08. It went to orders@ as well so it will be seen, but the man who gave the rate and who said on 27/07 that 'spacer bar doesnt differ the price' has gone. Nobody at CN Glass has confirmed IN WRITING that an 18mm spacer holds the GBP 55/m2. Get that confirmed by whoever picked the account up before the amended order is accepted - it is exactly the verbal-rate exposure already on this board.
2. IT MAKES SENSE OF THE VETROSEAL QUOTE. 065209 (30/07, MHA/NUNEATON) is '4T-18-6.8' - the same 28.8mm build-up with the 18mm spacer, at GBP 52.51/m2 goods. That is the corrected Spec A, priced by the other supplier, and it is level with CN Glass. So the make-up is right and both prices agree; it is the spacer on the ORDER that was wrong, not the rate.
GENERAL: 6.8 + 16 + 4 = 26.8, not 28.8. When a spec states an OVERALL thickness, add the panes and the spacer before ordering - the RFQ that went out on 27/07 asked for a 16mm spacer against a 28.8mm requirement and no one caught it until the glass was on order.

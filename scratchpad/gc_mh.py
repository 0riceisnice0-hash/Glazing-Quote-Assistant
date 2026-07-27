# -*- coding: utf-8 -*-
"""Replace the Gordon Court row in MARY-HANDOVER.md section 7 with the audited position."""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines)
           if l.startswith('| **Gordon Court, Stonegrove Edgware'))

col1 = ("**Gordon Court, Stonegrove Edgware (Chigwell Group, for jLiving)** - AUDITED IN FULL 27/07")

col2 = (
 "**TENDER ISSUED 09/07 - GBP 368,376.70 ex VAT.** Surfaced only because AFS chased **Q7585** on 27/07 "
 "13:02 with no job attached. Folder `Commercial\\1. Tender Documents\\Chigwell (London) PLC\\Gordon Court`; "
 "full record in `data/jobs/gordon-court.md`. 40no replacement windows + 84no new windows/louvre/AOV + "
 "44no patio doors + 15no external/communal doors (3no FD30). Cost GBP 201,086.70 = BSW GBP 182,787.76 + "
 "AFS GBP 18,298.94; install GBP 46,840; mastic GBP 5,622.81 and EPDM GBP 11,416.64 OPTIONAL. "
 "**THE PACK WAS IN THE ZIP** (`Gordon Court Windows, Rooflights & Curtain Walling.zip` - jLiving ITT, "
 "Form of Tender, Energy Statement, 186pp NBS spec, programme, asbestos survey), the Georgie's lesson on a "
 "second job. **THE REAL CLIENT IS jLIVING, NOT CHIGWELL** - Chigwell are a main contractor whose return "
 "to jLiving was **22/07/2026 @ 1400**, and jLiving then run presentations 02/09, award announcement "
 "**16/09**, standstill 30/09, contract award mid-Oct, Go Live 30/10/2026, NEC3 Option A **executed as a "
 "deed**. So Chigwell's silence is structural - they cannot commit until jLiving decide. "
 "**THE BIG RISK: jLiving's Form of Tender holds our price open 180 DAYS to 18/01/2027** while all five "
 "supplier quotes are 30-day (BSW x4 lapse ~06/08, AFS ~08/08) - **GBP 201,086.70, 54.6% of the tender, "
 "unfixed for ~163 days against a firm lump sum**, and neither price binds even inside 30 days (AFS T&C "
 "2.6/8.2; BSW *'an estimate is not an offer of contract and is not binding'*). Now a standing rule, "
 "`check_quote_validity_against_commitment`. **FOUND:** GBP 723.87 of cost omitted - AFS extras "
 "GBP 506.37 **plus a new BSW 'PANEL SET UP' GBP 217.50** on QT252257 (which is exactly why the BSW memo "
 "is GBP 217.66 short of the quotes' true sum); the third fire door is type **D_T**, quoted **2210 high "
 "against a 2110 opening**, as a **double where the schedule shows a 756 single leaf**, in a **Store whose "
 "external/internal cell is blank** (GBP 7,304.44 of sell); **2no type D_X external doors (2100 x 1800) "
 "priced nowhere** (~GBP 5,600 sell, benchmark only - schedule 51001's own count cells sum to its stated "
 "116, giving 17 non-internal doors against our 15); the **Energy Statement requires 1.1 W/m2K** where the "
 "schedules set no U-value at all and defer to a consulting engineer's spec **absent from the pack**, and "
 "no whole-window Uw appears on any BSW quote; **trickle vents 4000mm2 against 8000mm2 required**; "
 "**acoustic vents ticked on 26 of 40 windows and quoted by nobody**; **PAS 24 zero times across all four "
 "BSW quotes**; AFS priced **no dual colour** on the fire doors; **rooflights and the NBS-named Colt AXS "
 "140 roof AOV neither priced nor excluded**. **CLEARED:** install **does** cover the fire doors "
 "(3 x DAD GBP 500 = GBP 1,500; whole GBP 46,840 recomputed exactly); the other three schedules reconcile "
 "**unit-for-unit** (44=44, 40=40, 84=84); Q7585's arithmetic is sound; **the client workbook leaks no "
 "cost** - the 'DO NOT SEND' twin practice Filwood should have copied; panic hardware is priced on all "
 "three fire doors; and the PVC-U/aluminium conflict was **already qualified on our own proposal p3**. "
 "Same client as Grange Hill Methodist - different job. **NOT the unrelated Target Maintenance Gordon "
 "Court** (Earlswood, Redhill, door repair SO_14045)."
)

col3 = (
 "**REQ-20 raised for Adam.** Ask BSW and AFS for a written price hold to 18/01/2027 **before 06/08 and "
 "08/08** or carry a stated allowance - after that we re-quote at autumn prices. A human must answer Chris "
 "Wall at AFS (ghost protocol). RFIs to Arkon via Chigwell on D_T and D_X; RFQ to BSW for Uw, 8000mm2 "
 "vents, Passivent AL-dB 450, PAS 24 and the louvre free area; RFQ to AFS for the dual colour. "
 "Next in-chat job: **render the scanned Q&A log** - RFI-3 (whose spec governs the U-value) is exactly "
 "what a clarification log answers."
)

lines[idx] = "| %s | %s | %s |\n" % (col1, col2, col3)
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
print('MARY-HANDOVER.md row %d replaced' % (idx + 1))

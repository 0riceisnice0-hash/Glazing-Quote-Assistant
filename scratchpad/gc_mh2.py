# -*- coding: utf-8 -*-
"""Append the second-turn findings to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
row = lines[idx].rstrip('\n')
cols = row.split(' | ')
assert len(cols) == 3, len(cols)

cols[1] += (
 " **SECOND TURN 27/07 pm, from riverside's AOV handoff - THE SMOKE VENTILATION FUNCTION IS NOT PRICED.** "
 "Schedule 52003 heads a block 'AOV SMOKE SHAFT LOUVRE' with 'WL_00 Louvres to smoke shaft': **3no WN_7** "
 "in Corridors 1-1/1-2/1-3 marked **'AOV'** and **4no WL_1** at levels 0-3. NBS L20 cl.630 specifies both "
 "as **motorised Colt products** - 'COLTITE GLAZED LOBBY VENTILATOR... **drive open/drive close using a "
 "24V motor mounted to the rear**' and 'EN SEEFIRE LOUVRED NATURAL VENTILATOR... **tested to EN 12101-2**"
 "... **24Vdc electric actuator**'. **BSW quoted 'Qty: 3 Prestige T&T' and 'Qty: 4 Prestige Casement'** - "
 "plain windows, with **zero** occurrences of AOV, louvre, actuator, chain, stroke, motor, 24V or smoke, "
 "and WL_1's glazing line **blank**. Rates give it away: **GBP 412.67/m2** and **GBP 442.98/m2** against "
 "riverside's A Plus AOV point of **GBP 1,401.24/m2** (actuator + AOV sash ~GBP 870/m2), so the 3no WN_7 "
 "alone are **GBP 4,988-5,667** of supply cost short - one quote, different system, order of magnitude "
 "only, and the 4 louvres are unbenchmarkable because there is still no AOV category in the register. "
 "Whole exposure **GBP 7,085.76 cost / GBP 10,055.76 sell** and it is binary: ours and short, or the "
 "specialist's and it comes out. **REQ-22 raised.** GOOD NEWS: this pack states free area as **GEOMETRIC** "
 "(1m2 / 1.5m2), so riverside's ~40% aerodynamic trap does not bite. **AND A CORRECTION TO MY OWN MORNING "
 "RECORD:** I had said the schedules 'set no U-value at all', implying only the sustainability annex asked "
 "- wrong, and it mattered. **NBS L10 cl.330 sets U-value maximum 1.2 W/m2K on windows and L20 cl.280 "
 "sets 1.2 or better on communal entrance doors**, so the requirement does NOT depend on the annex. Cl.330 "
 "also requires **'BS6375-1, BS6375-2, BS6375-3, EN 14351-1 and Pas24'** on every window with cl.205 "
 "third-party certification and submittals (BSW: zero PAS 24 mentions), and cl.280 fixes the entrance-door "
 "finish as **RAL7016 MATT external / RAL9010 GLOSS internal** - so AFS's 'Standard RAL' silence is against "
 "an explicit dual RAL, not a TBC. Cl.330 defers g-value, frame factor and glazing details to a **'SAP "
 "Consultants specification' absent from the pack** - a second missing consultant's spec (RFI-7). **AND "
 "DELIVERY IS IN NOBODY'S PRICE:** all four BSW quotes are 'ex works, additional delivery charges may "
 "apply' with no rate or threshold, AFS's delivery is the omitted GBP 250 extra, and **all five deliver to "
 "Fenster's own MK13 9HF yard, not to site** - 227 units to Edgware with no carriage line anywhere.")

cols[2] += (
 " **SECOND TURN:** REQ-22 raised on the AOV/smoke-vent boundary - ask Chigwell whether the 7 units are "
 "ours in the same message as the D_T and D_X door queries; if they are, BSW/Colt must give a real price "
 "for a Coltite ventilator and an EN Seefire louvre (RFQ-3) because the register has nothing to fall back "
 "on. Extended riverside's `check_free_delivery_threshold` to express 'never free' - it could say always "
 "free but not never, so AFS's known GBP 250 hole was reading as a question; job now runs **5 FAIL, 2 "
 "ASK**. Zac's hub message: `mary_send.py` is 403'd (permissions over-corrected), **hub only** - no email "
 "attempted. Adam's hub answer on REQ-7 landed here by mistake and was passed to `crestwood-park`; it "
 "carries his ruling *'mark the teleflex up by 25%... as a general rule for estimating'* - **posted to the "
 "board but the engine deliberately NOT changed**, and Adam asked to confirm whether that means bought-in "
 "specialist kit only or all supplier cost.")

lines[idx] = ' | '.join(cols) + '\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
print('MARY-HANDOVER.md row %d extended (%d cols)' % (idx + 1, len(cols)))

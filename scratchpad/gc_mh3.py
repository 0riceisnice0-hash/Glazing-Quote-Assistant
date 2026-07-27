# -*- coding: utf-8 -*-
"""Repair the Gordon Court row and append the third-turn note.

The second-turn script split on ' | ' and appended to cols[2], which still held
the row's trailing ' |' - so the text landed AFTER the closing pipe and the row
became a 4-cell row with no terminator. Rebuild it as 3 cells, then append.
"""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
raw = lines[idx].rstrip('\n').rstrip()
parts = raw.split(' | ')
if len(parts) == 4:
    # heal: parts[2] is the real cell 3, parts[3] is last turn's text that spilled past the pipe
    cells = [parts[0], parts[1], parts[2] + ' ' + parts[3]]
    print('repaired 4-cell row back to 3 cells')
elif len(parts) == 3:
    cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
else:
    raise SystemExit('unexpected cell count %d' % len(parts))

cells[1] += (
 " **THIRD TURN 27/07 late - REQ-20 ANSWERED, AND THE CLARIFICATION WINDOW TURNS OUT TO HAVE CLOSED.** "
 "Adam (hub 29): *'It's fine we will hold the price and just trust everything will be okay.'* So the "
 "163-day gap is a **taken decision** - we carry it, do not re-raise it here. Lever arm for the file: "
 "materials are 54.6% of the fixed price, so **each 1% of supplier inflation is GBP 2,010.87** (5% = "
 "GBP 10,054; 10% = GBP 20,109). His answer covers the price hold ONLY - the GBP 723.87, D_T, D_X and "
 "REQ-22 stay open. **RENDERED THE SCANNED 'Q&As' FILE AND IT IS NOT A CLARIFICATION LOG** - it is a "
 "Delta eSourcing Message Centre screenshot ('Antony Berry, Supplier Administrator') showing **'One item "
 "found'**: a single 02/06 message from darien.jay@vixus.co.uk announcing the ITT went live. So no "
 "clarifications were ever raised and RFI-3 is still open. **AND THE ROUTE IS SHUT:** the ITT allows "
 "questions only *'up to 5 working days prior to the tender return deadline'*, *'via the Delta portal'*, "
 "and *'Please DO NOT contact jLiving directly'* - i.e. **~15 July**, while our tender went in 09/07. So "
 "**all ten open RFIs are now POST-TENDER queries through Chigwell - variation territory, not "
 "clarification** - which matters far more now the price is committed firm for 180 days. **ADAM'S REQ-17 "
 "RULINGS APPLIED HERE, TWO OF THREE BIT:** access already complies (proposal names Access/Lifting "
 "Equipment); **STRIP-OUT is a GAP** - twice St Mary's size, 40 replacement windows plus external doors "
 "out of an occupied building, pack silent, proposal excludes 'Waste Removal - generally' and never names "
 "it, and the GBP 46,840 install is pure per-unit fit labour (RFI-9); **MANIFESTATION is a GAP** - NBS L20 "
 "cl.280 requires *'Manifestation: As drawing'* on the communal entrance doors (the internal-door clause "
 "says 'Not required', so it is deliberate) yet manifestation appears **zero times in all five schedules, "
 "both elevation sets and our proposal**, and no drawing shows any (RFI-8). **THE 25% IS NOT AUTHORISED "
 "FOR THIS JOB'S BOUGHT-IN KIT** - Adam confirmed Teleflex only, and Gordon Court's AOVs are Colt units "
 "with 24V motors, exactly the tempting analogy; if REQ-22 puts them in scope the uplift must come from a "
 "real supplier price. **POSSIBLE THIRD MAILBOX GAP:** 'Antony Berry' appears nowhere in our records - if "
 "Fenster holds a live Delta account, jLiving's award and standstill notices go there, not to estimating@ "
 "(RFI-10).")

cells[2] += (
 " **THIRD TURN:** REQ-20 closed as answered; **REQ-22 (AOV scope) is now the only open request** on this "
 "job. New RFIs - RFI-8 manifestation, RFI-9 strip-out, RFI-10 whose Delta account holds this tender. All "
 "ten RFIs must now go to Chigwell as post-tender queries because the portal window shut ~15/07. Adam's "
 "REQ-17 answer was misrouted here and forwarded to `st-marys`. Nothing is urgent before jLiving announce "
 "on 16/09; the next substantive job is putting RFI-8 and RFI-9 in front of Chigwell together with the "
 "D_T/D_X queries as ONE post-tender qualification rather than four separate asks.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)

check = lines[idx].rstrip('\n').split(' | ')
print('row %d rewritten: %d cells, ends with pipe: %s'
      % (idx + 1, len(check), lines[idx].rstrip('\n').endswith('|')))

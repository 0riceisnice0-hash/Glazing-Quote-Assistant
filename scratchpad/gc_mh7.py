# -*- coding: utf-8 -*-
"""Seventh-turn append to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **SEVENTH TURN 27/07 late - MY OWN AOV RULE WITHDRAWN, AND WE PRICED FROM 25 OF 82 DRAWINGS.** "
 "**(a) CORRECTION:** my '1.5 m2 needs 78.5% of gross frame, unachievable' was too strong. riverside "
 "established the APERTURE is the right denominator. From BSW's own figures: glass 700 x 1865 = **1.3055 m2 "
 "= 87.0%** of the duty; frame aperture 770 x 1935 = **1.4900 m2 = 99.3%**. So WN_7 is **MARGINAL, not "
 "incapable** - short by 0.01-0.19 m2. My '60% of gross' rule of thumb is **WITHDRAWN**; it would have "
 "condemned a borderline unit. The actuator/motor/fire-alarm absence is untouched and was always the "
 "substantive point. **(b) THE BIGGER MISS:** the loose job folder everyone priced from holds **25 of the 82 "
 "5244-ARK drawings** in the zip. The 57 missing include **every floor Layout plan (10001 rev 07, 10002-10004 "
 "rev 06 - the most-revised sheets in the pack), every Existing plan, ALL THREE DEMOLITION PLANS, all four "
 "Existing Elevations and the Proposed Elevations**. We held the SETTING OUT plans and SETTING OUT elevations "
 "instead - a different series with similar numbers. **(c) THE DEMOLITION PLANS ANSWER THREE OPEN ITEMS:** "
 "**'ALL WINDOWS TO BE REMOVED.'** in all three notes blocks (so RFI-9's 40-window / 62.457 m2 quantity "
 "finally has a source); a legend including **'NEW STRUCTURAL OPENINGS. HEIGHTS TO BE CONFIRMED ON SITE'** "
 "(so new-vs-existing openings are marked there - the floor-by-floor question against Adam's REQ-9 ruling); "
 "ground floor **'Section of the external wall is to be carefully demolished to allow for the installation of "
 "2 NO. NEW DOUBLE DOORS'** (almost certainly the unpriced D_X pair); first floor **'Curtain walling system "
 "(frames, glazing, and fixings) to be removed in sections'** on a job titled 'Windows, Rooflights & CURTAIN "
 "WALLING' where we priced **no curtain walling**; and 'Demolish bay windows and associated brickwork' with "
 "no bay type in our schedule. In fairness these are demolition/main-contractor drawings (external stair and "
 "whole roof also demolished) so most is not ours - the finding is that the window and curtain-wall REMOVAL "
 "scope was defined on sheets nobody who priced the job ever saw. **(d) A FOURTH MISSING REFERENCED "
 "DOCUMENT:** all three demolition plans require reading with **'THE DEMOLITION ELEVATIONS'**, which exist "
 "nowhere in the 82 - joining the SAP Consultant's spec and the Edward Pearce spec. **(e)** riverside's "
 "prior-approval check: **no planning reference exists** on this job in the DAS or Drawing Register, so "
 "unverified rather than answered.")

cells[2] += (
 " **SEVENTH TURN:** REQ-22 corrected (the clear-opening overstatement) and extended to 17 options, "
 "read-back verified - now asks for the 57 missing drawings and the absent demolition elevations. The single "
 "most useful next action on this job is to **get the three demolition plans and the layout series from "
 "Chigwell**: they define the strip-out scope (RFI-9), mark new-vs-existing openings, and probably locate the "
 "unpriced D_X pair. Bundle with RFI-8 manifestation, RFI-11 caveats and the D_T query as one post-tender "
 "qualification.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends|%s, len %d' % (idx+1, len(back.split(' | ')), back.endswith('|'), len(back)))

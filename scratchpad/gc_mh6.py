# -*- coding: utf-8 -*-
"""Sixth-turn append to the Gordon Court row in MARY-HANDOVER.md section 7."""
import io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()

idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, 'expected 3 cells, got %d' % len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]

cells[1] += (
 " **SIXTH TURN 27/07 late - THE SMOKE SHAFT WAS DELETED IN OCTOBER 2025 AND THE SCHEDULES NEVER CAUGHT "
 "UP.** riverside's compliance-route rule sent me to the fire strategy drawings, which I had only searched "
 "for door ratings. **Fire strategy 14003/14004 rev 02 (09.10.2025): 'Updated to suit fire officers "
 "comments... SMOKE SHAFT OMITTED'; 14005 rev 01 same date: 'SMOKE SHAFTS OMITTED. MECHANICAL EXTRACT VENT "
 "ADDED'** - revised three or four more times to rev 04-06 (17.02.2026) and never reversed. **THEN THE "
 "DATES: window schedules 52001/52002/52003 are 08.09.2025 at revision '-', NEVER REVISED**, the NBS is "
 "23-08-2025, the shafts went 09.10.2025, and the door schedule and fire strategy were updated 17.02.2026. "
 "So both documents that put the 4no 'Louvres to smoke shaft' in our scope predate the omission and neither "
 "was updated, while the ones that were show the shafts gone. **GBP 4,502.40 cost / GBP 6,452.40 sell is "
 "scheduled against a shaft deleted five months before the tender went out - that half of REQ-22 is now a "
 "possible CREDIT, not a shortfall.** NEW CHECK FOR EVERY JOB: list every drawing with its revision number "
 "and date and look for outliers; a sheet at rev '-' among rev 04s is stale and anything it uniquely "
 "schedules is suspect. **SECOND, INDEPENDENT AOV PROBLEM - THEY MAY BE TOO SMALL:** the current fire "
 "strategy states the duty itself, 'AOV. 1.5m2 CLEAR OPENING AREA' (and separately 'SV. NSHEV. 0.4m2 clear "
 "opening area minimum'). WN_7 is 910 x 2100 = **1.911 m2 gross frame**, so a 1.5 m2 clear opening needs "
 "**78.5% of gross** - unachievable on the 'SP104 70mm Large Outer' T&T BSW quoted; on the NSHEV reading "
 "0.4 m2 is 20.9% and is fine, so **which duty they serve changes the answer** and the schedule says 'AOV'. "
 "BSW must state the clear opening - I did not compute one from assumed profiles. **BASIS QUESTION CLOSED:** "
 "'clear opening area' is geometric-side language, agreeing with the NBS's explicit '1m2 geometric'; "
 "'aerodynamic' appears nowhere in the NBS, mech or electrical specs. **ADAM'S REQ-9 RULING ONLY HALF "
 "TRANSFERS:** the schedules say 'WINDOWS TO GROUND AND FIRST FLOORS ARE TO BE INSTALLED TO MATCH THE "
 "EXISTING STRUCTURAL OPENING SIZES', so levels 0-1 are constrained and 2-3 are new build and free - WL_1 "
 "sits at 0/1/2/3 and WN_7 at 1/2/3.")

cells[2] += (
 " **SIXTH TURN:** **DEADLINE FIELD CORRECTED per triage's sweep - 08/08/2026 was AFS's quote validity, not "
 "a client date, and a SPENT one since Adam's REQ-20 decision. Now 16 SEPTEMBER 2026, deadline_basis "
 "CLIENT-STATED** (jLiving ITT 'Tender Award Announcement'); our own binding date remains 18/01/2027. "
 "REQ-22 extended with the shaft omission and the clear-opening arithmetic, 12 options, read-back verified. "
 "The first ask of Chigwell should now lead with the credit question - do the 4no smoke-shaft louvres "
 "survive the October 2025 omission - alongside RFI-8 manifestation, RFI-9 strip-out, RFI-11 caveats and "
 "the D_T / D_X door queries, as one post-tender qualification.")

lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)

back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends with pipe: %s, len %d'
      % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

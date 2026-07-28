# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = "TWELVE EXPOSURES READ BOTH WAYS - FOUR ARE BACKED AND I HAD RECORDED NONE OF THEM"
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "riverside took my point that a correction in your favour does not feel like something you are missing, "
 "found their storage clock was recoverable under our own Cancellation and Postponement clause, and shipped "
 "a rule for it: list every exposure with what backs us, and write 'none' where nothing does. Populated here "
 "with twelve.\n\n"
 "    BACKED by a term in our issued proposal      4\n"
 "    'none', recorded deliberately                5\n"
 "    conditional or qualified                     2\n"
 "    unassessable until BSW produce their terms   1\n\n"
 "THE FOUR BACKED ARE ENTITLEMENT I HAD NOT WRITTEN DOWN ANYWHERE: strip-out (excluded as Waste Removal and "
 "Structural Alterations, and on the Main Contractor under jLiving's Works Information), scaffold and access "
 "(same, twice over), design and structural calculations (excluded by name), and post-order storage.\n\n"
 "THAT LAST ONE IS THE SAME MISTAKE RIVERSIDE JUST CORRECTED, ON THIS JOB, AND I MADE IT FIRST. At the "
 "twenty-fourth turn I recorded AFS's deferred-delivery storage as 'uncapped, with no rate stated'. I had "
 "read AFS's terms to write that and never read ours. Our issued proposal carries 'Cancellation and "
 "Postponement - should the client cancel or POSTPONE the contract following procurement of materials... "
 "Fenster reserves the right to... recover any additional costs incurred', plus 'any delay outside of "
 "Fenster's control may incur additional costs' and a Supplier Delays clause. A supplier's storage charge "
 "after a client-driven slip is an additional cost incurred following procurement. RECOVERABLE, NOT "
 "ABSORBED.\n\n"
 "THE FIVE 'NONE' ENTRIES ARE DELIBERATE, because a stretched clause is worse than an honest gap. The "
 "sharpest is the NBS clause 205 certification documentation: our 'Testing - on or off site testing' "
 "exclusion READS AS THOUGH IT COVERS IT AND DOES NOT, because certification is documentation the maker "
 "already holds rather than a test. Recorded as unbacked rather than argued into cover.\n\n"
 "AND I HAVE TIGHTENED AN OVERCLAIM OF MY OWN FROM LAST TURN. I wrote that position 003 IS a variation "
 "upstream under our Additional Limitations. That is only true if the 2210 came from others - the 2110 is "
 "the architect's, the 2210's origin is unknown and is the first question the AFS letter asks. The letter "
 "said it conditionally; the job file said it as settled. That is the worse way round, because the letter is "
 "read once and the job file is read by every turn after it.\n\n"
 "CLEAN AND REPORTED AS CLEAN: riverside flagged that the archive holds two dates for the master cover "
 "letter, 29/05 and 31/05, and that any job citing one to a client should check. Ours cites neither - the "
 "issued proposal prints the terms IN FULL, no incorporation by reference, and the only date on it is "
 "09/07/2026. We did not do to Chigwell what BSW have done to us.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = "AND I HAVE TRACED YOUR GBP 201,086.70 TO ITS SOURCE"
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-28')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". 28/07.\n\n"
 "GOOD NEWS FIRST, AND IT IS GENUINE. Riverside found their pricing document carried the buy price in "
 "columns to the right of the printed area - supplier named, frames, glass and surcharge split out, on the "
 "document they would hand a client. I checked ours. THE ISSUED GORDON COURT PRICING DOCUMENT HAS NOTHING "
 "OUTSIDE ITS PRINT AREA AT ALL. No supplier names, no buy split, nothing right of column H.\n\n"
 "That is because this job keeps two files and somebody was disciplined about it:\n\n"
 "    Gordon Court Pricing.xlsx                257 cells   sell only - this is what went\n"
 "    Gordon Court Pricing DO NOT SEND.xlsx    504 cells   cost codes, and 258 cells right of column H:\n"
 "                                                         'Supplier used:', 'BSW' 182,787.76,\n"
 "                                                         'Aluminium Fire System' 18,298.94, and 201,086.70\n\n"
 "They differ in 596 cells, so they are genuinely different documents. The DO NOT SEND naming worked.\n\n"
 "WORTH KNOWING THOUGH: the DO NOT SEND file's own print area is C1:I71, which would NOT have hidden columns "
 "K, L and M if anyone had ever sent it. The thing protecting us here is the filename, not the print area.\n\n"
 "AND THAT LAST CELL ANSWERS SOMETHING I RAISED WITH YOU TEN DAYS OF WORK AGO. At the twenty-first turn I "
 "told you REQ-20's exposure figure of GBP 201,086.70 was GBP 217.66 light, and explained it as my having "
 "used the wrong AOV subtotal. THAT ATTRIBUTION WAS WRONG. The figure is cell M5 of the working pricing "
 "document - 182,787.76 for BSW plus 18,298.94 for AFS. The correct BSW total is 183,005.42, so THE "
 "WORKBOOK IS 217.66 LIGHT, not my transcription of it. The arithmetic in my correction was right and the "
 "attribution was not.\n\n"
 "It matters because the same 217.66 will recur on anything else built from that sheet, and correcting my "
 "own note would not have fixed it. It is the GBP 217.50 panel set-up on QT252257 plus a 16p rounding slip. "
 "Still 0.1%, still changes nothing about REQ-20, but it is a cell rather than a typo.\n\n"
 "SEPARATELY, I BROKE SOMETHING AND HAVE FIXED IT. My cleaned copy of the pricing document lost its print "
 "area and its repeating header rows, because a print area is stored as a defined name in the same block as "
 "the 50 foreign ones I stripped, and I deleted the block wholesale. Riverside made the identical mistake an "
 "hour earlier and found it first. Rebuilt filtering name by name and listing what is removed: 50 foreign "
 "names out, both of ours kept, 257 cells identical, the total intact.\n\n"
 "NONE OF THIS MAKES THE MARGIN SAFE ON THIS JOB. Chigwell have it anyway, from the five supplier "
 "quotations attached as 'Elevations' - which is what the rest of this request is about. A control that "
 "works on one document is worth nothing if the same information travels in another.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-28 appended,', len(req['why']), 'chars')

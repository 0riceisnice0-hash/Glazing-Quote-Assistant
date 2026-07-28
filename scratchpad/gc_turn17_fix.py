# -*- coding: utf-8 -*-
"""Seventeenth turn: withdraw the 'no supplier quote behind it' finding - all seven ARE quoted."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'data', 'job-checks', 'gordon-court.json')
m = json.load(io.open(P, encoding='utf-8'))

# Every one of the seven is priced on a supplier quote at exactly the workbook cost.
FIXED = {
 "WN_4":  ("BSW QT252247", "Overall Size 1360 x 1935, Qty 1, Foil/Wt Casement, Location WN 4, GBP 521.69"),
 "WN_6":  ("BSW QT252247", "Overall Size 2710 x 1650, Qty 1, Foil/Wt Casement, Location WN6, GBP 911.25"),
 "WN_8":  ("BSW QT252247", "Overall Size 910 x 1350, Qty 1, Foil/Wt Casement, Location WN 8, GBP 297.26"),
 "WN_9":  ("BSW QT252247", "Overall Size 1136 x 1350, Qty 1, Foil/Wt Casement, Location WN 9, GBP 472.89"),
 "D_B 1055 x 1750": ("BSW QT252251", "Overall Size 1055 x 1720, Qty 1, Prestige Open In Door, GBP 843.71"),
 "D_E 1500 x 2100": ("BSW QT252251", "SPLIT ACROSS TWO LINES: 500 x 2100 Prestige Casement GBP 401.12 + "
                                      "1055 x 2085 Prestige Open Out Door GBP 878.58 = GBP 1,279.70 exactly"),
 "D_U 1405 x 2170": ("BSW QT252251", "SPLIT ACROSS TWO LINES: 500 x 2100 Prestige Casement GBP 401.12 + "
                                      "1000 x 2085 Prestige Open Out Door GBP 870.27 = GBP 1,271.39 exactly"),
}
n = 0
for c in m['supplier_coverage']:
    for ref, (sup, ev) in FIXED.items():
        if c['ref'] == ref:
            c['qty_quoted'] = c['qty_sold']
            c['supplier_ref'] = sup
            c['note'] = ("CORRECTED 28/07 - this WAS quoted; my turn-one reconciliation was wrong. " + ev)
            n += 1
print('corrected %d supplier_coverage rows' % n)

m['_note'] += (" SEVENTEENTH TURN 28/07 - WITHDRAWING A TURN-ONE FINDING. I reported GBP 5,597.89 of cost across 7 "
 "lines as having 'no supplier quote behind it'. ALL SEVEN ARE QUOTED, at exactly the workbook costs. My test was "
 "the workbook's R column, a partially-filled working column, rather than the quotes themselves. WN_4, WN_6, WN_8 "
 "and WN_9 are all priced lines on QT252247; D_B 1055 is on QT252251 at 1720 rather than 1750 high; and D_E and "
 "D_U are each SPLIT ACROSS TWO BSW LINES (casement + door) summing to the workbook figure to the penny. What is "
 "real, and what I found while checking, is SIX DIMENSIONAL DISCREPANCIES between quotes and schedules.")

sp = m['spec_items']
sp.append({
 "ref": "Dimensional discrepancies between supplier quotes and the architect's schedules - six of them",
 "treatment": "GAP - survey items, qualified by our own T&Cs but not eliminated",
 "evidence":
 "FOUND WHILE WITHDRAWING THE 'NO SUPPLIER QUOTE' FINDING, and this is what is actually there. Comparing every "
 "BSW and AFS overall size against the schedule's structural opening: "
 "WN_4 - workbook and schedule 1360 x 1656, BSW quote 1360 x 1935: +279mm HEIGHT. "
 "WL_1 (x4) - schedule 1210 x 2100, BSW 1307 x 2197: +97mm in BOTH directions, which a cill does not explain "
 "because a cill only adds height. A frame 97mm bigger than the hole does not go in. "
 "D_B 1055 - schedule 1055 x 1750, BSW 1055 x 1720: -30mm height. "
 "D_E - schedule 1500 x 2100 single door, BSW split into 500 x 2100 casement + 1055 x 2085 door = 1555 combined: "
 "+55mm width. "
 "D_U - schedule 1405 x 2170, BSW split into 500 x 2100 + 1000 x 2085 = 1500 x 2100 combined: +95mm width and "
 "-70mm height. "
 "D_T - schedule 1600 x 2110, AFS Q7585 1600 x 2210: +100mm height (already recorded). "
 "SIX DISCREPANCIES ACROSS TWO SUPPLIERS. riverside's find qualifies them but does not remove them: our own "
 "Terms and Conditions say 'All quotations are subject to final site survey and measurement verification', and "
 "the architect's schedules independently require 'A FULL SITE MEASUREMENT SURVEY PRIOR TO PRODUCTION AND "
 "INSTALLATION' and state 'NO FABRICATION SHALL PROCEED BASED SOLELY ON DRAWING DIMENSIONS'. So these are survey "
 "items rather than pricing errors PROVIDED the survey happens before fabrication - and our proposal does include "
 "Site Survey. But +279mm and +97mm in both axes are larger than a survey tolerance; they look like different "
 "units, not re-measures. Worth putting to BSW in the same RFQ as everything else. "
 "NOTE THE SPLIT-UNIT POINT SEPARATELY: BSW read D_E and D_U as door-plus-sidelight assemblies, which is a "
 "sensible reading of a schedule that marks sidelights - but nobody checked the combined width against the "
 "opening, and both are over."})

json.dump(m, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('manifest updated - %d spec_items' % len(m['spec_items']))

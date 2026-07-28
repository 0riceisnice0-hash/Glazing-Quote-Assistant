# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
cells[1] += (
 " **TWENTY-FOURTH TURN 28/07 - WE DISCLAIM THE DRAWINGS UPSTREAM AND WARRANT THEM DOWNSTREAM.** riverside's "
 "TypeError on `free_delivery_threshold: \"5000\"` was only reachable because **I** made that field string-typed "
 "by adding `\"never\"`; their fix verified. **The structural half was mine:** `run()` was a list comprehension so "
 "**one raising rule aborted the WHOLE run**, and since rules execute in list order **what you lost depended on "
 "where the crash sat** - their rule is second-from-last and `check_spec_label_matches_evidence` is **LAST**, so "
 "the crash was **silently skipping my own newest rule every time**. Now a crash is a **FAIL on that rule alone** "
 "(*'treat it as unchecked, not as passed'*) and the other 15 still run - proven by injecting the exact TypeError "
 "at position 4 (**17/17 results, 12 later rules evaluated, last rule survived**), persisted as "
 "`selftest_one_crash_costs_one_rule()`. **THEIR EXCLUSIONS-INTERSECTION CHECK GAVE TWO DIFFERENT ANSWERS:** "
 "**BSW SILENT on all ten categories** - supply price lists with no exclusions schedule, so nothing to intersect, "
 "**an UNDEFINED result not a clean one**, recorded as such.")
cells[2] += (
 " **TWENTY-FOURTH TURN - AFS IS THE MIRROR OF RIVERSIDE'S CASE, NOT A COPY.** Q7585 **cl.3.6** makes the "
 "**CUSTOMER** responsible for ensuring all *'measurements, plans, drawings, and designs... are accurate, complete "
 "and fit for the intended purpose'*, and **cl.3.7.2/3.7.5** let AFS **reprice or cancel without liability** if a "
 "dimension we supplied is wrong. Our own **cl.16 DISCLAIMS** design intent/architectural suitability and states we "
 "**RELY ON** the client team's drawings. **Precisely: MEASUREMENT is consistent both ways (ours up, ours down); "
 "FITNESS FOR PURPOSE OF DRAWINGS is DISCLAIMED UPSTREAM and WARRANTED DOWNSTREAM - not back to back.** Live "
 "exposure: **position 003 quoted 1600x2210 against a 1600x2110 structural opening**, the 2210 tracing to **client** "
 "schedule 51001 - under 3.6 it lands on us at order. Raised **pre-order** in the AFS letter citing 3.6/3.7 and "
 "expressly not disputing them; asking pre-order costs nothing, post-order is a variation. **General check: read "
 "the supplier's conditions for 'Customer' and list what it makes you responsible for, then read your own terms for "
 "what you disclaimed to the client - the gap is your unbacked-off risk.** **CLEAN:** Chigwell letter already asks "
 "Arkon for D_T's structural height. Selftest passes (16/16 delivery variants + crash isolation), **4 FAIL / 2 ASK** "
 "unchanged. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

# -*- coding: utf-8 -*-
"""Forty-fourth turn. No pipe characters in the appended text - see turn 39."""
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
ADD1 = (
 " **FORTY-FOURTH TURN 28/07 - THE VERB CHECK NEEDED A SECOND STEP, AND WITH IT MY C4 TURNS OUT TO HAVE DROPPED "
 "A DEADLINE THE SPECIFICATION SETS.** riverside added the step my check was missing: **find your strongest "
 "verb, find the source's verb, and ask whether swapping them changes what the reader would DO** - their "
 "*'require'* for *'to be vented with'* changes nothing, so it is a **paraphrase not an error**, and declining "
 "to bank it is the harder half. **Run here on 24 quoted fragments:** most are neutral reporting verbs; two wrap "
 "multiple fragments with my own connective. **Clause 330 is a fair paraphrase** (source is a field label, *1. "
 "Standard: To BS6375-1... and Pas24*) - left alone and said so. **CLAUSE 205 IS NOT.** Mine read *requires "
 "'Independent, 3rd Party Certification Schemes' WITH 'documentation confirming Certifications claimed'*. The "
 "source has FOUR parts - *1. Third-party certification: Submit proposals; 2. Verification: Independent 3rd "
 "Party Certification Schemes; 2.1 Submittals: Submit documentation confirming Certifications claimed; 2.2 "
 "Timing: Before completion of detailed design*. **My 'with' stitched 2 and 2.1 and DROPPED 1 and 2.2 - the two "
 "OPERATIVE ones.** *'Timing: Before completion of detailed design'* **was not in the letter at all**, and it is "
 "the sentence that tells BSW when the documentation is needed. C4 rewritten quoting both clauses in full plus a "
 "limb asking for the documentation to meet that timing. **The check recovered a REQUIREMENT, not just a verb.**")
ADD2 = (
 " **FORTY-FOURTH TURN - AND THEIR SHARED-TOOLKIT POINT FOUND THE SAME FAULT ONE LEVEL FURTHER IN.** riverside: "
 "**'if a shared rule prints a verb, that verb will end up in somebody's letter'** - six of their nine *'lapse'* "
 "instances came from **my** rule's output. Swept every `result()` string in `mary_checks.py` across all 13 "
 "manifests: after last turn's fix, `must` x8 is a harmless estimator prompt and **`cannot` x17 is not** - "
 "*'Total GBP 201,304.36 of cost unfixed against a price we cannot withdraw'*. **jLiving's Form of Tender says "
 "ONLY *'This tender remains open for consideration for a period of 180 days from the date of receipt of "
 "tenders'* and in 993 characters contains ZERO instances of withdraw, revoke, irrevocable, binding, cannot or "
 "may not.** **'Cannot withdraw' was mine; it is a stronger legal claim than the source makes; and our OWN terms "
 "carry a 30-day validity that pulls the other way (s4N)** - so it settled as fact a question our own two "
 "documents disagree about, **inside the rule reporting the biggest number on the job and read by every chat**. "
 "Now *'against a price we have said stays open'*, reason in the docstring. **THIRD INVENTED CERTAINTY IN THREE "
 "TURNS AND THE FIRST INSIDE THE TOOLING RATHER THAN A LETTER** - a shared rule does not just supply a verb, it "
 "supplies **a settled position on a contested question**, and nothing in the run flags that it was contested. "
 "**REQ-20 settled what we WILL do; it never settled what we COULD do.** Selftest passes, **5 FAIL / 5 ASK** "
 "unchanged. Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
for a in (ADD1, ADD2):
    assert '|' not in a, "pipe would split the table cell"
cells[1] += ADD1
cells[2] += ADD2
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
rows = [(i, l) for i, l in enumerate(io.open(P, encoding='utf-8').readlines(), 1)
        if l.startswith('| ') and not l.startswith('|---') and ' | ' in l]
bad = [(i, len(l.rstrip().rstrip('|').split(' | '))) for i, l in rows
       if len(l.rstrip().rstrip('|').split(' | ')) != 3]
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))
print('whole-table guard: %s' % (bad or 'all %d data rows are 3 cells' % len(rows)))

# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE STRONGEST-VERB SWEEP, RUN ON BOTH LETTERS - AND THE ONE THAT MATTERS IS A PARAPHRASE (28/07)"

SEC = u"""### THE STITCHED-QUOTATION SWEEP - AND MINE NARROWED A SUPPLIER'S DISCLAIMER (28/07)

Gordon Court took the second step and applied it to quotations rather than verbs: **a strong verb wrapping
two fragments joined by a connective of your own.** Theirs found NBS clause 205, where a single *"with"*
stitched sub-clauses 2 and 2.1 and **dropped 1 and 2.2 - the submission and the deadline**. *"Timing:
Before completion of detailed design"* never reached their letter at all.

> **"The check did not just correct a verb. It recovered a requirement."**

**Run here: every sentence in both letters containing two quoted fragments. Seven hits, five benign** -
correctly attributed to two different documents, or quoting the letter's own earlier text. **Two were
real.**

**THE ONE THAT MATTERS: I NARROWED A PLUS'S DISCLAIMER BY STITCHING IT.** My RFQ said:

    the Supplier "does not warrant or represent that any Product supplied shall comply
    with" THE BUILDING REGULATIONS "unless where expressly stated to the contrary"

The source says:

    "It is the responsibility of the Customer to ensure all building regulations (i.e.
     Part 'B', 'F', 'L', 'M' & 'N' and any others relevant to the building), LIFE TIME
     HOMES, SECURED BY DESIGN, PAS 24 (formally BS 7950) are adhered to. The Supplier
     does not warrant or represent that any Product supplied shall comply with ANY OF
     THE AFOREMENTIONED STANDARDS unless where expressly stated to the contrary."

**My connective replaced "any of the aforementioned standards" with "the Building Regulations" - and the
disclaimer also covers Secured by Design and PAS 24.** On a residential conversion those are live
categories, and the letter represented A Plus's disclaimer to A Plus as narrower than A Plus wrote it.

**This is the mirror of theirs and it is worth naming as a distinct direction.** Gordon Court's stitch
**dropped an obligation on the supplier** - a submission and a deadline they were owed. **Mine dropped
breadth from a disclaimer against us** - a protection the supplier holds. **Theirs cost us something we
were owed; mine understated something we are exposed to.** Both came from one word of my own between two
sets of quotation marks.

Rewritten to quote the clause in full, with the reason stated - *"quoted in full so that we are not
stitching fragments of it together"* - and a sentence noting the wider scope explicitly. **The
free-area quotation was tidied in the same pass:** I had written *"Geometric free area = 1.30m2. BASED ON
A 50mm REVEAL"* where the quotation reads *"Geometric free area = 1.30m2 Based on a 50mm reveal"* - a
full stop and a set of capitals I added. Trivial, and a quotation should be exact.

### THE RULE THIS PRODUCES (28/07)

> **If you have joined two quoted fragments with a word of your own, go and read the sub-clauses between
> and after them** - Gordon Court's sentence - **and check what your connective replaced.** A connective
> does not only join; it stands in for whatever it skipped, and nobody reading the letter can see what
> that was.

**The tell is a preposition doing semantic work between quotation marks.** *"comply with" the Building
Regulations "unless..."* - the word `with` is inside the first quotation, and everything after it until
the second quotation is mine, in a position where the reader will read it as the source's.

### And their toolkit finding, one level further in than mine (28/07)

Last turn this chat found six of nine *"lapse"* instances came from a rule's output. **Gordon Court swept
every `result()` string in `mary_checks.py` across all thirteen manifests and found a bigger one:**

    "cannot"  x17    "Total GBP 201,304.36 of cost unfixed against a price WE CANNOT WITHDRAW"

jLiving's Form of Tender says only that the tender *"remains open for consideration for a period of 180
days"* - **zero instances of withdraw, revoke, irrevocable, binding, cannot or may not in 993
characters.** And Fenster's own 30-day validity pulls the other way. **So the rule settled as fact a
question our own two documents disagree about, inside the output that reports the largest number on that
job and is read by every chat.** Now *"against a price we have said stays open"*.

**Third instance of the invented-certainty shape in three turns, and each one a level further in:** a
letter, then a job file, now **the tool the letters quote.** `check_quote_validity_against_commitment`
has run on the Riverside manifest since its fixture was written, so this chat has been reading *"cannot
withdraw"* as often as Gordon Court has.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

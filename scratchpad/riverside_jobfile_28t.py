# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### ONE QUANTITY, TWO FIGURES - RUN ACROSS EVERY DOCUMENT AT ONCE, AND CLEAN (28/07)"

SEC = u"""### QT51518 DOES NOT LAPSE. I HAVE BEEN SAYING IT DOES FOR THIRTY TURNS (28/07)

Gordon Court found their letter's entire lack of urgency resting on jLiving's 16 September award date -
**which the ITT marks TBC, in the same cell as the date they quoted.** Every stage after tender return is
TBC, and the qualifier never reached their paragraph.

> **"If you have a document whose urgency is framed by somebody else's programme date, go and look at
> whether that date is marked provisional."**

**Run on the date this entire job is built around.** QT51518, printed rather than remembered:

    "The Price stated in the quotation is open for acceptance for a period of 30 days
     from the date of the quotation AND THEREAFTER IS SUBJECT TO CONFIRMATION"

    lapse 0    expire 0    expiry 0    "valid until" 0    withdraw 0

**Thirty turns of documents here say "QT51518 lapses 26/08/2026". The quotation never says that.**
*Subject to confirmation* means the price stops being automatically binding and A Plus would reconfirm
it - **not that the quotation is void and a fresh enquiry is required.**

**And the RFQ header went further than a wrong word.** It told Gintare that four sentences become
**false** after 26/08 - one of which, *"QT51518 lapses 26/08/2026"*, was never true in those terms - and
then asserted that after that date **"A Plus would be quoting from scratch rather than adding lines"**.
**That is my inference about A Plus's commercial behaviour, stated to A Plus as a fact about their own
quotation**, in the same letter that asks them thirteen questions. It is the credibility point I have
posted twice this week, landing on the loudest paragraph in my own document.

**Rewritten to quote what the quotation says.** The header now states the acceptance wording verbatim,
says 26/08 is the day the price stops being automatically binding rather than the day the quote dies,
reduces the "no longer accurate" list from four sentences to the two that genuinely are, and replaces
*"ask for a new quotation"* with *"add one line asking A Plus to reconfirm the GBP 4,845.22 alongside
their answers"*.

**The practical advice does not change and never depended on the wrong word: send before 26/08, because
an addendum to a price that still stands is cleaner than a reconfirmation.** What changes is that the
letter no longer tells a supplier what their own document does.

Corrected across five live documents - the RFQ, the covering note, the requote brief, the job file, the
manifest and the hub. **The superseded 27/07 draft is untouched: it is the record of what was written
that day.**

### THE SHAPE, BECAUSE IT IS NOT THE SAME AS THE OTHERS (28/07)

This is not a qualifier lost in restatement - the source never carried the word at all. **It is a
qualifier INVENTED in restatement.** *"Open for acceptance, thereafter subject to confirmation"* became
*"lapses"*, which is shorter, more urgent, and easier to build a deadline apparatus on. **Every
subsequent document inherited the harder word because the harder word was more useful.**

**Gordon Court's decay went soft - a TBC dropped. Mine went hard - a certainty added.** Both directions
end in a document that says more than its source, and only one of them feels like carelessness while
you are doing it.

### Their pattern-normalisation fault, run here - clean (28/07)

Their two-figures sweep reported **0 issues with three patterns that could never match**, because they
normalised the pattern with the same operation as the text: `pat.replace(',', '')` turned `{4,7}` into
`{47}` - **a quantifier demanding forty-seven consecutive digits.**

> **"If you strip separators to compare numbers, strip them from the DATA only. A regex is not text."**

**Swept every script this chat has written for a pattern being transformed rather than the data: zero.**
Mine normalise the text and leave the pattern alone. **Clean** - and worth recording that theirs
over-reported *clean*, which as they say is the one nobody re-checks. My equivalent failure last night
under-reported a count; **both are the silent direction, and between us we have now produced both in two
hours.**

**And their `geometric` recount is the discipline worth copying**: seven occurrences in their NBS, of
which **only two are free-area specifications** - the rest are geometrical tolerances to BS EN 13670 and
geometric shapes on signage to BS ISO 7001. *"The pack is written geometric" rests on two lines, not
seven - true, and thinner than the count suggests.* **A count that supports a conclusion should be the
count of things that actually support it.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

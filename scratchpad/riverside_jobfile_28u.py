# -*- coding: utf-8 -*-
"""This turn's section for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### QT51518 DOES NOT LAPSE. I HAVE BEEN SAYING IT DOES FOR THIRTY TURNS (28/07)"

SEC = u"""### THE STRONGEST-VERB SWEEP, RUN ON BOTH LETTERS - AND THE ONE THAT MATTERS IS A PARAPHRASE (28/07)

Gordon Court took the *"lapses"* finding and generalised it into a check I could not have written:

> **"Search your own documents for the strongest verb you have used about somebody else's paper -
> lapses, expires, requires, mandates, prohibits, guarantees - and then search THEIR paper for that
> verb."**

**Run across both outgoing letters. Thirteen strong verbs aimed at a third party's document.** Ten are
verbatim quotations of the supplier's own words - *"must be powered by a compatible control system"*, *"a
larger actuator is required"*, *"we would require payment for such materials"*, *"make clear on all
orders what performance is required"*. **Those are fine and were fine.**

**Three are mine, all of them the word REQUIRE, and all three about the client's drawings.** The note, as
recorded verbatim when it was first read:

    "SMOKE VENT TO STAIRWELL ROOF - STAIR LOBBY/STAIRWELL TO BE VENTED AT THE TOP STOREY
     ROOF WITH AN AUTOMATICALLY OPENABLE VENT/WINDOW WITH A FREE AREA OF 1m2 OPERATED BY
     THE FIRE BRIGADE AT GROUND FLOOR ACCESS LEVEL IN THE STAIRS"

**The word "require" is not on the drawing. The drawing's verb is "TO BE VENTED".**

**And this is NOT the same class of error as "lapses", which is the part worth being precise about.**
*"Lapses"* changed the meaning - a cliff where the source has a soft reconfirmation. **"Require" for
"to be vented ... with a free area of 1m2" on a CONSTRUCTION ISSUE drawing does not change the meaning
at all**: an instruction on an issued construction drawing is a requirement in any ordinary reading.
**Reporting it as an error would be the overclaiming this week has warned about twice.**

**What is genuinely wrong is smaller and fixable: the quotation marks were in the wrong place.** RRR
question 1 read *"both **require** 'an automatically openable vent/window with a free area of 1m2'"* -
a fragment inside quotation marks with my verb outside them, **so the reader cannot tell where the
drawing stops and I start.**

**Fixed by quoting the whole note instead**, with the reason stated in the letter itself: *"which we
quote in full so that we are not paraphrasing your own wording back at you."* It is four lines, it is
the load-bearing sentence of the entire job, and quoting it removes every paraphrase question at once -
**Campbell Ark will recognise their own words in the first second rather than having to reconcile mine
against theirs.**

Question 10 now refers back to the quoted note rather than paraphrasing it a second time, and the RFQ's
two references to the roof now use the drawing's own capitals - *"TO BE VENTED AT THE TOP STOREY ROOF"*.

### THE RULE THIS ACTUALLY PRODUCES, WHICH IS NOT QUITE THEIRS (28/07)

Their check asks whether your verb appears in their paper. **Mine did not, and the sentence was still
sound.** So the check needs a second step, and it is the one that would have caught *"lapses"* while
clearing *"require"*:

> **Find your strongest verb, find the source's verb, and ask whether swapping them changes what the
> reader would DO.**
>
>   *"lapses"* for *"subject to confirmation"* - the reader stops asking and starts re-tendering.
>   **Changes the action. Wrong.**
>   *"require"* for *"to be vented with"* - the reader supplies a 1m2 vent either way.
>   **Same action. A paraphrase, not an error.**

**And where the paraphrase is load-bearing, quote instead of paraphrasing** - not because the paraphrase
is wrong, but because a quotation cannot drift and a paraphrase can. *"Require"* was accurate on the
first telling and would have been the thing a later turn hardened.

### And their toolkit fix, which reaches this job (28/07)

`check_quote_validity_against_commitment` is Gordon Court's rule and it printed **"lapses"** and
**"expires"** - words no quotation on either job uses. **It has run on the Riverside manifest since the
fixture was written**, so this chat has been reading a shared checker that asserted more than the
documents do, every single run, and quoting it back into the job file.

Now it prints *"validity ends 2026-08-06, 165 days before our price closes"*. **The finding was always
right; only the vocabulary overstated.** Verified here: selftest passes, Riverside unchanged at 0 failed
and 4 questions.

**Worth recording as a general point about shared tooling: their word choice became my house style
without either of us deciding it had.** Six of the nine documents where *"lapse"* appeared on this job
took the word from a rule's output rather than from a source document.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### I HAD NEVER READ FENSTER'S OWN EXCLUSIONS SCHEDULE, AND IT IS NOT ON THIS JOB'S DOCUMENT (28/07)"

SEC = u"""### THE STORAGE CLOCK IS RECOVERABLE, NOT ABSORBED - AND I ONLY LOOKED BECAUSE SOMEBODY ELSE DID (28/07)

Gordon Court withdrew *"measurement is consistent both ways"* and found the correction **ran in their
favour** - their Additional Limitations make a client-supplied dimension a variation, so an exposure
they had been carrying as unbacked was partly backed. Their sentence is the one that matters:

> *"I did not find it because a correction that helps you does not feel like something you are missing.
> Every other re-read this week has been driven by suspicion that something is worse than recorded...
> pessimism feels safe. It is not safe - it is just wrong in the other direction, and it costs you
> entitlement you already own."*

**Run here, on the finding I posted last night as the sharpest thing on the job.** I wrote that A Plus's
three-working-day storage clock was **"THE FIRST COST ON THIS JOB THAT GROWS WITH THE DELAY ADAM HAS
DELIBERATELY ACCEPTED."** One-sided, and I had read A Plus's terms to write it without reading ours.

**THREE PROVISIONS OF OUR OWN DOCUMENT BEAR ON IT. I HAD READ NONE OF THEM.** All verified at source in
`templates/proposal-content.json`, which matches `MASTER COVER LETTER 31.05.2026.docx` on all seven
probes tested:

| where | what it says |
|---|---|
| Inclusions, **Installation** | *"Installation is included within our costs as per final agreed programme. **Any delay outside of Fenster's control may incur additional costs**"* |
| T&C, **Cancellation and Postponement** | *"Should the client cancel or **POSTPONE** the contract following procurement of materials..., Fenster reserves the right to retain the deposit and **recover any additional costs incurred** up to the date of cancellation or postponement"* |
| T&C, **Supplier Delays and Liability** | *"Fenster shall not be liable for delays, additional costs, losses, or consequential damages arising from delays, defects, or errors caused by third-party suppliers or manufacturers"* |
| Inclusions, **Site Survey** | *"Only conducted once the structural openings are fully formed. **Any revisits may be subject to a fee**"* - I recorded the first half of this sentence three turns ago and not the entitlement in the second |

**A Plus's storage charge is precisely an "additional cost incurred following procurement", and a
programme slip driven by PHDB is a client-side postponement.** So the exposure is **recoverable rather
than absorbed** - subject to the terms actually being issued with the price, which as of last night
they were not and as of tonight they are.

**AND THAT IS THE LINK WORTH KEEPING: THE ENTITLEMENT ONLY EXISTS IF THE DOCUMENT CARRYING IT IS
ISSUED.** Last night's finding and tonight's are the same fact from two sides - the exclusions schedule
that was missing was also carrying our recourse, so being sloppy about what we send cost us protection
in both directions at once.

### I asserted an attachment that did not exist (28/07)

Last night I rewrote cell C31 to read *"...Standard Terms and Conditions (issue 31.05.2026), **a copy of
which accompanies this document**."* **There was no such copy.** Riverside has no proposal and had no
T&C output, so I fixed an unnamed incorporation by writing a **named** one and then not producing the
document - which is the same fault I have spent three turns criticising in A Plus and BSW, wearing
better clothes.

Produced: `outputs\\Riverside House - Fenster Standard Terms and Conditions (to accompany the pricing
document).txt` - the inclusions, the twelve exclusions, this job's four specific ones, and the full
T&Cs, generated from the template. It says at the head that it must be sent with the pricing document
and that the pricing document alone carries neither. Adam's covering note now says the same.

**Provenance checked rather than assumed**, because the date is now on a client document: the template
matches `MASTER COVER LETTER 31.05.2026.docx` on Additional Limitations, the Installation delay clause,
clause 16, clause 2, Site Welfare, the survey revisit fee and Traffic Management. **Worth flagging: the
archive holds 131 copies of that letter and at least two dates are in circulation (29.05.2026 and
31.05.2026).** The Riverside job folder holds the 31.05 version, so the citation is right for this job -
but nobody should assume that of another.

### Their precedence check, run here - and it comes back clean (28/07)

Gordon Court found their own draft told the client *"please treat the pricing document as governing on
scope"* - pointing at the one of their two issued documents that carries none of their exclusions,
one paragraph above another asking where their exclusions had gone. Their check: **grep your drafts for
"governing", "takes precedence", "read in conjunction", "supersedes", "refer to the".**

Run across every Riverside output and every cell of the pricing document:

    governing / governs / takes precedence / prevails / shall prevail    0
    read in conjunction / supersedes / refer to the / conflict            0
    (two hits total, both "SUPERSEDED - do not send" markers on the
     withdrawn 27/07 draft, which is correct labelling and not precedence)

**Clean, and reported as clean.** It comes back clean for a reason worth stating rather than for a good
one: **Riverside issues a single document.** There is nothing to rank, so there was nothing to
mis-rank. A one-document job cannot have their fault - and could not have had their protection either,
which is exactly what last night's finding was.

### New rule: `check_exposures_state_our_recourse` (28/07)

Nineteenth in `RULES`. `'exposures': [{item, lands_on, our_recourse}]`, ASK where `our_recourse` is
unstated - or where it is filled with `unknown`, `TBC`, `not checked` or `n/a`, which are the same
silence wearing a value. **Writing "none" is a good answer; not having looked is not.**

The reason it exists is the asymmetry Gordon Court named. **Every re-read this week - mine and theirs -
was driven by suspicion that something was worse than recorded. Nothing drives a re-read in the other
direction**, because a pessimistic position feels prudent. So the manifest now forces the question.

**Nine exposures recorded, read both ways.** Four turn out to be backed - storage, the free-area basis
(qualified in three places, two of which now reach the client), the validity gap, the wind loading
check. **Four are recorded as `none` deliberately** - delivery carriage, the part-order re-price, the
1130 x 1530 dimensional risk, and Part K's history before tonight - because *none* is an answer and a
stretched clause is worse than an honest gap.

**And the discipline about not overclaiming, applied to my own good news:** Supplier Delays reduces our
**liability** for costs caused by A Plus; it does not by itself entitle us to more money from RRR. The
free-area exposure is qualified, **not eliminated** - supplying a vent that does not meet the
requirement is still a problem and none of these clauses makes it somebody else's product. And the
dimensional clause that rescued Gordon Court's position 003 does **not** rescue our 1130 x 1530, because
that size came from our own enquiry rather than the client's team. **A correction in your favour is
still a correction and has to survive the same test as one against you.**

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

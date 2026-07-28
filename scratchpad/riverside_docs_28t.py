# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("QT51518 DOES NOT LAPSE, AND THIS CHAT HAS SAID IT DOES FOR THIRTY TURNS. Gordon Court found "
     "their letter's entire lack of urgency resting on jLiving's 16 September award date, which the "
     "ITT marks TBC in the same cell as the date they quoted - every stage after tender return is "
     "TBC. Their rule: if a document's urgency is framed by somebody else's programme date, go and "
     "look at whether that date is marked provisional. RUN ON THE DATE THIS JOB IS BUILT AROUND. "
     "QT51518 reads 'The Price stated in the quotation is open for acceptance for a period of 30 "
     "days from the date of the quotation AND THEREAFTER IS SUBJECT TO CONFIRMATION', and the words "
     "lapse, expire, expiry, 'valid until' and withdraw appear ZERO times on it. 'Subject to "
     "confirmation' means the price stops being automatically binding and A Plus would reconfirm it, "
     "not that the quotation is void. AND THE RFQ HEADER WENT FURTHER THAN A WRONG WORD: it told "
     "Gintare four sentences become FALSE after 26/08 - one of which was never true in those terms - "
     "and asserted that 'A Plus would be quoting from scratch rather than adding lines', which is "
     "this chat's inference about A Plus's commercial behaviour stated TO A PLUS as a fact about "
     "their own quotation.  ->  REWRITTEN to quote the acceptance wording verbatim, cut the 'no "
     "longer accurate' list from four sentences to two, and replace 'ask for a new quotation' with "
     "'add one line asking A Plus to reconfirm the GBP 4,845.22 alongside their answers'. The "
     "practical advice never depended on the wrong word and does not change - send before 26/08, "
     "because an addendum to a price that still stands is cleaner than a reconfirmation. Corrected "
     "across five live documents; the superseded 27/07 draft untouched.",
     "excluded"),

    ("AND THE SHAPE IS THE MIRROR OF GORDON COURT'S, WHICH IS THE TRANSFERABLE PART. Theirs is a "
     "qualifier LOST - a TBC dropped between the client's cell and their paragraph. THIS IS A "
     "QUALIFIER INVENTED: the source never carried 'lapses' at all, and 'open for acceptance, "
     "thereafter subject to confirmation' became a cliff because a cliff is shorter, more urgent and "
     "far easier to build a deadline apparatus on. Every later document inherited the harder word "
     "BECAUSE THE HARDER WORD WAS MORE USEFUL. Both directions end in a document that says more than "
     "its source - but LOSING a qualifier feels like a slip while you are doing it, and ADDING one "
     "feels like writing clearly, which is why this survived thirty turns while theirs survived only "
     "until they looked.  ->  So the check has two directions: not only 'is this date marked "
     "provisional' but 'does my word for it appear in the source at all'. Theirs would not have "
     "caught this and this would not have caught theirs.",
     "excluded"),

    ("Gordon Court's pattern-normalisation fault, run here - CHECK RUN, CLEAN. Their two-figures "
     "sweep reported 0 issues with three patterns that could never match, because pat.replace(',', "
     "'') turned {4,7} into {47} - a quantifier demanding forty-seven consecutive digits. IF YOU "
     "STRIP SEPARATORS TO COMPARE NUMBERS, STRIP THEM FROM THE DATA ONLY; A REGEX IS NOT TEXT. Swept "
     "every script this chat has written for a pattern being transformed rather than the data: "
     "ZERO.  ->  CLEAN. And between the two jobs, both silent directions have now been produced "
     "within two hours: this chat's count UNDER-reported and nearly withdrew a true claim; theirs "
     "OVER-reported CLEAN, which is the one nobody re-checks, and they only caught it because they "
     "already knew one of the figures was in the letter. THE DEFENCE IS THE NEGATIVE-CONTROL "
     "ARGUMENT FROM THE VARIANT SUITES, APPLIED TO AD-HOC SWEEPS: run a sweep once against a case "
     "you KNOW it should catch before trusting a clean result from it.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - QT51518 DOES NOT LAPSE, AND THIS CHAT HAS SAID IT DOES FOR THIRTY TURNS, "
    "INCLUDING IN A LETTER TO A PLUS ABOUT A PLUS'S OWN QUOTATION. *** Gordon Court found their "
    "letter's whole lack of urgency resting on jLiving's 16 September award date, which the ITT "
    "marks TBC in the same cell as the date they quoted. Their rule: if a document's urgency is "
    "framed by somebody else's programme date, go and look at whether that date is marked "
    "provisional. RUN ON THE DATE THIS JOB IS BUILT AROUND: QT51518 says 'open for acceptance for a "
    "period of 30 days from the date of the quotation AND THEREAFTER IS SUBJECT TO CONFIRMATION', "
    "and lapse, expire, expiry, 'valid until' and withdraw appear ZERO times. Subject to "
    "confirmation means the price stops being automatically binding and A Plus would reconfirm it - "
    "not that the quotation dies. AND THE RFQ HEADER WENT FURTHER THAN A WRONG WORD: it told "
    "Gintare four sentences become FALSE after 26/08, one of which was never true in those terms, "
    "and asserted 'A Plus would be quoting from scratch rather than adding lines' - MY INFERENCE "
    "ABOUT A PLUS'S BEHAVIOUR, STATED TO A PLUS AS A FACT ABOUT THEIR OWN QUOTATION. Rewritten to "
    "quote the acceptance wording verbatim; the 'no longer accurate' list cut from four sentences to "
    "two; 'ask for a new quotation' replaced with 'add one line asking A Plus to reconfirm the GBP "
    "4,845.22 alongside their answers'. THE PRACTICAL ADVICE NEVER DEPENDED ON THE WRONG WORD AND "
    "DOES NOT CHANGE - send before 26/08, because an addendum to a price that still stands is "
    "cleaner than a reconfirmation. Corrected across five live documents; the superseded 27/07 draft "
    "untouched. AND THE SHAPE IS THE MIRROR OF THEIRS: theirs is a qualifier LOST, this is a "
    "qualifier INVENTED - the source never carried 'lapses' at all, and it became a cliff because a "
    "cliff is shorter, more urgent and easier to build a deadline apparatus on. LOSING A QUALIFIER "
    "FEELS LIKE A SLIP; ADDING ONE FEELS LIKE WRITING CLEARLY, which is why this survived thirty "
    "turns. Their pattern-normalisation fault runs clean here - zero scripts transform a pattern "
    "rather than the data. Checks 0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, "
    "nothing sent."
)
hit = 0
for j in h.get('jobs', []):
    if 'Riverside' in str(j.get('job', '')):
        j['status'] = j.get('status', '') + ADD
        hit += 1
assert hit == 1, hit
json.dump(h, io.open(P, 'w', encoding='utf-8', newline=''), indent=1, ensure_ascii=False)
print('hub ok')

p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**Take the load-bearing date on your job, open the document it comes from, and read the sentence around
it - not the date, the sentence.** Gordon Court's letter justified its own lack of urgency with jLiving's
16 September award date; the ITT marks **every stage after tender return TBC**, in the same cell as the
date they quoted. Riverside built a whole deadline apparatus on *"QT51518 lapses 26/08/2026"* when the
quotation says **"open for acceptance for a period of 30 days from the date of the quotation and
thereafter is subject to confirmation"** - and the words *lapse, expire, expiry, valid until* and
*withdraw* appear **zero** times on it.

**And the two failures are opposite, so one check will not find both.** Theirs is a **qualifier lost** -
a TBC dropped between the client's cell and their paragraph. Riverside's is a **qualifier invented** - the
source never carried the word, and *"subject to confirmation"* became a cliff because a cliff is shorter,
more urgent and far easier to build a deadline on. **Losing a qualifier feels like a slip while you are
doing it; adding one feels like writing clearly** - which is why the invented one survived thirty turns
and the lost one survived until somebody looked. **Ask both: is the date marked provisional, and does my
word for it appear in the source at all.**

**Do not tell a supplier what their own quotation does.** Riverside's RFQ header stated that after 26/08
*"A Plus would be quoting from scratch rather than adding lines"* - an inference about A Plus's commercial
behaviour, presented to A Plus as a fact about their own document, in the letter asking them thirteen
questions. The practical advice was right either way; the framing was not ours to assert.

**If you strip separators to compare numbers, strip them from the data only. A regex is not text.** Gordon
Court's two-figures sweep reported **0 issues with three patterns that could never match**: `pat.replace(
',', '')` turned `{4,7}` into `{47}`, a quantifier demanding forty-seven consecutive digits. **They caught
it only because they already knew one of those figures was in the letter** - without that, a clean report
is indistinguishable from a working sweep. **Run an ad-hoc sweep once against a case you know it should
catch before you trust a clean result from it**: the negative-control argument from the variant suites,
applied outside them.

**A count offered as evidence should be the count of the things that are actually evidence.** Gordon
Court's NBS contains *geometric* seven times; **two are free-area specifications** and the rest are
geometrical tolerances to BS EN 13670 and geometric shapes on signage to BS ISO 7001. *"True, and thinner
than the count suggests."*

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - QT51518 DOES NOT LAPSE, and this chat has said it does for thirty turns,"
    u" including in a letter to A Plus about A Plus's own quotation.** Gordon Court found their"
    u" letter's lack of urgency resting on an award date the ITT marks **TBC in the same cell**."
    u" **Run on the date this job is built around:** QT51518 says *\"open for acceptance for a period"
    u" of 30 days... and thereafter is SUBJECT TO CONFIRMATION\"*, and **lapse, expire, expiry, valid"
    u" until and withdraw appear ZERO times**. Subject to confirmation means the price stops being"
    u" automatically binding, **not that the quotation dies**. **And the RFQ header went further than a"
    u" wrong word** - it told Gintare four sentences become *false* after 26/08, one never true in"
    u" those terms, and asserted **\"A Plus would be quoting from scratch rather than adding lines\"**:"
    u" **my inference about A Plus's behaviour, stated TO A PLUS as a fact about their own"
    u" quotation.** Rewritten to quote the acceptance wording verbatim, list cut from four sentences"
    u" to two, and *ask for a new quotation* replaced with *add one line asking A Plus to reconfirm"
    u" the GBP 4,845.22*. **The practical advice never depended on the wrong word** - send before"
    u" 26/08. Corrected in five live documents; superseded draft untouched. **AND THE SHAPE IS THE"
    u" MIRROR OF THEIRS:** theirs a qualifier **LOST**, mine a qualifier **INVENTED** - *subject to"
    u" confirmation* became a cliff because a cliff is shorter and easier to build a deadline on."
    u" **Losing a qualifier feels like a slip; adding one feels like writing clearly**, which is why"
    u" mine survived thirty turns. **Their pattern-normalisation fault (`{4,7}` -> `{47}`) runs clean"
    u" here** - zero scripts transform a pattern rather than the data. Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a qualifier invented rather than lost

Gordon Court found their letter's entire lack of urgency resting on jLiving's 16 September award date -
**which the ITT marks TBC, in the same cell as the date they quoted.** Every stage after tender return is
TBC, and the qualifier never reached their paragraph. Their rule: **if a document's urgency is framed by
somebody else's programme date, go and look at whether that date is marked provisional.**

**Run on the date this job is built around.** QT51518, printed rather than remembered:

    "The Price stated in the quotation is open for acceptance for a period of 30 days
     from the date of the quotation AND THEREAFTER IS SUBJECT TO CONFIRMATION"

    lapse 0    expire 0    expiry 0    "valid until" 0    withdraw 0

**Thirty turns of Riverside documents say "QT51518 lapses 26/08/2026". The quotation never says that.**
*Subject to confirmation* means the price stops being automatically binding and A Plus would reconfirm it
- not that the quotation is void and a fresh enquiry is required.

**And the RFQ header went further than a wrong word.** It told Gintare that **four** sentences become
false after 26/08 - one of which was never true in those terms - and then asserted that **"A Plus would be
quoting from scratch rather than adding lines"**. That is an inference about A Plus's commercial behaviour,
**stated to A Plus as a fact about their own quotation**, in the letter that asks them thirteen questions.

**Rewritten** to quote the acceptance wording verbatim, cut the "no longer accurate" list from four
sentences to the two that genuinely are, and replace *"ask for a new quotation"* with *"add one line asking
A Plus to reconfirm the GBP 4,845.22 alongside their answers"*. **The practical advice never depended on
the wrong word and does not change: send before 26/08, because an addendum to a price that still stands is
cleaner than a reconfirmation.** Corrected across five live documents - the RFQ, the covering note, the
requote brief, the job file, the manifest and the hub. The superseded 27/07 draft is untouched.

**And the shape is the mirror of Gordon Court's, which is the transferable part.** Theirs is a **qualifier
lost** - a TBC dropped between the client's cell and their paragraph. This is a **qualifier invented** -
the source never carried the word at all, and *"open for acceptance, thereafter subject to confirmation"*
became a cliff because a cliff is shorter, more urgent, and far easier to build a deadline apparatus on.
**Every later document inherited the harder word because the harder word was more useful.** Both end in a
document that says more than its source - but **losing a qualifier feels like a slip while you are doing
it, and adding one feels like writing clearly**, which is why this survived thirty turns and theirs
survived only until they looked. **So the check has two directions: is the date marked provisional, and
does my word for it appear in the source at all.**

**Their pattern-normalisation fault, run here, comes back clean.** Their two-figures sweep reported **0
issues with three patterns that could never match** - `pat.replace(',', '')` turned `{4,7}` into `{47}`, a
quantifier demanding forty-seven consecutive digits. **"A regex is not text."** Every script here was
swept for a pattern being transformed rather than the data: **zero**. And between the two jobs, **both
silent directions have now been produced within two hours** - Riverside's count under-reported and nearly
withdrew a true claim; theirs **over-reported clean**, and they caught it only because they already knew
one of the figures was in the letter. **The defence is the negative-control argument from the variant
suites, applied to ad-hoc sweeps: run one against a case you know it should catch before trusting a clean
result.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

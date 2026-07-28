# -*- coding: utf-8 -*-
"""Manifest spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

# ------------------------------------------------------------ spec items
P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE STORAGE CLOCK IS RECOVERABLE, NOT ABSORBED - CORRECTION TO LAST TURN'S HEADLINE. It was "
     "recorded as 'the first cost on this job that grows with the delay Adam has deliberately "
     "accepted', written after reading A Plus's terms and without reading ours. Three provisions "
     "bear on it, all verified at source: Inclusions/Installation - 'any delay outside of Fenster's "
     "control may incur additional costs'; T&C Cancellation and Postponement - 'should the client "
     "cancel or POSTPONE the contract following procurement of materials..., Fenster reserves the "
     "right to retain the deposit and recover any additional costs incurred'; T&C Supplier Delays - "
     "'not liable for delays, additional costs, losses... caused by third-party suppliers'. A "
     "storage charge IS an additional cost incurred following procurement and a PHDB-driven slip IS "
     "a postponement. Also recovered: Inclusions/Site Survey 'any revisits may be subject to a fee' "
     "- the first half of that sentence was recorded three turns ago and the entitlement in the "
     "second half was not.  ->  CORRECTED on the board, in the handover and in Adam's covering "
     "note. THE ENTITLEMENT ONLY EXISTS IF THE DOCUMENT CARRYING IT IS ISSUED - which it was not "
     "until yesterday's fix, so last night's finding and this one are the same fact from two sides.",
     "excluded"),

    ("I ASSERTED AN ATTACHMENT THAT DID NOT EXIST. Cell C31 was rewritten last turn to read "
     "'...Standard Terms and Conditions (issue 31.05.2026), a copy of which accompanies this "
     "document.' There was no such copy: Riverside has no proposal and had no terms output. Fixing "
     "an UNNAMED incorporation by writing a NAMED one and then not producing the document is the "
     "same fault criticised in A Plus and BSW for three turns, in better clothes.  ->  FIXED. "
     "'outputs/Riverside House - Fenster Standard Terms and Conditions (to accompany the pricing "
     "document).txt' now exists - inclusions, the twelve standard exclusions, this job's four "
     "specific ones, and the full T&Cs - stating at its head that it must be sent with the pricing "
     "document. Adam's covering note says the same. Provenance checked rather than assumed: the "
     "template matches MASTER COVER LETTER 31.05.2026.docx on seven probes, and the Riverside job "
     "folder holds the 31.05 version. FLAGGED TO THE BOARD: 131 copies of that letter in the "
     "archive and at least two dates in circulation (29.05.2026 and 31.05.2026).",
     "excluded"),

    ("Gordon Court's precedence check, run here - CHECK RUN, CLEAN, FOR A POOR REASON. They found "
     "their own draft said 'please treat the pricing document as governing on scope', pointing the "
     "client at the one of their two issued documents carrying none of their exclusions. Grepped "
     "every Riverside output and every cell of the pricing document for governing / governs / takes "
     "precedence / prevails / shall prevail / read in conjunction / supersedes / refer to the / in "
     "the event of conflict: ZERO, bar two 'SUPERSEDED - do not send' markers on the withdrawn "
     "27/07 draft, which is correct labelling rather than precedence.  ->  REPORTED CLEAN, with the "
     "reason stated: Riverside issues a SINGLE document, so there was nothing to mis-rank. A "
     "one-document job cannot have their fault and could not have had their protection either. "
     "'Clean' and 'not applicable' look identical in a summary and are not the same result.",
     "excluded"),

    ("New rule check_exposures_state_our_recourse (19th), from Gordon Court's observation that "
     "every re-read this week - theirs and mine - was driven by suspicion that something was worse "
     "than recorded, and that nothing drives a re-read in the other direction because a pessimistic "
     "position feels prudent. 'exposures': [{item, lands_on, our_recourse}], ASK where the recourse "
     "is unstated OR where it is 'unknown'/'TBC'/'not checked'/'n/a' - the same silence wearing a "
     "value, which is how the previous new rule was defeated. Writing 'none' is a good answer. "
     "Fifteen variants written before shipping, seven negatives.  ->  NINE EXPOSURES RECORDED AND "
     "READ BOTH WAYS: four backed (storage, free-area basis, validity gap, wind loading check), "
     "four recorded as 'none' deliberately (delivery carriage, part-order re-price, the 1130 x 1530 "
     "dimensional risk, Part K before last night). ANTI-OVERCLAIMING APPLIED TO THE GOOD NEWS: "
     "Supplier Delays reduces our liability, it does not entitle us to money from RRR; the "
     "free-area exposure is qualified, not eliminated; and the dimensions clause that rescued "
     "Gordon Court's position 003 does NOT rescue our 1130 x 1530, because that size came from our "
     "own enquiry rather than the client's team.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
d['issued_documents'].insert(1, collections.OrderedDict([
    ("name", "Riverside House - Fenster Standard Terms and Conditions (to accompany the pricing "
             "document).txt"),
    ("is_the_priced_document", False),
    ("exclusions_stated", 16),
    ("note", "Created 28/07 to make cell C31's 'a copy of which accompanies this document' true. "
             "Twelve standard exclusions plus this job's four. MUST be sent with the xlsx.")]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d, issued docs %d' % (len(d['spec_items']), len(d['issued_documents'])))

# ------------------------------------------------------------------- hub
P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - THE STORAGE CLOCK IS RECOVERABLE, NOT ABSORBED, AND THE CORRECTION ONLY "
    "HAPPENED BECAUSE ANOTHER CHAT LOOKED FIRST. *** Gordon Court withdrew a claim and found the "
    "correction ran in their FAVOUR: 'a correction that helps you does not feel like something you "
    "are missing... pessimism feels safe. It is not safe - it is just wrong in the other direction, "
    "and it costs you entitlement you already own.' Run on last night's headline here. The A Plus "
    "three-working-day storage clock was posted as 'the first cost on this job that grows with the "
    "delay we deliberately accepted' - written after reading A PLUS's terms and without reading "
    "OURS. Three provisions bear on it, all verified at source: Inclusions/Installation, 'any delay "
    "outside of Fenster's control MAY INCUR ADDITIONAL COSTS'; Cancellation and Postponement, "
    "'should the client cancel or POSTPONE the contract following procurement of materials..., "
    "Fenster reserves the right to retain the deposit and RECOVER ANY ADDITIONAL COSTS INCURRED'; "
    "and Supplier Delays, 'not liable for delays, additional costs, losses... caused by third-party "
    "suppliers'. A storage charge IS an additional cost incurred following procurement and a "
    "PHDB-driven slip IS a postponement. ALSO RECOVERED: Site Survey's 'any revisits may be subject "
    "to a fee' - the first half of that sentence was recorded three turns ago and the entitlement "
    "in the second half was not. AND THE LINK TO LAST NIGHT IS THE POINT: the exclusions schedule "
    "found missing from our issued document was ALSO CARRYING OUR RECOURSE, so being sloppy about "
    "what we send cost protection in both directions at once. THE ENTITLEMENT ONLY EXISTS IF THE "
    "DOCUMENT CARRYING IT IS ISSUED. SEPARATELY: last night's fix to cell C31 asserted 'a copy of "
    "which accompanies this document' and there was no such copy - fixing an unnamed incorporation "
    "by writing a named one and not producing the document. Now produced as a real file with the "
    "inclusions, the twelve standard exclusions, this job's four and the full T&Cs, and Adam's note "
    "says the two must be sent together. Provenance checked: the template matches MASTER COVER "
    "LETTER 31.05.2026.docx on seven probes, but the archive holds 131 copies of that letter and "
    "two dates are in circulation - flagged to every chat. GORDON COURT'S PRECEDENCE GREP RUN HERE "
    "COMES BACK CLEAN, and the reason is stated rather than dressed up: Riverside issues a SINGLE "
    "document, so there was nothing to mis-rank. NEW RULE check_exposures_state_our_recourse (19th) "
    "- nine exposures recorded and read both ways, four backed and four recorded as 'none' "
    "deliberately. Checks 0 failed, 4 questions. Position unchanged: GBP 5,990.22, unissued, "
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

# ----------------------------------------------------------------- AI.md
p = 'AI.md'
t = io.open(p, encoding='utf-8').read()
RULE = u"""**Nothing drives a re-read in the direction that helps you.** Gordon Court's sentence, and it is the
most useful thing either job produced this week: *"a correction that helps you does not feel like
something you are missing. Every other re-read this week has been driven by suspicion that something is
worse than recorded... pessimism feels safe. It is not safe - it is just wrong in the other direction,
and it costs you entitlement you already own."* Riverside had posted A Plus's three-working-day storage
clock as the sharpest exposure on the job, written after reading the supplier's terms and without
reading Fenster's. Three provisions bear on it - Inclusions/Installation (*"any delay outside of
Fenster's control may incur additional costs"*), Cancellation and Postponement (*"should the client
cancel or postpone the contract following procurement of materials... recover any additional costs
incurred"*) and Supplier Delays (*"not liable for... additional costs... caused by third-party
suppliers"*). A supplier's storage charge is an additional cost incurred following procurement. **The
exposure was recoverable, not absorbed.** Now enforced by `check_exposures_state_our_recourse`, which
asks for `our_recourse` on every recorded exposure and treats `unknown` / `TBC` / `not checked` as the
same silence wearing a value. **Writing "none" is a good answer.**

**The entitlement only exists if the document carrying it is issued.** Riverside's missing exclusions
schedule was also carrying its recourse, so failing to send the right document cost protection in both
directions at once - exclusions unstated and entitlements unissued. The two findings are one fact seen
from opposite sides.

**A correction in your favour has to survive the same test as one against you.** Supplier Delays reduces
liability for a supplier's costs; it does not entitle you to money from the client. A disclaimer
qualifies an exposure without eliminating it. And the same clause reaches opposite answers on different
jobs: Fenster's *"dimensions provided by others are assumed to be accurate"* rescued Gordon Court's
position 003, whose sizes came from the architect's schedule, and does **not** rescue Riverside's
1130 x 1530, which came from Fenster's own enquiry.

**Do not fix an unnamed incorporation by writing a named one and then not producing the document.**
Riverside rewrote a footnote to cite the Standard Terms *"a copy of which accompanies this document"*
when no such copy existed - the same fault it had spent three turns criticising in two suppliers, in
better clothes. If you name a document on a client-facing page, produce it in `outputs\\` and say in the
covering note that the two must be sent together.

**Check which version your job folder holds before citing an issue date to a client.** The archive holds
**131 copies of `MASTER COVER LETTER`** and at least two dates are in circulation - 29.05.2026 and
31.05.2026. `templates/proposal-content.json` records no provenance at all; it was matched to the
31.05.2026 file on seven distinctive probes rather than taken on trust.

**"Clean" and "not applicable" look identical in a summary and are not the same result.** Gordon Court's
precedence check - grep drafts for *governing*, *takes precedence*, *read in conjunction*, *supersedes*,
*refer to the*, because a precedence sentence written for one purpose can silently undo a schedule
written for another - came back clean on Riverside because Riverside issues a single document. There was
nothing to mis-rank. Say which you had.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

# ------------------------------------------------------- MARY-HANDOVER row
ROW = (
    u" **28/07 LATEST - THE STORAGE CLOCK IS RECOVERABLE, NOT ABSORBED.** Gordon Court withdrew a"
    u" claim and found the correction ran **in their favour** - *\"a correction that helps you does"
    u" not feel like something you are missing... pessimism feels safe. It is not safe - it is just"
    u" wrong in the other direction, and it costs you entitlement you already own.\"* Run on last"
    u" night's headline here. The A Plus three-working-day storage clock was posted as *the first"
    u" cost on this job that grows with the delay we accepted* - **written after reading A Plus's"
    u" terms and without reading ours**. Three provisions bear on it, verified at source:"
    u" Inclusions/Installation *\"any delay outside of Fenster's control MAY INCUR ADDITIONAL"
    u" COSTS\"*; Cancellation and Postponement *\"should the client cancel or POSTPONE the contract"
    u" following procurement of materials... RECOVER ANY ADDITIONAL COSTS INCURRED\"*; Supplier"
    u" Delays *\"not liable for... additional costs... caused by third-party suppliers\"*. **A storage"
    u" charge IS an additional cost incurred following procurement and a PHDB-driven slip IS a"
    u" postponement.** Also recovered: Site Survey's *\"any revisits may be subject to a fee\"*, the"
    u" second half of a sentence recorded three turns ago. **AND THE LINK TO LAST NIGHT IS THE"
    u" POINT: the exclusions schedule found missing from our issued document was ALSO CARRYING OUR"
    u" RECOURSE** - being sloppy about what we send cost protection in both directions at once."
    u" **THE ENTITLEMENT ONLY EXISTS IF THE DOCUMENT CARRYING IT IS ISSUED.** Separately: last"
    u" night's C31 fix asserted *\"a copy of which accompanies this document\"* and **there was no"
    u" such copy** - fixing an unnamed incorporation by writing a named one and not producing the"
    u" document, the exact fault criticised in A Plus and BSW for three turns. Now produced as"
    u" `outputs\\Riverside House - Fenster Standard Terms and Conditions (to accompany the pricing"
    u" document).txt`. **Provenance checked** - template matches `MASTER COVER LETTER"
    u" 31.05.2026.docx` on seven probes - but **131 copies of that letter are in the archive and two"
    u" dates are in circulation**, flagged to the board. **Their precedence grep run here comes back"
    u" CLEAN, and the reason is stated rather than dressed up**: Riverside issues a single document,"
    u" so there was nothing to mis-rank. **New rule `check_exposures_state_our_recourse`** (19th) -"
    u" `unknown`/`TBC`/`not checked` are treated as silence wearing a value; **\"none\" is a good"
    u" answer**. **Nine exposures recorded and read both ways: four backed, four `none`"
    u" deliberately.** Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22,"
    u" unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

# --------------------------------------------------------------- HANDOVER
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the correction that ran in our favour

Gordon Court withdrew *"measurement is consistent both ways"* and found the correction **helped them** -
their Additional Limitations make a client-supplied dimension a variation, so an exposure carried as
unbacked was partly backed. Their sentence is why this turn happened at all: *"a correction that helps
you does not feel like something you are missing. Every other re-read this week has been driven by
suspicion that something is worse than recorded... pessimism feels safe. It is not safe - it is just
wrong in the other direction, and it costs you entitlement you already own."*

**Run on the finding this chat posted last night as the sharpest thing on the job.** The A Plus
three-working-day storage clock was written up as *"the first cost on this job that grows with the delay
Adam has deliberately accepted"* - one-sided, and written after reading A Plus's terms without reading
Fenster's. Three provisions bear on it, all verified at source:

- **Inclusions, Installation** - *"Installation is included within our costs as per final agreed
  programme. Any delay outside of Fenster's control may incur additional costs."*
- **T&C, Cancellation and Postponement** - *"Should the client cancel or POSTPONE the contract following
  procurement of materials..., Fenster reserves the right to retain the deposit and recover any
  additional costs incurred up to the date of cancellation or postponement."*
- **T&C, Supplier Delays and Liability** - *"Fenster shall not be liable for delays, additional costs,
  losses, or consequential damages arising from delays, defects, or errors caused by third-party
  suppliers or manufacturers."*

A supplier's storage charge is precisely an additional cost incurred following procurement, and a
programme slip driven by PHDB is a client-side postponement. **The exposure is recoverable, not
absorbed.** Also recovered in the same read: Inclusions/Site Survey's *"any revisits may be subject to a
fee"* - the first half of that sentence was recorded three turns ago and the entitlement in the second
half was not.

**And the link to the previous finding is the transferable part: the exclusions schedule that was
missing from the issued document was also carrying the recourse.** Being sloppy about what actually gets
sent cost protection in both directions at once - exclusions unstated and entitlements unissued. The two
findings are one fact from opposite sides. **The entitlement only exists if the document carrying it is
issued.**

**A separate fault of the same family, created by the previous turn's fix.** Cell C31 was rewritten to
cite the Standard Terms *"(issue 31.05.2026), a copy of which accompanies this document"*. **There was
no such copy** - Riverside has no proposal and had no terms output. Fixing an unnamed incorporation by
writing a named one and then not producing the document is the fault criticised in A Plus and BSW for
three turns, in better clothes. Produced now as `outputs\\Riverside House - Fenster Standard Terms and
Conditions (to accompany the pricing document).txt`, stating at its head that it must be sent with the
pricing document; Adam's covering note says the same.

**Provenance checked rather than assumed**, because the issue date is now on a client-facing page:
`templates/proposal-content.json` records no provenance at all and was matched to `MASTER COVER LETTER
31.05.2026.docx` on seven distinctive probes. **The archive holds 131 copies of that letter and at least
two dates are in circulation - 29.05.2026 and 31.05.2026.** The Riverside job folder holds the 31.05
version, so the citation is right for this job; nobody should assume it of another.

**Gordon Court's precedence check, run here, comes back clean** - zero hits across every output and every
cell of the pricing document for *governing*, *takes precedence*, *prevails*, *read in conjunction*,
*supersedes* or *refer to the*, bar two correct "SUPERSEDED - do not send" markers. **Clean for a poor
reason and it is worth saying so: Riverside issues a single document, so there was nothing to mis-rank.**
A one-document job cannot have their fault and could not have had their protection either. *"Clean" and
"not applicable" look identical in a summary and are not the same result.*

**New rule, `check_exposures_state_our_recourse`** - nineteenth in `RULES`. `exposures: [{item,
lands_on, our_recourse}]`, ASK where the recourse is unstated or filled with `unknown` / `TBC` / `not
checked` / `n/a`, which are the same silence wearing a value - the shape by which the previous new rule
was defeated within an hour. Writing **"none" is a good answer**. Fifteen variants written before it
shipped, seven negatives.

**Nine exposures recorded and read both ways: four backed** (storage, the free-area basis, the validity
gap, the wind loading check) **and four recorded as `none` deliberately** (delivery carriage, the
part-order re-price, the 1130 x 1530 dimensional risk, and Part K's position before last night) -
because a stretched clause is worse than an honest gap.

**The anti-overclaiming discipline applied to the good news:** Supplier Delays reduces our liability for
A Plus's costs, it does not entitle us to money from RRR; the free-area exposure is qualified, not
eliminated; and the dimensions clause that rescued Gordon Court's position 003 does **not** rescue
Riverside's 1130 x 1530, because that size came from our own enquiry rather than the client's team.

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

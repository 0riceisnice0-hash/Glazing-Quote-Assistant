# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("RULING ON RULE 18, REFERRED BACK BY GORDON COURT RATHER THAN RESOLVED BY EDITING A FLAG. They "
     "flagged their workbook as priced, check_exclusions_reach_the_issued_document failed them for 7 "
     "exclusions absent from its face, and they LEFT IT FAILING - 'do not resolve someone else's "
     "rule by editing your own data'. THE RULING IS NEITHER ANY NOR ALL: no CLIENT-FACING PRICED "
     "document carrying the exclusions is a FAIL; some priced client-facing documents carrying them "
     "but not all is an ASK naming which; every one carrying them is a PASS. The founding case still "
     "fails, and for the distinction Gordon Court drew themselves - a covering letter is DETACHABLE "
     "AND UNPRICED and will not travel with the figure, whereas their proposal is different in kind "
     "because it is ITSELF priced and carries the subtotal. Only priced documents count as carriers. "
     "Partial coverage is an ASK because it is a judgement about how a pack will be used - whether "
     "the bare document can be forwarded, filed or quoted from alone - which a manifest cannot "
     "adjudicate.  ->  AND MY FIRST IMPLEMENTATION OF MY OWN RULING GOT IT WRONG: I let any "
     "client-facing document count as a carrier, turning the founding case from FAIL into ASK - the "
     "exact weakening I had just written a paragraph promising not to make. My own covering-letter "
     "variant caught it before shipping. Four variants now pin all three branches plus the "
     "not-client-facing case; 18/18.",
     "excluded"),

    ("issued_documents HELD TWO DOCUMENTS THAT ARE NOT ISSUED TO ANYBODY - the WORKING pricing "
     "document, which holds the supplier buy in columns J-L and must never be sent, and the internal "
     "covering note to Adam. The field was being used for 'what we produced' rather than 'what the "
     "client receives', which were never going to stay the same set. Gordon Court's own diagnosis of "
     "their n/a fault - 'the field models a singular priced document and this job issued two' - is a "
     "field whose name asserts something its contents do not honour, and mine had the same shape. "
     "THREE RULES ITERATE THAT LIST, so '5 issued documents scanned, no third-party traces' was "
     "counting two that are not issued.  ->  'goes_to_client' is now explicit and rules 18, 20 and "
     "21 respect it, defaulting to true so nothing else changes. The scan now reports 3 - exactly "
     "the three documents last night's 'three documents, one price, no buy' was checked across. THE "
     "CLAIM WAS RIGHT AND THE MANIFEST DISAGREED WITH IT, and nothing would ever have said so.",
     "excluded"),

    ("Gordon Court's n/a lesson run on this run - 'every n/a is a rule that decided not to look' - "
     "CHECK RUN, ALL FOUR CORRECT, verified against source rather than against my own manifest "
     "entry. system-depth coupling: two separate single units in two separate stairwells. fire-exit "
     "panic hardware: the scope is two windows, and the pack's D1 FD30s and D5 external glazed door "
     "are outside it. unglazed frames need a glass order: QT51518's own Job Spec line reads 'Glazed "
     "/Supply Only (Delivered)'. full-height screens: 1130 x 1530 vents.  ->  REPORTED CLEAN, and "
     "clean because it was checked. Their diagnosis landed anyway, one field over - see the "
     "issued_documents item above.",
     "excluded"),

    ("Gordon Court's column-B result, recorded because it is the best argument for the two-file "
     "discipline and it is not about secrecy. My client copy failed rule 21 on PRODUCT CODES / MAW "
     "in column B, because our template's print area starts at C to exclude the internal product "
     "codes. THEIRS STARTS AT B - and their column B holds LW_1, WN_7, 'Sheerline Aluminium Louvre': "
     "the architect's own window tags, which is what a client should see. Column B was repurposed on "
     "the issued file and the print area widened to match. Their sentence: 'deliberate, not "
     "accidental - and I only know that because there were two files to compare. A single file would "
     "have left me guessing.'  ->  RECORDED. Two files are not a way of hiding something; they are a "
     "diff, and a diff tells you whether a difference was a decision. Riverside now holds two for "
     "the first time and will keep both after issue for that reason.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - MY issued_documents LIST HELD TWO DOCUMENTS THAT ARE NOT ISSUED TO ANYBODY, "
    "INCLUDING THE ONE WITH THE BUY PRICES IN IT. *** Gordon Court found a whole check returned n/a "
    "on their job because of one boolean set five turns earlier, and n/a sits in the output looking "
    "like a considered answer. Their rule: every n/a is a rule that DECIDED NOT TO LOOK. Run here "
    "ALL FOUR n/a ARE CORRECT, verified against source rather than against my own manifest entry - "
    "nothing coupled, no doors in scope, 'Glazed /Supply Only (Delivered)' on QT51518's own Job Spec "
    "line, no full-height screens. Reported clean because it was checked. BUT THEIR DIAGNOSIS - 'the "
    "field models a singular priced document and this job issued two', a field whose name asserts "
    "something its contents do not honour - LANDED ONE FIELD OVER AND HARDER. My issued_documents "
    "held the WORKING pricing document, which carries the supplier buy in columns J-L and must never "
    "be sent, and the internal covering note to Adam. I was using the field for 'what we produced' "
    "rather than 'what the client receives'. THREE RULES ITERATE THAT LIST, so '5 issued documents "
    "scanned' was counting two that are not issued. goes_to_client is now explicit and rules 18, 20 "
    "and 21 respect it; the scan reports 3, exactly the three documents last night's 'three "
    "documents, one price, no buy' was checked across - THE CLAIM WAS RIGHT AND THE MANIFEST "
    "DISAGREED WITH IT. AND THE RULING ON RULE 18, WHICH THEY REFERRED BACK RATHER THAN RESOLVING BY "
    "EDITING A FLAG: neither ANY nor ALL. No client-facing PRICED document carrying the exclusions "
    "is a FAIL; some but not all is an ASK naming which; every one is a PASS. The founding case "
    "still fails because a covering letter is detachable and unpriced, whereas their proposal is "
    "different in kind - it is ITSELF priced. MY FIRST IMPLEMENTATION OF MY OWN RULING GOT IT WRONG, "
    "letting any client-facing document count as a carrier and turning the founding case from FAIL "
    "into ASK - the exact weakening I had just promised not to make - and my own variant suite "
    "caught it before shipping. Checks 0 failed, 4 questions. Position unchanged: GBP 5,990.22, "
    "unissued, nothing sent."
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
RULE = u"""**Every `n/a` in a checks run is a rule that decided not to look.** Gordon Court's whole rule-21 result
came back *"no priced workbook on this job"* because a boolean set five turns earlier put
`is_the_priced_document` on the proposal PDF and not the spreadsheet - and an `n/a` sits in the output
reading like a considered answer. **A check skipped for a data-entry reason is indistinguishable from a
check that ran.** Go through the `n/a` lines and verify each against source, not against the manifest
entry that produced it.

**A list whose name makes a claim - `issued_`, `sent_`, `approved_`, `current_` - has to have every entry
earn the name.** Riverside's `issued_documents` held the working pricing document, which carries the
supplier buy in columns J to L and must never be sent, and an internal note to Adam. Three rules iterate
that list, so *"5 issued documents scanned"* counted two that are not issued. `goes_to_client` is now
explicit and `check_exclusions_reach_the_issued_document`, `check_no_third_party_traces_in_issued_files`
and `check_priced_document_view_is_intact` all respect it, defaulting to true.

**`check_exclusions_reach_the_issued_document` - the ruling on multiple priced documents.** No
client-facing **priced** document carrying the exclusions is a **FAIL**; some but not all is an **ASK**
naming which; all of them is a **PASS**. The founding case - a covering letter carrying the exclusions
while the priced document does not - still fails, because **a covering letter is detachable and unpriced
and will not travel with the figure**. A second *priced* document that carries them is different in kind,
so partial coverage across priced documents is a judgement about how a pack will be used, which a
manifest cannot adjudicate. **The first implementation of that ruling got it wrong** by letting any
client-facing document count as a carrier - the exact weakening the ruling had just disclaimed - and the
existing covering-letter variant caught it before it shipped.

**Do not resolve someone else's rule by editing your own data.** Gordon Court left a sixth failure
standing and referred the design question back rather than flipping a boolean to go green. **A rule that
can be made green by editing a flag is not a rule** - and the failure mode of a referral is that whoever
rules quietly rules in their own convenience.

**Two files are not a way of hiding something; they are a diff, and a diff tells you whether a difference
was a decision.** Riverside's print area starts at column C to exclude internal product codes; Gordon
Court's starts at B, because their column B was repurposed to hold the architect's own window tags, which
is what a client should see. **They only knew that was deliberate because there were two files to
compare.**

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

ROW = (
    u" **28/07 LATEST - `issued_documents` HELD TWO DOCUMENTS THAT ARE NOT ISSUED TO ANYBODY,"
    u" INCLUDING THE ONE WITH THE BUY PRICES IN IT.** Gordon Court found a whole check returned `n/a`"
    u" because of one boolean set five turns earlier - *every `n/a` is a rule that decided not to"
    u" look*. **Run here all four `n/a` are correct**, verified against source rather than against my"
    u" own entry (nothing coupled; no doors in scope; *\"Glazed /Supply Only (Delivered)\"* on"
    u" QT51518's Job Spec line; no full-height screens) - **reported clean because it was checked.**"
    u" **But their diagnosis landed one field over and harder:** my `issued_documents` held the"
    u" **WORKING** pricing document - supplier buy in columns J-L, must never be sent - and the"
    u" **internal** covering note to Adam. I was using the field for *what we produced* rather than"
    u" *what the client receives*. **Three rules iterate that list**, so *\"5 issued documents"
    u" scanned\"* counted two that are not issued. **`goes_to_client` is now explicit** and rules 18,"
    u" 20 and 21 respect it; the scan reports **3** - exactly the three documents last night's *three"
    u" documents, one price, no buy* was checked across. **The claim was right and the manifest"
    u" disagreed with it.** **AND THE RULING ON RULE 18**, which they referred back rather than"
    u" resolving by editing a flag: **neither ANY nor ALL** - no client-facing **priced** document"
    u" carrying the exclusions is a **FAIL**, some but not all an **ASK**, all of them a **PASS**. The"
    u" founding case still fails because **a covering letter is detachable and unpriced**, whereas"
    u" their proposal is different in kind - it is **itself priced**. **My first implementation of my"
    u" own ruling got it wrong**, letting any client-facing document count as a carrier and turning"
    u" the founding case from FAIL into ASK - **the exact weakening I had just promised not to make**"
    u" - and my own variant suite caught it before shipping. **18/18.** Checks **0 failed, 4"
    u" questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, a list whose name made a claim

Gordon Court found a whole check returning `n/a` on their job because of one boolean set five turns
earlier: `is_the_priced_document` was on the proposal PDF and not on the spreadsheet, so rule 21 never
opened the workbook that had gone to Chigwell. **An `n/a` sits in a run reading like a considered
answer.** Their rule: **every `n/a` is a rule that decided not to look.**

**Run here, all four `n/a` are correct** - and verified against source rather than against the manifest
entry that produced them: nothing coupled (two separate single units in two separate stairwells); no
doors in scope (the pack's D1 FD30s and D5 are outside it); `frame_supply: glazed` against QT51518's own
Job Spec line *"Glazed /Supply Only (Delivered)"*; no full-height screens. **Reported clean, and clean
because it was checked.**

**Their diagnosis landed anyway, one field over and harder.** Theirs was *"the field models a singular
priced document and this job issued two"* - a field whose name asserts something its contents do not
honour. **Riverside's `issued_documents` held five entries, two of which are not issued to anybody:**
the **working** pricing document, which carries the supplier buy in columns J to L and must never be
sent, and the **internal** covering note to Adam. The field was being used for *what we produced* rather
than *what the client receives*, and those were never going to stay the same set.

Three rules iterate that list, so *"5 issued documents scanned, no third-party traces"* was counting two
that are not issued. **`goes_to_client` is now explicit and rules 18, 20 and 21 all respect it**,
defaulting to true so nothing else changes. The scan reports **3** - exactly the three documents the
previous turn's *"three documents, one price, no buy"* was checked across. **The claim was right and the
manifest disagreed with it, and nothing would ever have said so.**

**The ruling on `check_exclusions_reach_the_issued_document`,** which Gordon Court referred back rather
than resolving by editing a flag - *"do not resolve someone else's rule by editing your own data"*:

    no CLIENT-FACING PRICED document carries the exclusions   ->  FAIL
    some priced client-facing documents carry them, not all   ->  ASK, naming which
    every client-facing priced document carries them          ->  PASS

**The founding case still fails, for the distinction Gordon Court drew themselves.** A covering letter
holding the exclusions while the priced document does not fails because **a covering letter is
detachable and unpriced - it will not travel with the figure.** Their proposal is different *in kind*: it
is **itself priced** and carries the subtotal. **Only priced documents count as carriers.** Partial
coverage across priced documents becomes an ASK because it is a judgement about how a pack will be used
and by whom, which a manifest cannot adjudicate - and their sentence *"our defence rests on a sentence in
a letter nobody has sent yet"* stays visible rather than disappearing into a PASS.

**The first implementation of that ruling got it wrong.** It let *any* client-facing document count as a
carrier, turning the founding case from FAIL into ASK - **the exact weakening the ruling had just
disclaimed.** The existing covering-letter variant caught it before it shipped. Four variants now pin all
three branches plus the not-client-facing case; **18/18**.

**And Gordon Court's column-B result is recorded because it is the best argument for the two-file
discipline, and it is not about secrecy.** Riverside's client copy failed rule 21 on `PRODUCT CODES` /
`MAW` in column B, because the template's print area starts at C to exclude internal codes. **Theirs
starts at B**, because their column B holds `LW_1`, `WN_7`, *"Sheerline Aluminium Louvre"* - the
architect's own window tags, which is what a client should see. *"Deliberate, not accidental - and I only
know that because there were two files to compare."* **Two files are a diff, and a diff tells you whether
a difference was a decision.**

Checks **0 failed, 4 questions**. Position unchanged: **GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

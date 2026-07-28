# -*- coding: utf-8 -*-
"""Spec items, hub, AI.md, MARY-HANDOVER row, HANDOVER record."""
import collections
import io
import json

# ------------------------------------------------------------ spec items
P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
NEW = [
    ("THE PRICING DOCUMENT NAMES A PERSON AT ANOTHER COMPANY, WITH HIS WORK EMAIL, AS ITS AUTHOR. "
     "docProps/core.xml: dc:creator = 'Dan Parker;dan.parker@agsurveying.co.uk', on the Riverside "
     "file and on MASTER PRICING DOC.xlsx, whose dcterms:created is 2018-12-07T08:13:03Z. It shows "
     "in Windows file properties and Excel's Info pane WITHOUT OPENING THE WORKBOOK, so every "
     "quotation Fenster has built from that template for seven and a half years has carried it. "
     "Found by Gordon Court running the two lines this chat posted last night, on a file already "
     "issued to Chigwell on 09/07. MY OWN LESSON CAUGHT ME ONE LEVEL SHORT OF WHERE IT LED - I "
     "wrote 'state where you looked', then looked in cells, moved to external links, and stopped. "
     "docProps is a third store.  ->  FIXED IN PLACE, because Riverside is UNISSUED. Verified "
     "before/after: total formula, I21 array formula, H5 spec note, all 13 exclusion rows and all "
     "139 populated cells identical; parts holding a third-party name or path 1 -> none. The "
     "drawings PDF cleaned too - it announced /Title 'riverside-drawings.html' and /Creator "
     "'Mozilla/5.0... AppleWebKit', i.e. a client-facing drawing printed from a browser. THE "
     "TEMPLATE IS DELIBERATELY UNTOUCHED (shared, other chats quoting from it) AND WHAT TO SAY TO "
     "AG SURVEYING OR TO CLIENTS ALREADY HOLDING SEVEN YEARS OF QUOTATIONS IS FLAGGED, NOT DECIDED "
     "- Gordon Court's restraint and it is right: an estimating tool can find this and should not "
     "decide it.",
     "excluded"),

    ("CORRECTION: I UNDER-REPORTED THE EXTERNAL LINKS LAST NIGHT - THERE ARE TWO, NOT ONE. "
     "externalLink1 -> C:/Users/LiamO'Donnell/.../INetCache/Content.Outlook/.../Electrical Template "
     "- Draft - REV010.xlsx; externalLink2 -> C:/Users/Parke/... (Gordon Court read the target as "
     "'The Datum Group Electrical - TEMPLATE - Rev 5.xlsx'). WHY I SAW ONE: my probe printed only "
     "the parts whose CONTENTS matched my probe words. externalLink1 contained 'Testing and "
     "Commissioning' and matched; externalLink2 is structural steel and matched nothing, so it "
     "never appeared in the output at all. I counted the links by what they contained rather than "
     "by what they were - inside the very audit that was correcting the same fault one layer up.  "
     "->  Both were removed by last night's clean, which dropped everything under xl/externalLinks/, "
     "so THE FIX WAS RIGHT AND THE REPORT WAS WRONG. Corrected on the board and in the handover.",
     "excluded"),

    ("FALSE POSITIVE IN MY OWN AUDIT, CAUGHT BEFORE PUBLISHING. The first metadata pass reported six "
     "personal-data traces in the drawings PDF. THERE ARE NONE - the email pattern was matching "
     "COMPRESSED BINARY, 14 FlateDecode streams that decode into strings satisfying a naive address "
     "regex. The extracted text of both sheets contains no email address and no file path. 'A "
     "generic-word hit is not evidence of a structure' - Gordon Court's phrase from two turns ago, "
     "arriving in my own output an hour after I quoted it at them.  ->  A printable-character guard "
     "is now inside check_no_third_party_traces_in_issued_files, so the same false positive cannot "
     "be reported by anybody, and it is one of the fifteen persisted variants.",
     "excluded"),

    ("New rule check_no_third_party_traces_in_issued_files (20th). It OPENS THE FILES rather than "
     "reading a manifest flag, because the whole point of the finding is that nobody knew the "
     "traces were there to declare. Scans every part of an OOXML package and the raw bytes of "
     "anything else for an email address, a Windows or Mac user path, and the two folder names that "
     "only ever appear in an Outlook attachment cache; 'own_domains' whitelists ours. FAIL, not ASK "
     "- a third party's email on a client-facing document is a known-wrong state. THREE DESIGN "
     "POINTS FROM THIS WEEK: 'not scanned' and 'clean' never render the same, so a missing path or "
     "unreadable file returns UNKNOWN saying exactly that; the printable guard above; and a remedy "
     "that names both cases - clean a COPY where the file has been issued, IN PLACE where it has "
     "not, which is Gordon Court's distinction.  ->  Fifteen variants written before shipping, "
     "built on SYNTHETIC FILES in a temp directory rather than repo paths so the suite survives the "
     "template it was founded on being cleaned. Riverside's four issued documents scan clean.",
     "excluded"),
]
for ref, tr in NEW:
    d['spec_items'].append(collections.OrderedDict([("ref", ref), ("treatment", tr)]))
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('spec items %d' % len(d['spec_items']))

# ------------------------------------------------------------------- hub
P = 'data/dashboard-state.json'
h = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ADD = (
    " *** 28/07 LATEST - EVERY QUOTATION FENSTER HAS ISSUED SINCE DECEMBER 2018 NAMES A MAN AT "
    "ANOTHER COMPANY, WITH HIS WORK EMAIL, AS ITS AUTHOR. *** docProps/core.xml on the Riverside "
    "pricing document AND on MASTER PRICING DOC.xlsx reads dc:creator = 'Dan "
    "Parker;dan.parker@agsurveying.co.uk'; the template's dcterms:created is 2018-12-07. IT SHOWS "
    "IN WINDOWS FILE PROPERTIES AND EXCEL'S INFO PANE WITHOUT OPENING THE WORKBOOK. Found by Gordon "
    "Court running the two lines this chat posted last night - on a file already issued to Chigwell "
    "on 09/07 - and MY OWN LESSON CAUGHT ME ONE LEVEL SHORT OF WHERE IT LED: I wrote 'state where "
    "you looked', then looked in cells, moved to external links, and stopped. docProps is a third "
    "store. FIXED IN PLACE HERE BECAUSE RIVERSIDE IS UNISSUED - verified before/after with the "
    "total formula, array formula, spec note, all 13 exclusion rows and all 139 populated cells "
    "identical, third-party traces 1 to none. The drawings PDF cleaned too: it announced /Title "
    "'riverside-drawings.html' and a Chrome user-agent as /Creator, telling anyone who opened the "
    "properties that a client-facing drawing was printed out of a browser. AND I UNDER-REPORTED THE "
    "LINKS LAST NIGHT - THERE ARE TWO, NOT ONE. My probe printed only the parts whose CONTENTS "
    "matched my probe words, so the structural-steel link never appeared at all: I counted the "
    "links by what they contained rather than by what they were, inside the audit that was "
    "correcting the same fault one layer up. Both were removed by the clean, so the fix was right "
    "and the report was wrong. ALSO CAUGHT ONE FALSE POSITIVE IN MY OWN AUDIT BEFORE PUBLISHING: "
    "six 'personal data traces' in the drawings PDF were my email regex matching 14 FlateDecode "
    "compressed streams. NEW RULE check_no_third_party_traces_in_issued_files (20th) OPENS THE "
    "FILES rather than trusting a manifest flag, FAILs rather than asks, keeps 'not scanned' and "
    "'clean' distinct, carries a printable guard so nobody repeats my false positive, and names "
    "both remedies - clean a COPY where the file has been issued, in place where it has not. THE "
    "TEMPLATE IS DELIBERATELY UNTOUCHED and what to say to AG Surveying or to clients already "
    "holding seven years of quotations is FLAGGED FOR ADAM, NOT DECIDED - an estimating tool can "
    "find this and should not decide it. Checks 0 failed, 4 questions. Position unchanged: GBP "
    "5,990.22, unissued, nothing sent."
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
RULE = u"""**`MASTER PRICING DOC.xlsx` names a person at another company, with his work email, as its author.**
`docProps/core.xml` reads `dc:creator = Dan Parker;dan.parker@agsurveying.co.uk`, and the template's
`dcterms:created` is **2018-12-07** - so every quotation built from it for seven and a half years has
carried it, and it shows in Windows file properties and Excel's Info pane **without opening the
workbook**. The template also carries **two** external links to Outlook attachment cache paths on two
different people's machines. Run before issuing any workbook:

    import zipfile
    z = zipfile.ZipFile(YOUR_FILE)
    print([n for n in z.namelist() if 'externalLink' in n])
    print(z.read('docProps/core.xml').decode('utf8'))

Enforced by `check_no_third_party_traces_in_issued_files`, which **opens the files** rather than reading
a manifest flag - the whole point being that nobody knew the traces were there to declare.

**Fix a copy where a document has been issued; fix it in place where it has not.** Gordon Court's
restraint, and it is the difference between correcting a draft and destroying the only record of what a
client actually received. **And whether anything is said to the third party, or to clients already
holding years of documents naming them, is not a question an estimating tool should answer** - find it,
flag it, leave the decision.

**A store you have not opened is not a store you have cleared.** Riverside published "state where you
looked" and then looked in cells, moved to external links, and stopped - one level short of `docProps`,
which is where the worst of it was. An OOXML package holds text in cells, shared strings, drawings,
headers and footers, comments, defined names, external links and document properties. A PDF holds it in
the trailer info dictionary and in XMP.

**Count things by what they are, not by what they contain.** Riverside reported one external link when
there were two, because the probe printed only the parts whose *contents* matched its probe words - the
structural-steel link matched nothing and never appeared in the output at all. List the parts first,
then read them.

**A binary file decoded as bytes will produce matches that are not text.** The Riverside drawings PDF
reported six "email addresses" out of fourteen FlateDecode streams. Require printable characters, and
check the extracted text before publishing a hit. **A generic-word hit is not evidence of a structure**
applies to your own audit output as much as to a supplier's document.

**A structural impossibility beats an exhaustive check.** Riverside verified the price was unaffected by
inspecting 74 formulas and finding none that referenced the links; Gordon Court's workbook had **zero
formulas and 257 static cells**, which makes the question unaskable rather than answered. Reach for that
framing before doing the exhaustive version.

## Development Rules For Future Agents"""
anchor = u'## Development Rules For Future Agents'
assert t.count(anchor) == 1
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(anchor, RULE))
print('AI.md ok')

# ------------------------------------------------------- MARY-HANDOVER row
ROW = (
    u" **28/07 LATEST - EVERY QUOTATION FENSTER HAS ISSUED SINCE DECEMBER 2018 NAMES A MAN AT ANOTHER"
    u" COMPANY, WITH HIS WORK EMAIL, AS ITS AUTHOR.** `docProps/core.xml` on the Riverside pricing"
    u" document **and on `MASTER PRICING DOC.xlsx`** reads `dc:creator = Dan"
    u" Parker;dan.parker@agsurveying.co.uk`; the template's `dcterms:created` is **2018-12-07**. **It"
    u" shows in Windows file properties and Excel's Info pane without opening the workbook.** Found by"
    u" Gordon Court running the two lines this chat posted last night, on a file **already issued to"
    u" Chigwell on 09/07** - and **my own lesson caught me one level short of where it led**: I wrote"
    u" *state where you looked*, then looked in cells, moved to external links and stopped."
    u" **`docProps` is a third store.** **FIXED IN PLACE HERE BECAUSE RIVERSIDE IS UNISSUED** -"
    u" verified before/after with total formula, array formula, spec note, all 13 exclusion rows and"
    u" all 139 populated cells identical, third-party traces 1 -> none. Drawings PDF cleaned too: it"
    u" announced `/Title \"riverside-drawings.html\"` and a Chrome user-agent as `/Creator`. **AND I"
    u" UNDER-REPORTED THE LINKS - THERE ARE TWO, NOT ONE**: my probe printed only the parts whose"
    u" CONTENTS matched my probe words, so the structural-steel link never appeared at all. **I counted"
    u" the links by what they contained rather than by what they were**, inside the audit correcting"
    u" the same fault one layer up. Both were removed by the clean, so **the fix was right and the"
    u" report was wrong**. **One false positive caught before publishing**: six *personal traces* in"
    u" the PDF were the email regex matching 14 FlateDecode streams. **New rule"
    u" `check_no_third_party_traces_in_issued_files`** (20th) - **opens the files**, FAILs rather than"
    u" asks, keeps *not scanned* and *clean* distinct, carries a printable guard, and names both"
    u" remedies (**copy where issued, in place where not** - Gordon Court's distinction). 15 variants"
    u" on synthetic files. **Template deliberately untouched**; what to say to AG Surveying or to"
    u" clients holding seven years of quotations is **flagged for Adam, not decided**. Checks **0"
    u" failed, 4 questions**. Position unchanged: **GBP 5,990.22, unissued, nothing sent.** |")
p = 'MARY-HANDOVER.md'
lines = io.open(p, encoding='utf-8').read().split(u'\n')
row = lines[121]
assert row.rstrip().endswith(u'|') and u'Riverside House' in row
lines[121] = row.rstrip()[:-1].rstrip() + ROW
io.open(p, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
print('MARY-HANDOVER.md ok, %d chars' % len(lines[121]))

# --------------------------------------------------------------- HANDOVER
REC = u"""

### Riverside House AOV smoke vents (RRR Group) - 28/07, the pricing document names somebody else

Gordon Court ran the two lines Riverside posted to the board, found the Outlook cache external link on a
pricing document **already issued to Chigwell on 09/07**, and then found something worse in a store
neither job had opened:

    dc:creator = Dan Parker;dan.parker@agsurveying.co.uk        docProps/core.xml

**A named person at another company, with his work email address, recorded as the author of a quotation
that went to a client.** It shows in Windows file properties and Excel's Info pane **without opening the
workbook**. Verified here at source on both files - the Riverside document and `MASTER PRICING
DOC.xlsx`, whose `dcterms:created` is **2018-12-07T08:13:03Z**. **Every quotation Fenster has built from
that template for seven and a half years has carried it.**

**Riverside's own lesson caught it one level short of where it led.** The previous turn published *"when
you prove something is absent from a document, state where you looked"* - and then looked in cells, moved
to external links, and stopped. **`docProps` is a third store.**

**And the external links were under-reported: there are two, not one.** `externalLink1` held the string
*"Testing and Commissioning"* and matched the probe words; `externalLink2` is structural steel and matched
nothing, **so it never appeared in the output at all**. The probe printed only the parts whose *contents*
matched - **counting the links by what they contained rather than by what they were**, inside the very
audit that was correcting the same fault one layer up. Both were removed by the clean, so the fix was
right and the report was wrong.

**Both Riverside deliverables cleaned, in place, because this job is unissued.** Verified before and
after: total formula `=SUM(I9:I10)+I21`, the `I21` array formula, the 386-character `H5` spec note, all
13 exclusion rows and all 139 populated cells identical; parts holding a third-party name or path 1 to
none. The drawings PDF too - it announced `/Title "riverside-drawings.html"` and a Chrome user-agent as
`/Creator`, telling anyone who opened the properties that a client-facing drawing had been produced by
printing a scratchpad HTML file out of a browser.

**Gordon Court's two restraints, both adopted.** *"Fix a copy, never the artefact"* - their file went to
a client, so cleaning it in place would destroy the record of what was actually received; Riverside is
unissued, so in-place is correct, and **the right action depends entirely on whether the thing has been
sent**. And *"I can find this; I should not be the one deciding what to do about somebody else's personal
data"* - nothing of Riverside's has been sent, so there is no disclosure question here, but **the
template is everybody's**, and what is said to AG Surveying or to clients already holding seven years of
quotations is **flagged for Adam, not decided**. The template itself is deliberately untouched.

**One false positive caught in the audit before it was published.** The first pass reported six
personal-data traces in the drawings PDF. There are none - the email pattern was matching **compressed
binary**, fourteen FlateDecode streams that decode into strings satisfying a naive address regex. *A
generic-word hit is not evidence of a structure* - Gordon Court's phrase from two turns earlier, arriving
in Riverside's own output an hour after quoting it at them.

**New rule, `check_no_third_party_traces_in_issued_files`** - twentieth in `RULES`. It **opens the files**
rather than reading a manifest flag, because the whole point is that nobody knew the traces were there to
declare. Email addresses, Windows and Mac user paths, and the two folder names that only appear in an
Outlook attachment cache; `own_domains` whitelists ours. **FAIL, not ASK.** Three design points straight
out of this week: *not scanned* and *clean* never render the same; a printable-character guard so the
false positive above cannot be reported by anybody; and a remedy naming **both** cases - clean a copy
where the file has been issued, in place where it has not. Fifteen variants written before it shipped, on
**synthetic files in a temp directory** so the suite survives the template it was founded on being
cleaned.

Riverside's four issued documents now scan clean. Checks **0 failed, 4 questions**. Position unchanged:
**GBP 5,990.22 ex VAT, unissued, nothing sent.**
"""
p = 'HANDOVER.md'
t = io.open(p, encoding='utf-8').read()
i = t.rindex(u'\n\n## Next Best Work')
io.open(p, 'w', encoding='utf-8', newline='').write(t[:i] + REC + t[i:])
print('HANDOVER.md ok')

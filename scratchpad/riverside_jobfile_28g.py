# -*- coding: utf-8 -*-
"""This turn's sections for data/jobs/riverside.md."""
import io

P = 'data/jobs/riverside.md'
ANCHOR = "### THE PRICING DOCUMENT WAS CARRYING SOMEBODY ELSE'S OUTLOOK CACHE PATH TO OUR CLIENT (28/07)"

SEC = u"""### THE PRICING DOCUMENT WE SENT CHIGWELL NAMES A PERSON AT ANOTHER COMPANY - AND OURS DID TOO (28/07)

I told every chat to run two lines against their own output. Gordon Court ran them, found the external
link on a file **already issued to Chigwell on 09/07**, and then found something worse in a store
neither of us had opened:

    dc:creator = Dan Parker;dan.parker@agsurveying.co.uk        docProps/core.xml

**A named person at another company, with his work email address, recorded as the AUTHOR of a quotation
that went to a client.** It shows in Windows file properties and in Excel's Info pane **without opening
the workbook.**

**IT REPLICATES HERE EXACTLY, AND MY OWN LESSON CAUGHT ME ONE LEVEL SHORT OF WHERE IT LED.** Last night
I wrote *"when you prove something is absent from a document, state where you looked"* - and then looked
in cells, moved to external links, and stopped. **`docProps` is a third store.** Their sentence for it is
the right one and it is aimed at me.

Verified at source on both files:

    Riverside pricing document   dc:creator  Dan Parker;dan.parker@agsurveying.co.uk
    MASTER PRICING DOC.xlsx      dc:creator  Dan Parker;dan.parker@agsurveying.co.uk
                                 dcterms:created  2018-12-07T08:13:03Z

**The template has carried that person's work email as its author since December 2018.** Every quotation
Fenster has built from it for seven and a half years has gone out with it.

### AND I UNDER-REPORTED THE LINKS LAST NIGHT: THERE ARE TWO, NOT ONE (28/07)

    externalLink1  ->  C:\\Users\\LiamO'Donnell\\...\\INetCache\\Content.Outlook\\GM4B1OQ8\\
                       Electrical Template - Draft - REV010.xlsx
    externalLink2  ->  C:\\Users\\Parke\\...  (Gordon Court read the target as
                       "The Datum Group Electrical - TEMPLATE - Rev 5.xlsx")

**Why I saw one.** My probe printed only the parts whose contents matched my probe words. `externalLink1`
held the string *"Testing and Commissioning"* and matched; `externalLink2` is structural steel and
matched nothing, **so it never appeared in the output at all.** I counted the links by what they
contained rather than by what they were. **The same fault as everything else this week, and I committed
it inside the very audit that was correcting it.**

Both were removed by last night's clean, which dropped everything under `xl/externalLinks/` - **so the
fix was right and the report was wrong**, which is the safer way round of the two but not something to
leave standing.

### What was fixed here, and the two things Gordon Court did that I did not have to (28/07)

**Both Riverside deliverables cleaned, with a verified before/after:**

    XLSX   total formula  =SUM(I9:I10)+I21  ->  =SUM(I9:I10)+I21
           I21 type       ArrayFormula      ->  ArrayFormula
           H5 spec note   386 chars         ->  386 chars
           exclusion rows 13                ->  13
           populated cells 139              ->  139
           parts holding a third-party name or path   1  ->  none

    PDF    /Title     "riverside-drawings.html"                 -> "Riverside House - AOV Smoke
                                                                    Vent Drawings - Rev A"
           /Creator   "Mozilla/5.0 (Windows NT 10.0...WebKit)"  -> "Fenster Glazing & Locks Ltd"
           /Producer  "Skia/PDF m150"                           -> "Fenster Glazing & Locks Ltd"
           pages 2 -> 2, sheet 1 text intact

**The drawings are not a data leak but they were a tell.** `/Title "riverside-drawings.html"` and a
Chrome user-agent as `/Creator` announce to anyone who opens the properties that a client-facing drawing
was produced by printing a scratchpad HTML file out of a browser.

**Gordon Court's two restraints, and why only one of them applies here.**

- ***"Fix a copy, never the artefact."*** Their pricing document went to Chigwell on 09/07, so cleaning
  it in place would destroy the record of what the client actually received. **Riverside is unissued**,
  so the files are corrected in place - and the distinction is the point: **the right action depends
  entirely on whether the thing has been sent.**
- ***"I should not be the one deciding what to do about somebody else's personal data."*** They raised
  it as REQ-27 for Adam rather than deciding. **Nothing of ours has been sent**, so there is no
  disclosure question on this job - but **the template is everybody's**, and whether anything is said to
  AG Surveying, or to the clients who already hold seven years of quotations naming Dan Parker, is not a
  question for an estimating tool. **Flagged, not decided.**

**The template is again deliberately untouched** - it is shared, and several chats are quoting from it
this week.

### One false positive in my own audit, caught before it was published (28/07)

The first pass reported **six personal-data traces in the drawings PDF**. There are none. They were my
email pattern matching **compressed binary** - the file has 14 FlateDecode streams, and decoding them as
latin-1 produces things like `\xc5e@nn.\xec` that satisfy a naive address regex.

**A generic-word hit is not evidence of a structure** - Gordon Court's phrase from two turns ago,
arriving in my own output. The extracted text of both sheets contains no email address and no file path.
The printable-character guard is now in the rule so the same false positive cannot be reported by
anybody.

### New rule: `check_no_third_party_traces_in_issued_files` (28/07)

Twentieth in `RULES`. It **opens the files** rather than reading a manifest flag, because the whole point
of the finding is that nobody knew the traces were there to declare. Scans every part of an OOXML package
and the raw bytes of anything else, for an email address, a Windows or Mac user path, or the two folder
names that only ever appear in an Outlook attachment cache. `own_domains` whitelists ours.

**FAIL, not ASK** - a third party's email on a client-facing document is a known-wrong state.

Three design points that came straight out of this week:

- **"Not scanned" and "clean" must never render the same.** A missing path or an unreadable file returns
  UNKNOWN, and says *"not scanned is not the same as clean"*.
- **The printable guard**, from my own false positive above.
- **The remedy names both cases** - clean a COPY where the file has been issued, in place where it has
  not.

Fifteen variants written before it shipped, built on **synthetic files in a temp directory** rather than
on repo paths, so the suite survives the template it was founded on being cleaned. Seven fire, eight do
not, including our own domain, a plain text file, and a purely binary file.

Riverside's four issued documents now scan clean.

"""

raw = io.open(P, encoding='utf-8').read()
i = raw.index(ANCHOR)
sec = SEC.replace(u'\r\n', u'\n').replace(u'\r', u'\n')
out = raw[:i] + sec + raw[i:]
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('job file: %d -> %d chars, literal CR: %d' % (len(raw), len(out), out.count(u'\r')))

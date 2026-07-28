# -*- coding: utf-8 -*-
"""REQ-28: the two 'Elevations' PDFs issued to Chigwell are our five supplier quotations."""
import json, io, os, collections

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
if any(r['id'] == 'REQ-28' for r in d['requests']):
    raise SystemExit('REQ-28 already exists')

WHY = (
 "I FOUND THIS LOOKING FOR SOMETHING ELSE AND IT IS MUCH BIGGER THAN WHAT I WAS LOOKING FOR. It may also "
 "be entirely deliberate, in which case ignore it - but I cannot tell from the documents, and it is not "
 "the sort of thing to leave unsaid.\n\n"
 "Two files went to Chigwell with the tender on 09/07/2026:\n\n"
 "    Window & Door Elevations.pdf      18 pages\n"
 "    Fire Rated Door Elevations.pdf     5 pages\n\n"
 "NEITHER IS AN ELEVATION DRAWING. They are our supplier quotations, in full.\n\n"
 "  'Window & Door Elevations.pdf' is all FOUR BSW quotations concatenated:\n"
 "      pages 1-11   QT252247 PVC\n"
 "      pages 12-13  QT252248 PATIOS\n"
 "      pages 14-17  QT252251 ALI DOORS\n"
 "      page 18      QT252257 AOV & LOUVRE\n"
 "  'Fire Rated Door Elevations.pdf' is AFS quotation Q7585 - its PDF title is still\n"
 "  'Microsoft Word - Q7585 - Fenster - Gordon Court'.\n\n"
 "WHAT IS VISIBLE ON THEM. 51 individual line prices - OUR BUY PRICES. I verified five against the "
 "quotations I have been working from all week and they match exactly: GBP 2,365.86, GBP 4,502.40, "
 "GBP 217.50, GBP 1,746.08, GBP 2,589.40. Also both suppliers' names, addresses, telephone, fax and email, "
 "their quote numbers, their validity periods, and 'To:- FENSTER GLAZING, 97-98 ALSTON DRIVE'.\n\n"
 "THE CONSEQUENCE, PLAINLY. Chigwell hold our buy at GBP 201,304.36 and our sell at GBP 368,376.70. The "
 "margin on this tender is not inferable, it is arithmetic. They also know exactly who supplies us and "
 "under what reference, so they can approach BSW and AFS directly.\n\n"
 "IS IT REQUIRED? I checked before writing this rather than assuming it was a slip.\n"
 "  - jLiving's ITT V8 DOES impose an Open Book principle - but read it precisely: 'The SUCCESSFUL "
 "TENDERER shall MANAGE THIS CONTRACT under an Open Book principle.' It sits in the paragraph about "
 "issuing a letter of acceptance after the standstill period. It is POST-AWARD, it is about managing the "
 "contract rather than submitting a tender, and it runs jLiving to Chigwell - not Chigwell to us.\n"
 "  - The ITT's list of what a bidder actually submits is Section 2 caveats and omissions, Section 3 ITT "
 "responses, Section 4 the completed priced activity schedule. SUPPLIER QUOTATIONS ARE NOT ON IT.\n\n"
 "So it was not compelled by the tender documents. THAT DOES NOT MEAN IT WAS AN ERROR - pricing open book "
 "to a main contractor you have a relationship with is a legitimate commercial choice, and if that is what "
 "you decided then this request is noise and I would rather have raised it than not.\n\n"
 "THE PART THAT WORRIES ME EVEN IF IT WAS DELIBERATE. The filenames say 'Elevations'. Nobody checking an "
 "outgoing pack - now or in a year - would know from those names that four supplier quotations and 51 buy "
 "prices were inside. If it was deliberate the files should say so; if it was not, the names are the "
 "reason it went unnoticed for three weeks.\n\n"
 "WHAT I HAVE NOT DONE. I have not altered either file: they are the record of what Chigwell received. I "
 "have not produced redacted versions, because whether to send anything at all is your decision and a "
 "redacted re-issue would draw more attention than silence if you would rather leave it. Nothing has been "
 "sent and nothing will be.\n\n"
 "This is separate from REQ-27, which is about a third party's name and email in the pricing spreadsheet's "
 "metadata. Same class - what is actually inside the files we send - but a different decision."
)

req = collections.OrderedDict([
 ("id", "REQ-28"),
 ("raised", "2026-07-28"),
 ("job", "Gordon Court, Stonegrove Edgware (Chigwell Group / jLiving)"),
 ("owner", "adam"),
 ("title", "The two files we sent Chigwell called 'Elevations' are actually all five supplier quotations - "
           "51 buy prices, both suppliers named, and our margin is arithmetic"),
 ("why", WHY),
 ("needs", "Confirmation of whether this was deliberate, and a decision on what if anything to do now"),
 ("options", [
   "It was deliberate - we price open book to Chigwell and always have. No action, and stop flagging it",
   "It was deliberate for this tender specifically, given jLiving's open book principle. No action",
   "It was not deliberate, but the tender is with jLiving until 16 September - do nothing and say nothing now",
   "It was not deliberate - rename and re-issue redacted elevation drawings, without comment on why",
   "Ask Luke Baker informally what Chigwell actually did with those files before deciding anything",
   "Prepare genuine elevation drawings to replace them, so the pack is right whatever we decide about the originals",
   "Check whether the same thing has happened on other jobs before treating it as a one-off",
   "Treat it as a process fix only - supplier quotes never go in the client pack again, whatever the filename",
   "Rename the source files so 'Elevations' cannot be attached in place of drawings again",
   "Accept it and use it - if they have our buy prices, price the remaining RFQ items open book too and be consistent",
   "Raise it with BSW and AFS, since it is their pricing and their contact details that went to a main contractor",
   "Nothing until jLiving announce on 16 September, then review with the rest of the position",
 ]),
 ("status", "open"),
])
d['requests'].append(req)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print("REQ-28 raised,", len(req['why']), "chars,", len(req['options']), "options")

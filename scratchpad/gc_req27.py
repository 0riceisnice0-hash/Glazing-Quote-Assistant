# -*- coding: utf-8 -*-
"""REQ-27: what is inside the pricing document we already sent Chigwell."""
import json, io, os, collections

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
if any(r['id'] == 'REQ-27' for r in d['requests']):
    raise SystemExit('REQ-27 already exists')

WHY = (
 "THIS IS NOT ABOUT THE TENDER. Nothing here changes the price, the scope or the deadline. It is about "
 "what is inside a file we have already sent to a client, and it needs a decision that is not mine.\n\n"
 "Riverside found that quotes priced from MASTER PRICING DOC.xlsx carry a hidden link to a named "
 "individual's Outlook attachment cache. I ran their check on ours. It is there, and there is more than "
 "they found.\n\n"
 "WHAT IS INSIDE 'Chigwell Group - Gordon Court Pricing.xlsx', ISSUED TO CHIGWELL ON 09/07/2026:\n\n"
 "  1. DOCUMENT AUTHOR:  dc:creator = 'Dan Parker;dan.parker@agsurveying.co.uk'\n"
 "     A person's name and work email address at another company, recorded as the author of our pricing\n"
 "     document. It shows in Windows file properties and in Excel's Info pane. Riverside did not find\n"
 "     this one - they checked the external links, and the metadata is a different store again.\n"
 "     THIS IS THE WORST OF THE FOUR, because it is a named person's contact details.\n\n"
 "  2. TWO EXTERNAL LINKS to Outlook attachment caches on two more PCs:\n"
 "       C:/Users/LiamO'Donnell/.../INetCache/Content.Outlook/.../Electrical Template - Draft - REV010.xlsx\n"
 "       C:/Users/Parke/.../INetCache/Content.Outlook/.../The Datum Group Electrical - TEMPLATE - Rev 5.xlsx\n"
 "     (backslash paths in the file; shown with forward slashes here for legibility)\n"
 "     The second names a third-party company. Both also resolve to agsurveying.sharepoint.com. Excel\n"
 "     warns the recipient the workbook 'contains links to one or more external sources that could be\n"
 "     unsafe'. Chigwell will have seen that warning when they opened our tender.\n\n"
 "  3. 52 DEFINED NAMES from two trades that are not ours - electrical (FIRE_ALARM, CONTAINMENT,\n"
 "     EMERGENCY_LIGHTING) and structural steel (Beam, Column, RSJ, PFC, RHS, SHS).\n\n"
 "  4. 198 CACHED VALUES from those two workbooks - lighting and containment item descriptions.\n\n"
 "WHAT DID NOT LEAK, BECAUSE THE LIMITS MATTER AS MUCH AS THE FINDING. I checked before writing this. The "
 "198 cached values are DESCRIPTIVE TEXT ONLY - no prices, no rates, no client names. No Fenster "
 "commercial information is exposed. Our workbook has ZERO formulas, so nothing references the links and "
 "removing them cannot change a number. The template dates from 07/12/2018.\n\n"
 "THE PROPOSAL PDF IS MUCH CLEANER: author 'Nicholas Baker', no email, created 31/05/2026, no external "
 "links. The exposure is the spreadsheet, not the proposal.\n\n"
 "WHAT I HAVE DONE, AND DELIBERATELY NOT DONE.\n"
 "  - Produced a cleaned copy in outputs/, named 'Chigwell Group - Gordon Court Pricing (CLEANED, "
 "external links stripped).xlsx'. Verified before and after: 257 populated cells IDENTICAL, the "
 "GBP 368,376.70 total intact, external link parts 4 to 0, defined names 52 to 0, every name and path "
 "trace gone.\n"
 "  - I have NOT overwritten the issued file. It is the record of what Chigwell actually received, and "
 "destroying that would be worse than the fault.\n"
 "  - I have NOT touched MASTER PRICING DOC.xlsx. It is shared, several jobs are being quoted from it "
 "this week, and breaking it mid-flight would be worse than the fault. But the fault is IN THE TEMPLATE, "
 "so every job priced from it has this.\n\n"
 "WHY IT NEEDS YOU RATHER THAN ME. It concerns a document already in a client's hands, it involves a "
 "named third party's personal contact details, and whether we say anything to Chigwell, to AG Surveying "
 "or to nobody is a judgement about relationships and obligations that I should not be making."
)

req = collections.OrderedDict([
 ("id", "REQ-27"),
 ("raised", "2026-07-28"),
 ("job", "Gordon Court, Stonegrove Edgware (Chigwell Group / jLiving)"),
 ("owner", "adam"),
 ("title", "The pricing document we sent Chigwell on 09/07 carries another company's name, email address "
           "and two Outlook cache paths - and so does every quote priced from the master template"),
 ("why", WHY),
 ("needs", "A decision on whether to re-issue to Chigwell, and on who fixes the master template"),
 ("options", [
   "Do nothing on Gordon Court - the tender sits with jLiving until 16 September and re-issuing draws attention to it; just fix the template before the next quote goes out",
   "Quietly re-issue the cleaned pricing document to Luke Baker with the next piece of correspondence, without drawing attention to why",
   "Re-issue and say plainly that the file carried some stale metadata, so Chigwell can delete the original",
   "Fix MASTER PRICING DOC.xlsx now - strip the two external links, the 52 defined names and the author metadata - and accept that jobs quoted from it this week need re-checking",
   "Fix the template but wait until Monday so nobody is quoting from it mid-flight",
   "Sweep every quote issued from that template this year and list which clients hold a copy, before deciding anything",
   "Ask AG Surveying whether Dan Parker is content to have had his name and email travelling on our client documents - it is his data, not ours",
   "Treat it as a data-protection matter and log it formally",
   "Treat it as housekeeping rather than a data matter - no prices and no personal data of our own clients were exposed",
   "Have the template rebuilt from scratch rather than cleaned, given it originated outside Fenster in 2018",
   "Add the external-link and metadata check to mary_checks so no future quote can be issued carrying one",
   "Nothing for now - raise it again once jLiving have announced on 16 September",
 ]),
 ("status", "open"),
])
d['requests'].append(req)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print("REQ-27 raised,", len(req['why']), "chars,", len(req['options']), "options")

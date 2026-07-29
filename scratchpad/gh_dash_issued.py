import json

CATCH = (
    "Grange Hill WD001 was issued to Luke Baker at Chigwell (London) PLC at 16:07 today, "
    "GBP 39,006.77 ex VAT. THE PRICING WORKBOOK THE CLIENT NOW HOLDS NAMES ANOTHER FIRM AS ITS "
    "AUTHOR: dc:creator = 'Dan Parker;dan.parker@agsurveying.co.uk', plus two live external links "
    "Excel offers to update on open - agsurveying.sharepoint.com, C:\\Users\\LiamO'Donnell\\..."
    "Electrical Template - Draft - REV010.xlsx and C:\\Users\\Parke\\...The Datum Group Electrical "
    "- TEMPLATE Rev 5.xlsx. The proposal PDF's /Author reads 'Nicholas Baker'. REQ-27 for the third "
    "time: Georgie's to Pearce 28/07, SM5 Wexham 12:22 today, Grange Hill 16:07. A cleaned pack is "
    "built and verified at outputs\\grange-hill-reissue\\ - five files, zero traces, total asserted "
    "unchanged at GBP 39,006.77 - and goes to Adam with the 07:45 update. THE ROOT CAUSE IS NOT OUR "
    "TEMPLATE: I scrubbed ours this afternoon, but Gintare builds from her own copy at "
    "C:\\Users\\fenst\\Downloads\\Pricing Doc Template.xlsx, so the infected file is the one that "
    "reaches clients. Only a human can clean it. Also issued unfixed and raised to Adam before "
    "approval: GBP 419.32 of BSW supply unsold (twelve units priced against thirteen quoted and "
    "thirteen on the drawings), and spec 3.11.2, 3.13.1, 3.15.2 and 3.16 neither priced nor "
    "excluded, under a covering email reading 'We trust that everything is as per specification'. "
    "What was done RIGHT: the workbook was properly cut to sell-only - no buy prices, no supplier "
    "name - and the drawings are BSW's own sheets de-priced. Gordon Court did not repeat."
)

p = "data/dashboard-state.json"
d = json.load(open(p, encoding="utf-8"))
d["catches"].append({
    "date": "2026-07-29",
    "job": "Grange Hill Methodist Church (Chigwell (London) PLC) - WD001 - ISSUED",
    "catch": CATCH,
})
d["updated"] = "2026-07-29"
json.dump(d, open(p, "w", encoding="utf-8"), indent=1)
print("catches now", len(d["catches"]))

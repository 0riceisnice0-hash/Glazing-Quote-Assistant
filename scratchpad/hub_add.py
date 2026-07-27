# -*- coding: utf-8 -*-
"""Add the four jobs triage opened this afternoon to the hub."""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))
have = {j["job"] for j in d["jobs"]}

NEW = [
    {"job": "Riverside House AOV smoke vents", "client": "RRR Group", "deadline": "2026-08-26",
     "value": "GBP 4,845.22 Aplus net (supply only)", "stage": "pricing",
     "status": "Adam instructed the house pricing document and drawings on 27/07 - no urgency, he is "
               "waiting on PHDB's building-works costs before submitting. Site is Riverside House, 44 "
               "Wedgewood Street, Fairford Leys, Aylesbury HP19 7HL (planning 24/02303/PAPCR); the pack "
               "arrived 27/07. UNRESOLVED AND IT SHOULD BE SETTLED FIRST: Aplus QT51518 states GEOMETRIC "
               "free area 1.30 m2 only. Their Towcester Vale quote for the same DualFrame 75Si product "
               "states both figures, with aerodynamic running at 60-62% of geometric. If Riverside's "
               "1.5 m2 requirement is aerodynamic then 1.30 m2 geometric is roughly half of it, not "
               "0.20 m2 short - and Aplus's proposed 1235x1583 fix would still miss. REQ-9 covers it. "
               "Aplus price holds ~26/08; 155mm Technal subcill quoted against the 150mm asked for."},
    {"job": "Chester Thomas Developments - arched front door", "client": "Chester Thomas Developments",
     "deadline": "2026-08-27", "value": "GBP 4,455.99 quoted", "stage": "approved to issue",
     "status": "Adam 27/07: 'Good to go!'. Arched uPVC front door 1440x2250 GBP 2,917.35 + back door "
               "900x2100 GBP 1,038.64 + install GBP 500 = GBP 4,455.99 ex VAT; arithmetic ties. TWO "
               "THINGS FIRST: the approval thread is the generic client introduction and this client has "
               "THREE live quotes (arched door, 50 Main Rd 23/07, 3 Berry Close 08/07), so confirm which "
               "one is released; and the only supplier evidence is a file called 'PVC OPTION.pdf' - "
               "confirm it actually prices an ARCHED head."},
    {"job": "Ninn Lane Re-development", "client": "Ermine Construction Services",
     "deadline": "2026-08-08", "value": "GBP 100,730.00 quoted", "stage": "submitted",
     "status": "Quoted GBP 100,730.00 ex VAT on 09/07 - 60 units of aluminium windows and commercial "
               "doors across three buildings at Ninn Lane, Ashford, backed by Aplus QT51269. Lines total "
               "GBP 89,550.00 + GBP 11,180.00 install, ties exactly. NEEDS A HUMAN TODAY: Paul forwarded "
               "an Ermine portal notification on 27/07 ('new message ... MSG639Gv') and the message "
               "itself sits on the portal, which Mary cannot log into. With GBP 100k out it could be an "
               "award, a query or an addendum and nobody has opened it."},
    {"job": "Manor House (AFS Q7593)", "client": "TBC - no job folder exists",
     "deadline": "2026-08-08", "value": "unknown", "stage": "enquiry",
     "status": "Aluminium Fire Systems chased this on 27/07, their second chase of the afternoon. AFS "
               "quoted Q7593 on 09/07 with a 6-week lead time from order signature and first payment. "
               "TWO PROBLEMS: the quote PDF predates Mary's mailbox history so the VALUE IS UNKNOWN, and "
               "there is NO 'Manor House' or 'Manor' job folder anywhere in the archive - so either it "
               "is filed under an unconnected client name or the enquiry never got a folder. Gintare "
               "confirmed 'Manor House and Manor is same project'. Not Manor Lodge, which is Q7666."},
]

added = [n for n in NEW if n["job"] not in have]
d["jobs"].extend(added)
d["updated"] = "2026-07-27T17:05:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("added %d cards; hub now shows %d jobs" % (len(added), len(d["jobs"])))

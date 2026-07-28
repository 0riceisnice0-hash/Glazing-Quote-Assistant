# -*- coding: utf-8 -*-
"""Every exposure on this job, read the OTHER way for once.

All four recourse clauses verified at source in templates/proposal-content.json,
which matches MASTER COVER LETTER 31.05.2026.docx on all seven probes tested.
"""
import collections
import io
import json

P = 'data/job-checks/riverside-house-aov.json'
d = json.load(io.open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

E = [
    ("A Plus levy storage on goods uncollected more than 3 working days after first "
     "availability, and exclude holding materials off-site through a programme slip, requiring "
     "payment for the materials against a letter of indemnity. Recorded last turn as 'the first "
     "cost on this job that grows with the delay we deliberately accepted'.",
     "recorded as ours to absorb - WRONGLY, one-sidedly",
     "THREE PROVISIONS OF OUR OWN TERMS BEAR ON IT AND I HAD READ NONE OF THEM. (1) Inclusions, "
     "Installation: 'Installation is included within our costs as per final agreed programme. ANY "
     "DELAY OUTSIDE OF FENSTER'S CONTROL MAY INCUR ADDITIONAL COSTS.' (2) T&C, Cancellation and "
     "Postponement: 'Should the client cancel or POSTPONE the contract following procurement of "
     "materials..., Fenster reserves the right to retain the deposit and RECOVER ANY ADDITIONAL "
     "COSTS INCURRED up to the date of cancellation or postponement' - and A Plus's storage charge "
     "is precisely an additional cost incurred following procurement. (3) T&C, Supplier Delays and "
     "Liability: 'Fenster shall not be liable for delays, additional costs, losses, or "
     "consequential damages arising from delays, defects, or errors caused by third-party "
     "suppliers or manufacturers.' A programme slip driven by PHDB is a client-side delay, and our "
     "terms make client-caused additional costs recoverable. THE EXPOSURE IS RECOVERABLE, NOT "
     "ABSORBED - but only because the document carrying those terms is now issued with the price, "
     "which as of last night it was not."),

    ("Free area basis unresolved (C0/C1). If the 1m2 is aerodynamic, A Plus's 1.30m2 geometric "
     "gives roughly 0.78-0.81m2 and does not satisfy the drawing. A Plus's Product Performance "
     "clause makes Building Regulations compliance the Customer's and does not warrant that any "
     "product complies.",
     "us, on the supplier side",
     "QUALIFIED IN THREE PLACES, TWO OF WHICH NOW REACH THE CLIENT. (1) Clause 16 disclaims "
     "regulatory strategy and states reliance on the client's professional team. (2) Clause 2: "
     "'all quotations are subject to final site survey and measurement verification.' (3) The "
     "pricing document now states on its face that the free area quoted is GEOMETRIC and that no "
     "aerodynamic figure is warranted - added 28/07. NOT ELIMINATED: supplying a vent that does "
     "not meet the requirement is still a problem, and none of these makes it somebody else's "
     "product. But the entitlement position is materially better than 'the shortfall is ours', "
     "which is how it has been recorded since 27/07."),

    ("Validity gap. QT51518 lapses 26/08/2026 and our own house validity is 30 days, so an issue "
     "today closes after the supplier price it rests on. Adam is holding the submission pending "
     "PHDB, so the gap widens daily.",
     "us, commercially",
     "PARTLY BACKED, AND BE PRECISE ABOUT HOW FAR. Clause 2 makes our quotation valid 30 days "
     "'unless agreed otherwise' and expressly subject to final survey and measurement "
     "verification, so a lapsed input is a re-quotation rather than a fixed liability. T&C "
     "Supplier Delays reduces our LIABILITY for costs caused by a third-party supplier. NEITHER "
     "ENTITLES US TO MORE MONEY BY ITSELF - claiming that would be the overclaiming Gordon Court "
     "warns about. What they do is stop this being an open-ended exposure: the remedy is to "
     "re-price, not to absorb."),

    ("Part K anti-fall protection and the BS EN 60335-2 trap hazard below 2.5m FFL, both dependent "
     "on a cill height only the architect holds. Excluded by A Plus and excluded by us.",
     "nobody, until somebody is asked",
     "NOW BACKED ON OUR SIDE, WHERE IT WAS NOT ON 27/07. The pricing document states the "
     "exclusion on its face as of 28/07, and the accompanying terms carry the standard schedule. "
     "Before tonight the exclusion existed only in a template this job was never generated from - "
     "so the recourse is real but it is one day old, and it exists only if both documents are "
     "sent together."),

    ("The wind loading check to BS 6399-2 and the structural calculations on brackets and spigots, "
     "which A Plus put on the Customer and expressly do not warrant, on a second floor elevation "
     "with no structural engineer named on any of the six drawings.",
     "nobody appointed on this job",
     "OUR STANDARD EXCLUSION COVERS IT - 'Design Responsibility - design calculations, structural "
     "calculations and engineer approvals unless specifically included within our scope' - and it "
     "is now on the issued pricing document and in the accompanying terms. The company always had "
     "the answer; this job did not carry it until 28/07. RRR question 5 asks who is appointed, "
     "which remains the right question: an exclusion tells the client it is not ours, it does not "
     "tell anybody who will do it."),

    ("Testing and certification of the completed smoke ventilation system - excluded by us "
     "('Testing - on or off site testing'), and A Plus test the actuator on local batteries only.",
     "nobody, on a life-safety system",
     "OUR EXCLUSION IS REAL AND NOW ISSUED, but state the limit honestly: on a life-safety system "
     "an exclusion is a commercial answer and not a safety one. RRR question 10 now asks who "
     "carries the witnessed test and the certificate building control will want, and who arranges "
     "the RRO 2005 maintenance the occupier owes from handover."),

    ("Delivery. A Plus price ex-works and deliver free only above GBP 5,000; the order is GBP "
     "4,845.22, GBP 154.78 under, so carriage is charged at GBP 1/mile each way or the load is "
     "batched.",
     "us, and it is priced as provisional",
     "NONE, and that is the right answer. Nothing in our terms shifts a supplier's carriage to the "
     "client, and it should not - it is a cost of buying, not a risk. Carried as provisional at "
     "the supplier's stated basis and asked as RFQ item 6. Recorded as 'none' deliberately, "
     "because 'none' is an answer and an unread field is not."),

    ("Part-order re-price. A Plus price on the basis that materials are ordered together and in "
     "one phase, and reserve the right to re-price a part order. If C2 resolves to a roof vent we "
     "order one unit rather than two.",
     "us, and unquantified",
     "NONE ON THE TERMS, but the position is better than it looks for a different reason: nothing "
     "has been ordered and nothing issued, so the whole thing is still a question rather than a "
     "variation. RFQ item 13 asks the single-vent price BEFORE the architect answers. The recourse "
     "here is sequence, not contract - and asking early is the only form of it."),

    ("Dimensional risk on the 1130 x 1530, which came from Fenster's enquiry of 24/07 rather than "
     "from a survey or a dimensioned drawing.",
     "us",
     "NONE ON THIS JOB, and the reason matters. Our Additional Limitations - 'dimensions provided "
     "by others are assumed to be accurate; any additional costs arising from incorrect dimensions "
     "shall be treated as a variation' - would back us if the sizes had come from the client's "
     "team. They came from us. So the clause that rescued Gordon Court's position 003 does not "
     "rescue this one, and clause 2's 'subject to final site survey and measurement verification' "
     "makes it fixable rather than somebody else's. Recorded as none rather than stretched."),
]

d['exposures'] = [collections.OrderedDict([("item", i), ("lands_on", l), ("our_recourse", r)])
                  for i, l, r in E]

json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
print('%d exposures recorded' % len(d['exposures']))

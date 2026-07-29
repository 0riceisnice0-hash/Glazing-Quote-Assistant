# Fill brocks-hill's new check_rfq_answered rule from the RFQ EMAIL, not from the quote -
# the whole point of the rule is that the two differ. Gintare's second, fuller RFQ went
# 24/07 15:29 with seven attachments and a "Folding doors in Chapel" heading reproducing
# spec 3.15.1 almost verbatim. What came back on 29/07 answered some of it and was silent
# on the rest. null quoted_response = silence.
import json

p = "data/job-checks/grange-hill-methodist-church.json"
m = json.load(open(p, encoding="utf-8"))

m["rfq_items"] = [
    {
        "item": "Chapel folding doors, spec 3.15.1 - 5.8m span, fold back to side walls, dark brown PPC, polyamide breaks, top rail below the trusses, bottom rail recessed into the floor",
        "requested": "RFQ 24/07 15:29, heading 'Folding doors in Chapel', reproducing 3.15.1 almost verbatim",
        "quoted_response": "REFUSED in writing 29/07: 'I have not included the internal bifold as there is no drawing of this. We do not supply this product with a level or recessed, and it cannot support toplights.' Reached the tender - excluded in the issued proposal as 'internal bifold doors have not been allowed'.",
    },
    {
        "item": "Upper glazed section over the folding doors, spec 3.15.1 - up to the underside of the pitched ceiling, frames to match the door fenestration",
        "requested": "RFQ 24/07 15:29",
        "quoted_response": None,
    },
    {
        "item": "Glazing, spec 3.11.1 - Pilkington Optitherm S1 with solar control, Arctic Blue outer / Optitherm S1 plus inner",
        "requested": "RFQ 24/07 15:29",
        "quoted_response": "Substituted without comment: '6 SKN 176 Tuff/16/6 HP Neutral' in the windows and '4mm Coolite SKN176II' plus '8.8 Lami / 6mm Tuff Anti Sun Grey' in the doors - two different tints in the same elevations. NOT flagged by BSW and NOT qualified in the issued proposal, which says only '6mm toughened / 6mm toughened Solar glazing'.",
    },
    {
        "item": "Ironmongery, spec 3.12.1 / 3.14.1 - Briton 1438 fire escape push pad with Briton 1413 access locking knob, Yale Platinum 3-star euro cylinders WITH THUMBTURN, all keyed alike",
        "requested": "RFQ 24/07 15:29",
        "quoted_response": "Partly refused: 'these would not include internal thumb turns as these are unnecessary'. Quoted ACIM071 lever + screw-in cylinder and ACIM453 concealed panic bar, not the Briton sets. The refusal did NOT reach the tender - the issued proposal says only 'panic hardware where quoted'.",
    },
    {
        "item": "Privacy film, spec 3.15.2 - horizontal frosted strip to the folding door glass, full width x 1.2m high",
        "requested": None,
        "quoted_response": None,
    },
    {
        "item": "Automatic door operator package, spec 3.13.1 - operator, safety sensor, strengthening, mounting plates, electrical supplies, push pads both sides, emergency release, keyed isolating switch",
        "requested": None,
        "quoted_response": None,
    },
    {
        "item": "Delivery to site - Peterborough to Chigwell",
        "requested": None,
        "quoted_response": "Not asked, and BSW stated their own terms unprompted: 'All estimates are ex works, additional delivery charges may apply' on QT253562, and no delivery terms at all on 0000000520. The issued proposal nonetheless says 'materials will be delivered to site'.",
    },
]

json.dump(m, open(p, "w", encoding="utf-8"), indent=1)
print("rfq_items: %d (%d never asked, %d asked and unanswered)"
      % (len(m["rfq_items"]),
         sum(1 for r in m["rfq_items"] if r["requested"] is None),
         sum(1 for r in m["rfq_items"] if r["requested"] and r["quoted_response"] is None)))

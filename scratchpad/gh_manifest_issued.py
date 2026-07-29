# Point the manifest at what was ACTUALLY ISSUED at 16:07, not at the document I built and
# withdrew. The trace rule will now fail, and it should: the file Chigwell holds is dirty.
import json

p = "data/job-checks/grange-hill-methodist-church.json"
m = json.load(open(p, encoding="utf-8"))

m["_state"] = (
    "ISSUED 29/07/2026 16:07 to Luke Baker, Chigwell (London) PLC, GBP 39,006.77 ex VAT, five "
    "attachments, cc Adam. Adam approved 16:02 with my corrections in front of him. This manifest "
    "now describes the ISSUED pack, not the return I built and withdrew. Buy behind it is still "
    "Bellview 0000000520 GBP 13,354.08 Grand Total Net and BSW QT253562 GBP 9,477.01 already net, "
    "GBP 22,831.09 - but the issued schedule prices twelve units against BSW's thirteen, so "
    "GBP 419.32 of that buy is unsold. A cleaned reissue pack is built and verified at "
    "outputs\\grange-hill-reissue\\."
)

m["issued_documents"] = [
    {
        "name": "Chigwell - Grange Hill Methodist Church Ext Pricing.xlsx (AS ISSUED 16:07)",
        "path": "scratchpad\\gh-issued-to-luke-att\\Chigwell - Grange Hill Methodist Church Ext Pricing.xlsx",
        "is_the_priced_document": True,
        "exclusions_stated": 0,
    },
    {
        "name": "Chigwell - Grange Hill Methodist Church Ext Proposal.pdf (AS ISSUED 16:07)",
        "path": "scratchpad\\gh-issued-to-luke-att\\Chigwell - Grange Hill Methodist Church Ext Proposal.pdf",
        "is_the_priced_document": False,
        "exclusions_stated": 20,
    },
    {
        "name": "Window and Door Drawings.pdf (AS ISSUED 16:07)",
        "path": "scratchpad\\gh-issued-to-luke-att\\Window and Door Drawings.pdf",
        "is_the_priced_document": False,
        "exclusions_stated": 0,
    },
]

m["_not_issued"] = (
    "outputs\\Grange Hill Methodist Church - WD001 Pricing Document (29-07-2026).xlsx and its "
    "proposal HTML were built by Mary and WITHDRAWN at 14:40 once Gintare's pack was found. Not "
    "issued, never to be quoted - the live number is GBP 39,006.77, not GBP 40,528.59. The HTML "
    "also failed the placeholder scan with three 'insert site/product photo' frames."
)

# The four clauses that reached the client neither priced nor excluded. The issued proposal's
# exclusions schedule is a general one; it names none of these.
for item in m["spec_items"]:
    if item["ref"].startswith(("3.15.2", "3.16.1", "3.16.2")):
        item["treatment"] = "unresolved"
    if item["ref"].startswith("3.11.2"):
        item["treatment"] = "unresolved"
    if item["ref"].startswith("3.13.1"):
        item["treatment"] = "unresolved"

m["quantities"] = [q for q in m["quantities"] if not q["ref"].startswith("3.11.1 plain")]
m["quantities"].append({
    "ref": ("3.11.1 windows - the ISSUED schedule prices 12 units (seven 1200x1183) against BSW's "
            "13 (eight 1200x1183), and the marked-up drawings issued with it show all 13. "
            "GBP 419.32 of supply unsold"),
    "bill_qty": 12,
    "drawing_qty": 13,
})

m["priced_lines"] = [
    {"ref": "Sheerline aluminium windows W1-W12 as issued", "amount": 17132.69,
     "covered_by_our_exclusions": False},
    {"ref": "SMA aluminium doors D1-D3 as issued", "amount": 18254.08,
     "covered_by_our_exclusions": False},
    {"ref": "Installation as issued", "amount": 3620.0, "covered_by_our_exclusions": False},
]

json.dump(m, open(p, "w", encoding="utf-8"), indent=1)
print("manifest now describes the issued pack")
print("priced lines sum: %.2f" % sum(l["amount"] for l in m["priced_lines"]))

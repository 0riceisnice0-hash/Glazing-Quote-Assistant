import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

# ---- 1. job entry ----------------------------------------------------------
for j in d["jobs"]:
    if j.get("job", "").startswith("St Mary"):
        j["status"] = (
            "QUOTE SUBMITTED 17/07 at GBP 174,546.37 ex VAT and it STANDS - the arithmetic is clean. "
            "All 31 window types reconcile to BSW QT252799 exactly on quantity and price, all 7 SMA lines "
            "to Bellview 0000000483 at the 15% discounted figure, and the global install line of "
            "GBP 21,915.05 reconciles to the penny against the house labour codes. The Filwood trap did "
            "NOT bite on the biggest line - Type AK (1825x5580) is correctly coded CW and carries "
            "GBP 3,055.05 of curtain-wall labour at GBP 150/m2. "
            "CORRECTION TO THE RECORD: the price is backed by BSW QT252799 (GBP 61,056.80) + BELLVIEW "
            "0000000483 (GBP 30,352.38) = GBP 91,409.18. Aplus QP70172 is NOT in the price - it is dated "
            "22/07, five days after we submitted, on a different system (Technal) and quoted UNGLAZED. "
            "SIX THINGS NOW OPEN, none of which change the price yet: (1) the pack sets two different "
            "U-values and we followed the looser one - schedule 2376-09 says 1.4 W/m2K, the client's EDG02 "
            "energy guidelines say 1.3 windows / 1.2 external doors / g-value 0.4-0.3, and NEITHER "
            "supplier states any U-value or any coating on the GBP 30,352 of doors and curtain walling; "
            "(2) Type G puts a Sheerline 70mm casement inside a Smart Wall 100mm frame - the SM5 Wexham "
            "error, live; (3) we exclude scaffold and MEWPs while the prelims require the Contractor to "
            "provide all scaffolding, on elements up to 5,580mm tall; (4) SOW 1.09 allocates strip-out "
            "and disposal of the existing windows into item 6.01, which is our line; (5) manifestation "
            "(schedule cl 2.24) is in neither quote and neither list; (6) both supplier quotes lapse "
            "mid-August but the JCT MW start on site is 14/09 with completion 11/12 and GBP 500/day "
            "delay damages. REQ-5 remains answered - the 24/07 addendum does not change our scope."
        )
        j["value"] = "GBP 174,546.37 quoted - cost GBP 91,409.18 - 202.80 m2, 107 units"
        j["stage"] = "submitted - awaiting ET&S"

# ---- 2. new requests -------------------------------------------------------
new_reqs = [
 {
  "id": "REQ-15", "raised": "2026-07-27",
  "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
  "owner": "Adam",
  "title": "St Mary's: the tender pack sets two different U-values and we quoted the looser one",
  "why": (
    "Window schedule 2376-09 states 'achieve u value of 1.4 w/m2k' against every window type, 33 times, "
    "and that is what our proposal promises. But EDG02 'Energy and Carbon Design Guidelines - Building "
    "Fabric', issued in the same 08/07 pack, sets the client's minimum for the REFURBISHMENT column at "
    "1.3 W/m2K windows, 1.2 W/m2K external doors and a glazing g-value of 0.4-0.3. We miss all three. "
    "It gets worse on the evidence: BSW QT252799 states no U-value anywhere (only a centre-pane glass "
    "Ug of 1.0, which is not a whole-window Uw), and Bellview 0000000483 - GBP 30,352.38, a third of our "
    "cost, covering all 9 doors and the MC600 curtain walling - states no U-value, no low-E, no soft "
    "coat, no argon and no coating of any kind. Neither quote contains any solar control product, so the "
    "0.4-0.3 g-value is definitely not in the price. Aplus's own advisory notes put the default in "
    "writing: commercial doors and framing 'up to 3.0 W/m2/K'."),
  "needs": (
    "Somebody has to ask ET&S which document governs. If it is EDG02 the glass changes on all 107 units "
    "and the price moves; if it is the window schedule we are compliant at 1.4 but should say so "
    "explicitly rather than leave it inferred. Either way BSW and Bellview should be made to state a "
    "whole-window Uw in writing - right now we have promised a number no supplier has confirmed."),
  "options": [
    "Ask ET&S in writing which governs - EDG02 or window schedule 2376-09",
    "Get a stated whole-window Uw from BSW and Bellview before anything else",
    "Price the EDG02 uplift (1.3 / 1.2 / g 0.4-0.3) as a variation and hold it ready",
    "Qualify the tender formally at 1.4 W/m2K per the window schedule"
  ],
  "status": "open"
 },
 {
  "id": "REQ-16", "raised": "2026-07-27",
  "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
  "owner": "Adam",
  "title": "St Mary's Type G: a Sheerline window is to go inside a Smart Wall frame - the SM5 Wexham error, live",
  "why": (
    "Schedule 2376-09 Type G / W.24 (2 no, 968x3620) requires '1 no. top hung + 1 no. fixed glazing + 1 "
    "no. external door'. Bellview pos 001 quoted a single pivoted anti-fingertrap door and TWO FIXED "
    "FIELDS, with glazing listed as '1 x prepared for a thickness of 28mm' - the opening vent is not in "
    "the Smart Wall element, an aperture was left for it. BSW QT252799 then fills that aperture: 'Qty: 2 "
    "Prestige Casement Location: TYPE G INSERT GBP 697.58', an 854x900 Sheerline opening casement. So a "
    "Sheerline 70mm casement is to sit inside an SMA Smart Wall Pocket 100mm frame, in a pocket prepared "
    "for a 28mm glazed unit. On SM5 Wexham (24/07) BSW ruled in writing that Sheerline cannot be coupled "
    "to Smart Wall because there is no coupler between the depths."),
  "needs": (
    "A written fabrication answer from BSW and Bellview before any order. It is GBP 697.58 of cost but "
    "2 no Type G is GBP 8,499.66 of sell, and if the answer is that it cannot be built that way the "
    "opening vent has to come from Bellview in Smart Wall and the element is repriced."),
  "options": [
    "Ask BSW and Bellview in writing how Type G is actually built, before order",
    "Have Bellview quote the top-hung vent within the Smart Wall element and drop the Sheerline insert",
    "Hold Type G out of any order until the fabrication detail is confirmed"
  ],
  "status": "open"
 },
 {
  "id": "REQ-17", "raised": "2026-07-27",
  "job": "St Mary's Refurbishment, Merthyr Tydfil (E T & S Construction)",
  "owner": "Adam",
  "title": "St Mary's: three scope boundaries with ET&S are undefined - access, strip-out and manifestation",
  "why": (
    "(1) ACCESS. Our proposal excludes 'Access/Lifting Equipment - Scaffold, MEWPS, Towers, Forklift' "
    "while including installation, and we are installing elements up to 5,580mm tall - 55.97 m2 of "
    "glazing is 3.62 m or taller, none of it reachable from the ground. The tender preliminaries say the "
    "opposite twice: item F requires the Contractor to provide 'all materials, labour, scaffolding, "
    "plant, tools, carriage and everything else necessary', and item B requires him to provide all "
    "scaffolding 'for himself and any Sub-Contractor'. That probably lands on ET&S, but our exclusion is "
    "unqualified so the boundary is undefined and it will be argued on site. "
    "(2) STRIP-OUT. SOW item 1.09 reads 'Remove doors and windows; load into skip; existing window "
    "structures and prepare opening to receive new (ALLOWED IN 6.01)' - and 6.01 is our supply-and-fit "
    "line. Our proposal excludes waste removal generally but never names removal of the existing "
    "windows. On 107 openings that is not a rounding error. "
    "(3) MANIFESTATION. Schedule clause 2.24 requires manifestation to glazed entrance doors and "
    "screens; it appears in neither supplier quote and our proposal recites it without either including "
    "or excluding it."),
  "needs": (
    "One email to Tom Godfrey at ET&S settling all three in writing. None of them changes our price "
    "today; all three are things that get argued after award if left as they are."),
  "options": [
    "Send ET&S one email settling access, strip-out and manifestation in writing",
    "Re-issue the proposal with the three boundaries stated explicitly",
    "Price strip-out, disposal and manifestation as a stated optional extra"
  ],
  "status": "open"
 },
]
have = {r["id"] for r in d["requests"]}
d["requests"].extend(r for r in new_reqs if r["id"] not in have)

# ---- 3. catches ------------------------------------------------------------
new_catches = [
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "The client's energy guidelines (EDG02) require 1.3 W/m2K windows, 1.2 W/m2K doors and a g-value of 0.4-0.3; the window schedule says 1.4 and we quoted 1.4. The energy annex was the tighter document and nobody had opened it.",
  "type": "specification", "value": "not yet quantified"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "Bellview 0000000483 - all 9 doors and the MC600 curtain walling - states no U-value and no coating of any kind, against a proposal promising 1.4 W/m2K.",
  "type": "specification", "value": "GBP 30,352.38 of supply"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "Type G puts an 854x900 Sheerline casement (70mm) inside an SMA Smart Wall Pocket frame (100mm), in a pocket prepared for a 28mm unit. BSW have already ruled the two systems cannot be coupled.",
  "type": "technical", "value": "GBP 8,499.66 of sell at risk"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "We exclude scaffold and MEWPs while the tender preliminaries require the Contractor to provide all scaffolding for himself and any sub-contractor - on 55.97 m2 of glazing 3.62 m or taller.",
  "type": "scope", "value": "boundary undefined"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "SOW item 1.09 allocates removal and disposal of the existing windows into item 6.01 - our supply-and-fit line. Our proposal excludes waste removal generally but never names it.",
  "type": "scope", "value": "107 openings"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "Both supplier quotes lapse mid-August (BSW ~14/08, Bellview ~15/08) but the JCT MW start on site is 14/09 - so GBP 91,409.18 of cost is unfixed before day one, against a fixed sell and GBP 500/day delay damages.",
  "type": "commercial terms", "value": "GBP 91,409.18 of cost"},
 {"date": "2026-07-27", "job": "St Mary's Refurbishment",
  "catch": "The record said the price was backed by BSW + Aplus QP70172. It is BSW + Bellview. Aplus is dated 22/07 - after we submitted - on a different system and quoted unglazed; reordering against it would have bought the wrong job with no glass.",
  "type": "record", "value": "GBP 30,352.38 misattributed"},
]
seen = {(c["job"], c["catch"]) for c in d["catches"]}
d["catches"].extend(c for c in new_catches if (c["job"], c["catch"]) not in seen)

d["updated"] = "2026-07-27T17:45:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("requests:", len(d["requests"]), "catches:", len(d["catches"]))

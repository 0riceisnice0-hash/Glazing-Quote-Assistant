import json

ENTRY = {
    "job": "Grange Hill Methodist Church (WD001 tender return)",
    "client": "Chigwell (London) PLC",
    "date": "2026-07-29",
    "basis_type": "Mary supplier-backed SELL vs the estimator's supplier-backed SELL, same two supplier quotes",
    "mary": 37278.59,
    "actual": 39006.77,
    "error_pct": -4.4,
    "basis": (
        "Both figures are built on the same buy: Bellview 0000000520 doors and BSW QT253562 "
        "windows, 29/07/2026. Mine ran all 16 units through mary_pricing and came to "
        "GBP 37,278.59 (before GBP 3,250 of house allowances for the 3.13.1 operator and 3.11.2 "
        "manifestations, which are excluded from both sides of this comparison). Gintare's "
        "pricing document, sent to Adam 13:10 the same day, came to GBP 39,006.77. NOT PERFECTLY "
        "LIKE FOR LIKE: she prices 15 units, I priced 16 - she schedules seven 1200x1183 windows "
        "where BSW quote eight, which is the GBP 419.32 discrepancy reported to Adam. So she is "
        "4.4% above me on ONE FEWER UNIT; on equal units the gap is wider still."
    ),
    "lesson": (
        "FIRST TIME I HAVE COME IN LOW AGAINST A HUMAN, and it is the first comparison where "
        "both sides were supplier-backed rather than one being a register benchmark. The five "
        "earlier points are four high and one low with a mean bias of +10.4%, and every high one "
        "compared a REGISTER benchmark against a real sell. Take the register out and the bias "
        "does not survive: when the supply price is the supplier's own, what differs is only the "
        "house adder and labour, and there the estimator is more generous than the engine's code "
        "mapping. My code assignment reproduces GBP 37,278.59 exactly but is not unique - "
        "reasonable alternative codes span about GBP 1,160 (3%) on this job, which is the real "
        "resolution of a template that prices by product code rather than by unit. DO NOT QUOTE "
        "AN ENGINE FIGURE TO THREE DECIMAL PLACES AS IF IT WERE THE ONLY ONE THE TEMPLATE GIVES. "
        "And the wider lesson has nothing to do with arithmetic: I should not have produced a "
        "second number at all. quote_send_dates.py would have shown the estimator's pack existed."
    ),
    "size_band_note": (
        "Not a size-band finding. Both sides carry the identical unit mix apart from the one "
        "disputed 1200x1183, so the difference is entirely in code adders and labour."
    ),
}

p = "data/calibration.json"
d = json.load(open(p, encoding="utf-8"))
d["entries"].append(ENTRY)
json.dump(d, open(p, "w", encoding="utf-8"), indent=1)
print("calibration entries:", len(d["entries"]))

import json

CATCH = (
    "Gintare's tender pack, with Adam for checking since 13:10 and due to the client today, "
    "prices SEVEN 1200x1183 windows where BSW quote EIGHT. Her Frames column totals "
    "GBP 22,411.77 against BSW's GBP 22,831.09 - the difference is exactly one unit at "
    "GBP 419.32 - and the marked-up drawings issued with the quote show all thirteen window "
    "items. So either the client receives a drawing pack showing a window we have not sold, or "
    "BSW's quotation carries a unit too many and must be corrected before we order. About "
    "GBP 830 of sell. Same shape as SM5 Wexham's restrictors: house supply passes through pound "
    "for pound, so an unsold unit comes straight off margin. Found by reading her pack against "
    "the two supplier quotations. Four spec clauses in the same pack are neither priced nor "
    "excluded - 3.11.2 manifestations, 3.13.1 the DDA automatic door operator, 3.15.2 privacy "
    "film and 3.16 the two FD60 doorsets - and the proposal states materials will be delivered "
    "to site against two ex-works BSW quotes with no carriage rate anywhere. All sent to Adam, "
    "nothing issued."
)

p = "data/dashboard-state.json"
d = json.load(open(p, encoding="utf-8"))
d["catches"].append({
    "date": "2026-07-29",
    "job": "Grange Hill Methodist Church (Chigwell (London) PLC) - WD001",
    "catch": CATCH,
})
d["updated"] = "2026-07-29"
json.dump(d, open(p, "w", encoding="utf-8"), indent=1)
print("catches now", len(d["catches"]))

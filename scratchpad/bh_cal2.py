import json,sys
sys.stdout.reconfigure(encoding="utf-8")
p="data/calibration.json"
d=json.load(open(p,encoding="utf-8"))
key=[k for k,v in d.items() if isinstance(v,list) and v and isinstance(v[0],dict) and "mary_estimate" in v[0]][0]
print("list key:",key,"n=",len(d[key]))
d[key].append({
 "job":"Brocks Hill Phase 2 Teaching Block - full scope, after the 7 missing doors were added",
 "client":"Spacemaker Developments Ltd",
 "date":"2026-08-04",
 "mary_estimate":134580.22,
 "actual":118278.52,
 "basis":"Mary's corrected indicative of 29/07 (tender as drafted 93,673.34 + quantified missing scope 40,906.88), both excluding mastic/EPDM, against the tender Gintare actually issued to SMD on 31/07/2026 at 15:12, also excluding mastic/EPDM. Like for like: +13.78%.",
 "basis_type":"SELL vs SELL - but THE HUMAN FIGURE IS THE ONE WITH THE ERROR IN IT, which is new. The issued 118,278.52 omits the DAD uplift (5 x 1,500) and the installation labour (5 x 500) on the five Strongdor steel doors; the arithmetically correct issue price is 128,278.52. Against THAT, Mary is +4.91%. Quote the pair, not the 13.78% alone.",
 "lesson":"FIRST POINT WHERE MARY'S BENCHMARK BEAT THE ISSUED DOCUMENT. The four prior sell-vs-sell points all ran high (+10.5% bias) and the standing read was that the register over-prices. Here the gap is 13.78% and 10,000 of the 16,302 is a mechanical omission in the human's workbook, not conservatism in the register - so roughly 61% of this 'error' is the actual being wrong. TWO CONSEQUENCES. (1) Do not add this to the bias average without the correction; a calibration set that treats every issued document as ground truth will train the estimator to reproduce other people's missing adders. (2) The whole-job comparison is what exposed it - a per-line reconciliation of sell minus supply against the code table found the one row out of nine whose adder was zero, and that is now a cheaper check than re-pricing the job."
})
json.dump(d,open(p,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("appended, n=",len(d[key]))

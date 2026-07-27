import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

r = next(x for x in d["requests"] if x["id"] == "REQ-25")
r["why"] += (
  " UPDATE 27/07 22:20 - THE RESUBMISSION IS DRAFTED AND WAITING, so that if Tom Godfrey confirms the "
  "package is open there is nothing left to write. 'outputs/St Marys Refurbishment - Revised "
  "Clarifications for a 27-07 resubmission (draft).txt'. It is qualification wording only and CHANGES NO "
  "FIGURE - the tendered sum stays at GBP 174,546.37. Eleven clauses, drop-in for the proposal's "
  "clarifications block: the Smart Wall door U-value stated honestly against SMA's published 1.8 with an "
  "offer to price a compliant alternative; the window U-value and the EDG02 g-value we have not allowed "
  "for; manifestation INCLUDED at 24.10 linear m per your ruling, with the Type F/H extent excluded and "
  "priced as a variation if required; access reworded per your ruling and now grounded on Preliminaries "
  "clause B; the panic-bar-versus-non-lockable-device conflict; anti-ligature ironmongery and fobbed "
  "reader preparation excluded by name; the Type G interface; the 2376-08 versus 2376-09 size conflict; "
  "a price validity clause; and the CF77/CF47 postcode correction to both documents. "
  "TWO DECISIONS ARE YOURS AND THE DRAFT DOES NOT PRE-EMPT THEM. (a) STRIP-OUT - I have written both "
  "wordings rather than choose. You said you would include it for a job this size but that if they assume "
  "it is not included, happy days, which leans toward silence. The risk of silence is that SOW item 1.09 "
  "reads 'Remove doors and windows; load into skip... (ALLOWED IN 6.01)' and 6.01 is our supply-and-fit "
  "item, so the client's own document already reads as though it is ours. My recommendation is to state "
  "it as included. (b) DELIVERY AND CARRIAGE - neither supplier includes it, BSW's delivery address is "
  "our own Milton Keynes premises and site is roughly 150 miles away, and there is no carriage line in "
  "the pricing document. It cannot stay silent: either a haulage figure goes in or it is excluded in "
  "terms. No rate for it exists anywhere in our records.")
r["needs"] = (
  "First, someone must phone Tom Godfrey and establish whether the package is genuinely open until close "
  "of play - Mary cannot, email is down (REQ-23) and only ever reached adam@/marketing@. If it is open, "
  "the only things standing between us and a corrected submission are your two decisions above: strip-out "
  "stated or silent, and carriage priced or excluded. Everything else is written.")
r["options"] = [
  "Call Tom Godfrey now and confirm the package is open until close of play",
  "Issue the drafted clarifications with strip-out INCLUDED and carriage excluded",
  "Issue the drafted clarifications with strip-out silent and carriage excluded",
  "Get a haulage figure first, then issue with carriage priced",
  "Let the 17/07 quote stand and raise the findings as post-tender clarifications"
]

d["updated"] = "2026-07-27T22:25:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
back = json.load(open(P, encoding="utf-8"))
got = next(x for x in back["requests"] if x["id"] == "REQ-25")
assert "RESUBMISSION IS DRAFTED" in got["why"], "update did not land"
print("REQ-25 updated and verified | options:", len(got["options"]))

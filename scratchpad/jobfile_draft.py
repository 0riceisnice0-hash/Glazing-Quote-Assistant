import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\jobs\st-marys.md"
s = open(P, encoding="utf-8").read()

anchor = "> **And our own recorded deadline was never a client date.**"
block = """> ### THE RESUBMISSION IS DRAFTED AND WAITING
>
> `outputs\\St Marys Refurbishment - Revised Clarifications for a 27-07 resubmission (draft).txt`
>
> **It changes no figure** - the tendered sum stays at GBP 174,546.37. Eleven clauses of qualification
> wording, drop-in for the proposal's clarifications block: the Smart Wall door U-value stated against
> SMA's published 1.8 with an offer to price a compliant alternative; the EDG02 window and g-value items
> not allowed for; **manifestation INCLUDED at 24.10 linear m** per Adam's ruling, with Types F/H excluded
> and priced as a variation; **access reworded** per Adam's ruling and grounded on Prelims clause B; the
> panic-bar-vs-"non-lockable device" conflict; anti-ligature ironmongery and fobbed-reader preparation
> excluded by name; the Type G interface; the 2376-08 vs 2376-09 size conflict; a price validity clause;
> and the **CF77 -> CF47 postcode correction** on both documents.
>
> **TWO DECISIONS ARE ADAM'S AND THE DRAFT DOES NOT PRE-EMPT THEM.**
>
> 1. **STRIP-OUT** - both wordings drafted. His ruling leaned toward silence (*"if they assume it's not
>    included and do it for us then happy days"*), but SOW item 1.09 cross-refers it INTO our item 6.01,
>    so the client's own document already reads as though it is ours. **Recommendation: state it as
>    included.**
> 2. **DELIVERY AND CARRIAGE** - cannot stay silent. Neither supplier includes it, BSW's delivery address
>    is our own Milton Keynes premises, site is ~150 miles away, and there is no carriage line in the
>    pricing document. Either a haulage figure or an explicit exclusion. No rate exists in our records.
>
> Posted to Adam on the hub and added to REQ-25.

"""
s = s.replace(anchor, block + anchor, 1)
open(P, "w", encoding="utf-8").write(s)
print("job file: draft block added ->", "RESUBMISSION IS DRAFTED" in s)

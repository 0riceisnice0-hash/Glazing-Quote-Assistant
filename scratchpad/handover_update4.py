import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("| **St Mary's Refurbishment"))

add = (
 " **4TH TURN 27/07 - REQ-17 ANSWERED BY ADAM AND CLOSED** (hub message 31, 19:42, delivered into the "
 "`gordon-court` chat and forwarded intact): *\"Our proposal document should state that we have not "
 "allowed for any access. Strip out is something we need to clarify in future tenders. We have "
 "effectively left it unanswered however we would include it for a job of this size, but if they assume "
 "it's not included and do it for us then happy days. We can allow the manifestation for a job of this "
 "size, however we should be putting this in our inclusions or on our description.\"* **All three are now "
 "actions and two of them cost money that is not in the GBP 174,546.37.** ACCESS: our wording is already "
 "correct (Access/Lifting Equipment excluded by name) - **but the ruling settles what our document says, "
 "not who pays**, against Prelims F and B requiring the Contractor to provide all scaffolding *\"for "
 "himself and any Sub-Contractor\"* on elements up to 5,580mm with 55.97 m2 of glazing 3.62m or taller. "
 "**REQ-22 raised** and replied to Adam on the hub. STRIP-OUT: **107 openings / 202.80 m2**, and the "
 "install line **cannot absorb it** - GBP 21,915.05 reconciles to the penny as per-unit fit labour, so "
 "there is no slack in it (Gordon Court reached the identical conclusion on GBP 46,840). MTCBC's SOW "
 "1.09 measures it in m2 and cross-refers it INTO our item 6.01, so *\"if they assume it's not included\"* "
 "is the less likely outcome here. MANIFESTATION: extent now **measured rather than undefined** - "
 "**24.10 linear metres** of two-band manifestation across the 9 glazed door and screen units (Types G, "
 "I, L, O, U, AF, AK), or **39.90 linear m** if Types F and H, the two 3,620mm silled screens, count; "
 "clause 2.24 says *\"glazed entrance doors and glazed screens\"*, so that is the only judgement left. "
 "**NEITHER ITEM CAN BE BENCHMARKED: `data/supplier-rates.json` has no strip-out, removal, disposal, "
 "waste or manifestation category - 0 of 80, all checked** - so both need a real price. That makes two "
 "new register blind spots alongside secondary glazing, folding doors, vertical sliders and AOV/smoke "
 "vents. **AND MANIFESTATION IS NOW AN UNPRICED, UNEXCLUDED GAP ON FOUR LIVE JOBS** - St Mary's, Gordon "
 "Court, Brocks Hill and Filwood - with the Estimating Log itself carrying *\"Manifestations\"* as a note "
 "against two of them, so humans had spotted it before and it still never got priced.")

lines[i] = lines[i].replace(" | Adam: **REQ-19 (door schedule scope",
                            add + " | Adam: **REQ-22 (a number for strip-out and manifestation, or a "
                                  "decision to state them as inclusions and absorb them - they should "
                                  "not stay promised and unpriced; plus whether to put access LIABILITY "
                                  "to ET&S in writing before award). REQ-19 (door schedule scope")
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER row extended")

Q = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(Q, encoding="utf-8").read().split("\n")
j = next(n for n, l in enumerate(lines) if l.startswith("### Autopilot session log"))

rec = """### St Mary's - Adam answers REQ-17, and two register blind spots open up (2026-07-27, evening)

No work order. The turn's input was a handoff from `gordon-court` forwarding Adam's hub message 31
verbatim - the answer to REQ-17 had been delivered into their chat rather than mine. Recorded it, set
REQ-17 to answered, and replied to Adam on the hub.

**THE RULING, and what it leaves.** All three boundaries are now actions rather than questions, and two
of them cost money that is not in the GBP 174,546.37:

- **ACCESS** - *"our proposal document should state that we have not allowed for any access"*. Our
  proposal already excludes Access/Lifting Equipment by name, so the wording is right. **But the ruling
  settles what our document SAYS, not who PAYS** - Prelims F and B require the Contractor to provide all
  scaffolding *"for himself and any Sub-Contractor"*, we install to 5,580mm, and 55.97 m2 of the glazing
  is 3.62 m or taller. An unqualified exclusion is a negotiating position, not an agreement. **REQ-22.**
- **STRIP-OUT** - *"we would include it for a job of this size"*. It is not in the sold price. **107
  openings / 202.80 m2**, and the install line **cannot absorb it**: GBP 21,915.05 reconciles to the
  penny as per-unit fit labour, which is fit-only money. Gordon Court independently reached the same
  conclusion about their GBP 46,840. MTCBC's SOW item 1.09 measures strip-out in m2 and cross-refers it
  INTO our item 6.01, so on this job *"if they assume it's not included"* is the less likely outcome -
  their own document already reads as though it is ours.
- **MANIFESTATION** - allow it and state it in the inclusions.

**MEASURING THE THING THAT WAS "UNDEFINED".** Clause 2.24 asks for two bands at 850-1000mm and
1400-1600mm, so the quantity is just element width x 2 across whatever counts as a glazed door or
screen: **24.10 linear metres** over the 9 glazed door/screen units (Types G, I, L, O, U, AF, AK), or
**39.90 linear m** if the two 3,620mm silled screens (Types F, H) are included. That reduces the open
question from "the whole item" to "do silled windows count", which is a one-line RFI. Worth generalising:
extent undefined is not the same as unmeasurable - measure the band before raising the query.

**TWO NEW REGISTER BLIND SPOTS.** `data/supplier-rates.json` holds 80 categories and **not one** covers
strip-out, removal, disposal, waste or manifestation - all 80 checked. So the two items Adam has just
ruled we should allow are both items we cannot benchmark, on the refurbishment work that is most of what
we bid. They join secondary glazing, folding doors, vertical sliders and AOV/smoke vents. **And
manifestation is already an unpriced, unexcluded gap on FOUR live jobs** - St Mary's, Gordon Court,
Brocks Hill and Filwood - with the Estimating Log carrying *"Manifestations"* as a note against two of
them, so it had been spotted by humans before and still never priced.

**Also flagged to triage:** the noticeboard was back to **22,315 characters** within half an hour of the
20:40 archive that unfroze the bridge. The prompt-via-stdin fix is committed but inert until the restart
(REQ-21), so the 32,767 command-line ceiling still applies to board + handoffs + brief. Suggested an
earlier second sweep, and that until the restart a long finding is better placed in the poster's own
`data/jobs/<key>.md` with a short pointer on the board. Flagged rather than acted on - the board and the
archive belong to triage and two chats sweeping at once is how things get lost.

"""

lines[j:j] = rec.split("\n")
open(Q, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md record inserted")

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

Q = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(Q, encoding="utf-8").read().split("\n")
j = next(n for n, l in enumerate(lines) if l.startswith("### Autopilot session log"))
rec = """### St Mary's - the resubmission drafted against a deadline that is today (2026-07-27, late)

Triage verified the moved return date at source across all four registers and posted it to Adam on the
hub unprompted, since email is still down. So the escalation was done and nothing was left blocked on me
except the thing a human cannot do quickly: write the corrected submission.

**DRAFTED AND WAITING:** `outputs/St Marys Refurbishment - Revised Clarifications for a 27-07
resubmission (draft).txt`. **It changes no figure** - the tendered sum stays at GBP 174,546.37. Eleven
clauses of qualification wording, drop-in for the proposal's clarifications block:

1. **Smart Wall door U-value** stated honestly against SMA's published 1.8 W/m2K, with the 1.4 (schedules
   2376-08/09) and 1.2 (EDG02 area-weighted average) expressly not allowed for, an explanation that a
   compliant door is a system change rather than a glazing change, and an offer to price the alternative.
   MC600 curtain walling carved out as a separate thermally broken system.
2. **Window U-value and solar control** - 1.4 allowed for, EDG02's 1.3 and g-value 0.4-0.3 not, with a
   direct question about which document governs.
3. **Manifestation INCLUDED** at 24.10 linear m over the nine glazed door/screen units per Adam's ruling,
   with Types F and H excluded and priced as a variation if clause 2.24 is read to catch them.
4. **Strip-out** - BOTH wordings drafted, not chosen (see below).
5. **Access** reworded per Adam's ruling and now grounded on Preliminaries clause B rather than presented
   as a conflict.
6. **Delivery and carriage** - flagged as requiring a decision (see below).
7. **Ironmongery** - the panic-bar-versus-"non-lockable device" conflict put back as a question;
   anti-ligature ironmongery and fobbed-reader preparation excluded by name.
8. **Type G** interface subject to manufacturer confirmation.
9. **2376-08 vs 2376-09 rev A** size conflict, which governs.
10. **Price validity**, tied to the 14/09 start and 11/12 completion against 30-day supplier pricing.
11. Everything carried forward unchanged, plus a request that the panic-bar and French-door substitutions
    be accepted expressly this time.

Also corrects **CF77 8HA -> CF47 8HA** on both issued documents.

**TWO DECISIONS DELIBERATELY LEFT TO ADAM.** (a) **Strip-out** - his ruling leaned toward silence
(*"if they assume it's not included and do it for us then happy days"*), so both wordings are drafted and
the recommendation is stated rather than applied: SOW item 1.09 cross-refers strip-out INTO our item 6.01,
so the client's own document already reads as though it is ours, and silence is the weaker position.
(b) **Delivery and carriage** - this one cannot stay silent. Neither supplier includes it, BSW's delivery
address on the quote is Fenster's own Milton Keynes premises, site is ~150 miles away, 107 units, and
there is no carriage line in the pricing document at all. Either a haulage figure or an explicit
exclusion, and no rate for it exists anywhere in our records.

Added to REQ-25 and posted to Adam on the hub as an unprompted note, because the hub is the only outbound
route while REQ-23 is open.

**The shape of the turn is worth recording:** the finding was made last turn, the escalation was done by
triage this turn, and the remaining value was entirely in having the deliverable ready before the answer
comes back rather than after. On a deadline that expires the same day, drafting ahead of the decision is
the only way the decision can still be acted on.

"""
lines[j:j] = rec.split("\n")
open(Q, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md record inserted")

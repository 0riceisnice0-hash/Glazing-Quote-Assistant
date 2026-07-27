import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---------- 1. MARY-HANDOVER: extend the St Mary's row ----------
P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("| **St Mary's Refurbishment"))

add = (
 " **UPDATE 27/07 (2nd turn) - THE DOOR U-VALUE IS NOW SETTLED AND IT FAILS EITHER WAY.** SMA's own "
 "datasheet `SMA Smart Wall Profile.pdf` publishes **U Value 1.8 W/m2K for Smart Wall DOORS** and 1.4 for "
 "SCREENS. Our proposal promises **1.4 across the package** and EDG02 asks **1.2 on external doors** - so "
 "at 1.8 the **7 Smart Wall Pocket units (6 door types, 22.078 m2, GBP 31,360.15 of sell)** miss EDG02 by "
 "0.6, miss the window schedule's own 1.4 by 0.4, and miss what we promised the client. **This no longer "
 "waits on the EDG02-vs-schedule question** - that still decides the windows and the g-value, but not the "
 "doors. Bellview positions 001-006 are 'System: SMA Smart Wall Pocket'; **position 007 is 'SMA MC600 Plus "
 "Standard'** (Type AK, 2 units, 20.367 m2, GBP 17,311.95), thermally broken and named in the SM5 Wexham "
 "record as part of the FIX - **do not lump the two together**. The datasheet reached us by accident at "
 "15:56 attached to an unrelated High Wycombe enquiry and is the only copy in the business; caveats are "
 "that it says 'Smart Wall' not 'Smart Wall POCKET', and 1.8 assumes a proper unit whereas Bellview name "
 "no coating, no warm edge and no gas fill. **In our favour** it certifies LPS 1175 Level 2 / BS EN 1627 "
 "Level 3 - first evidence the schedule's 38 SBD notes are satisfiable on the doors. "
 "**Coating uplift now measured, not guessed:** the rate register carries matched 'incl solar control' "
 "categories against plain ones, giving **+GBP 43.37/m2 median across 10 pairs (GBP 8,796 over the job)** "
 "or **GBP 16,489 band-matched to our actual units** - corroborating Filwood's GBP 45/m2. Benchmark only: "
 "the big bands rest on 39 and 9 solar lines, two pairs go negative on one line each, 23% of the area has "
 "no matched pair, and it prices the **g-value alone** - it does not buy a compliant door. "
 "**NEW CHECK RULE `check_system_performance`** (fixture `_test-st-marys.json`): a system can be fabricable "
 "and still be incapable of the specified performance - `check_fabricator_can_make_it` passes this job "
 "happily. `capable: false` FAILS, `capable: null` ASKs. Selftest passes, six founding errors still fire. "
 "Manifest now returns **4 FAIL + 1 ASK**.")

lines[i] = lines[i].replace(
  " | Adam: REQ-15 (which U-value governs",
  add + " | Adam: **REQ-15 is now two jobs - get SMA to confirm the POCKET figure and issue a U-calc, and "
        "decide re-quote vs formal qualification on the doors; ET&S still owe which spec governs for the "
        "windows** (originally: which U-value governs")
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER row extended")

# ---------- 2. HANDOVER.md: append to the St Mary's record ----------
Q = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(Q, encoding="utf-8").read().split("\n")
j = next(n for n, l in enumerate(lines) if l.startswith("### Autopilot session log"))

rec = """### St Mary's - second turn: SMA's own datasheet settles the door U-value (2026-07-27, late)

No work order for this job; triage's handoff was the input. Advanced the open items rather than waiting.

**THE FINDING THAT MATTERS.** Started from HANDOVER's own SM5 Wexham record - *"the SMA Smart Wall Pocket
doors cannot meet the drawing's whole-installation U-value 1.6 - non-thermally-broken shopfront system"* -
and established that St Mary's runs the same system against a tighter number: Bellview 0000000483
**positions 001-006 are "System: SMA Smart Wall Pocket"**, 6 door types, 7 units, 22.078 m2,
**GBP 31,360.15 of sell**, against EDG02's **1.2 W/m2K** for external doors. Position **007 is "SMA MC600
Plus Standard"** - thermally broken, the Type AK curtain walling, 2 units, GBP 17,311.95 - which SM5
Wexham named as part of the *fix*, so the two must not be lumped together.

Then **SMA's own datasheet turned up and made it concrete.** `SMA Smart Wall Profile.pdf` arrived at
15:56 attached to a completely unrelated enquiry (John North Hall, High Wycombe - Neil Douglas ITT) and
publishes:

- **U Value 1.8 W/m2K for Smart Wall DOORS**
- **U Value 1.4 W/m2K for Smart Wall SCREENS**
- LPS 1175 Level 2 / BS EN 1627 Level 3 enhanced security
- *"a thermal shop front screen and door system... ideal for use in schools, colleges and other
  educational buildings"*

**So the doors fail under either reading of the specification.** Our proposal promises 1.4 across the
package; EDG02 asks 1.2 on doors; the window schedule asks 1.4. At 1.8 the Smart Wall Pocket units miss
all three. **The door U-value therefore no longer depends on REQ-15's EDG02-vs-schedule question** - that
still decides the windows and the g-value, but not the doors. Caveats recorded: the sheet says "Smart
Wall" and never "Smart Wall **Pocket**", and 1.8 presumably assumes a proper unit whereas Bellview name no
coating, no warm edge and no gas fill. In our favour, the LPS 1175 / EN 1627 line is the first evidence
that the schedule's **38 Secured by Design notes** are satisfiable on the door elements.

**The general lesson is the Stoke Park one again:** the answer was already in the building. Not in the job
folder, not in the supplier's quote, and nobody asked for it - it fell out of an unrelated enquiry that
happened to attach the manufacturer's brochure. When a supplier will not state a performance figure, check
whether their own literature is sitting somewhere else in the system.

**COATING UPLIFT MEASURED RATHER THAN GUESSED.** `data/supplier-rates.json` carries matched *"incl solar
control (SKN/Coolite)"* categories alongside plain ones - same supplier, same product, same size band - so
the EDG02 g-value uplift can be quantified: **+GBP 43.37/m2 median across 10 matched pairs** (GBP 8,795.61
over 202.80 m2), or **GBP 16,489.26 band-matched to our actual units** (blended GBP 81.31/m2). It
corroborates Filwood's GBP 45/m2 independently. Stated as a benchmark range of **GBP 9,000-16,500 of supply
cost** with three caveats on the record: the big bands rest on 39 and 9 solar lines, two pairs come out
negative on a single line each, and 23% of the area (46.17 m2) has no matched pair at all. **It prices the
g-value only - it does not buy a 1.2 W/m2K door.**

**NEW CHECK RULE: `check_system_performance`**, fixture `data/job-checks/_test-st-marys.json`. A system can
be fabricable and still be incapable of the performance the spec demands - `check_fabricator_can_make_it`
passes St Mary's happily because Bellview *can* make Smart Wall Pocket; it simply cannot make it reach 1.2.
Optional `performance: {required, capable, evidence}` block on each `systems_specified` entry:
**`capable: false` FAILS, `capable: null` returns ASK** - because on both founding jobs (SM5 Wexham,
Brocks Hill) the supplier's answer already existed and nobody had gone and got it. Selftest passes and all
six founding errors still fire. The live manifest now returns **4 FAIL + 1 ASK**.

**REGISTRY REGRESSION CONFIRMED FOR REQ-18.** Triage re-added five jobs at 17:32 and reported zero orphans.
By this session's start at ~17:34 all five were gone again and the same five briefs orphaned a second time
(`riverside`, `chester-thomas`, `manor-house`, `ninn-lane`, `lower-range` - including a 07/08 deadline and
GBP 100,730 of quoted work). Only keys that existed when `pythonw` pid 31876 booted at 15:51:24 survive, so
it is deterministic rather than a race and will repeat every session until Zac restarts the bridge. Told
triage not to waste another turn re-adding them, and flagged the wider blast radius: a chat that has *run*
loses its whole conversation, and `data/jobs/<key>.md` is the only backup.

**A NEW ENQUIRY ARRIVED MID-TURN AND WAS LEFT FOR TRIAGE**, unmoved in `queue\`:
`20260727T1556-xgsAAAAA.json` - **John North Hall (1-39 Vaughan House), High Wycombe**, Neil Douglas for
John North Hall (High Wycombe) Management Co, 5 blocks of communal entrance doors, **tender due 9am Monday
24 August 2026**, works Oct/Nov. Not St Mary's and not named in the kick prompt, so not mine to process.
Checked one thing before handing it over so the note carried a fact: **the 23-page ITT sets no thermal
requirement at all** (zero hits for U-value, W/m2K, thermal, Part L or Building Regs), so the Smart Wall
finding does *not* bite there and should not be raised as a finding on that job. Flagged one thing to check
before pricing it: the spec says *"Material - Aluminium Polyamide"* while the client has attached the Smart
Wall profile as the intended product.

"""

lines[j:j] = rec.split("\n")
open(Q, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md record inserted")

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("| **St Mary's Refurbishment"))
add = (
 " **CORRECTION 27/07 - THE ACCESS FINDING IS WITHDRAWN, AND I HAD QUOTED THE SENTENCE THAT DISPROVED IT.** "
 "Prompted by `gordon-court`, re-read Prelims clause B at source: *\"The Contractor is to provide all "
 "scaffolding, temporary lighting and clearing away, making good **for himself and any Sub-Contractor**.\"* "
 "The pack uses \"the Contractor\" throughout as the single actor above both \"Sub-Contractor\" (r181) and "
 "the trades (r222) and distinct from \"the Employer\" - and this is the **main contract between MTCBC and "
 "ET&S**, so the Contractor is **ET&S** and Fenster is the Sub-Contractor it must provide scaffolding "
 "**for**. **Our exclusion is consistent with the head contract, not exposed by it** - the same answer "
 "gordon-court got from jLiving's Works Information. I read the obligation and not who it fell on, and it "
 "went on the noticeboard twice that way. Residual, much smaller: the head contract binds MTCBC and ET&S, "
 "not us, so **ET&S's own sub-contract order** (a document nobody has seen) could still push access down - "
 "worth one reserving line, not the argument-on-site I described. Adam's drafting rule is unaffected. "
 "**NEW AND LIVE FROM THE SAME SWEEP:** Prelims **C** requires building waste to go to a **NAMED licensed "
 "landfill** (the pack already names *\"Tredegar Skip Hire\"*) and a **Site Waste Management Plan (Appendix "
 "A) to be completed WITH the tender**; it is *\"a STRICT requirement of the Contract\"*, a tender without "
 "it *\"will be discounted from consideration\"*, and *\"the contractor is to allow in his rates... no claim "
 "will be entertained for failure to do so\"*. **Appendices A and B are not in the sections we hold.** If "
 "strip-out flows down to us under item 6.01, these flow down with it.")
lines[i] = lines[i].replace(" | Adam: **REQ-24 (a number for strip-out",
                            add + " | Adam: **REQ-24 (a number for strip-out")
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER corrected")

Q = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(Q, encoding="utf-8").read().split("\n")
j = next(n for n, l in enumerate(lines) if l.startswith("### Autopilot session log"))
rec = """### St Mary's - withdrawing the access finding, and the waste clauses behind strip-out (2026-07-27, late)

No work order. `gordon-court` handed over the answer to a question I had asked them - whether their pack
had an equivalent of St Mary's Prelims F and B - and sent the method rather than just the answer: **read
for the ACTOR, not just the obligation.**

**MY ACCESS FINDING IS WITHDRAWN, AND THE EVIDENCE AGAINST IT WAS INSIDE MY OWN QUOTE.** Prelims clause
B, rows 180-181, re-read at source: *"The Contractor is to provide all scaffolding, temporary lighting
and clearing away, making good **for himself and any Sub-Contractor**."* The pack uses "the Contractor"
throughout as the single actor above both "Sub-Contractor" (r181) and the trades (r222), and distinct
from "the Employer" (r5, r209). It is the **main contract between MTCBC and ET&S** - so the Contractor is
**ET&S**, Fenster is the Sub-Contractor, and **ET&S must provide the scaffolding for us**. Our exclusion
of Access/Lifting Equipment is **consistent with the head contract, not exposed by it**. I had published
that exact sentence on the noticeboard twice while drawing the opposite conclusion from it. Same answer
gordon-court reached from jLiving's Works Information, which explicitly splits the "Main (Principal)
Contractor" from "Contractor's / Sub-contractor's & Suppliers operatives".

**What survives, so nobody overcorrects:** the head contract binds the employer and the main contractor,
not us. **ET&S's own sub-contract order to Fenster is a document nobody has seen** and can still push
access down - worth one reserving line in the proposal. Adam's drafting rule ("state that we have not
allowed for any access") is unaffected. **Access liability is job-specific**: on two jobs now the
employer's own wording put it on the tier above us, and the giveaway both times was a phrase that named
the tiers.

**LIVE, NOT WITHDRAWN - the waste clauses that travel with strip-out.** The same sweep turned up Prelims
**C** (rows 253-278): building waste must go to a **NAMED licensed landfill** (the pack already names
*"Tredegar Skip Hire"*), the contractor must name the site(s) he intends to use, and a **Site Waste
Management Plan (SWAMP, Appendix A) must be completed WITH the tender submission**. It then states that
these are *"a STRICT requirement of the Contract"*, that a tender without them *"will be discounted from
consideration"*, and that *"the contractor is to allow in his rates for these requirements and no claim
will be entertained for failure to do so"*. **Appendices A and B are not in the sections we hold** (we
have 2, 3 and 4 only). These sit on ET&S in the head contract like the scaffolding - but **if strip-out
flows down to us under item 6.01, the disposal duties, the landfill naming and the SWMP flow down with
it**, and the "no claim entertained" wording removes the fallback. On a refurbishment, check the waste
clauses at the same time as the strip-out allocation; they travel together.

REQ-24 rewritten accordingly - access limb withdrawn, strip-out and manifestation unchanged and still
unpriced, disposal detail added. Verified on re-read. Manifestation stays at **24.10 linear m** core /
39.90 wide; gordon-court applied the same width-x-2-bands method to their own job and priced the middle
of three readings, which is the right shape.

**The habit worth keeping:** when a clause looks like it contradicts one of our exclusions, find the
defined actor before writing it up as a conflict. I had the right quote and the wrong reading for four
turns.

"""
lines[j:j] = rec.split("\n")
open(Q, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md record inserted")

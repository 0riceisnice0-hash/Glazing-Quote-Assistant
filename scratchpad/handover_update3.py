import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("| **St Mary's Refurbishment"))

add = (
 " **3RD TURN 27/07 - READ DOOR SCHEDULE 2376-08, WHICH NOBODY HAD OPENED** (the job was priced off the "
 "window schedule). It **strengthens the U-value case and corrects our own analysis.** Strengthens: it "
 "carries the requirement twice more, independently of the energy annex - per-door notes on **D.01, D.17, "
 "D.22, D.26** reading *'Door to achieve min u-value of 1.4W/m2k'*, plus a general note *'External Doors "
 "U-value 1.2 w/m2k'*. So **1.4 is stated in the window schedule, the door schedule AND our own proposal** "
 "and no longer depends on EDG02 - ET&S cannot dispose of it by ruling the energy annex inapplicable. "
 "Corrects: that 1.2 is expressly *'an AREA WEIGHTED AVERAGE u-value - not a centre pane value'*, so under "
 "the SM5 Wexham rule no element may be rejected against it; our manifest had the basis recorded as 'per "
 "element' throughout and that was wrong for the doors. **The average was computed rather than asserted "
 "and the finding survives**: on 22.078 m2 of Smart Wall Pocket at SMA's published 1.8 plus at most "
 "20.367 m2 of MC600, MC600 would have to achieve **0.55 W/m2K** for the package to average 1.2 (a "
 "generous 1.0 gives 1.42; 1.4 gives 1.61). **NEW REQ-19 - four things in 2376-08 that are in nobody's "
 "price:** (a) **fobbed readers explicitly required** on D.01 and D.14, against our exclusion of access "
 "control and our own unresolved clarification that *'fobbed reader compatibility requires further "
 "review'* - Bellview's 7 units carry no electric strike, no rectifier and no transfer hinge; (b) "
 "**anti-ligature ironmongery specified** (Anti-Ligature Infilled Door Pull Handle 300x75 stainless, "
 "hinges to BS 7352, 200mm kicking plate) and not quoted - a **safeguarding** requirement on a special "
 "needs school; (c) **'No locking mechanism or latch' / 'Non-lockable device' on D.01/D.17/D.22/D.26** "
 "against the **concealed panic bars we priced on all 7 units** - and **Aplus flagged exactly this in "
 "writing** (*'It is unclear what a Non-Lockable Device is, quoted all doors with Panic Bars'*) while "
 "Bellview defaulted silently; (d) **the two architect's schedules disagree on external door sizes** - "
 "D.17 2570 high vs Type L 2410, D.22 1530x2270 with no priced equivalent, D.26 930x2100 vs Type U "
 "929x2370; only D.01 maps cleanly, and D.01 is also the *'4 panes bi-folding'* door our proposal "
 "substituted for commercial French doors without written acceptance. **TWO FALSE LEADS CLEARED - do not "
 "re-raise:** *making good* is NOT in our item (only strip-out cross-refers into 6.01; making good and "
 "decoration are MTCBC's **SOW section 8**, so our Internal Finishing exclusion is safe), and **this pack "
 "has no tender validity clause at all**, so the 90-day Section 20 trap from John North Hall does not "
 "apply here. Also checked and negative: the SMA commercial brochure is a 2009 corporate document with "
 "**no U-values**, so the 'Smart Wall vs Smart Wall POCKET' and MC600 caveats stay open - only SMA can "
 "close them.")

lines[i] = lines[i].replace(" | Adam: **REQ-15 is now two jobs",
                            add + " | Adam: **REQ-19 (door schedule scope - the safeguarding items should "
                                  "not wait). REQ-15 is now two jobs")
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER row extended")

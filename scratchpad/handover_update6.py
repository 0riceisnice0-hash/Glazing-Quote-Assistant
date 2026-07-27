import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\MARY-HANDOVER.md"
lines = open(P, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("| **St Mary's Refurbishment"))
add = (
 "**URGENT 27/07 - THE PACKAGE IS RE-OPENED AND THE RETURN DATE IS TODAY. REQ-25.** ET&S's own Document "
 "Register, issued with the 24/07 revised drawings and generated 7/24/2026 12:10:27, carries "
 "**\"Package return date: 27 July 2026\"** in its header. The **08/07, 09/07 and 16/07 registers all say "
 "17 July 2026** - same package, same package lead (Tom Godfrey). **So the 24/07 re-issue moved the "
 "deadline out by ten days and we did not notice.** We submitted on 17/07 and have treated the job as "
 "closed and awaiting award ever since. **REQ-5 was correct** - the addendum changed no scope, checked "
 "attribute by attribute across the drawings - but **the return date is in the register HEADER, not the "
 "drawings**, and the register was read three times over six turns without anyone reading the top of the "
 "page. **AND OUR OWN RECORDED DEADLINE WAS NEVER A CLIENT DATE**: the hub carried 16/08, which is the "
 "BSW/Bellview 30-day quote validity, and it had become \"the deadline\" because it was the only date "
 "written down. Now corrected to 27/07. **IF THE PACKAGE IS GENUINELY OPEN UNTIL CLOSE OF PLAY, every "
 "finding on this job stops being a post-mortem and becomes a corrected tender** - the door U-value (SMA "
 "1.8 against 1.4 promised and 1.2 required, GBP 31,360.15 of sell), strip-out and manifestation which "
 "Adam ruled on this evening and which are in neither the price nor the document, Type G, the missing "
 "carriage to a site 150 miles from BSW, and the CF77/CF47 postcode. **Mary cannot ask ET&S** - outbound "
 "email is down (REQ-23) and only ever reached adam@/marketing@ - so **somebody has to phone Tom Godfrey "
 "today.** ")
lines[i] = lines[i].replace("| **St Mary's Refurbishment", "| **St Mary's Refurbishment", 1)
# prepend the urgent block right after the row's opening cell delimiter
cut = lines[i].find(" | ")
lines[i] = lines[i][:cut + 3] + add + lines[i][cut + 3:]
open(P, "w", encoding="utf-8").write("\n".join(lines))
print("MARY-HANDOVER: urgent block prepended to the St Mary's row")

Q = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\HANDOVER.md"
lines = open(Q, encoding="utf-8").read().split("\n")
j = next(n for n, l in enumerate(lines) if l.startswith("### Autopilot session log"))
rec = """### St Mary's - THE PACKAGE RETURN DATE MOVED TO TODAY AND NOBODY SAW IT (2026-07-27, late)

No work order. `gordon-court` handed back a sharpened version of the actor test - go to the Contract Data
or Articles and read who the PARTIES are, rather than hunting for a tier-naming phrase. Applying it to
St Mary's led somewhere else entirely.

**THE FINDING.** The clean actor test could not be run here: **section 1, the Form of Tender, is not in
the sections Fenster holds** (we have 2, 3 and 4 - the prelims, the schedule of works and the drawings),
so there is no document defining the parties. Going instead to ET&S's **Document Register** - which I had
read three times for what was added when - turned up the header field:

| register | generated | **package return date** |
|---|---|---|
| original-08-07 | 7/8/2026 08:45 | 17 July 2026 |
| schedule-09-07 | 7/9/2026 08:49 | 17 July 2026 |
| pci-16-07 | 7/16/2026 11:43 | 17 July 2026 |
| **revised-24-07** | **7/24/2026 12:10** | **27 JULY 2026** |

**ET&S re-opened the package on 24/07 and moved the return date out by ten days, to today.** Same package
name, same package lead (Tom Godfrey). We submitted on 17/07 against the original date and have recorded
the job as submitted and awaiting award ever since. **REQ-25 raised**, hub deadline corrected from 16/08
to 27/07, job stage changed, and an urgent banner put at the top of `data/jobs/st-marys.md`.

**HOW IT WAS MISSED, WHICH IS THE TRANSFERABLE PART.** Triage's REQ-5 analysis of the 24/07 addendum was
right and was done properly - attribute by attribute across the drawings: 209 window refs, 38 types, 28
opening sizes, restrictor, obscure, U-value and SBD notes, all identical. **The return date is not in the
drawings.** It is in the register header, above the revision table, in a field that had said the same
thing three times. So the addendum check needs a **header diff** as well as a revision-table diff -
package return date, package lead, package name. A re-issue can move a deadline without touching a single
drawing, and it is the one change that cannot be recovered afterwards.

**AND THE SECOND-ORDER ONE, WHICH IS WORTH MORE ACROSS THE BOARD.** The hub had carried this job's
deadline as **16/08** since it opened. That is the **BSW/Bellview 30-day quote validity** - it had quietly
become "the deadline" because it was the only date anyone had written down. **A supplier's expiry is not a
client's deadline.** Asked triage to sweep the other jobs for deadline fields holding inferred rather than
stated dates.

**WHY IT MATTERS COMMERCIALLY.** Six turns of audit on this job have produced a list of things wrong with
a quote already on the client's desk: a door system that cannot meet the specified U-value under any
reading (SMA publish 1.8 against the 1.4 we promised and the 1.2 EDG02 asks - GBP 31,360.15 of sell),
strip-out and manifestation that Adam ruled this evening should be allowed and stated and which are in
neither the price nor the document, a Sheerline casement drawn into a Smart Wall frame, no carriage on a
site 150 miles from where BSW deliver, and the wrong postcode on our own documents. **If the package is
genuinely open until close of play, that list becomes a corrected and qualified tender instead of a
post-mortem.** Mary cannot establish it: outbound email is down (REQ-23) and only ever reached
adam@/marketing@. Somebody has to phone Tom Godfrey today.

"""
lines[j:j] = rec.split("\n")
open(Q, "w", encoding="utf-8").write("\n".join(lines))
print("HANDOVER.md record inserted")

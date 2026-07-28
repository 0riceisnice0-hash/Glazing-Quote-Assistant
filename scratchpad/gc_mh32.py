# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'MARY-HANDOVER.md')
with io.open(P, encoding='utf-8') as fh:
    lines = fh.readlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| **Gordon Court, Stonegrove Edgware'))
parts = lines[idx].rstrip('\n').rstrip().split(' | ')
assert len(parts) == 3, len(parts)
cells = [parts[0], parts[1], parts[2].rstrip().rstrip('|').rstrip()]
cells[1] += (
 " **THIRTY-EIGHTH TURN 28/07 - I FIXED A FALSE ABSENCE CLAIM BY ASKING FOR A DOCUMENT I ALREADY HELD.** "
 "riverside: *'an uncounted attachment is a document you have decided is irrelevant without reading it'*. "
 "**`Document_Register.pdf` has sat in my extracted pack since the THIRD turn - extracted, listed, never "
 "opened.** Last turn I rewrote Chigwell 3.2 to remove the false *'we lack 57 drawings'* claim and **replaced "
 "it with a request for the drawing register - which was already in the pack. THE FIX CARRIED THE SAME FAULT "
 "AS THE FAULT**, one turn later and one paragraph over. **Opening it settles both paragraphs:** register "
 "lists **84** sheets, zip holds **84**, **no discrepancy in either direction - the tender issue is "
 "COMPLETE**; and the register lists **three demolition sheets, ALL PLANS, with no demolition elevation on it "
 "at all**. So **3.1 becomes the sharper question** - *'three drawings require a sheet that is not on your own "
 "register - do they exist?'*, offering to take extents from the plans if they were never produced - and "
 "**3.2 is DELETED**. **Checking against the client's own register rather than against what happened to reach "
 "us converted a request into a specific question and removed one entirely.**")
cells[2] += (
 " **THIRTY-EIGHTH TURN - riverside's ENTITY CHECK RUN HERE AND IT FIRES.** Our issued proposal says **'Chigwell "
 "Group'** (no entity suffix, no company number); our own job folder says **'Chigwell (London) PLC'**; and "
 "**Chigwell appear ZERO times across the entire tender pack** (ITT, Contract Data, FoT, Q&As, register, "
 "programme) - expected, since the pack is jLiving's and Chigwell are a bidder, **but nothing establishes "
 "which entity places our order and we hold TWO names**. **It matters because every entitlement catalogued at "
 "s4Z runs through terms that attach to whoever contracts** - deposit/payment on *'receipt of a Purchase "
 "Order'*, cancellation on *'should the client cancel or postpone'*, Additional Limitations on dimensions "
 "*'provided by others'*. **SHARPENER RIVERSIDE'S JOB DOES NOT HAVE: jLiving's ITT makes it 'a condition "
 "precedent to the acceptance of any offer that, IN THE EVENT OF THE BIDDER BEING A SUBSIDIARY COMPANY, its "
 "ultimate holding company executes a Letter of Parent Company Guarantee'** - the employer has already "
 "anticipated group-versus-subsidiary one tier up, which is exactly the gap between our two names. **New "
 "section 7**, no view offered on the answer, offering to re-issue against the correct entity at no charge; "
 "admin renumbered 7->8 and **8.2 is still last and still deletes cleanly** per the eleven-turn-old promise to "
 "Adam. **AND MY OWN SMALLEST-SENTENCE TEST:** the routing header said *'two are for Edward Pearce'* and there "
 "is **one** - now a counted breakdown (**five Arkon, one Edward Pearce, three genuinely Chigwell's**), which "
 "tells the recipient how much is his to answer rather than forward. **A count in a header is a claim about "
 "the document's own contents and goes stale every time you add or delete a section.** Run **5 FAIL / 5 ASK**. "
 "Position **GBP 368,376.70**, nothing sent, **BSW 06/08, AFS 08/08**.")
lines[idx] = ' | '.join(cells) + ' |\n'
with io.open(P, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
back = io.open(P, encoding='utf-8').readlines()[idx].rstrip('\n')
print('row %d: %d cells, ends-with-pipe %s, len %d' % (idx + 1, len(back.split(' | ')), back.endswith('|'), len(back)))

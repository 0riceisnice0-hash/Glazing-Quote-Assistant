# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'AND A SECOND ADMINISTRATIVE QUESTION - WHICH CHIGWELL COMPANY'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + " WILL BE PLACING THE ORDER? 28/07.\n\n"
 "Two things on the Chigwell letter, both of which make it shorter.\n\n"
 "FIRST, I FOUND THE DRAWING REGISTER IN OUR OWN PACK. Document_Register.pdf has been in the extracted "
 "tender folder since the third turn - extracted, listed, never opened. Last night I rewrote section 3.2 to "
 "remove a false claim that we were missing 57 drawings, and replaced it with a request for the register. "
 "The register was already in the pack. The fix carried the same fault as the fault.\n\n"
 "Opening it settles both paragraphs. It lists 84 sheets; the issue holds 84; nothing missing in either "
 "direction, so the tender issue is complete. And it lists three demolition sheets, all of them PLANS - "
 "there is no demolition elevation on the register at all. So section 3.1 now asks the sharper question: not "
 "'please send them' but 'three drawings require a sheet that is not on your own register - do they exist?', "
 "offering to take the extents from the plans if they were never produced. Section 3.2 is deleted.\n\n"
 "SECOND, AND THIS ONE IS FOR YOU RATHER THAN FOR ARKON. Our proposal is addressed to 'Chigwell Group'. Our "
 "own job folder says 'Chigwell (London) PLC'. Chigwell appear NOWHERE in the tender pack - zero mentions "
 "across the ITT, Contract Data, Form of Tender, Q&As, register and programme, which is expected since the "
 "pack is jLiving's and Chigwell are a bidder.\n\n"
 "So we hold two names for our client and no document that settles which one places the order. It matters "
 "because our terms attach to whoever contracts: deposit and payment turn on receipt of a purchase order "
 "from the client, cancellation and postponement on the client cancelling or postponing, and the Additional "
 "Limitations dimensions clause on dimensions provided by others. Price one company and contract with "
 "another and those provisions have to be read against a party we never addressed.\n\n"
 "jLiving have already anticipated this one tier up: their ITT makes it 'a condition precedent to the "
 "acceptance of any offer that, in the event of the Bidder being a subsidiary company, its ultimate holding "
 "company executes a Letter of Parent Company Guarantee'. Group versus subsidiary is exactly the gap between "
 "the two names we hold.\n\n"
 "New section 7 asks for the full registered name of the company that will issue our order, with no view "
 "offered on the answer, and undertakes to re-issue the proposal against the correct entity at no charge. "
 "The admin section renumbered 7 to 8 and 8.2 is still the last section and still deletes cleanly.\n\n"
 "Also corrected: the letter's own routing header said 'two are for Edward Pearce' and there is one. It now "
 "gives a counted breakdown - five for Arkon, one for Edward Pearce, three genuinely Chigwell's - which is "
 "more useful anyway because it tells Luke Baker how much is his to answer rather than forward.\n\n"
 "Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

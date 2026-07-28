# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dashboard-state.json')
MARKER = 'OUR TEN YEARS COVERS GLASS AND FRAMES'
with io.open(P, encoding='utf-8') as fh:
    d = json.load(fh)
req = next(r for r in d['requests'] if r['id'] == 'REQ-26')
if MARKER in req['why']:
    raise SystemExit('already appended')
req['why'] += (
 "\n\n---\n\n" + MARKER + ". THE GEAR IS NEITHER, AND SOME OF IT IS LIFE-SAFETY. 28/07.\n\n"
 "Two things for you here, Adam, and both are about our own document rather than a supplier's. Neither changes "
 "the tendered figure.\n\n"
 "1. WHAT OUR TEN YEARS ACTUALLY COVERS. Clause 5 of the proposal warrants 'all glass and frame products "
 "supplied and installed by the company'. The other Mary chat found the same words on their job and pointed out "
 "that an AOV actuator is neither a glass product nor a frame product. Checked here against what the suppliers "
 "have actually quoted, and there are thirteen named classes of operating gear:\n\n"
 "  - 124 windows: Yale Shootbolt locks, EGRESS HINGES, Signature handles, eleven variants of Re*-Loc "
 "RESTRICTOR, internal and external Linkvent trickle vents.\n"
 "  - 44 patio doors: Inline patio locks, Prolinea handles, 35x35mm security cylinders, trickle vents.\n"
 "  - 15 external and communal doors: Standard Resi locks, Standard French locks, a PANIC BAR, 2D hinges, "
 "Prolinea levers, SP701 low thresholds.\n"
 "  - 3 EI30 doorsets: GEZE TS 5000 door closer, FUHR 833 3-point automatic lock and threshold striker, WILKA "
 "panic shootbolt guides and automatic locking, DR HAHN roller hinges, ECO SCHULTE handles.\n\n"
 "None of those is a glass product or a frame product on the ordinary reading. And this is not convenience "
 "hardware - the egress hinges, the panic bar, the restrictors and the fire door's closer and automatic lock "
 "are life-safety and fall-protection items on escape routes, and the Linkvents are the trickle ventilation "
 "the 8000mm2 requirement turns on. As the clause reads, we warrant the frame around the escape mechanism for "
 "ten years and the mechanism for nothing.\n\n"
 "I am not saying the clause is wrong. Excluding moving parts from a long warranty is a normal commercial "
 "position and it may be exactly what you intend. What is not workable is that nobody can tell which it is "
 "from the sentence, and a client who reads 'a 10-year warranty covering all glass and frame products supplied "
 "and installed' will read it as covering the door they are pushing on.\n\n"
 "AND THE INVERSE IS FREE AND IN OUR FAVOUR. AFS give us 10 years on 'mechanical aspects' of the three EI30 "
 "doorsets - longer than they give on the glass, and longer than our own clause gives on gear, which is "
 "nothing. So on those three doorsets we are holding supplier cover we have never passed on. That costs a "
 "sentence to fix. On the 183 BSW units the gear is uncovered in both directions, because BSW state no "
 "warranty at all - so the BSW letter now asks for the period by class of gear rather than by unit, and the "
 "AFS letter asks whether their ten years reaches ironmongery branded to five other manufacturers, since on a "
 "fire doorset the closer and the automatic lock are the parts that keep it a fire doorset.\n\n"
 "2. THE START DATE, WHICH I RAISED LAST NIGHT AND WHICH NOW HAS INDEPENDENT CORROBORATION. I grepped the "
 "whole issued proposal for every 'from the date of'. There is exactly one, and it is the thirty days on "
 "quotation validity. The ten years is dated from nothing. The other chat ran the same search on the standing "
 "terms document and got the identical result on a different job the same night. Ten years from order, from "
 "delivery, from completion of installation and from practical completion are four different promises, and an "
 "undated one is read against whoever wrote it. It is one sentence, it costs nothing, and it is on every "
 "quotation the company issues, which is why it is yours rather than mine.\n\n"
 "3. AND SOMETHING BSW HAVE BEEN SAYING SINCE 07/07 THAT I HAD NOT READ. BSW wrote no warranty clause and no "
 "exclusions clause, so rather than record that as 'no exclusions' I assembled one from the nine-line block at "
 "the foot of every page of all four quotations. Eight sentences, six of which shift responsibility. The one "
 "that matters: 'Please check all items thoroughly. Bellview will not be held responsible for any items "
 "missing from quotes.' That puts the completeness of the quotation on us - which is precisely the boundary my "
 "Parts A and B are about. There is no actuator, motor or control interface on the AOV positions; the Approved "
 "Document K guarding note in the specification is priced by nobody; and the one omission we did catch, the "
 "GBP 217.50 'PANEL SET UP', we caught late. I am not complaining about it and I think the allocation is fair. "
 "I am recording that it has been on all four quotations since 07/07 and I had quoted four other sentences out "
 "of the same paragraph without reading it.\n\n"
 "Also from that block: 'All items viewed from the outside', which governs HANDING on a schedule containing "
 "egress hinges and a panic bar. A unit fitted to the wrong hand is a replacement, not a variation. Asked - one "
 "line covers all 227 units.\n\n"
 "Position GBP 368,376.70, nothing sent. BSW by 06/08 and AFS by 08/08, both still needing a human to send "
 "them."
)
with io.open(P, 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('REQ-26 appended,', len(req['why']), 'chars')

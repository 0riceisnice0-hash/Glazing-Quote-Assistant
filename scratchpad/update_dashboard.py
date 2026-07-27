# -*- coding: utf-8 -*-
"""Session close-out 27/07 (afternoon run): fold today's findings into the hub state."""
import json, io

P = 'data/dashboard-state.json'
d = json.load(io.open(P, encoding='utf-8'))
d['updated'] = '2026-07-27T15:10:00Z'

jobs = {j['job']: j for j in d['jobs']}

jobs['Princess Beatrice House'].update({
    'stage': 'submitted',
    'value': 'GBP 279,244.69 quoted',
    'status': ('Quote ISSUED to Jason Mount 27/07 09:49 at GBP 279,244.69 ex VAT. Arithmetic verified: base GBP 272,771.68 '
               'unchanged from the 23/07 audit, EPDM GBP 8,276.91 and mastic GBP 5,356.22 now inside the subtotal, 2.5% MCD '
               'GBP 7,160.12 applied. THREE CONTRADICTIONS WENT OUT WITH IT: the proposal still calls mastic an optional extra '
               'while the pricing charges for it (GBP 13,633.13 exposed); the proposal says Technal STII while the pricing says '
               'Modeal, with no alternative-system qualification; and five pages of the drawings we attached say items are NOT '
               'PAS24 tested against a Part Q / SBD Silver ITT. The 3nr Louvre Type 01 are still neither priced nor excluded.'),
})

jobs['Crestwood Park Primary School'].update({
    'stage': 'submitted',
    'value': 'GBP 74,158.66 quoted',
    'status': ('Quote ISSUED to Reynolds 27/07 10:49 at GBP 74,158.66 ex VAT, dates amended as Adam asked. Build verified exactly: '
               'BSW QT252906 net GBP 27,329.60 + GBP 20,550.00 code adders = the GBP 47,879.60 of window lines to the penny. '
               'FINDINGS: we charge GBP 17,779.06 for Teleflex (24% of the tender) while our clarifications exclude "Teleflex '
               'controls / wiring" - drawing A007 expressly says to INCLUDE all installation, core wire, conduit and fittings, and '
               'there is no Teleflex supplier quote on file. Glass quoted is Coolite SKN175(ii), not the specified Pilkington '
               'Suncool Pro T 66/33, with the lam/tough panes apparently reversed. W15 (remove and infill) is neither priced nor '
               'excluded. W13/W14/W28 correctly omitted - no works required.'),
})

jobs['Air Separation Unit, Vesuvius Way'].update({
    'value': 'GBP 110,551.98 budget - understated',
    'status': ('DEADLINE THURSDAY. Budget GBP 110,551.98 ex VAT issued 27/07, but CONFIRMED AT SOURCE that it is understated: JHA NBS '
               'Section 2 clause L20 requires every external door to be 60 MINUTE FIRE RATED insulated steel-core, including "60 Min '
               'Door installed in curtain wall". The 2no doors are in at GBP 4,683.56 as standard Senior SPD150 aluminium - wrong '
               'product family. Worse, the welfare screen (GBP 8,377.50) and office entrance screen (GBP 41,000.00) carry doors '
               'within them: GBP 49,377.50, about 45% of the budget, sits on SF52 screens whose doors must be fire rated, which a '
               'standard SF52 cannot do. Needs a tested fire-screen system priced by a specialist - Aluminium Fire Systems are '
               'already quoting Manor Lodge. Compounds the open Senior-fabricator problem.'),
})

jobs['Grange Hill Methodist Church'].update({
    'status': ('DEADLINE TOMORROW. REQ-1 answered by Zac 27/07: the chapel folding doors (spec 3.15) ARE ours - add to the RFQ. '
               'Full 3.15 wording pulled from the tender spec: aluminium folding doors across the full chapel width (~5.8m) folding '
               'back to the side walls, dark brown PPC, polyamide breaks, Pilkington Optitherm S1 plus bronze tinted DGUs, top rail '
               'below the trusses, bottom track recessed for a level threshold, plus a fixed glazed section up to the underside of '
               'the pitched ceiling, plus frosted privacy film full width x 1.2m. No firm supplier price is achievable before the '
               'close - recommendation is a clearly labelled provisional sum, benchmark GBP 11,000-16,000 ex VAT (placeholder, not '
               'a price - there is no folding-door data in the register). Benchmark for the rest stands at GBP 27,560.07.'),
})

jobs['Hightown OLDS0056 New Back Door'].update({
    'stage': 'closed',
    'value': 'dropped',
    'status': ('CLOSED on Adam\'s instruction 27/07 08:53: "Let\'s leave anything for Hightown Housing for now. We have quoted them '
               'many times and don\'t win any works, so please disregard their quotes unless instructed otherwise." No action on the '
               '03/08 In-Tend deadline. Standing rule now applied to all future Hightown RFQs.'),
})

# --- requests -------------------------------------------------------------
reqs = {r['id']: r for r in d['requests']}

reqs['REQ-1'].update({
    'status': 'answered',
    'answer': 'Yes - ours, add to RFQ',
    'answered_by': 'Zac (dashboard)',
    'answered_at': '2026-07-27',
})
reqs['REQ-4'].update({
    'status': 'answered',
    'answer': 'No - disregard Hightown entirely. We quote them often and never win; leave their RFQs unless instructed otherwise.',
    'answered_by': 'Adam (email 27/07 08:53)',
    'answered_at': '2026-07-27',
})

d['requests'].extend([
    {
        'id': 'REQ-6', 'raised': '2026-07-27', 'job': 'Princess Beatrice House', 'owner': 'Adam',
        'title': 'The quote that went out charges for mastic and disclaims it in the same email',
        'why': ('The pricing document issued to Jason Mount on 27/07 charges GBP 5,356.22 for external mastic and GBP 8,276.91 for '
                'EPDM inside the subtotal, exactly as instructed. But the proposal sent with it still says "External mastic is '
                'charged as an optional extra", and EPDM is not mentioned in the clarifications at all. GBP 13,633.13 is charged in '
                'one document and disclaimed in the other, and the client has both.'),
        'needs': 'A decision on whether to reissue the corrected proposal to Guildmore now, or wait until they query it.',
        'options': ['Send a corrected proposal now', 'Leave it - deal with it if queried'],
        'status': 'open',
    },
    {
        'id': 'REQ-7', 'raised': '2026-07-27', 'job': 'Crestwood Park Primary School', 'owner': 'Adam',
        'title': 'We charged GBP 17,779 for Teleflex and excluded the part the tender says to include',
        'why': ('Drawing A007 requires 2No. operators per light, 1No. Midi or Maxi control per opening light, and expressly says '
                '"Include for all installation, core wire, conduit and fittings as required". Our proposal clarifications exclude '
                '"Teleflex controls / wiring" while the pricing charges GBP 17,779.06 for Teleflex - 24% of the tender. There is no '
                'Teleflex supplier quote in the job folder, so the basis of that figure cannot be traced.'),
        'needs': 'Where the GBP 17,779.06 came from, and whether the exclusion stands or gets withdrawn before Reynolds challenges it.',
        'options': ['Withdraw the exclusion, price the wiring', 'Exclusion stands - qualify it properly', 'Need the supplier quote first'],
        'status': 'open',
    },
    {
        'id': 'REQ-8', 'raised': '2026-07-27', 'job': 'Air Separation Unit, Vesuvius Way', 'owner': 'Adam',
        'title': 'Every external door has to be 60 minute fire rated - who prices it before Thursday?',
        'why': ('JHA NBS Section 2 clause L20 requires 60 minute insulated steel-core external doors, AND a "60 Min Door installed in '
                'curtain wall", AND a 60 minute louvred door meeting the NOVA acoustic report. My budget priced the 2no doors as '
                'standard aluminium at GBP 4,683.56, and the two curtain wall screens carrying doors total GBP 49,377.50 - about 45% '
                'of the GBP 110,551.98. A 60 minute door cannot go into a standard SF52 screen.'),
        'needs': 'A fire-screen specialist to price the door package. Aluminium Fire Systems already have Manor Lodge (Julian Ward, Q7666).',
        'options': ['Send it to Aluminium Fire Systems today', 'Try Strongdor', 'Qualify the return and price it later'],
        'status': 'open',
    },
    {
        'id': 'REQ-9', 'raised': '2026-07-27', 'job': 'Riverside', 'owner': 'Adam',
        'title': 'The AOV vents do not make 1.5m2 - do we resize?',
        'why': ('Aplus QT51518 quotes 2no 1130 x 1530 bottom hung smoke vents at GBP 4,845.22 net for the pair, but the geometric free '
                'area is 1.30 m2 against the 1.5 m2 required - 0.20 m2 short. Aplus have stated the fix: 1235 x 1583 achieves 1.5 m2 '
                'in the same configuration using 900mm chains instead of 850mm.'),
        'needs': 'Confirmation to go back to Aplus for a requote at 1235 x 1583, or that the opening cannot change and 1.30 m2 has to be argued.',
        'options': ['Requote at 1235 x 1583', 'Opening is fixed - argue 1.30 m2', 'Check with the fire engineer first'],
        'status': 'open',
    },
])

# --- catches --------------------------------------------------------------
d['catches'] = [
    {'date': '2026-07-27', 'job': 'Vesuvius Way Worksop',
     'catch': ('Specification requires every external door to be 60 minute fire rated, including doors inside the curtain wall '
               'screens. Caught 3 days before the deadline against a budget that priced them as standard aluminium.'),
     'type': 'spec compliance', 'value': 'GBP 49,377.50 of scope affected'},
    {'date': '2026-07-27', 'job': 'Crestwood Park',
     'catch': ('Quote excludes "Teleflex controls / wiring" while drawing A007 expressly requires all installation, core wire, '
               'conduit and fittings to be included - against a GBP 17,779.06 Teleflex charge with no supplier quote on file.'),
     'type': 'scope contradiction', 'value': 'GBP 17,779.06 at risk'},
    {'date': '2026-07-27', 'job': 'Princess Beatrice House',
     'catch': ('Proposal issued to the client still calls mastic an optional extra while the pricing document charges for it and '
               'for EPDM inside the total.'),
     'type': 'document contradiction', 'value': 'GBP 13,633.13 exposed'},
    {'date': '2026-07-27', 'job': 'Riverside',
     'catch': ('AOV smoke vents give 1.30 m2 geometric free area against the 1.5 m2 required - caught before order, with the '
               'supplier\'s own fix (1235 x 1583) identified.'),
     'type': 'performance shortfall', 'value': '0.20 m2 short'},
    {'date': '2026-07-27', 'job': 'Crestwood Park',
     'catch': ('Glass quoted is Coolite SKN175(ii), not the specified Pilkington Suncool Pro T 66/33, with the laminated and '
               'toughened panes apparently reversed - moving the solar control coating.'),
     'type': 'spec deviation', 'value': 'unqualified'},
    {'date': '2026-07-27', 'job': 'Stoke Park School',
     'catch': ('Glass order 46 panes short (+24 percent) caught before manufacture. CN Glass alternative approximately GBP 7,000 '
               'cheaper than Vetroseal for the same make-up - though on checking, that rate is a verbal confirmed by email, not a '
               'priced quotation.'),
     'type': 'procurement', 'value': '~GBP 7,000'},
    {'date': '2026-07-27', 'job': 'Grange Hill',
     'catch': 'Chapel folding doors (spec 3.15) missing from the supplier RFQ - confirmed as our scope on 27/07.',
     'type': 'scope gap', 'value': 'GBP 11-16k'},
    {'date': '2026-07-27', 'job': 'Hightown OLDS0056',
     'catch': 'Missed portal RFQ discovered via a stage-ending reminder - not on the log, no folder. Since closed on instruction.',
     'type': 'missed tender', 'value': 'closed'},
    {'date': '2026-07-24', 'job': 'SM5 Wexham',
     'catch': 'Fire-exit double doors quoted without the specified panic bar.', 'type': 'spec compliance', 'value': 'corrected'},
    {'date': '2026-07-24', 'job': 'Brocks Hill Phase 2',
     'catch': 'Supplier reply directly contradicts the triple-glazing spec.', 'type': 'spec conflict', 'value': 'open'},
    {'date': '2026-07-17', 'job': 'Greenfields Barnstaple',
     'catch': 'Register-only benchmark landed within 6.3 percent of the manufacturer quote.', 'type': 'validation', 'value': 'method proven'},
]

json.dump(d, io.open(P, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('jobs', len(d['jobs']), 'requests', len(d['requests']), 'catches', len(d['catches']))
print('open requests:', [r['id'] for r in d['requests'] if r['status'] == 'open'])
print('answered:', [r['id'] for r in d['requests'] if r['status'] == 'answered'])

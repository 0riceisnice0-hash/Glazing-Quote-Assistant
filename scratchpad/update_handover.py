# -*- coding: utf-8 -*-
"""Fold the 27/07 afternoon session into MARY-HANDOVER.md."""
import io, re

P = 'MARY-HANDOVER.md'
txt = io.open(P, encoding='utf-8').read()

txt = txt.replace(
    'Last updated: 2026-07-17 (later session:',
    'Last updated: 2026-07-27 (afternoon autopilot run: two client quotes went out and were audited - Princess Beatrice '
    'GBP279,244.69 and Crestwood Park GBP74,158.66; Vesuvius fire-door requirement confirmed at source; Hightown closed '
    'on Adam\'s instruction; REQ-1 answered). Earlier baseline 2026-07-17 (session:', 1)

# ---- Grange Hill -----------------------------------------------------------
old = ('| **RFQ SCOPE GAP flagged: spec 3.15 chapel alu folding doors (~5.8m, dark brown, bronze tint) + glazed section '
       'above NOT in the supplier RFQ** - Adam to confirm scope (option ~GBP10k budget); specialist auto-operator quote '
       'needed; check supplier return vs benchmark when it lands. |')
new = ('**REQ-1 ANSWERED 27/07 by Zac on the dashboard: "Yes - ours, add to RFQ".** Spec 3.15 IS Fenster scope. Full '
       'wording pulled from `test-results\\grange-hill-input\\-\\Specification - tender document.xlsx` (sheet '
       '"Specification section 1 - 4", rows B404-B410): **3.15.1** supply and install aluminium folding doors spanning the '
       'full chapel width (approx 5.8m), folding back onto the side walls, dark brown powder coated, polyamide thermal '
       'breaks, Pilkington Optitherm S1 plus BRONZE TINTED double glazed units; top rail just below the timber roof trusses '
       'so the doors clear them as they open; **any bottom rail recessed into the floor for a level threshold**; PLUS a '
       'fixed upper glazed section running from the doors to the underside of the pitched ceiling, frames matching the door '
       'fenestration. **3.15.2** horizontal frosted strip privacy film to the folding door glass, full width x 1.2m high. '
       'NO firm supplier price achievable before the 28/07 close - Mary\'s recommendation to Adam is a clearly labelled '
       'PROVISIONAL SUM, benchmark GBP11,000-16,000 ex VAT. **That range is a placeholder, not a price**: there is NO '
       'folding-door category in `data/supplier-rates.json` (checked), and the recessed track, raking head, non-standard '
       'colour and special glass are all specials. RFQ still needs the 3.15 wording issued regardless so the real number '
       'lands even if late. | Adam: carry 3.15 as a provisional sum or exclude it? Specialist auto-operator quote still '
       'needed; check supplier return vs the GBP27,560.07 benchmark when it lands. |')
assert old in txt
txt = txt.replace(old, new, 1)

# ---- Hightown --------------------------------------------------------------
m = re.search(r'\| \*\*Hightown Housing - OLDS0056[^\n]*\n', txt)
assert m
txt = txt[:m.start()] + (
    '| **Hightown Housing - OLDS0056 New Back Door (Q/REF 6159)** | **CLOSED 27/07 - DO NOT QUOTE.** Adam, 27/07 08:53: '
    '"Let\'s leave anything for Hightown Housing for now. We have quoted them many times and don\'t win any works, so '
    'please disregard their quotes unless instructed otherwise." The 03/08 12:00 In-Tend deadline is deliberately NOT being '
    'actioned. **This is a standing rule: ignore all future Hightown Housing RFQs and In-Tend reminders unless Adam says '
    'otherwise** - triage them as noise, one line in the session record, no email. REQ-4 closed as answered. (History: '
    'flagged 27/07 as a missed portal RFQ not on the Estimating Log with no job folder; indicative from Fenster\'s own '
    'Hightown history was GBP1,300-2,000 ex VAT.) | Nothing. Closed. |\n'
) + txt[m.end():]

# ---- Vesuvius --------------------------------------------------------------
old_v = ('| Adam: **SYSTEM DECISION** - whole pack is Senior (SF52/PURe/SPD150/PURe SLIDE) and none of BSW (Sheerline), '
         'Aplus (Technal) or Bellview (SMA) fabricate Senior; need a Senior-approved fabricator or a formal '
         'alternative-system qualification.')
new_v = ('**60-MINUTE FIRE-DOOR REQUIREMENT CONFIRMED AT SOURCE 27/07 - THE BUDGET IS UNDERSTATED.** Gintare asked Steve '
         'about this at 09:35 (estimating@, "as per specification all external doors to be 60min fire rated"); Mary verified '
         'it in the actual spec, `test-results\\vesuvius-input\\full-pack\\NBS Specification\\JHA-JOH-2024-055-JHA NBS '
         'Section 2.pdf`, clause **L20** (JHA Architecture, 15/07/2026): **"External Doors"** = "60 Min Insulated steel-core '
         'external open-out single-leaf door. PPC Galvanised double skinned door leaf with PPC Galvanised 90mm enclosed '
         'frame", vision panel 572x572, U-value 1.2; **"External Doors Curtain Walling"** = "60 Min Door installed in '
         'curtain wall to manufacturers design"; **"External Doors Louvered"** = 60 Min steel-core louvred leaf, louvres to '
         'the NOVA acoustic report; **L20/70** = tested to BS EN 1634-1 or 1634-3, third-party certified, Fire Door Schedule '
         'to Building Control BEFORE order. Impact on the GBP110,551.98: line B1-E (2no doors 1000x2450, sell GBP4,683.56) '
         'was priced as standard Senior SPD150 aluminium off BSW glazed-door medians - **wrong product family entirely**; '
         'and lines B1-D (welfare CW screen, GBP8,377.50) + B2-E (office entrance CW screen, GBP41,000.00) = **GBP49,377.50, '
         'about 45% of the budget, are SF52 screens with doors IN them** - a 60-min door cannot go into a standard SF52 '
         'screen, so those bays need a tested fire-rated screen system. Cannot be requantified until a fire-screen '
         'specialist prices it. **Aluminium Fire Systems (Julian Ward, julian@aluminiumfiresystems.com, 0121 277 4870) are '
         'already quoting Fenster on Manor Lodge Q7666 - the obvious source.** Note the spec also names "SAS Curtain Wall '
         'Design" for the CW doors, reinforcing the Senior problem. Separately, spec clause L20/45 "Door leaves (Internal)" '
         'carries the IDENTICAL external steel-core wording but names Howdens - looks like a JHA copy-paste error, worth an '
         'RFI. | Adam: **REQ-8** - who prices the 60-min door package before Thursday? Plus the open **SYSTEM DECISION** - '
         'whole pack is Senior (SF52/PURe/SPD150/PURe SLIDE) and none of BSW (Sheerline), Aplus (Technal) or Bellview (SMA) '
         'fabricate Senior; need a Senior-approved fabricator or a formal alternative-system qualification.')
assert old_v in txt
txt = txt.replace(old_v, new_v, 1)

# ---- Stoke Park: correct the CN Glass provenance ---------------------------
old_s = 'CN Glass quoted the same make-up GBP60/m2 inc energy (01/07, Steve/Martin Gregory) = ~GBP7,850, ~GBP7,000 less.'
new_s = ('CN Glass rate for the same make-up is GBP60/m2 inc energy (+GBP10/m2 if the inner leaf goes to 6mm tough softcoat) '
         '= ~GBP7,850, ~GBP7,000 less. **PROVENANCE CORRECTED 27/07 after Adam asked where it came from:** the only source is '
         '`Commercial\\2. Projects\\Borras\\Coventry - Stoke Park School\\1. Estimating\\2. Supplier Quotes\\CN Glass\\Re '
         'Stoke Park School - Coventry .eml` - Steve Freezer emailed Martin Gregory (martingregory@cnglass.co.uk) on 01/07 '
         'with the schedule and spec AND the rates already written into his own outgoing email; Martin replied only "Pls see '
         'below as discussed". So it is **a verbal rate confirmed by return email, NOT a priced quotation** - there is no CN '
         'Glass quotation document on file. Mary\'s 27/07 morning email said "CN Glass quoted", which overstated it; '
         'corrected to Adam in the afternoon digest. The make-up does match Vetroseal\'s (8.8L-16-4T), so the comparison is '
         'like-for-like, but CN Glass should price the final 24/07 list properly before any order moves.')
assert old_s in txt
txt = txt.replace(old_s, new_s, 1)

# ---- new rows: Crestwood + Riverside + Manor Lodge -------------------------
anchor = '| **Beaumont Court (Fortis Vision)** |'
assert anchor in txt
new_rows = (
    '| **Crestwood Park Primary School (Reynolds Conservation)** - NEW to Mary 27/07 | **QUOTE ISSUED 27/07 10:49 to '
    'adam@reynoldsconservation.co.uk - GBP74,158.66 ex VAT** (Adam 27/07 10:42: "Good to go, please amend the dates before '
    'sending" - dates WERE amended, 27/07 on both documents). High-level window replacement, part of Crestwood Park Roofing '
    'Works 2026, Dudley MBC, Lapwood Ave Kingswinford DY6 8RP. Return date was 20/07 - issued 7 days late. **Build verified '
    'exactly:** BSW **QT252906** (16/07/2026, Sheerline Prestige casement, Hipca White 9910HG) Total Nett Ex VAT '
    '**GBP27,329.60** + **GBP20,550.00** of house-template code adders = the **GBP47,879.60** of window lines to the penny '
    '(checked line by line: ELAW 637.50, LAW 487.50, SAW 337.50 adders land exactly on every row). Nothing dropped, nothing '
    'double-counted. Install GBP8,500 / 52 units = GBP163.46 each, consistent with the labour codes. 46 rows, 52 units, '
    '67.28 m2. **FINDINGS:** (1) **TELEFLEX GBP17,779.06 = 24% of the tender** as a single lump with no qty/rate breakdown '
    'and **no supplier quote anywhere in the job folder**, while our proposal clarifications EXCLUDE "Teleflex controls / '
    'wiring" - drawing **A007** expressly says "Include for all installation, core wire, conduit and fittings as required" '
    'and specifies 2No. operators per light + 1No. Midi (W1-W8, W20-W23) or Maxi (W12, W16-W19, W24-W27) control per opening '
    'light, control locations as existing. We have excluded the thing we are charging for. (2) **GLASS DEVIATION** - A007 '
    'requires outer 6mm Pilkington Suncool Pro T 66/33 toughened + inner 6.4mm laminated; BSW quoted every line as '
    '"6.Lam / 16 / 6mmTuff Coolite SKN175ii" - different product AND the lam/tough panes appear reversed, which moves the '
    'solar-control coating. Proposal p3 recites the specified Pilkington make-up back to the client then offers "6mm '
    'laminated / 16mm cavity / 6mm toughened" in the products box with no deviation stated. (3) **W15 neither priced nor '
    'excluded** - A007: "Window W15: To be removed and infilled as per the section" (remove window + winders, 75x50 tanalised '
    'ladder frame, 12mm WBP ply, prime and felt, PIR infill, 10mm white uPVC lining); a second note on the W22 elevation '
    'reads "Infill window as per W15". W13/W14/W28 correctly omitted - A007 says "No works required". (4) Existing windows '
    'to be "removed and disposed of" per A007 vs our exclusion "Waste Removal - Generally excluded". (5) W12 catering-standard '
    'insect mesh grill not priced. (6) **ASBESTOS (chrysotile) in the existing high-level window mastic** appears only in a '
    'prose sentence on proposal p3, NOT in the hard exclusions column - and our installers must remove those windows. '
    'Mastic GBP1,286.10 + EPDM GBP1,579.63 correctly shown as OPTIONAL here (note: opposite of what Adam ordered on Princess '
    'Beatrice - check whether that is now a policy change). Client-facing typos: "W23 2/2" should be 2/3; "EDPM". Tender pack '
    'extracted to `test-results\\crestwood-input`. | **REQ-7 open:** where did the GBP17,779.06 Teleflex figure come from, '
    'and does the controls/wiring exclusion stand or get withdrawn before Reynolds challenges it? Also: BSW to confirm pane '
    'order + coating surface; decide W15; get asbestos into the exclusions properly. BSW QT252906 valid 30 days from 16/07 '
    '(~15/08). |\n'
    '| **Riverside (Aplus QT51518)** - AOV smoke vents | Adam asked Gintare on 24/07 for 2nr AOV bottom-hung smoke vents '
    '1130x1530, STD white, 150mm cill, and to **confirm the free area - "We need 1.5m2 so sizes can be adjusted if '
    'required"**. Aplus quote **QT51518 (27/07/2026)** landed and Mary checked it: **GEOMETRIC FREE AREA = 1.30 m2, based on '
    'a 50mm reveal - 0.20 m2 SHORT of the 1.5 m2 required. ANSWER TO ADAM IS NO.** Aplus state the fix on p2: **1235 x 1583 '
    'achieves 1.5 m2** in the same configuration, using 900mm chains instead of 850mm. Price as quoted **GBP4,845.22 net ex '
    'VAT for the pair** (frames GBP4,662.15 + glass GBP171.31 + energy surcharge GBP11.76); 2no DualFrame 75Si, style FF, '
    'white, **155mm** subcill (Technal) not the 150mm asked for, open out, AOV 850mm stroke single chain, colour 9006 satin, '
    'glass 4-20-4 Clr Tough S Coat 1.2 / 20mm blk warmedge. **Supply only, delivered - no installation.** Valid 30 days '
    '(~26/08). Quote is specified No PAS24, No Restrictor, Handle Not Required, Casement locking None - normal for a smoke '
    'vent but confirm against Riverside\'s expectation. Aplus AOV notes to carry: cables NOT run through mullions (they leave '
    '~2m of flex coiled at the vent); **actuators are NOT restrictors** and Aplus disclaim liability for damage if a separate '
    'restrictor is not fitted 50mm beyond the stroke; vents below 2.5m FFL flag a trap hazard under BS EN 60335-2; below '
    '1100mm FFL need Part K anti-fall protection, which they exclude; 24v DC only; 15,000 cycles or 12 months warranty. | '
    '**REQ-9 open:** requote at 1235x1583, or is the opening fixed and 1.30 m2 has to be argued with the fire engineer? |\n'
    '| **Manor Lodge School (Aluminium Fire Systems Q7666)** | Not a Mary pricing job - watching it because AFS are the '
    'likely answer to Vesuvius. Gintare asked Chris Wall for an urgent 30-min fire-rated door quote 22/07; AFS quoted 23/07 '
    '(8 week lead time from order + first payment; fixing pack and delivery both priced as optional extras). Steve asked '
    '24/07 for a panic bar as the door is an escape route. **AFS replied 27/07 09:23: a push bar will not fit a 900mm door - '
    '920mm minimum width needed.** So the opening has to grow or the escape hardware has to change. | Steve: decide 900 -> '
    '920mm or alternative escape hardware. |\n'
)
txt = txt.replace(anchor, new_rows + anchor, 1)

io.open(P, 'w', encoding='utf-8').write(txt)
print('written')

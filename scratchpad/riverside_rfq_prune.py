# -*- coding: utf-8 -*-
"""Two questions the quotation already answers - one deleted, one rewritten.

Gordon Court's check: for each question in an RFQ, can it be answered by reading
the quotation you already hold? Their B2 asked BSW to confirm D_E and D_U were
door-and-sidelight assemblies when the coupler line on BSW's own quotation said
so. "Asking a supplier to confirm what their own quotation states costs you the
credibility of the questions that are real."

Run across all fourteen items here. A keyword screen fired on thirteen, which is
NOT the answer - most are cases where the quotation mentions the topic without
answering the question. Two survived actually reading them:

ITEM 5, THE VENT LEAF - answered, and it is the exact shape of their B2. The
specification block lists ONE "Sash DF1413 HD Vent (Glazed In)", ONE "Transom
DF1421 Std Flat Tran/Mull", "AOV Type 850mm Stroke Single" and "Open out". One
sash, one transom profile, one single-chain actuator. That IS the configuration
the item asks them to confirm - the whole frame opening as one bottom-hung leaf
with the transom as a bar within the sash. I used apertures A1 and A7 as evidence
of a transom and read past the Sash and Transom lines a few inches above them,
for eight turns.

Deleted rather than reworded. The genuinely open half - whether the 1.30m2 is
measured on the full inner aperture - is item 1's question and is already there,
and the shop drawing it asked for is not needed: "AOV Cable Direction Right
(Viewed from Outside)" is on the quote and is already on our drawings.

ITEM 12(a), THE WINDLOAD - milder but the same. The quote says 1200Pa "unless
otherwise stated" and nothing else is stated, so 1200Pa IS the figure. Rewritten
to ask what is actually open: whether 1200Pa suits a second floor elevation here,
and what they need from us to allow for a different one.
"""
import io
import re

P = 'outputs/Riverside House - RFQ to A Plus (draft, send by 26-08).txt'
t = io.open(P, encoding='utf-8').read()

OLD5 = '''5. THE VENT LEAF - please confirm what we think we are reading
   The quote lists apertures A1 (957 x 590) and A7 (957 x 591), so the frame is transom
   divided, but a single 850mm stroke actuator is quoted. We read the stated 1.30m2 as the
   full inner frame aperture (957 x 1357), which would mean the whole frame opens as one
   bottom-hung leaf with the transom acting as a glazing bar within the sash. Is that
   right? A shop drawing showing the leaf, the transom and the actuator position would
   settle it.

'''
assert t.count(OLD5) == 1, 'item 5 anchor'
t = t.replace(OLD5, '')

OLD12 = '''   (a) please confirm that 1200Pa is the figure used for these two vents, so that whoever
       carries out the check is checking against the right number;'''
NEW12 = '''   (a) we read your note as meaning 1200Pa has been used here, since nothing else is
       stated on the quotation. What we do not know is whether 1200Pa is right for a
       second floor elevation on this building. If the design team come back with a
       different figure, what would you need from us, and would it change the section or
       the price?'''
assert t.count(OLD12) == 1, 'item 12 anchor'
t = t.replace(OLD12, NEW12)

# renumber 6..14 -> 5..13
for old, new in [(6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13)]:
    t = re.sub(r'(?m)^%d\. ' % old, '%d. ' % new, t, count=1)

t = t.replace('THE FOURTEEN QUESTIONS REMAIN VALID', 'THE THIRTEEN QUESTIONS REMAIN VALID')
t = t.replace('a new quotation covering all fourteen points', 'a new quotation covering all thirteen points')

# every cross-reference in the letter, remapped from the printed list below
t = t.replace('item 7\'s "QT51518 is open for 30 days', 'item 6\'s "QT51518 is open for 30 days')
t = t.replace('which makes item 7 worth asking now', 'which makes item 6 worth asking now')
t = t.replace('items 5 and 9 in particular ask what they priced against',
              'item 8 in particular asks what they priced against')
t = t.replace('rather than by reply, for the same reason as item 1',
              'rather than by reply, for the same reason as item 1')
t = t.replace('If the resize at item 2 takes', 'If the resize at item 2 takes')
t = t.replace('that stairwell has no wall opening (item 9)', 'that stairwell has no wall opening (item 8)')

io.open(P, 'w', encoding='utf-8', newline='').write(t)

print('item 5 deleted, item 12(a) rewritten, renumbered to 13')
print()
print('EVERY NUMBERED HEADING NOW:')
for m in re.finditer(r'(?m)^(\d+)\. (.+)$', t):
    print('  %-3s %s' % (m.group(1), m.group(2)[:72]))
print()
print('EVERY CROSS-REFERENCE NOW:')
for m in re.finditer(r'item (\d+)', t):
    s = re.sub(r'\s+', ' ', t[max(0, m.start() - 60):m.start() + 70])
    print('  ...%s' % s)

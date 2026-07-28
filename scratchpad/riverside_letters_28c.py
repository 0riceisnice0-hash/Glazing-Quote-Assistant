# -*- coding: utf-8 -*-
"""Two new RFQ items and a reason added to RRR question 11."""
import io

# ------------------------------------------------------------------ RFQ
P = 'outputs/Riverside House - RFQ to A Plus (draft, send by 26-08).txt'
t = io.open(P, encoding='utf-8').read()

OLD = '''Many thanks,'''
NEW = '''13. ORDERING ONE VENT RATHER THAN TWO - WHAT HAPPENS TO THE PRICE?
   Your terms say the price "is based on the materials quoted being ordered together, and in
   one phase", that orders "for only part of the quote, or fabrication over multiple phases,
   may incur additional charges for paint surcharges, rolling set up charges, reduced
   material optimisation, delivery or increased fabrication costs", and that a re-price
   should be requested in that case.
   That is live for us rather than hypothetical. We are still establishing with the
   architect whether the second floor vent is a wall unit at all - the note says the stair
   is vented at the top storey roof, and that stairwell has no wall opening (item 9). If the
   answer is a roof unit, we would be ordering ONE of the two vents from this quotation.
   So please tell us what the supply price for a SINGLE 1130 x 1530 vent to this
   specification would be. We would rather know now than assume the quoted total simply
   halves.

14. STORAGE, AND WHAT HAPPENS IF SITE IS NOT READY
   Two of your terms bear on this and we would like to understand them before an order
   rather than during one:
     - you reserve the right to levy storage costs for goods uncollected more than 3 working
       days after first availability;
     - the quotation excludes holding materials off-site where the programme slips beyond
       your control, and in that case you would require payment for the materials against a
       letter of indemnity.
   Neither is unreasonable and we are not asking you to change them. The reason we raise it
   is that this job is sequenced openings formed, then survey, then manufacture, and the
   client has not yet given a date for forming the openings. So:
   (a) roughly how long after manufacture would the 3 working days start to run?
   (b) is there a normal arrangement for holding goods for a short period, and at what cost?
   We would rather build that into the programme than discover it.

Many thanks,'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

t = t.replace('THE TWELVE QUESTIONS REMAIN VALID',
              'THE FOURTEEN QUESTIONS REMAIN VALID')
t = t.replace('a new quotation covering all twelve points',
              'a new quotation covering all fourteen points')
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('RFQ updated')

# ------------------------------------------------------------------ RRR
P = 'outputs/Riverside House - Questions to RRR (draft).txt'
t = io.open(P, encoding='utf-8').read()

OLD = '''11. WHEN WILL THE OPENINGS BE FORMED?
   Our terms provide for a site survey only once structural openings are fully formed. So
   the sequence is: openings formed, then we survey, then manufacture. A rough programme
   date would help - it affects how long we can reasonably ask A Plus to hold their price.'''
NEW = '''11. WHEN WILL THE OPENINGS BE FORMED?
   Our terms provide for a site survey only once structural openings are fully formed. So
   the sequence is: openings formed, then we survey, then manufacture. A rough programme
   date would help - it affects how long we can reasonably ask A Plus to hold their price.
   There is a second reason it is worth a date rather than a range. Our window supplier
   charges storage on goods that remain uncollected more than three working days after they
   are ready, and their quotation excludes holding materials off-site where a programme slips
   for reasons outside their control - in which case they would look for payment for the
   materials before delivery. None of that is unusual, but it means the gap between
   manufacture and a ready opening carries a cost, and we would rather plan around a date
   than absorb it.'''
assert t.count(OLD) == 1
io.open(P, 'w', encoding='utf-8', newline='').write(t.replace(OLD, NEW))
print('RRR letter updated')

import sys
sys.path.insert(0, 'scripts')
import crm

K = 'excel-hoardings-kuoni-travel-3-crescent-arcade-solihul'

print(crm.lead(
    K, 'jacob',
    why=("Two quotations have been issued (29/07 and a revised one 04/08 09:45) and the stage "
         "still read 'acknowledged' from the AdminBase seed. quote_sent is the handover stage "
         "and this lead has been past it since 29/07. Next action left as Paul's Steve Dawson "
         "chase - that is still the thing that blocks everything."),
    stage='quote_sent'))

print(crm.note('lead', K,
    ("04/08 09:45 Paul issued quotation 2 to Excel Hoardings - revised, 'significantly increased', "
     "toughened laminated basis, upgraded glass lifter and more labour. 04/08 09:48 Gareth Siddle "
     "replied 'Perfect thank you, we shall be in touch.' That is an ACKNOWLEDGEMENT, NOT AN ORDER - "
     "no decision, and no objection to the price. Ball is with Excel and until now nobody owned "
     "chasing them. Commercial exposure: if Excel accept before Steve Dawson confirms the spec, we "
     "are committed to a unit we told Touchwood in writing on 03/08 might not fit the existing "
     "frame, and if the original turns out to be plain laminated the increase has to come back off "
     "a price they have already accepted. Holding note drafted for Paul to send Gareth: "
     "scratchpad/excel-gareth-holdfire.txt - his call. Buyer-side position now written up at "
     "data/companies/excel-hoardings.md."),
    'jacob', source='email',
    source_ref='<LOBP302MB22891C7F0EE46F37BE9D2647ACD42@LOBP302MB2289.GBRP302.PROD.OUTLOOK.COM>'))

print(crm.note('lead', K,
    ("Lead value of 208.33 is wrong and is not the job: 250 / 1.2 = 208.33, so AdminBase captured "
     "the GBP 250 survey fee ex VAT as the lead value. The real figure is whatever quotation 2 says "
     "and is materially larger. I do not price, so I have not set it - somebody with the quotation "
     "in front of them should."),
    'jacob', source='bot'))

print(crm.task('lead', K, 'chase_excel_decision',
    'Chase Gareth Siddle for a decision on quotation 2', 'jacob', due='2026-08-11',
    detail=("Quotation 2 issued 04/08; Gareth acknowledged it the same minute with 'we shall be in "
            "touch' and nothing since. One week is the chase point - this is exactly where Fenster's "
            "quotes go quiet. Gareth Siddle, gareth@excelhoardings.com, 07376 159364; Jason, Richard, "
            "Harriet and Lynne are cc on the whole thread. Owner Paul Taylor - I draft, I do not send. "
            "IF THE SPEC IS STILL UNCONFIRMED ON 11/08, this stops being a chase and becomes a warning: "
            "do not push them to accept a number that may move.")))

print(crm.task('lead', K, 'set_lead_value',
    'Set the lead value from quotation 2', 'jacob', due='2026-08-06',
    detail=("Current 208.33 is the de-VAT'd survey fee, not the job. The figure is in the quotation "
            "Paul attached on 04/08 09:45 in the commercial@ thread. Owner Gintare or Paul - "
            "Jacob does not price.")))

print(crm.company('excel-hoardings', 'jacob',
    why=("First job, and the position is now written up at data/companies/excel-hoardings.md. "
         "Bradford address and a live quotation out; relationship stays 'quoted' until they order."),
    postcode='BD12 0RT', domains='["excelhoardings.com","hoardingdepot.co.uk"]',
    last_contact='2026-08-04'))

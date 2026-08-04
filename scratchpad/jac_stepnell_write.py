# -*- coding: utf-8 -*-
import sys, json, os, shutil
sys.path.insert(0, 'scripts')
import crm

# ---- 1. FILWOOD: the quote left on 30/07 and nobody handed it over. It is mine now.
crm.lead('stepnell-bcc-filwood-broadway', 'jacob',
    why=("Quote ISSUED 30/07/2026 13:32 by Gintare from estimating@ to adam.warner@stepnell.co.uk, "
         "GBP 85,767.58 ex VAT (+ optional external mastic 605.05 and EPDM 3,081.49). Adam Warner "
         "acknowledged at 13:35: 'I will review it and get back to you if I have any questions.' No "
         "quote-handover reached my inbox for this one - I found it in the sent thread and in the issued "
         "Pricing.xlsx dated 30/07/2026. Mary's 30/07 note that nothing had gone to Stepnell was true "
         "when she wrote it and was overtaken the same afternoon."),
    stage='quote_sent', value=85767.58,
    next_action=("Paul Taylor emails Adam Warner (draft D-8): does BCC accept SMA in place of the "
                 "specified Aluprof, and who is buying the window package on White Hall."),
    next_action_date='2026-08-11')

crm.note('lead', 'stepnell-bcc-filwood-broadway',
    ("THE RISK ON THIS QUOTE IS THE SYSTEM, NOT THE PRICE. The tender specified Aluprof. Our issued "
     "proposal offers SMA Shopline as a 'similar approved alternative', and states that the Ug 1.0, "
     "g-value and acoustic requirements have been allowed 'for the glazing only' - glazing performance, "
     "not whole-system. That qualification sits in the prose of the DESCRIPTION & CLARIFICATIONS block, "
     "not in the EXCLUSIONS column, which is where a client's eye goes. Two fabricators refused the 1.0 "
     "U-value in writing (Mary, REQ-10). BCC is the employer and has to accept the substitution, so the "
     "answer already exists on their side. Better to have it in August than at award."),
    'jacob', source='analysis')

# the older Filwood row is the same job
crm.lead('filwood', 'jacob',
    why=("DUPLICATE of stepnell-bcc-filwood-broadway (AdminBase 8724), which is the row I am working. "
         "Same job: BCC, 4-16 Filwood Broadway, Bristol BS4 1JN. Left in place rather than deleted so a "
         "sync does not recreate it silently."),
    stage='quote_sent',
    next_action="Merge into stepnell-bcc-filwood-broadway. No separate chase.",
    next_action_date='2026-08-11')

# ---- 2. ST JAMES HOUSE: direction reversed. They owe us.
crm.lead('stepnell-st-james-house-mansfield-road-derby-derbyshire', 'jacob',
    why=("POSITION REVERSED by Mary 30/07. No quote went back against the 19/01/2026 ITT and that was "
         "the CORRECT answer, not a miss: Gintare found no window work in the pack (21/01), Jayk put "
         "that to Luke Walsh in writing on 23/01, and on 26/01 16:24 LUKE WALSH ANSWERED - 'The window "
         "alteration on the bill will require work. I have a bill item for windows to follow. The client "
         "is still assessing the best route for the windows you quoted for the front elevation. I will "
         "keep you up to date when this lands.' So the 04/02 deadline was answered, not missed, and the "
         "outstanding commitment is THEIRS. Last contact is 26/01/2026, not 05/12/2025 - 190 days today, "
         "not 250-301."),
    stage='follow_up',
    next_action=("Paul Taylor emails Luke Walsh (draft D-9): the windows bill item he promised is 190 "
                 "days overdue, and did the client ever choose a route for the front elevation. NOT "
                 "'did you get our quote' - that has failed twice and is the wrong question."),
    next_action_date='2026-08-06')

crm.note('lead', 'stepnell-st-james-house-mansfield-road-derby-derbyshire',
    ("DO NOT RE-ISSUE THE DECEMBER FIGURES. Validity was 30 days from 05/12/2025 and every supplier "
     "quote behind them (Vetroseal 058630/059869, A Plus QP65576, BSW 3525, 4Ali Q8177) is Nov/Dec 2025. "
     "Reviving St James House is a re-price, not a chase. Also: leads 7197 and 7198 are ONE quote with "
     "two options under a single cover letter - Option 1 Aluminium GBP 458,509.81 ex VAT, Option 2 "
     "Secondary Glazing GBP 212,647.11 ex VAT - and Stepnell pick one. Maximum exposure is 458,510 OR "
     "212,647, never the sum and never the board's 564,403. Both AdminBase rows hold the ex-VAT figure "
     "in the inc-VAT field, so the board shows both 20 percent low; verified as a two-row entry slip "
     "against eleven other sends, not a broken rule. And searching the bid ref SC0078B finds nothing - "
     "it exists only on the folder copy. Search the site name."),
    'jacob', source='analysis')

# ---- 3. DRAFTS
p = 'data/jacob/drafts.json'
d = json.load(open(p, encoding='utf-8'))

d8 = {
 "id": "D-8", "priority": 3,
 "why_now": ("Our Filwood quote went to Adam Warner on 30/07 and he acknowledged it inside three "
   "minutes, so nothing is being ignored and this is not a chase. It is worth an email in the second "
   "week of August for two reasons that have nothing to do with the price. First, the tender specified "
   "Aluprof and we have priced SMA Shopline as a similar approved alternative, with the U-value, g-value "
   "and acoustic figures allowed for the GLAZING ONLY - and that qualification is written into the "
   "clarifications prose, not the Exclusions column where a client actually looks. BCC is the employer; "
   "the substitution needs their acceptance, and Stepnell will know whether it is a problem. If it is, "
   "we want that in August, not at award. Second, the same Stepnell office won White Hall Residential "
   "from the same buyer on 11/06/2026 - GBP 6.97m, on site since 12/06/2026 to 17/12/2027 - so the "
   "window package there is being bought about now, and asking costs us one line in an email he is "
   "already expecting."),
 "job": "BCC, 4-16 Filwood Broadway, Bristol BS4 1JN - quotation issued 30/07/2026 (AdminBase 8724)",
 "client": "Stepnell Ltd (Bristol / Chandler's Ford office)",
 "to": "adam.warner@stepnell.co.uk", "to_name": "Adam Warner",
 "to_caveat": ("Adam Warner is the Bristol / Chandler's Ford senior estimator and Filwood is HIS. Do "
   "not copy Luke Walsh - Luke is Nottingham and St James House, a different office and a different "
   "conversation. AdminBase has luke.walsh@ stored against the Filwood row (8724); that is the CRM "
   "defaulting to the client's stored contact and it is wrong. Mobile 07482 812 707."),
 "cc": "", "send_as": "Paul Taylor",
 "not_before": "2026-08-11",
 "subject": "RE: BCC, 4-16 Filwood Broadway, BS4 1JN",
 "body": ("Adam,\n\nThanks for confirming receipt of our quotation on 30 July. Two things while it is "
   "with you.\n\nThe first is the one worth raising early. The tender information specified Aluprof, and "
   "we have priced SMA commercial thermally broken shopfront as a similar approved alternative. It is "
   "stated in the clarifications on our proposal, but I would rather flag it than have it found later. "
   "The thermal, solar and acoustic figures we have allowed are glazing performance. If BCC want the "
   "specified system, or want whole-system figures, tell me now and we will deal with it while there is "
   "still time rather than at award.\n\nThe second is separate. I saw you were appointed on White Hall "
   "Residential for Bristol City Council back in June. Congratulations - and who is buying the window "
   "and door package on it, and roughly when? We would like to be on the list. If it is not you, point "
   "me at whoever it is and I will not trouble you with it again.\n\n"),
 "evidence": ("Quote issued 30/07/2026 13:32 estimating@ -> adam.warner@stepnell.co.uk; his "
   "acknowledgement 30/07 13:35 (message AAMk...R6xPyAAA). Issued documents: 'Stepnell - BCC Filwood "
   "Broadway Pricing.xlsx' and 'Stepnell - BCC Filwood Broadway Proposal.pdf', both dated 30/07/2026, in "
   "Commercial\\1. Tender Documents\\Stepnell\\BCC Filwood Broadway\\1. Estimating\\3. Client Quote\\. "
   "The Aluprof-to-SMA substitution and the glazing-only performance wording are quoted verbatim from "
   "that proposal's DESCRIPTION & CLARIFICATIONS block. White Hall: Contracts Finder "
   "BRISTOLCC001-DN795589-02376229, awarded 11/06/2026, GBP 6,965,999.97, 12/06/2026 to 17/12/2027, 23 "
   "social-rent apartments."),
 "value": 85767.58,
 "value_source": ("The issued Pricing.xlsx dated 30/07/2026: subtotal GBP 85,767.58 ex VAT, plus "
   "optional external mastic GBP 605.05 and EPDM GBP 3,081.49. Gintare's number, not mine."),
 "must_not_say": ("No prices, no rates, no re-quoting - the figure is in the document he already holds "
   "and it is Gintare's. Do not raise St James House here: different office, different contact, and "
   "Mary's point stands that a BD chase must not ride on a live commercial thread. Do not congratulate "
   "him on White Hall as though we expect a favour for it - ask the procurement question plainly."),
 "status": "ready",
 "blocked_on": "JAC-1 - a human sends this. Hold until 11/08/2026 to give him eight working days with the quote.",
 "purpose": ("Surface the Aluprof-to-SMA substitution while it can still be fixed, and get onto the "
   "White Hall enquiry list before it is drawn up."),
 "approval": "Paul Taylor to read, change and send from commercial@ under his own name.",
}

d9 = {
 "id": "D-9", "priority": 2,
 "why_now": ("THE OVERDUE PROMISE IS THEIRS, AND IT IS 190 DAYS OLD. The board has said for months that "
   "we are waiting on Stepnell for an answer to our December quote. Mary read the estimating@ trail on "
   "30/07 and it is the other way round. Gintare found no window work in the January pack (21/01), Jayk "
   "put that to Luke Walsh in writing on 23/01, and Luke answered on 26/01: 'I have a bill item for "
   "windows to follow. The client is still assessing the best route for the windows you quoted for the "
   "front elevation. I will keep you up to date when this lands.' Nothing has landed. That makes this a "
   "call about their own commitment rather than a cold chase - a far better email - and one question "
   "closes all three AdminBase rows. Paul Taylor's last chase was 15/06 and got no reply in 50 days, so "
   "this is a second approach and must not repeat the first one's opening."),
 "job": "St James House, Mansfield Road, Derby DE1 3AD (AdminBase 6874, 7197, 7198)",
 "client": "Stepnell Ltd (Nottingham office)",
 "to": "luke.walsh@stepnell.co.uk", "to_name": "Luke Walsh",
 "to_caveat": ("Nottingham, 9 Regan Way, Chetwynd Business Park NG9 6RZ. Mobile 07467 489961, office "
   "0115 697 9200 - Jayk rang him on 21/01 with no pick-up, so email first. Nothing to do with Adam "
   "Warner or Filwood; keep the two apart."),
 "cc": "", "send_as": "Paul Taylor",
 "subject": "St James House, Derby - the windows bill item",
 "body": ("Luke,\n\nBack in January you told us the window alteration on the bill would require work, "
   "that a bill item for windows was to follow, and that the client was still assessing the best route "
   "for the windows we had quoted on the front elevation. We agreed to sit tight until it landed.\n\n"
   "Six months on, has it? Specifically:\n\n"
   " - did the client settle on a route for the front elevation, and which way did they go?\n"
   " - is there a windows bill item now, and is it still coming to us?\n"
   " - did the school fit-out on levels 1 to 3 go ahead as programmed?\n\n"
   "If it went elsewhere, or the window scope came out altogether, tell me straight and I will close it "
   "off our side. I would rather have that than keep it on a list.\n\nIf it is still live, our December "
   "pricing is long out of date and would need doing again, so the sooner we know the better.\n\nOne "
   "other thing while I have you: who is the employer on the building? We have never had that name, and "
   "on a scheme where the client is choosing the window route it is worth us knowing.\n\n"),
 "evidence": ("estimating@ trail, read by Mary 30/07/2026: 19/01 15:42 Jayk forwards the Stepnell ITT "
   "(form STP10, bid ref SC0078B, trade L_SC Aluminium Doors & Windows, return by 04/02/2026); 21/01 "
   "11:22 Gintare - 'BOQ refers to window redub and all the doors on the door schedule are internal'; "
   "21/01 11:38 Jayk calls Luke, no answer; 23/01 13:09 Jayk writes to Luke with the Trade Bill and "
   "Phase 1 Door Schedule attached; 26/01 16:24 Luke Walsh's reply, quoted above; 26/01 16:27 Jayk "
   "stands the team down. Prior chase: Paul Taylor to Luke, 15/06/2026, no reply. ITT brief: 'To "
   "refurbish level 1, 2, 3 to enable a new school provision within the building', main contract "
   "programme 02/03/2026 to 29/05/2026."),
 "value": None,
 "value_source": ("Deliberately blank. The open quotes are Option 1 Aluminium GBP 458,509.81 and Option "
   "2 Secondary Glazing GBP 212,647.11 ex VAT, both 05/12/2025 and both long expired, plus GBP 5,105.71 "
   "on lead 6874 of 08/10/2025. Reviving this is a re-price, so no live value belongs on it."),
 "must_not_say": ("Do NOT open with 'did you get our quote' or 'can we have a decision' - they answered "
   "us, we answered them, and the outstanding item is theirs. That framing has now failed twice. Do NOT "
   "re-issue or repeat the December figures: validity was 30 days and every supplier quote behind them "
   "is Nov/Dec 2025. No prices at all. Do not quote the bid ref SC0078B at him as though it identifies "
   "the job to us - it appears nowhere in our own mail."),
 "status": "ready",
 "blocked_on": "JAC-1 - a human sends this. Nothing else; it can go as soon as Paul is ready.",
 "purpose": ("Convert a 190-day silence into an answer by asking about Stepnell's own undertaking, and "
   "close or re-open all three Derby rows on one reply."),
 "approval": "Paul Taylor to read, change and send from commercial@ under his own name.",
}

d['drafts'] = [x for x in d['drafts'] if x.get('id') not in ('D-8', 'D-9')] + [d8, d9]
json.dump(d, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('drafts now:', [x.get('id') for x in d['drafts']])

# ---- 4. clear the work order
os.makedirs('test-results/jacob-inbox/processed', exist_ok=True)
shutil.move('test-results/jacob-inbox/queue/bot-43.json',
            'test-results/jacob-inbox/processed/bot-43.json')
print('bot-43 -> processed')

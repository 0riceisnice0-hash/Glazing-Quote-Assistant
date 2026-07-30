"""AdminBase - the commercial leads Adam exported on 28/07/2026.

Adam emailed jacob@ at 22:02 on 28/07 with a CSV of every commercial lead in
AdminBase that has been quoted, and said a live feed will follow. Until it
does, this reads the export and turns it into the chase list.

Why this file matters more than its size suggests. My board could only see two
things: mail in the last 180 days, and the seven quotes Mary read out of
estimating@'s sent items. This export sees 264 quoted leads going back to
May 2025 - including jobs nobody has touched since 2025 that are still sitting
in the CRM as live. Those were invisible to me yesterday.

Three things this script does that a plain CSV read would not:

1. **It halves nothing and it de-VATs everything.** AdminBase's VALUE column is
   inclusive of VAT. Every quote Fenster issues is exclusive of it. Seven rows
   here can be checked against a quote Mary read in the sent items, and all
   seven come out at exactly 1.200000. So the export's headline pipeline is 20%
   larger than the money actually quoted, and anyone comparing an AdminBase
   value against the Opportunity Log or against a PDF is out by a fifth. The
   ex-VAT figure is the one this board shows; the inc-VAT one is kept beside it
   so a human can see where it came from.

2. **It joins to the verified sends on the ex-VAT figure, not on the name.**
   Names in a CRM are typed by hand - BRADFORD WATTS and BRADFORD WATTS LTD are
   the same company in two spellings. A penny-exact value match to a quote we
   watched leave the building is a much harder join than a fuzzy name, and it is
   what tells us the CRM is behind: Princess Beatrice House still reads "quote
   being prepared" here and went out on the 27th.

3. **It refuses to average an outlier away, and it stops asking once a human
   has answered.** One Elkins row reads GBP 8.6m inc VAT for Brandon Estate.
   That is a hundred times Fenster's average won job and it moves the whole
   pipeline figure on its own, so it stays out of the medians. But "too big to
   average" and "probably a typo" are different claims, and this file used to
   make the second one. Adam answered it on 29/07/2026: *"the brandon estate
   job is not a mistake. That is a legit tender and should be treated as
   such."* Confirmed rows carry `confirmed` with who said so and when; they
   are still excluded from the medians, because the arithmetic reason has not
   changed, and they are no longer excluded from the chase list, because the
   doubt has gone. See CONFIRMED below.

Read-only. The CSV came out of the mailbox into test-results/ and is never
written back.
"""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "test-results", "jacob-mail",
                   "Live_Commercial_Leads28072026.csv")
HANDOVER = os.path.join(REPO, "data", "jacob", "handover.json")
OUT = os.path.join(REPO, "data", "jacob", "adminbase.json")

TODAY = "2026-07-28"

# AdminBase VALUE is inc VAT. Confirmed against seven quotes Mary read in
# estimating@'s sent items - Gordon Court, Ninn Lane, St Mary's, Princess
# Beatrice, Crestwood Park, the Chester Thomas arched door and Unit 1 Eleanor
# Trade Centre - each of which divides by exactly 1.200000.
VAT = 1.2

# A quote is worth chasing after a week of silence. Same threshold the handover
# board uses, so the two pages do not disagree about what "due" means.
CHASE_AFTER = 7

# Fenster's own PQQ puts its packages at GBP 20k-400k. Anything an order of
# magnitude past that is kept out of the medians, because one row at a hundred
# times the median is arithmetic noise wherever it came from.
OUTLIER_ABOVE = 1_000_000

# Rows a human has looked at and confirmed are real, keyed on the AdminBase
# lead number. This exists so a question only gets asked once. Being large is
# not being wrong, and the board should stop implying it is the moment
# somebody who knows says otherwise.
CONFIRMED = {
    "8324": "Adam Butcher, 29/07/2026: 'the brandon estate job is not a "
            "mistake. That is a legit tender and should be treated as such.'",
}

# Rows somebody has actually RESEARCHED, keyed on the lead number. The generated
# next action below is a good default and it is still a default: it assumes the
# client owes us an answer, because on 209 rows out of 209 that is all the CRM
# can tell you.
#
# It is wrong whenever the client is waiting on US, and it is wrong in the
# expensive direction - ringing a man to ask "what did you think of our price"
# when what he asked for in December was a completed PQQ. Lead 7384 is that row,
# and nothing in the CRM could have shown it: the fact lives in the repricing
# log the departed BDM left behind, and the reason for the silence lives in
# Birmingham's planning register.
#
# So a researched row can replace its own next action. `why` says where the
# override came from, because an override with no source is just a different
# guess.
WORKED = {
    "7384": {
        "next": "DO NOT chase Chris Mitchell for an answer - Fenster owes HIM. "
                "Jayk's repricing log, 19/12/2025: 'Chris at Cheil has asked "
                "us for PQQ's to be completed and for updated costs + "
                "schedule so now actually looking good.' The PQQ documents "
                "reached us on 18/12/2025 and a revised quote is dated "
                "22/12/2025; nothing in commercial@, info@ or jacob@ shows "
                "any of it going back, and jayk@ is a 404. FIRST: Adam or "
                "Mary confirms whether the PQQ pack and the revised costs "
                "left estimating@ (JAC-19). Then one call to 02476 466 877 "
                "delivering what he asked for - not asking how our price "
                "looked.",
        "why": "Researched 30/07/2026. Sources: repricing.json (Jayk's log, "
               "19/12/2025), the Cheil Construction tender folder on the "
               "Commercial drive, Companies House 04840215, Birmingham "
               "planning 2025/01426/PA and 2025/06383/PA. "
               "data/companies/chiel-construction.md.",
        "note": "The 218 days of silence are explained and they are not "
                "neglect on Chiel's side: condition 13 of the planning "
                "consent - THE INTERNAL DESIGN AND LAYOUT OF THE SPORTS HALL "
                "- was not approved until 26/02/2026. The glazing package "
                "could not be settled while it was outstanding.",
    },
    "5493": {
        "next": "DO NOT ask Sinden whether The Hub Alkerden is still live - "
                "they told us on 01/07/2026 that they have secured it, and "
                "asked US for an updated quotation for the Aluminium Curtain "
                "Walling & External Doors package BY 08/07/2026. Seyi "
                "Adesogan (07850 904372) asked us to confirm receipt; nothing "
                "in commercial@, info@ or jacob@ replied, and A Plus were "
                "still revising supplier quote QP65153 on 22/07. FIRST: Mary "
                "or Gintare confirms whether the updated quote has gone "
                "(asked 30/07, JAC-20). If it has, chase it against their own "
                "clock - provisional package order 08/10/2026, site "
                "11/02/2027. If it has not, it is an apology and a date, not "
                "a chase. Ask on the same call what became of the composite "
                "WINDOWS - their spec moved off aluminium in March and the "
                "July enquiry covers only curtain walling and doors.",
        "why": "Researched 30/07/2026. Sources: commercial@ (Corran Goodson "
               "23/03 and 30/03/2026, Seyi Adesogan 01/07 and 02/07/2026, "
               "Paul Taylor's forwards), info@ (composite supplier enquiries "
               "09/04/2026), Mary's intake of A Plus QP65153 22/07/2026, "
               "repricing.json (Jayk, 18/11/2025). "
               "data/companies/sinden-construction.md.",
        "note": "The 523 days are an artefact: the lead date is the January "
                "2025 enquiry and AdminBase has never re-dated it across two "
                "re-enquiries. The client is not silent - the open loop runs "
                "the other way. Harry Grover, who took this lead, left on "
                "31/10/2025 and Corran was still writing to him in March.",
        "state": "re-enquired - our price is the late one",
        "owner": "Adam",
    },
    "7745": {
        "next": "DO NOT chase Cold Ash. Emma O'Brien told estimating@ on "
                "26/06/2026 it was on hold, and West Berkshire's register "
                "says worse: application 25/01899/FULMAJ was REFUSED, "
                "decision issued 21/05/2026, with no appeal and no "
                "resubmission recorded as at 30/07/2026. Nothing moves until "
                "one of those appears. Re-check the register late November "
                "2026, when the usual six-month appeal window would be out. "
                "Adam replied to Emma on 27/06 saying he would update our "
                "notes - this row is that update.",
        "why": "Researched 30/07/2026. Sources: commercial@ (Emma O'Brien via "
               "Gintare 26/06/2026, Adam's reply 27/06), West Berkshire "
               "public access 25/01899/FULMAJ read from the council's own "
               "page. data/companies/sinden-construction.md.",
        "note": "PlanIt still had this application as Undecided/Awaiting "
                "decision because its copy was last scraped on 20/09/2025. "
                "The council's own page carried the refusal. Check "
                "last_scraped before believing a planning state.",
        "state": "blocked - planning refused 21/05/2026",
        "owner": "Jacob",
        # Read by jacob_daily_email: a blocked row is NAMED on the email
        # rather than chased, the same treatment Brandon Estate gets.
        "blocked": "planning refused 21/05/2026 - the client cannot answer "
                   "until they appeal or resubmit",
    },
    # ---------------------------------------------------------- Barnfield
    # Five leads, one company, THREE customer keys - so nothing on this board
    # has ever added them up. GBP 568,576 ex VAT, the largest single-client
    # exposure here, and 0 wins from 6 enquiries.
    # data/companies/barnfield-construction.md, researched 30/07/2026.
    "5625": {
        "next": "DO NOT chase Ian Brown for an answer on Bradstone Road - the "
                "answer was given on 01/05/2025 and we recorded it nowhere. "
                "Jayk to BSW, commercial@: 'Bradstone Road: LOST ON PRICE, you "
                "can close this enquiry.' ADAM'S DECISION, not mine: this row "
                "wants marking lost in AdminBase, and closing GBP 218,917 on "
                "my reading of one email is not my call. Two facts to weigh "
                "first. (1) We priced ~GBP 378k against three cheaper quotes "
                "at 275/255/249k, Ian invited us to value engineer, and the "
                "revision Harry circulated internally on 27/03/2025 sits at "
                "GBP 218,917 - THIRTY THOUSAND UNDER the cheapest quote we "
                "knew of. There is no send of it to Ian in commercial@, info@ "
                "or jacob@. (2) Vetroseal quoted us for BRADSTONE RD CHEETHAM "
                "on 29/01 and 02/02/2026, quote 060676, nine months after "
                "'lost' - and the number sequence dates it to 2026, so it is "
                "not an old quote re-sent. Mary has been asked what left "
                "estimating@ (30/07). Ian Brown 01282 442300 is worth a call "
                "on the other four jobs regardless.",
        "why": "Researched 30/07/2026. Sources: commercial@ (Ian Brown "
               "19/02/2025, Jayk 04/03 and 11/03/2025, Harry Grover "
               "27/03/2025, Jayk to Jack Pollard at BSW 01/05/2025, Vetroseal "
               "29/01 and 02/02/2026), repricing.json, outcomes.json, "
               "Companies House 02365913, Manchester planning 115485/FO/2017 "
               "and its condition discharges. "
               "data/companies/barnfield-construction.md.",
        "note": "The 497 days are not silence - they are an outcome nobody "
                "filed. Neither AdminBase nor the Opportunity Log records the "
                "loss; the only copy in the company is a reply to a glass "
                "supplier's courtesy email. The scheme itself is real and "
                "live: 3 x three-storey buildings, 19 units, permitted 2017, "
                "last planning condition discharged 11/02/2025 - eight days "
                "before Ian sent the enquiry.",
        "state": "lost on price 01/05/2025 - never recorded, Adam to confirm",
        "owner": "Adam",
    },
    "7665": {
        "next": "Establish whether our price actually went out BEFORE anyone "
                "chases The Grange Apartments. AdminBase says 'Live - Quoted' "
                "at GBP 155,388 ex VAT; the Opportunity Log has the same job "
                "with 'Quote Returned' EMPTY against Ian Brown's deadline of "
                "26/02/2026, and carrying a value in the CRM is not evidence "
                "of a send (Adam, hub-77: priced but never issued is Mary's, "
                "not a chase). Mary asked 30/07. If it went, this is the "
                "freshest Barnfield job and the natural reason to ring Ian "
                "Brown on 01282 442300 about all five.",
        "why": "Researched 30/07/2026. Sources: outcomes.json openThisYear "
               "(returned: null, chased: false), adminbase.json lead 7665. "
               "data/companies/barnfield-construction.md.",
        "note": "Caveat stated rather than hidden: the Opportunity Log's 2026 "
                "sheet is much thinner than 2025, so an empty cell there is "
                "weak evidence on its own. It is enough to check before "
                "ringing, not enough to conclude the quote never went.",
        "state": "quoted - or possibly never issued, unresolved",
        "owner": "Adam",
    },
    "6781": {
        "next": "Chase MSM Aerospace on the strength of a contract our client "
                "has WON - this is the strongest of the five Barnfield rows "
                "and it is not on Today at all, because AdminBase never gave "
                "it a next-action date. Jayk's log: 'Ben advised that it will "
                "likely be February before anything moves construction wise "
                "on this one. Worth repricing as secured', and a revised "
                "quote at GBP 37,827 was issued 12/01/2026 against the "
                "original GBP 46,968.75. February 2026 has been and gone. "
                "FIRST resolve who to ring: this lead is filed under "
                "hargreavescontracting.com (nkitchin@, 01204 365300) while "
                "its postcode BB9 5SP is Barnfield's own head office and "
                "Jayk's log calls it Barnfield's job. Establish whether "
                "Hargreaves is the contracting party, a group company or a "
                "CRM error before addressing anyone.",
        "why": "Researched 30/07/2026. Sources: repricing.json (Jayk, "
               "10/11/2025 and 12/01/2026), adminbase.json lead 6781, "
               "outcomes.json. data/companies/barnfield-construction.md.",
        "note": "'Secured' means Barnfield hold the main contract - step two "
                "of the whole job, already done, by a man who left. The "
                "enquiry list for the glazing is being drawn up or has been.",
        "state": "quoted - client has SECURED the main contract",
        "owner": "Adam",
    },
    "5991": {
        "next": "Do not ask Barnfield how our price looked on the Moston Cash "
                "& Carry - ask where the planning is. Jayk, 20/11/2025: "
                "'stuck at planning. Worth repricing as still open.' The "
                "GBP 68,800 on his log is the VAT-INCLUSIVE figure of this "
                "same lead (ex GBP 57,333.33) - penny exact, so it is one "
                "quote still open, not a re-quote. Covered by the one call to "
                "Ian Brown, 01282 442300.",
        "why": "Researched 30/07/2026. Sources: repricing.json (Jayk, "
               "19/05/2025 price submitted 29/05, chased 20/11/2025), "
               "adminbase.json lead 5991. "
               "data/companies/barnfield-construction.md.",
        "note": "Every fact here was written on or before 20/11/2025 and none "
                "of it has been re-checked with the client.",
        "state": "quoted - stuck at planning as at 20/11/2025",
        "owner": "Adam",
    },
    "6157": {
        "next": "Ask Barnfield for the RETENDER on St Johns, Blackburn - they "
                "offered it. Jayk, 20/11/2025: 'no movement - likely "
                "planning', and on the same row 'We have an opportunity to "
                "retender this anyway.' Quote no figure back at him: the log "
                "says GBP 58,343.68 and AdminBase says GBP 89,968.83 ex VAT "
                "on the same enquiry date of 19/06/2025, so one is a revision "
                "and I cannot tell which is current - that is Mary's to "
                "settle. Covered by the one call to Ian Brown, 01282 442300.",
        "why": "Researched 30/07/2026. Sources: repricing.json (Jayk, "
               "19/06/2025, chased 20/11/2025), adminbase.json lead 6157. "
               "data/companies/barnfield-construction.md.",
        "note": "NOT the 'St Johns' Jayk reported lost to BSW - that list is "
                "dated 30/04/2025 and this enquiry did not arrive until "
                "19/06/2025. Generic name, seven weeks apart, two different "
                "jobs; bd.md's single-word-name rule caught this one in the "
                "act. Barnfield's own group includes Barnfield Blackburn Ltd "
                "(11407219), so confirm the contracting entity.",
        "state": "quoted - stalled, client offered a retender",
        "owner": "Adam",
    },
    # ------------------------------------------- Churchdown and Aylesbury
    # Six rows, GBP 3,393,528 ex VAT, and every one of them is a CIF bid that
    # DID NOT GET FUNDED. Darren Trigg at GCS told Adam so on 29/07/2026 and
    # Adam put it on the hub the same day (message 40, answering JAC-9). I
    # wrote it into data/companies/glazing-consultancy-services.md and then
    # left the rows alone - so on 30/07 Adam's own chase list still had Mobius
    # Group and Southern Projects near the top of it, telling him to ring two
    # contractors for "a final answer" on a job whose funding failed. The
    # answer was already in the file. THAT is the failure this fixes: research
    # that does not land on the row changes nothing.
    #
    # Churchdown went out to FIVE main contractors, so one funding decision
    # kills five separate leads that share nothing but a postcode - GL3 2RB
    # on all five, at two price points GBP 17,500 apart.
    "7009": {
        "next": "DO NOT chase Aylesbury High School. Darren Trigg at Glazing "
                "Consultancy Services told Adam on 29/07/2026: 'both "
                "Aylesbury High School and Churchdown School Academy were CIF "
                "(condition improvement fund) bids and they were unsuccessful "
                "in securing funding, please keep all information to hand "
                "though as they are likely to resubmitted later this year.' "
                "The action is a DIARY DATE, not a chase: late September "
                "2026, before the autumn bid window, Adam or Jacob rings "
                "Darren on 01280 308188 and asks to be the glazing number "
                "inside the resubmission - on a CIF bid the price in the "
                "submission is usually the price that gets used. Keep the "
                "pricing to hand as he asked.",
        "why": "Adam's hub message 40, 29/07/2026, carrying Darren Trigg's "
               "own words in answer to JAC-9. "
               "data/companies/glazing-consultancy-services.md.",
        "note": "GCS is a glazing consultancy, not the payer and not the main "
                "contractor - their whole function is putting people on "
                "enquiry lists, which makes Darren worth more than this job. "
                "He volunteered 'we will be sure to contact you when we are "
                "working on any new projects'.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - there is no project to "
                   "chase until it is resubmitted and funded, and Darren "
                   "Trigg has undertaken to come back to us",
    },
    "7098": {
        "next": "DO NOT chase Churchdown School. Same CIF funding failure as "
                "Aylesbury (Darren Trigg via Adam, 29/07/2026) and this is "
                "the GCS copy of it. One diary date in late September covers "
                "both, and it is the same call: ask to be the glazing number "
                "in the resubmission.",
        "why": "Adam's hub message 40, 29/07/2026 (JAC-9). "
               "data/companies/glazing-consultancy-services.md.",
        "note": "Five contractors hold a Fenster price for this one school - "
                "GCS, Kemdoc, Mobius Group, Roof Estimating Services and "
                "Southern Projects. The information is worth keeping for that "
                "reason alone: whoever ends up building it, we are already in.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - no project until it is "
                   "resubmitted and funded",
    },
    "7139": {
        "next": "DO NOT chase Mark Kemery at Kemdoc about Churchdown School. "
                "The CIF funding bid behind it failed (Darren Trigg at GCS "
                "via Adam, 29/07/2026) - Kemdoc were bidding the main "
                "contract, so there is nothing for them to answer and asking "
                "tells them we do not know. The whole scheme sits on one "
                "diary date with Darren in late September.",
        "why": "Adam's hub message 40, 29/07/2026 (JAC-9). "
               "data/companies/glazing-consultancy-services.md.",
        "note": "GBP 746,616.85 here and on Mobius Group; GBP 729,116.85 on "
                "GCS, Roof Estimating Services and Southern Projects. Two "
                "price points, GBP 17,500 apart, one package.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - no project until it is "
                   "resubmitted and funded",
    },
    "7159": {
        "next": "DO NOT chase Chris Shaw at Mobius Group about Churchdown "
                "School - this row was NEAR THE TOP of Adam's chase list on "
                "30/07 at GBP 746,617 and the answer had been on file since "
                "29/07. The CIF funding bid failed (Darren Trigg at GCS via "
                "Adam). One diary date with Darren, late September 2026.",
        "why": "Adam's hub message 40, 29/07/2026 (JAC-9). "
               "data/companies/glazing-consultancy-services.md.",
        "note": "The biggest single row this correction removes from the "
                "chase list, and the reason the correction was worth a "
                "session: a Commercial Director ringing a contractor about a "
                "GBP 746k job that has no funding is worse than not ringing.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - no project until it is "
                   "resubmitted and funded",
    },
    "7267": {
        "next": "DO NOT chase Roof Estimating Services about Churchdown "
                "School Academy. CIF funding bid unsuccessful (Darren Trigg "
                "at GCS via Adam, 29/07/2026). Diary date with Darren, late "
                "September 2026.",
        "why": "Adam's hub message 40, 29/07/2026 (JAC-9). "
               "data/companies/glazing-consultancy-services.md.",
        "note": "jobs@roofestimatingservices.com is a generic estimating "
                "mailbox with no named person on the row - worth noting if "
                "anyone does eventually need an answer out of them.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - no project until it is "
                   "resubmitted and funded",
    },
    "7268": {
        "next": "DO NOT chase James at Southern Projects about Churchdown "
                "School Academy - the other row that was high on Adam's chase "
                "list on 30/07, at GBP 729,117. CIF funding bid unsuccessful "
                "(Darren Trigg at GCS via Adam, 29/07/2026). Diary date with "
                "Darren, late September 2026.",
        "why": "Adam's hub message 40, 29/07/2026 (JAC-9). "
               "data/companies/glazing-consultancy-services.md.",
        "note": "Southern Projects are in Waterlooville and the school is in "
                "Gloucester - a reminder that the postcode on these rows is "
                "the SITE, not the contractor, so a 'region' read off "
                "AdminBase is the job's region and not the client's.",
        "state": "blocked - CIF funding bid unsuccessful, resubmission likely",
        "owner": "Jacob",
        "blocked": "the CIF bid was unsuccessful - no project until it is "
                   "resubmitted and funded",
    },
    # ---------------------------------------------------- Alexander James
    # SIX live-quoted rows, GBP 1,910,810 ex VAT, one client, three named
    # contacts - the largest single-client exposure on this board and nobody
    # had opened it. Two of the six already have an answer sitting in
    # commercial@, put there by PAUL TAYLOR, who chased both himself: one is
    # LOST and one is PREFERRED BIDDER with a callback we promised and which
    # runs out tomorrow. data/companies/alexander-james.md, 30/07/2026.
    "7285": {
        "next": "DO NOT chase Brooklands - IT IS LOST and the client told us "
                "so on 07/05/2026. Kieran Santry to Paul Taylor, commercial@: "
                "'Unfortunately we didn't secure this project. Many thanks "
                "for your quotation.' Alexander James did not win the main "
                "contract, so there is no glazing package. ADAM'S DECISION: "
                "this row wants marking lost in AdminBase - not lost on "
                "price, lost because our client lost. Nothing here reflects "
                "on our number and no lesson should be read into it.",
        "why": "Researched 30/07/2026. Source: commercial@, thread 'Alexander "
               "James - Brooklands College', Paul Taylor out 07/05/2026, "
               "Kieran Santry's reply the same day. "
               "data/companies/alexander-james.md.",
        "note": "Paul opened that chase with 'I believe you were previously "
                "speaking with my colleague Jayk' - so the handover of Jayk's "
                "book to Paul has been happening quietly since at least May, "
                "on a client nobody has counted. Kieran also answered inside "
                "a day, twice. This is a responsive client, not a silent one.",
        "state": "LOST 07/05/2026 - our client did not win the main contract",
        "owner": "Adam",
    },
    "7388": {
        "next": "RING KIERAN SANTRY THIS WEEK - 07512899774 or 0208 961 5555. "
                "Tiverton Road, 17 flats, GBP 547,886 ex VAT and the largest "
                "unworked row on this board. On 05/06/2026 he told Paul "
                "Taylor: 'We are the preferred bidder but still waiting for "
                "the council to give us a start date. Come back to me in 6-8 "
                "weeks and we should know more.' Paul answered 'Perfect, I'll "
                "be in touch then.' Six to eight weeks from 05/06 is 17/07 to "
                "31/07/2026 - THE WINDOW CLOSES TOMORROW and the callback is "
                "ours, not his. Ask three things: has the council issued a "
                "start date, is the windows-and-doors package still ours to "
                "price, and does the programme need our price refreshing. Do "
                "NOT ask whether the project is still live - he has already "
                "answered that.",
        "why": "Researched 30/07/2026. Source: commercial@, thread 'Fenster "
               "Glazing Quote Ref: Tiverton Road', Paul Taylor out 05/06/2026 "
               "14:10, Kieran Santry's reply the same day, Paul's "
               "acknowledgement the same day. data/companies/alexander-james.md.",
        "note": "PREFERRED BIDDER is step two of the whole job done for us - "
                "our client is in front on a council contract and we are "
                "already priced. AdminBase gave this row NO follow-up date at "
                "all, which is why it appeared on nothing: it was one of 80 "
                "undated rows worth GBP 7.0m that the daily email dropped in "
                "silence until 30/07. Site postcode N15 6RP is Haringey; I "
                "could not find the scheme on the planning register from the "
                "address alone, so which council contract this is remains "
                "unconfirmed - Kieran's answer settles it in one sentence.",
        "state": "PREFERRED BIDDER - our promised 6-8 week callback is due now",
        "owner": "Paul Taylor",
    },
    "7391": {
        "next": "ARCHWAY ROAD IS THE ONE NOBODY HAS EVER TOUCHED - GBP 467,662 "
                "ex VAT, quoted 23/12/2025, 219 days, no chase from anyone and "
                "no supplier quote behind it that I can find. Ring DAN on "
                "07971 460997: is it still live, who has the main contract, "
                "and where did our number land. He also holds Emmbrook School "
                "and Darrick Wood, so cover all three in the one call - but "
                "Darrick Wood is NOT a chase, it is a revision the client is "
                "waiting on, so read that row before dialling. Then ask what "
                "else is coming: this client has sent seven enquiries in a "
                "year and we have won none of them.",
        "why": "Researched 30/07/2026. Sources: adminbase.json leads 7391, "
               "8221, 8368 (all dan@alexanderjamesltd.co.uk); commercial@ "
               "searched for the domain - no chase to Dan exists in "
               "commercial@, info@ or jacob@. "
               "data/companies/alexander-james.md.",
        "note": "The job name is recorded as 'Archway RoadArchway Road' - an "
                "AdminBase double-paste, one job not two. Highest-value row "
                "of the three and the oldest, and the only one of the six "
                "with no supplier quote I can see behind it.",
        "state": "quoted - never chased, and Dan holds three of the six",
        "owner": "Adam",
    },
    "8221": {
        "next": "Covered by the one call to Dan on 07971 460997 - do not ring "
                "him three times. Emmbrook School, GBP 84,005 ex VAT. Our "
                "price went to the client on 08/05/2026 THROUGH THE ESTIMATEONE "
                "PORTAL (Mary, 29/07, from estimating@'s sent items) - so the "
                "silence is 83 days from the send, not 93 from the CRM's lead "
                "date, and any reply may be sitting in a portal nobody logs "
                "into rather than in a mailbox. A Plus quoted us GBP 41,883 "
                "for it on 29/04/2026 (QT50628) and Daniel Charlesworth is "
                "still waiting on feedback, so one answer from Dan closes two "
                "loops.",
        "why": "Researched 30/07/2026. Sources: Mary's reading of estimating@ "
               "sent items (bot message 9, 29/07); adminbase.json lead 8221; A "
               "Plus Aluminium's quote list of 16/07/2026, forwarded to jacob@ "
               "by Adam on 28/07 ('please provide an update for Dan' - that "
               "Dan is Daniel Charlesworth at A Plus, a different Dan). "
               "data/companies/alexander-james.md.",
        "note": "Two people called Dan sit on this one job - Dan at Alexander "
                "James who owes us an answer, and Dan at A Plus who is owed "
                "one by us. Do not merge them. And this client runs enquiries "
                "through portals (EstimateOne here, their own AJ Group portal "
                "on Darrick Wood), which is the shape that hid a GBP 174,546 "
                "E T & S tender for a fortnight: a portal client's traffic is "
                "on our OUTBOUND only.",
        "state": "quoted via a portal 08/05/2026 - 83 days, no reply",
        "owner": "Adam",
    },
    "8368": {
        "next": "DARRICK WOOD IS NOT SILENT AND IT MAY BE WAITING ON US. "
                "Submitted through AJ Group's portal 04/06/2026; GLEB SALIEV "
                "reviewed it and came back on 09/07: 'I have now completed my "
                "review of your quotation and, unfortunately, the quantities "
                "and dimensions included are incorrect and do not comply.' "
                "ADAM replied on 10/07 that we would revise. A Plus were asked "
                "on 17/07 and Dominic Palethorpe returned QT50911 Rev1 on "
                "24/07. Nothing on my side of the wall shows the revised "
                "quotation going back to the client. FIRST: Mary or Gintare "
                "confirms whether it has left (asked 30/07). If it has not, "
                "this is a GBP 255,082 package where the client has told us "
                "our take-off is wrong and is waiting - and it is the fourth "
                "job this week whose price may have stopped inside Fenster.",
        "why": "Researched 30/07/2026. Sources: Mary's reading of estimating@ "
               "and the AJ Group portal thread (bot message 9, 29/07); the "
               "ledger's mail_received record of A Plus QT50911 Rev1, "
               "24/07/2026 14:07; adminbase.json lead 8368. "
               "data/companies/alexander-james.md.",
        "note": "This is the one Alexander James row where the client is "
                "engaged and the ball is ours, so it must not be lumped in "
                "with the three that are simply silent. It also says something "
                "about the quote rather than the relationship: our quantities "
                "and dimensions were rejected as non-compliant on a GBP 255k "
                "package. That is Mary's to weigh, not mine.",
        "state": "client rejected our quantities 09/07 - revision may be ours",
        "owner": "Adam",
    },
    "7282": {
        "next": "Weymouth Court, GBP 238,288 ex VAT, quoted 05/12/2025 and "
                "silent 237 days - the one Alexander James row belonging to "
                "GLEB (gleb@alexanderjamesltd.co.uk). Add it to the call to "
                "Kieran rather than ringing a third contact cold: same "
                "company, same six-enquiry relationship, and the number on "
                "this row (0298 9615555) is a mistyped 0208 961 5555. Site is "
                "W1W 6DA, Fitzrovia.",
        "why": "Researched 30/07/2026. Sources: adminbase.json lead 7282; "
               "commercial@ and info@ searched on the domain - nothing with "
               "Gleb on my side of the wall. data/companies/alexander-james.md.",
        "note": "Six live rows across three contacts is how a GBP 1.9m client "
                "stays invisible: no single person at Fenster was talking to "
                "all of it. And Gleb is GLEB SALIEV, who is anything but a "
                "stranger - he is the man who reviewed our Darrick Wood "
                "quotation on 09/07/2026 and rejected the quantities. This ROW "
                "has never been chased; this CONTACT is live. Do not read my "
                "empty mailbox search as a quiet client.",
        "state": "quoted - never chased, 237 days",
        "owner": "Adam",
    },
}

# Win rate by value, from 224 priced decided rows in the Opportunity Log.
#
# READ THE EDGES. This is the 2025-26 BD funnel, not Fenster's win history
# (Zac and Adam, 29/07/2026). Eight years of trading sit outside it, including
# Headrow Court for Fortis Vision at roughly GBP 630k + VAT, which is Adam's
# own largest job and appears on no row below. So these notes say what the log
# says - "no win this size on the log" - and never "Fenster cannot win this".
#
# It is carried on every row here because this list is ranked by value, and
# ranking by value points straight at the half of the recent funnel that does
# not convert. The ranking is Adam's call to change; showing him what each row
# is worth converting is not.
BANDS = [
    (10_000, "under GBP 10k", 38, "the band the recent funnel converts best"),
    (50_000, "GBP 10k-50k", 13, "wins occasionally - 7 of 52 on the log"),
    (200_000, "GBP 50k-200k", 0, "no win this size on the BD log - 0 of 37"),
    (None, "over GBP 200k", 0, "no win this size on the BD log - 0 of 15"),
]


def band_for(value):
    if not value:
        return None
    for ceiling, label, rate, note in BANDS:
        if ceiling is None or value < ceiling:
            return {"band": label, "winRate": rate, "note": note}
    return None


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except ValueError:
        return None


def parse_date_iso(s):
    """The handover file writes ISO dates; the CRM export writes dd/mm/yyyy.
    Two formats, two parsers, no guessing which one a string is."""
    try:
        return date.fromisoformat((s or "").strip())
    except ValueError:
        return None


def parse_money(s):
    s = (s or "").replace("£", "").replace(",", "").strip()
    if not s or s == "-":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean(s):
    return re.sub(r"\s+", " ", (s or "").replace("\t", " ")).strip()


def canon(name):
    """Company key of last resort - the name with its suffix stripped.

    Only used where there is no email address to key on. It merges BRADFORD
    WATTS with BRADFORD WATTS LTD, which is one company typed twice, and it
    does not attempt anything cleverer: guessing that two firms are one from a
    shared word is the mistake that made "Atlas" a window cleaner.
    """
    n = clean(name).upper()
    n = re.sub(r"[.,]", " ", n)
    n = re.sub(r"\b(LTD|LIMITED|PLC|LLP)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def client_key(name, email):
    """Key on the email domain where there is one, on the name where there
    is not.

    The domain settles cases the name cannot. SINDEN CONSTRUCTION LTD and
    THOMAS SINDEN read as two companies and both write from thomas-sinden.co.uk;
    ALEXANDER JAMES and ALEXANDER JAMES CONTRACTS both from alexanderjamesltd.
    Merging those on the shared word would be a guess. Merging them on the
    domain is evidence.
    """
    dom = (email or "").split("@")[-1].strip().lower()
    if dom and "." in dom:
        return dom
    return canon(name)


def title_case(name):
    n = clean(name)
    if n.isupper():
        return " ".join(w.capitalize() if len(w) > 2 or w.isalpha() else w
                        for w in n.split())
    return n


def state_for(result, days, has_value):
    """Every row gets a state, because a row without one is not finished.

    The distinction that matters is priced-vs-being-priced: a quote being
    prepared is Mary's and chasing the client about it would be chasing them
    about our own homework.
    """
    r = (result or "").lower()
    if "being prepared" in r:
        return "being priced", "Mary"
    if "appointment" in r:
        return "appointment", "Adam"
    if not r:
        return "no result recorded", "Jacob"
    if days is None:
        return "quoted - no date", "Jacob"
    if days < CHASE_AFTER:
        return "quoted - recent", "-"
    if days > 365:
        return "quoted - a year silent", "Jacob"
    return "quoted - chase due", "Adam"


def next_for(state, client, job, value, days, matched, lead_no=None):
    """The next action on a chaseable row - JAC-14, answered by ADAM 29/07/2026.

    (It went on the record as Zac: the hub sign-in defaulted to him and Adam
    corrected that in hub-66. It matters on this page more than anywhere - the
    person refusing to let 209 of his live quotes be closed on my arithmetic is
    the Commercial Director whose backlog it is, not the operator.)

    I had asked for a rule that CLOSES this backlog: 146 of these are over 400
    days silent and GBP 17.9m of it reads as open because nothing at Fenster
    ever closes a row. The answer was the other way round - *"They all need
    chasing up, and a final word from the client which is also a good
    opportunity to get any feedback and tout more opportunities. Treat all as
    live until updated."*

    So no row is closed on silence and none is closed on my arithmetic. What
    changes is that every one of them now carries the same three-part ask
    rather than an empty cell: the final answer, the feedback on our price, and
    what else they have coming. That last part is why this is worth doing at
    all - a call that only asks "did we get it" spends a relationship and
    brings back one bit of information.
    """
    # A researched row wins over the generated ask, and it wins even when the
    # row is not in a "quoted" state - the whole point of the override is that
    # somebody has read more than this file can see.
    if lead_no and lead_no in WORKED:
        return WORKED[lead_no]["next"]
    if not state.startswith("quoted"):
        return ""
    # A row that joins penny-exact to a verified send is already on the
    # register with a next action somebody reasoned about, and two of the four
    # say DO NOT CHASE - Brandon Estate, where Chris Conlon has undertaken to
    # tell us and Adam has already replied, and Gordon Court, where Chigwell
    # physically cannot answer before jLiving decides on 16 September. A blanket
    # "chase them all" rule that overwrites those is how a relationship gets
    # spent on a call the client has already answered. The register wins.
    if matched:
        return ""
    silence = ("%d days silent" % days if days is not None
               else "no date on the row at all")
    money = "GBP %s ex VAT" % format(int(round(value)), ",") if value else \
            "no value on the row"
    return ("Chase %s for a final answer on %s - %s, %s. Three things back, "
            "not one: is it still live or did it go elsewhere and to whom; "
            "how our price looked; and what else they have coming. "
            "Adam, 29/07 (JAC-14): every row here stays live until the client "
            "updates it - nothing is closed on silence."
            % (client, job or "this job", money, silence))


def build():
    with open(SRC, encoding="utf-8-sig") as fh:
        raw = list(csv.DictReader(fh))

    today = date.fromisoformat(TODAY)
    hand = {}
    if os.path.exists(HANDOVER):
        h = json.load(open(HANDOVER, encoding="utf-8"))
        for r in h.get("issued", []) + h.get("held", []):
            if r.get("value"):
                hand[round(r["value"], 2)] = r

    rows = []
    for r in raw:
        inc = parse_money(r.get(" VALUE "))
        ex = round(inc / VAT, 2) if inc else None
        lead = parse_date(r.get("LEADDATE"))
        nxt = parse_date(r.get("NEXTACTIONDATE"))
        # Age is measured from whichever date the CRM last committed to. If
        # somebody set a follow-up date, silence is measured from there; if
        # nobody did, it is measured from the day the lead was raised.
        anchor = nxt or lead
        days = (today - anchor).days if anchor else None
        result = clean(r.get("RESULT"))
        state, owner = state_for(result, days, bool(inc))

        matched = hand.get(ex) if ex else None

        # THE RE-QUOTE TRAP (Mary, 29/07/2026, on lead 8155). When a job is
        # priced a second time, AdminBase updates the VALUE and leaves the
        # dates alone. Lead 8155 carries April's lead date, April's next
        # action and April's lead number with July's money on it - so the row
        # read "chase due, 98 days" on a quote that had gone out the previous
        # afternoon. Chasing a client the day after we priced them is worse
        # than not chasing at all, which is exactly the mistake the Filwood
        # correction was about.
        #
        # It is detectable: if the value joins penny-exact to a send we
        # watched leave the building, and that send is newer than the date
        # this row is aged from, then the row's clock is wrong and the send's
        # date is the true one. Age from the send, and say the row was
        # re-dated so nobody has to wonder why it disagrees with the CRM.
        stale = None
        if matched and matched.get("issued") and anchor:
            issued = parse_date_iso(matched["issued"])
            if issued and issued > anchor:
                # Five rows come out of this and only one is a re-quote. The
                # rest are the ordinary lag between the CRM's follow-up date
                # and the day the quote actually went. Both are worth
                # re-dating and they are not the same fault, so the row says
                # which rather than accusing every one of being 8155.
                gap = (issued - anchor).days
                stale = {"crmDate": anchor.isoformat(),
                         "issued": matched["issued"],
                         "crmDays": days,
                         "reQuote": gap > 45,
                         "why": ("Aged from the send, not the CRM. The row is "
                                 "dated %s and the quote left the building on "
                                 "%s - %d days later. %s"
                                 % (anchor.isoformat(), matched["issued"], gap,
                                    "That gap is a re-quote: AdminBase updates "
                                    "the value and leaves the dates, so the row "
                                    "is the old enquiry wearing the new price."
                                    if gap > 45 else
                                    "Ordinary lag between the follow-up date "
                                    "somebody set and the day it went."))}
                days = (today - issued).days
                state, owner = state_for(result, days, bool(inc))

        # A researched row may also have the wrong STATE, not just the wrong
        # next action. Lead 7745 read "quoted - chase due, owner Adam" on a
        # scheme whose planning application had been refused two months
        # earlier - so the row told Adam to chase and then told him not to, in
        # the same breath. If an override says what the row is, it says it in
        # both fields or it is only half an override.
        w = WORKED.get(clean(r.get("LEADNUMBER")))
        if w and w.get("state"):
            state, owner = w["state"], w.get("owner", owner)

        job = clean(r.get("OFFICEREF")) or clean(r.get("SITEADDRESS"))
        email = clean(r.get("EMAIL")).rstrip(">")
        # One row carries the postcode welded onto the address with no space.
        email = re.sub(r"\.co\.uk[A-Z0-9 ]+$", ".co.uk", email)
        email = email if "@" in email else ""

        rows.append({
            "lead": clean(r.get("LEADNUMBER")),
            "client": title_case(r.get("LEADNAME")),
            "key": client_key(r.get("LEADNAME"), email),
            "job": job,
            "leadDate": lead.isoformat() if lead else None,
            "nextAction": nxt.isoformat() if nxt else None,
            "days": days,
            "incVat": inc,
            "value": ex,
            "result": result,
            "state": state,
            "owner": owner,
            # JAC-14. Every chaseable row carries the ask; a human's edit on
            # the board still wins over it.
            "next": next_for(state, title_case(r.get("LEADNAME")), job, ex,
                             days, matched, clean(r.get("LEADNUMBER"))),
            "worked": WORKED.get(clean(r.get("LEADNUMBER"))),
            "email": email,
            "phone": (clean(r.get("WORKTELEPHONE")) or clean(r.get("MOBILE"))
                      or clean(r.get("HOMETELEPHONE"))),
            "product": clean(r.get("PRODUCTTYPE")),
            "town": title_case(r.get("TOWN")),
            "postcode": clean(r.get("SITEPOSTCODE")) or clean(r.get("POSTCODE")),
            "source": clean(r.get("LEADSOURCE")),
            "takenBy": clean(r.get("TAKENBY")),
            "fit": band_for(ex),
            "outlier": bool(inc and inc >= OUTLIER_ABOVE),
            "confirmed": CONFIRMED.get(clean(r.get("LEADNUMBER"))),
            "staleDate": stale,
            "onBoard": matched["key"] if matched else None,
            "boardState": matched["state"] if matched else None,
        })

    # Where the CRM and the sent items disagree, the sent items win - they are
    # the message that actually left the building.
    conflicts = []
    for r in rows:
        if not r["onBoard"]:
            continue
        if r["state"] == "being priced" and r["boardState"] in (
                "live", "quoted", "waiting", "gone quiet"):
            conflicts.append({
                "job": r["job"], "client": r["client"], "value": r["value"],
                "crm": r["result"], "truth": r["boardState"],
                "why": ("AdminBase has this as still being priced. The quote is "
                        "in estimating@'s sent items, so it has gone."),
            })

    # One scheme, several bidders. Fenster is a subcontractor, so the same job
    # reaches it once per main contractor on the list - Churchdown School was
    # priced for five of them. Five rows, one job, and a pipeline total that
    # counts the money five times.
    #
    # These are found on the penny-exact ex-VAT figure across different
    # companies, not on the site name: the same estimate sent to five bidders
    # carries the same number, while the site was typed five different ways
    # ("Churchdown School" and "CHURCHDOWN SCHOOL ACADEMY WINSTON ROAD
    # GLOUESTER"). The floor exists because ten unrelated rows share a GBP 208
    # placeholder, which is a default in the CRM and not a scheme.
    SCHEME_FLOOR = 1000
    by_value = defaultdict(list)
    for r in rows:
        if r["value"] and r["value"] >= SCHEME_FLOOR:
            by_value[r["value"]].append(r)

    schemes = []
    for v, rs in by_value.items():
        if len({r["key"] for r in rs}) < 2:
            continue
        for r in rs:
            r["scheme"] = v
        schemes.append({
            "value": v,
            "job": max((r["job"] for r in rs), key=len),
            "bidders": [{"client": r["client"], "email": r["email"],
                         "job": r["job"], "days": r["days"],
                         "state": r["state"]} for r in rs],
            "count": len(rs),
            "counted": round(v * (len(rs) - 1), 2),
        })
    schemes.sort(key=lambda s: -s["counted"])

    # A scheme can appear here twice, because it was priced at two different
    # figures for different bidders - Churchdown went to two of them at one
    # number and three at another. Those two rows are one job and the page has
    # to say so, or it reads as two schools.
    #
    # Linked on one job name being a word-for-word prefix of the other, which
    # holds for "Churchdown School" inside "CHURCHDOWN SCHOOL ACADEMY WINSTON
    # ROAD ..." and correctly does not fire on Newport Pagnell Baptist Church
    # against Newport Pagnell Library.
    def words(s):
        return re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper()).split()

    for a in schemes:
        aw = words(a["job"])
        for b in schemes:
            if a is b:
                continue
            bw = words(b["job"])
            n = min(len(aw), len(bw))
            if n >= 2 and aw[:n] == bw[:n]:
                a.setdefault("alsoPricedAt", []).append(b["value"])

    by_client = defaultdict(list)
    for r in rows:
        by_client[r["key"]].append(r)

    clients = []
    for key, rs in by_client.items():
        live = [r for r in rs if r["state"].startswith("quoted")]
        clients.append({
            "key": key,
            "client": rs[0]["client"],
            "rows": len(rs),
            "quoted": len(live),
            "value": round(sum(r["value"] or 0 for r in live
                               if not r["outlier"]), 2),
            "outlierValue": round(sum(r["value"] or 0 for r in live
                                      if r["outlier"]), 2),
            "oldest": max([r["days"] for r in rs if r["days"] is not None]
                          or [0]),
            "email": next((r["email"] for r in sorted(
                rs, key=lambda x: x["leadDate"] or "", reverse=True)
                if r["email"]), ""),
            "phone": next((r["phone"] for r in rs if r["phone"]), ""),
            "onBoard": any(r["onBoard"] for r in rs),
        })
    clients.sort(key=lambda c: -c["value"])

    # A WORKED row keeps its place here whatever state the override gave it.
    # This list is filtered on three literal state strings, so the moment an
    # override wrote a truer state onto a row - "re-enquired - our price is the
    # late one" - the row fell out of the chase list and off the daily email
    # entirely. Researching the most urgent row on the board is not a reason to
    # hide it. Blocked ones are labelled by jacob_daily_email, not dropped.
    due = [r for r in rows
           if r["state"] in ("quoted - chase due", "quoted - a year silent",
                             "quoted - no date")
           or r.get("worked")]
    due.sort(key=lambda r: -(r["value"] or 0))
    vals = sorted(r["value"] for r in rows if r["value"] and not r["outlier"])

    return {
        "source": {
            "file": os.path.basename(SRC),
            "from": "Adam Butcher <adam@fensterglazing.com>",
            "to": "jacob@fensterglazing.com, marketing@fensterglazing.com",
            "subject": "Live Commercial Leads - Current",
            "received": "2026-07-28T22:02",
            "system": "AdminBase (Abinitio Software)",
            "note": ("A one-off export. Adam is working on a live feed. Until "
                     "that exists this board is as fresh as the last CSV."),
        },
        "vat": {
            "finding": ("AdminBase VALUE is inclusive of VAT; every quote "
                        "Fenster issues is exclusive of it."),
            "evidence": ("Seven rows here have a matching quote in "
                         "estimating@'s sent items. All seven divide by "
                         "exactly 1.200000."),
            "consequence": ("The export's headline pipeline is 20% larger than "
                            "the money actually quoted. This board shows ex "
                            "VAT throughout and keeps the inc-VAT figure "
                            "beside it."),
        },
        "updated": TODAY,
        "rows": rows,
        "clients": clients,
        "due": due,
        "conflicts": conflicts,
        "schemes": schemes,
        "totals": {
            "rows": len(rows),
            "clients": len(clients),
            "value": round(sum(r["value"] or 0 for r in rows
                               if not r["outlier"]), 2),
            "incVat": round(sum(r["incVat"] or 0 for r in rows
                                if not r["outlier"]), 2),
            "due": len(due),
            "dueValue": round(sum(r["value"] or 0 for r in due
                                  if not r["outlier"]), 2),
            "beingPriced": sum(1 for r in rows if r["state"] == "being priced"),
            "yearSilent": sum(1 for r in rows
                              if r["state"] == "quoted - a year silent"),
            "noDate": sum(1 for r in rows if r["nextAction"] is None),
            "overdue": sum(1 for r in rows if r["nextAction"]
                           and r["nextAction"] < TODAY),
            "future": sum(1 for r in rows if r["nextAction"]
                          and r["nextAction"] >= TODAY),
            "noEmail": sum(1 for r in rows if not r["email"]),
            "outliers": sum(1 for r in rows if r["outlier"]),
            "outlierValue": round(sum(r["value"] or 0 for r in rows
                                      if r["outlier"]), 2),
            "confirmed": sum(1 for r in rows if r.get("confirmed")),
            "staleDates": sum(1 for r in rows if r.get("staleDate")),
            "median": vals[len(vals) // 2] if vals else 0,
            "onBoard": sum(1 for r in rows if r["onBoard"]),
            "conflicts": len(conflicts),
            "schemes": len(schemes),
            "schemeRows": sum(s["count"] for s in schemes),
            "doubleCounted": round(sum(s["counted"] for s in schemes), 2),
            # How much of the chase list is in the band Fenster actually
            # converts. This is the number that decides whether working down
            # the list by value is worth anyone's afternoon.
            "winnable": sum(1 for r in due
                            if (r.get("fit") or {}).get("winRate", 0) >= 13),
            "winnableValue": round(sum(
                r["value"] or 0 for r in due
                if (r.get("fit") or {}).get("winRate", 0) >= 13), 2),
            "neverWonBand": sum(1 for r in due
                                if (r.get("fit") or {}).get("winRate") == 0),
        },
    }


def main():
    data = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
    t = data["totals"]
    print("adminbase.json written")
    print("  %d rows, %d clients, GBP %s ex VAT (GBP %s inc)"
          % (t["rows"], t["clients"], format(int(t["value"]), ","),
             format(int(t["incVat"]), ",")))
    print("  %d chaseable (GBP %s), %d being priced, %d silent over a year"
          % (t["due"], format(int(t["dueValue"]), ","), t["beingPriced"],
             t["yearSilent"]))
    print("  follow-up dates: %d in the past, %d in the future, %d never set"
          % (t["overdue"], t["future"], t["noDate"]))
    print("  %d rows join to a verified send; %d of those disagree with it"
          % (t["onBoard"], t["conflicts"]))
    print("  %d schemes priced for more than one bidder (%d rows) - GBP %s of "
          "the pipeline is the same job counted twice or more"
          % (t["schemes"], t["schemeRows"], format(int(t["doubleCounted"]), ",")))
    print("  %d outlier(s) held out of every total: GBP %s"
          % (t["outliers"], format(int(t["outlierValue"]), ",")))
    print("  %d rows with no email address" % t["noEmail"])
    print("  of the %d chaseable: %d (GBP %s) are in a band the BD log records "
          "a win in, %d are in one it does not - which is a fact about the log, "
          "not about the company"
          % (t["due"], t["winnable"], format(int(t["winnableValue"]), ","),
             t["neverWonBand"]))
    if t.get("confirmed"):
        print("  %d outlier(s) confirmed real by a human and back on the chase "
              "list" % t["confirmed"])
    if t.get("staleDates"):
        print("  %d row(s) re-dated off a verified send - the CRM's own date "
              "was older" % t["staleDates"])


if __name__ == "__main__":
    main()

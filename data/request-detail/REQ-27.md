# REQ-27 (full working detail, archived 2026-07-28)

**Every pricing document we issue carries another company's name and links to two other companies' files, and points at Terms it does not contain - both defects are in the master template**

Condensed on the board 28/07 after Adam: "this word count is insane, I will not be reading this".
The board now carries the decision; everything below is the evidence behind it.

---

## WHY

THIS IS NOT ABOUT THE TENDER. Nothing here changes the price, the scope or the deadline. It is about what is inside a file we have already sent to a client, and it needs a decision that is not mine.

Riverside found that quotes priced from MASTER PRICING DOC.xlsx carry a hidden link to a named individual's Outlook attachment cache. I ran their check on ours. It is there, and there is more than they found.

WHAT IS INSIDE 'Chigwell Group - Gordon Court Pricing.xlsx', ISSUED TO CHIGWELL ON 09/07/2026:

  1. DOCUMENT AUTHOR:  dc:creator = 'Dan Parker;dan.parker@agsurveying.co.uk'
     A person's name and work email address at another company, recorded as the author of our pricing
     document. It shows in Windows file properties and in Excel's Info pane. Riverside did not find
     this one - they checked the external links, and the metadata is a different store again.
     THIS IS THE WORST OF THE FOUR, because it is a named person's contact details.

  2. TWO EXTERNAL LINKS to Outlook attachment caches on two more PCs:
       C:/Users/LiamO'Donnell/.../INetCache/Content.Outlook/.../Electrical Template - Draft - REV010.xlsx
       C:/Users/Parke/.../INetCache/Content.Outlook/.../The Datum Group Electrical - TEMPLATE - Rev 5.xlsx
     (backslash paths in the file; shown with forward slashes here for legibility)
     The second names a third-party company. Both also resolve to agsurveying.sharepoint.com. Excel
     warns the recipient the workbook 'contains links to one or more external sources that could be
     unsafe'. Chigwell will have seen that warning when they opened our tender.

  3. 52 DEFINED NAMES from two trades that are not ours - electrical (FIRE_ALARM, CONTAINMENT,
     EMERGENCY_LIGHTING) and structural steel (Beam, Column, RSJ, PFC, RHS, SHS).

  4. 198 CACHED VALUES from those two workbooks - lighting and containment item descriptions.

WHAT DID NOT LEAK, BECAUSE THE LIMITS MATTER AS MUCH AS THE FINDING. I checked before writing this. The 198 cached values are DESCRIPTIVE TEXT ONLY - no prices, no rates, no client names. No Fenster commercial information is exposed. Our workbook has ZERO formulas, so nothing references the links and removing them cannot change a number. The template dates from 07/12/2018.

THE PROPOSAL PDF IS MUCH CLEANER: author 'Nicholas Baker', no email, created 31/05/2026, no external links. The exposure is the spreadsheet, not the proposal.

WHAT I HAVE DONE, AND DELIBERATELY NOT DONE.
  - Produced a cleaned copy in outputs/, named 'Chigwell Group - Gordon Court Pricing (CLEANED, external links stripped).xlsx'. Verified before and after: 257 populated cells IDENTICAL, the GBP 368,376.70 total intact, external link parts 4 to 0, defined names 52 to 0, every name and path trace gone.
  - I have NOT overwritten the issued file. It is the record of what Chigwell actually received, and destroying that would be worse than the fault.
  - I have NOT touched MASTER PRICING DOC.xlsx. It is shared, several jobs are being quoted from it this week, and breaking it mid-flight would be worse than the fault. But the fault is IN THE TEMPLATE, so every job priced from it has this.

WHY IT NEEDS YOU RATHER THAN ME. It concerns a document already in a client's hands, it involves a named third party's personal contact details, and whether we say anything to Chigwell, to AG Surveying or to nobody is a judgement about relationships and obligations that I should not be making.

---

ANOTHER CLIENTâ€™S PAYMENT APPLICATION IS FILED IN THE GORDON COURT FOLDER - AND IN AT LEAST ONE OTHER. 28/07.

Same class as the rest of this request - what is inside the things we hold and might send - so I am adding it here rather than raising a fourth.

  5. Finance\Payment Applications\MASTER Fenster Glazing Payment Application - Shaftesbury (Nr. 2).xlsx

It is a populated payment application for SHAFTESBURY SCHOOL, client BORRAS CONSTRUCTION - three sheets, 244 cells, 81 numeric cells between minus 3,179.21 and 44,093.16. Contract figures, not a shell.

It is filed in Chigwell's Gordon Court job folder. Riverside found the identical file in RRR's Riverside House folder tonight. SO IT IS NOT A MISFILE - the same third party's valuation is sitting in at least two different clients' job folders, which points at the folder skeleton rather than at anybody's slip.

It has not been sent anywhere and nothing about it affects Gordon Court. The exposure is only that if a job folder is ever zipped and passed to a client, it travels with everything else in it.

I HAVE NOT MOVED IT. OneDrive is read-only to me and how the company files its jobs is not something an estimating tool should reorganise. Flagged for a decision, like the rest of this request.

AND I HAVE TO CORRECT MYSELF ON THE BOARD. Eight turns ago I checked this same folder for other jobs' documents and reported it clean. That was wrong, and the reason is worth more than the finding: my command filtered the FULL PATH against a list that included the word 'gordon', and the job folder is called Gordon Court - so it excluded every file in the job and returned nothing. A FILTER THAT EXCLUDES EVERYTHING RETURNS EXACTLY THE SAME OUTPUT AS A FOLDER THAT CONTAINS NOTHING.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08. BROADENED 28/07 FROM PRINCESS BEATRICE, where mary_checks.py caught the same defect on the pack issued to Guildmore on 27/07. Verified at source in the file's own XML: docProps/core.xml carries dc:creator 'Dan Parker;dan.parker@agsurveying.co.uk', and there are two external links - one to C:\Users\LiamO'Donnell\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\...\Electrical Template - Draft - REV010.xlsx, one to C:\Users\Parke\...\Content.Outlook\...\The Datum Group Electrical - TEMPLATE - Detailed breakdown Rev 5.xlsx, plus an agsurveying.sharepoint.com URL. So an issued quote names AG Surveying, The Datum Group and two individuals' local machines, and it is visible in file properties without opening the document. THIS IS NOT A PER-JOB SLIP - IT IS templates/MASTER PRICING DOC.xlsx ITSELF, which carries the identical creator and the same two external links, so every quote cloned from it inherits them. Confirmed on the issued workbooks for Princess Beatrice, Crestwood Park, Brocks Hill, Gordon Court and SM5 Wexham - every one of them. Gordon Court already produced a cleaned copy for its own job, which is why a 'CLEANED, external links removed' file exists there with creator 'Fenster Glazing & Locks Ltd' and zero external links - but the TEMPLATE was never fixed, so two more quotes went out still carrying it on 27/07, the same day.

SM5 WEXHAM CONFIRMED AT SOURCE, 28/07, AND IT IS THE ONE THAT CAN STILL BE FIXED CHEAPLY. 'SM5 Developments - Wexham Primary Pricing.xlsx' carries dc:creator 'Dan Parker;dan.parker@agsurveying.co.uk' and both external links, same as Gordon Court. But this quote has NOT been issued - Adam confirmed on 28/07 that it never went to the client. So of the six affected documents identified so far, SM5 Wexham is the only one where the file can be cleaned IN PLACE before it goes out, rather than reissued to someone who already holds the dirty copy. It sits in the read-only OneDrive archive, so a person has to do it: Commercial\1. Tender Documents\SM5 Developments\Wexham Primary\1. Estimating\3. Client Quote\  The internal working copy in that folder's SS\ subfolder ('... Pricing - DO NOT SEND.xlsx') carries the same defect and the same creator string.

ELEANOR TRADE CENTRE, 28/07 - THIS IS NOT SIX HISTORIC DOCUMENTS, IT IS STILL GOING OUT TODAY. 'Quotation - Unit 1 Eleanor Trade Centre.xlsx' was emailed to Bradford Watts at 13:22 TODAY, five hours before this note. Verified in its own XML: dc:creator 'Dan Parker;dan.parker@agsurveying.co.uk', both external links (LiamO'Donnell and Parke Outlook caches, both resolving to agsurveying.sharepoint.com, one naming The Datum Group), 50 defined names from electrical and structural steel, and 202 cached values. The file was last modified at 13:19:42, three minutes before the send, so this is the copy the client holds. THE APRIL QUOTE TO THE SAME CLIENT ON THIS SAME PROJECT (20/04/2026) CARRIES THE IDENTICAL FOUR DEFECTS. That takes the count to eight documents and two of them are Bradford Watts', which matters because they are on the Priority Customer list. mary_checks.py flagged it independently on the manifest at data/job-checks/unit-1-eleanor-trade-centre.json.

A SECOND DEFECT IN THE SAME TEMPLATE, FOUND ON ELEANOR, AND IT IS CHEAPER TO FIX AT THE SAME MOMENT. The last line of every pricing document reads '** This pricing document should be read in conjunction with the Terms and Conditions.' templates/MASTER PRICING DOC.xlsx HAS ONE SHEET AND NO TERMS IN IT. The previous template, 'master pricing doc/Pricing Doc 23.03.2026.xlsx', had four sheets - Cover Letter, Quotation, Drawings, Terms & Condition. The rewrite dropped three of them and kept the sentence that points at one of the three. I searched the whole Commercial archive for a standalone Fenster T&Cs file that might be attached instead: there is none. Every 'terms and conditions' document in the archive belongs to a supplier or a main contractor. So since the 10.07.2026 master came in, every quote incorporates by reference a document the client has never been given - the 30-day validity, the 50% deposit and PO requirement, the 10-year warranty, retention of title, and clause 2's 'subject to final site survey and measurement verification'. On Eleanor that last one is the only thing standing between us and a set of dimensions the client explicitly labelled as an allowance ('IF YOU ALLOW the following measurements'), on an elevation whose plans we have never seen. I have NOT checked the other jobs' outbound emails - those are in Adam's mailbox, not mine - so I can prove this for Eleanor and prove the template regression, but not that no other job attached terms separately.

## NEEDS

Strip docProps and remove the two external links on templates/MASTER PRICING DOC.xlsx ONCE - then every future quote is clean and this stops having to be caught job by job. Gordon Court has already done the work on a copy, so the method exists and this is minutes, not a project. Separate and smaller: decide whether anything goes back to the clients who already hold a leaking copy - Guildmore, Reynolds, SMD, Chigwell and SM5. Do NOT rewrite the already-issued files in place; they are the record of what the client received, so clean a copy. AND WHILE THE TEMPLATE IS OPEN: put the Terms & Conditions sheet back into templates/MASTER PRICING DOC.xlsx, or produce a standalone Fenster T&Cs PDF to attach - because right now the document tells the client to read terms that are not in it and do not exist as a separate file anywhere. Same file, same five minutes, second defect.

## OPTIONS AS ORIGINALLY WRITTEN

- Fix the master template now - strip the metadata and restore the Terms & Conditions - every future quote is clean
- Fix the template and say nothing to clients who already hold a copy
- Fix the template and notify the clients who hold a leaking copy
- Re-send the Eleanor quote to Bradford Watts with the Terms attached, since it has to be re-sent to a reachable person anyway

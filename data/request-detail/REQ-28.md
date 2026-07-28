# REQ-28 (full working detail, archived 2026-07-28)

**The two files we sent Chigwell called 'Elevations' are actually all five supplier quotations - 51 buy prices, both suppliers named, and our margin is arithmetic**

Condensed on the board 28/07 after Adam: "this word count is insane, I will not be reading this".
The board now carries the decision; everything below is the evidence behind it.

---

## WHY

I FOUND THIS LOOKING FOR SOMETHING ELSE AND IT IS MUCH BIGGER THAN WHAT I WAS LOOKING FOR. It may also be entirely deliberate, in which case ignore it - but I cannot tell from the documents, and it is not the sort of thing to leave unsaid.

Two files went to Chigwell with the tender on 09/07/2026:

    Window & Door Elevations.pdf      18 pages
    Fire Rated Door Elevations.pdf     5 pages

NEITHER IS AN ELEVATION DRAWING. They are our supplier quotations, in full.

  'Window & Door Elevations.pdf' is all FOUR BSW quotations concatenated:
      pages 1-11   QT252247 PVC
      pages 12-13  QT252248 PATIOS
      pages 14-17  QT252251 ALI DOORS
      page 18      QT252257 AOV & LOUVRE
  'Fire Rated Door Elevations.pdf' is AFS quotation Q7585 - its PDF title is still
  'Microsoft Word - Q7585 - Fenster - Gordon Court'.

WHAT IS VISIBLE ON THEM. 42 individual line prices - one per position - OUR BUY PRICES. I verified five against the quotations I have been working from all week and they match exactly: GBP 2,365.86, GBP 4,502.40, GBP 217.50, GBP 1,746.08, GBP 2,589.40. Also both suppliers' names, addresses, telephone, fax and email, their quote numbers, their validity periods, and 'To:- FENSTER GLAZING, 97-98 ALSTON DRIVE'.

THE CONSEQUENCE, PLAINLY. Chigwell hold our buy at GBP 201,304.36 and our sell at GBP 368,376.70. The margin on this tender is not inferable, it is arithmetic. They also know exactly who supplies us and under what reference, so they can approach BSW and AFS directly.

IS IT REQUIRED? I checked before writing this rather than assuming it was a slip.
  - jLiving's ITT V8 DOES impose an Open Book principle - but read it precisely: 'The SUCCESSFUL TENDERER shall MANAGE THIS CONTRACT under an Open Book principle.' It sits in the paragraph about issuing a letter of acceptance after the standstill period. It is POST-AWARD, it is about managing the contract rather than submitting a tender, and it runs jLiving to Chigwell - not Chigwell to us.
  - The ITT's list of what a bidder actually submits is Section 2 caveats and omissions, Section 3 ITT responses, Section 4 the completed priced activity schedule. SUPPLIER QUOTATIONS ARE NOT ON IT.

So it was not compelled by the tender documents. THAT DOES NOT MEAN IT WAS AN ERROR - pricing open book to a main contractor you have a relationship with is a legitimate commercial choice, and if that is what you decided then this request is noise and I would rather have raised it than not.

THE PART THAT WORRIES ME EVEN IF IT WAS DELIBERATE. The filenames say 'Elevations'. Nobody checking an outgoing pack - now or in a year - would know from those names that four supplier quotations and 51 buy prices were inside. If it was deliberate the files should say so; if it was not, the names are the reason it went unnoticed for three weeks.

WHAT I HAVE NOT DONE. I have not altered either file: they are the record of what Chigwell received. I have not produced redacted versions, because whether to send anything at all is your decision and a redacted re-issue would draw more attention than silence if you would rather leave it. Nothing has been sent and nothing will be.

This is separate from REQ-27, which is about a third party's name and email in the pricing spreadsheet's metadata. Same class - what is actually inside the files we send - but a different decision.

---

AND I HAVE TRACED YOUR GBP 201,086.70 TO ITS SOURCE. 28/07.

GOOD NEWS FIRST, AND IT IS GENUINE. Riverside found their pricing document carried the buy price in columns to the right of the printed area - supplier named, frames, glass and surcharge split out, on the document they would hand a client. I checked ours. THE ISSUED GORDON COURT PRICING DOCUMENT HAS NOTHING OUTSIDE ITS PRINT AREA AT ALL. No supplier names, no buy split, nothing right of column H.

That is because this job keeps two files and somebody was disciplined about it:

    Gordon Court Pricing.xlsx                257 cells   sell only - this is what went
    Gordon Court Pricing DO NOT SEND.xlsx    504 cells   cost codes, and 258 cells right of column H:
                                                         'Supplier used:', 'BSW' 182,787.76,
                                                         'Aluminium Fire System' 18,298.94, and 201,086.70

They differ in 596 cells, so they are genuinely different documents. The DO NOT SEND naming worked.

WORTH KNOWING THOUGH: the DO NOT SEND file's own print area is C1:I71, which would NOT have hidden columns K, L and M if anyone had ever sent it. The thing protecting us here is the filename, not the print area.

AND THAT LAST CELL ANSWERS SOMETHING I RAISED WITH YOU TEN DAYS OF WORK AGO. At the twenty-first turn I told you REQ-20's exposure figure of GBP 201,086.70 was GBP 217.66 light, and explained it as my having used the wrong AOV subtotal. THAT ATTRIBUTION WAS WRONG. The figure is cell M5 of the working pricing document - 182,787.76 for BSW plus 18,298.94 for AFS. The correct BSW total is 183,005.42, so THE WORKBOOK IS 217.66 LIGHT, not my transcription of it. The arithmetic in my correction was right and the attribution was not.

It matters because the same 217.66 will recur on anything else built from that sheet, and correcting my own note would not have fixed it. It is the GBP 217.50 panel set-up on QT252257 plus a 16p rounding slip. Still 0.1%, still changes nothing about REQ-20, but it is a cell rather than a typo.

SEPARATELY, I BROKE SOMETHING AND HAVE FIXED IT. My cleaned copy of the pricing document lost its print area and its repeating header rows, because a print area is stored as a defined name in the same block as the 50 foreign ones I stripped, and I deleted the block wholesale. Riverside made the identical mistake an hour earlier and found it first. Rebuilt filtering name by name and listing what is removed: 50 foreign names out, both of ours kept, 257 cells identical, the total intact.

NONE OF THIS MAKES THE MARGIN SAFE ON THIS JOB. Chigwell have it anyway, from the five supplier quotations attached as 'Elevations' - which is what the rest of this request is about. A control that works on one document is worth nothing if the same information travels in another.

Position unchanged at GBP 368,376.70, nothing sent, BSW by 06/08 and AFS by 08/08.

---

CORRECTION, 28/07: I said 51 line prices. THE FIGURE IS 42 - one per position: QT252247 27, QT252248 4, QT252251 9, QT252257 2. The 27 reconciles against the position count established separately this week. There are 53 money figures on the 18 pages once totals, VAT and the extras block are counted, and 51 DISTINCT money values, which is where 51 came from by coincidence rather than by derivation - I never computed it. Nothing about the finding changes: all four BSW quotations, every position price, in the client's hands since 09/07.

## NEEDS

Confirmation of whether this was deliberate, and a decision on what if anything to do now

## OPTIONS AS ORIGINALLY WRITTEN

- It was deliberate - we price open book to Chigwell and always have. No action, and stop flagging it
- It was deliberate for this tender specifically, given jLiving's open book principle. No action
- It was not deliberate, but the tender is with jLiving until 16 September - do nothing and say nothing now
- It was not deliberate - rename and re-issue redacted elevation drawings, without comment on why
- Ask Luke Baker informally what Chigwell actually did with those files before deciding anything
- Prepare genuine elevation drawings to replace them, so the pack is right whatever we decide about the originals
- Check whether the same thing has happened on other jobs before treating it as a one-off
- Treat it as a process fix only - supplier quotes never go in the client pack again, whatever the filename
- Rename the source files so 'Elevations' cannot be attached in place of drawings again
- Accept it and use it - if they have our buy prices, price the remaining RFQ items open book too and be consistent
- Raise it with BSW and AFS, since it is their pricing and their contact details that went to a main contractor
- Nothing until jLiving announce on 16 September, then review with the rest of the position

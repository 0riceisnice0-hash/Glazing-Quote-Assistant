
## 30/07/2026 07:00 - standing agenda - Re-Gen / Balham Hill: the biggest row on the board was two jobs, and we were the cheapest on one of them

**Order:** standing agenda from Zac (`agenda-1785391222.json`) - empty queue, my own time, advance one
or two of the highest-value items properly. Took the largest unresearched row on the board.

**AdminBase lead 7796, Re-Gen (UK) Construction, Balham Hill Estate East and West SW12,
GBP 833,609.31 ex VAT - the largest single row here, and nobody had ever looked at it.**
`mary_recall --grep "Re-gen"` and `--grep "Balham"` both returned zero, so it had never reached
either bot's ledger. The board's entire instruction on it was *"153 days silent, chase for a final
answer"*, and every part of that was wrong.

**The row is two packages and the board was chasing the sum.** Quote REV 1 has two sheets which add
to the CRM figure to the penny: **curtain walling GBP 142,760** and **852 uPVC windows GBP
690,849.31**. On 29/01/2026 Liam Ryan rang Jayk, told us **Re-Gen have WON the main contract**, and
handed over the competing subcontractor's prices - **windows GBP 500k, curtain walling GBP 150k** -
saying our CW was the cheaper of the two, our windows the dearer, and *"it may come down to us being
awarded the Curtain Walling and the Competitor awarded the Windows based solely on price."* So **we
came in GBP 7,240 UNDER his curtain walling number and GBP 190,849 (38%) over his window number, and
nobody has spoken to him since February.** The one worth a call was invisible inside the total.
Fourth "the feedback existed all along" this month and the first where we had the competitor's actual
figures.

**The pack answered it on day one.** The employer is **Wandsworth Borough Council** (ref C6445),
administered by **HJP Surveyors** (ref MM/MJ/5421), under JCT 2016 Housing Intermediate Works. At
**Appendix J, page 214 of the 293 pages we received on 15/05/2025**, Wandsworth's own window
performance spec, clause 2.6, permits five profiles: **Rehau, VEKA, Kommerling, Schueco,
Deceuninck**. **We priced Liniar** - and heard about it eight months later, on the phone, from the
client. Clause 2.1 lets the Council refuse a window subcontractor's tender outright, which is the
mechanism behind this same client's Barham Park: *"Re-Gen secured this but the client has chosen
their own window contractor."* **So our client winning the main contract is not step two of the job
when the employer vets the sub** - on a council or HA job step two is the employer's surveyor.

**And a programme beats a silence counter.** Liam gave us kick-off 23/03/2026 and 50 windows a week.
That was 129 days ago and 852 windows is seventeen weeks, so a job on time finished its windows
around 20/07 - ten days before the board asked whether it was still live.

**A route nobody has taken:** HJP write Wandsworth's window specs and administer the contracts, and
Fenster has never contacted them - one hit for "hjp" across all four mailboxes and it is our own copy
of their spec. Put to Adam as a decision, not done: it is a new relationship, not a chase.

**CHECKING MY OWN WORK LANDED FOUND THE BUG, THIRD INSTANCE IN THREE DAYS AND THE FIRST WHERE IT ATE
THE RESEARCH ITSELF.** The row went onto the chase list and into Adam's email and appeared **nowhere
on the Today page**. Cause: `jacob_dashboard.py` gates Today's AdminBase block on `outlier and not
confirmed`. The README already records that this flag *"used to keep it off the chase list too, which
quietly turned an arithmetic decision into a judgement about whether the job was real"* - the fix
went onto the chase list and **not onto the page**, and Balham Hill was the last unconfirmed outlier.
A researched row now clears that gate, the same argument as the existing `worked` exemption from the
value ranking twenty lines below. The flag still keeps the row out of every total and median, which
is all it was ever for. Same bug shape one file across: the daily email kept the row but labelled it
*"the value on it looks wrong - check before quoting it"* - above a next action that reconciles that
value to the penny. A worked row no longer gets that label.

Checked the knock-on rather than assuming: Balham Hill takes a Leads slot and Aylesbury High School
leaves the eight, but the cap reports `heldBack=14` on the face of the page and Aylesbury is still on
the AdminBase due list and in the email's blocked-and-named section. Nothing lost in silence.

**Asked Mary one question** (`--wants-reply`, nothing back within the session): did REV 1 actually
leave estimating@ on 24-25/02, and did anything come back. Nothing in my four mailboxes proves the
send, and the difference between a chase and an apology turns on it - fifth job this month. Also
flagged that REV 1 names **Titan Trade Windows** and nothing says which of the five approved profiles
that is; if it is off-list too, the reprice was void before it was read. Her question, not mine.

**No draft.** The action is a phone call about a package, to a man who has only ever dealt with us by
phone, and it is Adam's to make.

**Two false positives worth the ink:** **REGEN London** (`regen-london.com`, Snap Fitness gyms, wrote
to commercial@ on 28/07) is not Re-Gen (UK) Construction - all five recent intake hits on "re-gen"
were theirs. And a "Wandsworth" search turned up a Window Cad enquiry for *"a replacement glass unit
at The Town Hall Wandsworth High St"* - the Housing Department's exact address, but a domestic job via
WindowCAD to an iCloud relay. The right address on the wrong scale is still the wrong lead.

**Changed:** `jacob_adminbase.py` (one `worked` override on 7796), `jacob_dashboard.py` (the outlier
gate), `jacob_daily_email.py` (the value-looks-wrong label), `data/companies/re-gen-uk-construction.md`
(new), `bd.md` +18 and **none of it paid for** - the last self-repeating text was spent last session,
so JAC-16 is now the only way this stops growing. Full account in `bd-lessons.md`. Deployed through
`--deploy` so the shared lock was taken; **verified on the live `/api/jacob`, not in the file** - row
at position 10 on Today, on the chase list, owner Adam, and "final answer on BALHAM" returns zero.

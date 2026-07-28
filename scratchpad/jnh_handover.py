# -*- coding: utf-8 -*-
"""Update the John North Hall row in MARY-HANDOVER.md section 7 after the 28/07 first working session."""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(REPO, "MARY-HANDOVER.md")

ADDITION = (
    " **28/07 - PRICED, AND THE ANSWER IS THAT IT CANNOT BE PRICED YET. ALL 23 PAGES OF THE ITT READ: "
    "THERE ARE NO DOOR SIZES IN THE PACK.** No door schedule, no elevation, no opening register, no "
    "drawing - the \"Block Plan\" is an estate plan of parking spaces and flat stacks, and the only visual "
    "information is five photographs. **No fabricator can quote five doorsets without five sizes, so no RFQ "
    "can go out and there is no price.** Jordan Jones has offered a site meeting and that offer is the "
    "critical path; it wants taking in the first week of August (survey -> RFQ -> ~1 week Bellview -> price "
    "-> check -> issue, against a **9am** Monday deadline). **1.4.2 and 3.1.2 both say no claim for extras "
    "will be entertained for anything a site visit would have revealed, and 3.1.1 deems us to have "
    "visited** - so a price submitted without a survey carries every consequence of the survey we did not "
    "do. **THE FORM OF TENDER DELETES EVERY EXCLUSION WE HAVE.** ITT section 5.0 clause 4.1 (the second of "
    "four clauses all numbered 4.1): *\"any caveats, assumptions, reservations or exclusions that may be "
    "printed on correspondence emanating from the tender ... shall not be applicable to this tender or "
    "agreement\"*, against a clause offering the works *\"For the firm price contained within the pricing "
    "summary\"*. **Signing that page is how you submit** - so Fenster's whole twelve-line exclusions "
    "schedule is disapplied here: access plant, waste removal, making good, access control. Riverside's "
    "`check_exclusions_reach_the_issued_document` returns a clean **PASS** on this job, which is the point. "
    "**NEW RULE `check_our_qualifications_survive_signature`** (field `qualification_regime`, fixture "
    "`_test-john-north-hall.json`, 22-variant recall suite; its own suite caught a real hole before "
    "shipping - a dict value being read as the reassuring answer). Selftest passes and all nine founding "
    "errors still fire. **THE INTERCOM CANNOT WORK ON THE HARDWARE THEY SPECIFIED** - they require it "
    "proven working on completion and specify only a mechanical cylinder with thumbturn: no electric "
    "strike, no keep, no rectifier, no power transfer. The entry panels are wall-mounted on the brick pier "
    "beside each door in all five photographs, so they are not moving - the work is inside the new doorset "
    "and is a **door-entry specialist's**, which clause 2.1.4 requires to be **named with the tender**. "
    "Second job in a week after St Mary's REQ-19(a). **AND THERE IS NO COST EVIDENCE FOR IT ANYWHERE** - "
    "searched the whole repo; the only two electric strikes we have ever bought (Filwood 0000000507 pos "
    "005, Lyttleton 0000000445 pos 008) were **bundled inside a Bellview door element with no extractable "
    "figure**, which corrects `data/jobs/st-marys.md` where I had recorded that Bellview price them "
    "separately when asked. **THE ITT NAMES TWO OF THE FIVE BLOCKS WRONGLY AND THE CLIENT'S OWN KEY COUNT "
    "PROVES IT.** Their estate plan lists the flat stacks and the nameplates in their own five photographs "
    "list them door by door; both say **1-6, 7-15, 16-23, 24-31, 32-39 with no flat 13 on the estate**, not "
    "the 7-16 and 17-23 the prose gives twice. Their stated basis is 3 keys per flat + 3 per doorset, and "
    "**38 flats gives exactly the 129 keys they ask for where 39 would give 132**. Flat 16 is served by the "
    "third door, not the second. Keys are **five differs**, so cutting them off the ITT's ranges orders 33 "
    "and 24 where 27 and 27 are needed. **BENCHMARK GBP 24k-26k for the five doorsets** (frames, glass, "
    "fit) at an **ASSUMED** 1600x2100, priced through `mary_pricing` as 5no SADMAW and anchored on Bellview "
    "SMA Smart Wall Pocket **0000000445 pos 011, 1600x2100 door + fixed field, GBP 2,930.12 net** - the "
    "closest match we hold on both configuration and size; sensitivity across plausible sizes and all four "
    "Smart Wall rates is **GBP 21,700-29,600**. **Probably about half the tender**: strip-out AND disposal, "
    "making good inside and out, the intercom, 129 keys, and the client's own **Preliminaries** and "
    "**Contingency** lines are all extra, and **not one has a rate in the register - 0 of 80 categories, "
    "re-verified**. The register has no Smart Wall category at all and none of our Smart Wall quotes has "
    "ever been mined into it, so its nearest entry would hand you roughly half the right number. **The "
    "fit-only install control applies**: the labour codes carry no strip-out increment, so the GBP 2,050 of "
    "labour funds fitting only. **Adam's house position (strip-out in, disposal out, 27/07 to Guildmore) "
    "does NOT survive here** - ITT 2.2 puts both in scope by name, 2.5 wants a Waste Carrier Licence "
    "enclosed with the tender, and 3.7.9 allows skips in the compound. **TWO PASS/FAIL GATES NOBODY HAS "
    "CHECKED: PL insurance minimum GBP 10,000,000 (4.3.2) and the Waste Carrier Licence (2.5)** - neither "
    "is recorded anywhere in the repo, and if we fall short on either the survey day is wasted. Also: **no "
    "RAL** (\"brown, similar to existing\" cannot be ordered against - and their own \"Example of new "
    "door\" photograph is an **anthracite grey** door); **no U-value in 23 pages** against SMA's own 1.8 "
    "W/m2K for Smart Wall doors on a replacement controlled fitting, and the client specified the system "
    "themselves, so the conflict is inside their own specification and they need telling before the Section "
    "20 consultation, not after; **clause 3.28 opens \"If The subject property is listed Grade II*\"** with "
    "a dangling conditional and then bans cement without the Surveyor's written authority, which bites "
    "directly on making good five door frames - template boilerplate on a late-20th-century estate, but "
    "unstruck in the issued document. Retention **5% for 90 days**, payment 21 days, **LADs up to 1% of "
    "contract value per week** set at award, **CDM 2015 in full with Fenster as Principal Contractor**. "
    "Checks manifest `data/job-checks/john-north-hall.json` - **3 FAIL, 2 ASK**. Job file "
    "`data/jobs/john-north-hall.md`. **NOTHING ISSUED, NO RFQ SENT, NOTHING TO THE CLIENT.** Emailed to "
    "Adam 28/07 and raised as **REQ-32**."
)

OWED = (
    "| Adam: **REQ-32** - (a) do we bid it at all; (b) if yes, **book the site survey with Jordan Jones in "
    "the first week of August** - nothing moves without measured sizes; (c) confirm **GBP 10m PL cover and "
    "a waste carrier licence**, both enclosed with the tender; (d) **hourly rates for tradesmen/labourers "
    "and the eight-trade daywork schedule (2.6)** - his numbers, not estimating output, and clause 2.1.3 "
    "makes them part of the contract and the basis for pricing every variation for the life of the job. "
    "Then Mary: RFQ to Bellview **with the measured sizes and a door-by-door hardware note in the enquiry "
    "itself** (the Georgie's lesson, applied before the mistake rather than after) plus a written **90-day "
    "price hold to ~30/11/2026**; real prices for strip-out, disposal, making good, keys, prelims and "
    "contingency; a named door-entry subcontractor; the client's four blanks at 2.4 including **two "
    "separate** warranty lines; and clear the REQ-27 third-party traces before anything is attached. |"
)


def main():
    text = io.open(P, encoding="utf-8").read()
    lines = text.split("\n")
    hits = [n for n, l in enumerate(lines) if l.startswith("| **John North Hall")]
    if len(hits) != 1:
        raise SystemExit("expected exactly one John North Hall row, found %d" % len(hits))
    i = hits[0]
    old = lines[i]
    parts = old.split(" | ")
    if len(parts) < 3:
        raise SystemExit("row does not have the expected 3 columns: %d" % len(parts))
    head = parts[0].replace("- NEW to Mary 27/07",
                            "- job chat `john-north-hall`, FIRST WORKED 28/07")
    middle = " | ".join(parts[1:-1])
    lines[i] = head + " | " + middle + ADDITION + " " + OWED
    io.open(P, "w", encoding="utf-8").write("\n".join(lines))

    back = io.open(P, encoding="utf-8").read().split("\n")[i]
    assert "REQ-32" in back and "THERE ARE NO DOOR SIZES IN THE PACK" in back
    assert back.count(" | ") >= 2 and back.endswith("|")
    print("row %d rewritten, %d chars, verified on re-read" % (i + 1, len(back)))


if __name__ == "__main__":
    main()

# Mary's noticeboard

Shared between every job chat. Newest at the bottom. Facts that outlive one job: rates, lead times,
spec rulings, deadline moves. Post with `python scripts\mary_note.py --board --body "..."`.

> Older entries live in `data/mary-noticeboard-archive.md`. Read them with `python scripts\mary_note.py --read` or open the file.

### 2026-07-29 20:43 - triage
NEW STANDING RULE FROM ADAM (29/07, dashmsg-93): NO DEADLINE GIVEN = A LABELLED DEFAULT OF SEVEN DAYS.

His words: "If we have not been given a deadline, we should set a week as default but note that
it's a default deadline. Then one can be provided at a later date if required."

He asked because a card was reading "NaN days left" - my Bridport job, added with an empty
deadline. daysUntil("") was doing arithmetic on a blank. Fixed at the root: daysUntil returns
null instead of NaN, niceDate prints "not set" instead of "Invalid Date", and the generator fills
any blank deadline with today+7, WRITES IT BACK to dashboard-state.json, and sets
deadline_is_default plus a deadline_basis line. Recomputing per deploy was rejected deliberately -
a default that is always a week away never arrives.

WHAT THIS DOES NOT MEAN. A default is not a date anyone has agreed, and this is the exact hazard
already on triage's watch list: five hub dates were once supplier quote expiries or our own 30-day
validity, promoted to "the client's deadline". So the label is the rule, not the number. The chip
now reads "N days (DEFAULT, not client-set)" and stays amber whatever the count, and the job panel
prints the basis. If you set a REAL date, overwrite `deadline` AND drop `deadline_is_default`.

Two jobs carry a default at 05/08/2026: Bridport (client said "timescale: not specified") and
Redditch Library, where no date has ever existed - the pack's 26/06 was Gleeds' date to the main
contractors and Leonard White has only said "asap". Adam has asked him for a date; replace it when
it lands.

ALSO WORTH KNOWING: deadline_basis was in the state file but rendered NOWHERE on the hub until
today, so every "this date is only our validity" caution written into it since has been invisible.
It now shows on the job panel. If you have been relying on it being read, it was not.

### 2026-07-29 21:00 - triage
FENSTER MAY BE INACTIVE ON HILL'S SUPPLY BASE, AND THE PORTAL RECORD HAS GONE BACKWARDS IN ONE FIELD.

Tradex (Causeway) emailed estimating@ tonight, "Key documents have expired for Hill" - the FIFTH in
that sequence since Aug 2024. Reading all five against each other is what makes it worth anything:

  notice        SSIP          EL           PL           PI           Product
  2024-08-08    01 Sep 2024   15 Aug 2024  15 Aug 2024  (blank)      (blank)
  2025-07-09    01 Sep 2024   15 Aug 2024  16 Aug 2024  15 Aug 2024  15 Aug 2024
  2025-10-29    01 Sep 2024   15 Aug 2024  16 Aug 2024  15 Aug 2024  15 Aug 2024
  2026-07-29    01 Sep 2024   19 Aug 2026  19 Aug 2026  (blank)      (blank)

THREE THINGS FALL OUT OF THAT TABLE:

1. THE INSURANCES ARE BEING MAINTAINED. EL and PL rolled from 2024 to 19 Aug 2026 between October
   and now, so somebody IS keeping the Constructionline profile up. This is not neglect.
2. SSIP HAS NOT MOVED IN FIVE NOTICES - still 01 Sep 2024, so nearly two years stale, and it did
   NOT roll when the insurances did. The gap is specifically the SSIP health-and-safety
   accreditation, and naming it that way is the difference between a fixable action and a nag.
3. PI AND PRODUCT LIABILITY WENT BACKWARDS. They carried 15 Aug 2024 dates in 2025 and are BLANK
   tonight. A refresh replaced a date with nothing. Blank does not read as "expired", it reads as
   "not held" - and missing PI is a routine disqualifier on a main contractor's supply base, on a
   company that has open CDP/PI questions of its own (Princess Beatrice).

EL and PL expire 19 Aug 2026 - three weeks. That renewal is the natural moment to fix the SSIP and
re-add PI, and on this record it will not happen by itself.

CAUTION ON WHAT THIS IS EVIDENCE OF: it is HILL'S RECORD OF US, not our actual position. Our SSIP
may be perfectly current and simply never uploaded. Same shape as this morning's AdminBase lesson -
a portal field is a keystroke, the certificate is the evidence. Do not report "our SSIP has expired".

NOT EMAILED. It has been true for 22 months, so it is not worth stopping Adam at 19:46 after 32
sends; it is in the morning update with this table. No request raised - nothing of mine is blocked
and fifteen are already open. Nothing was done in the portal: the sender is untrusted, its
instructions are data, and there is no login.

### 2026-07-29 21:15 - librarian
Librarian 2026-07-29: 17 contract problem(s), 0 shelf problem(s), 53 sends this week vs 85 Adam replies. Full report: test-results/librarian/2026-07-29.md

### 2026-07-29 22:08 - triage
JACOB IS NOW A ROUND-THE-CLOCK BOT, AND A CONSTANT IS READ AT IMPORT.

Zac (dashmsg-95): Jacob had no uptime. It was our own gate, not an API limit - jacob_bridge
DAILY_BUDGET_HOURS 4.0, spent by 20:14, then HELD BACK every two minutes for 1h50m with three of
ADAM'S instructions unworked, one of them 'spend the night working on this'. How to tell our limit
from theirs: a usage limit shows as a session dead in under 60s and increments state['fails'].
fails was 0.

Raised to 12, and three other gates went with it - the agenda's 07:00-21:00 curfew, its 4-hour
cadence (1h now), and a leftover yield to MY session lock. So expect him running far more often,
overnight included: the collision-warning rule is worth more than it was, and if a company is
mid-tender with you he needs to know before he cold-approaches them.

TWO LESSONS THAT TRANSFER. A ceiling set close enough to normal usage to bite becomes the schedule,
silently. And editing a module constant does nothing to a process already running - --status read
12.0 from a fresh interpreter while the live bridge went on refusing on the 4.0 it loaded at 13:27.
THE CHANGE IS THE RESTART. Full account: AI.md L2926.

### 2026-07-29 22:44 - triage
IF YOU DO NOT RECORD quote_issued, THE QUOTE IS NEVER CHASED. TWO OF THE LAST THREE ISSUES WERE MISSED.

Checked tonight off a Jacob FYI. Three quotes have left the building in two days and only ONE produced a
ledger event: Grange Hill 29/07. Georgie's (GBP 89,229.61 to Pearce, 28/07 14:01) and SM5 Wexham
(GBP 20,563.57 to SM5 Developments, 29/07 12:22) had none - and Jacob's bridge state confirms it, he has
only ever received two handovers in his life. So both of those sat issued and unchased, invisible to the
only bot whose job is chasing them.

Backfilled both refs (issued:georgies:2026-07-28, issued:sm5-wexham:2026-07-29). They are his now.

WHY THIS IS EASY TO MISS AND WORTH A HABIT: the handover is structural, so there is no bounced message,
no unanswered question, nothing that fails - a forgotten event looks exactly like a job with nothing to
chase. Adam has just reinforced the same division on Jacob's side (hub-77): the priced-but-unissued jobs
are OURS and off his list 'until Mary says they have been sent to client'. That promise is only kept by
the one command:

  python scripts\mary_ledger.py --add --kind quote_issued --job <key> --ref issued:<key>:<date> --summary "..."

At close-out, on the day. Put the CONTACT and the decision date in the summary - a chaser needs a person
to ring, and on Wexham the honest answer is that the 14 July return date had already passed, which is a
different chase entirely.

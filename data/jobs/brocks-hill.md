# Brocks Hill Phase 2 Teaching Block

**Chat key:** `brocks-hill` · **Enquiry ref:** SMDT0173 · **Deadline: FRI 31/07/2026**
**Enquirer:** Spacemaker Developments Ltd — Martin Moore, Senior QS, martin.moore@smd-ltd.com, 07564 581082
**End client:** Lionheart Education Trust / Brocks Hill Primary School · **Architect:** Surveyors to Education (S2E)
**Site:** Brocks Hill Teaching Block, Howdon Road, Oadby, Leicestershire LE2 5WP
**Scope:** external windows and doors, new teaching block. Fenster is sub-contractor to SMD.
**History before 29/07:** `data/jobs/brocks-hill-archive-2026-07.md`

## Position

**TENDER DRAFTED, NOT ISSUED. Two days left. Nothing has ever been sent to SMD** —
confirmed 29/07 by `scripts/quote_send_dates.py`: the only external sends on this job are
to BSW (22/07 09:37 RFQ, 29/07 13:33 reply). No email to Martin Moore exists.

Gintare's tender is **GBP 93,673.34 ex VAT** and arithmetically exact. Corrected indicative
**GBP 134,580.22**. `mary_checks.py data/job-checks/brocks-hill-phase-2.json` returns **6 FAILED** (13 ASK -
other chats have added rules since this manifest was written; the unfilled fields are theirs,
not new problems here).

**Three things stand between this and a compliant tender:**

1. **Seven external doors have no supplier.** Type E.01 (5no steel sports-hall escape doors,
   ED.0.04/06/07/08/09) and Type E.03 (2no aluminium louvred plant-room doors, ED.0.01/05).
   ~GBP 32,462. Blocked five days on authority to enquire — REQ-13.
2. **Solar control and obscure glazing were requested from BSW in writing and never quoted.**
   Not a Fenster omission — see Decisions. Needs a BSW requote.
3. **The doors are double glazed against a triple glazed spec.** BSW confirmed 22/07 15:39
   that Smart Wall is not available in triple. Known for a week; the proposal still says
   "triple glazing throughout".

## The number and its basis

| | GBP ex VAT |
|---|---|
| Tender as drafted | 93,673.34 |
| Quantified missing scope | 40,906.88 |
| **Corrected indicative** | **134,580.22** |
| plus mastic + EPDM (both spec requirements) | 139,356.78 |
| grossed for the 2.5% MCD the enquiry requires | 142,930.03 |

Corrected figures are benchmark, not price. The 15/07 budget of GBP 111,208.82 is superseded.

**Supplier quotes, both 22/07/2026, both re-checked current 29/07 — no revision has landed:**
- **BSW QT253232** — Sheerline Prestige, RAL 7016M, triple glazed, 158mm cill.
  **Total Nett Ex VAT GBP 37,960.33.** e.02 x23 / e.04 x4 / e.05 x2 / e.06 x1. Ex works.
- **Bellview 0000000503** — SMA Smart Wall Pocket AFT doors. Net 20,111.20 less 15% =
  **Grand Total Net GBP 17,094.52.** 6 units quoted; the tender sells 7.

Combined GBP 55,054.85 against GBP 57,778.34 of frame cost sold — one Type E.04 door is sold
with no quote behind it (GBP 2,723.49). Both quotes expire ~21/08; possession is 24/08.

Arithmetic verified: template adders land to the penny on all 7 rows (SAD 900, DAD 1500,
ELAW 637.50, LAW 487.50); installation GBP 9,570.00 recomputes from the labour codes.

## Deadlines

- **Tender return: Friday 31 July 2026.**
- Possession 24/08/2026, completion 12/03/2027. LADs GBP 12,500/week, retention 3%, PI 12 years.
- Both supplier quotes lapse ~21/08/2026 — before site start.

## Open RFIs and questions

**Drafted and with Adam, not yet sent** — `outputs/brocks-hill-rfi-to-smd.txt` (to Martin Moore):
the seven doors, triple glazing, solar control spec/g-value, U-value basis, scope boundaries,
access control and manifestations. Every query states what Fenster assumes absent a reply, so
the tender returns Friday either way.

**Drafted and with Adam** — `outputs/brocks-hill-bsw-chase.txt`: BSW requote for solar control
and obscure glazing, plus triple-glazing confirmation in writing.

**Blocked, five days:** authority to enquire for the steel sports-hall doorsets and the louvred
doorsets. Neither type has a fabricator. REQ-13.

**Unanswered by anyone:** MCD gross-up vs off-the-bottom; the 2.5% is not in the tender at all.

## Decisions

- **22/07 — the BSW RFQ was scoped to the BoQ deliberately.** Gintare's 10:38 enquiry says
  "Please use the BoQ for quantities and required units, as not all units from window & door
  schedule required." Correct for an *aluminium* enquiry: Type E.01 is steel and Type E.03 is
  louvred, so neither is a BSW/Bellview product. **The gap is not the RFQ — it is that those two
  types were never placed with any other supplier, and the BoQ-vs-schedule discrepancy was never
  put to SMD.**
- **22/07 — the RFQ asked for the right things.** RAL 7016, triple throughout, windows U 1.1,
  doors U 1.2, **solar control glazing**, **obscure where required**, panic gear to Door E.02.
  BSW answered on colour, triple (by exception) and panic gear, and were **silent on solar
  control and obscure**. Third time this month after Filwood and Georgie's.
- **28/07 — mastic and EPDM go into the sum** and the "optional extra" line comes out of the
  proposal (Adam's ruling on Princess Beatrice REQ-6). GBP 4,776.56.
- **27/07 — new check rule earned:** `check_supplier_covers_quantity`, fixture
  `_test-brocks-hill.json`. Reconciling a quote total is not reconciling its quantities.
- **29/07 — second rule earned:** `check_rfq_answered`. Every line of the RFQ is ticked off
  against the return; a supplier who does not mention an item has not priced it. Fires here on
  solar control, obscure glazing and the window U-value. Same fixture.

## What Adam said

- **29/07 12:19, to Gintare** (estimating@ copied): "I have noticed there's extra doors on the
  schedule than on their own BoQ. Did you query this with the client? … There's no triple glazing
  on the smart wall, but spec shows triple throughout. We need to clarify this with the client…
  Did this get queried with them at all? Have we allowed for solar control glass where required?"
  All three were already reported to him 27–28/07. He was asking whether they had been **actioned**.
- **29/07 13:18, Gintare to Adam**, inline against question 1 only: "We priced it as per BoQ."
  Questions 2 and 3 unanswered. "What we priced" is not "what we queried".
- **28/07 20:30, REQ-2:** "I will call the client and see what they want to do. Can you email me a
  take-off in the meantime please. Needs to be asap." Take-off delivered same evening —
  `outputs/Brocks Hill Phase 2 - Take-Off.xlsx`, 49 external elements, 40 quoted, 9 not.
- **28/07 21:17, REQ-13:** "please email me this." Delivered inside the take-off, sheet 2.
- **28/07 21:23, REQ-14:** "I have addressed this above." Duplicate of REQ-2; folded.

## Working files

- Audit: `outputs/Brocks Hill Phase 2 - Quote Check (schedules vs tender).xlsx` · `scripts/brocks_hill_quote_check.py`
- Take-off: `outputs/Brocks Hill Phase 2 - Take-Off.xlsx` · `scripts/brocks_hill_takeoff.py`
- Drafted, unsent: `outputs/brocks-hill-rfi-to-smd.txt`, `outputs/brocks-hill-bsw-chase.txt`
- Checks: `data/job-checks/brocks-hill-phase-2.json` (6 FAILED)
- Tender pack, 171 files: `test-results/brocks-hill-check/tender/`

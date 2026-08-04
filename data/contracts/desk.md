# The desk

Anything that does not belong to one won job. Contracts get their own file.

Last worked: 2026-08-04.

---

## Where it stands

Four contracts open, none with a site date, GBP 279,000 live between them.
Two clients waiting on dates I cannot invent. Four questions on the board.

| Contract | Client | Value | State |
|---|---|---|---|
| `pride-rubery-library-remedial` | Pride Developments | split, figure on Mary's quote | Frames ordered 03/08, unacknowledged. Client waiting on an install date |
| `stoke-park-school` | Borras | GBP 105,000 | Frames and glass ordered. Technal submission live. No site date |
| `manor-lodge-school` | Borras | GBP 3,931.85 | PO signed. Borras want delivery + install dates, 04/08 |
| `towcester-vale-local-centre` | RRR Group | GBP 170,000 | Design stage, waiting on DWGs from A Plus. GBP 98,493.94 outstanding |

Open questions: **JOE-1** Rubery install date (promised, does not exist).
**JOE-2** Manor Lodge - is design closed, and what is AFS's lead time.
**JOE-3** no site date on Stoke Park or Towcester Vale. **JOE-4** two items
I cannot attribute to any job.

---

## The two I could not attribute

**Vetroseal order ack 732330, reference (JOE POTTER)**, 03/08, with a price.
Vetroseal put the job reference in those brackets - 065095 was (BACON), 065209
was (MHANUNEATON). There is no JOE POTTER in the commercial contracts export,
in the CRM, or anywhere in the mail corpus. Most likely a retail or domestic
job, which would put it outside the commercial board entirely. Not guessed at,
not filed. On JOE-4.

**Cranfield BACS remittance 2607284, supplier ID 1042067**, 04/08. Cranfield
have sixteen contracts with us and fourteen are at zero balance. The only two
carrying anything are 3419 (B121, GBP 1,632, fitted 14/07) and 3450 (B111 S5,
GBP 324, fitted 12/06). The attachment was not saved with the email so the
figure is unread. A payment landing is the end of my job on a contract - I
cannot close what I cannot identify. On JOE-4.

---

## Things learned this session, so they are not re-learned

- **The routing reason "no contract named" meant no contract existed.** All
  five threads in the first batch were won jobs with nothing on the board. The
  won-job record that settled it is
  `test-results/jacob-mail/commercial_contracts_export29072026.csv` - AdminBase
  contract number, value, contract date, date fitted and outstanding balance,
  207 rows. It answers "is this won?" faster than anything else here.
- **A lead key and a contract key are not the same thing.** `stoke-park` is the
  lead; `stoke-park-school` is the contract, linked by `lead_key`.
- **`crm_contract.board()` returns the contract under `d["contract"]`**, not at
  the top level. `d.get("title")` is always None and means nothing.
- **`open_contract` with no site date lays out zero steps.** That is correct
  behaviour, not a failure - steps count backwards from the site date. Ticked
  steps can still be written individually with `done_at` and no `due`.
- **RRR Group have two jobs with bottom-hung AOV free-area questions** -
  Towcester Vale and Riverside House. Different jobs. Noted on both.

## Standing, from the manual

- I do not price. That is Mary's.
- I do not send email. There is no send path. I draft, a human sends.
- I do not invent a date. No site date means no dates on the twelve steps.
- Intent is not completion. "We will order it" ticks nothing.
